#!/usr/bin/env python3
"""Verify every published number in chapter 00-04, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "00-04",
    COURSE / "chapters" / "00-04-toolchain-walkthrough.md",
    COURSE / "solutions" / "00-04-solutions.md",
    COURSE / "labs" / "00-04-lab" / "README.md",
)

# chapter examples -------------------------------------------------------------
I = 5 / (3e3 + 2e3)
v.check("Ex 00-04.1a", I * 2e3)
v.check("Ex 00-04.1b", I * 1e3)
v.check("Ex 00-04.1c", I**2 * 3e3 * 1e3)
v.check("Ex 00-04.2a", 5 * 1e6 / 2e6)
v.check("Ex 00-04.2b", 5 * 1e6 / (1e6 + 1e-3))
v.check("Ex 00-04.3a", np.finfo(float).eps)
v.check("Ex 00-04.3b", 0.1 + 0.2 - 0.3)
x = 1e-8
v.check("Ex 00-04.3c", 2 * math.sin(x / 2) ** 2)
v.assert_true("naive 1 - cos(1e-8) is exactly 0 in double precision", 1 - math.cos(x) == 0.0)
v.assert_true("0.1+0.2-0.3 is exactly one ulp of 0.3 (2^-54)",
              0.1 + 0.2 - 0.3 == np.spacing(0.3) == 2.0**-54)
v.assert_true("doubles just below 1 are 2^-53 apart", 1.0 - np.nextafter(1.0, 0.0) == 2.0**-53)
v.assert_true("1 - delta rounds to 1 only if delta < 2^-54: cos(1.4e-8) != 1",
              math.cos(1.4e-8) == 1 - 2.0**-53 and (1.4e-8) ** 2 / 2 > 2.0**-54 > 1e-16 / 2)
v.check("Ex 00-04.4a", 2**3)
v.check("Ex 00-04.4b", 2**64 / 1e9 / (365.25 * 24 * 3600))
v.check("Ex 00-04.5a", 1 / (2 * math.pi * 1e3 * 1e-6))

# problems ----------------------------------------------------------------------
for ident, val in [("00-04.1a", 4.7e3), ("00-04.1b", 10e-6), ("00-04.1c", 2.2e-9), ("00-04.1d", 1e6),
                   ("00-04.1e", 3e-3), ("00-04.1f", 1e-3)]:
    v.check(ident, val)
I2 = 12 / 15e3
v.check("00-04.2a", I2 * 5e3)
v.check("00-04.2b", I2 * 1e3)
v.check("00-04.2c", 12 * I2 * 1e3)
v.check("00-04.3a", abs(0.1 + 0.2 - 0.3) / 0.3)
v.assert_true("1 + eps/4 == 1", 1.0 + np.finfo(float).eps / 4 == 1.0)
# nodal solution of Problem 4: unknowns Va, Vb
G = np.array([[1 / 1e3 + 1 / 2e3 + 1 / 1e3, -1 / 1e3], [-1 / 1e3, 1 / 1e3 + 1 / 1e3]])
Va, Vb = np.linalg.solve(G, np.array([10 / 1e3, 0.0]))
v.check("00-04.4a", Va)
v.check("00-04.4b", Vb)
v.check("00-04.4c", (10 - Va) / 1e3 * 1e3)
fc = 1 / (2 * math.pi * 10e3 * 10e-9)
v.check("00-04.5a", fc / 1e3)
v.check("00-04.5b", 20 * math.log10(1 / math.sqrt(1 + (10e3 / fc) ** 2)))
xx = 1e8
v.assert_true("naive sqrt(x^2+1) - x is 0 at x = 1e8", math.sqrt(xx * xx + 1) - xx == 0.0)
v.check("00-04.6", 1 / (math.sqrt(xx * xx + 1) + xx))
v.check("00-04.7a", 2**16 / 1e9 * 1e6)
v.check("00-04.7b", 2**32 / 1e9)
v.check("00-04.7c", 2**64 / 1e9 / (365.25 * 24 * 3600))
v.check("00-04.8a", 1e-3 / 1e-9)
v.check("00-04.8b", 1e-3 / 1e-9 * 10e-6)
v.check("00-04.8c", 1e-3 / 1e-12 * 10e-6 / 3600)

Is, VT = 1e-14, 0.025852


def newton_step(V):
    g = (5 - V) / 1e3 - Is * math.expm1(V / VT)
    dg = -1 / 1e3 - Is / VT * math.exp(V / VT)
    return V - g / dg


V1 = newton_step(0.70)
V2 = newton_step(V1)
V3 = newton_step(V2)
v.check("00-04.9a", V1)
v.check("00-04.9b", V2)
v.check("00-04.9c", V3)
v.check("00-04.9d", (5 - V3) / 1e3 * 1e3)
v.check("00-04.9e", newton_step(0.60))


def iterations(V0, tol=1e-9):
    V, n = V0, 0
    while True:
        Vn, n = newton_step(V), n + 1
        if abs(Vn - V) < tol:
            return n, Vn
        V = Vn


n06, Vsol = iterations(0.60)
v.assert_true("from 0.60 V plain Newton takes 32 iterations (as stated)", n06 == 32, f"{n06}")
from scipy.optimize import brentq  # noqa: E402
v.assert_true("Newton solution agrees with bracketing root-finder",
              abs(Vsol - brentq(lambda V: (5 - V) / 1e3 - Is * math.expm1(V / VT), 0, 1)) < 1e-12)
v.check("00-04.10a", abs(2.21 - 2.2046))

# lab ------------------------------------------------------------------------------
v.check("Lab 00-04.1", iterations(0.70)[0])

v.finish()
