#!/usr/bin/env python3
"""Verify every published number in chapter 01-02, its solutions and its lab handout."""
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
    "01-02",
    COURSE / "chapters" / "01-02-limits-and-continuity.md",
    COURSE / "solutions" / "01-02-solutions.md",
    COURSE / "labs" / "01-02-lab" / "README.md",
)
x, h, n, t = sp.symbols("x h n t", real=True)
EPS = 2.22e-16


def lim(expr, var, at, direction="+-"):
    return float(sp.limit(expr, var, at, dir=direction))


# ---------------------------------------------------------------- chapter text tables
for xv, pub in [(0.5, 0.958851), (0.1, 0.998334), (0.01, 0.999983), (0.001, 0.9999998)]:
    v.assert_true(f"sin(x)/x table at {xv}", abs(math.sin(xv) / xv - pub) <= 0.5 * 10 ** -(len(str(pub)) - 2))
for hv, p2, p3 in [(0.1, 0.7177, 1.1612), (0.001, 0.6934, 1.0992)]:
    v.assert_true(f"(b^h-1)/h table at h={hv}",
                  round((2**hv - 1) / hv, 4) == p2 and round((3**hv - 1) / hv, 4) == p3)
v.assert_true("limits are ln 2 and ln 3", (round(math.log(2), 4), round(math.log(3), 4)) == (0.6931, 1.0986))
v.assert_true("sin(x)/x -> 1 (sympy)", sp.limit(sp.sin(x) / x, x, 0) == 1)
v.assert_true("(1-cos x)/x^2 -> 1/2 (sympy)", sp.limit((1 - sp.cos(x)) / x**2, x, 0) == sp.Rational(1, 2))
v.assert_true("(e^h-1)/h -> 1 (sympy)", sp.limit((sp.exp(h) - 1) / h, h, 0) == 1)
v.assert_true("(1+1/n)^n -> e (sympy)", sp.limit((1 + 1 / n) ** n, n, sp.oo) == sp.E)
v.assert_true("(sqrt(1+x)-1)/x -> 1/2", sp.limit((sp.sqrt(1 + x) - 1) / x, x, 0) == sp.Rational(1, 2))
v.assert_true("(3x^2+5)/(2x^2-x) -> 3/2", sp.limit((3 * x**2 + 5) / (2 * x**2 - x), x, sp.oo) == sp.Rational(3, 2))
v.assert_true("t^10 e^-t -> 0", sp.limit(t**10 * sp.exp(-t), t, sp.oo) == 0)
v.assert_true("e^-5 = 0.0067", round(math.exp(-5), 4) == 0.0067)
v.assert_true("sin(0.1)/0.1 = 0.99833", round(math.sin(0.1) / 0.1, 5) == 0.99833)

# ---------------------------------------------------------------- examples
v.check("Ex 01-02.1a", lim((x**2 - 4) / (x - 2), x, 2))
v.check("Ex 01-02.1b", lim(((2 + h) ** 2 - 4) / h, h, 0))
v.check("Ex 01-02.1c", (2.01**2 - 4) / 0.01)
v.check("Ex 01-02.2a", (1 + 1 / 12) ** 12)
v.check("Ex 01-02.2b", (1 + 1 / 365) ** 365)
v.check("Ex 01-02.2c", math.e)
v.check("Ex 01-02.2d", 100 * (math.exp(0.06) - 1))
v.assert_true("(1+1/n)^n increases toward e from below",
              all((1 + 1 / k) ** k < (1 + 1 / (k + 1)) ** (k + 1) < math.e for k in range(1, 400)))

R3, C3, V3 = 10e3, 100e-9, 5.0
tau3 = R3 * C3
v.check("Ex 01-02.3a", tau3 * 1e3)
v.check("Ex 01-02.3b", lim(V3 / R3 * sp.exp(-t / tau3), t, 0, "+") * 1e3)
v.check("Ex 01-02.3c", lim(V3 * (1 - sp.exp(-t / tau3)), t, sp.oo))
v.assert_true("v_C(0+) = 0", lim(V3 * (1 - sp.exp(-t / tau3)), t, 0, "+") == 0)

VT, IS = 0.02585, 1e-14


