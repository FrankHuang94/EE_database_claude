#!/usr/bin/env python3
"""Verify every number in chapter 10-02 (MOSFET DC operation and biasing), its solutions and lab.

Independent routes:
- every operating point is found by root finding on the nodal equations with a single continuous
  three-region MOSFET function (cutoff, triode, saturation chosen inside the model from the voltages), so
  the solver is never told the region; the region is then read off the solution and asserted;
- sensitivities by re-solving at shifted thresholds and by numerical differentiation of the solved
  current, not from the 1/(1 + g_m R_S) formula;
- the body-effect bias by a two-variable root finder (fsolve) on the source voltage and threshold together;
- the lab's Monte Carlo by seeded sampling.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, fsolve

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("10-02", COURSE / "chapters" / "10-02-mosfet-dc-operation-and-biasing.md",
                        COURSE / "solutions" / "10-02-solutions.md",
                        COURSE / "labs" / "10-02-lab" / "README.md")


def ids(vgs, vds, k, vt, lam=0.0):
    """NMOS drain current, square law with m = 1; region decided from the voltages."""
    vov = vgs - vt
    if vov <= 0:
        return 0.0
    if vds < vov:
        return k * (vov * vds - vds**2 / 2)
    return 0.5 * k * vov**2 * (1 + lam * vds)


def region(vgs, vds, vt):
    vov = vgs - vt
    return "cutoff" if vov <= 0 else ("triode" if vds < vov else "saturation")


def ddx(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)


# ------------------------------------------------------------------ data-sheet values (quoted, R-177)
for k_, val in (("T 10-02.a", 0.8), ("T 10-02.b", 1.5), ("T 10-02.c", 1.1), ("T 10-02.d", 1.8), ("T 10-02.e", -2),
                ("T 10-02.f", 1.19), ("T 10-02.g", 0.84), ("T 10-02.h", 0.7), ("T 10-02.i", 1.1), ("T 10-02.j", 2),
                ("T 10-02.k", 52)):
    v.check(k_, val)

# ------------------------------------------------------------------ Example 1
k1, vt1, vdd = 2e-3, 0.5, 3.3
for rd, keys in ((2e3, ("Ex 10-02.1a", "Ex 10-02.1b")), (12e3, None)):
    vd = brentq(lambda x: ids(1.0, x, k1, vt1) - (vdd - x) / rd, 0, vdd, xtol=1e-14)
    if keys:
        v.check(keys[0], (vdd - vd) / rd * 1e3)
        v.check(keys[1], vd)
        v.assert_true("Example 1(a) is saturated", region(1.0, vd, vt1) == "saturation")
    else:
        v.check("Ex 10-02.1e", vd)
        v.check("Ex 10-02.1f", (vdd - vd) / rd * 1e3)
        v.assert_true("Example 1(b) is in triode", region(1.0, vd, vt1) == "triode")
v.check("Ex 10-02.1c", 1.0 - vt1)
v.check("Ex 10-02.1d", vdd - 12e3 * 0.5 * k1 * 0.25)
v.check("Ex 10-02.1g", brentq(lambda rd: (vdd - rd * ids(1.0, vdd, k1, vt1)) - (1.0 - vt1), 1e3, 1e5) / 1e3)

# ------------------------------------------------------------------ Example 2 (PMOS: mirror the NMOS function)
kp, vtp = 1e-3, 0.5
vsd = brentq(lambda x: ids(1.2, x, kp, vtp) - (3.3 - x) / 4e3, 0, 3.3, xtol=1e-14)   # V_D = 3.3 - V_SD
v.check("Ex 10-02.2a", 1.2 - vtp)
v.check("Ex 10-02.2b", ids(1.2, vsd, kp, vtp) * 1e3)
v.check("Ex 10-02.2c", 3.3 - vsd)
v.check("Ex 10-02.2d", vsd)
v.assert_true("Example 2 PMOS is saturated", region(1.2, vsd, vtp) == "saturation")


# ------------------------------------------------------------------ Example 3: divider + R_S, solved as a 2-node circuit
def bias3(vt, k=4e-3, rs=1e3, rd=2e3, vg=2.0, vdd=5.0):
    """Source node by root finding, assuming only that the drain is high enough (checked by the caller);
    then the drain node from the drain resistor."""
    vs = brentq(lambda x: ids(vg - x, vdd, k, vt) * rs - x, 0, vg, xtol=1e-15)
    i = vs / rs
    return vs, vdd - rd * i, i


v.check("Ex 10-02.3a", 5.0 * 2e6 / 5e6)
vs3, vd3, i3 = bias3(0.5)
v.check("Ex 10-02.3b", 2.0 - vs3)
v.check("Ex 10-02.3c", 2.0 - vs3 - 0.5)
v.check("Ex 10-02.3d", i3 * 1e3)
v.check("Ex 10-02.3e", vs3)
v.check("Ex 10-02.3f", vd3)
v.check("Ex 10-02.3g", vd3 - vs3)
v.assert_true("Example 3 is saturated", region(2.0 - vs3, vd3 - vs3, 0.5) == "saturation")
roots = np.roots([0.5 * 4e-3 * 1e3, 1 - 2 * 0.5 * 4e-3 * 1e3 * 0.5, 0.5 * 4e-3 * 1e3 * 0.25 - 2.0])
v.check("Ex 10-02.3h", min(roots))
gm3 = ddx(lambda vgs: 0.5 * 4e-3 * (vgs - 0.5) ** 2, 2.0 - vs3)
v.check("Ex 10-02.3i", gm3 * 1e3)
v.check("Ex 10-02.3j", 1 + gm3 * 1e3)

# ------------------------------------------------------------------ Example 4: re-solve at shifted thresholds
lo, hi = bias3(0.45)[2], bias3(0.55)[2]
v.check("Ex 10-02.4a", lo * 1e3)
v.check("Ex 10-02.4b", hi * 1e3)
v.check("Ex 10-02.4c", (lo / i3 - 1) * 100)
v.check("Ex 10-02.4d", (hi / i3 - 1) * 100)
vgs3 = 2.0 - vs3
flo, fhi = ids(vgs3, 5, 4e-3, 0.45), ids(vgs3, 5, 4e-3, 0.55)
v.check("Ex 10-02.4e", flo * 1e3)
v.check("Ex 10-02.4f", fhi * 1e3)
v.check("Ex 10-02.4g", (flo / i3 - 1) * 100)
v.check("Ex 10-02.4h", (fhi / i3 - 1) * 100)
sens_fixed = -ddx(lambda vt: ids(vgs3, 5, 4e-3, vt), 0.5) / i3 * 0.05 * 100
sens_deg = -ddx(lambda vt: bias3(vt)[2], 0.5, 1e-4) / i3 * 0.05 * 100
v.check("Ex 10-02.4i", sens_fixed)
v.check("Ex 10-02.4j", sens_deg)


# ------------------------------------------------------------------ Example 5: reference and mirror
def ref(vt, lam=0.0, k=4e-3, r=10e3, vdd=3.3):
    vgs = brentq(lambda x: (vdd - x) / r - ids(x, x, k, vt, lam), vt, vdd, xtol=1e-15)
    return vgs, (vdd - vgs) / r


g5, i5 = ref(0.5)
v.check("Ex 10-02.5a", g5)
v.check("Ex 10-02.5b", i5 * 1e3)
g5l, i5l = ref(0.5, 0.1)
v.check("Ex 10-02.5c", g5l)
v.check("Ex 10-02.5d", i5l * 1e3)
i52 = ids(g5l, 2.0, 4e-3, 0.5, 0.1)
v.check("Ex 10-02.5e", i52 * 1e3)
v.check("Ex 10-02.5f", (i52 / i5l - 1) * 100)
v.check("Ex 10-02.5g", ref(0.45)[1] * 1e3)
v.check("Ex 10-02.5h", ref(0.55)[1] * 1e3)

# ------------------------------------------------------------------ Example 6: switches
ron = 1 / ddx(lambda vds: ids(1.8, vds, 50e-3, 0.5), 0.0, 1e-7)       # slope at the origin of the triode curve
v.check("Ex 10-02.6a", ron)
v.check("Ex 10-02.6b", 20**2 * 1.19e-3)
v.check("Ex 10-02.6c", 20**2 * 1.45e-3)
v.check("Ex 10-02.6d", 20**2 * 0.84e-3)
v.check("Ex 10-02.6e", 1.1 / 0.7)
v.check("Ex 10-02.6f", 2 * 0.052)
v.check("Ex 10-02.6g", 2**2 * 0.052)
v.check("Ex 10-02.6h", 2 * 0.052 / 3.3 * 100)


# ------------------------------------------------------------------ Example 7: body effect, two unknowns at once
def body(vg, rs, k, vt0, gam, phi):
    def eqs(x):
        vs, vt = x
        return [vt - (vt0 + gam * (math.sqrt(phi + vs) - math.sqrt(phi))), ids(vg - vs, 10.0, k, vt) * rs - vs]
    vs, vt = fsolve(eqs, [vg / 2, vt0], xtol=1e-12)
    return vs, vt, vs / rs


vs7, vt7, i7 = body(2.5, 2e3, 2e-3, 0.5, 0.4, 0.7)
v.check("Ex 10-02.7a", vs7)
v.check("Ex 10-02.7b", vt7)
v.check("Ex 10-02.7c", i7 * 1e3)
vs70, _, i70 = body(2.5, 2e3, 2e-3, 0.5, 0.0, 0.7)
v.check("Ex 10-02.7d", vs70)
v.check("Ex 10-02.7e", i70 * 1e3)
v.check("Ex 10-02.7f", (1 - i7 / i70) * 100)
x = vs70
its = []
for _ in range(3):
    vt_ = 0.5 + 0.4 * (math.sqrt(0.7 + x) - math.sqrt(0.7))
    if not its:
        v.check("Ex 10-02.7j", vt_)
    x = brentq(lambda s: ids(2.5 - s, 10.0, 2e-3, vt_) * 2e3 - s, 0, 2.5 - vt_)
    its.append(x)
v.check("Ex 10-02.7g", its[0])
v.check("Ex 10-02.7h", its[1])
v.check("Ex 10-02.7i", its[2])

# guided exercise predictions (first-order)
v.check("T 10-02.l", 2 * 0.025 / (vgs3 - 0.5) * 100)
v.check("T 10-02.m", 2 * 0.025 / (vgs3 - 0.5) / (1 + gm3 * 1e3) * 100)

# ------------------------------------------------------------------ solutions
v.check("10-02.2a", ids(0.9, 5, 1e-3, 0.4) * 1e3)
vd2 = brentq(lambda x: ids(0.9, x, 1e-3, 0.4) - (1.8 - x) / 5e3, 0, 1.8, xtol=1e-14)
v.check("10-02.2b", vd2)
v.check("10-02.2c", brentq(lambda rd: 1.8 - rd * ids(0.9, 1.8, 1e-3, 0.4) - 0.5, 1e3, 1e5) / 1e3)
vsd3 = brentq(lambda x: ids(1.0, x, 0.5e-3, 0.45) - (1.8 - x) / 2e3, 0, 1.8, xtol=1e-14)
v.check("10-02.3a", 1.0 - 0.45)
v.check("10-02.3b", ids(1.0, vsd3, 0.5e-3, 0.45) * 1e3)
v.check("10-02.3c", 1.8 - vsd3)
v.check("10-02.3d", vsd3)
vov4 = brentq(lambda x: 0.5 * 2e-3 * x**2 - 0.5e-3, 0, 2)
v.check("10-02.4a", vov4)
v.check("10-02.4b", 0.5 + vov4)
vg4 = 0.5 + vov4 + 0.5e-3 * 2e3
v.check("10-02.4c", vg4)
v.check("10-02.4d", (5 - 1.5 - 0.5e-3 * 2e3) / 0.5e-3 / 1e3)
v.check("10-02.4e", vg4 / 5 * 1e3)
v.check("10-02.4f", (1 - vg4 / 5) * 1e3)
gm4 = ddx(lambda vgs: 0.5 * 2e-3 * (vgs - 0.5) ** 2, 0.5 + vov4)
v.check("10-02.5a", gm4 * 1e3)
v.check("10-02.5b", 1 + gm4 * 2e3)
v.check("10-02.5c", 2 * 0.04 / vov4 * 100)
v.check("10-02.5d", 2 * 0.04 / vov4 / (1 + gm4 * 2e3) * 100)
for k_, vt in (("10-02.5e", 0.46), ("10-02.5f", 0.54)):
    v.check(k_, bias3(vt, k=2e-3, rs=2e3, rd=4e3, vg=vg4)[2] * 1e3)
for k_, vt in (("10-02.6c", 0.45), ("10-02.6d", 0.55)):
    v.check(k_, ref(vt, k=1e-3, r=10e3)[1] * 1e3)
g6, i6 = ref(0.5, k=1e-3, r=10e3)
v.check("10-02.6a", g6)
v.check("10-02.6b", i6 * 1e3)
g7, i7r = ref(0.6, k=2e-3, r=20e3, vdd=5.0)
v.check("10-02.7a", g7)
v.check("10-02.7b", i7r * 1e3)
v.check("10-02.7c", ids(g7, 3.0, 6e-3, 0.6) * 1e3)
g7l, i7l = ref(0.6, lam=0.05, k=2e-3, r=20e3, vdd=5.0)
v.check("10-02.7d", g7l)
v.check("10-02.7e", i7l * 1e3)
i72 = ids(g7l, 3.0, 6e-3, 0.6, 0.05)
v.check("10-02.7f", i72 * 1e3)
v.check("10-02.7g", (i72 / (3 * i7l) - 1) * 100)
v.check("10-02.8a", 50e-3 / 1.0 * 1e3)
wl8 = brentq(lambda wl: 1 / ddx(lambda vds: ids(3.3, vds, 200e-6 * wl, 0.6), 0.0, 1e-7) - 0.05, 1e3, 1e6)
v.check("10-02.8b", wl8)
v.check("10-02.8c", wl8 * 0.5e-6 * 1e3)
v.check("10-02.8d", 1**2 * 0.05 * 1e3)
v.check("10-02.9a", 30**2 * 1.19e-3)
v.check("10-02.9b", 30**2 * 1.45e-3)
v.check("10-02.9c", 30**2 * 1.45e-3 * 1.5)
vs10, vt10, i10 = body(3.0, 10e3, 1e-3, 0.5, 0.5, 0.8)
v.check("10-02.10a", vs10)
v.check("10-02.10b", vt10)
v.check("10-02.10c", i10 * 1e3)
vs100, _, i100 = body(3.0, 10e3, 1e-3, 0.5, 0.0, 0.8)
v.check("10-02.10d", vs100)
v.check("10-02.10e", i100 * 1e3)
v.check("10-02.10f", 3.0 - vs10)
v.check("10-02.10g", 3.0 - vs100)
vov11 = 2 * 0.02 / 0.05
v.check("10-02.11a", vov11)
v.check("10-02.11b", 2 * 0.2e-3 / vov11**2 * 1e3)
k11 = 2 * 0.2e-3 / 0.2**2
gm11 = ddx(lambda vgs: 0.5 * k11 * vgs**2, 0.2)
v.check("10-02.11c", gm11 * 1e3)
v.check("10-02.11d", 1 + gm11 * 5e3)
v.check("10-02.11e", 2 * 0.02 / 0.2 / (1 + gm11 * 5e3) * 100)
v.check("10-02.11f", 2 * 0.02 / 0.2 * 100)
ron12 = 1 / ddx(lambda vsd: ids(3.3, vsd, 2.0, 0.8), 0.0, 1e-7)
v.check("10-02.12a", ron12)
vsd12 = brentq(lambda x: ids(3.3, x, 2.0, 0.8) - 1.0, 0, 2.5, xtol=1e-14)   # exact triode drop at 1 A
v.assert_true("PMOS switch: the exact triode drop at 1 A is within 5% of I R_on", abs(vsd12 / ron12 - 1) < 0.05)
v.check("10-02.12b", 1.0 * ron12)
v.check("10-02.12c", 1.0**2 * ron12)

# ------------------------------------------------------------------ lab: Monte Carlo of the three bias schemes
rng = np.random.default_rng(1002)
dvt = rng.normal(0, 0.025, 10000)
fixed = np.array([ids(vgs3, 5, 4e-3, 0.5 + d) for d in dvt])
deg = np.array([bias3(0.5 + d)[2] for d in dvt[:2000]])
src = np.array([ref(0.5 + d)[1] for d in dvt[:2000]])
v.check("Lab 10-02.a", fixed.std() / fixed.mean() * 100)
v.check("Lab 10-02.b", deg.std() / deg.mean() * 100)
v.check("Lab 10-02.c", src.std() / src.mean() * 100)
v.check("Lab 10-02.d", fixed.std() / fixed.mean() / (deg.std() / deg.mean()))
r_exact = 0.1 / ids(1.8, 0.1, 50e-3, 0.5)
v.check("Lab 10-02.e", (r_exact / ron - 1) * 100)
v.check("Lab 10-02.f", ddx(lambda x: ids(x, x, 4e-3, 0.5), g5) * 10e3)

v.finish()
