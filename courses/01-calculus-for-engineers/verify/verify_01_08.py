#!/usr/bin/env python3
"""Verify every published number in chapter 01-08, its solutions and its lab handout."""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.special import iv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-08",
    COURSE / "chapters" / "01-08-sequences-series-and-taylor.md",
    COURSE / "solutions" / "01-08-solutions.md",
    COURSE / "labs" / "01-08-lab" / "README.md",
)
x, k, n = sp.symbols("x k n", positive=True)
VT = 0.02585


def bounce(Rs, Z0, RL, Vs=1.0, arrivals=1):
    Vl = Vs * Z0 / (Rs + Z0)
    gs, gl = (Rs - Z0) / (Rs + Z0), (RL - Z0) / (RL + Z0) if RL != float("inf") else 1.0
    return Vl, gs, gl, sum(Vl * (1 + gl) * (gs * gl) ** j for j in range(arrivals))


# ---------------------------------------------------------------- theory identities
for f, ser in [(sp.exp(x), sum(x**j / sp.factorial(j) for j in range(8))),
               (sp.sin(x), sum((-1) ** j * x ** (2 * j + 1) / sp.factorial(2 * j + 1) for j in range(4))),
               (sp.cos(x), sum((-1) ** j * x ** (2 * j) / sp.factorial(2 * j) for j in range(4))),
               (sp.log(1 + x), sum((-1) ** (j + 1) * x**j / j for j in range(1, 8))),
               (1 / (1 - x), sum(x**j for j in range(8))),
               (sp.sqrt(1 + x), 1 + x / 2 - x**2 / 8 + x**3 / 16)]:
    order = sp.Poly(ser, x).degree() + 1
    v.assert_true(f"Maclaurin series of {f}", sp.simplify(sp.series(f, x, 0, order).removeO() - ser) == 0)
aa, rr = sp.symbols("a r")
v.assert_true("finite geometric sum (n = 7)",
              sp.simplify(sum(aa * rr**j for j in range(7)) - aa * (1 - rr**7) / (1 - rr)) == 0)
v.assert_true("harmonic 1e6 terms ≈ 14.4", round(float(np.sum(1.0 / np.arange(1, 1_000_001))), 1) == 14.4)
v.assert_true("HD2/HD3 formulas from cos^2, cos^3 identities",
              sp.simplify(sp.cos(x) ** 3 - (sp.Rational(3, 4) * sp.cos(x) + sp.cos(3 * x) / 4)) == 0
              and sp.simplify(sp.cos(x) ** 2 - (1 + sp.cos(2 * x)) / 2) == 0)
th = np.linspace(0, 2 * np.pi, 4096, endpoint=False)
for A in (1e-3, 10e-3):
    Y = np.abs(np.fft.rfft(np.exp(A * np.cos(th) / VT)))
    v.assert_true(f"FFT HD2 equals Bessel ratio at {A*1e3:g} mV",
                  math.isclose(Y[2] / Y[1], iv(2, A / VT) / iv(1, A / VT), rel_tol=1e-9))
coef = sp.Poly(sp.series(1 / (1 + x**2), x, 0, 20).removeO(), x).all_coeffs()[::-1]
v.assert_true("1/(1+x^2) = 1 - x^2 + x^4 - ... (radius 1, poles at ±j)",
              all(coef[2 * j] == (-1) ** j for j in range(10)) and sp.solve(1 + x**2, x) == [])

# ---------------------------------------------------------------- examples
Vl, gs, gl, _ = bounce(10, 50, float("inf"))
v.check("Ex 01-08.1a", Vl)
v.check("Ex 01-08.1b", gs)
for j, key in enumerate("cdef", start=1):
    v.check(f"Ex 01-08.1{key}", bounce(10, 50, float("inf"), arrivals=j)[3])
v.check("Ex 01-08.1g", Vl * (1 + gl) / (1 - gs * gl))

