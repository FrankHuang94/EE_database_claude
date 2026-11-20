#!/usr/bin/env python3
"""Verify every number in chapter 14-01 and its problem set.

Independent routes:
- CPI and execution time by counting cycles over a generated instruction stream with the stated mix;
- Amdahl and Gustafson speedups by list-scheduling a serial phase and many equal parallel tasks on N
  workers and timing the result;
- capacitor-switching energy by integrating the RC charging current numerically (supply energy and
  resistor energy), which then scales to dynamic power and per-task energy;
- energy-optimal frequency and race-to-idle crossovers by numerical minimization and root finding;
- means computed directly from the benchmark data, with the reference-independence of the geometric
  mean checked by changing the reference.
"""
from __future__ import annotations

import heapq
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

ROOT = HERE.parent
v = Verifier.from_files("14-01", ROOT / "chapters" / "14-01-performance-power-iron-law.md",
                        ROOT / "solutions" / "14-01-solutions.md", ROOT / "labs" / "14-01-lab" / "README.md")


def stream_cycles(mix, n=100000, only=None):
    """Build a deterministic instruction stream with the given class fractions and count its cycles
    (all of them, or only those of class index `only`)."""
    stream = []
    for k, (frac, cpi) in enumerate(mix):
        stream += [(k, cpi)] * int(round(frac * n))
    assert len(stream) == n
    return sum(c for k, c in stream if only is None or k == only), len(stream)


def cpi_of(mix):
    cyc, n = stream_cycles(mix)
    return cyc / n


def makespan(serial, parallel, N, tasks_per_worker=50):
    """Serial phase, then the parallel work split into N*k equal tasks, list-scheduled on N workers."""
    M = N * tasks_per_worker
    task = parallel / M
    heap = [0.0] * N
    for _ in range(M):
        t = heapq.heappop(heap)
        heapq.heappush(heap, t + task)
    return serial + max(heap)


def amdahl_sim(p, N):
    return 1.0 / makespan(1 - p, p, N)


def amdahl_limit(p, N=4000):
    """Extrapolate 1/S, which is linear in 1/N, from simulated runs on N and 2N workers to 1/N -> 0."""
    inv1 = makespan(1 - p, p, N, tasks_per_worker=1)
    inv2 = makespan(1 - p, p, 2 * N, tasks_per_worker=1)
    return 1 / (2 * inv2 - inv1)


def switch_energy(C=1.0, V=1.0, R=1.0):
    """Charge C from 0 to V through R; return (supply energy, resistor energy) by integrating the current."""
    tau = R * C
    sol = solve_ivp(lambda t, q: [(V - q[0] / C) / R], (0, 40 * tau), [0.0], dense_output=True,
                    rtol=1e-12, atol=1e-15 * C * V)
    i = lambda t: (V - sol.sol(t)[0] / C) / R  # noqa: E731
    pts = [tau * k for k in (0.5, 1, 2, 5, 10)]
    E_sup = quad(lambda t: V * i(t), 0, 40 * tau, points=pts, limit=400)[0]
    E_res = quad(lambda t: i(t) ** 2 * R, 0, 40 * tau, points=pts, limit=400)[0]
    return E_sup, E_res


Es, Er = switch_energy()
v.assert_true("supply energy per charge is C V^2 (normalized)", abs(Es - 1) < 1e-8)
v.assert_true("resistor energy per charge is C V^2 / 2", abs(Er - 0.5) < 1e-8)
Es2, Er2 = switch_energy(R=37.0)
v.assert_true("energies independent of R", abs(Es2 - Es) < 1e-8 and abs(Er2 - Er) < 1e-8)


def p_dyn(aC, V, f):
    return switch_energy(aC, V, 1.0 / (aC * 1e12))[0] * f   # energy per cycle (C V^2) times cycles per second


