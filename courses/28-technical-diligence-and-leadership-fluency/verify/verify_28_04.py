#!/usr/bin/env python3
"""Verify every number in chapter 28-04 (domain question banks I), its problems and its
lab.

Independent routes (the lab module uses closed forms):
- iso-power requirements with exact rational arithmetic (fractions), and by solving
  g_C (R/g_IPC)^3 (1 - x) = 1 for x with a root finder;
- ridge-point batches by bisection on the roofline (smallest batch at which attainable
  throughput reaches peak), and decode FLOP and bytes counted per weight for a model;
- memory, link and port power from unit-by-unit products in SI (bytes -> bits -> joules);
- interview scoring with log-odds sums and a brute-force search for the number of strong
  answers needed.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "28-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import qbank as qb  # noqa: E402

v = Verifier.from_files(
    "28-04",
    ROOT / "chapters" / "28-04-question-banks-digital-ai-memory-interconnect.md",
    ROOT / "solutions" / "28-04-solutions.md",
    LAB / "README.md",
)
PJ = 1e-12


def iso_exact(perf, ipc, cap=Fr(1)):
    """Exact frequency ratio, power factor and reduction with rationals."""
    f = Fr(perf) / Fr(ipc)
    pf = Fr(cap) * f ** 3
    return f, pf, 1 - 1 / pf


def iso_root(perf, ipc, cap=1.0):
    """Reduction x solving cap (perf/ipc)^3 (1 - x) = 1."""
    return optimize.brentq(lambda x: cap * (perf / ipc) ** 3 * (1 - x) - 1, -5, 0.999999)


def ridge_batch_bisect(peak, bw, bytes_per_weight):
    """Batch (continuous) at which decode intensity 2B/b_w times bandwidth reaches peak."""
    lo, hi = 0.0, 1e6
    for _ in range(200):
        mid = (lo + hi) / 2
        if 2 * mid / bytes_per_weight * bw < peak:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def decode_counts(n_params, batch, bytes_per_weight):
    """FLOP and weight bytes of one decode step for a model of n_params."""
    flop = 2 * n_params * batch          # one multiply and one add per weight per sequence
    weight_bytes = n_params * bytes_per_weight
    return flop, weight_bytes


def power_from_bytes(bytes_per_s, pj):
    bits = bytes_per_s * 8
    return bits * pj * PJ


def post_logodds(prior, ratios):
    lo = math.log(prior / (1 - prior)) + sum(math.log(r) for r in ratios)
    odds = math.exp(lo)
    return odds, odds / (1 + odds)


# --- Example 28-04.1 ------------------------------------------------------------------
f, pf_freq, _ = iso_exact(Fr(125, 100), Fr(115, 100))
_, pf, red = iso_exact(Fr(125, 100), Fr(115, 100), Fr(110, 100))
v.check("Ex 28-04.1a", float(f))
v.check("Ex 28-04.1a1", 100 * float(f - 1))
v.check("Ex 28-04.1b", float(pf_freq))
v.check("Ex 28-04.1b1", 100 * float(pf_freq - 1))
v.check("Ex 28-04.1c", float(pf))
v.check("Ex 28-04.1d", 100 * float(red))
v.check("Ex 28-04.1e", 100 * (1 - 1 / 1.25))
v.assert_true("Ex 1: root finder agrees", abs(iso_root(1.25, 1.15, 1.10) - float(red)) < 1e-9)
v.assert_true("Ex 1: lab model agrees", abs(qb.iso_power(1.25, 1.15, 1.10)[2] - float(red)) < 1e-12)

# --- Example 28-04.2 ------------------------------------------------------------------
F2, BW2 = 2e15, 8e12
flop, wbytes = decode_counts(70e9, 16, 1)
I16 = flop / wbytes
v.check("Ex 28-04.2a", F2 / BW2)
v.check("Ex 28-04.2b", I16)
att = min(F2, I16 * BW2)
v.check("Ex 28-04.2b1", att / 1e12)
v.check("Ex 28-04.2b2", 100 * att / F2)
v.check("Ex 28-04.2c", ridge_batch_bisect(F2, BW2, 1))
v.check("Ex 28-04.2d", wbytes / 1e9)
v.assert_true("Ex 2: lab intensity agrees", qb.decode_intensity(16, 1) == I16)

# --- Example 28-04.3 ------------------------------------------------------------------
v.check("Ex 28-04.3a", 1024 * 9.6e9 / 8 / 1e9)
v.check("Ex 28-04.3b", 2048 * 8e9 / 8 / 1e9)
bw117 = 2048 * 11.7e9 / 8
v.check("Ex 28-04.3c", bw117 / 1e9)
v.check("Ex 28-04.3c1", 2048 * 13e9 / 8 / 1e9)
v.check("Ex 28-04.3d", power_from_bytes(bw117, 6.5))
v.check("Ex 28-04.3e", 248 / (4.52e12 * 8) / PJ)
v.check("Ex 28-04.3e1", 100 * 248 / 700)

# --- Example 28-04.4 ------------------------------------------------------------------
v.check("Ex 28-04.4a", 102.4e12 * 3 * PJ)
v.check("Ex 28-04.4b", power_from_bytes(4e12, 0.5))
v.check("Ex 28-04.4b1", power_from_bytes(4e12, 0.25))
v.check("Ex 28-04.4b2", power_from_bytes(4e12, 3))
v.check("Ex 28-04.4c", 4000 / 165)
v.check("Ex 28-04.4c1", 4000 / 1317)
v.assert_true("Ex 4: 4 TB/s is 32 Tb/s", 4e12 * 8 == 32e12)

# --- Example 28-04.5 ------------------------------------------------------------------
v.check("Ex 28-04.5a", 25 / 1.6e12 / PJ)
v.check("Ex 28-04.5a1", 5 / 1.6e12 / PJ)
v.check("Ex 28-04.5a2", 25 / 0.8e12 / PJ)
v.check("Ex 28-04.5a3", 5 / 0.8e12 / PJ)
v.check("Ex 28-04.5b", 144 * 25)
v.check("Ex 28-04.5b1", 144 * 5)
v.check("Ex 28-04.5b2", 144 * (25 - 5))
v.check("Ex 28-04.5c", 144 * 4)
v.check("Ex 28-04.5c1", 144 * 4 // 4)
v.check("Ex 28-04.5d", 10 ** 1.8)
v.check("Ex 28-04.5d1", 10 ** 0.9)
v.check("Txt 28-04.1", -math.log(0.05) / 1e6 * 1e9, tol=50)
v.assert_true("Ex 5: 22 dB to 4 dB is an 18 dB cut", 22 - 4 == 18)

# --- Example 28-04.6 ------------------------------------------------------------------
odds6, p6 = post_logodds(0.5, [3, 3, 0.4, 1, 3])
v.check("Ex 28-04.6a", odds6)
v.check("Ex 28-04.6b", 100 * p6)
odds6c, p6c = post_logodds(0.5, [3, 0.4, 1, 3])
v.check("Ex 28-04.6c", odds6c)
v.check("Ex 28-04.6d", 100 * p6c)
v.assert_true("Ex 6: lab posterior agrees", abs(qb.posterior(0.5, [3, 3, 0.4, 1, 3])[0] - odds6) < 1e-9)

# --- Problem 28-04.2 ------------------------------------------------------------------
f2, pf2, red2 = iso_exact(Fr(130, 100), Fr(112, 100))
v.check("28-04.1a", 100 * 2 * 32 * 8e12 / 2e15)
v.check("28-04.1b", 2 * 32 / 0.40)
v.check("28-04.2a", float(f2))
v.check("28-04.2b", 100 * float(f2 - 1))
v.check("28-04.2c", float(pf2))
v.check("28-04.2d", 100 * float(red2))
v.assert_true("P2: root finder agrees", abs(iso_root(1.30, 1.12) - float(red2)) < 1e-9)
v.assert_true("P2: exceeds N2's reported 30%", float(red2) > 0.30)

# --- Problem 28-04.3 ------------------------------------------------------------------
ch = 6400e6 * 64 / 8
v.check("28-04.3a", ch / 1e9)
tot = 12 * ch
v.check("28-04.3b", tot / 1e9)
v.check("28-04.3c", tot / 128 / 1e9)
v.check("28-04.3d", tot / 96 / 1e9)
v.check("28-04.3e", 128 / 96)
v.assert_true("P3: lab channel model agrees", abs(qb.ddr_channel_gbs(6400) - ch / 1e9) < 1e-12)

# --- Problem 28-04.4 ------------------------------------------------------------------
F4, BW4 = 5e15, 8e12
v.check("28-04.4a", F4 / BW4)
v.check("28-04.4b", ridge_batch_bisect(F4, BW4, 1))
v.check("28-04.4c", ridge_batch_bisect(F4, BW4, 0.5))
flop4, wb4 = decode_counts(70e9, 16, 1)
att4 = min(F4, flop4 / wb4 * BW4)
v.check("28-04.4d", att4 / 1e12)
v.check("28-04.4e", 100 * att4 / F4)

# --- Problem 28-04.5 ------------------------------------------------------------------
w5 = 405e9 * 1
kv5 = 64 * 2e9
v.check("28-04.5a", w5 / 1e9)
v.check("28-04.5b", kv5 / 1e9)
v.check("28-04.5c", (w5 + kv5) / 1e9)
n_w = next(n for n in range(1, 100) if n * 192e9 >= w5)
n_all = next(n for n in range(1, 100) if n * 192e9 >= w5 + kv5)
v.check("28-04.5d", n_w)
v.check("28-04.5e", n_all)
v.check("28-04.5f", (n_all * 192e9 - w5 - kv5) / 1e9)
v.assert_true("P5: lab device count agrees", qb.devices_for(w5 + kv5, 192e9) == n_all)

# --- Problem 28-04.6 ------------------------------------------------------------------
h3e = 1024 * 9.2e9 / 8
h4 = 2048 * 8e9 / 8
v.check("28-04.6a", h3e / 1e9)
v.check("28-04.6b", h4 / 1e9)
v.check("28-04.6c", h4 / h3e)
v.check("28-04.6d", 8 * 2048 * 11.7e9 / 8 / 1e12)

# --- Problems 28-04.7 to 28-04.9 ----------------------------------------------------
v.check("28-04.7", power_from_bytes(8e12, 6.5))
v.check("28-04.8a", 51.2e12 * (3 + 2) * PJ)
v.check("28-04.8b", 51.2e12 * 3 * PJ)
v.assert_true("P8: DSP is 40% of the total", abs(2 / 5 - 0.4) < 1e-15)
v.check("28-04.9a", power_from_bytes(2e12, 0.25))
v.check("28-04.9b", power_from_bytes(2e12, 0.5))
v.check("28-04.9c", 2000 / 165)
v.check("28-04.9d", 2000 / 1317)

# --- Problem 28-04.10 -----------------------------------------------------------------
v.check("28-04.10a", 64 * 25)
v.check("28-04.10b", 64 * 5)
v.check("28-04.10c", 25 / 800e9 / PJ)
v.check("28-04.10d", 5 / 800e9 / PJ)
mw = 10 ** (20 / 10)
v.check("28-04.10e", mw)
v.check("28-04.10f", mw / 1000 / 0.15)
v.assert_true("P10: lab dBm conversion agrees", abs(qb.dbm_to_mw(20) - mw) < 1e-12)

# --- Problem 28-04.11 -----------------------------------------------------------------
o11, p11 = post_logodds(0.5, [3, 0.4, 1, 3])
v.check("28-04.11a", o11)
v.check("28-04.11b", 100 * p11)
n11 = next(n for n in range(0, 50) if post_logodds(0.5, [0.4] + [3] * n)[1] >= 0.95)
v.check("28-04.11c", n11)
o4, p4 = post_logodds(0.5, [0.4] + [3] * n11)
v.check("28-04.11d", o4)
v.check("28-04.11e", 100 * p4)
v.assert_true("P11: three strong answers fall short", post_logodds(0.5, [0.4, 3, 3, 3])[1] < 0.95)
v.assert_true("P11: lab search agrees", qb.strong_needed(0.5, [0.4], 3, 0.95) == n11)

# --- Problem 28-04.12 identities -----------------------------------------------------
for R, g, c in ((1.25, 1.15, 1.10), (1.30, 1.12, 1.0), (1.40, 1.05, 0.95)):
    x = qb.iso_power(R, g, c)[2]
    v.assert_true(f"P12a: reduction holds power at R={R}", abs(c * (R / g) ** 3 * (1 - x) - 1) < 1e-12)
for n_p, b, bw in ((7e9, 4, 1), (70e9, 32, 0.5), (405e9, 8, 2)):
    fl, by = decode_counts(n_p, b, bw)
    v.assert_true(f"P12b: intensity 2B/b_w at B={b}", abs(fl / by - 2 * b / bw) < 1e-9)
v.assert_true("P12b: ridge batch b_w F/(2 B_mem)",
              abs(ridge_batch_bisect(3e15, 6e12, 1) - 1 * 3e15 / (2 * 6e12)) < 1e-6)
v.assert_true("P12c: halving pJ/bit doubles the bandwidth a budget buys",
              abs((10 / (0.25 * PJ)) / (10 / (0.5 * PJ)) - 2) < 1e-12)

# --- Lab ---------------------------------------------------------------------------------
fa, pfa, ra = iso_exact(Fr(125, 100), Fr(120, 100), Fr(110, 100))
v.check("Lab 28-04.a", float(fa))
v.check("Lab 28-04.a1", float(pfa))
v.check("Lab 28-04.a2", 100 * float(ra))
v.check("Lab 28-04.b", ridge_batch_bisect(F2, BW2, 0.5))
fl_b, by_b = decode_counts(70e9, 16, 0.5)
v.check("Lab 28-04.b1", 100 * min(F2, fl_b / by_b * BW2) / F2)
v.check("Lab 28-04.c", power_from_bytes(bw117, 6.5))
v.check("Lab 28-04.c1", 8 * power_from_bytes(bw117, 6.5))
v.check("Lab 28-04.c2", power_from_bytes(bw117, 5.5))
v.check("Lab 28-04.c3", power_from_bytes(bw117, 7.5))
od, pd = post_logodds(0.5, [3, 3, 0.4, 1, 3, 0.4])
v.check("Lab 28-04.d", od)
v.check("Lab 28-04.d1", 100 * pd)
v.assert_true("Lab: trajectory ends at the posterior",
              abs(qb.trajectory(0.5, [3, 3, 0.4, 1, 3, 0.4])[-1] - pd) < 1e-12)
v.assert_true("Lab: one evasion (0.4) costs less than a strong answer (3) gains", 3 * 0.4 > 1)
v.assert_true("Lab: a 0.1 dodge undoes two strong answers", 3 * 3 * 0.1 < 1)

v.check("28-04.12c", 64 * 32e9 / 8 / 1e9)
v.check("28-04.12d", 2 * 64 * 32e9 / 8 / 1e9 / 1317)

sys.exit(v.finish())