def g4(V):
    return (5 - V) / 1000 - IS * (math.exp(V / VT) - 1)


v.assert_true("g(0) = 5 mA > 0 and g(1) ≈ -6.3e2 A", math.isclose(g4(0), 5e-3) and round(g4(1), -1) == -630)
root4 = brentq(g4, 0, 1, xtol=1e-14)
v.check("Ex 01-02.4a", root4)
v.check("Ex 01-02.4b", (5 - root4) / 1000 * 1e3)
v.check("Ex 01-02.4c", math.ceil(math.log2(1 / 1e-3)))


def bisect(g, a, b, steps):
    for _ in range(steps):
        m = (a + b) / 2
        if g(m) > 0:
            a = m
        else:
            b = m
    return a, b


a10, b10 = bisect(g4, 0.0, 1.0, 10)
v.check("Ex 01-02.4d", (b10 - a10) * 1e3)
v.check("Ex 01-02.4e", a10)
v.check("Ex 01-02.4f", b10)
v.assert_true("root lies in the 10-step bracket", a10 <= root4 <= b10)
v.assert_true("KCL closes at the root: Is e^{V/VT} = 4.31 mA", round(IS * math.exp(root4 / VT) * 1e3, 2) == 4.31)


def lp_db(r):
    return 20 * math.log10(1 / math.sqrt(1 + r**2))


v.check("Ex 01-02.5a", lp_db(1))
v.check("Ex 01-02.5b", lp_db(10))
v.check("Ex 01-02.5c", -20 - lp_db(10))
v.check("Ex 01-02.5d", -(lp_db(100) - (-40)))
v.assert_true("asymptote error ≈ 4.34 (fc/f)^2 dB", math.isclose(10 / math.log(10), 4.343, rel_tol=1e-3))

# Amdahl (practitioner lens)
def amdahl(p, N):
    return 1 / ((1 - p) + p / N)


v.check("PL 01-02.a", amdahl(0.95, 8))
v.check("PL 01-02.b", amdahl(0.95, 64))
v.check("PL 01-02.c", amdahl(0.95, 1024))
v.check("PL 01-02.d", lim(1 / ((1 - sp.Rational(95, 100)) + sp.Rational(95, 100) / n), n, sp.oo))
v.assert_true("last 16x of hardware buys ~27 %", round(100 * (amdahl(0.95, 1024) / amdahl(0.95, 64) - 1)) == 27)

# concept-check numbers
v.assert_true("Q5: 21 bisection steps for 2 V -> 1 uV", math.ceil(math.log2(2 / 1e-6)) == 21)
v.assert_true("Q7: (e^h-1)/h at 1e-15 ≈ 1.11", round((math.exp(1e-15) - 1) / 1e-15, 2) == 1.11)
v.assert_true("Q8: Amdahl limit at p = 0.9 is 10", math.isclose(1 / (1 - 0.9), 10))

# ---------------------------------------------------------------- problems
v.check("01-02.1a", (math.exp(0.1) - 1) / 0.1)
v.check("01-02.1b", (math.exp(0.01) - 1) / 0.01)
v.check("01-02.1c", math.sin(0.3) / 0.1)
v.check("01-02.1d", math.sin(0.03) / 0.01)
v.check("01-02.1e", (1.1**3 - 1) / 0.1)
v.check("01-02.1f", (1.01**3 - 1) / 0.01)
v.assert_true("P1 left-side values 0.9516, 0.9950, 2.71, 2.9701",
              round((math.exp(-0.1) - 1) / -0.1, 4) == 0.9516 and round((math.exp(-0.01) - 1) / -0.01, 4) == 0.9950
              and round((0.9**3 - 1) / -0.1, 2) == 2.71 and round((0.99**3 - 1) / -0.01, 4) == 2.9701)

v.check("01-02.2a", lim((x**2 - 9) / (x - 3), x, 3))
v.check("01-02.2b", lim((sp.sqrt(4 + x) - 2) / x, x, 0))
v.check("01-02.2c", lim((x**2 + 3 * x + 2) / (x + 1), x, -1))
v.check("01-02.2d", lim(((1 + h) ** 3 - 1) / h, h, 0))
v.assert_true("P2(b) check at 0.01 = 0.24984", round((math.sqrt(4.01) - 2) / 0.01, 5) == 0.24984)

