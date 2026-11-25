#!/usr/bin/env python3
"""Verify every number in chapter 23-08 (emerging memories), its problems and its lab.

Independent routes (the lab module emem.py uses closed forms):
- MTJ read currents from a nodal solve of the series read path;
- thermal stability by root-finding on the expected number of flips, and temperature scaling through the barrier
  energy E_b = Delta k T;
- PCM heating, quench and SET plateau by integrating the thermal ODE C dT/dt = P - T/R with scipy, with an event for
  the cooling crossings;
- drift times by solving R(t)/R0 = factor in logarithms;
- the conductance quantum from CODATA via scipy.constants;
- FeRAM charge and signals in SI units throughout.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants, integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "23-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("23-08", ROOT / "chapters" / "23-08-emerging-memories.md",
                        ROOT / "solutions" / "23-08-solutions.md", LAB / "README.md")
YEAR = 365.25 * 86400
F0 = 1e9
KB = constants.k


# ---------------------------------------------------------------- independent helpers
def read_current(v_read, r_mtj, r_series):
    """Nodal solve: node x between the access device and the MTJ; returns the branch current."""
    g1, g2 = 1 / r_series, 1 / r_mtj
    x = np.linalg.solve(np.array([[g1 + g2]]), np.array([g1 * v_read]))[0]
    return x * g2


def delta_for(n_bits, t, flips=1.0):
    return optimize.brentq(lambda d: n_bits * t * F0 * math.exp(-d) - flips, 1, 200, xtol=1e-12)


def delta_rescaled(delta, t_from_c, t_to_c):
    eb = delta * KB * (t_from_c + 273.15)
    return eb / (KB * (t_to_c + 273.15))


def pcm_peak(power, r_th, tau, t_pulse):
    c_th = tau / r_th
    sol = integrate.solve_ivp(lambda t, y: [(power - y[0] / r_th) / c_th], (0, t_pulse), [0.0],
                              rtol=1e-10, atol=1e-9, max_step=tau / 20)
    return sol.y[0, -1]


def pcm_cool_time(r_th, tau, start, end):
    c_th = tau / r_th
    ev = lambda t, y: y[0] - end  # noqa: E731
    ev.terminal = True
    sol = integrate.solve_ivp(lambda t, y: [-y[0] / r_th / c_th], (0, 100 * tau), [start], events=ev,
                              rtol=1e-11, atol=1e-10)
    return sol.t_events[0][0]


def time_to_drift(factor, nu, t0=1.0):
    return t0 * math.exp(math.log(factor) / nu)


G0 = constants.physical_constants["conductance quantum"][0]

# ---------------------------------------------------------------- Example 23-08.1
rap = 4e3 + 1.5 * 4e3
v.check("Ex 23-08.1a", rap / 1e3)
ip = read_current(0.15, 4e3, 2e3)
iap = read_current(0.15, rap, 2e3)
v.check("Ex 23-08.1b", ip * 1e6)
v.check("Ex 23-08.1c", iap * 1e6)
v.check("Ex 23-08.1d", (ip - iap) * 1e6)
v.check("Ex 23-08.1e", (ip / iap - 1) * 100)
v.check("Ex 23-08.1f", (ip - iap) / 2 * 1e6)

# ---------------------------------------------------------------- Example 23-08.2
n2, t10 = 2 ** 25, 10 * YEAR
v.check("Ex 23-08.2e", t10)
v.check("Ex 23-08.2a", n2 * t10 * F0)
v.check("Ex 23-08.2a1", n2 * t10 * F0)
d2 = delta_for(n2, t10)
v.check("Ex 23-08.2b", d2)
v.check("Ex 23-08.2b1", d2)
v.check("Ex 23-08.2c", delta_rescaled(d2, 85, 25))
v.check("Ex 23-08.2d", delta_rescaled(d2, 150, 25))
v.check("Txt 23-08.a", math.log(1e6))

# ---------------------------------------------------------------- Example 23-08.3
for ident, d in (("a", 60), ("b", 40)):
    i = 1.5 * 1e-6 * d
    v.check(f"Ex 23-08.3{ident}1", i * 1e6)
    v.check(f"Ex 23-08.3{ident}", integrate.quad(lambda t: 0.5 * i, 0, 20e-9)[0] * 1e12)
tau40 = 1 / (F0 * math.exp(-40))
v.check("Ex 23-08.3c0", tau40)
v.check("Ex 23-08.3c1", tau40)
v.check("Ex 23-08.3c", tau40 / YEAR)
v.check("Ex 23-08.3d", 1 / (2 ** 20 * F0 * math.exp(-40)))

# ---------------------------------------------------------------- Example 23-08.4
p4 = (200e-6) ** 2 * 2e3
v.check("Ex 23-08.4a", p4 * 1e6)
rth4 = 600 / p4
v.check("Ex 23-08.4b", rth4 / 1e6)
v.assert_true("50 ns RESET reaches the melt rise within 0.1%", abs(pcm_peak(p4, rth4, 2e-9, 50e-9) / 600 - 1) < 1e-3)
v.check("Ex 23-08.4c", p4 * 50e-9 * 1e12)
v.check("Ex 23-08.4d", pcm_cool_time(rth4, 2e-9, 600, 125) * 1e9)
pset = 300 / rth4
v.check("Ex 23-08.4e0", pset * 1e6)
v.check("Ex 23-08.4e", math.sqrt(pset / 2e3) * 1e6)
v.check("Ex 23-08.4f", pset * 150e-9 * 1e12)
v.check("Txt 23-08.b", 150 / 50)

# ---------------------------------------------------------------- Example 23-08.5
for ident, t in (("a", 3600), ("b", 86400), ("c", 10 * YEAR)):
    v.check(f"Ex 23-08.5{ident}", math.exp(0.1 * math.log(t)))
t5 = time_to_drift(2, 0.1)
v.check("Ex 23-08.5d", t5)
v.check("Ex 23-08.5e", t5 / 60)

# ---------------------------------------------------------------- Example 23-08.6
v.check("Ex 23-08.6a", G0 * 1e6)
v.check("Ex 23-08.6b", 1 / G0 / 1e3)
v.check("Ex 23-08.6b1", 1 / G0 / 1e3)
v.check("Ex 23-08.6c", (1 / 3e3) / G0)
v.check("Ex 23-08.6d", 0.2 / 3e3 * 1e6)
v.check("Ex 23-08.6e", 0.2 / 100e3 * 1e6)
v.check("Ex 23-08.6f", 100e3 / 3e3)
v.check("Ex 23-08.6g", G0 / (1 / 3e3) * 100)

# ---------------------------------------------------------------- Example 23-08.7
area = (80e-9) ** 2
v.check("Ex 23-08.7a0", area * 1e4)
q7 = 2 * 0.20 * area  # 20 uC/cm^2 = 0.20 C/m^2
v.check("Ex 23-08.7a", q7 * 1e15)
v.check("Ex 23-08.7b", q7 / 30e-15 * 1e3)
v.check("Ex 23-08.7c", 2 * 1e8 * 10e-9)

# ---------------------------------------------------------------- Example 23-08.8
v.check("Ex 23-08.8a", 1024 / 105.1)
v.check("Ex 23-08.8b", 0.0396 / 0.028 ** 2)
v.check("Ex 23-08.8c", 37.6 * 1024 / 9.75)
v.check("Ex 23-08.8d", 68.87e9 / 14.8e6)

# ---------------------------------------------------------------- problems
r1ap = 3e3 * 3
v.check("23-08.1a", r1ap / 1e3)
i1p, i1ap = read_current(0.1, 3e3, 1.5e3), read_current(0.1, r1ap, 1.5e3)
v.check("23-08.1b", i1p * 1e6)
v.check("23-08.1b1", i1p * 1e6)
v.check("23-08.1c", i1ap * 1e6)
v.check("23-08.1c1", i1ap * 1e6)
v.check("23-08.1d", (i1p / i1ap - 1) * 100)

tau50 = math.exp(50) / F0
v.check("23-08.2a", tau50)
v.check("23-08.2b", tau50 / YEAR)
v.check("23-08.2c", 2 ** 26 * t10 / tau50)

d125 = delta_rescaled(75, 25, 125)
v.check("23-08.3a", d125)
v.check("23-08.3a1", d125)
req3 = delta_for(2 ** 24, t10)
v.check("23-08.3b", req3)
v.check("23-08.3b1", req3)
v.check("23-08.3c", 2 ** 24 * t10 * F0 * math.exp(-d125))
v.assert_true("Problem 23-08.3 array narrowly fails", 2 ** 24 * t10 * F0 * math.exp(-d125) > 1)
v.check("23-08.3d", delta_rescaled(req3, 125, 25))

e4 = {}
for ident, d in (("a", 45), ("b", 70)):
    i = 1.3 * 0.8e-6 * d
    e4[ident] = 0.6 * i * 10e-9
    v.check(f"23-08.4{ident}0", i * 1e6)
    v.check(f"23-08.4{ident}", e4[ident] * 1e12)
v.check("23-08.4c", math.exp(70) / math.exp(45))
v.check("23-08.4d", (e4["b"] / e4["a"] - 1) * 100)

p5 = 600 / 5e6
v.check("23-08.5a", p5 * 1e6)
v.check("23-08.5b", math.sqrt(p5 / 3e3) * 1e6)
v.check("23-08.5c", p5 * 30e-9 * 1e12)
v.check("23-08.5d", pcm_cool_time(5e6, 1.5e-9, 600, 150) * 1e9)
v.check("23-08.5e", pcm_peak(p5, 5e6, 1.5e-9, 3e-9))

t6a, t6b = time_to_drift(1.5, 0.05), time_to_drift(1.5, 0.1)
v.check("23-08.6a", t6a)
v.check("23-08.6a1", t6a / 60)
v.check("23-08.6b", t6b)
v.check("23-08.6b1", t6b)
v.check("23-08.6c", math.exp(0.05 * math.log(10 * YEAR)))
v.assert_true("time ratio equals 1.5^10", abs(t6a / t6b - 1.5 ** 10) < 1e-6)

v.check("23-08.7a", (1 / 6.45e3) / G0)
v.check("23-08.7b", 1 / G0 / 1e3)
v.check("23-08.7c", 1 / (3 * G0) / 1e3)

a8 = (60e-9) ** 2
v.check("23-08.8d0", a8 * 1e4)
q8 = 2 * 0.15 * a8
v.check("23-08.8a", q8 * 1e15)
v.check("23-08.8b", q8 / 20e-15 * 1e3)
dram = 0.5 * 10e-15 / (10e-15 + 20e-15)
v.check("23-08.8c", dram * 1e3)
v.check("23-08.8c1", dram)
v.check("23-08.8d", dram * 20e-15 / (2 * a8) * 1e2)  # C/m^2 to uC/cm^2: x 1e6 / 1e4

v.check("23-08.9a", 2 * 1.2e8 * 8e-9)
v.check("23-08.9b", 3 / (2 * 1e8) * 1e9)

w10 = 15 * YEAR
v.check("23-08.10a", w10)
v.check("23-08.10a1", w10)
v.check("23-08.10b", 1e5 / 3600)
v.check("23-08.10c", w10 / 1e5)
v.check("23-08.10d", w10 / 1e4)
v.check("23-08.10e", w10 / 1e6)

cell = 50 * 0.028 ** 2
v.check("23-08.11a", cell)
cells = 32 * 2 ** 20 * cell / 1e6
v.check("23-08.11b", cells)
v.check("23-08.11b1", cells)
v.check("23-08.11c", cells / 0.5)
sram = 32 * 2 ** 20 * 0.127 / 1e6 / 0.5
v.check("23-08.11d", sram)
v.check("23-08.11e", cells / 0.5 / sram)

v.check("23-08.12a", 16 * 1024 / 9.75)
v.check("23-08.12c", 26 * 33)
v.check("23-08.12b", 16 * 1024 / 9.75 / (26 * 33))

b13 = 8 * 2 ** 20
v.check("23-08.13a", b13)
v.check("23-08.13a1", b13)
v.check("23-08.13b", b13 * 0.7e-12 * 1e6)
v.check("23-08.13c", b13 * 4e-12 * 1e6)
v.check("23-08.13d", b13 * 100e-12 * 1e6)
v.check("23-08.13e", b13 * 100e-12 / 50e-6)

# ---------------------------------------------------------------- lab
v.check("Lab 23-08.a", pcm_peak(p4, rth4, 2e-9, 50e-9))
v.check("Lab 23-08.b", pcm_cool_time(rth4, 2e-9, 500, 125) * 1e9)
v.check("Lab 23-08.c", pcm_peak(pset, rth4, 2e-9, 150e-9))
dl = delta_for(2 ** 30, t10)
v.check("Lab 23-08.d", dl)
v.check("Lab 23-08.e", delta_rescaled(dl, 85, 25))
v.check("Lab 23-08.f", 1e4 * 1.0 * F0 * math.exp(-25))

sys.exit(v.finish())
