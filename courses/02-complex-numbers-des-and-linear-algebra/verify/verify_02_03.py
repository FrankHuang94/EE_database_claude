#!/usr/bin/env python3
"""Verify every published number in chapter 02-03, its solutions and its lab handout."""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-03",
    COURSE / "chapters" / "02-03-second-order-linear-odes.md",
    COURSE / "solutions" / "02-03-solutions.md",
    COURSE / "labs" / "02-03-lab" / "README.md",
)
t = sp.symbols("t", real=True)
y = sp.Function("y")
al, w0s, X = sp.symbols("alpha omega_0 X", positive=True)


def roots(alpha, w0):
    d = cmath.sqrt(alpha**2 - w0**2)
    return -alpha + d, -alpha - d


def overshoot(z):
    return math.exp(-math.pi * z / math.sqrt(1 - z * z))


def step_y(z, x):
    """Normalized step response y(x), x = w0 t."""
    if z < 1:
        wd = math.sqrt(1 - z * z)
        return 1 - math.exp(-z * x) * (math.cos(wd * x) + z / wd * math.sin(wd * x))
    if z == 1:
        return 1 - (1 + x) * math.exp(-x)
    r1, r2 = -z + math.sqrt(z * z - 1), -z - math.sqrt(z * z - 1)
    return 1 + (r2 * math.exp(r1 * x) - r1 * math.exp(r2 * x)) / (r1 - r2)


# ---------------------------------------------------------------- theory identities
u = sp.Function("u")
red = sp.expand(sp.diff(u(t) * sp.exp(-al * t), t, 2) + 2 * al * sp.diff(u(t) * sp.exp(-al * t), t) + al**2 * u(t) * sp.exp(-al * t))
v.assert_true("reduction of order leaves u'' e^{-at}", sp.simplify(red - sp.diff(u(t), t, 2) * sp.exp(-al * t)) == 0)
wd_s = sp.symbols("omega_d", positive=True)
ystep = X * (1 - sp.exp(-al * t) * (sp.cos(wd_s * t) + al / wd_s * sp.sin(wd_s * t)))
v.assert_true("underdamped step derivative = X w0^2/wd e^{-at} sin wd t",
              sp.simplify(sp.diff(ystep, t) - X * (al**2 + wd_s**2) / wd_s * sp.exp(-al * t) * sp.sin(wd_s * t)) == 0)
Ls, Cs, Rs = sp.symbols("L C R", positive=True)
iv, vv = sp.symbols("i v")
dw = Ls * iv * ((-Rs * iv - vv) / Ls) + Cs * vv * (iv / Cs)
v.assert_true("dw/dt = -R i^2", sp.simplify(dw + Rs * iv**2) == 0)
v.assert_true("wronskian of repeated-root pair is e^{-2at}",
              sp.simplify(sp.wronskian([sp.exp(-al * t), t * sp.exp(-al * t)], t) - sp.exp(-2 * al * t)) == 0)

# ---------------------------------------------------------------- Example 1
L1, C1 = 10e-6, 1e-6
w01 = 1 / math.sqrt(L1 * C1)
v.check("Ex 02-03.1a", w01 / 1e3)
v.check("Ex 02-03.1b", w01 / (2 * math.pi) / 1e3)
Rc = 2 * math.sqrt(L1 / C1)
v.check("Ex 02-03.1c", Rc)
v.check("Ex 02-03.1d", 1 / 2 * math.sqrt(C1 / L1))
v.check("Ex 02-03.1e", 20 / 2 * math.sqrt(C1 / L1))
s1, s2 = roots(20 / (2 * L1), w01)
v.check("Ex 02-03.1f", s1.real / 1e3)
v.check("Ex 02-03.1g", s2.real / 1e3)
v.check("Ex 02-03.1h", -1 / s1.real * 1e6)
v.check("Ex 02-03.1i", -w01 / (2 * (20 / 2 * math.sqrt(C1 / L1))) / 1e3)
v.assert_true("product and sum of roots", math.isclose((s1 * s2).real, w01**2) and math.isclose((s1 + s2).real, -2e6))

# ---------------------------------------------------------------- Example 2 (numerical ODE as an independent check)
a2 = 1 / (2 * L1)
wd2 = math.sqrt(w01**2 - a2**2)
sol2 = solve_ivp(lambda tt, s: [s[1] / C1, (-1.0 * s[1] - s[0]) / L1], (0, 100e-6), [5.0, 0.0],
                 rtol=1e-11, atol=1e-13, dense_output=True)
