#!/usr/bin/env python3
"""Verify every number in chapter 26-02 (design reviews, documentation and standards bodies), its problems
and its lab.

Independent routes:
- reviewer detection by simulating independent reviewers defect by defect, and the optimal team size by
  exhaustive search; the marginal bound by root-finding on the continuous condition;
- capture-recapture against the hypergeometric maximum-likelihood estimate and a Monte Carlo of two reviews;
- ballots by direct vote counting and exhaustive search over vote switches;
- royalties and draft-standard decisions by direct arithmetic and root-finding.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize
from scipy.special import gammaln

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "26-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import reviews  # noqa: E402

v = Verifier.from_files("26-02", ROOT / "chapters" / "26-02-design-reviews-and-standards.md",
                        ROOT / "solutions" / "26-02-solutions.md", LAB / "README.md")
RNG = np.random.default_rng(2602)


def sim_found(p, k, n_def=200_000):
    """Fraction of defects found by k simulated independent reviewers."""
    hits = RNG.random((n_def, k)) < p
    return hits.any(axis=1).mean()


def k_bound(cr, ce, n, p):
    """Continuous k at which the k-th reviewer's saving equals its cost (root-finding)."""
    return optimize.brentq(lambda k: ce * n * (1 - p) ** (k - 1) * p - cr, 0.5, 100)


def hypergeom_mle(n1, n2, m, n_max=10_000):
    """Maximum-likelihood population size for two independent samples (hypergeometric)."""
    best, best_ll = None, -np.inf
    for n in range(n1 + n2 - m, n_max):
        ll = (gammaln(n - n1 + 1) - gammaln(n - n1 - n2 + m + 1) - gammaln(n2 - m + 1)
              - (gammaln(n + 1) - gammaln(n - n2 + 1) - gammaln(n2 + 1)))
        if ll > best_ll:
            best, best_ll = n, ll
    return best


def ballot(group, a, d, ab):
    returned = a + d + ab
    return returned / group, a / (a + d), ab / returned


# ---------------------------------------------------------------- Example 26-02.2
N2, p2, cr2, ce2 = 20, 0.35, 10_000, 10_000
costs = [cr2 * k + ce2 * N2 * (1 - p2) ** k for k in range(1, 8)]
for key, c in zip(("Ex 26-02.2a", "Ex 26-02.2a1", "Ex 26-02.2a2", "Ex 26-02.2a3", "Ex 26-02.2a4", "Ex 26-02.2a5",
                   "Ex 26-02.2a6"), costs):
    v.check(key, c)
v.check("Ex 26-02.2b0", cr2 / (ce2 * N2 * p2))
v.check("Ex 26-02.2b1", math.log(1 - p2))
kb = k_bound(cr2, ce2, N2, p2)
v.check("Ex 26-02.2b", kb)
kopt = int(np.argmin(costs)) + 1
v.assert_true("Ex 2 exhaustive optimum equals the floor of the marginal bound", kopt == math.floor(kb) == reviews.best_k(N2, p2, cr2, ce2))
v.check("Ex 26-02.2b2", kopt)
f5 = 1 - (1 - p2) ** kopt
v.assert_true("Ex 2 simulated detection within 0.5 point", abs(sim_found(p2, kopt) - f5) < 0.005)
v.check("Ex 26-02.2c", 100 * f5)
v.check("Ex 26-02.2c1", N2 * (1 - p2) ** kopt)
fmix = reviews.p_found_mix([(0.70, 0.50), (0.30, 0.0)], kopt)
v.check("Ex 26-02.2d", 100 * fmix)
v.check("Ex 26-02.2d1", N2 * (1 - fmix))
v.check("Ex 26-02.2e", 100 * max(costs[3], costs[5]) / costs[4] - 100)

# ---------------------------------------------------------------- Example 26-02.3
n1, n2, m = 24, 18, 12
v.check("Ex 26-02.3a", m / n2)
v.check("Ex 26-02.3a1", m / n1)
lp = reviews.lincoln_petersen(n1, n2, m)
v.assert_true("Ex 3 hypergeometric MLE within 1 of Lincoln-Petersen (ties at integer values)", abs(hypergeom_mle(n1, n2, m) - lp) <= 1)
v.check("Ex 26-02.3b", lp)
ch = reviews.chapman(n1, n2, m)
v.check("Ex 26-02.3b1", ch)
found = n1 + n2 - m
v.check("Ex 26-02.3c", found)
v.check("Ex 26-02.3c1", lp - found)
v.check("Ex 26-02.3c2", ch - found)

