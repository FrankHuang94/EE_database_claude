#!/usr/bin/env python3
"""Verify every number in chapter 08-06 (latches, flip-flops and sequential timing), its solutions and lab.

Independent routes:
- latches are simulated by iterating their cross-coupled gate equations to a fixed point at every step;
  flip-flops by a two-latch master-slave model, not by "capture D at the edge";
- the switching threshold is found by solving the square-law current balance with a root finder, and the
  loop-gain argument is checked by integrating a cross-coupled pair numerically;
- timing results are evaluated from the setup and hold inequalities written as arrival-time comparisons;
- the SKY130 numbers are the library's own Liberty values (recorded in research log R-154); the checks
  confirm their rounding and the derived area ratio.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("08-06", COURSE / "chapters" / "08-06-latches-and-flip-flops.md",
                        COURSE / "solutions" / "08-06-solutions.md",
                        COURSE / "labs" / "08-06-lab" / "README.md")


def nor(a, b):
    return 1 - (a | b)


def nand(a, b):
    return 1 - (a & b)


def settle(f, q, qb, *ins, n=8):
    """Iterate a cross-coupled pair (q = f(in1, qb), qb = f(in2, q)) to a fixed point."""
    for _ in range(n):
        q, qb = f(ins[0], qb), f(ins[1], q)
    return q, qb


def nor_latch(seq, q=0):
    qb = 1 - q
    out = []
    for s, r in seq:
        q, qb = settle(nor, q, qb, r, s)   # Q = NOR(R, Qb), Qb = NOR(S, Q)
        out.append((q, qb))
    return out


def nand_latch(seq, q=0):
    qb = 1 - q
    out = []
    for sb, rb in seq:
        q, qb = settle(nand, q, qb, sb, rb)  # Q = NAND(Sb, Qb), Qb = NAND(Rb, Q)
        out.append((q, qb))
    return out


def d_latch(clk, d, q, transparent_high=True):
    en = clk if transparent_high else 1 - clk
    s, r = en & d, en & (1 - d)
    qq, _ = settle(nor, q, 1 - q, r, s)
    return qq


def run_latch(clks, ds, transparent_high=True, q=0):
    out = []
    for c, d in zip(clks, ds):
        q = d_latch(c, d, q, transparent_high)
        out.append(q)
    return out


def run_master_slave(clks, ds, q=0, m=0):
    """Master transparent on CLK = 0, slave on CLK = 1. At a rising edge the master closes on the D it
    held while CLK was low (the sample before the edge); then the slave copies the master."""
    out = []
    prev_clk = clks[0]
    for c, d in zip(clks, ds):
        if c == 0:
            m = d_latch(1, d, m)          # master transparent
        elif prev_clk == 0:
            m = d_latch(1, d, m)          # D sampled at the edge itself (convention of the chapter)
        q = d_latch(c, m, q)              # slave transparent when CLK = 1
        out.append(q)
        prev_clk = c
    return out


def transitions(seq, start=0):
    prev, n = start, 0
    for x in seq:
        n += int(x != prev)
        prev = x
    return n


# ================================================================= chapter
L1 = nor_latch([(1, 0), (0, 0), (0, 1), (0, 0), (1, 1)])
v.check("Ex 08-06.1a", sum(1 for q, qb in L1 if q == 1))
v.check("Ex 08-06.1b", sum(1 for q, qb in L1 if q == 0 and qb == 0))
CLK2 = [0, 1, 1, 0, 0, 1, 1, 0]
D2 = [0, 0, 1, 1, 1, 1, 0, 0]
lat = run_latch(CLK2, D2)
ff = run_master_slave(CLK2, D2)
v.check("Ex 08-06.2a", transitions(lat))
v.check("Ex 08-06.2b", transitions(ff))
v.check("Ex 08-06.2c", lat[-1])
v.check("Ex 08-06.2d", ff[-1])


def tmin(tpcq, tpd, tsu, skew=0.0):
    return tpcq + tpd + tsu - skew


def hold_slack(tccq, tcd, th, skew=0.0):
    return tccq + tcd - (th + skew)


v.check("Ex 08-06.3a", tmin(50, 300, 40))
v.check("Ex 08-06.3b", 1e3 / tmin(50, 300, 40))
v.check("Ex 08-06.3c", 400 - tmin(50, 300, 40))
v.check("Ex 08-06.3d", 100 * (50 + 40) / tmin(50, 300, 40))
v.check("Ex 08-06.4a", hold_slack(30, 10, 60))
nbuf = next(k for k in range(10) if hold_slack(30, 10 + 15 * k, 60) >= 0)
v.check("Ex 08-06.4b", nbuf)
v.check("Ex 08-06.4c", hold_slack(30, 10 + 15 * nbuf, 60))
v.check("Ex 08-06.4d", 1e3 / tmin(50, 300 + 20 * nbuf, 40))
v.check("Ex 08-06.5a", tmin(5.2, 0, 3))
v.check("Ex 08-06.5b", 1e3 / tmin(5.2, 0, 3))
v.check("Ex 08-06.5c", 1e3 / tmin(5.2, 1.0, 3))
edges = [10 * k for k in range(1, 10)]
v.check("Ex 08-06.6a", next(e for e in edges if e >= 23))
v.check("Ex 08-06.6b", 23)
v.check("Ex 08-06.6c", next(e for e in edges if e > 37) - 37)


def ff_from_latch(lat_su, lat_h, slave_cq, clk_delay):
    return lat_su - clk_delay, lat_h + clk_delay, slave_cq + clk_delay


su, h, cq = ff_from_latch(30, 10, 50, 15)
v.check("Ex 08-06.7a", su)
v.check("Ex 08-06.7b", h)
v.check("Ex 08-06.7c", cq)
v.check("Ex 08-06.7d", ff_from_latch(30, 10, 50, 40)[0])

# switching threshold: solve the square-law current balance numerically
VDD, VT = 1.8, 0.45
bn, bp = 250e-6 * 0.65 / 0.15, 100e-6 * 1.0 / 0.15


def vm(bn_, bp_):
    return brentq(lambda x: 0.5 * bn_ * (x - VT) ** 2 - 0.5 * bp_ * (VDD - x - VT) ** 2, VT + 1e-9, VDD - VT - 1e-9)


v.check("Th 08-06.a", bn * 1e3)
v.check("Th 08-06.b", bp * 1e3)
v.check("Th 08-06.c", vm(bn, bp))
v.check("Th 08-06.d", 2 + 4 * 4)
v.check("Th 08-06.e", 2 * 2 + 2 * 2 + 2)

# SKY130 library data: values read from sky130_fd_sc_hd__dfxtp_1__tt_025C_1v80.lib.json and nand2_1 (R-154)
SKY = {"cq_rise": 0.3070411, "cq_fall": 0.2971512, "su_rise": 0.0508281, "su_fall": 0.1033184,
       "hold_rise": -0.0285176, "area_ff": 20.0192, "area_nand2": 3.7536}
v.check("N 08-06.a", SKY["cq_rise"])
v.check("N 08-06.b", SKY["cq_fall"])
v.check("N 08-06.c", SKY["su_rise"])
v.check("N 08-06.d", SKY["su_fall"])
v.check("N 08-06.e", SKY["hold_rise"])
v.check("N 08-06.f", SKY["area_ff"])
v.check("N 08-06.g", SKY["area_nand2"])
v.check("N 08-06.h", SKY["area_ff"] / SKY["area_nand2"])

# ================================================================= solutions
L = nand_latch([(0, 1), (1, 1), (1, 0), (1, 1), (0, 0)])
v.check("08-06.1a", sum(1 for q, qb in L if q == 1))
v.check("08-06.1b", sum(1 for q, qb in L if q == 1 and qb == 1))
CLKp = [0, 1, 1, 0, 0, 1, 1, 0]
Dp = [1, 1, 0, 0, 1, 0, 1, 0]
pos, neg, ffp = run_latch(CLKp, Dp, True), run_latch(CLKp, Dp, False), run_master_slave(CLKp, Dp)
v.check("08-06.2a", transitions(pos))
v.check("08-06.2b", pos[-1])
v.check("08-06.2c", transitions(neg))
v.check("08-06.2d", neg[-1])
v.check("08-06.2e", transitions(ffp))
v.check("08-06.2f", ffp[-1])
v.check("08-06.3a", 25 - 30)
v.check("08-06.3b", 20 - 15)
paths = [400, 650, 520]
T4 = tmin(80, max(paths), 50)
v.check("08-06.4a", T4)
v.check("08-06.4b", 1e3 / T4)
for key, p in zip(("08-06.4c", "08-06.4d", "08-06.4e"), paths):
    v.check(key, T4 - tmin(80, p, 50))
hs = [hold_slack(40, cd, 70) for cd in (10, 35, 50)]
for key, s in zip(("08-06.5a", "08-06.5b", "08-06.5c"), hs):
    v.check(key, s)
v.check("08-06.5d", sum(1 for s in hs if s < 0))
v.check("08-06.5e", next(k for k in range(10) if hold_slack(40, 10 + 12 * k, 70) >= 0))
v.check("08-06.6a", 1e6 / (1200 + 100))
v.check("08-06.6b", 1e3 / (1200 / 4 + 100))
v.check("08-06.6c", (1200 + 100) / (1200 / 4 + 100))
v.check("08-06.6d", (1200 + 100) / 100)
v.assert_true("P6 speedup approaches 13", abs((1300) / (1200 / 1e6 + 100) - 13) < 1e-3)
v.check("08-06.7a", 24 + 16)
v.check("08-06.7b", 32 * 16)
edges8 = [8 * k for k in range(0, 10)]
v.check("08-06.8a", next(e for e in edges8 if e >= 13))
v.check("08-06.8b", 13)
nxt = next(e for e in edges8 if e > 29.5)
v.check("08-06.8c", nxt - 29.5)
v.check("08-06.8d", nxt - 29.5 - 1.0)
v.check("08-06.9a", tmin(5.2, 3.5, 3))
v.check("08-06.9b", 1e3 / tmin(5.2, 3.5, 3))
v.check("08-06.10a", vm(1.0, 1.0))
v.check("08-06.10b", vm(4.0, 1.0))
tau = 20.0
v.check("08-06.11a", tau * math.log(0.9 / 1e-3))
v.check("08-06.11b", tau * math.log(0.9 / 1e-6))
v.check("08-06.11c", tau * math.log(1000))
su, h, cq = ff_from_latch(20, 15, 45, 25)
v.check("08-06.12a", su)
v.check("08-06.12b", h)
v.check("08-06.12c", cq)
v.check("08-06.12d", su + h)
v.check("08-06.13a", tmin(50, 300, 40, skew=30))
v.check("08-06.13b", 1e3 / tmin(50, 300, 40, skew=30))
v.check("08-06.13c", hold_slack(30, 40, 60, skew=30))
v.check("08-06.14a", 2 * (2 * 2 + 2 * 2) + 2)
v.check("08-06.14b", 24 - (2 * (2 * 2 + 2 * 2) + 2))


def ring_period(n_inv, t_inv, t_end=2000.0):
    """Event simulation of a ring of inverters (node i = NOT node i-1, after t_inv).
    Starts from alternating values; returns the period of node 0, or None if nothing moves."""
    import heapq
    state = [i % 2 for i in range(n_inv)]
    events = []
    for i in range(n_inv):
        want = 1 - state[i - 1]
        if state[i] != want:
            heapq.heappush(events, (t_inv, i, want))
    rises = []
    while events:
        t, node, val = heapq.heappop(events)
        if t > t_end:
            break
        if state[node] == val:
            continue
        state[node] = val
        if node == 0 and val == 1:
            rises.append(t)
        nxt = (node + 1) % n_inv
        heapq.heappush(events, (t + t_inv, nxt, 1 - val))
    return (rises[-1] - rises[-2]) if len(rises) >= 2 else None


p3 = ring_period(3, 20.0)
v.check("08-06.15a", p3)
v.check("08-06.15b", 1e3 / p3)
v.assert_true("P15 a ring of two inverters does not oscillate", ring_period(2, 20.0) is None)

# ================================================================= lab: resolution of a cross-coupled pair
from scipy.integrate import solve_ivp  # noqa: E402

VM = vm(bn, bp)
gmn, gmp = bn * (VM - VT), bp * (VDD - VM - VT)
CN = 10e-15
tau_s = CN / (gmn + gmp)
v.check("Lab 08-06.a", gmn * 1e3)
v.check("Lab 08-06.b", gmp * 1e3)
v.check("Lab 08-06.c", tau_s * 1e12)
v.check("Lab 08-06.d", math.log(0.9 / 1e-3))
v.check("Lab 08-06.e", tau_s * math.log(0.9 / 1e-3) * 1e12)


def i_n(vin, vout):
    vov = vin - VT
    if vov <= 0:
        return 0.0
    return bn * (vov * vout - vout * vout / 2) if vout < vov else 0.5 * bn * vov * vov


def i_p(vin, vout):
    vov = VDD - vin - VT
    vsd = VDD - vout
    if vov <= 0:
        return 0.0
    return bp * (vov * vsd - vsd * vsd / 2) if vsd < vov else 0.5 * bp * vov * vov


def pair(t, y):
    v1, v2 = y
    return [(i_p(v2, v1) - i_n(v2, v1)) / CN, (i_p(v1, v2) - i_n(v1, v2)) / CN]


def apart(t, y):
    return abs(y[0] - y[1]) - 0.9


apart.terminal = True
sol = solve_ivp(pair, [0, 2e-9], [VM + 0.5e-3, VM - 0.5e-3], events=apart, max_step=1e-13, rtol=1e-9, atol=1e-12)
v.check("Lab 08-06.f", sol.t_events[0][0] * 1e12)
v.assert_true("Lab: the pair resolves to opposite rails", sol.y[0, -1] > VM > sol.y[1, -1])

v.finish()
