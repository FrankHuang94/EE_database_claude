#!/usr/bin/env python3
"""Verify every number published in chapter 04-02, its solutions and its lab handout.

Fields of continuous distributions are recomputed by numerical integration (not the closed forms);
point-charge systems by vector superposition; charged-particle motion by integrating Newton's law;
ESD pulses from the RC discharge.
"""
from __future__ import annotations

import math
import sys
from math import exp, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C = HERE.parent
v = Verifier.from_files("04-02", C / "chapters" / "04-02-charge-coulomb-and-electric-fields.md",
                        C / "solutions" / "04-02-solutions.md", C / "labs" / "04-02-lab" / "README.md")
E_CH = 1.602176634e-19
EPS0 = 8.8541878188e-12
KE = 1 / (4 * pi * EPS0)
ME, MP, GN = 9.1093837139e-31, 1.67262192595e-27, 6.67430e-11
KB = 1.380649e-23
CL = 299792458.0


def superpose(charges, point):
    E = np.zeros(2)
    for q, pos in charges:
        d = np.asarray(point, float) - np.asarray(pos, float)
        E += KE * q * d / np.linalg.norm(d) ** 3
    return E


def line_field(lam, L, y):            # bisector field of a finite line by numerical integration
    return quad(lambda x: KE * lam * y / (x * x + y * y) ** 1.5, -L / 2, L / 2, epsabs=0, epsrel=1e-12)[0]


def disk_field(sigma, R, z):          # axial field of a disk by integrating over its area
    # sum of rings: each ring of radius r and width dr carries sigma 2 pi r dr (the angular integral is exact)
    return quad(lambda r: KE * sigma * 2 * pi * r * z / (r * r + z * z) ** 1.5, 0, R, epsabs=0, epsrel=1e-12, limit=200,
                points=[z] if z < R else None)[0]


def ring_field(Q, R, z):
    return quad(lambda phi: KE * (Q / (2 * pi)) * z / (z * z + R * R) ** 1.5, 0, 2 * pi)[0]


def dipole_axis(q, d, r):
    return KE * q * (1 / (r - d / 2) ** 2 - 1 / (r + d / 2) ** 2)


def beta_rel(V):                       # exact relativistic speed of an electron after V volts
    kap = E_CH * V / (ME * CL**2)
    return sqrt(1 - 1 / (1 + kap) ** 2)


# ---------------------------------------------------------------- theory keys
v.check("T 04-02.a", KE)
v.check("T 04-02.b", minimize_scalar(lambda z: -ring_field(1.0, 1.0, z), bounds=(0.01, 3), method="bounded", options={"xatol": 1e-10}).x)
v.check("T 04-02.c", 3)                                   # textbook value, stated as approximate
v.check("T 04-02.d", sqrt(2 * E_CH * 100 / ME))
v.check("T 04-02.e", (sqrt(2 * E_CH * 100 / ME) / CL - beta_rel(100)) / (sqrt(2 * E_CH * 100 / ME) / CL) * 100)
# sheet and parallel plates as the large-R limit of the integrated disk
v.assert_true("disk -> sheet as R grows", abs(disk_field(1e-6, 1e3, 1e-3) / (1e-6 / (2 * EPS0)) - 1) < 1e-5)

