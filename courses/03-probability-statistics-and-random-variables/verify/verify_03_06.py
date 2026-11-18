#!/usr/bin/env python3
"""Verify every number published in chapter 03-06, its solutions and its lab handout.

Noise powers are recomputed by integrating densities numerically (not from the closed forms),
autocorrelation-PSD pairs by numerical Fourier integrals, the variance of a time average by its
double integral, and the NRZ spectrum fractions by integrating sinc^2.
"""
from __future__ import annotations

import math
import sys
from math import exp, log, log10, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.stats import chi2, norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C = HERE.parent
v = Verifier.from_files("03-06", C / "chapters" / "03-06-random-processes-preview.md",
                        C / "solutions" / "03-06-solutions.md", C / "labs" / "03-06-lab" / "README.md")
k = 1.380649e-23
q = 1.602176634e-19
INF = np.inf


def dbm(watts):
    return 10 * log10(watts / 1e-3)


def band_power(density_sq, f1, f2):
    """Integrate a one-sided power density over [f1, f2] on a log grid (robust for 1/f)."""
    return quad(lambda u: density_sq(exp(u)) * exp(u), log(f1), log(f2), limit=200)[0]


def var_time_average(sigma2, tc, T):
    """(2/T) * integral_0^T (1 - tau/T) sigma^2 e^{-tau/tc} d tau, numerically."""
    # substitute u = tau/tc so the integrand is not a narrow spike when T >> tc
    return 2 / T * tc * quad(lambda u: (1 - u * tc / T) * sigma2 * exp(-u), 0, T / tc, limit=400)[0]


def lorentzian(f, sigma2, tc):
    return 4 * sigma2 * tc / (1 + (2 * pi * f * tc) ** 2)


# ---------------------------------------------------------------- theory cross-checks
# Wiener-Khinchin for the exponential pair: one-sided G(f) = 2 * integral R(tau) e^{-j2 pi f tau}
for f in (0.0, 50.0, 300.0):
    two_sided = 2 * quad(lambda tau: exp(-tau / 1e-3) * math.cos(2 * pi * f * tau), 0, 0.05, limit=400)[0]
    v.assert_true(f"Lorentzian is the transform of e^(-|tau|/tc) at {f} Hz", abs(2 * two_sided - lorentzian(f, 1, 1e-3)) < 1e-9)
v.assert_true("Lorentzian integrates to the total power",
              abs(quad(lambda f: lorentzian(f, 1, 1e-3), 0, INF, limit=200)[0] - 1) < 1e-6)
# RC noise bandwidth equals (pi/2) f3dB, and 4kTR times it equals kT/C
R, Cc, T = 1e4, 1e-11, 300.0
f3 = 1 / (2 * pi * R * Cc)
bn = f3 * quad(lambda x: 1 / (1 + x * x), 0, INF)[0]     # integrate in units of f3
v.assert_true("noise bandwidth of RC is 1/(4RC)", abs(bn - 1 / (4 * R * Cc)) / bn < 1e-9)
v.assert_true("4kTR x noise bandwidth = kT/C", abs(4 * k * T * R * bn - k * T / Cc) / (k * T / Cc) < 1e-9)
# shot noise: Var(qN/T) for Poisson N divided by the 1/(2T) bandwidth equals 2qI
I, Tw = 1e-3, 1e-6
v.assert_true("shot-noise density from Poisson counting", abs((q * q * (I * Tw / q) / Tw**2) / (1 / (2 * Tw)) - 2 * q * I) < 1e-30)

# ---------------------------------------------------------------- theory keys
kT0 = k * 290
v.check("T 03-06.a", kT0)
v.check("T 03-06.b", sqrt(4 * k * 290 * 50) * 1e9)
v.check("T 03-06.c", sqrt(k * 300 / 1e-12) * 1e6)
v.check("T 03-06.d", bn / f3)
v.check("T 03-06.e", sqrt(band_power(lambda f: (5.2e-9) ** 2, 0.1, 10)) * 1e9)
v.check("T 03-06.f", 10 * log10(1e6))

# ---------------------------------------------------------------- Example 03-06.1
A, f0 = 2.0, 1e6
Rx = lambda tau: quad(lambda th: A * math.cos(th) * A * math.cos(2 * pi * f0 * tau + th) / (2 * pi), 0, 2 * pi)[0]  # noqa: E731
v.check("Ex 03-06.1a", Rx(0))
v.check("Ex 03-06.1b", Rx(250e-9))
v.check("Ex 03-06.1c", Rx(1 / 6 * 1e-6))
v.check("Ex 03-06.1d", A**2 / 4)
for th in (0.3, 2.0):
    tavg = quad(lambda t: (A * math.cos(2 * pi * f0 * t + th)) ** 2, 0, 1 / f0)[0] * f0
    v.assert_true(f"time-averaged power equals ensemble power (phase {th})", abs(tavg - Rx(0)) < 1e-9)