# ---------------------------------------------------------------- Example 26-02.4
r4, a4, ab4 = ballot(180, 108, 30, 12)
v.check("Ex 26-02.4a", 108 + 30 + 12)
v.check("Ex 26-02.4a1", 100 * r4)
v.check("Ex 26-02.4b", 100 * a4)
v.check("Ex 26-02.4c", 100 * ab4)
v.assert_true("Ex 4 passes under the module's rules", reviews.ieee_ballot(180, 108, 30, 12)["passes"])
v.check("Ex 26-02.4d0", 108 + 30)
v.check("Ex 26-02.4d1", 0.75 * 138)
need = min(a for a in range(0, 139) if a / 138 >= 0.75)
v.assert_true("Ex 4 approvals needed matches the module", need == reviews.approvals_needed(108, 30))
v.check("Ex 26-02.4d", need)
switch = max(s for s in range(0, 109) if reviews.ieee_ballot(180, 108 - s, 30 + s, 12)["passes"])
v.check("Ex 26-02.4d2", switch)

# ---------------------------------------------------------------- Example 26-02.5
v.check("Ex 26-02.5a", reviews.royalty_stack([0.005] * 30, 500))
v.check("Ex 26-02.5a1", 30 * 0.005 * 500 / 20)
v.check("Ex 26-02.5b0", 30 * 0.005)
v.check("Ex 26-02.5b", reviews.royalty_stack([0.005] * 30, 20))
v.check("Ex 26-02.5c", reviews.top_down_share(0.05, 500, 0.08))
v.check("Ex 26-02.5c1", 0.05 * 500)
v.check("Ex 26-02.5d", 500 / 20)

# ---------------------------------------------------------------- Example 26-02.6
v.check("Ex 26-02.6a", 6 * 5)
v.check("Ex 26-02.6a1", 0.4 * (3 + 2 * 5))
v.check("Ex 26-02.6a2", reviews.early_start_value(6, 5, 0.4, 3, 2))
v.check("Ex 26-02.6b", 0.4 * (25 + 6 * 5))
v.check("Ex 26-02.6b1", reviews.early_start_value(6, 5, 0.4, 25, 6))
v.check("Ex 26-02.6c", optimize.brentq(lambda p: reviews.early_start_value(6, 5, p, 25, 6), 0, 1))

# ---------------------------------------------------------------- Problem 3
N3, p3, cr3, ce3 = 30, 0.50, 8000, 5000
c3 = [cr3 * k + ce3 * N3 * (1 - p3) ** k for k in range(1, 7)]
v.check("26-02.3a", cr3 / (ce3 * N3 * p3))
kb3 = k_bound(cr3, ce3, N3, p3)
v.check("26-02.3a1", kb3)
k3 = int(np.argmin(c3)) + 1
v.check("26-02.3a2", k3)
v.check("26-02.3b", 100 * (1 - (1 - p3) ** k3))
v.check("26-02.3b1", N3 * (1 - p3) ** k3)
v.check("26-02.3b2", c3[k3 - 1])
for i, c in enumerate(c3, 1):
    v.check(f"26-02.3c{i}", c)
v.check("26-02.3c7", 100 * (max(c3[2], c3[4]) / c3[3] - 1))

# ---------------------------------------------------------------- Problem 4
cl = [(0.60, 0.6), (0.25, 0.2), (0.15, 0.0)]


def mix_sim(k, n_def=300_000):
    cls = RNG.choice(3, size=n_def, p=[0.60, 0.25, 0.15])
    pp = np.array([0.6, 0.2, 0.0])[cls]
    return (RNG.random((n_def, k)) < pp[:, None]).any(axis=1).mean()


v.check("26-02.4a", reviews.p_found_mix(cl, 1))
p43 = reviews.p_found_mix(cl, 3)
v.assert_true("P4 simulated three-reviewer detection within 0.5 point", abs(mix_sim(3) - p43) < 0.005)
v.check("26-02.4b", p43)
v.check("26-02.4c", reviews.p_found_mix(cl, 5))
v.check("26-02.4c1", reviews.p_found_mix(cl, 10))
v.check("26-02.4d", reviews.p_found_mix(cl, 400))
v.check("26-02.4e0", reviews.p_found_mix(cl, 4))
v.check("26-02.4e", min(k for k in range(1, 50) if reviews.p_found_mix(cl, k) >= 0.75))
pind = reviews.p_found(reviews.p_found_mix(cl, 1), 3)
v.check("26-02.4e1", pind)
v.check("26-02.4e2", pind - p43)

