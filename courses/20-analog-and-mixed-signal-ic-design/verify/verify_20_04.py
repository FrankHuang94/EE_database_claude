#!/usr/bin/env python3
"""Verify every number in chapter 20-04 (low-dropout regulators), its problems and its lab.

Independent routes:
- the charge-based inversion V_P/V_T = 2q + ln q is solved in closed form with the Lambert W function, and the
  saturated operating point by solving the quadratic q^2 + q(1 - lambda r) - r = 0 (r = I/I_spec) rather than
  root-finding V_SG; g_m is the analytic derivative, not a finite difference;
- the dropout width follows from the triode current being linear in W (no root-finding);
- loop gain, output impedance and PSRR are built as numpy polynomial ratios; crossovers come from the roots of
  |N(jw)|^2 - |D(jw)|^2 = 0 (a polynomial in w^2) and phases from sums of arctangents, not from sampled curves;
- the linear step response is a sum of exponentials from a partial-fraction expansion (scipy.signal.residue);
- the nonlinear load step is re-derived in absolute node voltages and integrated with LSODA (the lab uses
  deviations and Radau);
- the lab module (ldo.py) is asserted to agree; ngspice confirms the loop and PSRR netlists (run_spice).
"""
from __future__ import annotations

import math
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar
from scipy.special import lambertw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import ldo as lab  # noqa: E402

v = Verifier.from_files("20-04", ROOT / "chapters" / "20-04-ldo-regulators.md",
                        ROOT / "solutions" / "20-04-solutions.md", LAB / "README.md")

KB, QE = 1.380649e-23, 1.602176634e-19
VT = KB * 300.0 / QE
MU, COX, NN, VTH, VSAT, VAP, LCH = 100e-4, 8.6e-3, 1.3, 0.45, 6e4, 8e6, 0.15e-6
LAMC = MU * VT / (VSAT * LCH)
VOUT, VREF, BETA = 1.2, 0.6, 0.5
GMA, RA, CA, GMB = 1e-3, 100e3, 0.2e-12, 2e-3
CL, ESR, RDIV, VIN = 1e-6, 5e-3, 1.2e6, 1.8
TWO_PI = 2 * math.pi


def ispec(w):
    return 2 * NN * MU * COX * (w / LCH) * VT ** 2


def q_of(vp):
    """Inverse of V_P/V_T = 2q + ln q in closed form: q = W(2 e^u)/2."""
    return float(lambertw(2 * math.exp(vp / VT)).real) / 2


def i_sat(w, vsg):
    q = q_of((vsg - VTH) / NN)
    return ispec(w) * (q * q + q) / (1 + LAMC * q)


def op_point(w, i):
    """Saturated operating point from the quadratic in q; analytic g_m."""
    r = i / ispec(w)
    b = 1 - LAMC * r
    q = (-b + math.sqrt(b * b + 4 * r)) / 2
    vsg = VTH + NN * VT * (2 * q + math.log(q))
    di_dq = ispec(w) * ((2 * q + 1) * (1 + LAMC * q) - LAMC * (q * q + q)) / (1 + LAMC * q) ** 2
    gm = di_dq / (NN * VT * (2 + 1 / q))
    return {"vsg": vsg, "gm": gm, "ic": r, "q": q}


def size(vin_min, vdo, imax):
    qs, qd = q_of((vin_min - VTH) / NN), q_of((vin_min - VTH) / NN - vdo)
    per_w = ispec(1.0) * ((qs * qs + qs) - (qd * qd + qd))
    w_long = imax / per_w
    esat = VSAT / MU
    fac = 1 + vdo / (esat * LCH)
    return w_long, fac, w_long * fac, esat


W_LONG, VSF, W, ESAT = size(1.35, 0.15, 0.1)
CG = 2 / 3 * W * LCH * COX