tmin = minimize_scalar(lambda tt: sol2.sol(tt)[0], bounds=(5e-6, 15e-6), method="bounded", options={"xatol": 1e-13}).x
v.check("Ex 02-03.2a", a2)
v.check("Ex 02-03.2b", wd2 / 1e3)
v.check("Ex 02-03.2c", wd2 / (2 * math.pi) / 1e3)
v.check("Ex 02-03.2d", 5 * a2 / wd2)
v.check("Ex 02-03.2e", tmin * 1e6)
v.check("Ex 02-03.2f", sol2.sol(tmin)[0])
v.check("Ex 02-03.2g", 100 * (1 - (sol2.sol(tmin)[0] / 5) ** 2))
z2 = a2 / w01
v.check("Ex 02-03.2h", 1 / (2 * z2))
v.check("Ex 02-03.2i", math.log(100) / a2 * 1e6)
v.check("Ex 02-03.2j", math.log(100) / a2 * wd2 / (2 * math.pi))
v.check("Ex 02-03.2k", 100 * math.exp(-2 * a2 * 2 * math.pi / wd2))

# ---------------------------------------------------------------- Example 3
xc = brentq(lambda x: (1 + x) * math.exp(-x) - 0.02, 1, 20)
v.check("Ex 02-03.3a", xc)
v.check("Ex 02-03.3b", math.log(50))
zst = brentq(lambda z: overshoot(z) - 0.02, 0.5, 0.95)
v.check("Ex 02-03.3c", zst)
wdn = math.sqrt(1 - zst**2)
xs = brentq(lambda x: step_y(zst, x) - 0.98, 1, math.pi / wdn)
v.check("Ex 02-03.3d", xs)
v.check("Ex 02-03.3e", xc / xs)
v.check("Ex 02-03.3f", 4 / zst)
grid = np.linspace(0, 40, 400001)


def settle(z, tol=0.02):
    yv = np.array([step_y(z, x) for x in grid[::10]])
    idx = np.where(abs(yv - 1) > tol)[0]
    return grid[::10][idx[-1] + 1]


v.assert_true("ζ* settles faster than ζ = 0.7 and ζ = 0.9", settle(zst + 1e-4) < min(settle(0.7), settle(0.9)))

# ---------------------------------------------------------------- Example 4
lo = math.log(0.25)
z4 = -lo / math.sqrt(math.pi**2 + lo**2)
wd4 = math.pi / 2e-6
w04 = wd4 / math.sqrt(1 - z4**2)
v.check("Ex 02-03.4a", z4)
v.check("Ex 02-03.4b", wd4 / 1e6)
v.check("Ex 02-03.4c", w04 / 1e6)
v.check("Ex 02-03.4d", w04 / (2 * math.pi) / 1e3)
v.check("Ex 02-03.4e", 1 / (2 * z4))
v.assert_true("overshoot round-trips to 25 %", math.isclose(overshoot(z4), 0.25))

# ---------------------------------------------------------------- Example 5 (PDN)
L5, C5, R5, dI, V0 = 25e-12, 100e-9, 1e-3, 10.0, 0.75


def pdn(L, C, R=R5):
    sol = solve_ivp(lambda tt, s: [(s[1] - dI) / C, (V0 - R * s[1] - s[0]) / L], (0, 60e-9), [V0, 0.0],
                    rtol=1e-11, atol=1e-14, dense_output=True, max_step=2e-11)
    tt = np.linspace(0, 60e-9, 60001)
    vv_ = sol.sol(tt)[0]
    k = int(np.argmin(vv_))
    res = minimize_scalar(lambda x: sol.sol(x)[0], bounds=(tt[max(k - 2, 0)], tt[min(k + 2, len(tt) - 1)]),
                          method="bounded", options={"xatol": 1e-16})
    return V0 - res.fun, res.x


w05 = 1 / math.sqrt(L5 * C5)
Z0 = math.sqrt(L5 / C5)
z5 = R5 / (2 * Z0)
dr, tdr = pdn(L5, C5)
v.check("Ex 02-03.5a", w05 / (2 * math.pi) / 1e6)
v.check("Ex 02-03.5b", Z0 * 1e3)
v.check("Ex 02-03.5c", z5)
v.check("Ex 02-03.5d", 1 / (2 * z5))
v.check("Ex 02-03.5e", dr * 1e3)
v.check("Ex 02-03.5f", tdr * 1e9)
v.check("Ex 02-03.5g", 100 * dr / V0)
v.check("Ex 02-03.5h", dI * Z0 * 1e3)
Zt = 0.03 * V0 / dI
v.check("Ex 02-03.5i", Zt * 1e3)
Cn = L5 / Zt**2
v.check("Ex 02-03.5j", Cn * 1e6)
v.check("Ex 02-03.5k", Cn / C5)
v.check("Ex 02-03.5l", pdn(L5, 4.938e-6)[0] * 1e3)
a5 = R5 / (2 * L5)
v.check("Ex 02-03.5m", math.pi / (2 * math.sqrt(w05**2 - a5**2)) * 1e9)
v.check("Ex 02-03.5n", w05)
v.check("Ex 02-03.5o", 0.03 * V0 * 1e3)
v.check("C 02-03.1", 4 / 2 * math.sqrt(1e-6 / 1e-3))
v.check("C 02-03.2", 2 * math.sqrt(1e-3 / 1e-6))
v.check("C 02-03.3", math.sqrt(50e-12 / 200e-9) * 1e3)
v.check("C 02-03.4", 20 * math.sqrt(50e-12 / 200e-9))
v.check("Q 02-03.a", 16e6)

