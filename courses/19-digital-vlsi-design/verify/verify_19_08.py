#!/usr/bin/env python3
"""Verify every number in chapter 19-08 (SRAM design), its problems and its lab.

Independent routes:
- the read disturbance by solving the full six-transistor cell's two node equations together (not the half-cell
  balance), and the write level by bisection on the half-cell currents;
- the static noise margin from its definition as the largest equal-and-opposite DC noise at the two inverter
  inputs for which the cell stays bistable (counting fixed points of the loop), not by the butterfly rotation;
- yield by the Poisson CDF from scipy and tail probabilities from the normal distribution;
- the lab's module is checked against these results; ngspice confirms the read and write levels in cell.cir.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm, poisson

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import sram as sr  # noqa: E402

v = Verifier.from_files("19-08", ROOT / "chapters" / "19-08-sram-design.md",
                        ROOT / "solutions" / "19-08-solutions.md", LAB / "README.md")


def ids(k, vgs, vds, vt):
    ov = vgs - vt
    if ov <= 0 or vds <= 0:
        return 0.0
    return k * (ov * vds - vds * vds / 2) if vds < ov else k * ov * ov / 2


def full_cell_read(ka, kn, kp, vdd, vt):
    """Both nodes of the cell during a read (bitlines and wordline at VDD), starting from Q = 0, QB = VDD: for each
    trial Q, solve the QB node exactly, then solve the Q node."""
    def qb_of(q):
        def g(qb):
            return ids(kp, vdd - q, vdd - qb, vt) + ids(ka, vdd - qb, vdd - qb, vt) - ids(kn, q, qb, vt)
        if g(vdd * (1 - 1e-15)) >= 0 and ids(kn, q, vdd, vt) == 0.0:
            return vdd
        return brentq(g, 0.0, vdd, xtol=1e-15)

    def fq(q):
        qb = qb_of(q)
        return ids(kp, vdd - qb, vdd - q, vt) + ids(ka, vdd - q, vdd - q, vt) - ids(kn, qb, q, vt)
    q = brentq(fq, 0.0, vt, xtol=1e-15)
    return q, qb_of(q)


ka = 100e-6
for cr, key in ((1, "2a"), (1.5, "2b"), (2, "2c"), (3, "2d")):
    q, qb = full_cell_read(ka, cr * ka, 50e-6, 1.0, 0.3)
    v.check(f"Ex 19-08.{key}", q)
    v.assert_true(f"QB stays at VDD, CR = {cr}", abs(qb - 1.0) < 1e-6, f"{qb}")
v.check("Ex 19-08.2e", 0.3 - full_cell_read(ka, ka, 50e-6, 1.0, 0.3)[0])
v.check("Ex 19-08.2f", 0.3 - full_cell_read(ka, 3 * ka, 50e-6, 1.0, 0.3)[0])
v.check("Lab 19-08.a", full_cell_read(ka, 2 * ka, 50e-6, 1.0, 0.3)[0])
v.assert_true("lab read_disturb matches", abs(sr.read_disturb(ka, 2 * ka, 1.0, 0.3)
                                             - full_cell_read(ka, 2 * ka, 50e-6, 1.0, 0.3)[0]) < 1e-9, "")


def write_lvl(ka_, kp_, vdd, vt):
    lo, hi = 0.0, vdd
    for _ in range(200):
        mid = (lo + hi) / 2
        # access pulls down (gate VDD, source 0), pull-up pulls up (gate 0, source VDD)
        if ids(ka_, vdd, mid, vt) > ids(kp_, vdd, vdd - mid, vt):
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


for pr, key in ((0.5, "3a"), (1, "3b"), (2, "3c")):
    v.check(f"Ex 19-08.{key}", write_lvl(ka, pr * ka, 1.0, 0.3))
v.check("Lab 19-08.b", write_lvl(ka, 0.5 * ka, 1.0, 0.3))


# ---------------------------------------------------------------- SNM by the bistability definition
def vtc_point(x, vdd, vt, kn, kp, kacc):
    return brentq(lambda o: ids(kp, vdd - x, vdd - o, vt) + ids(kacc, vdd - o, vdd - o, vt) - ids(kn, x, o, vt),
                  0.0, vdd, xtol=1e-13)


def snm_bistable(vdd, vt, kn, kp, kacc=0.0):
    xs = np.linspace(0, vdd, 4001)
    f = np.array([vtc_point(x, vdd, vt, kn, kp, kacc) for x in xs])

    def fi(x):
        return np.interp(np.clip(x, 0, vdd), xs, f)

    def n_fixed(vn):
        g = fi(fi(xs - vn) + vn) - xs
        return int(np.sum(np.sign(g[:-1]) != np.sign(g[1:])))

    lo, hi = 0.0, vdd / 2
    for _ in range(50):
        mid = (lo + hi) / 2
        if n_fixed(mid) >= 3:
            lo = mid
        else:
            hi = mid
    return lo


hold = snm_bistable(1.0, 0.3, 200e-6, 100e-6)
v.check("Ex 19-08.6a", hold)
reads = {cr: snm_bistable(1.0, 0.3, cr * 100e-6, 100e-6, 100e-6) for cr in (1, 2, 3)}
v.check("Ex 19-08.6b", reads[1])
v.check("Ex 19-08.6c", reads[2])
v.check("Ex 19-08.6d", reads[3])
v.check("Ex 19-08.6e", 100 * (1 - reads[2] / hold))
v.check("Ex 19-08.6f", 100 * (reads[3] / reads[1] - 1))
v.check("Ex 19-08.6g", snm_bistable(1.0, 0.3, 200e-6, 200e-6))
v.assert_true("lab SNM matches the bistability definition",
              abs(sr.static_noise_margin(1.0, 0.3, 200e-6, 100e-6, 100e-6) - reads[2]) < 2e-3, "")
for vdd, kh, kr in ((1.0, "9a", "9b"), (0.8, "9c", "9d"), (0.6, "9e", "9f")):
    v.check(f"19-08.{kh}", snm_bistable(vdd, 0.3, 200e-6, 100e-6))
    v.check(f"19-08.{kr}", snm_bistable(vdd, 0.3, 200e-6, 100e-6, 100e-6))

# ---------------------------------------------------------------- area, bitlines, yield
v.check("Ex 19-08.1a", 2 ** 20 * 0.021e-6)
v.check("Ex 19-08.1b", 1 / 0.021)
v.check("Ex 19-08.1c", 2 ** 20 * 0.021e-6 / 0.7)
v.check("Ex 19-08.1d", 2 ** 20 * 1.896e-6)
v.check("Ex 19-08.1e", 1.896 / 0.021)
cbl = 256 * 0.08 + 15
v.check("Ex 19-08.4a", cbl)
t_bl = cbl * 1e-15 * 0.1 / 20e-6
t_sa = 15e-12 * math.log(10)
v.check("Ex 19-08.4b", t_bl * 1e12)
v.check("Ex 19-08.4c", t_sa * 1e12)
v.check("Ex 19-08.4d", cbl * 1e-15 * 1.0 / 20e-6 * 1e12)
v.check("Ex 19-08.4e", cbl * 1e-15 * 1.0 / 20e-6 / (t_bl + t_sa))
n64 = 2 ** 26
v.check("Ex 19-08.5a", norm.sf(6))
v.check("Ex 19-08.5b", n64 * norm.sf(6))
v.check("Ex 19-08.5c", 100 * poisson.cdf(0, n64 * norm.sf(6)))
v.check("Ex 19-08.5d", norm.sf(5))
v.check("Ex 19-08.5e", n64 * norm.sf(5))
v.check("Ex 19-08.5f", poisson.cdf(0, n64 * norm.sf(5)))
v.check("Ex 19-08.5g", 100 * poisson.cdf(32, n64 * norm.sf(5)))
v.check("Txt 19-08.a", 1 / 0.0175)
v.check("Txt 19-08.b", 100 * 38 / (1 / 0.0175))
v.check("Txt 19-08.c", 1.200 * 1.580)
v.check("Txt 19-08.d", vtc_point(1.0, 1.0, 0.3, 200e-6, 100e-6, 100e-6))

# Problem 1: count devices from the solved read operating point of the chapter's cell
q1, qb1 = full_cell_read(ka, 2 * ka, 50e-6, 1.0, 0.3)
VDD1, VT1 = 1.0, 0.3
dev = {  # (k, |V_GS|, |V_DS|)
    "access Q": (ka, VDD1 - q1, VDD1 - q1),
    "pull-down Q": (2 * ka, qb1, q1),
    "pull-up Q": (50e-6, VDD1 - qb1, VDD1 - q1),
    "pull-up QB": (50e-6, VDD1 - q1, VDD1 - qb1),
    "access QB": (ka, VDD1 - min(VDD1, qb1), abs(VDD1 - qb1)),
    "pull-down QB": (2 * ka, q1, qb1),
}
v.check("19-08.1a", sum(ids(k_, g_, d_, VT1) > 1e-12 for k_, g_, d_ in dev.values()))
v.check("19-08.1c", sum(g_ > VT1 for _, g_, _d in dev.values()))
v.check("19-08.1b", 8)
v.check("19-08.2a", 2 ** 18 * 0.0175e-6)
v.check("19-08.2b", 2 ** 18 / 38e6)
v.check("19-08.3a", 128 * 0.1 + 10)
v.check("19-08.3b", 22.8e-15 * 0.08 / 15e-6 * 1e12)
q4 = full_cell_read(ka, 1.5 * ka, 50e-6, 0.8, 0.3)[0]
v.check("19-08.4a", q4)
v.check("19-08.4b", 0.3 - q4)
v.check("19-08.5a", brentq(lambda c: full_cell_read(ka, c * ka, 50e-6, 1.0, 0.3)[0] - 0.1, 1.5, 5, xtol=1e-12))
v.check("19-08.6a", brentq(lambda p: write_lvl(ka, p * ka, 1.0, 0.3) - 0.3, 0.3, 1.0, xtol=1e-12))
n16 = 2 ** 24
v.check("19-08.7a", norm.sf(5.5))
v.check("19-08.7b", n16 * norm.sf(5.5))
v.check("19-08.7c", 100 * poisson.cdf(0, n16 * norm.sf(5.5)))
v.check("19-08.7d", 100 * poisson.cdf(4, n16 * norm.sf(5.5)))
v.check("19-08.8a", 6 * 10)
v.check("19-08.8b", 35.5e-15 * 0.06 / 20e-6 * 1e12)
v.check("19-08.8c", 15 * math.log(1 / 0.06))
v.check("19-08.10a", -math.log(0.99) / 2 ** 30)
v.check("19-08.10b", norm.isf(-math.log(0.99) / 2 ** 30))

sys.exit(v.finish())
