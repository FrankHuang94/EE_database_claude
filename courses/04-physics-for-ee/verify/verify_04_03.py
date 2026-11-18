#!/usr/bin/env python3
"""Verify every number published in chapter 04-03, its solutions and its lab handout.

Gauss's-law results are checked independently of Gauss's law wherever possible:
fluxes by numerical surface integration of Coulomb fields, sphere fields by direct
integration of Coulomb's law over the volume, line and slab fields by integrating
point and sheet contributions, junction fields by integrating the charge density,
and the conductor-plate problem by solving the zero-field conditions as a linear system.
"""
from __future__ import annotations

import sys
import warnings
from math import cos, pi, radians, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import dblquad, quad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C = HERE.parent
v = Verifier.from_files("04-03", C / "chapters" / "04-03-gauss-law.md",
                        C / "solutions" / "04-03-solutions.md", C / "labs" / "04-03-lab" / "README.md")
Q_E = 1.602176634e-19
EPS0 = 8.8541878188e-12
KE = 1 / (4 * pi * EPS0)
EPS_SI = 11.7 * EPS0


def point_field(q, src, p, n=2.0):
    d = np.asarray(p, float) - np.asarray(src, float)
    r = np.linalg.norm(d)
    return KE * q * d / r ** (n + 1)


def cube_flux(q, src, half=0.5, center=(0.0, 0.0, 0.0), face=None):
    """Outward flux of a point charge through an axis-aligned cube, by 2-D quadrature on each face."""
    c = np.asarray(center, float)
    total, faces = 0.0, []
    for axis in range(3):
        for sign in (-1, 1):
            o = [i for i in range(3) if i != axis]

            def integrand(b, a, axis=axis, sign=sign, o=o):
                p = c.copy()
                p[axis] += sign * half
                p[o[0]] += a
                p[o[1]] += b
                return sign * point_field(q, src, p)[axis]
            val = dblquad(integrand, -half, half, -half, half, epsabs=0, epsrel=1e-9)[0]
            faces.append(val)
            total += val
    return (total, faces) if face is None else faces[face]


def sphere_flux(q, r, n=2.0):
    """Flux through a sphere of radius r centered on q for a 1/r^n force, by quadrature over the sphere."""
    f = lambda th: KE * q / r**n * 2 * pi * r * r * np.sin(th)
    return quad(f, 0, pi)[0]


def shell_axial(s, r):
    """Field at distance r from the center of a thin shell of radius s and unit charge, by direct Coulomb integration."""
    f = lambda u: (r - s * u) / (r * r + s * s - 2 * r * s * u) ** 1.5
    return 0.5 * KE * quad(f, -1, 1, epsabs=0, epsrel=1e-11, limit=400)[0]


def solid_sphere_field(Q, R, r):
    rho = Q / (4 / 3 * pi * R**3)
    g = lambda s: rho * 4 * pi * s * s * shell_axial(s, r)
    return quad(g, 0, R, points=[r] if r < R else None, epsabs=0, epsrel=1e-10, limit=400)[0]


def line_field(lam, y):
    """Field of an infinite line at distance y, integrating point contributions along the line."""
    f = lambda x: KE * lam * y / (x * x + y * y) ** 1.5
    return 2 * quad(f, 0, np.inf, epsabs=0, epsrel=1e-11)[0]


def cylinder_field(rho, a, r):
    """Field of a uniformly charged infinite cylinder, built from line charges over its cross-section."""
    # each line element at (s, phi) contributes 2 k_e dλ / distance, resolved radially
    def integrand(phi, s):
        dx, dy = r - s * np.cos(phi), -s * np.sin(phi)
        d2 = dx * dx + dy * dy
        return 2 * KE * rho * s * dx / d2
    return dblquad(integrand, 0, a, 0, 2 * pi, epsabs=0, epsrel=1e-9)[0] if r > a else None


def slab_field(rho, t, x):
    """Field of a uniformly charged slab, summing the σ/(2ε0) fields of its thin layers."""
    f = lambda xp: rho / (2 * EPS0) * np.sign(x - xp)
    return quad(f, -t / 2, t / 2, points=[x] if abs(x) < t / 2 else None)[0]


