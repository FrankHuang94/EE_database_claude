#!/usr/bin/env python3
"""Verify every number in chapter 09-13 (compound and wide-bandgap semiconductors), its solutions and lab.

Independent routes:
- avalanche breakdown by integrating the electron-current continuity equation with avalanche generation
  (dJn/dx = an Jn + ap Jp, J constant) across the triangular field of a one-sided junction, as in 09-06,
  with root finding on the peak field and on the doping (the chapter used the closed ionization integral);
- the polarization charge by solving the elastic condition sigma_zz = 0 of a biaxially strained wurtzite
  film for the vertical strain (root finding) and applying the piezoelectric tensor;
- dies per wafer by the edge-loss formula, cross-checked by counting whole dies on a grid inside the circle;
- intrinsic ratios, Varshni gaps, Boltzmann gain factors and sheet resistances by direct evaluation.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-13", COURSE / "chapters" / "09-13-compound-and-wide-bandgap-semiconductors.md",
                        COURSE / "solutions" / "09-13-solutions.md",
                        COURSE / "labs" / "09-13-lab" / "README.md")

Q = C.e
E0 = C.epsilon_0 / 100
VT = C.k * 300 / C.e
EPS_SI, EPS_SIC = 11.7 * E0, 9.96 * E0

# ------------------------------------------------------------------ intrinsic
ratio = lambda dEg, T=300.0: math.exp(-dEg / (2 * C.k * T / C.e))
v.check("Ex 09-13.1a", ratio(3.26 - 1.12))
v.check("Ex 09-13.1b", ratio(3.26 - 1.12, 600))
v.check("Ex 09-13.1c", 2.1e6 / 1e10)
v.check("Ex 09-13.1d", 3.3e8 / 3.2e5)
varshni = lambda T, E0_=3.507, a=0.909e-3, b=830: E0_ - a * T ** 2 / (T + b)
v.check("T 09-13.a", varshni(300))

# ------------------------------------------------------------------ ionization models
an_si = lambda F: 3.318e5 * math.exp(-1.174e6 / F)
ap_si = lambda F: 2e6 * math.exp(-1.97e6 / F) if F < 5.3e5 else 5.6e5 * math.exp(-1.32e6 / F)
an_sic = lambda F: 1.76e8 * math.exp(-3.3e7 / F)
ap_sic = lambda F: 3.41e8 * math.exp(-2.5e7 / F)
for k_, val in (("T 09-13.b", 1.76e8), ("T 09-13.c", 3.3e7), ("T 09-13.d", 3.41e8), ("T 09-13.e", 2.5e7),
                ("T 09-13.f", 9.96)):
    v.check(k_, val)   # quoted from Burin et al. (Table XIII, [Hata04]) and the permittivity mean


def inv_mult(Em, N, eps, an, ap):
    """1/M_n from the continuity ODE dJn/dx = an Jn + ap (1 - Jn), integrated backward from Jn(W) = 1
    across the triangular field E(x) = Em (1 - x/W); breakdown when it reaches 0."""
    W = eps * Em / (Q * N)

    def rhs(x, y):
        F = max(Em * (1 - x / W), 1e3)
        return [an(F) * y[0] + ap(F) * (1 - y[0])]

    blow = lambda x, y: abs(y[0]) - 5.0       # far past breakdown the solution diverges; stop early
    blow.terminal = True
    sol = solve_ivp(rhs, [W, 0], [1.0], rtol=1e-9, atol=1e-12, max_step=W / 300, events=blow)
    return sol.y[0, -1] if sol.status == 0 else -5.0


def breakdown(N, eps, an, ap, lo, hi):
    Em = brentq(lambda E: inv_mult(E, N, eps, an, ap), lo, hi, xtol=1.0)
    W = eps * Em / (Q * N)
    return Em, W, Em * W / 2


SI = (EPS_SI, an_si, ap_si, 1.5e5, 6e5)
SIC = (EPS_SIC, an_sic, ap_sic, 1.5e6, 4e6)
Es, Ws, Vs = breakdown(1e16, *SI)
Ec_, Wc, Vc = breakdown(1e16, *SIC)
v.check("Ex 09-13.2a", Es)
v.check("Ex 09-13.2b", Ws * 1e4)
v.check("Ex 09-13.2c", Vs)
v.check("Ex 09-13.2d", Ec_)
v.check("Ex 09-13.2e", Wc * 1e4)
v.check("Ex 09-13.2f", Vc)
v.check("Ex 09-13.2g", Ec_ / Es)
v.check("Ex 09-13.2h", Vc / Vs)

mun = lambda N: 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)


def design(V, mat, Nlo, Nhi, mu=None):
    N = brentq(lambda n: breakdown(n, *mat)[2] - V, Nlo, Nhi, rtol=1e-7)
    Em, W, _ = breakdown(N, *mat)
    m = mun(N) if mu is None else mu
    return N, Em, W, m, W / (Q * m * N)


s12 = design(1200, (EPS_SI, an_si, ap_si, 1.2e5, 5e5), 5e13, 1e15)
c12 = design(1200, SIC, 1e15, 2e17, 1000)
for k_, val in zip("abcde", (s12[0], s12[1], s12[2] * 1e4, s12[3], s12[4] * 1e3)):
    v.check(f"Ex 09-13.3{k_}", val)
v.check("Ex 09-13.3f", c12[0])
v.check("Ex 09-13.3g", c12[1])
v.check("Ex 09-13.3h", c12[2] * 1e4)
v.check("Ex 09-13.3i", c12[4] * 1e3)
v.check("Ex 09-13.3j", s12[4] / c12[4])
bfom = lambda eps, mu, Ec: eps * mu * Ec ** 3
v.check("Ex 09-13.3k", bfom(EPS_SIC, 1000, c12[1]) / bfom(EPS_SI, s12[3], s12[1]))
v.check("Ex 09-13.3l", s12[4] / 0.1)
v.check("Ex 09-13.3m", c12[4] / 0.1 * 100)


# ------------------------------------------------------------------ polarization from the tensors
G = dict(a=3.189, e31=-0.35, e33=1.27, c13=106.0, c33=398.0, Psp=-0.029)
A = dict(a=3.112, e31=-0.50, e33=1.79, c13=108.0, c33=373.0, Psp=-0.081)


def film(x):
    p = {k: A[k] * x + G[k] * (1 - x) for k in G}
    exx = (G["a"] - p["a"]) / p["a"]                     # in-plane strain imposed by the GaN template
    ezz = brentq(lambda e: p["c13"] * 2 * exx + p["c33"] * e, -1, 1)   # sigma_zz = 0
    Ppz = p["e31"] * 2 * exx + p["e33"] * ezz
    sigma = G["Psp"] - (p["Psp"] + Ppz)                  # bound charge, z from GaN into AlGaN
    return p["a"], exx, p["Psp"], Ppz, sigma


a25, e25, psp25, ppz25, s25 = film(0.25)
v.check("Ex 09-13.4a", a25)
v.check("Ex 09-13.4b", e25)
v.check("Ex 09-13.4c", psp25)
v.check("Ex 09-13.4d", ppz25)
v.check("Ex 09-13.4e", s25)
v.check("Ex 09-13.4f", s25 / Q / 1e4)
v.check("Ex 09-13.4g", film(0.30)[4] / Q / 1e4)
v.check("Ex 09-13.4h", 3.9 * E0 / 2e-7 * 1.0 / Q)

# ------------------------------------------------------------------ modulation doping
v.check("Ex 09-13.5a", 1 / (Q * 1e13 * 1500))
v.check("Ex 09-13.5b", mun(2e18))
v.check("Ex 09-13.5c", 1 / (Q * 2e18 * 50e-7 * mun(2e18)))
v.check("Ex 09-13.5d", (1 / (Q * 1e13 * mun(2e18))) / (1 / (Q * 1e13 * 1500)))

# ------------------------------------------------------------------ HBT
boltz = lambda dE, T=300.0: math.exp(dE / (C.k * T / C.e))
v.check("Ex 09-13.6a", boltz(0.1))
v.check("Ex 09-13.6b", boltz(0.2))
v.check("Ex 09-13.6c", 0.1 * boltz(0.1))
v.check("Ex 09-13.6d", 0.1 * boltz(0.2))


# ------------------------------------------------------------------ dies per wafer
def gross(d, A_):
    return math.pi * (d / 2) ** 2 / A_ - math.pi * d / math.sqrt(2 * A_)


def counted(d, A_, offsets=11):
    """Best count of whole square dies of area A_ fully inside a circle of diameter d over grid offsets."""
    s = math.sqrt(A_)
    best = 0
    for ox in np.linspace(0, s, offsets, endpoint=False):
        for oy in np.linspace(0, s, offsets, endpoint=False):
            xs = np.arange(-d / 2 - s + ox, d / 2, s)
            ys = np.arange(-d / 2 - s + oy, d / 2, s)
            X, Y = np.meshgrid(xs, ys)
            corners = [(X, Y), (X + s, Y), (X, Y + s), (X + s, Y + s)]
            inside = np.all([cx ** 2 + cy ** 2 <= (d / 2) ** 2 for cx, cy in corners], axis=0)
            best = max(best, int(inside.sum()))
    return best


d150, d200 = gross(150, 25), gross(200, 25)
v.check("Ex 09-13.7a", d150)
v.check("Ex 09-13.7b", d200)
v.check("Ex 09-13.7c", d200 / d150)
v.check("Ex 09-13.7d", (200 / 150) ** 2)
v.check("Ex 09-13.7e", (300 / 200) ** 2)
v.assert_true("edge-loss formula within 3% of a direct count (150 mm, 25 mm²)",
              abs(counted(150, 25) / d150 - 1) < 0.03, f"{counted(150, 25)} vs {d150:.0f}")

# practitioner facts (quoted; see R-174)
for k_, val in (("P 09-13.a", 70), ("P 09-13.b", 60), ("P 09-13.c", 2022), ("P 09-13.d", 2024)):
    v.check(k_, val)

# ------------------------------------------------------------------ solutions
v.check("09-13.1a", ratio(3.435 - 1.12))
v.check("09-13.2a", varshni(400))
v.check("09-13.2b", varshni(77))
v.check("09-13.2c", (varshni(300) - varshni(400)) * 1e3)
Ecf, Vb3 = 2.5e6, 3300
N3 = brentq(lambda n: (EPS_SIC * Ecf / (Q * n)) * Ecf / 2 - Vb3, 1e14, 1e18)   # V = E W / 2
W3 = EPS_SIC * Ecf / (Q * N3)
v.check("09-13.3a", N3)
v.check("09-13.3b", W3 * 1e4)
v.check("09-13.3c", W3 / (Q * 1000 * N3) * 1e3)
s65 = design(650, (EPS_SI, an_si, ap_si, 1.2e5, 5e5), 5e13, 2e15)
c65 = design(650, SIC, 1e15, 3e17, 1000)
for k_, val in zip("abcde", (s65[0], s65[1], s65[2] * 1e4, s65[3], s65[4] * 1e3)):
    v.check(f"09-13.4{k_}", val)
v.check("09-13.4f", c65[0])
v.check("09-13.4g", c65[1])
v.check("09-13.4h", c65[2] * 1e4)
v.check("09-13.4i", c65[4] * 1e3)
v.check("09-13.4j", s65[4] / c65[4])
v.check("09-13.5a", math.log(c12[4] / c65[4]) / math.log(1200 / 650))
v.check("09-13.5b", math.log(s12[4] / s65[4]) / math.log(1200 / 650))
s15 = film(0.15)[4]
v.check("09-13.6a", s15)
v.check("09-13.6b", s15 / Q / 1e4)
v.check("09-13.7a", Q * 1e13 * 1e7)
v.check("09-13.7b", Q * 1e13 * 1e7 / 10)
v.check("09-13.8a", brentq(lambda d: boltz(d) - 100, 0, 1))
v.check("09-13.8b", brentq(lambda d: boltz(d, 400) - 100, 0, 1))
v.check("09-13.9a", math.exp(-3.26 / (2 * C.k * 600 / C.e)) / math.exp(-1.12 / (2 * VT)))
for (d, A_), k_ in (((200, 25), "a"), ((300, 25), "b"), ((200, 100), "d"), ((300, 100), "e")):
    v.check(f"09-13.10{k_}", gross(d, A_))
v.check("09-13.10c", gross(300, 25) / gross(200, 25))
v.check("09-13.10f", gross(300, 100) / gross(200, 100))
Cb = 9 * E0 / 20e-7
v.check("09-13.11a", Cb)
v.check("09-13.11b", Cb / Q)
v.check("09-13.11c", 1.39e13 * Q / Cb)
v.check("09-13.12a", (1.4 / d200) / (1.0 / d150))
v.check("09-13.12b", (1.4 / (d200 * 0.70)) / (1.0 / (d150 * 0.85)))
v.check("09-13.12c", 100 * brentq(lambda y: (1.4 / (d200 * y)) - (1.0 / (d150 * 0.85)), 0.1, 1))

# ------------------------------------------------------------------ lab
s6 = design(600, (EPS_SI, an_si, ap_si, 1.2e5, 5e5), 5e13, 2e15)
c6 = design(600, SIC, 1e15, 3e17, 1000)
s33 = design(3300, (EPS_SI, an_si, ap_si, 1.0e5, 5e5), 5e12, 2e14)
c33 = design(3300, SIC, 5e14, 1e17, 1000)
v.check("Lab 09-13.a", s6[4] / c6[4])
v.check("Lab 09-13.b", s33[4] / c33[4])
v.check("Lab 09-13.c", c33[1])
v.check("Lab 09-13.d", film(0.35)[4] / Q / 1e4)

v.finish()
