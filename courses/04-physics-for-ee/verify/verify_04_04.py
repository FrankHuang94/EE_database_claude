#!/usr/bin/env python3
"""Verify every number published in chapter 04-04, its solutions and its lab handout.

Independent routes: potentials by numerically integrating -E·dl in from infinity (or by summing
k dq / r over a discretized source), fields by numerically differentiating potentials, capacitances
from the integrated field energy U = Q^2 / 2C, layered dielectrics by integrating E through each layer,
charge sharing by integrating the circuit ODE with an energy accumulator, and the chuck force from a
numerical derivative of the stored energy with respect to the gap.
"""
from __future__ import annotations

import sys
import warnings
from math import cos, exp, hypot, log, pi, radians, sin, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C_DIR = HERE.parent
v = Verifier.from_files("04-04", C_DIR / "chapters" / "04-04-potential-capacitance-and-dielectrics.md",
                        C_DIR / "solutions" / "04-04-solutions.md", C_DIR / "labs" / "04-04-lab" / "README.md")
E_CH = 1.602176634e-19
EPS0 = 8.8541878188e-12
KE = 1 / (4 * pi * EPS0)


def field_pts(charges, p):
    E = np.zeros(2)
    for q, (x0, y0) in charges:
        d = np.asarray(p, float) - np.array([x0, y0])
        E += KE * q * d / np.linalg.norm(d) ** 3
    return E


def potential_by_integration(charges, p, direction=(0.6, 0.8)):
    """V(p) = integral of E·dl from p out to infinity along a ray (substituting s = t/(1-t))."""
    u = np.array(direction) / np.linalg.norm(direction)

    def integrand(t):
        s = t / (1 - t)
        return float(np.dot(field_pts(charges, np.asarray(p) + s * u), u)) / (1 - t) ** 2
    return quad(integrand, 0, 1, epsabs=0, epsrel=1e-11, limit=400)[0]


def ring_potential(Q, R, z):
    return quad(lambda ph: KE * (Q / (2 * pi)) / sqrt(z * z + R * R), 0, 2 * pi)[0]


def disk_potential(sigma, R, z):
    return quad(lambda r: KE * sigma * 2 * pi * r / sqrt(z * z + r * r), 0, R, epsabs=0, epsrel=1e-12)[0]


def deriv(f, x, h):
    return (f(x - 2 * h) - 8 * f(x - h) + 8 * f(x + h) - f(x + 2 * h)) / (12 * h)


def sphere_energy(Q, R, r_hi=np.inf):
    return quad(lambda r: 0.5 * EPS0 * (KE * Q / r**2) ** 2 * 4 * pi * r**2, R, r_hi, epsabs=0, epsrel=1e-12)[0]


def coax_C_per_m(a, b, er=1.0):
    lam = 1e-9
    Vab = quad(lambda r: lam / (2 * pi * er * EPS0 * r), a, b)[0]
    return lam / Vab


def layered_C_per_area(layers, V=1.0):
    """layers = [(thickness, eps_r)]; D is continuous, so integrate E = D/eps through the stack for D = 1."""
    V_per_D = sum(quad(lambda x, er=er: 1 / (er * EPS0), 0, t)[0] for t, er in layers)
    return 1 / V_per_D


def share(C1, V1, C2, V2, R, t_end):
    """Two capacitors joined through R: return final voltages and the energy dissipated (ODE + accumulator)."""
    def rhs(t, y):
        i = (y[0] - y[1]) / R
        return [-i / C1, i / C2, i * i * R]
    tau = R * C1 * C2 / (C1 + C2)
    sol = solve_ivp(rhs, (0, t_end), [V1, V2, 0.0], method="LSODA", rtol=1e-11, atol=1e-15, max_step=tau / 5)
    return sol.y[0, -1], sol.y[1, -1], sol.y[2, -1]


def chuck_force(S, l, er, V, g):
    Cg = lambda gg: EPS0 * S / (gg + l / er)
    return 0.5 * V * V * abs(deriv(Cg, g, 1e-8))


# ---------------------------------------------------------------- theory keys
v.check("T 04-04.a", E_CH * 1.0)
v.check("T 04-04.b", 2e-3 / minimize_scalar(lambda a: -a * log(2e-3 / a), bounds=(1e-5, 1.99e-3), method="bounded",
                                              options={"xatol": 1e-12}).x)
v.check("T 04-04.c", 0.5 * EPS0 * 3e6**2)
v.check("T 04-04.d", 1 / layered_C_per_area([(2e-9, 25)]) * 3.9 * EPS0 * 1e9)
# path independence: straight versus detoured line integral between two points
ch = [(1e-9, (0.0, 0.0)), (-1e-9, (0.04, 0.0))]
A, B = np.array([-0.02, 0.03]), np.array([0.06, -0.015])


