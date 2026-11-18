#!/usr/bin/env python3
"""Verify every number published in chapter 03-01, its solutions and its lab handout.

Values are recomputed independently: exact binomial sums, enumeration over small sample
spaces, root finding, and (where a formula is the subject) a brute-force check of the formula.
"""
from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C = HERE.parent
v = Verifier.from_files("03-01", C / "chapters" / "03-01-probability-in-ee-language.md",
                        C / "solutions" / "03-01-solutions.md", C / "labs" / "03-01-lab" / "README.md")


def p_any(n, p):
    """1 - (1 - p)^n without cancellation."""
    return -math.expm1(n * math.log1p(-p))


def binom_pmf(n, k, p):
    return comb(n, k) * p**k * (1 - p) ** (n - k)


def no_collision(k, N):
    out = 1.0
    for i in range(k):
        out *= 1 - i / N
    return out


# ---------------------------------------------------------------- theory section numbers
prior, sens, fa = 1e-3, 0.99, 0.01
v.check("T 03-01.a", prior * sens / (prior * sens + (1 - prior) * fa) * 100)
v.check("T 03-01.b", 1 - no_collision(10_000, 2**32))
v.check("T 03-01.c", 0.99**10)
v.check("T 03-01.d", 1 - 0.01**2)
# the union bound and inclusion-exclusion on a brute-force sample space (3 bits, p = 0.1)
p3 = 0.1
pats = list(itertools.product([0, 1], repeat=3))
prob = {s: math.prod(p3 if b else 1 - p3 for b in s) for s in pats}
any_err = sum(pr for s, pr in prob.items() if any(s))
v.assert_true("union bound holds on 3 bits", any_err <= 3 * p3)
v.assert_true("inclusion-exclusion for bits 1 and 2",
              abs(sum(pr for s, pr in prob.items() if s[0] or s[1]) - (2 * p3 - p3 * p3)) < 1e-15)
# TMR algebra: 3R^2 - 2R^3 - R = -R(2R - 1)(R - 1)
for R in (0.1, 0.3, 0.7, 0.95):
    v.assert_true(f"TMR factorization at R = {R}", abs(3 * R**2 - 2 * R**3 - R + R * (2 * R - 1) * (R - 1)) < 1e-15)
# Williams-Brown by brute force: N faults, each present w.p. pi; test covers TN of them
N_f, pi_f, T_f = 50, 0.004, 0.8
Y_f = (1 - pi_f) ** N_f
p_pass = (1 - pi_f) ** round(T_f * N_f)
v.assert_true("Williams-Brown P(good | pass) = Y^(1-T)", abs(Y_f / p_pass - Y_f ** (1 - T_f)) < 1e-12)

# ---------------------------------------------------------------- Example 1
n = 12_000
v.check("Ex 03-01.1a", p_any(n, 1e-12))
v.check("Ex 03-01.1b", p_any(n, 1e-6))
v.check("Ex 03-01.1c", p_any(n, 1e-4))
v.check("Ex 03-01.1d", n * 1e-4)
v.check("Ex 03-01.1e", binom_pmf(n, 1, 1e-4))
v.check("Ex 03-01.1f", 1 / (32e9 * 1e-12))
v.assert_true("binomial pmf sums to 1 (n = 12000, p = 1e-4)", abs(sum(binom_pmf(n, k, 1e-4) for k in range(60)) - 1) < 1e-12)

# ---------------------------------------------------------------- Example 2
v.check("Ex 03-01.2a", 0.05 + 0.04 - 0.01)
v.check("Ex 03-01.2b", 0.05 + 0.04 - 0.05 * 0.04)
v.check("Ex 03-01.2c", 0.01 / 0.05)

# ---------------------------------------------------------------- Example 3
YA, YB, sA, sB = 0.92, 0.85, 0.6, 0.4
Y3 = sA * YA + sB * YB
v.check("Ex 03-01.3a", Y3)
v.check("Ex 03-01.3b", sB * (1 - YB) / (1 - Y3))
v.check("Ex 03-01.3c", sB * YB / Y3)

# ---------------------------------------------------------------- Example 4 (exact fractions)
Y4, det, ok = Fraction(9, 10), Fraction(99, 100), Fraction(2, 100)
pp = Y4 * (1 - ok) + (1 - Y4) * (1 - det)
v.check("Ex 03-01.4a", float(pp))
v.check("Ex 03-01.4b", float((1 - Y4) * (1 - det) / pp) * 1e6)
v.check("Ex 03-01.4c", float(Y4 * ok / (1 - pp)))
e10 = brentq(lambda e: 0.1 * e / (0.882 + 0.1 * e) - 1e-5, 1e-9, 0.5, xtol=1e-16)
v.check("Ex 03-01.4d", e10)
v.check("Ex 03-01.4e", (1 - e10) * 100)
v.check("Ex 03-01.4f", 0.01 / e10)