def piecewise_field(edges, rhos, n=20000):
    """Field of a 1-D charge profile, integrating rho piece by piece with the midpoint rule (Gauss: eps E = running integral of rho)."""
    xs, Es, acc = [edges[0]], [0.0], 0.0
    for (x0, x1), rho in zip(zip(edges[:-1], edges[1:]), rhos):
        xx = np.linspace(x0, x1, n + 1)
        mid = 0.5 * (xx[:-1] + xx[1:])
        inc = np.cumsum(rho(mid) * np.diff(xx))
        xs.extend(xx[1:])
        Es.extend(acc + inc)
        acc += inc[-1]
    return np.array(xs), np.array(Es) / EPS_SI


# ---------------------------------------------------------------- theory keys
v.check("T 04-03.a", sphere_flux(1e-9, 0.37))
v.check("T 04-03.b", dblquad(lambda th, ph: np.sin(th), 0, 2 * pi, 0, pi)[0])
v.check("T 04-03.c", 11.7 / 3.9)
v.assert_true("flux independent of sphere radius", abs(sphere_flux(1e-9, 0.01) / sphere_flux(1e-9, 10) - 1) < 1e-12)
off_center, _ = cube_flux(1e-9, (0.2, -0.1, 0.3))
v.assert_true("off-center charge in a cube: flux q/eps0", abs(off_center / (1e-9 / EPS0) - 1) < 1e-6)
outside, _ = cube_flux(1e-9, (0.9, 0.1, 0.0))
v.assert_true("charge outside a cube: zero flux", abs(outside) < 1e-6)

# ---------------------------------------------------------------- examples
E0, A = 2000.0, 0.1 * 0.2
n_hat = np.array([cos(radians(30)), np.sin(radians(30)), 0])
v.check("Ex 04-03.1a", float(np.dot([E0, 0, 0], n_hat)) * A)
v.check("Ex 04-03.1b", float(np.dot([E0, 0, 0], [-1, 0, 0])) * 0.01)
v.check("Ex 04-03.1c", float(np.dot([E0, 0, 0], [1, 0, 0])) * 0.01)
v.check("Ex 04-03.1d", E0 * 0.01 - E0 * 0.01)
tot, faces = cube_flux(1e-9, (0, 0, 0), half=0.05)
v.check("Ex 04-03.2a", tot)
v.check("Ex 04-03.2b", faces[0])
v.check("Ex 04-03.2c", np.linalg.norm(point_field(1e-9, (0, 0, 0), (0.01, 0, 0))))
for key, r in (("Ex 04-03.3a", 0.02), ("Ex 04-03.3b", 0.05), ("Ex 04-03.3c", 0.10)):
    v.check(key, solid_sphere_field(1e-8, 0.05, r))
v.check("Ex 04-03.3d", abs(1e-8 * shell_axial(0.05, 0.02)))
lam, a, b = 2e-9, 5e-4, 2e-3
Ea, Eb = line_field(lam, a), line_field(lam, b)
v.check("Ex 04-03.4a", Ea)
v.check("Ex 04-03.4b", Eb)
v.check("Ex 04-03.4c", lam / (2 * pi * a))
v.check("Ex 04-03.4d", -lam / (2 * pi * b))
v.assert_true("sigma/eps0 reproduces the coax fields", abs(lam / (2 * pi * a) / EPS0 / Ea - 1) < 1e-9)
v.check("Ex 04-03.4e", line_field(lam, 5e-3) + line_field(-lam, 5e-3))
v.check("Ex 04-03.4f", 3e6 / line_field(1.0, a) * 1e9)
q5 = 2e-9
v.check("Ex 04-03.5a", np.linalg.norm(point_field(q5, (0, 0, 0), (0.02, 0, 0))))
v.check("Ex 04-03.5b", 0)
s_in, s_out = -q5 / (4 * pi * 0.03**2), q5 / (4 * pi * 0.04**2)
v.check("Ex 04-03.5c", s_in)
v.check("Ex 04-03.5d", s_out)
v.check("Ex 04-03.5e", s_out / EPS0)
# outside: point charge + inner shell (-q) + outer shell (+q), each shell by direct integration
E10 = KE * q5 / 0.1**2 + (-q5) * shell_axial(0.03, 0.1) + q5 * shell_axial(0.04, 0.1)
v.check("Ex 04-03.5f", E10)
v.check("Ex 04-03.5g", KE * q5 / 0.1**2 + (-q5) * shell_axial(0.03, 0.1))
v.assert_true("shells cancel the field in the metal",
              abs(KE * q5 / 0.035**2 + (-q5) * shell_axial(0.03, 0.035) + q5 * shell_axial(0.04, 0.035)) < 1e-6)

