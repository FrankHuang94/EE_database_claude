#!/usr/bin/env python3
"""Verify every number published in chapter 03-03, its solutions and its lab handout.

Moments are recomputed by direct summation or numerical integration (not by the closed forms
the chapter derives), and the closed forms are then checked against them. Change-of-variables
densities are checked by integrating them; clipping and PAPR results by quadrature and root
finding.
"""
from __future__ import annotations

import math
import sys
from math import comb, exp, log, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.special import erfc
from scipy.stats import norm, poisson

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C = HERE.parent
v = Verifier.from_files("03-03", C / "chapters" / "03-03-expectation-and-functions-of-rvs.md",
                        C / "solutions" / "03-03-solutions.md", C / "labs" / "03-03-lab" / "README.md")

HOURS_PER_YEAR = 8766.0
K_B_EV = 8.617333262e-5
Q = norm.sf
Qinv = norm.isf
phi = norm.pdf
INF = np.inf


def moments_pmf(values, probs):
    m1 = sum(x * p for x, p in zip(values, probs))
    m2 = sum(x * x * p for x, p in zip(values, probs))
    return m1, m2, m2 - m1 * m1


def clip_power(k):
    """Clipping-noise power of a unit Gaussian clipped at +/-k, by direct quadrature."""
    return 2 * quad(lambda z: (z - k) ** 2 * phi(z), k, INF)[0]


def clip_formula(k):
    return 2 * ((1 + k * k) * Q(k) - k * phi(k))


def snr_db(n_bits, k, clipping=True):
    noise = k * k / (3 * 4.0**n_bits) + (clip_formula(k) if clipping else 0.0)
    return 10 * math.log10(1 / noise)


# ---------------------------------------------------------------- closed forms of section 3.4, checked numerically
for n, p in ((4, 0.1), (20, 0.05), (50, 0.04)):
    pk = [comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)]
    m1, _, var = moments_pmf(range(n + 1), pk)
    v.assert_true(f"binomial({n},{p}) mean and variance", abs(m1 - n * p) < 1e-12 and abs(var - n * p * (1 - p)) < 1e-12)
for lam in (0.2, 1.2, 100.0):
    ks = range(0, int(lam + 40 * sqrt(lam) + 40))
    m1, _, var = moments_pmf(ks, [poisson.pmf(k, lam) for k in ks])
    v.assert_true(f"Poisson({lam}) mean = variance = lambda", abs(m1 - lam) < 1e-9 * max(1, lam) and abs(var - lam) < 1e-8 * max(1, lam))
for q in (0.98, 0.8869, 0.5):
    ks = range(1, 4000)
    m1, _, var = moments_pmf(ks, [(1 - q) ** (k - 1) * q for k in ks])
    v.assert_true(f"geometric({q}) mean 1/q, variance (1-q)/q^2", abs(m1 - 1 / q) < 1e-10 and abs(var - (1 - q) / q**2) < 1e-10)
r_ = 2.5
m1 = quad(lambda t: t * r_ * exp(-r_ * t), 0, INF)[0]
m2 = quad(lambda t: t * t * r_ * exp(-r_ * t), 0, INF)[0]
v.assert_true("exponential mean 1/r and variance 1/r^2", abs(m1 - 1 / r_) < 1e-10 and abs(m2 - m1**2 - 1 / r_**2) < 1e-10)
v.assert_true("exponential mean from survival integral", abs(quad(lambda t: exp(-r_ * t), 0, INF)[0] - 1 / r_) < 1e-10)
v.assert_true("uniform variance w^2/12", abs(quad(lambda x: (x - 1.5) ** 2 / 3, 0, 3)[0] - 9 / 12) < 1e-12)
v.assert_true("Gaussian E[Z^2] = 1, E[Z^4] = 3",
              abs(quad(lambda z: z * z * phi(z), -INF, INF)[0] - 1) < 1e-10 and abs(quad(lambda z: z**4 * phi(z), -INF, INF)[0] - 3) < 1e-9)
s_t = 0.7
v.assert_true("log-normal mean e^(mu + s^2/2)", abs(quad(lambda x: exp(x) * norm.pdf(x, 0.3, s_t), -20, 20)[0] - exp(0.3 + s_t**2 / 2)) < 1e-9)
v.assert_true("clipping formula equals quadrature", all(abs(clip_formula(k) - clip_power(k)) < 1e-12 for k in (1, 2, 3, 4, 5)))