T4 = sum(0.5**j / math.factorial(j) for j in range(5))
v.check("Ex 01-08.2a", T4)
v.check("Ex 01-08.2b", math.exp(0.5))
v.check("Ex 01-08.2c", math.exp(0.5) - T4)
v.check("Ex 01-08.2d", 2 * 0.5**5 / math.factorial(5))
v.check("Ex 01-08.2f", 3 / math.factorial(9))
v.check("Ex 01-08.2g", 3 / math.factorial(10))
v.check("Ex 01-08.2e", next(m for m in range(1, 30) if 3 / math.factorial(m) <= 1e-6))
v.assert_true("bound with e^0.5 < 2 still exceeds actual error", math.exp(0.5) - T4 < 2 * 0.5**5 / math.factorial(5))

A3, b3 = 1e5, 0.01
G3 = A3 / (1 + A3 * b3)
v.check("Ex 01-08.3a", G3)
v.check("Ex 01-08.3b", 100 * (G3 * b3 - 1))
v.check("Ex 01-08.3c", 100 / (A3 * b3))
v.assert_true("first-order and exact errors agree to ~1e-6", abs(1 / (A3 * b3) - (1 - G3 * b3)) < 1.1e-6)

v.check("Ex 01-08.4a", 0.1 - math.sin(0.1))
v.check("Ex 01-08.4b", 0.1**3 / 6)
v.check("Ex 01-08.4c", math.sqrt(1.02))
v.check("Ex 01-08.4d", -(0.02**2) / 8)
v.check("Ex 01-08.4e", 1.001**1000)

for A, a, b, c, d in [(1e-3, "a", "b", "c", "d"), (10e-3, "e", "f", "g", "h")]:
    xr = A / VT
    hd2, hd3 = xr / 4, xr * xr / 24
    v.check(f"Ex 01-08.5{a}", 100 * hd2)
    v.check(f"Ex 01-08.5{b}", 20 * math.log10(hd2))
    v.check(f"Ex 01-08.5{c}", hd3 if A == 1e-3 else 100 * hd3)
    v.check(f"Ex 01-08.5{d}", 20 * math.log10(hd3))
v.check("Ex 01-08.5i", 100 * iv(2, 10e-3 / VT) / iv(1, 10e-3 / VT))

# ---------------------------------------------------------------- problems
v.check("01-08.1a", float(sp.limit((2 * n + 1) / (3 * n - 2), n, sp.oo)))
v.check("01-08.1b", float(sp.limit((1 + 2 / n) ** n, n, sp.oo)))
v.check("01-08.1c", float(sp.summation(sp.Rational(1, 3) ** k, (k, 0, sp.oo))))
v.check("01-08.1d", float(sp.summation(sp.Rational(9, 10) ** k, (k, 1, sp.oo))))
v.check("01-08.1e", sum(2**j for j in range(10)))
v.check("01-08.2a", float(sp.summation(1 / k**2, (k, 1, sp.oo))))
v.check("01-08.2b", float(sp.summation(k / 2**k, (k, 1, sp.oo))))
v.check("01-08.2c", float(sp.summation((-1) ** (k + 1) / k, (k, 1, sp.oo))))
v.assert_true("P2(b) harmonic diverges", sp.summation(1 / k, (k, 1, sp.oo)) == sp.oo)
p3 = sum((-0.1) ** j / math.factorial(j) for j in range(4))
v.check("01-08.3a", p3)
v.check("01-08.3b", math.exp(-0.1))
v.check("01-08.4a", float(sp.limit(sp.Abs((1 / sp.Integer(3) ** k) / (1 / sp.Integer(3) ** (k + 1))), k, sp.oo)))

v.check("01-08.5a", float(sp.summation(sp.Rational(4, 5) ** k, (k, 0, sp.oo))))
v.check("01-08.5b", next(m for m in range(100) if 0.8**m < 0.01))
v.check("01-08.6a", sum(1.05**-j for j in range(1, 31)))
v.check("01-08.6b", float(sp.summation(sp.Rational(100, 105) ** k, (k, 1, sp.oo))))
v.check("01-08.6c", sum(1.08**-j for j in range(1, 11)))

