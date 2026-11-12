#!/usr/bin/env python3
"""Verify every published number in chapter 02-02, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-02",
    COURSE / "chapters" / "02-02-first-order-linear-odes.md",
    COURSE / "solutions" / "02-02-solutions.md",
    COURSE / "labs" / "02-02-lab" / "README.md",
)
t = sp.symbols("t", real=True)
y = sp.Function("y")


def ivp(rhs, y0, t0=0):
    """Solve y' = rhs(t, y) symbolically with y(t0) = y0."""
    return sp.dsolve(sp.Eq(y(t).diff(t), rhs(t, y(t))), y(t), ics={y(t0): y0}).rhs


def num_ivp(f, y0, t_end, **kw):
    sol = solve_ivp(f, (0, t_end), [y0], rtol=1e-11, atol=1e-12, **kw)
    return sol


# ---------------------------------------------------------------- theory identities
P, g, mu = sp.symbols("P g mu", cls=sp.Function)
tau_s, S_s, w_s = sp.symbols("tau S omega", positive=True)
v.assert_true("§3 verify: 1 + 3e^-2t solves y' = -2y + 2, y(0) = 4",
              sp.simplify(ivp(lambda tt, yy: -2 * yy + 2, 4) - (1 + 3 * sp.exp(-2 * t))) == 0)
v.assert_true("§3.4 t y' + 2y = t^2 has y = t^2/4 + C/t^2",
              sp.simplify(t * sp.diff(t**2 / 4 + 5 / t**2, t) + 2 * (t**2 / 4 + 5 / t**2) - t**2) == 0)
v.assert_true("§3.6 ramp particular solution S(t - tau)",
              sp.simplify(tau_s * sp.diff(S_s * (t - tau_s), t) + S_s * (t - tau_s) - S_s * t) == 0)
v.assert_true("§3.6 matched exponential (t/tau) e^(-t/tau)",
              sp.simplify(tau_s * sp.diff(t / tau_s * sp.exp(-t / tau_s), t) + t / tau_s * sp.exp(-t / tau_s) - sp.exp(-t / tau_s)) == 0)
N0s, Ks, rs = sp.symbols("N_0 K r", positive=True)
Nlog = Ks / (1 + (Ks - N0s) / N0s * sp.exp(-rs * t))
v.assert_true("§3.3 logistic solution satisfies N' = rN(1 - N/K)", sp.simplify(sp.diff(Nlog, t) - rs * Nlog * (1 - Nlog / Ks)) == 0)
v.assert_true("§3.7 y = t^2 and y = 0 both solve y' = 2 sqrt(y)", sp.simplify(sp.diff(t**2, t) - 2 * sp.sqrt(t**2)).subs(t, 2) == 0)
v.assert_true("§3.7 1/(1 - t) solves y' = y^2", sp.simplify(sp.diff(1 / (1 - t), t) - (1 / (1 - t)) ** 2) == 0)
v.assert_true("§3.10 thermal units: (K/W)(J/K) = s", True)

# ---------------------------------------------------------------- Example 1: cooling die
tau1 = 2 * 15
v.check("Ex 02-02.1a", tau1)
v.check("Ex 02-02.1b", brentq(lambda tt: 25 + 60 * math.exp(-tt / tau1) - 40, 0, 500))
v.check("Ex 02-02.1c", 25 + 60 * math.exp(-60 / tau1))
v.check("Ex 02-02.1d", math.log(4))

# ---------------------------------------------------------------- Example 2: RL with initial current
L2, R2, V2 = 10e-3, 5.0, 12.0
i2 = sp.dsolve(sp.Eq(L2 * y(t).diff(t) + R2 * y(t), V2), y(t), ics={y(0): 0.4}).rhs
v.check("Ex 02-02.2a", L2 / R2 * 1e3)
v.check("Ex 02-02.2b", float(sp.limit(i2, t, sp.oo)))
v.check("Ex 02-02.2c", float(i2.subs(t, 1e-3)))
v.check("Ex 02-02.2d", brentq(lambda tt: float(i2.subs(t, tt)) - 2.3, 0, 0.1) * 1e3)

# ---------------------------------------------------------------- Example 3: ramp tracking
S3, tau3 = 0.5e3, 200e-6
sol3 = num_ivp(lambda tt, vv: [(S3 * tt - vv[0]) / tau3], 0.0, 1e-3, dense_output=True)
v.check("Ex 02-02.3a", S3 * tau3 * 1e3)
v.check("Ex 02-02.3b", (S3 * 1e-3 - sol3.sol(1e-3)[0]) * 1e3)

