#!/usr/bin/env python3
"""Verify every number published in chapter 04-10, its solutions and its lab handout.

Independent routes: photon quantities from the exact SI constants; box energies by solving
sin(kL) = 0 numerically and checked against a finite-difference eigenvalue solve; hydrogen from the
constants; tunneling from a numerically solved 4×4 boundary-matching system (not the closed form);
probabilities by integrating |psi|^2; the finite well from its transcendental equations; the
photoelectric slope by least squares.
"""
from __future__ import annotations

import sys
import warnings
from math import exp, log, pi, sqrt, tan
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C_DIR = HERE.parent
v = Verifier.from_files("04-10", C_DIR / "chapters" / "04-10-intro-quantum-mechanics.md",
                        C_DIR / "solutions" / "04-10-solutions.md", C_DIR / "labs" / "04-10-lab" / "README.md")
H = 6.62607015e-34
C = 299792458.0
E_CH = 1.602176634e-19
KB = 1.380649e-23
ME = 9.1093837139e-31
EPS0 = 8.8541878188e-12
HBAR = H / (2 * pi)
HC_EV_NM = H * C / E_CH * 1e9


def photon_eV(lam_nm):
    return H * C / (lam_nm * 1e-9) / E_CH


def box_level(n, L, m=ME):
    """Energy (eV) of level n in an infinite well: solve sin(kL) = 0 for its n-th positive root."""
    k = brentq(lambda kk: np.sin(kk * L), (n - 0.5) * pi / L, (n + 0.5) * pi / L)
    return HBAR**2 * k**2 / (2 * m) / E_CH


def tunnel_T(E_eV, V0_eV, d, m=ME):
    """Solve the 4 matching conditions at x = 0 and x = d for unit incident amplitude."""
    k = sqrt(2 * m * E_eV * E_CH) / HBAR
    q = sqrt(2 * m * (V0_eV - E_eV) * E_CH) / HBAR
    A = np.array([[1, -1, -1, 0],
                  [-1j * k, -q, q, 0],
                  [0, np.exp(q * d), np.exp(-q * d), -np.exp(1j * k * d)],
                  [0, q * np.exp(q * d), -q * np.exp(-q * d), -1j * k * np.exp(1j * k * d)]], dtype=complex)
    rhs = np.array([-1, -1j * k, 0, 0], dtype=complex)
    r, c1, c2, t = np.linalg.solve(A, rhs)
    return abs(t) ** 2


# ---------------------------------------------------------------- theory keys
v.check("T 04-10.a", HC_EV_NM)
v.check("T 04-10.b", HBAR)
# finite-difference check of the 1 nm box ground state
N = 6000
dx = 1e-9 / (N + 1)
tfd = HBAR**2 / (2 * ME * dx**2)
w = eigh_tridiagonal(2 * tfd * np.ones(N), -tfd * np.ones(N - 1), select="i", select_range=(0, 0))[0]
v.assert_true("finite-difference box ground state matches", abs(w[0] / E_CH / box_level(1, 1e-9) - 1) < 1e-4)

# ---------------------------------------------------------------- examples
for key, lam in (("Ex 04-10.1a", 850), ("Ex 04-10.1b", 1310), ("Ex 04-10.1c", 1550), ("Ex 04-10.1d", 13.5)):
    v.check(key, photon_eV(lam))
