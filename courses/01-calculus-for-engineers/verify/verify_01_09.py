#!/usr/bin/env python3
"""Verify every published number in chapter 01-09, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.constants import Boltzmann as K_B, elementary_charge as Q
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-09",
    COURSE / "chapters" / "01-09-multivariable-calculus-1.md",
    COURSE / "solutions" / "01-09-solutions.md",
    COURSE / "labs" / "01-09-lab" / "README.md",
)
x, y, t = sp.symbols("x y t", real=True)
EG = 1.12


def num(e, subs):
    return float(e.subs(subs))


def tempco(V, T):
    """dV/dT of a junction at constant current, I_s ~ T^3 exp(-Eg/kT), by implicit differentiation."""
    Vs, Ts = sp.symbols("V T", positive=True)
    lnI = 3 * sp.log(Ts) - EG * Q / (K_B * Ts) + Q * Vs / (K_B * Ts)
    dVdT = -sp.diff(lnI, Ts) / sp.diff(lnI, Vs)
    return float(dVdT.subs({Vs: V, Ts: T}))


# ---------------------------------------------------------------- theory identities
vg, vd, k, vth, va = sp.symbols("V_GS V_DS k V_TH V_A", positive=True)
ID = sp.Rational(1, 2) * k * (vg - vth) ** 2 * (1 + vd / va)
v.assert_true("g_m formula", sp.simplify(sp.diff(ID, vg) - k * (vg - vth) * (1 + vd / va)) == 0)
v.assert_true("g_o formula", sp.simplify(sp.diff(ID, vd) - k * (vg - vth) ** 2 / (2 * va)) == 0)
v.assert_true("square-law g_m = 2 I_D / V_ov", sp.simplify(sp.diff(ID, vg) - 2 * ID / (vg - vth)) == 0)
Vs, Ts = sp.symbols("V T", positive=True)
lnI = 3 * sp.log(Ts) - EG * Q / (K_B * Ts) + Q * Vs / (K_B * Ts)
v.assert_true("tempco formula (V - Eg/q - 3kT/q)/T",
              sp.simplify(-sp.diff(lnI, Ts) / sp.diff(lnI, Vs) - (Vs - EG - 3 * K_B * Ts / Q) / Ts) == 0)
a_, b_ = sp.symbols("a b", real=True)
xs_, ys_ = [0, 1, 2, 3], [1, 3, 4, 6]
S = sum((yy - a_ - b_ * xx) ** 2 for xx, yy in zip(xs_, ys_))
sol = sp.solve([sp.diff(S, a_), sp.diff(S, b_)], [a_, b_])
v.assert_true("normal equations give a = 11/10, b = 8/5", sol[a_] == sp.Rational(11, 10) and sol[b_] == sp.Rational(8, 5))
v.assert_true("automotive range swing ≈ 0.3 V", round(1.8e-3 * 165, 1) == 0.3)
v.assert_true("Q8: eta < 0.2 for 5x^2", math.isclose(2 / 10, 0.2))

# ---------------------------------------------------------------- examples
aC, V0, f0 = 1e-9, 0.8, 2e9
Vv, fv = sp.symbols("V f", positive=True)
P = aC * Vv**2 * fv
sub = {Vv: V0, fv: f0}
v.check("Ex 01-09.1a", num(P, sub))
v.check("Ex 01-09.1b", num(sp.diff(P, Vv), sub))
v.check("Ex 01-09.1c", num(sp.diff(P, fv), sub) * 1e9)
v.check("Ex 01-09.1d", num(sp.diff(P, Vv), sub) * 0.01 * 1e3)
v.check("Ex 01-09.1e", num(sp.diff(P, fv), sub) * 100e6 * 1e3)
v.assert_true("1 % V saves 25.6 mW vs 12.8 mW for 1 % f",
              math.isclose(num(sp.diff(P, Vv), sub) * 0.008, 0.0256) and math.isclose(num(sp.diff(P, fv), sub) * 20e6, 0.0128))

s2 = {k: 2e-3, vth: 0.5, va: 10, vg: 0.8, vd: 1.0}
gm2, go2 = num(sp.diff(ID, vg), s2), num(sp.diff(ID, vd), s2)
v.check("Ex 01-09.2a", num(ID, s2) * 1e6)
v.check("Ex 01-09.2b", gm2 * 1e3)
v.check("Ex 01-09.2c", go2 * 1e6)
v.check("Ex 01-09.2d", 1 / go2 / 1e3)
v.check("Ex 01-09.2e", gm2 / go2)
v.check("Ex 01-09.2f", (gm2 * 0.01 + go2 * 0.1) * 1e6)
v.check("Ex 01-09.2g", (num(ID, {**s2, vg: 0.81, vd: 1.1}) - num(ID, s2)) * 1e6)

VT300 = K_B * 300 / Q
Vd = VT300 * math.log(1e-3 / 1e-14)
v.check("Ex 01-09.3a", Vd)
v.check("Ex 01-09.3b", tempco(Vd, 300) * 1e3)
v.check("Ex 01-09.3c", K_B * 300 / Q * 1e3)

f4 = x**2 + 4 * y**2
g4 = [sp.diff(f4, x).subs({x: 2, y: 1}), sp.diff(f4, y).subs({x: 2, y: 1})]
v.check("Ex 01-09.4a", math.hypot(*map(float, g4)))
v.check("Ex 01-09.4b", (float(g4[0]) + float(g4[1])) / math.sqrt(2))
p1 = (2 - 0.1 * float(g4[0]), 1 - 0.1 * float(g4[1]))
v.check("Ex 01-09.4c", float(f4.subs({x: p1[0], y: p1[1]})))


def cores(ks, F):
    ks = np.asarray(ks, float)
    w = 1 / np.sqrt(ks)
    f = F * w / w.sum()
    return f, float(np.sum(ks * f**3)), float(3 * ks[0] * f[0] ** 2)


f5, P5, lam5 = cores([0.1, 0.4], 3.0)
res = minimize(lambda f: 0.1 * f[0] ** 3 + 0.4 * f[1] ** 3, x0=[1.5, 1.5], method="SLSQP",
               constraints=[{"type": "eq", "fun": lambda f: f[0] + f[1] - 3}])
v.assert_true("numerical optimizer agrees with Lagrange (2 cores)", np.allclose(res.x, f5, atol=1e-4))
v.check("Ex 01-09.5a", f5[0])
v.check("Ex 01-09.5b", f5[1])
v.check("Ex 01-09.5c", P5)
v.check("Ex 01-09.5d", lam5)
v.check("Ex 01-09.5e", (0.1 + 0.4) * 1.5**3)
v.check("Ex 01-09.5f", 0.1 * 27)
v.check("Ex 01-09.5g", cores([0.1, 0.4], 3.1)[1])

# ---------------------------------------------------------------- problems
f1 = x**2 * y + sp.exp(x * y)
p = {x: 1, y: 2}
v.check("01-09.1a", num(sp.diff(f1, x), p))
v.check("01-09.1b", num(sp.diff(f1, y), p))
v.check("01-09.1c", num(sp.diff(f1, x, y), p))
v.assert_true("Clairaut", sp.simplify(sp.diff(f1, x, y) - sp.diff(f1, y, x)) == 0)

Vr, Rr = sp.symbols("V R", positive=True)
P2 = Vr**2 / Rr
v.check("01-09.2a", num(sp.diff(P2, Vr), {Vr: 10, Rr: 50}))
v.check("01-09.2b", num(sp.diff(P2, Rr), {Vr: 10, Rr: 50}))

f3 = x**2 + x * y + y**2
g3 = np.array([num(sp.diff(f3, x), {x: 1, y: -1}), num(sp.diff(f3, y), {x: 1, y: -1})])
v.check("01-09.3a", np.linalg.norm(g3))
v.check("01-09.3b", g3 @ np.array([3, 4]) / 5)

z4 = (sp.cos(t) ** 2 * sp.sin(t))
v.check("01-09.4a", float(sp.diff(z4, t).subs(t, sp.pi / 4)))

R5 = 1.72e-8 * 0.05 / (0.2e-3 * 35e-6)
v.check("01-09.5a", R5)
v.check("01-09.5b", 1 + 5 + 10)
v.check("01-09.5c", math.sqrt(1 + 25 + 100))

s6 = {k: 4e-3, vth: 0.4, va: 6, vg: 0.7, vd: 0.9}
gm6, go6 = num(sp.diff(ID, vg), s6), num(sp.diff(ID, vd), s6)
v.check("01-09.6a", num(ID, s6) * 1e6)
v.check("01-09.6b", gm6 * 1e3)
v.check("01-09.6c", go6 * 1e6)
v.check("01-09.6d", 1 / go6 / 1e3)
v.check("01-09.6e", gm6 / go6)
v.check("01-09.6f", (gm6 * 0.005 + go6 * 0.2) * 1e6)
v.check("01-09.6g", (num(ID, {**s6, vg: 0.705, vd: 1.1}) - num(ID, s6)) * 1e6)

v.check("01-09.7a", tempco(0.600, 350) * 1e3)
F7 = x**3 + y**3
v.check("01-09.7b", num(-sp.diff(F7, x) / sp.diff(F7, y), {x: 1, y: 2}))

f8 = x**3 - 3 * x + y**2 - 2 * y
crit = sp.solve([sp.diff(f8, x), sp.diff(f8, y)], [x, y], dict=True)
H = sp.hessian(f8, (x, y))
mins = [c for c in crit if H.subs(c).det() > 0 and H.subs(c)[0, 0] > 0]
saddles = [c for c in crit if H.subs(c).det() < 0]
v.check("01-09.8a", float(f8.subs(mins[0])))
v.check("01-09.8b", float(f8.subs(saddles[0])))

bb, aa = np.polyfit(xs_, ys_, 1)
v.check("01-09.9a", aa)
v.check("01-09.9b", bb)
v.check("01-09.9c", float(np.sum((np.array(ys_) - (aa + bb * np.array(xs_))) ** 2)))
HS = sp.hessian(S, (a_, b_))
v.assert_true("P9 Hessian positive definite", HS.det() > 0 and HS[0, 0] > 0)

xg, yg = 1.0, 1.0
for _ in range(3):
    xg, yg = xg - 0.04 * 2 * xg, yg - 0.04 * 20 * yg
v.check("01-09.10a", xg)
v.check("01-09.10b", yg)
v.check("01-09.10c", xg**2 + 10 * yg**2)
v.check("01-09.10d", 2 / 20)
v.check("01-09.10e", 20 / 2)

Pp = sp.symbols("P", positive=True)
lam = sp.symbols("lambda")
L11 = x * y - lam * (2 * x + 2 * y - Pp)
s11 = sp.solve([sp.diff(L11, x), sp.diff(L11, y), sp.diff(L11, lam)], [x, y, lam], dict=True)[0]
Astar = (x * y).subs(s11)
v.check("01-09.11a", float(Astar.subs(Pp, 20)))
v.check("01-09.11b", float(s11[lam].subs(Pp, 20)))
v.assert_true("lambda = dA*/dP", sp.simplify(sp.diff(Astar, Pp) - s11[lam]) == 0)


def capacity(p, N):
    return float(np.sum(np.log2(1 + np.asarray(p) / np.asarray(N))))


N12 = [1.0, 3.0]
mu = (6 + sum(N12)) / 2
v.check("01-09.12a", mu - N12[0])
v.check("01-09.12b", mu - N12[1])
v.check("01-09.12c", capacity([mu - N12[0], mu - N12[1]], N12))
v.check("01-09.12d", capacity([3, 3], N12))
r = minimize(lambda p: -capacity(p, N12), x0=[0.5, 0.5], method="SLSQP", bounds=[(0, None)] * 2,
             constraints=[{"type": "eq", "fun": lambda p: p.sum() - 1}])
v.check("01-09.12e", -r.fun, tol=1e-6)
v.assert_true("P12(c): optimizer puts all power in channel 1", r.x[1] < 1e-6)

f13, P13, lam13 = cores([0.1, 0.4, 0.9], 3.4)
v.check("01-09.13a", f13[0])
v.check("01-09.13b", f13[1])
v.check("01-09.13c", f13[2])
v.check("01-09.13d", P13)
v.check("01-09.13e", lam13)

v.check("01-09.14a", K_B / Q * 1e3)
dvbe = tempco(Vd, 300)
Kb = -dvbe / (K_B / Q)
v.check("01-09.14b", Kb)
v.check("01-09.14c", Vd + Kb * VT300)
v.check("01-09.14d", -dvbe * 1e3)
v.check("01-09.14e", K_B / Q * 1e3)
v.check("01-09.14f", Kb)
v.assert_true("V_out = Eg/q + 3kT/q", math.isclose(Vd + Kb * VT300, EG + 3 * VT300, rel_tol=1e-12))

V15 = np.array([0.6, 0.8, 1.0])
P15 = np.array([0.40, 0.70, 1.05])
A15 = np.vstack([V15**2, np.ones(3)]).T
(a15, b15), *_ = np.linalg.lstsq(A15, P15, rcond=None)
v.check("01-09.15a", a15)
v.check("01-09.15b", b15)
v.check("01-09.15c", float(np.sum((A15 @ [a15, b15] - P15) ** 2)))
v.check("01-09.15d", 100 * b15 / (a15 * 0.64 + b15))

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-09.a", 2 / (2 * 100))
V10u = VT300 * math.log(10e-6 / 1e-14)
v.check("Lab 01-09.b", tempco(V10u, 300) * 1e3)

v.check("01-09.12f", mu)

v.finish()
