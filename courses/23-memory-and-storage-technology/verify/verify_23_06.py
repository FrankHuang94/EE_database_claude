#!/usr/bin/env python3
"""Verify every number in chapter 23-06 (NAND flash and 3D NAND), its problems and its lab.

Independent routes (the lab module nand.py uses closed forms):
- threshold shifts from the storage node's charge balance, solved as a linear capacitor network;
- tunneling currents evaluated in logarithms;
- incremental-step programming by integrating the cell's charge ODE through the netlist's exact pulse train,
  and pulse counts by stepping a threshold until it reaches its target;
- raw bit error rates by integrating each Gaussian level over every read region and counting Gray-code bit
  flips (which includes non-adjacent misreads), and the sigma targets by root-finding on that function;
- densities, aspect ratios, retention, endurance and throughput from their definitions, by other groupings.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants, integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("23-06", ROOT / "chapters" / "23-06-nand-flash-and-3d-nand.md",
                        ROOT / "solutions" / "23-06-solutions.md", LAB / "README.md")
QE = constants.e
EPS0 = constants.epsilon_0
KB_EV = constants.k / constants.e
A_FN, B_FN = 1.25e-6, 2.33e10


# ---------------------------------------------------------------- independent helpers
def node_voltage(c_cg, c_other, v_cg, q):
    """Storage-node voltage from Kirchhoff's charge balance: C_CG (V - V_CG) + C_other V = Q."""
    m = np.array([[c_cg + c_other]])
    return float(np.linalg.solve(m, np.array([q + c_cg * v_cg]))[0])


def gate_threshold(c_cg, c_other, vt0, q):
    """Control-gate voltage that brings the node to vt0, by root-finding on node_voltage."""
    return optimize.brentq(lambda vg: node_voltage(c_cg, c_other, vg, q) - vt0, -50, 50, xtol=1e-14)


def j_fn(e):
    """Fowler-Nordheim current density computed in logarithms."""
    return math.exp(math.log(A_FN) + 2 * math.log(e) - B_FN / e)


def rber_exact(window, bits, sigma):
    """Raw bit error rate by integrating every level over every read region, weighting by Gray-code bit flips."""
    levels = 2 ** bits
    centres = np.linspace(0, window, levels)
    edges = np.concatenate(([-np.inf], (centres[:-1] + centres[1:]) / 2, [np.inf]))
    gray = [i ^ (i >> 1) for i in range(levels)]
    total = 0.0
    for i, c in enumerate(centres):
        for j in range(levels):
            if i == j:
                continue
            p = stats.norm.cdf(edges[j + 1], c, sigma) - stats.norm.cdf(edges[j], c, sigma)
            if j > i:  # use the upper tail directly for accuracy far from the centre
                p = stats.norm.sf(edges[j], c, sigma) - stats.norm.sf(edges[j + 1], c, sigma)
            total += p * bin(gray[i] ^ gray[j]).count("1")
    return total / levels / bits


def pulses_to_reach(v_start, v_target, step):
    """Count pulses by stepping the threshold one ISPP step at a time."""
    n, vt = 0, v_start
    while vt < v_target - 1e-9:
        vt += step
        n += 1
    return n


def af(ea, t_use_c, t_stress_c):
    """Arrhenius acceleration as the ratio of the two rates exp(-Ea/kT)."""
    rate = lambda t_c: math.exp(-ea / (KB_EV * (t_c + 273.15)))  # noqa: E731
    return rate(t_stress_c) / rate(t_use_c)


# ---------------------------------------------------------------- ISPP: integrate the netlist's cell
C_CG, C_TOX, TOX, AREA = 16e-18, 12.332618739e-18, 7e-9, 2.5e-15


