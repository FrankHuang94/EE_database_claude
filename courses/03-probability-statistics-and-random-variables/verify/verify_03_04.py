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
# TPDF dither: total error power with nonsubtractive triangular dither, averaged over the input offset
# E[(Q(x + d) - x)^2] for x uniform over one step and d triangular on [-1, 1] (Delta = 1)
xs_ = np.linspace(-0.5, 0.5, 401)
tot_pow = []
for x0 in xs_:
    g = lambda d: (np.round(x0 + d) - x0) ** 2 * max(0.0, 1 - abs(d))  # noqa: E731
    tot_pow.append(quad(g, -1, 1, points=[-0.5 - x0, 0.5 - x0, 1.5 - x0, -1.5 - x0, 0], limit=200)[0])
v.assert_true("TPDF: total error power is 1/4 for every input", max(abs(np.array(tot_pow) - 0.25)) < 1e-9)
v.check("T 03-04.f", 10 * math.log10((1 / 12 + 1 / 6) / (1 / 12)))
# law of total variance on the clustered wafer (enumerated exactly from binomial PMFs)
pb = 0.1
yc_g, ye_g = (0.95 - pb * 0.75) / (1 - pb), (0.80 - pb * 0.50) / (1 - pb)


def wafer_pmf(yc, ye):
    pc, pe = binom.pmf(np.arange(401), 400, yc), binom.pmf(np.arange(201), 200, ye)
    return np.convolve(pc, pe)


pmf_g, pmf_b = wafer_pmf(yc_g, ye_g), wafer_pmf(0.75, 0.50)
kk = np.arange(601)
m_g, m_b = float(kk @ pmf_g), float(kk @ pmf_b)
var_g, var_b = float(kk**2 @ pmf_g) - m_g**2, float(kk**2 @ pmf_b) - m_b**2
mix = (1 - pb) * pmf_g + pb * pmf_b
m_mix = float(kk @ mix)
var_mix = float(kk**2 @ mix) - m_mix**2
within, between = (1 - pb) * var_g + pb * var_b, (1 - pb) * pb * (m_g - m_b) ** 2
v.assert_true("mixture mean is 540", abs(m_mix - 540) < 1e-9)
v.assert_true("total variance law holds on the exact mixture", abs(var_mix - within - between) < 1e-7)
v.check("T 03-04.m", yc_g)
v.check("T 03-04.n", ye_g)
v.check("T 03-04.k", m_g)
v.check("T 03-04.l", var_g)
v.check("T 03-04.g", within)
v.check("T 03-04.h", between)
v.check("T 03-04.i", var_mix)
v.check("T 03-04.j", sqrt(var_mix))
v.check("T 03-04.o", sqrt(49 + 0.5 * 0.5 * 100**2))
# MMSE decomposition on a small joint table: E[(Y - g(X))^2] = E[Var(Y|X)] + E[(E[Y|X] - g(X))^2]
Jm = np.array([[0.2, 0.1, 0.1], [0.05, 0.25, 0.3]])
ysm = np.array([0.0, 1.0, 3.0])
pxm = Jm.sum(1)
cmean = (Jm @ ysm) / pxm
cvar = (Jm @ ysm**2) / pxm - cmean**2
for gx in (np.array([0.0, 0.0]), np.array([1.0, 2.0]), cmean):
    lhs = sum(Jm[i, j] * (ysm[j] - gx[i]) ** 2 for i in range(2) for j in range(3))
    rhs = float(pxm @ cvar) + float(pxm @ (cmean - gx) ** 2)
    v.assert_true("MMSE decomposition", abs(lhs - rhs) < 1e-12)
# jointly Gaussian: completing the square and the factorization (i) x (ii)
for (rr, uu, ww) in ((0.8, 0.3, -1.2), (-0.5, 1.7, 0.4)):
    v.assert_true("completing the square", abs(uu * uu - 2 * rr * uu * ww + ww * ww - ((ww - rr * uu) ** 2 + (1 - rr * rr) * uu * uu)) < 1e-12)
for (xx, yy) in ((0.4, 0.05), (-1.1, -0.2), (2.0, 0.17)):
    fi = norm.pdf(xx, 0, sx)
    fii = norm.pdf(yy, rho * sy * xx / sx, sy * sqrt(1 - rho * rho))
    v.assert_true("bivariate density factors into (i)(ii)", abs(f2(xx, yy) - fi * fii) < 1e-10 * f2(xx, yy))
