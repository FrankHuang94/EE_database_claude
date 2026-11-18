#!/usr/bin/env python3
"""Verify every number published in chapter 03-05, its solutions and its lab handout.

Interval multipliers come from scipy's t, chi-square and normal quantiles, and are cross-checked
against first principles: the Poisson-chi-square identity by direct summation, the t quantile by
integrating the t density, and the Weibull least-squares fit by the normal equations.
"""
from __future__ import annotations

import math
import sys
from math import exp, log, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import gamma as Gamma
from scipy.stats import chi2, norm, poisson
from scipy.stats import t as tdist

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C = HERE.parent
v = Verifier.from_files("03-05", C / "chapters" / "03-05-estimation-and-hypothesis-testing.md",
                        C / "solutions" / "03-05-solutions.md", C / "labs" / "03-05-lab" / "README.md")
Q, Qinv = norm.sf, norm.isf
K_B = 8.617333262e-5
HOURS_PER_YEAR = 8766.0
z975 = Qinv(0.025)


def t975(nu):
    return tdist.ppf(0.975, nu)


def poisson_upper(c, conf):
    """lambda_U solving P(N <= c; lambda) = 1 - conf, by root finding on the Poisson CDF."""
    return brentq(lambda lam: poisson.cdf(c, lam) - (1 - conf), 1e-9, 100)


def arrhenius(ea, t_use_c, t_stress_c, k=K_B, offset=273.15):
    return exp(ea / k * (1 / (t_use_c + offset) - 1 / (t_stress_c + offset)))


def cpk_se(cpk, n):
    return sqrt(1 / (9 * n) + cpk**2 / (2 * (n - 1)))


# ---------------------------------------------------------------- cross-checks of the tools
for c in (0, 1, 2, 5):
    for conf in (0.6, 0.9, 0.95):
        v.assert_true(f"Poisson bound = chi-square/2 (c={c}, {conf})",
                      abs(poisson_upper(c, conf) - chi2.ppf(conf, 2 * c + 2) / 2) < 1e-9)
for nu in (4, 9):
    dens = lambda x, nu=nu: Gamma((nu + 1) / 2) / (sqrt(nu * math.pi) * Gamma(nu / 2)) * (1 + x * x / nu) ** (-(nu + 1) / 2)  # noqa: E731
    v.assert_true(f"t quantile by integrating the density, nu={nu}", abs(quad(dens, -t975(nu), t975(nu))[0] - 0.95) < 1e-10)
# unbiasedness of S^2 by exact enumeration over a small discrete distribution (n = 3)
vals, probs = np.array([0.0, 1.0, 3.0]), np.array([0.5, 0.3, 0.2])
mu = vals @ probs
var = probs @ (vals - mu) ** 2
es2 = 0.0
for i in range(3):
    for j in range(3):
        for k in range(3):
            x = vals[[i, j, k]]
            es2 += probs[i] * probs[j] * probs[k] * x.var(ddof=1)
v.assert_true("E[S^2] = sigma^2 by enumeration", abs(es2 - var) < 1e-12)

# ---------------------------------------------------------------- theory keys
v.check("T 03-05.a", z975)
v.check("T 03-05.b", t975(4))
v.check("T 03-05.c", t975(29))
v.check("T 03-05.d", t975(99))
for key, (c, conf) in zip("efghijklm", [(c, conf) for conf in (0.6, 0.9, 0.95) for c in (0, 1, 2)]):
    v.check(f"T 03-05.{key}", poisson_upper(c, conf))
v.check("T 03-05.n", 1 - 0.95**20)
v.check("T 03-05.o", 2 * Q(3) * 1e6)
v.check("T 03-05.p", 2 * Q(4) * 1e6)
v.check("T 03-05.q", 2 * Q(5) * 1e6)
v.check("T 03-05.r", 2 * Q(6) * 1e9)
v.check("T 03-05.s", 2 * Qinv(0.25))
v.check("T 03-05.t", cpk_se(1.5, 30))
v.check("T 03-05.u", (1 - exp(-1)) * 100)
v.check("T 03-05.v", arrhenius(0.7, 55, 125, k=8.6e-5, offset=273))
v.check("T 03-05.w", 1000 * arrhenius(0.7, 55, 125) / HOURS_PER_YEAR)
v.check("T 03-05.x", (1 - 0.05 ** (1 / 1000)) * 100)