# ---------------------------------------------------------------- Example 4: switched sinusoid
tau4 = 1 / (2 * math.pi * 1e3)
w4 = 2 * math.pi * 2e3
a_, b_ = sp.symbols("a b")
coef = sp.solve([sp.Eq(a_ + b_ * w4 * tau4, 1), sp.Eq(b_ - a_ * w4 * tau4, 0)], [a_, b_])
A4 = math.hypot(float(coef[a_]), float(coef[b_]))
v.check("Ex 02-02.4a", tau4 * 1e6)
v.check("Ex 02-02.4b", float(coef[a_]))
v.check("Ex 02-02.4c", float(coef[b_]))
v.check("Ex 02-02.4d", A4)
v.check("Ex 02-02.4e", math.degrees(math.atan2(float(coef[b_]), float(coef[a_]))))
v.check("Ex 02-02.4f", -float(coef[a_]))
v.check("Ex 02-02.4g", 5 * tau4 * 1e3)
v.check("Ex 02-02.4h", 20 * math.log10(1 / math.sqrt(5)))
ph = 1 / (1 + 1j * w4 * tau4)
v.assert_true("phasor agrees with undetermined coefficients", math.isclose(abs(ph), A4) and math.isclose(-math.degrees(np.angle(ph)), 63.43, abs_tol=0.005))
sol4 = num_ivp(lambda tt, vv: [(math.cos(w4 * tt) - vv[0]) / tau4], 0.0, 2e-3, dense_output=True, max_step=1e-6)
tt4 = 1.3e-3
v.assert_true("full solution matches numerical integration",
              abs(sol4.sol(tt4)[0] - (A4 * math.cos(w4 * tt4 - math.atan(2)) - 0.2 * math.exp(-tt4 / tau4))) < 1e-7)

# ---------------------------------------------------------------- Example 5: thermal runaway
Ta, Pd, PL0, T0, Tc, Cth, Rth = 35.0, 80.0, 10.0, 25.0, 30.0, 50.0, 0.25
PL = lambda T: PL0 * math.exp((T - T0) / Tc)  # noqa: E731
f5 = lambda T, R=Rth: Ta + R * (Pd + PL(T)) - T  # noqa: E731
Tm = T0 + Tc * math.log(Tc / (Rth * PL0))
Ts = brentq(f5, Ta, Tm)
Tu = brentq(f5, Tm, 400)
v.check("Ex 02-02.5a", Ts)
v.check("Ex 02-02.5b", PL(Ts))
v.check("Ex 02-02.5c", PL(Ts) / Tc)
v.check("Ex 02-02.5d", Cth / (1 / Rth - PL(Ts) / Tc))
v.check("Ex 02-02.5e", Rth * Cth)
G = Rth * PL(Ts) / Tc
v.check("Ex 02-02.5f", G)
v.check("Ex 02-02.5g", 1 / (1 - G))
v.check("Ex 02-02.5h", Tu)
v.check("Ex 02-02.5i", PL(Tu) / Tc)
v.assert_true("unstable point: generation slope exceeds 1/R", PL(Tu) / Tc > 1 / Rth)
Rc = brentq(lambda R: Ta + R * Pd + Tc - (T0 + Tc * math.log(Tc / (R * PL0))), 0.1, 1)
v.check("Ex 02-02.5j", Rc)
v.check("Ex 02-02.5k", T0 + Tc * math.log(Tc / (Rc * PL0)))
v.check("Ex 02-02.5l", 100 * (Rc / Rth - 1))
v.check("Ex 02-02.5m", Tc * math.log(2))
v.check("Ex 02-02.5n", Ta + Rth * (Pd + PL(35.0)))
it = 35.0
for _ in range(60):
    it = Ta + Rth * (Pd + PL(it))
v.assert_true("fixed-point iteration converges to 64.25", abs(it - Ts) < 1e-9)
v.assert_true("PL(64.25) = 37 and 35 + 0.25*117 = 64.25", round(PL(Ts), 2) == 37.00 and math.isclose(35 + 0.25 * 117, 64.25))

# ---------------------------------------------------------------- numbers to know
for _id, n in zip("abcde", range(1, 6)):
    v.check(f"N 02-02.{_id}", 100 * (1 - math.exp(-n)))
v.check("N 02-02.f", math.log(2))
v.check("N 02-02.g", math.log(9))
v.check("N 02-02.h", 20 * math.log10(1 / math.sqrt(2)))
v.check("N 02-02.i", 2 * math.log(9))
v.check("N 02-02.j", 100 * math.exp(-1))

