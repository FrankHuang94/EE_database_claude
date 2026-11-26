#!/usr/bin/env python3
"""Verify every number in chapter 25-09 (reliability physics), its problems and lab.

Independent routes (the lab module reliability.py uses closed forms):
- the EM local exponent by a numerical derivative of ln MTTF, and its inverse by root-finding;
- TDDB models fitted by least squares in transformed coordinates (ln t against E, 1/E and ln E);
- chip-level percentiles from scipy's weibull_min for the minimum of M Weibull lives; lognormal percentiles
  from scipy's lognorm;
- the HBM discharge by integrating the circuit ODE (solve_ivp), including the energy in the clamp;
- HTOL bounds from scipy's chi2, with a Poisson Monte Carlo of the pass probability.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-09-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-09", ROOT / "chapters" / "25-09-reliability-physics.md",
                        ROOT / "solutions" / "25-09-solutions.md", LAB / "README.md")

K = 8.617333262e-5
YEAR = 3.15576e7  # s
H_YEAR = 8766.0   # h


def af(ea, t_use, t_stress, k=K, off=273.15):
    return math.exp(ea / k * (1 / (t_use + off) - 1 / (t_stress + off)))


def mttf2(j, b=1.0, c=1.0):
    return b / j**2 + c / j


def local_n(x):
    h = 1e-6
    return -(math.log(mttf2(x * (1 + h))) - math.log(mttf2(x * (1 - h)))) / (math.log(1 + h) - math.log(1 - h))


def fits(points):
    e = np.array([p[0] for p in points], float)
    lt = np.log([p[1] for p in points])
    out = {}
    for name, xcol in (("E", e), ("1/E", 1 / e), ("power", np.log(e))):
        a = np.vstack([np.ones_like(xcol), xcol]).T
        c0, c1 = np.linalg.lstsq(a, lt, rcond=None)[0]
        out[name] = (c0, c1)
    return out


def predict(f, name, e):
    c0, c1 = f[name]
    x = {"E": e, "1/E": 1 / e, "power": math.log(e)}[name]
    return math.exp(c0 + c1 * x)


def chip_life(area_ratio, frac, beta, eta=1.0):
    # minimum of M Weibull(beta, eta) lives is Weibull(beta, eta M^(-1/beta))
    return stats.weibull_min.ppf(frac, beta, scale=eta * area_ratio ** (-1 / beta))


def hbm_sim(v0, vh, ron, r=1500.0, c=100e-12):
    def rhs(t, y):
        vc, e_cl = y
        i = max(vc - vh, 0.0) / (r + ron)
        return [-i / c, vh * i + ron * i * i]
    tau = (r + ron) * c
    sol = integrate.solve_ivp(rhs, (0, 20 * tau), [v0, 0.0], rtol=1e-10, atol=1e-12, dense_output=True)
    i_at = lambda t: max(sol.sol(t)[0] - vh, 0) / (r + ron)  # noqa: E731
    return i_at(0.0), tau, vh + i_at(0.0) * ron, i_at(tau), sol.y[1, -1]


def fit_bound(chi, n, t, a):
    return chi / (2 * n * t * a) * 1e9


# ---------------------------------------------------------------- Example 1
a9 = af(0.90, 105, 300)
v.check("Ex 25-09.1a", a9)
v.check("Ex 25-09.1b", 100 * a9 * 5**2)
v.check("Ex 25-09.1b1", 100 * a9 * 5**2 / H_YEAR)
v.check("Ex 25-09.1c", 100 * a9 * 5)
v.check("Ex 25-09.1c1", 100 * a9 * 5 / H_YEAR)
a83 = af(0.83, 105, 300)
v.check("Ex 25-09.1d", a83)
v.check("Ex 25-09.1d1", a9 / a83)

# ---------------------------------------------------------------- Example 2
v.check("Ex 25-09.2a", local_n(0.2))
v.check("Ex 25-09.2a1", local_n(1.0))
v.check("Ex 25-09.2a2", local_n(5.0))
true_ratio = mttf2(0.2) / mttf2(5.0)
extrap = 25 ** local_n(5.0)
v.check("Ex 25-09.2b", true_ratio)
v.check("Ex 25-09.2b1", extrap)
v.check("Ex 25-09.2b2", true_ratio / extrap)

# ---------------------------------------------------------------- Example 3
v.check("Ex 25-09.3a", 3000 / 20e-4 / 1e6)
v.check("Ex 25-09.3b", 3000 / 2e6 * 1e4)

# ---------------------------------------------------------------- Examples 4-5
f4 = fits([(10, 10), (9, 100)])
v.check("Ex 25-09.4a", -f4["E"][1])
v.check("Ex 25-09.4b", f4["1/E"][1])
v.check("Ex 25-09.4c", -f4["power"][1])
tE, tP, tI = predict(f4, "E", 3), predict(f4, "power", 3), predict(f4, "1/E", 3)
v.check("Ex 25-09.4d", tE)
v.check("Ex 25-09.4d1", tP)
v.check("Ex 25-09.4d2", tI)
scale = chip_life(1000, 1e-4, 2)
v.check("Ex 25-09.5a", scale)
v.check("Ex 25-09.5a0", 1000 ** -0.5)
v.check("Ex 25-09.5a1", (-math.log(1 - 1e-4)) ** 0.5)
need = 10 * YEAR / scale
v.check("Ex 25-09.5b", need)
v.check("Ex 25-09.5c", tP / need)
v.assert_true("E model fails, power law and 1/E pass", tE < need < tP < tI)

# ---------------------------------------------------------------- Example 6
ratio = 10 * YEAR / 1e3
s6 = 3 * ratio ** (1 / 6)
s4 = 3 * ratio ** 0.25


def delay(vth):
    return 0.75 / (0.75 - vth) ** 1.3


v.check("Ex 25-09.6a", ratio)
v.check("Ex 25-09.6b", s6)
v.check("Ex 25-09.6c", s4)
v.check("Ex 25-09.6f", 0.75 - 0.30 - s6 / 1000)
v.check("Ex 25-09.6g", 0.75 - 0.30 - s4 / 1000)
v.check("Ex 25-09.6d", 100 * (delay(0.30 + s6 / 1000) / delay(0.30) - 1))
v.check("Ex 25-09.6e", 100 * (delay(0.30 + s4 / 1000) / delay(0.30) - 1))

# ---------------------------------------------------------------- Example 7
ipk, tau, vpk, itau, e_cl = hbm_sim(2000, 5, 1)
v.check("Ex 25-09.7a", ipk)
v.check("Ex 25-09.7b", tau * 1e9)
v.check("Ex 25-09.7c", vpk)
v.check("Ex 25-09.7d", itau)
v.check("Ex 25-09.7f", e_cl * 1e6)
v.check("Ex 25-09.7e", optimize.brentq(lambda ron: hbm_sim(2000, 5, ron)[2] - 8, 0.01, 50))

# ---------------------------------------------------------------- Example 8
chi = stats.chi2.ppf(0.60, 2)
a_ti = af(0.7, 55, 125, k=8.6e-5, off=273)
a_ex = af(0.7, 55, 125)
fit_ti = fit_bound(chi, 7859, 1000, a_ti)
v.check("Ex 25-09.8a", a_ti)
v.check("Ex 25-09.8b", chi)
v.check("Ex 25-09.8c", fit_ti)
v.check("Ex 25-09.8d", a_ex)
v.check("Ex 25-09.8d1", fit_bound(chi, 7859, 1000, a_ex))
v.check("Ex 25-09.8e", 1e9 / fit_ti)
v.check("Ex 25-09.8f", 16.7 * af(0.7, 55, 75))
fit06 = fit_bound(chi, 7859, 1000, af(0.6, 55, 125, k=8.6e-5, off=273))
v.check("Ex 25-09.8g", fit06)
v.check("Ex 25-09.8g1", fit06 / fit_ti)
v.check("Ex 25-09.8h", af(0.7, 55, 75))
v.check("Txt 25-09.a", af(0.8, 55, 125) / af(0.7, 55, 125))

# ---------------------------------------------------------------- Example 9
rates = [(2, 0.9), (3, 0.7), (1, 0.5)]
v.check("Ex 25-09.9a", af(0.9, 55, 85))
v.check("Ex 25-09.9a1", af(0.7, 55, 85))
v.check("Ex 25-09.9a2", af(0.5, 55, 85))
tot85 = sum(f * af(ea, 55, 85) for f, ea in rates)
one85 = 6 * af(0.7, 55, 85)
v.check("Ex 25-09.9b", tot85)
v.check("Ex 25-09.9c", one85)
v.check("Ex 25-09.9d", 100 * (1 - one85 / tot85))

# ---------------------------------------------------------------- Problems
v.check("25-09.1a", af(0.7, 85, 150))
v.check("25-09.1b", af(1.0, 85, 150))
a2 = af(0.9, 110, 300) * (5 / 0.5) ** 2
v.check("25-09.2a", a2)
v.check("25-09.2b", 200 * a2)
v.check("25-09.2b1", 200 * a2 / H_YEAR)
z = stats.norm.ppf(1e-4)
v.check("25-09.2c0", z)
t01 = stats.lognorm.ppf(1e-4, 0.4, scale=200 * a2)
v.check("25-09.2c1", t01 / (200 * a2))
v.check("25-09.2c", t01 / H_YEAR)
v.check("25-09.3b", optimize.brentq(lambda x: local_n(x) - 1.25, 0.01, 100))
v.check("25-09.3c", optimize.brentq(lambda x: local_n(x) - 1.75, 0.01, 100))
v.check("25-09.4a", 3000 / 8e-4 / 1e6)
v.check("25-09.4b", 3000 / 8e-4 / 1e6 / 1.0)
f5 = fits([(10, 10), (8, 1000)])
v.check("25-09.5a", -f5["E"][1])
v.check("25-09.5b", f5["1/E"][1])
v.check("25-09.5c", -f5["power"][1])
v.check("25-09.5d", predict(f5, "E", 5))
v.check("25-09.5d1", predict(f5, "power", 5))
v.check("25-09.5d2", predict(f5, "1/E", 5))
v.check("25-09.5e", predict(f4, "1/E", 5))
sc6 = chip_life(1000, 1e-4, 1.2)
v.check("25-09.6a", sc6)
v.check("25-09.6b", 10 * YEAR / sc6)
v.assert_true("with beta 1.2 only the 1/E model passes", tP < 10 * YEAR / sc6 < tI)
v.check("25-09.7a", 3 * 100 ** (1 / 6))
v.check("25-09.7b", 3 * 100 ** 0.25)
v.check("25-09.7c", 3 * 100 ** 0.25 - 3 * 100 ** (1 / 6))
i4, _, v4, _, _ = hbm_sim(4000, 5, 1)
v.check("25-09.8a", i4)
v.check("25-09.8b", v4)
v.check("25-09.8c", optimize.brentq(lambda ron: hbm_sim(4000, 5, ron)[2] - 8, 0.01, 50))
v.check("25-09.9a", 5 * 0.5)
v.check("25-09.9b", math.sqrt(5 * 0.5))
chi4, chi90 = stats.chi2.ppf(0.60, 4), stats.chi2.ppf(0.90, 2)
v.check("25-09.10a0", chi4)
v.check("25-09.10a", fit_bound(chi4, 7859, 1000, 78.6))
v.check("25-09.10b0", chi90)
v.check("25-09.10b", fit_bound(chi90, 7859, 1000, 78.6))
v.check("25-09.11a", math.ceil(chi / (2 * 1000 * 78.6 * 10e-9)))
tot105 = sum(f * af(ea, 55, 105) for f, ea in rates)
one105 = 6 * af(0.7, 55, 105)
v.check("25-09.12a", tot105)
v.check("25-09.12b", one105)
v.check("25-09.12c", 100 * (1 - one105 / tot105))
v.check("25-09.13a0", chi / 2)
v.check("25-09.13a", stats.poisson.pmf(0, chi / 2))
v.check("25-09.13b", stats.poisson.pmf(0, chi / 4))

# ---------------------------------------------------------------- Lab
v.check("Lab 25-09.a", optimize.brentq(lambda e: predict(f4, "power", e) / predict(f4, "E", e) - 1000, 1, 9.5))
v.check("Lab 25-09.b", sc6)
rng = np.random.default_rng(11)
mc = float(np.mean(rng.poisson(chi / 2, size=400_000) == 0))
v.check("Lab 25-09.c", mc)
v.assert_true("Monte Carlo pass fraction within 0.005 of exp(-chi2/2)", abs(mc - math.exp(-chi / 2)) < 0.005)
v.check("Lab 25-09.d", hbm_sim(2000, 5, 2)[2])

sys.exit(v.finish())
