#!/usr/bin/env python3
"""Verify every number in chapter 28-08 (post-acquisition integration risk), its problems
and its lab.

Independent routes (the lab module uses closed forms):
- synergy values by explicit year-by-year discounted cash-flow sums;
- parallel paths by Monte Carlo simulation of two programs, with correlated failures
  drawn from an explicit joint distribution;
- retention by month-by-month survival products and simulation;
- registers, royalties, TPP and earn-outs by direct arithmetic.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import integrate as ig  # noqa: E402

v = Verifier.from_files("28-08", ROOT / "chapters" / "28-08-integration-risk.md",
                        ROOT / "solutions" / "28-08-solutions.md", LAB / "README.md")
RNG = np.random.default_rng(2808)


def dcf(flows, rate):
    """flows: {year: amount}."""
    return sum(a / (1 + rate) ** t for t, a in flows.items())


def plan(per_year, years, rate, delay=0, rho=1.0, fixed=False):
    if fixed:
        flows = {t: rho * per_year for t in range(1 + delay, years + 1)}
    else:
        flows = {t + delay: rho * per_year for t in range(1, years + 1)}
    return dcf(flows, rate)


def paths_mc(p1, p2, both_fail, socket, trials=1_000_000):
    """Simulate outcomes from the joint distribution of (success1, success2)."""
    f1, f2 = 1 - p1, 1 - p2
    probs = [both_fail, f1 - both_fail, f2 - both_fail, 1 - f1 - f2 + both_fail]  # FF, F S, S F, SS
    outcome = RNG.choice(4, size=trials, p=probs)
    win = outcome != 0
    return socket * win.mean()


# --- Theory text ---------------------------------------------------------------------------
v.check("Txt 28-08.1", 100 * (1 - plan(50, 5, 0.10, delay=1, rho=0.8) / plan(50, 5, 0.10)))
v.check("Txt 28-08.2", 100 * 2613 / 4920)

# --- Example 28-08.1 ---------------------------------------------------------------------
p0 = plan(50, 5, 0.10)
v.check("Ex 28-08.1a", p0 / 50)
v.check("Ex 28-08.1a1", p0)
p1 = plan(50, 5, 0.10, delay=1, rho=0.8)
v.check("Ex 28-08.1b", p1)
v.check("Ex 28-08.1c", p0 - p1)
v.check("Ex 28-08.1c1", 100 * (p0 - p1) / p0)
v.assert_true("Ex 1: lab model agrees", abs(ig.synergy_value(50, 5, 0.1, 1, 0.8) - p1) < 1e-9)

# --- Examples 28-08.2 to 28-08.4 ---------------------------------------------------------
v.check("Ex 28-08.2a", 25 * 4 * 0.025)
v.check("Ex 28-08.2b", 60 * 3 / 12)
v.check("Ex 28-08.2c", 0.6 * 60 * 3 / 12)
v.check("Ex 28-08.2d", 0.6 * 60 * 3 / 12 / (25 * 4 * 0.025))
w_both = paths_mc(0.6, 0.5, 0.4 * 0.5, 200)
v.check("Ex 28-08.3a", 1 - 0.4 * 0.5)
v.check("Ex 28-08.3b", 200 * (1 - 0.4 * 0.5))
v.check("Ex 28-08.3c", 200 * 0.6)
v.check("Ex 28-08.3d", 200 * (1 - 0.4 * 0.5) - 120)
v.assert_true("Ex 3: Monte Carlo value within $0.5M", abs(w_both - 160) < 0.5)
rev = 50e6 * 20
for frac, a, b in ((0.01, "Ex 28-08.4a", "Ex 28-08.4d"), (0.02, "Ex 28-08.4b", "Ex 28-08.4e"),
                   (0.03, "Ex 28-08.4c", "Ex 28-08.4f")):
    v.check(a, rev * frac / 1e6)
    v.check(b, 100 * (rev * frac) / rev)

# --- Example 28-08.5 ---------------------------------------------------------------------
v.check("Ex 28-08.5a", 3.25 + 2.25)
v.check("Ex 28-08.5a1", 100 * 2.25 / 5.5)
v.check("Ex 28-08.5b", 3.25 + 0.4 * 2.25)
cont = dcf({3: 0.4 * 2.25}, 0.10)
v.check("Ex 28-08.5c", cont)
v.check("Ex 28-08.5c1", 3.25 + cont)

# --- Example 28-08.6 ---------------------------------------------------------------------
reg = [(0.30, 40), (0.20, 60), (0.50, 10), (0.10, 150), (0.25, 20)]
terms = [p * i for p, i in reg]
v.check("Ex 28-08.6a", sum(terms))
v.check("Ex 28-08.6a1", max(terms))
v.assert_true("Ex 6: largest term is the license dispute", terms.index(max(terms)) == 3)
reg_m = [(0.15, 40)] + reg[1:]
v.check("Ex 28-08.6b", sum(p * i for p, i in reg_m))
v.check("Ex 28-08.6b1", sum(terms) - sum(p * i for p, i in reg_m))

# --- Problem 28-08.2 ---------------------------------------------------------------------
q0 = plan(30, 4, 0.12)
v.check("28-08.2a", q0 / 30)
v.check("28-08.2b", q0)
q1, q2 = plan(30, 4, 0.12, 1, 0.75), plan(30, 4, 0.12, 2, 0.75)
v.check("28-08.2c", q1)
v.check("28-08.2d", q2)
v.check("28-08.2e", 100 * (1 - q1 / q0))
v.check("28-08.2f", 100 * (1 - q2 / q0))

# --- Problems 28-08.3 to 28-08.8 -----------------------------------------------------
v.check("28-08.3a", 40 * 6 * 0.022)
v.check("28-08.3b", 90 * 4 / 12)
v.check("28-08.3c", 0.55 * 90 * 4 / 12)
v.check("28-08.4a", 0.3 * 0.6)
v.check("28-08.4b", 1 - 0.3 * 0.6)
v.check("28-08.4c", 150 * (1 - 0.3 * 0.6))
v.check("28-08.4d", 150 * 0.7)
v.check("28-08.4e", 150 * (1 - 0.3 * 0.6) - 105)
v.check("28-08.4f", 150 * (1 - 0.25) - 105)
v.assert_true("P4: Monte Carlo correlated value within $0.5M", abs(paths_mc(0.7, 0.4, 0.25, 150) - 112.5) < 0.5)
v.assert_true("P4: lab gain agrees", abs(ig.parallel_gain(0.7, 0.4, 150, 0.25) - 7.5) < 1e-9)
rev5 = 30e6 * 12
v.check("28-08.5a", rev5 * 0.015 / 1e6)
v.check("28-08.5b", rev5 * 0.03 / 1e6)
v.check("28-08.5c", 100 * rev5 * (0.03 - 0.015) / rev5)
v.check("28-08.6a", 100 * 0.8 / 2.0)
v.check("28-08.6b", dcf({2: 0.5 * 0.8}, 0.10))
v.check("28-08.6c", 1.2 + dcf({2: 0.5 * 0.8}, 0.10))
v.check("28-08.6d", 1.2 + dcf({2: 0.7 * 0.8}, 0.10))
reg7 = [(0.40, 25), (0.15, 80), (0.05, 300), (0.30, 15)]
el7 = sum(p * i for p, i in reg7)
v.check("28-08.7a", el7)
v.check("28-08.7b", max(p * i for p, i in reg7))
el7b = sum(p * i for p, i in [(0.40, 25), (0.15, 80), (0.01, 300), (0.30, 15)])
v.check("28-08.7c", el7b)
v.check("28-08.7d", el7 - el7b)
v.check("28-08.8a", 2 * (400 / 2) * 8)
v.check("28-08.8b", 2 * (400 / 2) * 8 / 600)
v.check("28-08.8c", 2 * (1200 / 2) * 8)
v.check("28-08.8d", 2 * (150 / 2) * 8)
v.assert_true("P8: 400-TOPS part is in the 3A090.b.1 band (2400-4800, density 1.6-5.92)",
              2400 <= 3200 < 4800 and 1.6 <= 3200 / 600 < 5.92)

# --- Problems 28-08.9 to 28-08.11 ----------------------------------------------------
q9 = plan(50, 5, 0.10, 2, 0.8)
v.check("28-08.9a", q9)
v.check("28-08.9b", 100 * (1 - q9 / p0))
fixed = plan(50, 5, 0.10, delay=1, fixed=True)
shifted = plan(50, 5, 0.10, delay=1)
v.check("28-08.10a", fixed)
v.check("28-08.10b", 100 * (1 - fixed / p0))
v.check("28-08.10c", shifted)
v.check("28-08.10d", 100 * (1 - shifted / p0))
v.check("28-08.10e", (1 - fixed / p0) / (1 - shifted / p0))
v.assert_true("P10: lab fixed-window model agrees",
              abs(ig.synergy_value(50, 5, 0.10, delay=1, fixed_window=True) - fixed) < 1e-9)
rates = {"none": [0.01] * 27, "lump": [0.003] * 24 + [0.05] * 3, "staged": [0.005] * 27}
ret = {k: np.cumprod([1 - r for r in v]) for k, v in rates.items()}
for key, (pkg, month) in {"a": ("none", 24), "b": ("lump", 24), "c": ("staged", 24),
                           "d": ("none", 27), "e": ("lump", 27), "f": ("staged", 27)}.items():
    v.check(f"28-08.11{key}", 100 * ret[pkg][month - 1])
sim = (RNG.random((200_000, 27)) >= np.array(rates["lump"])).all(axis=1).mean()
v.assert_true("P11: simulated lump-package retention within 0.3 points", abs(sim - ret["lump"][26]) < 0.003)

# --- Problem 28-08.12 identities ----------------------------------------------------
for n, r in ((5, 0.10), (4, 0.12), (10, 0.07)):
    v.assert_true(f"P12a: annuity formula n={n}, r={r}",
                  abs(sum((1 + r) ** -t for t in range(1, n + 1)) - ig.annuity(n, r)) < 1e-12)
v.assert_true("P12c: correlation lowers the gain",
              ig.parallel_gain(0.6, 0.5, 200, 0.3) < ig.parallel_gain(0.6, 0.5, 200))

# --- Lab ---------------------------------------------------------------------------------------
v.check("Lab 28-08.a", plan(50, 5, 0.10, 3, 0.8))
v.check("Lab 28-08.a1", 100 * plan(50, 5, 0.10, 3, 0.8) / p0)
v.check("Lab 28-08.b", 200 * (1 - 0.35) - 120)
v.check("Lab 28-08.c", 2 * (2000 / 2) * 8)
v.check("Lab 28-08.d", sum(terms) - 0.10 * 150)

gross13 = 200 * ((1 - 0.4 * 0.5) - 0.6)
v.check("28-08.13a", gross13)
v.check("28-08.13b", gross13 - 30)
v.check("28-08.13c", gross13 - 12)
v.check("28-08.13d", (gross13 - 12) - (gross13 - 30))

sys.exit(v.finish())