c3 = 1 - 0.5**2 / 2 + 0.5**4 / 24
v.check("01-08.7a", c3)
v.check("01-08.7b", math.cos(0.5))
v.check("01-08.7c", c3 - math.cos(0.5))
v.check("01-08.7d", 0.5**6 / 720)
xm = math.pi / 2
terms = next(m for m in range(1, 20) if xm ** (2 * m + 1) / math.factorial(2 * m + 1) < 1e-6)
v.check("01-08.7e", terms)
xs = np.linspace(-xm, xm, 2001)
sin6 = sum((-1) ** j * xs ** (2 * j + 1) / math.factorial(2 * j + 1) for j in range(6))
sin5 = sum((-1) ** j * xs ** (2 * j + 1) / math.factorial(2 * j + 1) for j in range(5))
v.assert_true("6 terms suffice and 5 do not (actual max error)",
              np.max(np.abs(sin6 - np.sin(xs))) < 1e-6 < np.max(np.abs(sin5 - np.sin(xs))))

v.check("01-08.8a", 1 + 0.05 / 2)
v.check("01-08.8b", -(0.05**2) / 8)
v.check("01-08.8c", math.sqrt(1.05))
v.check("01-08.8d", 1 / 0.98)
v.check("01-08.8e", 0.02**2)
v.check("01-08.8f", 1.03**5)
v.check("01-08.8g", math.comb(5, 2) * 0.03**2)

for A, a, b in [(2e5, "a", "b"), (1000, "c", "d")]:
    G = A / (1 + A / 11)
    v.check(f"01-08.9{a}", G)
    v.check(f"01-08.9{b}", (1 - G / 11) * (1e6 if A == 2e5 else 100))

s10 = sum((1j * math.pi / 3) ** j / math.factorial(j) for j in range(7))
v.check("01-08.10a", abs(s10 - cmath.exp(1j * math.pi / 3)))
v.assert_true("Euler's formula (sympy)", sp.simplify(sp.exp(sp.I * x) - (sp.cos(x) + sp.I * sp.sin(x))) == 0)

D = lambda h: (math.exp(h) - 1) / h  # noqa: E731
C = lambda h: (math.exp(h) - math.exp(-h)) / (2 * h)  # noqa: E731
v.check("01-08.11a", D(0.1) - 1)
v.check("01-08.11b", C(0.1) - 1)
v.check("01-08.11c", (4 * C(0.05) - C(0.1)) / 3 - 1)

a1, a3 = 1.0, -0.05
v.check("01-08.12a", a1 * 1 + 0.75 * a3 * 1)
v.check("01-08.12b", 100 * abs(0.25 * a3) / (a1 + 0.75 * a3))
A1 = brentq(lambda A: 20 * math.log10(1 + 0.75 * a3 * A**2 / a1) + 1, 0.1, 3)
AIP3 = math.sqrt(4 / 3 * abs(a1 / a3))
v.check("01-08.12c", A1)
v.check("01-08.12d", AIP3)
v.check("01-08.12e", 20 * math.log10(AIP3 / A1))
y = 1.7 * np.cos(th) - 0.05 * (1.7 * np.cos(th)) ** 3
Y = np.abs(np.fft.rfft(y)) / 2048
v.assert_true("cubic: fundamental gain at the 1 dB point is -1.00 dB (FFT, 1.703 V)",
              round(20 * math.log10((np.abs(np.fft.rfft(A1 * np.cos(th) - 0.05 * (A1 * np.cos(th)) ** 3)) / 2048)[1] / A1), 2) == -1.00)

v.check("01-08.13a", 100 * (1e-3 / VT) / 4)
v.check("01-08.13b", 100 * iv(2, 1e-3 / VT) / iv(1, 1e-3 / VT))
v.check("01-08.13c", 100 * iv(2, 1.0) / iv(1, 1.0))
v.check("01-08.13d", 1e3 * brentq(lambda A: 1 - (iv(2, A / VT) / iv(1, A / VT)) / (A / VT / 4) - 0.01, 1e-3, 25e-3))

v.check("01-08.14a", math.ceil((4 / 1e-6 - 1) / 2))


