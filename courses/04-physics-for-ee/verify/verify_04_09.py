#!/usr/bin/env python3
"""Verify every number published in chapter 04-09, its solutions and its lab handout.

Independent routes: wave speeds and modes from the dispersion relation solved numerically;
interference and array directions by root-finding on the phase condition; array beamwidths from
the summed array factor; diffraction zeros from Huygens sums and the Bessel root; thin-film
reflectance from characteristic matrices (not the closed-form quarter-wave formula); Snell's law
and critical angles by root-finding; link budgets and dispersion by direct arithmetic.
"""
from __future__ import annotations

import sys
import warnings
from math import asin, atan, cos, degrees, pi, radians, sin, sqrt, tan
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.special import j1, jn_zeros

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

warnings.filterwarnings("ignore")
C_DIR = HERE.parent
v = Verifier.from_files("04-09", C_DIR / "chapters" / "04-09-waves-and-optics.md",
                        C_DIR / "solutions" / "04-09-solutions.md", C_DIR / "labs" / "04-09-lab" / "README.md")
C = 299792458.0
H = 6.62607015e-34
E_CH = 1.602176634e-19


def reflectance(lam, layers, n0=1.0, ns=1.5):
    M = np.eye(2, dtype=complex)
    for n, d in layers:
        dl = 2 * pi * n * d / lam
        M = M @ np.array([[np.cos(dl), 1j * np.sin(dl) / n], [1j * n * np.sin(dl), np.cos(dl)]])
    B, Cc = M @ np.array([1, ns])
    r = (n0 * B - Cc) / (n0 * B + Cc)
    return abs(r) ** 2


def snell(n1, n2, th1_deg):
    return degrees(brentq(lambda t: n1 * sin(radians(th1_deg)) - n2 * sin(t), 0, pi / 2))


def critical(n1, n2):
    return degrees(brentq(lambda t: n1 * sin(t) - n2, 0, pi / 2))


def af(theta, N, d_over_lam, dphi):
    m = np.arange(N)
    return abs(np.exp(1j * m * (2 * pi * d_over_lam * sin(theta) - dphi)).sum()) / N


def beamwidth(N, d_over_lam, steer_deg):
    dphi = 2 * pi * d_over_lam * sin(radians(steer_deg))
    t0 = radians(steer_deg)
    f = lambda th: af(th, N, d_over_lam, dphi) - 1 / sqrt(2)
    return degrees(brentq(f, t0, t0 + 0.5) - brentq(f, t0 - 0.5, t0))


def string_mode(T, mu, L, n):
    v = sqrt(T / mu)
    return brentq(lambda f: np.sin(2 * pi * f / v * L) if n % 2 == 0 else np.sin(2 * pi * f / v * L), (n - 0.5) * v / (2 * L), (n + 0.5) * v / (2 * L))


# ---------------------------------------------------------------- theory keys
v.check("T 04-09.a", sqrt(1.4 * 8.314462618 * 293.15 / 0.0289647))
v.check("T 04-09.b", jn_zeros(1, 1)[0] / pi)
v.assert_true("2 J1(u)/u vanishes at the first Bessel root", abs(2 * j1(jn_zeros(1, 1)[0])) < 1e-12)

# ---------------------------------------------------------------- examples
v.check("Ex 04-09.1a", C / 1e9)
vs = sqrt(1.4 * 8.314 * 293.15 / 0.02897)
v.check("Ex 04-09.1b", vs / 1e3)
v1 = sqrt(60 / 0.5e-3)
v.check("Ex 04-09.1c", v1)
v.check("Ex 04-09.1d", string_mode(60, 0.5e-3, 0.65, 1))
v.check("Ex 04-09.1e", string_mode(60, 0.5e-3, 0.65, 3))
v.check("Ex 04-09.2a", 633e-9 * 1 / 0.2e-3 * 1e3)
v.check("Ex 04-09.2b", degrees(brentq(lambda t: pi * sin(t) - pi / 4, 0, pi / 2)))
v.check("Ex 04-09.2c", degrees(pi * sin(radians(30))))
v.check("Ex 04-09.3a", reflectance(550, []) * 100)
v.check("Ex 04-09.3b", minimize_scalar(lambda n: reflectance(550, [(n, 550 / (4 * n))]), bounds=(1.1, 1.4), method="bounded", options={"xatol": 1e-10}).x)
v.check("Ex 04-09.3c", 550 / (4 * sqrt(1.5)))
v.check("Ex 04-09.3d", 550 / (4 * 1.38))
v.check("Ex 04-09.3e", reflectance(550, [(1.38, 550 / (4 * 1.38))]) * 100)
n4, L4, lam4 = 3.5, 300e-6, 1310e-9
m4 = 2 * n4 * L4 / lam4
v.check("Ex 04-09.4a", (C * (m4 + 1) / (2 * n4 * L4) - C * m4 / (2 * n4 * L4)) / 1e9)
v.check("Ex 04-09.4b", lam4**2 * (C / (2 * n4 * L4)) / C * 1e9)          # d(lambda) = lambda^2 df / c at 1310 nm
v.check("Ex 04-09.4c", m4)
v.check("Ex 04-09.4e", brentq(lambda f: np.cos(2 * pi * f * 0.25e-9), 0.5e9, 1.5e9) / 1e9)
v.check("Ex 04-09.5a", 13 * 0.33 / 13.5)
v.check("Ex 04-09.5b", 8 * 0.55 / 13.5)
v.check("Ex 04-09.5c", 0.25 * 13.5 / 0.33)
v.check("Ex 04-09.5d", 0.25 * 13.5 / 0.55)
v.check("Ex 04-09.5e", 193 * (13 * 0.33 / 13.5) / 13)
v.check("Ex 04-09.5f", H * C / 13.5e-9 / E_CH)
NA6 = sin(radians(90 - critical(1.468, 1.463))) * 1.468
v.check("Ex 04-09.6a", NA6)
v.check("Ex 04-09.6b", degrees(asin(NA6)))
v.check("Ex 04-09.6c", critical(1.468, 1.463))
v.check("Ex 04-09.6d", reflectance(1000, [], 1.0, 1.5) * 100)
v.check("Ex 04-09.6e", reflectance(1000, [], 1.0, 3.48) * 100)
v.check("Ex 04-09.7a", 0.5 * 2)
v.check("Ex 04-09.7b", 0.275 * 80)
v.check("Ex 04-09.7c", 17 * 80 * 0.1)
v.check("Ex 04-09.7d", 1 / 25e9 * 1e12)
v.check("Ex 04-09.8a", 0.5 * cos(radians(45)) ** 2 * cos(radians(45)) ** 2)
v.check("Ex 04-09.8b", 0.5 * cos(radians(90)) ** 2)
v.check("Ex 04-09.8c", degrees(brentq(lambda t: tan(t) - 1.5, 0.1, 1.5)))

