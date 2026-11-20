#!/usr/bin/env python3
"""Verify every number in chapter 13-06 (reflection and transmission of waves), its solutions and lab.

Independent routes (not the chapter's closed forms):
- each interface by solving the tangential-field continuity equations as a 2 x 2 linear system;
- layered structures (coatings, radomes, shields, the Salisbury screen) by the characteristic (ABCD) matrix
  method with complex wavenumbers and impedances, including lossy metal;
- Snell's law by phase matching (root finding on k1 sin(theta_i) = k2 sin(theta_t));
- standing-wave extrema by sampling the total field;
- the evanescent decay constant from the complex normal wavenumber.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-06-reflection-and-transmission.md",
         COURSE / "solutions" / "13-06-solutions.md"]
lab = COURSE / "labs" / "13-06-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-06", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 1 / math.sqrt(mu0 * e0)
eta0 = math.sqrt(mu0 / e0)


# ---------------------------------------------------------------- helpers
def interface(Z1, Z2):
    """Solve 1 + G = t and (1 - G)/Z1 = t/Z2 for (G, t), with Z the tangential E/H impedances."""
    A = np.array([[1, -1], [-1 / Z1, -1 / Z2]], dtype=complex)
    b = np.array([-1, -1 / Z1], dtype=complex)
    G, t = np.linalg.solve(A, b)
    return G, t


def snell(n1, n2, th_i):
    """Transmission angle by phase matching along the boundary (root finding)."""
    return brentq(lambda th: n2 * math.sin(th) - n1 * math.sin(th_i), 0, math.pi / 2, xtol=1e-15)


def te_tm_impedances(eta, th):
    return eta / math.cos(th), eta * math.cos(th)


def stack_reflection(f, layers, eta_in=None, eta_out=None):
    """Reflection from a stack of (eta, k, d) layers between eta_in and eta_out at normal incidence (ABCD)."""
    eta_in = eta0 if eta_in is None else eta_in
    eta_out = eta0 if eta_out is None else eta_out
    M = np.eye(2, dtype=complex)
    for eta, k, d in layers:
        b = k * d
        M = M @ np.array([[cmath.cos(b), 1j * eta * cmath.sin(b)], [1j * cmath.sin(b) / eta, cmath.cos(b)]])
    A, B, C, D = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
    Zin = (A * eta_out + B) / (C * eta_out + D)
    G = (Zin - eta_in) / (Zin + eta_in)
    # transmitted field ratio (incident wave of unit amplitude): E_out = 2 eta_out / (A eta_out + B + eta_in (C eta_out + D))
    t = 2 * eta_out / (A * eta_out + B + eta_in * (C * eta_out + D))
    return G, t


def dielectric(er, f, d):
    n = math.sqrt(er)
    return (eta0 / n, 2 * math.pi * f * n / c0, d)


def metal(sigma, f, d):
    w = 2 * math.pi * f
    k = cmath.sqrt(-1j * w * mu0 * sigma)  # e^{-jkz} with Im(k) < 0 decays
    if k.imag > 0:
        k = -k
    eta = cmath.sqrt(1j * w * mu0 / sigma)
    return (eta, k, d)


def standing_extrema(G, lam, span=None, n=200001):
    z = np.linspace(0, span or lam, n)  # distance in front of the boundary
    k = 2 * math.pi / lam
    E = np.abs(np.exp(1j * k * z) + G * np.exp(-1j * k * z))
    return z, E


# ---------------------------------------------------------------- Example 1
eta_g = eta0 / math.sqrt(2.25)
G1, t1 = interface(eta0, eta_g)
v.check("Ex 13-06.1a", eta_g)
v.check("Ex 13-06.1b", G1.real)
v.check("Ex 13-06.1c", t1.real)
v.check("Ex 13-06.1d", abs(G1) ** 2 * 100)
v.check("Ex 13-06.1e", (eta0 / eta_g) * abs(t1) ** 2 * 100)
z, E = standing_extrema(G1, 1.0)
v.check("Ex 13-06.1f", E.max() / E.min())

# ---------------------------------------------------------------- Example 2 (PEC: eta2 = 0)
lam2 = c0 / 2.4e9
G2, _ = interface(eta0, 1e-30)
z, E = standing_extrema(G2, lam2, span=2 * lam2)
zeros = z[1:-1][(E[1:-1] < E[:-2]) & (E[1:-1] < E[2:])]
maxima = z[1:-1][(E[1:-1] > E[:-2]) & (E[1:-1] > E[2:])]
v.check("Ex 13-06.2a", zeros[0] * 100)
v.check("Ex 13-06.2b", E.max())
v.check("Ex 13-06.2c", maxima[0] * 100)
v.check("Ex 13-06.2d", maxima[1] * 100)
v.check("Ex 13-06.2e", abs(1 - G2) / eta0 * 1e3)  # H at the wall = (E_i - E_r)/eta

# ---------------------------------------------------------------- Example 3 (optics: index form, quarter-wave layer)
f_opt = c0 / 550e-9
v.check("Ex 13-06.3a", brentq(lambda n: n * n - 1.5, 1, 1.5))
d_mgf2 = 550e-9 / (4 * 1.38)
v.check("Ex 13-06.3b", d_mgf2 * 1e9)
G3, _ = stack_reflection(f_opt, [dielectric(1.38**2, f_opt, d_mgf2)], eta_out=eta0 / 1.5)
v.check("Ex 13-06.3c", abs(G3) ** 2 * 100)
v.check("Ex 13-06.3d", abs(interface(eta0, eta0 / 1.5)[0]) ** 2 * 100)

# ---------------------------------------------------------------- Example 4
th_c = brentq(lambda th: 1.5 * math.sin(th) - 1, 0, math.pi / 2, xtol=1e-15)
v.check("Ex 13-06.4a", math.degrees(th_c))
th_cf = brentq(lambda th: 1.468 * math.sin(th) - 1.463, 0, math.pi / 2, xtol=1e-15)
v.check("Ex 13-06.4b", math.degrees(th_cf))
# acceptance: largest external angle whose refracted ray meets the side wall at the critical angle
inner = math.pi / 2 - th_cf
acc = brentq(lambda a: math.sin(a) - 1.468 * math.sin(inner), 0, math.pi / 2, xtol=1e-15)
v.check("Ex 13-06.4c", math.sin(acc))
v.check("Ex 13-06.4d", math.degrees(acc))
v.check("Ex 13-06.4e", math.degrees(inner))

# ---------------------------------------------------------------- Example 5
ti = math.radians(45)
tt = snell(1.0, 1.5, ti)
v.check("Ex 13-06.5a", math.degrees(tt))
Zte1, Ztm1 = te_tm_impedances(eta0, ti)
Zte2, Ztm2 = te_tm_impedances(eta0 / 1.5, tt)
Gte, _ = interface(Zte1, Zte2)
Gtm_tan, _ = interface(Ztm1, Ztm2)   # reflection of tangential E for TM, which is Ulaby's Gamma_parallel
Gtm = Gtm_tan.real
v.check("Ex 13-06.5b", Gte.real)
v.check("Ex 13-06.5c", Gtm)
v.check("Ex 13-06.5d", abs(Gte) ** 2 * 100)
v.check("Ex 13-06.5e", Gtm**2 * 100)
v.assert_true("Gamma_par = -Gamma_perp^2 at 45 deg", abs(Gtm + Gte.real**2) < 1e-12)
thB = minimize_scalar(lambda th: abs(interface(*[te_tm_impedances(eta0, th)[1],
                                                  te_tm_impedances(eta0 / 1.5, snell(1, 1.5, th))[1]])[0]),
                      bounds=(0.5, 1.4), method="bounded", options={"xatol": 1e-12}).x
v.check("Ex 13-06.5f", math.degrees(thB))

# ---------------------------------------------------------------- Example 6 (exact slab vs A + R)
f6 = 1e9
cu = metal(5.8e7, f6, 35e-6)
delta6 = -1 / cu[1].imag
G6, t6 = stack_reflection(f6, [cu])
SE_exact = -20 * math.log10(abs(t6))
A6 = 20 * math.log10(math.e) * 35e-6 / delta6
R6 = 20 * math.log10(eta0 / (4 * abs(cu[0])))
v.check("Ex 13-06.6a", 35e-6 / delta6)
v.check("Ex 13-06.6b", A6)
v.check("Ex 13-06.6c", abs(cu[0]) * 1e3)
v.check("Ex 13-06.6d", R6)
v.check("Ex 13-06.6e", A6 + R6)
v.assert_true("A + R within 0.1 dB of the exact slab", abs(SE_exact - (A6 + R6)) < 0.1, f"{SE_exact} vs {A6 + R6}")

# ---------------------------------------------------------------- practitioner and simulation
# Problem 13-05.13's coax (a = 0.5 mm, b = 1.75 mm, polyethylene eps_r 2.25, tan d 0.0002, copper) at 1 GHz:
# total attenuation from the exact propagation constant of its RLGC model, over the fibre's 0.30 dB/km
w_c = 2 * math.pi * 1e9
Rs_c = math.sqrt(w_c * mu0 / (2 * 5.8e7))
Rp_c = Rs_c / (2 * math.pi) * (1 / 0.5e-3 + 1 / 1.75e-3)
Lp_c = mu0 / (2 * math.pi) * math.log(3.5)
Cp_c = 2 * math.pi * 2.25 * e0 / math.log(3.5)
g_c = cmath.sqrt((Rp_c + 1j * w_c * Lp_c) * (w_c * Cp_c * 0.0002 + 1j * w_c * Cp_c))
v.check("Prac 13-06.a", 20 * math.log10(math.e) * g_c.real / 0.30e-3)
Gs, ts = interface(376.7, 251.13)
v.check("Sim 13-06.a", ts.real)
v.check("Sim 13-06.b", Gs.real)

# ---------------------------------------------------------------- Problems
G, t = interface(eta0, eta0 / 2)
v.check("13-06.1a", G.real)
v.check("13-06.1b", t.real)
v.check("13-06.1c", abs(G) ** 2 * 100)
v.check("13-06.1d", 2 * abs(t) ** 2 * 100)
z, E = standing_extrema(G, 1.0)
v.check("13-06.1e", E.max() / E.min())
G, _ = interface(eta0, eta0 / 9)
v.check("13-06.2a", G.real)
v.check("13-06.2b", abs(G) ** 2 * 100)
z, E = standing_extrema(G, 1.0)
v.check("13-06.2c", E.max() / E.min())
lam3 = c0 / 1e10
z, E = standing_extrema(interface(eta0, 1e-30)[0], lam3, span=2 * lam3)
zeros = z[1:-1][(E[1:-1] < E[:-2]) & (E[1:-1] < E[2:])]
maxima = z[1:-1][(E[1:-1] > E[:-2]) & (E[1:-1] > E[2:])]
v.check("13-06.3a", zeros[0] * 100)
v.check("13-06.3b", maxima[0] * 100)
v.check("13-06.4a", math.degrees(brentq(lambda th: 1.33 * math.sin(th) - 1, 0, math.pi / 2, xtol=1e-15)))
v.check("13-06.4b", math.degrees(snell(1.33, 1.0, math.radians(30))))
thB5 = brentq(lambda th: math.tan(th) - 1.5, 0.1, 1.5, xtol=1e-15)
tt5 = snell(1.0, 1.5, thB5)
G5, _ = interface(eta0 / math.cos(thB5), (eta0 / 1.5) / math.cos(tt5))
v.check("13-06.5a", math.degrees(tt5))
v.check("13-06.5b", G5.real)
v.check("13-06.5c", abs(G5) ** 2 * 100)
er6 = brentq(lambda er: (eta0 / math.sqrt(er)) ** 2 - eta0 * (eta0 / 3), 1.01, 8.99, xtol=1e-14)  # eta2^2 = eta1 eta3
v.check("13-06.6a", er6)
d6 = c0 / (4 * 1e10 * math.sqrt(er6))
v.check("13-06.6b", d6 * 1e3)
v.assert_true("quarter-wave layer cancels reflection",
              abs(stack_reflection(1e10, [dielectric(er6, 1e10, d6)], eta_out=eta0 / 3)[0]) < 1e-12)
d7 = c0 / (2 * 1e10 * 2)
v.check("13-06.7a", d7 * 1e3)
v.assert_true("half-wave radome transparent at 10 GHz", abs(stack_reflection(1e10, [dielectric(4, 1e10, d7)])[0]) < 1e-12)
v.check("13-06.7b", abs(stack_reflection(1.1e10, [dielectric(4, 1.1e10, d7)])[0]) ** 2 * 100)
v.check("13-06.7c", abs(stack_reflection(1.2e10, [dielectric(4, 1.2e10, d7)])[0]) ** 2 * 100)
th8 = brentq(lambda th: 1.47 * math.sin(th) - 1.46, 0, math.pi / 2, xtol=1e-15)
acc8 = brentq(lambda a: math.sin(a) - 1.47 * math.cos(th8), 0, math.pi / 2, xtol=1e-15)
v.check("13-06.8a", math.sin(acc8))
v.check("13-06.8b", math.degrees(acc8))
v.check("13-06.8c", math.degrees(th8))
w9 = 2 * math.pi * 1e4
eta9 = cmath.sqrt(1j * w9 * mu0 / (4 + 1j * w9 * 81 * e0))
G9, t9 = interface(eta0, eta9)
v.check("13-06.9a", eta9.real)
v.check("13-06.9b", eta9.imag)
v.check("13-06.9c", G9.real)
P_trans = (abs(t9) ** 2 * (1 / eta9).real) / (1 / eta0)  # Re{E H*} ratio
v.check("13-06.9d", P_trans * 100)
v.assert_true("energy balance at the sea surface", abs(P_trans + abs(G9) ** 2 - 1) < 1e-12)
v.check("13-06.9e", 4 * eta9.real / eta0 * 100)
al = metal(3.5e7, 1e6, 0.5e-3)
delta10 = -1 / al[1].imag
A10 = 20 * math.log10(math.e) * 0.5e-3 / delta10
R10 = 20 * math.log10(eta0 / (4 * abs(al[0])))
v.check("13-06.10a", A10)
v.check("13-06.10b", R10)
v.check("13-06.10c", A10 + R10)
v.assert_true("aluminium A + R within 0.1 dB of exact", abs(-20 * math.log10(abs(stack_reflection(1e6, [al])[1]))
                                                            - (A10 + R10)) < 0.1)
# 11: Salisbury screen as an ABCD stack: resistive sheet (shunt admittance 1/377) then air gap to a short
for r, keys in ((1.0, None), (1.2, ("a", "b", "c"))):
    beta_d = math.pi / 2 * r
    Zshort = 1j * eta0 * math.tan(beta_d)  # air section terminated in a short, seen from the sheet
    Y = 1 / eta0 + (1 / Zshort if abs(Zshort) > 0 else 0)
    G11 = (1 / Y - eta0) / (1 / Y + eta0)
    if keys is None:
        v.assert_true("Salisbury screen matched at f0", abs(G11) < 1e-12)
    else:
        v.check(f"13-06.11{keys[0]}", abs(G11))
        v.check(f"13-06.11{keys[1]}", 20 * math.log10(abs(G11)))
        v.check(f"13-06.11{keys[2]}", abs(G11) ** 2 * 100)
k0 = 2 * math.pi / 1550e-9
kx = k0 * 1.5 * math.sin(math.radians(60))
kz2 = cmath.sqrt(k0**2 - kx**2)  # imaginary beyond the critical angle
v.assert_true("beyond critical: kz purely imaginary", abs(kz2.real) < 1e-6 * abs(kz2))
v.check("13-06.12a", abs(kz2.imag) * 1e-6)
v.check("13-06.12b", 1 / abs(kz2.imag) * 1e9)
tt13 = snell(1.0, 1.5, math.radians(45))
G13, t13 = interface(eta0 / math.cos(math.radians(45)), (eta0 / 1.5) / math.cos(tt13))
T13 = (eta0 * math.cos(tt13)) / ((eta0 / 1.5) * math.cos(math.radians(45))) * abs(t13) ** 2
v.check("13-06.13a", t13.real)
v.check("13-06.13b", T13)
v.check("13-06.13c", T13 + abs(G13) ** 2)
lam14 = c0 / 1e10
G14, _ = interface(eta0, eta0 / 2)
z, E = standing_extrema(G14, lam14)
v.check("13-06.14a", E.max())
v.check("13-06.14b", E.min())
v.assert_true("minimum at the boundary", np.argmin(E) == 0)
v.check("13-06.14c", z[np.argmax(E)] * 1e3)

# ---------------------------------------------------------------- Lab
if lab.exists():
    # copper foil 35 um: exact SE at 10 MHz and 100 MHz (thin compared with a skin depth at low frequency)
    for f, key in ((1e7, "a"), (1e8, "b")):
        v.check(f"Lab 13-06.{key}", -20 * math.log10(abs(stack_reflection(f, [metal(5.8e7, f, 35e-6)])[1])))
    # half-wave radome: fractional bandwidth where reflectance stays below 1%
    lo = brentq(lambda f: abs(stack_reflection(f, [dielectric(4, f, d7)])[0]) ** 2 - 0.01, 8e9, 1e10, xtol=1)
    hi = brentq(lambda f: abs(stack_reflection(f, [dielectric(4, f, d7)])[0]) ** 2 - 0.01, 1e10, 1.2e10, xtol=1)
    v.check("Lab 13-06.c", (hi - lo) / 1e10 * 100)

# 15: oblique TM at 30 degrees, by solving the two boundary conditions as a linear system with the field vectors
n1_, n2_, thi = 1.0, 1.5, math.radians(30)
tht = math.asin(n1_ * math.sin(thi) / n2_)
e1_, e2_ = 376.7 / n1_, 376.7 / n2_
Ei = np.array([math.cos(thi), 0, -math.sin(thi)])
Er_dir = np.array([math.cos(thi), 0, math.sin(thi)])
Et_dir = np.array([math.cos(tht), 0, -math.sin(tht)])
# unknowns (Gamma, tau): tangential E_x and H_y continuous at z = 0
Amat = np.array([[Er_dir[0], -Et_dir[0]], [-1 / e1_, -1 / e2_]])
rhs = np.array([-Ei[0], -1 / e1_])
G15, t15 = np.linalg.solve(Amat, rhs)
v.check("13-06.15a", math.degrees(tht))
v.check("13-06.15b", G15)
v.check("13-06.15c", t15)
# power: z-component of the time-average Poynting vector of each wave
Sz = lambda Evec, amp, eta, hsign: 0.5 * np.cross(amp * Evec, np.array([0, hsign * amp / eta, 0]))[2]  # noqa: E731
Si, Sr, St = Sz(Ei, 1.0, e1_, 1), Sz(Er_dir, G15, e1_, -1), Sz(Et_dir, t15, e2_, 1)
v.check("13-06.15d", -100 * Sr / Si)
v.check("13-06.15e", 100 * St / Si)
v.assert_true("13-06.15 power balance", abs((-Sr + St) / Si - 1) < 1e-12)
# TE at the same angle: E along y, tangential H_x continuous
Ate = np.array([[1, -1], [math.cos(thi) / e1_, math.cos(tht) / e2_]])
G15te, _ = np.linalg.solve(Ate, np.array([-1, math.cos(thi) / e1_]))
v.check("13-06.15f", G15te)
v.check("13-06.15g", 100 * G15te**2)

sys.exit(v.finish())