def ispp_simulation(n_pulses=30, v0=15.0, dv=0.25, t_rise=1e-7, t_high=10e-6, period=15e-6):
    """Integrate dQ/dt = -I_FN(V_FG) through the PWL train of ispp.cir; return -Q/C_CG after each pulse."""
    ct = C_CG + C_TOX
    q = 0.0
    shifts, end_fields = [], []

    def rhs(t, y, vcg_fn):
        vfg = (C_CG * vcg_fn(t) + y[0] * 1e-18) / ct
        e = vfg / TOX
        return [-(j_fn(e) * AREA if e > 1e3 else 0.0) * 1e18]  # charge in attocoulombs

    for k in range(n_pulses):
        vp = v0 + dv * k
        segs = [(0.0, t_rise, lambda t, vp=vp: vp * t / t_rise),
                (t_rise, t_high, lambda t, vp=vp: vp),
                (t_high, t_high + t_rise, lambda t, vp=vp: vp * (1 - (t - t_high) / t_rise))]
        for a, b, fn in segs:
            sol = integrate.solve_ivp(rhs, (a, b), [q * 1e18], args=(fn,), method="Radau",
                                      rtol=1e-10, atol=1e-9, max_step=(b - a) / 50)
            q = sol.y[0, -1] * 1e-18
            if b == t_high:
                end_fields.append((C_CG * vp + q) / ct / TOX)
        shifts.append(-q / C_CG)
    assert period > t_high + t_rise
    return shifts, end_fields


# ---------------------------------------------------------------- chapter: Example 23-06.1
dvt = QE / 16e-18
v.check("Ex 23-06.1a", dvt * 1e3)
v.check("Ex 23-06.1b", 1 / dvt)
gap_qlc = 6 / 15
v.check("Ex 23-06.1c", gap_qlc)
v.check("Ex 23-06.1d", gap_qlc * 16e-18 / QE)
v.check("Ex 23-06.1e", 10 * QE / 16e-18)
v.check("Ex 23-06.1f", 10 * QE / 16e-18 / gap_qlc * 100)

# ---------------------------------------------------------------- Example 23-06.2
ctox = 3.9 * EPS0 * (50e-9 * 50e-9) / 7e-9
v.check("Ex 23-06.2a", ctox * 1e18)
v.check("Ex 23-06.2a1", ctox * 1e18)
alpha = node_voltage(16e-18, ctox, 1.0, 0.0)
v.check("Ex 23-06.2b", alpha)
v.check("Ex 23-06.2b1", alpha)
vfg = node_voltage(16e-18, ctox, 18.0, 0.0)
v.check("Ex 23-06.2c", vfg)
v.check("Ex 23-06.2c1", vfg)
e2 = vfg / 7e-9
v.check("Ex 23-06.2d", e2 / 1e8)
v.check("Ex 23-06.2d1", e2)
j2 = j_fn(e2)
v.check("Ex 23-06.2e", j2)
i2 = j2 * 2.5e-15
v.check("Ex 23-06.2f", i2 * 1e9)
v.check("Ex 23-06.2g", 100 * QE / i2 * 1e9)
v.check("Txt 23-06.a", j_fn(14.5e8) / j_fn(12e8))
v.check("Txt 23-06.a1", j_fn(14.5e8) / j_fn(10e8))

# ---------------------------------------------------------------- Example 23-06.3 and the lab's ISPP
shifts, end_fields = ispp_simulation()
steps = np.diff(shifts)
v.check("Ex 23-06.2h", end_fields[-1] / 1e8)
v.check("Ex 23-06.3a", steps[-1], tol=0.005)
v.assert_true("ISPP steady step within 0.1% of the pulse step", abs(steps[-1] - 0.25) < 2.5e-4)
v.check("Ex 23-06.3b", pulses_to_reach(-2, 4.5, 0.25))
v.check("Ex 23-06.3c", pulses_to_reach(-2, 4.5, 0.25) * 20)
v.check("Ex 23-06.3d0", (4.5 + 2) / 0.15)
v.check("Ex 23-06.3d", pulses_to_reach(-2, 4.5, 0.15))
v.check("Ex 23-06.3e", pulses_to_reach(-2, 4.5, 0.15) * 20)
v.check("Ex 23-06.3f", shifts[0])
v.check("Ex 23-06.3g", steps[-1])
v.check("Lab 23-06.a", shifts[0])
v.check("Lab 23-06.b", steps[-1])
v.check("Lab 23-06.c", shifts[-1])
v.assert_true("first ISPP step far exceeds the pulse step", shifts[0] > 4 * 0.25)

