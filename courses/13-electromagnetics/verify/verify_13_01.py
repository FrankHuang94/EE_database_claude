#!/usr/bin/env python3
"""Verify every number in chapter 13-01 (vector calculus refresher), its solutions and lab.

Independent routes (not the chapter's curvilinear formulas):
- every field is rewritten in Cartesian coordinates and differentiated there with sympy; the result is then
  projected numerically onto the cylindrical or spherical unit vectors at the point of interest;
- surface, volume and line integrals are evaluated by numerical quadrature over Cartesian parametrizations,
  so both sides of each integral theorem are computed separately.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import dblquad, quad, tplquad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-01-vector-calculus-refresher.md", COURSE / "solutions" / "13-01-solutions.md"]
lab = COURSE / "labs" / "13-01-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-01", *files)
EPS0, MU0 = 8.8541878128e-12, 4e-7 * math.pi
x, y, z = sp.symbols("x y z", real=True)
RHO = sp.sqrt(x ** 2 + y ** 2)
R = sp.sqrt(x ** 2 + y ** 2 + z ** 2)
PHI = sp.atan2(y, x)
THETA = sp.acos(z / R)


def unit(kind, X, Y, Z):
    """Unit vectors at a Cartesian point, from their definitions as derivatives of position."""
    rho, r = math.hypot(X, Y), math.sqrt(X * X + Y * Y + Z * Z)
    ph, th = math.atan2(Y, X), math.acos(Z / r)
    if kind == "cyl":
        return {"rho": np.array([math.cos(ph), math.sin(ph), 0]), "phi": np.array([-math.sin(ph), math.cos(ph), 0]),
                "z": np.array([0, 0, 1.0])}
    return {"r": np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)]),
            "theta": np.array([math.cos(th) * math.cos(ph), math.cos(th) * math.sin(ph), -math.sin(th)]),
            "phi": np.array([-math.sin(ph), math.cos(ph), 0])}


def cart_vec(comps):
    return sp.Matrix(comps)


def grad(f):
    return sp.Matrix([sp.diff(f, s) for s in (x, y, z)])


def div(F):
    return sp.diff(F[0], x) + sp.diff(F[1], y) + sp.diff(F[2], z)


def curl(F):
    return sp.Matrix([sp.diff(F[2], y) - sp.diff(F[1], z), sp.diff(F[0], z) - sp.diff(F[2], x),
                      sp.diff(F[1], x) - sp.diff(F[0], y)])


def at(expr, X, Y, Z):
    return np.array(sp.Matrix(expr).subs({x: X, y: Y, z: Z}).evalf(), dtype=float).ravel()


# symbolic unit vectors in Cartesian components
rho_hat = sp.Matrix([x / RHO, y / RHO, 0])
phi_hat = sp.Matrix([-y / RHO, x / RHO, 0])
r_hat = sp.Matrix([x / R, y / R, z / R])

# ============================================================ Example 1
P = (1.0, math.sqrt(3), 2.0)
v.check("Ex 13-01.1a", math.hypot(P[0], P[1]))
v.check("Ex 13-01.1b", math.degrees(math.atan2(P[1], P[0])))
v.check("Ex 13-01.1c", math.sqrt(sum(c * c for c in P)))
v.check("Ex 13-01.1d", math.degrees(math.acos(P[2] / math.sqrt(sum(c * c for c in P)))))
A = np.array([1.0, 1.0, 0.0])
uc, us = unit("cyl", *P), unit("sph", *P)
v.check("Ex 13-01.1e", A @ uc["rho"])
v.check("Ex 13-01.1f", A @ uc["phi"])
v.check("Ex 13-01.1g", A @ us["r"])
v.check("Ex 13-01.1h", A @ us["theta"])
v.assert_true("components preserve the magnitude", abs((A @ us["r"]) ** 2 + (A @ us["theta"]) ** 2 + (A @ us["phi"]) ** 2 - 2) < 1e-12)

# ============================================================ Example 2: dipole field = -grad V (Cartesian differentiation)
p = 1e-12
Vd = p * (z / R) / (4 * sp.pi * EPS0 * R ** 2)
Pt = (1e-3 * math.sin(math.radians(60)), 0.0, 1e-3 * math.cos(math.radians(60)))
Ed = at(-grad(Vd), *Pt)
us = unit("sph", *Pt)
v.check("Ex 13-01.2a", float(Vd.subs({x: Pt[0], y: Pt[1], z: Pt[2]})))
v.check("Ex 13-01.2b", Ed @ us["r"] / 1e6)
v.check("Ex 13-01.2c", Ed @ us["theta"] / 1e6)
v.check("Ex 13-01.2d", np.linalg.norm(Ed) / 1e6)

# ============================================================ Example 3: source-free exponents
n = sp.symbols("n")
for key, base, hat in (("Ex 13-01.3a", R, r_hat), ("Ex 13-01.3b", RHO, rho_hat)):
    sols = [s for s in range(-4, 3) if abs(float(div(base ** s * hat).subs({x: 0.7, y: -0.4, z: 0.5}))) < 1e-12]
    v.check(key, sols[0])
    v.assert_true(f"{key}: a single source-free exponent in -4..2", len(sols) == 1)
rho0 = sp.symbols("rho0", positive=True)
v.assert_true("Gauss's law inside the uniform sphere: div(rho0 r/3 r_hat) = rho0",
              sp.simplify(div(rho0 * R / 3 * r_hat) - rho0) == 0)

# ============================================================ Example 4: curl of the wire's field
I, a = 10.0, 1e-3
B_in = MU0 * I * RHO / (2 * sp.pi * a ** 2) * phi_hat
B_out = MU0 * I / (2 * sp.pi * RHO) * phi_hat
J = I / (math.pi * a ** 2)
v.check("Ex 13-01.4a", J)
v.assert_true("inside: curl B = mu0 J z_hat", np.allclose(at(curl(B_in), 3e-4, 2e-4, 0.1), [0, 0, MU0 * J], rtol=1e-12))
v.assert_true("outside: curl B = 0", np.allclose(at(curl(B_out), 2e-3, 1e-3, 0.1), [0, 0, 0], atol=1e-12))
v.check("Ex 13-01.4b", np.linalg.norm(at(B_in, 0.5e-3, 0, 0)) * 1e3)
v.check("Ex 13-01.4c", np.linalg.norm(at(B_out, 1e-3, 0, 0)) * 1e3)
v.check("Ex 13-01.4d", np.linalg.norm(at(B_out, 2e-3, 0, 0)) * 1e3)


# ============================================================ Example 5: divergence theorem on a sphere, numerically
def sphere_flux(Ffun, Rs):
    """Flux through a sphere of radius Rs, from the Cartesian field and the outward normal."""
    def integrand(th, ph):
        n_ = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])
        return Ffun(*(Rs * n_)) @ n_ * Rs * Rs * math.sin(th)
    return dblquad(integrand, 0, 2 * math.pi, 0, math.pi, epsabs=1e-10)[0]


F5 = R ** 2 * r_hat
F5f = sp.lambdify((x, y, z), F5, "numpy")
div5 = sp.lambdify((x, y, z), sp.simplify(div(F5)), "numpy")
Rs = 2.0
flux5 = sphere_flux(lambda X, Y, Z: np.array(F5f(X, Y, Z), dtype=float).ravel(), Rs)
vol5 = tplquad(lambda r_, th, ph: div5(r_ * math.sin(th) * math.cos(ph), r_ * math.sin(th) * math.sin(ph),
                                        r_ * math.cos(th)) * r_ * r_ * math.sin(th),
               0, 2 * math.pi, 0, math.pi, 1e-9, Rs, epsabs=1e-9)[0]
v.check("Ex 13-01.5a", flux5)
v.check("Ex 13-01.5b", vol5)

# ============================================================ Example 6: Stokes on a disc and a hemisphere
F6 = sp.Matrix([-y, x, 0])
c6 = sp.lambdify((x, y, z), curl(F6), "numpy")
Rc = 1.5
circ = quad(lambda t: np.array([-Rc * math.sin(t), Rc * math.cos(t), 0]) @ np.array([-Rc * math.sin(t), Rc * math.cos(t), 0]),
            0, 2 * math.pi)[0]
disc = dblquad(lambda r_, ph: np.array(c6(r_ * math.cos(ph), r_ * math.sin(ph), 0), dtype=float).ravel()[2] * r_,
               0, 2 * math.pi, 0, Rc)[0]
dome = dblquad(lambda th, ph: (lambda n_: np.array(c6(*(Rc * n_)), dtype=float).ravel() @ n_)(
    np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])) * Rc * Rc * math.sin(th),
    0, 2 * math.pi, 0, math.pi / 2)[0]
v.check("Ex 13-01.6a", circ)
v.check("Ex 13-01.6b", disc)
v.check("Ex 13-01.6c", dome)

# ============================================================ solutions
P1 = (-2.0, 2.0, 1.0)
v.check("13-01.1a", math.hypot(P1[0], P1[1]))
v.check("13-01.1b", math.degrees(math.atan2(P1[1], P1[0])))
v.check("13-01.1c", math.sqrt(sum(c * c for c in P1)))
v.check("13-01.1d", math.degrees(math.acos(P1[2] / 3)))
rr, th2, ph2 = 4.0, math.radians(30), math.radians(210)
xyz2 = rr * np.array([math.sin(th2) * math.cos(ph2), math.sin(th2) * math.sin(ph2), math.cos(th2)])
v.check("13-01.2a", xyz2[0])
v.check("13-01.2b", xyz2[1])
v.check("13-01.2c", xyz2[2])
v.check("13-01.3a", quad(lambda t: math.hypot(-3 * math.sin(t), 3 * math.cos(t)), 0, math.pi / 2)[0])
v.check("13-01.3b", dblquad(lambda th, ph: 4 * math.sin(th), 0, 2 * math.pi, 0, math.pi / 6)[0])
V4 = 10 * RHO ** 2 * sp.sin(PHI)
P4 = (math.cos(math.radians(30)), math.sin(math.radians(30)), 0.0)
g4 = at(grad(V4), *P4)
u4 = unit("cyl", *P4)
v.check("13-01.4a", g4 @ u4["rho"])
v.check("13-01.4b", g4 @ u4["phi"])
v.check("13-01.4c", np.linalg.norm(g4))
A5 = RHO ** 2 * sp.cos(PHI) * rho_hat + RHO * sp.sin(PHI) * phi_hat
v.check("13-01.5a", float(div(A5).subs({x: 2.0, y: 1e-12, z: 0})))
A6 = R * sp.sin(THETA) * phi_hat
c6v = at(curl(A6), 0.3, -0.7, 0.4)
v.check("13-01.6a", np.linalg.norm(c6v))
v.assert_true("curl of r sin(theta) phi_hat is 2 z_hat", np.allclose(c6v, [0, 0, 2], atol=1e-12))
lap = lambda f: div(grad(f))  # noqa: E731
pt = {x: 0.6, y: -0.3, z: 0.8}
v.check("13-01.7a", max(abs(float(lap(1 / R).subs(pt))), abs(float(lap(sp.log(RHO)).subs(pt)))))
v.check("13-01.7b", float(lap(R ** 2).subs(pt)))
v.check("13-01.7c", float(lap(RHO ** 2).subs(pt)))
F8 = RHO * rho_hat + sp.Matrix([0, 0, z])
d8 = sp.lambdify((x, y, z), div(F8), "numpy")
vol8 = tplquad(lambda zz, r_, ph: d8(r_ * math.cos(ph), r_ * math.sin(ph), zz) * r_, 0, 2 * math.pi, 1e-9, 1, 0, 2)[0]
F8f = sp.lambdify((x, y, z), F8, "numpy")
side = dblquad(lambda zz, ph: np.array(F8f(math.cos(ph), math.sin(ph), zz), dtype=float).ravel()
               @ np.array([math.cos(ph), math.sin(ph), 0]), 0, 2 * math.pi, 0, 2)[0]
top = dblquad(lambda r_, ph: np.array(F8f(r_ * math.cos(ph) + 1e-12, r_ * math.sin(ph), 2), dtype=float).ravel()[2] * r_,
              0, 2 * math.pi, 0, 1)[0]
bot = -dblquad(lambda r_, ph: np.array(F8f(r_ * math.cos(ph) + 1e-12, r_ * math.sin(ph), 0), dtype=float).ravel()[2] * r_,
               0, 2 * math.pi, 0, 1)[0]
v.check("13-01.8a", vol8)
v.check("13-01.8b", side)
v.check("13-01.8c", top)
v.check("13-01.8d", bot)
v.assert_true("problem 8: flux equals volume integral", abs(side + top + bot - vol8) < 1e-6)
# 9: circulation along the four edges and flux of the curl
F9 = lambda X, Y: np.array([0.0, X * X])  # noqa: E731
edges = [((0, 0), (1, 0)), ((1, 0), (1, 1)), ((1, 1), (0, 1)), ((0, 1), (0, 0))]
circ9 = sum(quad(lambda t, a_=a_, b_=b_: F9(*(np.array(a_) + t * (np.array(b_) - np.array(a_))))
                 @ (np.array(b_) - np.array(a_)), 0, 1)[0] for a_, b_ in edges)
c9 = sp.lambdify((x, y, z), curl(sp.Matrix([0, x ** 2, 0]))[2], "numpy")
v.check("13-01.9a", circ9)
v.check("13-01.9b", dblquad(lambda Y, X: c9(X, Y, 0), 0, 1, 0, 1)[0])
A10 = sp.Matrix([x * y, y * z, z * x])
v.check("13-01.10a", sp.simplify(div(curl(A10))))
v.check("13-01.10b", sum(abs(c) for c in sp.simplify(curl(grad(x ** 2 * y)))))
# 11: integral form by quadrature, then the differential check
a11, r0 = 1e-2, 1e-6
Q_in = quad(lambda r_: r0 * r_ / a11 * 2 * math.pi * r_, 0, a11)[0]   # charge per unit length
D11 = Q_in / (2 * math.pi * a11)
v.check("13-01.11a", D11)
v.check("13-01.11b", D11 / EPS0)
Din = r0 * RHO ** 2 / (3 * a11) * rho_hat
v.assert_true("problem 11: div D = rho_v inside", abs(float(div(Din).subs({x: 3e-3, y: 4e-3, z: 0})) - r0 * 5e-3 / a11) < 1e-15)


# 12: flux of r_hat/r^2 through cube faces by quadrature
def cube_flux(center, side):
    cx, cy, cz = center
    h = side / 2
    total = 0.0
    for axis in range(3):
        for sgn in (-1, 1):
            def integ(u, w, axis=axis, sgn=sgn):
                pt_ = [0.0, 0.0, 0.0]
                pt_[axis] = (cx, cy, cz)[axis] + sgn * h
                others = [i for i in range(3) if i != axis]
                pt_[others[0]] = (cx, cy, cz)[others[0]] + u
                pt_[others[1]] = (cx, cy, cz)[others[1]] + w
                r3 = (pt_[0] ** 2 + pt_[1] ** 2 + pt_[2] ** 2) ** 1.5
                return sgn * pt_[axis] / r3
            total += dblquad(integ, -h, h, -h, h, epsabs=1e-11)[0]
    return total


v.check("13-01.12a", cube_flux((0, 0, 0), 2.0))
v.check("13-01.12b", abs(cube_flux((3, 0, 0), 1.0)))

# ============================================================ guided exercise (lab)
if lab.exists():
    Fp = lambda X, Y, Z: np.array([X, Y, Z]) / (X * X + Y * Y + Z * Z) ** 1.5  # noqa: E731
    f_small, f_big = sphere_flux(Fp, 0.01), sphere_flux(Fp, 100.0)
    v.check("Lab 13-01.a", f_small)
    v.check("Lab 13-01.b", f_big)

sys.exit(v.finish())