# ---------------------------------------------------------------- Example 1
T_A = 2.5e9 * cpi_of([(1.0, 1.2)]) / 3e9
T_B = 2.0e9 * cpi_of([(1.0, 1.4)]) / 3e9
v.check("Ex 14-01.1a", T_A)
v.check("Ex 14-01.1b", T_B)
v.check("Ex 14-01.1c", T_A / T_B)
v.check("Ex 14-01.1d", 2.5e9 / T_A / 1e6)
v.check("Ex 14-01.1e", 2.0e9 / T_B / 1e6)

# ---------------------------------------------------------------- Example 2
mix2 = [(0.45, 1.0), (0.25, 2.5), (0.10, 1.0), (0.20, 1.8)]
cyc2, n2 = stream_cycles(mix2)
v.check("Ex 14-01.2a", cyc2 / n2)
v.check("Ex 14-01.2b", 100 * stream_cycles(mix2, only=1)[0] / cyc2)
mix2b = [(0.45, 1.0), (0.25, 1.6), (0.10, 1.0), (0.20, 1.8)]
v.check("Ex 14-01.2c", cpi_of(mix2b))
v.check("Ex 14-01.2d", cyc2 / stream_cycles(mix2b)[0])
pl = 0.25 * 2.5 / (cyc2 / n2)
v.assert_true("Amdahl agrees with the cycle count", abs(1 / ((1 - pl) + pl / (2.5 / 1.6)) - cyc2 / stream_cycles(mix2b)[0]) < 1e-12)

# ---------------------------------------------------------------- Example 3
v.check("Ex 14-01.3a", amdahl_sim(0.9, 16))
v.check("Ex 14-01.3b", amdahl_limit(0.9))
N80 = next(N for N in range(1, 1000) if amdahl_sim(0.9, N) >= 8 - 1e-9)
v.check("Ex 14-01.3c", N80)
run16 = makespan(0.1, 0.9 * 16, 16)                    # a scaled run: serial 10% of the 16-way time
v.check("Ex 14-01.3d", (0.1 + 0.9 * 16) / run16)

# ---------------------------------------------------------------- Example 4
P4 = p_dyn(1.5e-9, 0.9, 3.2e9)
v.check("Ex 14-01.4a", P4)
v.check("Ex 14-01.4b", P4 / 3.2e9 * 1e9)
v.check("Ex 14-01.4c", P4 + 1.2)

# ---------------------------------------------------------------- Example 5
P5 = p_dyn(1.5e-9, 0.75, 2.4e9)
v.check("Ex 14-01.5a", P5)
v.check("Ex 14-01.5b", P5 / P4)
Il = 1.2 / 0.9
Nc = 3.2e9
E_fast = P4 * (Nc / 3.2e9) + 1.2 * (Nc / 3.2e9)
t_slow = Nc / 2.4e9
E_slow = P5 * t_slow + Il * 0.75 * t_slow
v.check("Ex 14-01.5c", E_fast)
v.check("Ex 14-01.5d", P5 * t_slow)
v.check("Ex 14-01.5e", t_slow)
v.check("Ex 14-01.5f", E_slow)
v.check("Ex 14-01.5g", 100 * (1 - E_slow / E_fast))

# ---------------------------------------------------------------- Example 6
TA6, TB6 = np.array([1.0, 1000.0]), np.array([10.0, 100.0])
v.check("Ex 14-01.6a", TA6.sum() / TB6.sum())
v.check("Ex 14-01.6b", np.mean(TB6 / TA6))
v.assert_true("arithmetic mean contradicts itself", abs(np.mean(TA6 / TB6) - np.mean(TB6 / TA6)) < 1e-12)
gm = lambda x: float(np.exp(np.mean(np.log(x))))  # noqa: E731
v.check("Ex 14-01.6c", gm(TB6 / TA6))

# ---------------------------------------------------------------- simulation (switched capacitor)
v.check("Sim 14-01.a", p_dyn(1e-12, 1.0, 1e8) * 1e6)
v.check("Sim 14-01.b", switch_energy(1e-12, 1.0, 100.0)[1] * 1e12)

