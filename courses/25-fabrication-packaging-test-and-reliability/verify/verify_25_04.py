#!/usr/bin/env python3
"""Verify every number in chapter 25-04 (yield models and die cost), its problems and lab.

Independent routes (the lab module yieldcost.py uses closed forms and a grid search):
- yield models by numerically integrating e^(-AD) against the triangular and gamma densities;
- harvesting by enumerating binomial probabilities;
- exact die counts by counting, for each grid row, the columns whose four corners fit (a row-wise count);
- clustered yield by a Monte Carlo of gamma-mixed Poisson defects;
- learning times by root-finding on the yield curve directly;
- costs and depreciation by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-04", ROOT / "chapters" / "25-04-yield-and-die-cost.md",
                        ROOT / "solutions" / "25-04-solutions.md", LAB / "README.md")


def dpw(d, a):
    return math.pi * d**2 / (4 * a) - math.pi * d / math.sqrt(2 * a)


def y_poisson(x):
    return math.exp(-x)


def y_murphy_num(x):
    """Average e^(-x u) over the triangular density on [0, 2] (u = D/D0)."""
    return integrate.quad(lambda u: (u if u < 1 else 2 - u) * math.exp(-x * u), 0, 2, points=[1])[0]


def y_gamma_num(x, alpha):
    """Average e^(-x u) over a gamma density with shape alpha and mean 1 (u = D/D0)."""
    beta = 1 / alpha
    f = lambda u: u ** (alpha - 1) * math.exp(-u / beta) / (special.gamma(alpha) * beta**alpha)  # noqa: E731
    return integrate.quad(lambda u: f(u) * math.exp(-x * u), 0, np.inf)[0]


def exact_count(d, p, steps=40):
    """Row-wise count: for each row band, columns whose four corners lie inside the circle."""
    r = d / 2
    best = 0
    for ox in np.linspace(0, p, steps, endpoint=False):
        for oy in np.linspace(0, p, steps, endpoint=False):
            total = 0
            for y0 in np.arange(-r - p + oy, r + p, p):
                ymax = max(abs(y0), abs(y0 + p))
                if ymax > r:
                    continue
                half = math.sqrt(r**2 - ymax**2)       # columns need |x|, |x+p| <= half
                xs = np.arange(-r - p + ox, r + p, p)
                total += int(np.sum((xs >= -half) & (xs + p <= half)))
            best = max(best, total)
    return best


# ---------------------------------------------------------------- Example 1
a1 = 10.1**2
v.check("Ex 25-04.1a", a1)
v.check("Ex 25-04.1a1", 300 - 2 * 3)
v.check("Ex 25-04.1b0", math.pi * 294**2 / (4 * a1))
v.check("Ex 25-04.1b1", math.pi * 294 / math.sqrt(2 * a1))
v.check("Ex 25-04.1b", dpw(294, a1))
n_exact = exact_count(294, 10.1)
v.check("Ex 25-04.1c", n_exact)
v.check("Ex 25-04.1c1", 100 * (n_exact / dpw(294, a1) - 1))

# ---------------------------------------------------------------- Example 2
v.check("Ex 25-04.2a", y_poisson(0.1))
v.check("Ex 25-04.2a0", 1 - math.exp(-0.1))
v.check("Ex 25-04.2a1", y_murphy_num(0.1))
v.check("Ex 25-04.2a2", y_gamma_num(0.1, 3))
v.check("Ex 25-04.2a3", y_gamma_num(0.1, 1))
v.check("Ex 25-04.2a4", 1 + 0.1 / 3)
v.check("Ex 25-04.2b", y_poisson(1.0))
v.check("Ex 25-04.2b1", y_murphy_num(1.0))
v.check("Ex 25-04.2b2", y_gamma_num(1.0, 3))
v.check("Ex 25-04.2b3", y_gamma_num(1.0, 1))
v.assert_true("closed forms match numerical averages",
              abs(y_gamma_num(1.0, 3) - (1 + 1 / 3) ** -3) < 1e-9 and abs(y_murphy_num(1.0) - (1 - math.exp(-1)) ** 2) < 1e-9)

# ---------------------------------------------------------------- Example 3
res = {}
for a in (100, 600):
    n = dpw(300, a)
    yy = y_gamma_num(a / 100 * 0.1, 3)
    res[a] = (n, yy, n * yy, 20000 / (n * yy))
v.check("Ex 25-04.3a", res[100][0])
v.check("Ex 25-04.3a1", res[600][0])
v.check("Ex 25-04.3b", res[100][1])
v.check("Ex 25-04.3b1", res[600][1])
v.check("Ex 25-04.3c", res[100][2])
v.check("Ex 25-04.3c1", res[600][2])
v.check("Ex 25-04.3d", res[100][3])
v.check("Ex 25-04.3d1", res[600][3])
v.check("Ex 25-04.3e", res[600][3] / res[100][3])


# ---------------------------------------------------------------- Example 4
def nb(x, alpha):
    return (1 + x / alpha) ** (-alpha)


v.check("Ex 25-04.4a", nb(0.5, 3))
v.check("Ex 25-04.4a1", nb(0.08, 3))
d80 = optimize.brentq(lambda d: y_gamma_num(d, 3) - 0.80, 0.01, 1)
v.check("Ex 25-04.4b", d80)
v.check("Ex 25-04.4b0", d80 - 0.08)


def month_for(tau):
    return optimize.brentq(lambda t: nb(0.08 + 0.42 * math.exp(-t / tau), 3) - 0.80, 0, 100)


v.check("Ex 25-04.4b1", month_for(6))

# ---------------------------------------------------------------- Example 5


def at_least(n, yc, yu, good_min):
    return yu * sum(math.comb(n, k) * yc**k * (1 - yc) ** (n - k) for k in range(good_min, n + 1))


v.check("Ex 25-04.5a", at_least(8, 0.95, 0.97, 8))
v.check("Ex 25-04.5b0", 0.95**8)
v.check("Ex 25-04.5b1", 8 * 0.95**7 * 0.05)
v.check("Ex 25-04.5b", at_least(8, 0.95, 0.97, 7))
added = at_least(8, 0.95, 0.97, 7) - at_least(8, 0.95, 0.97, 8)
v.check("Ex 25-04.5c", added)
v.check("Ex 25-04.5c1", 100 * added / at_least(8, 0.95, 0.97, 8))

# ---------------------------------------------------------------- Examples 6-8
starts = 50000 * 12
v.check("Ex 25-04.6a", starts)
dep = 28e9 / 5 / starts
v.check("Ex 25-04.6b", dep)
v.check("Ex 25-04.6c", 100 * dep / 30000)
v.check("Ex 25-04.6d", 0)
v.check("Ex 25-04.7a", (30000 / 20000) / 1.15)
v.check("Ex 25-04.7a1", (30000 / 18500) / 1.15)
d8 = optimize.brentq(lambda d: math.exp(-d * 1.05) - 0.70, 0.01, 5)
v.check("Ex 25-04.8a", d8)
v.check("Ex 25-04.8b0", d8 * 6)
v.check("Ex 25-04.8b", math.exp(-d8 * 6))
v.check("Ex 25-04.8b1", y_gamma_num(d8 * 6, 3))

# ---------------------------------------------------------------- Problems 1-7
v.check("25-04.1a", y_poisson(0.1))
v.check("25-04.1b", y_poisson(0.8))
v.check("25-04.2b0", (1 - math.exp(-2)) / 2)
v.check("25-04.2b", y_murphy_num(2.0))
v.check("25-04.3a", y_gamma_num(2.0, 1))
v.check("25-04.3b", y_gamma_num(2.0, 3))
v.check("25-04.3c", y_poisson(2.0))
v.check("25-04.3d", y_gamma_num(2.0, 1) / y_poisson(2.0))
v.check("25-04.4a", math.pi * 300**2 / (4 * 750))
v.check("25-04.4b", math.pi * 300 / math.sqrt(1500))
n4 = dpw(300, 750)
v.check("25-04.4c", n4)
y5 = y_gamma_num(0.75, 3)
v.check("25-04.5a", y5)
v.check("25-04.5b", n4 * y5)
c_mono = 30000 / (n4 * y5)
v.check("25-04.5c", c_mono)
ac = 187.5 * 1.1
v.check("25-04.6a", ac)
nc = dpw(300, ac)
v.check("25-04.6b", nc)
yc = y_gamma_num(ac / 100 * 0.1, 3)
v.check("25-04.6c", yc)
c_ch = 30000 / (nc * yc)
v.check("25-04.6d", c_ch)
v.check("25-04.6e", 4 * c_ch)
v.check("25-04.6e1", c_mono - 4 * c_ch)
v.check("25-04.7a", y_poisson(0.2))
from scipy.stats import poisson  # noqa: E402
v.check("25-04.7b", poisson.cdf(2, 0.2))

# ---------------------------------------------------------------- Problems 8-14
v.check("25-04.8a", at_least(16, 0.97, 0.95, 16))
v.check("25-04.8b0", 0.97**16)
v.check("25-04.8b1", 16 * 0.97**15 * 0.03)
v.check("25-04.8b", at_least(16, 0.97, 0.95, 15))
v.check("25-04.9a", month_for(3))
dep3 = 20e9 / 5 / starts
v.check("25-04.10a", dep3)
v.check("25-04.10b", 100 * dep3 / 20000)
v.check("25-04.11a", 30000 / 20000)
v.check("25-04.12a", optimize.brentq(lambda d: y_poisson(d) - 0.5, 0.01, 5))
v.check("25-04.12b", optimize.brentq(lambda d: y_gamma_num(d, 3) - 0.5, 0.01, 5))
lam = 0.3 * 0.3 + 0.2 * 0.5 + 0.4 * 0.2
v.check("25-04.13a", lam)
v.check("25-04.13b", y_poisson(lam))
v.check("25-04.14a", y_poisson(0.15))
v.check("25-04.14b", 0.72 / y_poisson(0.15))

# ---------------------------------------------------------------- Lab
v.check("Lab 25-04.a", n_exact)
rng = np.random.default_rng(9)
dens = rng.gamma(3, 1 / 3, size=(1500, 600))
sim_cl = float(np.mean(rng.poisson(dens) == 0))
v.check("Lab 25-04.b", y_gamma_num(1.0, 3))
v.assert_true("clustered Monte Carlo within 1% of the negative binomial", abs(sim_cl / y_gamma_num(1.0, 3) - 1) < 0.01)
v.check("Lab 25-04.b1", y_poisson(1.0))


def cpmm(a):
    return 20000 / (dpw(300, a) * y_gamma_num(a / 100 * 0.1, 3) * a)


v.check("Lab 25-04.c", optimize.brentq(lambda a: cpmm(a) - 2 * cpmm(50), 60, 800))
v.check("Lab 25-04.d", month_for(3))

sys.exit(v.finish())
