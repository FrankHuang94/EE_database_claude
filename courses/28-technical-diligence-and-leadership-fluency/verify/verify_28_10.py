#!/usr/bin/env python3
"""Verify every number in chapter 28-10 (conversation scenarios), its problems and its lab.

Independent routes: each live check is recomputed from first principles here (not from the
lab module), with Monte Carlo or exact enumeration where a probability is involved, and the
lab module is cross-checked against those values.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import convo as cv  # noqa: E402

v = Verifier.from_files("28-10", ROOT / "chapters" / "28-10-conversation-scenarios.md",
                        ROOT / "solutions" / "28-10-solutions.md", LAB / "README.md")
RNG = np.random.default_rng(2810)
H = 8766.0


def odds_post(prior, ratios):
    o = prior / (1 - prior) * math.prod(ratios)
    return o, o / (1 + o)


def dpw(a, d=300.0):
    return math.pi * d * d / (4 * a) - math.pi * d / math.sqrt(2 * a)


def area_budget(die_budget, wafer=18500, d0=0.001):
    return optimize.brentq(lambda a: wafer / (dpw(a) * math.exp(-a * d0)) - die_budget, 5, 400)


# --- Examples 1-5 ---------------------------------------------------------------------------
v.check("Ex 28-10.1a", 2e15 / 4e12)
v.check("Ex 28-10.1b", 2 * 8 / 1)
v.check("Ex 28-10.1c", 16 * 4e12 / 1e12)
v.check("Ex 28-10.1d", 100 * 16 * 4e12 / 2e15)
v.check("Ex 28-10.1e", (2e15 / 4e12) / 2)
v.assert_true("Ex 1: lab roofline agrees", abs(cv.roofline(2e15, 4e12, 8)[3] - 0.032) < 1e-12)
f2 = 1.2 / 1.1
v.check("Ex 28-10.2a", f2)
v.check("Ex 28-10.2b", f2 ** 3)
v.check("Ex 28-10.2c", 100 * (1 - 1 / f2 ** 3))
s3 = 2048 * 10e9 / 8
v.check("Ex 28-10.3a", s3 / 1e9)
v.check("Ex 28-10.3b", 8 * s3 / 1e12)
v.check("Ex 28-10.3c", s3 * 8 * 6e-12)
v.check("Ex 28-10.4a", 51.2e12 * 4e-12)
v.check("Ex 28-10.4b", 51.2e12 * 2.5e-12)
v.check("Ex 28-10.4c", 100 * (4 - 2.5) / 4)
v.check("Ex 28-10.4d", 100 * (4 / 2.5 - 1))
lam = optimize.brentq(lambda x: math.exp(-x * 1e6) - 0.05, 1e-9, 1e-4)  # P(0 events) = 5%
v.check("Ex 28-10.5a", lam * 1e6)
v.check("Ex 28-10.5b", 1e4 * 24 * lam)
v.assert_true("Ex 5: lab bound agrees", abs(cv.zero_failure_bound(1e6) - lam) < 1e-15)

# --- Examples 6-10 --------------------------------------------------------------------------
v.check("Ex 28-10.6a", 62 + 10 * math.log10(2.5e8 / 0.05))
v.check("Ex 28-10.6b", (62 - 1.76) / 6.02)
a7 = 10 ** (-7 / 20)
th = np.linspace(-math.pi / 2, math.pi / 2, 200001)
dc = np.trapezoid(np.cos(th), th) / (2 * math.pi)       # half-sine of unit peak: mean over a period
f1 = np.trapezoid(np.cos(th) ** 2, th) / math.pi         # fundamental amplitude
v.check("Ex 28-10.7a", 100 * 0.5 * a7 * f1 / dc)         # class B at relative swing a7
v.check("Ex 28-10.7b", 100 * 2 * 0.5 * a7 * f1 / dc)     # Doherty carrier: twice class B below half amplitude
l96, l975 = 5000 / 0.96 - 5000, 5000 / 0.975 - 5000
v.check("Ex 28-10.8a", l96)
v.check("Ex 28-10.8b", l975)
v.check("Ex 28-10.8c", l96 - l975)
v.check("Ex 28-10.8d", 100 * (l96 - l975) / l96)
v.check("Ex 28-10.9", 100 * 0.992 * np.prod([0.996] * 6) * 0.985)
i10 = 1.2 + 3000 * 0.004 / 2 + 6000 * 0.002 / 30
yrs10 = 230 / (i10 / 1000) / H
v.check("Ex 28-10.10a", i10)
v.check("Ex 28-10.10b", yrs10)
v.check("Ex 28-10.10c", 100 * (yrs10 - 3) / yrs10)

# --- Examples 11-15 -------------------------------------------------------------------------
v.check("Ex 28-10.11a", 100 * (1.4 + 3) / (10 + 4))
v.check("Ex 28-10.11b", 4 / 14)
v.assert_true("Ex 11: lab Beta mean agrees", abs(cv.beta_mean(3, 4) - 4.4 / 14) < 1e-12)
g12 = math.exp((math.log(1.2) + math.log(1.35)) / 2)
v.check("Ex 28-10.12a", g12)
v.check("Ex 28-10.12b", 15 * g12)
sim = (RNG.random((400_000, 8)) < 0.10).any(axis=1).mean()
v.check("Ex 28-10.13", 100 * (1 - 0.9 ** 8))
v.assert_true("Ex 13: simulation within 0.3 points", abs(sim - (1 - 0.9 ** 8)) < 0.003)
h14 = 0.6 ** 2 + 0.25 ** 2 + 0.15 ** 2
v.check("Ex 28-10.14a", h14)
v.check("Ex 28-10.14b", 1 / h14)
fac = np.mean([1.12 ** -k for k in (2, 3, 4)])
v.check("Ex 28-10.15a", fac)
v.check("Ex 28-10.15b", 30 * 0.4 * 4 * fac)
v.check("Ex 28-10.15c", 120 / (30 * 0.4 * 4 * fac))

# --- Examples 16-21 -------------------------------------------------------------------------
v.check("Ex 28-10.16a", 80 * 3 / 12)
v.check("Ex 28-10.16b", 15 * 4 * 0.03)
v.check("Ex 28-10.17", 20e6 * 15 * 0.025 / 1e6)
v.check("Ex 28-10.18a", 2 * (800 / 2) * 8)
v.check("Ex 28-10.18b", 2 * (800 / 2) * 8 / 700)
v.check("Ex 28-10.19a", 40 * 0.45)
v.check("Ex 28-10.19b", 40 * 0.45 - 5)
v.check("Ex 28-10.19c", area_budget(13))
e750, e600 = 0.75 * 1.25 * 5 * H * 0.10, 0.60 * 1.25 * 5 * H * 0.10
v.check("Ex 28-10.20a", e750)
v.check("Ex 28-10.20b", e600)
v.check("Ex 28-10.20c", e750 - e600)
v.check("Ex 28-10.20d", 100 * (0.75 / 0.6 - 1))
v.check("Ex 28-10.21", 10e-9 * 2e6 * 400)

# --- Examples 22-26 -------------------------------------------------------------------------
def tail(n, p, k):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


t3, h3 = tail(20, 0.35, 3), tail(20, 0.05, 3)
v.check("Ex 28-10.22a", 100 * t3)
v.check("Ex 28-10.22b", 100 * h3)
v.check("Ex 28-10.22c", t3 / h3)
v.assert_true("Ex 22: scipy binomial agrees", abs(stats.binom.sf(2, 20, 0.35) - t3) < 1e-12)
p23 = 0.80 * 0.85 * 0.95
v.check("Ex 28-10.23a", p23)
v.check("Ex 28-10.23b", p23 / 1.15 ** (11 / 12))
e10 = float(np.mean(np.sort(RNG.standard_normal((200_000, 10)), axis=1)[:, -1]))
v.check("Ex 28-10.24", math.exp(0.2 * 1.54))
v.assert_true("Ex 24: simulated expected max of ten normals is 1.54", abs(e10 - 1.54) < 0.01)
v.check("Ex 28-10.25a", 1e6 / (3000 * 0.85))
v.check("Ex 28-10.25b", 1e6 / (3000 * 0.85) / 24)
o26, p26 = odds_post(0.4, [3, 2, 0.5, 1, 3])
v.check("Ex 28-10.26a", o26)
v.check("Ex 28-10.26b", 100 * p26)

# --- Problems -------------------------------------------------------------------------------
v.check("28-10.2a", 3e15 / 6e12)
v.check("28-10.2b", 2 * 32)
v.check("28-10.2c", 64 * 6e12 / 1e12)
v.check("28-10.2d", 100 * 64 * 6e12 / 3e15)
v.check("28-10.2e", (3e15 / 6e12) / 2)
f3 = 1.15 / 1.05
v.check("28-10.3a", f3)
v.check("28-10.3b", 1.05 * f3 ** 3)
v.check("28-10.3c", 100 * (1 - 1 / (1.05 * f3 ** 3)))
v.check("28-10.4", 25.6e12 * 3.5e-12)
lam5 = optimize.brentq(lambda x: math.exp(-x * 5e5) - 0.05, 1e-9, 1e-3)
v.check("28-10.5a", lam5 * 1e6)
v.check("28-10.5b", 4000 * 24 * lam5)
i6 = 2 + 5000 * 0.010 / 5 + 8000 * 0.003 / 60
v.check("28-10.6a", i6)
v.check("28-10.6b", 1000 / (i6 / 1000) / H)
v.check("28-10.7a", 100 * (1.4 + 5) / 16)
v.check("28-10.7b", 6 / 16)
o8, p8 = odds_post(0.3, [3, 0.4, 2, 1, 0.5])
v.check("28-10.8a", o8)
v.check("28-10.8b", 100 * p8)
o8b, p8b = odds_post(0.3, [3, 0.4, 2, 1])
v.check("28-10.8c", o8b)
v.check("28-10.8d", 100 * p8b)
v.assert_true("P8: lab debrief groups the shared cause",
              abs(cv.debrief(0.3, [(3, 'a'), (0.4, 'w'), (2, 'b'), (1, 'c'), (0.5, 'w')])[1] - p8b) < 1e-12)
fac9 = np.mean([1.1 ** -k for k in (1, 2, 3)])
v.check("28-10.9a", fac9)
v.check("28-10.9b", 50 * 0.3 * 2 * fac9)
v.check("28-10.9c", 100 / (50 * 0.3 * 2 * fac9))
v.check("28-10.10a", np.mean([(0.8 - 1) ** 2] * 5 + [(0.6 - 0) ** 2] * 5))
v.check("28-10.10b", 0.25)
v.check("28-10.10c", np.mean([(0.95 - 1) ** 2] * 6 + [0.95 ** 2] * 4))
v.check("28-10.11a", 25 * 0.5)
v.check("28-10.11b", 25 * 0.5 - 3)
v.check("28-10.11c", area_budget(9.5))
q = 0.7
mc = RNG.random(400_000) < q
v.check("28-10.12a", float(np.mean((0.7 - mc) ** 2)), tol=0.002)
v.check("28-10.12b", float(np.mean((0.9 - mc) ** 2)), tol=0.002)
v.assert_true("P12b: closed form (p-q)^2 + q(1-q)", abs((0.9 - q) ** 2 + q * (1 - q) - 0.25) < 1e-12)
v.assert_true("P12a: order of answers does not matter",
              abs(odds_post(0.3, [3, 0.4, 2])[0] - odds_post(0.3, [2, 3, 0.4])[0]) < 1e-12)

# --- Lab ---------------------------------------------------------------------------------------
v.check("Lab 28-10.a", 100 * odds_post(0.4, [3, 2, 0.5, 1, 3, 0.3])[1])
v.check("Lab 28-10.c", cv.brier([0.8] * 5 + [0.6] * 5, [1] * 5 + [0] * 5))
v.check("Lab 28-10.d", 100 * odds_post(0.4, [3, 2, 0.5, 1])[1])

sys.exit(v.finish())