# ---------------------------------------------------------------- theory keys (T)
r_part = 1e-5
v.check("T 03-03.a", quad(lambda u: exp(-u), 0, 60)[0] / r_part)            # integrate in units of 1/r
v.check("T 03-03.b", quad(lambda u: 1 - (1 - exp(-u)) ** 2, 0, 60)[0] / r_part)
v.check("T 03-03.c", 100 / 2**2)
v.check("T 03-03.d", 2 * Q(2) * 100)
v.check("T 03-03.e", 100 / 3**2)
v.check("T 03-03.f", 2 * Q(3) * 100)
v.check("T 03-03.g", sqrt(1 / 1e-6))
v.check("T 03-03.h", Qinv(0.5e-6))
v.check("T 03-03.i", 10 * math.log10(3))             # triangle: crest factor sqrt(3)
v.check("T 03-03.j", Qinv(5e-5))
v.check("T 03-03.k", 10 * math.log10(Qinv(5e-5) ** 2))
for key, p in (("l", 1e-2), ("m", 1e-3), ("o", 1e-6)):
    v.check(f"T 03-03.{key}", 10 * math.log10(log(1 / p)))
v.check("T 03-03.p", 20 * math.log10(2))
v.check("T 03-03.q", 10 * math.log10(3))
for n_bits, kk, sk in ((8, "r", "s"), (12, "t", "u")):
    opt = minimize_scalar(lambda k: -snr_db(n_bits, k), bounds=(2, 8), method="bounded", options={"xatol": 1e-9})
    v.check(f"T 03-03.{kk}", opt.x)
    v.check(f"T 03-03.{sk}", -opt.fun)
v.check("T 03-03.v", snr_db(12, 4))
v.check("T 03-03.w", exp(-(10 ** 1.165)))
# sanity on the PAPR CCDFs: real Gaussian power CCDF is 2Q(sqrt x); complex Gaussian e^-x via a 2-D integral
x_test = 3.0
cplx = quad(lambda rr: rr * exp(-rr * rr / 2), sqrt(2 * x_test), INF)[0]   # |Z|^2/2 with E = 1: R^2 = 2P
v.assert_true("complex Gaussian power CCDF is e^-x", abs(cplx - exp(-x_test)) < 1e-12)
v.assert_true("real Gaussian power CCDF is 2Q(sqrt x)", abs(0.5 * erfc(sqrt(x_test / 2)) * 2 - 2 * Q(sqrt(x_test))) < 1e-15)

# ---------------------------------------------------------------- Example 03-03.1
pk = [comb(4, k) * 0.1**k * 0.9 ** (4 - k) for k in range(5)]
m1, m2, var = moments_pmf(range(5), pk)
v.check("Ex 03-03.1a", m1)
v.check("Ex 03-03.1b", m2)
v.check("Ex 03-03.1c", var)
v.check("Ex 03-03.1d", sqrt(var))
pe = -math.expm1(12_000 * math.log1p(-1e-5))
q = 1 - pe
ks = range(1, 400)
gm1, _, gvar = moments_pmf(ks, [pe ** (k - 1) * q for k in ks])
v.check("Ex 03-03.1e", q)
v.check("Ex 03-03.1f", gm1)
v.check("Ex 03-03.1g", gvar)
v.check("Ex 03-03.1h", sqrt(gvar))

# ---------------------------------------------------------------- Example 03-03.2
mean_good = 400 * 0.95 + 200 * 0.80
var_good = 400 * 0.95 * 0.05 + 200 * 0.80 * 0.20
v.check("Ex 03-03.2a", mean_good)
v.check("Ex 03-03.2b", mean_good / 600)
v.check("Ex 03-03.2c", mean_good * 50)
v.check("Ex 03-03.2d", var_good)
v.check("Ex 03-03.2e", sqrt(var_good))

# ---------------------------------------------------------------- Example 03-03.3 (time averages of the waveform)
tri = lambda t: 1.5 * (4 * abs(t - 0.5) - 1)  # noqa: E731
ms_a = quad(lambda t: (10 + tri(t)) ** 2, 0, 1, points=[0.5])[0]
v.check("Ex 03-03.3a", sqrt(ms_a))
v.check("Ex 03-03.3b", ms_a * 0.004)
v.check("Ex 03-03.3c", (ms_a / 100 - 1) * 100)
ms_b = quad(lambda t: (20 * t) ** 2, 0, 1)[0]
v.check("Ex 03-03.3d", sqrt(ms_b))
v.check("Ex 03-03.3e", ms_b * 0.004)
v.check("Ex 03-03.3f", (ms_b / 100 - 1) * 100)