class Loop:
    """Loop gain L = K Rout (1 + s ESR C)/[(1 + s (Rout + ESR) C)(1 + s/pa)(1 + s/pg)(1 + s/pp)] as polynomials."""

    def __init__(self, il, cl=CL, esr=ESR, gma=GMA, ca=CA, w=W, cg=CG, extra_pole=None):
        o = op_point(w, il)
        self.gm, self.rds = o["gm"], VAP * LCH / il
        self.rl = VOUT / il
        self.rout = 1 / (1 / self.rds + 1 / self.rl + 1 / RDIV)
        self.k = gma * RA * BETA * self.gm
        self.cl, self.esr = cl, esr
        self.pa, self.pg = 1 / (RA * ca), GMB / cg
        self.zn = np.array([self.rout * esr * cl, self.rout])
        self.zd = np.array([(self.rout + esr) * cl, 1.0])
        de = np.polymul([1 / self.pa, 1.0], [1 / self.pg, 1.0])
        if extra_pole:
            de = np.polymul(de, [1 / extra_pole, 1.0])
        self.de = de
        self.ln = self.k * self.zn
        self.ld = np.polymul(self.zd, de)
        self.extra = extra_pole

    def L(self, f):
        s = 2j * math.pi * f
        return np.polyval(self.ln, s) / np.polyval(self.ld, s)

    def crossover(self):
        """Largest positive w with |N(jw)| = |D(jw)|, from polynomial roots in y = s^2 (frequency-scaled)."""
        wn = 1e6
        n = self.ln * wn ** np.arange(len(self.ln) - 1, -1, -1)
        d = self.ld * wn ** np.arange(len(self.ld) - 1, -1, -1)

        def even(p):
            pm = p * (-1.0) ** np.arange(len(p) - 1, -1, -1)
            pr = np.polymul(p, pm)
            return pr[::-1][::2][::-1]
        en, ed = even(n), even(d)
        m = max(len(en), len(ed))
        poly = np.pad(en, (m - len(en), 0)) - np.pad(ed, (m - len(ed), 0))
        ws = [math.sqrt(-y.real) * wn for y in np.roots(poly) if abs(y.imag) < 1e-6 * abs(y) and y.real < 0]
        wc = max(ws)
        wc = brentq(lambda x: abs(self.L(x / TWO_PI)) - 1, 0.999 * wc, 1.001 * wc, xtol=1e-12 * wc)
        return wc / TWO_PI

    def phase_deg(self, f):
        w = TWO_PI * f
        ph = math.atan(w * self.esr * self.cl) - math.atan(w * (self.rout + self.esr) * self.cl)
        ph -= math.atan(w / self.pa) + math.atan(w / self.pg)
        if self.extra:
            ph -= math.atan(w / self.extra)
        return math.degrees(ph)

    def margins(self):
        fc = self.crossover()
        return fc, 180 + self.phase_deg(fc)

    def l0(self):
        return self.k * self.rout

    def psrr_db(self, f, kg):
        inj = self.gm * (1 - kg) + 1 / self.rds
        s = 2j * math.pi * f
        h = inj * np.polyval(np.polymul(self.zn, self.de), s) / np.polyval(
            np.polyadd(np.polymul(self.zd, self.de), self.k * self.zn), s)
        return -20 * math.log10(abs(h))


# ------------------------------------------------------------------ Example 20-04.1 and text efficiencies
print("Example 20-04.1")
IQ = 120e-6
eff = lambda vin, il, iq=IQ, vo=VOUT: vo * il / (vin * (il + iq)) * 100  # noqa: E731
v.check("Ex 20-04.1a", eff(1.8, 0.1))
v.check("Ex 20-04.1b", eff(1.35, 0.1))
v.check("Ex 20-04.1c", eff(1.8, 100e-6))
v.check("Ex 20-04.1d", 1.2 / 1.8 * 100)
v.check("Ex 20-04.1e", 1.2 / 1.35 * 100)
v.check("Txt 20-04.n", 1.2 / 1.8 * 100)
v.check("Txt 20-04.o", 1.2 / 1.35 * 100)
v.check("Txt 20-04.p", 100e-6 / 220e-6 * 100)