v.check("01-02.3a", lim(sp.sin(5 * x) / x, x, 0))
v.check("01-02.3b", lim(sp.tan(x) / x, x, 0))
v.check("01-02.3c", lim((1 - sp.cos(x)) / x**2, x, 0))
v.check("01-02.3d", lim(x / sp.sin(sp.pi * x), x, 0))

c = sp.symbols("c")
c_sol = sp.solve(sp.Eq(1**2, 2 * 1 + c), c)[0]
v.check("01-02.4a", float(c_sol))
v.check("01-02.4b", lim(x**2, x, 1, "-"))
v.check("01-02.4c", lim(2 * x, x, 1, "+"))
v.check("01-02.4d", lim(2 * x, x, 1, "+") - lim(x**2, x, 1, "-"))
v.check("01-02.4e", lim(sp.Abs(x) / x, x, 0, "-"))
v.check("01-02.4f", lim(sp.Abs(x) / x, x, 0, "+"))
v.check("01-02.4g", lim((x**2 - 9) / (x + 3), x, -3))

v.check("01-02.5a", lim((3 * x**2 + 5) / (2 * x**2 - x), x, sp.oo))
v.check("01-02.5b", lim((5 * x + 1) / (x**2 + 2), x, sp.oo))
v.check("01-02.5c", lim(sp.sqrt(x**2 + 4 * x) - x, x, sp.oo))
v.check("01-02.5d", lim(x * sp.exp(-x), x, sp.oo))
v.check("01-02.5e", lim(sp.log(x) / x, x, sp.oo))
v.assert_true("P5(c) check at 1e4 = 1.9998", round(math.sqrt(1e8 + 4e4) - 1e4, 4) == 1.9998)

tau7 = 0.030 / 6
i7 = lambda tt: 2 * (1 - math.exp(-tt / tau7))  # noqa: E731
vl7 = lambda tt: 12 * math.exp(-tt / tau7)  # noqa: E731
v.check("01-02.7a", tau7 * 1e3)
v.check("01-02.7b", i7(0.0), tol=1e-12)
v.check("01-02.7c", vl7(0.0))
v.check("01-02.7d", lim(2 * (1 - sp.exp(-t / tau7)), t, sp.oo))
v.check("01-02.7e", i7(0.010))
v.check("01-02.7f", vl7(0.010))
v.assert_true("P7 KVL at 10 ms", math.isclose(6 * i7(0.010) + vl7(0.010), 12.0))

for k, nn in zip("abcd", (1, 4, 12, 365)):
    v.check(f"01-02.8{k}", (1 + 0.06 / nn) ** nn)
v.check("01-02.8e", math.exp(0.06))
v.check("01-02.8f", (math.exp(0.06) - (1 + 0.06 / 365) ** 365) * 1e4)
r = sp.symbols("r", positive=True)
v.assert_true("(1 + r/n)^n -> e^r (sympy)", sp.simplify(sp.limit((1 + r / n) ** n, n, sp.oo) - sp.exp(r)) == 0)


def g9(V):
    return (3.3 - V) / 1e4 - 1e-15 * (math.exp(V / VT) - 1)


v.assert_true("P9 bracket: g(0) > 0 > g(1)", g9(0) > 0 > g9(1))
root9 = brentq(g9, 0, 1, xtol=1e-14)
v.check("01-02.9a", math.ceil(math.log2(1 / 1e-4)))
v.check("01-02.9b", root9)
v.check("01-02.9c", (3.3 - root9) / 1e4 * 1e3)
v.check("01-02.9d", root4 - root9)
I4, I9 = (5 - root4) / 1000, (3.3 - root9) / 1e4
v.assert_true("P9(d) decomposition: -decades*59.5 mV + 59.5 mV = dV",
              math.isclose(-math.log10(I4 / I9) * VT * math.log(10) + VT * math.log(10), root9 - root4, abs_tol=1e-9))
v.assert_true("P9(d) current ratio ≈ 16", round(I4 / I9) == 16)


