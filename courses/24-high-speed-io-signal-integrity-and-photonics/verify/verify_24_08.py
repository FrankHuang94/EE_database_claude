#!/usr/bin/env python3
"""Verify every number in chapter 24-08 (silicon photonics and optical transceivers), its problems and lab.

Independent routes (the lab module siph.py uses closed forms):
- cutoff wavelengths from the CODATA constants written out here;
- critical angles by root-finding Snell's law; the single-mode slab thickness by counting the roots of the
  symmetric-slab TE dispersion equations and bisecting on the thickness where a second mode appears;
- coupling by numerical quadrature of the overlap integral (separable in x and y), and offsets by root-finding it;
- the grating coupler by solving phase matching for the angle at each wavelength, with the dispersion by
  finite differences and the band edges by root-finding the exact tilt loss;
- the driver-bond-modulator response from complex impedances, with the peak by bounded minimization and the
  -3 dB point by root-finding;
- linear-chain BER by numerically convolving the segments' noise densities and integrating the tail;
- yield from the binomial distribution; budgets, powers and growth rates by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special, stats
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-08-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-08", ROOT / "chapters" / "24-08-silicon-photonics.md",
                        ROOT / "solutions" / "24-08-solutions.md", LAB / "README.md")

h, q, c = 6.62607015e-34, 1.602176634e-19, 299792458.0
HC = h * c / q * 1e9  # nm·eV


def db(x):
    return 10 * math.log10(x)


def critical(n1, n2):
    return math.degrees(optimize.brentq(lambda t: n1 * math.sin(t) - n2, 0.0, math.pi / 2))


def te_modes(d_um, lam_um, n1, n2):
    """Count guided TE modes of a symmetric slab by counting sign changes of the pole-free dispersion functions."""
    vv = math.pi * d_um / lam_um * math.sqrt(n1 ** 2 - n2 ** 2)
    u = np.linspace(1e-9, vv * (1 - 1e-12), 20001)
    w = np.sqrt(np.maximum(vv ** 2 - u ** 2, 0))
    even = u * np.sin(u) - w * np.cos(u)  # u tan u = w
    odd = u * np.cos(u) + w * np.sin(u)  # -u cot u = w
    return int(np.sum(np.diff(np.sign(even)) != 0) + np.sum(np.diff(np.sign(odd)) != 0))


def single_mode_limit(lam_um, n1, n2):
    lo, hi = 0.01, 3.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if te_modes(mid, lam_um, n1, n2) < 2 else (lo, mid)
    return 0.5 * (lo + hi)


def eta(w1, w2, d=0.0):
    """Normalized overlap of two circular Gaussians, by quadrature (separable)."""
    lim = 12 * max(w1, w2) + abs(d)
    ox = integrate.quad(lambda x: math.exp(-x ** 2 / w1 ** 2 - (x - d) ** 2 / w2 ** 2), -lim, lim, limit=200)[0]
    oy = integrate.quad(lambda y: math.exp(-y ** 2 / w1 ** 2 - y ** 2 / w2 ** 2), -lim, lim, limit=200)[0]
    n1 = integrate.quad(lambda x: math.exp(-2 * x ** 2 / w1 ** 2), -lim, lim)[0] ** 2
    n2 = integrate.quad(lambda x: math.exp(-2 * x ** 2 / w2 ** 2), -lim, lim)[0] ** 2
    return (ox * oy) ** 2 / (n1 * n2)


# ---------------------------------------------------------------- Example 24-08.1 and Problem 1
v.check("Ex 24-08.1a", HC)
v.check("Ex 24-08.1b", HC / 1.12)
v.check("Ex 24-08.1c", HC / 0.80)
v.check("Ex 24-08.1c1", HC / 0.66)
v.check("Ex 24-08.1d", HC / 0.75)
v.check("24-08.1a", HC / 1.42)
v.check("24-08.1b", HC / 1.34)
v.assert_true("850 nm absorbed by GaAs and InP, 1310 nm by neither",
              HC / 1.42 > 850 and HC / 1.34 > 850 and HC / 1.42 < 1310 and HC / 1.34 < 1310)

# ---------------------------------------------------------------- Example 24-08.2, Problem 2
na_si = math.sqrt(3.48 ** 2 - 1.44 ** 2)
na_f = math.sqrt(1.4504 ** 2 - 1.4447 ** 2)
v.check("Ex 24-08.2a", critical(3.48, 1.44))
v.check("Ex 24-08.2a1", critical(1.4504, 1.4447))
v.check("Txt 24-08.e", critical(1.4504, 1.4447))
v.check("Ex 24-08.2b", (3.48 - 1.44) / 3.48)
v.check("Ex 24-08.2b1", (1.4504 - 1.4447) / 1.4504)
v.check("Ex 24-08.2b2", ((3.48 - 1.44) / 3.48) / ((1.4504 - 1.4447) / 1.4504))
v.check("Ex 24-08.2c0", na_si)
d_si = single_mode_limit(1.55, 3.48, 1.44)
v.check("Ex 24-08.2c", d_si)
v.check("Ex 24-08.2d0", na_f)
core = special.jn_zeros(0, 1)[0] * 1.55 / (math.pi * na_f)
v.check("Ex 24-08.2d", core)
v.check("Txt 24-08.b", core / d_si)
v.check("24-08.2a", critical(2.0, 1.44))
v.check("24-08.2b0", math.sqrt(2.0 ** 2 - 1.44 ** 2))
d_sin = single_mode_limit(1.31, 2.0, 1.44)
d_si13 = single_mode_limit(1.31, 3.48, 1.44)
v.check("24-08.2b", d_sin)
v.check("24-08.2c", d_si13)
v.check("24-08.2c1", d_sin / d_si13)

# ---------------------------------------------------------------- Example 24-08.3, Problem 3, Lab a
for key, w in (("3a", 0.5), ("3b", 1.5), ("3c", 4.0)):
    e = eta(4.6, w)
    v.check(f"Ex 24-08.{key}", e)
    v.check(f"Ex 24-08.{key}1", db(e))
v.check("Lab 24-08.a", eta(4.6, 1.5))
for key, w in (("3d", 4.6), ("3d1", 1.5)):
    v.check(f"Ex 24-08.{key}", optimize.brentq(lambda d, w=w: db(eta(w, w, d)) + 0.5, 0.0, 5 * w))
e3 = eta(4.6, 2.0)
v.check("24-08.3a", e3)
v.check("24-08.3a1", db(e3))
v.check("24-08.3b0", eta(4.6, 4.6, 1.0))
v.check("24-08.3b", db(eta(4.6, 4.6, 1.0)))
v.check("24-08.3c0", eta(2.0, 2.0, 1.0))
v.check("24-08.3c", db(eta(2.0, 2.0, 1.0)))


# ---------------------------------------------------------------- Example 24-08.4, Problems 4 and 12, Lab b
def grating(lam0, neff, th_deg, w_um):
    k = lambda lam: 2 * math.pi / lam  # noqa: E731
    period = optimize.brentq(lambda p: neff * k(lam0) - 2 * math.pi / p - k(lam0) * math.sin(math.radians(th_deg)),
                             lam0 / (neff + 1) * 1.0001, lam0 / (neff - 1))

    def angle(lam):  # phase matching solved for the radiation angle
        return math.degrees(optimize.brentq(lambda t: neff * k(lam) - 2 * math.pi / period - k(lam) * math.sin(t),
                                            -1.2, 1.2))
    disp = (angle(lam0 - 0.01) - angle(lam0 + 0.01)) / 0.02  # degrees per nm, magnitude
    div = math.degrees(lam0 * 1e-3 / (math.pi * w_um))
    loss = lambda lam: -db(math.exp(-((angle(lam) - th_deg) / div) ** 2))  # noqa: E731
    return period, disp, div, angle, loss


per4, disp4, div4, ang4, loss4 = grating(1310.0, 2.8, 10.0, 4.6)
v.check("Ex 24-08.4a", per4)
v.check("Ex 24-08.4b0", math.radians(disp4))
v.check("Ex 24-08.4b", disp4)
v.check("Txt 24-08.c", disp4)
v.check("Ex 24-08.4c", 60 * disp4)
v.check("Ex 24-08.4d", div4)
a1db = div4 * math.sqrt(0.1 * math.log(10))
v.check("Ex 24-08.4e0", a1db)
v.check("Ex 24-08.4e1", a1db / disp4)
v.check("Ex 24-08.4e", 2 * a1db / disp4)
v.check("Ex 24-08.4f0", 30 * disp4)
v.check("Ex 24-08.4f", db(math.exp(-((30 * disp4) / div4) ** 2)))
lo_edge = optimize.brentq(lambda lam: loss4(lam) - 1.0, 1250, 1310)
hi_edge = optimize.brentq(lambda lam: loss4(lam) - 1.0, 1310, 1370)
v.check("Lab 24-08.b", lo_edge)
v.check("Lab 24-08.b1", hi_edge)
v.check("Lab 24-08.b2", hi_edge - lo_edge)
v.check("Lab 24-08.i", 1 / disp4)
per_p4, disp_p4, div_p4, _, _ = grating(1550.0, 2.85, 8.0, 5.2)
v.check("24-08.4a", per_p4)
v.check("24-08.4b", disp_p4)
v.check("24-08.4c", div_p4)
v.check("24-08.4d", 2 * div_p4 * math.sqrt(0.1 * math.log(10)) / disp_p4)
for key, off in (("12a", 30), ("12b", 10)):
    v.check(f"24-08.{key}0", off * disp4)
    v.check(f"24-08.{key}", -db(math.exp(-((off * disp4) / div4) ** 2)))

# ---------------------------------------------------------------- Example 24-08.5 (in linear transmissions)
t_out = 10 ** (-0.18 / 10) * 10 ** (-1.0 / 10) * 10 ** (-1.5 / 10) * 10 ** (-4.0 / 10) * 0.5  # quadrature: half
p_req_mw = 10 ** ((-8.0 + 2.0) / 10)
p_mod = p_req_mw / t_out
v.check("Ex 24-08.5a", db(p_mod))
v.check("Ex 24-08.5a1", p_mod)
v.check("Txt 24-08.a", -db(0.5))
t_split = 0.25 * 10 ** (-0.5 / 10) * 10 ** (-1.5 / 10)
p_las = p_mod / t_split
v.check("Ex 24-08.5b0", -db(0.25 * 10 ** (-0.5 / 10)))
v.check("Ex 24-08.5b", db(p_las))
v.check("Ex 24-08.5b1", p_las)
v.check("Ex 24-08.5c", p_las / 0.15)
v.check("Ex 24-08.5d", 2 * p_las / 0.15 / 1e3)
v.check("Ex 24-08.5d1", 100 * 2 * p_las / 0.15 / 1e3 / 16)
p5 = 10 ** ((-7.0 + 2.0) / 10) / (10 ** (-0.72 / 10) * 10 ** (-1.0 / 10) * 10 ** (-1.5 / 10) * 10 ** (-6 / 10))
v.check("24-08.5a", db(p5))
v.check("24-08.5b", p5)
v.check("24-08.5c", 4 * p5)


# ---------------------------------------------------------------- Example 24-08.6, Problem 6, Lab c-e
def bond(r, l, cap):
    mag = lambda f: abs(1 / (1 + (r + 2j * math.pi * f * l) * 2j * math.pi * f * cap))  # noqa: E731  divider
    res = optimize.minimize_scalar(lambda lf: -mag(10 ** lf), bounds=(9, 12.5), method="bounded",
                                   options={"xatol": 1e-10})
    fpk, pk = 10 ** res.x, mag(10 ** res.x)
    f3 = optimize.brentq(lambda f: mag(f) - 1 / math.sqrt(2), max(fpk, 1e9), 1e13, xtol=1e3)
    return fpk, pk, f3


f0w, zw = 1 / (2 * math.pi * math.sqrt(1e-9 * 20e-15)), 25 * math.sqrt(20e-15 / 1e-9)
fpk, pk, f3w = bond(50, 1e-9, 20e-15)
v.check("Ex 24-08.6a", f0w / 1e9)
v.check("Ex 24-08.6a1", zw)
v.check("Ex 24-08.6b", fpk / 1e9)
v.check("Txt 24-08.d", fpk / 1e9)
v.check("Ex 24-08.6c", pk)
v.check("Ex 24-08.6c1", 20 * math.log10(pk))
v.check("Ex 24-08.6d", f3w / 1e9)
v.check("Lab 24-08.c", 20 * math.log10(pk))
v.check("Lab 24-08.d", f3w / 1e9)
v.check("Ex 24-08.6e", 1 / (2 * math.pi * math.sqrt(10e-12 * 20e-15)) / 1e9)
v.check("Ex 24-08.6e1", 25 * math.sqrt(20e-15 / 10e-12))
fpk_h, pk_h, f3h = bond(50, 10e-12, 20e-15)
v.assert_true("hybrid bond does not peak", pk_h < 1 + 1e-9)
v.check("Ex 24-08.6f", f3h / 1e9)
v.check("Lab 24-08.e", f3h / 1e9)
v.check("Ex 24-08.6g", 1 / (2 * math.pi * 50 * 20e-15) / 1e9)
v.check("Ex 24-08.6g1", 113.4375 / 2)
fpk6, pk6, f36 = bond(50, 0.5e-9, 20e-15)
v.check("24-08.6a", 1 / (2 * math.pi * math.sqrt(0.5e-9 * 20e-15)) / 1e9)
v.check("24-08.6a1", 25 * math.sqrt(20e-15 / 0.5e-9))
v.check("24-08.6b", fpk6 / 1e9)
v.check("24-08.6b0", pk6)
v.check("24-08.6b1", 20 * math.log10(pk6))
v.check("24-08.6c", f36 / 1e9)


# ---------------------------------------------------------------- Example 24-08.7, Problem 7, Lab f-h, j, k
def linear_ber(qs):
    """BER of a decision on unit half-eye after adding independent Gaussian noises of sigma = 1/Q_i: convolve the
    densities numerically and integrate the tail beyond the eye."""
    x = np.linspace(-3, 3, 60001)
    dx = x[1] - x[0]
    pdf = None
    for qi in qs:
        g = norm.pdf(x, scale=1 / qi)
        pdf = g if pdf is None else np.convolve(pdf, g, mode="same") * dx
    tail = x >= 1.0
    return float(integrate.trapezoid(pdf[tail], x[tail]))


q0 = norm.isf(1e-12)
v.check("Ex 24-08.7a", q0)
v.check("Ex 24-08.7b", 3 * norm.sf(q0))
b3 = linear_ber([q0] * 3)
q3 = norm.isf(b3)
v.check("Ex 24-08.7c", q3)
v.check("Ex 24-08.7c1", b3)
v.check("Ex 24-08.7d", q0 * math.sqrt(3))
v.check("Ex 24-08.7d1", 20 * math.log10(math.sqrt(3)))
v.check("Lab 24-08.f", linear_ber([q0] * 2))
v.check("Lab 24-08.g", b3)
v.check("Lab 24-08.h", linear_ber([q0] * 4))
v.check("Lab 24-08.j", q0 * 2)
v.check("Lab 24-08.k", 20 * math.log10(2))
b7 = linear_ber([9, 7.5, 9])
v.check("24-08.7a", norm.isf(b7))
v.check("24-08.7a1", b7)
v.check("24-08.7b", 2 * norm.sf(9) + norm.sf(7.5))

# ---------------------------------------------------------------- Example 24-08.8, Problems 8 and 13
v.check("Ex 24-08.8a", 16 / 800e9 * 1e12)
v.check("Ex 24-08.8a1", 33.5 / 1600e9 * 1e12)
v.check("Ex 24-08.8a2", 33.5 / 16)
v.check("Ex 24-08.8b", 144 / 2)
v.check("Ex 24-08.8b1", 72 * 33.5 / 1e3)
v.check("Ex 24-08.8b2", 144 * 0.8)
v.check("Ex 24-08.8c", 100 * (1 - 15 / 20))
v.check("Ex 24-08.8c1", 20 / 1600e9 * 1e12)
v.check("Ex 24-08.8c2", 15 / 1600e9 * 1e12)
v.check("24-08.8a", 64 * 16)
v.check("24-08.8b", 100 * 64 * 16 / (64 * 16 + 1500))
v.check("24-08.8c", 64 * 16 / 51.2e12 * 1e12)
v.check("24-08.13a", 2 * 2 * 16)
v.check("24-08.13a1", 3 * 2 * 16)
v.check("24-08.13b", 1e5 * 64 / 1e6)
v.check("24-08.13b1", 1e5 * 96 / 1e6)
v.check("24-08.13c", 0.25 * 1e5 * 96 / 1e6)

# ---------------------------------------------------------------- Example 24-08.9, Problem 9 (binomial yield)
y8 = stats.binom.pmf(8, 8, 0.99)
v.check("Ex 24-08.9a", y8)
v.check("Ex 24-08.9b", 3 / y8)
v.check("Ex 24-08.9c", 1 / y8 + 2)
v.check("Ex 24-08.9d", 100 * (1 - (1 / y8 + 2) / (3 / y8)))
y16 = stats.binom.pmf(16, 16, 0.998)
v.check("24-08.9a", y16)
v.check("24-08.9b", 4 / y16)
v.check("24-08.9c", 1 / y16 + 3)
v.check("24-08.9d", 100 * (1 - (1 / y16 + 3) / (4 / y16)))
v.check("24-08.9e", 1 / (1 - y16))

# ---------------------------------------------------------------- Problems 10 and 11, text growth rates
v.check("24-08.10a", 16 * 32)
v.check("24-08.10b", 8 * 2 * 16 * 32)
v.assert_true("optical side matches 16 UCIe-S modules of 512 Gb/s", 8 * 2 * 16 * 32 == 16 * 512)
v.check("24-08.10c", 8192 / 896)
cagr = optimize.brentq(lambda g: 8 * (1 + g) ** 5 - 20, 0, 1)
v.check("24-08.11a", 100 * cagr)
v.check("24-08.11b", 100 * (26 / 16.5 - 1))
v.check("Txt 24-08.f", 100 * cagr)
v.check("Txt 24-08.g", 100 * (26 / 16.5 - 1))

sys.exit(v.finish())