# ---------------------------------------------------------------- Example 03-03.4
form = quad(lambda t: math.cos(t) ** 2, 0, 2 * math.pi)[0] / (2 * math.pi)
form = sqrt(form) / (quad(lambda t: abs(math.cos(t)), 0, 2 * math.pi)[0] / (2 * math.pi))
eabs = quad(lambda x: abs(x) * phi(x), -INF, INF)[0]
v.check("Ex 03-03.4a", form)
v.check("Ex 03-03.4b", eabs)
v.check("Ex 03-03.4c", form * eabs)
v.check("Ex 03-03.4d", 20 * math.log10(form * eabs))
v.assert_true("meter reading on noise equals sqrt(pi)/2", abs(form * eabs - sqrt(math.pi) / 2) < 1e-12)

# ---------------------------------------------------------------- Example 03-03.5
fy = lambda y: exp(-y / 2) / sqrt(2 * math.pi * y)  # noqa: E731
v.assert_true("chi-square(1) density integrates to 1", abs(quad(fy, 0, INF)[0] - 1) < 1e-8)
ey = quad(lambda y: y * fy(y), 0, INF)[0]
ey2 = quad(lambda y: y * y * fy(y), 0, INF)[0]
v.check("Ex 03-03.5a", sqrt(ey2 - ey**2) / ey)
v.check("Ex 03-03.5b", quad(fy, 4, INF)[0])

# ---------------------------------------------------------------- Example 03-03.6
VT = 1.380649e-23 * 300 / 1.602176634e-19
s = 0.025 / (1.4 * VT)
mean_ln = quad(lambda x: exp(x) * norm.pdf(x, 0, s), -20, 20)[0]
m2_ln = quad(lambda x: exp(2 * x) * norm.pdf(x, 0, s), -20, 20)[0]
v.check("Ex 03-03.6a", VT * 1e3)
v.check("Ex 03-03.6b", s)
v.check("Ex 03-03.6c", mean_ln)
v.check("Ex 03-03.6d", sqrt(m2_ln - mean_ln**2) / mean_ln)
v.check("Ex 03-03.6e", norm.sf(log(2), 0, s))
v.check("Ex 03-03.6f", exp(norm.isf(1e-3, 0, s)))
v.check("Ex 03-03.6g", 1e8 * 1e-9 * mean_ln)

# ---------------------------------------------------------------- Example 03-03.7
x4 = log(1e4)
v.check("Ex 03-03.7a", 10 * math.log10(x4))
# sinusoid: instantaneous power 2cos^2 relative to its average, peak 2
v.check("Ex 03-03.7b", 10 * math.log10(2))
x8 = 10**0.8
v.check("Ex 03-03.7c", exp(-x8))
excess = quad(lambda pw: (pw - x8) * exp(-pw), x8, INF)[0]                # E[(P - c)+] with mean 1
v.check("Ex 03-03.7d", 10 * math.log10(excess))
fR = lambda r: 2 * r * exp(-r * r)  # noqa: E731   Rayleigh with mean power 1
er = quad(lambda r: r * fR(r), 0, INF)[0]
er2 = quad(lambda r: r * r * fR(r), 0, INF)[0]
v.check("Ex 03-03.7e", math.pi / 4 * er2 / (sqrt(x4) * er) * 100)
v.check("Ex 03-03.7f", math.pi / 4 * 100)
v.check("Ex 03-03.7g", math.pi / 4 / sqrt(x4) * 100)

# ================================================================ solutions
m1, m2, var = moments_pmf([0, 1, 2, 3], [0.5, 0.3, 0.15, 0.05])
v.check("03-03.1a", m1)
v.check("03-03.1b", m2)
v.check("03-03.1c", var)
v.check("03-03.1d", sqrt(var))

f2 = lambda x: 3 * x * x / 8  # noqa: E731
e1 = quad(lambda x: x * f2(x), 0, 2)[0]
e2 = quad(lambda x: x * x * f2(x), 0, 2)[0]
v.check("03-03.2a", e1)
v.check("03-03.2b", e2)
v.check("03-03.2c", e2 - e1**2)
v.check("03-03.2d", sqrt(e2 - e1**2))
ey1 = quad(lambda x: (3 * x - 2) * f2(x), 0, 2)[0]
ey2 = quad(lambda x: (3 * x - 2) ** 2 * f2(x), 0, 2)[0]
v.check("03-03.2e", ey1)
v.check("03-03.2f", ey2 - ey1**2)
v.check("03-03.2g", ey2)