# ---------------------------------------------------------------- Example 03-05.1
d1 = np.array([1.2, 0.8, 1.5, 0.9, 1.1, 1.4, 0.7, 1.3, 1.0, 1.1])
m1, s1 = d1.mean(), d1.std(ddof=1)
se1 = s1 / sqrt(d1.size)
v.check("Ex 03-05.1a", m1)
v.check("Ex 03-05.1b", s1)
v.check("Ex 03-05.1c", se1)
v.check("Ex 03-05.1d", t975(9))
v.check("Ex 03-05.1e", m1 - t975(9) * se1)
v.check("Ex 03-05.1f", m1 + t975(9) * se1)
v.check("Ex 03-05.1g", z975 * se1)

# ---------------------------------------------------------------- Example 03-05.2
p2 = 912 / 1000
se2 = sqrt(p2 * (1 - p2) / 1000)
v.check("Ex 03-05.2a", p2)
v.check("Ex 03-05.2b", se2)
v.check("Ex 03-05.2c", p2 - z975 * se2)
v.check("Ex 03-05.2d", p2 + z975 * se2)
v.check("Ex 03-05.2e", brentq(lambda p: (1 - p) ** 300 - 0.05, 1e-6, 0.5))

# ---------------------------------------------------------------- Example 03-05.3
lo3, hi3 = chi2.ppf(0.025, 50), chi2.ppf(0.975, 50)
v.check("Ex 03-05.3a", lo3)
v.check("Ex 03-05.3b", hi3)
v.check("Ex 03-05.3c", 50 / hi3)
v.check("Ex 03-05.3d", 50 / lo3)
v.check("Ex 03-05.3e", 10 * math.log10(50 / hi3))
v.check("Ex 03-05.3f", 10 * math.log10(50 / lo3))

# ---------------------------------------------------------------- Example 03-05.4
lam0 = 1e4 * 1140e-9 * HOURS_PER_YEAR
kc = max(k for k in range(200) if poisson.cdf(k, lam0) <= 0.05)
v.check("Ex 03-05.4a", poisson.cdf(80, lam0))
v.check("Ex 03-05.4b", kc)
v.check("Ex 03-05.4c", poisson.cdf(kc, lam0))
v.check("Ex 03-05.4d", poisson.cdf(kc, 0.8 * lam0))
v.check("Ex 03-05.4e", lam0)
v.check("Ex 03-05.4f", 0.8 * lam0)

# ---------------------------------------------------------------- Example 03-05.5
mu5, s5, lsl5, usl5 = 1.205, 0.006, 1.170, 1.230
cpu5, cpl5 = (usl5 - mu5) / (3 * s5), (mu5 - lsl5) / (3 * s5)
cpk5 = min(cpu5, cpl5)
v.check("Ex 03-05.5a", (usl5 - lsl5) / (6 * s5))
v.check("Ex 03-05.5b", cpu5)
v.check("Ex 03-05.5g", cpl5)
v.check("Ex 03-05.5c", cpk5)
v.check("Ex 03-05.5d", (norm.sf(usl5, mu5, s5) + norm.cdf(lsl5, mu5, s5)) * 1e6)
v.check("Ex 03-05.5e", cpk_se(cpk5, 30))
v.check("Ex 03-05.5f", cpk5 - Qinv(0.05) * cpk_se(cpk5, 30))