# ---------------------------------------------------------------- Example 03-06.2
v.check("Ex 03-06.2a", 1.0**2 + 0.1**2)
v.check("Ex 03-06.2b", 1.0**2)
v.check("Ex 03-06.2c", 2 * norm.sf(2))

# ---------------------------------------------------------------- Example 03-06.3
e1k = sqrt(4 * k * 300 * 1e3)
v.check("Ex 03-06.3a", e1k * 1e9)
v.check("Ex 03-06.3b", sqrt(band_power(lambda f: e1k**2, 1, 2e7 + 1)) * 1e6)
v.check("Ex 03-06.3c", dbm(kT0))
v.check("Ex 03-06.3d", 10 * log10(2e7))
floor = dbm(kT0 * 2e7)
v.check("Ex 03-06.3e", floor)
v.check("Ex 03-06.3f", floor + 7)
v.check("Ex 03-06.3g", floor + 7 + 10)

# ---------------------------------------------------------------- Example 03-06.4
v.check("Ex 03-06.4a", f3 / 1e6)
v.check("Ex 03-06.4b", bn / 1e6)
v.check("Ex 03-06.4c", sqrt(4 * k * T * R * bn) * 1e6)
v.check("Ex 03-06.4d", sqrt(4 * k * T * R) * 1e9)
v.check("Ex 03-06.4e", R * Cc * 1e9)
v.check("Ex 03-06.4f", exp(-50e-9 / (R * Cc)))

# ---------------------------------------------------------------- Example 03-06.5
ish = sqrt(2 * q * 1e-3)
v.check("Ex 03-06.5a", ish * 1e12)
v.check("Ex 03-06.5b", ish * sqrt(1e9) * 1e6)
v.check("Ex 03-06.5c", 1e-3 / (ish * sqrt(1e9)))
v.check("Ex 03-06.5d", 20 * log10(1e-3 / (ish * sqrt(1e9))))
v.check("Ex 03-06.5e", sqrt(4 * k * 300 / 1e3) * 1e12)
v.check("Ex 03-06.5f", 4 * k * 300 / 1e3 / (2 * q) * 1e6)

# ---------------------------------------------------------------- Example 03-06.6
s6, tc6, T6 = 1e-3, 1e-3, 1.0
v.check("Ex 03-06.6a", sqrt(var_time_average(s6**2, tc6, T6)) * 1e6)
v.check("Ex 03-06.6b", sqrt(2 * s6**2 * tc6 / T6) * 1e6)
v.check("Ex 03-06.6c", T6 / (2 * tc6))
v.check("Ex 03-06.6d", s6 / sqrt(1e5) * 1e6)

# ---------------------------------------------------------------- Example 03-06.7
ew, fc = 10e-9, 100.0
flick = lambda f: ew**2 * (1 + fc / f)  # noqa: E731
v.check("Ex 03-06.7a", sqrt(band_power(flick, 0.1, 10)) * 1e9)
v.check("Ex 03-06.7b", sqrt(band_power(lambda f: ew**2, 0.1, 10)) * 1e9)
v.check("Ex 03-06.7c", sqrt(band_power(flick, 1e-3, 10)) * 1e9)
v.check("Ex 03-06.7d", sqrt(band_power(lambda f: ew**2 * fc / f, 1e-3, 1e-2)) * 1e9)
v.check("Ex 03-06.7e", sqrt(band_power(lambda f: (5.2e-9) ** 2, 0.1, 10)) * 1e9)

# ================================================================ solutions
mean1 = quad(lambda th: math.cos(pi / 2 + th) / pi, 0, pi)[0]
v.check("03-06.1a", mean1)

v.check("03-06.2a", 4 + 1)
v.check("03-06.2b", 1)
v.check("03-06.2c", 4)
v.check("03-06.2d", exp(-1))

v.check("03-06.3a", math.ceil((norm.isf(0.025) / 0.1) ** 2 / 2 + 1))

e50 = sqrt(4 * k * 290 * 50)
v.check("03-06.4a", e50 * 1e9)
v.check("03-06.4b", e50 * sqrt(1e6) * 1e6)
v.check("03-06.4c", e50 * sqrt(1e9) * 1e6)
v.check("03-06.4d", dbm(kT0 * 1e6))
v.check("03-06.4e", dbm(kT0 * 1e9))

v.check("03-06.5c", 10 * log10(2e6))
v.check("03-06.5a", dbm(kT0 * 2e6) + 2)
v.check("03-06.5b", dbm(kT0 * 2e6) + 2 + 6)

kT300 = k * 300
for bits, (qa, ca) in ((12, ("a", "b")), (16, ("c", "d"))):
    qn = (1 / 2**bits) / sqrt(12)
    v.check(f"03-06.6{qa}", qn * 1e6)
    v.check(f"03-06.6{ca}", kT300 / qn**2 * 1e12)