# ------------------------------------------------------------------ Example 20-04.2
print("Example 20-04.2")
v.check("Ex 20-04.2a", W_LONG * 1e3)
v.check("Ex 20-04.2b", VSF)
v.check("Txt 20-04.a", VSF)
v.check("Ex 20-04.2c", W * 1e3)
v.check("Ex 20-04.2d", CG * 1e12)
v.check("Ex 20-04.2m", ESAT / 1e6)
v.check("Txt 20-04.b", ESAT / 1e6)
OP_LO, OP_HI = op_point(W, 100e-6), op_point(W, 0.1)
v.check("Ex 20-04.2e", OP_LO["vsg"])
v.check("Ex 20-04.2f", OP_HI["vsg"])
v.check("Ex 20-04.2g", OP_LO["gm"] / 100e-6)
v.check("Ex 20-04.2h", OP_HI["gm"] / 0.1)
v.check("Ex 20-04.2i", OP_LO["ic"])
v.check("Ex 20-04.2j", OP_HI["ic"])
v.check("Ex 20-04.2k", VIN - OP_LO["vsg"])
v.check("Ex 20-04.2l", VIN - OP_HI["vsg"])
v.check("Ex 20-04.2n", OP_HI["gm"] / OP_LO["gm"])
v.assert_true("closed-form operating point reproduces the current",
              abs(i_sat(W, OP_HI["vsg"]) / 0.1 - 1) < 1e-10 and abs(i_sat(W, OP_LO["vsg"]) / 100e-6 - 1) < 1e-10)
h = 1e-7
v.assert_true("analytic g_m matches a central difference",
              abs((i_sat(W, OP_HI["vsg"] + h) - i_sat(W, OP_HI["vsg"] - h)) / (2 * h) / OP_HI["gm"] - 1) < 1e-6)

# ------------------------------------------------------------------ Example 20-04.3
print("Example 20-04.3")
LO, HI = Loop(100e-6), Loop(0.1)
v.check("Ex 20-04.3a", LO.gm * 1e3)
v.check("Ex 20-04.3b", HI.gm)
v.check("Ex 20-04.3c", LO.rds / 1e3)
v.check("Ex 20-04.3d", HI.rds)
v.check("Ex 20-04.3e", LO.rout / 1e3)
v.check("Ex 20-04.3f", HI.rout)
v.check("Ex 20-04.3g", LO.l0())
v.check("Ex 20-04.3h", 20 * math.log10(LO.l0()))
v.check("Ex 20-04.3i", HI.l0())
v.check("Ex 20-04.3j", 20 * math.log10(HI.l0()))
v.check("Ex 20-04.3k", LO.rout / (1 + LO.l0()))
v.check("Ex 20-04.3l", HI.rout / (1 + HI.l0()) * 1e3)
v.check("Ex 20-04.3m", LO.rout / LO.rds / (1 + LO.l0()) * 1e3)
v.check("Ex 20-04.3n", HI.rout / HI.rds / (1 + HI.l0()) * 1e3)
DVSG = OP_HI["vsg"] - OP_LO["vsg"]
v.check("Ex 20-04.3o", DVSG)
v.check("Ex 20-04.3p", -DVSG / (GMA * RA * BETA) * 1e3)
VA_ABS = VAP * LCH


def dc_shift(i0, i1, gma=GMA):
    """Exact DC output change: the pass device carries load + divider current, with V_SD-dependent r_ds."""
    vsg0 = op_point(W, i0 + VOUT / RDIV)["vsg"]
    a = gma * RA * BETA

    def bal(x):
        return i_sat(W, vsg0 - a * x) * (1 - x / VA_ABS) - (i1 + (VOUT + x) / RDIV)
    return brentq(bal, -0.1, 0.01, xtol=1e-16)


X_DC = dc_shift(100e-6, 0.1)
v.check("Ex 20-04.3q", X_DC * 1e3)
v.check("Txt 20-04.j", -X_DC * 1e3)
v.check("Ex 20-04.6e", X_DC * 1e3)

