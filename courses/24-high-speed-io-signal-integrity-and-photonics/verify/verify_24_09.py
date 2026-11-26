#!/usr/bin/env python3
"""Verify every number in chapter 24-09 (linear-drive and co-packaged optics), its problems and lab.

Independent routes (the lab module cpo.py uses closed forms and the chi-square distribution):
- linear-chain Q and BER by numerically convolving the segments' Gaussian noise densities;
- dB conversions through natural logarithms; laser sharing in milliwatts;
- failure-rate bounds by root-finding the Poisson probability of observing at most r failures;
- energy, power, availability and deal figures by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-09", ROOT / "chapters" / "24-09-lpo-and-cpo.md",
                        ROOT / "solutions" / "24-09-solutions.md", LAB / "README.md")

YEAR = 8766.0
Q_KP4 = norm.isf(2.4e-4)


def pj(watts, gbps):
    return watts / (gbps * 1e9) * 1e12


def linear_ber(qs):
    """Decision on unit half-eye after independent Gaussian noises of sigma = 1/Q_i (numerical convolution)."""
    x = np.linspace(-3, 3, 60001)
    dx = x[1] - x[0]
    pdf = None
    for qi in qs:
        g = norm.pdf(x, scale=1 / qi)
        pdf = g if pdf is None else np.convolve(pdf, g, mode="same") * dx
    tail = x >= 1.0
    return float(integrate.trapezoid(pdf[tail], x[tail]))


def margin(q):
    return 20 * math.log10(q / Q_KP4)


def poisson_bound(device_hours, failures=0, conf=0.95):
    """Rate (per hour) at which observing <= failures has probability 1 - conf."""
    return optimize.brentq(lambda lam: stats.poisson.cdf(failures, lam * device_hours) - (1 - conf),
                           1e-15, 1e-3, xtol=1e-18)


def mw(dbm):
    return math.exp(dbm / 10 * math.log(10))


def db(ratio):
    return 10 * math.log(ratio) / math.log(10)


# ---------------------------------------------------------------- Example 24-09.1, text factors, Problem 1, 12
for key, w in (("1a", 6.4), ("1a1", 5.5), ("1a2", 3.5), ("1b", 16), ("1b1", 18)):
    v.check(f"Ex 24-09.{key}", pj(w, 800))
v.check("Ex 24-09.1c", 100 * (1 - 3.5 / 16))
v.check("Ex 24-09.1c1", 100 * (1 - 3.5 / 18))
v.check("Ex 24-09.1d", 100 * (1 - 3.5 / 6.4))
v.check("Txt 24-09.d", 16 / 3.5)
v.check("Txt 24-09.e", 18 / 3.5)
v.check("24-09.1a", 16 * 6.4)
v.check("24-09.1b", 16 * 6.4 / 0.8)
v.check("24-09.1c", 128 * 3.5)
v.check("24-09.1d", 128 * 16)
v.check("24-09.1e", 128 * (16 - 3.5))
v.check("24-09.12a", optimize.brentq(lambda p: 1 - 3.5 / p - 0.70, 4, 100))
v.check("24-09.12b", 5 * 5)

# ---------------------------------------------------------------- Example 24-09.2, Problems 4 and 8, text
v.check("Ex 24-09.2a", pj(25, 1600))
v.check("Ex 24-09.2a1", pj(5, 1600))
v.check("Ex 24-09.2a2", pj(25, 800))
v.check("Ex 24-09.2a3", pj(5, 800))
v.check("Ex 24-09.2b", 9 * 3.5)
v.check("Ex 24-09.2c", math.exp(1.8 * math.log(10)))
v.check("Ex 24-09.2c1", math.exp(0.9 * math.log(10)))
v.check("Txt 24-09.a", db(64))
v.check("24-09.4a", 1000 * math.exp(-22 / 20 * math.log(10)))
v.check("24-09.4b", 1000 * math.exp(-4 / 20 * math.log(10)))
v.check("24-09.8", pj(9, 1600))

# ---------------------------------------------------------------- Example 24-09.3, Problem 3, Lab a
v.check("Ex 24-09.3a", 2 * norm.sf(10) + norm.sf(8))
b3 = linear_ber([10, 8, 10])
q3 = norm.isf(b3)
v.check("Ex 24-09.3b", q3)
v.check("Ex 24-09.3b1", b3)
v.check("Ex 24-09.3c0", Q_KP4)
v.check("Ex 24-09.3c", margin(q3))
b3d = linear_ber([10, 6, 10])
q3d = norm.isf(b3d)
v.check("Ex 24-09.3d", q3d)
v.check("Ex 24-09.3d1", b3d)
v.check("Ex 24-09.3d2", margin(q3d))
v.check("Txt 24-09.c", margin(q3) - margin(q3d))
bp3 = linear_ber([12, 7, 12])
v.check("24-09.3a", norm.isf(bp3))
v.check("24-09.3b", bp3)
v.check("24-09.3c", margin(norm.isf(bp3)))
qa = optimize.brentq(lambda qo: margin(norm.isf(linear_ber([10, qo, 10]))) - 2.0, 4.5, 8.0, xtol=1e-6)
v.check("Lab 24-09.a", qa)


# ---------------------------------------------------------------- Example 24-09.4, Problems 2, 5, 11, Lab b
def share(src_dbm):
    avail_mw = mw(src_dbm) / mw(2.5) / mw(1.0)  # power after path and excess loss
    n = avail_mw / mw(3.69)
    return db(n), n, 2 ** int(math.log2(n))


a4, n4, b4 = share(23)
v.check("Ex 24-09.4a", a4)
v.check("Ex 24-09.4a1", n4)
v.check("Ex 24-09.4a2", b4)
per_lane = mw(23) / mw(2.5) / mw(1.0) / 4
v.check("Ex 24-09.4b", db(per_lane))
v.check("Ex 24-09.4b1", db(per_lane / mw(3.69)))
v.check("Ex 24-09.4c", 102.4e12 / 200e9)
v.check("Ex 24-09.4c1", 102.4e12 / 200e9 / 4)
a5, n5, b5 = share(26)
v.check("24-09.5a", a5)
v.check("24-09.5b", n5)
v.check("24-09.5c", b5)
v.check("Lab 24-09.b", b4)
v.check("Lab 24-09.b1", b5)
v.check("24-09.2a", mw(11))
v.check("24-09.2b", mw(17))
v.check("24-09.2c", mw(26))
v.check("24-09.2d", mw(26) / mw(11))
v.check("24-09.11a", 512 / 4)
v.check("24-09.11b", 512 / 4 / 8)
v.check("24-09.11c", 128 * mw(23) / 1e3)
v.check("24-09.11d", 128 * mw(23) / 1e3 / 0.15)
v.check("24-09.11e", 100 * 128 * mw(23) / 1e3 / 0.15 / 448)

# ---------------------------------------------------------------- Example 24-09.5, Problem 9
v.check("Ex 24-09.5a", 6.4e6 * 30 / 1e6)
v.check("Ex 24-09.5a1", 6.4e6 * 10 / 1e6)
v.check("Ex 24-09.5b", 100 * 192 / 400)
v.check("Ex 24-09.5b1", 100 * 64 / 400)
v.check("Ex 24-09.5b2", 100 * 42 / 400)
v.check("Ex 24-09.5c", 42e6 / 6.4e6)
v.check("Ex 24-09.5c1", 100 * (1 - 42 / 192))
v.check("24-09.9a", 1e5 * (20 - 15) / 1e6)
v.check("24-09.9b", 1e5 * 20 * 0.50 / 1e6)
v.check("24-09.9b1", 1e5 * 20 * 0.60 / 1e6)

# ---------------------------------------------------------------- Example 24-09.6, Problem 6, Lab c-d, text
lam0 = poisson_bound(1e6)
v.check("Ex 24-09.6a0", lam0 * 1e6)
v.check("Ex 24-09.6a", lam0 * 1e9)
v.check("Ex 24-09.6b", 1 / lam0)
v.check("Ex 24-09.6c", 1e6 / YEAR)
v.check("Ex 24-09.6d", lam0 * 1e6 / 100e-9 / 1e6)
v.check("Txt 24-09.b", 2 * lam0 * 1e6)  # chi-square 95% with 2 dof equals 2 x (-ln 0.05)
v.check("Lab 24-09.c", stats.poisson.pmf(0, lam0 * 1e6))
v.check("Lab 24-09.d", lam0 * 1e9)
v.check("Lab 24-09.d1", poisson_bound(1e6, 1) * 1e9)
v.check("Lab 24-09.d2", poisson_bound(1e6, 2) * 1e9)
v.check("24-09.6a", poisson_bound(15e6) * 1e9)
v.check("24-09.6a1", poisson_bound(50e6) * 1e9)
v.check("24-09.6b0", poisson_bound(15e6, 1) * 15e6)
v.check("24-09.6b", poisson_bound(15e6, 1) * 1e9)
v.check("24-09.6c", poisson_bound(15e6, 1) / poisson_bound(15e6))


# ---------------------------------------------------------------- Example 24-09.7, Problem 7, Lab e
def lost(fit, ports_lost, mttr, ports_unit):
    return fit * 1e-9 * YEAR * ports_lost * mttr / ports_unit


p_lost, c_lost = lost(200, 1, 1, 1), lost(400, 8, 24, 8)
v.check("Ex 24-09.7a", p_lost)
v.check("Ex 24-09.7a1", c_lost)
v.check("Ex 24-09.7b", c_lost / p_lost)
v.check("Ex 24-09.7c", c_lost * 60)
v.check("24-09.7a", lost(400, 8, 4, 8) / p_lost)
t_eq = optimize.brentq(lambda t: lost(400, 8, t, 8) - p_lost, 1e-3, 24)
v.check("24-09.7b", t_eq)
v.check("Lab 24-09.e", t_eq)

# ---------------------------------------------------------------- Example 24-09.8, Problem 10
v.check("Ex 24-09.8a", 2.25e9 / 27.2e6)
v.check("Ex 24-09.8b", 1.0 + 2.25 + 2.25)
v.check("Ex 24-09.8c", (1.0 + 2.25) / 0.5)
v.check("Ex 24-09.8d", (1.0 + 2.25 + 2.25) / 1.0)
v.check("Ex 24-09.8e", 100 * 2.25 / 5.5)
v.check("24-09.10a", 100 * 1.0 / 3.25)
v.check("24-09.10b", 100 * 4.5 / 5.5)
v.check("24-09.10c", 1.0 + 2 * 2.25 + 2 * 2.25)

# ---------------------------------------------------------------- audit additions: text, Example 7(c), Problem 13
v.check("Txt 24-09.f", pj(20 - 15, 1600))
v.check("Txt 24-09.g", 4 * 3.2)
chi6 = stats.chi2.ppf(0.95, 6)
v.check("Txt 24-09.h", chi6)
v.check("Txt 24-09.i", chi6 / 20)  # 2 failures in 10T: chi2_{0.95,6}/(2 x 10T)
v.assert_true("2 failures at rate chi6/(20T) over 10T has P(N<=2) = 5%",
              abs(stats.poisson.cdf(2, chi6 / 20 * 10) - 0.05) < 1e-9)
v.check("Txt 24-09.j", 3.5 / (1 - 0.70))
v.check("Txt 24-09.k", 3.5 / (1 - 0.70) / 3.5)
c_swap = lost(400, 128, 24, 8)
v.check("Ex 24-09.7d", c_swap)
v.check("Ex 24-09.7d1", c_swap / p_lost)
v.check("Ex 24-09.7d2", c_swap * 60)
# switch view: 16 engines' failures, each downing all 128 ports, spread over 128 ports
v.assert_true("switch-swap loss equals 16 engines x 128 ports x 24 h / 128 ports",
              abs(lost(16 * 400, 128, 24, 128) - c_swap) < 1e-12)
mu1 = optimize.brentq(lambda m: math.exp(-m) * (1 + m) - 0.05, 0.1, 20)
v.check("24-09.13a", mu1)
v.check("24-09.13a1", stats.chi2.ppf(0.95, 4) / 2)
v.check("24-09.13a", poisson_bound(1e6, 1) * 1e6)  # second route: generic Poisson bound
lam_sw = 16 * 400e-9
u_sw = lam_sw * 24
v.check("24-09.13c0", lam_sw)
v.check("24-09.13c", u_sw)
v.check("24-09.13c1", u_sw / (1 + u_sw))
v.check("24-09.13c2", u_sw * YEAR)
# simulate an alternating renewal process to confirm the down fraction
rng = np.random.default_rng(7)
up = rng.exponential(1 / lam_sw, 200_000)
down = np.full_like(up, 24.0)
v.assert_true("simulated down fraction matches lambda*MTTR/(1+lambda*MTTR) within 2%",
              abs(down.sum() / (up.sum() + down.sum()) / (u_sw / (1 + u_sw)) - 1) < 0.02)

sys.exit(v.finish())
