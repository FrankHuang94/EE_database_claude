#!/usr/bin/env python3
"""Verify every number published in chapter 04-07, its solutions and its lab handout.

Independent routes: EMFs by numerically differentiating flux; motional EMF from the Lorentz force
integrated along the rod; skin depth by solving the 1-D diffusion equation's decay rate
numerically and AC resistance from the exact Bessel solution; inductances from integrated flux
or field energy; transformer and link quantities from the coupled-circuit equations solved as
complex linear systems; eddy loss by integrating J^2 rho over the lamination and over a cycle.
"""
from __future__ import annotations

import sys
import warnings
from math import cos, log, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import dblquad, quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import ellipe, ellipk, ellipkm1, jv

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C_DIR = HERE.parent
v = Verifier.from_files("04-07", C_DIR / "chapters" / "04-07-faraday-lenz-and-inductance.md",
                        C_DIR / "solutions" / "04-07-solutions.md", C_DIR / "labs" / "04-07-lab" / "README.md")
MU0 = 1.25663706127e-6
EPS0 = 8.8541878188e-12
RHO_CU = 1.68e-8
C_LIGHT = 299792458.0


def deriv(f, x, h):
    return (f(x - 2 * h) - 8 * f(x - h) + 8 * f(x + h) - f(x + 2 * h)) / (12 * h)


def skin_depth(rho, f, mur=1.0):
    """Decay length of the diffusion equation d2B/dx2 = j omega mu sigma B: B ~ exp(-gamma x), gamma = sqrt(j w mu / rho)."""
    gamma = np.sqrt(1j * 2 * pi * f * mur * MU0 / rho)
    return 1 / gamma.real


def ac_ratio(a, f, rho=RHO_CU):
    d = skin_depth(rho, f)
    k = (1 - 1j) / d
    Z = k * rho / (2 * pi * a) * jv(0, k * a) / jv(1, k * a)
    return Z.real / (rho / (pi * a * a))


def M_loops(r1, r2, d):
    m = 4 * r1 * r2 / ((r1 + r2) ** 2 + d * d)
    k = sqrt(m)
    return MU0 * sqrt(r1 * r2) * ((2 / k - k) * ellipk(m) - 2 / k * ellipe(m))


def reluctance_L(N, A, lc, mur, g):
    return N**2 / (lc / (mur * MU0 * A) + g / (MU0 * A))


def coupled(L1, L2, k, f, ZL, i1=1.0):
    """Solve the coupled-coil equations for a current-driven primary: returns (v1, v2) complex."""
    w = 2 * pi * f
    M = k * sqrt(L1 * L2)
    # secondary loop: j w L2 i2 + j w M i1 + ZL i2 = 0 (i2 defined into the dotted end)
    i2 = -1j * w * M * i1 / (1j * w * L2 + ZL)
    v2 = -ZL * i2
    v1 = 1j * w * L1 * i1 + 1j * w * M * i2
    return v1, v2


# ---------------------------------------------------------------- theory keys
v.check("T 04-07.a", quad(lambda x: 1.0**2 / (2 * MU0), 0, 1)[0])
v.check("T 04-07.b", skin_depth(RHO_CU, 1e9) * 1e6)

# ---------------------------------------------------------------- examples
Phi1 = lambda t: 0.2 * min(max(t, 0), 0.01) / 0.01 * 10e-4
v.check("Ex 04-07.1a", Phi1(0.01) - Phi1(0))
emf1 = 100 * deriv(Phi1, 0.005, 1e-5)
v.check("Ex 04-07.1b", emf1)
v.check("Ex 04-07.1c", emf1 / 10)
emf2 = quad(lambda y: 4.0 * 0.5, 0, 0.5)[0]             # integral of (v x B) along the rod
v.check("Ex 04-07.2a", emf2)
I2 = emf2 / 2
v.check("Ex 04-07.2b", I2)
v.check("Ex 04-07.2c", I2 * 0.5 * 0.5)
v.check("Ex 04-07.2d", I2 * 0.5 * 0.5 * 4)
lam_gen = lambda t: 200 * 0.5 * 0.01 * cos(2 * pi * 50 * t)
ts = np.linspace(0, 0.02, 20001)
emf_gen = -np.gradient([lam_gen(t) for t in ts], ts)
v.check("Ex 04-07.2e", emf_gen.max())
v.check("Ex 04-07.2f", sqrt(np.trapezoid(emf_gen**2, ts) / 0.02))
for key, f, scale in (("Ex 04-07.3a", 60, 1e3), ("Ex 04-07.3b", 1e5, 1e3), ("Ex 04-07.3c", 1e6, 1e6), ("Ex 04-07.3d", 1e9, 1e6)):
    v.check(key, skin_depth(RHO_CU, f) * scale)