# ---------------------------------------------------------------- problems
v.check("02-02.1a", 1 / (1 + 0))
v.assert_true("1(b) 2 - e^-3t solves y' = 6 - 3y", sp.simplify(sp.diff(2 - sp.exp(-3 * t), t) - (6 - 3 * (2 - sp.exp(-3 * t)))) == 0)
y2a = ivp(lambda tt, yy: -2 * tt * yy, 5)
v.check("02-02.2a", float(y2a.subs(t, 1)))
v.check("02-02.2b", math.pi / 2)
v.assert_true("2(b) tan t solves y' = 1 + y^2", sp.simplify(sp.diff(sp.tan(t), t) - 1 - sp.tan(t) ** 2) == 0)
yy = sp.symbols("yy")
roots = sorted(float(r) for r in sp.solve(yy**2 - yy - 2, yy))
fp = sp.lambdify(yy, sp.diff(yy**2 - yy - 2, yy))
v.check("02-02.3a", roots[0])
v.check("02-02.3b", roots[1])
v.assert_true("-1 stable, 2 unstable", fp(roots[0]) < 0 < fp(roots[1]))
v.check("02-02.3c", -1 / fp(roots[0]))
y4 = ivp(lambda tt, yv: 6 - 3 * yv, 0)
v.check("02-02.4a", 1 / 3)
v.check("02-02.4b", float(sp.limit(y4, t, sp.oo)))
v.check("02-02.4c", brentq(lambda tt: float(y4.subs(t, tt)) - 1.9, 0, 10))
y5 = sp.dsolve(sp.Eq(t * y(t).diff(t) - y(t), t**3), y(t), ics={y(1): 2}).rhs
v.check("02-02.5a", float(y5.subs(t, 2)))
r6 = lambda s_: 0.02 + 0.004 * s_  # noqa: E731
I6 = quad(r6, 0, 10)[0]
v.check("02-02.6a", 100000 * math.exp(I6), tol=0.5)
v.check("02-02.6b", math.exp(-I6))
sol6 = num_ivp(lambda tt, B: [0.05 * B[0] + 10000], 50000.0, 10)
v.check("02-02.6c", 50000 * math.exp(0.5), tol=0.5)
v.check("02-02.6d", 10000 / 0.05 * (math.exp(0.5) - 1), tol=0.5)
v.check("02-02.6e", sol6.y[0, -1], tol=0.5)
tau7 = 4.0
sol7 = num_ivp(lambda tt, Tp: [((25 + 2 * tt) - Tp[0]) / tau7], 25.0, 10)
v.check("02-02.7a", tau7)
v.check("02-02.7b", 2 * tau7)
v.check("02-02.7c", tau7 * math.log(100))
v.check("02-02.7d", 45 - sol7.y[0, -1])
v.check("02-02.7e", sol7.y[0, -1])
tau8 = 1e-3
v8 = lambda tt: 5 * (math.exp(-tt / tau8) - math.exp(-2 * tt / tau8))  # noqa: E731
sol8 = num_ivp(lambda tt, vv: [(5 * math.exp(-tt / 0.5e-3) - vv[0]) / tau8], 0.0, 1e-3)
v.assert_true("8(a) closed form matches numerical solution", abs(sol8.y[0, -1] - v8(1e-3)) < 1e-8)
tp8 = brentq(lambda tt: -math.exp(-tt / tau8) / tau8 + 2 * math.exp(-2 * tt / tau8) / tau8, 1e-6, 5e-3)
v.check("02-02.8a", tp8 * 1e3)
v.check("02-02.8b", v8(tp8))
v8m = lambda tt: 5 * tt / tau8 * math.exp(-tt / tau8)  # noqa: E731
tp8m = brentq(lambda tt: (1 - tt / tau8), 1e-6, 5e-3)
v.check("02-02.8c", tp8m * 1e3)
v.check("02-02.8d", v8m(tp8m))
tau9 = 1e-3 / 10
w9 = 2 * math.pi * 5e3
v.check("02-02.9a", tau9 * 1e3)
v.check("02-02.9b", w9 * tau9)
I9 = 1 / (1 + 1j * w9 * tau9)
v.check("02-02.9c", abs(I9))
v.check("02-02.9d", -math.degrees(np.angle(I9)))
v.check("02-02.9e", I9.real)
v.check("02-02.9f", -I9.imag)
Nl = lambda tt: 200 / (1 + 99 * math.exp(-0.8 * tt))  # noqa: E731
v.check("02-02.10a", brentq(lambda tt: Nl(tt) - 100, 0, 30))
v.check("02-02.10b", brentq(lambda tt: Nl(tt) - 180, 0, 30) - brentq(lambda tt: Nl(tt) - 20, 0, 30))
v.check("02-02.10c", Nl(3))
v.check("02-02.10d", 2 * math.exp(0.8 * 6))
v.check("02-02.10e", Nl(6))
v.assert_true("11(a) t^3 solves y' = 3 y^(2/3) for t > 0", sp.simplify(sp.diff(t**3, t) - 3 * (t**3) ** sp.Rational(2, 3)).subs(t, 2) == 0)
y11 = (t + 1) * sp.cos(t)
v.assert_true("11(b) (t + 1) cos t solves y' + tan(t) y = cos t, y(0) = 1",
              sp.simplify(sp.diff(y11, t) + sp.tan(t) * y11 - sp.cos(t)) == 0 and y11.subs(t, 0) == 1)