# ---------------------------------------------------------------- Problems 5 and 6
v.check("26-02.5a", 15 / 22)
v.check("26-02.5a1", 15 / 30)
lp5 = reviews.lincoln_petersen(30, 22, 15)
v.assert_true("P5 hypergeometric MLE within 1 of Lincoln-Petersen (ties at integer values)", abs(hypergeom_mle(30, 22, 15) - lp5) <= 1)
v.check("26-02.5b", lp5)
v.check("26-02.5b1", reviews.chapman(30, 22, 15))
v.check("26-02.5c", 30 + 22 - 15)
v.check("26-02.5c1", lp5 - 37)
v.check("26-02.5c2", reviews.chapman(30, 22, 15) - 37)
en1 = 20 * 0.8 + 20 * 0.2
em = 20 * 0.8**2 + 20 * 0.2**2
v.check("26-02.6c", en1)
v.check("26-02.6c1", em)
v.check("26-02.6c2", en1 * en1 / em)
v.check("26-02.6c3", 100 * (1 - en1 * en1 / em / 40))
v.check("26-02.6d", 40 * 0.5**2)
v.assert_true("P6 Chapman finite at m = 0", math.isfinite(reviews.chapman(10, 8, 0)))

# ---------------------------------------------------------------- Problems 7 and 8
r7 = ballot(220, 105, 40, 15)
v.check("26-02.7a", 100 * r7[0])
v.check("26-02.7a1", 100 * r7[1])
v.check("26-02.7a2", 100 * r7[2])
r7b = ballot(220, 110, 40, 15)
v.check("26-02.7b", 100 * r7b[0])
v.check("26-02.7b1", 100 * r7b[1])
v.assert_true("P7b still fails", not reviews.ieee_ballot(220, 110, 40, 15)["passes"])
sw7 = min(s for s in range(0, 41) if reviews.ieee_ballot(220, 110 + s, 40 - s, 15)["passes"])
v.check("26-02.7c0", 0.75 * 150)
v.check("26-02.7c", 110 + sw7)
v.check("26-02.7c1", sw7)
r8 = ballot(200, 90, 25, 55)
v.check("26-02.8a", 100 * r8[0])
v.check("26-02.8a1", 100 * r8[1])
v.check("26-02.8a2", 100 * r8[2])
v.check("26-02.8b0", 0.30 * 170)
v.check("26-02.8b", max(x for x in range(0, 171) if x / 170 < 0.30))
v.assert_true("P8c passes at exactly 75%", reviews.ieee_ballot(200, 90, 30, 50)["passes"])
v.check("26-02.8c", 100 * 90 / 120)

# ---------------------------------------------------------------- Problems 9 to 11
v.check("26-02.9a", reviews.royalty_stack([0.0025] * 40, 1000))
v.check("26-02.9a1", 40 * 0.0025 * 1000 / 6)
v.check("26-02.9b", reviews.royalty_stack([0.0025] * 40, 6))
v.check("26-02.9c", reviews.top_down_share(0.03, 1000, 0.05))
v.check("26-02.9c1", 0.03 * 1000)
v.check("26-02.10b", 100 * optimize.brentq(lambda r: r * 500 - 20, 0, 1))
v.check("26-02.10b1", 100 * 0.01 * 500 / 20)
v.check("26-02.10c", 100 * (0.55 - 0.01 * 500 / 20))
v.check("26-02.11a", 4 * 3)
v.check("26-02.11a1", 0.3 * (2 + 1 * 3))
v.check("26-02.11a2", reviews.early_start_value(4, 3, 0.3, 2, 1))
v.check("26-02.11b", 0.3 * (20 + 5 * 3))
v.check("26-02.11b1", reviews.early_start_value(4, 3, 0.3, 20, 5))
v.check("26-02.11c", optimize.brentq(lambda p: reviews.early_start_value(4, 3, p, 20, 5), 0, 1))

# ---------------------------------------------------------------- Lab
h = 0.5
v.check("Lab 26-02.a1", 0.35 / (1 - h))
v.check("Lab 26-02.a", 100 * reviews.p_found_mix([(1 - h, 0.35 / (1 - h)), (h, 0.0)], 5))
e1 = 25 * 0.6 + 11 * 0.1
e2 = 25 * 0.75 + 11 * 0.1
emm = 25 * 0.6 * 0.75 + 11 * 0.1 * 0.1
v.check("Lab 26-02.b0", e1)
v.check("Lab 26-02.b1", e2)
v.check("Lab 26-02.b2", emm)
est = e1 * e2 / emm
v.check("Lab 26-02.b", est)
v.check("Lab 26-02.b3", 100 * (1 - est / 36))
sim = reviews.simulate_two_reviews(36, 0.6, 0.75, hard_fraction=11 / 36, hard_p=0.1)
v.assert_true("Lab Monte Carlo Chapman mean within 3% of the expected-count estimate", abs(sim.mean() / est - 1) < 0.03,
              f"{sim.mean():.2f}")
block = max(g for g in range(4, 200) if not reviews.ieee_ballot(g, g - 3, 3, 0)["passes"])
v.check("Lab 26-02.c", block)
v.check("Lab 26-02.c1", 100 * (block - 3) / block)
v.check("Lab 26-02.d", optimize.brentq(lambda p: reviews.early_start_value(6, 10, p, 25, 6), 0, 1))

sys.exit(v.finish())