# ---------------------------------------------------------------- Example 5
P1, flip = 0.05, 0.1
r1 = P1 * (1 - flip) + (1 - P1) * flip
r0 = 1 - r1
v.check("Ex 03-01.5a", P1 * (1 - flip) / r1)
v.check("Ex 03-01.5b", P1 * flip / r0)
v.check("Ex 03-01.5e", (1 - P1) * flip / r1)
v.check("Ex 03-01.5f", (1 - P1) * (1 - flip) / r0)
# MAP error: enumerate decision rules on {received 0, received 1}
rules = list(itertools.product([0, 1], repeat=2))
def p_err(rule):
    pe = 0.0
    for sent, ps in ((0, 1 - P1), (1, P1)):
        for rec in (0, 1):
            pr = (1 - flip) if rec == sent else flip
            pe += ps * pr * (rule[rec] != sent)
    return pe
best = min(rules, key=p_err)
v.assert_true("MAP rule is 'always decide 0'", best == (0, 0))
v.check("Ex 03-01.5c", p_err(best))
v.check("Ex 03-01.5d", p_err((0, 1)))

# ---------------------------------------------------------------- Example 6
def tmr(R):
    return sum(comb(3, k) * R**k * (1 - R) ** (3 - k) for k in (2, 3))
v.check("Ex 03-01.6a", tmr(0.99))
v.check("Ex 03-01.6b", tmr(0.9))
v.check("Ex 03-01.6c", tmr(0.4))
v.check("Ex 03-01.6h", (1 - 0.99) / (1 - tmr(0.99)))
q, beta = 0.01, 0.1
both_cm = beta * q + (1 - beta * q) * ((1 - beta) * q) ** 2
v.check("Ex 03-01.6d", q * q)
v.check("Ex 03-01.6e", both_cm)
v.check("Ex 03-01.6f", both_cm / q**2)
HOURS = 365.25 * 24
v.check("Ex 03-01.6g", (1 - 0.99999) * HOURS * 60)

# ---------------------------------------------------------------- Example 7
def dl(Y, T):
    return -math.expm1((1 - T) * math.log(Y))
v.check("Ex 03-01.7a", dl(0.8, 0.99) * 1e6)
T100 = brentq(lambda T: dl(0.8, T) - 1e-4, 0.9, 1 - 1e-9, xtol=1e-15)
T10 = brentq(lambda T: dl(0.8, T) - 1e-5, 0.9, 1 - 1e-12, xtol=1e-16)
v.check("Ex 03-01.7b", T100)
v.check("Ex 03-01.7c", T10)
v.check("Ex 03-01.7f", 1 - T100)
v.check("Ex 03-01.7d", dl(0.5, 0.999) * 1e6)
v.check("Ex 03-01.7e", 0.01 * math.log(1 / 0.8))

# ---------------------------------------------------------------- Numbers to know
v.check("N 03-01.a", (1 - 0.999) * HOURS)
v.check("N 03-01.b", (1 - 0.9999) * HOURS * 60)
v.check("N 03-01.c", (1 - 0.99999) * HOURS * 60)
v.check("N 03-01.d", -math.log(0.05))
v.check("N 03-01.e", 3 * 77)
v.check("N 03-01.f", -math.log(0.05) / 1e-12 / 32e9)
v.check("N 03-01.g", -math.log(0.05) / 1e-12 / 400e9)
v.check("N 03-01.h", -math.log(0.05) / 1e-15 / 400e9 / 3600)

