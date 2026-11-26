#!/usr/bin/env python3
"""Verify every number in chapter 25-01 (process flow overview), its problems and lab.

Independent routes (the lab module process.py uses closed forms):
- oxide thickness by integrating dx/dt = B/(A + 2x) numerically, and oxidation times by quadrature;
- the 0.379 RC distributed delay from the Fourier-series step response of an RC line;
- silicon consumption from atomic densities; wire resistance from cross-sections;
- Little's law by a discrete simulation of a fab; step yield by logarithms;
- recipe temperature by root-finding on the numerical oxidation time.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-01", ROOT / "chapters" / "25-01-process-flow-overview.md",
                        ROOT / "solutions" / "25-01-solutions.md", LAB / "README.md")

K_EV = 8.617333262e-5
DG = {"dry": (772.0, 1.23, 6.23e6, 2.0), "wet": (386.0, 0.78, 1.63e8, 2.05)}
MONTH = 365.25 / 12
YEAR_W = 365.25 / 7


def kt(tc):
    return K_EV * (tc + 273.15)


def coeffs(tc, amb):
    c1, e1, c2, e2 = DG[amb]
    b = c1 * math.exp(-e1 / kt(tc))
    ba = c2 * math.exp(-e2 / kt(tc)) / 1.68
    return b, ba, b / ba


def x_ode(t_h, tc, amb, xi=0.0):
    b, ba, a = coeffs(tc, amb)
    sol = integrate.solve_ivp(lambda t, x: b / (a + 2 * x), (0, t_h), [xi], rtol=1e-11, atol=1e-14)
    return float(sol.y[0, -1])


def t_quad(x, tc, amb, xi=0.0):
    """Time to grow from xi to x: integral of (A + 2x)/B dx."""
    b, ba, a = coeffs(tc, amb)
    return integrate.quad(lambda s: (a + 2 * s) / b, xi, x)[0]


def t50_over_rc():
    """50% crossing of the far end of an open RC line, from its Fourier-series step response."""
    n = np.arange(400)

    def vfar(s):
        return 1 - (4 / np.pi) * np.sum((-1) ** n / (2 * n + 1) * np.exp(-(2 * n + 1) ** 2 * np.pi**2 * s / 4))
    return optimize.brentq(lambda s: vfar(s) - 0.5, 0.05, 2)


T50 = t50_over_rc()
v.assert_true("distributed-line 50% delay is 0.379 RC", abs(T50 - 0.379) < 5e-4)


def r_um(w, h, tb, rho):
    return rho * 1e-8 / ((w - 2 * tb) * (h - tb) * 1e-18) * 1e-6


# ---------------------------------------------------------------- Example 1, text
v.check("Ex 25-01.1a", math.pi * 15**2)
v.check("Ex 25-01.1a1", (300 / 200) ** 2)
n_si = 8 / (0.5431e-7) ** 3
n_ox = 2.20 * 6.02214076e23 / 60.08
v.check("Ex 25-01.1b", n_si)
v.check("Ex 25-01.1b1", n_ox)
ratio = n_ox / n_si
v.check("Ex 25-01.1b2", ratio)
v.check("Ex 25-01.1c", 0.44 * 100)
v.check("Ex 25-01.1c1", 100 - 0.44 * 100)
v.check("Txt 25-01.a", 1 - ratio)
v.check("Txt 25-01.b", 1 / ratio)

# ---------------------------------------------------------------- Examples 2 and 3 (oxidation)
b, ba, a = coeffs(1000, "wet")
v.check("Ex 25-01.2a0", kt(1000))
v.check("Ex 25-01.2a", b)
v.check("Ex 25-01.2a1", ba)
v.check("Ex 25-01.2a2", a)
v.check("Ex 25-01.2b", t_quad(0.5, 1000, "wet"))
v.assert_true("ODE reaches 500 nm at the Deal-Grove time", abs(x_ode(t_quad(0.5, 1000, "wet"), 1000, "wet") - 0.5) < 1e-8)
v.check("Ex 25-01.2c", 0.5 / ba)
v.check("Ex 25-01.2c1", 0.25 / b)
bd, bad, ad = coeffs(1000, "dry")
v.check("Ex 25-01.3a", bd)
v.check("Ex 25-01.3a1", bad)
v.check("Ex 25-01.3a2", ad)
t_dry = t_quad(0.5, 1000, "dry")
v.check("Ex 25-01.3b", t_dry)
v.check("Ex 25-01.3c", t_dry / t_quad(0.5, 1000, "wet"))
v.check("Ex 25-01.3c1", b / bd)

# ---------------------------------------------------------------- Example 4 (gate trench)
v.check("Ex 25-01.4a", 16 - 2 * (1.8 + 3.0))
v.check("Ex 25-01.4a1", 16 - 2 * (1.8 + 4.5))
v.check("Ex 25-01.4b", (16 - 2 * 4.8) / (16 - 2 * 6.3))
v.check("Ex 25-01.4c", 2 * (1.8 + 4.5))

# ---------------------------------------------------------------- Example 5 (contacts), text
ac = 18e-7 * 40e-7
v.check("Ex 25-01.5a", ac)
v.check("Ex 25-01.5b", 1e-9 / ac)
v.check("Ex 25-01.5b1", 1e-8 / ac / 1e3)
for key, rc in (("Ex 25-01.5c", 1e-9 / ac), ("Ex 25-01.5c1", 1e-8 / ac)):
    # second route: solve I' = I(1 - gm Rs I'/I) self-consistently as a fixed point
    frac = optimize.brentq(lambda f: f - (1 - 1e-3 * rc * f), 0, 1)
    v.check(key, 100 * (1 - frac))
v.check("Txt 25-01.c", 100 * (1 - 1 / (1 + 1e-3 * 100)))
v.check("Txt 25-01.d", 100 * 2 / 14)

# ---------------------------------------------------------------- Example 6 (wire tiers)
tiers = {"": (20, 40, 2, 4.5), "1": (40, 80, 2, 2.8), "2": (400, 800, 2, 1.9)}
areas = {k: (w - 2 * tb) * (h - tb) for k, (w, h, tb, rho) in tiers.items()}
v.check("Ex 25-01.6a", areas[""])
v.check("Ex 25-01.6a1", r_um(*tiers[""]))
v.check("Ex 25-01.6a2", areas["1"])
v.check("Ex 25-01.6a3", r_um(*tiers["1"]))
v.check("Ex 25-01.6a4", areas["2"])
v.check("Ex 25-01.6a5", r_um(*tiers["2"]))
C1MM = 0.2e-15 * 1000
v.check("Ex 25-01.6b", T50 * r_um(*tiers[""]) * 1000 * C1MM * 1e9)
v.check("Ex 25-01.6b1", T50 * r_um(*tiers["1"]) * 1000 * C1MM * 1e9)
v.check("Ex 25-01.6b2", T50 * r_um(*tiers["2"]) * 1000 * C1MM * 1e12)
tof = 1e-3 * math.sqrt(3.0) / 2.99792458e8
v.check("Ex 25-01.6c", tof * 1e12)
v.check("Ex 25-01.6e", r_um(*tiers[""]) / r_um(*tiers["2"]))
v.check("Ex 25-01.6d", 800 / 40)

# ---------------------------------------------------------------- Example 7 (fab flow)
v.check("Ex 25-01.7a", math.exp(1000 * math.log(0.9999)))
v.check("Ex 25-01.7a1", math.exp(1000 * math.log(0.999)))
v.check("Ex 25-01.7b", 70 * 1.5)
v.check("Ex 25-01.7b1", 70 * 1.5 / 7)
m12 = 84 / MONTH
v.check("Ex 25-01.7c0", m12)
v.check("Ex 25-01.7c", 100000 * m12)
v.check("Ex 25-01.7c1", 100000 * m12 * 5000 / 1e9)
v.check("Ex 25-01.7d0", 12 / YEAR_W)
v.check("Ex 25-01.7d", 17e6 * 12 / YEAR_W)

# ---------------------------------------------------------------- Example 8 (density)
g_logic = optimize.brentq(lambda g: 1 / (0.5 / g + 0.5) - 1.15, 1.0, 3.0)
v.check("Ex 25-01.8a", g_logic)
v.check("Ex 25-01.8b", 313 / 238)

# ---------------------------------------------------------------- Problems 1-5
v.check("25-01.1a", math.pi * 10**2)
v.check("25-01.1a1", math.pi * 15**2)
v.check("25-01.1b", 1.5 / 2.25)
v.check("25-01.2a", 0.44 * 15)
v.check("25-01.2b", 15 - 0.44 * 15)
b3, ba3, a3 = coeffs(1100, "dry")
v.check("25-01.3a0", kt(1100))
v.check("25-01.3a", b3)
v.check("25-01.3a1", ba3)
v.check("25-01.3a2", a3)
v.check("25-01.3a3", b3)
v.check("25-01.3a4", ba3)
tau3 = t_quad(0.025, 1100, "dry")  # time-equivalent of the 25 nm patch
v.check("25-01.3b", tau3)
v.check("25-01.3b1", 1 + tau3)
x3 = optimize.brentq(lambda x: t_quad(x, 1100, "dry") - (1 + tau3), 0.025, 1)
v.check("25-01.3c", x3)
v.check("25-01.3c1", x3 * 1000)
x3_0 = x_ode(1.0, 1100, "dry")
v.check("25-01.3d0", x3_0 * 1000)
v.check("25-01.3d", (x3 - x3_0) * 1000)
v.assert_true("ODE from 25 nm matches the tau-shifted closed form", abs(x_ode(1.0, 1100, "dry", 0.025) - x3) < 1e-8)
b4, ba4, a4 = coeffs(1100, "wet")
v.check("25-01.4a", b4)
v.check("25-01.4a1", ba4)
v.check("25-01.4a0", b4)
v.check("25-01.4a2", ba4)
t4 = t_quad(0.5, 1100, "wet")
v.check("25-01.4b", t4)
v.check("25-01.4c", t_quad(0.5, 1000, "wet") / t4)
v.assert_true("at 1100 C wet, the parabolic term dominates the 500 nm time", 0.25 / b4 > 0.5 / ba4)
xe = optimize.brentq(lambda x: x**2 / b - x / ba, 1e-3, 5)  # equal parabolic and linear terms, wet 1000 C
v.check("25-01.5c", xe)

# ---------------------------------------------------------------- Problems 6-10
twf = (14 - 3.0) / 2 - 1.6
v.check("25-01.6a", twf)
v.check("25-01.6b", 3.0 + 2 * (1.6 + twf + 1.0))
v.check("25-01.7a", 80 * 1.2)
v.check("25-01.7a1", 80 * 1.2 / 7)
v.check("25-01.7b", 84 / 80)
a8 = 15e-7 * 30e-7
v.check("25-01.8a0", a8)
v.check("25-01.8a", 50 * a8)
v.check("25-01.8b", 100 * (1 - 1 / (1 + 1e-3 * 50)))
v.check("25-01.8c", 50 * a8 / 1e-9)
acu, aru = (12 - 4) * (24 - 2), 12 * 24
v.check("25-01.9a", acu)
v.check("25-01.9a1", aru)
r_ru = 7.0e-8 / (aru * 1e-18) * 1e-6
v.check("25-01.9b", r_ru)
v.check("25-01.9c", optimize.brentq(lambda rho: rho * 1e-8 / (acu * 1e-18) * 1e-6 - r_ru, 1, 20))
r_cu = 6.0e-8 / (acu * 1e-18) * 1e-6
v.check("25-01.9d", r_cu)
v.check("25-01.9d1", 100 * (1 - r_ru / r_cu))
v.check("25-01.9d2", 100 * (1 - acu / aru))
ri, rl = r_um(*tiers["1"]), r_um(*tiers[""])
v.check("25-01.10a0", ri * 2000 / 1e3)
v.check("25-01.10a", T50 * ri * 2000 * 400e-15 * 1e9)
v.check("25-01.10b0", rl * 2000 / 1e3)
v.check("25-01.10b", T50 * rl * 2000 * 400e-15 * 1e9)
v.check("25-01.10c", 4 * T50 * ri * 500 * 100e-15 * 1e9)

# ---------------------------------------------------------------- Problems 11-15
y11 = math.exp(math.log(0.95) / 1200)
v.check("25-01.11a", y11)
v.check("25-01.11a1", 1 - y11)
v.check("25-01.11b", math.exp(1200 * math.log(0.99995)))
m14 = 98 / MONTH
v.check("25-01.12a0", m14)
v.check("25-01.12a1", m12)
v.check("25-01.12a", 50000 * m14)
v.check("25-01.12a2", 50000 * m12)
v.check("25-01.12b", 50000 * (m14 - m12))
v.check("25-01.12b1", 50000 * (m14 - m12) * 6000 / 1e6)


def f_alpha(vdd):
    return (vdd - 0.30) ** 1.3 / vdd


fr = f_alpha(0.73) / f_alpha(0.70)
v.check("25-01.13a", fr)
v.check("25-01.13a1", 100 * (fr - 1))
v.check("25-01.14a", 1 / (0.5 / 1.6 + 0.3 + 0.2))
v.check("25-01.14b", 1 / (0.5 / 1.6 + 0.3 / 1.2 + 0.2))
t15 = optimize.brentq(lambda tc: t_quad(0.3, tc, "wet") - 1.0, 800, 1200)
v.check("25-01.15a", t15)
b15, ba15, _ = coeffs(t15, "wet")
v.check("25-01.15b", b15)
v.check("25-01.15b1", ba15)
v.check("25-01.15c", 0.09 / round(b15, 3) + 0.3 / round(ba15, 3))

# ---------------------------------------------------------------- Lab
v.check("Lab 25-01.a", x_ode(1.0, 1000, "wet") * 1000)
v.check("Lab 25-01.b", x_ode(1.0, 1000, "dry", 0.025) * 1000)
v.check("Lab 25-01.c", 3.0 + 2 * (1.8 + 4.5))
rg = r_um(*tiers["2"])
v.check("Lab 25-01.d", optimize.brentq(lambda L: T50 * rg * L * 0.2e-15 * L - L * 1e-6 * math.sqrt(3.0) / 2.99792458e8,
                                       10, 1e5) / 1000)
lam = 100000 / MONTH
v.check("Lab 25-01.e", lam * 84)
rng = np.random.default_rng(3)
days = 4000
n = rng.poisson(lam, days)
start = np.repeat(np.arange(days), n) + rng.random(n.sum())
finish = start + rng.exponential(84.0, start.size)  # a different distribution from the lab's gamma
tt = np.arange(800, days - 800)
wip = np.searchsorted(np.sort(start), tt) - np.searchsorted(np.sort(finish), tt)
v.assert_true("simulated WIP (exponential cycle times) within 1% of lambda*T", abs(wip.mean() / (lam * 84) - 1) < 0.01)

sys.exit(v.finish())
