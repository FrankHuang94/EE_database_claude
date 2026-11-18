#!/usr/bin/env python3
"""Verify every number published in chapter 03-04, its solutions and its lab handout.

Joint-distribution results are recomputed from the joint tables or densities themselves;
convolutions by numerical integration; jointly Gaussian conditionals by integrating the
bivariate density; FEC tails by exact binomial sums with math.comb.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from math import comb, exp, log, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import dblquad, quad
from scipy.optimize import brentq
from scipy.stats import binom, gamma, norm, poisson

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C = HERE.parent
v = Verifier.from_files("03-04", C / "chapters" / "03-04-joint-distributions-and-clt.md",
                        C / "solutions" / "03-04-solutions.md", C / "labs" / "03-04-lab" / "README.md")
Q, Qinv = norm.sf, norm.isf
INF = np.inf


def table_stats(J, xs, ys):
    J = np.asarray(J, float)
    px, py = J.sum(1), J.sum(0)
    ex, ey = float(px @ xs), float(py @ ys)
    exy = float(sum(J[i, j] * xs[i] * ys[j] for i in range(len(xs)) for j in range(len(ys))))
    vx = float(px @ (np.asarray(xs) ** 2)) - ex**2
    vy = float(py @ (np.asarray(ys) ** 2)) - ey**2
    return px, py, ex, ey, exy - ex * ey, vx, vy


def ucr_exact(n, t, ps):
    """Binomial upper tail P(N > t), summed exactly term by term."""
    return sum(comb(n, i) * ps**i * (1 - ps) ** (n - i) for i in range(t + 1, n + 1))


def ser(ber, m=10):
    return -math.expm1(m * math.log1p(-ber))


# ---------------------------------------------------------------- identities used in the theory
# Poisson + Poisson by discrete convolution
l1, l2 = 0.27, 0.05
conv = [sum(poisson.pmf(k, l1) * poisson.pmf(z - k, l2) for k in range(z + 1)) for z in range(8)]
v.assert_true("Poisson sum is Poisson", max(abs(c - poisson.pmf(z, l1 + l2)) for z, c in enumerate(conv)) < 1e-15)
# Gaussian + Gaussian by numerical convolution at a few points
for z in (-2.0, 0.3, 4.0):
    val = quad(lambda x: norm.pdf(x, 1, 1.5) * norm.pdf(z - x, -0.5, 2), -INF, INF)[0]
    v.assert_true(f"Gaussian convolution at {z}", abs(val - norm.pdf(z, 0.5, 2.5)) < 1e-12)
# uncorrelated but dependent: X uniform on [-1, 1], Y = X^2
v.assert_true("Cov(X, X^2) = 0 for symmetric X", abs(quad(lambda x: x**3 / 2, -1, 1)[0]) < 1e-15)
# bivariate Gaussian: marginal and conditional by integration
rho, sx, sy = 0.8, 1.0, 0.1


def f2(x, y, r=rho):
    u, w = x / sx, y / sy
    return exp(-(u * u - 2 * r * u * w + w * w) / (2 * (1 - r * r))) / (2 * math.pi * sx * sy * sqrt(1 - r * r))


v.assert_true("bivariate marginal is Gaussian", abs(quad(lambda y: f2(0.7, y), -2, 2)[0] - norm.pdf(0.7)) < 1e-10)
cm = quad(lambda y: y * f2(1.5, y), -2, 2)[0] / quad(lambda y: f2(1.5, y), -2, 2)[0]
cv = quad(lambda y: (y - cm) ** 2 * f2(1.5, y), -2, 2)[0] / quad(lambda y: f2(1.5, y), -2, 2)[0]
v.assert_true("conditional mean and variance by integration", abs(cm - 0.12) < 1e-10 and abs(cv - 0.0036) < 1e-10)
# polar transform of a complex Gaussian (sigma = 1): Rayleigh envelope, exponential power with mean 2
v.assert_true("Rayleigh density integrates to 1", abs(quad(lambda r: r * exp(-r * r / 2), 0, INF)[0] - 1) < 1e-12)
v.assert_true("power is exponential with mean 2",
              abs(quad(lambda p: exp(-p / 2) / 2, 3, INF)[0] - dblquad(lambda th, r: r * exp(-r * r / 2) / (2 * math.pi), sqrt(3), 12, 0, 2 * math.pi)[0]) < 1e-9)

# ---------------------------------------------------------------- theory keys
v.check("T 03-04.a", 2 * Q(6))
v.check("T 03-04.b", sqrt(2 * (1 - 0.9)))
v.check("T 03-04.c", sqrt(10 * 1.0**2))
v.check("T 03-04.d", sqrt(1 - 0.6**2))
v.check("T 03-04.e", sqrt(1 - 0.8**2))
v.assert_true("12 uniforms minus 6 cannot exceed 6", 12 * 1 - 6 == 6)

# ---------------------------------------------------------------- Example 03-04.1
J1 = [[0.85, 0.05], [0.05, 0.05]]           # rows X = 0, 1; columns Y = 0, 1
px, py, ex, ey, cov, vx, vy = table_stats(J1, [0, 1], [0, 1])
v.check("Ex 03-04.1a", px[1])
v.check("Ex 03-04.1b", J1[1][1] / px[1])
v.check("Ex 03-04.1c", cov)
v.check("Ex 03-04.1d", cov / sqrt(vx * vy))
v.check("Ex 03-04.1e", vx + vy + 2 * cov)
v.check("Ex 03-04.1f", J1[0][0])
v.check("Ex 03-04.1g", px[0] * py[0])

# ---------------------------------------------------------------- Example 03-04.2
for (r, kn, ka) in ((0.9, "a", "b"), (0.0, "c", "d")):
    cov2 = np.array([[100, 100 * r], [100 * r, 100]])
    w = np.array([1, -1])
    sd = sqrt(w @ cov2 @ w)
    v.check(f"Ex 03-04.2{kn}", sd)
    v.check(f"Ex 03-04.2{ka}", 20 * math.log10(2 * 10 / sd))

# ---------------------------------------------------------------- Example 03-04.3 (Delta = 1)
tri = lambda z: max(0.0, 1 - abs(z))  # noqa: E731
v.assert_true("triangle equals convolution of two uniforms",
              all(abs(quad(lambda x: 1.0 * (abs(z - x) <= 0.5), -0.5, 0.5, points=[z - 0.5, z + 0.5])[0] - tri(z)) < 1e-10 for z in (0.0, 0.3, -0.8)))
v.check("Ex 03-04.3a", quad(lambda z: z * z * tri(z), -1, 1, points=[0])[0])
v.check("Ex 03-04.3b", 2 * quad(tri, 0.5, 1)[0])
f3_0 = quad(lambda x: tri(x) * (abs(x) <= 0.5), -0.5, 0.5, points=[0])[0]   # (f*f*f)(0)
v.check("Ex 03-04.3c", f3_0)
v.check("Ex 03-04.3d", norm.pdf(0, 0, sqrt(3 / 12)))

# ---------------------------------------------------------------- Example 03-04.4
v.check("Ex 03-04.4a", (2 / 0.1) ** 2)
v.check("Ex 03-04.4b", (1 - 1 / 9) * 100)
v.check("Ex 03-04.4c", (1 - 2 * Q(3)) * 100)
v.check("Ex 03-04.4d", 10 * math.log10(64))

# ---------------------------------------------------------------- Example 03-04.5 (covariance matrix of 20 gate delays)
ng, sg, sl = 20, 0.6, 0.8
Sig = np.full((ng, ng), sg**2) + np.eye(ng) * sl**2
var_path = float(np.ones(ng) @ Sig @ np.ones(ng))
v.check("Ex 03-04.5a", Sig[0, 1] / sqrt(Sig[0, 0] * Sig[1, 1]))
v.check("Ex 03-04.5b", var_path)
v.check("Ex 03-04.5c", sqrt(var_path))
v.check("Ex 03-04.5d", 200 + 3 * sqrt(var_path))
v.check("Ex 03-04.5e", ng * (10 + 3 * sqrt(Sig[0, 0])))
v.check("Ex 03-04.5f", sqrt(np.trace(Sig)))
v.check("Ex 03-04.5g", 200 + 3 * sqrt(np.trace(Sig)))

# ---------------------------------------------------------------- Example 03-04.6 (conditional by integration)
cmF = 3.0 + cm                                  # cm computed above for x = 1.5, sigma_F = 0.1
csF = sqrt(cv)
v.check("Ex 03-04.6a", cmF)
v.check("Ex 03-04.6b", csF * 1e3)
v.check("Ex 03-04.6c", Q((3.2 - cmF) / csF))
v.check("Ex 03-04.6d", Q((3.2 - 3.0) / 0.1))

# ---------------------------------------------------------------- Example 03-04.7
n, t = 544, 15
ps = ser(2.4e-4)
u_ex = ucr_exact(n, t, ps)
sd7 = sqrt(n * ps * (1 - ps))
z7 = (t + 0.5 - n * ps) / sd7
v.check("Ex 03-04.7a", ps)
v.check("Ex 03-04.7b", n * ps)
v.check("Ex 03-04.7c", u_ex)
v.assert_true("exact sum matches scipy binomial tail", abs(u_ex / binom.sf(t, n, ps) - 1) < 1e-9)
v.check("Ex 03-04.7d", poisson.sf(t, n * ps))
v.check("Ex 03-04.7e", sd7)
v.check("Ex 03-04.7f", z7)
v.check("Ex 03-04.7g", Q(z7))
v.check("Ex 03-04.7h", (t + 1) / (n * 10) * u_ex)
u38 = ucr_exact(n, t, ser(3.8e-4))
v.check("Ex 03-04.7i", u38)
v.check("Ex 03-04.7j", u38 / u_ex)

# ================================================================ solutions
J = [[0.30, 0.20, 0.10], [0.10, 0.15, 0.15]]
px, py, ex, ey, cov, vx, vy = table_stats(J, [0, 1], [0, 1, 2])
for key, val in zip("abcde", (px[0], px[1], py[0], py[1], py[2])):
    v.check(f"03-04.1{key}", val)
v.check("03-04.1f", J[1][2] / px[1])
v.check("03-04.1g", ex)
v.check("03-04.1h", ey)
v.check("03-04.1i", cov)
v.check("03-04.1j", cov / sqrt(vx * vy))
v.check("03-04.1k", vy)

c2 = 1 / dblquad(lambda y, x: x + y, 0, 1, 0, 1)[0]
fxy = lambda y, x: c2 * (x + y)  # noqa: E731
e_x = dblquad(lambda y, x: x * fxy(y, x), 0, 1, 0, 1)[0]
e_x2 = dblquad(lambda y, x: x * x * fxy(y, x), 0, 1, 0, 1)[0]
e_xy = dblquad(lambda y, x: x * y * fxy(y, x), 0, 1, 0, 1)[0]
v.check("03-04.2a", c2)
v.check("03-04.2b", dblquad(fxy, 0, 1, 0, lambda x: 1 - x)[0])
v.check("03-04.2c", e_x)
v.check("03-04.2d", e_xy)
v.check("03-04.2e", e_xy - e_x**2)
v.check("03-04.2f", (e_xy - e_x**2) / (e_x2 - e_x**2))
v.assert_true("covariance is exactly -1/144", Fraction(1, 3) - Fraction(7, 12) ** 2 == Fraction(-1, 144))


def irwin_hall_cdf(x, nn):
    return sum((-1) ** k * comb(nn, k) * (x - k) ** nn for k in range(int(math.floor(x)) + 1)) / math.factorial(nn)


s_tot = sqrt(10) * 20 / sqrt(12)
v.check("03-04.4a", 10 * 10)
v.check("03-04.4b", s_tot)
v.check("03-04.4d", 50 / s_tot)
v.check("03-04.4c", 2 * Q(50 / s_tot))
exact4 = 2 * irwin_hall_cdf(2.5, 10)        # sum of 10 U(0,1) below 2.5 or above 7.5
v.check("03-04.4e", exact4)
v.check("03-04.4f", (2 * Q(50 / s_tot) / exact4 - 1) * 100)

v.check("03-04.5a", sqrt(3**2 + 4**2 + 12**2))
v.check("03-04.5b", sqrt(3**2 + 4**2 + 6**2))
v.check("03-04.5c", sqrt((3 + 4) ** 2 + 12**2))

v.check("03-04.6a", 20 * sqrt(2 * (1 - 0.95)))
v.check("03-04.6b", brentq(lambda r: 20 * sqrt(2 * (1 - r)) - 2, 0, 0.99999))

lam7 = sum(poisson.pmf(k, 0.27) * poisson.pmf(0 - k, 0.05) for k in range(1))
v.check("03-04.7a", lam7)
v.check("03-04.7b", conv[2])

r8 = 1e-5
fT = lambda tt: quad(lambda s: r8 * exp(-r8 * s) * r8 * exp(-r8 * (tt - s)), 0, tt)[0]  # noqa: E731
v.assert_true("Erlang density by convolution", abs(fT(3e4) - r8**2 * 3e4 * exp(-0.3)) < 1e-18)
v.check("03-04.8a", quad(lambda u: u * u * exp(-u), 0, 60)[0] / r8)     # E[T] with t = u/r
v.check("03-04.8b", quad(lambda u: u * exp(-u), 0.1, 60)[0])           # R(0.1/r) = int f
v.check("03-04.8c", 1 - (1 - exp(-0.1)) ** 2)

n9 = (Qinv(0.025) * 5 / 0.5) ** 2
v.check("03-04.9b", n9)
v.check("03-04.9a", math.ceil(n9))

mu10, sd10 = 600 * 0.1, sqrt(600 * 0.1 * 0.9)
v.check("03-04.10a", mu10)
v.check("03-04.10b", sd10)
v.check("03-04.10d", (75.5 - mu10) / sd10)
v.check("03-04.10c", Q((75.5 - mu10) / sd10))
v.check("03-04.10e", binom.sf(75, 600, 0.1))
v.check("03-04.10f", (1 - Q((75.5 - mu10) / sd10) / binom.sf(75, 600, 0.1)) * 100)

Sig11 = np.full((100, 100), 0.01) + np.eye(100) * 0.99
v.check("03-04.11a", sqrt(np.ones(100) @ Sig11 @ np.ones(100)) / 100)
v.check("03-04.11b", sqrt(0.01))

cm12 = 0.75 + 0.9 * (0.73 - 0.75)
cs12 = 0.010 * sqrt(1 - 0.81)
v.check("03-04.12a", cm12)
v.check("03-04.12b", cs12 * 1e3)
v.check("03-04.12c", norm.cdf(0.72, cm12, cs12))
v.check("03-04.12d", norm.cdf(0.72, 0.75, 0.01))

v.check("03-04.13a", quad(lambda r: r * r * exp(-r * r / 2), 0, INF)[0])
v.check("03-04.13b", quad(lambda r: r * exp(-r * r / 2), 3, INF)[0])
v.check("03-04.13c", quad(lambda r: r**3 * exp(-r * r / 2), 0, INF)[0])

S14 = np.array([[4.0, 1.2], [1.2, 1.0]])
w14 = np.array([1, -2])
v.check("03-04.14a", w14 @ S14 @ w14)
a14 = brentq(lambda a: -2 * S14[0, 1] + 2 * a * S14[1, 1], 0, 5)
v.check("03-04.14b", a14)
v.check("03-04.14c", np.array([1, -a14]) @ S14 @ np.array([1, -a14]))

u15 = ucr_exact(n, t, ser(1e-4))
v.check("03-04.15a", u15)
v.check("03-04.15b", poisson.sf(t, n * ser(1e-4)))
v.check("03-04.15e", n * ser(1e-4))
v.check("03-04.15c", brentq(lambda b: log(ucr_exact(n, t, ser(b))) - log(1e-10), 1e-5, 1e-3, xtol=1e-12))
u15c = ucr_exact(528, 7, ser(2.4e-4))
v.check("03-04.15d", u15c)
v.check("03-04.15f", 528 * ser(2.4e-4))
v.check("03-04.15g", u15c / u_ex)

lam16 = n * ps
pr = poisson.sf(15, lam16)
pp = poisson.sf(7, lam16 / 2)
v.check("03-04.16a", pr)
v.check("03-04.16b", pp)
v.check("03-04.16f", pp / pr)
lb = brentq(lambda L: log(poisson.sf(7, L)) - log(pr), 1e-3, 1, xtol=1e-14)
v.check("03-04.16c", lb)
v.check("03-04.16d", 2 * lb)
v.check("03-04.16e", 2.4e-4 * 2 * lb / lam16)
v.check("03-04.16g", lam16 / (2 * lb))

# ================================================================ lab handout
v.check("Lab 03-04.a", 0.05 - 0.1 * 0.1)
v.check("Lab 03-04.b", 0.04 / 0.09)
v.check("Lab 03-04.c", 10 * sqrt(2 * (1 - 0.9)))
v.check("Lab 03-04.d", 10 * sqrt(2 * (1 + 0.5)))
v.check("Lab 03-04.e", f3_0)
tail30 = gamma.sf(30 + 3 * sqrt(30), 30)
v.check("Lab 03-04.f", tail30)
v.check("Lab 03-04.g", tail30 / Q(3))
v.check("Lab 03-04.h", sqrt(math.pi / 2))
v.check("Lab 03-04.i", exp(-4.5))
v.check("Lab 03-04.j", ucr_exact(n, t, ser(1.5e-3)))
v.check("Lab 03-04.k", n * ser(1.5e-3))

sys.exit(v.finish())
