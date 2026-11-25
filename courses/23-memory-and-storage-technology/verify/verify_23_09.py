#!/usr/bin/env python3
"""Verify every number in chapter 23-09 (compute-in-memory and near-memory computing), its problems and its lab.

Independent routes (the lab module cim.py uses closed forms):
- crossbar outputs by summing per-cell currents in a loop, and resistive-sensed columns by a full nodal solve;
- compute SNR by a seeded Monte Carlo that must agree with 1/sigma^2 within 0.5 dB, and effective bits from SNR;
- ADC resolution by enumerating the largest column sum, energy per MAC by counting conversions;
- PIM throughput by multiplying out the hardware, decode rates from bytes per token;
- Amdahl fractions by root-finding on the speedup.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("23-09", ROOT / "chapters" / "23-09-compute-in-memory.md",
                        ROOT / "solutions" / "23-09-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- independent helpers
def column_current_loop(volts, gcol):
    total = 0.0
    for vi, gi in zip(volts, gcol):
        total += vi * gi
    return total


def sensed_column(volts, gcol, r_sense):
    """Nodal solve of one column node: sum_i G_i (V_i - Vc) = Vc / R."""
    gsum = sum(gcol)
    a = np.array([[gsum + 1 / r_sense]])
    b = np.array([sum(g * vv for g, vv in zip(gcol, volts))])
    vc = np.linalg.solve(a, b)[0]
    return vc, vc / r_sense


def snr_db(sigma):
    return 10 * math.log10(1 / sigma ** 2)


def enob_from(snr):
    return (snr - 1.76) / 6.02


def speedup(f, s):
    return 1 / ((1 - f) + f / s)


def frac_for(target, s):
    return optimize.brentq(lambda f: speedup(f, s) - target, 0, 1, xtol=1e-14)


def pair(weights, g, gmin):
    gp = [g * max(w, 0) + gmin for w in weights]
    gn = [g * max(-w, 0) + gmin for w in weights]
    return gp, gn


# ---------------------------------------------------------------- Example 23-09.1
mac_dram = 640 + 3.7 + 0.9
mac_sram = 5 + 3.7 + 0.9
v.check("Ex 23-09.1a", mac_dram)
v.check("Ex 23-09.1b", mac_sram)
v.check("Ex 23-09.1c", mac_dram / mac_sram)
v.check("Ex 23-09.1d", 7e9 * mac_dram * 1e-12)
v.check("Ex 23-09.1e", 640 / mac_dram * 100)
v.check("Txt 23-09.a", 640 / (3.7 + 0.9))

# ---------------------------------------------------------------- Example 23-09.2 and the lab
W = [[1, -2], [3, 0], [-1, 2], [2, 1]]
x = [2, 1, 0, 3]
V = [0.1 * xi for xi in x]
y = [sum(x[i] * W[i][j] for i in range(4)) for j in range(2)]
v.check("Ex 23-09.2a", y[0])
v.check("Ex 23-09.2a1", y[1])
cols = {}
for j in range(2):
    gp, gn = pair([W[i][j] for i in range(4)], 10e-6, 1e-6)
    cols[(j, "p")], cols[(j, "n")] = gp, gn
cur = {k: column_current_loop(V, g) for k, g in cols.items()}
v.check("Ex 23-09.2b", cur[(0, "p")] * 1e6)
v.check("Ex 23-09.2c", cur[(0, "n")] * 1e6)
v.check("Ex 23-09.2d", cur[(1, "p")] * 1e6)
v.check("Ex 23-09.2e", cur[(1, "n")] * 1e6)
v.check("Ex 23-09.2f", (cur[(0, "p")] - cur[(0, "n")]) * 1e6)
v.check("Ex 23-09.2g", (cur[(1, "p")] - cur[(1, "n")]) * 1e6)
v.check("Ex 23-09.2h", 0.1 * 10e-6 * 1e6)
v.check("Ex 23-09.2i", sum(V) * 1e-6 * 1e6)
v.check("Lab 23-09.a", cur[(0, "p")] * 1e6)
v.check("Lab 23-09.b", cur[(1, "n")] * 1e6)
v.check("Lab 23-09.c", (cur[(0, "p")] - cur[(0, "n")]) * 1e6)
v.check("Lab 23-09.d", (cur[(1, "p")] - cur[(1, "n")]) * 1e6)
sens = {k: sensed_column(V, g, 10e3) for k, g in cols.items()}
y1b = sens[(0, "p")][1] - sens[(0, "n")][1]
y2b = sens[(1, "p")][1] - sens[(1, "n")][1]
v.check("Lab 23-09.e", y1b * 1e6)
v.check("Lab 23-09.f", y2b * 1e6)
v.check("Lab 23-09.g", sens[(0, "p")][0] * 1e3)
v.check("Lab 23-09.h", (1 - y1b / 11e-6) * 100)
v.check("Txt 23-09.c", (1 - y1b / 11e-6) * 100)

# ---------------------------------------------------------------- Example 23-09.3 and the SNR Monte Carlo
for ident, s in (("a", 0.05), ("b", 0.01)):
    v.check(f"Ex 23-09.3{ident}0", snr_db(s))
    v.check(f"Ex 23-09.3{ident}", enob_from(snr_db(s)))
v.check("Ex 23-09.3a1", snr_db(0.05))
v.check("Txt 23-09.d", enob_from(snr_db(0.05)))
v.check("Txt 23-09.e", enob_from(snr_db(0.01)))
v.check("Lab 23-09.i", snr_db(0.05))
v.check("Lab 23-09.j", enob_from(snr_db(0.05)))
rng = np.random.default_rng(7)
w_mc = rng.normal(size=(256, 64))
sig, err = 0.0, 0.0
for _ in range(100):
    xm = rng.normal(size=256)
    ideal = xm @ w_mc
    noisy = xm @ (w_mc * (1 + 0.05 * rng.normal(size=w_mc.shape)))
    sig += np.sum(ideal ** 2)
    err += np.sum((noisy - ideal) ** 2)
v.assert_true("Monte Carlo SNR within 0.5 dB of 1/sigma^2", abs(10 * math.log10(sig / err) - snr_db(0.05)) < 0.5)

# ---------------------------------------------------------------- Example 23-09.4
max_sum = 256 * 1 * 1
v.check("Ex 23-09.4a", math.log2(max_sum + 1))
e_conv = 5e-15 * 2 ** 8
v.check("Ex 23-09.4b", e_conv * 1e12)
v.check("Ex 23-09.4c", e_conv / 256 * 1e15)
v.check("Ex 23-09.4h", 8 * 8)
v.check("Ex 23-09.4i", 4 * 4)
e8 = e_conv * 64 / 256
e4 = e_conv * 16 / 256
v.check("Ex 23-09.4d", e8 * 1e15)
v.check("Ex 23-09.4e", 2 / e8 / 1e12)
v.check("Ex 23-09.4f", e4 * 1e15)
v.check("Ex 23-09.4g", 2 / e4 / 1e12)

# ---------------------------------------------------------------- Example 23-09.5
v.check("Ex 23-09.5a", 4 * 32 * 16 * 2 * 300e6 / 1e12)
bw = 9.6e9 * 64 / 8
v.check("Ex 23-09.5b", bw / 1e9)
v.check("Ex 23-09.5c", 614e9 / bw)
v.check("Ex 23-09.5d", 614e9 / bw)

# ---------------------------------------------------------------- Example 23-09.6
v.check("Ex 23-09.6a", 76.8 / 7)
v.check("Ex 23-09.6b", 614 / 7)
f301 = frac_for(3.01, 8)
f228 = frac_for(2.28, 8)
v.check("Ex 23-09.6c", f301)
v.check("Ex 23-09.6d", f228)
v.check("Ex 23-09.6e", (1 - f301) * 100)
v.check("Ex 23-09.6f", (1 - f228) * 100)

# ---------------------------------------------------------------- Example 23-09.7 and 23-09.8
en = 200 / 8.25
v.check("Ex 23-09.7a", en)
v.check("Ex 23-09.7a1", en)
v.check("Ex 23-09.7b", 150 / en)
v.check("Ex 23-09.7c", 2400 / 600)
p_h = 63.1 / 9.76
v.check("Ex 23-09.7d", p_h)
v.check("Ex 23-09.8a", 63.1 * 0.3)
v.check("Ex 23-09.8a1", 63.1 * 0.3)
v.check("Ex 23-09.8b", 63.1 * 0.3 / p_h)
v.check("Txt 23-09.b", 3)

# ---------------------------------------------------------------- problems
v.check("23-09.1a", column_current_loop([0.1, 0.2, 0.05], [20e-6, 10e-6, 0]) * 1e6)
v.check("23-09.1b", column_current_loop([0.1, 0.2, 0.05], [5e-6, 15e-6, 25e-6]) * 1e6)

gp2, gn2 = pair([-2, 1, 3], 5e-6, 0.5e-6)
V2 = [0.1, 0.1, 0.2]
i2p, i2n = column_current_loop(V2, gp2), column_current_loop(V2, gn2)
v.check("23-09.2a", i2p * 1e6)
v.check("23-09.2b", i2n * 1e6)
v.check("23-09.2c", (i2p - i2n) * 1e6)
v.check("23-09.2d", -2 * 1 + 1 * 1 + 3 * 2)
v.check("23-09.2e", sum(V2) * 0.5e-6 * 1e6)

for ident, b in (("a", 8), ("b", 4)):
    snr = 6.02 * b + 1.76
    v.check(f"23-09.3{ident}0", snr)
    v.check(f"23-09.3{ident}", optimize.brentq(lambda s: snr_db(s) - snr, 1e-5, 1) * 100)
v.check("23-09.3a1", 6.02 * 8 + 1.76)

v.check("23-09.4a0", 64 / 0.1 ** 2)
v.check("23-09.4a", 10 * math.log10(64 / 0.1 ** 2))
v.check("23-09.4b0", 1 / 0.1 ** 2)
v.check("23-09.4b", 10 * math.log10(1 / 0.1 ** 2))

ms = 128 * 3 * 1
v.check("23-09.5a", ms)
v.check("23-09.5b", math.log2(ms + 1))
v.check("23-09.5c", math.ceil(math.log2(ms + 1)))
ec5 = 10e-15 * 2 ** 9
v.check("23-09.5d", ec5 * 1e12)
v.check("23-09.5e", ec5 / 128 * 1e15)

for ident, b in (("a", 8), ("b", 4)):
    e = 2e-15 * 2 ** 7 * b * b / 512
    v.check(f"23-09.6{ident}0", e * 1e15)
    v.check(f"23-09.6{ident}", 2 / e / 1e12)

ib = 16 * 256 / 8 / 4e-9
eb = 16 * 8e9 / 8
v.check("23-09.7a", ib / 1e9)
v.check("23-09.7b", eb / 1e9)
v.check("23-09.7c", ib / eb)

mb = 13e9 * 4 / 8
v.check("23-09.8a0", mb / 1e9)
v.check("23-09.8a", 4 * 76.8e9 / mb)
v.check("23-09.8b", 4 * 614e9 / mb)

v.check("23-09.9a", speedup(0.6, 8))
v.check("23-09.9b", speedup(0.9, 8))
v.check("23-09.9c", speedup(0.9, 1e12))

pc = (2 + 3) / 0.85
v.check("23-09.10a", pc)
v.check("23-09.10a1", pc)
v.check("23-09.10b", 40 / pc)
v.check("23-09.10c", 40 / 2)

v.check("23-09.11a", 100 * 0.4 / 7)
v.check("23-09.11b", 100 / 10)

vc, ic = sensed_column([0.2] * 4, [10e-6] * 4, 1e3)
v.check("23-09.12a", vc * 1e3)
v.check("23-09.12b", ic * 1e6)
v.check("23-09.12b1", ic * 1e6)
v.check("23-09.12c", (1 - ic / 8e-6) * 100)
rmax = optimize.brentq(lambda r: 1 - sensed_column([0.2] * 4, [10e-6] * 4, r)[1] / 8e-6 - 0.01, 1, 1e4)
v.check("23-09.12d", rmax)

emac = 2 / 100e12
v.check("23-09.13a", emac * 1e15)
econv = emac * 256 / 64
v.check("23-09.13b", econv * 1e15)
v.check("23-09.13c", econv / 2 ** 8 * 1e15)
v.check("23-09.13c1", econv / 2 ** 8 * 1e15)
v.check("23-09.13d", 5e-15 / (econv / 2 ** 8))

sys.exit(v.finish())