def line_work(path, n=40001):
    s = np.linspace(0, 1, n)
    P = np.array([path(si) for si in s])
    dP = np.gradient(P, s, axis=0)
    Ef = np.array([field_pts(ch, p) for p in P])
    return np.trapezoid((Ef * dP).sum(axis=1), s)


perp = np.array([-(B - A)[1], (B - A)[0]]) / np.linalg.norm(B - A)
w_straight = line_work(lambda s: A + s * (B - A))
w_wiggly = line_work(lambda s: A + s * (B - A) + 0.015 * np.sin(5 * pi * s) * perp)
v.assert_true("work is path independent", abs(w_straight - w_wiggly) < 1e-4 * abs(w_straight))

# ---------------------------------------------------------------- examples
c1 = [(2e-9, (0.0, 0.0)), (-2e-9, (0.04, 0.0))]
v.check("Ex 04-04.1a", potential_by_integration(c1, (0.02, 0.03)))
V1b = potential_by_integration(c1, (0.0, 0.03))
v.check("Ex 04-04.1b", V1b)
v.check("Ex 04-04.1c", 1e-9 * V1b)
v.check("Ex 04-04.1d", -2e-9 * potential_by_integration([(2e-9, (0.0, 0.0))], (0.04, 0.0)))
v.check("Ex 04-04.2a", ring_potential(1e-8, 0.05, 0.05))
v.check("Ex 04-04.2b", -deriv(lambda z: ring_potential(1e-8, 0.05, z), 0.05, 1e-5))
v.check("Ex 04-04.2c", ring_potential(1e-8, 0.05, 0.0))
for (kc, kq, ke_, kv), R in ((("Ex 04-04.3a", "Ex 04-04.3c", "Ex 04-04.3e", "Ex 04-04.3g"), 1e-3),
                             (("Ex 04-04.3b", "Ex 04-04.3d", "Ex 04-04.3f", "Ex 04-04.3h"), 0.1)):
    Cs = 1e-18 / (2 * sphere_energy(1e-9, R))          # C = Q^2 / 2U
    v.check(kc, Cs * 1e12)
    v.check(kq, Cs * 1e3)
    v.check(ke_, KE * Cs * 1e3 / R**2)
    v.check(kv, 3e6 / (KE * Cs / R**2) / 1e3)      # surface field per volt is k_e C / R^2
v.check("Ex 04-04.3i", 1e-18 / (2 * sphere_energy(1e-9, 6.371e6)) * 1e3)
Ap, dp = 10e-4, 1e-3
Cp = EPS0 * Ap / dp
v.check("Ex 04-04.4a", Cp * 1e12)
v.check("Ex 04-04.4b", Cp * 100 * 1e12)
v.check("Ex 04-04.4c", 100 / dp)
v.check("Ex 04-04.4d", 0.5 * Cp * 100**2 * 1e9)
v.check("Ex 04-04.4e", quad(lambda x: 0.5 * EPS0 * (100 / dp) ** 2 * Ap, 0, dp)[0] * 1e9)
v.check("Ex 04-04.4f", 3.9 * Cp * 1e12)
a5, b5 = 5e-4, 2e-3
Cc = coax_C_per_m(a5, b5)
v.check("Ex 04-04.5a", Cc * 1e12)
v.check("Ex 04-04.5b", 2e-9 / Cc)
v.check("Ex 04-04.5c", 3e6 * a5 * log(b5 / a5))
opt = minimize_scalar(lambda a: -3e6 * a * log(b5 / a), bounds=(1e-5, 1.99e-3), method="bounded", options={"xatol": 1e-13})
v.check("Ex 04-04.5d", opt.x * 1e3)
v.check("Ex 04-04.5e", -opt.fun)
c_if, c_hk = layered_C_per_area([(0.5e-9, 3.9)]), layered_C_per_area([(2e-9, 25)])
c_st = layered_C_per_area([(0.5e-9, 3.9), (2e-9, 25)])
v.check("Ex 04-04.6a", c_if * 100)
v.check("Ex 04-04.6b", c_hk * 100)
v.check("Ex 04-04.6c", c_st * 100)
v.check("Ex 04-04.6d", 3.9 * EPS0 / c_st * 1e9)
D6 = c_st * 0.7
v.check("Ex 04-04.6e", D6 / (3.9 * EPS0) / 1e8)
v.check("Ex 04-04.6f", D6 / (3.9 * EPS0) * 0.5e-9)
v.check("Ex 04-04.6g", D6 / (25 * EPS0) / 1e8)
v.check("Ex 04-04.6h", D6 / (25 * EPS0) * 2e-9)
vA, vB, lossA = share(1e-6, 10, 1e-6, 0, 10, 1e-3)
_, _, lossB = share(1e-6, 10, 1e-6, 0, 1000, 0.1)
v.check("Ex 04-04.7a", vA)
v.check("Ex 04-04.7b", 0.5 * 1e-6 * 10**2 * 1e6)
v.check("Ex 04-04.7c", (0.5 * 1e-6 * vA**2 + 0.5 * 1e-6 * vB**2) * 1e6)
v.check("Ex 04-04.7d", lossA * 1e6)
v.assert_true("loss is independent of R", abs(lossA - lossB) < 1e-9)
_, vbl, _ = share(10e-15, 1.0, 100e-15, 0.5, 1e3, 1e-9)
v.check("Ex 04-04.7e", (vbl - 0.5) * 1e3)
v.check("Ex 04-04.7f", 10e-15 * 1.0 / E_CH)
S8, l8, er8, V8 = pi * 0.1**2, 0.54e-3, 8.8, 1000.0
C8 = layered_C_per_area([(l8, er8)]) * S8
v.check("Ex 04-04.8a", C8 * 1e9)
v.check("Ex 04-04.8b", C8 * V8 * 1e6)
D8 = C8 * V8 / S8
v.check("Ex 04-04.8c", D8)
v.check("Ex 04-04.8d", D8 / (er8 * EPS0))
v.check("Ex 04-04.8e", D8 / EPS0)
F8 = chuck_force(S8, l8, er8, V8, 0.0)
v.check("Ex 04-04.8f", F8 / S8)
v.check("Ex 04-04.8g", F8)
v.assert_true("energy-method force equals D^2 S / (2 eps0)", abs(F8 / (D8**2 * S8 / (2 * EPS0)) - 1) < 1e-8)