# ---------------------------------------------------------------- examples
v.check("Ex 04-02.1a", 1 / E_CH)
v.check("Ex 04-02.1b", 1e-12 / E_CH)
v.check("Ex 04-02.1c", 4.5 * 3600)
Fe = KE * E_CH**2 / 1e-20
Fg = GN * ME * MP / 1e-20
v.check("Ex 04-02.2a", Fe)
v.check("Ex 04-02.2b", Fg)
v.check("Ex 04-02.2c", Fe / Fg)
v.check("Ex 04-02.2d", KE * 1e-12 / 1e-4)
ch3 = [(2e-9, (0, 0)), (-2e-9, (0.04, 0))]
F3 = 1e-9 * superpose(ch3, (0.02, 0.03))
v.check("Ex 04-02.3a", sqrt(0.02**2 + 0.03**2) * 100)
v.check("Ex 04-02.3b", np.linalg.norm(1e-9 * superpose([ch3[0]], (0.02, 0.03))) * 1e6)
v.check("Ex 04-02.3c", np.linalg.norm(F3) * 1e6)
v.assert_true("net force along +x", F3[0] > 0 and abs(F3[1]) < 1e-18)
v.check("Ex 04-02.4a", line_field(10e-9, 2e-3, 1e-3))
v.check("Ex 04-02.4b", 10e-9 / (2 * pi * EPS0 * 1e-3))
v.check("Ex 04-02.4c", line_field(10e-9, 2e-3, 1.0))
v.check("Ex 04-02.4d", KE * 20e-12 / 1.0)
v.check("Ex 04-02.5a", 1e-6 / (2 * EPS0))
v.check("Ex 04-02.5b", 1e-6 / EPS0)
Ed = disk_field(1e-6, 0.01, 1e-3)
v.check("Ex 04-02.5c", Ed)
v.check("Ex 04-02.5d", Ed / (1e-6 / (2 * EPS0)))
Eex6, Eap6 = dipole_axis(1e-9, 1e-3, 0.1), 2 * KE * 1e-12 / 0.1**3
v.check("Ex 04-02.6a", 1e-9 * 1e-3)
v.check("Ex 04-02.6b", Eex6)
v.check("Ex 04-02.6c", Eap6)
v.check("Ex 04-02.6d", (Eex6 - Eap6) / Eex6)
# torque by summing the forces on the two charges in a uniform field at 90 degrees
# torque = sum of x*F_y - y*F_x over the two charges, dipole along x, field along y
tau = sum(x * fy - y * fx for (x, y), (fx, fy) in (((0.0005, 0.0), (0.0, 1e-9 * 1e5)), ((-0.0005, 0.0), (0.0, -1e-9 * 1e5))))
v.check("Ex 04-02.6e", tau)
v.check("Ex 04-02.6f", 2 * 1e-12 * 1e5)
E7 = 100 / 0.01
a7 = E_CH * E7 / ME
hit = lambda t, s: s[0] - 0.01  # noqa: E731
hit.terminal = True
sol7 = solve_ivp(lambda t, s: [s[1], a7], (0, 1e-8), [0, 0], events=hit, rtol=1e-12, atol=1e-18)
t7, v7 = sol7.t_events[0][0], sol7.y_events[0][0][1]
v.check("Ex 04-02.7a", E7)
v.check("Ex 04-02.7b", a7)
v.check("Ex 04-02.7c", t7 * 1e9)
v.check("Ex 04-02.7d", v7)
v.check("Ex 04-02.7e", 0.5 * ME * v7**2)
v.check("Ex 04-02.7f", v7 / CL)
# HBM: integrate the RC discharge
Ch, Rh = 100e-12, 1500.0
sol8 = solve_ivp(lambda t, q: [-q[0] / (Rh * Ch)], (0, 1e-6), [Ch * 2000], dense_output=True, rtol=1e-12, atol=1e-20)
v.check("Ex 04-02.8a", Ch * 2000 * 1e9)
v.check("Ex 04-02.8b", 0.5 * Ch * 2000**2 * 1e3)
v.check("Ex 04-02.8c", 2000 / Rh)
v.check("Ex 04-02.8d", Rh * Ch * 1e9)
v.check("Ex 04-02.8e", sol8.sol(300e-9)[0] / Ch / Rh)
v.check("Ex 04-02.8f", KE * 2e-7 / 1e-4)

# ================================================================ solutions
v.check("04-02.1a", 1e-6 / E_CH)
v.check("04-02.1b", 1e-3 / E_CH)
v.check("04-02.1c", E_CH / MP)
v.check("04-02.1d", E_CH / ME)
v.check("04-02.2a", KE * 25e-18 / 4e-4)
v.check("04-02.2b", brentq(lambda r: KE * 25e-18 / r**2 - 1e-6, 0.01, 10))
E3 = np.linalg.norm(superpose([(4e-9, (0, 0))], (0.03, 0)))
v.check("04-02.3a", E3)
v.check("04-02.3b", E_CH * E3)
v.check("04-02.3c", E_CH * E3 / ME)
null = brentq(lambda x: superpose([(2e-9, (0, 0)), (-8e-9, (0.06, 0))], (x, 0))[0], -0.5, -0.001)
v.check("04-02.4a", null * 100)
sq = [(1e-9, (0, 0)), (1e-9, (0.02, 0)), (1e-9, (0, 0.02)), (1e-9, (0.02, 0.02))]
v.check("04-02.5a", np.linalg.norm(superpose(sq, (0.01, 0.01))))
v.check("04-02.5b", np.linalg.norm(1e-9 * superpose(sq[1:], (0, 0))))
v.check("04-02.6a", ring_field(1e-8, 0.05, 0.05))
r6 = minimize_scalar(lambda z: -ring_field(1e-8, 0.05, z), bounds=(0.001, 0.2), method="bounded", options={"xatol": 1e-11})
v.check("04-02.6b", r6.x * 100)
v.check("04-02.6c", ring_field(1e-8, 0.05, r6.x))
v.check("04-02.7a", 50e-9 / (2 * EPS0))
Req = 0.1 / sqrt(pi)
v.check("04-02.7b", Req * 100)
v.check("04-02.7c", disk_field(50e-9, Req, 1e-3))
v.check("04-02.7d", brentq(lambda z: disk_field(50e-9, Req, z) / (50e-9 / (2 * EPS0)) - 0.9, 1e-4, 0.05) * 1e3)
v.check("04-02.8a", EPS0 * 1e6)
v.check("04-02.8b", EPS0 * 1e6 * 1e-4 * 1e9)
v.check("04-02.9a", 3e-30 * 1e7)
v.check("04-02.9b", 2 * 3e-30 * 1e7)
v.check("04-02.9c", KB * 300)
v.check("04-02.9d", 3e-30 * 1e7 / (KB * 300))
ax_ex, ax_ap = dipole_axis(1e-9, 1e-3, 5e-3), 2 * KE * 1e-12 / 5e-3**3
br_ex = np.linalg.norm(superpose([(1e-9, (0.0005, 0)), (-1e-9, (-0.0005, 0))], (0, 5e-3)))
br_ap = KE * 1e-12 / 5e-3**3
v.check("04-02.10a", ax_ex)
v.check("04-02.10b", ax_ap)
v.check("04-02.10c", (ax_ex - ax_ap) / ax_ex * 100)
v.check("04-02.10d", br_ex)
v.check("04-02.10e", br_ap)
v.check("04-02.10f", (br_ap - br_ex) / br_ex * 100)
v11 = sqrt(2 * E_CH * 2000 / ME)
a11 = E_CH * (50 / 0.005) / ME
sol11 = solve_ivp(lambda t, s: [s[2], s[3], 0, a11], (0, 0.02 / v11), [0, 0, v11, 0], rtol=1e-12, atol=1e-18)
v.check("04-02.11a", v11)
v.check("04-02.11b", v11 / CL)
v.check("04-02.11c", 0.02 / v11 * 1e9)
v.check("04-02.11d", sol11.y[1, -1] * 1e3)
v.check("04-02.11e", sol11.y[3, -1] / v11)
v.check("04-02.11f", (v11 / CL - beta_rel(2000)) / (v11 / CL) * 100)
v.check("04-02.12a", E_CH * 1e4)
v.check("04-02.12b", sqrt(2 * E_CH * 1e4 / (11 * 1.6605e-27)))
for key, y in (("a", 1e-3), ("c", 0.05), ("e", 1.0)):
    v.check(f"04-02.13{key}", line_field(2e-9, 0.1, y))