# pn junction: integrate rho(x) numerically
NA, ND, xn = 1e23, 1e22, 0.3e-6
xp = ND * xn / NA
x, Ex = piecewise_field([-xp, 0.0, xn], [lambda u: -Q_E * NA + 0 * u, lambda u: Q_E * ND + 0 * u])
v.check("Ex 04-03.6a", EPS_SI)
v.check("Ex 04-03.6b", xp * 1e6)
v.check("Ex 04-03.6c", (xn + xp) * 1e6)
v.check("Ex 04-03.6d", np.max(np.abs(Ex)))
v.check("Ex 04-03.6e", np.max(np.abs(Ex)) / 1e5)
v.check("Ex 04-03.6f", ND * 1e-6 * xn * 100)
v.check("Ex 04-03.6g", abs(np.trapezoid(Ex, x)))
v.assert_true("junction field returns to zero (neutrality)", abs(Ex[-1]) < 1e-6 * np.max(np.abs(Ex)))
VT = 1.380649e-23 * 300 / Q_E
Vbi = VT * np.log(NA * ND / 1e16**2)
W_eq = sqrt(2 * EPS_SI * Vbi / Q_E * (1 / NA + 1 / ND))
v.assert_true("x_n = 0.3 um is close to equilibrium (n_i = 1e10 cm^-3)", abs(W_eq * NA / (NA + ND) / xn - 1) < 0.02)
Afing = pi * 4.5e-3**2
CF = 3 * EPS0 * Afing / 2e-3
v.check("Ex 04-03.7a", Afing * 1e6)
v.check("Ex 04-03.7b", CF * 1e12)
v.check("Ex 04-03.7c", CF / 33e-12 * 100)
v.check("Ex 04-03.7d", 3 * EPS0 * Afing / 4e-3 * 1e12)

# ---------------------------------------------------------------- solutions
v.check("04-03.1a", 500 * 6)
v.check("04-03.1b", abs(np.dot([0, 0, -500], [np.sin(radians(40)), 0, cos(radians(40))])) * 6)
v.check("04-03.1c", 0)
v.check("04-03.2a", EPS0 * -5000)
v.check("04-03.3a", np.linalg.norm(point_field(5e-9, (0, 0, 0), (0.1, 0, 0))))
v.check("04-03.3b", cube_flux(5e-9, (0, 0, 0), half=0.5)[0])
v.assert_true("same flux through the 10 cm sphere", abs(sphere_flux(5e-9, 0.1) / (5e-9 / EPS0) - 1) < 1e-12)
# corner charge: cube [0, 0.1]^3 with the charge at the origin, by direct surface integration of the far faces
far = []
for axis in range(3):
    o = [i for i in range(3) if i != axis]

    def integ(bb, aa, axis=axis, o=o):
        p = np.zeros(3)
        p[axis] = 0.1
        p[o[0]], p[o[1]] = aa, bb
        return point_field(8e-9, (0, 0, 0), p)[axis]
    far.append(dblquad(integ, 0, 0.1, 0, 0.1, epsabs=0, epsrel=1e-10)[0])
v.check("04-03.4a", sum(far))
v.check("04-03.4b", far[0])
v.check("04-03.5a", abs(KE * -5e-9 / 0.05**2 + 20e-9 * shell_axial(0.1, 0.05)))
v.check("04-03.5b", KE * -5e-9 / 0.15**2 + 20e-9 * shell_axial(0.1, 0.15))
rho6, a6 = 0.01, 1e-3
lam6 = rho6 * pi * a6**2
v.check("04-03.6a", rho6 * 0.5e-3 / (2 * EPS0))
v.check("04-03.6b", line_field(lam6, a6))
v.check("04-03.6c", cylinder_field(rho6, a6, 5e-3))
v.check("04-03.7a", 0)
v.check("04-03.7b", line_field(3e-9, 0.02))
v.check("04-03.7c", line_field(2e-9, 0.04))
for key, xx in (("04-03.8a", 0.0), ("04-03.8b", 0.5e-3), ("04-03.8c", 1e-3), ("04-03.8d", 11e-3)):
    v.check(key, slab_field(1e-4, 2e-3, xx))
