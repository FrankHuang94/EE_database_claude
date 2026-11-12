#!/usr/bin/env python3
"""Verify every published number in chapter 01-10, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.constants import epsilon_0, mu_0
from scipy.integrate import dblquad, quad, tplquad
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-10",
    COURSE / "chapters" / "01-10-multivariable-calculus-2.md",
    COURSE / "solutions" / "01-10-solutions.md",
    COURSE / "labs" / "01-10-lab" / "README.md",
)
x, y, z, t, r, th, ph = sp.symbols("x y z t r theta phi", real=True)
KE = 1 / (4 * math.pi * epsilon_0)


def dpw(d, A):
    return math.pi * (d / 2) ** 2 / A - math.pi * d / math.sqrt(2 * A)


def line_int(F, path, a=0, b=1):
    X, Y = path
    integrand = (F[0].subs({x: X, y: Y}) * sp.diff(X, t) + F[1].subs({x: X, y: Y}) * sp.diff(Y, t))
    return float(sp.integrate(sp.simplify(integrand), (t, a, b)))


def div(F):
    return sp.diff(F[0], x) + sp.diff(F[1], y) + sp.diff(F[2], z)


def curl(F):
    return (sp.diff(F[2], y) - sp.diff(F[1], z), sp.diff(F[0], z) - sp.diff(F[2], x), sp.diff(F[1], x) - sp.diff(F[0], y))


# ---------------------------------------------------------------- theory identities
v.assert_true("polar Jacobian = r", sp.simplify(sp.Matrix([r * sp.cos(th), r * sp.sin(th)]).jacobian([r, th]).det()) == r)
rho = sp.symbols("rho", positive=True)
sph = sp.Matrix([rho * sp.sin(ph) * sp.cos(th), rho * sp.sin(ph) * sp.sin(th), rho * sp.cos(ph)])
v.assert_true("spherical Jacobian = rho^2 sin phi", sp.simplify(sph.jacobian([rho, ph, th]).det()) == rho**2 * sp.sin(ph))
v.assert_true("curl of a gradient is zero", all(sp.simplify(c) == 0 for c in curl([sp.diff(x**2 * y * z, s) for s in (x, y, z)])))
v.assert_true("Gaussian integral = sqrt(pi)", sp.integrate(sp.exp(-x**2), (x, -sp.oo, sp.oo)) == sp.sqrt(sp.pi))
v.assert_true("Q8: beam fraction within w/2 = 39.3 %", round(100 * (1 - math.exp(-0.5)), 1) == 39.3)
v.assert_true("field 1 cm from 1 A = 20 uT", round(mu_0 / (2 * math.pi * 0.01) * 1e6) == 20)
v.assert_true("Q2 = 9; Q4 flux = 20", math.isclose(2 * 4.5, 9) and math.isclose(5 * 4, 20))
v.assert_true("300 mm wafer area 70686 mm^2", round(math.pi * 150**2) == 70686)

# ---------------------------------------------------------------- examples
p1 = lambda yy, xx: 0.2 + 0.02 * xx * yy  # noqa: E731
P1 = dblquad(p1, 0, 10, 0, 10)[0]
v.check("Ex 01-10.1a", P1)
v.check("Ex 01-10.1b", P1 / 100)
v.check("Ex 01-10.1c", p1(10, 10))
v.check("Ex 01-10.1d", p1(10, 10) / (P1 / 100))

I_g = quad(lambda s: math.exp(-s * s), -np.inf, np.inf)[0]
v.check("Ex 01-10.2a", I_g)
w = 1.0
frac = lambda a: quad(lambda rr: math.exp(-2 * rr * rr / w**2) * rr, 0, a)[0] / quad(lambda rr: math.exp(-2 * rr * rr / w**2) * rr, 0, np.inf)[0]  # noqa: E731
v.check("Ex 01-10.2b", 100 * frac(1.0))

v.check("Ex 01-10.3a", dpw(300, 100))
v.check("Ex 01-10.3b", 100 * (math.pi * 300 / math.sqrt(200)) / (math.pi * 150**2 / 100))
v.check("Ex 01-10.3c", dpw(300, 800))
v.check("Ex 01-10.3d", 100 * (math.pi * 300 / math.sqrt(1600)) / (math.pi * 150**2 / 800))
v.assert_true("edge-loss ratio ≈ sqrt(8)", round(26.7 / 9.4, 1) == round(math.sqrt(8), 1))

Fc = (2 * x * y, x**2)
v.check("Ex 01-10.4a", line_int(Fc, (t, 2 * t)))
v.assert_true("axis path also gives 2",
              math.isclose(line_int(Fc, (t, 0 * t)) + line_int(Fc, (1 + 0 * t, 2 * t)), 2.0))
v.check("Ex 01-10.4b", mu_0 * 1.0)

rho0, Rs = 1e-6, 0.1
Qr = lambda rr: quad(lambda s: rho0 * (1 - s / Rs) * 4 * math.pi * s * s, 0, rr)[0]  # noqa: E731
v.check("Ex 01-10.5a", Qr(Rs))
v.check("Ex 01-10.5b", KE * Qr(Rs) / Rs**2)
Q3 = tplquad(lambda rr, pp, tt: rho0 * (1 - rr / Rs) * rr**2 * math.sin(pp), 0, 2 * math.pi, 0, math.pi, 0, Rs)[0]
v.assert_true("full triple integral agrees", math.isclose(Q3, Qr(Rs), rel_tol=1e-9))

# ---------------------------------------------------------------- problems
v.check("01-10.1a", float(sp.integrate(sp.integrate(x + y, (y, 0, 2)), (x, 0, 1))))
v.check("01-10.1b", float(sp.integrate(sp.integrate(x * y, (y, 0, x)), (x, 0, 1))))
v.check("01-10.1c", dblquad(lambda xx, yy: math.exp(xx * xx), 0, 1, lambda yy: yy, lambda yy: 1)[0])
v.check("01-10.2a", float(sp.integrate(sp.integrate(r, (r, 1, 2)), (th, 0, 2 * sp.pi))))
v.check("01-10.2b", float(sp.integrate(sp.integrate(r**3, (r, 0, 1)), (th, 0, 2 * sp.pi))))
v.check("01-10.2c", float(sp.integrate(sp.integrate(sp.exp(-r**2) * r, (r, 0, 2)), (th, 0, 2 * sp.pi))))
v.check("01-10.3a", float(sp.integrate(rho**2 * sp.sin(ph), (rho, 0, 2), (ph, 0, sp.pi), (th, 0, 2 * sp.pi))))
v.check("01-10.3b", float(sp.integrate(r, (r, 0, 1), (th, 0, 2 * sp.pi), (z, 0, 3))))
v.check("01-10.3c", float(sp.integrate(rho**4 * sp.sin(ph), (rho, 0, 1), (ph, 0, sp.pi), (th, 0, 2 * sp.pi))))
F4 = (x**2, x * y, z)
v.check("01-10.4a", float(div(F4).subs({x: 1, y: 2, z: 3})))
v.check("01-10.4b", float(curl(F4)[2].subs({x: 1, y: 2, z: 3})))
v.check("01-10.4c", float(curl((-y, x, 0 * z))[2]))
v.assert_true("curl F = (0, 0, y); div G = 0",
              [sp.simplify(c) for c in curl(F4)] == [0, 0, y] and div((-y, x, 0 * z)) == 0)

Q5 = dblquad(lambda yy, xx: 2e-9 * (1 + xx / 0.1), 0, 0.1, 0, 0.05)[0]
v.check("01-10.5a", Q5 * 1e12)
v.check("01-10.5b", Q5 / (0.1 * 0.05) * 1e9)

P6 = dblquad(lambda yy, xx: 0.3 + 0.9 * math.exp(-xx / 2), 0, 8, 0, 6)[0]
v.check("01-10.6a", P6)
v.check("01-10.6b", P6 / 48)
v.check("01-10.6c", 1.2 / (P6 / 48))

I0, wb = sp.symbols("I_0 w", positive=True)
v.assert_true("beam total power = pi I0 w^2 / 2",
              sp.simplify(sp.integrate(I0 * sp.exp(-2 * r**2 / wb**2) * r, (r, 0, sp.oo)) * 2 * sp.pi - sp.pi * I0 * wb**2 / 2) == 0)
v.check("01-10.7a", 100 * frac(1.0))
v.check("01-10.7b", 100 * frac(1.5))
v.check("01-10.7c", 100 * (1 - math.exp(-2 * (4.5 / 5.2) ** 2)))

F8 = (y**2, 2 * x * y)
v.assert_true("P8 field is conservative", sp.diff(F8[1], x) - sp.diff(F8[0], y) == 0)
v.check("01-10.8a", line_int(F8, (2 * t, t)))
G8 = (-y, x)
v.check("01-10.8b", line_int(G8, (2 * sp.cos(t), 2 * sp.sin(t)), 0, 2 * math.pi))

v.check("01-10.9a", 1000 * 0.02)
v.check("01-10.9b", quad(lambda s: KE * 1e-18 / s**2, 0.01, np.inf)[0])

v.check("01-10.10a", mu_0 * 2)
v.check("01-10.10b", mu_0 * 2 / (2 * math.pi * 0.01) * 1e6)
v.check("01-10.10c", 1e-3 * 10e-6 * 2 * math.pi * 50 * 1e6)

a11 = 2.0
v.check("01-10.11a", a11 * 4 * math.pi * a11**2)
v.assert_true("divergence theorem for (x, y, z), radius 2",
              math.isclose(3 * 4 / 3 * math.pi * a11**3, a11 * 4 * math.pi * a11**2))
v.check("01-10.11b", 1e-9 / epsilon_0)

E12 = lambda rr: KE * Qr(rr) / rr**2  # noqa: E731
v.check("01-10.12a", Qr(0.05))
v.check("01-10.12b", E12(0.05))
m12 = minimize_scalar(lambda rr: -E12(rr), bounds=(1e-3, Rs), method="bounded", options={"xatol": 1e-10})
v.check("01-10.12c", m12.x)
v.check("01-10.12d", -m12.fun)

rho_cu, Rw = 1.72e-8, 1e-3
for f, a, b, c in [(1e5, "a", "c", "e"), (1e6, "b", "d", "f")]:
    dl = math.sqrt(rho_cu / (math.pi * f * mu_0))
    Aeff = quad(lambda rr: math.exp((rr - Rw) / dl) * 2 * math.pi * rr, 0, Rw)[0]
    v.check(f"01-10.13{a}", dl * 1e3)
    v.check(f"01-10.13{b}", Aeff * 1e6)
    v.check(f"01-10.13{c}", math.pi * Rw**2 / Aeff)

good = {}
for A in (25, 100, 400, 800, 200):
    good[A] = dpw(300, A) * math.exp(-0.001 * A)
v.check("01-10.14a", dpw(300, 25))
v.check("01-10.14b", good[25])
v.check("01-10.14c", 100 * math.exp(-0.1))
v.check("01-10.14d", good[100])
v.check("01-10.14e", good[400])
v.check("01-10.14f", 100 * math.exp(-0.8))
v.check("01-10.14g", good[800])
v.check("01-10.14h", good[100] / good[800])
v.check("01-10.14i", good[200] / 4)
v.check("01-10.14j", 100 * math.exp(-0.025))
v.check("01-10.14k", dpw(300, 100))
v.check("01-10.14l", dpw(300, 400))
v.check("01-10.14m", 100 * math.exp(-0.4))
v.check("01-10.14n", dpw(300, 800))
v.check("01-10.14o", dpw(300, 200))
v.check("01-10.14p", good[200])
v.check("01-10.14q", 100 * math.exp(-0.2))
v.check("01-10.14r", (good[200] / 4) / good[800])
v.check("01-10.16a", 1e-9 / (2 * math.pi * epsilon_0 * 0.01))
v.check("01-10.16b", math.log(3))
C16 = 2 * math.pi * epsilon_0 * 2.1 / math.log(3)
v.check("01-10.16c", C16 * 1e12)
v.check("01-10.16d", C16 * 50 * 1e9)
v.check("01-10.16e", 50 / (0.5e-3 * math.log(3)) / 1e3)
rr_ = sp.symbols("rr", positive=True)
v.assert_true("coax V = λ/(2πε) ln(b/a) by integration",
              sp.simplify(sp.integrate(1 / rr_, (rr_, 1, 3)) - sp.log(3)) == 0)
# §3.6/3.8 cylinder flux check: F = (x, y, 0) through the side of radius a, height h equals 2πa²h = ∭ div F
aa_, hh_, tt_, zz_ = sp.symbols("a h theta z", positive=True)
side = sp.integrate(sp.integrate(aa_**2, (tt_, 0, 2 * sp.pi)), (zz_, 0, hh_))
v.assert_true("cylinder side flux = 2πa²h = volume integral of div F", sp.simplify(side - 2 * sp.pi * aa_**2 * hh_) == 0)

v.check("01-10.15a", float(sp.integrate(sp.Rational(1, 2) * ((3 * sp.cos(t)) * sp.diff(2 * sp.sin(t), t)
                                                           - (2 * sp.sin(t)) * sp.diff(3 * sp.cos(t), t)), (t, 0, 2 * sp.pi))))
W15 = (-y / (x**2 + y**2), x / (x**2 + y**2))
v.check("01-10.15b", line_int(W15, (sp.cos(t), sp.sin(t)), 0, 2 * math.pi))
v.assert_true("P15 curl is zero away from the origin",
              sp.simplify(sp.diff(W15[1], x) - sp.diff(W15[0], y)) == 0)

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-10.a", math.sqrt(100))
v.check("Lab 01-10.b", dpw(300, 625))


def whole_dies(d, s, ox=0.0, oy=0.0):
    count = 0
    for i in np.arange(-d / 2 - s, d / 2 + s, s) + ox:
        for j in np.arange(-d / 2 - s, d / 2 + s, s) + oy:
            if all(math.hypot(cx, cy) <= d / 2 for cx, cy in [(i, j), (i + s, j), (i, j + s), (i + s, j + s)]):
                count += 1
    return count


v.check("Lab 01-10.c", whole_dies(300.0, 25.0))

v.finish()