v.check("Ex 04-07.3e", 0.5e-3 / (2 * skin_depth(RHO_CU, 1e6)))
v.check("Ex 04-07.3f", ac_ratio(0.5e-3, 1e6))
d3 = skin_depth(RHO_CU, 1e6)
v.check("Ex 04-07.3g", pi * 0.5e-3**2 / (pi * 0.5e-3**2 - pi * (0.5e-3 - d3) ** 2))   # current in a curved shell of depth δ
v.check("Ex 04-07.3h", 0.5e-3 / (2 * d3) + 0.25)
N4, l4, r4 = 500, 0.1, 0.01
B4 = MU0 * N4 / l4 * 2
L4 = N4 * B4 * pi * r4**2 / 2                          # flux linkage per ampere
v.check("Ex 04-07.4a", L4 * 1e3)
v.check("Ex 04-07.4b", quad(lambda i: L4 * i, 0, 2)[0] * 1e3)
v.check("Ex 04-07.4c", B4 * 1e3)
v.check("Ex 04-07.4d", B4**2 / (2 * MU0))
v.check("Ex 04-07.4e", B4**2 / (2 * MU0) * pi * r4**2 * l4 * 1e3)
N5, A5, lc5, mur5, g5 = 20, 4e-5, 0.05, 2000, 5e-4
Rc, Rg = lc5 / (mur5 * MU0 * A5), g5 / (MU0 * A5)
v.check("Ex 04-07.5a", Rc)
v.check("Ex 04-07.5b", Rg)
L5 = reluctance_L(N5, A5, lc5, mur5, g5)
L50 = reluctance_L(N5, A5, lc5, mur5, 0)
v.check("Ex 04-07.5c", L5 * 1e6)
v.check("Ex 04-07.5d", L50 * 1e6)
Isat = brentq(lambda I: N5 * I / (Rc + Rg) / A5 - 0.39, 0, 100)
v.check("Ex 04-07.5e", Isat)
B5 = 0.39
U_core = B5**2 / (2 * mur5 * MU0) * A5 * lc5
U_gap = B5**2 / (2 * MU0) * A5 * g5
v.check("Ex 04-07.5f", (U_core + U_gap) * 1e3)
v.assert_true("field energy equals 1/2 L I^2", abs((U_core + U_gap) / (0.5 * L5 * Isat**2) - 1) < 1e-9)
v.check("Ex 04-07.5g", U_gap / (U_core + U_gap) * 100)
v.check("Ex 04-07.5h", B5**2 / (2 * mur5 * MU0) * A5 * lc5 * 1e6)
v.check("Ex 04-07.6a", brentq(lambda n: 230 * n / 1150 - 12, 1, 1000))
v.check("Ex 04-07.6b", 2 * 12 / 230)                     # power balance v1 i1 = v2 i2
v.check("Ex 04-07.6c", (230 / 12) ** 2 * 6)
v1o, v2o = coupled(10e-6, 10e-6, 0.5, 360e3, 1e12)
v.check("Ex 04-07.7a", 0.5 * sqrt(10e-6 * 10e-6) * 1e6)
v.check("Ex 04-07.7b", abs(v2o))
v.check("Ex 04-07.7c", abs(v1o))
v.check("Ex 04-07.7d", abs(coupled(10e-6, 10e-6, 0.2, 360e3, 1e12)[1]))
v.check("Ex 04-07.7e", abs(coupled(10e-6, 10e-6, 0.8, 360e3, 1e12)[1]))
D8 = 1.05 / 1.7
v.check("Ex 04-07.8a", D8)
dI = quad(lambda t: (1.7 - 1.05) / 2e-9, 0, D8 / 140e6)[0]
v.check("Ex 04-07.8b", dI)
v.check("Ex 04-07.8c", brentq(lambda L: (1.7 - 1.05) * D8 / 1e6 / L - dI, 1e-9, 1e-5) * 1e9)