v.check("Ex 04-10.1e", H * 5e9 / E_CH * 1e6)
v.check("Ex 04-10.1f", KB * 300 / E_CH * 1e3)
v.check("Ex 04-10.1g", 1e-3 / (photon_eV(1550) * E_CH))
v.check("Ex 04-10.1h", brentq(lambda lam: photon_eV(lam) - 1.12, 500, 3000))
v.check("Ex 04-10.2a", brentq(lambda lam: photon_eV(lam) - 4.5, 100, 1000))
v.check("Ex 04-10.2b", photon_eV(200) - 4.5)
v.check("Ex 04-10.2c", (photon_eV(200) - 4.5) * E_CH / E_CH)
v.check("Ex 04-10.2d", 0.8 * E_CH / (photon_eV(850) * E_CH))
v.check("Ex 04-10.2e", photon_eV(1310))
lam_db = lambda m, KE_J: H / sqrt(2 * m * KE_J)
v.check("Ex 04-10.3a", lam_db(ME, 100 * E_CH) * 1e9)
v.check("Ex 04-10.3b", lam_db(ME, 1 * E_CH) * 1e9)
v.check("Ex 04-10.3c", H / (0.145 * 40))
dp4 = HBAR / (2 * 1e-9)
v.check("Ex 04-10.4a", dp4)
v.check("Ex 04-10.4b", dp4**2 / (2 * ME) / E_CH * 1e3)
v.check("Ex 04-10.4c", (HBAR / (2 * 1e-10)) ** 2 / (2 * ME) / E_CH)
E1a, E2a = box_level(1, 1e-9), box_level(2, 1e-9)
v.check("Ex 04-10.5a", E1a)
v.check("Ex 04-10.5b", E2a - E1a)
v.check("Ex 04-10.5c", HC_EV_NM / (E2a - E1a) / 1e3)
E1b, E2b = box_level(1, 1e-8), box_level(2, 1e-8)
v.check("Ex 04-10.5d", E1b * 1e3)
v.check("Ex 04-10.5e", (E2b - E1b) * 1e3)
v.check("Ex 04-10.5f", HC_EV_NM / (E2b - E1b) / 1e3)
v.check("Ex 04-10.5g", box_level(1, 1e-8, 0.067 * ME) * 1e3)
Ry = ME * E_CH**4 / (8 * EPS0**2 * H**2) / E_CH
v.check("Ex 04-10.6a", Ry)
v.check("Ex 04-10.6b", Ry * (1 - 1 / 4))
v.check("Ex 04-10.6c", HC_EV_NM / (Ry * 0.75))
v.check("Ex 04-10.6d", EPS0 * H**2 / (pi * ME * E_CH**2) * 1e9)
v.check("Ex 04-10.7a", sqrt(2 * ME * 2.1 * E_CH) / HBAR)
T12, T20 = tunnel_T(1.0, 3.1, 1.2e-9), tunnel_T(1.0, 3.1, 2.0e-9)
v.check("Ex 04-10.7b", T12)
v.check("Ex 04-10.7c", T20)
v.check("Ex 04-10.7d", T12 / T20)
v.check("Ex 04-10.7e", exp(2 * sqrt(2 * ME * 2.1 * E_CH) / HBAR * 1e-10))
v.check("Ex 04-10.7f", tunnel_T(1.0, 3.1, 1.2e-9, 0.5 * ME) / tunnel_T(1.0, 3.1, 2.0e-9, 0.5 * ME))
v.check("Ex 04-10.8a", 2**50)
v.check("Ex 04-10.8b", 2**50 * 16 / 1e15)
v.check("Ex 04-10.8c", 0.143 / 2.14**3)
v.check("Ex 04-10.8d", 2 * 13**2)

# ---------------------------------------------------------------- solutions
for key, lam in (("04-10.1a", 405), ("04-10.1b", 650), ("04-10.1c", 940)):
    v.check(key, photon_eV(lam))
