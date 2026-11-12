#!/usr/bin/env python3
"""Verify every published number in chapter 01-03, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-03",
    COURSE / "chapters" / "01-03-derivatives.md",
    COURSE / "solutions" / "01-03-solutions.md",
    COURSE / "labs" / "01-03-lab" / "README.md",
)
x, t, h = sp.symbols("x t h", real=True)
EPS = 2.22e-16
VT = 0.02585


def d_at(expr, var, at):
    return float(sp.diff(expr, var).subs(var, at))


def d_def(expr, var, at):
    """Derivative from the limit definition (independent of the rules)."""
    return float(sp.limit((expr.subs(var, at + h) - expr.subs(var, at)) / h, h, 0))


# ---------------------------------------------------------------- rule identities (sympy)
f, g = sp.Function("f")(x), sp.Function("g")(x)
v.assert_true("product rule", sp.simplify(sp.diff(f * g, x) - (sp.diff(f, x) * g + f * sp.diff(g, x))) == 0)
v.assert_true("quotient rule",
              sp.simplify(sp.diff(f / g, x) - (sp.diff(f, x) * g - f * sp.diff(g, x)) / g**2) == 0)
for expr, der in [(sp.exp(x), sp.exp(x)), (sp.log(x), 1 / x), (sp.sin(x), sp.cos(x)), (sp.cos(x), -sp.sin(x)),
                  (sp.tan(x), 1 + sp.tan(x) ** 2), (sp.atan(x), 1 / (1 + x**2)), (sp.asin(x), 1 / sp.sqrt(1 - x**2)),
                  (2**x, 2**x * sp.log(2)), (sp.log(x, 10), 1 / (x * sp.log(10)))]:
    v.assert_true(f"d/dx {expr}", sp.simplify(sp.diff(expr, x) - der) == 0)
v.assert_true("derivative from definition: sin -> cos at 0.7",
              math.isclose(d_def(sp.sin(x), x, sp.Rational(7, 10)), math.cos(0.7), rel_tol=1e-12))
v.assert_true("secant slopes 5.5, 4.8, 4.3 at x = 2 (Figure 1)",
              [round(((2 + hh) ** 2 - 4) / hh, 1) for hh in (1.5, 0.8, 0.3)] == [5.5, 4.8, 4.3])
v.assert_true("sin returns after 4 derivatives", sp.diff(sp.sin(x), x, 4) == sp.sin(x))

# ---------------------------------------------------------------- examples
v.check("Ex 01-03.1a", d_def(sp.sqrt(x), x, 4))
v.check("Ex 01-03.1b", d_def(1 / x, x, 2))
w2 = 2 * math.pi * 1000
v.check("Ex 01-03.2a", 1e-6 * 5 * w2 * 1e3)
v.check("Ex 01-03.2b", 1e-6 * 5 / 1e-3 * 1e3)
v.assert_true("sine draws ~6.3x the ramp's peak current", round(5 * w2 / 5000, 1) == 6.3)
v.check("Ex 01-03.3a", 10e-3 * (0 - 0.1) / 1e-6)
v.check("Ex 01-03.3b", 10e-3 * (0 - 0.1) / 1e-6 * 0.1)
v.check("Ex 01-03.3c", 0.5 * 10e-3 * 0.1**2 * 1e6)
tau4, w4, C4 = 2e-3, 2 * math.pi * 500, 100e-9
v4 = 10 * sp.exp(-t / tau4) * sp.cos(w4 * t)
dv4 = sp.diff(v4, t)
v.check("Ex 01-03.4a", C4 * float(dv4.subs(t, 0)) * 1e3)
v.check("Ex 01-03.4b", float(dv4.subs(t, 0.5e-3)))
v.check("Ex 01-03.4c", C4 * float(dv4.subs(t, 0.5e-3)) * 1e3)
I5, Is5 = 1e-3, 1e-14
V5 = VT * math.log(I5 / Is5)
gd = Is5 / VT * math.exp(V5 / VT)
v.check("Ex 01-03.5a", gd * 1e3)
v.check("Ex 01-03.5b", 1 / gd)
v.check("Ex 01-03.5c", gd * 1e-3 * 1e6)
v.check("Ex 01-03.5d", 100 * math.expm1(1e-3 / VT))
v.check("Ex 01-03.5e", 0.6547 / VT)
v.assert_true("V at 1 mA is 0.6547 V (Ex 01-01.3)", round(V5, 4) == 0.6547)
v.assert_true("tangent underestimates by ~2 % of the change", round(100 * (1 - (1e-3 / VT) / math.expm1(1e-3 / VT))) == 2)

# numbers to know
v.check("N 01-03.a", VT / 1e-3)
v.check("N 01-03.b", 0.3e6 / (2 * math.pi * 10) / 1e3)
v.assert_true("1 uF at 1 V/us = 1 A; 1 uH at 1 A/us = 1 V", math.isclose(1e-6 * 1e6, 1) and math.isclose(1e-6 * 1e6, 1))
v.assert_true("~3.9 % current change per mV", round(100 * math.expm1(1e-3 / VT), 1) == 3.9)
v.assert_true("practitioner: 500 A in 1 us through 10 pH = 5 mV", math.isclose(10e-12 * 500 / 1e-6, 5e-3))
v.assert_true("Q6: r_d at 2 mA ≈ 12.9 ohm", round(VT / 2e-3, 1) == 12.9)

# ---------------------------------------------------------------- problems
v.check("01-03.1a", d_def(3 * x**2 - x, x, 1))
v.check("01-03.1b", d_def(1 / x, x, 2))
v.check("01-03.2a", d_at(4 * x**3 - 2 * x + 7, x, 2))
v.check("01-03.2b", d_at(x**-2, x, 1))
v.check("01-03.2c", d_at(sp.sqrt(x), x, 9))
v.check("01-03.2d", d_at(5 / x**3, x, 1))
v.check("01-03.3a", d_at(sp.exp(-3 * t), t, 0))
v.check("01-03.3b", d_at(sp.log(5 * x), x, 2))
v.check("01-03.3c", d_at(sp.sin(377 * t), t, 0))
v.check("01-03.3d", d_at(2**x, x, 3))
v.check("01-03.3e", d_at(sp.tan(x), x, sp.pi / 4))
v.check("01-03.4a", d_at(x**2 * sp.exp(x), x, 1))
v.check("01-03.4b", d_at(sp.sin(x) / x, x, sp.pi / 2))
v.check("01-03.4c", d_at((x + 1) / (x - 1), x, 3))
v.check("01-03.5a", d_at((3 * x + 1) ** 5, x, 0))
v.check("01-03.5b", d_at(sp.sqrt(1 + x**2), x, 1))
v.check("01-03.5c", d_at(sp.exp(-t**2), t, 1))
Vm, w, ph = sp.symbols("V_m omega phi")
v.assert_true("P5(d)", sp.simplify(sp.diff(Vm * sp.cos(w * t + ph), t) + Vm * w * sp.sin(w * t + ph)) == 0)

C7 = 10e-6
v.check("01-03.7a", C7 * 10 / 2e-3 * 1e3)
v.check("01-03.7b", C7 * -10 / 1e-3 * 1e3)
v.check("01-03.7c", 0.5 * C7 * 10**2 * 1e3)
v.check("01-03.7d", 5 * C7 * 10 / 2e-3)
v.check("01-03.7e", 10 * C7 * 10 / 2e-3)
v.assert_true("P7 energy over ramp = average power x time", math.isclose(0.25 * 2e-3, 0.5e-3))

v.check("01-03.8a", 1e6 / (2 * math.pi * 10) / 1e3)
v.check("01-03.8b", 1e6 / (2 * math.pi * 1) / 1e3)
v.check("01-03.8c", 0.3e6 / (2 * math.pi * 10) / 1e3)
w9 = 2 * math.pi * 50e3
v.check("01-03.9a", 100e-6 * 0.5 * w9)
v.check("01-03.9b", w9 * 100e-6)
v.check("01-03.9c", 8.7 / 4.7e-6 / 1e6)
v.check("01-03.9d", 8.7 / 4.7e-6 * 0.3e-6)

v10 = 5 * sp.exp(-200 * t) * sp.sin(1000 * t)
dv10 = sp.diff(v10, t)
v.check("01-03.10a", 2e-6 * float(dv10.subs(t, 0)) * 1e3)
t1 = brentq(lambda tt: float(dv10.subs(t, tt)), 1e-4, 2e-3)
v.check("01-03.10b", t1 * 1e3)
v.check("01-03.10c", float(v10.subs(t, t1)))
v.assert_true("P10 t1 = atan(5)/1000", math.isclose(t1, math.atan(5) / 1000, rel_tol=1e-9))

k, n_, V = sp.symbols("k n V", positive=True)
v.assert_true("elasticity of kx^n is n", sp.simplify(x / (k * x**n_) * sp.diff(k * x**n_, x)) == n_)
v.check("01-03.11a", 100 * (1 / 0.99**3 - 1))
v.check("01-03.11b", 100 * (1 / 1.05 - 1))
v.check("01-03.11c", 100 * (1 / 0.95 - 1))

v.check("01-03.12a", float(sp.solve(sp.Eq(2 * 3 + 2 * 4 * sp.Symbol("yp"), 0))[0]))
v.check("01-03.12b", d_at(sp.atan(x), x, 1))
I = sp.symbols("I", positive=True)
dVdI = sp.diff(VT * sp.log(I / 1e-14), I)
v.check("01-03.12c", float(dVdI.subs(I, 1e-3)))
v.check("01-03.12d", float(dVdI.subs(I, 10e-3)))

s_, c1 = math.sin, math.cos(1)
cen1 = (s_(1.1) - s_(0.9)) / 0.2
v.check("01-03.13a", cen1)
v.check("01-03.13b", (s_(1.01) - s_(0.99)) / 0.02)
v.check("01-03.13c", (s_(1.1) - s_(1)) / 0.1)
v.check("01-03.13d", -0.01 / 6 * c1)
v.check("01-03.13e", (3 * EPS) ** (1 / 3))
v.assert_true("P13 forward error ~48x central at h = 0.1",
              round(abs((s_(1.1) - s_(1)) / 0.1 - c1) / abs(cen1 - c1)) == 48)

sp_soft = sp.log(1 + sp.exp(x))
v.assert_true("softplus' = sigmoid", sp.simplify(sp.diff(sp_soft, x) - 1 / (1 + sp.exp(-x))) == 0)
v.check("01-03.14a", float(sp_soft.subs(x, 0)))
v.check("01-03.14b", d_at(sp_soft, x, 0))
v.check("01-03.14c", float(sp_soft.subs(x, 5)))
v.check("01-03.14d", d_at(sp_soft, x, 5))
v.check("01-03.14e", float(sp_soft.subs(x, 5)) - 5)

C15, Vm15, w15 = 1e-6, 170.0, 377.0
v.check("01-03.15a", C15 * Vm15 * w15 * 1e3)
tt = np.linspace(0, 2 * math.pi / w15, 200001)
p15 = Vm15 * np.sin(w15 * tt) * C15 * Vm15 * w15 * np.cos(w15 * tt)
v.check("01-03.15b", p15.max())
v.check("01-03.15c", (Vm15 / math.sqrt(2)) ** 2 * w15 * C15)
v.assert_true("P15 average power is zero", abs(np.trapezoid(p15, tt)) < 1e-6)

B = 20e6
snr_db = sp.symbols("x")
Cap = B * sp.log(1 + 10 ** (snr_db / 10), 2)
dC = sp.diff(Cap, snr_db)
v.check("01-03.16a", float(dC.subs(snr_db, 30)) / 1e6)
v.check("01-03.16b", float(dC.subs(snr_db, 0)) / 1e6)
v.check("01-03.16c", float(Cap.subs(snr_db, 31) - Cap.subs(snr_db, 30)) / 1e6)
v.assert_true("P16 +1 dB = 26 % more power; 6.6 Mb/s ≈ 3 % of 199 Mb/s",
              round(100 * (10**0.1 - 1)) == 26 and round(100 * 6.637 / 199.3) == 3)

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-03.a", VT / 2e-3)
v.check("Lab 01-03.b", 100 * ((5e-3 / VT) / math.expm1(5e-3 / VT) - 1))

v.finish()
