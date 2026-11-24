#!/usr/bin/env python3
"""Verify every number in chapter 21-11 (link budgets), its problems and its lab.

Independent routes (the lab module linkbudget.py uses closed forms and scipy.integrate.quad):
- the combined shadowing-plus-Rayleigh margin is found from a Gauss-Hermite quadrature of the Suzuki integral
  and cross-checked by a seeded Monte Carlo with a different seed;
- Jakes's area coverage is recomputed by direct numerical integration of P(r) over the disc, not the closed form;
- Shannon's Eb/N0 bound is checked against a numerical solution of C = B log2(1 + (Eb/N0)(R/B)) at C = R;
- the satellite slant range comes from the law of cosines on the Earth-centred triangle;
- path-loss inversions are solved numerically; BER-to-PER uses a binomial sum.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-11-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("21-11", ROOT / "chapters" / "21-11-link-budgets.md",
                        ROOT / "solutions" / "21-11-solutions.md", LAB / "README.md")
lg = math.log10
db10 = lambda x: 10 * lg(x)  # noqa: E731
C = 299_792_458.0
GH_X, GH_W = np.polynomial.hermite.hermgauss(200)


def suzuki_outage(margin, sigma):
    """Gauss-Hermite: x = sqrt(2) sigma t."""
    x = math.sqrt(2) * sigma * GH_X
    return float(np.sum(GH_W * (1 - np.exp(-10 ** (-(margin + x) / 10)))) / math.sqrt(math.pi))


def combined_margin(sigma, p):
    return optimize.brentq(lambda m: suzuki_outage(m, sigma) - p, -30, 80)


def area_coverage_numeric(p_edge, sigma, n):
    m = sigma * special.ndtri(p_edge)
    f = lambda r: 0.5 * special.erfc(-(m - 10 * n * lg(r)) / (sigma * math.sqrt(2))) * 2 * r  # noqa: E731
    return integrate.quad(f, 1e-12, 1, limit=200)[0]


def ebn0_shannon(eta):
    """Solve 1 = log2(1 + x eta)/eta for x = Eb/N0 (C/B = eta)."""
    return db10(optimize.brentq(lambda x: math.log2(1 + x * eta) - eta, 1e-9, 1e6))


def slant(h, el, re=6_371_000.0):
    """Law of cosines: (re + h)^2 = re^2 + d^2 + 2 re d sin(el); solve the quadratic for d."""
    b = 2 * re * math.sin(math.radians(el))
    c = re ** 2 - (re + h) ** 2
    return (-b + math.sqrt(b * b - 4 * c)) / 2


def fspl(f, d):
    return 20 * lg(4 * math.pi * d * f / C)


def per(ber, bits):
    """Probability of at least one error in 'bits' independent bits, as 1 minus the binomial zero-error term."""
    return 1 - math.comb(bits, 0) * (1 - ber) ** bits


def pl_office(d, f=2.44):
    return 23.9 * lg(d) + 30.13 + 24.0 * lg(f)


# ================================================================ chapter text
print("Text")
v.check("Txt 21-11.a", 10 ** (10 / 35))
v.check("Txt 21-11.b", (10 ** (1 / 20) - 1) * 100)
v.check("Txt 21-11.c", (10 ** (1 / 35) - 1) * 100)
v.check("Txt 21-11.d", -db10(-math.log(0.99)))
v.check("Txt 21-11.e", -db10(0.5))
v.check("Txt 21-11.f", -db10(0.25))
v.check("Txt 21-11.g", 20 * lg(slant(600e3, 30) / 600e3))
v.check("Txt 21-11.h", per(0.001, 368) * 100)
v.check("Txt 21-11.i", (30 + 6) - 20)
v.check("Txt 21-11.j", 22 + 148)
rate = lambda sf, bw: sf * bw / 2 ** sf * 0.8  # noqa: E731
v.check("Txt 21-11.k", rate(12, 10.4e3))
v.check("Txt 21-11.l", rate(12, 125e3))
ae = db10((C / 1.9e9) ** 2 / (4 * math.pi))
v.check("Txt 21-11.m", -120 + ae + 30)
v.check("Txt 21-11.n", -110.6 + ae + 30)

print("Example 21-11.1")
pr = -5 - pl_office(20) - 5
sm = 5.01 * special.ndtri(0.9)
v.check("Ex 21-11.1a", -5)
v.check("Ex 21-11.1b", pl_office(1))
v.check("Ex 21-11.1c", pl_office(20))
v.check("Ex 21-11.1d", pr)
v.check("Ex 21-11.1e", pr + 96.5)
v.check("Ex 21-11.1f", sm)
v.check("Ex 21-11.1g", pr + 96.5 - sm)
v.check("Ex 21-11.1h", pr + 70)
v.check("Ex 21-11.1i", optimize.brentq(lambda d: -10 - pl_office(d) - (-70 + sm), 0.5, 100))
v.check("Ex 21-11.1j", pr + 102)

print("Example 21-11.2")
v.check("Ex 21-11.2a", db10(8))
v.check("Ex 21-11.2b", -96.5 + 102)
v.check("Ex 21-11.2c", -95 + 103)
v.check("Ex 21-11.2d", -98.9 + 106.4)
v.check("Ex 21-11.2e", 10 ** (5.5 / 23.9))
v.check("Ex 21-11.2f", 10 ** (db10(8) / 23.9))
v.check("Ex 21-11.2g", ebn0_shannon(1.0))
v.check("Ex 21-11.2h", ebn0_shannon(0.125))
v.check("Ex 21-11.2i", db10(math.log(2)))

print("Example 21-11.3")
for (a, b, c, d), p in ((("a", "b", "c", "d"), 0.1), (("e", "f", "g", "h"), 0.01)):
    ms, mf = 8 * special.ndtri(1 - p), -db10(-math.log(1 - p))
    v.check(f"Ex 21-11.3{a}", ms)
    v.check(f"Ex 21-11.3{b}", mf)
    v.check(f"Ex 21-11.3{c}", ms + mf)
    v.check(f"Ex 21-11.3{d}", combined_margin(8, p))

print("Example 21-11.4")
v.check("Ex 21-11.4a", area_coverage_numeric(0.75, 8, 3.5) * 100)
v.check("Ex 21-11.4b", area_coverage_numeric(0.90, 8, 3.5) * 100)
v.check("Ex 21-11.4c", 8 * special.ndtri(0.75))
v.check("Ex 21-11.4d", 8 * special.ndtri(0.90))
pe = optimize.brentq(lambda p: area_coverage_numeric(p, 8, 3.5) - 0.95, 0.6, 0.95)
v.check("Ex 21-11.4e", pe * 100)
v.check("Ex 21-11.4f", 8 * special.ndtri(pe))
rng = np.random.default_rng(77)
r = np.sqrt(rng.uniform(0, 1, 2_000_000))
for key, p in (("a", 0.75), ("b", 0.90)):
    cov = np.mean(8 * special.ndtri(p) - 35 * np.log10(r) + rng.normal(0, 8, r.size) > 0)
    v.assert_true(f"Monte Carlo area coverage for {p:.0%} edge within 0.1 point", abs(cov - area_coverage_numeric(p, 8, 3.5)) < 1e-3)

print("Example 21-11.5")
rt = lambda bits, cr: 234 * bits * cr / 13.6e-6  # noqa: E731
r0, r9, r11 = rt(1, 0.5), rt(8, 5 / 6), rt(10, 5 / 6)
v.check("Ex 21-11.5a", r0 / 1e6)
v.check("Ex 21-11.5b", r9 / 1e6)
v.check("Ex 21-11.5c", r11 / 1e6)
v.check("Ex 21-11.5d", db10(r11 / r0))
v.check("Ex 21-11.5e", -52 - (-82))
e0, e11 = ebn0_shannon(r0 / 20e6), ebn0_shannon(r11 / 20e6)
v.check("Ex 21-11.5f", e0)
v.check("Ex 21-11.5g", e11)
v.check("Ex 21-11.5h", e11 - e0 + db10(r11 / r0))
v.check("Ex 21-11.5i", 19.5 + 93.8)
v.check("Ex 21-11.5j", 16.5 + 69.0)
v.check("Ex 21-11.5k", (19.5 + 93.8) - (16.5 + 69.0))
v.check("Ex 21-11.5l", 10 ** (((19.5 + 93.8) - (16.5 + 69.0)) / 23.9))

print("Example 21-11.6")
mcl = lambda p, bw, nf: p - db10(bw) + 174 - nf  # noqa: E731
v.check("Ex 21-11.6a", mcl(46, 10e6, 9))
v.check("Ex 21-11.6b", mcl(23, 10e6, 5))
v.check("Ex 21-11.6c", mcl(23, 360e3, 5))
v.check("Ex 21-11.6d", mcl(46, 10e6, 9) - mcl(23, 360e3, 5))
v.check("Ex 21-11.6e", 10 ** (3 / 39.08))

print("Example 21-11.7")
s7 = 23 - 164
n15 = -174 + db10(15e3) + 5
v.check("Ex 21-11.7a", s7)
v.check("Ex 21-11.7b", n15)
v.check("Ex 21-11.7c", s7 - n15)
v.check("Ex 21-11.7d", s7 - (-174 + db10(160) + 5))
need = 10 ** ((1 - (s7 - n15)) / 10)
v.check("Ex 21-11.7e", 2 ** math.ceil(math.log2(need)))

print("Example 21-11.8")
d8 = slant(600e3, 30)
L8 = fspl(2e9, d8)
T8 = 290 + 290 * (10 ** 0.7 - 1)
gt = -db10(T8)
eirp = 34 + db10(30)
cn_dl = eirp - L8 - 5.3 + gt + 228.6
cn_ul = -7 - L8 - 5.3 + 1.1 + 228.6
v.check("Ex 21-11.8a", d8 / 1e3)
v.check("Ex 21-11.8b", L8)
v.check("Ex 21-11.8c", T8)
v.check("Ex 21-11.8d", gt)
v.check("Ex 21-11.8e", eirp)
v.check("Ex 21-11.8f", cn_dl)
v.check("Ex 21-11.8g", cn_dl - db10(30e6))
v.check("Ex 21-11.8h", cn_ul)
v.check("Ex 21-11.8i", cn_ul - db10(360e3))
v.check("Ex 21-11.8j", 360e3 * math.log2(1 + 10 ** ((cn_ul - db10(360e3)) / 10)) / 1e3)

print("Example 21-11.9")
cn9 = -128.5 + 174 - 2
v.check("Ex 21-11.9a", cn9)
v.check("Ex 21-11.9b", cn9 - db10(2e6))
v.check("Ex 21-11.9c", cn9 - db10(1e3))
v.check("Ex 21-11.9d", -128.5 - (-167))
v.check("Ex 21-11.9e", -128.5 - (-148))
v.check("Ex 21-11.9f", -167 + 174 - 2)

# ================================================================ problems
print("Problems")
pr1 = 20 - 2 + 3 - 110 - 8 + 0 - 1
v.check("21-11.1a", 20 - 2 + 3)
v.check("21-11.1b", pr1)
v.check("21-11.1c", pr1 + 95)
v.check("21-11.1d", 6 - (pr1 + 95))
for (k1, k2), n in ((("a", "d"), 2), (("b", "e"), 3), (("c", "f"), 4)):
    v.check(f"21-11.2{k1}", (10 ** (1 / (10 * n)) - 1) * 100)
    v.check(f"21-11.2{k2}", 10 ** (6 / (10 * n)))
v.check("21-11.3a", -174 + db10(1e6) + 12 + 7)
v.check("21-11.3b", -174 + db10(125e3) + 12 + 7)
v.check("21-11.3c", ebn0_shannon(0.1))
v.check("21-11.3d", ebn0_shannon(4.0))
r7 = rt(6, 5 / 6)
v.check("21-11.4a", r7 / 1e6)
v.check("21-11.4b", -64 + 82)
v.check("21-11.4c", db10(r7 / r0))
ms5, mf5 = 6 * special.ndtri(0.95), -db10(-math.log(0.95))
v.check("21-11.5a", ms5)
v.check("21-11.5b", mf5)
v.check("21-11.5c", combined_margin(6, 0.05))
v.check("21-11.5d", ms5 + mf5)
v.check("21-11.6a", area_coverage_numeric(0.90, 6, 3.908) * 100)
v.check("21-11.6b", area_coverage_numeric(0.95, 6, 3.908) * 100)
for key, load in (("a", 0.3), ("b", 0.6), ("c", 0.9)):
    v.check(f"21-11.7{key}", -db10(1 - load))
f8 = 3.5
lgl, lc, lirr = 2 + 0.2 * f8, 5 + 4 * f8, 25.4 + 0.11 * f8
low = 5 - db10(0.3 * 10 ** (-lgl / 10) + 0.7 * 10 ** (-lc / 10))
high = 5 - db10(0.7 * 10 ** (-lirr / 10) + 0.3 * 10 ** (-lc / 10))
v.check("21-11.8a", lgl)
v.check("21-11.8b", lc)
v.check("21-11.8c", lirr)
v.check("21-11.8d", low)
v.check("21-11.8e", high)
v.check("21-11.8f", high - low)
rf = 10 ** (3 / 39.08)
v.check("21-11.9a", rf)
v.check("21-11.9b", rf ** 2)
v.check("21-11.9c", (1 - rf ** -2) * 100)
n375 = -174 + db10(3750) + 5
v.check("21-11.10a", n375)
v.check("21-11.10b", s7 - n375)
v.check("21-11.10c", 2 ** math.ceil(math.log2(10 ** ((1 - (s7 - n375)) / 10))))
v.check("21-11.11a", rate(12, 10.4e3))
v.check("21-11.11b", rate(12, 125e3))
v.check("21-11.11c", 22 + 148)
v.check("21-11.11d", 22 + 137)
v.check("21-11.11e", 10 ** (11 / 35))
c12 = -7 - 190.6 - 5.3 + 19 + 228.6
v.check("21-11.12a", c12)
v.check("21-11.12b", c12 - db10(360e3))
v.check("21-11.13a", ae)
v.check("21-11.13b", -120 + ae + 30)
v.check("21-11.13c", -110.6 + ae + 30)
nfl = -174 + db10(1e6) + 6
v.check("21-11.13d", (-120 + ae + 30) - nfl)
v.check("21-11.13e", (-110.6 + ae + 30) - nfl)
v.check("21-11.13f", (-110.6 + ae + 30 - 3) - nfl)
c14 = -128.5 + 174 - 3
v.check("21-11.14a", c14)
v.check("21-11.14b", c14 - db10(2e6))
v.check("21-11.14c", db10(1023))
v.check("21-11.14d", c14 - db10(1 / 20e-3))
v.check("21-11.15a", per(0.001, 368) * 100)
v.check("21-11.15b", per(0.00017, 255 * 8 + 72) * 100)
v.check("21-11.15c", 255 * 8 + 72)

# ================================================================ lab
print("Lab")
v.check("Lab 21-11.a", -10 - pl_office(10))
v.check("Lab 21-11.b", -10 - pl_office(30))
rng = np.random.default_rng(4242)
m10 = combined_margin(8, 0.1)
out = np.mean(m10 + rng.normal(0, 8, 2_000_000) + 10 * np.log10(rng.exponential(1, 2_000_000)) < 0)
v.check("Lab 21-11.c", out * 100)
v.check("Lab 21-11.d", area_coverage_numeric(0.75, 8, 3.5) * 100)
v.check("Lab 21-11.e", db10(32))
bits = rng.choice([-1.0, 1.0], 100_000)
amp = 10 ** (-10 / 20)
comb = (amp * bits[:, None] + rng.normal(0, 1, (100_000, 32))).mean(axis=1)
gain = db10(amp ** 2 / np.var(comb - amp * bits)) + 10
v.assert_true("simulated coherent repetition gain within 0.05 dB of 10 log 32", abs(gain - db10(32)) < 0.05, f"{gain:.3f}")
for key, el in (("f", 90), ("g", 20)):
    v.check(f"Lab 21-11.{key}", -7 - fspl(2e9, slant(600e3, el)) - 5.3 + 1.1 + 228.6 - db10(360e3))

v.finish()
