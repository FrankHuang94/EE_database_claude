#!/usr/bin/env python3
"""Verify every published number in chapter 01-05, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-05",
    COURSE / "chapters" / "01-05-integrals.md",
    COURSE / "solutions" / "01-05-solutions.md",
    COURSE / "labs" / "01-05-lab" / "README.md",
)
x, t = sp.symbols("x t", real=True)


def sums(f, a, b, n):
    h = (b - a) / n
    xs = a + h * np.arange(n)
    left = h * f(xs).sum()
    right = h * f(xs + h).sum()
    mid = h * f(xs + h / 2).sum()
    return left, right, mid, (left + right) / 2


def integ(expr, a, b, var=x):
    return float(sp.integrate(expr, (var, a, b)))


# ---------------------------------------------------------------- theory identities
for f_, F_ in [(x**3, x**4 / 4), (1 / x, sp.log(x)), (sp.exp(3 * x), sp.exp(3 * x) / 3), (2**x, 2**x / sp.log(2)),
               (sp.sin(x), -sp.cos(x)), (sp.cos(x), sp.sin(x)), (sp.sec(x) ** 2, sp.tan(x)), (1 / (1 + x**2), sp.atan(x))]:
    v.assert_true(f"antiderivative of {f_}", sp.simplify(sp.diff(F_, x) - f_) == 0)
v.assert_true("FTC part 1 (symbolic)", sp.diff(sp.Integral(sp.cos(t**2), (t, 0, x)).doit(), x).simplify() == sp.cos(x**2))
v.assert_true("average of |sin| over a half period = 2/pi", sp.integrate(sp.sin(x), (x, 0, sp.pi)) / sp.pi == 2 / sp.pi)
v.assert_true("average of sin^2 over a period = 1/2", sp.integrate(sp.sin(x) ** 2, (x, 0, 2 * sp.pi)) / (2 * sp.pi) == sp.Rational(1, 2))
C, V = sp.symbols("C V", positive=True)
v.assert_true("w_C = integral of C v dv = CV^2/2", sp.integrate(C * x, (x, 0, V)) == C * V**2 / 2)
v.assert_true("1 Ah = 3600 C; 1 kWh = 3.6 MJ", math.isclose(1 * 3600, 3600) and math.isclose(1e3 * 3600, 3.6e6))

# ---------------------------------------------------------------- examples
L1, R1, M1, T1 = sums(lambda z: z**2, 0, 2, 4)
v.check("Ex 01-05.1a", L1)
v.check("Ex 01-05.1b", R1)
v.check("Ex 01-05.1c", M1)
v.check("Ex 01-05.1d", T1)
v.check("Ex 01-05.1e", integ(x**2, 0, 2))
v.assert_true("Ex1 errors +0.083 and -0.042", round(T1 - 8 / 3, 3) == 0.083 and round(M1 - 8 / 3, 3) == -0.042)

v.check("Ex 01-05.2a", 2e-3 * 5e-3 * 1e6)
v.check("Ex 01-05.2b", 2e-3 * 5e-3 / 1e-6)
v.check("Ex 01-05.2c", quad(lambda tt: 5e-3 * math.exp(-tt / 2e-3), 0, np.inf)[0] * 1e6)

C3, V3 = 100e-6, 5.0
Rs = sp.symbols("R", positive=True)
tau = Rs * C3
i3 = V3 / Rs * sp.exp(-t / tau)
w_R = sp.integrate(i3**2 * Rs, (t, 0, sp.oo))
w_S = sp.integrate(V3 * i3, (t, 0, sp.oo))
v.check("Ex 01-05.3a", 0.5 * C3 * V3**2 * 1e3)
v.check("Ex 01-05.3b", float(sp.simplify(w_S)) * 1e3)
v.check("Ex 01-05.3c", float(sp.simplify(w_R)) * 1e3)
v.assert_true("w_R independent of R", sp.diff(sp.simplify(w_R), Rs) == 0)

v.check("Ex 01-05.4a", quad(lambda th: abs(170 * math.sin(th)), 0, 2 * math.pi)[0] / (2 * math.pi))
v.check("Ex 01-05.4b", quad(lambda th: max(170 * math.sin(th), 0), 0, 2 * math.pi, points=[math.pi])[0] / (2 * math.pi))
v.check("Ex 01-05.4c", quad(lambda th: (2 * math.sin(th)) ** 2 * 10, 0, 2 * math.pi)[0] / (2 * math.pi))

q_hour = quad(lambda m: 5.0 if m < 2 else 0.5, 0, 60, points=[2])[0]  # mA*min
iavg = q_hour / 60
v.check("Ex 01-05.5a", iavg)
v.check("Ex 01-05.5b", 300 / iavg)
v.check("Ex 01-05.5c", 300 / iavg / 24)
v.check("Ex 01-05.5d", 100 * 0.010 / iavg)
v.check("Ex 01-05.5e", 100 * 10 / q_hour)
v.assert_true("drift over a week ≈ 1.7 mAh", round(0.010 * 168, 1) == 1.7)

# ---------------------------------------------------------------- problems
L, R, M, T = sums(np.exp, 0, 1, 4)
for k, val in zip("abcd", (L, R, M, T)):
    v.check(f"01-05.1{k}", val)
v.check("01-05.1e", math.e - 1)

v.check("01-05.2a", integ(sp.sqrt(x), 1, 4))
v.check("01-05.2b", integ(sp.sin(x), 0, sp.pi))
v.check("01-05.2c", integ(1 / x, 1, sp.E))
v.check("01-05.2d", integ(3 * x**2 - 2 * x + 1, 0, 2))
v.check("01-05.2e", integ(sp.exp(2 * x), 0, sp.log(2)))
v.check("01-05.2f", integ(sp.sec(x) ** 2, 0, sp.pi / 4))

G = sp.integrate(sp.log(t), (t, 1, x**2))
v.check("01-05.3a", float(sp.diff(G, x).subs(x, 2)))
v.assert_true("P3(c) derivative = -e^-x", sp.simplify(sp.diff(sp.integrate(sp.exp(-t), (t, x, 5)), x) + sp.exp(-x)) == 0)

v.assert_true("P4(a) odd integrand integrates to 0", abs(quad(lambda z: z**3 * math.cos(z), -1, 1)[0]) < 1e-14)
v.check("01-05.4a", integ(x**2, -2, 2))
v.check("01-05.4b", math.exp(-1))
v.check("01-05.4c", 1.0)
v.assert_true("P4(c) true value 0.7468 lies inside", round(quad(lambda z: math.exp(-z * z), 0, 1)[0], 4) == 0.7468)

Cc = 2e-6
v.check("01-05.5a", 1 + 10e-3 * 1e-3 / Cc)
v.check("01-05.5b", 1 + (10e-3 * 1e-3 - 5e-3 * 2e-3) / Cc)
v.check("01-05.5c", (10e-3 * 1e-3 - 5e-3 * 2e-3) * 1e6, tol=1e-9)

Lh = 10e-6
i2 = 0.5 + 5 * 2e-6 / Lh
v.check("01-05.6a", i2)
v.check("01-05.6b", i2 - 5 * 2e-6 / Lh)
tt = np.linspace(0, 4e-6, 400001)
itri = np.where(tt < 2e-6, 0.5 + 5 * tt / Lh, i2 - 5 * (tt - 2e-6) / Lh)
v.check("01-05.6c", np.trapezoid(itri, tt) / 4e-6)
v.check("01-05.6d", 0.5 * Lh * i2**2 * 1e6)

v.check("01-05.7a", 0.5 * 10e-6 * 144 * 1e3)
v.check("01-05.7b", 10e-6 * 144 * 1e3)
N_ = sp.symbols("N", positive=True, integer=True)
v.assert_true("stepped charging loses CV^2/(2N)", sp.simplify(N_ * sp.Rational(1, 2) * C * (V / N_) ** 2 - C * V**2 / (2 * N_)) == 0)

v.check("01-05.8a", quad(lambda z: math.sin(z) ** 2, 0, 2 * math.pi)[0] / (2 * math.pi))
v.check("01-05.8b", quad(lambda z: 3 * z, 0, 1)[0])
v.check("01-05.8c", 3.3 * 0.30)
v.check("01-05.8d", quad(lambda z: max(10 * math.sin(z), 0), 0, 2 * math.pi, points=[math.pi])[0] / (2 * math.pi))

q9 = 15 * 3 + 1.2 * 57
i9 = q9 / 60
v.check("01-05.9a", i9)
v.check("01-05.9b", 300 / i9)
v.check("01-05.9c", 300 / i9 / 24)
v.check("01-05.9d", 0.050 * 24)
v.check("01-05.9e", 100 * 0.050 * 24 / 300)
v.check("01-05.9h", 0.050 * 24 * 7)
v.check("01-05.9f", 300 / ((7.5 * 3 + 1.2 * 57) / 60))
v.check("01-05.9g", 300 / ((15 * 3 + 0.96 * 57) / 60))
v.assert_true("P9 bursts are 40 % of charge", round(100 * 45 / q9) == 40)


def trap(f, a, b, n):
    xs = np.linspace(a, b, n + 1)
    h = (b - a) / n
    return h * (f(xs).sum() - 0.5 * (f(xs[0]) + f(xs[-1])))


def midp(f, a, b, n):
    h = (b - a) / n
    return h * f(a + h * (np.arange(n) + 0.5)).sum()


T4, T8, M4 = trap(np.sin, 0, math.pi, 4), trap(np.sin, 0, math.pi, 8), midp(np.sin, 0, math.pi, 4)
v.check("01-05.10a", T4)
v.check("01-05.10b", 2 - T4)
v.check("01-05.10c", T8)
v.check("01-05.10d", 2 - T8)
v.check("01-05.10e", (2 - T4) / (2 - T8))
v.check("01-05.10f", M4)
v.check("01-05.10g", (2 * M4 + T4) / 3)

RC = 10e3 * 100e-9
v.check("01-05.11a", -0.5 * 2e-3 / RC)
v.check("01-05.11b", -0.5 / RC)
v.check("01-05.11c", 12 / (0.5 / RC) * 1e3)
v.check("01-05.11d", 1.0 * 0.5e-3 / RC)

v.check("01-05.12a", 0.35 * 20e-3 / 1.0 * 1e3)
v.check("01-05.12b", 0.35 * 20e-3 / 1.0 * 1e6)
A_, ph = sp.symbols("A phi", real=True)
v.assert_true("P12: 50 Hz integrates to zero over 20 ms",
              sp.simplify(sp.integrate(A_ * sp.sin(2 * sp.pi * 50 * t + ph), (t, 0, sp.Rational(1, 50)))) == 0)
v.assert_true("P12: 60 Hz does not cancel over 20 ms",
              abs(quad(lambda s: math.sin(2 * math.pi * 60 * s), 0, 0.02)[0]) > 1e-4)

A13 = sp.integrate(t**2 - 4, (t, 0, x))
v.check("01-05.13a", float(sp.solve(sp.diff(A13, x), x)[0]) if sp.solve(sp.diff(A13, x), x)[0] > 0
        else float(sp.solve(sp.diff(A13, x), x)[1]))
v.check("01-05.13b", float(A13.subs(x, 2)))
v.check("01-05.13c", float(max(sp.solve(A13, x))))

C0, a14 = 1e-6, -0.1
v.check("01-05.14a", quad(lambda vv: C0 * (1 + a14 * vv), 0, 5)[0] * 1e6)
v.check("01-05.14b", quad(lambda vv: vv * C0 * (1 + a14 * vv), 0, 5)[0] * 1e6)
v.check("01-05.14c", quad(lambda vv: C0 * (1 + a14 * vv), 0, 5)[0] / 5 * 1e6)

w = 2 * math.pi * 50
P_exact = quad(lambda s: 325 * math.sin(w * s) * 10 * math.sin(w * s - math.pi / 6), 0, 0.02)[0] / 0.02


def P_N(N, t0=0.0):
    tk = t0 + np.arange(N) * 0.02 / N
    return float((325 * np.sin(w * tk) * 10 * np.sin(w * tk - math.pi / 6)).mean())


v.check("01-05.15a", P_exact)
v.check("01-05.15b", P_N(80))
v.check("01-05.15c", P_N(3))
v.check("01-05.15d", P_N(2, 1e-3))
v.check("01-05.15e", P_exact / 1e3)

# ---------------------------------------------------------------- lab handout
week = 7 * 24  # hours
v.check("Lab 01-05.a", iavg * week)
v.check("Lab 01-05.b", 0.010 * week)
v.check("Lab 01-05.c", 0.01 * iavg * week)
v.check("Lab 01-05.d", min(n for n in range(1, 10) if all(abs(P_N(n, t0) - P_exact) < 1e-6 for t0 in np.linspace(0, 0.02, 37))))

v.finish()