# ------------------------------------------------------------------ Example 20-04.4
print("Example 20-04.4")
v.check("Ex 20-04.4a", HI.pa / TWO_PI / 1e6)
v.check("Ex 20-04.4b", HI.pg / TWO_PI / 1e6)
fc_lo, pm_lo = LO.margins()
fc_hi, pm_hi = HI.margins()
v.check("Ex 20-04.4c", fc_lo / 1e3)
v.check("Txt 20-04.c", fc_lo / 1e3)
v.check("Ex 20-04.4d", pm_lo)
fc, pm = Loop(1e-3).margins()
v.check("Ex 20-04.4e", fc / 1e3)
v.check("Ex 20-04.4f", pm)
fc, pm = Loop(10e-3).margins()
v.check("Ex 20-04.4g", fc / 1e3)
v.check("Ex 20-04.4h", pm)
v.check("Ex 20-04.4i", fc_hi / 1e6)
v.check("Txt 20-04.d", fc_hi / 1e6)
v.check("Ex 20-04.4j", pm_hi)
fc, pm = Loop(100e-6, cl=0.1e-6).margins()
v.check("Ex 20-04.4k", fc / 1e3)
v.check("Ex 20-04.4l", pm)
fc, pm = Loop(0.1, cl=0.1e-6).margins()
v.check("Ex 20-04.4m", fc / 1e6)
v.check("Ex 20-04.4n", pm)
v.check("Txt 20-04.e", pm)
fc, pm = Loop(100e-6, cl=10e-6).margins()
v.check("Ex 20-04.4o", fc / 1e3)
v.check("Ex 20-04.4p", pm)
fc, pm = Loop(0.1, cl=10e-6).margins()
v.check("Ex 20-04.4q", fc / 1e3)
v.check("Ex 20-04.4r", pm)
v.check("Ex 20-04.4s", 1 / (TWO_PI * ESR * 10e-6) / 1e6)
v.assert_true("crossover from polynomial roots has |L| = 1", abs(abs(HI.L(fc_hi)) - 1) < 1e-9)
v.assert_true("arctangent phase matches the complex angle",
              abs(math.degrees(np.angle(HI.L(fc_hi))) - HI.phase_deg(fc_hi)) < 1e-9)

# ------------------------------------------------------------------ Example 20-04.5
print("Example 20-04.5")
for key, f, kg in (("5a", 1e-3, 1.0), ("5b", 1e6, 1.0), ("5c", 1e7, 1.0), ("5d", 1e-3, 0.0), ("5e", 1e6, 0.0),
                   ("5f", 1e7, 0.0)):
    v.check(f"Ex 20-04.{key}", HI.psrr_db(f, kg))
v.check("Ex 20-04.5g", LO.psrr_db(1e-3, 1.0))
v.check("Txt 20-04.f", HI.psrr_db(1e-3, 1.0))
v.check("Txt 20-04.g", HI.psrr_db(1e-3, 0.0))
v.check("Ex 20-04.5h", 20 * math.log10((HI.gm + 1 / HI.rds) * HI.rds))
v.check("Ex 20-04.5i", (HI.gm + 1 / HI.rds) * HI.rds)
v.check("Ex 20-04.5j", HI.gm * HI.rds)
v.assert_true("DC PSRR(k=1) equals the line regulation",
              abs(10 ** (-HI.psrr_db(1e-3, 1.0) / 20) - HI.rout / HI.rds / (1 + HI.l0())) < 1e-9)

# ------------------------------------------------------------------ Example 20-04.6: nonlinear load step


def nonlinear_step(i0, i1, cl=CL, t_end=1.5e-6, tr=1e-9):
    """Absolute node voltages: V_out, error-amplifier output V_E, gate V_G. The error amplifier is biased so that
    V_E = V_G0 when V_out = 1.2 V (the reference absorbs its static error); the gate buffer drives C_g."""
    vg0 = VIN - op_point(W, i0 + VOUT / RDIV)["vsg"]

    def iload(t):
        return i0 + (i1 - i0) * min(max(t / tr, 0.0), 1.0)

    def rhs(t, st):
        vo, ve, vg = st
        ip = i_sat(W, VIN - vg) * (1 + ((VIN - vo) - (VIN - VOUT)) / VA_ABS)
        return [(ip - iload(t) - vo / RDIV) / cl,
                (GMA * (BETA * vo - VREF) + (vg0 - ve) / RA) / CA,
                GMB * (ve - vg) / CG]
    sol = solve_ivp(rhs, (0, t_end), [VOUT, vg0, vg0], method="LSODA", max_step=1e-9, rtol=1e-9, atol=1e-13,
                    dense_output=True)
    t = np.linspace(0, t_end, 150001)
    vo = sol.sol(t)[0] - VOUT
    i = int(np.argmin(vo))
    lo, hi = t[max(i - 2, 0)], t[min(i + 2, len(t) - 1)]
    res = minimize_scalar(lambda x: sol.sol(x)[0], bounds=(lo, hi), method="bounded",
                          options={"xatol": 1e-14})
    return res.fun - VOUT, res.x, vo[-1]