# ---------------------------------------------------------------- Solutions
v.check("03-01.1a", 0.3 + 0.5 - 0.1); v.check("03-01.1b", 1 - 0.7)
v.check("03-01.1c", 0.3 - 0.1); v.check("03-01.1d", 0.2 + 0.4)
v.check("03-01.2a", 1e9 * 1e-12); v.check("03-01.2b", p_any(10**9, 1e-12))
v.check("03-01.3a", comb(8, 2)); v.check("03-01.3b", binom_pmf(8, 2, 0.01)); v.check("03-01.3c", binom_pmf(8, 0, 0.01))
f4 = 1 - sum(binom_pmf(255, k, 1e-3) for k in range(3))
v.check("03-01.4a", f4); v.check("03-01.4b", p_any(255, 1e-3)); v.check("03-01.4c", p_any(255, 1e-3) / f4)
N16 = 2**16
v.check("03-01.5a", 1 - no_collision(100, N16))
v.check("03-01.5b", math.sqrt(2 * N16 * math.log(2)))
v.check("03-01.5c", next(k for k in range(2, 5000) if 1 - no_collision(k, N16) >= 0.5))
v.check("03-01.6a", 0.6 * 0.25 + 0.4 * 0.5); v.check("03-01.6b", 0.15 / 0.35)
al = 1e-4 * 0.95 + (1 - 1e-4) * 0.002
v.check("03-01.7a", 1e-4 * 0.95 / al); v.check("03-01.7b", 1e5 * al); v.check("03-01.7c", 1e5 * 1e-4 * 0.95)
v.check("03-01.7d", brentq(lambda f: 1e-4 * 0.95 - (1 - 1e-4) * f, 0, 1))
rx1 = 0.5 * 0.99 + 0.5 * 0.001
v.check("03-01.8a", 0.5 * 0.99 / rx1); v.check("03-01.8b", 0.5 * 0.01 / (1 - rx1)); v.check("03-01.8c", 0.5 * 0.01 + 0.5 * 0.001)
v.check("03-01.9a", 0.2 * 0.3); v.check("03-01.9b", 0.1 / 0.3)
# parity bits by enumeration
outs = [(b1, b2, b1 ^ b2) for b1 in (0, 1) for b2 in (0, 1)]
v.check("03-01.10a", sum(0.25 for o in outs if o[0] == 1 and o[2] == 1))
v.check("03-01.10b", sum(0.25 for o in outs if o == (1, 1, 1)))
fan = sum(binom_pmf(4, k, 0.97) for k in (3, 4))
v.check("03-01.11a", fan); v.check("03-01.11b", (1 - 0.02**2) * 0.995 * fan)
v.check("03-01.11c", 0.5); v.check("03-01.11d", (1 - fan) * 100); v.check("03-01.11e", 0.02**2 * 100)
q12, b12 = 0.02, 0.05
f12 = b12 * q12 + (1 - b12 * q12) * ((1 - b12) * q12) ** 2
v.check("03-01.12a", q12**2); v.check("03-01.12b", f12); v.check("03-01.12c", f12 / q12**2)
v.check("03-01.13a", 0.999 * tmr(0.95))
g = lambda R: 0.999 * tmr(R) - R  # noqa: E731
v.check("03-01.13b", brentq(g, 0.3, 0.7, xtol=1e-14)); v.check("03-01.13c", brentq(g, 0.9, 0.99999, xtol=1e-14))
u14 = brentq(lambda u: -math.expm1(u * math.log(0.7)) - 5e-5, 1e-8, 1e-2, xtol=1e-18)
v.check("03-01.14a", u14); v.check("03-01.14b", 1 - u14); v.check("03-01.14c", dl(0.9, 1 - u14) * 1e6)
v.check("03-01.15a", -math.log(0.01) / 1e-12); v.check("03-01.15b", -math.log(0.01) / 1e-12 / 112e9)
v.check("03-01.15c", brentq(lambda m: 1 - math.exp(-m) * (1 + m) - 0.95, 1, 10))
v.check("03-01.15d", -math.log(0.05) / 1e12)
v.check("03-01.16a", 1 - 0.99**231)
v.check("03-01.16b", math.ceil(math.log(0.1) / math.log(0.999)))
v.check("03-01.16c", math.ceil(math.log(0.1) / math.log1p(-1e-5)))

# ---------------------------------------------------------------- Lab handout
v.check("Lab 03-01.a", p_any(12_000, 1e-5))
v.check("Lab 03-01.b", math.exp(-3.0))
v.check("Lab 03-01.c", next(k for k in range(2, 5000) if 1 - no_collision(k, N16) >= 0.5))
v.check("Lab 03-01.d", float((1 - Y4) * (1 - det) / pp) * 1e6)
nbad = 1e6 * 0.1 * 0.01
v.check("Lab 03-01.e", nbad)
sig_dppm = math.sqrt(nbad) / (1e6 * 0.883) * 1e6
v.check("Lab 03-01.f", sig_dppm)
v.check("Lab 03-01.g", (1173 - 1132.5) / sig_dppm)
v.check("Lab 03-01.h", 1e6 * (1 / 0.01**2) / nbad)          # 1/sqrt(N_bad) = 1% needs 10^4 bad dies
v.check("Lab 03-01.i", -math.log(0.05) / 1e-15 / 100e9 / 3600)