# ---------------------------------------------------------------- numbers to know
for _id, z in zip("abc", (0.3, 0.5, 0.707)):
    v.check(f"N 02-03.{_id}", 100 * overshoot(z))
v.check("N 02-03.d", zst)
v.check("N 02-03.e", xs)
v.check("N 02-03.f", xc)

# ---------------------------------------------------------------- problems
v.check("02-03.1a", 50 / (2 * 10e-3))
v.check("02-03.1b", 1 / math.sqrt(10e-3 * 1e-6))
v.check("02-03.1c", (50 / (2 * 10e-3)) / 1e4)
v.check("02-03.1d", 1 / (2 * 1000 * 1e-6))
v.check("02-03.1e", 500 / 1e4)
v.check("02-03.1f", math.sqrt(80 / 0.2))
v.check("02-03.1g", 2 / (2 * 0.2))
v.check("02-03.1h", 5 / 20)
v.check("02-03.2a", math.sqrt(10))
v.check("02-03.2b", 1 / math.sqrt(10))
y3 = sp.dsolve(sp.Eq(y(t).diff(t, 2) + 5 * y(t).diff(t) + 6 * y(t), 0), y(t), ics={y(0): 1, y(t).diff(t).subs(t, 0): 0}).rhs
v.check("02-03.3a", float(y3.subs(t, 1)))
s1e = -5 + math.sqrt(24)
v.check("02-03.4a", s1e)
v.check("02-03.4b", 100 * (1 - (-0.1) / s1e))
y5 = sp.dsolve(sp.Eq(y(t).diff(t, 2) + 4 * y(t).diff(t) + 4 * y(t), 0), y(t), ics={y(0): 2, y(t).diff(t).subs(t, 0): -1}).rhs
v.check("02-03.5a", float(y5.subs(t, 1)))
v.assert_true("5: y = (2 + 3t) e^{-2t}", sp.simplify(y5 - (2 + 3 * t) * sp.exp(-2 * t)) == 0)
w0sym = sp.symbols("w0", positive=True)
y6 = sp.dsolve(sp.Eq(y(t).diff(t, 2) + 2 * w0sym * y(t).diff(t) + w0sym**2 * y(t), w0sym**2 * X), y(t),
               ics={y(0): 0, y(t).diff(t).subs(t, 0): 0}).rhs
v.assert_true("6(a) critically damped step formula", sp.simplify(y6 - X * (1 - (1 + w0sym * t) * sp.exp(-w0sym * t))) == 0)
x90 = brentq(lambda x: step_y(1.0, x) - 0.9, 0.1, 20)
v.check("02-03.6a", x90)
v.check("02-03.6b", x90 / 1e4 * 1e6)
wd7 = 1000 * math.sqrt(1 - 0.09)
v.check("02-03.7a", wd7)
v.check("02-03.7b", math.pi / wd7 * 1e3)
v.check("02-03.7c", 100 * overshoot(0.3))
L8, C8, R8 = 1e-3, 10e-6, 2.0
a8, w08 = R8 / (2 * L8), 1 / math.sqrt(L8 * C8)
wd8 = math.sqrt(w08**2 - a8**2)
sol8 = solve_ivp(lambda tt, s: [s[1] / C8, (-R8 * s[1] - s[0]) / L8], (0, 400e-6), [0.0, 1.0], rtol=1e-11, atol=1e-13, dense_output=True)
pk8 = minimize_scalar(lambda tt: -sol8.sol(tt)[0], bounds=(50e-6, 250e-6), method="bounded", options={"xatol": 1e-13})
v.check("02-03.8a", a8)
v.check("02-03.8b", w08)
v.check("02-03.8c", wd8)
v.check("02-03.8d", 1.0 / C8)
v.check("02-03.8e", 1.0 / C8 / wd8)
v.check("02-03.8f", pk8.x * 1e6)
v.check("02-03.8g", -pk8.fun)
v.check("02-03.8h", 0.5 * C8 * pk8.fun**2 * 1e3)
v.check("02-03.8i", 100 * (0.5 * C8 * pk8.fun**2) / (0.5 * L8 * 1.0))
a9 = 1 / (2 * 200 * 1e-6)
wd9 = math.sqrt(1e8 - a9**2)
v.check("02-03.9a", a9)
v.check("02-03.9b", a9 / 1e4)
v.check("02-03.9c", wd9)
vp9 = -(10 / 200) / 1e-6
v.check("02-03.9d", vp9)
v.check("02-03.9e", (vp9 + a9 * 10) / wd9)
sol9 = solve_ivp(lambda tt, s: [-(s[0] / 200 + s[1]) / 1e-6, s[0] / 10e-3], (0, 1e-3), [10.0, 0.0], rtol=1e-11, atol=1e-13, dense_output=True)
tt9 = 0.3e-3
v.assert_true("9: closed form matches numerical solution",
              abs(sol9.sol(tt9)[0] - math.exp(-a9 * tt9) * (10 * math.cos(wd9 * tt9) + (vp9 + a9 * 10) / wd9 * math.sin(wd9 * tt9))) < 1e-6)
