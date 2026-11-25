#!/usr/bin/env python3
"""Verify every number in chapter 24-03 (SerDes architecture and equalization), its problems and its lab.

Independent routes (the lab module serdes.py uses closed forms and a linear solve for the FFE):
- FFE taps by root-finding (fsolve) on the zero-forcing equations, then explicit convolution;
- the CTLE by nodal analysis of the small-signal half-circuit (a complex 2x2 solve per frequency);
- DFE error continuation by Gaussian quadrature over the noise;
- bang-bang detector gain by a numerical derivative of the exact average detector output;
- the second-order CDR transient by integrating its ODE (solve_ivp);
- powers, rates and break-even losses by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-03", ROOT / "chapters" / "24-03-serdes-architecture.md",
                        ROOT / "solutions" / "24-03-solutions.md", LAB / "README.md")
Q = stats.norm.sf
Qi = stats.norm.isf
PAM4_PEN = 20 * math.log10(3)


def conv(c, h):
    g = {}
    for j, cj in c.items():
        for k, hk in h.items():
            g[k + j] = g.get(k + j, 0.0) + cj * hk
    return g


def isi(g, skip=(0,)):
    return sum(abs(x) for k, x in g.items() if k not in skip)


def zf3(h):
    def eqs(c):
        cm, c0, c1 = c
        g = conv({-1: cm, 0: c0, 1: c1}, h)
        return [g.get(-1, 0.0), g.get(1, 0.0), abs(cm) + abs(c0) + abs(c1) - 1]
    sol = optimize.fsolve(eqs, [-0.05, 0.8, -0.15], xtol=1e-14)
    v.assert_true("FFE equations solved", max(abs(x) for x in eqs(sol)) < 1e-12)
    return dict(zip((-1, 0, 1), sol))


# ================================================================ chapter
baud = 106.25e9 / 2
ui = 1e12 / baud
v.check("Ex 24-03.1a", baud / 1e9)
v.check("Ex 24-03.1a1", ui)
v.check("Ex 24-03.1b", baud / 4 / 1e9)
v.check("Ex 24-03.1c", baud / 64 / 1e9)
v.check("Ex 24-03.1d", 106.25e9 / 256 / 1e6)
v.check("Ex 24-03.1e", ui / 90)
v.check("Ex 24-03.1f", 2 * ui / 90)


def cml(vpp, vdd):
    return vdd * vpp / 50


def sst_loop_power(vreg, vsupply):
    # source 50 ohm + 100 ohm termination + 50 ohm: current vreg/200 drawn from vsupply
    i = vreg / (50 + 100 + 50)
    vdiff = i * 100
    v.assert_true("SST differential swing equals supply", abs(2 * vdiff - vreg) < 1e-15)
    return vsupply * i


v.check("Ex 24-03.2a", 0.8 / 50 * 1e3)
v.check("Ex 24-03.2a1", cml(0.8, 1.0) * 1e3)
v.check("Ex 24-03.2b", sst_loop_power(0.8, 0.8) * 1e3)
v.check("Ex 24-03.2c0", 0.8 / 200 * 1e3)
v.check("Ex 24-03.2c", sst_loop_power(0.8, 1.0) * 1e3)
v.check("Ex 24-03.2d", cml(0.8, 1.0) / 106.25e9 * 1e12)
v.check("Ex 24-03.2d1", sst_loop_power(0.8, 1.0) / 106.25e9 * 1e12)
v.check("Txt 24-03.a", cml(0.8, 1.0) / sst_loop_power(0.8, 1.0))

# Ex 3: cursors as stated in the example
h = {-1: 0.02156, 0: 0.73402, 1: 0.21088, 2: 0.02967, 3: 0.00345, 4: 0.00037}
c = zf3(h)
v.check("Ex 24-03.3a", c[-1])
v.check("Ex 24-03.3a1", c[0])
v.check("Ex 24-03.3a2", c[1])
g = conv(c, h)
v.check("Ex 24-03.3b", g[0])
v.check("Ex 24-03.3c0", g[2])
v.check("Ex 24-03.3c00", g[3])
r = isi(g)
v.check("Ex 24-03.3c", r)
e_ffe = g[0] - r
v.check("Ex 24-03.3c1", e_ffe)
v.check("Ex 24-03.3c2", g[0] / 3 - r)
v.check("Ex 24-03.3c3", h[0] - isi(h))
v.check("Ex 24-03.3c4", h[0] / 3 - isi(h))
v.check("Ex 24-03.3b1", h[0])
v.check("Ex 24-03.3d0", sum(c.values()))
v.check("Ex 24-03.3d", -20 * math.log10(sum(c.values())))
rd = isi(h, skip=(0, 1, 2))
v.check("Ex 24-03.3e0", rd)
v.check("Ex 24-03.3e", h[0] - rd)
v.check("Ex 24-03.3e1", h[0] / 3 - rd)
v.check("Ex 24-03.3f", 100 * (e_ffe / (h[0] - isi(h)) - 1))


def ctle_nodal(f, gm, rd, rs, cs, cl):
    """Half-circuit: node s (RS/2 || 2CS to ground), node out (RD || CL); VCCS gm(vin - vs) from out to s."""
    w = 2 * math.pi * f
    ys = 1 / (rs / 2) + 1j * w * 2 * cs
    yo = 1 / rd + 1j * w * cl
    # KCL at s: ys*vs - gm*(1 - vs) = 0 ; KCL at out: yo*vo + gm*(1 - vs) = 0  (vin = 1)
    a = np.array([[ys + gm, 0], [-gm, yo]], dtype=complex)
    b = np.array([gm, -gm], dtype=complex)
    vs, vo = np.linalg.solve(a, b)
    return abs(vo)


gm, RD, RS, CL = 20e-3, 200.0, 400.0, 40e-15
CS = 1 / (2 * math.pi * RS * 2e9)
v.check("Ex 24-03.4a", CS * 1e15)
g_dc = ctle_nodal(1.0, gm, RD, RS, CS, CL)
g_hf_ideal = ctle_nodal(1e15, gm, RD, RS, CS, 0.0)
v.check("Ex 24-03.4b", g_dc)
v.check("Ex 24-03.4b1", 20 * math.log10(g_dc))
v.check("Ex 24-03.4b2", g_hf_ideal)
v.check("Ex 24-03.4b3", 20 * math.log10(g_hf_ideal))
pk_ideal = 20 * math.log10(g_hf_ideal / g_dc)
v.check("Ex 24-03.4c", pk_ideal)
v.check("Ex 24-03.4g1", pk_ideal)
# first pole: root of the nodal determinant's source factor (ys + gm), ys = 2/RS + s*2CS
s_pole = np.roots([2 * CS, 2 / RS + gm])[0]
fp1 = -s_pole.real / (2 * math.pi)
v.check("Ex 24-03.4d", fp1 / 1e9)
v.check("Ex 24-03.4d1", 1 / (2 * math.pi * RD * CL) / 1e9)
res = optimize.minimize_scalar(lambda lf: -ctle_nodal(10 ** lf, gm, RD, RS, CS, CL), bounds=(9.5, 10.8),
                               method="bounded", options={"xatol": 1e-10})
fpk, gpk = 10 ** res.x, -res.fun
v.check("Ex 24-03.4e", gpk)
v.check("Ex 24-03.4e1", 20 * math.log10(gpk))
v.check("Ex 24-03.4e2", fpk / 1e9)
boost = 20 * math.log10(gpk / g_dc)
v.check("Ex 24-03.4e3", boost)
v.check("Txt 24-03.g", boost)
g16 = ctle_nodal(16e9, gm, RD, RS, CS, CL)
v.check("Ex 24-03.4f0", g16)
v.check("Ex 24-03.4f", 20 * math.log10(g16 / g_dc))
v.check("Ex 24-03.4g", pk_ideal - boost)

ui53 = 1e12 / 53.125e9
v.check("Ex 24-03.5a", 8 + 7 + 5)
v.check("Ex 24-03.5a1", ui53)
v.check("Ex 24-03.5b", 8 + 4 + 5)
v.check("Ex 24-03.5b1", ui53 - 17)
v.check("Ex 24-03.5c", 2 * 1)
v.check("Ex 24-03.5c1", 4 * 3)
v.check("Txt 24-03.e", ui53)


def p_cont(h0, h1, sigma):
    """P(error | previous error) by quadrature: the residual 2 h1 a_{n-1} helps or hurts with probability 1/2."""
    tot = 0.0
    for sgn in (+1, -1):
        margin = h0 - sgn * 2 * h1
        val, _ = integrate.quad(lambda x: stats.norm.pdf(x, 0, sigma), margin, np.inf, epsabs=1e-15)
        tot += 0.5 * val
    return tot


s6 = 1 / Qi(1e-6)
v.check("Ex 24-03.6a", s6)
pa, pb = p_cont(1, 0.5, s6), p_cont(1, 0.25, s6)
v.check("Ex 24-03.6b", pa)
v.check("Ex 24-03.6b1", pb)
v.check("Ex 24-03.6c", 1 / (1 - pa))
v.check("Ex 24-03.6c1", 1 / (1 - pb))

drift = 100e-6 * 53.125e9
v.check("Ex 24-03.7a", drift)
v.check("Ex 24-03.7b", drift / (2 * math.pi * 4e6))
sig = 0.02
dphi = 1e-6
kbb = ((1 - 2 * Q(dphi / sig)) - (1 - 2 * Q(-dphi / sig))) / (2 * dphi)
v.check("Ex 24-03.7c", kbb)
v.check("Txt 24-03.b", kbb * sig)
G = 2 ** -14 * 0.5 * kbb
v.check("Ex 24-03.7d0", G)
fc_bb = G * 53.125e9 / (2 * math.pi)
v.check("Ex 24-03.7d", fc_bb / 1e6)
v.check("Ex 24-03.7e0", 0.5 * 2 ** -14)
v.check("Ex 24-03.7e", 0.5 * 2 ** -14 * 1e6)
v.check("Ex 24-03.7f", drift / (2 * math.pi * fc_bb))

v.check("Ex 24-03.8a", 224e9 * 3e-12)
v.check("Ex 24-03.8b", 4.1 / 1.89)
v.check("Ex 24-03.8c", 51.2e12 * 3e-12)
v.check("Ex 24-03.8c1", 51.2e12 * 4.5e-12)
v.check("Ex 24-03.8d", 112.5e9 * 4.5e-12)
v.check("Ex 24-03.8d1", 212.5e9 * 2.05e-12)
v.check("Ex 24-03.8d2", 212.5e9 * 2.05e-12 * 4.1 / 1.89)
v.check("Ex 24-03.8e", 51.2e12 * 0.1e-12)


def break_even(alpha):
    f = 26.5625e9  # any frequency: only the ratio of losses at f and 2f matters
    loss_ratio_extra = alpha * (math.sqrt(2 * f / f) - 1) + (1 - alpha) * (2 * f / f - 1)
    return PAM4_PEN / loss_ratio_extra


v.check("Txt 24-03.c", break_even(0.0))
v.check("Txt 24-03.d", break_even(1.0))
v.check("Txt 24-03.f", 1e-12 * 100e9 * 1e3)

# ================================================================ solutions
b1 = 64e9
v.check("24-03.1a", b1 / 1e9)
v.check("24-03.1a1", 1e12 / b1)
v.check("24-03.1b", b1 / 4 / 1e9)
v.check("24-03.1c", 1e12 / b1 / 90)
v.check("24-03.1d", b1 / 64 / 1e9)

v.check("24-03.2a0", 1.0 / 50 * 1e3)
v.check("24-03.2a", cml(1.0, 1.2) * 1e3)
v.check("24-03.2b0", 1.0 / 200 * 1e3)
v.check("24-03.2b", sst_loop_power(1.0, 1.2) * 1e3)
v.check("24-03.2c", sst_loop_power(1.0, 1.0) * 1e3)
v.check("24-03.2d", cml(1.0, 1.2) / sst_loop_power(1.0, 1.2))

a2 = math.exp(-2)
h3 = {k: (1 - a2) * a2 ** k for k in range(0, 60)}
c3 = optimize.brentq(lambda c0: c0 + c0 * a2 - 1, 0.1, 1.0)
g3 = conv({0: c3, 1: -c3 * a2}, h3)
v.assert_true("P3 all post-cursors cancel", max(abs(g3[k]) for k in range(1, 59)) < 1e-15)
v.check("24-03.3b", c3)
v.check("24-03.3b1", -c3 * a2)
v.check("24-03.3c", g3[0])
v.assert_true("P3 main cursor is tanh 1", abs(g3[0] - math.tanh(1)) < 1e-14)
v.check("24-03.3d", -20 * math.log10(c3 - c3 * a2))
v.check("24-03.3e", g3[0] / 3)
v.check("24-03.3e0", h3[0] - isi(h3))
v.check("24-03.3e1", h3[0] / 3 - isi(h3))

h4 = {-1: 0.10, 0: 0.60, 1: 0.25, 2: 0.05}
c4 = zf3(h4)
g4 = conv(c4, h4)
v.check("24-03.4a", c4[-1])
v.check("24-03.4a1", c4[0])
v.check("24-03.4a2", c4[1])
v.check("24-03.4a3", g4[0])
v.check("24-03.4a4", g4[-2])
v.check("24-03.4a5", g4[2])
v.check("24-03.4a6", g4[3])
v.check("24-03.4a7", isi(g4))
v.check("24-03.4a8", g4[0] - isi(g4))
v.check("24-03.4a9", h4[0] - isi(h4))
v.check("24-03.4a10", isi(h4))
c0b = optimize.brentq(lambda c0: c0 + c0 * h4[-1] / h4[0] - 1, 0.1, 1.0)
cmb = -c0b * h4[-1] / h4[0]
g4b = conv({-1: cmb, 0: c0b}, h4)
v.check("24-03.4b", c0b)
v.check("24-03.4b1", cmb)
v.check("24-03.4b2", g4b[0])
v.check("24-03.4b3", g4b[-2])
v.check("24-03.4b4", g4b[0] - sum(abs(x) for k, x in g4b.items() if k < 0))

ratio = 10 ** (12 / 20)
gm5, RD5, CL5 = 25e-3, 160.0, 30e-15
RS5 = 2 * (ratio - 1) / gm5
CS5 = 1 / (2 * math.pi * RS5 * 1.5e9)
v.check("24-03.5a0", ratio)
v.check("24-03.5a1", ratio - 1)
v.check("24-03.5a", RS5)
v.check("24-03.5a2", CS5 * 1e15)
v.check("24-03.5b", ratio * 1.5)
v.check("24-03.5b1", 1 / (2 * math.pi * RD5 * CL5) / 1e9)
dc5 = ctle_nodal(1.0, gm5, RD5, RS5, CS5, CL5)
v.check("24-03.5c", dc5)
g5 = ctle_nodal(13.28125e9, gm5, RD5, RS5, CS5, CL5)
v.check("24-03.5d", g5)
v.check("24-03.5d1", 20 * math.log10(g5 / dc5))
v.check("24-03.5d2", 13.28 / (ratio * 1.5))


def h6(f):
    ch = 1 / (1 + 1j * f / 5e9)
    ct = 0.2 * (1 + 1j * f / 5e9) / ((1 + 1j * f / 25e9) * (1 + 1j * f / 40e9))
    return abs(ch * ct)


v.check("24-03.6b", 20 * math.log10(h6(1.0)))
bw6 = optimize.brentq(lambda f: h6(f) - h6(1.0) / math.sqrt(2), 1e9, 1e11)
v.check("24-03.6c", bw6 / 1e9)
v.check("24-03.6c1", bw6 / 5e9)
v.check("24-03.6d", -20 * math.log10(h6(1.0)))

ui64 = 1e12 / 64e9
v.check("24-03.7a0", ui64)
v.check("24-03.7a", 7 + 6 + 4)
v.check("24-03.7b", 7 + 3 + 4)
v.check("24-03.7b1", ui64 - 14)
v.check("24-03.7c0", 4 ** 2)
v.check("24-03.7c", 3 * 4 ** 2)
v.assert_true("P7 direct loop fails, unrolled closes", 17 > ui64 > 14)

q5 = Qi(1e-5)
s8 = 1 / q5
p8 = p_cont(1, 0.4, s8)
v.check("24-03.8a0", q5)
v.check("24-03.8a", s8)
v.check("24-03.8b", p8)
v.check("24-03.8c", 1 / (1 - p8))
v.check("24-03.8d", 1e-5 / (1 - p8))
v.check("24-03.8e", 100 * p8 / (1 - p8))

mu = 2 ** -8
n9 = 0.21088 / mu
v.check("24-03.9a0", n9)
v.check("24-03.9a", math.ceil(n9))
v.check("24-03.9b", math.ceil(n9) * 64 * ui53 / 1e3)
v.check("24-03.9c0", mu)
v.check("24-03.9c", 100 * mu / 0.73402)

for sj, a, b in ((0.01, "10a", "10a1"), (0.04, "10b", "10b1")):
    k = ((1 - 2 * Q(dphi / sj)) - (1 - 2 * Q(-dphi / sj))) / (2 * dphi)
    v.check(f"24-03.{a}", k)
    v.check(f"24-03.{b}", 2 ** -13 * 0.5 * k * 64e9 / (2 * math.pi) / 1e6)
v.check("24-03.10c0", 0.5 * 2 ** -13)
v.check("24-03.10c", 0.5 * 2 ** -13 * 1e6)

wn, zeta = 2 * math.pi * 2e6, 1 / math.sqrt(2)
dw = 100e-6 * 53.125e9


def loop(t, y):
    # e'' + 2 zeta wn e' + wn^2 e = 0 for t > 0 with e(0) = 0, e'(0) = dw (ramp input of slope dw)
    e, de = y
    return [de, -2 * zeta * wn * de - wn ** 2 * e]


sol = integrate.solve_ivp(loop, (0, 2e-6), [0.0, dw], max_step=1e-10, rtol=1e-11, atol=1e-14, dense_output=True)
tt = np.linspace(0, 2e-6, 400001)
ee = sol.sol(tt)[0]
i = int(np.argmax(ee))
tpk = optimize.minimize_scalar(lambda t: -sol.sol(t)[0], bounds=(tt[i - 5], tt[i + 5]), method="bounded",
                               options={"xatol": 1e-15}).x
v.check("24-03.11a", abs(ee[-1]))
v.check("24-03.11b0", wn * math.sqrt(1 - zeta ** 2))
v.check("24-03.11b", tpk * 1e9)
v.check("24-03.11b1", dw)
v.check("24-03.11b2", sol.sol(tpk)[0])
v.check("24-03.11c", dw / (2 * math.pi * 2e6))

v.check("24-03.12a", 72 * 224e9 * 3e-12)
v.check("24-03.12b", 72 * 224e9 * 1.11e-12)
v.check("24-03.12c", 72 * 224e9 * (3 - 1.11) * 1e-12)

k13 = 0.5 * (math.sqrt(2) - 1) + 0.5
v.check("24-03.13a0", k13)
v.check("24-03.13a", break_even(0.5))
v.check("24-03.13b", 18 * k13)
v.check("24-03.13c", 18 * k13 - PAM4_PEN)

sig14 = 8.0
for e, a0, a1, a in ((0.520, "14a0", "14a1", "14a"), (0.709, "14a2", "14a3", "14a4")):
    mv = e * 400
    v.check(f"24-03.{a0}", mv)
    v.check(f"24-03.{a1}", mv / 2 / sig14)
    v.check(f"24-03.{a}", Q(mv / 2 / sig14))
v.check("24-03.14a00", 0.520 * 400 / 2)
for e, keys in ((0.155, ("14b0", "14b1", "14b", "14b2")), (0.219, ("14b3", "14b4", "14b5", "14b6"))):
    mv = e * 400
    x = mv / 2 / sig14
    v.check(f"24-03.{keys[0]}", mv)
    v.check(f"24-03.{keys[1]}", x)
    v.check(f"24-03.{keys[2]}", 1.5 * Q(x))
    v.check(f"24-03.{keys[3]}", 0.75 * Q(x))
v.check("24-03.14b00", 0.155 * 400 / 2)
v.assert_true("P14 only the DFE PAM4 option meets 1e-6", 0.75 * Q(0.155 * 400 / 16) > 1e-6 > 0.75 * Q(0.219 * 400 / 16))

# ================================================================ lab
v.check("Lab 24-03.a", g_dc)
v.check("Lab 24-03.b", gpk)
v.check("Lab 24-03.c", fpk / 1e9)
v.check("Lab 24-03.d", g16)
v.check("Lab 24-03.e", pk_ideal)
v.check("Lab 24-03.f", e_ffe)
v.check("Lab 24-03.g", h[0] - rd)
v.check("Lab 24-03.h", 1 / Qi(1e-3))
v.check("Lab 24-03.i", p_cont(1, 0.5, 1 / Qi(1e-3)))
v.check("Lab 24-03.j", h[1])
v.check("Lab 24-03.k", h[2])
v.check("Lab 24-03.l", h[0])
v.check("Lab 24-03.m", 0.5 * 2 ** -14 * 1e6)
v.check("Lab 24-03.n", 100e-6)

# ---------------------------------------------------------------- Problems 24-03.15 and 24-03.16
g15, rd15, rs15, cs15, cl15 = 25e-3, 250.0, 320.0, 250e-15, 30e-15
num = np.array([rs15 * cs15, 1.0]) * g15 * rd15
den = np.polymul([rs15 * cs15, 1 + g15 * rs15 / 2], [rd15 * cl15, 1.0])
v.check("24-03.15b", abs(np.roots([rs15 * cs15, 1.0])[0]) / (2 * math.pi) / 1e9)
poles = sorted(abs(np.roots(den)) / (2 * math.pi))
v.check("24-03.15b1", poles[0] / 1e9)
v.check("24-03.15b2", poles[1] / 1e9)
hmag = lambda f: abs(np.polyval(num, 2j * math.pi * f) / np.polyval(den, 2j * math.pi * f))  # noqa: E731
v.check("24-03.15b3", hmag(1.0))
v.check("24-03.15b4", g15 * rd15)
res15 = optimize.minimize_scalar(lambda lf: -hmag(10 ** lf), bounds=(8, 12), method="bounded",
                                 options={"xatol": 1e-10})
v.check("24-03.15c", hmag(10 ** res15.x))
v.check("24-03.15c1", 10 ** res15.x / 1e9)
v.check("24-03.15c2", 20 * math.log10(hmag(10 ** res15.x) / hmag(1.0)))
v.check("24-03.15c3", 20 * math.log10(g15 * rd15 / hmag(1.0)) - 20 * math.log10(hmag(10 ** res15.x) / hmag(1.0)))
from scipy.stats import norm as _n  # noqa: E402
mean_sgn = lambda ph: integrate.quad(lambda x: np.sign(ph + x) * _n.pdf(x), -12, 12, points=[-ph])[0]  # noqa: E731
v.check("24-03.16b", math.sqrt(2 / math.pi) / 0.02)
for key, r in (("", 0.5), ("3", 1.0)):
    exact = mean_sgn(r)
    lin = math.sqrt(2 / math.pi) * r
    if r == 0.5:
        v.check("24-03.16c", exact)
        v.check("24-03.16c1", lin)
        v.check("24-03.16c2", 100 * (lin / exact - 1))
    else:
        v.check("24-03.16c3", exact)
        v.check("24-03.16c4", lin)
        v.check("24-03.16c5", 100 * (lin / exact - 1))

sys.exit(v.finish())