# ---------------------------------------------------------------- solutions
q1 = [(5e-9, (0.0, 0.0))]
V10, V30 = potential_by_integration(q1, (0.1, 0.0)), potential_by_integration(q1, (0.3, 0.0))
v.check("04-04.1a", V10)
v.check("04-04.1b", V30)
v.check("04-04.1c", 1e-9 * (V10 - V30))
v.check("04-04.2a", 1000 * E_CH)
v.check("04-04.2b", -E_CH * 5)
v.check("04-04.2c", 5)
v.check("04-04.3a", -quad(lambda x: 500.0, 0, 0.04)[0])
v.check("04-04.3b", -quad(lambda y: 0.0, 0, 0.04)[0])
v.check("04-04.4a", disk_potential(1e-6, 0.01, 1e-3))
v.check("04-04.4b", disk_potential(1e-6, 0.01, 0.0))
v.check("04-04.4c", -deriv(lambda z: disk_potential(1e-6, 0.01, z), 1e-3, 1e-6))
dip = [(1e-6, (0.0, 0.5e-6)), (-1e-6, (0.0, -0.5e-6))]      # p = 1e-12 C m along z (the y-axis), nearly point-like


def dip_V(r, th):
    return sum(KE * q / hypot(r * sin(th) - x0, r * cos(th) - y0) for q, (x0, y0) in dip)


