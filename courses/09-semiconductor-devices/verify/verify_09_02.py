#!/usr/bin/env python3
"""Verify every number in chapter 09-02 (carriers, doping and the Fermi level), its solutions and lab.

Independent routes:
- effective densities of states by integrating g(E) exp(-(E - E_C)/kT) over the band numerically, and the
  distribution's peak, mean and tail by numerical maximization and quadrature;
- carrier densities by solving charge neutrality for the Fermi level with a root finder (never with the
  closed-form quadratic): with n = n_i exp((E_F - E_i)/kT) for the course's n_i convention, with full
  Fermi-Dirac integrals for degenerate material, and with the donor and acceptor occupation statistics for
  partial ionization;
- intrinsic levels by solving n = p for E_F; hydrogenic donor values from the CODATA constants directly;
- temperatures by root finding on the full model; dopant statistics from the Poisson distribution, checked
  against random sampling.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import poisson

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-02", COURSE / "chapters" / "09-02-carriers-doping-fermi-level.md",
                        COURSE / "solutions" / "09-02-solutions.md",
                        COURSE / "labs" / "09-02-lab" / "README.md")

K = C.k / C.e                       # eV/K
KT = K * 300
NC0, NV0, EG, NI0 = 3.2e19, 1.8e19, 1.12, 1.0e10
HBAR, M0, Q, H = C.hbar, C.m_e, C.e, C.h


def F12(eta):
    return 2 / math.sqrt(math.pi) * quad(lambda x: math.sqrt(x) / (1 + math.exp(min(x - eta, 700))),
                                         0, max(eta, 0) + 60, limit=200, epsabs=0, epsrel=1e-11)[0]


def g_band(dE_eV, m):
    """Density of states per cm^3 per eV at dE above the band edge, from the k-space volume derivative."""
    def count(E):              # states per m^3 below E (two spins, sphere in k-space)
        k = math.sqrt(2 * m * M0 * E * Q) / HBAR
        return 2 * (4 / 3) * math.pi * k**3 / (2 * math.pi) ** 3
    h = dE_eV * 1e-6
    return (count(dE_eV + h) - count(dE_eV - h)) / (2 * h) / 1e6


def N_eff_numeric(m, T=300.0):
    kT = K * T
    return quad(lambda x: g_band(x * kT, m) * math.exp(-x) * kT, 0, 80, limit=200)[0]


def ef_boltz(ND=0.0, NA=0.0, ni=NI0, T=300.0):
    """E_F - E_i (eV) from neutrality with full ionization and n = n_i exp(+u/kT), p = n_i exp(-u/kT)."""
    kT = K * T
    def charge(u):
        return ni * math.exp(-u / kT) + ND - ni * math.exp(u / kT) - NA
    u = brentq(charge, -1.0, 1.0, xtol=1e-14)
    return u, ni * math.exp(u / kT), ni * math.exp(-u / kT)


def intrinsic_level(NC, NV, Eg, T=300.0):
    """E_F (from E_V) where n = p, with Fermi-Dirac carriers."""
    kT = K * T
    f = lambda EF: NC * F12((EF - Eg) / kT) - NV * F12(-EF / kT)
    EF = brentq(f, 0.0, Eg, xtol=1e-14)
    return EF, NC * F12((EF - Eg) / kT)


def partial_n(ND, dE, T, NA=0.0, NCref=NC0, fd=False):
    """Solve n + N_A = N_D+ (holes neglected) for n by root finding on u = E_F - E_C."""
    kT = K * T
    NC = NCref * (T / 300) ** 1.5
    nfun = (lambda u: NC * F12(u / kT)) if fd else (lambda u: NC * math.exp(u / kT))
    def charge(u):
        return ND / (1 + 2 * math.exp(min((u + dE) / kT, 700))) - NA - nfun(u)
    u = brentq(charge, -1.5, 0.3, xtol=1e-15)
    n = nfun(u)
    return n, u, n + NA


def partial_p(NA, dE, T, NVref=NV0):
    kT = K * T
    NV = NVref * (T / 300) ** 1.5
    def charge(w):             # w = E_V - E_F (negative when E_F is above E_V)
        p = NV * math.exp(w / kT)
        return p - NA / (1 + 4 * math.exp(min((dE + w) / kT, 700)))
    w = brentq(charge, -1.5, 0.3, xtol=1e-15)
    return NV * math.exp(w / kT)


def eg_T(T):
    return 1.17 - 4.73e-4 * T**2 / (T + 636)


def ni_T(T):
    return NI0 * (T / 300) ** 1.5 * math.exp(eg_T(300) / (2 * K * 300) - eg_T(T) / (2 * K * T))


def eta_of(r):
    return brentq(lambda e: F12(e) - r, -20, 20, xtol=1e-12)


# ================================================================= chapter
# Example 1
kT_J = C.k * 300
v.check("Ex 09-02.1c", kT_J)
gkT = g_band(KT, 1.18)
v.check("Ex 09-02.1a", gkT)
v.check("Ex 09-02.1b", gkT * 1e6 / Q)
v.check("Ex 09-02.1d", N_eff_numeric(1.18))
v.check("Ex 09-02.1e", N_eff_numeric(0.81))
peak = minimize_scalar(lambda x: -math.sqrt(x) * math.exp(-x), bounds=(1e-6, 5), method="bounded",
                       options={"xatol": 1e-10}).x
v.check("Ex 09-02.1f", peak * KT * 1e3)
num = quad(lambda x: x**1.5 * math.exp(-x), 0, 80)[0]
den = quad(lambda x: x**0.5 * math.exp(-x), 0, 80)[0]
v.check("Ex 09-02.1g", num / den * KT * 1e3)
v.check("Ex 09-02.1h", quad(lambda x: x**0.5 * math.exp(-x), 3, 80)[0] / den)
slice_states = quad(lambda x: g_band(x, 1.18), 0, KT)[0]
v.assert_true(abs(slice_states / (gkT * KT) - 1) < 0.35, "the kT slice estimate g(kT)*kT is the right order")
v.check("Ex 09-02.1i", gkT * KT)
v.check("Ex 09-02.1j", 1e16 / (gkT * KT))
v.check("Ex 09-02.1k", (gkT * KT) / 1e16)

# Example 2: intrinsic levels from n = p with Fermi-Dirac carriers
EFi, ni_si = intrinsic_level(NC0, NV0, EG)
v.check("Ex 09-02.2a", math.exp(-EG / (2 * KT)))
v.check("Ex 09-02.2b", math.sqrt(NC0 * NV0))
v.check("Ex 09-02.2c", ni_si)
v.check("Ex 09-02.2d", (9.65e9 - ni_si) / 9.65e9 * 100)
v.check("Ex 09-02.2e", (EFi - EG / 2) * 1e3)
_, ni_ge = intrinsic_level(1.04e19, 6.0e18, 0.66)
EFg, ni_gaas = intrinsic_level(4.7e17, 7.0e18, 1.42)
v.check("Ex 09-02.2f", ni_ge)
v.check("Ex 09-02.2g", ni_gaas)
v.check("Ex 09-02.2h", (EFg - 1.42 / 2) * 1e3)
v.check("Ex 09-02.2i", 1 / (Q * NI0 * (1400 + 450)))
v.check("Ex 09-02.2j", round(ni_ge / ni_si, -3))
v.check("Ex 09-02.2k", round(ni_si / ni_gaas, -2))
v.check("Ex 09-02.2l", math.exp(0.1 / (2 * KT)))

# Example 3: hydrogen model from constants
eps0 = C.epsilon_0


def hydrogenic(m_rel, eps_r):
    E = m_rel * M0 * Q**4 / (8 * (eps_r * eps0) ** 2 * H**2) / Q
    a = eps_r * eps0 * H**2 / (math.pi * m_rel * M0 * Q**2)
    return E, a


E_d, a_d = hydrogenic(0.26, 11.7)
E_a, a_a = hydrogenic(0.39, 11.7)
v.check("Ex 09-02.3a", E_d * 1e3)
v.check("Ex 09-02.3b", a_d * 1e9)
v.check("Ex 09-02.3c", E_a * 1e3)
v.check("Ex 09-02.3d", a_a * 1e9)
v.check("Ex 09-02.3e", a_d / 0.5431e-9)
vol = 4 / 3 * math.pi * (a_d * 100) ** 3
v.check("Ex 09-02.3f", vol)
v.check("Ex 09-02.3g", round(vol * 8 / (5.431e-8) ** 3, -1))
v.check("Ex 09-02.3h", 2 * a_d * 1e9)
v.check("Ex 09-02.3i", (2 * a_d * 100) ** -3)
E_H, a_H = hydrogenic(1.0, 1.0)
v.check("T 09-02.i", E_H)
v.check("T 09-02.j", a_H * 1e9)

# Example 4: neutrality with the course n_i
u, n, p = ef_boltz(ND=1e16)
v.check("Ex 09-02.4a", p)
v.check("Ex 09-02.4c", u)
EC_Ei_nc = KT * math.log(NC0 / NI0)
v.check("Ex 09-02.4d", EC_Ei_nc)
v.check("Ex 09-02.4b", EC_Ei_nc - u)
v.assert_true(abs((EC_Ei_nc - u) - KT * math.log(NC0 / n)) < 1e-9, "E_C - E_F from N_C agrees with the n_i route")
EC_Ei_gap = EG / 2 - (EFi - EG / 2)
v.check("Ex 09-02.4e", EC_Ei_gap)
v.check("Ex 09-02.4f", EC_Ei_gap - u)
v.check("Ex 09-02.4g", (EC_Ei_gap - EC_Ei_nc) * 1e3)
u, n, p = ef_boltz(ND=1e16, NA=4e15)
v.check("Ex 09-02.4h", p)
v.check("Ex 09-02.4i", u)
u, n, p = ef_boltz(NA=1e17)
v.check("Ex 09-02.4j", n)
v.check("Ex 09-02.4k", KT * math.log(NV0 / p))
v.check("Ex 09-02.4l", -u)
u, n, p = ef_boltz(ND=2e10)
v.check("Ex 09-02.4m", n)
v.check("Ex 09-02.4n", p)
v.check("Ex 09-02.4o", u * 1e3)

# Example 5: partial ionization by root finding
v.check("Ex 09-02.5a", math.exp(0.045 / KT))
a300 = 2 * math.exp(0.045 / KT) / NC0
v.check("Ex 09-02.5b", a300)
v.check("Ex 09-02.5c", 4 * a300 * 1e16)
n300, u300, _ = partial_n(1e16, 0.045, 300)
v.check("Ex 09-02.5d", n300)
v.check("Ex 09-02.5e", n300 / 1e16 * 100)
v.check("Ex 09-02.5f", -u300)
kT77 = K * 77
NC77 = NC0 * (77 / 300) ** 1.5
v.check("Ex 09-02.5g", kT77 * 1e3)
v.check("Ex 09-02.5h", NC77)
v.check("Ex 09-02.5i", math.exp(0.045 / kT77))
a77 = 2 * math.exp(0.045 / kT77) / NC77
v.check("Ex 09-02.5j", a77)
v.check("Ex 09-02.5k", 4 * a77 * 1e16)
n77, u77, _ = partial_n(1e16, 0.045, 77)
v.check("Ex 09-02.5l", n77)
v.check("Ex 09-02.5m", n77 / 1e16 * 100)
v.check("Ex 09-02.5n", -u77 * 1e3)
v.check("Ex 09-02.5o", NC0 / NC77)

# Example 6: the temperature window
v.check("Ex 09-02.6a", ni_T(400))
v.check("Ex 09-02.6b", ni_T(400) / NI0)
v.check("Ex 09-02.6c", (4 / 3) ** 1.5)
v.check("Ex 09-02.6d", ni_T(400) / NI0 / (4 / 3) ** 1.5)
v.check("Ex 09-02.6e", K * 400 * 1e3)
T01 = brentq(lambda T: ni_T(T) - 1e14, 300, 900)
T1 = brentq(lambda T: ni_T(T) - 1e15, 300, 900)
v.check("Ex 09-02.6f", T01)
v.check("Ex 09-02.6g", T1)
for key, T in (("Ex 09-02.6h", T01), ("Ex 09-02.6i", T1)):
    _, n, p = ef_boltz(ND=1e15, ni=ni_T(T), T=T)
    v.check(key, n / 1e15)
_, n, p = ef_boltz(ND=1e15, ni=ni_T(T1), T=T1)
v.check("Ex 09-02.6j", p / 1e15 * 100)
T50 = brentq(lambda T: partial_n(1e15, 0.045, T)[0] - 0.5e15, 20, 200)
v.check("Ex 09-02.6k", T50)
v.check("Ex 09-02.6l", round(T01 - 273.15, -2))

# Example 7: degenerate doping
v.check("Ex 09-02.7a", KT * math.log(NC0 / 1e19) * 1e3)
r19 = 1e19 / NC0
v.check("Ex 09-02.7b", r19)
e19 = eta_of(r19)
v.check("Ex 09-02.7c", e19)
v.check("Ex 09-02.7d", -e19 * KT * 1e3)
v.check("Ex 09-02.7e", math.log(r19) + r19 / math.sqrt(8))
v.check("Ex 09-02.7f", math.log(r19))
v.check("Ex 09-02.7g", r19 / math.sqrt(8))
v.check("Ex 09-02.7h", (KT * math.log(NC0 / 1e19) + e19 * KT) * 1e3)
r20 = 1e20 / NC0
v.check("Ex 09-02.7i", r20)
e20 = eta_of(r20)
v.check("Ex 09-02.7j", e20)
v.check("Ex 09-02.7k", e20 * KT * 1e3)
v.check("Ex 09-02.7l", KT * math.log(r20) * 1e3)
bgn = 3.5e-8 * (1e19) ** (1 / 3)
v.check("Ex 09-02.7m", bgn * 1e3)
v.check("Ex 09-02.7n", math.exp(bgn / KT))

# Theory rows
v.check("T 09-02.a", (math.exp(-3) * (1 + math.exp(3)) - 1) * 100)
v.check("T 09-02.b", KT * math.log(10) * 1e3)
v.check("T 09-02.c", (math.exp(0.005 / KT) - 1) * 100)
v.check("T 09-02.d", (NI0 - ni_si) / NI0 * 100)
v.check("T 09-02.e", 1 / (Q * NI0 * 1850) * 0.1 / 0.01 / 1e6)
v.check("T 09-02.f", brentq(lambda N: KT * math.log(NC0 / N) - 3 * KT, 1e15, 1e19))
_, n, p = ef_boltz(ND=1e16)
v.check("T 09-02.g", n / p)
v.check("T 09-02.h", (4 / 3) ** 2.54 * math.exp(6726 * (1 / 300 - 1 / 400)))
v.check("T 09-02.k", 8 / (5.431e-8) ** 3 / 1e6)
v.check("T 09-02.l", 8 / (5.431e-8) ** 3 / 1e6 / NI0)
v.check("T 09-02.m", 8 / (5.431e-8) ** 3 / NI0)
v.check("T 09-02.n", (4 / 3) ** 1.5 * math.exp(1.12 / (2 * K) * (1 / 300 - 1 / 400)))

# Practitioner rows
v.check("P 09-02.a", (1.45 / 0.965) ** 2)
mean = 1e18 * 20e-7 * 20e-7 * 10e-7
v.check("P 09-02.b", mean)
v.check("P 09-02.c", poisson(mean).std())
v.check("P 09-02.d", poisson(mean).std() / mean * 100)

# ================================================================= solutions
pref = N_eff_numeric(1.0)
v.check("09-02.1a", N_eff_numeric(0.067))
v.check("09-02.1b", N_eff_numeric(0.063))
v.check("09-02.1c", (4.7e17 - N_eff_numeric(0.067)) / N_eff_numeric(0.067) * 100)
v.check("09-02.1d", NC0 * (77 / 300) ** 1.5)
v.check("09-02.1e", NC0 * (400 / 300) ** 1.5)

fd = lambda x: 1 / (1 + math.exp(x))
for key, x in (("09-02.2a", 1), ("09-02.2b", 3), ("09-02.2c", 10)):
    v.check(key, fd(x))
for key, x in (("09-02.2d", 1), ("09-02.2e", 3), ("09-02.2f", 10)):
    v.check(key, (math.exp(-x) / fd(x) - 1) * 100)
v.check("09-02.2g", -0.10 / KT)
v.check("09-02.2h", 1 - fd(-0.10 / KT))

u, n, p = ef_boltz(ND=5e15)
v.check("09-02.3a", p)
v.check("09-02.3b", u)
v.check("09-02.3c", KT * math.log(NC0 / n))

p4 = NV0 * math.exp(-0.20 / KT)
u, n, p = ef_boltz(NA=p4)
v.check("09-02.4a", p)
v.check("09-02.4b", n)
v.check("09-02.4c", -u)

u, n, p = ef_boltz(ND=5e16, NA=3e16)
v.assert_true(n > p, "counter-doped region is n-type")
v.check("09-02.5a", p)
v.check("09-02.5b", u)
v.check("09-02.5c", 5e16 + 3e16)

v.check("09-02.6a", eg_T(250))
v.check("09-02.6b", eg_T(350))
v.check("09-02.6c", K * 250 * 1e3)
v.check("09-02.6d", K * 350 * 1e3)
v.check("09-02.6e", ni_T(250))
v.check("09-02.6f", ni_T(350))
v.check("09-02.6g", ni_T(350) / ni_T(250))

v.check("09-02.7a", NI0**2 / 2.0e15)
v.check("09-02.7b", 2.1e15 * 1.0e14 / NI0**2)
v.check("09-02.7c", (2.1e15 - 2.0e15) / 2.0e15 * 100)
v.check("09-02.7d", 1.0e14 / (NI0**2 / 2.0e15))

E8, a8 = hydrogenic(0.067, 12.9)
v.check("09-02.8a", E8 * 1e3)
v.check("09-02.8b", a8 * 1e9)
N8 = (2 * a8 * 100) ** -3
v.check("09-02.8c", N8)
v.check("09-02.8d", E8 / K)
v.check("09-02.8e", ((2 * a_d * 100) ** -3) / N8)

v.check("09-02.9a", math.exp(0.045 / KT))
v.check("09-02.9b", 4 * math.exp(0.045 / KT) / NV0)
pB = partial_p(1e16, 0.045, 300)
v.check("09-02.9c", pB)
v.check("09-02.9d", pB / 1e16 * 100)
v.check("09-02.9e", math.exp(0.157 / KT))
v.check("09-02.9f", 4 * math.exp(0.157 / KT) / NV0)
pIn = partial_p(1e16, 0.157, 300)
v.check("09-02.9g", pIn)
v.check("09-02.9h", pIn / 1e16 * 100)

kT600 = K * 600
v.check("09-02.10b", kT600 * 1e3)
EF600, _ = intrinsic_level(NC0 * 8, NV0 * 8, eg_T(600), T=600)   # (600/300)^1.5 = 2.83; ratio is what matters
v.check("09-02.10a", (kT600 / 2) * math.log(NV0 / NC0) * 1e3)
v.assert_true(abs((EF600 - eg_T(600) / 2) - (kT600 / 2) * math.log(NV0 / NC0)) < 2e-3,
              "intrinsic level from n = p matches the logarithmic formula at 600 K")
ni600 = ni_T(600)
v.check("09-02.10c", ni600)
u, n, p = ef_boltz(ND=1e15, ni=ni600, T=600)
v.check("09-02.10d", n)
v.check("09-02.10e", p)
v.check("09-02.10f", u * 1e3)
v.check("09-02.10g", (n / p - 1) * 100)

for (ka, kb), T in ((("09-02.11a", "09-02.11b"), 310), (("09-02.11c", "09-02.11d"), 350), (("09-02.11e", "09-02.11f"), 400)):
    r = ni_T(T) / NI0
    v.check(ka, r)
    v.check(kb, r * r)
v.check("09-02.11g", brentq(lambda T: ni_T(T) / NI0 - 2, 300, 340) - 300)
v.check("09-02.11h", brentq(lambda T: (ni_T(T) / NI0) ** 2 - 2, 300, 340) - 300)

v.check("09-02.12a", KT * math.log(NV0 / 1e19) * 1e3)
r12 = 1e19 / NV0
v.check("09-02.12b", r12)
e12 = eta_of(r12)
v.check("09-02.12c", e12)
v.check("09-02.12d", -e12 * KT * 1e3)
v.check("09-02.12e", math.log(r12) + r12 / math.sqrt(8))
v.check("09-02.12f", (KT * math.log(NV0 / 1e19) + e12 * KT) * 1e3)

for (ka, kb), T in ((("09-02.13a", "09-02.13b"), 423), (("09-02.13c", "09-02.13d"), 473)):
    v.check(ka, ni_T(T))
    v.check(kb, brentq(lambda N: ef_boltz(ND=N, ni=ni_T(T), T=T)[1] / N - 1.0099019513592785, 1e12, 1e17))

V1 = 30e-7 * 30e-7 * 10e-7
v.check("09-02.14a", V1)
d1 = poisson(1e18 * V1)
v.check("09-02.14b", d1.mean())
v.check("09-02.14c", d1.std())
v.check("09-02.14d", d1.std() / d1.mean() * 100)
V2 = 7e-7 * 40e-7 * 20e-7
v.check("09-02.14e", V2)
d2 = poisson(1e17 * V2)
v.check("09-02.14f", d2.mean())
v.check("09-02.14g", d2.pmf(0))
v.check("09-02.14h", d2.sf(1))
v.check("09-02.14i", brentq(lambda N: poisson(N * V1).std() / (N * V1) - 0.1, 1e17, 1e21))
rng = np.random.default_rng(7)
v.assert_true(abs(np.mean(rng.poisson(1e17 * V2, 400_000) == 0) - d2.pmf(0)) < 0.003, "sampling matches P(0)")

nc, uc, ndp = partial_n(1e16, 0.045, 77, NA=1e15)
v.check("09-02.15a", -uc * 1e3)
v.check("09-02.15b", nc)
v.check("09-02.15c", ndp)
v.check("09-02.15d", ndp / 1e16 * 100)
v.check("09-02.15e", (n77 - nc) / n77 * 100)
v.check("09-02.15f", (-uc + u77) * 1e3)
EA_above_EF = (EG - (-uc)) - 0.045           # E_F - E_A, eV
v.assert_true(1 / (1 + 4 * math.exp(-EA_above_EF / kT77)) > 1 - 1e-12, "boron fully ionized at 77 K in the compensated sample")

# ================================================================= lab
eta5 = brentq(lambda e: F12(e) / math.exp(e) - 0.95, -10, 5)
v.check("Lab 09-02.a", eta5)
v.check("Lab 09-02.b", NC0 * F12(eta5))
n17, _, _ = partial_n(1e17, 0.045, 300, fd=True)
v.check("Lab 09-02.c", n17 / 1e17 * 100)
v.check("Lab 09-02.d", brentq(lambda T: partial_n(1e17, 0.045, T, fd=True)[2] / 1e17 - 0.5, 40, 300))
v.check("Lab 09-02.e", brentq(lambda T: partial_n(1e17, 0.045, T)[2] / 1e17 - 0.5, 40, 300))
d3 = poisson(1e18 * V2)
v.check("Lab 09-02.f", d3.mean())
v.check("Lab 09-02.g", d3.std())
v.check("Lab 09-02.h", d3.std() / d3.mean() * 100)

v.finish()
