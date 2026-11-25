#!/usr/bin/env python3
"""Verify every number in chapter 23-03 (DRAM cells, arrays and refresh), its problems and its lab.

Independent routes (the lab module dramtech.py uses closed forms):
- charge sharing by integrating the two-capacitor RC circuit to steady state;
- bitline limits by root finding on the charge-sharing signal against cells per bitline;
- writes by integrating C dV/dt = I(V) with an independently written square-law current;
- the latch by integrating its coupled linear equations (estimate) and the full level-1 circuit (lab);
- latencies by stepping a bank's command timeline;
- activation energy by integrating the supply current of an RC bitline charge;
- weak cells by numerically integrating the lognormal density;
- PARA by the binomial probability of zero refreshes, and its p by root finding;
- array sigma by integrating the normal density and root finding.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants, integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("23-03", ROOT / "chapters" / "23-03-dram-cells-arrays-refresh.md",
                        ROOT / "solutions" / "23-03-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- independent helpers
def share(c_s, c_bl, v_cell, v_pre, r=1e4):
    """Bitline change after a cell and bitline share charge through r (integrated to steady state)."""
    def f(t, y):
        i = (y[0] - y[1]) / r
        return [-i / c_s, i / c_bl]
    tau = r * c_s * c_bl / (c_s + c_bl)
    sol = integrate.solve_ivp(f, (0, 60 * tau), [v_cell, v_pre], rtol=1e-12, atol=1e-15)
    return sol.y[1, -1] - v_pre


def i_n(k, vg, va, vb, vt):
    """Square-law n-channel current from terminal a to terminal b (either may act as source)."""
    if va < vb:
        return -i_n(k, vg, vb, va, vt)
    vov, vds = vg - vb - vt, va - vb
    if vov <= 0:
        return 0.0
    return 0.5 * k * vov * vov if vds >= vov else k * (vov * vds - 0.5 * vds * vds)


def i_p(k, vg, va, vb, vt):
    """Square-law p-channel current from terminal a to terminal b (vt is the threshold magnitude)."""
    return -i_n(k, -vg, -va, -vb, vt)


def write_ode(t_end, k, c, v_wl, v_th, v_bl):
    sol = integrate.solve_ivp(lambda t, y: [i_n(k, v_wl, v_bl, y[0], v_th) / c], (0, t_end), [0.0],
                              method="LSODA", rtol=1e-11, atol=1e-16)
    return sol.y[0, -1]


def q_inv(tail):
    """k with an upper-tail normal probability of `tail`, by integrating the density."""
    pdf = stats.norm.pdf
    return optimize.brentq(lambda k: integrate.quad(pdf, k, np.inf, epsabs=1e-30)[0] - tail, 0, 12, xtol=1e-12)


def sigma_array(n_bits, y=0.99):
    return q_inv(-math.log(y) / n_bits)


def lognormal_below(t_w, median, s_ln):
    """P(retention < t_w) by integrating the lognormal density in log time."""
    mu = math.log(median)
    f = lambda x: math.exp(-0.5 * ((x - mu) / s_ln) ** 2) / (s_ln * math.sqrt(2 * math.pi))  # noqa: E731
    return integrate.quad(f, mu - 40 * s_ln, math.log(t_w), epsabs=1e-30, epsrel=1e-12, limit=200)[0]


def latch_linear_time(tau, dv, v_final):
    """Time for the coupled latch equations C dv1/dt = -g v2, C dv2/dt = -g v1 to reach v1 - v2 = v_final."""
    ev = lambda t, y: (y[0] - y[1]) - v_final  # noqa: E731
    ev.terminal = True
    sol = integrate.solve_ivp(lambda t, y: [-y[1] / tau, -y[0] / tau], (0, 50 * tau), [dv / 2, -dv / 2],
                              events=ev, rtol=1e-12, atol=1e-15)
    return sol.t_events[0][0]


def bank_latency(state):
    """First-data time for a read, stepping the bank's commands: PRE (tRP), ACT (tRCD), RD (tCL)."""
    t_cl, t_rcd, t_rp = state["t"]
    t = 0.0
    if state["open"] is not None and state["open"] != state["row"]:
        t += t_rp
        state["open"] = None
    if state["open"] is None:
        t += t_rcd
        state["open"] = state["row"]
    return t + t_cl


