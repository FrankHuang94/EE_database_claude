#!/usr/bin/env python3
"""Verify every published number in chapter 01-01, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.constants import Boltzmann as K_B, elementary_charge as Q
from scipy.optimize import brentq
from sympy.physics import units as u

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-01",
    COURSE / "chapters" / "01-01-functions-models-and-units.md",
    COURSE / "solutions" / "01-01-solutions.md",
    COURSE / "labs" / "01-01-lab" / "README.md",
)


def vt(T):
    return K_B * T / Q


def dbp(x):
    return 10 * math.log10(x)


def dba(x):
    return 20 * math.log10(x)


LN10 = math.log(10)

# ---------------------------------------------------------------- chapter examples
# Ex 1: tau = 2 ms
v.check("Ex 01-01.1a", 2 * math.log(2))
v.check("Ex 01-01.1b", 2 * math.log(10))
# Ex 2: gain chain
g = 20 - 3 + 15
v.check("Ex 01-01.2a", g)
v.check("Ex 01-01.2b", 10 ** (g / 10))
v.check("Ex 01-01.2c", -40 + g)
v.check("Ex 01-01.2d", 10 ** ((-40 + g) / 10))
v.check("Ex 01-01.2e", 10 ** (g / 20))
v.assert_true("voltage gain is sqrt of power gain", math.isclose(10 ** (g / 20), math.sqrt(10 ** (g / 10))))
# Ex 3: diode, Is = 1e-14 A, VT = 25.85 mV as stated in the example
VT_EX = 0.02585
Is = 1e-14
v.check("Ex 01-01.3a", Is * (math.exp(0.6 / VT_EX) - 1) * 1e3)
v.check("Ex 01-01.3b", VT_EX * math.log(1e-3 / Is + 1))
v.check("Ex 01-01.3c", VT_EX * LN10 * 1e3)
v.assert_true("VT at 300 K rounds to 25.85 mV", round(vt(300) * 1e3, 2) == 25.85)
I06 = Is * (math.exp(0.6 / VT_EX) - 1)
v.assert_true("sanity: 0.92 decades x 59.5 mV = 54.7 mV = 0.6547 - 0.6",
              round(math.log10(1e-3 / I06), 2) == 0.92 and round(0.92 * 59.5, 1) == 54.7
              and abs((0.6547 - 0.6) - math.log10(1e-3 / I06) * VT_EX * LN10) < 1e-4)
# Ex 4: 170 cos(377 t + pi/6)
w = 377.0
v.check("Ex 01-01.4a", w / (2 * math.pi))
v.check("Ex 01-01.4b", 2 * math.pi / w * 1e3)
v.check("Ex 01-01.4c", 170 / math.sqrt(2))
t_pk = brentq(lambda t: math.sin(w * t + math.pi / 6), 0.010, 0.0165)  # derivative zero → peak
v.assert_true("t_pk is a maximum", math.cos(w * t_pk + math.pi / 6) > 0.999999)
v.check("Ex 01-01.4d", t_pk * 1e3)
# Ex 5: power-law fit to the published synthetic data
V = np.array([0.6, 0.7, 0.8, 0.9, 1.0])
P = np.array([0.130, 0.206, 0.307, 0.437, 0.600])
v.assert_true("data are 0.6 V^3 rounded to 3 decimals", np.allclose(P, np.round(0.6 * V**3, 3)))
n_fit, lnk = np.polyfit(np.log(V), np.log(P), 1)
v.check("Ex 01-01.5a", n_fit)
v.check("Ex 01-01.5b", math.exp(lnk))
v.check("Ex 01-01.5c", 100 * (1 - 0.9**n_fit))
v.assert_true("exact cubic gives 27.1 %", round(100 * (1 - 0.9**3), 1) == 27.1)
v.assert_true("energy per op falls ~19 % (0.9^2)", round(100 * (1 - 0.9**2)) == 19)
# Sanity check in Ex 1: number of halvings to 10 %
v.assert_true("log2(10) = 3.32", round(math.log2(10), 2) == 3.32)

# numbers to know
v.check("N 01-01.a", 10 ** (36 / 10) / 1e3)
v.check("N 01-01.b", 10 ** (30 / 10) / 1e3)
v.check("N 01-01.c", 10 ** (5 / 10))
v.assert_true("1 rad = 57.30 deg", round(math.degrees(1), 2) == 57.30)
v.assert_true("small-angle error at 0.1 rad ≈ 0.17 %",
              round(100 * (0.1 - math.sin(0.1)) / math.sin(0.1), 2) == 0.17)
v.assert_true("EVM -38 dB = 1.26 %", round(100 * 10 ** (-38 / 20), 2) == 1.26)
v.assert_true("+3 dB -> range x1.41 (sqrt of 2x power)", round(math.sqrt(10 ** 0.3), 2) == 1.41)
v.assert_true("landmark: 6 dB ≈ 4x power, 2x amplitude",
              round(10 ** 0.6, 1) == 4.0 and round(10 ** 0.3, 2) == 2.0)
v.assert_true("ln2, ln10, log10(2)", (round(math.log(2), 4), round(LN10, 4), round(math.log10(2), 4))
              == (0.6931, 2.3026, 0.3010))

# ---------------------------------------------------------------- problems
# P1: sensor + ADC
Vs = lambda T: 0.5 + 0.01 * T  # noqa: E731
N = lambda Vx: 4096 * Vx / 3.3  # noqa: E731
v.check("01-01.1a", Vs(-40))
v.check("01-01.1b", Vs(125))
v.check("01-01.1c", N(Vs(25)))
v.check("01-01.1d", (N(Vs(1)) - N(Vs(0))))
T_of_N = brentq(lambda T: N(Vs(T)) - 1500, -40, 125)
v.check("01-01.1e", T_of_N)
v.check("01-01.1f", N(Vs(-40)))
v.check("01-01.1g", N(Vs(125)))

# P2: dimensional validity via sympy units
def same_units(expr, target):
    return u.convert_to(expr, target) == target


v.assert_true("RC is a time, so t/(RC) is dimensionless", same_units(u.ohm * u.farad, u.second))
v.assert_true("L/R is a time, so Rt/L is dimensionless", same_units(u.henry / u.ohm, u.second))
v.assert_true("f t is dimensionless", u.convert_to(u.hertz * u.second, u.second) == 1)
v.assert_true("2 pi f is NOT dimensionless", same_units(u.hertz, 1 / u.second))

# P3
v.check("01-01.3a", math.exp(3) * math.exp(-5) / math.exp(-2))
v.check("01-01.3b", math.log(math.exp(4) * math.sqrt(math.e)))
v.check("01-01.3c", math.log10(0.001))
v.check("01-01.3d", math.log2(1024))
v.check("01-01.3e", math.log(20) - math.log(5) + math.log(0.25), tol=1e-12)
v.check("01-01.3f", math.log(10) / math.log(2))
v.check("01-01.3g", math.log(math.exp(2) ** (1 / 3)))

# P4
v.check("01-01.4a", brentq(lambda t: 5 * math.exp(-t / 3) - 1, 0, 20))
v.check("01-01.4b", brentq(lambda x: 2**x - 50, 0, 10))
v.check("01-01.4c", brentq(lambda x: 10 ** (x / 10) - 0.25, -20, 0))
v.check("01-01.4d", brentq(lambda tau: 4.0 * math.exp(-10 / tau) - 1.5, 1, 100))

# P5
v.check("01-01.5a", dbp(2))
v.check("01-01.5b", dbp(0.01))
v.check("01-01.5c", dbp(1000))
v.check("01-01.5d", dbp(0.5))
v.check("01-01.5e", 10 ** 1.3)
v.check("01-01.5f", 10 ** -0.7)
v.check("01-01.5g", dba(0.5))
v.check("01-01.5h", 10 ** (46 / 20))
v.check("01-01.5i", 10 ** (100 / 20))

# P6
v.check("01-01.6a", dbp(100 / 1))
v.check("01-01.6b", dbp(1e-6 / 1e-3))
v.check("01-01.6c", dbp(2 / 1e-3))
v.check("01-01.6d", dbp(0.25))
v.check("01-01.6e", 1e-3 * 10 ** (-90 / 10) * 1e12)
v.check("01-01.6f", 10 ** (17 / 10))
vrms = math.sqrt(1e-3 * 50)
v.check("01-01.6g", vrms)
v.check("01-01.6h", vrms * math.sqrt(2))
v.check("01-01.6i", dba(vrms / 1.0))

# P7: i = 0.5 cos(2000 pi t - 0.7) mA
w7 = 2000 * math.pi
v.check("01-01.7a", w7 / (2 * math.pi))
v.check("01-01.7b", 2 * math.pi / w7 * 1e3)
v.check("01-01.7c", math.degrees(-0.7))
v.check("01-01.7d", 0.5 / math.sqrt(2))
v.check("01-01.7e", 0.5 * math.cos(w7 * 1e-4 - 0.7))
t7 = brentq(lambda t: math.sin(w7 * t - 0.7), 0, 2.5e-4)
v.check("01-01.7f", t7 * 1e3)
v.assert_true("i(0.1 ms) is before the peak", 1e-4 < t7)

# P8: RC charging, R = 10k, C = 100n
tau8 = 10e3 * 100e-9
vc = lambda t: 5 * (1 - math.exp(-t / tau8))  # noqa: E731
v.check("01-01.8a", tau8 * 1e3)
v.check("01-01.8b", brentq(lambda t: vc(t) - 2.5, 0, 0.01) * 1e3)
v.check("01-01.8c", brentq(lambda t: vc(t) - 4.5, 0, 0.01) * 1e3)
t10 = brentq(lambda t: vc(t) - 0.5, 0, 0.01)
t90 = brentq(lambda t: vc(t) - 4.5, 0, 0.01)
v.check("01-01.8d", (t90 - t10) * 1e3)
v.assert_true("rise time = tau ln 9", math.isclose(t90 - t10, tau8 * math.log(9), rel_tol=1e-9))
v.check("01-01.8e", vc(3e-3))
v.check("01-01.8f", brentq(lambda t: vc(t) - 3.5, 0, 0.01) * 1e3)

# P9: diode temperature dependence (exact CODATA constants)
for T, a, b in [(250, "a", "d"), (300, "b", "e"), (400, "c", "f")]:
    v.check(f"01-01.9{a}", vt(T) * 1e3)
    v.check(f"01-01.9{b}", vt(T) * LN10 * 1e3)
I_s9 = 1e-3 / math.exp(0.650 / vt(300))
v.check("01-01.9g", vt(300) * math.log(10e-6 / I_s9))
v.check("01-01.9h", vt(300) * math.log(100e-3 / I_s9))
v.check("01-01.9i", I_s9 * math.exp(0.700 / vt(300)) * 1e3)

# P10: link budget
pr = 20 - 2 + 3 - 80 + 3
v.check("01-01.10a", pr)
v.check("01-01.10b", 1e-3 * 10 ** (pr / 10))
margin = pr - (-90)
v.check("01-01.10c", margin)
v.check("01-01.10d", 10 ** (margin / 20))
v.check("01-01.10e", dbp(2))
v.check("01-01.10f", 10 ** (dbp(2) / 20))

# P11: tilt sensor
for deg, a, b in [(5, "a", "b"), (15, "c", "d"), (30, "e", "f")]:
    th = math.radians(deg)
    v.check(f"01-01.11{a}", math.degrees(math.sin(th)))
    v.check(f"01-01.11{b}", 100 * (1 - math.sin(th) / th))
v.check("01-01.11g", math.degrees(math.sqrt(0.06)))
th1 = brentq(lambda t: math.sin(t) / t - 0.99, 0.01, 1.0)
v.check("01-01.11h", math.degrees(th1))

# P12: DVFS
P0, V0, f0 = 1.5, 1.0, 2.0e9
alphaC = P0 / (V0**2 * f0)
Pa = alphaC * 0.8**2 * f0
Pb = alphaC * 0.8**2 * 1.6e9
v.check("01-01.12a", Pa)
v.check("01-01.12b", Pb)
v.check("01-01.12c", P0 / f0 * 1e9)
v.check("01-01.12d", Pb / 1.6e9 * 1e9)
cyc = 3e9
tn, td = cyc / f0, cyc / 1.6e9
v.check("01-01.12e", tn)
v.check("01-01.12f", P0 * tn)
v.check("01-01.12g", td)
v.check("01-01.12h", Pb * td)
En, Ed = (P0 + 0.2) * tn, (Pb + 0.2) * td
v.check("01-01.12i", En)
v.check("01-01.12j", Ed)
v.check("01-01.12k", 100 * (1 - Ed / En))
v.check("01-01.12l", 100 * (1 - Pb * td / (P0 * tn)))

# P13: exponential fit to published data
t13 = np.arange(5.0)
v13 = np.array([4.000, 2.054, 1.054, 0.541, 0.278])
v.assert_true("P13 data are 4 exp(-t/1.5) rounded", np.allclose(v13, np.round(4 * np.exp(-t13 / 1.5), 3)))
s13, c13 = np.polyfit(t13, np.log(v13), 1)
v.check("01-01.13a", -1 / s13)
v.check("01-01.13b", math.exp(c13))
v.check("01-01.13c", 4 / math.log(4.000 / 0.278))
v.check("01-01.13d", 4.00 * math.exp(-6 / 1.50))
v.assert_true("ln v data as printed", np.allclose(np.log(v13), [1.386, 0.7198, 0.0526, -0.6143, -1.280], atol=6e-4))

# P14: log-distance path loss fit
d14 = np.array([1, 2, 5, 10, 20.0])
p14 = np.array([-40.0, -49.0, -61.0, -70.0, -79.0])
s14, c14 = np.polyfit(np.log10(d14), p14, 1)
v.check("01-01.14a", -s14 / 10)
v.check("01-01.14b", c14)
v.check("01-01.14c", brentq(lambda d: -40.0 - 30 * math.log10(d) + 90, 1, 1e4))
v.check("01-01.14d", brentq(lambda d: -40.0 - 20 * math.log10(d) + 90, 1, 1e4))
v.assert_true("indoor range ~7x shorter", round(316.2 / 46.4) == 7)

# P15: doubling times
a15 = 2 ** 0.5
v.check("01-01.15a", a15)
v.check("01-01.15b", 100 * (a15 - 1))
r15 = math.log(2) / 2
v.check("01-01.15c", r15)
v.check("01-01.15d", 1 / r15)
v.check("01-01.15e", math.exp(r15 * 10))
v.check("01-01.15f", 70 / 41.42)
v.check("01-01.15g", 70 / 7)
v.check("01-01.15h", math.log(2) / math.log(1.07))
v.assert_true("rule-of-70 error ~15 % at 41 %, ~2 % at 7 %",
              round(100 * (1 - (70 / 41.42) / 2)) == 15 and round(100 * (1 - 10 / 10.2448)) == 2)

v.check("01-01.16a", (math.e + math.exp(-1)) / 2)
v.check("01-01.16b", (math.e - math.exp(-1)) / 2)
v.check("01-01.16c", math.cosh(1) ** 2)
v.check("01-01.16d", math.sinh(1) ** 2)
v.assert_true("cosh^2 - sinh^2 = 1", math.isclose(math.cosh(1) ** 2 - math.sinh(1) ** 2, 1.0))
v.check("01-01.16e", (1 - math.exp(-6)) / (1 + math.exp(-6)))
v.check("01-01.16f", 1 - 2 * math.exp(-6))
v.check("01-01.16g", 1 - math.tanh(3))

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-01.a", vt(360) * 1e3)
v.check("Lab 01-01.b", vt(360) * LN10 * 1e3)
v.check("Lab 01-01.c", -40 + 20 - 3 + 15 - 6)
v.check("Lab 01-01.d", 10 ** ((-40 + 20 - 3 + 15 - 6) / 10) * 1e3)

v.finish()