# ---------------------------------------------------------------- solutions
v.check("04-07.1a", 50 * 0.5 * 20e-4 / 0.1)
emf_p2 = 0.3 * 0.1 * 2
v.check("04-07.2a", emf_p2)
v.check("04-07.2b", emf_p2 / 0.5)
v.check("04-07.2c", emf_p2 / 0.5 * 0.1 * 0.3)
v.check("04-07.2d", (emf_p2 / 0.5) ** 2 * 0.5)
v.check("04-07.3a", brentq(lambda n: n * 1.2 * 0.02 * 2 * pi * 50 / sqrt(2) - 230, 1, 1000))
v.check("04-07.4a", 0.02 * 500)
v.check("04-07.4b", (12 - 10) / 0.5)
v.check("04-07.4c", 12 / 0.5)
v.check("04-07.4d", 10 * 4)
v.check("04-07.5a", skin_depth(RHO_CU, 5e4) * 1e3)
v.check("04-07.5b", skin_depth(RHO_CU, 1e10) * 1e6)
v.check("04-07.5c", skin_depth(1e-7, 50, 1000) * 1e3)
L6 = 100 * quad(lambda r: MU0 * 100 * 1.0 / (2 * pi * r) * 0.01, 0.02, 0.03)[0]
v.check("04-07.6a", L6 * 1e6)
v.check("04-07.6b", 2000 * L6 * 1e3)
sol7 = solve_ivp(lambda t, i: [(10 - 5 * i[0]) / 10e-3], (0, 0.05), [0.0], rtol=1e-11, atol=1e-14, dense_output=True)
v.check("04-07.7a", 10e-3 / 5 * 1e3)
v.check("04-07.7b", sol7.y[0, -1])
v.check("04-07.7c", 0.5 * 10e-3 * sol7.y[0, -1] ** 2 * 1e3)
v.check("04-07.7d", brentq(lambda t: sol7.sol(t)[0] - 1.0, 1e-5, 0.01) * 1e3)
a8, b8 = 0.45e-3, 1.475e-3
L8 = quad(lambda r: MU0 / (2 * pi * r), a8, b8)[0]
C8 = 1 / quad(lambda r: 1 / (2 * pi * 2.25 * EPS0 * r), a8, b8)[0]
v.check("04-07.8a", L8 * 1e6)
v.check("04-07.8b", sqrt(L8 / C8))
v.check("04-07.8c", 1 / sqrt(L8 * C8))
v.check("04-07.8d", C_LIGHT * sqrt(L8 * C8))
uB, uE = 1.5**2 / (2 * MU0), 0.5 * EPS0 * 3e6**2
v.check("04-07.9a", uB)
v.check("04-07.9b", uE)
v.check("04-07.9c", uB / uE)
v.check("04-07.10a", 0.98 * sqrt(100e-6 * 25e-6) * 1e6)
v.check("04-07.10b", sqrt(25e-6 / 100e-6))
v.check("04-07.11a", brentq(lambda n: n**2 * 8 - 800, 1, 100))
v.check("04-07.12a", 1e-5 * 10 / (0.39 * 4e-5))
g12 = brentq(lambda g: MU0 * 49 * 4e-5 / g - 1e-5, 1e-6, 1e-2)
v.check("04-07.12b", g12 * 1e3)
v.check("04-07.12c", brentq(lambda I: MU0 * 7 * I / g12 - 0.39, 0, 100))


def lam_loss(f, Bm, t, rho):
    """Time- and thickness-averaged rho J^2 with J = (x/rho) dB/dt."""
    w = 2 * pi * f
    T = 1 / f
    inner = lambda tt: quad(lambda x: (x * w * Bm * cos(w * tt)) ** 2 / rho, -t / 2, t / 2)[0] / t
    return quad(inner, 0, T, limit=200)[0] / T


P13 = lam_loss(50, 1.5, 0.35e-3, 4.7e-7)
v.check("04-07.13a", P13)
v.check("04-07.13b", P13 / 7650)
v.check("04-07.13c", lam_loss(400, 1.5, 0.1e-3, 4.7e-7) / 7650)
v.check("04-07.14a", 1e-9 * 0.1 / 100e-12)
v.check("04-07.14b", 1e-9 / 10 * 0.1 / 100e-12)
v.check("04-07.15a", skin_depth(RHO_CU, 1e5) * 1e3)
v.check("04-07.15b", ac_ratio(0.5e-3, 1e5))
v.check("04-07.15c", ac_ratio(0.05e-3, 1e5))
# 16: series-resonant link, solved as a 2x2 complex system at resonance
w16 = 2 * pi * 360e3
L16, R16, RL16 = 10e-6, 0.1, 5.0
C16 = 1 / (w16**2 * L16)
M16 = 0.5 * L16
Z = np.array([[R16 + 1j * w16 * L16 + 1 / (1j * w16 * C16), 1j * w16 * M16],
              [1j * w16 * M16, R16 + RL16 + 1j * w16 * L16 + 1 / (1j * w16 * C16)]])