def atan_s(z, N):
    return sum((-1) ** j * z ** (2 * j + 1) / (2 * j + 1) for j in range(N))


pm = 16 * atan_s(1 / 5, 5) - 4 * atan_s(1 / 239, 5)
v.check("01-08.14b", pm)
v.check("01-08.14c", pm - math.pi)

Vl2, gs2, gl2, _ = bounce(25, 50, 100)
v.check("01-08.15a", Vl2)
v.check("01-08.15b", gs2)
v.check("01-08.15c", gl2)
vinf = Vl2 * (1 + gl2) / (1 - gs2 * gl2)
v.check("01-08.15d", vinf)
v.assert_true("matches DC divider", math.isclose(vinf, 100 / 125))
v.check("01-08.15e", next(m for m in range(1, 20) if abs(bounce(25, 50, 100, arrivals=m)[3] - vinf) / vinf < 0.01))

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-08.a", 100 * iv(2, 3e-3 / VT) / iv(1, 3e-3 / VT))
Y17 = np.abs(np.fft.rfft(1.7 * np.cos(th) - 0.05 * (1.7 * np.cos(th)) ** 3)) / 2048
v.check("Lab 01-08.b", 20 * math.log10(Y17[1] / 1.7))
v.check("Lab 01-08.c", 1e4 / (1 + 1e4 * 0.01))

# ---------------------------------------------------------------- audit additions
v.check("01-08.4b", float(sp.limit(sp.Abs(k / (k + 1)), k, sp.oo)) ** -1)
v.check("01-08.4c", 0)
v.check("01-08.9e", 100 * 11 / 1000)
v.check("01-08.9f", 100 * 11 / 1000 - 100 * (1 - (1000 / (1 + 1000 / 11)) / 11))
v.check("01-08.9g", 1e4 * 11)
v.check("01-08.9h", 20 * math.log10(1.1e5))
v.check("01-08.10b", s10.real)
v.check("01-08.10c", s10.imag)
v.check("01-08.12f", 100 * abs(a3) / (4 * a1))
v.check("01-08.12g", (AIP3 / A1) ** 2)
for _id, _A, kind in [("e", 5e-3, "t"), ("f", 5e-3, "x"), ("g", 10e-3, "t"), ("h", 10e-3, "x"), ("i", VT, "t")]:
    val = 100 * (_A / VT) / 4 if kind == "t" else 100 * iv(2, _A / VT) / iv(1, _A / VT)
    v.check(f"01-08.13{_id}", val)
sums = [bounce(25, 50, 100, arrivals=m)[3] for m in (1, 2, 3)]
for _id, val in zip("fgh", sums):
    v.check(f"01-08.15{_id}", val)
for _id, val in zip("ijk", sums):
    v.check(f"01-08.15{_id}", 100 * abs(val - vinf) / vinf)
kk = sp.symbols("kk", integer=True, positive=True)
v.check("01-08.16a", float(sp.summation(1 / (kk**2 + 3 * kk), (kk, 1, sp.oo))))
v.assert_true("16(b) limit-comparison ratio 1/2, (d) root-test limit 1/2",
              sp.limit(kk / (2 * kk + 1), kk, sp.oo) == sp.Rational(1, 2))
S10 = sum(1 / j**3 for j in range(1, 11))
z3 = float(sp.zeta(3))
v.check("01-08.17a", S10)
v.check("01-08.17b", 1 / (2 * 11**2))
v.check("01-08.17c", 1 / (2 * 10**2))
v.check("01-08.17d", S10 + 1 / 242)
v.check("01-08.17e", S10 + 1 / 200)
v.check("01-08.17f", S10 + (1 / 242 + 1 / 200) / 2)
v.check("01-08.17g", abs(S10 + (1 / 242 + 1 / 200) / 2 - z3))
v.check("01-08.17h", z3 - S10)
v.check("01-08.17i", math.ceil(math.sqrt(0.5e6)))
v.assert_true("true sum inside the bracket", S10 + 1 / 242 <= z3 <= S10 + 1 / 200)

v.finish()
