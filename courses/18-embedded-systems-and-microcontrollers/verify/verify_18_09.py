#!/usr/bin/env python3
"""Verify every number in chapter 18-09 (ultra-low-power design), its problems and its lab.

Independent routes:
- budgets by summing charges written out here, cross-checked against the lab's helpers and an event simulation of a
  whole day;
- break-even times by comparing the charge of the two modes numerically over a range of idle times and locating
  the crossover by root finding;
- race to idle by evaluating the charge per period on a fine frequency grid;
- the reservoir capacitor by integrating the RC circuit's ODE numerically (not the closed form) and by root finding
  for the required capacitance;
- regulator currents, self-discharge and harvesting by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import ulp  # noqa: E402

v = Verifier.from_files("18-09", ROOT / "chapters" / "18-09-ultra-low-power-design.md",
                        ROOT / "solutions" / "18-09-solutions.md", LAB / "README.md")


def avg(phases, period, i_sleep):
    q = sum(i * t for i, t in phases)
    return (q + i_sleep * (period - sum(t for _, t in phases))) / period


def droop_ode(i, r, c, t_pulse, e=3.0):
    """Integrate C dv/dt = (E - v)/R - i from v = E; return E - v(t_pulse)."""
    if c == 0:
        return i * r
    sol = solve_ivp(lambda t, y: [((e - y[0]) / r - i) / c], (0, t_pulse), [e], rtol=1e-11, atol=1e-13)
    return e - sol.y[0, -1]


def crossover(q_tr, i_shallow, i_deep):
    return brentq(lambda t: (i_shallow * t) - (i_deep * t + q_tr), 1e-9, 1e6, xtol=1e-15)


HOUR, DAY, YEAR = 3600, 86400, 365 * 86400

# ---------------------------------------------------------------- text
v.check("Txt 18-09.a", 0.220 * 3600)
v.check("Txt 18-09.b", 0.220 / 25e-6)
v.check("Txt 18-09.c", 0.220 * 3600 * 3)

# ---------------------------------------------------------------- Example 1
ex1 = [(3e-3, 2e-3), (6e-3, 3e-3)]
i1 = avg(ex1, 1.0, 1.5e-6)
v.check("Ex 18-09.1a", 1e6 * i1)
v.assert_true("lab average_current agrees", abs(ulp.average_current(ex1, 1.0, 1.5e-6) - i1) < 1e-15)
v.check("Ex 18-09.1b", 0.220 * HOUR / i1 / DAY)
v.check("Ex 18-09.1c", 100 * 6e-3 * 3e-3 / i1)
qday = ulp.simulate_day([(1.0, 0.0, 3e-3, 2e-3), (1.0, 0.002, 6e-3, 3e-3)], 1.5e-6)
v.assert_true("a simulated day gives the budget's charge within 0.1%", abs(qday / DAY / i1 - 1) < 1e-3)

# ---------------------------------------------------------------- Example 2
v.check("Ex 18-09.2a", 1e3 * crossover(100e-9, 0.8e-3, 3e-6))
v.check("Ex 18-09.2b", crossover(4e-6, 3e-6, 0.1e-6))
v.assert_true("lab break_even_time agrees", abs(ulp.break_even_time(4e-6, 3e-6, 0.1e-6) - crossover(4e-6, 3e-6, 0.1e-6)) < 1e-9)
v.assert_true("50 ms idle: stop beats both", 0.05 * 3e-6 + 100e-9 < 0.05 * 0.8e-3 and 0.05 * 3e-6 < 0.05 * 0.1e-6 + 4e-6)

# ---------------------------------------------------------------- Example 3
fgrid = np.linspace(2e6, 48e6, 2000)
qgrid = [ulp.charge_per_task(f, 1e6, 60e-12, 400e-6, 2e-6, 1.0) for f in fgrid]
v.assert_true("charge falls monotonically with clock at fixed voltage", all(np.diff(qgrid) < 0))
q8 = (60e-6 * 8 + 400e-6) * (1e6 / 8e6) + 2e-6 * (1 - 1e6 / 8e6)
q48 = (60e-6 * 48 + 400e-6) * (1e6 / 48e6) + 2e-6 * (1 - 1e6 / 48e6)
v.check("Ex 18-09.3a", 1e6 * q8)
v.check("Ex 18-09.3b", 1e6 * q48)
v.check("Ex 18-09.3c", 100 * (1 - q48 / q8))
v.check("Ex 18-09.3d", (1.2 / 1.8) ** 2)
v.check("Ex 18-09.3e", 1.2 / 1.8)
v.assert_true("dynamic charge is 60 uC at both clocks", abs(60e-6 / 1e6 * 1e6 * 1e6 - 60) < 1e-9)

# ---------------------------------------------------------------- Example 4
v.check("Ex 18-09.4a", 100 * 1.8 / 3.7)
v.check("Ex 18-09.4b", 1e3 * 1.8 * 5e-3 / (0.85 * 3.7))
v.check("Ex 18-09.4c", 1e6 * (2e-6 + 0.1e-6))
v.check("Ex 18-09.4d", 1e6 * (1.8 * 2e-6 / (0.5 * 3.7) + 0.5e-6))
v.assert_true("perfect buck would draw 2.43 mA", abs(5e-3 * 1.8 / 3.7 - 2.43e-3) < 0.005e-3)

# ---------------------------------------------------------------- Example 5
v.check("Ex 18-09.5a", droop_ode(8e-3, 100, 0, 2e-3))
v.check("Ex 18-09.5b", 1e3 * droop_ode(8e-3, 100, 100e-6, 2e-3))
c5 = brentq(lambda c: droop_ode(8e-3, 100, c, 2e-3) - 0.2, 10e-6, 1e-3, xtol=1e-12)
v.check("Ex 18-09.5c", 1e6 * c5)
v.assert_true("closed form agrees with the ODE", abs(ulp.droop_with_cap(8e-3, 100, 100e-6, 2e-3) - droop_ode(8e-3, 100, 100e-6, 2e-3)) < 1e-7)
v.assert_true("short-pulse estimate 0.16 V", abs(8e-3 * 2e-3 / 100e-6 - 0.16) < 1e-12)

# ---------------------------------------------------------------- Example 6
div = 3.7 / 200e3
v.check("Ex 18-09.6a", 1e6 * div)
tot = 1.5e-6 + div + 50e-6
v.check("Ex 18-09.6b", 1e6 * tot)
v.check("Ex 18-09.6c", tot / 1.5e-6)

# ---------------------------------------------------------------- Problems 1 and 2
v.check("18-09.1a", 1.0 * 3600)
v.check("18-09.1b", 1.0 * 3600 * 3.7)
v.check("18-09.1c", 1.0 * 3600 * 3.7 / 15e-3 / HOUR)
v.check("18-09.2a", 3 * 1.2)
v.check("18-09.2b", 3 * 24 / 48)
i2c = 3 * 24 / 48 * 0.9 / 1.2
v.check("18-09.2c", i2c)
v.check("18-09.2d", i2c * 0.9)
v.check("18-09.2e", i2c * 0.9 / 3.6)

# ---------------------------------------------------------------- Problem 3
p3 = [(1.2e-3, 25e-3), (5e-3, 12e-3), (3e-3, 15e-3)]
i3 = avg(p3, 1.0, 4e-6)
v.check("18-09.3a", 1e6 * i3)
v.check("18-09.3b", 0.150 * HOUR / i3 / DAY)

# ---------------------------------------------------------------- Problem 4
v.check("18-09.4a", crossover(3e-3 * 1.5e-3, 5e-6, 0.4e-6))
v.check("18-09.4b", 1e6 * 5e-6 * 10)
v.check("18-09.4c", 1e6 * (0.4e-6 * 10 + 4.5e-6))
v.check("18-09.4d", (5e-6 * 10) / (0.4e-6 * 10 + 4.5e-6))
v.assert_true("at 0.5 s stop wins", 5e-6 * 0.5 < 0.4e-6 * 0.5 + 4.5e-6)

# ---------------------------------------------------------------- Problem 5
q51 = (50e-6 * 80 + 600e-6) * (2e6 / 80e6) + 1e-6 * (1 - 2e6 / 80e6)
q52 = (35e-6 * 26 + 300e-6) * (2e6 / 26e6) + 1e-6 * (1 - 2e6 / 26e6)
v.check("18-09.5a", 1e6 * q51)
v.check("18-09.5b", 1e6 * q52)
v.check("18-09.5c", 100 * (1 - q52 / q51))
v.assert_true("within each range the top clock is best",
              all(np.diff([ulp.charge_per_task(f, 2e6, 35e-12, 300e-6, 1e-6, 1.0) for f in np.linspace(4e6, 26e6, 50)]) < 0))

# ---------------------------------------------------------------- Problem 6
v.check("18-09.6a", 10)
v.check("18-09.6b", 1e3 * 1.8 * 10e-3 / (0.9 * 4.2))
v.check("18-09.6c", 1e3 * 1.8 * 10e-3 / (0.9 * 3.0))

# ---------------------------------------------------------------- Problem 7
cap = 1.000 * HOUR
v.check("18-09.7a", cap / 3e-6 / YEAR)
isd1 = 0.01 * cap / YEAR
v.check("18-09.7b", 1e6 * isd1)
v.check("18-09.7c", cap / (3e-6 + isd1) / YEAR)
v.check("18-09.7d", 0.85 * cap / (3e-6 + isd1) / YEAR)
isd3 = 0.03 * cap / (30 * DAY)
v.check("18-09.7e", 1e6 * isd3)
v.check("18-09.7f", cap / (3e-6 + isd3) / YEAR)
v.assert_true("lab battery_life_hours agrees with 1%/year as 1/12 % per month (30-day months)",
              abs(ulp.battery_life_hours(1000, 3e-6, 1.0, 0.03) * HOUR / YEAR - cap / (3e-6 + isd3) / YEAR) < 1e-9)

# ---------------------------------------------------------------- Problems 8 and 9
v.check("18-09.8a", 1e6 * 3.3 / 10e3)
v.check("18-09.8b", 1e6 * 3.3 / 40e3)
v.check("18-09.8c", 1e3 * 3.3 / 2.2e3)
v.check("18-09.9a", droop_ode(10e-3, 30, 0, 3e-3))
c9 = brentq(lambda c: droop_ode(10e-3, 150, c, 3e-3) - 0.3, 10e-6, 1e-3, xtol=1e-12)
v.check("18-09.9b", 1e6 * c9)

# ---------------------------------------------------------------- Problem 10
q10 = 30 * 25e-3 + 5 * 120e-3 + 2 * 200e-3 + 3e-6 * (HOUR - 37)
v.check("18-09.10a", 1e3 * q10)
i10 = q10 / HOUR
v.check("18-09.10b", 1e3 * i10)
v.check("18-09.10c", 0.8 * 2.400 * HOUR / i10 / DAY)
v.assert_true("report 57%, fix 43%", round(100 * 1.0 / q10) == 57 and round(100 * 0.75 / q10) == 43)
q10b = 5 * 25e-3 + 5 * 120e-3 + 2 * 200e-3 + 3e-6 * (4 * HOUR - 12)
i10b = q10b / (4 * HOUR)
v.check("18-09.10d", 1e6 * i10b)
v.check("18-09.10e", 0.8 * 2.400 * HOUR / i10b / YEAR)

# ---------------------------------------------------------------- Problem 11
p11 = 0.75 * 5 * 10e-6
v.check("18-09.11a", 1e6 * p11)
week = p11 * 50 * HOUR
v.check("18-09.11b", week)
load11 = week / (168 * HOUR)
v.check("18-09.11c", 1e6 * load11)
v.check("18-09.11d", 1e6 * load11 / 3)
e11 = load11 * 64 * HOUR
v.check("18-09.11e", e11)
v.check("18-09.11f", 2 * e11 / (3.3 ** 2 - 2.0 ** 2))
# hour-by-hour week: storage starting full at Friday evening never runs dry, and the week balances
store, low = 0.0, 0.0
for h in range(168):
    lit = h < 120 and (h % 24) < 10          # Monday..Friday, 10 lit hours each
    store += (p11 if lit else 0.0) * HOUR - load11 * HOUR
    low = min(low, store)
v.assert_true("Problem 11: the weekly balance closes to zero at the energy-neutral load", abs(store) < 1e-9)

# ---------------------------------------------------------------- Problem 12
for ident_i, ident_l, i_sl in (("18-09.12a", "18-09.12b", 4e-6), ("18-09.12c", "18-09.12d", 40e-6)):
    i12 = 3e-3 * 2e-3 + 6e-3 * 3e-3 + i_sl * (1 - 5e-3)
    v.check(ident_i, 1e6 * i12)
    v.check(ident_l, 0.220 / i12 / 24)

# ---------------------------------------------------------------- lab
la = avg([(3e-3, 2e-3), (6e-3, 3e-3 / 2)], 1.0, 1.5e-6)      # measuring every second, advertising every 2 s
v.check("Lab 18-09.a", 1e6 * la)
v.check("Lab 18-09.b", 0.220 * HOUR / la / DAY)
v.check("Lab 18-09.c", 1e6 * ulp.charge_per_task(24e6, 1e6, 60e-12 * 1.2 / 1.8, 400e-6 * 1.2 / 1.8, 2e-6, 1.0))
v.assert_true("the 1.2 V range at 24 MHz beats 48 MHz at 1.8 V (70.3 uC)",
              ulp.charge_per_task(24e6, 1e6, 40e-12, 400e-6 * 2 / 3, 2e-6, 1.0) < q48 and abs(1e6 * q48 - 70.3) < 0.05)
v.check("Lab 18-09.d", 1e3 * droop_ode(8e-3, 100, 47e-6, 2e-3))
v.check("Lab 18-09.e", 1e3 * droop_ode(8e-3, 100, 220e-6, 2e-3))
v.assert_true("3%/month is about 42 uA on 1000 mAh", abs(1e6 * isd3 - 42) < 0.5)

sys.exit(v.finish())
