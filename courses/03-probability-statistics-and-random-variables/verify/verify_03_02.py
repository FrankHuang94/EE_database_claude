#!/usr/bin/env python3
"""Verify every number published in chapter 03-02, its solutions and its lab handout.

Values are recomputed independently of the prose: exact PMF sums with math.comb, Q-function
tails from scipy (cross-checked against erfc and direct numerical integration), numerical
integration of densities, and root finding on the bathtub curve.
"""
from __future__ import annotations

import math
import sys
from math import comb, exp
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erfc
from scipy.stats import binom, norm, poisson

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C = HERE.parent
v = Verifier.from_files("03-02", C / "chapters" / "03-02-random-variables-and-distributions.md",
                        C / "solutions" / "03-02-solutions.md", C / "labs" / "03-02-lab" / "README.md")

HOURS_PER_YEAR = 8766.0
Q, Qinv = norm.sf, norm.isf


def bpmf(n, k, p):
    return comb(n, k) * p**k * (1 - p) ** (n - k)


def ppmf(lam, k):
    return lam**k * exp(-lam) / math.factorial(k)


# ---------------------------------------------------------------- Q-function cross-checks
for x in (0.5, 1, 2, 3, 4.5, 6, 7, 8):
    v.assert_true(f"Q({x}) equals erfc form", abs(Q(x) - 0.5 * erfc(x / math.sqrt(2))) <= 1e-12 * Q(x))
    v.assert_true(f"Q({x}) equals integral of the density",
                  abs(quad(lambda z: exp(-z * z / 2) / math.sqrt(2 * math.pi), x, np.inf)[0] - Q(x)) < 1e-6 * Q(x))
    phi = exp(-x * x / 2) / math.sqrt(2 * math.pi)
    v.assert_true(f"Q bounds at {x}", phi * x / (1 + x * x) < Q(x) < phi / x and Q(x) <= 0.5 * exp(-x * x / 2))
v.assert_true("Gaussian density integrates to 1",
              abs(quad(lambda z: exp(-z * z / 2), -np.inf, np.inf)[0] - math.sqrt(2 * math.pi)) < 1e-10)

# ---------------------------------------------------------------- numbers to know (N) and theory (T)
v.check("N 03-02.a", (1 - 2 * Q(1)) * 100)
v.check("N 03-02.b", (1 - 2 * Q(2)) * 100)
v.check("N 03-02.c", (1 - 2 * Q(3)) * 100)
v.check("N 03-02.d", Q(3))
v.check("N 03-02.e", Q(4.5))
v.check("N 03-02.f", Q(6))
v.check("N 03-02.g", Qinv(1e-9))
v.check("N 03-02.h", Qinv(1e-12))
v.check("N 03-02.i", Qinv(1e-15))
v.check("N 03-02.j", 2 * Qinv(1e-12))
v.check("N 03-02.k", 2 * Qinv(1e-15))

v.check("T 03-02.a", Q(1))
v.check("T 03-02.b", Q(2))
v.check("T 03-02.c", Q(7))
# rho_T = 1: BER = erfc(Q/sqrt2) = 2 Q(Q_BER), so Q(Q_BER) = BER/2
qb1 = brentq(lambda q: erfc(q / math.sqrt(2)) - 1e-12, 5, 9)
v.check("T 03-02.d", 2 * qb1)
v.check("T 03-02.e", (exp(-49 / 2) / (7 * math.sqrt(2 * math.pi)) / Q(7) - 1) * 100)
v.check("T 03-02.f", Q(8))
v.check("T 03-02.g", Q(7) / Q(8))
g1 = 10 ** (1 / 20)
a0 = Qinv(1e-12)
v.check("T 03-02.h", a0 / g1)
v.check("T 03-02.i", Q(a0 / g1))
v.check("T 03-02.j", Q(a0 / g1) / 1e-12)
v.check("T 03-02.k", -math.expm1(-1000e-9 * HOURS_PER_YEAR) * 100)
v.check("T 03-02.l", 1e6 / HOURS_PER_YEAR)

# ---------------------------------------------------------------- Example 03-02.1: known-good die
pk = [bpmf(4, k, 0.1) for k in range(5)]
v.assert_true("KGD PMF sums to 1", abs(sum(pk) - 1) < 1e-15)
for k, key in enumerate("abcde"):
    v.check(f"Ex 03-02.1{key}", pk[k])
v.check("Ex 03-02.1f", pk[0] + pk[1])
v.check("Ex 03-02.1g", (1 - 0.9**4) * 100)

