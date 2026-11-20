#!/usr/bin/env python3
"""Verify the Term 4 checkpoint: recompute every answer and check every multiple-choice letter.

Each value is recomputed by a route other than the hand formula where one exists:
- electronics by solving the large-signal pair, nodal (MNA) analysis of the small-signal circuits, sympy for the
  open-circuit time constants, root finding on loop gains and oscillator networks, eigenvalues of the LC tank and
  numerical integration of the class B waveforms;
- electromagnetics by a finite-difference Laplace solve and field-energy integrals for the coax, integration of
  the induced charge for the image force, field matching at interfaces, sampled standing waves, a many-section LC
  ladder for the bounce diagram, a finite-difference eigenvalue problem for the waveguide and the aperture route
  for the link budget;
- computer systems by synthetic traces and cycle-by-cycle counts, and by the Course 14 lab models (cache address
  split, Sv32 page-table walker, MESI protocol, SIMT warp executor, roofline).
For numerical multiple-choice questions, the option text is parsed from README.md, and the script checks that
the letter in solutions.md is the only option matching the computed value to its printed precision.
"""
from __future__ import annotations

import importlib.util
import math
import re
import struct
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal, expm, solve_banded
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import Verifier, parse_value  # noqa: E402

LABS = ROOT / "courses" / "14-computer-organization-and-architecture" / "labs"


