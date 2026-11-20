#!/usr/bin/env python3
"""Verify every number in chapter 13-11 (radiation and antenna fundamentals), its solutions and lab.

Independent routes (not the chapter's closed forms):
- the Hertzian dipole's fields by numerically differentiating its retarded vector potential (finite-difference
  curls in spherical coordinates);
- radiated power, directivity and radiation resistance by numerical integration of the far-field power density
  over the sphere;
- the half-wave dipole by summing Hertzian elements along its sinusoidal current, then integrating;
- beamwidths and nulls by root finding on the computed patterns;
- array factors by direct summation of element phasors, directivity by integration over the sphere;
- link budgets by evaluating the Friis product directly.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import dblquad, quad
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-11-radiation-and-antennas.md",
         COURSE / "solutions" / "13-11-solutions.md"]
lab = COURSE / "labs" / "13-11-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-11", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 1 / math.sqrt(mu0 * e0)
eta0 = math.sqrt(mu0 / e0)
db = lambda x: 10 * math.log10(x)  # noqa: E731


# ---------------------------------------------------------------- Hertzian dipole by numerical curls
def hertz_fields(I0, ell, lam, r, th, h=1e-5):
    """E_theta and H_phi at (r, th) from A_z = mu I0 ell e^{-jkr}/(4 pi r) by finite-difference curls."""
    k = 2 * math.pi / lam
    w = k * c0
    Az = lambda rr: mu0 * I0 * ell * cmath.exp(-1j * k * rr) / (4 * math.pi * rr)  # noqa: E731
    def Hphi(rr, tt):
        Ar = lambda r_, t_: Az(r_) * math.cos(t_)  # noqa: E731
        At = lambda r_, t_: -Az(r_) * math.sin(t_)  # noqa: E731
        dr = h * min(rr, lam)  # step small against both r and the wavelength
        d_rAt = ((rr + dr) * At(rr + dr, tt) - (rr - dr) * At(rr - dr, tt)) / (2 * dr)
        d_Ar = (Ar(rr, tt + h) - Ar(rr, tt - h)) / (2 * h)
        return (d_rAt - d_Ar) / (mu0 * rr)
    dr = h * min(r, lam)
    d_rH = ((r + dr) * Hphi(r + dr, th) - (r - dr) * Hphi(r - dr, th)) / (2 * dr)
    Eth = -d_rH / r / (1j * w * e0)
    return Eth, Hphi(r, th)


def sphere_power(U):
    """Integrate a radiation intensity U(theta) (phi-symmetric) over the sphere."""
    return 2 * math.pi * quad(lambda t: U(t) * math.sin(t), 0, math.pi, limit=200)[0]


# theory
v.check("T 13-11.a", 1 / (2 * math.pi))
lam0 = 1.0
U_h = lambda t: (eta0 / 2) * (2 * math.pi / lam0 * 1.0 * 1.0 / (4 * math.pi)) ** 2 * math.sin(t) ** 2  # noqa
P_h = sphere_power(U_h)  # I0 = 1, ell = 1 lambda-units => R = 2P/(ell/lam)^2
v.check("T 13-11.b", 2 * P_h)

# Example 1
Rrad1 = 2 * sphere_power(lambda t: (eta0 / 2) * (2 * math.pi / 50 / (4 * math.pi)) ** 2 * math.sin(t) ** 2)
v.check("Ex 13-11.1a", Rrad1)
v.check("Ex 13-11.1b", Rrad1 / (Rrad1 + 1) * 100)
lam1 = 1.0
Eth, Hph = hertz_fields(1.0, lam1 / 50, lam1, 1000.0 * lam1 / lam1, math.pi / 2)
# the field at 1 km depends on l/lambda only through (l/lambda)/r; evaluate with lambda = 1 m and r = 1000 m
v.check("Ex 13-11.1c", abs(Eth) * 1e3)
v.assert_true("far field: E/H = eta", abs(abs(Eth / Hph) / eta0 - 1) < 1e-4)

# Example 2
Uh = lambda t: math.sin(t) ** 2  # noqa: E731
D_h = 4 * math.pi * 1.0 / sphere_power(Uh)
v.check("Ex 13-11.2a", D_h)
v.check("Ex 13-11.2b", db(D_h))
t_half = brentq(lambda t: Uh(t) - 0.5, 0.01, math.pi / 2)
v.check("Ex 13-11.2c", 2 * (90 - math.degrees(t_half)))


# Example 3: half-wave dipole by summing elements I(z) = cos(kz), |z| < lambda/4
def hw_field(t, lam=1.0):
    k = 2 * math.pi / lam
    re = quad(lambda z: math.cos(k * z) * math.cos(k * z * math.cos(t)), -lam / 4, lam / 4)[0]
    return (eta0 * k / (4 * math.pi)) * math.sin(t) * re  # |E| * r for I0 = 1


Uhw = lambda t: hw_field(t) ** 2 / (2 * eta0)  # noqa: E731
P_hw = sphere_power(Uhw)
D_hw = 4 * math.pi * Uhw(math.pi / 2) / P_hw
v.check("Ex 13-11.3a", 2 / D_hw)
v.check("Ex 13-11.3b", D_hw)
v.check("Ex 13-11.3c", db(D_hw))
v.check("Ex 13-11.3d", 2 * P_hw)
th_hp = brentq(lambda t: Uhw(t) / Uhw(math.pi / 2) - 0.5, 0.2, math.pi / 2)
v.check("Ex 13-11.3e", math.degrees(th_hp))
v.check("Ex 13-11.3f", 180 - 2 * math.degrees(th_hp))

# Example 4
lam24 = c0 / 2.4e9
fspl = -db((lam24 / (4 * math.pi * 100)) ** 2)
v.check("Ex 13-11.4a", fspl)
v.check("Ex 13-11.4b", 20 + 2 * db(D_hw) - fspl)
v.check("Ex 13-11.4c", D_hw * lam24**2 / (4 * math.pi) * 1e4)

# Example 5 (fixed apertures)
for f, key in ((2.4e9, "a"), (28e9, "b")):
    lam = c0 / f
    Gt = Gr = 4 * math.pi * 1e-3 / lam**2
    v.check(f"Ex 13-11.5{key}", db(Gt * Gr * (lam / (4 * math.pi * 100)) ** 2))
v.check("Ex 13-11.5c", db((28 / 2.4) ** 2))
v.check("Ex 13-11.5d", db(4 * math.pi * 1e-3 / (c0 / 28e9) ** 2))


# Example 6 (array by phasor summation)
def array_power(theta, N, d, beta):
    n = np.arange(N)
    return np.abs(np.exp(1j * n[None, :] * (2 * math.pi * d * np.sin(theta)[:, None] + beta)).sum(axis=1) / N) ** 2


def hpbw(N, d, th0):
    beta = -2 * math.pi * d * math.sin(math.radians(th0))
    f = lambda t: array_power(np.array([t]), N, d, beta)[0] - 0.5  # noqa: E731
    t0 = math.radians(th0)
    lo = brentq(f, t0 - 0.5, t0)
    hi = brentq(f, t0, t0 + 0.5)
    return math.degrees(hi - lo), math.degrees(beta)


v.check("Ex 13-11.6a", db(8))
bw0, _ = hpbw(8, 0.5, 0)
bw30, b30 = hpbw(8, 0.5, 30)
v.check("Ex 13-11.6b", bw0)
v.check("Ex 13-11.6c", b30)
v.check("Ex 13-11.6d", bw30)
v.check("Ex 13-11.6e", math.degrees(0.886 / (8 * 0.5)))
v.check("Ex 13-11.6f", math.degrees(0.886 / (8 * 0.5)) / math.cos(math.radians(30)))

# practitioner and simulation
v.check("Prac 13-11.a", c0 / 28e9 / 2 * 1e3)
v.check("Prac 13-11.b", 8 * c0 / 28e9 / 2 * 100)
v.check("Prac 13-11.c", 5 + db(160))
# matched small antenna: the L-network delivers the available power to R_rad + R_loss (solve it)
Rt = Rrad1 + 1.0
w = 2 * math.pi * 1e8
L = brentq(lambda L: (1 / (Rt + 1j * w * L)).real - 1 / 50, 1e-12, 1e-6, xtol=1e-20)
C = -(1 / (Rt + 1j * w * L)).imag / w
Zin = 1 / (1 / (Rt + 1j * w * L) + 1j * w * C)
Iin = 1.0 / (50 + Zin)
Vport = Iin * Zin
Iant = Vport / (Rt + 1j * w * L)
v.check("Sim 13-11.a", 0.5 * abs(Iant) ** 2 * Rrad1 / (1 / 400) * 100)

# ---------------------------------------------------------------- Problems
for f, keys in ((900e6, "ab"), (2.4e9, "cd"), (28e9, "ef")):
    lam = c0 / f
    v.check(f"13-11.1{keys[0]}", lam * 100)
    v.check(f"13-11.1{keys[1]}", lam / 2 * 100)
lam2 = c0 / 1e8
v.check("13-11.2a", 2 * sphere_power(lambda t: (eta0 / 2) * (2 * math.pi * 0.01 / lam2 / (4 * math.pi)) ** 2
                                     * math.sin(t) ** 2) * 1e3)
v.check("13-11.3a", db(100))
v.check("13-11.3b", 20 + 15)
v.check("13-11.3c", 10 ** 3.5 / 1e3)
lam12 = c0 / 12e9
v.check("13-11.4a", 2 * 1.0**2 / lam12)
Ae5 = 1e4 * lam12**2 / (4 * math.pi)
v.check("13-11.5a", Ae5)
v.check("13-11.5b", Ae5 / (math.pi * 0.25) * 100)
lam58 = c0 / 5.8e9
fs6 = -db((lam58 / (4 * math.pi * 1000)) ** 2)
v.check("13-11.6a", fs6)
v.check("13-11.6b", 30 + 40 - fs6)
R7 = brentq(lambda R: 20 + 4 - (-db((lam24 / (4 * math.pi * R)) ** 2)) + 90, 10, 1e6)
v.check("13-11.7a", R7 / 1e3)
e8 = (2 * P_hw) / (2 * P_hw + 2)
v.check("13-11.8a", e8 * 100)
v.check("13-11.8b", db(e8 * D_hw))
v.check("13-11.9a", math.sqrt(2 * eta0 * D_h * 1.0 / (4 * math.pi * 1000**2)) * 1e3)
# 10: compare the 1/r^3 and 1/r parts of the exact (numerical-curl) field: ratio |near|/|far| = 1/(kr)^2
for rr, key in ((1.0, "a"), (0.1, "b")):
    v.check(f"13-11.10{key}", 1 / (2 * math.pi * rr) ** 2)
Eex, _ = hertz_fields(1.0, 1e-3, 1.0, 1.0, math.pi / 2)
far = eta0 * 2 * math.pi * 1e-3 / (4 * math.pi * 1.0)
v.assert_true("numerical field at r = lambda includes the near terms", abs(abs(Eex) / far - abs(1 + 1 / (2j * math.pi)
                                                                                         - 1 / (2 * math.pi) ** 2)) < 1e-3)
t = np.linspace(-math.pi / 2, math.pi / 2, 200001)
p4 = array_power(t, 4, 0.5, 0.0)
nulls = t[1:-1][(p4[1:-1] < p4[:-2]) & (p4[1:-1] < p4[2:]) & (p4[1:-1] < 1e-6)]
v.check("13-11.11a", math.degrees(nulls[nulls > 0].min()))
# directivity of a 4-element line array (axis along z, elements isotropic): integrate over the sphere
AFz = lambda th: abs(sum(cmath.exp(1j * n * math.pi * math.cos(th)) for n in range(4)) / 4) ** 2  # noqa: E731
v.check("13-11.11b", 4 * math.pi * 1.0 / sphere_power(AFz))
s_g = math.sin(math.radians(40)) - 1 / 0.8
v.check("13-11.12a", math.degrees(math.asin(s_g)))
pg = array_power(np.array([math.asin(s_g)]), 16, 0.8, -2 * math.pi * 0.8 * math.sin(math.radians(40)))[0]
v.assert_true("grating lobe is as strong as the main beam", abs(pg - 1) < 1e-9)
v.check("13-11.12b", brentq(lambda d: d * (1 + math.sin(math.radians(60))) - 1, 0.1, 1))
for B, key in ((20, "a"), (80, "b"), (160, "c"), (320, "d")):
    v.check(f"13-11.13{key}", min(30.0, 5 + db(B)))
v.check("13-11.14a", db(64))
v.check("13-11.14b", db(64 * 10))
v.check("13-11.14c", db(64 * 10) + db(64) + 5)

# ---------------------------------------------------------------- Lab
if lab.exists():
    # directivity of a full-wave dipole by element summation, and the 16-element broadside beamwidth
    def fw_field(t, lam=1.0):
        k = 2 * math.pi / lam
        re = quad(lambda z: math.sin(k * (lam / 2 - abs(z))) * math.cos(k * z * math.cos(t)), -lam / 2, lam / 2,
                  limit=200)[0]
        return math.sin(t) * re
    Ufw = lambda t: fw_field(t) ** 2  # noqa: E731
    v.check("Lab 13-11.a", 4 * math.pi * Ufw(math.pi / 2) / sphere_power(Ufw))
    v.check("Lab 13-11.b", hpbw(16, 0.5, 0)[0])

sys.exit(v.finish())
