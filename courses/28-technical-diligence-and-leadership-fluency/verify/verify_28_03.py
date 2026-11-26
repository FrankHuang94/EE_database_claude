#!/usr/bin/env python3
"""Verify every number in chapter 28-03 (maturity scales for silicon), its problems and
its lab.

Independent routes (the lab module uses closed forms):
- stage chains by explicit loops over the chain and a Monte Carlo check of the
  probability of reaching production;
- acceleration factors from the Arrhenius ratio with scipy's Boltzmann constant;
- failure-rate bounds by solving the Poisson tail equation P(N <= r) = 1 - C for lambda
  with a root finder (not the chi-square quantile);
- the Goel-Okumoto fits by nonlinear least squares and by root-finding on the ratio
  equation.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import matscale as ms  # noqa: E402

v = Verifier.from_files("28-03", ROOT / "chapters" / "28-03-silicon-maturity-scales.md",
                        ROOT / "solutions" / "28-03-solutions.md", LAB / "README.md")
KB = constants.k / constants.e  # eV/K
CHAIN = [(0.95, 4.5), (0.80, 6), (0.85, 5), (0.95, 2)]


def chain(stages, rate=0.15):
    p, t = 1.0, 0.0
    for q, m in stages:
        p *= q
        t += m
    return p, t, (1 + rate) ** (t / 12), p / (1 + rate) ** (t / 12)


def af(ea, tu, ts):
    return math.exp(ea / KB * (1 / (tu + 273.15) - 1 / (ts + 273.15)))


def bound_fit(n, hours, failures, accel, conf):
    """Solve P(N <= r | lambda T) = 1 - C for lambda (Poisson tail), return FIT."""
    t_eq = n * hours * accel
    g = lambda lam: stats.poisson.cdf(failures, lam * t_eq) - (1 - conf)  # noqa: E731
    lam = optimize.brentq(g, 1e-15, 1e-3, xtol=1e-22)
    return lam * 1e9


def go_ratio_fit(t1, m1, m2):
    """Root-find b in m2/m1 = (1 - exp(-2 b t1))/(1 - exp(-b t1)), then a."""
    b = optimize.brentq(lambda bb: (1 - math.exp(-2 * bb * t1)) / (1 - math.exp(-bb * t1)) - m2 / m1,
                        1e-6, 10)
    return m1 / (1 - math.exp(-b * t1)), b


# ---------------------------------------------------------------------------
# Example 28-03.2
# ---------------------------------------------------------------------------
p2, t2, d2, v2 = chain(CHAIN)
v.check("Ex 28-03.2a", p2)
v.check("Ex 28-03.2a1", t2)
v.check("Ex 28-03.2b", d2)
v.check("Ex 28-03.2b1", v2)
p4, t4, d4, v4 = chain(CHAIN[2:])
v.check("Ex 28-03.2c", p4)
v.check("Ex 28-03.2c1", t4)
v.check("Ex 28-03.2c2", d4)
v.check("Ex 28-03.2c3", v4)
v.check("Ex 28-03.2d", v4 / v2)
rng = np.random.default_rng(9)
sims = np.all(rng.random((400_000, 4)) < np.array([q for q, _ in CHAIN]), axis=1).mean()
v.assert_true("Monte Carlo chain probability agrees", abs(sims - p2) < 0.003)
v.assert_true("lab value multiplier agrees", abs(ms.value_multiplier(CHAIN, 0.15) - v2) < 1e-12)

# Example 28-03.3
a55 = af(0.7, 55, 125)
v.check("Ex 28-03.3a", a55)
v.check("Ex 28-03.3b", 231 * 1000 * a55)
v.check("Ex 28-03.3c", stats.chi2.ppf(0.6, 2))
v.check("Ex 28-03.3c1", bound_fit(231, 1000, 0, a55, 0.6))
v.check("Ex 28-03.3c2", stats.chi2.ppf(0.9, 2))
v.check("Ex 28-03.3c3", bound_fit(231, 1000, 0, a55, 0.9))
v.check("Ex 28-03.3d", bound_fit(7859, 1000, 0, 78.6, 0.6))
v.assert_true("lab chi-square bound agrees with the Poisson tail",
              abs(ms.fit_upper(231, 1000, 0, a55, 0.6) - bound_fit(231, 1000, 0, a55, 0.6)) < 1e-6)
v.check("Txt 28-03.1", math.exp(0.7 / 8.6e-5 * (1 / 328 - 1 / 398)))
v.check("Txt 28-03.2", bound_fit(231, 1000, 0, a55, 0.6))

# Example 28-03.4
a4, b4 = go_ratio_fit(10, 300, 420)
v.check("Ex 28-03.4a", b4)
v.check("Ex 28-03.4a1", a4)
v.check("Ex 28-03.4b", a4 * math.exp(-b4 * 20))
v.check("Ex 28-03.4b1", a4 * b4 * math.exp(-b4 * 20))
ts = optimize.brentq(lambda t: a4 * b4 * math.exp(-b4 * t) - 1.0, 0, 500)
v.check("Ex 28-03.4c", ts)
v.check("Ex 28-03.4c1", ts - 20)
v.check("Ex 28-03.4d", a4 * math.exp(-b4 * ts))
v.check("Ex 28-03.4e", a4 * math.exp(-b4 * 26))
v.check("Ex 28-03.4f", 100 * 420 / a4)

# Example 28-03.5
v.check("Ex 28-03.5a", stats.chi2.ppf(0.6, 4))
n0 = 1
while bound_fit(n0, 1000, 0, a55, 0.6) > 10:
    n0 += 1
v.check("Ex 28-03.5b", n0)
n1 = n0
while bound_fit(n1, 1000, 1, a55, 0.6) > 10:
    n1 += 1
v.check("Ex 28-03.5c", n1)

# ---------------------------------------------------------------------------
# Solutions
# ---------------------------------------------------------------------------
p3, t3, _, v3 = chain(CHAIN[1:])
v.check("28-03.3a", p3)
v.check("28-03.3b", t3)
v.check("28-03.3c", v3)
_, _, d5, v5 = chain(CHAIN[3:])
v.check("28-03.4a", d5)
v.check("28-03.4b", v5)
v.check("28-03.4c", v5 / v2)
a70 = af(0.7, 70, 125)
v.check("28-03.5a", a70)
v.check("28-03.5b", af(0.9, 70, 125))
v.check("28-03.6", bound_fit(462, 1000, 0, a70, 0.6))
v.check("28-03.7", bound_fit(462, 1000, 1, a70, 0.6))
v.check("28-03.8a", stats.chi2.ppf(0.9, 2) * 1e9 / (2 * 5 * 1000 * a55))
n8 = 5000
while bound_fit(n8, 1000, 0, a55, 0.9) > 5:
    n8 += 1
v.check("28-03.8b", n8)
a9, b9 = go_ratio_fit(8, 160, 256)
v.check("28-03.9a", b9)
v.check("28-03.9b", a9)
v.check("28-03.9c", a9 * math.exp(-b9 * 16))
v.check("28-03.9d", a9 * b9 * math.exp(-b9 * 16))
t10 = optimize.brentq(lambda t: a9 * b9 * math.exp(-b9 * t) - 2.0, 0, 500)
v.check("28-03.10a", t10)
v.check("28-03.10b", t10 - 16)
v.check("28-03.10c", a9 * math.exp(-b9 * t10))
v.check("28-03.11", 1000)

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
for k, key in enumerate(("Lab 28-03.a", "Lab 28-03.a1", "Lab 28-03.a2", "Lab 28-03.a3")):
    v.check(key, chain(CHAIN[k:])[3])
v.check("Lab 28-03.b", bound_fit(1000, 1000, 0, a55, 0.6))
v.check("Lab 28-03.b1", bound_fit(1000, 1000, 0, a55, 0.9))
wk = np.arange(1, 21)
cnt = np.round(500 * (1 - np.exp(math.log(0.4) / 10 * wk)))
res = optimize.least_squares(lambda p: p[0] * (1 - np.exp(-p[1] * wk)) - cnt, x0=[300, 0.2])
af_, bf_ = res.x
v.check("Lab 28-03.c", af_)
v.check("Lab 28-03.c1", bf_)
v.check("Lab 28-03.c2", af_ * math.exp(-bf_ * 20))
for ea, k1, k2 in ((0.5, "d", "d1"), (1.0, "d2", "d3")):
    a_ = af(ea, 55, 125)
    v.check(f"Lab 28-03.{k1}", a_)
    v.check(f"Lab 28-03.{k2}", bound_fit(231, 1000, 0, a_, 0.6))

sys.exit(v.finish())
