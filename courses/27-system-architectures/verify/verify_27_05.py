#!/usr/bin/env python3
"""Verify every number in chapter 27-05 (the PC SoC), its problems and its lab.

Independent routes (the lab module uses closed forms):
- residency power by simulating a long random state sequence with the given residencies;
- turbo durations by stepping the discrete EWMA of package power until it reaches P1;
- decode bounds by counting bytes read per token, prefill by counting operations;
- dies per wafer by counting whole die sites inside the wafer on a grid, not by formula, checked
  against 25-04's formula, and yields by Poisson;
- link and I/O power from bits per second times energy per bit.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "27-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import pcsoc as pc  # noqa: E402

v = Verifier.from_files("27-05", ROOT / "chapters" / "27-05-pc-soc.md",
                        ROOT / "solutions" / "27-05-solutions.md", LAB / "README.md")


def residency_sim(states, n=200_000, seed=1):
    """Average power from a random sequence of n time slots drawn with the residencies;
    the exact expectation is returned alongside for a tolerance check."""
    rng = np.random.default_rng(seed)
    fr = np.array([s[0] for s in states])
    pw = np.array([s[1] for s in states])
    idx = rng.choice(len(states), size=n, p=fr / fr.sum())
    sim = pw[idx].mean()
    exact = float(np.dot(fr, pw))
    assert abs(sim - exact) < 0.02 * max(exact, 0.1)
    return exact


def turbo_steps(pl1, pl2, tau, p0, dt=1e-4):
    """Step the EWMA y += a (P2 - y) until it reaches P1; return elapsed time."""
    a = 1 - math.exp(-dt / tau)
    y, t = p0, 0.0
    while y < pl1:
        y += a * (pl2 - y)
        t += dt
    return t


def decay_steps(start, end, p_idle, tau, dt=1e-3):
    a = 1 - math.exp(-dt / tau)
    y, t = start, 0.0
    while y > end:
        y += a * (p_idle - y)
        t += dt
    return t


def bw(bus, mt):
    return bus / 8 * mt * 1e6 / 1e9


def tokens_per_s(bw_gbs, params_b, bits):
    bytes_per_token = params_b * 1e9 * bits / 8
    return bw_gbs * 1e9 / bytes_per_token


def gross_dies_grid(area_mm2, wafer=300.0):
    """Gross dies per wafer (25-04 formula), checked against a square-die site count on a grid."""
    formula = math.floor(math.pi * wafer ** 2 / (4 * area_mm2) - math.pi * wafer / math.sqrt(2 * area_mm2))
    s = math.sqrt(area_mm2)
    r = wafer / 2
    best = 0
    for ox in np.linspace(0, s, 8, endpoint=False):
        for oy in np.linspace(0, s, 8, endpoint=False):
            xs = np.arange(-r - s + ox, r + s, s)
            ys = np.arange(-r - s + oy, r + s, s)
            X, Y = np.meshgrid(xs, ys)
            corners = [np.hypot(X + dx, Y + dy) for dx in (0, s) for dy in (0, s)]
            inside = np.all(np.stack(corners) <= r, axis=0)
            best = max(best, int(inside.sum()))
    assert abs(best - formula) <= 0.12 * formula, (best, formula)
    return formula


def good_die_cost(area, wafer_cost, d0):
    return wafer_cost / (gross_dies_grid(area) * math.exp(-area / 100 * d0))


# ---------------------------------------------------------------------------
# Example 27-05.1
# ---------------------------------------------------------------------------
v.check("Ex 27-05.1a1", 0.08 * 5.0)
v.check("Ex 27-05.1a2", 0.22 * 1.2)
v.check("Ex 27-05.1a3", 0.70 * 0.25)
soc = residency_sim([(0.08, 5.0), (0.22, 1.2), (0.70, 0.25)])
plat = 1.8 + 0.3 + 0.1 + 0.2 + 0.6
v.check("Ex 27-05.1a", soc)
v.check("Ex 27-05.1b", soc + plat)
life = 70 / (soc + plat)
v.check("Ex 27-05.1b1", life)
v.check("Ex 27-05.1c", 100 * soc / (soc + plat))
v.check("Ex 27-05.1c1", 100 * 1.8 / (soc + plat))
soc2 = residency_sim([(0.08, 5.0), (0.92, 1.2)])
v.check("Ex 27-05.1d", soc2)
v.check("Ex 27-05.1d1", soc2 + plat)
life2 = 70 / (soc2 + plat)
v.check("Ex 27-05.1d2", life2)
v.check("Ex 27-05.1d3", life - life2)
v.check("Ex 27-05.1d4", 100 * (life - life2) / life)

# ---------------------------------------------------------------------------
# Example 27-05.2
# ---------------------------------------------------------------------------
v.check("Ex 27-05.2a", turbo_steps(28, 64, 28, 5))
v.check("Ex 27-05.2b", turbo_steps(28, 64, 28, 20))
spd = (64 / 28) ** (1 / 3)
v.check("Ex 27-05.2c", spd)
v.check("Ex 27-05.2c1", 64 / 28)
v.check("Ex 27-05.2c2", 100 * (spd - 1))
v.assert_true("lab turbo formula agrees", abs(pc.turbo_seconds(28, 64, 28, 5) - turbo_steps(28, 64, 28, 5)) < 1e-3)

# ---------------------------------------------------------------------------
# Example 27-05.3
# ---------------------------------------------------------------------------
bwa, bwb = bw(128, 8533), bw(256, 8000)
v.check("Ex 27-05.3a", bwa)
v.check("Ex 27-05.3a1", bwb)
v.check("Txt 27-05.1", bwa)
v.check("Txt 27-05.2", bwb)
v.check("Ex 27-05.3b", 70e9 * 4 / 8 / 1e9)
v.check("Ex 27-05.3b1", tokens_per_s(bwa, 70, 4))
v.check("Ex 27-05.3b2", tokens_per_s(bwb, 70, 4))
v.check("Ex 27-05.3c0", 8e9 * 4 / 8 / 1e9)
v.check("Ex 27-05.3c", tokens_per_s(bwb, 8, 4))
v.check("Ex 27-05.3c1", tokens_per_s(448, 8, 4))
ops = 2 * 70e9 * 1000
v.check("Ex 27-05.3d", ops / (50e12 * 0.4))

# ---------------------------------------------------------------------------
# Example 27-05.4
# ---------------------------------------------------------------------------
work = 30 * 12e9
v.check("Ex 27-05.4a", work / 1e9)
npu = work / 6e12
gpu_work = work / 1.5e12
gpu = gpu_work + 0.5
cpu = work / 0.3e12
v.check("Ex 27-05.4b", npu)
v.check("Ex 27-05.4b1", 100 * npu * 1 / 70)
v.check("Ex 27-05.4c0", gpu_work)
v.check("Ex 27-05.4c", gpu)
v.check("Ex 27-05.4c1", 100 * gpu / 70)
v.check("Ex 27-05.4d", cpu)
v.check("Ex 27-05.4d1", 100 * cpu / 70)

# ---------------------------------------------------------------------------
# Example 27-05.5
# ---------------------------------------------------------------------------
v.check("Ex 27-05.5a", gross_dies_grid(240))
v.check("Ex 27-05.5a3", 240 / 100)
v.check("Ex 27-05.5a0", 240 / 100 * 0.10)
v.check("Ex 27-05.5a1", math.exp(-0.24))
mono = good_die_cost(240, 18500, 0.10)
v.check("Ex 27-05.5a2", mono)
v.check("Ex 27-05.5b", gross_dies_grid(100))
v.check("Ex 27-05.5b1", math.exp(-0.10))
c1 = good_die_cost(100, 18500, 0.10)
v.check("Ex 27-05.5b2", c1)
v.check("Ex 27-05.5b3", gross_dies_grid(160))
v.check("Ex 27-05.5b4", math.exp(-1.6 * 0.07))
c2 = good_die_cost(160, 9346, 0.07)
v.check("Ex 27-05.5b5", c2)
tiled = (c1 + c2 + 6) / 0.98
v.check("Ex 27-05.5b6", tiled)
v.check("Ex 27-05.5c", tiled / mono)
v.check("Ex 27-05.5c1", 100 * (1 - tiled / mono))
v.check("Ex 27-05.5d", (c1 + good_die_cost(160, 18500, 0.10) + 6) / 0.98)
v.check("Ex 27-05.5e", 200e9 * 8 * 0.5e-12)
v.check("Ex 27-05.5e1", 200e9 * 8 * 0.05e-12)
v.assert_true("lab chiplet_cost agrees",
              abs(pc.chiplet_cost([(100, 18500, 0.1), (160, 9346, 0.07)], 6, 0.98) - tiled) < 1e-9)

# ---------------------------------------------------------------------------
# Example 27-05.6
# ---------------------------------------------------------------------------
for k, bwg in [("a", 60), ("b", 2)]:
    off = bwg * 1e9 * 8 * 6e-12
    on = bwg * 1e9 * 8 * 4e-12
    v.check(f"Ex 27-05.6{k}", off)
    v.check(f"Ex 27-05.6{k}1", on)
    v.check(f"Ex 27-05.6{k}2", off - on)
v.check("Ex 27-05.6b3", 100 * (2e9 * 8 * 2e-12) / (soc + plat))

# ---------------------------------------------------------------------------
# Solutions
# ---------------------------------------------------------------------------
v.check("27-05.2a", bw(128, 9600))
v.check("27-05.2b", bw(512, 8533))
s3 = residency_sim([(0.05, 6.0), (0.15, 1.5), (0.80, 0.30)])
v.check("27-05.3a", s3)
v.check("27-05.3b", s3 + 2.5)
v.check("27-05.3c", 60 / (s3 + 2.5))
v.check("27-05.4a", turbo_steps(45, 115, 56, 10))
v.check("27-05.4b", decay_steps(45, 10, 5, 56))
v.check("27-05.5a", 24e9 / (4 / 8) / 1e9)
v.check("27-05.5b", 24e9 / (8 / 8) / 1e9)
v.check("27-05.5c", 32e9 * 4 / 8 / 1e9)
v.check("27-05.5d", tokens_per_s(136.5, 32, 4))
pf = 2 * 8e9 * 2000 / (40e12 * 0.5)
dec_rate = tokens_per_s(136.5, 8, 4)
v.check("27-05.6a", pf)
v.check("27-05.6b", dec_rate)
v.check("27-05.6c", 500 / dec_rate)
v.check("27-05.6d", pf + 500 / dec_rate)
tn = 5e13 / (40e12 * 0.5)
en = 5e13 / 6e12
tg = 5e13 / (120e12 * 0.6)
eg_work = 5e13 / 1.5e12
eg = eg_work + 0.5 * tg
v.check("27-05.7a", tn)
v.check("27-05.7b", en)
v.check("27-05.7c", tg)
v.check("27-05.7d", eg_work)
v.check("27-05.7e", eg)
v.check("27-05.7f", tn / tg)
v.check("27-05.7g", eg / en)
v.check("27-05.8a", gross_dies_grid(400))
v.check("27-05.8b", math.exp(-0.40))
m8 = good_die_cost(400, 18500, 0.10)
v.check("27-05.8c", m8)
v.check("27-05.8d", gross_dies_grid(200))
v.check("27-05.8e", math.exp(-0.20))
t8 = good_die_cost(200, 18500, 0.10)
v.check("27-05.8f", t8)
p8 = (2 * t8 + 10) / 0.97
v.check("27-05.8g", p8)
v.check("27-05.8h", p8 / m8)
v.check("27-05.8i", 100 * (1 - p8 / m8))
v.check("27-05.9", 1.0 / (1e12 * 8) * 1e12)
v.check("27-05.10", 1.0 / (8 * 2e-12) / 1e9)
allowed = 70 / 20 - 2.7
v.check("27-05.11a", allowed)
x = optimize.brentq(lambda r: 0.08 * 5.0 + (0.92 - r) * 1.2 + r * 0.25 - allowed, 0, 0.92)
v.check("27-05.11b", x)
v.check("27-05.11c", 100 * x)
v.check("27-05.11d", 0.08 * 5.0 + 0.92 * 1.2 - allowed)
t_turbo = turbo_steps(28, 64, 28, 5)
v.check("27-05.12d", spd)
done = t_turbo * spd
v.check("27-05.12a", done)
v.check("27-05.12e", 60 - done)
total = t_turbo + (60 - done)
v.check("27-05.12b", total)
v.check("27-05.12c", 100 * (60 - total) / 60)
v.check("27-05.12f", 100 * (60 / total - 1))

# Problem 27-05.13: integrate the averaging ODE numerically until y reaches P1
from scipy.integrate import solve_ivp  # noqa: E402

ev = lambda t, y: y[0] - 28.0  # noqa: E731
ev.terminal = True
sol13 = solve_ivp(lambda t, y: [(64.0 - y[0]) / 28.0], (0, 100), [25.0], events=ev, rtol=1e-11, atol=1e-11)
t13 = sol13.t_events[0][0]
v.check("27-05.13a", t13)
v.check("27-05.13b", 28 * 3 / 36)
v.check("27-05.13c", 100 * (28 * 3 / 36 / t13 - 1))

# ---------------------------------------------------------------------------
# Lab
# ---------------------------------------------------------------------------
sa = residency_sim([(0.08, 5.0), (0.07, 1.2), (0.85, 0.25)])
v.check("Lab 27-05.a", sa)
v.check("Lab 27-05.a1", 70 / (sa + plat))
v.check("Lab 27-05.b", turbo_steps(28, 64, 56, 5))
v.check("Lab 27-05.c", 256 / (10 * 0.5))
first = next(A for A in range(100, 600)
             if (2 * good_die_cost(A / 2, 18500, 0.1) + 10) / 0.97 < good_die_cost(A, 18500, 0.1))
v.check("Lab 27-05.d", first)

v.check("Txt 27-05.3", 72.4 / 24)
v.check("Txt 27-05.4", 72.4 / 24)
v.check("Txt 27-05.5", tokens_per_s(256, 128, 4))

sys.exit(v.finish())