# ---------------------------------------------------------------- Example 03-05.6 (normal equations, no polyfit)
t6 = np.array([457, 714, 823, 912, 976, 1182, 1600, 1706], float)
n6 = t6.size
F6 = (np.arange(1, n6 + 1) - 0.3) / (n6 + 0.4)
x6, y6 = np.log(t6), np.log(-np.log(1 - F6))
xb, yb = x6.mean(), y6.mean()
g6 = np.sum((x6 - xb) * (y6 - yb)) / np.sum((x6 - xb) ** 2)
a6 = exp(xb - yb / g6)                       # from yb = g*xb - g*ln(alpha)
v.check("Ex 03-05.6a", g6)
v.check("Ex 03-05.6b", a6)
v.check("Ex 03-05.6c", a6 * (-log(0.9)) ** (1 / g6))
v.check("Ex 03-05.6d", quad(lambda tt: exp(-((tt / a6) ** g6)), 0, 20 * a6)[0])    # MTTF = area under R
v.check("Ex 03-05.6e", xb)
v.check("Ex 03-05.6f", yb)
v.check("Ex 03-05.6g", (1 - 0.3) / 8.4)
v.check("Ex 03-05.6h", (8 - 0.3) / 8.4)

# ---------------------------------------------------------------- Example 03-05.7
af7 = arrhenius(0.7, 55, 125)
D7 = 231 * 1000 * af7
v.check("Ex 03-05.7a", af7)
v.check("Ex 03-05.7b", 1000 * af7 / HOURS_PER_YEAR)
v.check("Ex 03-05.7c", D7)
v.check("Ex 03-05.7d", poisson_upper(0, 0.6) / D7 * 1e9)
v.check("Ex 03-05.7e", poisson_upper(0, 0.9) / D7 * 1e9)
v.check("Ex 03-05.7f", poisson_upper(1, 0.9) / D7 * 1e9)
v.check("Ex 03-05.7g", math.ceil(poisson_upper(0, 0.9) * 1e9 / 10 / (1000 * af7)))

# ---------------------------------------------------------------- Example 03-05.8 (two proportions)
pA, pB = 912 / 1000, 931 / 1000
pool = (912 + 931) / 2000
se8 = sqrt(pool * (1 - pool) * (2 / 1000))
z8 = (pB - pA) / se8
v.check("Ex 03-05.8a", pool)
v.check("Ex 03-05.8b", se8)
v.check("Ex 03-05.8c", z8)
v.check("Ex 03-05.8d", norm.sf(z8))
zb8 = norm.isf(0.2)
n8 = (norm.isf(0.05) + zb8) ** 2 * (0.91 * 0.09 + 0.92 * 0.08) / 0.01**2
v.check("Ex 03-05.8e", n8)
v.check("Ex 03-05.8f", math.ceil(n8))
v.check("Ex 03-05.8g", zb8)
# Monte Carlo check of the sample-size formula: power at n8 is close to 0.80
rng8 = np.random.default_rng(2026)
na = math.ceil(n8)
xa, xb8 = rng8.binomial(na, 0.91, 40000), rng8.binomial(na, 0.92, 40000)
pp8 = (xa + xb8) / (2 * na)
zz8 = (xb8 - xa) / na / np.sqrt(pp8 * (1 - pp8) * 2 / na)
v.assert_true("two-proportion sample size gives about 80% power", abs(np.mean(zz8 > norm.isf(0.05)) - 0.80) < 0.01)
# Poisson-chi-square identity: P(N <= c; lam) = P(chi2_{2c+2} > 2 lam)
v.assert_true("Poisson-chi-square identity", all(abs(poisson.cdf(c, lam) - chi2.sf(2 * lam, 2 * c + 2)) < 1e-14
                                                  for c in range(4) for lam in (0.3, 2.0, 7.5)))
# sample-size derivation: power at n = ((z_a + z_b) sigma/delta)^2 equals 1 - beta
nss = ((norm.isf(0.05) + norm.isf(0.1)) * 1.0 / 0.5) ** 2
v.assert_true("sample-size formula gives the stated power", abs(norm.cdf(0.5 * sqrt(nss) / 1.0 - norm.isf(0.05)) - 0.9) < 1e-12)