def bitline_supply_energy(c, v, r=1e3):
    """Energy drawn from a supply at v while charging c from v/2 to v through r (integrated)."""
    tau = r * c
    i = lambda t: (v / 2) / r * math.exp(-t / tau)  # noqa: E731
    return v * integrate.quad(i, 0, 60 * tau, epsabs=1e-30)[0]


def para_miss(p, n):
    return stats.binom.pmf(0, n, p / 2)


def para_p(target, n):
    return optimize.brentq(lambda p: stats.binom.logpmf(0, n, p / 2) - math.log(target), 1e-9, 1.0, xtol=1e-14)


def pwl(t, t0, v0, v1, tr):
    if t <= t0:
        return v0
    if t >= t0 + tr:
        return v1
    return v0 + (v1 - v0) * (t - t0) / tr


def full_read(t_end):
    """Integrate the lab's Part C circuit: cell, two bitlines and a level-1 cross-coupled latch."""
    k_acc, kl, cs, cb = 20e-6, 100e-6, 8e-15, 40e-15

    def f(t, y):
        sn, bl, blb = y
        wl = pwl(t, 1e-9, 0.0, 1.8, 0.1e-9)
        nsrc = pwl(t, 5e-9, 0.5, 0.0, 0.2e-9)
        psrc = pwl(t, 5e-9, 0.5, 1.0, 0.2e-9)
        i_acc = i_n(k_acc, wl, bl, sn, 0.5)                     # bitline -> cell
        i_bl = i_p(kl, blb, psrc, bl, 0.3) - i_n(kl, blb, bl, nsrc, 0.3)
        i_blb = i_p(kl, bl, psrc, blb, 0.3) - i_n(kl, bl, blb, nsrc, 0.3)
        return [i_acc / cs, (i_bl - i_acc) / cb, i_blb / cb]

    ev = lambda t, y: (y[1] - y[2]) - 0.9  # noqa: E731
    ev.direction = 1
    sol = integrate.solve_ivp(f, (0, t_end), [1.0, 0.5, 0.5], method="LSODA", rtol=1e-10, atol=1e-13,
                              max_step=2e-12, events=ev)
    return sol


Q_E = constants.e
EPS0 = constants.epsilon_0

# ---------------------------------------------------------------- Example 23-03.1
d1 = share(8e-15, 40e-15, 1.0, 0.5)
v.check("Ex 23-03.1a", d1 * 1e3)
v.check("Ex 23-03.1b", d1 / 0.5)
v.check("Ex 23-03.1c0", 8e-15 * 1.0 * 1e15)
v.check("Ex 23-03.1c", 8e-15 * 1.0 / Q_E)
v.check("Txt 23-03.u", 8e-15 / Q_E)
v.check("Ex 23-03.1d", share(8e-15, 40e-15, 0.9, 0.5) * 1e3)
v.check("Ex 23-03.1e", share(8e-15, 40e-15, 0.0, 0.5) * 1e3)
v.check("Txt 23-03.t", (d1 - share(8e-15, 40e-15, 0.9, 0.5)) * 1e3)


# ---------------------------------------------------------------- Example 23-03.2
def n_max(c_s, v_sig, dv_min, c_b, c0):
    return optimize.brentq(lambda n: share(c_s, n * c_b + c0, v_sig, 0.0) - dv_min, 1, 5000, xtol=1e-9)


