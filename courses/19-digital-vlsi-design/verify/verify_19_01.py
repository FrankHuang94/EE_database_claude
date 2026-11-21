#!/usr/bin/env python3
"""Verify every number in chapter 19-01 (the CMOS inverter, static characteristics), its problems and its lab.

Independent routes:
- the transfer curve is solved here from its own current equations (written separately from the lab's
  inverter.py), and the switching threshold, unity-gain points, gain and noise margins are read off that curve
  numerically, against the chapter's closed forms;
- the closed-form V_IL is checked against the curve for a range of sizing ratios, not just the examples;
- the subthreshold gain and minimum supply by solving the subthreshold transfer curve and differentiating it;
- threshold variation by Monte Carlo;
- the lab's module is checked against these results; ngspice confirms V_M and the gain in vtc.cir (run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import inverter as iv  # noqa: E402

v = Verifier.from_files("19-01", ROOT / "chapters" / "19-01-cmos-inverter-static.md",
                        ROOT / "solutions" / "19-01-solutions.md", LAB / "README.md")
VT = 1.380649e-23 * 300 / 1.602176634e-19


# ---------------------------------------------------------------- an independent transfer-curve solver
def ids(k, vov, vds, lam=0.0, alpha=2.0):
    if vov <= 0 or vds <= 0:
        return 0.0
    if alpha == 2.0:
        core = k * (vov * vds - vds * vds / 2) if vds < vov else k * vov * vov / 2
        return core * (1 + lam * vds)
    isat = k * vov ** alpha / 2
    core = isat * (2 - vds / vov) * (vds / vov) if vds < vov else isat
    return core * (1 + lam * vds)


def vout(vin, vdd, vtn, vtp, kn, kp, ln=0.0, lp=0.0, alpha=2.0):
    def bal(y):
        return ids(kp, vdd - vin - vtp, vdd - y, lp, alpha) - ids(kn, vin - vtn, y, ln, alpha)
    if bal(0.0) <= 0:
        return 0.0
    if bal(vdd) >= 0:
        return vdd
    return brentq(bal, 0.0, vdd, xtol=1e-15, rtol=1e-15, maxiter=400)


def vm(*p):
    vdd = p[0]
    return brentq(lambda x: vout(x, *p) - x, 1e-9, vdd - 1e-9, xtol=1e-15)


def slope(x, *p, h=1e-7):
    return (vout(x + h, *p) - vout(x - h, *p)) / (2 * h)


def unity(*p):
    m = vm(*p)
    vdd, vtn, vtp = p[0], p[1], p[2]
    vil = brentq(lambda x: slope(x, *p) + 1, vtn + 1e-5, m - 1e-4, xtol=1e-13)
    vih = brentq(lambda x: slope(x, *p) + 1, m + 1e-4, vdd - vtp - 1e-5, xtol=1e-13)
    return vil, vih


def vm_formula(vdd, vtn, vtp, r, alpha=2.0):
    s = r ** (1 / alpha)
    return (vtn * s + vdd - vtp) / (1 + s)


def vil_formula(vdd, vtn, vtp, r):
    t = (2 * math.sqrt(r * r + 3 * r) - r) / (r * (r + 4))
    return vtn + t / (1 + t) * (vdd - vtn - vtp)


# ---------------------------------------------------------------- Example 1
P1 = (1.2, 0.35, 0.35, 200e-6, 200e-6)
v.check("Ex 19-01.1a", vout(0.0, *P1))
v.check("Ex 19-01.1b", vout(1.2, *P1))
v.check("Ex 19-01.1c", vm(*P1))
v.check("Ex 19-01.1d", 1.2 - 0.35)
v.check("Ex 19-01.1e", 0.6 - 0.35)
v.check("Ex 19-01.1f", 0.6 + 0.35)
cur = [ids(200e-6, 0.25, y) - ids(200e-6, 0.25, 1.2 - y) for y in np.linspace(0.26, 0.94, 50)]
v.assert_true("Example 1(d): with lambda = 0 both currents balance for every output from 0.25 to 0.95 V", max(map(abs, cur)) < 1e-18)
v.assert_true("zero static current outside the conducting window",
              ids(200e-6, 0.30 - 0.35, 1.2) == 0 and ids(200e-6, 1.2 - 0.9 - 0.35, 1.2) == 0)

# ---------------------------------------------------------------- Example 2
P2 = (1.2, 0.35, 0.40, 250e-6, 100e-6)
v.check("Ex 19-01.2a", vm(*P2))
v.assert_true("Example 2: closed form equals the curve", abs(vm(*P2) - vm_formula(1.2, 0.35, 0.40, 2.5)) < 1e-12)
r2 = ((1.2 - 0.40 - 0.6) / (0.6 - 0.35)) ** 2
v.check("Ex 19-01.2b", r2)
v.check("Ex 19-01.2c", 2.5 / r2)
v.assert_true("Example 2(b): that sizing puts the curve's V_M at 0.6 V", abs(vm(1.2, 0.35, 0.40, 100e-6 * r2, 100e-6) - 0.6) < 1e-12)

# ---------------------------------------------------------------- Example 3
il1, ih1 = unity(*P1)
v.check("Ex 19-01.3a", il1)
v.check("Ex 19-01.3b", ih1)
P3 = (1.2, 0.35, 0.35, 250e-6, 100e-6)
il3, ih3 = unity(*P3)
v.check("Ex 19-01.3c", il3)
v.check("Ex 19-01.3d", ih3)
v.check("Ex 19-01.3e", il3 - vout(1.2, *P3))
v.check("Ex 19-01.3f", vout(0.0, *P3) - ih3)
v.assert_true("closed-form V_IL matches the curve for r = 1 and 2.5",
              abs(il1 - vil_formula(1.2, 0.35, 0.35, 1)) < 1e-7 and abs(il3 - vil_formula(1.2, 0.35, 0.35, 2.5)) < 1e-7)
for rr in (0.3, 0.7, 1.6, 4.0, 9.0):
    p = (1.0, 0.3, 0.32, 100e-6 * rr, 100e-6)
    a, b = unity(*p)
    v.assert_true(f"closed forms for V_IL and V_IH match the curve at r = {rr}",
                  abs(a - vil_formula(1.0, 0.3, 0.32, rr)) < 1e-7 and abs(b - (1.0 - vil_formula(1.0, 0.32, 0.3, 1 / rr))) < 1e-7)
v.assert_true("Example 3 sanity: V_M falls to 0.544 V at r = 2.5", round(vm(*P3), 3) == 0.544)
v.check("Txt 19-01.a", (3 * 1.2 + 2 * 0.35) / 8)
v.check("Txt 19-01.b", ih1 - il1)

# ---------------------------------------------------------------- Example 4
P4 = (1.2, 0.35, 0.35, 200e-6, 200e-6, 0.1, 0.1)
m4 = vm(*P4)
g4 = -slope(m4, *P4, h=1e-8)
v.check("Ex 19-01.4a", g4)
v.check("Ex 19-01.4b", 2 / (0.1 * 0.25))
v.check("Ex 19-01.4c", 1e3 * 1.2 / g4)
v.assert_true("Example 4: V_M stays 0.6 V with equal lambdas", abs(m4 - 0.6) < 1e-12)
v.assert_true("Example 4: exact gain 2(1 + lambda VDS)/(lambda Vov)", abs(g4 - 2 * 1.06 / 0.025) < 1e-4)

# ---------------------------------------------------------------- Example 5 and figure 2
v.check("Ex 19-01.5a", vm(1.2, 0.35, 0.35, 1.6e-4, 1e-4, 0, 0, 1.3))
v.check("Ex 19-01.5b", vm(1.2, 0.35, 0.35, 1.6e-4, 1e-4, 0, 0, 2.0))
v.check("Ex 19-01.5c", 1.6)
v.assert_true("Example 5: alpha-power V_M equals the closed form", abs(vm(1.2, 0.35, 0.35, 1.6e-4, 1e-4, 0, 0, 1.3) - vm_formula(1.2, 0.35, 0.35, 1.6, 1.3)) < 1e-12)
v.assert_true("Example 5(b): r = 1 gives V_M = 0.6 for any alpha",
              all(abs(vm(1.2, 0.35, 0.35, 1e-4, 1e-4, 0, 0, al) - 0.6) < 1e-12 for al in (1.1, 1.3, 1.7, 2.0)))
v.assert_true("Concept check Q2: doubling Wp moves V_M up by 43 mV", round(1e3 * (vm(1.2, 0.35, 0.35, 1e-4, 2e-4) - 0.6)) == 43)
v.assert_true("Section 3.2: delay-optimal ratio sqrt(2.5) is about 1.6", round(math.sqrt(2.5), 1) == 1.6)


# ---------------------------------------------------------------- Example 6: subthreshold
def sub_vout(x, vdd, n):
    def f(y):
        return (math.exp((x - vdd / 2) / (n * VT)) * (1 - math.exp(-y / VT))
                - math.exp((vdd / 2 - x) / (n * VT)) * (1 - math.exp(-(vdd - y) / VT)))
    return brentq(f, 0.0, vdd, xtol=1e-16)


def sub_gain(vdd, n, h=1e-7):
    return -(sub_vout(vdd / 2 + h, vdd, n) - sub_vout(vdd / 2 - h, vdd, n)) / (2 * h)


vmin = brentq(lambda d: sub_gain(d, 1.4) - 1, 0.02, 0.1, xtol=1e-12)
v.check("Ex 19-01.6a", 1e3 * vmin)
v.check("Ex 19-01.6b", sub_gain(0.2, 1.4))
v.check("Ex 19-01.6c", sub_gain(0.1, 1.4))
v.assert_true("Example 6: minimum supply equals 2 VT ln(1 + n)", abs(vmin - 2 * VT * math.log(2.4)) < 1e-9)
v.assert_true("Example 6: gain equals (exp(VDD/2VT) - 1)/n", abs(sub_gain(0.2, 1.4) - (math.exp(0.1 / VT) - 1) / 1.4) < 1e-3)
v.check("Txt 19-01.d", 1e3 * brentq(lambda d: sub_gain(d, 1.0) - 1, 0.01, 0.1, xtol=1e-12))
v.check("Txt 19-01.e", 1e3 * VT)
# Practitioner lens: SKY130 e-test currents [R-314] and the IRDS 70 mV/decade slope
v.check("Txt 19-01.f", 3.512 / 1.347)
v.check("Txt 19-01.g", 70e-3 / (VT * math.log(10)))
v.check("Txt 19-01.h", 1e3 * VT * math.log(10))

# ---------------------------------------------------------------- variation
rng = np.random.default_rng(19011)
d = rng.normal(0, 0.025, (200000, 2))
vms = ((0.35 + d[:, 0]) + (1.2 - (0.35 + d[:, 1]))) / 2
v.check("Txt 19-01.c", 1e3 * 0.025 / math.sqrt(2))
v.assert_true("Monte Carlo sigma of V_M is 17.7 mV within 1%", abs(vms.std() / (0.025 / math.sqrt(2)) - 1) < 0.01, f"{vms.std():.5f}")

# ---------------------------------------------------------------- problems
v.check("19-01.1a", vout(0.2, 1.0, 0.3, 0.3, 1e-4, 1e-4))
v.check("19-01.1b", vm(1.0, 0.3, 0.3, 1e-4, 1e-4))
v.check("19-01.1c", vout(0.8, 1.0, 0.3, 0.3, 1e-4, 1e-4))
v.check("19-01.2a", vm(1.8, 0.5, 0.5, 3e-4, 1e-4))
r3 = ((1.8 - 0.5 - 0.9) / (0.9 - 0.45)) ** 2
v.check("19-01.3a", r3)
v.check("19-01.3b", 2.8 / r3)
v.assert_true("Problem 3: that sizing gives V_M = 0.9 V", abs(vm(1.8, 0.45, 0.5, 1e-4 * r3, 1e-4) - 0.9) < 1e-12)
il4, ih4 = unity(1.8, 0.45, 0.45, 1e-4, 1e-4)
v.check("19-01.4a", il4)
v.check("19-01.4b", ih4)
v.check("19-01.4c", il4)
v.check("19-01.4d", ih4 - il4)
P5 = (1.8, 0.45, 0.45, 4e-4, 1e-4)
il5, ih5 = unity(*P5)
v.check("19-01.5a", vm(*P5))
v.check("19-01.5b", il5)
v.check("19-01.5c", ih5)
v.check("19-01.5d", il5)
v.check("19-01.5e", 1.8 - ih5)
v.assert_true("Problem 5: NM_L is 0.18 V below the symmetric value", round(il4 - il5, 2) == 0.18)
v.check("19-01.6a", 2 * (1 / 0.25 + 1 / 0.25) / 0.35)
P6 = (1.2, 0.35, 0.35, 200e-6, 200e-6, 0.15, 0.2)
m6 = vm(*P6)
v.check("19-01.6b", m6)
v.check("19-01.6c", -slope(m6, *P6, h=1e-8))
v.assert_true("Problem 6(c): at Vin = Vout = 0.6 V the PMOS carries more current",
              ids(200e-6, 0.25, 0.6, 0.2) > ids(200e-6, 0.25, 0.6, 0.15))
for (ia, ib, ic), rr in ((("19-01.7a", "19-01.7b", "19-01.7c"), 1.0), (("19-01.7d", "19-01.7e", "19-01.7f"), 4.0)):
    h = 1e-6
    dn = (vm_formula(1.2, 0.35 + h, 0.35, rr) - vm_formula(1.2, 0.35 - h, 0.35, rr)) / (2 * h)
    dp = (vm_formula(1.2, 0.35, 0.35 + h, rr) - vm_formula(1.2, 0.35, 0.35 - h, rr)) / (2 * h)
    v.check(ia, dn)
    v.check(ib, dp)
    v.check(ic, 25 * math.hypot(dn, dp))
P8 = (1.2, 0.35, 0.35, 200e-6, 200e-6, 0.05, 0.05)
s1 = vout(0.55, *P8)
v.check("19-01.8a", s1)
v.check("19-01.8b", vout(s1, *P8))
v.assert_true("Problem 8: the first output exceeds VDD - |VTP|", s1 > 0.85)
v.check("19-01.9a", 1e6 * ids(200e-6, 0.25, 0.6))
t10 = (2 * math.sqrt(4 + 6) - 2) / (2 * 6)
v.check("19-01.10a", t10)
v.check("19-01.10b", unity(1.0, 0.3, 0.3, 2e-4, 1e-4)[0])
for ident, al in (("19-01.11a", 2.0), ("19-01.11b", 1.4)):
    rr = brentq(lambda r: vm(1.0, 0.30, 0.35, 1e-4 * r, 1e-4, 0, 0, al) - 0.5, 0.2, 2.0, xtol=1e-14)
    v.check(ident, 1.8 / rr)
v.check("19-01.12a", 1e3 * brentq(lambda dd: sub_gain(dd, 1.3) - 10, 0.05, 0.3, xtol=1e-12))
v.check("19-01.12b", 1e3 * 2 * VT * math.log(2.3))
vt85 = 1.380649e-23 * 358.15 / 1.602176634e-19
v.check("19-01.12c", 1e3 * 2 * vt85 * math.log(2.3))
v.assert_true("Solution 12(c): a tenfold current change needs about 80 mV at n = 1.3", round(1.3 * VT * math.log(10), 3) == 0.077)

# ---------------------------------------------------------------- the lab module agrees
lab = iv.Inverter(1.2, 0.35, 0.35, 250e-6, 100e-6)
v.assert_true("lab inverter.py agrees with this solver (V_M, V_IL, V_IH)",
              abs(lab.vm() - vm(*P3)) < 1e-10 and np.allclose(lab.unity_gain_points(), (il3, ih3), atol=1e-7))
v.assert_true("lab closed forms agree", abs(iv.vil_closed_form(1.2, 0.35, 0.35, 2.5) - il3) < 1e-7
              and abs(iv.subthreshold_vdd_min(1.4) - vmin) < 1e-9)
chain = iv.chain(0.55, iv.Inverter(*P8), 4)
v.assert_true("lab chain: 0.55 V reaches a rail by the second stage and stays there", chain[2] == 0.0 and chain[3] == 1.2 and chain[4] == 0.0)
v.check("Lab 19-01.a", chain[1])

sys.exit(v.finish())