# ---------------------------------------------------------------- Example 03-02.2: fleet soft errors
fit = 11.4 * 100
lam_y = fit * 1e-9 * HOURS_PER_YEAR
v.check("Ex 03-02.2a", fit)
v.check("Ex 03-02.2b", lam_y)
v.check("Ex 03-02.2c", exp(-lam_y))
v.check("Ex 03-02.2g", 5 * lam_y)
v.check("Ex 03-02.2d", -math.expm1(-5 * lam_y))
v.check("Ex 03-02.2e", 1e4 * lam_y)
v.check("Ex 03-02.2f", sum(ppmf(1e4 * lam_y, k) for k in range(81)))
v.assert_true("fleet CDF matches scipy", abs(poisson.cdf(80, 1e4 * lam_y) - sum(ppmf(1e4 * lam_y, k) for k in range(81))) < 1e-12)

# ---------------------------------------------------------------- Example 03-02.3: Poisson vs binomial
n, p = 12_000, 1e-4
for k, key in enumerate("abc"):
    v.check(f"Ex 03-02.3{key}", ppmf(1.2, k))
    v.assert_true(f"binomial agrees with Poisson at k={k} to 4 digits", round(bpmf(n, k, p), 4) == round(ppmf(1.2, k), 4))
v.check("Ex 03-02.3d", 1 - ppmf(1.2, 0) - ppmf(1.2, 1))
v.assert_true("binomial P(>=2) agrees", round(binom.sf(1, n, p), 4) == round(1 - ppmf(1.2, 0) - ppmf(1.2, 1), 4))
pe = -math.expm1(n * math.log1p(-1e-5))
v.assert_true("1 - e^-0.12 matches exact packet error to 4 digits", round(pe, 4) == round(-math.expm1(-0.12), 4))
v.check("Ex 03-02.3e", pe)
v.check("Ex 03-02.3f", pe * (1 - pe))
v.check("Ex 03-02.3g", pe**3)

# ---------------------------------------------------------------- Example 03-02.4: exponential lifetimes
r = 50e-9
v.check("Ex 03-02.4a", -math.expm1(-r * 10 * HOURS_PER_YEAR))
v.check("Ex 03-02.4b", 1 / r)
v.check("Ex 03-02.4c", 1 / r / HOURS_PER_YEAR)
# memoryless: P(T <= 10 y | T > 5 y) computed from the survival function itself
S = lambda t: exp(-r * t)  # noqa: E731
cond = (S(5 * HOURS_PER_YEAR) - S(10 * HOURS_PER_YEAR)) / S(5 * HOURS_PER_YEAR)
v.check("Ex 03-02.4d", cond)
v.assert_true("memoryless: conditional equals unconditional", abs(cond + math.expm1(-r * 5 * HOURS_PER_YEAR)) < 1e-15)
v.check("Ex 03-02.4e", 1e6 * r * HOURS_PER_YEAR)

# ---------------------------------------------------------------- Example 03-02.5: Gaussian tolerances
v.check("Ex 03-02.5a", norm.cdf(9900, 10_000, 50) + norm.sf(10_100, 10_000, 50))
v.check("Ex 03-02.5b", norm.cdf(9850, 10_000, 50) + norm.sf(10_150, 10_000, 50))
v.check("Ex 03-02.5c", norm.cdf(0.72, 0.75, 0.01))
v.check("Ex 03-02.5e", Qinv(1e-6))
v.check("Ex 03-02.5d", norm.ppf(1e-6, 0.75, 0.01))

# ---------------------------------------------------------------- Example 03-02.6: BER
v.check("Ex 03-02.6a", 100 / 15)
v.check("Ex 03-02.6b", Q(100 / 15))
v.check("Ex 03-02.6c", 15 * Qinv(1e-12))
v.check("Ex 03-02.6d", 20 * math.log10(Qinv(1e-12)))
v.check("Ex 03-02.6e", 20 * math.log10(100 / 15))

# ---------------------------------------------------------------- Example 03-02.7: dual-Dirac budget
ui = 1e12 / 32e9
m12, m15 = 2 * Qinv(1e-12), 2 * Qinv(1e-15)
v.check("Ex 03-02.7a", ui)
v.check("Ex 03-02.7b", 8 + m12 * 1.2)
v.check("Ex 03-02.7c", ui - 8 - m12 * 1.2)
v.check("Ex 03-02.7d", (ui - 8 - m12 * 1.2) / ui)
v.check("Ex 03-02.7e", 8 + m15 * 1.2)
v.check("Ex 03-02.7g", (m15 - m12) * 1.2)
v.check("Ex 03-02.7i", 0.7 * ui)
rj_max = (0.7 * ui - 8) / m12
v.check("Ex 03-02.7f", rj_max)
v.check("Ex 03-02.7h", (1 - rj_max / 1.2) * 100)