print("Example 20-04.6")
v.check("Ex 20-04.6a", 0.0999 / (TWO_PI * fc_hi * CL) * 1e3)
v.check("Txt 20-04.h", 0.0999 / (TWO_PI * fc_hi * CL) * 1e3)
v.check("Ex 20-04.6b", 0.1 * ESR * 1e3)
v.check("Txt 20-04.i", 0.1 * ESR * 1e3)
vmin, tmin, vend = nonlinear_step(100e-6, 0.1)
v.check("Ex 20-04.6c", vmin * 1e3)
v.check("Ex 20-04.6d", tmin * 1e6)
v.assert_true("nonlinear step settles to the exact DC shift", abs(vend - X_DC) < 5e-5, f"{vend} vs {X_DC}")
v.check("Ex 20-04.6f", 100e-12 * 0.1 / 0.1 * 1e9)
v.check("Txt 20-04.m", 100e-12 * 0.1 / 0.1 * 1e9)
v.check("Txt 20-04.k", OP_LO["gm"] / (TWO_PI * 100e-12) / 1e6)
v.check("Txt 20-04.l", OP_HI["gm"] / (TWO_PI * 100e-12) / 1e9)

# ------------------------------------------------------------------ lab
print("Lab 20-04")
w100 = size(1.3, 0.10, 0.1)
v.check("Lab 20-04.a", w100[2] * 1e3)
v.check("Lab 20-04.b", nonlinear_step(1e-3, 0.1)[0] * 1e3)
v.check("Lab 20-04.c", nonlinear_step(10e-3, 0.1)[0] * 1e3)
vmin01, tmin01, vend01 = nonlinear_step(100e-6, 0.1, cl=0.1e-6, t_end=1e-6)
v.check("Lab 20-04.d", vmin01 * 1e3)
v.check("Lab 20-04.e", tmin01 * 1e9)
v.assert_true("0.1 uF step settles to the same DC shift", abs(vend01 - X_DC) < 5e-5, f"{vend01} vs {X_DC}")

