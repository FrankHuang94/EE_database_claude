#!/usr/bin/env python3
"""Verify every number published in chapter 04-08, its solutions and its lab handout.

Independent routes: displacement-current fields from Ampère–Maxwell with the enclosed flux
integrated over the disk; wave speeds and impedances from the CODATA constants; Poynting power by
integrating S over the actual surfaces; boundary reflection by solving the two continuity
equations as a linear system; dielectric attenuation from the exact complex propagation constant
(not the small-tan-delta formula), checked to agree.
"""
from __future__ import annotations

import sys
import warnings
from math import exp, log, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C_DIR = HERE.parent
v = Verifier.from_files("04-08", C_DIR / "chapters" / "04-08-maxwell-preview.md",
                        C_DIR / "solutions" / "04-08-solutions.md", C_DIR / "labs" / "04-08-lab" / "README.md")
MU0 = 1.25663706127e-6
EPS0 = 8.8541878188e-12
C = 1 / sqrt(MU0 * EPS0)
ETA0 = sqrt(MU0 / EPS0)
RHO_CU = 1.68e-8
NP_TO_DB = 20 / log(10)


def alpha_exact(f, er, tand):
    """Attenuation (Np/m) from k = omega sqrt(mu eps (1 - j tan d)), exact."""
    k = 2 * pi * f * np.sqrt(MU0 * er * EPS0 * (1 - 1j * tand))
    return -k.imag if k.imag < 0 else k.imag


def B_ampere_maxwell(i, R, r):
    """B at radius r between circular plates (radius R) charged by current i: enclosed displacement current."""
    dEdt = i / (EPS0 * pi * R**2)
    rr = min(r, R)
    id_enc = EPS0 * quad(lambda s: dEdt * 2 * pi * s, 0, rr)[0]
    return MU0 * id_enc / (2 * pi * r)


def fresnel(eta1, eta2):
    """Solve E_i + E_r = E_t and (E_i - E_r)/eta1 = E_t/eta2 for E_i = 1."""
    A = np.array([[1.0, -1.0], [-1.0 / eta1, -1.0 / eta2]])
    rhs = np.array([-1.0, -1.0 / eta1])
    Er, Et = np.linalg.solve(A, rhs)
    return Er, Et


# ---------------------------------------------------------------- theory keys
v.check("T 04-08.a", C / 1e9 * 100)
v.check("T 04-08.b", 20 * np.log10(np.e))
v.assert_true("c from CODATA mu0 and eps0 equals the exact SI value", abs(C - 299792458.0) < 0.5)

# ---------------------------------------------------------------- examples
v.check("Ex 04-08.1a", 0.5 * EPS0 * 1e6**2)
v.check("Ex 04-08.1b", 0.5 * 3.9 * EPS0 * 5e8**2)
v.check("Ex 04-08.1c", 1.0**2 / (2 * MU0))
v.check("Ex 04-08.1d", 1e-3**2 / (2 * MU0))
R2 = 0.05
v.check("Ex 04-08.2a", 1.0 / (EPS0 * pi * R2**2))
v.check("Ex 04-08.2b", EPS0 * pi * R2**2 * (1.0 / (EPS0 * pi * R2**2)))
v.check("Ex 04-08.2c", B_ampere_maxwell(1.0, R2, 0.03) * 1e6)
v.check("Ex 04-08.2d", B_ampere_maxwell(1.0, R2, 0.05) * 1e6)
v.check("Ex 04-08.2e", B_ampere_maxwell(1.0, R2, 0.10) * 1e6)
v.check("Ex 04-08.3a", C)
v.check("Ex 04-08.3b", ETA0)
v_fr4 = 1 / sqrt(MU0 * 4.6 * EPS0)
v.check("Ex 04-08.3c", v_fr4)
v.check("Ex 04-08.3d", 1e-3 / v_fr4 * 1e12)
v.check("Ex 04-08.3e", 0.1 / v_fr4 * 1e12)
v.check("Ex 04-08.3f", v_fr4 / 1e10 * 1e3)
v.check("Ex 04-08.3g", C / 1e10 * 1e3)
E0 = 100.0
v.check("Ex 04-08.4a", E0 / C * 1e9)
T = 1e-9
S_avg = quad(lambda t: (E0 * np.cos(2 * pi * t / T)) ** 2 / ETA0, 0, T)[0] / T
v.check("Ex 04-08.4b", S_avg)
u_avg = quad(lambda t: 0.5 * EPS0 * (E0 * np.cos(2 * pi * t / T)) ** 2 + (E0 / C * np.cos(2 * pi * t / T)) ** 2 / (2 * MU0), 0, T)[0] / T
v.check("Ex 04-08.4c", u_avg)
v.assert_true("intensity = energy density x c", abs(S_avg / (u_avg * C) - 1) < 1e-9)
a5, L5, I5 = 0.5e-3, 1.0, 10.0
R5 = RHO_CU * L5 / (pi * a5**2)
V5 = I5 * R5
B5 = MU0 * I5 / (2 * pi * a5)
S5 = (V5 / L5) * B5 / MU0
v.check("Ex 04-08.5a", R5 * 1e3)
v.check("Ex 04-08.5b", V5)
v.check("Ex 04-08.5c", B5 * 1e3)
v.check("Ex 04-08.5d", S5)
v.check("Ex 04-08.5e", quad(lambda z: S5 * 2 * pi * a5, 0, L5)[0])
Bc = B_ampere_maxwell(1.0, 0.05, 0.05)
Sc = (100 / 1e-3) * Bc / MU0
v.check("Ex 04-08.5f", Sc)
v.check("Ex 04-08.5g", quad(lambda z: Sc * 2 * pi * 0.05, 0, 1e-3)[0])
for (kn, kd, k10), (er, tand) in ((("Ex 04-08.6a", "Ex 04-08.6b", "Ex 04-08.6c"), (3.92, 0.025)),
                                  (("Ex 04-08.6d", "Ex 04-08.6e", "Ex 04-08.6f"), (3.66, 0.0037))):
    al = alpha_exact(10e9, er, tand)
    v.check(kn, al)
    v.check(kd, NP_TO_DB * al)
    v.check(k10, NP_TO_DB * al * 0.1)