v.check("04-02.13b", 2e-9 / (2 * pi * EPS0 * 1e-3))
v.check("04-02.13d", 2e-9 / (2 * pi * EPS0 * 0.05))
v.assert_true("both approximations equal at y = L/2", abs(KE * 2e-9 * 0.1 / 0.05**2 - 2e-9 / (2 * pi * EPS0 * 0.05)) < 1e-9)
v.check("04-02.13f", KE * 2e-9 * 0.1 / 1.0)
v.check("04-02.13g", 2e-9 / (2 * pi * EPS0 * 1.0))
v.check("04-02.13h", KE * 2e-9 * 0.1 / 1e-6)
v.check("04-02.13i", brentq(lambda y: (2e-9 / (2 * pi * EPS0 * y)) / line_field(2e-9, 0.1, y) - 1.1, 1e-3, 0.5) * 100)
v.check("04-02.14a", brentq(lambda z: disk_field(1e-6, 1.0, z) / (1e-6 / (2 * EPS0)) - 0.99, 1e-4, 0.5))
Eox = 1.0 / 1.2e-9
v.check("04-02.15a", Eox / 1e8)
v.check("04-02.15b", 10e8 * 1.2e-9)
v.check("04-02.15c", 3.9 * EPS0 * Eox)
v.check("04-02.15d", 3.9 * EPS0 * Eox / E_CH / 1e18)
v.check("04-02.15e", 1 / (3.9 * EPS0 * Eox / E_CH / 1e18))
for (kq, kE, kI, kT), (Cc, Rr) in ((("a", "c", "e", "g"), (100e-12, 1500.0)), (("b", "d", "f", "h"), (150e-12, 330.0))):
    v.check(f"04-02.16{kq}", Cc * 8000 * 1e6)
    v.check(f"04-02.16{kE}", 0.5 * Cc * 8000**2 * 1e3)
    v.check(f"04-02.16{kI}", 8000 / Rr)
    v.check(f"04-02.16{kT}", Rr * Cc * 1e9)

# ================================================================ lab handout
lam, L, y0 = 10e-9, 2e-3, 1e-3
ex = line_field(lam, L, y0)
for key, N in (("a", 2), ("b", 10), ("c", 20)):
    xs = -L / 2 + (np.arange(N) + 0.5) * L / N
    Ey = sum(KE * lam * (L / N) * y0 / (xx**2 + y0**2) ** 1.5 for xx in xs)
    v.check(f"Lab 04-02.{key}", (Ey / ex - 1) * 100)
v.check("Lab 04-02.d", dipole_axis(1e-9, 1e-3, 0.1) / (2 * KE * 1e-12 / 0.1**3))
v.check("Lab 04-02.f", dipole_axis(1e-9, 1e-3, 3e-3) / (2 * KE * 1e-12 / 3e-3**3))
rr = np.logspace(np.log10(0.05), 0, 100)
v.check("Lab 04-02.e", np.polyfit(np.log(rr), np.log(dipole_axis(1e-9, 1e-3, rr)), 1)[0])

sys.exit(v.finish())
