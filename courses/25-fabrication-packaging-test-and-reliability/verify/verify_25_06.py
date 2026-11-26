#!/usr/bin/env python3
"""Verify every number in chapter 25-06 (packaging I), its problems and lab.

Independent routes (the lab module package.py uses closed forms):
- escape routing by brute force: the largest n with n*w + (n+1)*s <= p - d, found by counting up;
- I/O crossover by root-finding where the two counts are equal;
- joint strain from the displacement difference of die and substrate points;
- the weakest-link package life by Monte Carlo over all joints and by numerical integration of the survival
  function; the strain-map fraction by an exact integer count of grid joints;
- market and panel figures by direct arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "25-06-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("25-06", ROOT / "chapters" / "25-06-packaging-fundamentals.md",
                        ROOT / "solutions" / "25-06-solutions.md", LAB / "README.md")


def traces(p, d, w, s):
    n = 0
    while (n + 1) * w + (n + 2) * s <= p - d + 1e-9:
        n += 1
    return n


def layers(rows, p, d, w, s):
    return math.ceil(rows / (traces(p, d, w, s) + 1))


def strain(dalpha_ppm, dt, l_mm, h_mm):
    die = 2.6e-6 * dt * l_mm
    sub = (2.6 + dalpha_ppm) * 1e-6 * dt * l_mm
    return (sub - die) / h_mm


# ---------------------------------------------------------------- Example 1
v.check("Ex 25-06.1a", 4 * 10 / 0.060)
v.check("Ex 25-06.1a1", (10 / 0.150) ** 2)
v.check("Ex 25-06.1a2", (10 / 0.150) ** 2 / (4 * 10 / 0.060))
v.check("Ex 25-06.1b", optimize.brentq(lambda d: (d / 0.150) ** 2 - 4 * d / 0.060, 0.1, 100))

# ---------------------------------------------------------------- Example 2
v.check("Ex 25-06.2a", traces(150, 90, 15, 15))
v.check("Ex 25-06.2a1", layers(15, 150, 90, 15, 15))
v.check("Ex 25-06.2b", traces(150, 90, 10, 10))
v.check("Ex 25-06.2b1", layers(15, 150, 90, 10, 10))

# ---------------------------------------------------------------- Example 3
i3 = 1000 / 0.75
v.check("Ex 25-06.3a", i3)
v.check("Ex 25-06.3b", i3 / 0.15)
v.check("Ex 25-06.3c", 2 * i3 / 0.15)
v.check("Ex 25-06.3d", 2 * i3 / 0.15 * 0.150**2)

# ---------------------------------------------------------------- Example 4
v.check("Ex 25-06.4a", 16 - 2.6)
g4 = strain(13.4, 100, 10, 0.070)
v.check("Ex 25-06.4b", g4)
v.check("Ex 25-06.4c", (g4 / (g4 / 10)) ** 2)

# ---------------------------------------------------------------- Examples 5-6
v.check("Ex 25-06.5a", (510 // 90) * (515 // 90))
v.check("Ex 25-06.5a1", (510 // 110) * (515 // 110))
v.check("Ex 25-06.5b", 110**2 / 90**2)
v.check("Ex 25-06.5c", 3.5 * 18 / 6)
v.check("Ex 25-06.5d", 100 * (1 - 16 / 25))
tot = 41.56
v.check("Ex 25-06.6a", 100 * 18.54 / tot)
v.check("Ex 25-06.6a1", 100 * 6.32 / tot)
v.check("Ex 25-06.6a2", 100 * 5.00 / tot)
v.check("Ex 25-06.6b", 100 * (18.54 + 6.32 + 5.00) / tot)
v.check("Ex 25-06.6c", 18.54 / 6.32)

# ---------------------------------------------------------------- Problems
v.check("25-06.1a", 4 * 5 / 0.050)
v.check("25-06.1a1", (5 / 0.130) ** 2)
v.check("25-06.1b", optimize.brentq(lambda d: (d / 0.130) ** 2 - 4 * d / 0.050, 0.1, 100))
v.check("25-06.2a", traces(150, 80, 12, 12))
v.check("25-06.2b", layers(15, 150, 80, 12, 12))
v.check("25-06.3a", traces(110, 70, 10, 10))
v.check("25-06.3b", layers(20, 110, 70, 10, 10))
i4 = 1500 / 0.70
v.check("25-06.4a", i4)
v.check("25-06.4b", i4 / 0.2)
v.check("25-06.4c", 2 * i4 / 0.2)
v.check("25-06.4d", 2 * i4 / 0.2 * 0.130**2)
g5 = strain(13.4, 165, 10, 0.070)
v.check("25-06.5a", g5)
v.check("25-06.5b", (g4 / g5) ** 2)
g6 = strain(13.4, 100, 14.14, 0.070)
v.check("25-06.6a", g6)
v.check("25-06.6b", (g4 / g6) ** 2)
g7 = strain(13.4, 100, 10, 0.100)
v.check("25-06.7a", g7)
v.check("25-06.7b", (g4 / g7) ** 2)
# weakest link for 1000 equal joints: integrate the survival function to get the mean, compare with eta*Gamma
beta, m = 4.0, 1000
mean_pkg = integrate.quad(lambda n: math.exp(-m * n**beta), 0, 5)[0]
scale = mean_pkg / math.gamma(1 + 1 / beta)
v.check("25-06.8b", scale)
v.check("25-06.9a", (510 // 130) * (515 // 130))
v.check("25-06.9b", 130**2 / 110**2)
v.check("25-06.10a", 100 * (18.54 + 6.32 + 5.00 + 3.32 + 2.28) / tot)
v.check("25-06.11a0", 1.0 * 2)
v.check("25-06.11a", 2e-9 * 8 * 0.020 / 1.0e-9)
v.check("25-06.11b", 0.05e-9 * 8 * 0.020 / 1.0e-9 * 1e3)
v.check("25-06.11c", 2e-9 / 0.05e-9)
v.check("25-06.12a", optimize.brentq(lambda w: 3 * w + 4 * w - 50, 1, 50))
v.assert_true("7.14 um lines give 3 traces and 5 layers", traces(130, 80, 7.14, 7.14) == 3 and layers(20, 130, 80, 7.14, 7.14) == 5)

# ---------------------------------------------------------------- Lab
v.check("Lab 25-06.a", layers(15, 150, 80, 12, 12))
# joints within 10% of the corner strain on the 25 mm / 0.15 mm grid, counted with exact integer arithmetic:
# 167 x 167 joints at offsets k = -83..83 pitches; strain >= 0.9 corner  <=>  i^2 + j^2 >= 0.81 * 2 * 83^2
half = int(round(25 / 0.15)) // 2
lim = 81 * 2 * half**2  # compare 100*(i^2+j^2) with 81*2*83^2
cnt = sum(1 for i in range(-half, half + 1) for j in range(-half, half + 1) if 100 * (i * i + j * j) >= lim)
frac = cnt / (2 * half + 1) ** 2
v.check("Lab 25-06.b", 100 * frac)
n = int(round(20 / 0.15))
c = (np.arange(n) - (n - 1) / 2) * 0.15
xx, yy = np.meshgrid(c, c)
r = np.hypot(xx, yy).ravel()
gam = 13.4e-6 * 100 * r / 0.070
rel = (gam / gam.max()) ** 2
sc = float(np.sum(rel**4) ** (-1 / 4))
v.check("Lab 25-06.c", sc)
v.check("Lab 25-06.c1", sc**-4)
rng = np.random.default_rng(13)
eta = np.where(gam > 0, (gam.max() / np.where(gam > 0, gam, 1)) ** 2, np.inf)
first = np.array([np.min(eta * rng.weibull(4.0, eta.size)) for _ in range(600)])
v.assert_true("Monte Carlo mean first failure within 2% of eta_pkg*Gamma(1.25)",
              abs(first.mean() / (sc * math.gamma(1.25)) - 1) < 0.02)
v.check("Lab 25-06.d", 1500 / 0.70 / 0.2)

sys.exit(v.finish())