# ---------------------------------------------------------------- Problems
v.check("14-01.1a", 4e9 * cpi_of([(1.0, 0.8)]) / 4e9)
v.check("14-01.1b", 1 / cpi_of([(1.0, 0.8)]))
v.check("14-01.2a", 10 / 1.3)
v.check("14-01.2b", 10 / 7)
v.check("14-01.2c", (10 / 7 - 1) * 100)
mix3 = [(0.5, 1), (0.3, 3), (0.2, 2)]
c3, n3 = stream_cycles(mix3)
v.check("14-01.3a", c3 / n3)
v.check("14-01.3b", 100 * stream_cycles(mix3, only=1)[0] / c3)
v.check("14-01.4a", (1e9 * 1.0 / 3e9) / (1e9 * 1.3 / 4e9))


def enhance(parts):
    """parts: list of (time fraction, speedup); simulate by summing new part times."""
    return 1 / sum(t / s for t, s in parts)


v.check("14-01.5a", enhance([(0.6, 1), (0.4, 4)]))
v.check("14-01.5b", enhance([(0.4, 1), (0.6, 1.2)]))
v.check("14-01.6a", brentq(lambda s: enhance([(0.4, 1), (0.6, s)]) - 1.5, 1.01, 100, xtol=1e-14))
v.assert_true("2.5x is out of reach", enhance([(0.4, 1), (0.6, 1e12)]) < 2.5)
for N, ks, ke in ((8, "a", "b"), (64, "c", "d")):
    S = amdahl_sim(0.95, N)
    v.check(f"14-01.7{ks}", S)
    v.check(f"14-01.7{ke}", 100 * S / N)
v.check("14-01.7e", amdahl_limit(0.95))
times8 = np.array([1e9 / 100e6, 1e9 / 200e6, 1e9 / 400e6])
v.check("14-01.8a", times8.sum())
v.check("14-01.8b", 3e9 / times8.sum() / 1e6)
v.check("14-01.8c", np.mean([100, 200, 400]))
for key_p, key_e, V, f in (("a", "b", 0.8, 2.0e9), ("c", "d", 0.6, 1.5e9)):
    P = p_dyn(0.5e-9, V, f)
    v.check(f"14-01.9{key_p}", P)
    v.check(f"14-01.9{key_e}", P / f * 1e9)
v.check("14-01.9e", (p_dyn(0.5e-9, 0.6, 1.5e9) / 1.5e9) / (p_dyn(0.5e-9, 0.8, 2.0e9) / 2.0e9))
V10 = 1.0 * 2 / 3
v.check("14-01.10a", p_dyn(1e-9, V10, 2e9) / p_dyn(1e-9, 1.0, 3e9))
v.check("14-01.10b", (p_dyn(1e-9, V10, 2e9) / 2e9) / (p_dyn(1e-9, 1.0, 3e9) / 3e9))
v.check("14-01.10c", (1 / 2e9) / (1 / 3e9))


def task_energy(f_ghz, Ncyc=1e9, aC=1e-9, Ileak=0.5):
    V = 0.3 + 0.2 * f_ghz
    t = Ncyc / (f_ghz * 1e9)
    return p_dyn(aC, V, f_ghz * 1e9) * t + V * Ileak * t


grid = np.linspace(0.2, 4.0, 381)
f_coarse = grid[np.argmin([task_energy(g) for g in grid])]
opt = minimize_scalar(task_energy, bounds=(f_coarse - 0.05, f_coarse + 0.05), method="bounded",
                      options={"xatol": 1e-10})
v.check("14-01.11a", opt.x)
v.check("14-01.11b", 0.3 + 0.2 * opt.x)
v.check("14-01.11c", opt.fun)
v.check("14-01.11d", task_energy(3.0))
v.check("14-01.11e", 100 * (1 - opt.fun / task_energy(3.0)))


