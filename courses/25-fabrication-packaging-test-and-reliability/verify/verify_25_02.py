#!/usr/bin/env python3
"""Verify every number in chapter 25-02 (lithography), its problems and lab.

Independent routes (the lab module litho.py sums diffraction orders numerically):
- resolution limits from the pupil inequality by root-finding;
- depth of focus from the exact quarter-wave condition, solved for the defocus numerically;
- image contrast from closed-form two- and three-beam intensities, maximized and minimized on a grid;
- Fourier amplitudes of the grating by numerical integration;
- photon counts from J and eV conversions; a Monte Carlo of absorbed photons;
- scanner throughput and cost by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-02", ROOT / "chapters" / "25-02-lithography.md",
                        ROOT / "solutions" / "25-02-solutions.md", LAB / "README.md")

H, C_LIGHT, Q = 6.62607015e-34, 2.99792458e8, 1.602176634e-19
HC = 1239.84  # eV nm, as published


def e_photon_ev(lam_nm):
    return H * C_LIGHT / (lam_nm * 1e-9) / Q


def pmin(lam, na, off_axis):
    """Smallest pitch with two orders inside the pupil, by root-finding the pupil condition."""
    f = (lambda p: lam / (2 * p) - na) if off_axis else (lambda p: lam / p - na)
    return optimize.brentq(f, lam / 100, lam * 100)


def dof(lam, na, n):
    """Total DOF: solve 2*pi*n*z*(1 - cos(theta))/lam = pi/2 for z, times 2."""
    one_minus_cos = 1 - math.cos(math.asin(na / n))
    z = optimize.brentq(lambda z: 2 * math.pi * n * z * one_minus_cos / lam - math.pi / 2, 1e-3, 1e5)
    return 2 * z


def amp(m, f):
    """Fourier amplitude by numerical integration over one period (p = 1)."""
    re = integrate.quad(lambda x: math.cos(2 * math.pi * m * x), -f / 2, f / 2)[0]
    return re


def contrast_two_beam(a0, a1):
    u = np.linspace(0, 2 * math.pi, 20001)
    i = a0**2 + a1**2 + 2 * a0 * a1 * np.cos(u)
    return (i.max() - i.min()) / (i.max() + i.min())


def photons_nm2(dose_mj, lam):
    return dose_mj * 1e-3 / (e_photon_ev(lam) * Q) / 1e14


WAFER_HOURS = 5 * 8766 * 0.8

# ---------------------------------------------------------------- Example 1
v.check("Ex 25-02.1a", pmin(193, 1.35, False))
v.check("Ex 25-02.1b", pmin(193, 1.35, True))
v.check("Ex 25-02.1b1", pmin(193, 1.35, True) / 2)
s0 = 0.9 * 1.35
v.check("Ex 25-02.1c", s0)
v.check("Ex 25-02.1c0", 193 / 80)
v.check("Ex 25-02.1c1", s0 - 193 / 80)
v.check("Ex 25-02.1c2", s0 + 193 / 80)
v.assert_true("80 nm: orders 0 and -1 inside the pupil, +1 outside",
              abs(s0) <= 1.35 and abs(s0 - 193 / 80) <= 1.35 and abs(s0 + 193 / 80) > 1.35)
v.check("Ex 25-02.1d", 40 * 1.35 / 193)

# ---------------------------------------------------------------- Example 2, text
c_arf = math.cos(math.asin(1.35 / 1.44))
v.check("Ex 25-02.2a0", c_arf)
v.check("Ex 25-02.2a1", 1 - c_arf)
v.check("Ex 25-02.2a", dof(193, 1.35, 1.44))
v.check("Ex 25-02.2b0", math.cos(math.asin(0.33)))
v.check("Ex 25-02.2b", dof(13.5, 0.33, 1.0))
v.check("Ex 25-02.2c0", math.cos(math.asin(0.55)))
v.check("Ex 25-02.2c", dof(13.5, 0.55, 1.0))
v.check("Ex 25-02.2d", dof(13.5, 0.55, 1.0) / dof(13.5, 0.33, 1.0))
v.check("Ex 25-02.2e", 13.5 / 0.33**2)
v.check("Ex 25-02.2e1", 13.5 / 0.55**2)
v.check("Ex 25-02.2e2", 1.44 * 193 / 1.35**2)

# ---------------------------------------------------------------- Example 3
v.check("Ex 25-02.3a", 1.44 * 0.94)
v.check("Ex 25-02.3b", 193 / 1.44)
v.check("Ex 25-02.3c", (1.44 * 0.94) / 0.94)
v.check("Ex 25-02.3d", 1.0 * 0.94)

# ---------------------------------------------------------------- Example 4
v.check("Ex 25-02.4a", 76 / 28)
v.check("Ex 25-02.4a1", 76 / 4)
v.check("Ex 25-02.4b", 14 * 0.33 / 13.5)
v.check("Ex 25-02.4c", math.ceil(76 / 28))
v.check("Ex 25-02.4c1", 76 / 2)

# ---------------------------------------------------------------- Example 5
v.check("Ex 25-02.5a", 32 - 4)
v.check("Ex 25-02.5a1", 32 + 4)
v.check("Ex 25-02.5b", 100 * 4 / 32)
v.check("Ex 25-02.5c", 0.10 * 32)

# ---------------------------------------------------------------- Example 6, text
ee, ea = e_photon_ev(13.5), e_photon_ev(193)
v.check("Ex 25-02.6a", ee)
v.check("Ex 25-02.6a1", ea)
v.check("Ex 25-02.6a2", ee / ea)
v.check("Ex 25-02.6b0", ee * Q)
pe, pa = photons_nm2(30, 13.5), photons_nm2(30, 193)
v.check("Ex 25-02.6b", pe)
v.check("Ex 25-02.6b1", pa)
v.check("Ex 25-02.6c", pe * 100)
v.check("Ex 25-02.6c1", 100 / math.sqrt(pe * 100))
v.check("Ex 25-02.6d", pe * 100 * 0.2)
v.check("Ex 25-02.6d1", 100 / math.sqrt(pe * 100 * 0.2))
n2 = optimize.brentq(lambda n: 1 / math.sqrt(n) - 0.02, 10, 1e6)
v.check("Ex 25-02.6e", n2)
v.check("Ex 25-02.6e0", n2 / 0.2 / 100)
v.check("Ex 25-02.6e1", n2 / 0.2 / 100 / pe * 30)
v.check("Txt 25-02.b", math.sqrt(ee / ea))

# ---------------------------------------------------------------- Example 7
v.check("Ex 25-02.7a0", WAFER_HOURS)
v.check("Ex 25-02.7a", 170e6 / (WAFER_HOURS * 220))
v.check("Ex 25-02.7a1", 350e6 / (WAFER_HOURS * 175))
v.check("Ex 25-02.7a2", 350e6 / (WAFER_HOURS * 125))
v.check("Ex 25-02.7b", 2 * 170e6 / (WAFER_HOURS * 220))

# ---------------------------------------------------------------- Example 8, text
v.check("Ex 25-02.8a", 26 * 33)
v.check("Ex 25-02.8a1", 26 * 16.5)
v.check("Ex 25-02.8b", 4 * 26)
v.check("Ex 25-02.8b1", 4 * 33)
v.check("Ex 25-02.8d", 100 * (1 - 125 / 175))
v.assert_true("750 mm2 fits the full field but not the half field", 750 < 858 and 750 > 429)
v.check("Txt 25-02.a", 100 * 0.7**10)
v.check("Txt 25-02.c", 38 * 1.35 / 193)
v.check("Txt 25-02.d", 13 * 0.33 / 13.5)
v.check("Txt 25-02.e", 8 * 0.55 / 13.5)
v.check("Txt 25-02.f", 100 * (1000 / 600 - 1))

# ---------------------------------------------------------------- Problems 1-7
v.check("25-02.1a", pmin(248, 0.80, False))
v.check("25-02.1b", pmin(248, 0.80, True))
v.check("25-02.1c", pmin(248, 0.80, True) / 2)
v.check("25-02.2a", 1.65 * 0.94)
v.check("25-02.2b", pmin(193, 1.65 * 0.94, True) / 2)
v.check("25-02.3a", 13.5 / 48)
v.check("25-02.3b", pmin(13.5, 0.33, True))
v.check("25-02.3c", pmin(13.5, 0.33, False))
v.check("25-02.3d", 12 * 0.33 / 13.5)
cd = math.cos(math.asin(0.93))
cw = math.cos(math.asin(0.93 / 1.44))
v.check("25-02.4a0", cd)
v.check("25-02.4a1", 1 - cd)
v.check("25-02.4a", dof(193, 0.93, 1.0))
v.check("25-02.4a2", cw)
v.check("25-02.4a3", 1 - cw)
v.check("25-02.4b", dof(193, 0.93, 1.44))
v.check("25-02.4c", dof(193, 0.93, 1.44) / dof(193, 0.93, 1.0))
for key_a, key_c, f in (("25-02.5a", "25-02.5b", 0.5), ("25-02.5c", "25-02.5d", 0.25)):
    a0, a1 = amp(0, f), amp(1, f)
    v.check(key_a, a1)
    v.check(key_c, contrast_two_beam(a0, a1))
v.check("25-02.6a", 76 / 4)
v.check("25-02.6b", 10.5 * 0.33 / 13.5)
v.check("25-02.6c", 10.5 * 0.55 / 13.5)
v.check("25-02.7a", 24 - 2.5)
v.check("25-02.7a1", 24 + 2.5)
v.check("25-02.7a2", 100 * 2.5 / 24)
v.check("25-02.7b", 0.08 * 24)

# ---------------------------------------------------------------- Problems 8-14
p50 = photons_nm2(50, 13.5)
v.check("25-02.8a", p50)
v.check("25-02.8b", p50 * 64)
v.check("25-02.8c", p50 * 64 * 0.2)
v.check("25-02.8d", 100 / math.sqrt(p50 * 64 * 0.2))
n9 = 1 / 0.03**2
v.check("25-02.9a", n9)
v.check("25-02.9b", n9 / 0.25 / 64)
v.check("25-02.9c", n9 / 0.25 / 64 / pe * 30)
t_w = 3600 / 220
t_e = t_w - 6.0
v.check("25-02.10a0", t_w)
v.check("25-02.10a", t_e)
v.check("25-02.10a1", t_e)
v.check("25-02.10b0", t_e * 50 / 30)
v.check("25-02.10b", 3600 / (6 + t_e * 50 / 30))
v.check("25-02.10c0", t_e * 102 / 30)
v.check("25-02.10c1", 6 + t_e * 102 / 30)
w102 = 3600 / (6 + t_e * 102 / 30)
v.check("25-02.10c", w102)
v.check("25-02.10d", 100 * (1 - w102 / 220))
v.check("25-02.11a", 350e6 / (WAFER_HOURS * 135))
v.check("25-02.11b", 175 / 135)
v.check("25-02.12a", 100 * 700 / 858)
v.assert_true("700 mm2 exceeds the half field", 700 > 26 * 16.5)
v.check("25-02.13a0", t_e * 0.6)
w1000 = 3600 / (6 + t_e * 600 / 1000)
v.check("25-02.13a", w1000)
v.check("25-02.13a1", 100 * (w1000 / 220 - 1))
v.check("25-02.13b0", 3600 / 330)
v.check("25-02.13b1", 3600 / 220 - 3600 / 330)
sol = np.linalg.solve([[1, 1], [1, 0.6]], [3600 / 220, 3600 / 330])
v.check("25-02.13b2", sol[0])
v.check("25-02.13b", sol[1])
v.check("25-02.14a", 18)
v.check("25-02.14a1", 64 - 18 - 2 * 16)
v.check("25-02.14b", 18 - (64 - 18 - 2 * 16))
v.check("25-02.14c", 2 / 2)

# ---------------------------------------------------------------- Lab
v.check("Lab 25-02.a", pmin(13.5, 0.33, True))


def three_beam_contrast(p, lam, na, n, z, f=0.5):
    """On-axis: orders 0 and +-1 with defocus phase on the first orders relative to the zeroth."""
    s1 = lam / p
    assert s1 <= na
    phi = 2 * math.pi * n * z * (math.sqrt(1 - (s1 / n) ** 2) - 1) / lam
    a0, a1 = amp(0, f), amp(1, f)
    u = np.linspace(0, 2 * math.pi, 40001)
    e = a0 + 2 * a1 * np.exp(1j * phi) * np.cos(u)
    i = np.abs(e) ** 2
    return (i.max() - i.min()) / (i.max() + i.min())


v.check("Lab 25-02.b", three_beam_contrast(160, 193, 1.35, 1.44, 0))
v.check("Lab 25-02.b1", three_beam_contrast(160, 193, 1.35, 1.44, 50))
v.check("Lab 25-02.b2", contrast_two_beam(amp(0, 0.5), amp(1, 0.5)))
n_abs = pe * 100 * 0.2
v.check("Lab 25-02.c", math.sqrt(n_abs))
rng = np.random.default_rng(11)
sim = rng.binomial(rng.poisson(pe * 100, 200_000), 0.2)
v.assert_true("simulated absorbed-photon std within 1% of sqrt(N)", abs(sim.std() / math.sqrt(n_abs) - 1) < 0.01)
v.check("Lab 25-02.d", 3600 / (6 + t_e * 60 / 30))

sys.exit(v.finish())
