#!/usr/bin/env python3
"""Verify every number in the Course 01 final-exam solutions."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import sympy as sp
from scipy.constants import epsilon_0, mu_0
from scipy.integrate import dblquad, quad
from scipy.optimize import brentq, minimize_scalar
from scipy.special import iv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("01-exam", HERE.parent / "exam" / "solutions.md")
x, y, t = sp.symbols("x y t", real=True)

# 1 · decibels and exponentials
v.check("X01.1a", 20 - 6 + 14)
v.check("X01.1b", 10 ** (28 / 20))
v.check("X01.1c", 10 ** (28 / 10))
v.check("X01.1d", brentq(lambda tt: math.exp(-tt / 2e-3) - 0.01, 0, 1) * 1e3)

# 2 · limits and continuity
v.check("X01.2a", float(sp.limit(sp.sin(3 * x) / x, x, 0)))
f = sp.symbols("f", positive=True)
v.check("X01.2b", float(sp.limit(f / sp.sqrt(1 + (f / 1000) ** 2), f, sp.oo)))
a = sp.symbols("a")
v.check("X01.2c", float(sp.solve(sp.Eq(2 * 1, a - 1), a)[0]))

# 3 · derivatives
tau, w, C = 1e-6, 2 * math.pi * 1e6, 10e-9
vt = 5 * sp.exp(-t / tau) * sp.sin(w * t)
v.check("X01.3a", C * float(sp.diff(vt, t).subs(t, 0)) * 1e3)
v.check("X01.3b", float(sp.diff(sp.log(1 + x**2), x).subs(x, 2)))
Is, VT = 1e-14, 0.02585
Vd = lambda I: VT * math.log(I / Is + 1)  # noqa: E731
h = 1e-9
v.check("X01.3c", (Vd(1e-3 + h) - Vd(1e-3 - h)) / (2 * h))
v.check("X01.3d", 1 / (w * C))

# 4 · maximum power transfer
RL = sp.symbols("R_L", positive=True)
P = 100 * RL / (50 + RL) ** 2
Ropt = sp.solve(sp.diff(P, RL), RL)[0]
v.check("X01.4a", float(Ropt))
v.check("X01.4b", float(P.subs(RL, Ropt)))
v.check("X01.4c", float(P.subs(RL, 100)))
v.check("X01.4d", 100 * float(P.subs(RL, 100) / P.subs(RL, Ropt)))
v.check("X01.4e", float(P.subs(RL, 25)))
v.check("X01.4f", 100 * (1 - float(P.subs(RL, 100) / P.subs(RL, Ropt))))
v.assert_true("P/Pmax symmetric under x -> 1/x", math.isclose(float(P.subs(RL, 25)), float(P.subs(RL, 100))))

# 5 · Newton's method for the diode circuit
R = 1000.0
g = lambda V, Vs=5.0: Is * (math.exp(V / VT) - 1) - (Vs - V) / R  # noqa: E731
dg = lambda V: Is / VT * math.exp(V / VT) + 1 / R  # noqa: E731
V0 = 0.7
v.check("X01.5l", Is * math.exp(V0 / VT) * 1e3)
v.check("X01.5m", (5 - V0) / R * 1e3)
v.check("X01.5a", g(V0) * 1e3)
v.check("X01.5b", dg(V0))
s1 = g(V0) / dg(V0)
V1 = V0 - s1
v.check("X01.5c", s1 * 1e3)
v.check("X01.5d", V1)
s2 = g(V1) / dg(V1)
V2 = V1 - s2
v.check("X01.5e", s2 * 1e3)
v.check("X01.5f", V2)
V3 = V2 - g(V2) / dg(V2)
v.check("X01.5n", abs(V3 - V2) * 1e3)
Vsol = brentq(g, 0, 1)
v.check("X01.5g", Vsol)
I = (5 - Vsol) / R
v.check("X01.5h", I * 1e3)
rd = VT / (I + Is)
v.check("X01.5i", rd)
v.check("X01.5j", 0.1 * rd / (R + rd) * 1e3)
v.check("X01.5k", (brentq(lambda V: g(V, 5.1), 0, 1) - Vsol) * 1e3)
v.assert_true("linear estimate exceeds exact rise", 0.1 * rd / (R + rd) > brentq(lambda V: g(V, 5.1), 0, 1) - Vsol)

# 6 · charge
v.check("X01.6a", quad(lambda tt: 3e-3 * math.exp(-tt / 2e-3), 0, math.inf)[0] * 1e6)
v.check("X01.6b", quad(lambda tt: 3e-3 * math.exp(-tt / 2e-3), 0, 2e-3)[0] * 1e6)
v.check("X01.6c", 100 * (1 - math.exp(-1)))

# 7 · techniques of integration
v.check("X01.7a", float(sp.integrate(x * sp.exp(x), (x, 0, 1))))
v.check("X01.7b", float(sp.integrate(1 / ((x + 1) * (x + 2)), (x, 0, 1))))
Rr, Cc, V0s = sp.symbols("R C V_0", positive=True)
W = sp.integrate(V0s**2 / Rr * sp.exp(-2 * t / (Rr * Cc)), (t, 0, sp.oo))
v.assert_true("resistor energy = C V0^2 / 2 for any R", sp.simplify(W - Cc * V0s**2 / 2) == 0)
v.check("X01.7c", float(W.subs({Cc: 1e-6, V0s: 10, Rr: 1234})) * 1e6)

# 8 · half-wave rectified sine
T = 1.0
hw = lambda tt: 10 * math.sin(2 * math.pi * tt / T) if (tt % T) < T / 2 else 0.0  # noqa: E731
avg = quad(hw, 0, T, points=[T / 2], limit=200)[0] / T
ms = quad(lambda tt: hw(tt) ** 2, 0, T, points=[T / 2], limit=200)[0] / T
v.check("X01.8a", avg)
v.check("X01.8f", ms)
v.check("X01.8b", math.sqrt(ms))
v.check("X01.8c", ms / 50)
v.check("X01.8d", avg**2 / 50)
v.check("X01.8e", ms / avg**2)

# 9 · quantization noise
e, D = sp.symbols("e Delta", positive=True)
v.assert_true("uniform mean square = Delta^2/12", sp.simplify(sp.integrate(e**2 / D, (e, -D / 2, D / 2)) - D**2 / 12) == 0)
Dn = 1 / 2**12
erms = Dn / math.sqrt(12)
srms = 0.5 / math.sqrt(2)
v.check("X01.9a", Dn * 1e6)
v.check("X01.9b", erms * 1e6)
v.check("X01.9c", srms)
v.check("X01.9d", 20 * math.log10(srms / erms))
v.check("X01.9e", 20 * math.log10(2))
v.check("X01.9f", 20 * math.log10(math.sqrt(1.5)))
v.check("X01.9g", 12 * 20 * math.log10(2))
v.check("X01.9h", 6.02 * 12 + 1.76)

# 10 · Taylor series
P3 = float(sp.series(sp.exp(x), x, 0, 4).removeO().subs(x, sp.Rational(1, 10)))
v.check("X01.10a", P3, tol=5e-7)
v.check("X01.10b", 1e-4 / 24)
v.check("X01.10c", 1.2 * 1e-4 / 24)
v.assert_true("3^0.1 < 1.2 and e^0.1 < 3^0.1", math.exp(0.1) < 3**0.1 < 1.2)
v.check("X01.10d", math.exp(0.1) - P3)
l3 = float(sp.series(sp.log(1 + x), x, 0, 4).removeO().subs(x, sp.Rational(1, 5)))
v.check("X01.10e", l3)
v.check("X01.10f", math.log(1.2))
v.check("X01.10g", l3 - math.log(1.2))
v.check("X01.10h", 0.2**4 / 4)
v.assert_true("ln error within alternating bound", 0 < l3 - math.log(1.2) < 0.2**4 / 4)
aa = 0.1
v.check("X01.10i", 100 * aa / 4)
v.assert_true("exact Bessel HD2 agrees with a/4 to 0.1 %", abs(iv(2, aa) / iv(1, aa) / (aa / 4) - 1) < 1e-3)


# 11 · dies per wafer and cost
def terms(d, A):
    return math.pi * d**2 / (4 * A), math.pi * d / math.sqrt(2 * A)


t1, e1 = terms(300, 300)
t2, e2 = terms(300, 600)
v.check("X01.11a", t1)
v.check("X01.11b", e1)
v.check("X01.11c", t1 - e1)
v.check("X01.11d", t2)
v.check("X01.11e", e2)
v.check("X01.11f", t2 - e2)
v.check("X01.11g", (t1 - e1) / (t2 - e2))
Y1, Y2 = math.exp(-0.07 * 3.0), math.exp(-0.07 * 6.0)
g1, g2 = (t1 - e1) * Y1, (t2 - e2) * Y2
v.check("X01.11h", 100 * Y1)
v.check("X01.11i", g1)
v.check("X01.11j", 100 * Y2)
v.check("X01.11k", g2)
v.check("X01.11l", 17000 / g1)
v.check("X01.11m", 17000 / g2)
v.check("X01.11n", g1 / g2)

# 12 · tolerance
L, Cs = sp.symbols("L C", positive=True)
f0 = 1 / (2 * sp.pi * sp.sqrt(L * Cs))
vals = {L: 10e-6, Cs: 100e-12}
v.check("X01.12h", math.sqrt(10e-6 * 100e-12))
v.check("X01.12a", float(f0.subs(vals)) / 1e6)
v.check("X01.12b", float(sp.simplify(sp.diff(f0, L) * L / f0)))
v.check("X01.12c", float(sp.simplify(sp.diff(f0, Cs) * Cs / f0)))
v.check("X01.12d", 0.5 * 2 + 0.5 * 5)
v.check("X01.12e", math.hypot(0.5 * 2, 0.5 * 5))
v.check("X01.12f", 100 * 25 / 29)
v.check("X01.12g", math.hypot(0.5 * 2, 0.5 * 1))

# 13 · Lagrange multipliers
R1, R2, It = 10e-3, 15e-3, 100.0
opt = minimize_scalar(lambda i1: R1 * i1**2 + R2 * (It - i1) ** 2, bounds=(0, It), method="bounded", options={"xatol": 1e-10})
i1, i2 = opt.x, It - opt.x
v.check("X01.13a", i1)
v.check("X01.13b", i2)
v.check("X01.13c", opt.fun)
v.check("X01.13d", 2 * R1 * i1)
Rp = R1 * R2 / (R1 + R2)
v.check("X01.13e", Rp * 1e3)
v.assert_true("dP*/dI = lambda", math.isclose(2 * Rp * It, 2 * R1 * i1, rel_tol=1e-6))
v.check("X01.13f", R1 * 50**2 + R2 * 50**2)
v.check("X01.13g", 100 * ((R1 + R2) * 2500 / opt.fun - 1))
v.check("X01.13h", R1 * i1)
v.check("X01.13i", 2 * (R1 + R2))

# 14 · coaxial cable
aw, ratio, er = 0.45e-3, 3.5, 2.25
r = sp.symbols("r", positive=True)
lam = sp.symbols("lambda", positive=True)
eps = epsilon_0 * er
Vexpr = sp.integrate(lam / (2 * sp.pi * eps * r), (r, aw, ratio * aw))
Cp = float(lam / Vexpr)
v.check("X01.14a", ratio * aw * 1e3)
v.check("X01.14b", math.log(ratio))
v.check("X01.14c", Cp * 1e12)
v.check("X01.14d", math.sqrt(mu_0 / epsilon_0) / (2 * math.pi * math.sqrt(er)) * math.log(ratio))
v.check("X01.14e", Cp * 100 * 1e9)
v.check("X01.14f", Cp * 100 / (2 * math.pi * eps * aw) / 1e3)

# 15 · current, Ampere's law, potential
J0, aw2 = 10e6, 0.5e-3  # A/m^2, m
Iw = dblquad(lambda rr, th: J0 * (rr / aw2) ** 2 * rr, 0, 2 * math.pi, 0, aw2)[0]
v.check("X01.15a", Iw)
v.check("X01.15b", J0 * math.pi * aw2**2)
v.check("X01.15c", mu_0 * Iw / (2 * math.pi * aw2) * 1e3)
F = (2 * x * y + 1, x**2)
v.assert_true("F is curl-free", sp.diff(F[1], x) - sp.diff(F[0], y) == 0)
phi = x**2 * y + x
v.assert_true("phi is a potential for F", sp.diff(phi, x) == F[0] and sp.diff(phi, y) == F[1])
work = float(sp.integrate(F[0].subs({x: t, y: 2 * t**2}) * 1 + F[1].subs({x: t, y: 2 * t**2}) * 4 * t, (t, 0, 1)))
v.check("X01.15d", work)

v.check("X01.10j", 100 * iv(2, 0.1) / iv(1, 0.1))
v.check("X01.10k", 100 * 0.1**2 / 24)
S20 = sum(1 / k**2 for k in range(1, 21))
v.check("X01.10l", 1 / 21)
v.check("X01.10m", 1 / 20)
v.check("X01.10n", math.pi**2 / 6)
v.check("X01.10o", S20)
v.check("X01.10p", math.pi**2 / 6 - S20)
v.assert_true("S20 error inside the integral-test bracket", 1 / 21 < math.pi**2 / 6 - S20 < 1 / 20)
xs_, ys_, zs_ = sp.symbols("x_s y_s z_s", real=True)
Gv = (xs_, ys_, zs_**2)
divG = sp.diff(Gv[0], xs_) + sp.diff(Gv[1], ys_) + sp.diff(Gv[2], zs_)
vol = sp.integrate(divG, (xs_, 0, 1), (ys_, 0, 1), (zs_, 0, 1))
flux = (sp.integrate(Gv[0].subs(xs_, 1), (ys_, 0, 1), (zs_, 0, 1)) - sp.integrate(Gv[0].subs(xs_, 0), (ys_, 0, 1), (zs_, 0, 1))
        + sp.integrate(Gv[1].subs(ys_, 1), (xs_, 0, 1), (zs_, 0, 1)) - sp.integrate(Gv[1].subs(ys_, 0), (xs_, 0, 1), (zs_, 0, 1))
        + sp.integrate(Gv[2].subs(zs_, 1), (xs_, 0, 1), (ys_, 0, 1)) - sp.integrate(Gv[2].subs(zs_, 0), (xs_, 0, 1), (ys_, 0, 1)))
v.check("X01.15e", float(vol))
v.check("X01.15f", float(flux))
v.assert_true("exam totals: 4 A + 6 B + 5 C = 128 points", 4 * 5 + 6 * 8 + 5 * 12 == 128)

v.finish()
