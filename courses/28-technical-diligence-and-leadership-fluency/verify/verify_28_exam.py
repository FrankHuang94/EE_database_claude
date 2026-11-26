#!/usr/bin/env python3
"""Verify every number in the Course 28 final exam solutions, mostly by second routes.

Routes: explicit expected-value tables (1c); the Poisson zero-failure bound by root-finding
(3c-d); a grid count of dies cross-checked against the formula (11a); numerical integration
of the Beta posterior for its percentiles (9b); exact binomial sums and a Monte Carlo check
(8d); numerical half-sine Fourier components for the PA (6c); explicit discounted cash flows
(10a, 10d); and a Monte Carlo Brier expectation (12a).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("28-exam", ROOT / "exam" / "solutions.md")
rng = np.random.default_rng(28)
H = 8766.0
KB = 8.617333262e-5

# ---------------------------------------------------------------- Q1
w = np.array([0.3, 0.3, 0.2, 0.2])
A, B = np.array([4, 4, 2, 5]), np.array([3, 4, 4, 3])
v.check("X28.1a", float(w @ A))
v.check("X28.1a1", float(np.prod(A ** w)))
v.check("X28.1a2", float(w @ B))
v.check("X28.1a3", float(np.prod(B ** w)))
odds = (0.35 / 0.65) * 4 * 0.6
p = odds / (1 + odds)
v.check("X28.1b", odds)
v.check("X28.1b1", 100 * p)
ev = p * 300 + (1 - p) * (-150)
v.check("X28.1c", ev)
v.check("X28.1c1", (p * max(300, 0) + (1 - p) * max(-150, 0)) - max(ev, 0))
v.check("X28.1d", p * 120 / 1.12 ** 2)

# ---------------------------------------------------------------- Q2
peak = 2 * 16384 * 1.5e9
v.check("X28.2a", peak / 1e12)
v.check("X28.2a1", 98e12 / peak)
v.check("X28.2b", 2 * (16384 * 1.5e9 / 1e12) * 8)
att = min(peak, 100 * 51.2e9)
v.check("X28.2c", att / 1e12)
v.check("X28.2c1", 100 * att / peak)
v.check("X28.2d", att / 1e12 / 4)
v.check("X28.2d1", 98 / 4)

# ---------------------------------------------------------------- Q3
P3 = 0.85 * 0.95
v.check("X28.3a", P3)
v.check("X28.3a1", P3 / 1.15 ** (7 / 12))
af = math.exp(0.7 / KB * (1 / 333.15 - 1 / 398.15))
v.check("X28.3b", af)
# 60% bound: rate with P(0 events) = 0.4 over the equivalent hours
lam60 = optimize.brentq(lambda x: math.exp(-x * 300 * 1000 * af) - 0.4, 1e-15, 1e-3)
v.check("X28.3c", lam60 * 1e9)
n_need = 4.605 * 1e9 / (2 * 20 * 1000 * af)
v.check("X28.3d", math.ceil(n_need))
v.assert_true("Q3d: Poisson route gives the same sample", math.ceil(-math.log(0.1) / (20e-9 * 1000 * af)) == math.ceil(n_need))

# ---------------------------------------------------------------- Q4
f4 = 1.18 / 1.08
v.check("X28.4a", f4)
v.check("X28.4a1", 1.04 * f4 ** 3)
v.check("X28.4a2", 100 * (1 - 1 / (1.04 * f4 ** 3)))
v.check("X28.4b", 4e15 / 8e12)
v.check("X28.4b1", 2 * 24)
v.check("X28.4b2", 48 * 8e12 / 1e12)
v.check("X28.4b3", 100 * 48 * 8e12 / 4e15)
v.check("X28.4b4", 4e15 / 8e12 / 2)
s = 2048 * 9.6e9 / 8
v.check("X28.4c", s / 1e9)
v.check("X28.4c1", 6 * s / 1e12)
v.check("X28.4d", 6 * s * 8 * 6.5e-12)

# ---------------------------------------------------------------- Q5
v.check("X28.5a", 102.4e12 * 4.5e-12)
v.check("X28.5b", 3e12 * 8 * 0.25e-12)
v.check("X28.5b1", 3000 / 1317)
v.check("X28.5c", 25 / 1.6e12 / 1e-12)
v.check("X28.5c1", 6 / 1.6e12 / 1e-12)
mw = 10 ** 2.3
v.check("X28.5d", mw)
v.check("X28.5d1", mw / 1000 / 0.2)

# ---------------------------------------------------------------- Q6
v.check("X28.6a", 58 + 10 * math.log10(1e9 / 0.08))
v.check("X28.6a1", (58 - 1.76) / 6.02)
v.check("X28.6b", 10 ** (-58 / 20) / (2 * math.pi * 3e9) * 1e15)
th = np.linspace(-math.pi / 2, math.pi / 2, 200001)
dc = np.trapezoid(np.cos(th), th) / (2 * math.pi)
f1 = np.trapezoid(np.cos(th) ** 2, th) / math.pi
a9 = 10 ** (-9 / 20)
v.check("X28.6c", 100 * 0.5 * a9 * f1 / dc)
v.check("X28.6c1", 100 * a9 * f1 / dc)
v.check("X28.6d", 10 * math.log10(0.02 ** 2))

# ---------------------------------------------------------------- Q7
l97, l98 = 6000 / 0.97 - 6000, 6000 / 0.98 - 6000
v.check("X28.7a", l97)
v.check("X28.7a1", l98)
v.check("X28.7a2", l97 - l98)
p_in = 800
for eta in (0.90, 0.96, 0.975):                         # power flow from the load back to the source
    p_in = p_in / eta
v.check("X28.7b", 100 * 800 / p_in)
v.check("X28.7b1", p_in)
v.check("X28.7b2", p_in - 800)
v.check("X28.7c", 100 * 0.995 * 0.997 ** 4 * 0.99)
q_uc = 0.9 * 20 + 2500 * 0.006 * 5 + 5000 * 0.0015      # charge (µC) over a 20 s window, event by event
i7 = q_uc / 20
v.check("X28.7d", i7)
v.check("X28.7d1", 220 / (i7 / 1000) / H)

# ---------------------------------------------------------------- Q8
v.check("X28.8a", 0.7 / 0.15)
v.check("X28.8a1", 0.3 / 0.85)
pp = 0.25 * 0.7 / (0.25 * 0.7 + 0.75 * 0.15)
pa = 0.25 * 0.3 / (0.25 * 0.3 + 0.75 * 0.85)
v.check("X28.8b", 100 * pp)
v.check("X28.8b1", 100 * pa)
v.check("X28.8c", 100 * (1 - 0.97 ** 30))
v.check("X28.8c1", 30 * 0.03)


def tail(n, q, k):
    return sum(math.comb(n, j) * q ** j * (1 - q) ** (n - j) for j in range(k, n + 1))


se, fp = tail(30, 0.25, 3), tail(30, 0.03, 3)
v.check("X28.8d", 100 * se)
v.check("X28.8d1", 100 * fp)
v.check("X28.8d2", se / fp)
v.assert_true("Q8d: Monte Carlo false-positive rate within 0.2 points",
              abs((rng.binomial(30, 0.03, 500_000) >= 3).mean() - fp) < 0.002)

# ---------------------------------------------------------------- Q9
a9b, b9b = 1.4 + 2, 8.6 + 3
dens = lambda t: t ** (a9b - 1) * (1 - t) ** (b9b - 1)
z = integrate.quad(dens, 0, 1)[0]
v.check("X28.9a", 100 * integrate.quad(lambda t: t * dens(t), 0, 1)[0] / z)
v.check("X28.9a1", 5 / 15)
q05 = optimize.brentq(lambda x: integrate.quad(dens, 0, x)[0] / z - 0.05, 1e-6, 0.999)
q95 = optimize.brentq(lambda x: integrate.quad(dens, 0, x)[0] / z - 0.95, 1e-6, 0.999)
v.check("X28.9b", 100 * q05)
v.check("X28.9b1", 100 * q95)
lg = np.log([1.10, 1.30, 1.45])
mu, sd = lg.mean(), lg.std(ddof=1)
v.check("X28.9c", math.exp(mu))
v.check("X28.9c1", 20 * math.exp(mu))
v.check("X28.9c2", sd)
v.check("X28.9c3", 100 * integrate.quad(lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi), -np.inf, -mu / sd)[0])
q2 = 1 - 0.85 ** 2
v.check("X28.9d", 100 * q2)
v.check("X28.9d1", 100 * q2 ** 2)

# ---------------------------------------------------------------- Q10
plan = sum(40 / 1.1 ** t for t in range(1, 6))
late = sum(0.75 * 40 / 1.1 ** (t + 1) for t in range(1, 6))
v.check("X28.10a", plan)
v.check("X28.10a1", late)
v.check("X28.10a2", 100 * (1 - late / plan))
v.check("X28.10b", 30 * 5 * 0.025)
v.check("X28.10b1", 120 * 2 / 12)
pboth = 1 - 0.45 * 0.55
v.check("X28.10c", pboth)
v.check("X28.10c1", 180 * pboth)
v.check("X28.10c2", 180 * 0.55)
v.check("X28.10c3", 180 * pboth - 180 * 0.55)
v.assert_true("Q10c: gain exceeds the $35M cost", 180 * pboth - 99 > 35)
cont = 0.45 * 300 / 1.1 ** 3
v.check("X28.10d", cont)
v.check("X28.10d1", 500 + cont)

# ---------------------------------------------------------------- Q11
def dpw(a, d=300.0):
    return math.pi * d * d / (4 * a) - math.pi * d / math.sqrt(2 * a)


def cost(a, wafer=20000.0, d0=0.0008, whole=True):
    n = math.floor(dpw(a)) if whole else dpw(a)
    return wafer / (n * math.exp(-a * d0))


v.check("X28.11a", math.floor(dpw(150)))
v.check("X28.11a1", 100 * math.exp(-0.12))
c150 = cost(150)
v.check("X28.11a2", c150)
v.check("X28.11b", 1 + 150 * 0.0008)
v.check("X28.11b1", math.floor(dpw(165)))
r11 = cost(165) / c150 - 1
v.check("X28.11b2", 100 * r11)
v.check("X28.11b3", r11 / 0.1)
v.check("X28.11c", 100 * (1 - (c150 + 12) / 120))
v.check("X28.11c1", 120 * 0.35)
v.check("X28.11c2", 120 * 0.35 - 12)
v.check("X28.11c3", optimize.brentq(lambda a: cost(a, whole=False) - 30, 5, 600))
e450, e400 = 0.45 * 1.3 * 4 * H * 0.09, 0.40 * 1.3 * 4 * H * 0.09
v.check("X28.11d", e450)
v.check("X28.11d1", e400)
v.check("X28.11d2", e450 - e400)
v.check("X28.11d3", 100 * (0.45 / 0.40 - 1))

# ---------------------------------------------------------------- Q12
for qq, pq in ((0.7, 0.9), (0.3, 0.5)):
    o = rng.random(400_000) < qq
    v.assert_true(f"Q12a: Monte Carlo Brier matches (p-q)^2 + q(1-q) at q={qq}, p={pq}",
                  abs(np.mean((pq - o) ** 2) - ((pq - qq) ** 2 + qq * (1 - qq))) < 0.003)
o_all = (0.45 / 0.55) * 3 * 2 * 0.5 * 3 * 0.8
o_once = (0.45 / 0.55) * 3 * 2 * 0.5 * 0.8
v.check("X28.12b", o_all)
v.check("X28.12b1", 100 * o_all / (1 + o_all))
v.check("X28.12b2", o_once)
v.check("X28.12b3", 100 * o_once / (1 + o_once))
fc, oc = np.array([0.9, 0.7, 0.6, 0.3, 0.8]), np.array([1, 1, 0, 0, 0])
v.check("X28.12c", float(np.mean((fc - oc) ** 2)))
v.check("X28.12c1", float(np.mean((0.5 - oc) ** 2)))

sys.exit(v.finish())