bn7 = 1e4 * quad(lambda x: 1 / (1 + x * x), 0, INF)[0]
v.check("03-06.7a", bn7 / 1e3)
v.check("03-06.7b", 10e-9 * sqrt(bn7) * 1e6)

i8 = sqrt(2 * q * 1e-5 * 1e8)
v.check("03-06.8a", i8 * 1e9)
v.check("03-06.8b", 1e-5 / i8)
v.check("03-06.8c", 20 * log10(1e-5 / i8))

tot9 = e50**2 + (1e-9) ** 2 + (2e-12 * 50) ** 2
v.check("03-06.9a", sqrt(tot9) * 1e9)
v.check("03-06.9b", tot9 / e50**2)
v.check("03-06.9c", 10 * log10(tot9 / e50**2))

v.check("03-06.10a", sqrt(2 * (2e-3) ** 2 * 0.01 / 10) * 1e6)
v.check("03-06.10b", 10 / (2 * 0.01))
v.check("03-06.10c", 2e-3 / sqrt(1e4) * 1e6)

fc11 = 1 / (2 * pi * 1e-3)
v.check("03-06.11a", fc11)
v.check("03-06.11b", sqrt(lorentzian(0, 1e-6, 1e-3)) * 1e6)
v.check("03-06.11c", quad(lambda f: lorentzian(f, 1, 1e-3), 0, fc11)[0])

v.check("03-06.12a", sqrt(band_power(lambda f: (5e-9) ** 2 * (1 + 10 / f), 0.1, 10)) * 1e9)
v.check("03-06.12b", sqrt(band_power(lambda f: (5.2e-9) ** 2, 0.1, 10)) * 1e9)

v.check("03-06.13a", 1 * sqrt(100e-6 / 1e-6))
v.check("03-06.13b", 1 * sqrt(1e-3 / 1e-6))

sinc2 = lambda x: 1.0 if x == 0 else (math.sin(pi * x) / (pi * x)) ** 2  # noqa: E731
tot14 = 2 * quad(sinc2, 0, 200, limit=2000)[0]        # whole spectrum (should be 1)
v.assert_true("sinc^2 integrates to 1", abs(tot14 - 1) < 1e-2)
v.check("03-06.14a", 2 * quad(sinc2, 0, 0.5)[0])
v.check("03-06.14b", 2 * quad(sinc2, 0, 1)[0])
v.check("03-06.14c", 10)

lo15, hi15 = chi2.ppf(0.025, 32), chi2.ppf(0.975, 32)
v.check("03-06.15a", lo15)
v.check("03-06.15b", hi15)
v.check("03-06.15c", 32 / hi15)
v.check("03-06.15d", 32 / lo15)
v.check("03-06.15e", 10 * log10(32 / hi15))
v.check("03-06.15f", 10 * log10(32 / lo15))
kmin = next(K for K in range(2, 1000) if 10 * log10(2 * K / chi2.ppf(0.025, 2 * K)) <= 1)
v.check("03-06.15g", kmin)
v.check("03-06.15h", 10 * log10(2 * kmin / chi2.ppf(0.975, 2 * kmin)))

es = sqrt(4 * k * 300 * 1e3)
dA = lambda f: es**2 + (5e-9) ** 2 * (1 + 10 / f)  # noqa: E731
dB = lambda f: es**2 + (8e-9) ** 2  # noqa: E731
nA, nB = sqrt(band_power(dA, 0.1, 100)), sqrt(band_power(dB, 0.1, 100))
v.check("03-06.16a", es * 1e9)
v.check("03-06.16b", nA * 1e9)
v.check("03-06.16c", nB * 1e9)
v.check("03-06.16d", 100 * nA * 1e6)
v.check("03-06.16e", 100 * nB * 1e6)
v.check("03-06.16f", sqrt(band_power(dA, 0.01, 1)) * 1e9)
v.check("03-06.16g", sqrt(band_power(dB, 0.01, 1)) * 1e9)

# ================================================================ lab handout
v.check("Lab 03-06.a", sqrt(k * 300 / 1e-11) * 1e6)
v.check("Lab 03-06.b", fc11)
v.check("Lab 03-06.c", exp(-1))
v.check("Lab 03-06.d", 1e-9 / q * 1e-9)
v.check("Lab 03-06.e", 2 * q * 1e-9 / (2 * 1e-9))
v.check("Lab 03-06.f", sqrt(2 * 1e-3 / 0.01))
v.check("Lab 03-06.g", sqrt(2 * 1e-3 / 0.1))
v.check("Lab 03-06.h", sqrt(var_time_average(1, 1e-3, 0.01)))
v.check("Lab 03-06.i", 2 * norm.sf(2))

sys.exit(v.finish())
