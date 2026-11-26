#!/usr/bin/env python3
"""Verify every number in chapter 28-01 (a framework for evaluating a chip company's
technology), its problems and its lab.

Independent routes (the lab module uses closed forms):
- scorecards by numpy dot products and log-sums; score variance as w^T Sigma w from an
  explicit covariance matrix, with Monte Carlo cross-checks of the rank-reversal
  probability;
- posteriors by the full form of Bayes' rule (joint likelihoods over T and not-T), not
  the odds form;
- spin statistics with exact fractions;
- the value of information by enumerating the decision tree (test result, then the best
  action), not by the EVSI formula.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import dilmodel as dm  # noqa: E402

v = Verifier.from_files("28-01", ROOT / "chapters" / "28-01-technology-evaluation-framework.md",
                        ROOT / "solutions" / "28-01-solutions.md", LAB / "README.md")


def arith(w, s):
    return float(np.dot(w, s))


def geo(w, s):
    return float(np.exp(np.dot(w, np.log(s))))


def cov_var(w, sig, rho=0.0):
    w, sig = np.asarray(w, float), np.asarray(sig, float)
    corr = np.full((len(w), len(w)), rho)
    np.fill_diagonal(corr, 1.0)
    cov = corr * np.outer(sig, sig)
    return float(w @ cov @ w)


def bayes_full(prior, likelihoods):
    """likelihoods: list of (P(E|T), P(E|not T)); conditional independence assumed."""
    jt, jf = prior, 1 - prior
    for pt, pf in likelihoods:
        jt *= pt
        jf *= pf
    return jt / (jt + jf)


def tree_value(p, gain, loss, sens=None, spec=None):
    """Best expected value of the buy-or-pass decision, optionally after a test."""
    if sens is None:
        return max(p * gain + (1 - p) * loss, 0.0)
    total = 0.0
    for result in ("pass", "fail"):
        pw = p * (sens if result == "pass" else 1 - sens)
        pb = (1 - p) * ((1 - spec) if result == "pass" else spec)
        pr = pw + pb
        total += pr * max((pw * gain + pb * loss) / pr, 0.0)
    return total


# ---------------------------------------------------------------------------
# Examples
# ---------------------------------------------------------------------------
# Inputs typed from the chapter's Example 28-01.1 table (independent of the lab module)
W = [0.20, 0.15, 0.15, 0.15, 0.10, 0.15, 0.10]
A = [4.5, 4.0, 3.0, 4.5, 4.0, 2.0, 3.5]
B = [3.5, 3.5, 4.0, 3.5, 3.5, 4.0, 3.5]
SA = [0.75, 0.5, 0.5, 0.75, 0.5, 0.5, 0.5]
SB = [0.4] * 7
v.assert_true("lab module inputs match the chapter",
              (dm.WEIGHTS, dm.TARGET_A, dm.TARGET_B, dm.SIGMA_A, dm.SIGMA_B) == (W, A, B, SA, SB))
v.check("Ex 28-01.1a", arith(W, A))
v.check("Ex 28-01.1a1", arith(W, B))
v.check("Ex 28-01.1a2", arith(W, A) - arith(W, B))
v.check("Ex 28-01.1b0", math.log(geo(W, A)))
v.check("Ex 28-01.1b", geo(W, A))
v.check("Ex 28-01.1b1", geo(W, B))
v.assert_true("geometric score never exceeds arithmetic", geo(W, A) <= arith(W, A) and geo(W, B) <= arith(W, B))

terms = [w ** 2 * (a ** 2 + b ** 2) for w, a, b in zip(W, SA, SB)]
v.check("Ex 28-01.2a0", terms[0])
v.check("Ex 28-01.2a1", terms[3])
v.check("Ex 28-01.2a2", terms[1])
v.check("Ex 28-01.2a3", terms[4])
var_d = cov_var(W, SA) + cov_var(W, SB)
v.assert_true("variance terms sum to the covariance-matrix variance", abs(sum(terms) - var_d) < 1e-12)
v.check("Ex 28-01.2a", var_d)
sd_d = math.sqrt(var_d)
v.check("Ex 28-01.2a4", sd_d)
mu_d = arith(W, A) - arith(W, B)
v.check("Ex 28-01.2a5", mu_d / sd_d)
p_rev = stats.norm.cdf(-mu_d / sd_d)
v.check("Ex 28-01.2b", 100 * p_rev)
rng = np.random.default_rng(3)
draw_a = rng.normal(A, SA, size=(400_000, 7)) @ np.asarray(W)
draw_b = rng.normal(B, SB, size=(400_000, 7)) @ np.asarray(W)
v.assert_true("Monte Carlo rank reversal within 0.5 points", abs(np.mean(draw_b > draw_a) - p_rev) < 0.005)
v.check("Ex 28-01.2c", 100 * terms[0] / var_d)
v.check("Ex 28-01.2c1", 100 * terms[3] / var_d)
v.check("Ex 28-01.2c2", 100 * terms[5] / var_d)

v.check("Ex 28-01.3a", 0.25 / 0.75)
p3 = bayes_full(0.25, [(0.9, 0.3), (0.8, 0.2), (0.3, 0.6)])
v.check("Ex 28-01.3b", p3 / (1 - p3))
v.check("Ex 28-01.3b1", 100 * p3)
# correlated case: the customer's result given the demo has likelihood ratio 1.5
p3c = bayes_full(0.25, [(0.9, 0.3), (0.6, 0.4), (0.3, 0.6)])
v.check("Ex 28-01.3c", p3c / (1 - p3c))
v.check("Ex 28-01.3c1", 100 * p3c)

dist = {1: 14, 2: 25, 3: 28, 4: 16, 5: 10, 6: 4}
tot = sum(dist.values())
mean_k = Fraction(sum(k * n for k, n in dist.items()), tot)
v.check("Ex 28-01.4a", float(mean_k))
v.check("Ex 28-01.4b", 100 * float(Fraction(dist[1] + dist[2], tot)))
beyond2 = Fraction(sum((k - 2) * n for k, n in dist.items() if k > 2), tot)
v.check("Ex 28-01.4c", float(beyond2))
v.check("Ex 28-01.4d", float(4 * beyond2))
v.check("Ex 28-01.4d1", float(25 * beyond2))
raw = {1: 14, 2: 25, 3: 28, 4: 16, 5: 10, 6: 4, 7: 3}
v.check("Ex 28-01.4e", sum((k - 2) * q for k, q in raw.items() if k > 2) / 100)

p5 = 0.6 * 0.5
v.check("Ex 28-01.5a", p5)
df5 = math.exp(3.2 * math.log(1.10))
v.check("Ex 28-01.5b0", df5)
pv5 = p5 * 2.25 / df5
v.check("Ex 28-01.5b", pv5)
v.check("Ex 28-01.5c", 3.25 + pv5)
v.check("Ex 28-01.5c1", 3.25 + 2.25)
p_be = (4.0 - 3.25) * df5 / 2.25
v.check("Ex 28-01.5d", p_be)
v.assert_true("break-even probability reproduces 4.0 B", abs(3.25 + p_be * 2.25 / df5 - 4.0) < 1e-12)

e_now = tree_value(0.4, 500, -200)
v.check("Ex 28-01.6a", e_now)
v.check("Ex 28-01.6a1", 0.4 * 500 - e_now)
pp = 0.4 * 0.8 + 0.6 * 0.1
v.check("Ex 28-01.6b", pp)
qp = bayes_full(0.4, [(0.8, 0.1)])
qf = bayes_full(0.4, [(0.2, 0.9)])
v.check("Ex 28-01.6b1", qp)
v.check("Ex 28-01.6b2", qf)
v.check("Ex 28-01.6c", qp * 500 - (1 - qp) * 200)
v.check("Ex 28-01.6c1", qf * 500 - (1 - qf) * 200)
v.check("Ex 28-01.6d", tree_value(0.4, 500, -200, 0.8, 0.9) - e_now)
v.assert_true("lab EVSI agrees with the tree", abs(dm.evsi(0.4, 500, -200, 0.8, 0.9)[0]
                                                    - (tree_value(0.4, 500, -200, 0.8, 0.9) - e_now)) < 1e-9)

v.check("Txt 28-01.1", (0.8 / 0.2) / (0.2 / 0.8))
v.check("Txt 28-01.2", 0.8 ** 4)

# ---------------------------------------------------------------------------
# Solutions
# ---------------------------------------------------------------------------
w4 = [0.3, 0.3, 0.2, 0.2]
X, Y = [5, 5, 1, 4], [4, 4, 3, 3.5]
v.check("28-01.2a", arith(w4, X))
v.check("28-01.2b", arith(w4, Y))
v.check("28-01.2c", geo(w4, X))
v.check("28-01.2d", geo(w4, Y))
X3 = [5, 5, 3, 4]
v.check("28-01.3a", arith(w4, X3))
v.check("28-01.3b", geo(w4, X3))
v.assert_true("X fails the IP gate", not dm.passes_gates(X, [None, None, 2, None]))

sx = [1.0, 0.5, 0.5, 0.3]
vx = cov_var(w4, sx)
v.check("28-01.4a", vx)
v.check("28-01.4b", math.sqrt(vx))
v.check("28-01.4c", 100 * (0.3 * 1.0) ** 2 / vx)
vx2 = cov_var(w4, [0.4, 0.5, 0.5, 0.3])
v.check("28-01.4d", vx2)
v.check("28-01.4e", math.sqrt(vx2))

vy = cov_var(w4, [0.4] * 4)
v.check("28-01.5a", vy)
sd5 = math.sqrt(vx + vy)
v.check("28-01.5b", sd5)
v.check("28-01.5c", 100 * stats.norm.cdf(-0.3 / sd5))
ws = [a * b for a, b in zip(w4, sx)]
pair_sum = sum(ws[i] * ws[j] for i in range(4) for j in range(i + 1, 4))
v.check("28-01.5d", pair_sum)
vxc = cov_var(w4, sx, 0.6)
v.check("28-01.5e", vxc)
sd5c = math.sqrt(vxc + vy)
v.check("28-01.5f", sd5c)
v.check("28-01.5g", 100 * stats.norm.cdf(-0.3 / sd5c))
v.assert_true("lab variance with correlation agrees", abs(dm.score_variance(w4, sx, 0.6) - vxc) < 1e-12)

v.check("28-01.6a", 0.3 / 0.7)
# likelihood pairs chosen with the stated ratios (only the ratios matter)
p6 = bayes_full(0.3, [(0.8, 0.4), (0.5, 0.1), (0.3, 0.6)])
v.check("28-01.6b", p6 / (1 - p6))
v.check("28-01.6c", 100 * p6)
p7a = bayes_full(0.3, [(0.8, 0.4), (0.5, 0.1), (0.3, 0.6), (0.5, 0.1)])
p7b = bayes_full(0.3, [(0.8, 0.4), (0.5, 0.1), (0.3, 0.6), (0.6, 0.5)])
v.check("28-01.7a", p7a / (1 - p7a))
v.check("28-01.7b", 100 * p7a)
v.check("28-01.7c", p7b / (1 - p7b))
v.check("28-01.7d", 100 * p7b)

def lr_needed(prior, target):
    return (target / (1 - target)) / (prior / (1 - prior))


v.check("28-01.8a", lr_needed(0.1, 0.5))
v.check("28-01.8b", lr_needed(0.1, 0.9))
v.assert_true("lab required_lr agrees", abs(dm.required_lr(0.1, 0.9) - lr_needed(0.1, 0.9)) < 1e-12)
n8 = 0
while bayes_full(0.1, [(0.9, 0.3)] * n8) < 0.9 - 1e-12:
    n8 += 1
v.check("28-01.8c", n8)

v.check("28-01.9a", 100 * float(Fraction(dist[1] + dist[2] + dist[3], tot)))
beyond3 = Fraction(sum((k - 3) * n for k, n in dist.items() if k > 3), tot)
v.check("28-01.9b", float(beyond3))
v.check("28-01.9c", float(5 * beyond3))
v.check("28-01.9d", float(30 * beyond3))

p10 = 0.8 * 0.5 * 0.9 * 0.6
v.check("28-01.10a", p10)
v.check("28-01.10b", p10 * 1.2 + (1 - p10) * 0.1)
v.check("28-01.10c", 0.8 * (1 - 0.5))

df11 = 1.12 ** 3
v.check("28-01.11a", df11)
v.check("28-01.11b", 0.7 * 400 / df11)
v.check("28-01.11c", 600 + 0.7 * 400 / df11)
v.check("28-01.11d", 0.3 * 400 / df11)
v.check("28-01.11e", 600 + 0.3 * 400 / df11)
v.check("28-01.11f", 0.4 * 400 / df11)
v.assert_true("both sides prefer the earn-out to 700 cash",
              600 + 0.7 * 400 / df11 > 700 and 600 + 0.3 * 400 / df11 < 700)

for pre, k in ((0.9, "abcdef"), (0.2, "ghijkl")):
    now = pre * 500 + (1 - pre) * (-200)
    v.check(f"28-01.12{k[0]}", now)
    v.check(f"28-01.12{k[1]}", pre * 500 - max(now, 0))
    v.check(f"28-01.12{k[2]}", pre * 0.8 + (1 - pre) * 0.1)
    if pre == 0.9:
        q = bayes_full(pre, [(0.2, 0.9)])
    else:
        q = bayes_full(pre, [(0.8, 0.1)])
    v.check(f"28-01.12{k[3]}", q)
    v.check(f"28-01.12{k[4]}", q * 500 - (1 - q) * 200)
    v.check(f"28-01.12{k[5]}", tree_value(pre, 500, -200, 0.8, 0.9) - max(now, 0))

v.check("28-01.13a", 150 / 3.0)
need = 24 * 3.0 + 2 * 45
v.check("28-01.13b", need)
v.check("28-01.13c", need - 150)
v.check("28-01.13d", need + 20 - 150)
v.check("28-01.13e", (150 - 2 * 45) / 3.0)

for rho, ka, kb in ((0.0, "a", "b"), (0.5, "c", "d")):
    var = cov_var([1 / 7] * 7, [0.5] * 7, rho)
    v.assert_true(f"closed form matches the matrix at rho = {rho}",
                  abs(var - 0.25 / 7 * (1 + 6 * rho)) < 1e-12)
    v.check(f"28-01.14{ka}", var)
    v.check(f"28-01.14{kb}", math.sqrt(var))
lim = cov_var([1 / 2000] * 2000, [0.5] * 2000, 0.5)
v.assert_true("large-n variance approaches rho sigma^2", abs(lim - 0.125) < 1e-4)
v.check("28-01.14e", 0.5 * 0.25)
v.check("28-01.14f", math.sqrt(0.125))

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
A2 = list(A)
A2[0] = 4.0
SA2 = list(SA)
SA2[0] = 0.3
v.check("Lab 28-01.a", arith(W, A2))
v.check("Lab 28-01.a3", arith(W, B) - arith(W, A2))
sd_a = math.sqrt(cov_var(W, SA2) + cov_var(W, SB))
v.check("Lab 28-01.a1", sd_a)
v.check("Lab 28-01.a2", 100 * stats.norm.cdf((arith(W, B) - arith(W, A2)) / sd_a))
v.check("Lab 28-01.b", 100 * bayes_full(0.25, [(0.9, 0.3), (0.8, 0.2), (0.3, 0.6), (0.2, 0.8)]))
v.check("Lab 28-01.c", 100 * float(Fraction(dist[1] + dist[2] + dist[3], tot)))
v.check("Lab 28-01.c1", float(beyond3))
v.check("Lab 28-01.c2", float(4 * beyond3))
v.check("Lab 28-01.c3", float(25 * beyond3))
pp_d = 0.4 * 0.8 + 0.6 * 0.3
q_d = 0.4 * 0.8 / pp_d
v.check("Lab 28-01.d", pp_d)
v.check("Lab 28-01.d1", q_d)
v.check("Lab 28-01.d2", q_d * 500 - (1 - q_d) * 200)
v.check("Lab 28-01.d3", tree_value(0.4, 500, -200, 0.8, 0.7) - tree_value(0.4, 500, -200))

sys.exit(v.finish())
