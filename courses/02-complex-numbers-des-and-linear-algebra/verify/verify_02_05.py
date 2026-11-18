#!/usr/bin/env python3
"""Verify every published number in chapter 02-05, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar
from scipy.signal import residue

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-05",
    COURSE / "chapters" / "02-05-laplace-transform-for-odes.md",
    COURSE / "solutions" / "02-05-solutions.md",
    COURSE / "labs" / "02-05-lab" / "README.md",
)
t = sp.symbols("t", positive=True)
s = sp.symbols("s")
y = sp.Function("y")


def L(f):
    return sp.simplify(sp.laplace_transform(f, t, s, noconds=True))


def Linv(F):
    return sp.simplify(sp.inverse_laplace_transform(F, s, t))


def same(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


def ivp2(a1, a0, rhs, y0, dy0):
    eq = sp.Eq(y(t).diff(t, 2) + a1 * y(t).diff(t) + a0 * y(t), rhs)
    return sp.dsolve(eq, y(t), ics={y(0): y0, y(t).diff(t).subs(t, 0): dy0}).rhs


# ---------------------------------------------------------------- theory: table and properties
a, w = sp.symbols("a omega", positive=True)
table = [
    (sp.Integer(1), 1 / s), (t, 1 / s**2), (t**3, 6 / s**4), (sp.exp(-a * t), 1 / (s + a)),
    (sp.cos(w * t), s / (s**2 + w**2)), (sp.sin(w * t), w / (s**2 + w**2)),
    (t * sp.exp(-a * t), 1 / (s + a) ** 2), (sp.exp(-a * t) * sp.cos(w * t), (s + a) / ((s + a) ** 2 + w**2)),
    (sp.exp(-a * t) * sp.sin(w * t), w / ((s + a) ** 2 + w**2)),
]
v.assert_true("transform table entries", all(same(L(f), F) for f, F in table))
tr = sp.symbols("t_r", real=True)  # with t declared positive, SymPy evaluates DiracDelta(t) to 0
v.assert_true("delta transforms to 1 (lower limit 0-)", sp.laplace_transform(sp.DiracDelta(tr), tr, s, noconds=True) == 1)
g = sp.exp(-3 * t) * sp.cos(2 * t)
v.assert_true("derivative rule L{f'} = sF - f(0)", same(L(sp.diff(g, t)), s * L(g) - g.subs(t, 0)))
v.assert_true("second-derivative rule", same(L(sp.diff(g, t, 2)), s**2 * L(g) - s * g.subs(t, 0) - sp.diff(g, t).subs(t, 0)))
v.assert_true("multiplication by t: L{t f} = -F'", same(L(t * g), -sp.diff(L(g), s)))
v.assert_true("integral rule L{int f} = F/s", same(L(sp.integrate(g.subs(t, sp.Symbol("x")), (sp.Symbol("x"), 0, t))), L(g) / s))
lam = sp.symbols("lambda", positive=True)
conv = sp.integrate(sp.exp(-lam) * sp.exp(-2 * (t - lam)), (lam, 0, t))
v.assert_true("convolution theorem on e^-t * e^-2t", same(L(conv), 1 / ((s + 1) * (s + 2))))
T0 = sp.Integer(2)
v.assert_true("time shift: L{(t-2)u(t-2)} = e^{-2s}/s^2",
              same(sp.laplace_transform((t - T0) * sp.Heaviside(t - T0), t, s, noconds=True), sp.exp(-2 * s) / s**2))

# ---------------------------------------------------------------- Example 1
Fa = 3 / s - 2 / (s + 4) + 10 / (s**2 + 4)
v.assert_true("Ex 1(a) transform", same(L(3 - 2 * sp.exp(-4 * t) + 5 * sp.sin(2 * t)), Fa))
v.assert_true("Ex 1(b) transform", same(L(t * sp.exp(-2 * t)), 1 / (s + 2) ** 2))
v.assert_true("Ex 1(c) transform", same(L(sp.exp(-t) * sp.cos(3 * t)), (s + 1) / ((s + 1) ** 2 + 9)))
v.check("Ex 02-05.1a", float(sp.limit(s * Fa, s, sp.oo)))

# ---------------------------------------------------------------- Example 2
Y2 = (s**2 + 5 * s + 12) / (s * (s + 2) * (s + 3))
pf2 = sp.apart(Y2, s)
v.check("Ex 02-05.2a", float(sp.limit(s * Y2, s, 0)))
v.check("Ex 02-05.2b", float(sp.limit((s + 2) * Y2, s, -2)))
v.check("Ex 02-05.2c", float(sp.limit((s + 3) * Y2, s, -3)))
y2 = ivp2(5, 6, 12, 1, 0)
v.assert_true("Ex 2: Laplace result equals dsolve", same(Linv(pf2), y2) and same(pf2, 2 / s - 3 / (s + 2) + 2 / (s + 3)))
v.check("Ex 02-05.2d", float(y2.subs(t, 1)))
v.check("Ex 02-05.2e", float(sp.limit(s * Y2, s, 0)))

# ---------------------------------------------------------------- Example 3 (series RLC, 50 ohm)
R3, L3, C3 = 50.0, 10e-3, 1e-6
al3, w03 = R3 / (2 * L3), 1 / math.sqrt(L3 * C3)
wd3 = math.sqrt(w03**2 - al3**2)
v.check("Ex 02-05.3a", wd3)
sol3 = solve_ivp(lambda tt, x: [x[1], w03**2 * (1 - x[0]) - 2 * al3 * x[1]], (0, 2e-3), [0, 0],
                 max_step=1e-7, rtol=1e-10, atol=1e-12, dense_output=True)
pk3 = minimize_scalar(lambda tt: -sol3.sol(tt)[0], bounds=(0.2e-3, 0.45e-3), method="bounded",
                      options={"xatol": 1e-12})
v.assert_true("Ex 3: ODE overshoot equals e^{-alpha pi/wd}", abs(-pk3.fun - 1 - math.exp(-al3 * math.pi / wd3)) < 1e-6)
v.check("Ex 02-05.3b", 100 * math.exp(-al3 * math.pi / wd3))
v.check("Ex 02-05.3c", pk3.x * 1e3)
w0s, als = sp.symbols("omega_0 alpha", positive=True)
v.assert_true("Ex 3 partial fractions", same(sp.apart(w0s**2 / (s * (s**2 + 2 * als * s + w0s**2)), s),
                                            1 / s - (s + 2 * als) / (s**2 + 2 * als * s + w0s**2)))

# ---------------------------------------------------------------- Example 4 (RC pulse)
tau4 = 1e-3


def v4(tt):
    out = 5 * (1 - math.exp(-tt / tau4)) if tt >= 0 else 0.0
    if tt >= 2e-3:
        out -= 5 * (1 - math.exp(-(tt - 2e-3) / tau4))
    return out


sol4 = solve_ivp(lambda tt, x: [((5.0 if tt < 2e-3 else 0.0) - x[0]) / tau4], (0, 3e-3), [0.0],
                 max_step=1e-6, rtol=1e-10, atol=1e-12, dense_output=True)
v.assert_true("Ex 4: time-shift formula equals direct ODE", abs(sol4.sol(3e-3)[0] - v4(3e-3)) < 1e-6)
v.check("Ex 02-05.4a", v4(2e-3))
v.check("Ex 02-05.4b", v4(3e-3))
v.assert_true("Ex 4 check: 4.323 e^-1 = 1.590", abs(v4(2e-3) * math.exp(-1) - v4(3e-3)) < 1e-12)

# ---------------------------------------------------------------- Example 5 / Problem 14 (PDN)
R5, L5, C5, dI = 1e-3, 25e-12, 100e-9, 10.0
al5 = R5 / (2 * L5)
wd5 = math.sqrt(1 / (L5 * C5) - al5**2)
roots5 = np.roots([L5 * C5, R5 * C5, 1])
v.assert_true("Ex 5: poles of Z are -alpha +/- j wd",
              np.allclose(sorted(roots5, key=lambda z: z.imag), [complex(-al5, -wd5), complex(-al5, wd5)], rtol=1e-9))
v.check("Ex 02-05.5a", al5)
v.check("Ex 02-05.5b", wd5)
v.check("Ex 02-05.5c", wd5 / (2 * math.pi) / 1e6)
v.check("Ex 02-05.5d", -R5 / L5)
Rs, Ls, Cs, dIs = sp.symbols("R L C DeltaI", positive=True)
Zs = (Rs + s * Ls) / (Ls * Cs * s**2 + Rs * Cs * s + 1)
dV = -Zs * dIs / s
v.assert_true("Ex 5: Z = (R + sL) || 1/(sC)", same(Zs, 1 / (1 / (Rs + s * Ls) + s * Cs)))
v.assert_true("Ex 5: initial value 0", sp.limit(s * dV, s, sp.oo) == 0)
slope_sym = sp.limit(s * s * dV, s, sp.oo)
v.assert_true("Ex 5: initial slope -DeltaI/C", same(slope_sym, -dIs / Cs))
final_sym = sp.limit(s * dV, s, 0)
v.check("Ex 02-05.5e", float(slope_sym.subs({dIs: dI, Cs: C5})))
v.check("Ex 02-05.5f", float(final_sym.subs({dIs: dI, Rs: R5})) * 1e3)

# Problem 14: partial fractions and the closed form
P, Qp = -Rs * Ls * Cs, Ls - Rs**2 * Cs
Ds = Ls * Cs * s**2 + Rs * Cs * s + 1
v.assert_true("P14: (R + sL)/(s D) = R/s + (Ps + Q')/D", same((Rs + s * Ls) / (s * Ds), Rs / s + (P * s + Qp) / Ds))
A14 = R5 * dI
B14 = -dI * (1 / C5 - R5 * al5) / wd5


def dv14(tt):
    return -dI * R5 + math.exp(-al5 * tt) * (A14 * math.cos(wd5 * tt) + B14 * math.sin(wd5 * tt))


# independent check: integrate the circuit ODEs (inductor current iL, capacitor voltage dv)
def pdn(tt, x):
    iL, dvv = x  # deviations from the pre-step operating point
    return [(-dvv - R5 * iL) / L5, (iL - dI) / C5]


sol14 = solve_ivp(pdn, (0, 20e-9), [0.0, 0.0], max_step=2e-12, rtol=1e-10, atol=1e-14, dense_output=True)
tt14 = np.linspace(0, 20e-9, 401)
v.assert_true("P14: closed form matches the circuit ODE",
              max(abs(sol14.sol(x)[1] - dv14(x)) for x in tt14) < 1e-6)
mn = minimize_scalar(dv14, bounds=(1e-9, 4e-9), method="bounded", options={"xatol": 1e-16})
v.check("02-05.14a", A14 * 1e3)
v.check("02-05.14b", B14 * 1e3)
v.check("02-05.14c", -mn.fun * 1e3)
v.check("02-05.14d", mn.x * 1e9)
v.check("Ex 02-05.5g", -mn.fun * 1e3)

# ---------------------------------------------------------------- Problems 1-4
v.assert_true("P1 transforms", same(L(sp.exp(-2 * t)), 1 / (s + 2)) and same(L(t), 1 / s**2)
              and same(sp.laplace_transform(5 * sp.Heaviside(t - 3), t, s, noconds=True), 5 * sp.exp(-3 * s) / s))
n = sp.symbols("n", positive=True, integer=True)
v.assert_true("P2 recursion n/s * (n-1)!/s^n = n!/s^(n+1)", sp.simplify(n / s * sp.factorial(n - 1) / s**n - sp.factorial(n) / s ** (n + 1)) == 0)
v.check("02-05.2a", float(sp.simplify(L(t**3) * s**4)))
v.assert_true("P2(b) L{t^2 e^-t} = 2/(s+1)^3", same(L(t**2 * sp.exp(-t)), 2 / (s + 1) ** 3))
v.assert_true("P3 transforms", same(L(2 * sp.cos(5 * t) - 3 * sp.sin(5 * t)), (2 * s - 15) / (s**2 + 25))
              and same(L(sp.exp(-3 * t) * sp.sin(4 * t)), 4 / ((s + 3) ** 2 + 16)))
f4 = [Linv(6 / (s * (s + 3))), Linv((2 * s + 3) / (s**2 + 9)), Linv(1 / (s + 2) ** 3)]
v.assert_true("P4 inverses", same(f4[0], 2 - 2 * sp.exp(-3 * t)) and same(f4[1], 2 * sp.cos(3 * t) + sp.sin(3 * t))
              and same(f4[2], t**2 * sp.exp(-2 * t) / 2))
for k, f in zip("abc", f4):
    v.check(f"02-05.4{k}", float(f.subs(t, 1)))

# ---------------------------------------------------------------- Problem 5 (repeated pole), checked with SciPy
r5, p5, _ = residue([1, 4], [1, 2, 0, 0])
res = {}
for rr, pp in zip(r5, p5):
    res.setdefault(round(pp.real, 9), []).append(rr.real)
v.assert_true("P5 SciPy residues: -0.5 and 2 at 0, 0.5 at -2",
              np.allclose(sorted(res[0.0]), [-0.5, 2]) and np.allclose(res[-2.0], [0.5]))
Y5 = (s + 4) / (s**2 * (s + 2))
v.check("02-05.5a", float(sp.limit(s**2 * Y5, s, 0)))
v.check("02-05.5b", float(sp.limit(sp.diff(s**2 * Y5, s), s, 0)))
v.check("02-05.5c", float(sp.limit((s + 2) * Y5, s, -2)))
v.check("02-05.5d", float(Linv(Y5).subs(t, 1)))

# ---------------------------------------------------------------- Problems 6-10
y6 = Linv((3 * s + 7) / (s**2 + 4 * s + 13))
v.assert_true("P6 inverse", same(y6, sp.exp(-2 * t) * (3 * sp.cos(3 * t) + sp.sin(3 * t) / 3)))
v.check("02-05.6a", float(y6.subs(t, sp.Rational(1, 2))))
v.check("02-05.6b", float(sp.limit(s * (3 * s + 7) / (s**2 + 4 * s + 13), s, sp.oo)))
y7 = sp.dsolve(sp.Eq(y(t).diff(t) + 4 * y(t), 8), y(t), ics={y(0): 5}).rhs
v.assert_true("P7 Laplace result", same(Linv((5 * s + 8) / (s * (s + 4))), y7))
v.check("02-05.7a", float(y7.subs(t, sp.Rational(1, 4))))
y8 = ivp2(0, 4, sp.sin(t), 0, 0)
v.assert_true("P8 Laplace result", same(Linv(1 / ((s**2 + 1) * (s**2 + 4))), y8)
              and same(y8, sp.sin(t) / 3 - sp.sin(2 * t) / 6))
v.check("02-05.8a", float(y8.subs(t, sp.pi / 2)))
tau9 = 2.0
v9 = lambda tt: 10 * (1 - math.exp(-(tt - 1) / tau9)) if tt >= 1 else 0.0  # noqa: E731
sol9 = solve_ivp(lambda tt, x: [((10.0 if tt >= 1 else 0.0) - x[0]) / tau9], (0, 3), [0.0], max_step=1e-3,
                 rtol=1e-10, atol=1e-12)
v.assert_true("P9 delayed step matches the ODE", abs(sol9.y[0, -1] - v9(3)) < 1e-6)
v.check("02-05.9a", v9(3))
y10 = Linv(3 / (s**2 + 2 * s + 5))
v.assert_true("P10 y = 1.5 e^-t sin 2t", same(y10, sp.Rational(3, 2) * sp.exp(-t) * sp.sin(2 * t)))
y10h = ivp2(2, 5, 0, 0, 3)
v.assert_true("P10(b) impulse = ICs y(0+)=0, y'(0+)=3", same(y10, y10h))
v.check("02-05.10a", float(sp.diff(y10, t).subs(t, 0)))
f10 = sp.lambdify(t, y10)
pk10 = minimize_scalar(lambda tt: -f10(tt), bounds=(0.1, 1.2), method="bounded", options={"xatol": 1e-12})
v.assert_true("P10 peak at atan(2)/2", abs(pk10.x - math.atan(2) / 2) < 1e-6)
v.check("02-05.10b", pk10.x)
v.check("02-05.10c", -pk10.fun)

# ---------------------------------------------------------------- Problem 11
F11 = (2 * s + 3) / (s * (s + 1) * (s + 3))
v.check("02-05.11a", float(sp.limit(s * F11, s, sp.oo)))
v.check("02-05.11b", float(sp.limit(s * F11, s, 0)))
f11 = Linv(F11)
v.assert_true("P11(a) inverse settles to 1", sp.limit(f11, t, sp.oo) == 1)
F11b = 4 / (s * (s**2 - s + 2))
v.assert_true("P11(b) poles of sF in right half-plane", all(sp.re(r) > 0 for r in sp.roots(s**2 - s + 2, s)))
v.check("02-05.11c", float(sp.limit(s * F11b, s, 0)))
H11 = 10 * (s + 2) / (s**2 + 3 * s + 20)
v.check("02-05.11d", float(H11.subs(s, 0)))
p11 = np.roots([1, 3, 20])
v.check("02-05.11e", p11[0].real)
v.check("02-05.11f", abs(p11[0].imag))

# ---------------------------------------------------------------- Problem 12
v.assert_true("P12 direct convolution", same(conv, sp.exp(-t) - sp.exp(-2 * t)))
num12, _ = quad(lambda x: math.exp(-x) * math.exp(-2 * (1 - x)), 0, 1)
v.assert_true("P12 numerical integral", abs(num12 - (math.exp(-1) - math.exp(-2))) < 1e-12)
v.check("02-05.12a", float(conv.subs(t, 1)))

# ---------------------------------------------------------------- Problem 13 (band-pass)
R13, L13, C13 = 100.0, 10e-3, 1e-6
Rs13 = sp.Symbol("R")
H13 = sp.simplify(Rs13 / (Rs13 + s * Ls + 1 / (s * Cs)))
v.assert_true("P13 H(s)", same(H13, (Rs13 / Ls) * s / (s**2 + (Rs13 / Ls) * s + 1 / (Ls * Cs))))
a13, w013 = R13 / (2 * L13), 1 / math.sqrt(L13 * C13)
wd13 = math.sqrt(w013**2 - a13**2)
z13 = a13 / w013
v.check("02-05.13a", wd13)
v.check("02-05.13b", z13)
v.check("02-05.13c", 1 / (2 * z13))
amp13 = (R13 / L13) / wd13
v.check("02-05.13d", amp13)
y13 = lambda tt: amp13 * math.exp(-a13 * tt) * math.sin(wd13 * tt)  # noqa: E731
pk13 = minimize_scalar(lambda tt: -y13(tt), bounds=(10e-6, 300e-6), method="bounded", options={"xatol": 1e-14})
v.assert_true("P13 peak at (pi/3)/wd", abs(pk13.x - (math.pi / 3) / wd13) < 1e-10)
v.check("02-05.13e", pk13.x * 1e6)
v.check("02-05.13f", -pk13.fun)
Y13s = sp.inverse_laplace_transform(sp.Integer(10**4) / (s**2 + 10**4 * s + 10**8), s, t)
v.assert_true("P13 step response symbolic matches", abs(float(Y13s.subs(t, sp.Rational(1, 10000))) - y13(1e-4)) < 1e-9)

# ---------------------------------------------------------------- Problem 15 (imperfect cancellation)
Y15 = (s + sp.Rational(11, 10)) / (s * (s + 1) * (s + 10))
c0 = sp.limit(s * Y15, s, 0)
c1 = sp.limit((s + 1) * Y15, s, -1)
c10 = sp.limit((s + 10) * Y15, s, -10)
v.assert_true("P15 partial fractions", same(sp.apart(Y15, s), c0 / s + c1 / (s + 1) + c10 / (s + 10)))
v.check("02-05.15a", float(c0))
v.check("02-05.15b", float(c1))
v.check("02-05.15c", float(c10))
v.check("02-05.15d", float(-c1 / c0) * 100)
err15 = lambda tt: abs(float(c1) * math.exp(-tt) + float(c10) * math.exp(-10 * tt)) - 0.01 * float(c0)  # noqa: E731
ts15 = brentq(err15, 0.5, 10, xtol=1e-14)
grid = np.linspace(ts15 + 1e-6, 30, 3000)
v.assert_true("P15 stays inside the band after settling", all(err15(x) < 0 for x in grid))
v.check("02-05.15e", ts15)
v.check("02-05.15f", math.log(100) / 10)

# ---------------------------------------------------------------- lab handout
v.check("Lab 02-05.a", 3 / (2 * math.pi))
v.check("Lab 02-05.b", math.exp(20))
sig_new, wd_new = 1000.0, 9950.0
den_new = np.poly([complex(-sig_new, wd_new), complex(-sig_new, -wd_new)]).real
v.check("Lab 02-05.d", den_new[2])
num_new = 1e8
sol_lab = solve_ivp(lambda tt, x: [x[1], num_new - den_new[1] * x[1] - den_new[2] * x[0]], (0, 1e-3), [0, 0],
                    max_step=1e-7, rtol=1e-10, atol=1e-12, dense_output=True)
pk_lab = minimize_scalar(lambda tt: -sol_lab.sol(tt)[0], bounds=(0.2e-3, 0.45e-3), method="bounded",
                         options={"xatol": 1e-12})
final_lab = num_new / den_new[2]
v.assert_true("Lab: simulated overshoot equals e^{-sigma pi/wd}",
              abs((-pk_lab.fun - final_lab) / final_lab - math.exp(-sig_new * math.pi / wd_new)) < 1e-6)
v.check("Lab 02-05.c", 100 * math.exp(-sig_new * math.pi / wd_new))
v.assert_true("Lab: FVT values of the trap table", sp.limit(s * 2 / (s**2 + 4), s, 0) == 0
              and sp.limit(s * 1 / (s - 1), s, 0) == 0 and sp.limit(s * F11b, s, 0) == 2)

# 16 · piecewise, impulsive and periodic inputs (numerical ODE as an independent check)
from scipy.integrate import solve_ivp as _ivp, quad as _quad  # noqa: E402
_v = lambda t_: t_ if t_ < 1 else 1.0  # noqa: E731
_y16 = _ivp(lambda t_, y_: [_v(t_) - y_[0]], (0, 2), [0.0], rtol=1e-12, atol=1e-14, max_step=1e-3)
v.check("02-05.16a", _y16.y[0, -1])
_y16c = _ivp(lambda t_, y_: [-y_[0]], (1, 2), [0.5], rtol=1e-12, atol=1e-14)   # impulse 0.5 at t = 1 -> jump of 0.5
v.check("02-05.16b", _y16c.y[0, -1])
_sq = sum(_quad(lambda t_: math.exp(-t_), 2 * k, 2 * k + 1)[0] for k in range(60))
v.check("02-05.16c", _sq)
ss_, tt_ = sp.symbols("ss_ tt_", positive=True)
v.assert_true("t u(t-2) transform", sp.simplify(sp.integrate(tt_ * sp.exp(-ss_ * tt_), (tt_, 2, sp.oo)) - sp.exp(-2 * ss_) * (1 / ss_**2 + 2 / ss_)) == 0)
# 17 · convolution
_h = lambda t_: math.exp(-t_) - math.exp(-2 * t_)  # noqa: E731
v.check("02-05.17a", _quad(lambda l_: _h(1 - l_) * 1.0, 0, 1)[0])
v.check("02-05.17b", _quad(lambda l_: _h(1 - l_) * math.exp(-3 * l_), 0, 1)[0])
v.check("02-05.17c", _quad(lambda t_: t_ * math.sin(2 * t_) * math.exp(-t_), 0, 60, limit=400)[0])
v.check("02-05.17d", _quad(lambda t_: 0.5 * (1 - math.cos(2 * t_)) * math.exp(-t_), 0, 60, limit=400)[0])

v.finish()
