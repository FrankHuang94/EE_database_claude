#!/usr/bin/env python3
"""Verify every number in chapter 28-09 (the business <-> engineering translation table),
its problems and its lab.

Independent routes (the lab module uses closed forms and a root finder):
- dies per wafer by counting whole dies on a grid inside the wafer (checked to be close to
  the formula, which the chapter uses by convention), and the formula itself;
- yields by Monte Carlo placement of Poisson defects for one case;
- elasticities by finite differences of log cost and by the analytic 1 + AD0;
- area budgets by bisection; energy, failures, delays and tornado changes by arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import translate as tr  # noqa: E402

v = Verifier.from_files("28-09", ROOT / "chapters" / "28-09-business-engineering-translation.md",
                        ROOT / "solutions" / "28-09-solutions.md", LAB / "README.md")
RNG = np.random.default_rng(2809)
H = 8766.0


def dpw_formula(a, d=300.0):
    return math.pi * d * d / (4 * a) - math.pi * d / math.sqrt(2 * a)


def dpw_grid(a, d=300.0, offsets=12):
    """Best whole-die count of square dies of area a on a grid inside the wafer."""
    s = math.sqrt(a)
    r = d / 2
    best = 0
    for ox in np.linspace(0, s, offsets, endpoint=False):
        for oy in np.linspace(0, s, offsets, endpoint=False):
            xs = np.arange(-r - s + ox, r, s)
            ys = np.arange(-r - s + oy, r, s)
            X, Y = np.meshgrid(xs, ys)
            corners = [(X, Y), (X + s, Y), (X, Y + s), (X + s, Y + s)]
            inside = np.all([cx ** 2 + cy ** 2 <= r * r for cx, cy in corners], axis=0)
            best = max(best, int(inside.sum()))
    return best


def cost(a, wafer, d0=0.001, whole=True):
    n = math.floor(dpw_formula(a)) if whole else dpw_formula(a)
    return wafer / (n * math.exp(-a * d0))


def bisect(f, lo, hi, n=200):
    for _ in range(n):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def gm(asp, a, wafer, d0, pkg):
    return 1 - (cost(a, wafer, d0) + pkg) / asp


# --- Theory text ---------------------------------------------------------------------------
v.check("Txt 28-09.1", 1 + 100 * 0.001)
v.check("Txt 28-09.2", 1 + 600 * 0.001)
for a in (100, 300, 600):
    v.assert_true(f"grid count (no scribe lines) within 8% above the formula at {a} mm2",
                  0 <= dpw_grid(a) - dpw_formula(a) <= 0.08 * dpw_formula(a))

# --- Example 28-09.1 ---------------------------------------------------------------------
v.check("Ex 28-09.1a", math.floor(dpw_formula(100)))
v.check("Ex 28-09.1a1", 100 * math.exp(-0.1))
c100, c120 = cost(100, 18500), cost(120, 18500)
v.check("Ex 28-09.1a2", c100)
v.check("Ex 28-09.1b", math.floor(dpw_formula(120)))
v.check("Ex 28-09.1b1", 100 * math.exp(-0.12))
v.check("Ex 28-09.1b2", c120)
v.check("Ex 28-09.1c", 100 * (c120 / c100 - 1))
v.check("Ex 28-09.1c1", (c120 / c100 - 1) / 0.2)
mc = (RNG.poisson(0.1, 400_000) == 0).mean()
v.assert_true("Ex 1: Monte Carlo Poisson yield at AD0 = 0.1 within 0.2 points", abs(mc - math.exp(-0.1)) < 0.002)

# --- Example 28-09.2 ---------------------------------------------------------------------
v.check("Ex 28-09.2a", 60 * 0.40)
v.check("Ex 28-09.2b", 60 * 0.40 - 8)
a2 = bisect(lambda a: cost(a, 18500, whole=False) - 16, 5, 300)
v.check("Ex 28-09.2c", a2)
v.check("Ex 28-09.2d", 100 * gm(60, 100, 18500, 0.001, 8))
v.assert_true("Ex 2: lab budget agrees", abs(tr.area_budget(60, 8, 0.60, 18500) - a2) < 1e-6)

# --- Examples 28-09.3 to 28-09.5 -------------------------------------------------------
v.check("Ex 28-09.3a", 300 * 4 / 12)
v.check("Ex 28-09.3b", 300 * 4 / 12 * 0.6)
v.check("Ex 28-09.3c", 40 + 300 * 4 / 12 * 0.6)
kwh = 1.0 * 1.3 * 4 * H
v.check("Ex 28-09.4a", kwh)
v.check("Ex 28-09.4b", kwh * 0.08)
v.check("Ex 28-09.4c", 0.9 * 1.3 * 4 * H * 0.08)
v.check("Ex 28-09.4d", 0.1 * 1.3 * 4 * H * 0.08)
v.check("Ex 28-09.4e", 0.1 * 1.3 * 4 * H * 0.08 * 10000 / 1e6)
v.check("Ex 28-09.4f", 100 * (1 / 0.9 - 1))
f100 = 100e-9 * 1e6 * H
v.check("Ex 28-09.5a", f100)
v.check("Ex 28-09.5b", f100 * 500 / 1e6)
v.check("Ex 28-09.5c", 5 * f100)
v.check("Ex 28-09.5d", 5 * f100 * 500 / 1e6)

# --- Example 28-09.6 ---------------------------------------------------------------------
b6 = gm(90, 100, 18500, 0.001, 8)
v.check("Ex 28-09.6a", 100 * b6)
v.check("Ex 28-09.6b", 100 * (gm(99, 100, 18500, 0.001, 8) - b6))
v.check("Ex 28-09.6c", 100 * (gm(90, 110, 18500, 0.001, 8) - b6))
v.check("Ex 28-09.6d", 100 * (gm(90, 100, 20350, 0.001, 8) - b6))
v.check("Ex 28-09.6e", 100 * (gm(90, 100, 18500, 0.0011, 8) - b6))
v.check("Ex 28-09.6f", 100 * (gm(90, 100, 18500, 0.001, 8.8) - b6))
_, t6 = tr.tornado(dict(asp=90, area=100, wafer=18500, d0=0.001, pkg=8))
v.assert_true("Ex 6: lab tornado agrees on area", abs(t6["area"] - 100 * (gm(90, 110, 18500, 0.001, 8) - b6)) < 1e-9)

# --- Problems ------------------------------------------------------------------------------
n2a, n2b = cost(100, 30000), cost(120, 30000)
v.check("28-09.2a", n2a)
v.check("28-09.2b", n2b)
v.check("28-09.2c", 100 * (n2b / n2a - 1))
v.check("28-09.3a", 1 + 0.6)
v.check("28-09.3b", math.floor(dpw_formula(600)))
v.check("28-09.3c", math.floor(dpw_formula(660)))
r3 = cost(660, 18500) / cost(600, 18500) - 1
v.check("28-09.3d", 100 * r3)
v.check("28-09.3e", r3 / 0.1)
v.check("28-09.4a", 45 * 0.45)
v.check("28-09.4b", 45 * 0.45 - 6)
v.check("28-09.4c", bisect(lambda a: cost(a, 18500, whole=False) - 14.25, 5, 300))
v.check("28-09.5a", 120 * 5 / 12)
v.check("28-09.5b", 120 * 5 / 12 * 0.5)
v.check("28-09.5c", 15 + 120 * 5 / 12 * 0.5)
e7, e6 = 0.7 * 1.2 * 5 * H * 0.12, 0.6 * 1.2 * 5 * H * 0.12
v.check("28-09.6a", e7)
v.check("28-09.6b", e6)
v.check("28-09.6c", e7 - e6)
v.check("28-09.6d", 100 * (0.7 / 0.6 - 1))
v.check("28-09.7a", 20e-9 * 5e6 * 500)
v.check("28-09.7b", 20e-9 * 5e6 * 500 * 2000 / 1e6)
e8a, e8b = 1.3 * 4 * H * 0.08, 1.3 * 4 * H * 0.15
v.check("28-09.8a", e8a)
v.check("28-09.8b", 100 * e8a / 25000)
v.check("28-09.8c", e8b)
v.check("28-09.8d", 100 * e8b / 25000)
v.check("28-09.9", (150 + 40) / 30)
v.check("28-09.10a", 100 * (1 - b6) * (1 - 1 / 1.1))
v.check("28-09.10b", 100 * (1 / 0.9 - 1))
for a in (50, 200, 600):
    v.assert_true(f"P10a: no-edge elasticity is 1 + AD0 at {a} mm2",
                  abs((math.log((a * 1.0001) * math.exp(a * 1.0001 * 0.001)) - math.log((a * 0.9999) * math.exp(a * 0.9999 * 0.001)))
                      / (math.log(1.0001) - math.log(0.9999)) - (1 + a * 0.001)) < 1e-6)
v.assert_true("P10b: ASP formula matches Example 6", abs((1 - b6) * (1 - 1 / 1.1) - (gm(99, 100, 18500, 0.001, 8) - b6)) < 1e-12)

# --- Lab ---------------------------------------------------------------------------------------
hh = 1e-4
el600 = (math.log(cost(600 * (1 + hh), 18500, whole=False)) - math.log(cost(600 * (1 - hh), 18500, whole=False))) / (math.log(1 + hh) - math.log(1 - hh))
v.check("Lab 28-09.a", el600)
v.check("Lab 28-09.b", bisect(lambda a: cost(a, 30000, whole=False) - 16, 5, 300))
v.check("Lab 28-09.c", 1.3 * 4 * H * 0.15)
bb = gm(900, 600, 18500, 0.001, 80)
v.check("Lab 28-09.d", 100 * bb)
v.check("Lab 28-09.d1", 100 * (gm(900, 600, 18500, 0.0011, 80) - bb))
v.check("Lab 28-09.d2", 100 * (gm(900, 660, 18500, 0.001, 80) - bb))

sys.exit(v.finish())