def lab(name, sub):
    spec = importlib.util.spec_from_file_location(name, LABS / sub / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


cache_m, vm, mesi, simt, roof = (lab("cache", "14-09-lab"), lab("vm", "14-10-lab"), lab("mesi", "14-12-lab"),
                                 lab("simt", "14-13-lab"), lab("roofline", "14-15-lab"))

README, SOL = HERE / "README.md", HERE / "solutions.md"
v = Verifier.from_files("term-4", SOL)
k_B = 1.380649e-23
c0, eps0, mu0, eta0 = 2.998e8, 8.854e-12, 4 * math.pi * 1e-7, 376.7
ans: dict[int, float] = {}

# ================================================================= block 1 · Electronics II
k, ISS, RD, VTH = 2e-3, 200e-6, 20e3, 0.5


def pair(vid, vcm=1.5):
    """Drain currents of a square-law pair: solve for the common-source voltage so that i1 + i2 = I_SS."""
    i = lambda vg, vs: 0.5 * k * max(vg - vs - VTH, 0.0) ** 2
    vs = brentq(lambda vs: i(vcm + vid / 2, vs) + i(vcm - vid / 2, vs) - ISS, -5, vcm)
    return i(vcm + vid / 2, vs), i(vcm - vid / 2, vs)


h = 1e-5
ans[1] = (np.subtract(*pair(h)) - np.subtract(*pair(-h))) / (2 * h) * RD
lo, hi = 0.0, 1.0                     # bisection on "transistor 2 still conducts"
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if pair(mid)[1] > 0 else (lo, mid)
ans[2] = hi


def diffpair_out(vg1, vg2, gm=1e-3, rd=10e3, rss=100e3):
    """Small-signal pair, nodes (d1, d2, s); returns v_d1."""
    G = np.array([[1 / rd, 0, -gm], [0, 1 / rd, -gm], [0, 0, 1 / rss + 2 * gm]])
    b = np.array([-gm * vg1, -gm * vg2, gm * (vg1 + vg2)])
    return np.linalg.solve(G, b)[0]


Adm = abs(diffpair_out(0.5, -0.5))
Acm = abs(diffpair_out(1.0, 1.0))
v.assert_true("the single-ended differential gain is g_m R_D / 2 = 5", abs(Adm - 5) < 1e-9)
ans[3] = 20 * math.log10(Adm / Acm)

ro1 = ro2 = 50e3
gm2 = 2e-3
# unknowns (v_x, i_t) with a 1 V test source at the output: KCL at x, and the test current into the drain of M2
M = np.array([[1 / ro2 + gm2 + 1 / ro1, 0], [-(1 / ro2 + gm2), -1]])
vx, it = np.linalg.solve(M, [1 / ro2, -1 / ro2])
ans[4] = 1 / it / 1e6

gm5, Cgs5, Cgd5 = 5e-3, 50e-15, 10e-15
w5 = brentq(lambda w: gm5 / (w * (Cgs5 + Cgd5)) - 1, 1e9, 1e12)
ans[5] = w5 / (2 * math.pi) / 1e9
w5x = brentq(lambda w: abs((gm5 - 1j * w * Cgd5) / (1j * w * (Cgs5 + Cgd5))) - 1, 1e9, 1e12)
v.assert_true("including the feed-forward current through C_gd moves f_T by under 2%", abs(w5x / w5 - 1) < 0.02)

w6 = 2 * math.pi * 1e6
Yin = 1j * w6 * 40e-15 + 1j * w6 * 10e-15 * (1 - (-20))    # C_gd sees v_in - A v_in
ans[6] = Yin.imag / w6 / 1e-15

s = sp.symbols("s")
vg, vd = sp.symbols("v_g v_d")
RS, gm7, RL, Cgs, Cgd, CL = 10e3, 2e-3, 5e3, 100e-15, 20e-15, 200e-15
sol7 = sp.solve([(vg - 1) / RS + s * Cgs * vg + s * Cgd * (vg - vd),
                 vd / RL + s * CL * vd + s * Cgd * (vd - vg) + gm7 * vg], [vg, vd], dict=True)[0]
num7, den7 = sp.fraction(sp.together(sol7[vd]))
den7 = sp.Poly(sp.expand(den7), s)
c7 = [float(x) for x in den7.all_coeffs()[::-1]]
b1 = c7[1] / c7[0]
ans[7] = 1 / (2 * math.pi * b1) / 1e6
H7 = sp.lambdify(s, sol7[vd] / sol7[vd].subs(s, 0))
f7 = brentq(lambda f: abs(H7(2j * math.pi * f)) - 1 / math.sqrt(2), 1e6, 1e9)
v.assert_true("the exact -3 dB frequency lies above the OCTC estimate (real poles: OCTC is conservative)",
              f7 > ans[7] * 1e6)


def closed_loop(A, beta=0.01):
    y, _e = np.linalg.solve([[1, -A], [beta, 1]], [0, 1])     # y = A e, e = x - beta y, x = 1
    return y


ans[8] = closed_loop(1e4)
ans[9] = 100 * (1 - closed_loop(9e3) / closed_loop(1e4))
T10 = lambda f: 1e5 / ((1 + 1j * f / 10) * (1 + 1j * f / 1e6))
fc10 = brentq(lambda f: abs(T10(f)) - 1, 1e3, 1e8)
ans[10] = 180 + math.degrees(np.angle(T10(fc10)))
v.assert_true("the loop's phase at crossover is between -90 and -180 degrees (no wrap)", -180 < math.degrees(np.angle(T10(fc10))) < -90)


def two_stage(f, gm1=1e-3, Cc=2e-12, R1=1e6, C1=10e-15, gm2=0.1, R2=1e6, C2=1e-12):
    w = 2 * math.pi * f
    Y = np.array([[1 / R1 + 1j * w * (C1 + Cc), -1j * w * Cc],
                  [gm2 - 1j * w * Cc, 1 / R2 + 1j * w * (C2 + Cc)]])
    return np.linalg.solve(Y, [-gm1, 0])[1]


ans[11] = brentq(lambda f: abs(two_stage(f)) - 1, 1e6, 1e9) / 1e6
y12 = [0.0]
dt12, Cc12 = 1e-9, 2e-12
for _ in range(1000):                 # charge C_c with the whole tail current for 1 microsecond
    y12.append(y12[-1] + 100e-6 * dt12 / Cc12)
ans[12] = y12[-1] / 1.0                # volts in 1 us = V/us


def class_b(Vcc, Vop, RL=8.0, n=200000):
    th = (np.arange(n) + 0.5) * 2 * math.pi / n
    vo = Vop * np.sin(th)
    PL = np.mean(vo ** 2) / RL
    PS = Vcc * np.mean(np.abs(vo)) / RL      # each rail supplies its half-cycle
    return PL, PS


PL13, PS13 = class_b(12, 10)
ans[13] = 100 * PL13 / PS13
r14 = minimize_scalar(lambda a: -np.subtract(*class_b(15, a)[::-1]), bounds=(0, 15), method="bounded",
                      options={"xatol": 1e-9})
ans[14] = -r14.fun
v.assert_true("worst dissipation occurs at V_op = 2 V_CC / pi", abs(r14.x - 30 / math.pi) < 1e-3)

R15, C15 = 10e3, 10e-9


def wien(f):
    w = 2 * math.pi * f
    Zs = R15 + 1 / (1j * w * C15)
    Zp = 1 / (1 / R15 + 1j * w * C15)
    return Zp / (Zs + Zp)


f15 = brentq(lambda f: wien(f).imag, 100, 10e3)
v.assert_true("the Wien network's gain at zero phase is 1/3", abs(abs(wien(f15)) - 1 / 3) < 1e-9)
ans[15] = f15 / 1e3
L16, C1, C2 = 10e-6, 1e-9, 1e-9
A16 = np.array([[0, 0, 1 / C1], [0, 0, 1 / C2], [-1 / L16, -1 / L16, 0]])   # states v1, v2, i around the tank
ans[16] = max(np.linalg.eigvals(A16).imag) / (2 * math.pi) / 1e6
R17, B17 = 10e3, 1e6
C17 = 1 / (4 * R17 * B17)             # an RC whose noise bandwidth 1/(4RC) is 1 MHz has total noise kT/C
ans[17] = math.sqrt(k_B * 300 / C17) * 1e6
v.assert_true("integrating 4kTR over the band gives the same rms",
              abs(math.sqrt(quad(lambda f: 4 * k_B * 300 * R17, 0, B17)[0]) * 1e6 - ans[17]) < 1e-9)

# ================================================================= block 2 · Electromagnetics
a, b, er = 0.5e-3, 1.75e-3, 2.25
N = 20000
rho = np.linspace(a, b, N + 1)
rh = (rho[1:] + rho[:-1]) / 2         # flux-conservative finite differences for d/drho(rho dV/drho) = 0
main = np.zeros(N - 1)
main[:] = rh[:-1] + rh[1:]
off = -rh[1:-1]
ab = np.zeros((3, N - 1))
ab[0, 1:] = off
ab[1] = main
ab[2, :-1] = off
rhs = np.zeros(N - 1)
rhs[0] = rh[0] * 1.0                   # V(a) = 1 V, V(b) = 0
V = np.concatenate([[1.0], solve_banded((1, 1), ab, rhs), [0.0]])
flux = -2 * math.pi * eps0 * er * rh * np.diff(V) / np.diff(rho)
v.assert_true("the radial flux is the same at every radius (Gauss)", np.ptp(flux) / flux.mean() < 1e-9)
Cp = flux.mean()
ans[18] = Cp * 1e12
Wm = quad(lambda r: (mu0 / (2 * math.pi * r)) ** 2 / (2 * mu0) * 2 * math.pi * r, a, b)[0]   # I = 1 A
ans[19] = math.sqrt(2 * Wm / Cp)
q20, d20 = 1e-9, 0.01
sig = lambda r: -q20 * d20 / (2 * math.pi * (r * r + d20 * d20) ** 1.5)
Qind = quad(lambda r: sig(r) * 2 * math.pi * r, 0, np.inf, epsabs=0, epsrel=1e-12, limit=200)[0]
v.assert_true("the induced charge totals -q", abs(Qind / q20 + 1) < 1e-8)
F20 = quad(lambda r: q20 * sig(r) * 2 * math.pi * r * d20 / (4 * math.pi * eps0 * (r * r + d20 * d20) ** 1.5), 0, np.inf,
           epsabs=0, epsrel=1e-12, limit=200)[0]
v.assert_true("the force points toward the plane (attractive)", F20 < 0)
ans[20] = abs(F20) * 1e6
Nt, mur, ell, Acore, gap = 200, 2000, 0.20, 1e-4, 1e-3
Hc, Hg = np.linalg.solve([[ell, gap], [mur, -1]], [Nt * 1.0, 0])     # Ampere's loop; B continuous across the gap
Phi = mu0 * Hg * Acore
L21 = Nt * Phi / 1.0
W21 = 0.5 * mu0 * mur * Hc ** 2 * Acore * ell + 0.5 * mu0 * Hg ** 2 * Acore * gap
v.assert_true("the field energy gives the same inductance (2W/I^2)", abs(2 * W21 / L21 - 1) < 1e-12)
ans[21] = L21 * 1e3
w22 = 2 * math.pi * 100e6
g22 = np.sqrt(1j * w22 * mu0 * (5.8e7 + 1j * w22 * eps0))
ans[22] = 1 / g22.real * 1e6
t23 = np.linspace(0, 1, 100001)[:-1]
E23 = 10 * np.cos(2 * math.pi * t23)
ans[23] = np.mean(E23 * E23 / eta0)
eta_g = eta0 / 1.5
Er, Et = np.linalg.solve([[1, -1], [-1 / eta0, -1 / eta_g]], [-1, -1 / eta0])   # E and H continuity
v.assert_true("power balances at the interface", abs(Er ** 2 + Et ** 2 * eta0 / eta_g - 1) < 1e-12)
ans[24] = 100 * Er ** 2


def gamma_par(th, n1=1.0, n2=1.5):
    tt = math.asin(n1 * math.sin(th) / n2)
    e1, e2 = eta0 / n1, eta0 / n2
    return (e2 * math.cos(tt) - e1 * math.cos(th)) / (e2 * math.cos(tt) + e1 * math.cos(th))


ans[25] = math.degrees(brentq(gamma_par, math.radians(1), math.radians(89)))
lam = 1.0
th26 = np.linspace(0, math.pi, 200001)
Eth = lambda t: eta0 * (2 * math.pi / lam) * 1.0 * (lam / 20) * np.sin(t) / (4 * math.pi)   # r = 1 m, I = 1 A
P26 = 2 * math.pi * np.trapezoid(Eth(th26) ** 2 / (2 * eta0) * np.sin(th26), th26)
ans[26] = 2 * P26
Z0, ZL = 50.0, 75 + 25j
G27 = (ZL - Z0) / (ZL + Z0)
d27 = np.linspace(0, 0.5, 200001)
Vz = np.abs(np.exp(2j * math.pi * d27) + G27 * np.exp(-2j * math.pi * d27))
ans[27] = Vz.max() / Vz.min()
G_mag = (ans[27] - 1) / (ans[27] + 1)
ans[28] = -10 * math.log10(G_mag ** 2)


def zin_quarter(Z1, RL=100.0):
    bl = math.pi / 2
    Am, Bm, Cm, Dm = math.cos(bl), 1j * Z1 * math.sin(bl), 1j * math.sin(bl) / Z1, math.cos(bl)
    return (Am * RL + Bm) / (Cm * RL + Dm)


ans[29] = brentq(lambda z: zin_quarter(z).real - 50, 51, 99)

# question 30: a 400-section LC ladder for the line (Z0 = 50 ohm, one-way delay T = 1), stepped exactly with expm
Nsec, Zl, Td = 400, 50.0, 1.0
Ls, Cs = Zl * Td / Nsec, Td / (Zl * Nsec)
nst = 2 * Nsec                         # states: inductor currents i_1..i_N, then capacitor voltages v_1..v_N
Asys = np.zeros((nst, nst))
Bsys = np.zeros(nst)
for kk in range(Nsec):
    Asys[kk, Nsec + kk] = -1 / Ls                  # L di_k/dt = v_{k-1} - v_k
    if kk > 0:
        Asys[kk, Nsec + kk - 1] = 1 / Ls
    Asys[Nsec + kk, kk] = 1 / Cs                   # C dv_k/dt = i_k - i_{k+1}
    if kk < Nsec - 1:
        Asys[Nsec + kk, kk + 1] = -1 / Cs
Asys[0, 0] = -25.0 / Ls                            # source: L di_1/dt = Vs - Rs i_1 - v_1
Bsys[0] = 3.0 / Ls
dt30 = Td / 200
Phi30 = expm(Asys * dt30)
Gam30 = np.linalg.solve(Asys, (Phi30 - np.eye(nst)) @ Bsys)
x30 = np.zeros(nst)
vL = []
for _ in range(int(5 * Td / dt30)):
    x30 = Phi30 @ x30 + Gam30
    vL.append(x30[-1])
tt30 = (np.arange(len(vL)) + 1) * dt30
ans[30] = float(np.mean(np.array(vL)[(tt30 > 3.6) & (tt30 < 4.4)]))
v.assert_true("the ladder's first plateau (1T to 3T) sits at 2 v+ = 4 V within 0.5%",
              abs(np.mean(np.array(vL)[(tt30 > 1.6) & (tt30 < 2.4)]) / 4.0 - 1) < 5e-3)
vel = 0.66 * c0
ans[31] = brentq(lambda d: 2 * d / vel - 4.0e-9, 0, 10) * 100
ans[32] = brentq(lambda Z: (Z - 50) / (Z + 50) - 0.20, 50, 500)
a33, N33 = 22.86e-3, 4000
hh = a33 / N33
ev = eigh_tridiagonal(np.full(N33 - 1, 2 / hh ** 2), np.full(N33 - 2, -1 / hh ** 2), select="i", select_range=(0, 0))[0]
ans[33] = c0 * math.sqrt(ev[0]) / (2 * math.pi) / 1e9
lam34 = c0 / 2.4e9
S34 = 1.0 * 10 / (4 * math.pi * 100 ** 2)           # power density at the receiver
Ae34 = 10 * lam34 ** 2 / (4 * math.pi)              # effective aperture of the receiving antenna
ans[34] = 10 * math.log10(S34 * Ae34 / 1e-3)

# ================================================================= block 3 · Computer systems
mix = ["alu"] * 500 + ["ls"] * 300 + ["br"] * 200
cyc = {"alu": 1, "ls": 2, "br": 3}
ans[35] = sum(cyc[x] for x in mix) * (1e9 / len(mix)) / 2.0e9
tasks = [0.625] * 1440                              # the 900 parallel units, split evenly
core_t = [0.0] * 16
for t in tasks:
    core_t[core_t.index(min(core_t))] += t
ans[36] = 1000 / (100 + max(core_t))


def supply_energy(Vdd, R=1e3, C=1e-12):
    """Energy drawn from the supply while charging C through R from 0 to Vdd."""
    return quad(lambda t: Vdd * (Vdd / R) * math.exp(-t / (R * C)), 0, 60 * R * C)[0]


ans[37] = 100 * supply_energy(0.8) * 2.4e9 / (supply_energy(1.0) * 3.0e9)
stages = [300, 200, 250, 350, 200]
clock = max(stages) + 20
cycle, n_done = 0, 0
while n_done < 1000:                                # instruction i is in stage s during cycle i + s
    cycle += 1
    n_done = sum(1 for i in range(1000) if i + len(stages) <= cycle)
ans[38] = cycle * clock / 1000
prog = ["op"] * 100
for i in range(5, 55, 5):
    prog[i] = "lu"                                  # load followed by a dependent use: one bubble
for i in range(57, 87, 2):
    prog[i] = "tb"                                  # taken branch resolved in EX: two flushed slots
wb = []
for i, kind in enumerate(prog):
    issue = 1 if i == 0 else wb[-1] - 4 + 1 + (1 if prog[i - 1] == "lu" else 0) + (2 if prog[i - 1] == "tb" else 0)
    wb.append(issue + 4)
v.assert_true("the hazard positions give 10 load-use stalls and 15 taken branches",
              prog.count("lu") == 10 and prog.count("tb") == 15)
ans[39] = wb[-1] / 100
n40, cycles40, nbr = 100000, 0, 0
for i in range(n40):
    cycles40 += 1
    if i % 5 == 0:
        nbr += 1
        if nbr % 20 == 0:
            cycles40 += 15
ans[40] = cycles40 / n40
c41 = cache_m.Cache(32 * 1024, 64, 4)
ans[41] = c41.split(0xFFFF_FFFF)[0].bit_length()
lat = []
l1m = 0
for i in range(100000):
    if i % 20 == 19:
        l1m += 1
        lat.append(1 + 10 + (200 if l1m % 5 == 0 else 0))
    else:
        lat.append(1)
ans[42] = float(np.mean(lat))
mem = vm.Memory()
pt = vm.PageTable(mem)
pt.map(0x1234_5678, 0x0ABCD)
pa43, reads43, lvl43 = pt.walk(0x1234_5678)
v.assert_true("the walk reads two PTEs and ends at a level-0 leaf", reads43 == 2 and lvl43 == 0)
ans[43] = pa43


def alias_free(size, ways=8, block=64, page=4096):
    c = cache_m.Cache(size, block, ways)
    rng = np.random.default_rng(4)
    return all(c.split(int(x))[1:] == c.split(int(x) % page)[1:] for x in rng.integers(0, 2 ** 32, 2000))


ans[44] = max(sz for sz in (2 ** e for e in range(12, 21)) if alias_free(sz)) / 1024
ans[45] = float(Fraction(16 * 10 ** 9) * 16 * Fraction(128, 130) / 8) / 1e9
nodes = [(x, y) for x in range(8) for y in range(8)]
ans[46] = float(np.mean([abs(p[0] - q[0]) + abs(p[1] - q[1]) for p in nodes for q in nodes]))
ans[47] = struct.unpack(">I", struct.pack(">f", -6.25))[0]
sys48 = mesi.System(2).run([(0, 0x40, False), (0, 0x40, True), (1, 0x40, False), (1, 0x40, True)])
blk = 0x40 // 64
eff = simt.run_warp([("if", lambda i: i < 24, [("op", 10)], [("op", 20)])])
ans[49] = 100 * eff[1] / (32 * eff[0])
ans[50] = roof.attainable(100e12, 2.0e12, 10) / 1e12
v.assert_true("the kernel sits left of the ridge (memory-bound)", 10 < roof.ridge(100e12, 2.0e12))

for qn, value in sorted(ans.items()):
    v.check(f"T4.{qn:02d}", value)

# ================================================================= multiple-choice letters
readme = README.read_text(encoding="utf-8")
sol_text = SOL.read_text(encoding="utf-8")
letters = {int(n): l_ for n, l_ in re.findall(r"^\*\*(\d+)\. Answer: \(([A-D])\)", sol_text, re.M)}
options = {}
for block in re.split(r"^\*\*(?=\d+\.\*\*)", readme, flags=re.M)[1:]:
    n = int(block.split(".", 1)[0])
    opt_line = next((ln for ln in block.splitlines() if ln.startswith("(A)")), None)
    if opt_line:
        options[n] = dict(re.findall(r"\(([A-D])\)\s*([^·]+?)\s*(?:·|$)", opt_line))


def option_value(text):
    try:
        pub = parse_value(text.split()[0].rstrip(";,°%"))
    except Exception:  # noqa: BLE001 - non-numeric option text
        return None
    part = pub.parts[0]
    return part.value, part.halfulp


numeric_mc = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 50]
for qn in numeric_mc:
    target = ans[qn]
    scored = sorted((abs(p[0] - target), letter, p[1]) for letter, text in options[qn].items()
                    if (p := option_value(text)) is not None)
    (best_err, best_l, tol), second_err = scored[0], scored[1][0]
    v.assert_true(f"Q{qn}: answer letter {letters.get(qn)} is the option closest to the computed value, within its precision",
                  best_l == letters.get(qn) and best_err <= tol * (1 + 1e-9) and second_err > best_err,
                  f"closest {best_l} (error {best_err:.3g}), options {options[qn]}")
# question 48: the MESI model must give 3 bus transactions, core 0 Invalid and core 1 Modified (option B only)
fin = (sys48.bus, sys48.state[0].get(blk, "I"), sys48.state[1].get(blk, "I"))
v.assert_true("Q48: three bus transactions (BusRd, BusRd with flush, BusUpgr); core 0 I, core 1 M",
              fin == (3, "I", "M") and sys48.stats["silent_upgrades"] == 1, str(fin))
opt48 = {l_: re.match(r"(\d+); core 0 (\w+), core 1 (\w+)", t).groups() for l_, t in options[48].items()}
match48 = [l_ for l_, (nb, s0, s1) in opt48.items() if (int(nb), s0[0], s1[0]) == fin]
v.assert_true("Q48: exactly one option matches the model, and it is the keyed letter",
              match48 == [letters.get(48)], str(match48))
v.assert_true("every multiple-choice question has an answer letter", set(options) <= set(letters))
v.assert_true("50 questions, numbered 1 to 50",
              sorted(int(n) for n in re.findall(r"^\*\*(\d+)\.\*\*", readme, re.M)) == list(range(1, 51)))

sys.exit(v.finish())
