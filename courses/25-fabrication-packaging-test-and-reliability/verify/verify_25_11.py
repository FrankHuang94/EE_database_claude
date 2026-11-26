#!/usr/bin/env python3
"""Verify every number in chapter 25-11 (test: ATE, sort, burn-in and binning), its problems and lab.

Independent routes (the lab module testcost.py integrates over the population and uses scipy.stats.norm):
- escapes and overkill from the bivariate normal CDF of (true, measured) values (scipy multivariate_normal);
- bin fractions from math.erfc;
- burn-in survival by integrating the Weibull hazard numerically;
- break-even efficiencies and guard bands by root-finding on separately written functions.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-11-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-11", ROOT / "chapters" / "25-11-test-ate-sort-burn-in.md",
                        ROOT / "solutions" / "25-11-solutions.md", LAB / "README.md")


def qfun(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def tn(t1, n, eta):
    return t1 + (n - 1) * t1 * (1 - eta)


def cost(rate_h, t1, n, eta, idx):
    return rate_h / 3600 * (tn(t1, n, eta) + idx) / n


def weak_cdf(t, eta_w, beta):
    # F = 1 - exp(-H), H = integral of hazard (beta/eta)(s/eta)^(beta-1)
    h = integrate.quad(lambda s: beta / eta_w * (s / eta_w) ** (beta - 1), 0, t, limit=200)[0]
    return 1 - math.exp(-h)


def bins(mu, s, thr):
    up = [qfun((x - mu) / s) for x in thr]
    return [up[0]] + [up[i + 1] - up[i] for i in range(len(up) - 1)]


def revenue(mu, s, g=0.0):
    f = bins(mu, s, [3.2 + g, 3.0 + g, 2.8 + g])
    return f, f[0] * 500 + f[1] * 400 + f[2] * 300


def esc_ovk(g, mu=3.0, s=0.15, sm=0.02, lim=3.0):
    cov = [[s * s, s * s], [s * s, s * s + sm * sm]]
    mvn = stats.multivariate_normal(mean=[mu, mu], cov=cov)
    p_f_lt = stats.norm.cdf(lim, mu, s)
    p_m_lt = stats.norm.cdf(lim + g, mu, math.sqrt(s * s + sm * sm))
    both_lt = mvn.cdf([lim, lim + g])
    esc = p_f_lt - both_lt            # F < L and M >= L + g
    ovk = p_m_lt - both_lt            # F >= L and M < L + g
    return esc, ovk


# ---------------------------------------------------------------- Example 1
v.check("Ex 25-11.1a0", 250 / 3600)
v.check("Ex 25-11.1a", cost(250, 2.0, 1, 1.0, 0.3))
v.check("Ex 25-11.1b", tn(2.0, 4, 0.9))
v.check("Ex 25-11.1c", cost(250, 2.0, 4, 0.9, 0.3))
v.check("Ex 25-11.1c1", cost(250, 2.0, 4, 0.9, 0.3) / 0.9)
v.check("Ex 25-11.1d", 4 * 2.0 / tn(2.0, 4, 0.9))

# ---------------------------------------------------------------- Example 2
for key, frac in (("", 0.02), ("1", 0.05), ("2", 0.07)):
    v.check(f"Ex 25-11.2a{key}", frac * 30_000)
    v.check(f"Ex 25-11.2b{key}", frac * 30_000 / 500)

# ---------------------------------------------------------------- Examples 3-4
fb = weak_cdf(1200, 100, 0.5)
v.check("Ex 25-11.3a", 24 * 50)
v.check("Ex 25-11.3b", fb)
v.check("Ex 25-11.3c", 1e6 * 0.01 * (1 - fb))
v.check("Ex 25-11.3d", 1e6 * 0.01 * weak_cdf(8766, 100, 0.5))
cond = 1 - (1 - weak_cdf(1200 + 8766, 100, 0.5)) / (1 - fb)
v.check("Ex 25-11.3e0", cond)
v.check("Ex 25-11.3e", 1e6 * 0.01 * (1 - fb) * cond)
teq = optimize.brentq(lambda t: 0.01 * (1 - weak_cdf(t, 100, 0.5)) - 1e-4, 100, 1e5)
v.check("Ex 25-11.4a", teq)
v.check("Ex 25-11.4b", teq / 50)
v.check("Ex 25-11.4c", 100 * (teq / 50 / 24 - 1))

# ---------------------------------------------------------------- Example 5
f0, r0 = revenue(3.0, 0.15)
fg, rg = revenue(3.0, 0.15, 0.05)
v.check("Ex 25-11.5a", f0[0])
v.check("Ex 25-11.5a1", f0[1])
v.check("Ex 25-11.5b", r0)
v.check("Ex 25-11.5c", rg)
v.check("Ex 25-11.5c0", fg[0])
v.check("Ex 25-11.5c1", fg[1])
v.check("Ex 25-11.5c2", fg[2])
v.check("Ex 25-11.5d", r0 - rg)
v.check("Ex 25-11.5d1", 100 * (1 - rg / r0))

# ---------------------------------------------------------------- Example 6
for key, g in (("a", 0.0), ("b", 0.04), ("c", 0.06)):
    e, o = esc_ovk(g)
    v.check(f"Ex 25-11.6{key}", 1e6 * e)
    v.check(f"Ex 25-11.6{key}1", 1e6 * o)

# ---------------------------------------------------------------- Problems
v.check("25-11.1a", 1 - (2.4 - 1.5) / (7 * 1.5))
v.check("25-11.1b", 8 * 1.5 / 2.4)
v.check("25-11.2a", 300 / 3600 * (2.4 + 0.5) / 8)
v.check("25-11.3a", 0.02 / (250 / 3600))
k = 8.617333262e-5
aft = math.exp(0.7 / k * (1 / 328.15 - 1 / 398.15))
v.check("25-11.4a", aft)
v.check("25-11.4b", aft * math.exp(5 * 0.2))
v.check("25-11.4c", 1200 / (aft * math.exp(1)))
f3 = weak_cdf(1200, 100, 0.3)
v.check("25-11.5a", f3)
v.check("25-11.5b", 1e6 * 0.01 * (1 - f3))
teq3 = optimize.brentq(lambda t: 0.01 * (1 - weak_cdf(t, 100, 0.3)) - 1e-4, 1000, 1e6)
v.check("25-11.5c0", teq3)
v.check("25-11.5c", teq3 / 50)
v.check("25-11.6a", 100 * 0.01 * fb)
f10, r10 = revenue(3.0, 0.10)
v.check("25-11.7a", f10[0])
v.check("25-11.7a1", f10[1])
v.check("25-11.7b", r10)
g100 = optimize.brentq(lambda g: esc_ovk(g)[0] - 1e-4, 0.0, 0.1)
v.check("25-11.8a", 1000 * g100)
v.check("25-11.8b", 100 * esc_ovk(g100)[1])
v.check("25-11.9a", 100 * (1128.6 / 779.7 - 1))
v.check("25-11.9b", 100 * 499.1 / 1128.6)
v.check("25-11.9c", 100 * (1863.0 / 1128.6 - 1))
v.check("25-11.10a", 100 * (1306 / 769 - 1))
v.check("25-11.10b", 100 * 1072 / 1306)
v.check("25-11.11a", 9.0 / 1.5)
bad = round(1000 * (1 - 0.86))
v.check("25-11.12a", bad * 3)
v.check("25-11.12b", 1000 * 0.05 + bad * 0.05 * 3)
v.check("25-11.12c", bad * 3 - (1000 * 0.05 + bad * 0.05 * 3))

# ---------------------------------------------------------------- Lab
c4 = cost(250, 2.0, 4, 0.9, 0.3)
v.check("Lab 25-11.a", optimize.brentq(lambda e: cost(250, 2.0, 8, e, 0.3) - c4, 0.1, 1))
v.check("Lab 25-11.b", f3)
v.check("Lab 25-11.c", 1000 * g100)
v.check("Lab 25-11.d", r10)

sys.exit(v.finish())