# ---------------------------------------------------------------- unkeyed numbers flagged by the course audit
v.check("Ex 03-01.5g", brentq(lambda p1: p1 * 0.9 - (1 - p1) * 0.1, 1e-6, 0.999))   # MAP follows a received 1
v.check("N 03-01.i", -math.log(0.05) / 1e-12)
v.check("C 03-01.a", p_any(1000, 1e-5))
v.check("C 03-01.b", 0.1 * 0.01 / (0.9 * 0.98 + 0.1 * 0.01) * 100)
v.check("C 03-01.c", 0.5 * 0.01 / (0.5 * 0.98 + 0.5 * 0.01) * 100)

# ---------------------------------------------------------------- Problems 03-01.17 to 03-01.20
# (a) three-event inclusion-exclusion and (b) complements, checked by brute force on a random finite space
import random
rnd = random.Random(2026)
pts = [rnd.random() for _ in range(40)]
w = [x / sum(pts) for x in pts]
P = lambda S: sum(w[i] for i in S)  # noqa: E731
Aev, Bev, Cev = {i for i in range(40) if i % 2}, {i for i in range(40) if i % 3 == 0}, {i for i in range(40) if i < 17}
lhs = P(Aev | Bev | Cev)
rhs = P(Aev) + P(Bev) + P(Cev) - P(Aev & Bev) - P(Aev & Cev) - P(Bev & Cev) + P(Aev & Bev & Cev)
v.assert_true("three-event inclusion-exclusion", abs(lhs - rhs) < 1e-14)
# independent product space: complements stay independent
pa, pb_ = 0.3, 0.6
v.assert_true("complements of independent events", abs((1 - pa) * pb_ - (pb_ - pa * pb_)) < 1e-15 and abs((1 - pa) * (1 - pb_) - (1 - pa - pb_ + pa * pb_)) < 1e-15)
v.check("03-01.17a", math.sqrt(2 * math.log(2)))
v.check("03-01.17b", math.sqrt(2 * 1e6 * math.log(2)))
v.check("03-01.17c", next(k for k in range(2, 5000) if 1 - no_collision(k, 10**6) >= 0.5))
pbad, sens, fal = 0.05, 0.9, 0.04
f1 = pbad * sens + (1 - pbad) * fal
f12 = pbad * sens**2 + (1 - pbad) * fal**2
v.check("03-01.18a", f1)
v.check("03-01.18b", f12)
v.check("03-01.18c", f12 / f1)
v.check("03-01.18d", pbad * sens / f1)
v.check("03-01.18e", pbad * sens**2 / f12)
MIN_PER_YEAR = 8766 * 60
u19 = 1 - 0.9995
a_s = (1 - u19) ** 2
v.check("03-01.19a", a_s)
v.check("03-01.19b", (1 - a_s) * MIN_PER_YEAR)
a_p = (1 - u19**2) ** 2
v.check("03-01.19c", a_p)
v.check("03-01.19d", (1 - a_p) * MIN_PER_YEAR * 60)
up = 0.1 * u19 + (1 - 0.1 * u19) * (0.9 * u19) ** 2
v.check("03-01.19e", (1 - (1 - up) ** 2) * MIN_PER_YEAR)
v.check("03-01.19f", up)
c0, Y20 = 0.02, 0.85
for L, keys in ((500, "abcde"), (5000, "fg h i")):
    cost = lambda u: c0 * math.log(1 / u) + L * u * math.log(1 / Y20)  # noqa: E731
    us = math.exp(brentq(lambda lu: -c0 + L * math.exp(lu) * math.log(1 / Y20), -30, 0))   # dC/du = 0, solved in log u
    v.assert_true(f"optimum is a minimum (L = {L})", cost(us) < min(cost(us * 1.01), cost(us / 1.01)))
    if L == 500:
        v.check("03-01.20a", us); v.check("03-01.20b", 1 - us); v.check("03-01.20c", us * math.log(1 / Y20) * 1e6)
        v.check("03-01.20d", c0 * math.log(1 / us)); v.check("03-01.20e", cost(us))
    else:
        v.check("03-01.20f", us); v.check("03-01.20g", 1 - us); v.check("03-01.20h", us * math.log(1 / Y20) * 1e6)
        v.check("03-01.20i", cost(us))
    v.assert_true("optimal DL equals c0/L", abs(us * math.log(1 / Y20) - c0 / L) < 1e-15)
v.check("03-01.20j", math.log(1 / Y20))

sys.exit(v.finish())
