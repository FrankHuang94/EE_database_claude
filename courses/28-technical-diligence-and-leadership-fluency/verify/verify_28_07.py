#!/usr/bin/env python3
"""Verify every number in chapter 28-07 (evaluating engineering teams), its problems and
its lab.

Independent routes (the lab module uses closed forms and scipy):
- posterior means and credible intervals by numerical integration of prior x likelihood
  on a grid (no conjugate formula), with percentiles found by root-finding on the
  integrated density;
- schedule statistics with numpy (ddof = 1) and the normal tail by quadrature;
- bench-depth risks by Monte Carlo simulation of departures, including the group event;
- scorecards, retention values, capacity and channels by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import teameval as te  # noqa: E402

v = Verifier.from_files("28-07", ROOT / "chapters" / "28-07-evaluating-engineering-teams.md",
                        ROOT / "solutions" / "28-07-solutions.md", LAB / "README.md")
RNG = np.random.default_rng(2807)
A0, B0 = 1.4, 8.6


def post_density(s, n):
    """Unnormalized posterior density from prior x binomial likelihood."""
    return lambda t: t ** (A0 - 1 + s) * (1 - t) ** (B0 - 1 + n - s)


def post_mean_num(s, n):
    f = post_density(s, n)
    z = integrate.quad(f, 0, 1)[0]
    return integrate.quad(lambda t: t * f(t), 0, 1)[0] / z


def post_quantile_num(s, n, p):
    f = post_density(s, n)
    z = integrate.quad(f, 0, 1)[0]
    return optimize.brentq(lambda x: integrate.quad(f, 0, x)[0] / z - p, 1e-9, 1 - 1e-9)


def phi(x):
    return integrate.quad(lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi), -np.inf, x)[0]


def loss_mc(q, k, c=0.0, trials=400_000):
    group = RNG.random(trials) < c
    each = (RNG.random((trials, k)) < q).all(axis=1)
    return float(np.mean(group | each))


# --- Example 28-07.1 ---------------------------------------------------------------------
v.check("Ex 28-07.1a", 0.14 * 10)
v.check("Ex 28-07.1a1", 0.86 * 10)
v.check("Ex 28-07.1b", 100 * post_mean_num(4, 5))
v.check("Ex 28-07.1b1", 100 * 4 / 5)
v.check("Ex 28-07.1b2", 5 / (10 + 5))
v.check("Ex 28-07.1c", 100 * post_quantile_num(4, 5, 0.05))
v.check("Ex 28-07.1c1", 100 * post_quantile_num(4, 5, 0.95))
v.check("Ex 28-07.1d", 100 * post_mean_num(2, 2))
v.check("Ex 28-07.1d1", 100 * post_quantile_num(2, 2, 0.05))
v.check("Ex 28-07.1d2", 100 * post_quantile_num(2, 2, 0.95))
v.assert_true("Ex 1: lab conjugate mean agrees", abs(te.posterior_mean(A0, B0, 4, 5) - post_mean_num(4, 5)) < 1e-9)
v.assert_true("Ex 1: first team's 5th percentile exceeds 14%", post_quantile_num(4, 5, 0.05) > 0.14)
v.assert_true("Ex 1: second team's 5th percentile is below 14%", post_quantile_num(2, 2, 0.05) < 0.14)

# --- Example 28-07.2 ---------------------------------------------------------------------
logs = np.log([1.25, 1.40, 1.30, 1.10])
mu, sd = logs.mean(), logs.std(ddof=1)
v.check("Ex 28-07.2a", math.exp(mu))
v.check("Ex 28-07.2b", sd)
v.check("Ex 28-07.2c", 18 * math.exp(mu))
v.check("Ex 28-07.2d", 100 * phi(-mu / sd))
z90 = optimize.brentq(lambda z: phi(z) - 0.9, 0, 3)
v.check("Ex 28-07.2e", 18 * math.exp(mu + z90 * sd))
v.check("Ex 28-07.2c1", 18 * math.exp(mu + sd ** 2 / 2))
sc2 = sd * math.sqrt(1 + 1 / 4)
v.check("Ex 28-07.2f", 100 * stats.t.cdf(-mu / sc2, 3))
v.check("Ex 28-07.2g", 18 * math.exp(mu + stats.t.ppf(0.9, 3) * sc2))
v.check("Txt 28-07.1", stats.t.ppf(0.9, 3))
v.assert_true("Ex 2: z0.9 = 1.2816", abs(z90 - 1.2816) < 1e-4)

# --- Example 28-07.3 ---------------------------------------------------------------------
for k, ida, idb in ((1, "Ex 28-07.3a", "Ex 28-07.3b"), (2, "Ex 28-07.3a1", "Ex 28-07.3b1"),
                    (3, "Ex 28-07.3a2", "Ex 28-07.3b2")):
    v.check(ida, 100 * 0.12 ** k)
    v.check(idb, 100 * (1 - 0.88 ** 2) ** k)
q2 = 1 - 0.88 ** 2
v.check("Ex 28-07.3c", 100 * (1 - (1 - q2) ** 6))
v.check("Ex 28-07.3d", 1 / (1 - 0.88 ** 2))
v.assert_true("Ex 3: Monte Carlo two owners within 0.2 points", abs(loss_mc(q2, 2) - q2 ** 2) < 0.002)

# --- Example 28-07.4 ---------------------------------------------------------------------
w = np.array([0.25, 0.20, 0.20, 0.15, 0.10, 0.10])
s1 = np.array([4, 3, 2, 4, 3, 2])
s2 = np.array([4, 3, 4, 4, 3, 2])
ws1, gs1 = float(w @ s1), float(np.prod(s1 ** w))
ws2, gs2 = float(w @ s2), float(np.prod(s2 ** w))
v.check("Ex 28-07.4a", ws1)
v.check("Ex 28-07.4a1", gs1)
v.check("Ex 28-07.4b", ws2)
v.check("Ex 28-07.4b1", gs2)
v.check("Ex 28-07.4c", gs2 - gs1)
v.check("Ex 28-07.4c1", ws2 - ws1)
v.assert_true("Ex 4: gate passes (lowest 2)", te.gate_passes(list(s1)))

# --- Example 28-07.5 ---------------------------------------------------------------------
v.check("Ex 28-07.5a", 60 * 1.5 * 0.70)
v.check("Ex 28-07.5b", 60 * 1.5 * 0.85)
v.check("Ex 28-07.5c", 60 * 1.5 * 0.15)
v.check("Ex 28-07.5d", 60 * 1.5 * 0.15 - 8)
v.check("Ex 28-07.5e", 100 / (60 * 1.5))

# --- Example 28-07.6 ---------------------------------------------------------------------
h6 = 2e6 * 0.5 / (2000 * 0.8)
v.check("Ex 28-07.6a", h6)
v.check("Ex 28-07.6a1", h6 / 24)
v.check("Ex 28-07.6b", 2e6 * 0.5 / (5000 * 0.8) / 24)

# --- Problems 28-07.2 and 28-07.3 --------------------------------------------------
v.check("28-07.2a", 100 * post_mean_num(1, 3))
v.check("28-07.2b", 3 / 13)
v.check("28-07.2c", 100 * post_mean_num(6, 8))
v.check("28-07.2d", 8 / 18)
v.check("28-07.3a", 100 * post_quantile_num(4, 5, 0.025))
v.check("28-07.3b", 100 * post_quantile_num(4, 5, 0.975))

# --- Problem 28-07.4 ---------------------------------------------------------------------
l4 = np.log([1.15, 1.35, 1.50])
m4, s4 = l4.mean(), l4.std(ddof=1)
v.check("28-07.4a", math.exp(m4))
v.check("28-07.4b", 24 * math.exp(m4))
v.check("28-07.4c", s4)
v.check("28-07.4d", 100 * phi(-m4 / s4))

# --- Problems 28-07.5 to 28-07.11 ------------------------------------------------------
q3 = 1 - 0.85 ** 3
for k, a, b in ((1, "28-07.5a", "28-07.5d"), (2, "28-07.5b", "28-07.5e"), (3, "28-07.5c", "28-07.5f")):
    v.check(a, 100 * 0.15 ** k)
    v.check(b, 100 * q3 ** k)
v.check("28-07.6", 100 * (1 - (1 - q2) ** 4))
w7, s7 = np.array([0.30, 0.25, 0.25, 0.20]), np.array([5, 4, 1, 4])
v.check("28-07.7a", float(w7 @ s7))
v.check("28-07.7b", float(np.prod(s7 ** w7)))
v.assert_true("P7: gate fails", not te.gate_passes(list(s7)))
v.check("28-07.8a", 40 * 1.2 * 0.65)
v.check("28-07.8b", 40 * 1.2 * 0.80)
v.check("28-07.8c", 40 * 1.2 * 0.15)
v.check("28-07.8d", 100 / (40 * 1.2))
v.check("28-07.9", 3e6 * 0.25 / (1000 * 0.75) / 24)
v.check("28-07.10a", 15 + 0.49 * 40)
v.check("28-07.10b", 0.51 * 40)
v.check("28-07.10c", (15 + 0.49 * 40) / (0.51 * 40))
v.assert_true("P10: head-count ratio understates effort by more than four times",
              ((15 + 0.49 * 40) / (0.51 * 40)) / (15 / 40) > 4)
ch20, ch30 = math.comb(20, 2), math.comb(30, 2)
v.check("28-07.11a", ch20)
v.check("28-07.11b", ch30)
v.check("28-07.11c", ch30 / ch20)

# --- Problem 28-07.12 ---------------------------------------------------------------------
for k, ident in ((1, "28-07.12a"), (2, "28-07.12b"), (3, "28-07.12c")):
    exact = 0.05 + 0.95 * 0.2 ** k
    v.check(ident, 100 * exact)
    v.assert_true(f"P12c: Monte Carlo k={k} within 0.3 points", abs(loss_mc(0.2, k, c=0.05) - exact) < 0.003)
for s, n in ((0, 3), (3, 3), (7, 12)):
    wgt = n / (10 + n)
    v.assert_true(f"P12a: mean is the weighted average for {s}/{n}",
                  abs(post_mean_num(s, n) - ((1 - wgt) * 0.14 + wgt * (s / n if n else 0))) < 1e-9)

# --- Lab ----------------------------------------------------------------------------------
v.check("Lab 28-07.a", 100 * post_mean_num(5, 5))
v.check("Lab 28-07.b", 24 * math.exp(mu + z90 * sd))
v.check("Lab 28-07.c", 100 * (1 - 0.88 ** 3) ** 2)
v.check("Lab 28-07.d", 60 * 1.5 * 0.15)

l4 = np.log([1.15, 1.35, 1.50])
sc4 = l4.std(ddof=1) * math.sqrt(1 + 1 / 3)
v.check("28-07.4e", 100 * stats.t.cdf(-l4.mean() / sc4, 2))
v.check("28-07.4f", 24 * math.exp(l4.mean() + stats.t.ppf(0.9, 2) * sc4))
v.assert_true("t_0.9;2 is 1.886", abs(stats.t.ppf(0.9, 2) - 1.886) < 5e-4)

v.check("28-07.3c", 100 * stats.beta.sf(0.14, 5.4, 9.6))

v.check("28-07.10d", (34.6 / 20.4) / (15 / 40))
v.check("28-07.10e", 1.49 / 0.51)

sys.exit(v.finish())