# ---------------------------------------------------------------- Example 23-06.4
for ident, bits in (("a", 1), ("b", 2), ("c", 3), ("d", 4)):
    v.check(f"Ex 23-06.4{ident}", 6 / (2 ** bits - 1))
v.check("Ex 23-06.4a0", 6 / 0.12)
v.check("Ex 23-06.4b0", 2 / 0.12)
v.check("Ex 23-06.4e0", (6 / 7) / 0.12)
v.check("Ex 23-06.4e", rber_exact(6, 3, 0.06))
v.check("Ex 23-06.4f0", (6 / 15) / 0.12)
v.check("Ex 23-06.4f", rber_exact(6, 4, 0.06))
v.check("Ex 23-06.4g0", (6 / 15) / 0.16)
v.check("Ex 23-06.4g", rber_exact(6, 4, 0.08))
v.check("Txt 23-06.b", math.log10(rber_exact(6, 4, 0.06) / rber_exact(6, 3, 0.06)))
v.check("Txt 23-06.c", (1 / 15) / (1 / 7))

# ---------------------------------------------------------------- Example 23-06.5
d280 = 28.5 / 280 / 4
d332 = 37.6 / 332 / 4
v.check("Ex 23-06.5a", d280)
v.check("Ex 23-06.5b", d332)
v.check("Ex 23-06.5c", (d332 - d280) / d280 * 100)
v.check("Ex 23-06.5d", 1 / (d280 * 1e9) * 1e6)  # mm^2 to um^2
h = 332 * 45e-9
v.check("Ex 23-06.5e", h * 1e6)
v.check("Ex 23-06.5e1", h * 1e6)
v.check("Ex 23-06.5f", h / 110e-9)
v.check("Ex 23-06.5g", (h / 2) / 110e-9)
v.check("Ex 23-06.5h", (h / 3) / 110e-9)

# ---------------------------------------------------------------- Example 23-06.6
af85 = af(1.1, 30, 85)
v.check("Ex 23-06.6a", af85)
v.check("Ex 23-06.6b", 365 * 24 / af85)
v.check("Txt 23-06.f", 365 * 24)
af40 = af(1.1, 30, 40)
v.check("Ex 23-06.6c", af40)
v.check("Ex 23-06.6d", 3 * af40)

# ---------------------------------------------------------------- Example 23-06.7
nand_writes = 7.68 * 3000
host = nand_writes / 2.5
v.check("Ex 23-06.7a", host)
v.check("Ex 23-06.7b", host / 7.68 / (5 * 365))
host_q = 30.72 * 1000 / 1.5
v.check("Ex 23-06.7c", host_q)
v.check("Ex 23-06.7d", host_q / 30.72 / (5 * 365))

# ---------------------------------------------------------------- Example 23-06.8
page_bits = 16 * 1024 * 8
w = 4 * page_bits / 8 / 500e-6
r = 4 * page_bits / 8 / 50e-6
v.check("Ex 23-06.8a", w / 1e6)
v.check("Ex 23-06.8a1", w / 1e6)
v.check("Ex 23-06.8b", r / 1e9)
v.check("Ex 23-06.8c0", 4.8e9 / w)
v.check("Ex 23-06.8c", math.ceil(4.8e9 / w))
v.check("Ex 23-06.8d0", 4.8e9 / r)
v.check("Ex 23-06.8d", math.ceil(4.8e9 / r))
v.check("Ex 23-06.8e0", 14e9 / w)
v.check("Ex 23-06.8e", math.ceil(14e9 / w))

# ---------------------------------------------------------------- practitioner arithmetic (TrendForce 2Q26)
total = 23.06 / 0.293
v.check("Txt 23-06.d", total)
v.check("Txt 23-06.e", 68.87 / total * 100)
v.assert_true("Kioxia's share gives a consistent total", abs(10.72 / 0.136 - total) / total < 0.005)
v.assert_true("top-five sum matches the reported total",
              abs(23.06 + 14.27 + 11.85 + 10.72 + 8.97 - 68.87) < 0.01)