from scipy.optimize import brentq  # noqa: E402
v.check("03-03.3a", brentq(lambda t: exp(-t / 1000) - 0.5, 1, 5000))
v.check("03-03.3b", 0)
mode = minimize_scalar(lambda y: -exp(-log(y) ** 2 / (2 * s * s)) / y, bounds=(0.05, 3), method="bounded", options={"xatol": 1e-10}).x
v.check("03-03.3c", mode)


def p_collision(k, n):
    out = 1.0
    for i in range(k):
        out *= 1 - i / n
    return 1 - out


v.check("03-03.4a", comb(302, 2) / 2**16)
v.check("03-03.4b", comb(10_000, 2) / 2**32)
v.assert_true("Markov bound holds for both ID cases",
              p_collision(302, 2**16) <= comb(302, 2) / 2**16 and p_collision(10_000, 2**32) <= comb(10_000, 2) / 2**32)
v.assert_true("exact collision values quoted from 03-01", round(p_collision(302, 2**16), 4) == 0.5007 and round(p_collision(10_000, 2**32), 5) == 0.01157)

ks = range(1, 200)
gm1, _, gvar = moments_pmf(ks, [0.02 ** (k - 1) * 0.98 for k in ks])
v.check("03-03.5a", gm1)
v.check("03-03.5b", gvar)
v.check("03-03.5c", sqrt(gvar))
v.check("03-03.5d", 1 - brentq(lambda qq: 1 / qq - 1.5, 0.1, 1))

v.check("03-03.6a", sqrt(poisson.var(100)))
v.check("03-03.6b", 1 / 2**2)
lo, hi = poisson.cdf(80, 100), poisson.sf(119, 100)
v.check("03-03.6c", lo)
v.check("03-03.6d", hi)
v.check("03-03.6e", lo + hi)
v.check("03-03.6f", 2 * Q(2))

mttf_y = 1 / (1000e-9) / HOURS_PER_YEAR
v.check("03-03.7a", mttf_y)
v.check("03-03.7b", 1e6 * sqrt(quad(lambda u: (u - 1) ** 2 * exp(-u), 0, 80)[0]) / HOURS_PER_YEAR)   # t = 1e6 u hours
v.check("03-03.7c", log(2) * mttf_y)
v.check("03-03.7d", exp(-1))

R1 = lambda t: exp(-r_part * t)  # noqa: E731
R2 = lambda t: 1 - (1 - exp(-r_part * t)) ** 2  # noqa: E731
R3 = lambda t: sum(comb(3, j) * exp(-r_part * t) ** j * (1 - exp(-r_part * t)) ** (3 - j) for j in (2, 3))  # noqa: E731
v.check("03-03.8a", quad(lambda u: R1(u / r_part), 0, 60)[0] / r_part)
v.check("03-03.8b", quad(lambda u: R2(u / r_part), 0, 60)[0] / r_part)
v.check("03-03.8c", quad(lambda u: R3(u / r_part), 0, 60)[0] / r_part)
v.check("03-03.8d", R1(1e4))
v.check("03-03.8e", R3(1e4))
v.check("03-03.8f", brentq(lambda t: R3(t) - R1(t), 1e3, 5e5))
v.assert_true("TMR formula 3e^-2rt - 2e^-3rt", abs(R3(1e4) - (3 * exp(-0.2) - 2 * exp(-0.3))) < 1e-15)

v.check("03-03.9a", 10 * 0.25)
v.check("03-03.9b", sqrt(100 * 0.25))
v.check("03-03.9c", sqrt(100 * 0.25 - 2.5**2))

ms_sig = quad(lambda t: (0.01 * math.cos(t)) ** 2, 0, 2 * math.pi)[0] / (2 * math.pi)
ms_tot = ms_sig + 0.001**2
v.check("03-03.10a", sqrt(ms_tot) * 1e3)
v.check("03-03.10b", 10 * math.log10(ms_tot / 50 / 1e-3))
v.check("03-03.10c", 10 * math.log10(ms_sig / 0.001**2))

