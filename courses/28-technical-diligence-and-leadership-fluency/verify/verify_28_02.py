#!/usr/bin/env python3
"""Verify every number in chapter 28-02 (validating claims), its problems and its lab.

Independent routes (the lab module uses closed forms):
- peak throughput from MacTOPS and per-unit operation counts, TPP from the rule's own
  definition, the roofline with numpy;
- energy floors from the 45 nm table entries [R-208, R-458] and HBM2's 3.9 pJ/bit [R-459];
- operating points by fitting alpha*C from the measured point and evaluating P = aCV^2 f;
- means with scipy.stats.gmean; expected maxima of normals by scipy quadrature of the
  order-statistic density, with a Monte Carlo cross-check;
- schedules by summing explicit step lists.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import claimcheck as cc  # noqa: E402

v = Verifier.from_files("28-02", ROOT / "chapters" / "28-02-validating-claims.md",
                        ROOT / "solutions" / "28-02-solutions.md", LAB / "README.md")


def emax(n):
    f = lambda x: x * n * stats.norm.pdf(x) * stats.norm.cdf(x) ** (n - 1)  # noqa: E731
    return integrate.quad(f, -12, 12, limit=200)[0]


def weeks(steps):
    return sum(steps)


DAY = 30.44  # days per month, as the chapter states
# ---------------------------------------------------------------------------
# Example 28-02.1
# ---------------------------------------------------------------------------
mactops = 32768 * 1.2e9 / 1e12
dense = 2 * mactops
v.check("Ex 28-02.1a", dense)
v.check("Ex 28-02.1b", 2 * dense)
v.check("Ex 28-02.1c", 0.35 * dense)
v.check("Ex 28-02.1d", mactops)
tpp8 = 2 * mactops * 8
v.check("Ex 28-02.1d1", tpp8)
v.check("Ex 28-02.1d2", 100 * tpp8 / 4800)
v.assert_true("TPP unchanged at INT4", abs(2 * (2 * mactops) * 4 - tpp8) < 1e-9)

# Example 28-02.2
e_op = 1 / (100e12)
v.check("Ex 28-02.2a", e_op * 1e15)
v.check("Ex 28-02.2a1", 2 * e_op * 1e15)
mac45 = (0.2 + 0.03) * 1e-12
v.check("Ex 28-02.2b", mac45 * 1e15)
v.check("Ex 28-02.2b1", mac45 / 2 * 1e15)
v.check("Ex 28-02.2b2", (mac45 / 2) / e_op)
dram_b = 640e-12 / 4
v.check("Ex 28-02.2c", dram_b * 1e12)
v.check("Ex 28-02.2c1", dram_b / (0.1 * e_op))
hbm_b = 3.9e-12 * 8
v.check("Ex 28-02.2d", hbm_b * 1e12)
v.check("Ex 28-02.2d1", hbm_b / (0.1 * e_op))

# Example 28-02.3: fit alpha*C*k from the measured point, then evaluate
ops0, p0, v0, f0 = 80e12, 4.0, 0.60, 0.4e9
ac = p0 / (v0 ** 2 * f0)          # alpha*C in W/(V^2 Hz)
ops_per_hz = ops0 / f0
p_pk = ac * 0.90 ** 2 * 1.0e9
v.check("Ex 28-02.3a", p_pk)
v.check("Ex 28-02.3b", ops_per_hz * 1.0e9 / 1e12 / p_pk)
v.check("Ex 28-02.3c", 20 / (0.90 / 0.60) ** 2)
v.assert_true("200 TOPS is the peak point's throughput", abs(ops_per_hz * 1.0e9 - 200e12) < 1)

# Example 28-02.4
card = (10 + 3 + 1.5) / 0.9
server = card * 1.3
fac = server * 1.2
v.check("Ex 28-02.4a", 50 / 10)
v.check("Ex 28-02.4b", card)
v.check("Ex 28-02.4b1", 50 / card)
v.check("Ex 28-02.4c", server)
v.check("Ex 28-02.4c1", 50 / server)
v.check("Ex 28-02.4d", fac)
v.check("Ex 28-02.4d1", 50 / fac)

# Example 28-02.5
sp = np.array([1.2, 1.5, 0.8, 4.0])
v.check("Ex 28-02.5a", float(np.mean(sp)))
v.check("Ex 28-02.5a1", float(stats.gmean(sp)))
v.check("Ex 28-02.5b", float(np.mean(1 / sp)))
v.check("Ex 28-02.5b1", float(1 / np.mean(1 / sp)))
v.check("Ex 28-02.5b2", float(stats.gmean(1 / sp)))
e10 = emax(10)
v.check("Ex 28-02.5c", e10)
v.check("Ex 28-02.5c1", 1.5 * math.exp(0.3 * e10))
rng = np.random.default_rng(5)
mc10 = rng.standard_normal((200_000, 10)).max(axis=1).mean()
v.assert_true("Monte Carlo E[max of 10] agrees", abs(mc10 - e10) < 0.01)
v.assert_true("lab expected maximum agrees", abs(cc.expected_max_std_normal(10) - e10) < 1e-6)

# Example 28-02.6
qual_wk = 1000 / 168
v.check("Ex 28-02.6a", 9 * DAY / 7)
v.check("Ex 28-02.6b", qual_wk)
w_resp = weeks([3, 16, 4, 12]) + weeks([3, 16, 4]) + qual_wk + 2
v.check("Ex 28-02.6b1", w_resp)
v.check("Ex 28-02.6b2", w_resp * 7 / DAY)
w_none = weeks([3, 16, 4, 12]) + qual_wk + 2
v.check("Ex 28-02.6c", w_none)
v.check("Ex 28-02.6c1", w_none * 7 / DAY)
v.assert_true("lab schedule agrees",
              abs(cc.tapeout_to_production(3, 16, 4, 12, 1, 3, 16, 1000, 2) - w_resp) < 1e-12)

# Text
v.check("Txt 28-02.1", 1 / 50e12 * 1e15)
v.check("Txt 28-02.2", 640 / 32)
v.check("Txt 28-02.3", 80 * 1.0 / 7)
v.check("Txt 28-02.4", 80 * 1.5 / 7)
v.check("Txt 28-02.5", emax(5))
v.check("Txt 28-02.6", emax(20))
v.check("Txt 28-02.7", 1.5 * math.exp(0.3 * e10))

# ---------------------------------------------------------------------------
# Solutions
# ---------------------------------------------------------------------------
d1 = 2 * 128 * 128 * 0.94e9 / 1e12
v.check("28-02.1a", d1)
v.check("28-02.1b", 2 * d1)
v.check("28-02.1c", 4 * d1)
v.check("28-02.1d", 0.4 * d1)
for k, eta in (("a", 10), ("c", 2.5), ("e", 50)):
    v.check(f"28-02.2{k}", 1e15 / (eta * 1e12))
    v.check(f"28-02.2{chr(ord(k) + 1)}", 2e12 / (eta * 1e12))
v.check("28-02.3a", 200e12 / 3.2e12)
for ka, kb, inten in (("b", "c", 40), ("d", "e", 10)):
    att = float(np.minimum(200e12, inten * 3.2e12))
    v.check(f"28-02.3{ka}", att / 1e12)
    v.check(f"28-02.3{kb}", 100 * att / 200e12)
terms = [0.05, 0.6 / 10, 31.2 / 500]
floor = sum(terms)
v.check("28-02.4a", floor)
v.check("28-02.4b", 1 / floor)
for k, t in zip("cde", terms):
    v.check(f"28-02.4{k}", 100 * t / floor)
v.check("28-02.5", 30 * (0.55 / 0.85) ** 2)
mod = (4.0 + 1.2 + 0.3) / 0.85
v.check("28-02.6a", mod)
v.check("28-02.6b", 26 / mod)
v.check("28-02.6c", 26 / 2.6)
v.check("28-02.7a", 2 * 500 * 16)
v.check("28-02.7b", 2 * 300 * 8)
v.check("28-02.7c", 2 * 500 * 16 / 800)
tR, tR2, tA, tB = np.array([10, 10]), np.array([5, 20]), np.array([5, 20]), np.array([8, 8])
for (ka, kg), ref, m in ((("a", "b"), tR, tA), (("c", "d"), tR, tB), (("e", "f"), tR2, tA), (("g", "h"), tR2, tB)):
    r = ref / m
    v.check(f"28-02.8{ka}", float(np.mean(r)))
    v.check(f"28-02.8{kg}", float(stats.gmean(r)))
v.check("28-02.9a", emax(5))
v.check("28-02.9b", 1.3 * math.exp(0.25 * emax(5)))
v.check("28-02.9c", emax(20))
v.check("28-02.9d", 1.3 * math.exp(0.25 * emax(20)))
v.check("28-02.11a", 70 * 1.2 / 7)
v.check("28-02.11b", 70 * 1.5 / 7)
base = weeks([2.5, 14, 3, 10])
qual = qual_wk + 2
w_m = base + weeks([1, 5, 3]) + qual
w_f = base + weeks([2.5, 14, 3]) + qual
v.check("28-02.12a", w_m)
v.check("28-02.12b", w_m * 7 / DAY)
v.check("28-02.12c", w_f)
v.check("28-02.12d", w_f * 7 / DAY)
v.check("28-02.12e", 0.6 * w_m + 0.4 * w_f)
v.check("28-02.12f", (0.6 * w_m + 0.4 * w_f) * 7 / DAY)
v.check("28-02.12g", 12 * DAY / 7)
v.check("28-02.12h", 0.6)
v.check("28-02.12i", qual)
v.assert_true("only the metal-only path meets 12 months", w_m < 12 * DAY / 7 < w_f)
v.check("28-02.13a", 1000 / 75)
dec = 200e9 / 7e9
v.check("28-02.13b", dec)
v.check("28-02.13c", 4000 / dec)
v.check("28-02.14a", (0.90 / 0.60) ** 2)

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
pk = 2 * 32768 * 1.2e9
v.check("Lab 28-02.a", pk / 64e9)
att = min(pk, 300 * 64e9)
v.check("Lab 28-02.a1", att / 1e12)
v.check("Lab 28-02.a2", 100 * att / pk)
v.check("Lab 28-02.b", ops_per_hz * 0.7e9 / 1e12)
p_b = ac * 0.75 ** 2 * 0.7e9
v.check("Lab 28-02.b1", p_b)
v.check("Lab 28-02.b2", ops_per_hz * 0.7e9 / 1e12 / p_b)
v.check("Lab 28-02.c", emax(20))
v.check("Lab 28-02.c1", 1.5 * math.exp(0.3 * emax(20)))
w_l = weeks([3, 16, 4, 12]) + weeks([2, 6, 4]) + qual_wk + 2
v.check("Lab 28-02.d", w_l)
v.check("Lab 28-02.d1", w_l * 7 / DAY)

sys.exit(v.finish())