# ================================================================ solutions
d = np.array([3, 5, 4, 6, 7], float)
v.check("03-05.1a", d.mean())
v.check("03-05.1b", d.var(ddof=1))
v.check("03-05.1c", d.std(ddof=1))
v.check("03-05.1d", d.std(ddof=1) / sqrt(5))
v.check("03-05.1e", d.var(ddof=0))

v.check("03-05.2a", z975 * 2 / 4)
v.check("03-05.2b", 10.3 - z975 * 0.5)
v.check("03-05.2c", 10.3 + z975 * 0.5)

se3 = d.std(ddof=1) / sqrt(5)
v.check("03-05.3a", t975(4) * se3)
v.check("03-05.3b", 5 - t975(4) * se3)
v.check("03-05.3c", 5 + t975(4) * se3)
v.check("03-05.3d", z975 * se3)
v.check("03-05.3e", (t975(4) / z975 - 1) * 100)

v.check("03-05.4a", math.ceil((z975 * 3 / 0.5) ** 2))
v.check("03-05.4b", math.ceil(z975**2 * 0.09 / 0.01**2))
v.check("03-05.4c", math.ceil(z975**2 * 0.25 / 0.01**2))

p5 = 46 / 500
se5 = sqrt(p5 * (1 - p5) / 500)
v.check("03-05.5a", p5)
v.check("03-05.5b", se5)
v.check("03-05.5c", p5 - z975 * se5)
v.check("03-05.5d", p5 + z975 * se5)
v.check("03-05.5e", 1 - 0.05 ** (1 / 1000))

lq, hq = chi2.ppf(0.025, 99), chi2.ppf(0.975, 99)
v.check("03-05.6a", 0.40 * sqrt(99 / hq))
v.check("03-05.6b", 0.40 * sqrt(99 / lq))
v.check("03-05.6c", lq)
v.check("03-05.6d", hq)
m12 = 2 * Qinv(1e-12)
v.check("03-05.6e", m12 * 0.40)
v.check("03-05.6f", m12 * 0.40 * sqrt(99 / lq))

v.check("03-05.7a", 2 / 5e8 * 1e9)
v.check("03-05.7b", poisson_upper(2, 0.9) / 5e8 * 1e9)
v.check("03-05.7c", poisson_upper(0, 0.9) / 5e8 * 1e9)

z8 = (93 - 100) / (20 / 5)
v.check("03-05.8a", z8)
v.check("03-05.8b", norm.cdf(z8))
v.check("03-05.8c", 2 * norm.cdf(z8))

crit = 100 - Qinv(0.05) * 4
v.check("03-05.9a", crit)
v.check("03-05.9b", norm.cdf(crit, 90, 4))
n9 = ((Qinv(0.05) + Qinv(0.10)) * 20 / 10) ** 2
v.check("03-05.9d", n9)
v.check("03-05.9c", math.ceil(n9))

v.check("03-05.10a", 1 - 0.95**20)
v.check("03-05.10b", 0.05 / 20)
v.check("03-05.10c", 1 - (1 - 0.05 / 20) ** 20)

v.check("03-05.11a", 100 / 72)
v.check("03-05.11b", 40 / 36)
v.check("03-05.11c", 60 / 36)
v.check("03-05.11d", (norm.sf(50, 10, 12) + norm.cdf(-50, 10, 12)) * 1e6)
v.check("03-05.11e", 2 * norm.sf(50, 0, 12) * 1e6)
v.check("03-05.11f", brentq(lambda s: 40 / (3 * s) - 4 / 3, 1, 20))

v.check("03-05.12a", cpk_se(1.5, 30))
v.check("03-05.12b", 1.5 - Qinv(0.05) * cpk_se(1.5, 30))
v.check("03-05.12c", math.ceil(brentq(lambda n: 1.5 - Qinv(0.05) * cpk_se(1.5, n) - 1.33, 5, 1000)))

rs = (2.37 - 2.10) / 1.35
v.check("03-05.13a", rs)
v.check("03-05.13b", 2.23 - 6 * rs)
v.check("03-05.13c", 2.23 + 6 * rs)
v.check("03-05.13d", 2.30 - 6 * 0.35)
v.check("03-05.13e", 2.30 + 6 * 0.35)