# ================================================================ solutions
# 1. discrete PMF and CDF
pmf1 = np.array([0.5, 0.3, 0.15, 0.05])
F1 = np.cumsum(pmf1)
v.check("03-02.1a", F1[0])
v.check("03-02.1b", F1[1])
v.check("03-02.1c", F1[2])
v.check("03-02.1d", pmf1[1] + pmf1[2])
v.check("03-02.1e", pmf1[2] + pmf1[3])

# 2. density c x^2 on [0, 2]
c2 = 1 / quad(lambda x: x * x, 0, 2)[0]
v.check("03-02.2a", c2)
v.check("03-02.2b", quad(lambda x: c2 * x * x, 0, 1.5)[0])
v.check("03-02.2c", quad(lambda x: c2 * x * x, 1, 2)[0])

# 3. binomial n = 20, p = 0.05
b3 = [bpmf(20, k, 0.05) for k in range(21)]
v.check("03-02.3a", b3[0])
v.check("03-02.3d", b3[1])
v.check("03-02.3e", b3[2])
v.check("03-02.3b", b3[0] + b3[1])
v.check("03-02.3c", sum(b3[3:]))

# 4. Poisson yield with single-defect repair
lam4 = 0.1 * 2
v.check("03-02.4a", ppmf(lam4, 0))
v.check("03-02.4b", ppmf(lam4, 1))
v.check("03-02.4c", ppmf(lam4, 0) + ppmf(lam4, 1))
v.check("03-02.4d", (1 - ppmf(lam4, 0)) * 100)
v.check("03-02.4e", (1 - ppmf(lam4, 0) - ppmf(lam4, 1)) * 100)

# 5. binomial(50, 0.04) vs Poisson(2)
v.check("03-02.5a", bpmf(50, 0, 0.04))
v.check("03-02.5b", ppmf(2, 0))
v.check("03-02.5c", bpmf(50, 2, 0.04))
v.check("03-02.5d", ppmf(2, 2))
v.check("03-02.5e", (ppmf(2, 0) / bpmf(50, 0, 0.04) - 1) * 100)
v.check("03-02.5f", (1 - ppmf(2, 2) / bpmf(50, 2, 0.04)) * 100)

# 6. geometric retries, failure probability 0.02
v.check("03-02.6a", 0.02**2 * 0.98)
v.check("03-02.6b", 1 - 0.98 - 0.02 * 0.98)

# 7. accelerator SRAM soft errors
fit7 = 15 * 2048
v.check("03-02.7a", fit7)
v.check("03-02.7b", fit7 * 1e-9 * HOURS_PER_YEAR)
v.check("03-02.7c", exp(-fit7 * 1e-9 * HOURS_PER_YEAR))
v.check("03-02.7d", 1e4 * fit7 * 1e-9 * 24)

# 8. MTTF 1e6 h
v.check("03-02.8a", 1e-6 / 1e-9)
v.check("03-02.8b", -math.expm1(-1e-6 * HOURS_PER_YEAR) * 100)
v.check("03-02.8c", exp(-1e-6 * 10 * HOURS_PER_YEAR))
v.check("03-02.8d", 1e6 / HOURS_PER_YEAR)

# 9. series system: the minimum of exponentials, checked by integrating the joint survival
rates = np.array([200, 300, 500]) * 1e-9
t5 = 5 * HOURS_PER_YEAR
v.check("03-02.9a", float(np.prod(np.exp(-rates * t5))))
v.assert_true("min of exponentials is exponential with summed rate",
              abs(np.prod(np.exp(-rates * t5)) - exp(-rates.sum() * t5)) < 1e-15)

# 10. uniform quantization error
v.check("03-02.10a", 2 * quad(lambda e: 1.0, 0.4, 0.5)[0])
v.check("03-02.10b", quad(lambda e: 1.0, -0.5, 0.3)[0])

# 11. supply rail N(1.0, 15 mV), limits +/- 50 mV
out = norm.cdf(0.95, 1.0, 0.015) + norm.sf(1.05, 1.0, 0.015)
k11 = Qinv(0.5e-6)
v.check("03-02.11a", out)
v.check("03-02.11c", out * 1e6)
v.check("03-02.11d", k11)
v.check("03-02.11b", 50 / k11)
v.check("03-02.11e", (1 - (50 / k11) / 15) * 100)
v.check("03-02.11f", out / 1e-6)
v.assert_true("sigma from 11b gives 1 ppm", abs(2 * Q(50 / (50 / k11)) - 1e-6) < 1e-15)

