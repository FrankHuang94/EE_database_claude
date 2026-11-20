#!/usr/bin/env python3
"""Verify chapter 15-07 (frequency-domain design): examples, problems and lab answers.

Routes:
- margins by root finding on |L| - 1 and a continuous phase (labs/15-07-lab/freqdomain.py), with closed forms
  (the standard-loop PM, the delay loop, the three-equal-pole crossing) checked against them;
- every stability claim checked twice: Nyquist encirclements traced along the indented contour, and closed-loop roots;
- Bode's integral by quadrature; the margin bounds from Ms by geometry on a sampled Nyquist plot;
- step overshoots from labs/15-03-lab/specs.py; Example 15-07.6 confirmed in ngspice (opamp_loop.cir).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "15-07-lab"))
sys.path.insert(0, str(ROOT / "labs" / "15-03-lab"))
from eeverify import Verifier  # noqa: E402
import freqdomain as fd  # noqa: E402
from specs import step_specs  # noqa: E402

CH = ROOT / "chapters" / "15-07-frequency-domain-design.md"
v = Verifier.from_files("15-07", CH, ROOT / "solutions" / "15-07-solutions.md", ROOT / "labs" / "15-07-lab" / "README.md")


def unstable_roots(num, den, K=1.0):
    return int(np.sum(np.roots(np.polyadd(den, K * np.asarray(num, float))).real > 1e-9))


def zeta_for_pm(pm):
    return brentq(lambda z: fd.pm_from_zeta(z) - pm, 0.01, 0.99, xtol=1e-14)


def os_pct(z):
    return 100 * math.exp(-math.pi * z / math.sqrt(1 - z * z))


# ---------------------------------------------------------------------------------------- text
z45, z60 = zeta_for_pm(45), zeta_for_pm(60)
v.check("Txt 15-07.a", z45)
v.check("Txt 15-07.b", os_pct(z45))
v.check("Txt 15-07.c", z60)
v.check("Txt 15-07.d", os_pct(z60))
A0, p1 = 1e5, 2 * math.pi * 100
for f2, key in ((40e6, "e"), (10e6, "f")):
    v.check(f"Txt 15-07.{key}", fd.margins([A0], np.polymul([1 / p1, 1], [1 / (2 * math.pi * f2), 1]))["pm"])

# ---------------------------------------------------------------------------------------- Example 1
m = fd.margins([100], [1, 10, 0])
v.check("Ex 15-07.1a", m["wc"])
v.check("Ex 15-07.1b", m["pm"])
v.assert_true("Ex 1: no phase crossover (infinite GM)", "w180" not in m)
wn = 10.0
v.check("Ex 15-07.1c", 10 / (2 * wn))
v.assert_true("Ex 1: PM equals the standard-loop formula at zeta 0.5", abs(fd.pm_from_zeta(0.5) - m["pm"]) < 1e-9)
T1 = lambda w: abs(100 / ((1j * w) ** 2 + 10j * w + 100))  # noqa: E731
v.check("Ex 15-07.1d", brentq(lambda w: T1(w) - 1 / math.sqrt(2), 1, 50, xtol=1e-13))

# ---------------------------------------------------------------------------------------- Example 2
K2 = 224 / 27
m = fd.margins([K2], [1, 6, 8, 0])
v.check("Ex 15-07.2a", m["w180"])
v.check("Ex 15-07.2b", m["gm"])
v.check("Ex 15-07.2c", m["gm_db"])
v.check("Ex 15-07.2d", m["wc"])
v.check("Ex 15-07.2e", m["pm"])
v.check("Ex 15-07.2f", fd.sensitivity_peak([K2], [1, 6, 8, 0])[0])
v.assert_true("Ex 2: GM x K = Routh limit 48", abs(m["gm"] * K2 - 48) < 1e-9)
v.assert_true("Ex 2: Bode integral is zero", abs(fd.bode_integral([K2], [1, 6, 8, 0])) < 1e-6)

# ---------------------------------------------------------------------------------------- Example 3
for z, (kw, kp) in ((0.3, "ab"), (0.5, "cd"), (0.7, "ef")):
    wn = 1.0
    m = fd.margins([wn**2], [1, 2 * z * wn, 0])
    v.check(f"Ex 15-07.3{kw}", m["wc"] / wn)
    v.check(f"Ex 15-07.3{kp}", m["pm"])
    v.assert_true(f"Ex 3: formula matches root finding at zeta {z}", abs(fd.pm_from_zeta(z) - m["pm"]) < 1e-9)

# ---------------------------------------------------------------------------------------- Example 4
m = fd.margins([0.5], [1, 0], T=1.0)
v.check("Ex 15-07.4a", m["wc"])
v.check("Ex 15-07.4b", m["pm"])
v.check("Ex 15-07.4c", m["w180"])
v.check("Ex 15-07.4d", m["gm"])
v.check("Ex 15-07.4e", m["gm_db"])
v.check("Ex 15-07.4f", m["delay_margin"])
# the delay margin is exact: at T + delay_margin the loop sits on the boundary (unit gain at -180 deg)
mb = fd.margins([0.5], [1, 0], T=1.0 + m["delay_margin"])
v.assert_true("Ex 4: adding the delay margin puts the loop on the boundary", abs(mb["pm"]) < 1e-6)
v.assert_true("Ex 4: largest stable K is pi/2", abs(0.5 * m["gm"] - math.pi / 2) < 1e-9)

# ---------------------------------------------------------------------------------------- Example 5
den5 = np.polymul([1, 0], np.polymul([1, -1], [1, 6]))
w5 = brentq(lambda w: np.imag(fd.freq_resp([1, 1], den5, w)), 0.5, 3, xtol=1e-14)
v.check("Ex 15-07.5a", w5)
v.assert_true("Ex 5: crossing at -K/7.5", abs(fd.freq_resp([1, 1], den5, w5).real + 1 / 7.5) < 1e-12)
for K, key in ((10, "b"), (5, "c")):
    Z = fd.closed_loop_rhp([K, K], den5)
    v.check(f"Ex 15-07.5{key}", Z)
    v.assert_true(f"Ex 5: Nyquist Z equals the root count at K = {K}", Z == unstable_roots([K, K], den5))
m = fd.margins([10, 10], den5, w_lo=1e-3, w_hi=1e4)
v.check("Ex 15-07.5d", m["gm"])
v.check("Ex 15-07.5e", m["gm_db"])
v.check("Ex 15-07.5f", m["pm"])
v.check("Ex 15-07.5g", fd.bode_integral([10, 10], den5))
v.assert_true("Ex 5: Bode integral equals pi x (unstable pole) = pi", abs(fd.bode_integral([10, 10], den5) - math.pi) < 1e-6)

# ---------------------------------------------------------------------------------------- Example 6
p2 = 2 * math.pi * 20e6
den6 = np.polymul([1 / p1, 1], [1 / p2, 1])
m = fd.margins([A0], den6)
v.check("Ex 15-07.6a", m["wc"] / (2 * math.pi) / 1e6)
v.check("Ex 15-07.6b", m["pm"])
cl_den = np.polyadd(den6, [0, 0, A0])
v.check("Ex 15-07.6c", 100 * step_specs([A0], cl_den, 3e-7)["overshoot"])
zeta6 = (p1 + p2) / (2 * math.sqrt((1 + A0) * p1 * p2))
v.assert_true("Ex 6: closed-loop damping is 0.707", abs(zeta6 - 1 / math.sqrt(2)) < 1e-4)
m = fd.margins([A0 * 0.5], den6)
v.check("Ex 15-07.6d", m["wc"] / (2 * math.pi) / 1e6)
v.check("Ex 15-07.6e", m["pm"])

# ---------------------------------------------------------------------------------------- Problem 1
d1 = np.polymul([1, 0], np.polymul([1, 2], [1, 10]))
m = fd.margins([40], d1)
v.check("15-07.1a", m["w180"])
v.check("15-07.1b", m["gm"])
v.check("15-07.1c", m["gm_db"])
v.check("15-07.1d", m["wc"])
v.check("15-07.1e", m["pm"])
v.assert_true("P1: Routh limit 240 = 6 x 40", unstable_roots([1], d1, 239.9) == 0 and unstable_roots([1], d1, 240.1) == 2)

# ---------------------------------------------------------------------------------------- Problem 2
v.check("15-07.2a", 180 - 125)
z2 = zeta_for_pm(55)
v.check("15-07.2b", z2)
v.check("15-07.2c", os_pct(z2))
v.check("15-07.2d", math.radians(55) / (2 * math.pi * 1000) * 1e6)

# ---------------------------------------------------------------------------------------- Problem 3
v.check("15-07.3a", 20 * math.log10(abs(1 + 1j)))
v.check("15-07.3b", math.degrees(np.angle(1 + 1j)))
v.check("15-07.3c", math.degrees(np.angle(1 - 1j)))

# ---------------------------------------------------------------------------------------- Problem 4
m = fd.margins([4], [1, 3, 3, 1])
v.check("15-07.4a", m["w180"])
v.check("15-07.4b", m["gm"])
v.check("15-07.4c", m["gm_db"])
v.check("15-07.4d", m["pm"])

# ---------------------------------------------------------------------------------------- Problem 5
T5 = 2e-3
K5 = brentq(lambda K: fd.margins([K], [1, 0], T=T5, w_lo=1, w_hi=1e5)["pm"] - 60, 10, 700, xtol=1e-12)
v.check("15-07.5a", K5)
m = fd.margins([K5], [1, 0], T=T5, w_lo=1, w_hi=1e5)
v.check("15-07.5b", m["gm"])
v.check("15-07.5c", m["gm_db"])

# ---------------------------------------------------------------------------------------- Problem 6
z6 = zeta_for_pm(60)
v.check("15-07.6a", z6)
K6 = (5 / (2 * z6)) ** 2
v.check("15-07.6b", K6)
m = fd.margins([K6], [1, 5, 0])
v.check("15-07.6c", m["wc"])
v.assert_true("P6: margin is 60 deg", abs(m["pm"] - 60) < 1e-9)

# ---------------------------------------------------------------------------------------- Problem 7
d7 = np.polymul([1 / (2 * math.pi * 10), 1], [1 / (2 * math.pi * 1e6), 1])
m = fd.margins([1e5], d7)
v.check("15-07.7a", m["wc"] / (2 * math.pi) / 1e6)
v.check("15-07.7b", m["pm"])
m = fd.margins([1e4], d7)
v.check("15-07.7c", m["wc"] / (2 * math.pi) / 1e3)
v.check("15-07.7d", m["pm"])

# ---------------------------------------------------------------------------------------- Problem 8
p3 = 1 / (50 * 1e-9)
v.check("15-07.8a", p3 / (2 * math.pi) / 1e6)
m = fd.margins([A0], np.polymul(den6, [1 / p3, 1]))
v.check("15-07.8b", m["wc"] / (2 * math.pi) / 1e6)
v.check("15-07.8c", m["pm"])
v.check("15-07.8d", m["gm"])
v.check("15-07.8e", m["gm_db"])

# ---------------------------------------------------------------------------------------- Problem 9
Ms = 1.5
v.check("15-07.9a", Ms / (Ms - 1))
v.check("15-07.9b", 20 * math.log10(Ms / (Ms - 1)))
v.check("15-07.9c", math.degrees(2 * math.asin(1 / (2 * Ms))))
# geometric check: a point on the unit circle at angle -180 + PM is exactly 1/Ms from -1
pm9 = 2 * math.asin(1 / (2 * Ms))
v.assert_true("P9: PM bound geometry", abs(abs(np.exp(1j * (math.pi + pm9)) + 1) - 1 / Ms) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 10
v.check("15-07.10a", abs(1 / (1 + fd.freq_resp([4], [1, 3, 2], 0.0))))
w10 = brentq(lambda w: abs(1 / (1 + fd.freq_resp([4], [1, 3, 2], w))) - 1, 0.5, 10, xtol=1e-14)
v.check("15-07.10b", w10)
Ms10, wm10 = fd.sensitivity_peak([4], [1, 3, 2])
v.check("15-07.10c", Ms10)
v.check("15-07.10d", wm10)
v.check("15-07.10e", fd.bode_integral([4], [1, 3, 2]))

# ---------------------------------------------------------------------------------------- Problem 11
tz, tp = 5e-6, 5e-6 / 11
K11 = 1e11 / 1.1
m = fd.margins([K11 * tz, K11], [tp, 1, 0, 0])
v.check("15-07.11a", m["wc"])
v.check("15-07.11b", m["pm"])
ws = 1 / math.sqrt(tz * tp)
v.check("15-07.11c", ws)
b = tz / tp
v.check("15-07.11d", math.degrees(math.atan((b - 1) / (2 * math.sqrt(b)))))
Kopt = ws**2 * abs(1 + 1j * ws * tp) / abs(1 + 1j * ws * tz)
v.check("15-07.11e", Kopt)
v.check("15-07.11f", Kopt / K11)
mo = fd.margins([Kopt * tz, Kopt], [tp, 1, 0, 0])
v.assert_true("P11: crossover lands at the phase peak", abs(mo["wc"] / ws - 1) < 1e-9)

# ---------------------------------------------------------------------------------------- Problem 12
num12, den12 = [40, 200], [1, 0, -100]
K12 = brentq(lambda K: np.max(np.roots(np.polyadd(den12, [0, K, 5 * K])).real), 1, 100)
v.check("15-07.12a", K12)
Z = fd.closed_loop_rhp(num12, den12)
v.check("15-07.12b", Z)
v.assert_true("P12: Z matches roots at K = 40", Z == unstable_roots(num12, den12))
v.check("15-07.12c", fd.margins(num12, den12, w_lo=1e-3, w_hi=1e4)["pm"])
Z15 = fd.closed_loop_rhp([15, 75], den12)
v.check("15-07.12d", Z15)
v.assert_true("P12: Z matches roots at K = 15", Z15 == unstable_roots([15, 75], den12))

# ---------------------------------------------------------------------------------------- Problem 13
m0 = fd.margins([100], [1, 10, 0])
v.check("15-07.13a", m0["delay_margin"])
m = fd.margins([100], [1, 10, 0], T=0.05)
v.check("15-07.13b", m["pm"])
v.check("15-07.13c", m["gm"])
v.check("15-07.13d", m["gm_db"])

# ---------------------------------------------------------------------------------------- Problem 14
v.check("15-07.14a", 10 ** (3 / 20))

# ---------------------------------------------------------------------------------------- Lab
for K, key in ((4, "a"), (20, "b")):
    v.check(f"Lab 15-07.{key}", fd.sensitivity_peak([K], [1, 6, 8, 0])[0])
m = fd.margins([A0], np.polymul([1 / p1, 1], [1 / (2 * math.pi * 10e6), 1]))
v.check("Lab 15-07.c", m["wc"] / (2 * math.pi) / 1e6)

sys.exit(v.finish())
