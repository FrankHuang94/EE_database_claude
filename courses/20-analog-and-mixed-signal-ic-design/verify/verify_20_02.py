#!/usr/bin/env python3
"""Verify every number in chapter 20-02 (two-stage op-amp design), its problems and its lab.

Independent routes:
- devices: the drain current is computed from V_GS by solving 2q + ln q = V_P/V_T, g_m by a central finite difference,
  operating points at a target g_m/I_D by root-finding on V_GS (as in verify_20_01), not by the lab's closed forms;
- saturation voltages by root-finding on V_DS in the forward-reverse charge model;
- circuits: transfer functions are evaluated by solving the nodal matrix Y(s) v = b numerically at each frequency, and
  poles are the roots of det Y(s) expanded with sympy; margins come from dense frequency grids with unwrapped phase;
- the second-stage g_m6 is found by root-finding on the p2 expression rather than by its closed-form inversion;
- settling: step responses from scipy.signal, slewing from an ODE simulation (solve_ivp), CMFB by iterating the
  charge-sharing recursion;
- symbolic identities (the Miller coefficients, indirect-compensation approximations, the nested-Miller Butterworth
  match, the PSRR expression) are checked with sympy;
- the lab module (opamp.py) is asserted to agree with these results; ngspice confirms the netlists (run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import signal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import opamp as lab  # noqa: E402

v = Verifier.from_files("20-02", ROOT / "chapters" / "20-02-two-stage-op-amp-design.md",
                        ROOT / "solutions" / "20-02-solutions.md", LAB / "README.md")

KB, QE = 1.380649e-23, 1.602176634e-19
COX, N, VTH, VAL = 8.6e-3, 1.3, 0.45, 8e6
MUN, MUP, VSN, VSP = 350e-4, 100e-4, 8e4, 6e4
U, PF, FF = 1e-6, 1e-12, 1e-15
T = 300.0
VT = KB * T / QE
KT = KB * T
GAMMA = 2 / 3


class Dev:
    """Independent implementation of the 20-01 charge-based model (per device)."""

    def __init__(self, w, length, mu=MUN, vsat=VSN, vel_sat=True):
        self.w, self.l, self.mu = w, length, mu
        self.ispec = 2 * N * mu * COX * (w / length) * VT ** 2
        self.lam = mu * VT / (vsat * length) if vel_sat else 0.0

    @staticmethod
    def q_of_vp(vp):
        return brentq(lambda q: 2 * q + math.log(q) - vp / VT, 1e-40, 1e7, xtol=1e-40, rtol=1e-15)

    def q_of_vgs(self, vgs):
        return self.q_of_vp((vgs - VTH) / N)

    def i_d(self, vgs):
        q = self.q_of_vgs(vgs)
        return self.ispec * (q * q + q) / (1 + self.lam * q)

    def g_m(self, vgs, h=1e-6):
        return (self.i_d(vgs + h) - self.i_d(vgs - h)) / (2 * h)

    def gmid(self, vgs):
        return self.g_m(vgs) / self.i_d(vgs)

    def vgs_for_gmid(self, target):
        return brentq(lambda x: self.gmid(x) - target, VTH - 0.6, VTH + 2.5, xtol=1e-14)

    def f_t(self, vgs):
        return self.g_m(vgs) / (2 * math.pi * (2 / 3) * self.w * self.l * COX)


def vdsat(vgs):
    """V_DS at which the reverse charge term is 2 % of the forward term (long-channel forward-reverse model)."""
    vp = (vgs - VTH) / N
    qs = Dev.q_of_vp(vp)
    fwd = qs * qs + qs

    def ratio(vds):
        qd = Dev.q_of_vp(vp - vds)
        return (qd * qd + qd) / fwd - 0.02
    return brentq(ratio, 1e-6, vp + 40 * VT, xtol=1e-15)


def vdsat_q(q):
    """Same, starting from a source charge q."""
    vp = VT * (2 * q + math.log(q))
    return vdsat(vp * N + VTH)


# ---------------------------------------------------------------- circuit helpers
def solve_nodal(y_of_s, b, out, freqs):
    """Return H(j 2 pi f) for each frequency by solving the nodal matrix Y(s) v = b (batched over frequency)."""
    sv = 2j * math.pi * np.asarray(freqs, dtype=float)
    rows = y_of_s(sv)
    n = len(rows)
    y = np.empty(sv.shape + (n, n), dtype=complex)
    for i, row in enumerate(rows):
        for j, e in enumerate(row):
            y[..., i, j] = e
    rhs = np.broadcast_to(np.asarray(b, dtype=complex), sv.shape + (n,))[..., None]
    return np.linalg.solve(y, rhs)[..., out, 0]


def margins_of(h_func, f_lo=1e2, f_hi=3e10, n=40001):
    f = np.logspace(math.log10(f_lo), math.log10(f_hi), n)
    hv = h_func(f)
    if hv[0].real < 0:
        hv = -hv
    mag = np.abs(hv)
    ph = np.unwrap(np.angle(hv))
    ph = ph - ph[0] + np.angle(hv[0])
    lf = np.log10(f)
    i = int(np.where(mag < 1)[0][0])
    # refine the crossover by bisection on a fine local grid
    ff = np.logspace(lf[i - 1], lf[i], 2001)
    mm = np.abs(h_func(ff))
    k = int(np.where(mm < 1)[0][0])
    fc = 10 ** np.interp(0.0, [math.log10(mm[k]), math.log10(mm[k - 1])], [math.log10(ff[k]), math.log10(ff[k - 1])])
    pm = 180 + math.degrees(np.interp(math.log10(fc), lf, ph))
    out = {"fc": fc, "pm": pm, "f180": None, "gm": None}
    j = np.where(ph < -math.pi)[0]
    if len(j):
        j = int(j[0])
        lf180 = np.interp(-math.pi, [ph[j], ph[j - 1]], [lf[j], lf[j - 1]])
        out["f180"] = 10 ** lf180
        out["gm"] = -20 * math.log10(np.interp(lf180, lf, mag))
    return out


def miller_h(gm1, gm6, r1, r2, c1, cl, cc, rz):
    g1, g2 = 1 / r1, 1 / r2
    if rz == 0:
        def y(s):
            return [[g1 + s * (c1 + cc), -s * cc], [gm6 - s * cc, g2 + s * (cl + cc)]]
        b, out = np.array([-gm1, 0], dtype=complex), 1
    else:
        gz = 1 / rz

        def y(s):
            return [[g1 + s * c1 + gz, -gz, 0], [-gz, gz + s * cc, -s * cc], [gm6, -s * cc, g2 + s * (cl + cc)]]
        b, out = np.array([-gm1, 0, 0], dtype=complex), 2
    return lambda f: solve_nodal(y, b, out, np.atleast_1d(f))


def miller_poles(gm6, r1, r2, c1, cl, cc, rz):
    s = sp.symbols("s")
    g1, g2 = 1 / r1, 1 / r2
    if rz == 0:
        y = sp.Matrix([[g1 + s * (c1 + cc), -s * cc], [gm6 - s * cc, g2 + s * (cl + cc)]])
    else:
        gz = 1 / rz
        y = sp.Matrix([[g1 + s * c1 + gz, -gz, 0], [-gz, gz + s * cc, -s * cc], [gm6, -s * cc, g2 + s * (cl + cc)]])
    coeffs = [float(c) for c in sp.Poly(sp.expand(y.det()), s).all_coeffs()]
    return np.sort(np.abs(np.roots(coeffs)))


def indirect_y(gm6, gmc, r1, r2, rx, c1, cl, cc, cx):
    g1, g2, gx = 1 / r1, 1 / r2, 1 / rx

    def y(s):
        return [[g1 + s * c1, -gmc, 0], [0, gmc + gx + s * (cx + cc), -s * cc], [gm6, -s * cc, g2 + s * (cl + cc)]]
    return y


def nmc_y(gm2, gm3, r1, r2, r3, cn1, cn2, cl, cm1, cm2):
    g1, g2, g3 = 1 / r1, 1 / r2, 1 / r3

    def y(s):
        return [[g1 + s * (cn1 + cm1), 0, -s * cm1], [-gm2, g2 + s * (cn2 + cm2), -s * cm2],
                [-s * cm1, gm3 - s * cm2, g3 + s * (cl + cm1 + cm2)]]
    return y


def complex_pair(ymat_sym, s):
    coeffs = [float(c) for c in sp.Poly(sp.expand(ymat_sym.det()), s).all_coeffs()]
    r = np.roots(coeffs)
    pc = [x for x in r if abs(x.imag) > 1.0]
    return pc[0]


# ================================================================ section 3 identities (sympy)
s_, gm1_, gm6_, G1_, G2_, C1_, CL_, Cc_, Rz_ = sp.symbols("s g_m1 g_m6 G1 G2 C1 C_L C_c R_z", positive=True)
v1_, vx_, vo_ = sp.symbols("v1 vx vo")
sol = sp.solve([(G1_ + s_ * C1_) * v1_ + s_ * Cc_ * (v1_ - vo_) + gm1_,
                (G2_ + s_ * CL_) * vo_ + s_ * Cc_ * (vo_ - v1_) + gm6_ * v1_], [v1_, vo_], dict=True)[0]
a_s = sp.together(sol[vo_])
R1s, R2s = 1 / G1_, 1 / G2_
pub_a = gm1_ * gm6_ * R1s * R2s * (1 - s_ * Cc_ / gm6_) / (
    1 + s_ * (gm6_ * R1s * R2s * Cc_ + R1s * (C1_ + Cc_) + R2s * (CL_ + Cc_)) + s_ ** 2 * R1s * R2s * (
        C1_ * CL_ + Cc_ * (C1_ + CL_)))
v.assert_true("two-node Miller transfer function matches section 3.2", sp.simplify(a_s - pub_a) == 0, "")
sol3 = sp.solve([(G1_ + s_ * C1_) * v1_ + (v1_ - vx_) / Rz_ + gm1_,
                 (vx_ - v1_) / Rz_ + s_ * Cc_ * (vx_ - vo_),
                 (G2_ + s_ * CL_) * vo_ + s_ * Cc_ * (vo_ - vx_) + gm6_ * v1_], [v1_, vx_, vo_], dict=True)[0]
num3, den3 = sp.fraction(sp.together(sol3[vo_]))
den3 = sp.Poly(sp.expand(den3), s_)
c = den3.all_coeffs()[::-1]
a1p = gm6_ * R1s * R2s * Cc_ + R1s * (C1_ + Cc_) + R2s * (CL_ + Cc_) + Rz_ * Cc_
a2p = R1s * R2s * (C1_ * CL_ + Cc_ * (C1_ + CL_)) + Rz_ * Cc_ * (R1s * C1_ + R2s * CL_)
a3p = R1s * R2s * Rz_ * C1_ * CL_ * Cc_
v.assert_true("nulling-resistor coefficients a1, a2, a3 match section 3.4",
              all(sp.simplify(c[k] / c[0] - p) == 0 for k, p in ((1, a1p), (2, a2p), (3, a3p))), "")
zero_s = sp.solve(sp.expand(num3), s_)
v.assert_true("nulling-resistor zero at 1/[C_c(1/g_m6 - R_z)]",
              any(sp.simplify(z - 1 / (Cc_ * (1 / gm6_ - Rz_))) == 0 for z in zero_s), "")
# nested Miller: matching the Butterworth polynomial
w0 = sp.symbols("w0", positive=True)
gm2_, gm3_ = sp.symbols("g_m2 g_m3", positive=True)
cm1 = 4 * gm1_ * CL_ / gm3_
cm2 = 2 * gm2_ * CL_ / gm3_
w0v = gm3_ / (2 * CL_)
v.assert_true("NMC Butterworth match", all(sp.simplify(e) == 0 for e in (
    cm1 / gm1_ - 2 / w0v, cm1 * cm2 / (gm1_ * gm2_) - 2 / w0v ** 2, cm1 * cm2 * CL_ / (gm1_ * gm2_ * gm3_) - 1 / w0v ** 3)), "")
# PSRR expression (section 3.10)
G6_, G7_, vss_, vin_ = sp.symbols("G6 G7 v_ss v_in", positive=True)
solp = sp.solve([G1_ * (v1_ - vss_) + s_ * C1_ * (v1_ - vss_) + s_ * Cc_ * (v1_ - vo_) + gm1_ * vin_,
                 gm6_ * (v1_ - vss_) + G6_ * (vo_ - vss_) + G7_ * vo_ + s_ * CL_ * vo_ + s_ * Cc_ * (vo_ - v1_)],
                [v1_, vo_], dict=True)[0]
ass = sp.diff(solp[vo_], vss_)
adm = sp.diff(solp[vo_], vin_)
pub_inv = (G1_ * G6_ + s_ * (Cc_ * gm6_ + C1_ * G6_ + Cc_ * (G1_ + G6_)) + s_ ** 2 * C1_ * Cc_) / (gm1_ * (gm6_ - s_ * Cc_))
v.assert_true("PSRR- expression of section 3.10", sp.simplify(sp.Abs(1) * (ass / adm) + pub_inv) == 0
              or sp.simplify(ass / adm - pub_inv) == 0, "")

# ================================================================ the two-pole loop (section 3.2)
def two_pole(k):
    x = brentq(lambda x: x * math.sqrt(1 + (x / k) ** 2) - 1, 1e-6, 1.0)
    pm = 180 + math.degrees(np.angle(1 / (1j * x * (1 + 1j * x / k))))
    return x, pm


x15, pm15 = two_pole(1.5)
v.check("Txt 20-02.a", x15)
v.check("Txt 20-02.b", pm15)
v.check("Txt 20-02.c", two_pole(2.0)[1])
v.assert_true("k = 1.5 gives exactly 60 degrees", abs(pm15 - 60) < 1e-9 and abs(x15 - math.sqrt(3) / 2) < 1e-9, "")
v.check("Txt 20-02.at", math.degrees(math.atan(0.1)))

# ================================================================ Example 20-02.1
WU = 2 * math.pi * 50e6
SR = 30e6
v.check("Txt 20-02.am", VT * 1e3)
v.check("Txt 20-02.an", KT)
v.check("Txt 20-02.ao", WU)
gmid_max = 2 * WU / SR
gm1_min = 8 * KT * GAMMA * 1.56 / (15e-9) ** 2
v.check("Ex 20-02.1a", gmid_max)
v.check("Ex 20-02.1b", gm1_min / U)
v.check("Ex 20-02.1c", gm1_min / WU / PF)
iss_min = 2 * gm1_min / gmid_max
v.check("Ex 20-02.1d", iss_min / U)
v.check("Ex 20-02.1e", iss_min / (gm1_min / WU) / 1e6)

# ================================================================ Example 20-02.2 and the design devices
CL, CC, CP = 2 * PF, 0.6 * PF, 30 * FF
L1 = L3 = L5 = 1 * U
L6 = L7 = 0.5 * U
m6 = Dev(1 * U, L6)
vgs6 = m6.vgs_for_gmid(10.0)
ic6 = m6.i_d(vgs6) / m6.ispec
ft6 = m6.f_t(vgs6)
wt6 = 2 * math.pi * ft6
v.check("Ex 20-02.2a", ic6)
v.check("Ex 20-02.2b", ft6 / 1e9)
v.check("Ex 20-02.2c", ft6 * CC / (CL + CC) / 1e6)


def p2_of(gm6, cc, wt, cp=CP, cl=CL):
    c1 = cp + gm6 / wt
    return gm6 * cc / (c1 * cl + cc * (c1 + cl))


def gm6_for(p2, cc, wt):
    return brentq(lambda g: p2_of(g, cc, wt) - p2, 1e-7, 1.0, xtol=1e-16)


GM6 = gm6_for(2 * WU, CC, wt6)
v.check("Ex 20-02.2d", GM6 * 1e3)
v.check("Ex 20-02.2e", 2 * WU * CL * 1e3)
v.check("Ex 20-02.2f", (GM6 / (2 * WU * CL) - 1) * 100)
CGG6 = GM6 / wt6
C1 = CP + CGG6
v.check("Ex 20-02.2g", CGG6 / FF)
v.check("Ex 20-02.2h", C1 / FF)
m6l = Dev(1 * U, 1 * U)
vgs6l = m6l.vgs_for_gmid(10.0)
ft6l = m6l.f_t(vgs6l)
v.check("Ex 20-02.2i", ft6l / 1e9)
v.check("Ex 20-02.2j", ft6l * CC / (CL + CC) / 1e6)
v.check("Ex 20-02.2k", gm6_for(2 * WU, CC, 2 * math.pi * ft6l) * 1e3)
v.check("Txt 20-02.aa", MUN / MUP)


# ---------------------------------------------------------------- current against C_c (section 3.3)
def itot(cc, gmid6=10.0, wt=wt6):
    return 2 * WU * cc / 18 + gm6_for(2 * WU, cc, wt) / gmid6


ropt = minimize_scalar(itot, bounds=(0.3 * PF, 2 * PF), method="bounded", options={"xatol": 1e-17})
imin = ropt.fun
v.check("Ex 20-02.3a", ropt.x / PF)
v.check("Txt 20-02.ab", ropt.x / PF)
lo = brentq(lambda c: itot(c) / imin - 1.01, 0.3 * PF, ropt.x, xtol=1e-18)
hi = brentq(lambda c: itot(c) / imin - 1.01, ropt.x, 3 * PF, xtol=1e-18)
v.check("Txt 20-02.ac", lo / PF)
v.check("Txt 20-02.ad", hi / PF)
v.check("Txt 20-02.ae", (itot(CC) / imin - 1) * 100)

# ================================================================ Example 20-02.3 (the design)
GM1 = WU * CC
ID1 = GM1 / 18
ISS = 2 * ID1
v.check("Ex 20-02.3b", GM1 / U)
v.check("Ex 20-02.3c", ID1 / U)
v.check("Ex 20-02.3d", ISS / U)
SRD = ISS / CC
v.check("Ex 20-02.3e", SRD / 1e6)
v.check("Ex 20-02.3ao", (SRD / SR - 1) * 100)
m1 = Dev(1 * U, L1, mu=MUP, vsat=VSP)
vsg1 = m1.vgs_for_gmid(18.0)
v.check("Ex 20-02.3f", m1.i_d(vsg1) / m1.ispec)
v.check("Ex 20-02.3g", (vsg1 - VTH) * 1e3)
W1 = ID1 / m1.i_d(vsg1) * U
v.check("Ex 20-02.3h", W1 / U)
I6 = GM6 / 10
W6 = I6 / m6.i_d(vgs6) * U
v.check("Ex 20-02.3i", I6 / U)
v.check("Ex 20-02.3j", W6 / U)
v.check("Txt 20-02.ag", W6 / U)
v.check("Ex 20-02.3k", ISS * (1 + CL / CC) / U)
m3 = Dev(1 * U, L3)
ic3 = m3.i_d(vgs6) / m3.ispec
gmid3 = m3.gmid(vgs6)
v.check("Ex 20-02.3l", ic3)
v.check("Ex 20-02.3m", gmid3)
v.check("Ex 20-02.3n", ID1 / m3.i_d(vgs6) * U / U)
v.check("Ex 20-02.3ai", vgs6)
v.check("Txt 20-02.af", 2 * vgs6)
m7 = Dev(1 * U, L7, mu=MUP, vsat=VSP)
vsg7 = m7.vgs_for_gmid(10.0)
v.check("Ex 20-02.3o", m7.i_d(vsg7) / m7.ispec)
v.check("Ex 20-02.3p", I6 / m7.i_d(vsg7))
m5 = Dev(1 * U, L5, mu=MUP, vsat=VSP)
v.check("Ex 20-02.3q", m5.i_d(vsg7) / m5.ispec)
v.check("Ex 20-02.3r", ISS / m5.i_d(vsg7))
R1 = 1 / (ID1 / (VAL * L1) + ID1 / (VAL * L3))
R2 = 1 / (I6 / (VAL * L6) + I6 / (VAL * L7))
A1, A2 = GM1 * R1, GM6 * R2
v.check("Ex 20-02.3s", R1 / 1e3)
v.check("Ex 20-02.3t", A1)
v.check("Ex 20-02.3u", R2 / 1e3)
v.check("Ex 20-02.3v", A2)
v.check("Ex 20-02.3w", A1 * A2)
v.check("Ex 20-02.3x", 20 * math.log10(A1 * A2))
vd6, vd7, vd1, vd5 = vdsat(vgs6), vdsat(vsg7), vdsat(vsg1), vdsat(vsg7)
v.check("Ex 20-02.3y", vd6)
v.check("Ex 20-02.3z", vd7)
v.check("Ex 20-02.3ak", vd5)
v.check("Ex 20-02.3al", vd1)
v.check("Ex 20-02.3aa", 1.2 - vd7)
v.check("Ex 20-02.3ab", 1.2 - vd7 - vd6)
v.check("Ex 20-02.3aj", vsg1)
v.check("Ex 20-02.3ac", vgs6 + vd1 - vsg1)
v.check("Ex 20-02.3ad", 1.2 - vd5 - vsg1)
v.check("Ex 20-02.3am", gmid3 / 18)
noise = math.sqrt(8 * KT * GAMMA / GM1 * (1 + gmid3 / 18))
v.check("Ex 20-02.3ae", noise * 1e9)
ITOT = ISS + I6
v.check("Ex 20-02.3af", ITOT / U)
v.check("Ex 20-02.3ag", 1.2 * ITOT / U)
v.check("Ex 20-02.3ah", 50 * 2 / (ITOT * 1e3))
v.check("Ex 20-02.3an", I6 / ITOT * 100)

# ---------------------------------------------------------------- section 3.4: the triode R_z
lc6 = Dev(W6, L6, vel_sat=False)
q6 = lc6.q_of_vgs(vgs6)
# triode conductance at V_DS = 0 of a device with the same channel charge, from the forward-reverse model
def i_fr(dev, vp, vds):
    qs, qd = Dev.q_of_vp(vp), Dev.q_of_vp(vp - vds)
    return dev.ispec * ((qs * qs + qs) - (qd * qd + qd))


vp6 = (vgs6 - VTH) / N
unit = Dev(1 * U, 1 * U, vel_sat=False)   # W/L = 1
gds_unit = (i_fr(unit, vp6, 1e-6) - i_fr(unit, vp6, -1e-6)) / 2e-6
wl_z = lc6.g_m(vgs6) / gds_unit
v.assert_true("R_z g_m6 = (W/L)_6 / (n (W/L)_z) in the long-channel model",
              abs(wl_z - (W6 / L6) / N) < 1e-4 * wl_z, f"{wl_z} vs {(W6 / L6) / N}")
v.check("Txt 20-02.d", (W6 / L6) / N)

# ================================================================ Example 20-02.4
fgrid = np.logspace(2, math.log10(3e10), 120001)
results = {}
for tag, cl, rz in (("a", CL, 0.0), ("b", CL, 1 / GM6), ("c", CL, (1 + CL / CC) / GM6),
                    ("a4", 4 * PF, 0.0), ("b4", 4 * PF, 1 / GM6), ("c4", 4 * PF, (1 + CL / CC) / GM6)):
    h = miller_h(GM1, GM6, R1, R2, C1, cl, CC, rz)
    results[tag] = (margins_of(h), miller_poles(GM6, R1, R2, C1, cl, CC, rz))
ma, pa = results["a"]
v.check("Ex 20-02.4a", pa[0] / (2 * math.pi) / 1e3)
v.check("Ex 20-02.4b", 1 / (2 * math.pi * GM6 * R1 * R2 * CC) / 1e3)
v.check("Ex 20-02.4c", pa[1] / (2 * math.pi) / 1e6)
v.check("Ex 20-02.4d", GM6 / CC / (2 * math.pi) / 1e6)
v.check("Ex 20-02.4e", ma["fc"] / 1e6)
v.check("Ex 20-02.4f", ma["pm"])
v.check("Ex 20-02.4g", ma["gm"])
mb, pb = results["b"]
v.check("Ex 20-02.4h", 1 / GM6)
v.check("Ex 20-02.6a", 4 * WU * CL * 1e3)
v.check("Ex 20-02.4i", pb[1] / (2 * math.pi) / 1e6)
v.check("Ex 20-02.4j", pb[2] / (2 * math.pi) / 1e9)
p3est = GM6 * (1 / C1 + 1 / CC + 1 / CL) / (2 * math.pi)
v.check("Ex 20-02.4k", p3est / 1e9)
v.check("Ex 20-02.4l", mb["fc"] / 1e6)
v.check("Ex 20-02.4m", mb["pm"])
v.check("Ex 20-02.4n", mb["gm"])
mc, pc = results["c"]
v.check("Ex 20-02.4o", (1 + CL / CC) / GM6)
v.check("Ex 20-02.4aa", 1 + CL / CC)
v.check("Ex 20-02.4p", pc[1] / (2 * math.pi) / 1e6)
v.check("Ex 20-02.4q", pc[2] / (2 * math.pi) / 1e6)
v.check("Ex 20-02.4r", mc["fc"] / 1e6)
v.check("Ex 20-02.4s", mc["pm"])
v.assert_true("cancelling R_z leaves no phase crossover below 30 GHz", mc["f180"] is None, "")
v.check("Ex 20-02.4t", results["b4"][0]["pm"])
v.check("Ex 20-02.4u", results["b4"][0]["fc"] / 1e6)
v.check("Ex 20-02.4v", results["c4"][0]["pm"])
v.check("Ex 20-02.4w", results["c4"][1][1] / (2 * math.pi) / 1e6)
v.check("Ex 20-02.4x", results["a4"][0]["pm"])
v.check("Ex 20-02.4y", mc["pm"] - mb["pm"])
v.check("Ex 20-02.4z", results["c4"][0]["pm"] - results["b4"][0]["pm"])
v.check("Txt 20-02.ap", 2 / 18)

# ================================================================ Example 20-02.5 (indirect compensation)
GM6I = 1e-3
C1I = CP + GM6I / wt6
R2I = 1 / (100e-6 / (VAL * L6) + 100e-6 / (VAL * L7))
v.check("Ex 20-02.5a", ISS * (1 + CL / CC) / U)
v.check("Ex 20-02.5b", C1I / FF)
v.check("Ex 20-02.5c", R2I / 1e3)
v.check("Ex 20-02.5d", p2_of(GM6I, CC, wt6) / (2 * math.pi) / 1e6)
p2ind = GM6I * CC / (C1I * (CL + CC))
v.check("Ex 20-02.5e", p2ind / (2 * math.pi) / 1e6)
v.check("Txt 20-02.au", 1 + CC * CL / (C1I * (CL + CC)))
s = sp.symbols("s")
ind = {}
for tag, gmc in (("b", GM1), ("c", 600e-6), ("p13", 300e-6)):
    y = indirect_y(GM6I, gmc, R1, R2I, 1e6, C1I, CL, CC, 20 * FF)
    h = (lambda yy: (lambda f: solve_nodal(yy, np.array([0, -GM1, 0], dtype=complex), 2, np.atleast_1d(f))))(y)
    ysym = sp.Matrix([[1 / R1 + s * C1I, -gmc, 0], [0, gmc + 1e-6 + s * (20 * FF + CC), -s * CC],
                      [GM6I, -s * CC, 1 / R2I + s * (CL + CC)]])
    pole = complex_pair(ysym, s)
    ind[tag] = (margins_of(h), -pole.real / abs(pole), abs(pole) / (2 * math.pi), gmc * (CL + CC) / (CL * CC))
mb5, zb, fnb, p3b = ind["b"]
v.check("Ex 20-02.5f", p3b / (2 * math.pi) / 1e6)
v.check("Ex 20-02.5g", mb5["fc"] / 1e6)
v.check("Ex 20-02.5h", mb5["pm"])
v.check("Ex 20-02.5i", zb)
v.check("Ex 20-02.5j", mb5["f180"] / 1e6)
v.check("Ex 20-02.5k", mb5["gm"])
mc5, zc, fnc, p3c = ind["c"]
v.check("Ex 20-02.5l", p3c / (2 * math.pi) / 1e6)
v.check("Ex 20-02.5m", mc5["fc"] / 1e6)
v.check("Ex 20-02.5n", mc5["pm"])
v.check("Ex 20-02.5o", zc)
v.check("Ex 20-02.5p", mc5["gm"])
v.check("Ex 20-02.5q", mc5["f180"] / 1e6)
v.check("Ex 20-02.5r", 600e-6 / 18 / U)
itot_ind = ISS + 600e-6 / 18 + 100e-6
v.check("Ex 20-02.5s", itot_ind / U)
v.check("Ex 20-02.5t", (1 - itot_ind / ITOT) * 100)
v.check("Ex 20-02.5u", p3b / WU)
v.check("Ex 20-02.5v", 20 * math.log10(p3b / WU))
v.check("Ex 20-02.5w", p3c / WU)
v.check("Ex 20-02.5x", 20 * math.log10(p3c / WU))
v.check("Ex 20-02.5y", mc5["pm"] - mb["pm"])

# ================================================================ Example 20-02.6 (nested Miller)
GM3 = 4 * WU * CL
CM1, CM2 = 4 * GM1 * CL / GM3, 2 * GM1 * CL / GM3
v.check("Ex 20-02.6b", CM1 / PF)
v.check("Ex 20-02.6c", CM2 / PF)
v.check("Ex 20-02.6d", GM3 / 10 / U)
v.check("Ex 20-02.6e", 25 * 25 * 20)
v.check("Ex 20-02.6f", 20 * math.log10(25 * 25 * 20))
v.check("Ex 20-02.6t", 20 * math.log10(25 * 25 * 20) - 20 * math.log10(A1 * A2))
CGG3 = GM3 / wt6
v.check("Ex 20-02.6j", CGG3 / FF)
v.check("Ex 20-02.6r", (30 * FF + CGG3) / FF)


def nmc_h(gm1, gm2, gm3, a, cn1, cn2, cl, cm1, cm2):
    y = nmc_y(gm2, gm3, a[0] / gm1, a[1] / gm2, a[2] / gm3, cn1, cn2, cl, cm1, cm2)
    return lambda f: solve_nodal(y, np.array([gm1, 0, 0], dtype=complex), 2, np.atleast_1d(f))


m6b = margins_of(nmc_h(GM1, GM1, GM3, (25, 25, 20), 0, 0, CL, CM1, CM2))
v.check("Ex 20-02.6g", m6b["fc"] / 1e6)
v.check("Ex 20-02.6h", m6b["pm"])
v.check("Ex 20-02.6i", m6b["gm"])
m6c = margins_of(nmc_h(GM1, GM1, GM3, (25, 25, 20), 30 * FF, 30 * FF + CGG3, CL, CM1, CM2))
v.check("Ex 20-02.6k", m6c["pm"])
v.check("Ex 20-02.6l", m6c["gm"])
v.check("Ex 20-02.6m", m6c["fc"] / 1e6)
m6d = margins_of(nmc_h(GM1, 2 * GM1, 2 * GM3, (25, 25, 20), 30 * FF, 30 * FF + 2 * CGG3, CL, CM1, 0.4 * PF))
v.check("Ex 20-02.6s", 2 * GM3 * 1e3)
v.check("Ex 20-02.6n", 2 * GM3 / 10 / U)
v.check("Ex 20-02.6o", m6d["pm"])
v.check("Ex 20-02.6p", m6d["gm"])
v.check("Ex 20-02.6q", m6d["fc"] / 1e6)
v.check("Ex 20-02.6u", (2 * GM3 / 10) / I6)
# ideal Butterworth loop (section 3.6)
lb = lambda w: (0.5 / (1j * w)) / (1 + 1j * w + (1j * w) ** 2 / 2)  # noqa: E731
wc_b = brentq(lambda w: abs(lb(w)) - 1, 1e-3, 10)
v.check("Txt 20-02.e", wc_b / 0.5)
v.check("Txt 20-02.f", 180 + math.degrees(np.angle(lb(wc_b))))

# ================================================================ section 3.7: gain boosting


def boost_settle(gm, cl, a_unb, ab0, beta, fub, eps=1e-4, t_end=600e-9, npts=1200001):
    r0 = a_unb / gm
    wpb = 2 * math.pi * fub / ab0
    ss = sp.symbols("s")
    rout = r0 * (1 + ab0 / (1 + ss / wpb))
    z = rout / (1 + ss * cl * rout)
    a = gm * z
    tcl = sp.together(a / (1 + beta * a))
    nn, dd = sp.fraction(tcl)
    nc = [float(x) for x in sp.Poly(sp.expand(nn), ss).all_coeffs()]
    dc = [float(x) for x in sp.Poly(sp.expand(dd), ss).all_coeffs()]
    final = nc[-1] / dc[-1]
    t = np.linspace(0, t_end, npts)
    _, yv = signal.step((np.array(nc) / final, dc), T=t)
    bad = np.where(np.abs(yv - 1) > eps)[0]
    return t[bad[-1] + 1]


v.check("Txt 20-02.g", 1e-3 / 1e-12 / (2 * math.pi) / 1e6)
v.check("Txt 20-02.h", 300 * 101)
v.check("Txt 20-02.i", 100 / (0.5 * 300))
v.check("Txt 20-02.j", boost_settle(1e-3, 1e-12, 300, 100, 0.5, 20e6) / 1e-9)
v.check("Txt 20-02.k", boost_settle(1e-3, 1e-12, 300, 100, 0.5, 300e6) / 1e-9)
v.check("Txt 20-02.l", math.log(1e4) / (0.5 * 1e9) / 1e-9)
v.check("Txt 20-02.bf", 0.5 * 1e9 / (2 * math.pi) / 1e6)
# exact tail of the f_ub = 20 MHz case: residue and pole of the closed-loop error, from the polynomial model
r0b, wpbb = 300 / 1e-3, 2 * math.pi * 20e6 / 100
ss = sp.symbols("s")
zb_ = r0b * (1 + 100 / (1 + ss / wpbb)) / (1 + ss * 1e-12 * r0b * (1 + 100 / (1 + ss / wpbb)))
err = sp.together(1 / (ss * (1 + 0.5 * 1e-3 * zb_)))
ne, de = sp.fraction(err)
dcoef = [float(x) for x in sp.Poly(sp.expand(de), ss).all_coeffs()]
ncoef = [float(x) for x in sp.Poly(sp.expand(ne), ss).all_coeffs()]
roots_e = np.roots(dcoef)
slow = max([r for r in roots_e if abs(r) > 1.0], key=lambda r: r.real)   # the slowest non-zero pole
dprime = np.polyval(np.polyder(dcoef), slow)
residue = np.polyval(ncoef, slow) / dprime
v.check("Txt 20-02.bc", abs(residue.real) * 100)
v.check("Txt 20-02.bd", 1 / abs(slow.real) / 1e-9)
v.check("Txt 20-02.be", abs(slow.real) / (2 * math.pi) / 1e6)

# ================================================================ section 3.8: slewing and settling


def slew_sim(vstep, sr, tau, eps):
    """Single-pole follower with a slew-rate clip, integrated numerically; time to stay within eps of the final value."""
    def rhs(_, y):
        return [max(-sr, min(sr, (vstep - y[0]) / tau))]
    t_end = 20 * tau + vstep / sr
    sol_ = solve_ivp(rhs, (0, t_end), [0.0], max_step=tau / 200, rtol=1e-10, atol=1e-13, dense_output=True)
    tt = np.linspace(0, t_end, 400001)
    yy = sol_.sol(tt)[0]
    bad = np.where(np.abs(yy - vstep) > eps * vstep)[0]
    return tt[bad[-1] + 1]


TAU = 1 / WU
v.check("Txt 20-02.m", TAU / 1e-9)
v.check("Txt 20-02.n", SRD * TAU)
t_slew = (0.5 - SRD * TAU) / SRD
v.check("Txt 20-02.o", t_slew / 1e-9)
t_tot = slew_sim(0.5, SRD, TAU, 1e-3)
v.check("Txt 20-02.q", t_tot / 1e-9)
v.check("Txt 20-02.p", (t_tot - t_slew) / 1e-9)
v.check("Txt 20-02.r", TAU * math.log(1e3) / 1e-9)
v.check("Txt 20-02.s", math.log(1e3))


def ts_two_pole(k, eps=1e-3, t_end=40.0, npts=200001):
    t = np.linspace(0, t_end, npts)
    _, yv = signal.step(([1.0], [1 / k, 1.0, 1.0]), T=t)
    bad = np.where(np.abs(yv - 1) > eps)[0]
    return t[bad[-1] + 1]


ks = np.arange(3.1, 3.6, 0.01)
tss = np.array([ts_two_pole(k) for k in ks])
kmin = ks[int(np.argmin(tss))]
v.check("Txt 20-02.t", tss.min())
v.check("Txt 20-02.u", kmin)
v.check("Txt 20-02.v", two_pole(kmin)[1])
v.check("Txt 20-02.w", ts_two_pole(1.5))
v.assert_true("two-pole settling is not monotonic in k", ts_two_pole(2.5) < ts_two_pole(3.0) or
              ts_two_pole(3.5) < ts_two_pole(4.0), "")

# ================================================================ section 3.9: saturation voltage limits
v.check("Txt 20-02.x", vdsat_q(1e-6) / VT)
v.check("Txt 20-02.ah", vdsat_q(1e-6) * 1e3)
v.check("Txt 20-02.ai", math.sqrt(0.02))
qbig = 1e4
vbig = vdsat_q(qbig) / VT
v.check("Txt 20-02.aj", 1 - math.sqrt(0.02))
v.check("Txt 20-02.ak", vbig - 2 * qbig * (1 - math.sqrt(0.02)))
v.assert_true("strong-inversion offset tends to (1 - sqrt 0.02) + ln(1/sqrt 0.02)",
              abs(vbig - 2 * qbig * (1 - math.sqrt(0.02)) - (1 - math.sqrt(0.02)) - math.log(1 / math.sqrt(0.02))) < 1e-3, "")
v.check("Txt 20-02.al", N / 2)

# ================================================================ section 3.10: PSRR of the design


def psrr_open(f, gm1=GM1, gm6=GM6, r1=R1, ro6=VAL * L6 / I6, ro7=VAL * L7 / I6, c1=C1, cc=CC, cl=CL):
    """A_dm / A_ss from the two-node model with VSS moving, solved numerically."""
    sv = 2j * math.pi * f
    g1, g6, g7 = 1 / r1, 1 / ro6, 1 / ro7
    y = np.array([[g1 + sv * (c1 + cc), -sv * cc], [gm6 - sv * cc, g6 + g7 + sv * (cl + cc)]], dtype=complex)
    b_ss = np.array([(g1 + sv * c1), gm6 + g6], dtype=complex)        # v_ss = 1
    b_dm = np.array([-gm1, 0], dtype=complex)                          # v_in = 1
    ass = np.linalg.solve(y, b_ss)[1]
    adm = np.linalg.solve(y, b_dm)[1]
    return adm, ass


def psrr_db(f):
    adm, ass = psrr_open(f)
    return 20 * math.log10(abs(adm / ass))


v.check("Txt 20-02.aw", GM1 * R1 * GM6 * VAL * L6 / I6)
v.check("Txt 20-02.ax", psrr_db(1.0))
v.check("Txt 20-02.ay", 1 / (2 * math.pi * GM6 * R1 * (VAL * L6 / I6) * CC) / 1e3)
v.check("Txt 20-02.av", psrr_db(1e6))
v.check("Txt 20-02.az", 20 * math.log10(50))
v.check("20-02.10a", psrr_db(1e4))
v.check("20-02.10b", psrr_db(1e5))
v.check("20-02.10c", brentq(lambda f: psrr_db(f) - 40, 1e4, 1e7) / 1e3)
v.check("20-02.10d", 50e6 / 100 / 1e3)
v.check("20-02.10e", (500e3 / brentq(lambda f: psrr_db(f) - 40, 1e4, 1e7) - 1) * 100)

# ================================================================ section 3.11: SC CMFB


def cycles(cs, cr, factor):
    e, k = 1.0, 0
    while e > 1 / factor:
        e *= cs / (cs + cr)
        k += 1
    return k


v.check("Txt 20-02.y", cycles(1, 0.25, 1e3))
v.check("Txt 20-02.z", cycles(1, 0.5, 1e3))
v.check("Txt 20-02.bb", 1 / (1 + 0.25))

# ================================================================ section 7 and 9 numbers
v.check("Txt 20-02.aq", 2 * N * VT * 1e3)
v.check("Txt 20-02.ba", 1 / (N * VT))
# R-324: computed f_u C_L / I from the published GBW, load and current of each multistage OTA
foms = {
    "Tan & Ki 2015 (table)": 3.37 * 680 / 10.5e-3,
    "Marano 2016": 2.72 * 10000 / 24.49e-3,
    "Qu 2017": 1.18 * 18000 / 58e-3,
    "Grasso 2018, 30 nF": 0.91 * 30000 / 6.36e-3,
    "Grasso 2018, 10 nF": 1.70 * 10000 / 6.36e-3,
    "Grasso 2018, 100 nF": 0.43 * 100000 / 6.36e-3,
    "Qin 2017": 0.52 * 3200 / (60e-3 / 1.6),
}
v.check("Txt 20-02.ar", min(foms.values()))
v.check("Txt 20-02.as", max(foms.values()))

# ================================================================ problems
# 20-02.1
wu1 = 2 * math.pi * 20e6
g1max = 2 * wu1 / 10e6
g1min = 8 * KT * GAMMA * 1.5 / (20e-9) ** 2
v.check("20-02.1a", g1max)
v.check("20-02.1b", g1min / U)
v.check("20-02.1c", g1min / wu1 / PF)
v.check("20-02.1d", 2 * g1min / g1max / U)
g1max25 = 2 * wu1 / 25e6
v.check("20-02.1e", g1max25)
v.check("20-02.1f", 2 * g1min / g1max25 / U)
v.check("20-02.1g", (2 * g1min / g1max25) / (2 * g1min / g1max))
# 20-02.2
for k, (ix, ip, ie) in ((1.0, ("a", "b", "c")), (2.2, ("d", "e", "f")), (3.0, ("g", "h", "i"))):
    xk, pmk = two_pole(k)
    v.check(f"20-02.2{ix}", xk)
    v.check(f"20-02.2{ip}", pmk)
    v.check(f"20-02.2{ie}", 90 - math.degrees(math.atan(1 / k)))
v.check("20-02.2j", two_pole(1.0)[1] - 45.0)
# 20-02.3
w10 = 2 * math.pi * 10e6
for gi, (a, b) in ((25, ("a", "d")), (15, ("b", "e")), (5, ("c", "f"))):
    v.check(f"20-02.3{a}", 2 / gi * 1e3)
    v.check(f"20-02.3{b}", 2 / gi * w10 / 1e6)
v.check("20-02.3g", 2 * N * VT * 1e3)
v.check("20-02.3h", 2 * N * VT * w10 / 1e6)
# 20-02.4
p4 = dict(gm1=100e-6, gm6=1e-3, r1=1e6, r2=50e3, c1=0.1e-12, cl=1e-12, cc=0.3e-12)
v.check("20-02.4a", p4["gm1"] * p4["r1"] * p4["gm6"] * p4["r2"])
a1_4 = p4["gm6"] * p4["r1"] * p4["r2"] * p4["cc"] + p4["r1"] * (p4["c1"] + p4["cc"]) + p4["r2"] * (p4["cl"] + p4["cc"])
a2_4 = p4["r1"] * p4["r2"] * (p4["c1"] * p4["cl"] + p4["cc"] * (p4["c1"] + p4["cl"]))
v.check("20-02.4b", a1_4 / U)
v.check("20-02.4c", a2_4)
pp4 = miller_poles(p4["gm6"], p4["r1"], p4["r2"], p4["c1"], p4["cl"], p4["cc"], 0.0)
v.check("20-02.4d", pp4[0] / (2 * math.pi) / 1e3)
v.check("20-02.4e", pp4[1] / (2 * math.pi) / 1e6)
v.check("20-02.4f", 1 / (2 * math.pi * p4["gm6"] * p4["r1"] * p4["r2"] * p4["cc"]) / 1e3)
v.check("20-02.4g", p4["gm6"] * p4["cc"] / (p4["c1"] * p4["cl"] + p4["cc"] * (p4["c1"] + p4["cl"])) / (2 * math.pi) / 1e6)
v.check("20-02.4h", p4["gm6"] / p4["cl"] / (2 * math.pi) / 1e6)
v.check("20-02.4i", p4["gm1"] / p4["cc"] / (2 * math.pi) / 1e6)
v.check("20-02.4j", p4["gm6"] / p4["cc"] / (2 * math.pi) / 1e6)
m4 = margins_of(miller_h(p4["gm1"], p4["gm6"], p4["r1"], p4["r2"], p4["c1"], p4["cl"], p4["cc"], 0.0))
v.check("20-02.4k", m4["fc"] / 1e6)
v.check("20-02.4l", m4["pm"])
v.check("20-02.4m", m4["gm"])
v.check("20-02.4n", (1 / (2 * math.pi * p4["gm6"] * p4["r1"] * p4["r2"] * p4["cc"]) / (pp4[0] / (2 * math.pi)) - 1) * 100)
v.assert_true("both pole-splitting estimates are about 3 % off", abs(1 - p4["gm6"] * p4["cc"] / (p4["c1"] * p4["cl"] + p4["cc"]
              * (p4["c1"] + p4["cl"])) / pp4[1]) * 100 < 3.5, "")
v.check("20-02.4o", (p4["gm6"] / p4["cl"] / pp4[1] - 1) * 100)
# 20-02.5
m6p = Dev(1 * U, 0.5 * U, mu=MUP, vsat=VSP)
vsg6p = m6p.vgs_for_gmid(10.0)
ft6p = m6p.f_t(vsg6p)
v.check("20-02.5a", m6p.i_d(vsg6p) / m6p.ispec)
v.check("20-02.5b", ft6p / 1e9)
v.check("20-02.5c", ft6p * CC / (CL + CC) / 1e6)
gm6p = gm6_for(2 * WU, CC, 2 * math.pi * ft6p)
v.check("20-02.5d", gm6p * 1e3)
v.check("20-02.5e", (CP + gm6p / (2 * math.pi * ft6p)) / FF)
v.check("20-02.5f", gm6p / 10 / U)
v.check("20-02.5g", (gm6p / 10) / I6)
v.check("20-02.5h", ft6 / ft6p)
# 20-02.6
inv = 1 / GM6
v.check("20-02.6a", inv)
v.check("20-02.6b", GM6 / (0.2 * CC) / (2 * math.pi) / 1e9)
g_lo, g_hi, r_lo, r_hi = inv / 1.15, inv / 0.85, 0.8 * inv, 1.2 * inv
v.check("20-02.6c", g_lo)
v.check("20-02.6d", g_hi)
v.check("20-02.6e", r_lo)
v.check("20-02.6f", r_hi)
z_rhp = 1 / (CC * (g_hi - r_lo))
v.check("20-02.6g", z_rhp / (2 * math.pi) / 1e9)
v.check("20-02.6h", 1 / (CC * (r_hi - g_lo)) / (2 * math.pi) / 1e9)
v.check("20-02.6i", math.degrees(math.atan(2 * math.pi * mb["fc"] / z_rhp)))
v.check("20-02.6j", (W6 / L6) / N)
v.check("20-02.6k", g_hi - r_lo)
v.check("20-02.6l", r_hi - g_lo)
# 20-02.7
for vs, (a, b, c3) in ((0.2, ("a", "b", "c")), (1.0, ("d", "e", "f"))):
    ttot = slew_sim(vs, SRD, TAU, 1e-3)
    tsl = (vs - SRD * TAU) / SRD
    v.check(f"20-02.7{a}", tsl / 1e-9)
    v.check(f"20-02.7{b}", (ttot - tsl) / 1e-9)
    v.check(f"20-02.7{c3}", ttot / 1e-9)
v.check("20-02.7i", TAU / 1e-9)
v.check("20-02.7j", SRD * TAU)
sr30 = brentq(lambda x: slew_sim(1.0, x, TAU, 1e-3) - 30e-9, 4e7, 2e8, xtol=1e3)
v.check("20-02.7g", sr30 / 1e6)
v.check("20-02.7h", 2 * WU / sr30)
# 20-02.8
v.check("20-02.8a", ISS * (1 + 5 / 0.6) / U)
v.check("20-02.8b", (I6 - ISS) / 5e-12 / 1e6)
# 20-02.9
lcn = Dev(1 * U, 1 * U, vel_sat=False)
for ic, (a, b) in ((0.1, ("a", "b")), (1.0, ("c", "d")), (10.0, ("e", "f"))):
    vg = brentq(lambda x: lcn.i_d(x) / lcn.ispec - ic, VTH - 1, VTH + 2, xtol=1e-15)
    v.check(f"20-02.9{a}", lcn.q_of_vgs(vg))
    v.check(f"20-02.9{b}", vdsat(vg))
vg1 = brentq(lambda x: lcn.i_d(x) / lcn.ispec - 1.0, VTH - 1, VTH + 2, xtol=1e-15)
vg10 = brentq(lambda x: lcn.i_d(x) / lcn.ispec - 10.0, VTH - 1, VTH + 2, xtol=1e-15)
v.check("20-02.9g", 0.9 - 2 * vdsat(vg1))
v.check("20-02.9h", 0.9 - 2 * vdsat(vg10))
v.check("20-02.9i", 2 * vdsat(vg10) - 2 * vdsat(vg1))
# 20-02.11
cmir = 2 * (2 / 3) * 3.707e-6 * 1e-6 * COX
gm3v = 10.125 * 10.47e-6
fpm = gm3v / (2 * math.pi * cmir)
v.check("20-02.11a", cmir / FF)
v.check("20-02.11b", gm3v / U)
v.check("20-02.11c", fpm / 1e6)
v.check("20-02.11d", 2 * fpm / 1e6)
cost = math.degrees(math.atan(43.62e6 / fpm) - math.atan(43.62e6 / (2 * fpm)))
v.check("20-02.11e", cost)
v.check("20-02.11f", mb["pm"] - cost)
# 20-02.12
rz = 1 / GM6
a1b = GM6 * R1 * R2 * CC + R1 * (C1 + CC) + R2 * (CL + CC) + rz * CC
a2b = R1 * R2 * (C1 * CL + CC * (C1 + CL)) + rz * CC * (C1 * R1 + CL * R2)
a3b = R1 * R2 * rz * C1 * CL * CC
v.check("20-02.12a", a1b / U)
v.check("20-02.12b", a2b)
v.check("20-02.12c", a3b)
v.check("20-02.12d", a2b / a3b / (2 * math.pi) / 1e9)
v.check("20-02.12e", p3est / 1e9)
v.check("20-02.12f", pb[2] / (2 * math.pi) / 1e9)
# 20-02.13
m13, z13, fn13, p313 = ind["p13"]
v.check("20-02.13a", p2ind / (2 * math.pi) / 1e6)
v.check("20-02.13b", p313 / (2 * math.pi) / 1e6)
v.check("20-02.13c", 0.5 * math.sqrt(p313 / p2ind))
v.check("20-02.13d", math.sqrt(p2ind * p313) / (2 * math.pi) / 1e6)
v.check("20-02.13e", 20 * math.log10(p313 / WU))
v.check("20-02.13f", m13["fc"] / 1e6)
v.check("20-02.13g", m13["pm"])
v.check("20-02.13h", z13)
v.check("20-02.13i", fn13 / 1e6)
v.check("20-02.13j", m13["gm"])
v.check("20-02.13k", (math.sqrt(p2ind * p313) / (2 * math.pi) / fn13 - 1) * 100)
v.check("20-02.13l", (1 - 0.5 * math.sqrt(p313 / p2ind) / z13) * 100)
v.check("20-02.13m", 20 * math.log10(p313 / WU) - m13["gm"])
# 20-02.14
gm14, cl14, au14, ab14, b14 = 2e-3, 4e-12, 400, 100, 1 / 3
wu14 = gm14 / cl14
v.check("20-02.14a", wu14 / (2 * math.pi) / 1e6)
v.check("20-02.14b", b14 * wu14 / (2 * math.pi) / 1e6)
v.check("20-02.14c", au14 * (1 + ab14))
v.check("20-02.14d", 100 / (b14 * au14 * (1 + ab14)))
v.check("20-02.14e", 100 / (b14 * au14))
v.check("20-02.14f", math.log((1 / (b14 * au14)) / 1e-4) / (2 * math.pi * 10e6) / 1e-9)
v.check("20-02.14g", math.log(1e4) / (b14 * wu14) / 1e-9)
v.check("20-02.14h", boost_settle(gm14, cl14, au14, ab14, b14, 10e6) / 1e-9)
v.check("20-02.14i", boost_settle(gm14, cl14, au14, ab14, b14, 100e6) / 1e-9)
# 20-02.15
v.check("20-02.15a", 0.8 / 1.0)
n15a = cycles(0.8, 0.2, 100)
v.check("20-02.15b", n15a)
v.check("20-02.15c", n15a / 50e6 / 1e-9)
v.check("20-02.15d", 0.8 / 0.9)
n15b = cycles(0.8, 0.1, 100)
v.check("20-02.15e", n15b)
v.check("20-02.15f", n15b / 50e6 / 1e-9)
# 20-02.16
wu16, cl16, g16 = 2 * math.pi * 20e6, 10e-12, 50e-6
gm3_16 = 4 * wu16 * cl16
v.check("20-02.16a", gm3_16 * 1e3)
v.check("20-02.16b", 4 * g16 * cl16 / gm3_16 / PF)
v.check("20-02.16c", 2 * g16 * cl16 / gm3_16 / PF)
m16 = margins_of(nmc_h(g16, g16, gm3_16, (30, 30, 20), 0, 0, cl16, 4 * g16 * cl16 / gm3_16, 2 * g16 * cl16 / gm3_16))
v.check("20-02.16d", m16["pm"])
v.check("20-02.16e", m16["fc"] / 1e6)
v.check("20-02.16f", m16["gm"])
v.check("20-02.16g", 2 * wu16 * cl16 * 1e3)
v.check("20-02.16h", gm3_16 / (2 * wu16 * cl16))
# 20-02.17
w17 = 2 * math.pi * 100e6
v.check("20-02.17a", 100 * 10 / 2)
v.check("20-02.17b", 2 * w17 / 200e6)
v.check("20-02.17c", 2 * w17 / 5e6)
v.check("20-02.17d", 2 * N * VT * w17 / 1e6)
v.check("20-02.17e", (2 * w17 / 5e6) * N * VT)
v.check("20-02.17f", 1 / (N * VT))

# ================================================================ lab README
# Part 1: (g_m/I_D)_6 = 6 S/A, and the slew-constrained optimum over (g_m/I_D)_6 and C_c
def wt_for(gmid6):
    d6 = Dev(1 * U, L6)
    return 2 * math.pi * d6.f_t(d6.vgs_for_gmid(gmid6))


wt6_6 = wt_for(6.0)
r6 = minimize_scalar(lambda c: itot(c, 6.0, wt6_6), bounds=(0.3 * PF, 2 * PF), method="bounded",
                     options={"xatol": 1e-17})
v.check("Lab 20-02.a", r6.x / PF)
v.check("Lab 20-02.b", r6.fun / U)


def constrained_best(gmid6):
    wt = wt_for(gmid6)

    def i6_of(c):
        return gm6_for(2 * WU, c, wt) / gmid6

    def slack(c):
        return i6_of(c) - (2 * WU * c / 18) * (1 + CL / c)
    r = minimize_scalar(lambda c: itot(c, gmid6, wt), bounds=(0.35 * PF, 2 * PF), method="bounded",
                        options={"xatol": 1e-17})
    c_best = r.x
    if slack(c_best) < 0:   # the output-slew condition binds: largest feasible C_c below the unconstrained optimum
        c_best = brentq(slack, 0.35 * PF, c_best, xtol=1e-18)
    return itot(c_best, gmid6, wt), c_best, wt


rr = minimize_scalar(lambda gi: constrained_best(gi)[0], bounds=(10.0, 26.0), method="bounded",
                     options={"xatol": 1e-4})
i_best, c_best, wt_best = constrained_best(rr.x)
v.check("Lab 20-02.g", rr.x)
v.check("Lab 20-02.h", i_best / U)
v.check("Lab 20-02.n", c_best / PF)
v.check("Lab 20-02.r", (1 - i_best / ITOT) * 100)
# width and C_1 at 18 S/A and the 0.93 pF of the README
gopt = rr.x
gm6_18 = gm6_for(2 * WU, c_best, wt_best)
d18 = Dev(1 * U, L6)
vg18 = d18.vgs_for_gmid(gopt)
w6_18 = (gm6_18 / gopt) / d18.i_d(vg18) * U
wt18 = wt_best
v.check("Lab 20-02.s", w6_18 / W6)
c1_18 = CP + gm6_18 / wt18
v.check("Lab 20-02.t", c1_18 / C1)
v.check("Lab 20-02.w", gm6_18 / c1_18 / (2 * math.pi) / 1e9)
# Part 3: slewing of the behavioral model of slew.cir, integrated with solve_ivp
RZ = 1 / GM6


def slew_rhs(t, y, vin_of_t):
    vo, v1, u = y                      # u = voltage across C_c (v_x - v_out)
    vin = vin_of_t(t)
    b1 = max(-ISS, min(ISS, GM1 * (vin - vo)))
    iz = (v1 - vo - u) / RZ
    b6 = max(0.0, I6 + GM6 * v1)
    dvo = (I6 - b6 - (vo - 0.6) / R2 + iz) / CL
    dv1 = (-b1 - v1 / R1 - iz) / C1
    du = iz / CC
    return [dvo, dv1, du]


def vin_step(t):
    return 0.2 if t < 50e-9 else 1.0


# settle at 0.2 V first
y0 = [0.2, (0.6 - 0.2) / (R2 * GM6), 0.0]
sol_s = solve_ivp(slew_rhs, (0, 120e-9), y0, args=(vin_step,), method="Radau", max_step=2e-11, rtol=1e-9,
                  atol=1e-12, dense_output=True)
tt = np.linspace(50e-9, 120e-9, 700001)
vv = sol_s.sol(tt)[0]
t04 = tt[np.where(vv >= 0.4)[0][0]]
t07 = tt[np.where(vv >= 0.7)[0][0]]
sr_sim = 0.3 / (t07 - t04)
v.check("Lab 20-02.c", sr_sim / 1e6)
v.check("Lab 20-02.d", SRD / (1 + 1 / A2) / 1e6)
v.check("Lab 20-02.v", 1 + 1 / A2)
v.check("Lab 20-02.y", (1 - sr_sim / (SRD / (1 + 1 / A2))) * 100)
# Part 4: the follower's rejection A_ss/(1 + A_dm)
for f, key in ((1e3, "Lab 20-02.e"), (1e6, "Lab 20-02.f")):
    adm, ass = psrr_open(f)
    v.check(key, -20 * math.log10(abs(ass / (1 + adm))))
# Part 5: closed-loop step overshoot of the indirect designs
for gmc, key in ((GM1, "Lab 20-02.i"), (600e-6, "Lab 20-02.j")):
    ysym = sp.Matrix([[1 / R1 + s * C1I, -gmc, 0], [0, gmc + 1e-6 + s * (20 * FF + CC), -s * CC],
                      [GM6I, -s * CC, 1 / R2I + s * (CL + CC)]])
    hs = sp.together(ysym.LUsolve(sp.Matrix([0, -GM1, 0]))[2])
    nn, dd = sp.fraction(hs)
    nc = np.array([float(x) for x in sp.Poly(sp.expand(nn), s).all_coeffs()])
    dc = np.array([float(x) for x in sp.Poly(sp.expand(dd), s).all_coeffs()])
    dcl = np.polyadd(dc, nc)
    t = np.linspace(0, 200e-9, 400001)
    _, yv = signal.step((nc, dcl), T=t)
    fin = nc[-1] / dcl[-1]
    v.check(key, max(0.0, (yv.max() / fin - 1) * 100))
v.check("Lab 20-02.u", mb5["f180"] / 1e6)
# Part 6: nested Miller re-tuning on the README's grid (vectorized nodal solve by Cramer's rule)
def nmc_vec(f, gm2, gm3, cn2, cm2):
    sv = 2j * math.pi * np.asarray(f, dtype=float)
    g1, g2, g3 = GM1 / 25, gm2 / 25, gm3 / 20
    cn1 = 30 * FF
    a11, a13 = g1 + sv * (cn1 + CM1), -sv * CM1
    a21, a22, a23 = -gm2 + 0 * sv, g2 + sv * (cn2 + cm2), -sv * cm2
    a31, a32, a33 = -sv * CM1, gm3 - sv * cm2, g3 + sv * (CL + CM1 + cm2)
    det = a11 * (a22 * a33 - a23 * a32) + a13 * (a21 * a32 - a22 * a31)
    return GM1 * (a21 * a32 - a22 * a31) / det        # Cramer's rule for the output, b = (g_m1, 0, 0)


best = None
for f3 in np.round(np.arange(1.0, 3.0001, 0.1), 2):
    gm3 = f3 * GM3
    cn2 = 30 * FF + gm3 / wt6
    for g2f in (1, 1.5, 2, 3):
        for cm2 in np.round(np.arange(0.1, 0.8001, 0.05), 2):
            mm = margins_of(lambda f, a=g2f * GM1, b3=gm3, c2=cn2, cm=cm2 * PF: nmc_vec(f, a, b3, c2, cm))
            if mm["pm"] >= 60 and mm["gm"] is not None and mm["gm"] >= 10:
                if best is None:
                    best = (f3, g2f, cm2)
    if best:
        break
v.assert_true("nested Miller grid finds a design", best is not None, "")
v.check("Lab 20-02.k", best[0])
v.check("Lab 20-02.l", best[1])
v.check("Lab 20-02.m", best[2])
mbest = margins_of(nmc_h(GM1, best[1] * GM1, best[0] * GM3, (25, 25, 20), 30 * FF, 30 * FF + best[0] * GM3 / wt6,
                         CL, CM1, best[2] * PF))
v.check("Lab 20-02.o", mbest["pm"])
v.check("Lab 20-02.p", mbest["gm"])
v.check("Lab 20-02.q", best[0] * GM3 / 10 / U)

# ================================================================ the lab module agrees
d = lab.design_two_stage()
v.assert_true("opamp.py design matches the independent one",
              all(abs(d[k] / x - 1) < 1e-6 for k, x in (("gm1", GM1), ("gm6", GM6), ("i6", I6), ("w6", W6),
                                                          ("c1", C1), ("r1", R1), ("r2", R2), ("w1", W1))), "")
v.assert_true("opamp.py saturation voltages match", all(abs(d[k] - x) < 1e-9 for k, x in (
    ("vdsat6", vd6), ("vdsat7", vd7), ("vdsat1", vd1), ("vdsat5", vd5))), "")
nb, db = lab.miller_tf(GM1, GM6, R1, R2, C1, CL, CC, 1 / GM6)
mlab = lab.margins(lab.poly_tf(nb, db))
v.assert_true("opamp.py margins match", abs(mlab["pm"] - mb["pm"]) < 1e-3 and abs(mlab["fc"] / mb["fc"] - 1) < 1e-5,
              f"{mlab['pm']} vs {mb['pm']}")
v.assert_true("opamp.py two-pole PM matches", abs(lab.two_pole_pm(2.0) - two_pole(2.0)[1]) < 1e-9, "")
v.assert_true("opamp.py C_c optimum matches", abs(lab.optimum_cc(lab.Spec(), lab.Choices()) / ropt.x - 1) < 1e-4, "")
v.assert_true("opamp.py CMFB cycles match", math.ceil(lab.cmfb_cycles(1, 0.25, 1e3)) == cycles(1, 0.25, 1e3), "")

sys.exit(v.finish())