N2 = 10e-6 / (photon_eV(850) * E_CH)
v.check("04-10.2a", N2)
v.check("04-10.2b", 0.7 * E_CH * N2 * 1e6)
v.check("04-10.2c", 0.7 * E_CH * N2 / 10e-6)
fs = C / np.array([450e-9, 365e-9])
slope, icpt = np.polyfit(fs, [0.605, 1.247], 1)
v.check("04-10.3a", slope)
v.check("04-10.3b", slope * E_CH)
v.check("04-10.3c", H * fs[0] / E_CH - 0.605)
v.check("04-10.4a", lam_db(ME, 30000 * E_CH) * 1e9)
v.check("04-10.4b", lam_db(1.675e-27, 0.025 * E_CH) * 1e9)
dp5 = HBAR / (2 * 5e-9)
v.check("04-10.5a", dp5)
v.check("04-10.5b", dp5**2 / (2 * ME) / E_CH * 1e3)
E61, E62 = box_level(1, 5e-9, 0.067 * ME), box_level(2, 5e-9, 0.067 * ME)
v.check("04-10.6a", E61 * 1e3)
v.check("04-10.6b", E62 * 1e3)
v.check("04-10.6c", (E62 - E61) * 1e3)
v.check("04-10.6d", HC_EV_NM / (E62 - E61) / 1e3)
v.check("04-10.7a", quad(lambda u: 2 * np.sin(pi * u) ** 2, 1 / 3, 2 / 3)[0])
v.check("04-10.7b", quad(lambda u: 2 * np.sin(2 * pi * u) ** 2, 1 / 3, 2 / 3)[0])
v.check("04-10.8a", 13.61 * (1 / 4 - 1 / 9))
v.check("04-10.8b", HC_EV_NM / (13.61 * (1 / 4 - 1 / 9)))
MP = 1.67262192595e-27
lam_ha = HC_EV_NM / (Ry / (1 + ME / MP) * (1 / 4 - 1 / 9))     # exact Rydberg energy, reduced mass
v.assert_true("reduced-mass H-alpha rounds to the measured 656.5 nm (vacuum)", round(lam_ha, 1) == 656.5)
q9 = sqrt(2 * ME * 4.5 * E_CH) / HBAR
v.check("04-10.9a", q9)
v.check("04-10.9b", exp(2 * q9 * 1e-10))
v.check("04-10.10a", brentq(lambda d: log(tunnel_T(1.0, 3.1, d)) - log(1e-10), 0.5e-9, 3e-9, xtol=1e-20) * 1e9)
n11 = 1.806e-17 / (photon_eV(550) * E_CH)
v.check("04-10.11a", n11)
v.check("04-10.11b", 0.6 * n11)
v.check("04-10.11c", sqrt(0.6 * n11))
Ec = 3 * box_level(1, 4e-9, 0.13 * ME)          # three identical 1-D ground-state energies
v.check("04-10.12a", Ec)
v.check("04-10.12b", 1.74 + Ec)
v.check("04-10.12c", HC_EV_NM / (1.74 + Ec))
amps = np.array([0.5, 1j * sqrt(3) / 2])
v.check("04-10.13a", abs(amps[0]) ** 2)
v.check("04-10.13b", abs(amps[1]) ** 2)
v.check("04-10.13c", 1000 * abs(amps[1]) ** 2)
v.check("04-10.13d", sqrt(1000 * 0.75 * 0.25))
v.check("04-10.14a", brentq(lambda lam: photon_eV(lam) - 3.6, 100, 1000))
v.check("04-10.14b", 3.6 / (H * 5e9 / E_CH))

# ---------------------------------------------------------------- lab
a_half, V0 = 1e-9, 1.0
def even(E):
    k = sqrt(2 * ME * E * E_CH) / HBAR
    q = sqrt(2 * ME * (V0 - E) * E_CH) / HBAR
    return k * tan(k * a_half) - q


def odd(E):
    k = sqrt(2 * ME * E * E_CH) / HBAR
    q = sqrt(2 * ME * (V0 - E) * E_CH) / HBAR
    return -k / tan(k * a_half) - q


roots = []
Es = np.linspace(1e-5, 0.99999, 200001)
for f in (even, odd):
    vals = np.array([f(E) for E in Es])
    for i in np.where(np.sign(vals[:-1]) != np.sign(vals[1:]))[0]:
        if abs(vals[i]) < 5e10 and abs(vals[i + 1]) < 5e10:      # skip the tan() poles
            roots.append(brentq(f, Es[i], Es[i + 1]))
v.check("Lab 04-10.a", len(roots))
v.check("Lab 04-10.b", min(roots) * 1e3)
v.check("Lab 04-10.c", tunnel_T(1.0, 3.1, 1.0e-9))
v.check("Lab 04-10.d", tunnel_T(0.5, 1.0, 0.5e-9))
v.check("Lab 04-10.e", slope * E_CH)

sys.exit(v.finish())
