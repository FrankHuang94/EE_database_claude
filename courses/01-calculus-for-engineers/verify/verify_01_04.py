#!/usr/bin/env python3
"""Verify every published number in chapter 01-04, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import sympy as sp
from scipy.constants import epsilon_0
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-04",
    COURSE / "chapters" / "01-04-applications-of-derivatives.md",
    COURSE / "solutions" / "01-04-solutions.md",
    COURSE / "labs" / "01-04-lab" / "README.md",
)
x, t, R, n_ = sp.symbols("x t R n", positive=True)


def argmin(f, lo, hi):
    return minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-12}).x


# ---------------------------------------------------------------- theory identities
Vs, Rs, RL = sp.symbols("V_s R_s R_L", positive=True)
P = Vs**2 * RL / (Rs + RL) ** 2
v.assert_true("dP/dRL = Vs^2 (Rs - RL)/(Rs + RL)^3",
              sp.simplify(sp.diff(P, RL) - Vs**2 * (Rs - RL) / (Rs + RL) ** 3) == 0)
v.assert_true("Pmax = Vs^2/(4 Rs)", sp.simplify(P.subs(RL, Rs) - Vs**2 / (4 * Rs)) == 0)
a, b = sp.symbols("a b", positive=True)
g = a * x + b / x
xs = sp.solve(sp.diff(g, x), x)[0]
v.assert_true("balance principle: x* = sqrt(b/a), g = 2 sqrt(ab)",
              sp.simplify(xs - sp.sqrt(b / a)) == 0 and sp.simplify(g.subs(x, xs) - 2 * sp.sqrt(a * b)) == 0)
A, B, V = sp.symbols("A B V", positive=True)
E = A * V**2 + B / V
Vst = sp.solve(sp.diff(E, V), V)[0]
v.assert_true("V* = (B/2A)^(1/3)", sp.simplify(Vst - (B / (2 * A)) ** sp.Rational(1, 3)) == 0)
v.assert_true("leakage = 2 x switching at V*", sp.simplify((B / V) / (A * V**2)).subs(V, Vst).simplify() == 2)
v.assert_true("reciprocal Newton: eps_{k+1} = eps_k^2",
              sp.expand(1 - a * x * (2 - a * x) - (1 - a * x) ** 2) == 0)
tau, tau2 = sp.symbols("tau tau2", positive=True)
h2 = (sp.exp(-t / tau) - sp.exp(-t / tau2)) / (tau - tau2)
v.assert_true("L'Hopital limit of two-tau response", sp.simplify(sp.limit(h2, tau2, tau) - t / tau**2 * sp.exp(-t / tau)) == 0)
v.assert_true("(e^x - 1 - x)/x^2 -> 1/2", sp.limit((sp.exp(x) - 1 - x) / x**2, x, 0) == sp.Rational(1, 2))

# ---------------------------------------------------------------- examples
Pf = lambda rl, vs=10.0, rs=50.0: vs**2 * rl / (rs + rl) ** 2  # noqa: E731
r_opt = argmin(lambda r: -Pf(r), 1, 1000)
v.check("Ex 01-04.1a", r_opt)
v.check("Ex 01-04.1b", Pf(r_opt))
v.check("Ex 01-04.1c", 100 * r_opt / (50 + r_opt))
v.check("Ex 01-04.1d", Pf(100))
v.check("Ex 01-04.1e", 100 * Pf(100) / Pf(50))
v.assert_true("load voltage at match is 5 V", math.isclose(10 * 50 / 100, 5))

Ef = lambda vv, A_=1.0, B_=0.05: A_ * vv**2 + B_ / vv  # noqa: E731
vst = argmin(Ef, 0.05, 2)
v.check("Ex 01-04.2a", vst)
v.check("Ex 01-04.2b", Ef(vst))
v.check("Ex 01-04.2c", Ef(1.0) / Ef(vst))
v.check("Ex 01-04.2d", (0.05 / vst) / (vst**2))
v.assert_true("E''(V*) = 6.0", round(2 + 2 * 0.05 / vst**3, 1) == 6.0)

fc = 1 / (2 * math.pi * 10e3 * 10e-9)
v.check("Ex 01-04.3a", fc)
v.check("Ex 01-04.3b", fc * 0.06)
v.check("Ex 01-04.3c", fc * math.hypot(0.01, 0.05))
v.check("Ex 01-04.3d", 100 * (1 / (0.99 * 0.95) - 1))
v.check("Ex 01-04.3e", 100 * (1 / (1.01 * 1.05) - 1))
v.assert_true("1 % capacitor cuts the spread ~3.5x", round(math.hypot(1, 5) / math.hypot(1, 1), 1) == 3.6
              or round(math.hypot(1, 5) / math.hypot(1, 1), 1) == 3.5)

xk, xs2, it = 1.0, math.sqrt(2), []
for _ in range(4):
    xk = (xk + 2 / xk) / 2
    it.append(xk)
v.check("Ex 01-04.4a", it[2])
v.check("Ex 01-04.4b", it[2] - xs2)
v.check("Ex 01-04.4c", it[3] - xs2)
v.assert_true("Ex4 table: 1.5, 1.416667, errors 8.58e-2, 2.45e-3",
              it[0] == 1.5 and round(it[1], 6) == 1.416667 and round(it[0] - xs2, 4) == 0.0858
              and round(it[1] - xs2, 5) == 0.00245)
v.assert_true("Ex4 theory: 0.354 x (2.12e-6)^2 = 1.59e-12", round(0.354 * 2.12e-6**2 / 1e-12, 2) == 1.59)

hlim = lambda tt, ta=1e-3: tt / ta**2 * math.exp(-tt / ta)  # noqa: E731
t_pk = argmin(lambda tt: -hlim(tt), 1e-5, 5e-3)
v.check("Ex 01-04.5a", t_pk * 1e3)
v.check("Ex 01-04.5b", hlim(t_pk))
v.check("Ex 01-04.5c", (math.exp(-1) - math.exp(-1 / 1.001)) / (1e-3 - 1.001e-3))

# ---------------------------------------------------------------- problems
f1 = lambda xx: xx**3 - 3 * xx  # noqa: E731
v.check("01-04.1a", f1(-1))
v.check("01-04.1b", f1(1))
v.check("01-04.1c", max(f1(-2), f1(-1), f1(1), f1(3)))
v.check("01-04.1d", min(f1(-2), f1(-1), f1(1), f1(3)))

f2 = x * sp.exp(-x)
x_max = sp.solve(sp.diff(f2, x), x)[0]
x_inf = sp.solve(sp.diff(f2, x, 2), x)[0]
v.check("01-04.2a", float(f2.subs(x, x_max)))
v.check("01-04.2b", float(f2.subs(x, x_inf)))
v.check("01-04.2c", float(sp.limit(f2, x, sp.oo)))

v.check("01-04.3a", float(sp.limit((sp.exp(x) - 1 - x) / x**2, x, 0)))
v.check("01-04.3b", float(sp.limit(x * sp.log(x), x, 0, "+")))
v.check("01-04.3c", float(sp.limit(sp.log(x) / (x - 1), x, 1)))
v.check("01-04.3d", float(sp.limit((1 - sp.cos(3 * x)) / x**2, x, 0)))
v.check("01-04.3e", float(sp.limit(x ** (1 / x), x, sp.oo)))

v.check("01-04.4a", 2 + 0.1 / 4)
v.check("01-04.4b", math.sqrt(4.1))
v.check("01-04.4c", 0.5 * float(sp.diff(sp.sqrt(x), x, 2).subs(x, 4)) * 0.1**2)
v.check("01-04.4d", 1 + 0.05)
v.check("01-04.4e", math.exp(0.05))
v.check("01-04.4f", 0.2)
v.check("01-04.4g", math.sin(0.2))
v.check("01-04.4h", 1 + 10 * 0.02)
v.check("01-04.4i", 1.02**10)
v.assert_true("P4 actual error -1.54e-4", round(math.sqrt(4.1) - 2.025, 6) == -0.000154)

r5 = argmin(lambda r: -Pf(r, 1.0, 2000.0), 10, 1e5)
v.check("01-04.5a", r5 / 1e3)
v.check("01-04.5b", Pf(r5, 1.0, 2000.0) * 1e6)
v.check("01-04.5c", Pf(1000, 1.0, 2000.0) * 1e6)
v.check("01-04.5d", 100 * Pf(1000, 1.0, 2000.0) / Pf(2000, 1.0, 2000.0))
rs_best = argmin(lambda rs: -(1.0**2 * 2000 / (rs + 2000) ** 2), 0, 1e4)
v.check("01-04.5e", rs_best, tol=1e-3)

T6 = lambda nn: 20 * nn + 800 / nn  # noqa: E731
n6 = argmin(T6, 1, 50)
v.check("01-04.6a", n6)
v.check("01-04.6b", T6(n6))
best_int = min(range(1, 30), key=T6)
v.check("01-04.6c", best_int)
v.check("01-04.6d", T6(best_int))
v.check("01-04.6e", T6(1))
v.check("01-04.6f", T6(1) / T6(6))

xr = 0.3
iters = []
for _ in range(3):
    xr = xr * (2 - 3 * xr)
    iters.append(xr)
v.check("01-04.7a", iters[0])
v.check("01-04.7b", iters[1])
v.check("01-04.7c", iters[2])
v.check("01-04.7d", 1 - 3 * iters[0])
v.check("01-04.7e", 1 - 3 * iters[1])
v.check("01-04.7f", 1 - 3 * iters[2])
k = 0
e = 2.0**-8
while e > 2.0**-53:
    e, k = e * e, k + 1
v.check("01-04.7g", k)

nt = lambda xx: xx - math.atan(xx) * (1 + xx * xx)  # noqa: E731
v.check("01-04.8a", nt(1.0))
v.check("01-04.8b", nt(1.5))
v.check("01-04.8c", brentq(lambda xx: 2 * xx - (1 + xx * xx) * math.atan(xx), 1, 2))
seq = [1.5]
for _ in range(4):
    seq.append(nt(seq[-1]))
sq1 = [1.0]
for _ in range(4):
    sq1.append(nt(sq1[-1]))
v.check("01-04.8d", sq1[2])
v.check("01-04.8e", sq1[3])
v.check("01-04.8f", sq1[4])
v.check("01-04.8g", abs(sq1[4]) / abs(sq1[3]) ** 3)
v.check("01-04.8h", seq[2])
v.check("01-04.8i", seq[3])
v.check("01-04.8j", seq[4])
v.assert_true("P8 from 1.5 diverges (|x| grows each step)", all(abs(seq[i + 1]) > abs(seq[i]) for i in range(4)))
seq1 = [1.0]
for _ in range(4):
    seq1.append(nt(seq1[-1]))
v.assert_true("P8 from 1.0 converges", abs(seq1[-1]) < 1e-9)

A9, d9 = 1e-6, 2e-6
v.check("01-04.9a", epsilon_0 * A9 / d9 * 1e12)
v.check("01-04.9b", 5 * (-epsilon_0 * A9 / d9**2) * 1e-3 * 1e9)
v.check("01-04.9c", (d9 / (d9 / 2)) ** 2)

v.check("01-04.10a", 5.0**2 / 100)
v.check("01-04.10b", 2 * 1 + 1 * 2)
v.check("01-04.10c", 0.25 * 0.04)
v.check("01-04.10d", math.hypot(2 * 1, 1 * 2))
v.check("01-04.10e", 0.25 * math.hypot(0.02, 0.02))

v.check("01-04.11a", 1.0 * 2)
v.check("01-04.11b", 0.5 * 10)
v.check("01-04.11c", 0.01 / 1e-6 * 50e-6)

E12 = lambda vv: Ef(vv, 0.8, 0.1)  # noqa: E731
v12 = argmin(E12, 0.05, 2)
v.check("01-04.12a", v12)
v.check("01-04.12b", E12(v12))
v.check("01-04.12c", E12(0.9))
v.check("01-04.12d", E12(0.9) / E12(v12))

T13 = lambda nn, gam=0.04: (600 / nn + 40) * (1 + gam * nn)  # noqa: E731
v.assert_true("P13 expansion", sp.simplify((600 / n_ + 40) * (1 + sp.Rational(4, 100) * n_)
                                           - (64 + 600 / n_ + sp.Rational(8, 5) * n_)) == 0)
n13 = argmin(T13, 1, 100)
v.check("01-04.13a", n13)
v.check("01-04.13b", T13(n13))
v.check("01-04.13c", T13(1))
v.check("01-04.13d", T13(5))
v.check("01-04.13e", T13(19))
v.check("01-04.13f", T13(1) / T13(19))
v.check("01-04.13g", T13(n13 / 2))
v.check("01-04.13j", 100 * (T13(n13 / 2) / T13(n13) - 1))
v.assert_true("P13 symmetric penalty", math.isclose(T13(math.sqrt(375) / 2), T13(2 * math.sqrt(375)), rel_tol=1e-12))
n13b = argmin(lambda nn: T13(nn, 0.02), 1, 100)
v.check("01-04.13h", n13b)
v.check("01-04.13i", T13(n13b, 0.02))
v.assert_true("T(20) = 126.0 and 19 is the best integer", round(T13(20), 1) == 126.0 and T13(19) < T13(20))

errs = []
xk = 1.0
for _ in range(4):
    xk = (xk + 2 / xk) / 2
    errs.append(xk - xs2)
v.check("01-04.14a", errs[1] / errs[0] ** 2)
v.check("01-04.14b", errs[2] / errs[1] ** 2)
v.check("01-04.14c", errs[3] / errs[2] ** 2, rtol=2e-4)
v.check("01-04.14d", 1 / (2 * xs2))
v.check("01-04.14e", (1.5 + 2 / 1.5) / 2)
v.check("01-04.14f", ((1.5 + 2 / 1.5) / 2 + 2 / ((1.5 + 2 / 1.5) / 2)) / 2)
v.assert_true("x^2-2: e_{k+1} = e_k^2/(2 x_k) exactly", all(abs(errs[i + 1] - errs[i] ** 2 / (2 * (errs[i] + xs2))) < 1e-15 for i in range(3)))

Ta, Rth, tau_th = 40.0, 0.5, 2.0
Tt = lambda tt, P_: Ta + P_ * Rth * (1 - math.exp(-tt / tau_th))  # noqa: E731
v.check("01-04.15a", float(sp.diff(Ta + 100 * Rth * (1 - sp.exp(-t / tau_th)), t).subs(t, 0)))
v.check("01-04.15b", Ta + 100 * Rth)
v.check("01-04.15c", brentq(lambda tt: Tt(tt, 100) - 85, 0, 100))
v.check("01-04.15d", brentq(lambda tt: Tt(tt, 150) - 85, 0, 100))
v.check("01-04.15e", 45 / (150 * Rth / tau_th))
v.check("01-04.15f", (85 - Ta) / Rth)

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-04.a", 100 * (1 - Pf(100) / Pf(50)))
v.check("Lab 01-04.b", 100 * (T6(2 * n6) / T6(n6) - 1))
v.check("Lab 01-04.c", math.sqrt((1 + 25) / 3))
v.check("Lab 01-04.d", Pf(argmin(lambda r: -Pf(r, 10.0, 25.0), 1, 1000), 10.0, 25.0))
v.check("Lab 01-04.e", 100 * (Ef(vst / 2) / Ef(vst) - 1))
v.check("Lab 01-04.f", 100 * (Ef(2 * vst) / Ef(vst) - 1))
v.check("Lab 01-04.g", math.sqrt(1 + 25))
v.assert_true("Lab: min-energy penalties +41.7 % and +66.7 %",
              round(100 * (Ef(vst / 2) / Ef(vst) - 1), 1) == 41.7 and round(100 * (Ef(2 * vst) / Ef(vst) - 1), 1) == 66.7)

v.check("T 01-04.a", 100 * (1 - 4 * 1.1 / 2.1**2))
v.check("T 01-04.b", math.sqrt(1 + 25) / math.sqrt(1 + 1))
v.check("T 01-04.c", (1 + 5) / (1 + 1))

v.finish()