a = 1.0
uni_abs = quad(lambda x: abs(x) / (2 * a), -a, a)[0]
uni_rms = sqrt(quad(lambda x: x * x / (2 * a), -a, a)[0])
v.check("03-03.11a", (form * uni_abs / uni_rms - 1) * 100)
v.check("03-03.11b", (form * eabs - 1) * 100)
v.check("03-03.11c", 2 * Q(3) * 100)
v.check("03-03.11d", clip_power(3))
v.check("03-03.11e", (sqrt(1 - clip_power(3)) - 1) * 100)

fyu = lambda y: 1 / (2 * sqrt(y))  # noqa: E731
v.assert_true("density of U^2 integrates to 1", abs(quad(fyu, 0, 1)[0] - 1) < 1e-8)
v.check("03-03.12a", quad(lambda y: y * fyu(y), 0, 1)[0])
v.assert_true("E[U^2] directly", abs(quad(lambda u: u * u, 0, 1)[0] - 1 / 3) < 1e-15)

v.check("03-03.13a", er)
v.check("03-03.13b", brentq(lambda m: quad(fR, 0, m)[0] - 0.5, 0.1, 3))
v.check("03-03.13c", quad(fR, 2 * er, INF)[0])
v.check("03-03.13d", 10 * math.log10(er**2))

ea_k = 0.7 / K_B_EV
rate = lambda tc: exp(-ea_k / (tc + 273.15))  # noqa: E731
hot, cold = rate(85) / rate(65), rate(45) / rate(65)
v.check("03-03.14e", ea_k)
v.check("03-03.14a", hot)
v.check("03-03.14b", cold)
v.check("03-03.14c", (hot + cold) / 2)
v.check("03-03.14d", hot / (hot + cold))
v.assert_true("Jensen: average rate exceeds rate at average temperature", (hot + cold) / 2 > 1)

for k, (g, c, t) in ((3, ("a", "b", "c")), (4, ("d", "e", "f")), (5, ("g", "h", "i"))):
    v.check(f"03-03.15{g}", snr_db(10, k, clipping=False))
    v.check(f"03-03.15{c}", 10 * math.log10(1 / clip_power(k)))
    v.check(f"03-03.15{t}", snr_db(10, k))
opt10 = minimize_scalar(lambda k: -snr_db(10, k), bounds=(2, 8), method="bounded", options={"xatol": 1e-9})
v.check("03-03.15j", opt10.x)
v.check("03-03.15k", -opt10.fun)
v.check("03-03.15l", snr_db(10, opt10.x, clipping=False))
v.check("03-03.15m", 10 * math.log10(1.5 * 4.0**10))


def efficiency(x):
    return math.pi / 4 * er2 / (sqrt(x) * er) * 100


for db, (pk_, ck, ek) in ((6, ("a", "b", "c")), (8, ("d", "e", "f")), (10, ("g", "h", "i"))):
    x = 10 ** (db / 10)
    v.check(f"03-03.16{pk_}", quad(lambda pw: exp(-pw), x, INF)[0])
    v.check(f"03-03.16{ck}", 10 * math.log10(quad(lambda pw: (pw - x) * exp(-pw), x, INF)[0]))
    v.check(f"03-03.16{ek}", efficiency(x))
x30 = brentq(lambda x: exp(-x) - 1e-3, 1, 20)
v.check("03-03.16j", 10 * math.log10(x30))
v.check("03-03.16k", efficiency(x30))

# ================================================================ lab handout
v.check("Lab 03-03.a", 1 / q)
v.check("Lab 03-03.b", mean_good)
v.check("Lab 03-03.c", sqrt(var_good))
v.check("Lab 03-03.d", sqrt(ms_a))
v.check("Lab 03-03.e", 2 * Q(2))
v.check("Lab 03-03.f", mean_ln)
v.check("Lab 03-03.g", 1 / 9)
v.assert_true("three-point distribution has unit variance and meets the bound",
              abs(2 * 9 / 18 - 1) < 1e-15 and abs(2 / 18 - 1 / 9) < 1e-15)
v.check("Lab 03-03.h", 10 * math.log10(x4))
opt8 = minimize_scalar(lambda k: -snr_db(8, k), bounds=(2, 8), method="bounded", options={"xatol": 1e-9})
v.check("Lab 03-03.i", opt8.x)
v.check("Lab 03-03.j", -opt8.fun)
v.check("Lab 03-03.k", snr_db(8, 3))
b_lap = 1 / sqrt(2)
v.check("Lab 03-03.l", 2 * quad(lambda x: exp(-x / b_lap) / (2 * b_lap), 3, INF)[0])

sys.exit(v.finish())