for key_s, key_e, r in (("Ex 04-08.7a", "Ex 04-08.7c", 1.0), ("Ex 04-08.7b", "Ex 04-08.7d", 0.1)):
    S = 1.0 / quad(lambda th: 2 * pi * r * r * np.sin(th), 0, pi)[0]
    v.check(key_s, S * (1e3 if r == 1.0 else 1.0))
    v.check(key_e, sqrt(S * ETA0))
v.check("Ex 04-08.7e", 1e-3 / 1e-4)

# ---------------------------------------------------------------- solutions
uE1, uB1 = 0.5 * EPS0 * 1e4**2, 0.01**2 / (2 * MU0)
v.check("04-08.1a", uE1)
v.check("04-08.1b", uB1)
v.check("04-08.1c", uB1 / uE1)
v.check("04-08.2a", C / 60 / 1e3)
v.check("04-08.2b", C / 2.4e9 * 100)
v.check("04-08.2c", C / 28e9 * 1e3)
v.check("04-08.2d", C / 193.4e12 * 1e6)
d_s, d_m = 0.3 * sqrt(MU0 * 3.66 * EPS0), 0.3 * sqrt(MU0 * 2.9 * EPS0)
v.check("04-08.3a", d_s * 1e9)
v.check("04-08.3b", d_m * 1e9)
v.check("04-08.3c", (d_s - d_m) * 1e12)
ts = np.linspace(0, 1e-6, 20001)
q = 10e-9 * np.sin(2 * pi * 1e6 * ts)
v.check("04-08.4a", np.max(np.abs(np.gradient(q, ts))) * 1e3)
E5 = sqrt(2 * ETA0 * 1000)
v.check("04-08.5a", E5)
v.check("04-08.5b", E5 / C * 1e6)
Er, Et = fresnel(ETA0, ETA0 / 2)
v.check("04-08.6a", ETA0 / 2)
v.check("04-08.6b", Er)
v.check("04-08.6c", Er**2)
v.check("04-08.6d", Et**2 * ETA0 / (ETA0 / 2))
a7, b7, V7, I7 = 0.45e-3, 1.475e-3, 10.0, 0.2
S7 = lambda r: (V7 / (r * log(b7 / a7))) * (I7 / (2 * pi * r))
v.check("04-08.7a", S7(a7))
v.check("04-08.7b", quad(lambda r: S7(r) * 2 * pi * r, a7, b7)[0])
v.check("04-08.8a", 0.2 / (4 * pi * 0.05**2))
al9 = alpha_exact(28e9, 3.66, 0.0037)
v.check("04-08.9a", al9)
v.check("04-08.9b", NP_TO_DB * al9)
v.check("04-08.10a", 2 * pi * 1e9 * EPS0 / 5.95e7)
v.check("04-08.10b", 2 * pi * 1e9 * 81 * EPS0 / 4)
v.check("04-08.11a", 2 * pi * 10e9 * sqrt(MU0 * 4.6 * EPS0))
v.check("04-08.12a", (C * 5.9e-12 / 1e-3) ** 2)
v.check("04-08.13a", 20e-3 / 10e-3)
v.check("04-08.13b", 0.3 * 20e-3 / 1e-3)
i14 = 2 * pi * 10e6 * 1e-9 * 10
v.check("04-08.14a", i14)
v.check("04-08.14b", MU0 * i14 / (2 * pi * 0.02) * 1e6)

# ---------------------------------------------------------------- lab (analytic references the FDTD reproduces)
ErL, EtL = fresnel(ETA0, ETA0 / 2)
v.check("Lab 04-08.a", ErL)
v.check("Lab 04-08.b", EtL)
v.check("Lab 04-08.c", (1 / sqrt(MU0 * 4 * EPS0)) / C)
al_d = alpha_exact(10e9, 4.0, 0.05)
v.check("Lab 04-08.d", al_d)
al_e = quad(lambda x: pi * 5e9 * sqrt(3.92) * 0.025 / C, 0, 1)[0]      # the notebook's small-tan-delta formula, per meter
v.check("Lab 04-08.e", NP_TO_DB * al_e)
v.assert_true("formula within 0.01% of exact at tan d = 0.025", abs(al_e / alpha_exact(5e9, 3.92, 0.025) - 1) < 1e-4)
v.assert_true("small-tan-delta formula within 0.1% of exact", abs(al_d / (pi * 10e9 * 2 * 0.05 / C) - 1) < 1e-3)

sys.exit(v.finish())
