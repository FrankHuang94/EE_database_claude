#!/usr/bin/env python3
"""Verify every number in the Course 25 final-exam solutions.

Second routes for about a third of the values:
- Question 1(a): oxide growth by integrating the Deal-Grove rate dx/dt = B/(A + 2x) numerically;
- Question 3(b): junction depth by root-finding on the Gaussian profile;
- Question 4(b): clustered yields by integrating Poisson yield over a gamma-distributed defect density, and
  Murphy's by integrating over a triangular density;
- Question 7(b): bond yield from the normal CDF; 7(c): escapes from the joint probability table;
- Question 8(c): fin efficiency by solving the fin ODE as a boundary-value problem;
- Question 9(b): E-model and power-law fits by least squares in transformed coordinates;
- Question 11(b): the package scale by integrating the product of joint survival functions.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-exam", ROOT / "exam" / "solutions.md")
K = 8.617333262e-5
H, C0 = 6.626e-34, 2.998e8

# ---------------------------------------------------------------- Q1
A, B = 0.165, 0.0117


def grow_time(x_target):
    # dx/dt = B/(A + 2x)  ->  t = integral (A + 2x)/B dx
    return integrate.quad(lambda x: (A + 2 * x) / B, 0, x_target)[0]


v.check("X25.1a", grow_time(0.10))
v.check("X25.1a1", grow_time(0.50))
v.check("X25.1b", 0.44 * 0.10)
v.check("X25.1c", 60000 / 30 * 90)
v.check("X25.1d", 0.379 * 24e3 * 0.4e-12 * 1e12)
v.check("X25.1d1", 0.379 * 12e3 * 0.2e-12 * 1e12)

# ---------------------------------------------------------------- Q2
for key, lam, na in (("2a", 193, 1.35), ("2a1", 13.5, 0.33), ("2a2", 13.5, 0.55)):
    v.check(f"X25.{key}", lam / (2 * na))
v.check("X25.2b", 13.5 / (2 * 0.33**2))
v.check("X25.2b1", 13.5 / (2 * 0.55**2))
n_ph = 300 * (20e-9) ** 2 / (H * C0 / 13.5e-9)
v.check("X25.2c", n_ph)
v.check("X25.2c1", 100 / math.sqrt(n_ph))
v.check("X25.2d", 3600 / 22)
v.check("X25.2d1", 3600 / 34)

# ---------------------------------------------------------------- Q3
Q, RP, DRP = 1e15, 50e-7, 20e-7
NP = Q / (math.sqrt(2 * math.pi) * DRP)
v.check("X25.3a", NP)
xj = optimize.brentq(lambda x: NP * math.exp(-((x - RP) ** 2) / (2 * DRP**2)) - 1e17, RP, RP + 10 * DRP)
v.check("X25.3b", xj * 1e7)
drp2 = math.sqrt(DRP**2 + 2 * 2e-12)
v.check("X25.3c", drp2 * 1e7)
v.check("X25.3c1", Q / (math.sqrt(2 * math.pi) * drp2))
v.check("X25.3d", 1 / (1 / 1 + 1 / 5))
v.check("X25.3d1", 0.020 * 63.55 / (2 * 96485 * 8.96) * 1e4 * 60)

# ---------------------------------------------------------------- Q4
dpw = round(math.pi * 300**2 / (4 * 150) - math.pi * 300 / math.sqrt(300))
v.check("X25.4a", dpw)
AD = 1.5 * 0.15
y_p = math.exp(-AD)
# Murphy: average of exp(-A D) over a triangular density on [0, 2 D0]
d0 = 0.15
tri = lambda d: (d / d0**2) if d <= d0 else ((2 * d0 - d) / d0**2)  # noqa: E731
y_m = integrate.quad(lambda d: math.exp(-1.5 * d) * tri(d), 0, 2 * d0, points=[d0])[0]
# negative binomial: average over gamma(alpha = 2, scale = d0/2)
y_nb = integrate.quad(lambda d: math.exp(-1.5 * d) * stats.gamma.pdf(d, 2, scale=d0 / 2), 0, np.inf)[0]
v.check("X25.4b", y_p)
v.check("X25.4b1", y_m)
v.check("X25.4b2", y_nb)
v.check("X25.4c", 18000 / (dpw * y_p))
v.check("X25.4d", 18000 / (dpw * y_nb))

# ---------------------------------------------------------------- Q5
def delay(vth):
    return 0.75 / (0.75 - vth) ** 1.3


v.check("X25.5a", delay(0.34) / delay(0.30))
v.check("X25.5a1", delay(0.26) / delay(0.30))
v.check("X25.5a2", delay(0.34) / delay(0.26))
cox, csi, cbox = 3.9 / 1.0, 11.7 / 6, 3.9 / 20
v.check("X25.5b", 1000 * (1 / (1 / csi + 1 / cbox)) / cox)
v.check("X25.5c", max(3, 4) * 15000)

# ---------------------------------------------------------------- Q6
v.check("X25.6a", 4 * 0.11**2 / 0.045)
n_tr = 0
while (n_tr + 1) * 10 + (n_tr + 2) * 10 <= 130 - 75:
    n_tr += 1
v.check("X25.6b", n_tr)
v.check("X25.6b1", math.ceil(18 / (n_tr + 1)))
g = 13.4e-6 * 120 * 12 / 0.08
g0 = 13.4e-6 * 100 * 10 / 0.07
v.check("X25.6c", g)
v.check("X25.6c0", g0)
v.check("X25.6c1", (g0 / g) ** 2)
v.check("X25.6d", 500 ** (-1 / 5))

# ---------------------------------------------------------------- Q7
v.check("X25.7a", (1000 / 5) ** 2)
v.check("X25.7a1", 5 / 4)
p_axis = stats.norm.cdf(1.25, 0, 0.35) - stats.norm.cdf(-1.25, 0, 0.35)
v.check("X25.7b", 100 * p_axis**2)
good, bad_pass = 0.85, 0.15 * (1 - 0.98)
esc = bad_pass / (good + bad_pass)
v.check("X25.7c", 100 * esc)
v.check("X25.7c1", 0.998**7 * (1 - esc) * (1 - 0.004) ** 6)


def pkg(areas, pkg_cost, d0=0.12):
    s = sum((0.30 * a + 3) / math.exp(-a / 100 * d0) for a in areas)
    return (s + pkg_cost) / 0.99 ** len(areas)


mono, chip = pkg([600], 50), pkg([220] * 3, 90)
v.check("X25.7d", mono)
v.check("X25.7d1", chip)
v.check("X25.7d2", chip / mono)

# ---------------------------------------------------------------- Q8
v.check("X25.8a", 30e-6 / (4 * 600e-6))
v.check("X25.8a1", 1000 * 30e-6 / (4 * 600e-6))
a8 = 0.4e-3
q8 = 3 / (math.pi * a8**2)
v.check("X25.8b", integrate.quad(lambda rr: q8 / 150, 0, a8)[0])
v.check("X25.8b1", 8 / (3 * math.pi**2 * 150 * a8))
m2 = 2 * 60 / (200 * 0.8e-3)
x = np.linspace(0, 0.030, 101)
sol = integrate.solve_bvp(lambda s, y: np.vstack([y[1], m2 * y[0]]), lambda ya, yb: np.array([ya[0] - 1, yb[1]]),
                          x, np.vstack([np.ones_like(x), np.zeros_like(x)]), tol=1e-8)
xs = np.linspace(0, 0.030, 4001)
v.check("X25.8c", math.sqrt(m2) * 0.030)
v.check("X25.8c1", integrate.trapezoid(sol.sol(xs)[0], xs) / 0.030)
rise = 1200 / (1000 * 4180 * 1.5 / 6e4)
v.check("X25.8d", rise)
v.check("X25.8d1", 40 + rise / 2 + 1200 * 0.030)

# ---------------------------------------------------------------- Q9
aft = math.exp(0.85 / K * (1 / 383.15 - 1 / 553.15))
v.check("X25.9a", aft)
v.check("X25.9a1", aft * 4**1.5)
e = np.array([10.0, 9.5])
lt = np.log([30.0, 300.0])
cE = np.polyfit(e, lt, 1)
cP = np.polyfit(np.log(e), lt, 1)
v.check("X25.9b", -cE[0])
v.check("X25.9b1", math.exp(np.polyval(cE, 6.0)))
v.check("X25.9b2", -cP[0])
v.check("X25.9b3", math.exp(np.polyval(cP, math.log(6.0))))
v.check("X25.9c", stats.chi2.ppf(0.6, 2) / (2 * 2000 * 1000 * 50) * 1e9)
v.check("X25.9c1", stats.chi2.ppf(0.6, 4) / (2 * 2000 * 1000 * 50) * 1e9)

# ---------------------------------------------------------------- Q10
v.check("X25.10a", (205 / 40) ** 2)
v.check("X25.10a1", 1000 * (205 / 40) ** 2 / (2 * 365.25))
tot, rf, lat = 165, 0.02 * 100, 0.2 * 15
v.check("X25.10b", 100 * (1 - rf / tot))
v.check("X25.10b1", 100 * (1 - lat / (tot - rf)))
v.check("X25.10c", 100 * optimize.brentq(lambda dc: 1 - (1 - dc) * 100 / tot - 0.99, 0.5, 1))
v.check("X25.10d", 100 * stats.binom.sf(0, 12000, 0.5e-6))

# ---------------------------------------------------------------- Q11
v.check("X25.11a", A)
v.check("X25.11a1", grow_time(A))
surv = lambda n: math.exp(-100 * n**4 - 10000 * (n / 4) ** 4)  # noqa: E731
mean = integrate.quad(surv, 0, 2)[0]
v.check("X25.11b", mean / math.gamma(1.25))
v.check("X25.11b1", 100 * 10000 * 4**-4 / 100)
v.check("X25.11c", 3e-9 * 1e-7 * 1000 * 1e9)
v.check("X25.11d", optimize.brentq(lambda xx: (2 + xx) / (1 + xx) - 1.6, 0.01, 10))

# ---------------------------------------------------------------- Q12
m12, c12 = pkg([800], 50, 0.1), pkg([220] * 4, 110, 0.1)
v.check("X25.12a", 100 * (1 - c12 / m12))
need = (95 - 35 - 1500 * 0.020) / 1500
v.check("X25.12b", need)
v.check("X25.12b1", 0.0627 / need)
for key, frac in (("", 0.02), ("1", 0.05), ("2", 0.07)):
    v.check(f"X25.12c{key}", frac * 20000 / 500)
ph = 16 / 320
z = stats.norm.ppf(0.975)
hi = optimize.brentq(lambda p: (ph - p) ** 2 - z * z * p * (1 - p) / 320, ph, 0.5)
v.check("X25.12d", 100 * hi)

sys.exit(v.finish())