i = np.linalg.solve(Z, [1.0, 0.0])
Zin = 1 / i[0]
v.check("04-07.16a", (Zin - R16).real)
v.check("04-07.16b", abs(i[1]) ** 2 * RL16 / (abs(i[0]) ** 2 * Zin.real))
v.check("04-07.16c", w16 * L16 / R16)
R17, dBdt = 0.02, 0.5
flux_rate = lambda r: quad(lambda rr: dBdt * 2 * pi * rr if rr <= R17 else 0.0, 0, r, points=[R17] if r > R17 else None)[0]
v.check("04-07.17a", flux_rate(0.01) / (2 * pi * 0.01) * 1e3)      # Faraday: E 2 pi r = d(flux)/dt
v.check("04-07.17b", flux_rate(0.03) / (2 * pi * 0.03) * 1e3)
v.check("04-07.17c", flux_rate(0.03) * 1e3)

# ---------------------------------------------------------------- lab
mdip, Rl = 1.0, 0.01
Phi = lambda z: MU0 * mdip * Rl**2 / (2 * (Rl**2 + z**2) ** 1.5)
z_peak = brentq(lambda z: deriv(lambda zz: deriv(Phi, zz, 1e-6), z, 1e-6), 1e-4, 0.02)
v.check("Lab 04-07.a", abs(deriv(Phi, z_peak, 1e-7)) * 1.0 * 1e3)
v.check("Lab 04-07.b", brentq(lambda f: ac_ratio(0.5e-3, f) - 2, 1e4, 1e7) / 1e3)
# Current-sheet inductance from ring-to-ring mutual inductances. M(s) has a log singularity at s = 0, so the
# first millimetre is integrated in u = ln s (ds = e^u du), which makes the integrand smooth and tiny at u → -∞.
def M_equal(r, s):
    """M of two coaxial loops of radius r a distance s apart, using K(1 - p) directly so tiny s stays accurate."""
    p = s * s / (4 * r * r + s * s)                      # 1 - m
    k = sqrt(1 - p)
    return MU0 * r * ((2 / k - k) * ellipkm1(p) - 2 / k * ellipe(1 - p))


sheet_f = lambda s: (0.1 - s) * M_equal(0.01, s)
near = quad(lambda u: sheet_f(np.exp(u)) * np.exp(u), log(1e-30), log(1e-3), limit=400, epsabs=0, epsrel=1e-12)[0]
far = quad(sheet_f, 1e-3, 0.1, limit=400, epsabs=0, epsrel=1e-12)[0]
Lsheet = (500 / 0.1) ** 2 * 2 * (near + far)
L_long = MU0 * 500**2 * pi * 0.01**2 / 0.1
k2n = 4 * 0.01**2 / (4 * 0.01**2 + 0.1**2)            # Nagaoka's closed form (complete elliptic integrals)
kn, kpn = sqrt(k2n), sqrt(1 - k2n)
K_nag = 4 / (3 * pi * kpn) * ((kpn**2 / k2n) * (ellipk(k2n) - ellipe(k2n)) + ellipe(k2n) - kn)
v.assert_true("ring-sum inductance matches Nagaoka's closed form", abs(Lsheet / L_long / K_nag - 1) < 1e-6)
v.check("Lab 04-07.c", Lsheet / L_long)
v.check("Lab 04-07.d", Lsheet * 1e3)
Mneu = MU0 / (4 * pi) * 0.05**2 * dblquad(lambda p1, p2: cos(p1 - p2) / sqrt(2 * 0.05**2 * (1 - cos(p1 - p2)) + 0.05**2),
                                         0, 2 * pi, 0, 2 * pi)[0]
v.check("Lab 04-07.e", Mneu * 1e9)
v.assert_true("Neumann matches Maxwell's formula", abs(Mneu / M_loops(0.05, 0.05, 0.05) - 1) < 1e-8)
g100 = brentq(lambda g: reluctance_L(20, 4e-5, 0.05, 2000, g) - 100e-6, 0, 2e-3)
v.check("Lab 04-07.f", g100 * 1e3)
v.check("Lab 04-07.g", 0.39 * 4e-5 * (0.05 / (2000 * MU0 * 4e-5) + g100 / (MU0 * 4e-5)) / 20)

sys.exit(v.finish())