wdx, alx = sp.symbols("w_d a", positive=True)
W10 = sp.simplify(sp.wronskian([sp.exp(-alx * t) * sp.cos(wdx * t), sp.exp(-alx * t) * sp.sin(wdx * t)], t))
v.assert_true("10(c) W = wd e^{-2at}", sp.simplify(W10 - wdx * sp.exp(-2 * alx * t)) == 0)
v.check("02-03.10a", float(W10.subs({wdx: 3, alx: 1, t: 0})))
lo11 = math.log(0.10)
z11 = -lo11 / math.sqrt(math.pi**2 + lo11**2)
wd11 = math.pi / 50e-6
v.check("02-03.11a", z11)
v.check("02-03.11b", wd11 / 1e3)
v.check("02-03.11c", wd11 / math.sqrt(1 - z11**2) / 1e3)
v.check("02-03.11d", 1 / (2 * z11))
L12, C12, R12 = 100e-6, 100e-9, 0.5
w012 = 1 / math.sqrt(L12 * C12)
Q12 = math.sqrt(L12 / C12) / R12
a12 = R12 / (2 * L12)
v.check("02-03.12a", w012 / 1e3)
v.check("02-03.12b", Q12)
v.check("02-03.12c", Q12 / math.pi)
v.check("02-03.12d", 100 * (1 - math.exp(-4 * math.pi * a12 / math.sqrt(w012**2 - a12**2))))
v.check("02-03.12e", 100 * 2 * math.pi / Q12)
L13, C13 = 2e-9, 2e-12
w013 = 1 / math.sqrt(L13 * C13)
z13 = 10 / 2 * math.sqrt(C13 / L13)
v.check("02-03.13a", w013)
v.check("02-03.13b", w013 / (2 * math.pi) / 1e9)
v.check("02-03.13c", z13)
v.check("02-03.13d", 100 * overshoot(z13))
v.check("02-03.13e", 2 * 0.7 * math.sqrt(L13 / C13))
v.check("02-03.13f", 100 * overshoot(0.7))
L14, C14, dI14, V14 = 5e-12, 1e-6, 50.0, 0.8
Zt14 = V14 * 0.05 / dI14
Z014 = math.sqrt(L14 / C14)
v.check("02-03.14a", Zt14 * 1e3)
v.check("02-03.14b", Z014 * 1e3)
v.check("02-03.14c", dI14 * Z014 * 1e3)
v.check("02-03.14d", 100 * dI14 * Z014 / V14)
v.check("02-03.14e", 1 / (2 * math.pi * math.sqrt(L14 * C14)) / 1e6)
v.check("02-03.14f", L14 / Zt14**2 * 1e6)
v.check("02-03.14g", Zt14**2 * C14 * 1e12)
r15 = roots(-2 / (2 * 1e-3), 1 / math.sqrt(1e-3 * 10e-6))
v.assert_true("15: roots in the right half-plane", r15[0].real > 0 and r15[1].real > 0)
v.check("02-03.15a", abs(r15[0].imag) / (2 * math.pi))
v.check("02-03.15b", 1 / r15[0].real * 1e3)
t15 = math.log(1000) / r15[0].real
v.check("02-03.15c", t15 * 1e3)
v.check("02-03.15d", t15 * abs(r15[0].imag) / (2 * math.pi))

# ---------------------------------------------------------------- lab handout
v.check("Lab 02-03.a", math.log(20) / 0.1)
v.check("Lab 02-03.b", math.log(20) / 0.1 * math.sqrt(1 - 0.01) / (2 * math.pi))
v.check("Lab 02-03.c", 0.5 * C1 * 25 * 1e6)
v.check("Lab 02-03.d", pdn(L5, 2 * C5)[0] * 1e3)
v.check("Lab 02-03.e", pdn(L5 / 2, C5)[0] * 1e3)
v.check("Lab 02-03.f", math.pi / math.sqrt(0.75))

v.finish()