def hp_db(r_):
    return 20 * math.log10(r_ / math.sqrt(1 + r_**2))


v.check("01-02.10a", hp_db(1))
v.check("01-02.10b", hp_db(0.1))
v.check("01-02.10c", hp_db(10))
v.check("01-02.11a", math.log(100))
v.assert_true("P11(a) limit is 0", sp.limit(x**2 * sp.sin(1 / x), x, 0) == 0)
v.assert_true("P11(c) limit is 0", sp.limit(sp.sin(x) / x, x, sp.oo) == 0)

v.check("01-02.12a", (1 - math.cos(0.1)) / 0.01)
v.check("01-02.12b", 2**-53 / 1e-10)
v.check("01-02.12c", 100 * 2**-53 / 1e-14)
v.check("01-02.12d", 2 * math.sin(0.5e-8) ** 2 / 1e-16)
v.assert_true("P12 naive value collapses to 0 at 1e-8", (1 - math.cos(1e-8)) / 1e-16 == 0.0)
naive7 = (1 - math.cos(1e-7)) / 1e-14
v.assert_true("P12 naive error at 1e-7 is within the 1.1 % bound", abs(naive7 - 0.5) / 0.5 <= 0.0111)

D = lambda hh: (math.exp(hh) - 1) / hh  # noqa: E731
v.check("01-02.13a", D(0.1))
v.check("01-02.13b", D(0.01))
v.check("01-02.13c", D(1e-5))
hstar = math.sqrt(2 * EPS)
v.check("01-02.13d", hstar)
v.check("01-02.13e", hstar / 2 + EPS / hstar)
v.check("01-02.13f", EPS / 1e-12)
err12 = abs(D(1e-12) - 1)
v.assert_true("P13(c) observed rounding error is the same order (1e-5..3e-4)", 1e-5 < err12 < 3e-4)
v.assert_true("P13 error ≈ h/2 for small h", math.isclose(D(1e-5) - 1, 0.5e-5, rel_tol=1e-3))
v.assert_true("P13(d) expm1 is accurate", abs(math.expm1(1e-12) / 1e-12 - 1) < 1e-11)

C1 = C2 = 10e-6
Vf = C1 * 5 / (C1 + C2)
v.check("01-02.14a", Vf)
Eb, Ea = 0.5 * C1 * 25, 0.5 * (C1 + C2) * Vf**2
v.check("01-02.14b", Eb * 1e6)
v.check("01-02.14c", Ea * 1e6)
v.check("01-02.14d", (Eb - Ea) * 1e6)
Cs = C1 * C2 / (C1 + C2)
v.check("01-02.14e", 1 * Cs * 1e6)
v.check("01-02.14f", 5 / 1)
v.check("01-02.14g", 0.01 * Cs * 1e9)
v.check("01-02.14h", 5 / 0.01)
Rs = sp.symbols("R", positive=True)
E_R = sp.integrate((5 / Rs) ** 2 * Rs * sp.exp(-2 * t / (Rs * sp.Rational(5, 10**6))), (t, 0, sp.oo))
v.assert_true("energy dissipated in R is 62.5 uJ for every R", sp.simplify(E_R - sp.Rational(625, 10**7)) == 0)

v.check("01-02.15a", 1024**2 / (1024 * 10))
v.check("01-02.15b", 2**40 / (2**20 * 20))
v.check("01-02.15c", math.log(1e10) / 1e10**0.1)
v.check("01-02.15d", brentq(lambda N: math.log(N) - N**0.1, 2, 10))
v.check("01-02.15e", brentq(lambda N: math.log(N) - N**0.1, 1e14, 1e17))
v.assert_true("N log N / N^2 -> 0", sp.limit(x * sp.log(x) / x**2, x, sp.oo) == 0)

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-02.a", math.ceil(math.log2(1 / 1e-6)))
v.check("Lab 01-02.b", V3 / R3 * math.exp(-1e-6 / tau3) * 1e3)
v.check("Lab 01-02.c", V3 * (1 - math.exp(-20e-3 / tau3)))
v.check("Lab 01-02.d", V3 * (1 - math.exp(-1e-6 / tau3)) * 1e3)

v.finish()