# Z1, Z2 recipe reproduces the covariance and the variance of a linear combination
a_, b_, sX, sY, r_ = 2.0, -3.0, 1.5, 0.7, 0.6
L = np.array([[sX, 0], [sY * r_, sY * sqrt(1 - r_ * r_)]])
Cv = L @ L.T
v.assert_true("recipe gives the covariance matrix", np.allclose(Cv, [[sX * sX, r_ * sX * sY], [r_ * sX * sY, sY * sY]]))
v.assert_true("linear combination variance", abs((a_ * sX + b_ * r_ * sY) ** 2 + (b_ * sY * sqrt(1 - r_ * r_)) ** 2
                                                 - (a_ * a_ * sX * sX + b_ * b_ * sY * sY + 2 * a_ * b_ * r_ * sX * sY)) < 1e-12)
# Cauchy: tan of a uniform angle and ratio of Gaussians have density 1/(pi(1+x^2)); averages stay Cauchy
cau = lambda x: 1 / (math.pi * (1 + x * x))  # noqa: E731
# P(tan(Theta) <= x) = (atan(x) + pi/2)/pi for Theta uniform on (-pi/2, pi/2); compare with the integrated density
v.assert_true("tan(uniform) is Cauchy", all(abs((math.atan(x) + math.pi / 2) / math.pi - quad(cau, -INF, x)[0]) < 1e-9 for x in (-3, 0.2, 5)))
for zz in (0.0, 0.7, 2.5):
    ratio = 2 * quad(lambda yv: yv * norm.pdf(zz * yv) * norm.pdf(yv), 0, 40)[0]
    v.assert_true("ratio of standard Gaussians is Cauchy", abs(ratio - cau(zz)) < 1e-12)
    s2 = quad(lambda x: cau(x) * cau(2 * zz - x), -INF, INF)[0] * 2      # density of (X1 + X2)/2
    v.assert_true("average of two Cauchy is Cauchy", abs(s2 - cau(zz)) < 1e-9)
v.assert_true("Cauchy mean diverges", quad(lambda x: x * cau(x), 0, 1e6, limit=500)[0] > 4)

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
v.check("03-04.16h", 2.4e-4 * 2 * lb / lam16)
v.check("03-04.16e", -math.expm1(math.log1p(-2 * lb / n) / 10))
v.check("03-04.16g", lam16 / (2 * lb))

# Problem 17: compound Poisson, by exact enumeration of the distribution of S
pk = {1: 0.6, 2: 0.3, 3: 0.1}
EK = sum(k * p_ for k, p_ in pk.items())
VK = sum(k * k * p_ for k, p_ in pk.items()) - EK**2
kpmf = np.zeros(4)
for k, p_ in pk.items():
    kpmf[k] = p_
sp = np.zeros(1)
sp[0] = 1.0
s_pmf = np.zeros(400)
for nn in range(0, 120):
    w_ = poisson.pmf(nn, 4)
    s_pmf[: len(sp)] += w_ * sp[:400]
    sp = np.convolve(sp, kpmf)
ss = np.arange(400)
ES = float(ss @ s_pmf)
VS = float(ss**2 @ s_pmf) - ES**2
v.assert_true("compound PMF sums to 1", abs(s_pmf.sum() - 1) < 1e-12)
v.check("03-04.17a", EK)
v.check("03-04.17b", VK)
v.check("03-04.17c", ES)
v.check("03-04.17d", VS)
v.check("03-04.17e", sqrt(VS))
v.check("03-04.17f", VS / ES)

# Problem 18: min and max of exponentials by integrating survival functions
r1, r2 = 2e-5, 1e-5
v.check("03-04.18a", quad(lambda u: exp(-u), 0, 60)[0] / (r1 + r2))
v.check("03-04.18b", quad(lambda u: exp(-u) * exp(-u * r2 / r1), 0, 60)[0])      # int r1 e^{-r1 t} e^{-r2 t} dt, u = r1 t
mt_max = quad(lambda u: 1 - (1 - exp(-u)) * (1 - exp(-u * r2 / r1)), 0, 80)[0] / r1
v.check("03-04.18c", mt_max)
v.check("03-04.18d", (mt_max * r2 - 1) * 100)

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