def race_minus_slow(PL, Psys=0.0):
    fast = P4 * 1.0 + PL * 1.0 + Psys * 1.0
    slow = P5 * t_slow + (PL / 0.9) * 0.75 * t_slow + Psys * t_slow
    return fast - slow


v.check("14-01.12a", brentq(lambda PL: race_minus_slow(PL), 0.1, 100, xtol=1e-12))
v.check("14-01.12b", brentq(lambda Ps: race_minus_slow(1.2, Ps), 0.0, 100, xtol=1e-12))
ref = np.array([100.0, 200.0, 400.0])
TA13, TB13 = np.array([20.0, 50.0, 200.0]), np.array([25.0, 40.0, 100.0])
gA, gB = gm(ref / TA13), gm(ref / TB13)
v.check("14-01.13a", gA)
v.check("14-01.13b", gB)
v.check("14-01.13c", gB / gA)
v.check("14-01.13d", TA13.sum() / TB13.sum())
aA, aB = np.mean(ref / TA13), np.mean(ref / TB13)
v.check("14-01.13e", aA)
v.check("14-01.13f", aB)
v.check("14-01.13g", aB / aA)
v.check("14-01.13h", np.mean(TA13 / TB13))
v.assert_true("geometric mean independent of the reference", abs(gm(TA13 / TB13) - gB / gA) < 1e-12)
run64 = makespan(0.05, 0.95 * 64, 64)                  # the 64-way run: 5% of its time serial
one = 0.05 + 0.95 * 64                                 # the same work on one processor
v.check("14-01.14a", one / run64)
s1 = 0.05 / one
v.check("14-01.14b", 100 * s1)
v.assert_true("Amdahl with the single-processor fraction gives the same speedup",
              abs(amdahl_sim(1 - s1, 64) - one / run64) < 1e-9)
v.check("14-01.14c", amdahl_sim(1 - s1, 128))
v.check("14-01.15a", 2 * 1)
v.check("14-01.15b", 1.2 * 1.5)
v.check("14-01.15c", 2 * 1**2)
v.check("14-01.15d", 1.2 * 1.5**2)
# slow A to 1.5 s: f falls by 1/1.5 and V with it (dynamic energy only), energy = C V^2 N scales by (1/1.5)^2
EA = 2.0
v.check("14-01.15e", EA * (p_dyn(1e-9, 1 / 1.5, 1e9) / p_dyn(1e-9, 1.0, 1e9)))

# ---------------------------------------------------------------- Lab
Ns = np.arange(1, 257)
T_ov = [makespan(0.01, 0.99, int(n), tasks_per_worker=1) + 1e-4 * n for n in Ns]
v.check("Lab 14-01.a", 1 / min(T_ov))
TAl = np.array([1.0, 1000.0, 50.0, 20.0, 5.0])
TBl = np.array([10.0, 100.0, 40.0, 25.0, 4.0])
R1 = np.array([2.0, 500.0, 100.0, 40.0, 10.0])
R2 = np.array([20.0, 50.0, 100.0, 40.0, 10.0])
v.check("Lab 14-01.b", TAl.sum() / TBl.sum())
v.check("Lab 14-01.c", np.mean(R1 / TBl) / np.mean(R1 / TAl))
v.check("Lab 14-01.d", np.mean(R2 / TBl) / np.mean(R2 / TAl))
v.check("Lab 14-01.e", gm(R1 / TBl) / gm(R1 / TAl))
v.assert_true("geometric-mean ratio identical for both references", abs(gm(R1 / TBl) / gm(R1 / TAl) - gm(R2 / TBl) / gm(R2 / TAl)) < 1e-12)

# Numbers to know: Horowitz's 45 nm table (R-208): one DRAM access (1.3-2.6 nJ) against a 32-bit add (0.1 pJ)
v.assert_true("a DRAM access costs more than 10,000 32-bit adds", min(1.3e-9, 2.6e-9) / 0.1e-12 > 1e4)

sys.exit(v.finish())
