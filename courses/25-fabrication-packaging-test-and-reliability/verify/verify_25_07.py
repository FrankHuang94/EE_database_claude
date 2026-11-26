#!/usr/bin/env python3
"""Verify every number in chapter 25-07 (packaging II), its problems and lab.

Independent routes (the lab module chiplets.py uses vectorized grids and closed forms):
- rectangles per wafer by a row-by-row chord count over grid offsets, in plain Python;
- bond yield from the normal CDF (scipy.stats) and by Monte Carlo; sigma by root-finding on the CDF;
- test escapes by exact rational arithmetic (fractions) from the joint probability table;
- clustered yield as the zero-defect probability of scipy's negative binomial;
- cost break-evens by root-finding on separately written cost functions.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-07", ROOT / "chapters" / "25-07-advanced-packaging-and-chiplets.md",
                        ROOT / "solutions" / "25-07-solutions.md", LAB / "README.md")


def rect_count(w: float, h: float, d: float = 300.0, steps: int = 48) -> int:
    """Whole w x h rectangles inside a circle of diameter d, best over grid offsets, counted row by row."""
    r = d / 2
    best = 0
    for i in range(steps):
        oy = -r + h * i / steps
        for j in range(steps):
            ox = -r + w * j / steps
            total = 0
            y0 = oy - h * math.ceil((oy + r) / h)
            while y0 < r:
                y1 = y0 + h
                ymax = max(abs(y0), abs(y1))
                if ymax <= r:
                    half = math.sqrt(r * r - ymax * ymax)
                    # columns at x0 = ox + k*w with -half <= x0 and x0 + w <= half
                    kmin = math.ceil((-half - ox) / w - 1e-12)
                    kmax = math.floor((half - w - ox) / w + 1e-12)
                    total += max(0, kmax - kmin + 1)
                y0 = y1
            best = max(best, total)
    return best


def dpw_formula(d, a):
    return math.pi * d**2 / (4 * a) - math.pi * d / math.sqrt(2 * a)


def p_within(a, sigma):
    return stats.norm.cdf(a / sigma) - stats.norm.cdf(-a / sigma)


def die_yield(p, sigma):
    return p_within(p / 4, sigma) ** 2


def z_for(target):
    return optimize.brentq(lambda z: p_within(z, 1.0) ** 2 - target, 0.1, 10)


def escape(y, c):
    y, c = Fraction(y), Fraction(c)
    good_pass, bad_pass = y, (1 - y) * (1 - c)
    return float(bad_pass / (good_pass + bad_pass))


def y_nb(area_mm2, d0, alpha):
    lam = area_mm2 / 100 * d0
    return stats.nbinom.pmf(0, alpha, alpha / (alpha + lam))


def cost(areas, d0, alpha=None, c=0.30, t=3.0, pkg=50.0, ya=0.99):
    total = 0.0
    for a in areas:
        y = math.exp(-a / 100 * d0) if alpha is None else y_nb(a, d0, alpha)
        total += (c * a + t) / y
    return (total + pkg) / ya ** len(areas)


def mono(area, d0, alpha=None):
    return cost([area], d0, alpha, pkg=50.0)


def chip(area, d0, alpha=None):
    return cost([area / 4 * 1.1] * 4, d0, alpha, pkg=110.0)


da = 16.5e-6  # copper minus oxide expansion, 1/K

# ---------------------------------------------------------------- Example 1
v.check("Ex 25-07.1a", 3.3 * 26 * 33)
v.check("Ex 25-07.1a1", 3.3 * 830)
v.check("Ex 25-07.1b", 5.5 * 26 * 33)
v.check("Ex 25-07.1c", 120 * 150)
v.check("Ex 25-07.1c1", 9.5 * 830 / (120 * 150))
v.check("Txt 25-07.c", 100 * (858 - 830) / 830)

# ---------------------------------------------------------------- Example 2
for key, ws, in (("a", 1), ("b", 2), ("c", 10)):
    n = 4 / (2 * ws * 1e-3)
    v.check(f"Ex 25-07.2{key}", n)
    v.check(f"Ex 25-07.2{key}1", 2048 / n)

# ---------------------------------------------------------------- Examples 3-4
n_int = rect_count(52, 52)
n_br = rect_count(3, 18)
v.check("Ex 25-07.3a", n_int)
v.check("Ex 25-07.3a1", dpw_formula(300, 52 * 52))
v.check("Ex 25-07.3b", n_br)
v.check("Ex 25-07.3c", n_br / 4)
v.check("Ex 25-07.3d", 52 * 52 / (4 * 3 * 18))
n_a, n_b = rect_count(50, 65), rect_count(75, 105)
v.check("Ex 25-07.4a", n_a)
v.check("Ex 25-07.4b", 1e5 * n_a * 0.95)
v.check("Ex 25-07.4c", n_b)
v.check("Ex 25-07.4d", 1e5 * n_b * 0.95)
v.check("Ex 25-07.4e", 75 * 105 / (50 * 65))
v.check("Ex 25-07.4f", n_a / n_b)

# ---------------------------------------------------------------- Example 5
for key, p in (("a", 9), ("a1", 6), ("a2", 4.5)):
    v.check(f"Ex 25-07.5{key}", 1e6 / p**2)
v.check("Ex 25-07.5b", (1e6 / 6**2) / (1e6 / 9**2))
v.check("Ex 25-07.5b1", (1e6 / 4.5**2) / (1e6 / 6**2))
v.check("Ex 25-07.5c", 9 / 4)
v.check("Ex 25-07.5c1", 6 / 4)
v.check("Ex 25-07.5c2", 4.5 / 4)
v.check("Ex 25-07.5d", 200 / 4)

# ---------------------------------------------------------------- Example 6
y6 = die_yield(6, 0.5)
v.check("Ex 25-07.6a0", p_within(3, 1))
v.check("Ex 25-07.6a", 100 * y6)
v.check("Txt 25-07.b", 1 / (1 - y6))
z = z_for(0.999)
v.check("Ex 25-07.6b0", z)
v.check("Ex 25-07.6b", 1.5 / z)
v.check("Ex 25-07.6b1", 3 * 1.5 / z)
v.check("Ex 25-07.6c0", 0.5 / 3)
v.check("Ex 25-07.6c", 4 * z * 0.5 / 3)
v.check("Ex 25-07.6d0", p_within(1.5, 1))
v.check("Ex 25-07.6d", 100 * die_yield(1, 0.5 / 3))
rng = np.random.default_rng(7)
e = rng.normal(0, 0.5, size=(400_000, 2))
v.assert_true("Monte Carlo die yield at sigma = p/12 within 0.1 point of formula",
              abs(np.mean(np.all(np.abs(e) <= 1.5, axis=1)) - y6) < 1e-3)

# ---------------------------------------------------------------- Example 7
v.check("Ex 25-07.7a", 5e-9 / (da * 1.0e-6))
v.check("Ex 25-07.7a1", 25 + 5e-9 / (da * 1.0e-6))
v.check("Ex 25-07.7b", 2e-9 / (da * 1.0e-6))
v.check("Ex 25-07.7c", 5e-9 / (da * 2.0e-6))
v.check("Txt 25-07.d", 100 * (1 - 2 / 5))

# ---------------------------------------------------------------- Example 8
e1 = escape("0.8", "0.99")
yp1 = 0.998**10 * (1 - e1) ** 2 * 0.995**8
v.check("Ex 25-07.8a", 100 * e1)
v.check("Ex 25-07.8b", yp1)
v.check("Ex 25-07.8b1", 4200 / yp1)
v.check("Ex 25-07.8b2", 4200 / yp1 - 4200)
e2 = escape("0.8", "0.999")
yp2 = 0.998**10 * (1 - e2) ** 2 * 0.995**8
v.check("Ex 25-07.8c", 100 * e2)
v.check("Ex 25-07.8c1", yp2)
v.check("Ex 25-07.8c2", 4200 / yp1 - 4200 / yp2)

# ---------------------------------------------------------------- Example 9
v.check("Ex 25-07.9a", math.exp(-0.8))
v.check("Ex 25-07.9a1", math.exp(-0.22))
cm, cc = mono(800, 0.1), chip(800, 0.1)
v.check("Ex 25-07.9b", cm)
v.check("Ex 25-07.9c", cc)
v.check("Ex 25-07.9d", cc / cm)
v.check("Ex 25-07.9e", optimize.brentq(lambda d: mono(800, d) - chip(800, d), 0.001, 1))
be_area = optimize.brentq(lambda a: mono(a, 0.1) - chip(a, 0.1), 100, 2000)
v.check("Txt 25-07.a", be_area)

# ---------------------------------------------------------------- Problems
v.check("25-07.1a", 14 * 858)
v.check("25-07.1a1", 14 * 830)
v.check("25-07.1b", 100 * (14 * 858 - 14 * 830) / (14 * 830))
v.check("25-07.1c", 6864 / 8)
v.check("25-07.1c1", 7722 / 9)
v.check("25-07.2a", (55 / 45) ** 2)
v.check("25-07.2b", (45 / 35) ** 2)
v.check("25-07.2c", (45 / 36) ** 2)
v.check("25-07.2c1", 100 * ((45 / 36) ** 2 - 1))
v.check("25-07.2d", min((35, 36), key=lambda p: abs((45 / p) ** 2 - 1.65)))
v.check("25-07.3a", 2 / 0.004)
v.check("25-07.3b", 2048 / 500)
v.check("25-07.3c0", 2048 / 2 * 0.004)
v.check("25-07.3c", math.ceil(2048 / 2 * 0.004))
n40 = rect_count(40, 40)
v.check("25-07.4a", n40)
v.check("25-07.4b", dpw_formula(300, 1600))
v.check("25-07.4c", 120_000 * n40 * 0.95)
v.check("25-07.5a", 1.275e6 / 12)
v.check("25-07.5b", 100 * (2.73 / 1.275 - 1))
v.check("25-07.5b1", 100 * (3.48 / 2.73 - 1))
v.check("25-07.5c", 100 * (250 / 160 - 1))
v.check("25-07.5d", 1.8**5)
v.check("25-07.5d1", 2**3)
v.check("25-07.5e", 12_000 * 1e6 / 3e6)
v.check("25-07.5e1", 12_000 * 1e6 / 2e6)
v.check("25-07.5e2", math.sqrt(12_000 * 1e6 / 3e6))
v.check("25-07.5e3", math.sqrt(12_000 * 1e6 / 2e6))
rc = math.hypot(5, 5)
v.check("25-07.6a", rc)
v.check("25-07.6b", 1.5e-3 / rc * 1e6)
v.check("25-07.6c", math.degrees(1.5e-3 / rc))
v.check("25-07.7a", 3e-9 / (da * 0.5e-6))
v.check("25-07.7b", da * 1.0e-6 * 225 * 1e9)
v.check("25-07.8b", 100 * escape("0.5", "0.99"))
v.check("25-07.8b1", 100 * 0.5 * 0.01 / 0.5)
v.check("25-07.8c", 100 * escape("0.95", "0.99"))
v.check("25-07.8c1", escape("0.5", "0.99") / escape("0.95", "0.99"))
yp9 = 0.998**14 * (1 - e1) ** 2 * 0.995**12
v.check("25-07.9a", yp9)
v.check("25-07.9b", 5400 / yp9)
v.check("25-07.9c", 5400 / yp9 - 5400)
for key, d0 in (("a", 0.1), ("b", 0.2), ("c", 0.05)):
    v.check(f"25-07.10{key}", optimize.brentq(lambda a: mono(a, d0) - chip(a, d0), 100, 3000))
v.check("25-07.11a", y_nb(800, 0.1, 2))
v.check("25-07.11a1", y_nb(220, 0.1, 2))
cm2, cc2 = mono(800, 0.1, 2), chip(800, 0.1, 2)
v.check("25-07.11b", cm2)
v.check("25-07.11b1", cc2)
v.check("25-07.11c", cc2 / cm2)
v.check("25-07.11c1", 100 * (1 - cc2 / cm2))
v.check("25-07.11c2", 100 * (1 - cc / cm))
be_nb = optimize.brentq(lambda d: mono(800, d, 2) - chip(800, d, 2), 0.001, 1)
v.check("25-07.11d", be_nb)
v.check("25-07.12a", (900 - 160) / 20)
v.check("25-07.12b", (900 - 160) / 20 - 10)
v.check("25-07.13a", 5.5 * 858 / (6 * 54))
v.check("25-07.13b", n_br // 6)
v.check("25-07.13c", rect_count(55, 86))
v.check("25-07.14a", 4.5 / 4 / z)
v.check("25-07.14a1", 3 * 4.5 / 4 / z)
v.check("25-07.14b", z * 0.5 / 3)
v.assert_true("required tolerance exceeds half of a 1 um pitch", z * 0.5 / 3 > 0.5)

# ---------------------------------------------------------------- Lab
v.check("Lab 25-07.a", n_a)
v.check("Lab 25-07.a1", dpw_formula(300, 50 * 65))
v.check("Lab 25-07.b", 100 * die_yield(6, 0.6))
v.check("Lab 25-07.c", be_nb)
v.check("Lab 25-07.d", be_area)

sys.exit(v.finish())
