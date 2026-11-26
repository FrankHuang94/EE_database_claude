#!/usr/bin/env python3
"""Verify every number in chapter 27-02 (the smartphone SoC), its problems and its lab.

Independent routes:
- energy per instruction as core power divided by throughput (the lab adds dynamic and static terms);
- minimum-energy frequencies as the positive real root of the cubic dE/df = 0 (numpy.roots; the lab
  minimizes numerically);
- crossovers by a fine grid search followed by bisection on functions written here;
- dies per wafer re-derived here and yields by the Poisson zero-defect probability;
- the BOM shift by solving the share equation directly.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "27-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import socmodel as sm  # noqa: E402

v = Verifier.from_files("27-02", ROOT / "chapters" / "27-02-smartphone-soc.md",
                        ROOT / "solutions" / "27-02-solutions.md", LAB / "README.md")

BIG = dict(ipc=6.0, c=1.2, v0=0.45, k=0.12, ps=0.10, fmax=4.2)
LIT = dict(ipc=2.5, c=0.22, v0=0.45, k=0.30, ps=0.02, fmax=2.4)


def power(core, f):
    vv = core["v0"] + core["k"] * f
    return core["c"] * vv * vv * f + core["ps"]


def epi(core, f):
    """Energy per instruction (nJ) = power (W) / throughput (10^9 instructions/s)."""
    return power(core, f) / (core["ipc"] * f)


def epi_at(core, gips):
    f = gips / core["ipc"]
    return epi(core, f) if f <= core["fmax"] + 1e-12 else math.inf


def crossover(a, b):
    grid = np.linspace(0.3, b["ipc"] * b["fmax"], 20001)
    diff = [epi_at(a, g) - epi_at(b, g) for g in grid]
    j = next(i for i in range(1, len(grid)) if diff[i - 1] > 0 >= diff[i])
    return optimize.bisect(lambda g: epi_at(a, g) - epi_at(b, g), grid[j - 1], grid[j], xtol=1e-12)


def fstar(core):
    """Positive real root of 2 c k (V0 + k f) f^2 - Ps = 0, i.e. 2ck^2 f^3 + 2ckV0 f^2 - Ps = 0."""
    c, k, v0, ps = core["c"], core["k"], core["v0"], core["ps"]
    roots = np.roots([2 * c * k * k, 2 * c * k * v0, 0.0, -ps])
    return float(max(r.real for r in roots if abs(r.imag) < 1e-12 and r.real > 0))


def dpw(area, d=300.0):
    return math.floor(math.pi * (d / 2) ** 2 / area - math.pi * d / math.sqrt(2 * area))


def die(wafer, area, d0):
    n = dpw(area)
    y = math.exp(-d0 * area / 100)
    return n, y, wafer / (n * y)


def bw(rate, width=64):
    return rate * width / 8 / 1000  # MT/s x bits / 8 -> MB/s -> GB/s


# ---------------------------------------------------------------- Example 1 (bandwidth)
v.check("Ex 27-02.1a", bw(10667))
v.check("Ex 27-02.1a1", bw(9600))
frame = 3000 * 1400 * 4 * 120 / 1e9
v.check("Ex 27-02.1b", frame)
v.check("Ex 27-02.1b1", 3 * frame)
demand = {"display": 3 * frame, "camera": 4.32, "gpu": 30.0, "cpu": 10.0}
tot = sum(demand.values())
v.check("Ex 27-02.1b2", tot)
v.check("Ex 27-02.1b3", 100 * tot / bw(10667))
saved = 0.4 * (demand["gpu"] + demand["cpu"])
v.check("Ex 27-02.1c", saved)
v.check("Ex 27-02.1c1", tot - saved)
v.check("Ex 27-02.1c2", 100 * (tot - saved) / bw(10667))
v.assert_true("Ex 1 lab SLC traffic matches", abs(sm.dram_traffic(demand, {"gpu": 0.4, "cpu": 0.4}) - (tot - saved)) < 1e-12)

# ---------------------------------------------------------------- Example 2 (big vs little)
v.check("Ex 27-02.2a0", BIG["v0"] + BIG["k"] / 6)
v.check("Ex 27-02.2a", epi_at(BIG, 1.0))
v.check("Ex 27-02.2a2", LIT["v0"] + LIT["k"] * 0.4)
v.check("Ex 27-02.2a1", epi_at(LIT, 1.0))
v.check("Ex 27-02.2a3", epi_at(BIG, 1.0) / epi_at(LIT, 1.0))
v.check("Ex 27-02.2b1", LIT["v0"] + LIT["k"] * 2.4)
v.check("Ex 27-02.2b", epi_at(LIT, 6.0))
v.check("Ex 27-02.2c", crossover(BIG, LIT))

# ---------------------------------------------------------------- Example 3 (minimum energy)
fb = fstar(BIG)
v.assert_true("Ex 3 root equals the lab's numerical minimum",
              abs(fb - sm.f_min_energy(dict(BIG, f_max=BIG["fmax"]))) < 1e-6)
v.check("Ex 27-02.3a", fb)
v.check("Ex 27-02.3a1", epi(BIG, fb))
v.check("Ex 27-02.3b", BIG["v0"] + BIG["k"] * 4.2)
v.check("Ex 27-02.3b1", epi(BIG, 4.2))
v.check("Ex 27-02.3b2", epi(BIG, 4.2) / epi(BIG, fb))
hot = dict(BIG, ps=0.6)
v.check("Ex 27-02.3c", fstar(hot))
v.check("Ex 27-02.3c1", epi(hot, fstar(hot)))

# ---------------------------------------------------------------- Example 4 (cluster and throttling)
pb, pl = power(BIG, 4.2), power(LIT, 2.4)
v.check("Ex 27-02.4a", pb)
v.check("Ex 27-02.4a1", pl)
v.check("Ex 27-02.4a2", 2 * pb + 4 * pl)
f15 = optimize.bisect(lambda f: power(BIG, f) - 1.5, 0.1, 4.2, xtol=1e-12)
v.check("Ex 27-02.4b", f15)
v.check("Ex 27-02.4b1", 100 * f15 / 4.2)
v.check("Ex 27-02.4b2", BIG["v0"] + BIG["k"] * f15)
v.check("Ex 27-02.4b3", 6 * f15)
v.check("Ex 27-02.4b4", 6 * 4.2)
v.check("Ex 27-02.4b5", pb / 1.5)
v.check("Ex 27-02.4b6", 4.2 / f15)

# ---------------------------------------------------------------- Example 5 (on-device model)
b5 = bw(10667)
v.check("Ex 27-02.5a0", 3e9 * 2 / 8 / 1e9)
v.check("Ex 27-02.5a", b5 / (3e9 * 2 / 8 / 1e9))
v.check("Ex 27-02.5a1", b5 / (3e9 * 4 / 8 / 1e9))
v.check("Ex 27-02.5b", 3e9 * 2 * 4.0e-12 * 1e3)
v.check("Ex 27-02.5b1", 3e9 * 4 * 4.0e-12 * 1e3)
v.check("Ex 27-02.5c", 3e9 * 2 * 4.0e-12 * 20)

# ---------------------------------------------------------------- Example 6 (die cost)
for key, (w, a, d0) in {"a": (18500, 98.6, 0.10), "b": (18500, 140.79, 0.10)}.items():
    n, y, c = die(w, a, d0)
    v.check(f"Ex 27-02.6{key}", n)
    v.check(f"Ex 27-02.6{key}1", y)
    v.check(f"Ex 27-02.6{key}2", c)
v.check("Ex 27-02.6b3", 100 * (140.79 / 98.6 - 1))
v.check("Ex 27-02.6b4", 100 * (die(18500, 140.79, 0.10)[2] / die(18500, 98.6, 0.10)[2] - 1))
n2, y2, c2 = die(30000, 98.6, 0.15)
v.check("Ex 27-02.6c", y2)
v.check("Ex 27-02.6c1", c2)
v.check("Ex 27-02.6c2", c2 / die(18500, 98.6, 0.10)[2])
v.check("Txt 27-02.1", 100 * (c2 / die(18500, 98.6, 0.10)[2] - 1))
v.check("Txt 27-02.2", 100 * (30000 / 18500 - 1))
v.check("Txt 27-02.3", math.log(power(BIG, 4.2) / power(BIG, 2.25)) / math.log(4.2 / 2.25))

# ---------------------------------------------------------------- Example 7 (BOM shift)
m = optimize.brentq(lambda x: x / (x + 0.90) - 0.34, 0.0, 10.0)
v.check("Ex 27-02.7a", 0.90)
v.check("Ex 27-02.7a0", m)
v.check("Ex 27-02.7a1", m / 0.10)
v.check("Ex 27-02.7a2", m + 0.90)
v.check("Ex 27-02.7a3", 100 * (m + 0.90 - 1))
v.check("Ex 27-02.7b", 38 - 100 * (m + 0.90 - 1))

# ---------------------------------------------------------------- Problems
v.check("27-02.2", bw(14400))
v.check("27-02.2a", bw(10667))
v.check("27-02.2b", bw(14400) / bw(10667))
r120 = 2400 * 1080 * 4 * 120 / 1e9
v.check("27-02.3", r120)
v.check("27-02.3a", 2400 * 1080 * 4 / 1e9)
v.check("27-02.3b", 120)
v.check("27-02.4", 0.35 * 45)
v.check("27-02.4a", 60 - 0.35 * 45)
v.check("27-02.4b", 0.35 * 45e9 * 8 * 4.0e-12)
MID = dict(ipc=4.0, c=0.6, v0=0.45, k=0.15, ps=0.05, fmax=3.0)
v.check("27-02.5a0", 0.45 + 0.15 * 2)
v.check("27-02.5a", epi(MID, 2.0))
v.check("27-02.5b", power(MID, 2.0))
v.check("27-02.5b1", 4 * 2.0)
v.check("27-02.5c", epi(MID, 2.0) * 8)
fm = fstar(MID)
v.check("27-02.6", fm)
v.check("27-02.6a", 0.45 + 0.15 * fm)
v.check("27-02.6b", epi(MID, fm))
v.check("27-02.7a", 1.5 * 9600)
v.check("27-02.7b", 1.5 * 64)
v.check("27-02.7c", 1.5 * bw(9600))
f2 = optimize.bisect(lambda f: power(BIG, f) - 2.0, 0.1, 4.2, xtol=1e-12)
v.check("27-02.8", f2)
v.check("27-02.8a", 100 * f2 / 4.2)
v.check("27-02.8b", 6 * f2)
v.check("27-02.9a", 7e9 * 4 / 8 / 1e9)
v.check("27-02.9a1", bw(14400) / 3.5)
v.check("27-02.9b", 100 * 3.5 / 12)
for key, (w, a, d0) in {"a": (18500, 126.2, 0.10), "b": (18500, 111.2, 0.10), "c": (12000, 25, 0.08)}.items():
    n, y, c = die(w, a, d0)
    v.check(f"27-02.10{key}" if key != "c" else "27-02.10c", n)
    v.check(f"27-02.10{key}1", y)
    v.check(f"27-02.10{key}2", c)
split = die(18500, 111.2, 0.10)[2] + die(12000, 25, 0.08)[2] + 1.50
v.check("27-02.10c3", split)
v.check("27-02.10c4", split - die(18500, 126.2, 0.10)[2])
n_inst = 2e9
f_pace = n_inst / (6 * 1e9)
v.check("27-02.11a0", f_pace)
v.check("27-02.11a1", epi(BIG, f_pace))
v.check("27-02.11a", n_inst * epi(BIG, f_pace) * 1e-9)
v.check("27-02.11a2", n_inst * epi(BIG, 4.2) * 1e-9)
v.check("27-02.11a3", n_inst / (6 * 4.2e9))
v.check("27-02.11b", n_inst * epi(dict(BIG, ps=0.6), f_pace) * 1e-9)
v.check("27-02.11b1", n_inst * epi(dict(BIG, ps=0.6), 4.2) * 1e-9)
for tag, ps in (("", 0.10), ("2", 0.6)):
    core_d = dict(BIG, ps=ps)
    opt = optimize.minimize_scalar(lambda f: epi(core_d, f), bounds=(0.05, BIG["fmax"]), method="bounded",
                                   options={"xatol": 1e-9})
    f_c = max(opt.x, f_pace)
    v.check("27-02.11d" + tag, opt.x)
    v.check("27-02.11d" + ("1" if tag == "" else "3"), n_inst * epi(core_d, f_c) * 1e-9)
v.check("27-02.12a", 100 * 150 / (450 + 150))
gm0, gm1 = (1099 - 540) / 1099, (1099 - 640) / 1099
v.check("27-02.12b", 100 * gm0)
v.check("27-02.12b1", 100 * gm1)
v.check("27-02.12b2", 100 * (gm0 - gm1))
v.check("27-02.12c", 640 / (1 - gm0))
v.check("27-02.12c1", 640 / (1 - gm0) - 1099)

# ---------------------------------------------------------------- Lab
v.check("Lab 27-02.a", crossover(BIG, dict(LIT, k=0.25)))
v.check("Lab 27-02.b", fstar(dict(BIG, ps=0.05)))
v.check("Lab 27-02.b1", fstar(dict(BIG, ps=1.0)))
v.check("Lab 27-02.c", bw(14400) / 0.75)
v.check("Lab 27-02.c1", 100 * (bw(14400) / bw(10667) - 1))
v.check("Lab 27-02.d", die(18500, 120, 0.10)[2])
v.check("Lab 27-02.d1", die(30000, 120, 0.15)[2])
v.check("Lab 27-02.d2", die(30000, 120, 0.15)[2] / die(18500, 120, 0.10)[2])

# Problem 27-02.13: energy per instruction from frequency, the crossover by bisection
def e_core(rate_gips, ipc, c_nf, v0, k, ps):
    f = rate_gips / ipc  # GHz
    return c_nf * (v0 + k * f) ** 2 / ipc + ps / (ipc * f)


e_mid = lambda r: e_core(r, 4, 0.6, 0.45, 0.15, 0.05)  # noqa: E731
e_lit = lambda r: e_core(r, 2.5, 0.22, 0.45, 0.30, 0.02)  # noqa: E731
v.check("27-02.13a", e_mid(1.5))
v.check("27-02.13b", e_lit(1.5))
v.check("27-02.13c", e_mid(5.0))
v.check("27-02.13d", e_lit(5.0))
lo, hi = 1.0, 6.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if (e_lit(lo) - e_mid(lo)) * (e_lit(mid) - e_mid(mid)) <= 0:
        hi = mid
    else:
        lo = mid
v.check("27-02.13e", 0.5 * (lo + hi))
v.assert_true("one crossing between 1 and 6 GIPS",
              sum(1 for r in np.linspace(1, 5.99, 500)
                  if (e_lit(r) - e_mid(r)) * (e_lit(r + 0.01) - e_mid(r + 0.01)) < 0) == 1)
v.check("27-02.13f", e_lit(2.0))
v.check("27-02.13g", e_mid(2.0))
v.check("27-02.13h", 100 * (1 - e_lit(2.0) / e_mid(2.0)))

sys.exit(v.finish())