n8 = n_max(8e-15, 0.4, 0.06, 0.08e-15, 4e-15)
n6 = n_max(6e-15, 0.4, 0.06, 0.08e-15, 4e-15)
v.check("Ex 23-03.2a0", (n8 * 0.08 + 4))
v.check("Ex 23-03.2a", (n8 * 0.08 + 4))
v.check("Ex 23-03.2b", n8)
v.check("Ex 23-03.2c", (n6 * 0.08 + 4))
v.check("Ex 23-03.2cn", n6)
a_cell = 6 * 15.9e-3 ** 2  # µm²
v.check("Ex 23-03.2d0", a_cell)
a512, a256 = a_cell + 0.15 / 512, a_cell + 0.15 / 256
v.check("Ex 23-03.2d", a512)
v.check("Ex 23-03.2e", a256)
v.check("Ex 23-03.2f", 100 * (a256 / a512 - 1))

# ---------------------------------------------------------------- Example 23-03.3
K, CS = 20e-6, 8e-15
v.check("Ex 23-03.3a1", K / (2 * CS))
v.check("Ex 23-03.3a2", K * 10e-9 / (2 * CS))
v.check("Ex 23-03.3a", write_ode(10e-9, K, CS, 1.0, 0.5, 1.0))
v.check("Ex 23-03.3b", write_ode(1e-3, K, CS, 1.0, 0.5, 1.0))
v.check("Ex 23-03.3c1", 1.8 - 0.5 - 1.0)
v.check("Ex 23-03.3c2", 0.3 * K / CS)
v.check("Ex 23-03.3c3", CS / (0.3 * K) * 1e9)
v.check("Ex 23-03.3c4", 0.3 * K / CS * 10e-9)
v.check("Ex 23-03.3c5", 1.0 / (0.3 + 0.5) * math.exp(-0.3 * K / CS * 10e-9))
v.check("Ex 23-03.3c", (1.0 - write_ode(10e-9, K, CS, 1.8, 0.5, 1.0)) * 1e3)
v.check("Ex 23-03.3d", optimize.brentq(lambda w: write_ode(2e-6, K, CS, w, 0.5, 1.0) - 0.999, 1.2, 1.8, xtol=1e-6),
        tol=0.01)
v.assert_true("a wordline 10 mV below V_ARY + V_TH cannot reach 0.999 V even after 2 µs",
              write_ode(2e-6, K, CS, 1.49, 0.5, 1.0) < 0.991)

# ---------------------------------------------------------------- Example 23-03.4 and the lab's linear estimate
tau = 40e-15 / 40e-6
v.check("Ex 23-03.4a", tau * 1e9)
v.check("Ex 23-03.4b1", 1.0 / d1)
v.check("Ex 23-03.4b", latch_linear_time(tau, d1, 1.0) * 1e9)
d075 = share(8e-15, 40e-15, 0.75, 0.5)
v.check("Ex 23-03.4c", d075 * 1e3)
v.check("Ex 23-03.4d1", 1.0 / d075)
v.check("Ex 23-03.4d", latch_linear_time(tau, d075, 1.0) * 1e9)
v.check("Ex 23-03.4e", (latch_linear_time(tau, d1 / 2, 1.0) - latch_linear_time(tau, d1, 1.0)) * 1e9)
t_lin = latch_linear_time(tau, d1, 0.9)
v.check("Lab 23-03.d", t_lin * 1e9)

