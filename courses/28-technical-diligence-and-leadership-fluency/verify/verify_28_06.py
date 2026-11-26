#!/usr/bin/env python3
"""Verify every number in chapter 28-06 (red flags and green flags), its problems and its
lab.

Independent routes (the lab module uses closed forms and scipy):
- posteriors from an explicit joint-probability table (prior x likelihood, normalized);
- binomial tails by exact summation with math.comb, cross-checked by Monte Carlo;
- key-person risk by simulating departures person-year by person-year;
- HHI from shares; funnel values by explicit year-by-year cash flows.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import flagmodel as fm  # noqa: E402

v = Verifier.from_files("28-06", ROOT / "chapters" / "28-06-red-and-green-flags.md",
                        ROOT / "solutions" / "28-06-solutions.md", LAB / "README.md")
RNG = np.random.default_rng(2806)


def joint_post(prior, likes):
    """likes: list of (P(e|T), P(e|not T)) for observed evidence. Returns (odds, prob)."""
    a, b = prior, 1 - prior
    for pt, pn in likes:
        a *= pt
        b *= pn
    return a / b, a / (a + b)


def tail_exact(n, p, k):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def tail_mc(n, p, k, trials=400_000):
    return float(np.mean(RNG.binomial(n, p, trials) >= k))


def keyperson_mc(m, q, years, trials=400_000):
    left = RNG.random((trials, m * years)) < q
    return float(np.mean(left.any(axis=1)))


def funnel_cashflows(n_wins, p, life, years, rate):
    per_year = n_wins * p * life / len(years)
    return sum(per_year / (1 + rate) ** y for y in years)


# --- Theory text -------------------------------------------------------------------------
v.check("Txt 28-06.1", 0.6 / 0.1)
v.check("Txt 28-06.2", 0.9 / 0.5)
v.check("Txt 28-06.3", 100 * tail_exact(25, 0.04, 1))
v.check("Txt 28-06.4", 100 * (1 - 0.88 ** 10))
v.check("Txt 28-06.5", 0.4 / 0.9)

# --- Example 28-06.1 ---------------------------------------------------------------------
v.check("Ex 28-06.1a", 0.6 / 0.1)
v.check("Ex 28-06.1a1", (1 - 0.6) / (1 - 0.1))
o, p = joint_post(0.2, [(0.6, 0.1)])
v.check("Ex 28-06.1b", o)
v.check("Ex 28-06.1b1", 100 * p)
o, p = joint_post(0.2, [(0.4, 0.9)])
v.check("Ex 28-06.1c", o)
v.check("Ex 28-06.1c1", 100 * p)
v.assert_true("Ex 1: lab posterior agrees", abs(fm.posterior(0.2, 6)[1] - 0.6) < 1e-12)

# --- Example 28-06.2 ---------------------------------------------------------------------
v.check("Ex 28-06.2a", 100 * tail_exact(25, 0.04, 1))
v.check("Ex 28-06.2a1", 25 * 0.04)
h3, t3 = tail_exact(25, 0.04, 3), tail_exact(25, 0.30, 3)
v.check("Ex 28-06.2b", 100 * h3)
v.check("Ex 28-06.2b1", 25 * 0.30)
v.check("Ex 28-06.2b2", 100 * t3)
v.check("Ex 28-06.2b3", t3 / h3)
h4, t4 = tail_exact(25, 0.04, 4), tail_exact(25, 0.30, 4)
v.check("Ex 28-06.2c", 100 * h4)
v.check("Ex 28-06.2c1", 100 * t4)
v.check("Ex 28-06.2c2", t4 / h4)
lrp, lrm = 0.30 / 0.04, 0.70 / 0.96
exact = {k: stats.binom.pmf(k, 25, 0.30) / stats.binom.pmf(k, 25, 0.04) for k in (3, 4, 5)}
v.assert_true("exact-count LR equals (LR+)^k (LR-)^(n-k)", all(abs(exact[k] - lrp ** k * lrm ** (25 - k)) < 1e-9 * exact[k] for k in exact))
v.check("Ex 28-06.2d", exact[3])
v.check("Ex 28-06.2d1", exact[4])
v.check("Ex 28-06.2d2", exact[5])
v.check("Ex 28-06.2d3", 100 * 0.25 * exact[3] / (1 + 0.25 * exact[3]))
tail3 = stats.binom.sf(2, 25, 0.30) / stats.binom.sf(2, 25, 0.04)
v.check("Ex 28-06.2d4", 100 * 0.25 * tail3 / (1 + 0.25 * tail3))
v.assert_true("Ex 2: Monte Carlo healthy tail within 0.2 points", abs(tail_mc(25, 0.04, 3) - h3) < 0.002)
v.assert_true("Ex 2: lab tail agrees", abs(fm.tail(25, 0.30, 3) - t3) < 1e-12)

# --- Example 28-06.3 ---------------------------------------------------------------------
v.check("Ex 28-06.3a", 100 * (1 - 0.88 ** 5))
v.check("Ex 28-06.3a1", 5 * 0.12)
v.check("Ex 28-06.3b", 100 * (1 - 0.88 ** 10))
v.check("Ex 28-06.3c", 100 * (1 - 0.94 ** 10))
v.assert_true("Ex 3: simulation within 0.3 points", abs(keyperson_mc(5, 0.12, 2) - (1 - 0.88 ** 10)) < 0.003)

# --- Example 28-06.4 ---------------------------------------------------------------------
shares = [0.45, 0.20, 0.10, 0.10] + [0.01] * 15
v.assert_true("Ex 4: shares sum to 1", abs(sum(shares) - 1) < 1e-12)
h = float(np.dot(shares, shares))
v.check("Ex 28-06.4a", h)
v.check("Ex 28-06.4b", 1 / h)
v.check("Ex 28-06.4c", 100 * shares[0])
v.check("Ex 28-06.4c1", 100 * (shares[0] + shares[1]))

# --- Example 28-06.5 ---------------------------------------------------------------------
pv5 = funnel_cashflows(40, 0.5, 3, [2, 3, 4], 0.12)
v.check("Ex 28-06.5a", pv5 / 60)
v.check("Ex 28-06.5b", 40 * 0.5 * 3)
v.check("Ex 28-06.5c", pv5)
v.check("Ex 28-06.5d", 120 / pv5)
v.assert_true("Ex 5: lab funnel agrees", abs(fm.funnel_value(40, 0.5, 3, 2, 3, 0.12) - pv5) < 1e-9)

# --- Example 28-06.6 ---------------------------------------------------------------------
lr = [3, 2.5, 1.5, 0.5, 0.6]
o6 = (0.25 / 0.75) * math.prod(lr)
v.check("Ex 28-06.6a", o6)
v.check("Ex 28-06.6a1", 100 * o6 / (1 + o6))
o6b = (0.25 / 0.75) * math.prod([3, 1.5, 0.5, 0.6])
v.check("Ex 28-06.6b", o6b)
v.check("Ex 28-06.6b1", 100 * o6b / (1 + o6b))

# --- Problem 28-06.2 ---------------------------------------------------------------------
v.check("28-06.2a", 0.5 / 0.05)
v.check("28-06.2b", 0.5 / 0.95)
o, p = joint_post(0.3, [(0.5, 0.05)])
v.check("28-06.2c", o)
v.check("28-06.2d", 100 * p)
o, p = joint_post(0.3, [(0.5, 0.95)])
v.check("28-06.2e", o)
v.check("28-06.2f", 100 * p)

# --- Problems 28-06.3 and 28-06.4 ---------------------------------------------------
v.check("28-06.3a", 100 * tail_exact(40, 0.025, 1))
v.check("28-06.3b", 40 * 0.025)
v.check("28-06.3c", 100 * tail_exact(40, 0.025, 2))
v.check("28-06.3d", 100 * (1 - math.exp(-1)))
s2, f2 = tail_exact(25, 0.30, 2), tail_exact(25, 0.04, 2)
v.check("28-06.4a", 100 * s2)
v.check("28-06.4b", 100 * f2)
v.check("28-06.4c", s2 / f2)
s5, f5 = tail_exact(25, 0.30, 5), tail_exact(25, 0.04, 5)
v.check("28-06.4d", 100 * s5)
v.check("28-06.4e", 100 * f5)
v.check("28-06.4f", s5 / f5)

# --- Problems 28-06.5 to 28-06.8 -----------------------------------------------------
v.check("28-06.5a", 100 * (1 - 0.85 ** 3))
v.check("28-06.5b", 100 * (1 - 0.85 ** 9))
v.check("28-06.5c", 100 * (1 - 0.925 ** 9))
sh6 = [0.30, 0.25, 0.15, 0.10, 0.10, 0.10]
v.check("28-06.6a", float(np.dot(sh6, sh6)))
v.check("28-06.6b", 1 / float(np.dot(sh6, sh6)))
v.check("28-06.6c", 100 * (sh6[0] + sh6[1]))
pv7 = funnel_cashflows(60, 0.35, 2, [1, 2, 3], 0.10)
v.check("28-06.7a", pv7 / 42)
v.check("28-06.7b", 60 * 0.35 * 2)
v.check("28-06.7c", pv7)
v.check("28-06.7d", 120 / pv7)
o8 = (0.4 / 0.6) * 4 * 2 * 0.5
v.check("28-06.8a", o8)
v.check("28-06.8b", 100 * o8 / (1 + o8))
o8b = (0.4 / 0.6) * 4 * 0.5
v.check("28-06.8c", o8b)
v.check("28-06.8d", 100 * o8b / (1 + o8b))

# --- Problems 28-06.9 to 28-06.11 ----------------------------------------------------
v.check("28-06.9a", 100 * 0.14 ** 3)
v.check("28-06.9b", 100 * 0.30 ** 3)
v.check("28-06.9c", 100 * 0.05 ** 3)
spins = {1: 14, 2: 25, 3: 28, 4: 16, 5: 10, 6: 4}  # chart readings, R-645
v.check("28-06.9d", sum(val for k, val in spins.items() if k >= 4))
v.check("28-06.10a", 15 / 40)
v.check("28-06.10b", 40 - 15)
v.check("28-06.10c", (40 - 15) * 0.25)
mean_over = np.mean([25, 40, 30])
v.check("28-06.11a", mean_over)
v.check("28-06.11b", 18 * (1 + mean_over / 100))

# --- Problem 28-06.12 identities ----------------------------------------------------
for f, n in ((0.01, 30), (0.03, 10), (0.05, 5)):
    v.assert_true(f"P12b: exponential approximation within 1.5 points (f={f}, n={n})",
                  abs((1 - (1 - f) ** n) - (1 - math.exp(-n * f))) < 0.015)
for sh in ([0.5, 0.3, 0.2], [0.25] * 4, [0.7, 0.1, 0.1, 0.1]):
    v.assert_true(f"P12c: HHI >= 1/N for {sh}", float(np.dot(sh, sh)) >= 1 / len(sh) - 1e-12)
lrs = [tail_exact(25, 0.3, k) / tail_exact(25, 0.04, k) for k in range(1, 9)]
v.assert_true("P12d: tail ratio rises with the threshold", all(b > a for a, b in zip(lrs, lrs[1:])))

# --- Lab ----------------------------------------------------------------------------------
v.check("Lab 28-06.a", 100 * tail_exact(50, 0.03, 1))
k_best = next(k for k in range(1, 26) if tail_exact(25, 0.3, k) / tail_exact(25, 0.04, k) > 100)
v.check("Lab 28-06.b", k_best)
v.check("Lab 28-06.b1", 100 * tail_exact(25, 0.3, k_best))
v.check("Lab 28-06.c", 100 * (1 - 0.88 ** 15))
v.check("Lab 28-06.d", funnel_cashflows(40, 0.4, 3, [2, 3, 4], 0.12))
v.check("Lab 28-06.e", 100 * funnel_cashflows(40, 0.4, 3, [2, 3, 4], 0.12) / 120)
for f_, n_ in ((0.02, 34), (0.05, 14), (0.10, 7)):
    v.assert_true(f"alt text: 50% false-alarm length at f={f_} is about {n_}", round(math.log(0.5) / math.log(1 - f_)) == n_)

v.check("28-06.12e", stats.binom.pmf(2, 25, 0.30) / stats.binom.pmf(2, 25, 0.04))

# Problem 28-06.13: chain rule for dependent flags
pT1, pH1 = 0.6, 0.2
pT2_1, pH2_1, pT2_0, pH2_0 = 0.9, 0.6, 0.2, 0.05
lr1 = pT1 / pH1
lr2 = (pT2_1 * pT1 + pT2_0 * (1 - pT1)) / (pH2_1 * pH1 + pH2_0 * (1 - pH1))
joint = (pT1 * pT2_1) / (pH1 * pH2_1)
v.assert_true("P13: chain rule equals LR(F1) * LR(F2|F1)", abs(joint - lr1 * (pT2_1 / pH2_1)) < 1e-12)
post = lambda lr: 100 * (lr / 3) / (1 + lr / 3)
v.check("28-06.13a", lr1)
v.check("28-06.13b", lr2)
v.check("28-06.13c", joint)
v.check("28-06.13d", lr1 * lr2)
v.check("28-06.13e", post(joint))
v.check("28-06.13f", post(lr1 * lr2))
v.check("28-06.13g", post(max(lr1, lr2)))

v.check("28-06.9e", 100 * 30 / 97)
v.check("28-06.9f", 100 * (1.4 + 3) / (10 + 3))

sys.exit(v.finish())
