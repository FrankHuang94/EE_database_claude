#!/usr/bin/env python3
"""Verify every number in chapter 13-05 (plane waves in lossless and lossy media), its solutions and lab.

Independent routes (not the chapter's closed forms):
- propagation constants and impedances by complex square roots of j omega mu (sigma + j omega eps), checked against
  the closed-form alpha and beta and their limits;
- skin depth and surface resistance by solving the field equations inside a conductor as a finite-difference
  boundary-value problem and integrating its loss;
- round-wire AC resistance by the exact Bessel-function solution;
- polarization by tracing E(t) over a cycle (principal axes and rotation sense);
- the RG-58 loss split by solving the two-point fit as a linear system;
- energy and power by numerical time averages.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
import scipy.sparse as sps
import scipy.sparse.linalg as spla
from scipy.optimize import brentq
from scipy.special import jv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-05-plane-waves.md",
         COURSE / "solutions" / "13-05-solutions.md"]
lab = COURSE / "labs" / "13-05-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-05", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 1 / math.sqrt(mu0 * e0)
eta0 = math.sqrt(mu0 / e0)
NP_DB = 20 * math.log10(math.e)
SIG_CU = 5.8e7


# ---------------------------------------------------------------- helpers
def gamma_eta(f, sigma, er=1.0, tand=0.0, mur=1.0):
    """Exact propagation constant and intrinsic impedance from the complex-permittivity form."""
    w = 2 * math.pi * f
    y = sigma + 1j * w * er * e0 * (1 - 1j * tand)
    z = 1j * w * mur * mu0
    g = cmath.sqrt(z * y)
    if g.real < 0:
        g = -g
    return g, cmath.sqrt(z / y)


def conductor_fd(f, sigma, depth_in_delta=24, n=12000):
    """Solve d2E/dz2 = j w mu sigma E in 0 < z < D with E(0) = 1, E(D) = 0 by finite differences.
    Returns z, E(z), the surface H from Faraday (dE/dz = -j w mu H), and the loss per area."""
    w = 2 * math.pi * f
    delta_guess = 1 / math.sqrt(math.pi * f * mu0 * sigma)
    D = depth_in_delta * delta_guess
    z = np.linspace(0, D, n + 1)
    h = z[1] - z[0]
    k2 = 1j * w * mu0 * sigma
    main = np.full(n - 1, -2 / h**2 - k2, dtype=complex)
    off = np.full(n - 2, 1 / h**2, dtype=complex)
    A = sps.diags([off, main, off], [-1, 0, 1], format="csc")
    rhs = np.zeros(n - 1, dtype=complex)
    rhs[0] = -1 / h**2
    E = np.concatenate([[1.0], spla.spsolve(A, rhs), [0.0]])
    # surface H from the current integral (Ampere: H_t at the surface = total current per width)
    J = sigma * E
    Ht = np.sum((J[1:] + J[:-1]) / 2) * h
    loss = np.sum((np.abs(J[1:]) ** 2 + np.abs(J[:-1]) ** 2) / 2) * h / (2 * sigma)
    return z, E, Ht, loss


def skin_depth_fd(f, sigma):
    z, E, _, _ = conductor_fd(f, sigma)
    return brentq(lambda zz: np.interp(zz, z, np.abs(E)) - math.exp(-1), z[1], z[-1] / 2, xtol=1e-15)


def Rs_fd(f, sigma):
    _, _, Ht, loss = conductor_fd(f, sigma)
    return 2 * loss / abs(Ht) ** 2


def wire_Z_bessel(f, a, sigma):
    """Exact internal impedance per metre of a round wire: Z = (k/(2 pi a sigma)) J0(ka)/J1(ka), k^2 = -j w mu sigma."""
    w = 2 * math.pi * f
    k = cmath.sqrt(-1j * w * mu0 * sigma)
    return k / (2 * math.pi * a * sigma) * jv(0, k * a) / jv(1, k * a)


def trace_polarization(Ex, Ey, n=4000):
    """Field tip over one cycle for phasor components (Ex, Ey) at z = 0; returns points and rotation sign about +z."""
    wt = np.linspace(0, 2 * math.pi, n, endpoint=False)
    ex = (Ex * np.exp(1j * wt)).real
    ey = (Ey * np.exp(1j * wt)).real
    rot = np.mean(ex * np.gradient(ey) - ey * np.gradient(ex))  # z-component of E x dE/dt
    return ex, ey, rot


def axes(ex, ey):
    s = np.linalg.svd(np.stack([ex, ey]), compute_uv=False)
    return s[0], s[1]


# ---------------------------------------------------------------- theory
d1g = skin_depth_fd(1e9, SIG_CU)
v.check("T 13-05.a", 2 * math.pi * d1g * 1e6)
v.check("T 13-05.b", 2 * math.pi * 1e9 * d1g / 1e3)
g_cu = gamma_eta(1e9, SIG_CU)[0]
v.assert_true("good conductor: alpha = beta", abs(g_cu.real / g_cu.imag - 1) < 1e-6)

# ---------------------------------------------------------------- Example 1
g1, eta1 = gamma_eta(2.4e9, 0.0)
v.check("Ex 13-05.1a", 2 * math.pi / g1.imag * 100)
v.check("Ex 13-05.1b", g1.imag)
v.check("Ex 13-05.1c", 1 / abs(eta1) * 1e3)
v.check("Ex 13-05.1d", 1 / (2 * eta1.real) * 1e3)
g1d, eta1d = gamma_eta(2.4e9, 0.0, er=4)
v.check("Ex 13-05.1e", 2 * math.pi / g1d.imag * 100)
v.check("Ex 13-05.1f", eta1d.real)
v.check("Ex 13-05.1g", 2 * math.pi * 2.4e9 / g1d.imag)

# ---------------------------------------------------------------- Example 2
ex, ey, rot = trace_polarization(3, 4)
v.check("Ex 13-05.2a", math.degrees(math.atan2(ey[np.argmax(ex)], ex.max())))
ex, ey, rot = trace_polarization(1, -1j)
v.assert_true("x - jy is circular", abs(np.ptp(np.hypot(ex, ey))) < 1e-9)
v.assert_true("x - jy rotates x -> y (right-hand for +z travel)", rot > 0)
v.check("Ex 13-05.2b", 10 * math.log10(np.mean(ex**2) / np.mean(ex**2 + ey**2)))

# ---------------------------------------------------------------- Example 3
for f, key, scale in ((60, "a", 1e3), (1e6, "b", 1e6), (1e9, "c", 1e6), (1e10, "d", 1e6)):
    v.check(f"Ex 13-05.3{key}", skin_depth_fd(f, SIG_CU) * scale)
Rs1g = Rs_fd(1e9, SIG_CU)
v.check("Ex 13-05.3e", Rs1g * 1e3)
v.assert_true("Rs = Re(eta_c)", abs(Rs1g / gamma_eta(1e9, SIG_CU)[1].real - 1) < 1e-4)

# ---------------------------------------------------------------- Example 4
a4 = 0.5e-3
d4 = skin_depth_fd(1e8, SIG_CU)
Rdc4 = 1 / (SIG_CU * math.pi * a4**2)
Rac4 = Rs_fd(1e8, SIG_CU) / (2 * math.pi * a4)
v.check("Ex 13-05.4a", d4 * 1e6)
v.check("Ex 13-05.4b", Rdc4 * 1e3)
v.check("Ex 13-05.4c", Rac4)
v.check("Ex 13-05.4d", Rac4 / Rdc4)
Zb = wire_Z_bessel(1e8, a4, SIG_CU)
v.assert_true("Bessel AC resistance within 1% of the thin-skin estimate", abs(Zb.real / Rac4 - 1) < 0.01,
              f"{Zb.real} vs {Rac4}")
# the a/(2 delta) + 1/4 statement and the 5% at a = 10 delta statement
for a_over_d in (10, 30):
    dd = 1 / math.sqrt(math.pi * 1e6 * mu0 * SIG_CU)
    aa = a_over_d * dd
    ratio = wire_Z_bessel(1e6, aa, SIG_CU).real * SIG_CU * math.pi * aa**2
    v.assert_true(f"Bessel ratio near a/2d + 1/4 at a = {a_over_d} delta", abs(ratio - (a_over_d / 2 + 0.25)) < 0.02)
    if a_over_d == 10:
        v.assert_true("simple form within 5% at a = 10 delta", abs((a_over_d / 2) / ratio - 1) < 0.05)

# ---------------------------------------------------------------- Example 5 (low-loss form beta tan(delta)/2, with
# beta from the lossless complex root; the exact complex-permittivity root must agree to order tan^2(delta))


def alpha_lowloss(f, er, tand):
    return gamma_eta(f, 0.0, er=er)[0].imag * tand / 2


a5 = alpha_lowloss(1e10, 4.0, 0.02)
b5 = alpha_lowloss(1e10, 3.45, 0.0031)
v.assert_true("low-loss alpha within tan^2/8 of exact", abs(gamma_eta(1e10, 0.0, er=4.0, tand=0.02)[0].real / a5 - 1)
              < 0.02**2 / 8 * 1.01)
v.check("Ex 13-05.5a", a5)
v.check("Ex 13-05.5b", a5 * NP_DB)
v.check("Ex 13-05.5c", b5)
v.check("Ex 13-05.5d", b5 * NP_DB)
v.check("Ex 13-05.5e", a5 / b5)
v.check("Ex 13-05.5f", alpha_lowloss(2.8e10, 4.0, 0.02) * NP_DB / 100)

# ---------------------------------------------------------------- Example 6
v.check("Ex 13-05.6a", skin_depth_fd(1e4, 4.0))
v.check("Ex 13-05.6b", skin_depth_fd(1e6, 4.0))
g10k = gamma_eta(1e4, 4.0, er=81)[0]
v.check("Ex 13-05.6c", 20 * g10k.real * NP_DB)
g6 = gamma_eta(1e9, 4.0, er=81)[0]
v.check("Ex 13-05.6d", g6.real)
v.check("Ex 13-05.6e", g6.imag)
gc6 = math.sqrt(math.pi * 1e9 * mu0 * 4.0)
v.check("Ex 13-05.6f", gc6)
v.check("Ex 13-05.6g", g6.real * NP_DB)
v.check("Ex 13-05.6h", 20 * g10k.real)
v.check("Ex 13-05.6i", (gc6 / g6.real - 1) * 100)
v.check("Ex 13-05.6j", 4.0 / (2 * math.pi * 1e4 * 81 * e0))
# closed-form alpha/beta agree with the complex root
x6 = 4.0 / (2 * math.pi * 1e9 * 81 * e0)
pref = 2 * math.pi * 1e9 * math.sqrt(mu0 * 81 * e0 / 2)
v.assert_true("closed-form alpha", abs(pref * math.sqrt(math.sqrt(1 + x6**2) - 1) / g6.real - 1) < 1e-12)
v.assert_true("closed-form beta", abs(pref * math.sqrt(math.sqrt(1 + x6**2) + 1) / g6.imag - 1) < 1e-12)

# ---------------------------------------------------------------- practitioner and simulation
fitA = np.array([[math.sqrt(100), 100], [math.sqrt(1000), 1000]])
ab = np.linalg.solve(fitA, np.array([4.9, 21.5]))
v.check("Prac 13-05.a", ab[0] * math.sqrt(100))
v.check("Prac 13-05.b", ab[1] * 100)
v.check("Prac 13-05.c", ab[0] * math.sqrt(1000))
v.check("Prac 13-05.d", ab[1] * 1000)
v.check("Prac 13-05.e", skin_depth_fd(2e4, SIG_CU) * 1e3)
# laminate data-sheet values (R-193): exact complex gamma of each dielectric, ratio of attenuation constants
alpha_d = lambda f, er, tand: (2 * math.pi * f * cmath.sqrt(mu0 * er * e0 * (1 - 1j * tand)) * 1j).real  # noqa: E731
v.check("Prac 13-05.f", alpha_d(1e10, 3.92, 0.0250) / alpha_d(1e10, 3.45, 0.0031))
v.check("Prac 13-05.g", alpha_d(1e10, 3.92, 0.0250) * NP_DB / 100)
for key, awg_d, f in (("h", 2.053e-3, 2e4), ("i", 2.053e-3, 1e4), ("j", 1.291e-3, 2e4)):
    aw_ = awg_d / 2
    v.check(f"Prac 13-05.{key}", wire_Z_bessel(f, aw_, SIG_CU).real * SIG_CU * math.pi * aw_**2)
Zs = gamma_eta(1e9, SIG_CU)[1]
v.check("Sim 13-05.a", Zs.real * 1e3)
v.check("Sim 13-05.b", Zs.imag * 1e3)

# ---------------------------------------------------------------- Problems
w1 = 2 * math.pi * 1e9
er1 = brentq(lambda er: gamma_eta(1e9, 0.0, er=er)[0].imag - 42, 1, 10, xtol=1e-14)
eta_1 = gamma_eta(1e9, 0.0, er=er1)[1].real
v.check("13-05.1a", er1)
v.check("13-05.1b", eta_1)
v.check("13-05.1c", 5 / eta_1 * 1e3)
tt = np.linspace(0, 1e-9, 4000, endpoint=False)
v.check("13-05.1d", np.mean(5 * np.cos(w1 * tt) * (5 / eta_1) * np.cos(w1 * tt)) * 1e3)

for f, key, scale in ((60, "a", 1e-3), (2.4e9, "b", 100), (28e9, "c", 100), (193.4e12, "d", 1e6)):
    v.check(f"13-05.2{key}", 2 * math.pi / gamma_eta(f, 0.0)[0].imag * scale)
ex, ey, rot = trace_polarization(1, 2j)
big, small = axes(ex, ey)
v.check("13-05.3a", big / small)
v.assert_true("x + 2jy is left-hand for +z travel", rot < 0)
v.assert_true("x + jy is left-hand for +z travel", trace_polarization(1, 1j)[2] < 0)

E4 = brentq(lambda E: E**2 / (2 * eta0) - 10, 1, 1000)
v.check("13-05.4a", E4)
v.check("13-05.4b", E4 / gamma_eta(1e9, 0.0)[1].real)
v.check("13-05.4c", gamma_eta(1e9, 0.0, er=81)[1].real)

for sig, key in ((3.5e7, "a"), (4.1e7, "b")):
    v.check(f"13-05.5{key}", skin_depth_fd(1e9, sig) * 1e6)
v.check("13-05.5c", Rs_fd(1e9, 3.5e7) * 1e3)


def ratio_alpha(x):
    """alpha_exact / alpha_good_conductor at sigma / (w eps) = x, from the complex root (eps = eps0, w = 1e9 rad/s)."""
    w = 1e9
    sig = x * w * e0
    g = cmath.sqrt(1j * w * mu0 * (sig + 1j * w * e0))
    return g.real / math.sqrt(w * mu0 * sig / 2)


x6p = brentq(lambda x: ratio_alpha(x) - 0.99, 1, 1e4, xtol=1e-12)
v.check("13-05.6a", x6p)
v.check("13-05.6b", 4.0 / (2 * math.pi * 81 * e0 * x6p) / 1e6)
a7 = alpha_lowloss(1e9, 2.25, 0.0002)
v.check("13-05.7a", a7)
v.check("13-05.7b", a7 * NP_DB)

Rdc8 = 0.1 / (SIG_CU * 1e-4 * 35e-6)
Rac8 = Rs_fd(1e9, SIG_CU) * 0.1 / (2 * 1e-4)
v.check("13-05.8a", Rdc8)
v.check("13-05.8b", Rac8)
v.check("13-05.8c", Rac8 / Rdc8)
g9 = gamma_eta(1e4, 4.0, er=81)[0].real * NP_DB
v.check("13-05.9a", g9)
v.check("13-05.9b", 100 / g9)
v.check("13-05.9c", 100 / (gamma_eta(100, 4.0, er=81)[0].real * NP_DB))
g10, e10 = gamma_eta(1e9, 4.0, er=81)
v.check("13-05.10a", g10.real)
v.check("13-05.10b", g10.imag)
v.check("13-05.10c", abs(e10))
v.check("13-05.10d", math.degrees(cmath.phase(e10)))
_, _, Ht11, loss11 = conductor_fd(1e9, SIG_CU)
v.check("13-05.11a", loss11 / abs(Ht11) ** 2 * 1.0**2 * 1e3)
w12 = 2 * math.pi * 1e9
E12 = math.sqrt(2 * eta0 * 10)
tt = np.linspace(0, 2 * math.pi / w12, 4000, endpoint=False)
# H from Faraday's law (dH/dt = -(1/mu0) dE/dz) rather than assuming H = E/eta0, then average the energy density
zs_, ts_ = sp.symbols("z_s t_s", real=True)
k12 = w12 / c0
Ex12 = E12 * sp.cos(w12 * ts_ - k12 * zs_)
Hy12 = sp.integrate(-sp.diff(Ex12, zs_) / mu0, ts_)
fH12 = sp.lambdify(ts_, Hy12.subs(zs_, 0), "numpy")
u12 = np.mean(0.5 * e0 * (E12 * np.cos(w12 * tt)) ** 2 + 0.5 * mu0 * fH12(tt) ** 2)
v.check("13-05.12a", u12)
v.assert_true("u v = S", abs(u12 * c0 / 10 - 1) < 1e-9)

Rs13 = Rs_fd(1e9, SIG_CU)
Rp13 = Rs13 / (2 * math.pi) * (1 / 0.5e-3 + 1 / 1.75e-3)
Z0_13 = eta0 / (2 * math.pi * 1.5) * math.log(3.5)
ac13 = Rp13 / (2 * Z0_13) * NP_DB
ad13 = a7 * NP_DB
v.check("13-05.13a", Rp13)
v.check("13-05.13b", ac13)
v.check("13-05.13c", ad13)
v.check("13-05.13d", ac13 + ad13)
ex, ey, _ = trace_polarization(2, 1j)  # axial ratio 2, major axis along x
best = np.mean(ex**2) / np.mean(ex**2 + ey**2)
worst = np.mean(ey**2) / np.mean(ex**2 + ey**2)
v.check("13-05.14a", best)
v.check("13-05.14b", 10 * math.log10(best))
v.check("13-05.14c", 10 * math.log10(worst))

# ---------------------------------------------------------------- Lab
if lab.exists():
    a_l = 0.5e-3
    Rdc_l = 1 / (SIG_CU * math.pi * a_l**2)
    v.check("Lab 13-05.a", wire_Z_bessel(1e6, a_l, SIG_CU).real / Rdc_l)
    f2 = brentq(lambda f: wire_Z_bessel(f, a_l, SIG_CU).real / Rdc_l - 2, 1e3, 1e7, xtol=1e-6)
    v.check("Lab 13-05.b", f2 / 1e3)
    f10 = brentq(lambda f: math.sqrt(math.pi * f * mu0 * 4.0) / gamma_eta(f, 4.0, er=81)[0].real - 1.10, 1e5, 1e10,
                 xtol=1e-3)
    v.check("Lab 13-05.c", f10 / 1e6)

sys.exit(v.finish())
