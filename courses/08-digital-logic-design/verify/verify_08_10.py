#!/usr/bin/env python3
"""Verify every number in chapter 08-10 (timing, metastability, clock-domain crossing), solutions and lab.

Independent routes:
- timing numbers are computed by arrival-time arithmetic on each path, with skew and jitter applied as
  shifts of the capture edge;
- MTBF comes from the closed form e^(S/tau)/(T_W F_C F_D), cross-checked by numerically integrating
  the failure window over uniformly distributed data arrivals (the derivation of chapter 3.4-3.5);
- CDC counts are found by enumerating every possible sample of every changing bit;
- FIFO and handshake numbers from the problem data; lab numbers by re-running the notebook's
  computations (STA by topological propagation and by brute-force path enumeration).
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-10", COURSE / "chapters" / "08-10-timing-metastability-cdc.md",
                        COURSE / "solutions" / "08-10-solutions.md",
                        COURSE / "labs" / "08-10-lab" / "README.md")
YEAR = 365.25 * 24 * 3600


def setup_slack(Tc, tpcq, tpd, tsu, skew=0.0, jitter=0.0):
    """Required time at the capture edge (Tc + skew - jitter - tsu) minus arrival (tpcq + tpd)."""
    return (Tc + skew - jitter - tsu) - (tpcq + tpd)


def hold_slack(tccq, tcd, thold, skew=0.0):
    return (tccq + tcd) - (skew + thold)


def mtbf(S, tau, tw, fc, fd):
    return math.exp(S / tau) / (tw * fc * fd)


def mtbf_by_integration(S, tau, tw, fc, fd, n=400001):
    """Failure probability per data transition = P(|dt| < (tw/2) e^{-S/tau}) for dt uniform over a period."""
    Tc = 1 / fc
    dt = np.linspace(-Tc / 2, Tc / 2, n)
    unresolved = np.abs(dt) < (tw / 2) * math.exp(-S / tau)
    p_fail = np.trapezoid(unresolved.astype(float), dt) / Tc
    return 1 / (fd * p_fail) if p_fail > 0 else float("inf")


# the closed form agrees with the window integration where the window is resolvable on the grid
v.assert_true("MTBF closed form equals the integrated failure window (S = 20 to 60 ps)",
              all(abs(mtbf_by_integration(S, 20e-12, 20e-12, 1e9, 2e8) / mtbf(S, 20e-12, 20e-12, 1e9, 2e8) - 1) < 0.01
                  for S in (20e-12, 40e-12, 60e-12)))

# ================================================================= chapter
paths = {"400": 400, "320": 320, "150": 150}
tmin = max(50 + d + 30 for d in paths.values())
v.check("Ex 08-10.1a", tmin)
v.check("Ex 08-10.1b", 1e3 / tmin)
v.check("Ex 08-10.1c", setup_slack(500, 50, 400, 30))
v.check("Ex 08-10.1d", setup_slack(500, 50, 320, 30))
v.check("Ex 08-10.1e", setup_slack(500, 50, 150, 30))
v.check("Ex 08-10.2a", 50 + 400 + 30 - 40)
v.assert_true("at 440 ps with 40 ps skew the setup slack is zero", setup_slack(440, 50, 400, 30, skew=40) == 0)
v.check("Ex 08-10.2b", hold_slack(35, 25, 20))
v.check("Ex 08-10.2c", hold_slack(35, 25, 20, skew=40))
v.check("Ex 08-10.2d", hold_slack(35, 25, 20, skew=60))
v.check("Ex 08-10.2e", 50 + 400 + 30 + 15)


def pipeline(stages, overhead=80):
    Tc = max(stages) + overhead
    return Tc, 1e3 / Tc, len(stages) * Tc


Tc1, f1, lat1 = pipeline([900])
Tc3, f3, lat3 = pipeline([300, 300, 300])
v.check("Ex 08-10.3a", f1)
v.check("Ex 08-10.3b", lat1)
v.check("Ex 08-10.3c", f3)
v.check("Ex 08-10.3d", lat3)
v.check("Ex 08-10.3e", Tc1 / Tc3)
v.check("Ex 08-10.3f", pipeline([400, 300, 200])[1])

TW, FC, FD, TAU = 20e-12, 1e9, 200e6, 20e-12
S1 = (1000 - 50 - 400 - 30) * 1e-12
S2 = (1000 - 50 - 30) * 1e-12
m1 = mtbf(S1, TAU, TW, FC, FD)
v.check("Ex 08-10.4a", m1)
v.check("Ex 08-10.4b", m1 / 3600)
v.check("Ex 08-10.4c", mtbf(S2, TAU, TW, FC, FD) / YEAR)
v.check("Ex 08-10.4d", mtbf(2 * S2, TAU, TW, FC, FD) / YEAR)
m5 = mtbf(S2, 40e-12, TW, FC, FD)
v.check("Ex 08-10.5a", m5)
v.check("Ex 08-10.5b", m5 / 60)
n_ff = next(k for k in range(2, 10) if mtbf((k - 1) * S2, 40e-12, TW, FC, FD) >= mtbf(S2, TAU, TW, FC, FD) * 0.999)
v.check("Ex 08-10.5c", n_ff)
v.check("Ex 08-10.5d", mtbf((n_ff - 1) * S2, 40e-12, TW, FC, FD) / YEAR)


def samples(a, b, nbits):
    changed = [i for i in range(nbits) if ((a ^ b) >> i) & 1]
    out = set()
    for pick in itertools.product((0, 1), repeat=len(changed)):
        x = a
        for i, p in zip(changed, pick):
            if p:
                x ^= 1 << i
        out.add(x)
    return changed, out


def gray(x):
    return x ^ (x >> 1)


ch, sv = samples(7, 8, 4)
v.check("Ex 08-10.6a", len(ch))
v.check("Ex 08-10.6b", len(sv))
v.check("Ex 08-10.6c", max(abs(x - t) for x in sv for t in (7, 8)))   # largest distance from either correct value
v.check("Ex 08-10.6d", len(samples(gray(7), gray(8), 4)[1]))
v.assert_true("Gray 7 and 8 are 0100 and 1100", gray(7) == 0b0100 and gray(8) == 0b1100)
reads = 120 / 200e6 * 150e6
v.check("Ex 08-10.7a", reads)
v.check("Ex 08-10.7b", 120 - reads)
depth = 2 ** math.ceil(math.log2(120 - reads + 2))
v.check("Ex 08-10.7c", depth)
v.check("Ex 08-10.7d", int(math.log2(depth)))
v.check("Ex 08-10.7e", int(math.log2(depth)) + 1)

# ================================================================= solutions
v.check("08-10.1a", 1e3 / (60 + 520 + 40))
v.check("08-10.1b", setup_slack(1e3 / 1.5, 60, 520, 40))
v.check("08-10.1c", setup_slack(1e3 / 1.5, 60, 480, 40))
v.check("08-10.2a", hold_slack(30, 15, 25))
v.check("08-10.2b", hold_slack(30, 15, 25, skew=30))
v.check("08-10.3a", math.e)
v.check("08-10.3b", math.log(1e6))
v.check("08-10.4a", setup_slack(800, 50, 700, 40))
v.check("08-10.4b", setup_slack(800, 50, 700, 40, skew=-30))
v.check("08-10.4c", setup_slack(800, 50, 700, 40, jitter=25))
v.check("08-10.4d", 800 - 30 - 25 - 50 - 40)
for k, key in ((1, "08-10.5a"), (4, "08-10.5b"), (12, "08-10.5c")):
    v.check(key, 1e3 / (1200 / k + 100))
v.check("08-10.5d", 1e3 / 100)
v.check("08-10.5e", 4 * (1200 / 4 + 100))
v.check("08-10.5f", next(k for k in range(1, 50) if 1200 / k + 100 <= (1200 + 100) / 2))
v.check("08-10.6a", pipeline([500, 300, 400], 100)[1])
v.check("08-10.6b", pipeline([400, 400, 400], 100)[1])
Sst = (500 - 60 - 40) * 1e-12
args7 = (25e-12, 30e-12, 2e9, 50e6)
v.check("08-10.7a", mtbf(Sst, *args7))
v.check("08-10.7b", mtbf(2 * Sst, *args7) / YEAR)
v.check("08-10.7c", mtbf(3 * Sst, *args7) / YEAR)
v.check("08-10.7d", next(k for k in range(2, 12) if mtbf((k - 1) * Sst, *args7) >= 1000 * YEAR))
v.check("08-10.8a", 20 * math.log(1e4 * YEAR * 4e6))
ch3, sv3 = samples(3, 4, 3)
v.check("08-10.9a", len(ch3))
v.check("08-10.9b", len(sv3))
v.check("08-10.9c", max(abs(x - t) for x in sv3 for t in (3, 4)))
v.check("08-10.9d", len(samples(gray(3), gray(4), 3)[1]))
spacing = 2 * (1 / 100e6)
v.check("08-10.10a", spacing * 1e9)
v.check("08-10.10b", spacing / (1 / 400e6))
v.check("08-10.10c", 1 / spacing / 1e6)
t_hs = 2 * 3 / 80e6 + 2 * 3 / 100e6
v.check("08-10.11a", t_hs * 1e9)
v.check("08-10.11b", 1 / t_hs / 1e6)
v.check("08-10.11c", 32 / t_hs / 1e6)
r12 = math.floor(256 / 250e6 * 100e6)
v.check("08-10.12a", r12)
v.check("08-10.12b", 256 - r12)
d12 = 2 ** math.ceil(math.log2(256 - r12 + 3))
v.check("08-10.12c", d12)
v.check("08-10.12d", int(math.log2(d12)))
v.check("08-10.12e", int(math.log2(d12)) + 1)
v.check("08-10.12f", 256 / 3e-6 / 1e6)
v.check("08-10.13a", 1e9 / 2000)
v.check("08-10.13b", 5e6 * 2000 / 1e9)
tau14 = 100e-12 / math.log(1e5 / 100)
v.check("08-10.14a", tau14 * 1e12)
v.check("08-10.14b", 1e5 * math.exp(-600e-12 / tau14))
v.check("08-10.15a", 1e3 / (600 + 300 + 80))
v.check("08-10.15b", 1e3 / (300 + 80))

# ================================================================= lab
T_PCQ, T_SETUP = 50, 30
gates = {"g1": (40, ["R1", "R2"]), "g2": (60, ["g1", "R3"]), "g3": (45, ["g2", "g1"]), "g4": (20, ["R3"]),
         "g5": (55, ["g4", "g2"]), "g6": (70, ["g3", "g5"])}
launch, captures = ["R1", "R2", "R3"], {"R4": "g6", "R5": "g4"}
arr = {r: T_PCQ for r in launch}
for g, (d, ins) in gates.items():
    arr[g] = max(arr[i] for i in ins) + d


def all_paths(n):
    return [[n]] if n in launch else [p + [n] for i in gates[n][1] for p in all_paths(i)]


plist = [p for net in captures.values() for p in all_paths(net)]
pdel = [T_PCQ + sum(gates[g][0] for g in p[1:]) for p in plist]
crit = max(arr[n] for n in captures.values())
v.assert_true("topological STA equals brute-force path enumeration", crit == max(pdel))
v.check("Lab 08-10.a", crit)
v.check("Lab 08-10.b", 1e3 / (crit + T_SETUP))
v.check("Lab 08-10.c", 1e3 / 3 - T_SETUP - crit)
v.check("Lab 08-10.d", len(plist))
rng = np.random.default_rng(810)
dt = rng.uniform(-0.5e-9, 0.5e-9, 10_000_000)
ratio = np.abs(dt) / 10e-12
t_res = np.where(ratio >= 1, 0.0, 20e-12 * np.log(1 / np.maximum(ratio, 1e-300)))
tt = np.arange(20e-12, 160e-12, 10e-12)
frac = np.array([(t_res > x).mean() for x in tt])
slope, _ = np.polyfit(tt, np.log(frac), 1)
v.check("Lab 08-10.e", -1 / slope * 1e12)
lr = ((2000 - 80) - (1000 - 80)) / 20 / math.log(10) + math.log10(1e9 / 5e8)
v.check("Lab 08-10.f", lr)
imp_bin = sum(len(samples(c, (c + 1) % 16, 4)[1] - {c, (c + 1) % 16}) for c in range(16))
imp_gray = sum(len(samples(gray(c), gray((c + 1) % 16), 4)[1] - {gray(c), gray((c + 1) % 16)}) for c in range(16))
v.check("Lab 08-10.g", imp_bin)
v.check("Lab 08-10.h", imp_gray)
v.check("Lab 08-10.i", 16 + 3000)
v.check("Lab 08-10.j", 200)

# ---- Problem 16: reset synchronizer, simulated edge by edge
period, t_assert, t_release, recovery = 5.0, 1.0, 13.0, 0.3
ff, out_release = [0, 0], None
for edge in range(1, 10):
    t = edge * period
    if t_assert <= t < t_release:
        ff = [0, 0]                                     # held in reset (asynchronous clear)
        continue
    if t < t_assert:
        continue
    ff = [1, ff[0]]                                     # shift the tied-high 1 along
    if ff[1] == 1 and out_release is None:
        out_release = (edge, t)
edges_after = sum(1 for e in range(1, out_release[0] + 1) if e * period > t_release)
v.check("08-10.16a", t_assert)
v.check("08-10.16b", edges_after)
v.check("08-10.16c", out_release[1])
first_edge = math.ceil(t_release / period) * period
v.check("08-10.16d", first_edge - recovery - t_release)
v.finish()