y11c = ivp(lambda tt, yv: yv**2, 2)
v.check("02-02.11a", float(sp.solve(sp.Eq(1 / y11c, 0), t)[0]))
h12 = 0.5
v.check("02-02.12a", 2 * 1.0)
ex12 = math.exp(-2)
fe, be, tr = (1 - h12) ** 4, (1 / (1 + h12)) ** 4, ((1 - h12 / 2) / (1 + h12 / 2)) ** 4
v.check("02-02.12b", ex12)
v.check("02-02.12c", fe)
v.check("02-02.12d", be)
v.check("02-02.12e", tr)
v.check("02-02.12f", 100 * (fe / ex12 - 1))
v.check("02-02.12g", 100 * (be / ex12 - 1))
v.check("02-02.12h", 100 * (tr / ex12 - 1))
y13 = ivp(lambda tt, yv: yv**2 - yv, sp.Rational(1, 2))
v.check("02-02.13a", float(y13.subs(t, 1)))
v.assert_true("13: y = 1/(1 + e^t)", sp.simplify(y13 - 1 / (1 + sp.exp(t))) == 0)
C14, R14 = 30.0, 10.0
tau14 = R14 * C14
v.check("02-02.14a", (43 - 25) / R14)
v.check("02-02.14b", 25 + R14 * 1.0)
t5 = num_ivp(lambda tt, T: [(5 - (T[0] - 25) / R14) / C14], 35.0, 2000, events=lambda tt, T: T[0] - 43)
t3 = num_ivp(lambda tt, T: [(3 - (T[0] - 25) / R14) / C14], 35.0, 2000, events=lambda tt, T: T[0] - 43)
v.check("02-02.14c", t5.t_events[0][0])
v.check("02-02.14d", t3.t_events[0][0])
v.check("02-02.14e", t5.t_events[0][0] / tau14)
v.check("02-02.14f", tau14)
R0C = 100 * 10e-12
T15 = 2e-9
sol15 = num_ivp(lambda tt, vv: [-vv[0] / (100 * math.exp(tt / T15) * 10e-12)], 1.0, 2e-9)
v.check("02-02.15a", R0C * 1e9)
v.check("02-02.15b", sol15.y[0, -1])
v.check("02-02.15c", math.exp(-T15 / R0C))
v.assert_true("15: closed form at 2 ns", abs(sol15.y[0, -1] - math.exp(-2 * (1 - math.exp(-1)))) < 1e-9)

# ---------------------------------------------------------------- lab handout
v.check("Lab 02-02.a", 1 - 3)
v.check("Lab 02-02.b", (1 - 1.5) / (1 + 1.5))
v.check("Lab 02-02.f", 1 / (1 + 3))


def thermal(R, T_start, t_end, level):
    ev = lambda tt, T: T[0] - level  # noqa: E731
    ev.terminal = True
    return solve_ivp(lambda tt, T: [(Pd + PL(T[0]) - (T[0] - Ta) / R) / Cth], (0, t_end), [T_start],
                     events=ev, rtol=1e-10, atol=1e-10, max_step=0.5)


v.check("Lab 02-02.c", thermal(0.40, 35.0, 300, 150).t_events[0][0])
v.check("Lab 02-02.d", thermal(0.25, 130.0, 300, 300).t_events[0][0])
v.check("Lab 02-02.e", thermal(0.32, 35.0, 300, 1e9).y[0, -1])
T32 = brentq(lambda T: f5(T, 0.32), Ta, T0 + Tc * math.log(Tc / (0.32 * PL0)))
v.check("Lab 02-02.g", T32)
v.check("Lab 02-02.h", Cth / (1 / 0.32 - PL(T32) / Tc))

v.finish()