# ---------------------------------------------------------------- Example 23-03.5
bits = 32 * 65536 * (1024 * 8)
v.check("Ex 23-03.5a", bits)
v.assert_true("16 Gib = 2^34 bits", bits == 2 ** 34)
v.check("Ex 23-03.5b", 100 * (16 * 8) / (1024 * 8))
v.check("Ex 23-03.5c", 65536 // 8192)
v.check("Ex 23-03.5d", 131072 // 8192)
v.check("Ex 23-03.5e", bits / 66.26 / 1e9)
v.check("Ex 23-03.5e1", 16 / 66.26)
v.check("Ex 23-03.5f", 6 * 15.9 ** 2)
v.check("Ex 23-03.5f1", 6 * 15.9 ** 2)
cells_mm2 = bits * 6 * 15.9 ** 2 * 1e-12
v.check("Ex 23-03.5g", cells_mm2)
v.check("Ex 23-03.5h", 100 * cells_mm2 / 66.26)
v.check("Txt 23-03.r", 100 * (1 - cells_mm2 / 66.26))
v.check("Txt 23-03.f1", 100 * cells_mm2 * (1 + 8 / 128) / 66.26)
v.check("Ex 23-03.5i", 0.021 / a_cell)
v.check("Txt 23-03.o", bits / 66.26 / 38.1e6)
v.check("Txt 23-03.s", (1024 * 8) / (16 * 8))
v.assert_true("DDR4 16 Gb x16: 8 banks x 2^17 rows x 2 KB = 2^34", 8 * 131072 * 1024 * 16 == 2 ** 34)

# ---------------------------------------------------------------- Example 23-03.6
ddr4, ddr5 = (13.75, 13.75, 13.75), (16.0, 16.0, 16.0)
lat = {}
for name, tt in (("ddr4", ddr4), ("ddr5", ddr5)):
    hit = bank_latency({"t": tt, "open": 1, "row": 1})
    miss = bank_latency({"t": tt, "open": None, "row": 1})
    conf = bank_latency({"t": tt, "open": 2, "row": 1})
    lat[name] = (hit, miss, conf)
v.check("Ex 23-03.6a", lat["ddr4"][0])
v.check("Ex 23-03.6b", lat["ddr4"][1])
v.check("Ex 23-03.6c", lat["ddr4"][2])
avg4 = np.dot([0.6, 0.1, 0.3], lat["ddr4"])
avg5 = np.dot([0.6, 0.1, 0.3], lat["ddr5"])
v.check("Ex 23-03.6d", avg4)
v.check("Ex 23-03.6e", avg5)
v.check("Txt 23-03.n", 100 * (avg5 / avg4 - 1))
t_rc = 32 + 13.75
v.check("Txt 23-03.c", t_rc)
bw_bank = 64 / (t_rc * 1e-9)
v.check("Ex 23-03.6f", bw_bank / 1e9)
v.check("Ex 23-03.6g", 3200e6 * 8 / 1e9)
# Little's law route: requests in flight = throughput (lines/s) x service time
v.check("Ex 23-03.6h", (25.6e9 / 64) * t_rc * 1e-9)
h_star = optimize.brentq(lambda h: h * 13.75 + (1 - h) * 41.25 - 27.5, 0, 1)
v.check("Txt 23-03.e", h_star)

# ---------------------------------------------------------------- Example 23-03.7 and refresh text
refi4 = 64e-3 / 8192
v.check("Txt 23-03.a", refi4 * 1e6)
v.check("Txt 23-03.b", 32e-3 / 8192 * 1e6)
v.check("Ex 23-03.7a", 100 * 350e-9 / refi4)
v.check("Ex 23-03.7b", 100 * 350e-9 / (32e-3 / 8192))
v.check("Ex 23-03.7c", 100 * 160e-9 / refi4)
v.check("Txt 23-03.d", 350 / 160)
e_row = 8192 * bitline_supply_energy(40e-15, 1.0)
v.check("Ex 23-03.7d", e_row * 1e9)
rows_s = 16 * 131072 / 64e-3
v.check("Ex 23-03.7e1", rows_s)
v.check("Ex 23-03.7e", rows_s * e_row * 1e3)
v.check("Ex 23-03.7f", e_row / 128 * 1e12)
v.check("Ex 23-03.7g", e_row / 8192 * 1e12)

# ---------------------------------------------------------------- Example 23-03.8
i_leak = 8e-15 * 0.1 / 64e-3
v.check("Ex 23-03.8a", i_leak * 1e15)
v.assert_true("constant leakage of that size droops 0.1 V in exactly 64 ms",
              abs(integrate.quad(lambda t: i_leak / 8e-15, 0, 64e-3)[0] - 0.1) < 1e-12)
t_ret = 1.0
for _ in range(4):  # 45 -> 85 °C in 10 °C steps
    t_ret /= 2
v.check("Ex 23-03.8b", t_ret * 1e3)
v.check("Ex 23-03.8c", t_ret / 2 * 1e3)
v.check("Ex 23-03.8d1", math.log(0.064 / 10) / 1.0)
w64 = 2 ** 34 * lognormal_below(0.064, 10, 1.0)
w32 = 2 ** 34 * lognormal_below(0.032, 10, 1.0)
v.check("Ex 23-03.8d", w64)
v.check("Ex 23-03.8e", w32)
v.check("Txt 23-03.p", w64 / w32)
v.check("Lab 23-03.e", 1e3 * math.exp(optimize.brentq(
    lambda x: math.log(2 ** 34 * lognormal_below(math.exp(x), 10, 1.0)), math.log(1e-3), math.log(0.1))))
v.check("Lab 23-03.g", math.log(2) / 1.0)

# ---------------------------------------------------------------- Example 23-03.9 and row-hammer text
acts = 64e-3 / (t_rc * 1e-9)
v.check("Ex 23-03.9a", acts)
v.check("Ex 23-03.9b", 7812.5 / t_rc)
v.check("Ex 23-03.9c", 9600 * t_rc * 1e-9 * 1e3)
v.check("Txt 23-03.q", acts / 139e3)
v.check("Txt 23-03.l", 139 / 4.8)
pm = para_miss(0.001, 100000)
v.check("Ex 23-03.9d1", math.log(pm))
v.check("Ex 23-03.9d", pm)
v.check("Ex 23-03.9e1", 365 * 24 * 3600)
v.check("Ex 23-03.9e2", 365 * 24 * 3600 / 0.064)
v.check("Ex 23-03.9e", pm * 365 * 24 * 3600 / 0.064)
v.assert_true("Kim et al. Table 7 entries reproduce (1.9e-22, 9.4e-14; 1.4e-11, 6.8e-3)",
              round(pm, 23) == 1.9e-22 and abs(pm * 4.9275e8 - 9.4e-14) < 0.05e-14
              and abs(para_miss(0.001, 50000) - 1.4e-11) < 0.05e-11
              and abs(para_miss(0.001, 50000) * 4.9275e8 - 6.8e-3) < 0.05e-3)
v.check("Ex 23-03.9f", para_p(pm, 4800))
v.check("Ex 23-03.9g", para_p(pm, 1000))

# ---------------------------------------------------------------- remaining text values
v.check("Txt 23-03.f", sigma_array(2 ** 24))  # one sense amplifier per bitline pair
v.check("Txt 23-03.f2", 8 / 128 * 100)
v.check("Txt 23-03.f3", 2 * 4800)
v.check("Txt 23-03.f4", 550 / 7812.5 * 100)
v.check("Txt 23-03.f5", 550 / 3906.25 * 100)
area = 8e-15 * 6e-9 / (EPS0 * 25)
v.check("Txt 23-03.g", area * 1e12)
v.check("Txt 23-03.h", area * 1e12 / a_cell)
v.check("Txt 23-03.i", area / (math.pi * 30e-9) * 1e6)
v.check("Txt 23-03.j", 100 * (1 - 4 / 6))
v.check("Txt 23-03.k", 6 / 4)

# ---------------------------------------------------------------- lab: full circuit
v.check("Lab 23-03.a", write_ode(10e-9, K, CS, 1.5, 0.5, 1.0))
sol = full_read(40e-9)
t_cross = sol.t_events[0][0]
v.check("Lab 23-03.b", (t_cross - 5e-9) * 1e9)
v.check("Lab 23-03.c", sol.y[0, -1])
v.check("Txt 23-03.m", (t_cross - 5e-9) / t_lin)
v.assert_true("bitline difference just before sense enable equals the charge-sharing signal (0.1%)",
              abs((np.interp(5e-9, sol.t, sol.y[1]) - np.interp(5e-9, sol.t, sol.y[2])) - d1) < 1e-3 * d1)
v.check("Lab 23-03.f", para_miss(0.002, 2000))
v.check("Lab 23-03.h", math.sqrt(para_miss(0.002, 2000) * (1 - para_miss(0.002, 2000)) / 20000))

# ---------------------------------------------------------------- Problems
d = share(10e-15, 60e-15, 1.1, 0.55)
v.check("23-03.1a", d * 1e3)
v.check("23-03.1b", share(10e-15, 60e-15, 0.0, 0.55) * 1e3)
v.check("23-03.1c", d / 0.55)
v.check("23-03.1d0", 10 * 1.1)
v.check("23-03.1d", 11e-15 / Q_E)

v.check("23-03.2a", 2 ** 10 * 16)
v.check("23-03.2b", 8 * 131072 * 2 ** 10 * 16)
v.check("23-03.2c", 131072 // 8192)
v.check("23-03.2d0", 8 * 16)
v.check("23-03.2d", 100 * 8 * 16 / (2 ** 10 * 16))

v.check("23-03.3a", 32e-3 / 8192 * 1e6)
v.check("23-03.3b", 16e-3 / 8192 * 1e6)
v.check("23-03.3c", 100 * 295e-9 / (32e-3 / 8192))
v.check("23-03.3d", 100 * 295e-9 / (16e-3 / 8192))

n7 = n_max(7e-15, 0.40, 0.05, 0.07e-15, 3e-15)
n5 = n_max(5e-15, 0.40, 0.05, 0.07e-15, 3e-15)
v.check("23-03.4a0", 0.40 / 0.05)
v.check("23-03.4a", n7 * 0.07 + 3)
v.check("23-03.4b", n7)
v.check("23-03.4c", n5 * 0.07 + 3)
v.check("23-03.4cn", n5)
v.check("23-03.4d0", 512 * 0.07 + 3)
v.check("23-03.4d", 1e15 * optimize.brentq(
    lambda c: share(c, 512 * 0.07e-15 + 3e-15, 0.40, 0.0) - 0.05, 1e-15, 20e-15, xtol=1e-22))

v.check("23-03.5a", write_ode(1e-3, 25e-6, 6e-15, 1.1, 0.45, 1.1))
v.check("23-03.5b1", 25e-6 / 12e-15)
v.check("23-03.5b2", 25e-6 * 5e-9 / 12e-15)
v.check("23-03.5b", write_ode(5e-9, 25e-6, 6e-15, 1.1, 0.45, 1.1))
v.check("23-03.5c", 1e9 * optimize.brentq(lambda t: write_ode(t, 25e-6, 6e-15, 1.1, 0.45, 1.1) - 0.9 * 0.65,
                                          1e-10, 50e-9, xtol=1e-15))
v.check("23-03.5d", 1.1 + 0.45)

tau6 = 50e-15 / 25e-6
v.check("23-03.6a", tau6 * 1e9)
t60 = latch_linear_time(tau6, 0.06, 1.0)
v.check("23-03.6b", t60 * 1e9)
v.check("23-03.6c0", 1.0 / 0.06)
tau_need = optimize.brentq(lambda tt: latch_linear_time(tt, 0.06, 1.0) - 3e-9, 0.1e-9, 5e-9, xtol=1e-16)
v.check("23-03.6c1", tau_need * 1e9)
v.check("23-03.6c", 50e-15 / tau_need * 1e6)
t30 = latch_linear_time(tau6, 0.03, 1.0)
v.check("23-03.6d", t30 * 1e9)
v.check("23-03.6e0", math.log(2))
v.check("23-03.6e", (t30 - t60) * 1e9)

l5 = lat["ddr5"]
v.check("23-03.7a", l5[0])
v.check("23-03.7b", l5[1])
v.check("23-03.7c", l5[2])
v.check("23-03.7d", np.dot([0.4, 0.2, 0.4], l5))
v.check("23-03.7e", optimize.brentq(lambda h: h * l5[0] + (1 - h) * l5[2] - l5[1], 0, 1))

trc5 = 32 + 16
v.check("23-03.8a0", trc5)
bw5 = 64 / (trc5 * 1e-9)
v.check("23-03.8a", bw5 / 1e9)
v.check("23-03.8b", 6400e6 * 4 / 1e9)
v.check("23-03.8c", 25.6e9 / bw5)
v.check("23-03.8d", (25.6e9 / 64) * 48e-9)

i9 = 6e-15 * 0.15 / 32e-3
v.check("23-03.9a", i9 * 1e15)
i25 = i9
for _ in range(7):
    i25 /= 2
v.check("23-03.9b", i25 * 1e15)
v.check("23-03.9c", 6e-15 * 0.15 / i25)
v.check("23-03.9d1", math.log(0.032 / 2) / 0.8)
v.check("23-03.9d", 2 ** 34 * lognormal_below(0.032, 2, 0.8))
v.check("23-03.9e", 2 ** 34 * lognormal_below(0.016, 2, 0.8))

e10 = 8192 * bitline_supply_energy(35e-15, 1.1)
rows10 = 32 * 65536
v.check("23-03.10a", e10 * 1e9)
v.check("23-03.10b0", rows10)
v.check("23-03.10b1", rows10 / 32e-3)
v.check("23-03.10b", rows10 / 32e-3 * e10 * 1e3)
v.check("23-03.10c", rows10 / 16e-3 * e10 * 1e3)
v.check("23-03.10d", e10 / 128 * 1e12)

v.check("23-03.11a", 32e-3 / 48e-9)
v.check("23-03.11b", 3906.25 / 48)
v.check("23-03.11c", 9600 * 48e-9 * 1e3)
v.check("23-03.11d0", math.log(1e-15))
v.check("23-03.11d", para_p(1e-15, 4800))
v.check("23-03.11e", para_p(1e-15, 1000))

b12, k12, c12 = 2.0 - 0.5 - 1.1, 20e-6, 8e-15
v.check("23-03.12a0", b12)
v.check("23-03.12a1", b12 * k12 / c12)
v.check("23-03.12a2", 1.1 / (b12 + 0.55))
v.check("23-03.12a3", 1.1 / (b12 + 0.55) * math.exp(-b12 * k12 / c12 * 5e-9))
v.check("23-03.12a", (1.1 - write_ode(5e-9, k12, c12, 2.0, 0.5, 1.1)) * 1e3)
v.check("23-03.12b1", (1.1 / (b12 + 0.55)) / (1e-3 / (b12 + 0.5e-3)))
v.check("23-03.12b", 1e9 * optimize.brentq(lambda t: (1.1 - write_ode(t, k12, c12, 2.0, 0.5, 1.1)) - 1e-3,
                                           1e-9, 20e-9, xtol=1e-14))

a13 = 6e-15 * 6e-9 / (EPS0 * 25)
v.check("23-03.13a", a13 * 1e12)
h13 = a13 / (math.pi * 25e-9)
v.check("23-03.13b", h13 * 1e6)
v.check("23-03.13c", h13 / 25e-9)
v.check("23-03.13d", h13 / 2 * 1e6)
v.check("23-03.13e", optimize.brentq(lambda er: EPS0 * er * 2 * math.pi * 25e-9 * 1.0e-6 / 6e-9 - 6e-15, 1, 100))
v.check("23-03.13f", 6e-15 * 5e-9 / (EPS0 * 25) / (math.pi * 25e-9) * 1e6)

k25, k26 = sigma_array(2 ** 25), sigma_array(2 ** 26)
s512 = share(8e-15, 512 * 0.08e-15 + 4e-15, 0.25, 0.0)
s256 = share(8e-15, 256 * 0.08e-15 + 4e-15, 0.25, 0.0)
v.check("23-03.14a", k25)
v.check("23-03.14b0", 512 * 0.08 + 4)
v.check("23-03.14b", s512 * 1e3)
v.check("23-03.14c", s512 / k25 * 1e3)
v.check("23-03.14d", k26)
v.check("23-03.14e0", 256 * 0.08 + 4)
v.check("23-03.14e", s256 * 1e3)
v.check("23-03.14f", s256 / k26 * 1e3)
v.check("23-03.14g", k26 - k25)
v.check("23-03.14h", 100 * (s256 / s512 - 1))

sys.exit(v.finish())