smax = EPS0 * 3e6
v.check("04-03.9a", smax)
v.check("04-03.9b", smax / Q_E / 1e4)
v.check("04-03.9c", 1 / (0.3e-7) ** 2)
v.check("04-03.9d", smax / Q_E / 1e4 * (0.3e-7) ** 2)
v.check("04-03.10a", -2)
v.check("04-03.10b", 3 - (-2))
v.check("04-03.10c", 5e-9 / (4 * pi * 0.05**2))
v.check("04-03.10d", 5e-9 * shell_axial(0.05, 0.1))
# four sheets: zero field inside each plate, plus the plate charges
Ap = 0.01
M = np.array([[1, -1, -1, -1], [1, 1, 1, -1], [1, 1, 0, 0], [0, 0, 1, 1]], float)
sig = np.linalg.solve(M, [0, 0, 4e-9 / Ap, -1e-9 / Ap])
v.check("04-03.11a", sig[0] * Ap * 1e9)
v.assert_true("outer faces carry equal charge", abs(sig[0] - sig[3]) < 1e-20)
v.check("04-03.11b", sig[1] * Ap * 1e9)
v.check("04-03.11c", sig[2] * Ap * 1e9)
v.check("04-03.11d", (sig[0] + sig[1] - sig[2] - sig[3]) / (2 * EPS0))
v.check("04-03.11e", sig.sum() / (2 * EPS0))
NA2, ND2, xn2 = 1e24, 1e21, 1e-6
xp2 = ND2 * xn2 / NA2
x2, E2 = piecewise_field([-xp2, 0.0, xn2], [lambda u: -Q_E * NA2 + 0 * u, lambda u: Q_E * ND2 + 0 * u])
v.check("04-03.12a", xp2 * 1e9)
v.check("04-03.12b", np.max(np.abs(E2)))
v.check("04-03.12c", np.max(np.abs(E2)) / 1e5)
v.check("04-03.12d", abs(np.trapezoid(E2, x2)))
Eox = 5e8
v.check("04-03.13a", 3.9 * Eox / 11.7 / 1e8)
v.check("04-03.13b", 3.9 * EPS0 * Eox)
v.check("04-03.13c", 3.9 * EPS0 * Eox / Q_E / 1e4)
# cavity: superpose a big sphere (R = 10 cm) and a -rho sphere (radius 3 cm, centered 2 cm away), at several points
rho14, Rbig, rc, dvec = 1e-6, 0.10, 0.03, np.array([0.02, 0, 0])


def usphere(rho, R, center, p):
    d = np.asarray(p) - center
    r = np.linalg.norm(d)
    Q = rho * 4 / 3 * pi * R**3
    mag = solid_sphere_field(Q, R, r)
    return mag * d / r


pts = [dvec + np.array(o) for o in ((0.005, 0.0, 0.0), (0.0, 0.012, 0.0), (-0.01, 0.0, 0.015))]
Ecav = [usphere(rho14, Rbig, np.zeros(3), p) + usphere(-rho14, rc, dvec, p) for p in pts]
v.check("04-03.14a", np.linalg.norm(Ecav[0]))
v.assert_true("cavity field is uniform", max(np.linalg.norm(E - Ecav[0]) for E in Ecav) < 1e-6 * np.linalg.norm(Ecav[0]))
Ab = pi * 5e-3**2
Cg, Ca = 7 * EPS0 * Ab / 1.5e-3, 2.6 * EPS0 * Ab / 3e-3
v.check("04-03.15a", Cg * 1e12)
v.check("04-03.15b", Cg / 20e-12 * 100)
v.check("04-03.15c", Ca * 1e12)
v.check("04-03.15d", Ca / 20e-12 * 100)
v.check("04-03.15e", Cg / Ca)
v.check("04-03.16a", sphere_flux(1e-9, 2.0, n=2.01) / sphere_flux(1e-9, 1.0, n=2.01))

# ---------------------------------------------------------------- lab
lab_in, _ = cube_flux(1e-9, (0.2, 0.1, -0.3))
lab_out, _ = cube_flux(1e-9, (0.6, 0.0, 0.0))
v.check("Lab 04-03.a", lab_in)
v.check("Lab 04-03.b", lab_out)
v.check("Lab 04-03.c", sphere_flux(1e-9, 3.0, n=2.05) / sphere_flux(1e-9, 1.0, n=2.05))
a_g, W_g = 1e29, 0.5e-6                       # graded junction: rho = q a x for |x| < W/2
xg, Eg = piecewise_field([-W_g / 2, W_g / 2], [lambda u: Q_E * a_g * u])
v.check("Lab 04-03.d", np.max(np.abs(Eg)) / 1e5)
v.check("Lab 04-03.e", 3 * EPS0 * Afing / 1e-3 * 1e12)

sys.exit(v.finish())
