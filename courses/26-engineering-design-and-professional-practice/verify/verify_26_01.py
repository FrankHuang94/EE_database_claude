#!/usr/bin/env python3
"""Verify every number in chapter 26-01 (requirements, specifications and the design process), its problems
and its lab.

Independent routes:
- battery life by integrating charge over an explicit one-week timeline of mode intervals, and duty limits
  by root-finding on that integral;
- error budgets by Monte Carlo (Gaussian and uniform) and by numerical convolution of the uniform densities;
- the escalation model as an absorbing Markov chain solved with the fundamental matrix, and by the backward
  recursion of Problem 26-01.10, against the closed form of 26-01 section 3.6;
- decision-matrix tie weights by root-finding on the swept scores, against the closed form;
- lognormal battery life by Monte Carlo.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize
from scipy.signal import fftconvolve
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "26-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import reqs  # noqa: E402

v = Verifier.from_files("26-01", ROOT / "chapters" / "26-01-requirements-and-specifications.md",
                        ROOT / "solutions" / "26-01-solutions.md", LAB / "README.md")
RNG = np.random.default_rng(2601)


# ---------------------------------------------------------------- helpers
def timeline_charge(profile, hours=168.0, slot=0.25):
    """Charge drawn (mAh) over `hours`, building an explicit schedule of 15-minute slots.

    Each slot is split into the modes in proportion to their duty, in a fixed order, so the integral is a
    sum over intervals rather than the duty-weighted average itself.
    """
    n = int(round(hours / slot))
    q = 0.0
    for _ in range(n):
        t0 = 0.0
        for duty, current in profile:
            dt = duty * slot
            q += current * dt
            t0 += dt
        assert abs(t0 - slot) < 1e-12
    return q


def markov_cost(p_detect, factors):
    """Expected relative cost per error from an absorbing Markov chain (transient states = phases)."""
    k = len(p_detect)
    q = np.zeros((k, k))
    r = np.zeros(k)
    for i, p in enumerate(p_detect):
        if i + 1 < k:
            q[i, i + 1] = 1 - p
        r[i] = p * factors[i]
    # cost of escaping past the last listed phase goes to the field
    r[k - 1] += (1 - p_detect[-1]) * factors[k]
    nmat = np.linalg.inv(np.eye(k) - q)
    return float(nmat[0] @ r)


def backward(p_detect, factors):
    """Backward recursion c_k = p_k c_k + (1 - p_k) c_{k+1}, returning the list of averages per phase."""
    cbar = [float(factors[-1])]
    for p, c in zip(reversed(p_detect), reversed(factors[:-1])):
        cbar.insert(0, p * c + (1 - p) * cbar[0])
    return cbar


# ---------------------------------------------------------------- Example 26-01.1, 26-01.2
v.check("Ex 26-01.1a", 7 * 24)
prof = [(0.78, 0.050), (0.15, 2.0), (0.03, 10.0), (0.04, 25.0)]
usable = 300 * 0.85
v.check("Ex 26-01.2a0", usable)
imax = usable / 168
v.check("Ex 26-01.2a", imax)
v.check("Ex 26-01.2a1", imax)
q_week = timeline_charge(prof)
ibar = q_week / 168
v.assert_true("timeline integral equals duty average", abs(ibar - reqs.duty_average(prof)) < 1e-12)
for key, (d, i) in zip(("Ex 26-01.2b3", "Ex 26-01.2b4", "Ex 26-01.2b5", "Ex 26-01.2b6"), prof):
    v.check(key, d * i)
v.check("Ex 26-01.2b", ibar)
life = usable / ibar
v.check("Ex 26-01.2b1", life)
v.check("Ex 26-01.2b2", life / 24)
v.check("Ex 26-01.2c", 100 * 0.04 * 25 / ibar)
budget = imax / 1.10
v.check("Ex 26-01.2d", budget)


def prof_d(d):
    return [(0.82 - d, 0.050), (0.15, 2.0), (0.03, 10.0), (d, 25.0)]


d_ok = optimize.brentq(lambda d: timeline_charge(prof_d(d)) / 168 - budget, 0.0, 0.08)
v.check("Ex 26-01.2d1", 100 * d_ok)
v.check("Ex 26-01.2d2", d_ok * 1440)
v.check("Ex 26-01.2d3", 0.04 * 1440)
v.check("Ex 26-01.2d4", 0.050 * 0.82 + 0.30 + 0.30)
v.check("Ex 26-01.2d5", 25 - 0.050)
v.check("Ex 26-01.2d6", 100 * (1 - d_ok / 0.04))
v.check("Ex 26-01.2e", 0.78 * 0.050 / 2)
v.check("Ex 26-01.2e1", 100 * 0.78 * 0.050 / 2 / ibar)

# ---------------------------------------------------------------- Example 26-01.3
b = [0.40, 0.35, 0.30, 0.25, 0.20, 0.30]
v.check("Ex 26-01.3a", sum(b))
v.check("Ex 26-01.3b0", sum(x * x for x in b))
rss = math.sqrt(sum(x * x for x in b))
v.check("Ex 26-01.3b", rss)
sig = rss / 3
v.check("Ex 26-01.3b1", sig)
v.check("Ex 26-01.3b2", 1.0 / sig)
p_ind = 2 * norm.sf(1.0 / sig)
v.check("Ex 26-01.3b3", 1e6 * p_ind)
rho = np.eye(6)
rho[0, 5] = rho[5, 0] = 1.0
sig_c = reqs.stack_corr(np.array(b) / 3, rho)
v.check("Ex 26-01.3c4", b[0] + b[5])
v.check("Ex 26-01.3c0", (b[0] + b[5]) ** 2 + sum(x * x for x in b[1:5]))
v.check("Ex 26-01.3c", 3 * sig_c)
v.check("Ex 26-01.3c1", 1.0 / sig_c)
p_cor = 2 * norm.sf(1.0 / sig_c)
v.check("Ex 26-01.3c2", 1e6 * p_cor)
v.check("Ex 26-01.3c3", p_cor / p_ind)
# Monte Carlo cross-checks
n_mc = 4_000_000
z = RNG.standard_normal((n_mc, 6))
e_ind = (z * (np.array(b) / 3)).sum(axis=1)
z[:, 5] = z[:, 0]
e_cor = (z * (np.array(b) / 3)).sum(axis=1)
pm_i, pm_c = (np.abs(e_ind) > 1).mean(), (np.abs(e_cor) > 1).mean()
v.assert_true("Ex 3 Monte Carlo (independent) within 20% of closed form", abs(pm_i / p_ind - 1) < 0.2, f"{pm_i:.2e}")
v.assert_true("Ex 3 Monte Carlo (correlated) within 8% of closed form", abs(pm_c / p_cor - 1) < 0.08, f"{pm_c:.2e}")
others = sum(x * x for x in b[1:5])
v.check("Ex 26-01.3d0", others)
left = rss**2 - others
v.check("Ex 26-01.3d1", left)
pair = math.sqrt(left)
v.check("Ex 26-01.3d2", pair)
ref_new = pair - b[5]
v.check("Ex 26-01.3d", ref_new)
v.assert_true("Ex 3d restores the independent RSS total",
              abs(3 * reqs.stack_corr(np.array([ref_new] + b[1:]) / 3, rho) - rss) < 1e-12)

# ---------------------------------------------------------------- Example 26-01.4
v.check("Ex 26-01.4a", 100 * 108 / 120)
esc = 3 * 0.30 + 9 * 0.05
v.check("Ex 26-01.4b0", esc)
v.check("Ex 26-01.4b", reqs.escape_cost([(3, 0.30), (9, 0.05)], 2.0))
v.check("Ex 26-01.4b1", 3 * 0.30)
v.check("Ex 26-01.4b2", 100 * 0.9 / esc)
v.check("Ex 26-01.4c", 12 * 0.020)
v.check("Ex 26-01.4c1", esc * 2.0 / (12 * 0.020))

# ---------------------------------------------------------------- Example 26-01.5
f5 = [1, 5, 10, 50, 100]
down = [0.4, 0.3, 0.6]
cd = markov_cost(down, f5[1:])
v.assert_true("Ex 5 Markov chain equals backward recursion", abs(cd - backward(down, f5[1:])[0]) < 1e-12)
v.check("Ex 26-01.5a", cd)
for key, val in zip(("Ex 26-01.5a1", "Ex 26-01.5a2", "Ex 26-01.5a3", "Ex 26-01.5a4"),
                    (0.4 * 5, 0.6 * 0.3 * 10, 0.6 * 0.7 * 0.6 * 50, 0.6 * 0.7 * 0.4 * 100)):
    v.check(key, val)
found_l, cost_l = reqs.defect_flow(100, [0.2] + down, f5)
found_f, cost_f = reqs.defect_flow(100, [0.6] + down, f5)
for i, x in enumerate(found_l, 1):
    v.check(f"Ex 26-01.5g{i}", x)
for i, x in enumerate(found_f, 1):
    v.check(f"Ex 26-01.5h{i}", x)
v.assert_true("Ex 5 closed form N[p c1 + (1-p) cdown]", abs(cost_l - 100 * (0.2 + 0.8 * cd)) < 1e-9
              and abs(cost_f - 100 * (0.6 + 0.4 * cd)) < 1e-9)
v.check("Ex 26-01.5b", cost_l)
v.check("Ex 26-01.5c", cost_f)
v.check("Ex 26-01.5d", cost_l - cost_f)
v.check("Ex 26-01.5d1", (cost_l - cost_f) * 1e4 / 1e6)
slope = 100 * (cd - 1)
v.check("Ex 26-01.5e0", slope)
v.check("Ex 26-01.5e", slope / 100)
v.check("Ex 26-01.5e1", slope / 100 * 1e4)
v.check("Ex 26-01.5f", found_l[3] * 50 + found_l[4] * 100)

# ---------------------------------------------------------------- Example 26-01.6
S6 = np.array([[5, 2, 5, 5], [4, 4, 3, 3], [3, 5, 2, 2]], dtype=float)
w6 = [0.40, 0.25, 0.20, 0.15]
sc = reqs.weighted_scores(w6, S6)
for key, x in zip(("Ex 26-01.6a", "Ex 26-01.6a1", "Ex 26-01.6a2"), sc):
    v.check(key, x)
v.check("Ex 26-01.6b3", 0.40 + 0.20 + 0.15)
rest = [0, 2, 3]
R = S6[:, rest] @ (np.array(w6)[rest] / 0.75)
for key, x in zip(("Ex 26-01.6b", "Ex 26-01.6b1", "Ex 26-01.6b2"), R):
    v.check(key, x)


def tie(scores, weights, j, a, bb):
    return optimize.brentq(lambda w: np.diff(reqs.scores_vs_weight(weights, scores, j, np.array([w]))[0][[bb, a]])[0],
                           0.0, 1.0)


for key, (a, bb) in zip(("Ex 26-01.6c", "Ex 26-01.6c1", "Ex 26-01.6c2"), ((0, 1), (0, 2), (1, 2))):
    w_root = tie(S6, w6, 1, a, bb)
    v.assert_true(f"{key} root equals closed form", abs(w_root - reqs.flip_weight(w6, S6, 1, a, bb)) < 1e-9)
    v.check(key, w_root)
v.check("Ex 26-01.6c3", 100 * (tie(S6, w6, 1, 0, 1) / 0.25 - 1))

# ---------------------------------------------------------------- section 3.3 / numbers to know
v.check("Txt 26-01.a", 100 * 2 * norm.sf(3))
v.check("Txt 26-01.a1", 1e6 * 2 * norm.sf(3))
v.check("Txt 26-01.b", 1e6 * 2 * norm.sf(4))
v.check("Txt 26-01.c", 1e6 * 2 * norm.sf(5))

# ---------------------------------------------------------------- Problem 3
p3 = [(0.90, 0.010), (0.085, 0.40), (0.015, 3.0)]
use3 = 0.80 * 22
v.check("26-01.3a0", use3)
im3 = use3 / 120
v.check("26-01.3a", im3)
v.check("26-01.3a1", im3)
for key, (d, i) in zip(("26-01.3b0", "26-01.3b1", "26-01.3b2"), p3):
    v.check(key, d * i)
i3 = timeline_charge(p3, hours=120) / 120
v.check("26-01.3b", i3)
v.check("26-01.3b3", use3 / i3)
v.check("26-01.3b4", use3 / i3 / 24)


def prof3(d):
    return [(0.915 - d, 0.010), (0.085, 0.40), (d, 3.0)]


v.check("26-01.3c0", 0.010 * 0.915 + 0.034)
v.check("26-01.3c1", 1 - 0.085)
v.check("26-01.3c2", 3.0 - 0.010)
v.check("26-01.3c", 100 * optimize.brentq(lambda d: timeline_charge(prof3(d), 120) / 120 - im3, 0, 0.2))
im3b = 0.70 * 22 / 120
v.check("26-01.3d0", im3b)
v.check("26-01.3d", 100 * optimize.brentq(lambda d: timeline_charge(prof3(d), 120) / 120 - im3b, 0, 0.2))

# ---------------------------------------------------------------- Problem 4
ui = 1e12 / 32e9
dj = [4.0, 3.0, 2.0]
rj = [0.30, 0.25, 0.22]
v.check("26-01.4a", ui)
v.check("26-01.4a7", 0.50 * ui)
v.check("26-01.4a1", sum(dj))
srj = reqs.stack_rss(rj)
v.check("26-01.4a0", srj**2)
v.check("26-01.4a2", srj)
v.check("26-01.4a3", 2 * 7.03 * srj)
tj = sum(dj) + 2 * 7.03 * srj
v.check("26-01.4a4", tj)
v.check("26-01.4a5", tj / ui)
v.check("26-01.4a6", 0.5 * ui - tj)
dj_rss = reqs.stack_rss(dj)
v.check("26-01.4b", dj_rss)
v.check("26-01.4b1", dj_rss + 2 * 7.03 * srj)
v.check("26-01.4b2", 0.5 * ui - (dj_rss + 2 * 7.03 * srj))
v.check("26-01.4c0", 2 * 7.03 * sum(rj))
v.check("26-01.4c", sum(dj) + 2 * 7.03 * sum(rj))
v.check("26-01.4c1", sum(dj) + 2 * 7.03 * sum(rj) - 0.5 * ui)

# ---------------------------------------------------------------- Problem 5
s5, m5 = 0.90, 0.50
v.check("26-01.5a", (3 - m5) / s5)
v.check("26-01.5a0", (3 + m5) / s5)
up, lo = norm.sf((3 - m5) / s5), norm.cdf((-3 - m5) / s5)
v.check("26-01.5a1", up)
v.check("26-01.5a2", lo)
v.check("26-01.5a3", reqs.p_outside(s5, 3.0, m5))
v.assert_true("P5 tails sum to the total", abs(up + lo - reqs.p_outside(s5, 3.0, m5)) < 1e-15)
p0 = reqs.p_outside(s5, 3.0)
v.check("26-01.5b", p0)
v.check("26-01.5b1", (up + lo) / p0)

# ---------------------------------------------------------------- Problem 6
n6, r6 = 6, 0.2
rho6 = np.full((n6, n6), r6)
np.fill_diagonal(rho6, 1.0)
s_cor = reqs.stack_corr(np.ones(n6), rho6)
v.assert_true("P6 closed form sqrt(n + n(n-1)rho)", abs(s_cor - math.sqrt(n6 + n6 * (n6 - 1) * r6)) < 1e-12)
v.check("26-01.6d", s_cor)
v.check("26-01.6d1", math.sqrt(n6))
v.check("26-01.6d2", 100 * (s_cor - math.sqrt(n6)) / (n6 - math.sqrt(n6)))
v.assert_true("P6 all-ones correlation gives the worst case",
              abs(reqs.stack_corr([0.4, 0.3, 0.2], np.ones((3, 3))) - 0.9) < 1e-12)

# ---------------------------------------------------------------- Problem 7
for key_w, key_r, n in (("26-01.7a", "26-01.7a2", 4), ("26-01.7a1", "26-01.7a3", 9)):
    v.check(key_w, optimize.brentq(lambda x: n * x - 1.0, 0, 1))
    v.check(key_r, optimize.brentq(lambda x: math.sqrt(n) * x - 1.0, 0, 1))
v.check("26-01.7b", math.sqrt(4))
v.check("26-01.7b1", math.sqrt(9))
v.check("26-01.7c", math.sqrt((1.0 - 0.5**2) / 3))
v.check("26-01.7c1", (1.0 - 0.5) / 3)

# ---------------------------------------------------------------- Problem 8
v.check("26-01.8a", 100 * 231 / 250)
e8 = 4 * 0.25 + 15 * 0.04
v.check("26-01.8b", e8)
v.check("26-01.8b1", reqs.escape_cost([(4, 0.25), (15, 0.04)], 1.5))
v.check("26-01.8c", 19 * 0.015)
v.check("26-01.8c1", e8 * 1.5 / (19 * 0.015))
v.check("26-01.8d0", 4 * 0.25)
v.check("26-01.8d", reqs.escape_cost([(13, 0.04)], 1.5))

# ---------------------------------------------------------------- Problems 9 and 10
f9 = [1, 4, 12, 40, 200]
d9 = [0.5, 0.2, 0.7]
cd9 = markov_cost(d9, f9[1:])
v.check("26-01.9a", cd9)
for key, val in zip(("26-01.9a1", "26-01.9a2", "26-01.9a3", "26-01.9a4"),
                    (0.5 * 4, 0.5 * 0.2 * 12, 0.5 * 0.8 * 0.7 * 40, 0.5 * 0.8 * 0.3 * 200)):
    v.check(key, val)
fa, ca = reqs.defect_flow(60, [0.3] + d9, f9)
fb, cb = reqs.defect_flow(60, [0.5] + d9, f9)
for i, x in enumerate(fa, 1):
    v.check(f"26-01.9b{i}", x)
for i, x in enumerate(fb, 1):
    v.check(f"26-01.9c{i}", x)
v.check("26-01.9b", ca)
v.check("26-01.9c", cb)
v.check("26-01.9d", ca - cb)
v.check("26-01.9d1", (ca - cb) * 8000 / 1e6)
bw = backward(d9, f9[1:])
v.check("26-01.10a", bw[2])
v.check("26-01.10a1", bw[1])
v.assert_true("P10 recursion reproduces P9(a)", abs(bw[0] - cd9) < 1e-12)
v.check("26-01.10b0", cd9 - 1)
v.check("26-01.10b", -60 * (cd9 - 1))
v.check("26-01.10b2", 60 * (cd9 - 1) / 100)
v.check("26-01.10b1", 60 * (cd9 - 1) / 100 * 8000)
dp = optimize.brentq(lambda d: 60 * d * (cd9 - 1) * 8000 - 250000, 0, 1)
v.check("26-01.10c0", dp)
v.check("26-01.10c", 100 * dp)

# ---------------------------------------------------------------- Problems 11 and 12
S11 = np.array([[5, 4, 2, 2], [2, 3, 5, 5]], dtype=float)
w11 = [0.35, 0.30, 0.20, 0.15]
s11 = reqs.weighted_scores(w11, S11)
v.check("26-01.11a", s11[0])
v.check("26-01.11a1", s11[1])
v.check("26-01.11b0", 0.35 + 0.30 + 0.15)
r11 = S11[:, [0, 1, 3]] @ (np.array(w11)[[0, 1, 3]] / 0.80)
v.check("26-01.11b1", r11[0])
v.check("26-01.11b2", r11[1])
w11t = tie(S11, w11, 2, 0, 1)
v.check("26-01.11b", w11t)
v.check("26-01.11c", 100 * (w11t / 0.20 - 1))
v.check("26-01.11c1", 100 * (tie(S6, w6, 1, 0, 1) / 0.25 - 1))
S12 = S11.copy()
S12[:, 2] = [4, 10]
s12 = S12 @ np.array(w11)
v.check("26-01.12b", s12[0])
v.check("26-01.12b1", s12[1])
v.check("26-01.12c0", 2 * 0.20)
v.check("26-01.12c1", 1 + 0.20)
w_eff = 0.40 / 1.20
v.check("26-01.12c", w_eff)
w_norm = np.array([0.35, 0.30, 0.40, 0.15]) / 1.20
v.assert_true("P12 doubled scale equals renormalized doubled weight (same ranking)",
              np.argmax(S11 @ w_norm) == np.argmax(s12))

# ---------------------------------------------------------------- Problem 14
v.check("26-01.14a", 40 * 2.5)
v.check("26-01.14a1", 40 * 2.5 * 5000 / 1e6)
v.check("26-01.14b", 40 * 0.15 * 1.0)
v.check("26-01.14b1", 40 * 0.15 * 1.0 * 2.0)
v.check("26-01.14c", (40 * 0.15 * 2.0e6) / (40 * 2.5 * 5000))

# ---------------------------------------------------------------- Problem 15
sl = math.sqrt(0.03**2 + 0.05**2)
v.check("26-01.15a", sl)
z15 = math.log(168 / 175) / sl
v.check("26-01.15b", z15)
v.check("26-01.15b1", 100 * norm.cdf(z15))
v.check("26-01.15c", 168 * math.exp(norm.ppf(0.99) * sl))
cap = np.exp(RNG.normal(0, 0.03, 2_000_000))
cur = np.exp(RNG.normal(0, 0.05, 2_000_000))
life15 = 175 * cap / cur
v.assert_true("P15 Monte Carlo fraction short within 1 point", abs(100 * (life15 < 168).mean() - 100 * norm.cdf(z15)) < 1.0)

# ---------------------------------------------------------------- Lab
dx = 1e-5
x = np.arange(-2.0, 2.0 + dx / 2, dx)
pdf = None
for bi in b:
    u = (np.abs(x) <= bi).astype(float)
    u /= u.sum() * dx
    pdf = u if pdf is None else fftconvolve(pdf, u, mode="same") * dx
pdf /= pdf.sum() * dx
p_uni = pdf[np.abs(x) > 1.0].sum() * dx
mc_uni = (np.abs(reqs.mc_budget(b, dist="uniform", n=2_000_000)) > 1.0).mean()
v.assert_true("Lab uniform Monte Carlo within 3% of convolution", abs(mc_uni / p_uni - 1) < 0.03, f"{mc_uni:.4f}")
v.check("Lab 26-01.a", 100 * p_uni)
sig_u = math.sqrt(sum(bi**2 / 3 for bi in b))
v.check("Lab 26-01.a1", sig_u)
v.check("Lab 26-01.a2", 100 * 2 * norm.sf(1.0 / sig_u))
v.check("Lab 26-01.a3", 1 / math.sqrt(3))
d_nm = optimize.brentq(lambda d: timeline_charge(prof_d(d)) / 168 - imax, 0, 0.08)
v.check("Lab 26-01.b", 100 * d_nm)
v.check("Lab 26-01.b1", d_nm * 1440)
v.check("Lab 26-01.b2", d_nm * 1440 - d_ok * 1440)
lo_f, hi_f = [1, 3, 7, 21, 29], [1, 8, 16, 78, 1500]
savings = []
for key, f in (("Lab 26-01.c", lo_f), ("Lab 26-01.c1", hi_f)):
    sv = reqs.defect_flow(100, [0.2] + down, f)[1] - reqs.defect_flow(100, [0.6] + down, f)[1]
    v.assert_true(f"{key} saving equals 40 N-points x (cdown - c1)",
                  abs(sv - 0.4 * 100 * (markov_cost(down, f[1:]) - 1)) < 1e-9)
    v.check(key, sv)
    savings.append(sv)
v.check("Lab 26-01.c3", savings[1])
v.check("Lab 26-01.c2", savings[1] / savings[0])

sys.exit(v.finish())