al, ga = 20.0, 3.0
R14 = lambda tt: exp(-((tt / al) ** ga))  # noqa: E731
v.check("03-05.14a", R14(10))
h = 1e-6
v.check("03-05.14b", -(log(R14(10 + h)) - log(R14(10 - h))) / (2 * h))   # hazard = -d ln R/dt
v.check("03-05.14c", brentq(lambda tt: R14(tt) - 0.9, 0.1, 40))
v.check("03-05.14d", quad(R14, 0, 200)[0])
v.check("03-05.14e", brentq(lambda tt: R14(tt) - 0.5, 0.1, 60))

ea15 = brentq(lambda e: arrhenius(e, 150, 175) - 4000 / 1200, 0.1, 2)
af15 = arrhenius(ea15, 105, 150)
v.check("03-05.15a", ea15)
v.check("03-05.15b", af15)
v.check("03-05.15c", 4000 * af15)
v.check("03-05.15d", 4000 * af15 / HOURS_PER_YEAR)

D16 = poisson_upper(0, 0.6) * 1e9 / 20
N16 = math.ceil(D16 / (1000 * arrhenius(0.7, 55, 125)))
v.check("03-05.16a", D16)
v.check("03-05.16b", N16)
v.check("03-05.16c", arrhenius(0.5, 55, 125))
v.check("03-05.16d", poisson_upper(0, 0.6) / (N16 * 1000 * arrhenius(0.5, 55, 125)) * 1e9)

# ================================================================ lab handout
v.check("Lab 03-05.a", (5 - 1) / 5)
v.check("Lab 03-05.b", 2 * tdist.cdf(1.96, 4) - 1)
v.check("Lab 03-05.c", 2 * tdist.cdf(1.96, 29) - 1)
v.check("Lab 03-05.d", poisson.cdf(kc, 0.8 * lam0))
v.check("Lab 03-05.e", cpk_se(cpk5, 30))
v.check("Lab 03-05.f", cpk_se(cpk5, 125))
lam7 = 150e-9 * 231 * 1000 * 77.65
v.check("Lab 03-05.g", lam7)
v.check("Lab 03-05.h", exp(-lam7))
# coverage: the 90% bound covers 150 FIT whenever c >= 1 (bound at c = 1 is above 150 FIT)
D_lab = 231 * 1000 * 77.65
v.assert_true("bound at c = 1 exceeds 150 FIT and at c = 0 does not",
              poisson_upper(1, 0.9) / D_lab * 1e9 > 150 > poisson_upper(0, 0.9) / D_lab * 1e9)
v.check("Lab 03-05.i", 1 - exp(-lam7))

# ---------------------------------------------------------------- Problem 03-05.17 (paired versus Welch)
bef = np.array([1.20, 0.85, 1.45, 0.95, 1.10, 1.38, 0.72, 1.31])
aft = np.array([1.12, 0.80, 1.36, 0.90, 1.05, 1.27, 0.70, 1.22])
dd = bef - aft
sd17 = dd.std(ddof=1)
t17 = dd.mean() / (sd17 / sqrt(8))
v.check("03-05.17a", dd.mean())
v.check("03-05.17b", sd17)
v.check("03-05.17k", sd17 / sqrt(8))
v.check("03-05.17c", t17)
v.check("03-05.17d", tdist.sf(t17, 7))
sb17, sa17 = bef.std(ddof=1), aft.std(ddof=1)
se17 = sqrt(sb17**2 / 8 + sa17**2 / 8)
nu17 = se17**4 / ((sb17**2 / 8) ** 2 / 7 + (sa17**2 / 8) ** 2 / 7)
v.check("03-05.17e", sb17)
v.check("03-05.17f", sa17)
v.check("03-05.17g", se17)
v.check("03-05.17h", dd.mean() / se17)
v.check("03-05.17i", nu17)
v.check("03-05.17j", tdist.sf(dd.mean() / se17, nu17))

sys.exit(v.finish())