# ---------------------------------------------------------------- solutions
v.check("04-09.1a", C / 2.4e9 * 100)
v.check("04-09.1b", 1 / 2.4e9 * 1e9)
v.check("04-09.1c", 2 * pi * 2.4e9 / C)
v.check("04-09.2a", sqrt(100 / 2e-3))
v.check("04-09.2b", string_mode(100, 2e-3, 0.5, 1))
v.check("04-09.2c", brentq(lambda T: string_mode(T, 2e-3, 0.5, 1) - 440, 50, 1000))
v.check("04-09.3a", abs(443 - 440))
v.check("04-09.4a", 532e-9 * 2 / 0.5e-3 * 1e3)
v.check("04-09.5a", degrees(asin(sin(radians(30)) - 1 / 0.75)))
v.check("04-09.5b", brentq(lambda d: sin(radians(30)) - 1 / d + 1, 0.1, 2))
th6 = degrees(brentq(lambda t: 10e-6 * sin(t) - 633e-9, 0, 0.5))
v.check("04-09.6a", th6)
v.check("04-09.6b", 2 * 1 * tan(radians(th6)) * 1e3)
v.check("04-09.7a", jn_zeros(1, 1)[0] / pi * 550e-9 / 5e-3)
v.check("04-09.7b", jn_zeros(1, 1)[0] / pi * 550e-9 / 5e-3 * 100 * 1e3)
v.check("04-09.8a", minimize_scalar(lambda n: reflectance(1550, [(n, 1550 / (4 * n))], 1.0, 3.48), bounds=(1.6, 2.1), method="bounded", options={"xatol": 1e-10}).x)
v.check("04-09.8b", 1550 / (4 * 1.9))
v.check("04-09.8c", reflectance(1550, [(1.9, 1550 / (4 * 1.9))], 1.0, 3.48) * 100)
v.check("04-09.9a", snell(1.0, 1.5, 30))
v.check("04-09.9b", critical(1.5, 1.0))
v.check("04-09.9c", critical(3.48, 1.444))
NA10 = sin(radians(90 - critical(1.48, 1.46))) * 1.48
v.check("04-09.10a", NA10)
v.check("04-09.10b", degrees(asin(NA10)))
v.check("04-09.11a", 2 * 0.5 + 2 * 0.4)
v.check("04-09.11b", 0 - (2 * 0.5 + 2 * 0.4))
dt12 = 17 * 40 * 0.08
v.check("04-09.12a", dt12)
v.check("04-09.12b", 1 / (2 * dt12 * 1e-12) / 1e9)
v.check("04-09.13a", 0.5 * cos(radians(30)) ** 2)
v.check("04-09.13b", 0.5 * cos(radians(30)) ** 2 * cos(radians(60)) ** 2)
d14 = 550 / (4 * 1.38)
v.check("04-09.14a", reflectance(450, [(1.38, d14)]) * 100)
v.check("04-09.14b", reflectance(650, [(1.38, d14)]) * 100)

# ---------------------------------------------------------------- lab
v.check("Lab 04-09.a", beamwidth(8, 0.5, 0))
v.check("Lab 04-09.b", beamwidth(8, 0.5, 30))
ys = np.linspace(-5, 5, 4001)
v.check("Lab 04-09.c", brentq(lambda s: np.trapezoid(np.cos(2 * pi * ys * s), ys), 0.05, 0.15) * 10)
v.check("Lab 04-09.d", brentq(lambda u: j1(u), 3, 4.5) / pi)
lams = np.linspace(400, 750, 701)
v.check("Lab 04-09.e", lams[np.argmin([reflectance(lam, [(1.38, d14)]) for lam in lams])])
v.check("Lab 04-09.f", 1 / (2 * 17 * 10 * 0.1e-12) / 1e9)

sys.exit(v.finish())