# ---------------------------------------------------------------- problems
dv20 = QE / 20e-18
v.check("23-06.1a", dv20 * 1e3)
v.check("23-06.1a1", dv20 * 1e3)
v.check("23-06.1b", round(2 / dv20))
v.check("23-06.1c", 5.6 / 7)
v.check("23-06.1d", 0.8 * 20e-18 / QE)

v.check("23-06.2a", node_voltage(18e-18, 12e-18, 1.0, 0.0))
v.check("23-06.2a1", node_voltage(18e-18, 12e-18, 1.0, 0.0) * 100)
vt_neutral = gate_threshold(18e-18, 12e-18, 0.9, 0.0)
vt_160 = gate_threshold(18e-18, 12e-18, 0.9, -160 * QE)
v.check("23-06.2b", vt_neutral)
v.check("23-06.2c", vt_160 - vt_neutral)
v.check("23-06.2c1", vt_160 - vt_neutral)
v.check("23-06.2d", vt_160)

e3 = 9 / 6e-9
v.check("23-06.3a", e3 / 1e8)
v.check("23-06.3a1", e3)
v.check("23-06.3b0", A_FN * e3 * e3)
v.check("23-06.3b00", B_FN / e3)
j3 = j_fn(e3)
v.check("23-06.3b", j3)
v.check("23-06.3b1", j3)
v.check("23-06.3c0", (40e-9) ** 2)
i3 = j3 * (40e-9) ** 2
v.check("23-06.3c", i3 * 1e9)
v.check("23-06.3c1", i3 * 1e9)
v.check("23-06.3d", 50 * QE / i3 * 1e9)
v.check("23-06.3e0", B_FN / 1e8)
v.check("23-06.3e", j_fn(15e8) / j_fn(13e8))
v.check("23-06.3e1", (15 / 13 - 1) * 100)

v.check("23-06.4b", 16e-18 * 0.3 / QE)
v.assert_true("electrons per pulse independent of C_other",
              all(abs((gate_threshold(16e-18, co, 0.9, -16e-18 * 0.3) - gate_threshold(16e-18, co, 0.9, 0.0)) - 0.3)
                  < 1e-9 for co in (5e-18, 12e-18, 30e-18)))

v.check("23-06.5a", pulses_to_reach(-3, 5, 0.2))
v.check("23-06.5b", pulses_to_reach(-3, 5, 0.2) * 25e-3)
v.check("23-06.5c", pulses_to_reach(-3, 5, 0.1))
v.check("23-06.5d", pulses_to_reach(-3, 5, 0.1) * 25e-3)

for ident, bits in (("a", 2), ("c", 3), ("f", 4)):
    v.check(f"23-06.6{ident}", 6.4 / (2 ** bits - 1))
v.check("23-06.6a1", 6.4 / 3)
v.check("23-06.6b", 6.4 / 3 / 0.14)
v.check("23-06.6c1", 6.4 / 7)
v.check("23-06.6d", 6.4 / 7 / 0.14)
v.check("23-06.6e", rber_exact(6.4, 3, 0.07))
v.check("23-06.6f1", 6.4 / 15)
v.check("23-06.6g", 6.4 / 15 / 0.14)
v.check("23-06.6h", rber_exact(6.4, 4, 0.07))
v.check("23-06.6i0", 2e-3 * 64 / 30)
s6 = optimize.brentq(lambda s: rber_exact(6.4, 4, s) - 2e-3, 0.03, 0.2, xtol=1e-12)
v.check("23-06.6i", (6.4 / 15) / (2 * s6))
v.check("23-06.6i1", (6.4 / 15) / (2 * s6))
v.check("23-06.6j", s6)
v.check("23-06.6k", (s6 / 0.07 - 1) * 100)
v.check("23-06.6k1", 2e-3 / rber_exact(6.4, 4, 0.07))

gray2 = [i ^ (i >> 1) for i in range(4)]
v.assert_true("MLC Gray code 11,10,00,01 has single-bit neighbours",
              all(bin(a ^ b).count("1") == 1 for a, b in zip([3, 2, 0, 1], [2, 0, 1])) and
              all(bin(gray2[i] ^ gray2[i + 1]).count("1") == 1 for i in range(3)))
v.check("23-06.7b", np.mean([2, 3, 2]))