# ------------------------------------------------------------------ problems
print("Problems")
# 1
v.check("20-04.1a", eff(1.2, 0.05, 30e-6, 1.0))
v.check("20-04.1b", 0.2 * 0.05 * 1e3)
v.check("20-04.1c", 3.3 * 0.05003 * 1e3)
v.check("20-04.1d", eff(3.3, 0.05, 30e-6, 1.0))
v.check("20-04.1e", 2.3 * 0.05 * 1e3)
v.check("20-04.1f", 0.05 / 0.9 * 1e3)
v.check("20-04.1g", 1.2 * 0.05003 * 1e3)
# 2
v.check("20-04.2a", 1.2 + 0.75)
v.check("20-04.2b", 1.2 + 0.75 + 0.15)
v.check("20-04.2c", 1.2 / 2.1 * 100)
v.check("20-04.2d", 1.2 / 1.35 * 100)
# 3
v.check("20-04.3a", w100[0] * 1e3)
v.check("20-04.3b", w100[1])
v.check("20-04.3c", w100[2] * 1e3)
v.check("20-04.3d", w100[2] / W)
cg100 = 2 / 3 * w100[2] * LCH * COX
v.check("20-04.3e", cg100 * 1e12)
v.check("20-04.3f", GMB / (TWO_PI * cg100) / 1e6)
v.check("20-04.3g", 0.10 / 0.15)
# 4
M10 = Loop(10e-3)
op10 = op_point(W, 10e-3)
v.check("20-04.4a", op10["vsg"])
v.check("20-04.4b", op10["gm"] / 10e-3)
v.check("20-04.4c", M10.gm * 1e3)
v.check("20-04.4d", M10.rds)
v.check("20-04.4e", M10.rout)
v.check("20-04.4f", M10.l0())
v.check("20-04.4g", 20 * math.log10(M10.l0()))
v.check("20-04.4h", M10.rout / (1 + M10.l0()))
v.check("20-04.4i", M10.rout / M10.rds / (1 + M10.l0()) * 1e3)
# 5
a_req = DVSG / (BETA * 5e-3)
v.check("20-04.5a", a_req)
v.check("20-04.5b", 20 * math.log10(a_req))
v.check("20-04.5c", a_req / RA * 1e3)
fc, pm = Loop(100e-6, gma=a_req / RA).margins()
v.check("20-04.5d", fc / 1e3)
v.check("20-04.5e", pm)
fc, pm = Loop(0.1, gma=a_req / RA).margins()
v.check("20-04.5f", fc / 1e6)
v.check("20-04.5g", pm)
# 6
cmin = brentq(lambda c: Loop(0.1, cl=c).margins()[1] - 60, 0.1e-6, 1e-6, xtol=1e-15)
fc6 = Loop(0.1, cl=cmin).margins()[0]
v.check("20-04.6a", cmin * 1e6)
v.check("20-04.6b", fc6 / 1e6)
v.check("20-04.6c", HI.k / (TWO_PI * cmin) / 1e6)
v.check("20-04.6d", math.hypot(1, fc6 / (HI.pa / TWO_PI)))
# 7
v.check("20-04.7a", 1 / (TWO_PI * 0.5 * 1e-6) / 1e3)
fc, pm = Loop(0.1, esr=0.5).margins()
v.check("20-04.7b", fc / 1e6)
v.check("20-04.7c", pm)
l7 = Loop(0.1, esr=0.5)
plateau = abs(l7.k * np.polyval(l7.zn, 2j * math.pi * 1e11) / np.polyval(l7.zd, 2j * math.pi * 1e11))   # |K Z_out| far above the zero
v.check("20-04.7d", plateau)
v.assert_true("plateau is K (R_out || R_ESR)", abs(plateau - l7.k * l7.rout * 0.5 / (l7.rout + 0.5)) < 1e-6)
PP = TWO_PI * 30e6
fc_a, pm_a = Loop(0.1, extra_pole=PP).margins()
v.check("20-04.7e", fc_a / 1e6)
v.check("20-04.7f", pm_a)
fc, pm = Loop(0.1, esr=0.5, extra_pole=PP).margins()
v.check("20-04.7g", fc / 1e6)
v.check("20-04.7h", pm)
v.check("20-04.7i", pm_hi - pm_a)
# 8
r1, r0 = HI.psrr_db(2e6, 1.0), HI.psrr_db(2e6, 0.0)
v.check("20-04.8a", r1)
v.check("20-04.8b", 20e-3 * 10 ** (-r1 / 20) * 1e6)
v.check("20-04.8c", r0)
v.check("20-04.8d", 20e-3 * 10 ** (-r0 / 20) * 1e6)
v.check("20-04.8e", 10 ** ((r1 - r0) / 20))
# 9
ref_e, div_e, off_e, load_e = 0.005 * 1.2, 0.002 * 1.2, 2e-3 / BETA, 13.41e-3
v.check("20-04.9a", ref_e * 1e3)
v.check("20-04.9b", div_e * 1e3)
v.check("20-04.9c", off_e * 1e3)
v.check("20-04.9d", (ref_e + div_e + off_e + load_e) * 1e3)
v.check("20-04.9e", (ref_e + div_e + off_e + load_e) / 1.2 * 100)
rss = math.sqrt(ref_e ** 2 + div_e ** 2 + off_e ** 2)
v.check("20-04.9f", rss * 1e3)
v.check("20-04.9g", (rss + load_e) * 1e3)
# 10: linear step of 10 mA at 100 mA by partial fractions
v.check("20-04.10a", 0.01 / (TWO_PI * fc_hi * CL) * 1e3)
v.check("20-04.10b", 0.01 * ESR * 1e3)
zcl0 = HI.rout / (1 + HI.l0())
v.check("20-04.10c", 0.01 * zcl0 * 1e3)
tn = 1e-7                                      # time scale for conditioning
num = np.polymul(HI.zn, HI.de) * (1 / tn) ** np.arange(len(np.polymul(HI.zn, HI.de)) - 1, -1, -1)
den = np.polyadd(np.polymul(HI.zd, HI.de), HI.k * HI.zn)
den = den * (1 / tn) ** np.arange(len(den) - 1, -1, -1)
rr, pp, _ = signal.residue(num, np.polymul(den, [1.0, 0.0]))
tt = np.linspace(0, 3e-6, 300001)
vt = 0.01 * np.real(sum(r * np.exp(p * tt / tn) for r, p in zip(rr, pp)))
fin = 0.01 * zcl0
v.check("20-04.10d", vt.max() * 1e3)
v.check("20-04.10e", (vt.max() / fin - 1) * 100)
t90 = tt[int(np.argmax(vt >= 0.9 * fin))]
v.check("20-04.10f", t90 * 1e9)
v.check("20-04.10g", 2.3 / (TWO_PI * fc_hi) * 1e9)
v.check("20-04.10h", 0.01 * ESR / fin * 100)
v.assert_true("partial-fraction step reaches the DC value", abs(vt[-1] / fin - 1) < 1e-6)
v.assert_true("ESR step at t = 0+", abs(vt[1] - 0.01 * ESR * HI.rout / (HI.rout + ESR)) < 2e-6)
# 11
op1 = op_point(W, 1e-3)
p2 = op1["gm"] / (TWO_PI * 200e-12)
v.check("20-04.11a", op1["gm"] * 1e3)
v.check("20-04.11b", p2 / 1e6)
v.check("20-04.11c", p2 * math.tan(math.radians(30)) / 1e6)
tr11 = 200e-12 * 0.06 / 0.02
v.check("20-04.11d", tr11 * 1e9)
v.check("20-04.11e", 1 / (TWO_PI * tr11) / 1e6)
# 12
iu, fclk, co = 0.5e-3, 100e6, 100e-9
v.check("20-04.12a", iu / (fclk * co) * 1e3)
v.check("20-04.12b", 0.1 / iu)
t12 = 0.01 / (iu * fclk)
v.check("20-04.12c", t12 * 1e6)
v.check("20-04.12d", 0.5 * 0.01 * t12 / co * 1e3)
# 13
ls, la = 1.8 * 6e-6, 1.8 * 3.001e-3
bs, ba = 0.9 * 5e-6 / 0.6, 0.9 * 3e-3 / 0.85
avg = lambda s_, a_: 0.99 * s_ + 0.01 * a_  # noqa: E731
v.check("20-04.13a", ls * 1e6)
v.check("20-04.13b", la * 1e3)
v.check("20-04.13c", avg(ls, la) * 1e6)
v.check("20-04.13d", bs * 1e6)
v.check("20-04.13e", ba * 1e3)
v.check("20-04.13f", avg(bs, ba) * 1e6)
v.check("20-04.13g", avg(ls, la) / avg(bs, ba))
v.check("20-04.13h", 0.9 * 3e-3 / la * 100)
v.check("20-04.13i", 0.9 * 5e-6 / ls * 100)
# 14
v.check("20-04.14a", 1 / (TWO_PI * RA * 2e-12) / 1e3)
fc, pm = Loop(100e-6, ca=2e-12).margins()
v.check("20-04.14b", fc / 1e3)
v.check("20-04.14c", pm)
S14 = Loop(0.1, ca=2e-12)
fc, pm = S14.margins()
v.check("20-04.14d", fc / 1e6)
v.check("20-04.14e", pm)
v.check("20-04.14f", S14.psrr_db(1e5, 1.0))
v.check("20-04.14g", S14.psrr_db(1e6, 1.0))
v.check("20-04.14h", HI.psrr_db(1e5, 1.0))
v.check("20-04.14i", HI.psrr_db(1e6, 1.0))
v.check("20-04.14j", HI.psrr_db(1e6, 1.0) - S14.psrr_db(1e6, 1.0))

# ------------------------------------------------------------------ agreement with the lab module
print("Lab module agreement")
reg = lab.design()
v.assert_true("ldo.py width matches", abs(reg.w / W - 1) < 1e-9, f"{reg.w} vs {W}")
lp, *_ = reg.transfer(0.1)
m = lab.margins(lp)
v.assert_true("ldo.py full-load margins match", abs(m["fc"] / fc_hi - 1) < 1e-6 and abs(m["pm"] - pm_hi) < 1e-4,
              f"{m} vs {fc_hi}, {pm_hi}")
_, _, _, pinv, _ = replace(reg, k_gate=0.0).transfer(0.1)
v.assert_true("ldo.py PSRR matches", abs(-20 * math.log10(abs(pinv(2j * math.pi * 1e6))) - HI.psrr_db(1e6, 0.0)) < 1e-6)
st = lab.load_step_droop(reg, 0.1, 0.01)
v.assert_true("ldo.py linear step matches", abs(st["droop"] - vt.max()) < 1e-8, f"{st['droop']} vs {vt.max()}")

sys.exit(v.finish())