r5, th5 = 0.1, radians(60)
v.check("04-04.5a", dip_V(r5, th5))
Er = -deriv(lambda r: dip_V(r, th5), r5, 1e-5)
Et = -deriv(lambda th: dip_V(r5, th), th5, 1e-4) / r5
v.check("04-04.5b", Er)
v.check("04-04.5c", Et)
v.check("04-04.5d", hypot(Er, Et))
# two spheres: equal potentials from field-energy capacitances
Ca, Cb = (1e-18 / (2 * sphere_energy(1e-9, R)) for R in (0.01, 0.1))
Q1, Q2 = 22e-9 * Ca / (Ca + Cb), 22e-9 * Cb / (Ca + Cb)
v.check("04-04.6a", Q1 * 1e9)
v.check("04-04.6b", Q2 * 1e9)
v.check("04-04.6c", Q1 / Ca)
v.check("04-04.6d", KE * Q1 / 0.01**2)
v.check("04-04.6e", KE * Q2 / 0.1**2)
v.check("04-04.6f", Q1 / (4 * pi * 0.01**2))
v.check("04-04.6g", Q2 / (4 * pi * 0.1**2))
Cser = 1 / (1 / 2e-6 + 1 / 3e-6)
v.check("04-04.7a", (Cser + 4e-6) * 1e6)
v.check("04-04.7b", Cser * 10 * 1e6)
v.check("04-04.7c", Cser * 10 / 2e-6)
v.check("04-04.7d", Cser * 10 / 3e-6)
v.check("04-04.7e", 0.5 * (Cser + 4e-6) * 100 * 1e6)
A8 = 0.01
c8 = layered_C_per_area([(1e-3, 1.0), (1e-3, 4.0)]) * A8
D8b = c8 * 100 / A8
v.check("04-04.8a", c8 * 1e12)
v.check("04-04.8b", D8b / EPS0)
v.check("04-04.8c", D8b / (4 * EPS0))
v.check("04-04.8d", D8b / EPS0 * 1e-3)
v.check("04-04.8e", D8b / (4 * EPS0) * 1e-3)
v.check("04-04.8f", (layered_C_per_area([(2e-3, 1.0)]) + layered_C_per_area([(2e-3, 4.0)])) * A8 / 2 * 1e12)
Ccab = coax_C_per_m(0.45e-3, 1.475e-3, 2.25)
v.check("04-04.9a", Ccab * 1e12)
v.check("04-04.9b", Ccab * 1.5 * 1e12)
v.check("04-04.10a", 0.5 * EPS0 * 3e6**2)
Csph = 1e-18 / (2 * sphere_energy(1e-9, 0.1))
Q10 = Csph * 1e5
v.check("04-04.10b", sphere_energy(Q10, 0.1))
v.assert_true("1/2 C V^2 equals field energy", abs(sphere_energy(Q10, 0.1) / (0.5 * 4 * pi * EPS0 * 0.1 * 1e10) - 1) < 1e-9)
opt11 = minimize_scalar(lambda a: -3e6 * a * log(5e-3 / a), bounds=(1e-5, 4.99e-3), method="bounded", options={"xatol": 1e-13})
v.check("04-04.11a", opt11.x * 1e3)
v.check("04-04.11b", -opt11.fun / 1e3)
v.check("04-04.11c", 3e6 * 5e-4 * log(5e-3 / 5e-4) / 1e3)
dQ = quad(lambda t: 2.0, 0, 0.5e-6)[0]
for key, Cd in (("04-04.12a", 100e-6), ("04-04.12b", 90e-6), ("04-04.12c", 60e-6)):
    v.check(key, dQ / Cd * 1e3)
t_hk = minimize_scalar(lambda t: (3.9 * EPS0 / layered_C_per_area([(0.4e-9, 3.9), (t, 25)]) - 0.9e-9) ** 2,
                       bounds=(1e-10, 1e-8), method="bounded", options={"xatol": 1e-16}).x
v.check("04-04.13a", t_hk * 1e9)
v.check("04-04.13b", (t_hk + 0.4e-9) * 1e9)
v.check("04-04.13c", layered_C_per_area([(0.4e-9, 3.9), (t_hk, 25)]) * 100)
_, vbl14, _ = share(8e-15, 1.1, 80e-15, 0.55, 1e3, 1e-9)
v.check("04-04.14a", (vbl14 - 0.55) * 1e3)
from scipy.optimize import brentq  # noqa: E402
vmin = brentq(lambda vc: share(8e-15, vc, 80e-15, 0.55, 1e3, 1e-9)[1] - 0.55 - 0.040, 0.6, 1.1, xtol=1e-14)
v.check("04-04.14b", vmin)
v.check("04-04.14c", 1.1 - vmin)
v.check("04-04.14d", (1.1 - vmin) * 8e-15 * 1e15)
v.check("04-04.14e", (1.1 - vmin) * 8e-15 / E_CH)
for key, g in (("04-04.15a", 0.0), ("04-04.15b", 1e-6), ("04-04.15c", 10e-6)):
    v.check(key, chuck_force(S8, l8, er8, V8, g))
U16 = sphere_energy(1e-8, 0.05)
v.check("04-04.16a", U16)
v.check("04-04.16b", 1e-16 / (2 * U16) * 1e12)
v.check("04-04.16c", sphere_energy(1e-8, 0.05, 0.10) / U16)

# ---------------------------------------------------------------- lab
v.check("Lab 04-04.a", w_straight)
v.assert_true("lab work equals -(V_B - V_A)", abs(w_straight + (potential_by_integration(ch, B) - potential_by_integration(ch, A))) < 1e-3)
v.check("Lab 04-04.b", 1e-16 / (2 * sphere_energy(1e-8, 0.05)) * 1e12)
lam = 2e-9
U_c = quad(lambda r: 0.5 * EPS0 * (lam / (2 * pi * EPS0 * r)) ** 2 * 2 * pi * r, a5, b5)[0]
v.check("Lab 04-04.c", lam**2 / (2 * U_c) * 1e12)
v.check("Lab 04-04.d", 3.9 * EPS0 / layered_C_per_area([(0.4e-9, 3.9), (3e-9, 25)]) * 1e9)
v.check("Lab 04-04.e", chuck_force(S8, l8, er8, V8, 5e-6))

sys.exit(v.finish())