d8 = 1024 / 50
v.check("23-06.8a", d8)
v.check("23-06.8a1", d8)
dlb = d8 / (286 * 3)
v.check("23-06.8b", dlb)
v.check("23-06.8b1", dlb)
v.check("23-06.8c0", 1 / (dlb * 1e9))
v.check("23-06.8c", 1 / (dlb * 1e9) * 1e6)
v.check("23-06.8d", round(37.6 / 3 / dlb))
v.check("23-06.8e", (d332 / dlb - 1) * 100)
v.check("23-06.8e1", d332)

h9 = 400 * 40e-9
v.check("23-06.9a", h9 * 1e6)
v.check("23-06.9b", h9 / 100e-9)
v.check("23-06.9c", h9 / 100e-9 / 3)
v.check("23-06.9d", h9 / 100e-9 / 70)
v.check("23-06.9e", next(n for n in range(1, 10) if h9 / n / 100e-9 <= 70))
v.check("23-06.9f", h9 / 2 / 100e-9)

af10 = af(1.0, 25, 125)
v.check("23-06.10a0", math.log(af10))
v.check("23-06.10a", af10)
v.check("23-06.10a1", af10)
bake = 10 * 8760 / af10
v.check("23-06.10b", bake)
v.check("23-06.10b1", bake)
af06 = af(0.6, 25, 125)
v.check("23-06.10c0", math.log(af06))
v.check("23-06.10c", af06)
v.check("23-06.10c1", af06)
v.check("23-06.10d", bake * af06 / 8760)
v.check("23-06.10e", bake * af06 / 8760 * 12)

host11 = 3.84 * 1 * 365 * 5
v.check("23-06.11a", host11)
v.check("23-06.11b", host11 * 3 / 3.84)
v.check("23-06.11b0", 365 * 5)
v.check("23-06.11c", 1500 / 3 / (365 * 5))

page = 16 * 1024
t12 = 6 * page / 400e-6
q12 = 6 * page / 2e-3
v.check("23-06.12a", t12 / 1e6)
v.check("23-06.12a1", t12 / 1e6)
v.check("23-06.12b", q12 / 1e6)
v.check("23-06.12b1", q12 / 1e6)
v.check("23-06.12c0", 12e9 / t12)
v.check("23-06.12c", math.ceil(12e9 / t12))
v.check("23-06.12d0", 12e9 / q12)
v.check("23-06.12d", math.ceil(12e9 / q12))
v.check("23-06.12e", 6 * page / 60e-6 / 1e9)

k13 = 0.4 / 0.18
v.check("23-06.13a", k13)
v.check("23-06.13a1", k13)
r13 = rber_exact(6, 4, 0.09)
v.check("23-06.13b", r13)
v.assert_true("QLC fails the 5e-3 ECC limit at sigma 0.09 V", r13 > 5e-3)
v.check("23-06.13c", (6 / 7) / 0.18)
v.check("23-06.13c1", (6 / 7) / 0.18)
v.check("23-06.13d", rber_exact(6, 3, 0.09))
s13 = optimize.brentq(lambda s: rber_exact(6, 4, s) - 5e-3, 0.03, 0.2, xtol=1e-12)
v.check("23-06.13e", s13)
v.check("23-06.13f", 0.4 / (2 * s13))
v.check("23-06.13f1", 0.4 / (2 * s13))

w14 = 6 * page / 2.5e-3
v.check("23-06.14a", w14 / 1e6)
v.check("23-06.14a1", w14 / 1e6)
v.check("23-06.14b", w14 / 600e6 * 100)
v.check("23-06.14c0", 600e6 / w14)
v.check("23-06.14c", math.ceil(600e6 / w14))
d14 = 30 / (400 * 3)
v.check("23-06.14d", d14)
v.check("23-06.14e", (1 - d14 / d332) * 100)

# ---------------------------------------------------------------- lab: sigma targets
for ident, bits in (("d", 3), ("e", 4)):
    s = optimize.brentq(lambda x, b=bits: rber_exact(6, b, x) - 1e-3, 0.02, 0.5, xtol=1e-12)
    v.check(f"Lab 23-06.{ident}", s)

sys.exit(v.finish())
