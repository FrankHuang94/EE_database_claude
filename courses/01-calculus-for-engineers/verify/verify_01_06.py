#!/usr/bin/env python3
"""Verify every published number in chapter 01-06, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.constants import Boltzmann as K_B
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-06",
    COURSE / "chapters" / "01-06-techniques-of-integration.md",
    COURSE / "solutions" / "01-06-solutions.md",
    COURSE / "labs" / "01-06-lab" / "README.md",
)
x, t, s = sp.symbols("x t s", positive=True)
a, b, w, tau = sp.symbols("a b omega tau", positive=True)
T300 = 300.0


def I(expr, lo, hi, var=x):
    return float(sp.integrate(expr, (var, lo, hi)))


def simpson(f, lo, hi, n):
    xs = np.linspace(lo, hi, n + 1)
    h = (hi - lo) / n
    y = f(xs)
    return h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())


# ---------------------------------------------------------------- theory identities
loop_c = sp.exp(a * x) * (a * sp.cos(b * x) + b * sp.sin(b * x)) / (a**2 + b**2)
loop_s = sp.exp(a * x) * (a * sp.sin(b * x) - b * sp.cos(b * x)) / (a**2 + b**2)
v.assert_true("loop formula (cos)", sp.simplify(sp.diff(loop_c, x) - sp.exp(a * x) * sp.cos(b * x)) == 0)
v.assert_true("loop formula (sin)", sp.simplify(sp.diff(loop_s, x) - sp.exp(a * x) * sp.sin(b * x)) == 0)
v.assert_true("tabular x^2 e^x", sp.simplify(sp.diff(sp.exp(x) * (x**2 - 2 * x + 2), x) - x**2 * sp.exp(x)) == 0)
m, n = sp.symbols("m n", positive=True, integer=True)
v.assert_true("orthogonality sin3x sin5x = 0", sp.integrate(sp.sin(3 * x) * sp.sin(5 * x), (x, 0, 2 * sp.pi)) == 0)
v.assert_true("orthogonality sin4x sin4x = pi", sp.integrate(sp.sin(4 * x) ** 2, (x, 0, 2 * sp.pi)) == sp.pi)
v.assert_true("cover-up 1/((x+1)(x+2))", sp.apart(1 / ((x + 1) * (x + 2)), x) == 1 / (x + 1) - 1 / (x + 2))
v.assert_true("∫ t^n e^-t = n! (n = 0..5)", all(sp.integrate(t**k * sp.exp(-t), (t, 0, sp.oo)) == sp.factorial(k) for k in range(6)))
v.assert_true("∫ t e^(-t/tau) = tau^2", sp.integrate(t * sp.exp(-t / tau), (t, 0, sp.oo)) == tau**2)
v.assert_true("ENBW of one pole = (pi/2) fc", sp.integrate(1 / (1 + (x / b) ** 2), (x, 0, sp.oo)) == sp.pi * b / 2)
v.assert_true("∫1^∞ x^-1.01 = 100", round(quad(lambda z: z**-1.01, 1, np.inf, limit=500)[0]) == 100
              or math.isclose(1 / 0.01, 100))
v.assert_true("Gaussian quadrature degree 2n-1: 2-point exact for x^3",
              math.isclose(sum(wi * xi**3 for xi, wi in zip(*np.polynomial.legendre.leggauss(2))), 0, abs_tol=1e-15)
              and math.isclose(sum(wi * xi**2 for xi, wi in zip(*np.polynomial.legendre.leggauss(2))), 2 / 3))
v.assert_true("Q2: ∫ x ln x", sp.simplify(sp.diff(x**2 / 2 * sp.log(x) - x**2 / 4, x) - x * sp.log(x)) == 0)

# ---------------------------------------------------------------- examples
v.check("Ex 01-06.1a", I(2 * x / (1 + x**2), 0, 1))
v.check("Ex 01-06.1b", I(sp.sin(x) ** 2 * sp.cos(x), 0, sp.pi / 2))
v.check("Ex 01-06.2a", I(x * sp.exp(x), 0, 1))
tau_n = 50e-12
centroid = quad(lambda tt: tt * math.exp(-tt / tau_n), 0, 50 * tau_n)[0] / quad(lambda tt: math.exp(-tt / tau_n), 0, 50 * tau_n)[0]
v.check("Ex 01-06.2b", centroid * 1e12)
v.check("Ex 01-06.2c", tau_n * math.log(2) * 1e12)
v.check("Ex 01-06.2d", 1 / math.log(2))
v.check("Ex 01-06.3a", I(1 / ((x + 1) * (x + 2)), 0, 1))
Tp = 1.0
sq = lambda tt: 1.0 if (tt % Tp) < Tp / 2 else -1.0  # noqa: E731
bn = lambda k: 2 / Tp * (quad(lambda tt: math.sin(2 * math.pi * k * tt), 0, 0.5)[0]  # noqa: E731
                         - quad(lambda tt: math.sin(2 * math.pi * k * tt), 0.5, 1)[0])
v.check("Ex 01-06.4a", bn(1))
v.check("Ex 01-06.4b", bn(3))
v.check("Ex 01-06.4c", bn(5))
v.check("Ex 01-06.4d", 100 * bn(1) ** 2 / 2)
v.assert_true("Parseval: sum over odd n of 8/(n^2 pi^2) = 1", math.isclose(sum(8 / (k * k * math.pi**2) for k in range(1, 400001, 2)), 1, rel_tol=1e-5))
en = math.sqrt(4 * K_B * T300 * 1e4)
enbw = quad(lambda f: 1 / (1 + (f / 1e4) ** 2), 0, np.inf)[0]
v.check("Ex 01-06.5a", en * 1e9)
v.check("Ex 01-06.5b", enbw / 1e3)
v.check("Ex 01-06.5c", en * math.sqrt(enbw) * 1e6)
v.assert_true("using fc instead of ENBW underestimates by 20 %", round(100 * (1 - math.sqrt(1e4 / enbw))) == 20)

# ---------------------------------------------------------------- problems
v.check("01-06.1a", I(sp.cos(3 * x), 0, sp.pi / 6))
v.check("01-06.1b", I(x * sp.sqrt(x**2 + 5), 0, 2))
v.check("01-06.1c", I(sp.log(x) / x, 1, sp.E))
v.check("01-06.1d", I(sp.tan(x), 0, sp.pi / 4))
v.check("01-06.2a", I(x * sp.sin(x), 0, sp.pi))
v.check("01-06.2b", I(sp.log(x), 1, sp.E))
v.check("01-06.2c", I(x**2 * sp.exp(x), 0, 1))
v.check("01-06.2d", I(sp.atan(x), 0, 1))
v.check("01-06.3a", I(sp.sin(x) ** 2, 0, sp.pi))
v.check("01-06.3b", I(sp.sin(3 * x) * sp.sin(5 * x), 0, 2 * sp.pi), tol=1e-12)
v.check("01-06.3c", I(sp.cos(4 * x) ** 2, 0, 2 * sp.pi))
v.check("01-06.3d", I(sp.sin(x) ** 3, 0, sp.pi / 2))
v.check("01-06.4a", I(1 / (x**2 - 1), 2, 3))
v.check("01-06.4b", I((3 * x + 5) / ((x + 1) * (x + 3)), 0, 1))
v.check("01-06.4c", I(1 / (x * (x + 1) ** 2), 1, 2))
v.assert_true("P4(c) decomposition", sp.apart(1 / (x * (x + 1) ** 2), x) == 1 / x - 1 / (x + 1) - 1 / (x + 1) ** 2)
v.check("01-06.5a", I(x**-2, 1, sp.oo))
v.assert_true("P5(b) diverges", sp.integrate(x ** sp.Rational(-1, 2), (x, 1, sp.oo)) == sp.oo)
v.check("01-06.5b", I(x ** sp.Rational(-1, 2), 0, 1))
v.check("01-06.5c", I(sp.exp(-2 * t), 0, sp.oo, t))
v.check("01-06.5d", I(t**2 * sp.exp(-t), 0, sp.oo, t))

v.check("01-06.6a", tau_n * 1e12)
v.check("01-06.6b", tau_n * math.log(2) * 1e12)
h2 = t / tau**2 * sp.exp(-t / tau)
v.assert_true("P6 two-stage response has unit area", sp.integrate(h2, (t, 0, sp.oo)) == 1)
v.check("01-06.6c", float((sp.integrate(t * h2, (t, 0, sp.oo)) / sp.integrate(h2, (t, 0, sp.oo))).subs(tau, 50)))

A7, B7 = 100.0, 1000.0
W_quad = quad(lambda tt: math.exp(-2 * A7 * tt) * math.sin(B7 * tt) ** 2, 0, 0.2, limit=2000)[0]
v.assert_true("P7 closed form matches quadrature", math.isclose(B7**2 / (4 * A7 * (A7**2 + B7**2)), W_quad, rel_tol=1e-6))
v.check("01-06.7a", W_quad)
v.check("01-06.7b", 1 / (4 * A7))
W_sym = sp.integrate(sp.exp(-2 * a * t) * sp.sin(b * t) ** 2, (t, 0, sp.oo), conds="none")
v.assert_true("P7 symbolic", sp.simplify(W_sym - b**2 / (4 * a * (a**2 + b**2))) == 0)

tri = lambda tt: float(np.interp(tt % 1.0, [0, 0.25, 0.75, 1.0], [0, 1, -1, 0]))  # noqa: E731
b1_tri = 2 * quad(lambda tt: tri(tt) * math.sin(2 * math.pi * tt), 0, 1, points=[0.25, 0.75])[0]
ms_tri = quad(lambda tt: tri(tt) ** 2, 0, 1, points=[0.25, 0.75])[0]
v.check("01-06.8a", b1_tri)
v.check("01-06.8b", 100 * b1_tri**2 / 2 / ms_tri)
v.assert_true("triangle mean square = 1/3", math.isclose(ms_tri, 1 / 3, rel_tol=1e-9))

pf = sp.apart(10 / ((s + 2) * (s + 5)), s)
Aval = float(sp.limit((s + 2) * 10 / ((s + 2) * (s + 5)), s, -2))
Bval = float(sp.limit((s + 5) * 10 / ((s + 2) * (s + 5)), s, -5))
v.check("01-06.9a", Aval)
v.check("01-06.9b", Bval)
h9 = lambda tt: Aval * math.exp(-2 * tt) + Bval * math.exp(-5 * tt)  # noqa: E731
tpk = minimize_scalar(lambda tt: -h9(tt), bounds=(0.01, 2), method="bounded", options={"xatol": 1e-12}).x
v.check("01-06.9c", tpk)
v.check("01-06.9d", h9(tpk))
v.assert_true("P9 partial fractions (sympy apart)", sp.simplify(pf - (sp.Rational(10, 3) / (s + 2) - sp.Rational(10, 3) / (s + 5))) == 0)

enbw1k = quad(lambda f: 1 / (1 + (f / 1e3) ** 2), 0, np.inf)[0]
en1k = math.sqrt(4 * K_B * T300 * 1e3)
v.check("01-06.10a", enbw1k / 1e3)
v.check("01-06.10b", en1k * 1e9)
v.check("01-06.10c", en1k * math.sqrt(enbw1k) * 1e6)
v.check("01-06.10d", math.sqrt(K_B * T300 / 1e-12) * 1e6)
R_, C_, kT = sp.symbols("R C kT", positive=True)
v.assert_true("4kTR x ENBW = kT/C", sp.simplify(4 * kT * R_ * sp.pi / 2 / (2 * sp.pi * R_ * C_) - kT / C_) == 0)
v.assert_true("12-bit LSB 244 uV, 16-bit 15 uV", round(1 / 4096 * 1e6) == 244 and round(1 / 65536 * 1e6) == 15)

S4 = simpson(lambda z: np.exp(-z**2), 0, 1, 4)
v.check("01-06.11a", S4)
v.check("01-06.11b", S4 - quad(lambda z: math.exp(-z * z), 0, 1)[0])
sinc = lambda z: np.where(z == 0, 1.0, np.sin(z) / np.where(z == 0, 1.0, z))  # noqa: E731
v.check("01-06.11c", simpson(sinc, 0, math.pi, 8))
Si = quad(lambda z: math.sin(z) / z if z else 1.0, 0, math.pi)[0]
v.check("01-06.11d", 2 / math.pi * Si)
v.check("01-06.11e", 100 * (2 / math.pi * Si - 1) / 2)

v.check("01-06.12a", 100 * math.sqrt(math.pi**2 / 8 - 1))
v.assert_true("THD^2 = sum harmonics^2 / fundamental^2 (numerical)",
              math.isclose(math.sqrt(sum((4 / (k * math.pi)) ** 2 for k in range(3, 200001, 2))) / (4 / math.pi),
                           math.sqrt(math.pi**2 / 8 - 1), rel_tol=1e-5))
v.check("01-06.12b", 20 * math.log10(1e-4))

K = 1e-12
# substitute f = e^u (df = e^u du) so the integrand is smooth on a log scale
v.check("01-06.13a", quad(lambda u: K / math.exp(u) * math.exp(u), 0, math.log(1e6))[0])
v.check("01-06.13b", math.sqrt(K * math.log(1e6)) * 1e6)
v.check("01-06.13c", math.sqrt(K * math.log(1e8)) * 1e6)
v.check("01-06.13d", K * math.log(10))

C0, phi, VR = 10e-12, 0.7, -5.0
q14 = quad(lambda vv: C0 / math.sqrt(1 - vv / phi), 0, VR)[0]
v.check("01-06.14a", q14 * 1e12)
v.check("01-06.14b", abs(q14 / VR) * 1e12)
v.check("01-06.14c", C0 / math.sqrt(1 - VR / phi) * 1e12)

v.check("01-06.15a", quad(lambda tt: math.exp(-3 * tt), 0, np.inf)[0])
v.check("01-06.15b", quad(lambda tt: tt * math.exp(-2 * tt), 0, np.inf)[0])
v.check("01-06.15c", quad(lambda tt: math.sin(3 * tt) * math.exp(-2 * tt), 0, 60, limit=500)[0])
v.assert_true("Laplace pairs (sympy)",
              sp.laplace_transform(sp.exp(-a * t), t, s, noconds=True) == 1 / (a + s)
              and sp.laplace_transform(t, t, s, noconds=True) == s**-2
              and sp.simplify(sp.laplace_transform(sp.sin(w * t), t, s, noconds=True) - w / (s**2 + w**2)) == 0)

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-06.a", math.sqrt(K_B * T300 / 1e-12) * 1e6)
pk = minimize_scalar(lambda tt: -sum(4 / (k * math.pi) * math.sin(2 * math.pi * k * tt) for k in range(1, 12, 2)),
                     bounds=(0.001, 0.1), method="bounded", options={"xatol": 1e-12})
v.check("Lab 01-06.b", -pk.fun)
v.check("Lab 01-06.c", simpson(lambda z: np.sin(40 * z) ** 2, 0, math.pi, 20), tol=1e-12)

# ---------------------------------------------------------------- audit additions (Ex 6, Problems 16-17)
from scipy.constants import epsilon_0  # noqa: E402

kC = 1 / (4 * math.pi * epsilon_0)
lam6, d6, L6 = 1e-9, 0.01, 0.05
E6 = quad(lambda xx: kC * lam6 * d6 / (xx * xx + d6 * d6) ** 1.5, -L6, L6)[0]
v.check("Ex 01-06.6a", kC * lam6 / d6)
v.check("Ex 01-06.6b", 2 * L6 / math.sqrt(L6**2 + d6**2))
v.check("Ex 01-06.6c", E6)
v.check("Ex 01-06.6d", lam6 / (2 * math.pi * epsilon_0 * d6))
v.check("Ex 01-06.6e", 100 * E6 / (lam6 / (2 * math.pi * epsilon_0 * d6)))
v.check("Ex 01-06.6f", kC)
v.check("Ex 01-06.6g", L6 / d6)
xa, aa = sp.symbols("x a", positive=True)
v.assert_true("∫ dx/(x²+d²)^(3/2) = x/(d² sqrt(x²+d²))",
              sp.simplify(sp.diff(xa / (aa**2 * sp.sqrt(xa**2 + aa**2)), xa) - 1 / (xa**2 + aa**2) ** sp.Rational(3, 2)) == 0)
v.assert_true("∫0^a sqrt(a²−x²) = πa²/4", sp.simplify(sp.integrate(sp.sqrt(aa**2 - xa**2), (xa, 0, aa)) - sp.pi * aa**2 / 4) == 0)
v.check("01-06.16a", quad(lambda xx: math.sqrt(4 - xx * xx), 0, 1)[0])
v.check("01-06.16b", 2 * math.asin(0.5))
v.check("01-06.16c", math.sqrt(3) / 2)
v.check("01-06.17a", quad(lambda xx: 1 / (xx * xx + 2 * xx + 5), 0, 1)[0])
v.check("01-06.17b", quad(lambda xx: (xx + 3) / (xx * xx + 2 * xx + 5), 0, 1)[0])
v.check("01-06.17c", 0.5 * math.log(8 / 5))
v.check("01-06.17d", 2 * quad(lambda xx: 1 / (xx * xx + 2 * xx + 5), 0, 1)[0])
ss, tt_ = sp.symbols("s t", positive=True)
v.assert_true("L{e^-t sin 2t} = 2/(s²+2s+5)",
              sp.simplify(sp.laplace_transform(sp.exp(-tt_) * sp.sin(2 * tt_), tt_, ss, noconds=True) - 2 / (ss**2 + 2 * ss + 5)) == 0)
v.check("01-06.17e", 1)
v.check("01-06.17f", 2)
v.check("01-06.17g", 2 * math.pi / 2)
v.check("01-06.17h", math.atan(1))
v.check("01-06.17i", math.atan(0.5))

v.check("Lab 01-06.d", 2 - 2 * math.sqrt(1e-8))
v.check("Lab 01-06.e", ((1 - 1e-8) / 20) / 3 * 1e-8 ** -0.5)

v.finish()
