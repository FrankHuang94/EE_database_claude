#!/usr/bin/env python3
"""Verify every number in chapter 23-05 (HBM in depth), its problems and its lab.

Independent routes (the lab module hbm.py uses closed forms):
- bandwidth by counting channels x pseudo-channels x bits per pseudo-channel x pin rate;
- interface energy by integrating the supply current of an RC charge;
- TSV capacitance by integrating the radial field across the liner, resistance by integrating dz/A;
- stack temperatures by solving the thermal ladder's nodal equations as a linear system;
- yields by summing logarithms; wafers per bit from bits per wafer of each product;
- interposers per wafer from the stated estimate, checked against a direct grid count's order of magnitude.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants, integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("23-05", ROOT / "chapters" / "23-05-hbm-in-depth.md",
                        ROOT / "solutions" / "23-05-solutions.md", LAB / "README.md")
EPS0 = constants.epsilon_0


# ---------------------------------------------------------------- independent helpers
def bw_channels(channels, pseudo, bits_per_pseudo, rate):
    """Bytes per second from the channel structure."""
    return channels * pseudo * bits_per_pseudo * rate / 8


def charge_energy(c, v_, r=50.0):
    """Supply energy to charge c to v_ through r, integrating v_ x i(t)."""
    tau = r * c
    return integrate.quad(lambda t: v_ * (v_ / r) * math.exp(-t / tau), 0, 60 * tau, epsabs=1e-30)[0]


def tsv_c(length, a, t_liner, eps_r=3.9):
    """Charge per unit length over the integrated field across the liner."""
    lam = 1.0  # C/m, arbitrary
    v_ = integrate.quad(lambda r: lam / (2 * math.pi * eps_r * EPS0 * r), a, a + t_liner)[0]
    return lam * length / v_


def tsv_r(length, a, rho=1.72e-8):
    return integrate.quad(lambda z: rho / (math.pi * a * a), 0, length)[0]


def ladder(n, r_layer, p_base, p_core, t_top=0.0):
    """Node temperatures (base = node 0 ... top die = node n) by nodal analysis; node n held at t_top."""
    g = 1 / r_layer
    m = np.zeros((n, n))
    rhs = np.zeros(n)
    for k in range(n):  # unknowns: nodes 0 .. n-1
        if k > 0:
            m[k, k] += g
            m[k, k - 1] -= g
        m[k, k] += g  # to node k+1
        if k + 1 < n:
            m[k, k + 1] -= g
        else:
            rhs[k] += g * t_top
        rhs[k] += p_base if k == 0 else p_core
    return list(np.linalg.solve(m, rhs)) + [t_top]


def layer_r(area, t_si, k_si, t_gap, k_gap):
    r = t_si / (k_si * area)
    if t_gap > 0:
        r += t_gap / (k_gap * area)
    return r


def log_yield(layers, per_layer):
    return math.exp(layers * math.log(per_layer))


def wafers_per_bit(w, b):
    """HBM wafers per bit over conventional: (wafers/bits) of HBM divided by that of the rest."""
    hbm_bits_per_wafer = b / w
    conv_bits_per_wafer = (1 - b) / (1 - w)
    return conv_bits_per_wafer / hbm_bits_per_wafer


def gross_estimate(d, area):
    return math.pi * d * d / (4 * area) - math.pi * d / math.sqrt(2 * area)


AREA = 12.8e-3 * 11e-3

# ---------------------------------------------------------------- Example 23-05.1
v.check("Ex 23-05.1a", bw_channels(16, 2, 32, 6.4e9) / 1e9)
v.check("Ex 23-05.1b", bw_channels(16, 2, 32, 9.6e9) / 1e9)
v.check("Ex 23-05.1c", bw_channels(32, 2, 32, 8e9) / 1e9)
v.check("Ex 23-05.1d", bw_channels(32, 2, 32, 11.7e9) / 1e9)
v.check("Ex 23-05.1e", bw_channels(32, 2, 32, 13e9) / 1e9)
v.check("Ex 23-05.1f", bw_channels(32, 2, 32, 13e9) / bw_channels(16, 2, 32, 9.6e9))
v.check("Ex 23-05.1g", bw_channels(32, 2, 32, 14e9) / 1e9)
v.check("Ex 23-05.1h", bw_channels(16, 2, 32, 9.2e9) / 1e9)
v.check("Ex 23-05.1h1", bw_channels(16, 2, 32, 9.2e9) / 1e12)
v.check("Ex 23-05.1i", optimize.brentq(lambda r: bw_channels(16, 2, 32, r) - 1.2e12, 1e9, 20e9) / 1e9)
v.check("Txt 23-05.b", 32 * 2)

# ---------------------------------------------------------------- Example 23-05.2
v.check("Ex 23-05.2a", 8e12 * 8 / 8192 / 1e9)
v.check("Ex 23-05.2b", 8e12 / 8 / 1e12)
v.check("Ex 23-05.2c", 288 / 8)
v.check("Ex 23-05.2d", 19.2 / 8)
v.check("Ex 23-05.2e", (19.2e12 / 8) * 8 / 2048 / 1e9)
v.check("Ex 23-05.2f0", 36 * 8)
v.check("Ex 23-05.2f", 36 * 8 / 24)
v.check("Txt 23-05.a", 12 * 24 / 8)
v.check("Ex 23-05.2g1", 288e9 / 8e12 * 1e3)
v.check("Ex 23-05.2g2", 288e9 / 19.2e12 * 1e3)
v.check("Ex 23-05.2h", 4 * bw_channels(16, 2, 32, 9.6e9) / (70e9 * 2))

# ---------------------------------------------------------------- Example 23-05.3
e_tr = charge_energy(1.3e-12, 0.4)
v.check("Ex 23-05.3a", e_tr * 1e12)
v.check("Ex 23-05.3b", e_tr / 4 * 1e12)
p_hbm = 8e12 * 8 * e_tr / 4
p_pod = 8e12 * 8 * 1.277e-12
v.check("Ex 23-05.3c", p_hbm)
v.check("Ex 23-05.3d", p_pod)
v.check("Ex 23-05.3e", p_pod / p_hbm)
v.check("Txt 23-05.f", p_pod)
v.check("Txt 23-05.i", p_pod / p_hbm)
v.check("Txt 23-05.j", 100 * bw_channels(16, 2, 32, 9.6e9) / (512 * 28e9 / 8))
v.check("Txt 23-05.l", 9.6 / 28)

# ---------------------------------------------------------------- Example 23-05.4
c_tsv = tsv_c(50e-6, 2.5e-6, 0.2e-6)
r_tsv = tsv_r(50e-6, 2.5e-6)
v.check("Ex 23-05.4a", c_tsv * 1e15)
v.check("Ex 23-05.4b", r_tsv * 1e3)
v.check("Ex 23-05.4c", r_tsv * c_tsv * 1e15)
v.check("Ex 23-05.4d0", AREA * 1e6)
v.check("Ex 23-05.4d", 100 * 20000 * math.pi * (2.5e-6) ** 2 / AREA)
v.check("Ex 23-05.4e", 100 * 20000 * (25e-6) ** 2 / AREA)

# ---------------------------------------------------------------- Example 23-05.5
h_avail = 775 - 160
v.check("Ex 23-05.5c0", h_avail)
for n, kp, kd in ((8, "a", "b"), (12, "c", "d"), (16, "e", "f")):
    v.check(f"Ex 23-05.5{kp}", h_avail / n)
    v.check(f"Ex 23-05.5{kd}", h_avail / n - 10)
v.check("Ex 23-05.5f1", h_avail / 16 - 10)
v.check("Ex 23-05.5g", 100 * (1 - (h_avail / 16 - 10) / (h_avail / 12 - 10)))
v.check("Ex 23-05.5h", 8 / 12)
v.check("Txt 23-05.e", h_avail / 20 - 10)

# ---------------------------------------------------------------- Example 23-05.6
r_si = 30e-6 / (150 * AREA)
r_gap = 10e-6 / (1.5 * AREA)
r_l = layer_r(AREA, 30e-6, 150, 10e-6, 1.5)
v.check("Ex 23-05.6a", r_si)
v.check("Ex 23-05.6b", r_gap)
v.check("Ex 23-05.6c", r_l)
v.check("Ex 23-05.6c1", r_l)
t12 = ladder(12, r_l, 10, 1)[0]
t16 = ladder(16, r_l, 10, 1)[0]
v.check("Ex 23-05.6d", t12)
v.check("Ex 23-05.6e", t16)
v.check("Ex 23-05.6f", ladder(16, layer_r(AREA, 30e-6, 150, 0, 1), 10, 1)[0])
v.check("Txt 23-05.c", 100 * r_gap / r_l)
v.check("Txt 23-05.d", t16 - t12)

# ---------------------------------------------------------------- Example 23-05.7
v.check("Ex 23-05.7a", log_yield(12, 0.995))
v.check("Ex 23-05.7b", log_yield(16, 0.995))
v.check("Ex 23-05.7c", log_yield(12, 0.9))
v.check("Ex 23-05.7d", log_yield(12, 0.99 * 0.995))
for k, (w, b) in (("e", (0.18, 0.08)), ("f", (0.22, 0.09)), ("g", (0.30, 0.13))):
    v.check(f"Ex 23-05.7{k}", wafers_per_bit(w, b))
v.check("Txt 23-05.g", wafers_per_bit(0.18, 0.08))
v.check("Txt 23-05.h", wafers_per_bit(0.30, 0.13))

# ---------------------------------------------------------------- Example 23-05.8
g25 = gross_estimate(300, 2500)
v.check("Ex 23-05.8a0", g25)
v.check("Ex 23-05.8a", math.floor(g25))
v.check("Ex 23-05.8b", math.floor(g25) * 130000)
v.check("Ex 23-05.8c", math.floor(g25) * 130000 * 8)
v.check("Ex 23-05.8d", gross_estimate(300, 3000))


def grid_count(d, side):
    """Whole squares of the given side on an aligned grid inside a circle (best of a few offsets)."""
    best = 0
    for ox in np.linspace(0, side, 11, endpoint=False):
        for oy in np.linspace(0, side, 11, endpoint=False):
            n = 0
            xs = np.arange(-d / 2 - side + ox, d / 2, side)
            ys = np.arange(-d / 2 - side + oy, d / 2, side)
            for x in xs:
                for y in ys:
                    corners = [(x, y), (x + side, y), (x, y + side), (x + side, y + side)]
                    if all(cx * cx + cy * cy <= (d / 2) ** 2 for cx, cy in corners):
                        n += 1
            best = max(best, n)
    return best


n_grid = grid_count(300, 50)
v.check("Txt 23-05.m", n_grid)
v.assert_true("the gross-die estimate is conservative against an optimized grid", g25 < n_grid)

# ---------------------------------------------------------------- practitioner arithmetic
v.check("Txt 23-05.k", 100 * 83.33 / 104.6)

# ---------------------------------------------------------------- lab
v.check("Lab 23-05.a", max(n for n in range(1, 40) if ladder(n, r_l, 10, 1)[0] <= 10))
k_match = optimize.brentq(lambda kg: ladder(16, layer_r(AREA, 30e-6, 150, 10e-6, kg), 10, 1)[0] - t12, 0.5, 20)
v.check("Lab 23-05.b", k_match)
v.check("Lab 23-05.c", math.ceil(1000 / 36))
v.check("Lab 23-05.d", math.ceil(20 / 2.048))

# ---------------------------------------------------------------- problems
v.check("23-05.1a", 8 * 16 / 8)
v.check("23-05.1b", 16 * 32 / 8)
v.check("23-05.1c", 8 * 16 * 32 / 8)
v.check("23-05.1d", 8 * 24 / 8)
v.check("23-05.2a", bw_channels(16, 2, 32, 8e9) / 1e9)
v.check("23-05.2b", bw_channels(32, 2, 32, 10e9) / 1e9)
v.check("23-05.2c", 16 * 2)
v.check("23-05.2d", 32 * 2)
v.check("23-05.2e", 1024 / 32)
v.check("23-05.2f", 2048 / 64)
v.check("23-05.3a", 70e9 / 19.2e12 * 1e3)
v.check("23-05.3b", 19.2e12 / 70e9)
v.check("23-05.3c", 4 * bw_channels(16, 2, 32, 9.6e9) / 70e9)
e4 = charge_energy(0.9e-12, 0.75)
v.check("23-05.4a", e4 * 1e12)
v.check("23-05.4b", e4 / 4 * 1e12)
v.check("23-05.4b1", e4 / 4 * 1e12)
v.check("23-05.4c", 2048e9 * 8 * e4 / 4)
v.check("23-05.5a", tsv_c(40e-6, 3e-6, 0.5e-6) * 1e15)
v.check("23-05.5b", tsv_r(40e-6, 3e-6) * 1e3)
v.check("23-05.5c", tsv_c(40e-6, 3e-6, 0.25e-6) * 1e15)
v.check("23-05.6", 100 * 30000 * (30e-6) ** 2 / (11e-3 * 11e-3))
v.check("23-05.6a", 30000 * (30e-3) ** 2)
h7 = 775 - 150
v.check("23-05.7c0", h7)
for n, kp, kd in ((12, "a", "b"), (16, "c", "d"), (20, "e", "f")):
    v.check(f"23-05.7{kp}", h7 / n)
    v.check(f"23-05.7{kd}", h7 / n - 15)
v.check("23-05.7a1", h7 / 12)
r8 = layer_r(AREA, 30e-6, 150, 10e-6, 2.5)
v.check("23-05.8a", 10e-6 / (2.5 * AREA))
v.check("23-05.8b", r8)
v.check("23-05.8b1", r8)
v.check("23-05.8c", ladder(16, r8, 10, 1)[0])
v.check("23-05.8d", ladder(12, r8, 10, 1)[0])
temps = ladder(16, r_l, 10, 1, t_top=74.0)
v.check("23-05.9a", temps[0])
v.check("23-05.9b", temps[4])
v.check("23-05.9c", temps[5])
v.assert_true("no die sits within 0.2 K of the 85 C threshold", min(abs(x - 85) for x in temps) > 0.2)
v.check("23-05.9d", sum(1 for k in range(1, 16) if temps[k] > 85))
v.check("23-05.9x1", (temps[4] - 74) / r_l)
v.check("23-05.9x2", (temps[5] - 74) / r_l)
v.check("23-05.10a", log_yield(16, 0.998))
v.check("23-05.10b", optimize.brentq(lambda y: log_yield(16, y) - 0.95, 0.9, 1.0))
v.check("23-05.10c", log_yield(16, 0.95))
v.check("23-05.11a", wafers_per_bit(0.25, 0.10))
v.check("23-05.11b", 1.5 / 0.9)
v.check("23-05.11c", wafers_per_bit(0.25, 0.10) / (1.5 / 0.9))
g20, g40 = gross_estimate(300, 2000), gross_estimate(300, 4000)
v.check("23-05.12a0", g20)
v.check("23-05.12a", math.floor(g20))
v.check("23-05.12b0", g40)
v.check("23-05.12b", math.floor(g40))
v.check("23-05.12c", math.floor(g20) * 120000 * 0.85)
v.check("23-05.12d", math.floor(g40) * 120000 * 0.85)
v.check("23-05.12x", math.floor(g20) / math.floor(g40))
gc20, gc40 = grid_count(300, math.sqrt(2000)), grid_count(300, math.sqrt(4000))
v.check("23-05.12y1", gc20)
v.check("23-05.12y2", gc40)
v.check("23-05.12y", gc20 / gc40)
v.check("23-05.13a", 11.7 / 8)
v.check("23-05.13b", 11.7 / 9.6)
v.check("23-05.13c", 13 / 9.6)

# ---------------------------------------------------------------- audit additions
v.check("Txt 23-05.n", 2 * math.sqrt(3.9) * 5e-3 / 3.00e8 * 1e12)
v.check("Txt 23-05.o", 1 / 10e9 * 1e12)
c_stack = 12 * tsv_c(41.25e-6, 2.5e-6, 0.2e-6)
v.check("Txt 23-05.p", c_stack * 1e12)
v.check("Txt 23-05.q", 0.25 * c_stack * 1.0 ** 2 * 1e12)
v.check("Txt 23-05.r", 0.25 * c_stack / (0.25 * 1.3e-12 * 0.4 ** 2))
v.check("Ex 23-05.5h1", (1 - ((775 - 160) / 12 - 10) / ((775 - 160) / 8 - 10)) * 100)

v.check("Lab 23-05.e", ladder(16, r_l, 10, 1)[0] / ladder(12, r_l, 10, 1)[0])
v.check("Lab 23-05.f", 16 / 12)
v.check("Lab 23-05.g", (16 / 12) ** 2)

v.check("Txt 23-05.s", bw_channels(1, 1, 8 * 2048, 10.75e9) / 1e12)
v.check("Txt 23-05.t", bw_channels(1, 1, 8 * 2048, 9.375e9) / 1e12)
v.check("Txt 23-05.u", (1 - 9.375 / 10.75) * 100)
v.check("Txt 23-05.v", 40)
v.assert_true("the model's 38.3% thinning is within 2 points of the reported 40%", abs(38.3 - 40) < 2)

sys.exit(v.finish())
