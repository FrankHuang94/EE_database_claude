#!/usr/bin/env python3
"""Verify every published number in chapter 00-05, its solutions and its lab handout.

Schedule distributions are computed by numerical convolution of triangular densities and
cross-checked by Monte Carlo sampling.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "00-05",
    COURSE / "chapters" / "00-05-how-chip-companies-are-organized.md",
    COURSE / "solutions" / "00-05-solutions.md",
    COURSE / "labs" / "00-05-lab" / "README.md",
)
DX = 0.001
X = np.arange(0, 140, DX)


def tri_pdf(a, m, b):
    up = np.where((X >= a) & (X < m), 2 * (X - a) / ((b - a) * (m - a)), 0.0)
    down = np.where((X >= m) & (X <= b), 2 * (b - X) / ((b - a) * (b - m)), 0.0)
    p = up + down
    return p / (p.sum() * DX)


def total_dist(phases):
    pdf = None
    for a, m, b in phases:
        p = tri_pdf(a, m, b)
        pdf = p if pdf is None else np.convolve(pdf, p)[: len(X)] * DX
    cdf = np.cumsum(pdf) * DX
    return pdf, cdf


def stats(phases):
    pdf, cdf = total_dist(phases)
    mean = (X * pdf).sum() * DX
    mode_sum = sum(m for _, m, _ in phases)
    return mode_sum, mean, np.interp(mode_sum, X, cdf), np.interp(0.8, cdf, X)


def mc(phases, n=2_000_000, seed=11):
    rng = np.random.default_rng(seed)
    return sum(rng.triangular(a, m, b, n) for a, m, b in phases)


# Example 1
v.check("Ex 00-05.1a", 80 * 1.25)
v.check("Ex 00-05.1b", 80 * 1.25 / 7)
v.check("Ex 00-05.1c", 12 * 1.25)
# Example 2
v.check("Ex 00-05.2", 500 * 3 / 12 * 0.60)
# Example 3
ey = 0.5 * 250e6 / 300e3
v.check("Ex 00-05.3a", ey)
v.check("Ex 00-05.3b", ey / 2.5)
# Example 4
v.check("Ex 00-05.4a", 100 * 0.98**10)
v.check("Ex 00-05.4b", 100 * 0.98**50)
v.check("Ex 00-05.4c", 0.95 ** (1 / 50))
# Example 5
EX5 = [(20, 26, 40), (10, 12, 20), (12, 14, 20)]
ms, mean, p_ms, p80 = stats(EX5)
v.check("Ex 00-05.5a", ms)
v.check("Ex 00-05.5b", mean)
v.check("Ex 00-05.5c", 100 * p_ms)
v.check("Ex 00-05.5d", p80)
s = mc(EX5)
v.assert_true("Ex5 Monte Carlo agrees with convolution",
              abs(s.mean() - mean) < 0.02 and abs((s <= ms).mean() - p_ms) < 0.002 and abs(np.quantile(s, 0.8) - p80) < 0.03)
v.assert_true("Ex5 mean equals sum of (a+m+b)/3", abs(mean - sum((a + m + b) / 3 for a, m, b in EX5)) < 1e-3)

# Problems
v.check("00-05.3a", 60 * 1.5)
v.check("00-05.3b", 60 * 0.8)
v.check("00-05.3c", 12 * 1.2)
v.check("00-05.4a", 100 * 0.99**20)
v.check("00-05.4b", 0.90 ** (1 / 100))
v.check("00-05.5", 300 * 4 / 12 * 0.55)
ey6 = 0.6 * 400e6 / 350e3
v.check("00-05.6a", ey6)
v.check("00-05.6b", ey6 / 3)
v.check("00-05.7a", 100 * 31000 / 42000)
v.check("00-05.7b", 100 * 13000 / 24500)
v.check("00-05.8", (1 - 0.14) / (1 - 0.30))
P9 = [(16, 20, 32), (8, 10, 16), (12, 14, 20)]
ms9, mean9, p9, p809 = stats(P9)
v.check("00-05.9a", ms9)
v.check("00-05.9b", mean9)
v.check("00-05.9c", 100 * p9)
v.check("00-05.9d", p809)
v.check("00-05.10a", 0.29 * 725)
v.check("00-05.10b", 725 / 1.66)
v.check("00-05.10c", 725 / 1.50)

# Lab: add a 30 % chance of a 6-10 week (triangular 6, 8, 10) metal fix to Example 5
q = 0.30
v.check("Lab 00-05.1", mean + q * 8)
rng = np.random.default_rng(5)
n = 2_000_000
base = sum(rng.triangular(a, m, b, n) for a, m, b in EX5)
fix = np.where(rng.random(n) < q, rng.triangular(6, 8, 10, n), 0.0)
v.check("Lab 00-05.2", np.quantile(base + fix, 0.8), tol=0.06)  # Monte Carlo noise ~0.01 week
v.check("Lab 00-05.3", 0.5 ** (1 / 100))

v.finish()