# 12. +/- 1 dB from BER 1e-12
lo, hi = a0 / g1, a0 * g1
v.check("03-02.12f", g1)
v.check("03-02.12g", lo)
v.check("03-02.12a", Q(lo))
v.check("03-02.12b", hi)
v.check("03-02.12c", Q(hi))
v.check("03-02.12d", Q(lo) / Q(a0))
v.check("03-02.12e", Q(a0) / Q(hi))
v.check("03-02.12h", Q(7.034 / g1))

# 13. comparator offset of 0.5 sigma at A/sigma = 6
v.check("03-02.13d", Q(6.5))
v.check("03-02.13e", Q(5.5))
v.check("03-02.13f", Q(5.5) - Q(6))
ber13 = 0.5 * (Q(5.5) + Q(6.5))
v.check("03-02.13a", ber13)
v.check("03-02.13b", Q(6))
v.check("03-02.13c", ber13 / Q(6))
# brute force: integrate the two conditional Gaussian densities across the shifted threshold
th = 0.5
p_err = 0.5 * quad(lambda x: norm.pdf(x, 6, 1), -np.inf, th)[0] + 0.5 * quad(lambda x: norm.pdf(x, -6, 1), th, np.inf)[0]
v.assert_true("offset BER by integration", abs(p_err - ber13) < 1e-3 * ber13)

# 14. 64 GT/s budget
ui14 = 1e12 / 64e9
tj14 = 4 + m12 * 0.4
v.check("03-02.14a", ui14)
v.check("03-02.14b", tj14)
v.check("03-02.14c", ui14 - tj14)
v.check("03-02.14d", (ui14 - tj14) / ui14)
v.check("03-02.14e", math.hypot(0.3, 0.25))
v.check("03-02.14f", math.hypot(0.15, 0.25))
v.check("03-02.14g", math.hypot(0.3, 0.125))
v.check("03-02.14h", m12 * 0.1)
v.check("03-02.14i", m12 * 0.1 / ui14 * 100)

# 15. Six Sigma
v.check("03-02.15a", 2 * Q(6) * 1e9)
v.check("03-02.15b", Q(4.5) + Q(7.5))
v.check("03-02.15d", Q(7.5))
v.check("03-02.15e", Q(1.5))
v.check("03-02.15c", (Q(1.5) + Q(4.5)) * 1e6)

# ================================================================ lab handout
v.check("Lab 03-02.a", 100 / (2 * Q(3)))
v.check("Lab 03-02.b", 100 / (2 * Q(5)))


def tv(nn, lam):
    k = np.arange(0, nn + 1)
    return 0.5 * np.sum(np.abs(binom.pmf(k, nn, lam / nn) - poisson.pmf(k, lam))) + 0.5 * poisson.sf(nn, lam)


v.check("Lab 03-02.c", tv(12, 1.2))
v.check("Lab 03-02.d", tv(12_000, 1.2))
v.assert_true("Le Cam bound holds", all(tv(nn, 1.2) <= 1.2**2 / nn for nn in (12, 120, 1200, 12_000)))
v.check("Lab 03-02.e", exp(-2))
v.check("Lab 03-02.f", exp(-500 / 1000))
eta = 1000 / math.gamma(1 + 1 / 3)
Sw = lambda t: exp(-((t / eta) ** 3))  # noqa: E731
v.assert_true("Weibull mean is 1000 h", abs(quad(Sw, 0, np.inf)[0] - 1000) < 1e-6)
v.check("Lab 03-02.g", Sw(500))
v.check("Lab 03-02.h", quad(Sw, 500, np.inf)[0] / Sw(500))
v.check("Lab 03-02.i", 100 / Q(4))
v.check("Lab 03-02.j", 0.5 * Q(3) + 0.5 * Q(3 + 8 / 1.2))
ber_t = lambda t: Q((t - 4) / 1.2) + Q((31.25 - t - 4) / 1.2)  # noqa: E731
left = brentq(lambda t: math.log(ber_t(t)) - math.log(1e-12), 4, 31.25 / 2)
right = brentq(lambda t: math.log(ber_t(t)) - math.log(1e-12), 31.25 / 2, 31.25 - 4)
v.check("Lab 03-02.k", right - left)
v.check("Lab 03-02.l", 0.5 * (Q(3.5) + Q(4.5)))

sys.exit(v.finish())
