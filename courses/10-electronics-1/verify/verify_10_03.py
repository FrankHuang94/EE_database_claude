#!/usr/bin/env python3
"""Verify every number in chapter 10-03 (BJT DC operation and biasing), its solutions and lab.

Independent routes:
- bias networks are solved as linear systems of Kirchhoff equations (numpy.linalg.solve) with the transistor
  as a 0.7 V base-emitter source and a current-controlled current source, not from the chapter's closed
  forms; the region is then checked from the solved voltages, and saturated cases re-solved with 0.2 V;
- the current mirror with an exponential (Ebers-Moll) transistor and the Early effect, solving KCL for V_BE;
- temperature and thermal-loop results by numerically differentiating a self-heated exponential transistor;
- the lab's Monte Carlo by seeded sampling.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("10-03", COURSE / "chapters" / "10-03-bjt-dc-operation-and-biasing.md",
                        COURSE / "solutions" / "10-03-solutions.md",
                        COURSE / "labs" / "10-03-lab" / "README.md")

VT = 1.380649e-23 * 300 / 1.602176634e-19


def ddx(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)


def four_resistor(vcc, r1, r2, re, rc, beta, vbe=0.7):
    """Unknowns [V_B, V_E, V_C, I_B]; base node KCL, V_BE source, emitter KCL, collector KCL."""
    A = np.array([[-(1 / r1 + 1 / r2), 0, 0, -1],
                  [1, -1, 0, 0],
                  [0, 1 / re, 0, -(beta + 1)],
                  [0, 0, 1, beta * rc]], float)
    b = np.array([-vcc / r1, vbe, 0, vcc])
    vb, ve, vc, ib = np.linalg.solve(A, b)
    return dict(vb=vb, ve=ve, vc=vc, ib=ib, ic=beta * ib, ie=(beta + 1) * ib)


def base_drive(vbb, rb, rc, vcc, beta, re=0.0):
    """Base driven through rb (optional emitter resistor); returns the active solution."""
    A = np.array([[rb + (beta + 1) * re]], float)
    ib = np.linalg.solve(A, [vbb - 0.7])[0]
    ic = beta * ib
    return ib, ic, vcc - rc * ic


# ------------------------------------------------------------------ data-sheet values (quoted, R-178)
for k_, val in (("T 10-03.a", 100), ("T 10-03.b", 300), ("T 10-03.c", 30), ("T 10-03.d", 0.2), ("T 10-03.e", 0.3),
                ("T 10-03.f", 0.85), ("T 10-03.g", 0.95), ("T 10-03.h", 200), ("T 10-03.k", 60), ("T 10-03.l", 625),
                ("T 10-03.m", 40)):
    v.check(k_, val)
v.check("T 10-03.i", ddx(lambda t: math.log(math.exp(0.002 * t / VT)), 0.0) * 100)   # d(ln I)/dT at fixed V_BE
v.check("T 10-03.j", (1 - 1 / (1 + 2 / 100)) * 100)

# ------------------------------------------------------------------ Example 1
ib1, ic1, vc1 = base_drive(2.0, 100e3, 2e3, 5.0, 100)
v.check("Ex 10-03.1a", ib1 * 1e6)
v.check("Ex 10-03.1b", ic1 * 1e3)
v.check("Ex 10-03.1c", vc1)
v.assert_true("beta = 100 is active", vc1 > 0.3)
_, ic3, vc3 = base_drive(2.0, 100e3, 2e3, 5.0, 300)
v.check("Ex 10-03.1d", ic3 * 1e3)
v.check("Ex 10-03.1e", vc3)
v.assert_true("beta = 300 fails the active check", vc3 < 0.3)
ics = (5.0 - 0.2) / 2e3
v.check("Ex 10-03.1f", ics * 1e3)
v.check("Ex 10-03.1g", ics / ib1)
v.check("Ex 10-03.1h", brentq(lambda b: 5.0 - 2e3 * b * ib1 - 0.3, 50, 500))

# ------------------------------------------------------------------ Example 2 (PNP, emitter at V_B + 0.7)
ve2 = 3.0 + 0.7
ie2 = (5.0 - ve2) / 3.3e3
v.check("Ex 10-03.2a", ve2)
v.check("Ex 10-03.2b", ie2 * 1e3)
v.check("Ex 10-03.2c", ie2 * 100 / 101 * 1e3)
v.check("Ex 10-03.2d", 2e3 * ie2 * 100 / 101)
v.check("Ex 10-03.2e", ve2 - 2e3 * ie2 * 100 / 101)

# ------------------------------------------------------------------ Example 3
v.check("Ex 10-03.3a", 12 * 10 / 57)
v.check("Ex 10-03.3b", 1 / (1 / 47e3 + 1 / 10e3) / 1e3)
s3 = four_resistor(12, 47e3, 10e3, 1e3, 4.7e3, 100)
v.check("Ex 10-03.3c", s3["ie"] * 1e3)
v.check("Ex 10-03.3d", s3["ic"] * 1e3)
v.check("Ex 10-03.3e", s3["ib"] * 1e6)
v.check("Ex 10-03.3f", s3["vc"])
v.check("Ex 10-03.3g", s3["ve"])
v.check("Ex 10-03.3h", s3["vc"] - s3["ve"])
v.assert_true("Example 3 is active", s3["vc"] - s3["ve"] > 0.3)
s3h, s3l = four_resistor(12, 47e3, 10e3, 1e3, 4.7e3, 300), four_resistor(12, 47e3, 10e3, 1e3, 4.7e3, 50)
v.check("Ex 10-03.3i", s3h["ic"] * 1e3)
v.check("Ex 10-03.3j", (s3h["ic"] / s3["ic"] - 1) * 100)
v.check("Ex 10-03.3k", s3l["ic"] * 1e3)
v.check("Ex 10-03.3l", (s3l["ic"] / s3["ic"] - 1) * 100)
idiv = (12 - s3["vb"]) / 47e3
v.check("Ex 10-03.3m", 12 / 57e3 * 1e3)
v.check("Ex 10-03.3n", 12 / 57e3 / s3["ib"])
v.assert_true("the loaded divider current differs from the unloaded one only by I_B", abs(idiv - s3["vb"] / 10e3 - s3["ib"]) < 1e-12)
v.check("T 10-03.n", s3h["ic"] / s3["ic"])
v.check("T 10-03.o", 0.02 / (12 * 10 / 57 - 0.7) * 100)

# ------------------------------------------------------------------ Example 4
s85 = four_resistor(12, 47e3, 10e3, 1e3, 4.7e3, 100, vbe=0.7 - 0.002 * 60)
v.check("Ex 10-03.4a", s85["ic"] * 1e3)
v.check("Ex 10-03.4b", (s85["ic"] / s3["ic"] - 1) * 100)
VT85 = 1.380649e-23 * 358.15 / 1.602176634e-19
v.check("Ex 10-03.4c", math.exp(0.12 / VT85))


# ------------------------------------------------------------------ Example 5: exponential mirror with Early effect
def mirror(iref, beta, va=None, vce2=0.7):
    def ic(vbe, vce):
        return 1e-15 * math.exp(vbe / VT) * (1 + (vce / va if va else 0))
    vbe = brentq(lambda x: ic(x, x) + ic(x, x) / beta + ic(x, vce2) / beta - iref, 0.3, 1.0, xtol=1e-15)
    return ic(vbe, vce2)


v.check("Ex 10-03.5a", (5 - 0.7) / 1e-3 / 1e3)
io = mirror(1e-3, 100)
v.check("Ex 10-03.5b", io * 1e3)
v.check("Ex 10-03.5c", (io / 1e-3 - 1) * 100)
io2 = mirror(1e-3, 100, va=50, vce2=3.0)
# with V_A the diode-connected Q1 sits at its own V_BE, not 0.7 V; the chapter uses 0.7 V for Q1's V_CE
io2_ch = (1e-3 / (1 + 2 / 100)) * (1 + 3.0 / 50) / (1 + 0.7 / 50)
v.check("Ex 10-03.5d", io2_ch * 1e3)
v.check("Ex 10-03.5e", (io2_ch / 1e-3 - 1) * 100)
v.assert_true("the exponential mirror agrees with the chapter's Early-effect estimate within 0.2%",
              abs(io2 / io2_ch - 1) < 2e-3, f"{io2*1e3:.5f} mA")

# ------------------------------------------------------------------ Example 6
v.check("Ex 10-03.6a", 12 / 240 * 1e3)
v.check("Ex 10-03.6b", 0.05 / 10 * 1e3)
v.check("Ex 10-03.6c", (3.3 - 0.85) / 5e-3)
ib6 = (3.3 - 0.85) / 470
v.check("Ex 10-03.6d", ib6 * 1e3)
v.check("Ex 10-03.6e", 0.05 / ib6)
v.check("Ex 10-03.6f", 0.3 * 0.05 * 1e3)
v.check("Ex 10-03.6g", 0.85 * ib6 * 1e3)
v.check("Ex 10-03.6h", (0.3 * 0.05 + 0.85 * ib6) * 1e3)


# ------------------------------------------------------------------ Example 7: thermal loop by numerical differentiation
def ic_of_T(dT, re, i0=0.01):
    """Collector current at junction temperature rise dT, base voltage fixed at its dT = 0 value,
    V_BE(I, T) = V_T ln(I/I_S) - 2 mV/K * dT (the course's temperature model)."""
    vb = VT * math.log(i0 / 1e-15) + i0 * re
    return brentq(lambda i: VT * math.log(i / 1e-15) - 0.002 * dT + i * re - vb, 1e-6, 1.0, xtol=1e-16)


v.check("Ex 10-03.7a", 5 * 0.01 * 1e3)
v.check("Ex 10-03.7b", 5 * 0.01 * 200)
for k_, ka, re in (("Ex 10-03.7c", "Ex 10-03.7d", 0.0), ("Ex 10-03.7e", "Ex 10-03.7f", 100.0)):
    L = ddx(lambda t: ic_of_T(t, re), 0.0, 1e-3) * 5 * 200
    v.check(k_, L)
    v.check(ka, 1 / (1 - L))
v.check("Ex 10-03.7g", 1 / ddx(lambda vbe: 1e-15 * math.exp(vbe / VT), VT * math.log(0.01 / 1e-15)))

# ------------------------------------------------------------------ solutions
for k_, b in (("10-03.2a", 50), ("10-03.2b", 100), ("10-03.2c", 300)):
    v.check(k_, b / (b + 1))
v.check("10-03.2d", brentq(lambda b: b / (b + 1) - 0.995, 1, 1e4))
ib, ic, vc = base_drive(3.0, 200e3, 3e3, 9.0, 120)
v.check("10-03.3a", ib * 1e6)
v.check("10-03.3b", ic * 1e3)
v.check("10-03.3c", vc)
v.check("10-03.4a", 1.5 / 1e-3 / 1e3)
v.check("10-03.4b", (9 - 3 - 1.5) / 1e-3 / 1e3)
v.check("10-03.4c", 1.5 + 0.7)
v.check("10-03.4d", 9 / 0.1e-3 / 1e3)
v.check("10-03.4e", 90 * 2.2 / 9)
v.check("10-03.4f", 90 - 90 * 2.2 / 9)
v.check("10-03.4g", 1 / (1 / 68e3 + 1 / 22e3) / 1e3)
s4 = four_resistor(9, 68e3, 22e3, 1.5e3, 4.5e3, 100)
v.check("10-03.4h", s4["ic"] * 1e3)
v.check("10-03.4i", (s4["ic"] / 1e-3 - 1) * 100)
s4h = four_resistor(9, 68e3, 22e3, 1.5e3, 4.5e3, 300)
v.check("10-03.5a", s4h["ic"] * 1e3)
v.check("10-03.5b", (s4h["ic"] / s4["ic"] - 1) * 100)
s4t = four_resistor(9, 68e3, 22e3, 1.5e3, 4.5e3, 100, vbe=0.6)
v.check("10-03.5c", s4t["ic"] * 1e3)
v.check("10-03.5d", (s4t["ic"] / s4["ic"] - 1) * 100)


def coll_fb(beta):
    """Unknowns [V_C, I_B]: R_C carries I_E = (beta + 1) I_B; base loop V_C = I_B R_B + 0.7."""
    A = np.array([[1, (beta + 1) * 2e3], [1, -200e3]], float)
    vc, ib = np.linalg.solve(A, [5.0, 0.7])
    return vc, ib


vc6, ib6s = coll_fb(100)
v.check("10-03.6a", 101 * ib6s * 1e3)
v.check("10-03.6b", 100 * ib6s * 1e3)
v.check("10-03.6c", vc6)
vc6h, ib6h = coll_fb(300)
v.check("10-03.6d", 300 * ib6h * 1e3)
v.check("10-03.6e", (300 * ib6h / (100 * ib6s) - 1) * 100)
v.check("10-03.7a", 0.05 / 10 * 1e3)
v.check("10-03.7b", (5 - 0.95) / 5e-3)
ib7 = (5 - 0.95) / 750
v.check("10-03.7c", ib7 * 1e3)
v.check("10-03.7d", 0.05 / ib7)
v.check("10-03.7e", 0.4 * 0.05 * 1e3)
io8 = mirror(0.5e-3, 50)
v.check("10-03.8a", io8 * 1e3)
v.check("10-03.8b", (io8 / 0.5e-3 - 1) * 100)
# buffered mirror: the reference supplies I_C1 plus the buffer's base current 2 I_C/(beta(beta+1))
icb = brentq(lambda i: i + 2 * i / (50 * 51) - 0.5e-3, 0, 1e-3, xtol=1e-18)
v.check("10-03.8c", icb * 1e3)
v.check("10-03.8d", (icb / 0.5e-3 - 1) * 100)
c40 = four_resistor(12, 47e3, 10e3, 1e3, 4.7e3, 100, vbe=0.7 + 0.002 * 65)
c85 = four_resistor(12, 47e3, 10e3, 1e3, 4.7e3, 100, vbe=0.7 - 0.002 * 60)
v.check("10-03.9a", c40["ic"] * 1e3)
v.check("10-03.9b", c85["ic"] * 1e3)
v.check("10-03.9c", (c85["ic"] / c40["ic"] - 1) * 100)
v.check("10-03.10a", brentq(lambda i: ddx(lambda t: ic_of_T(t, 0.0, i), 0.0, 1e-3) * 5 * 200 - 1, 1e-4, 0.1) * 1e3)
v.check("10-03.10b", 0.002 * 1000 / 10)
v.assert_true("with 10 ohms the loop gain stays below 0.2 even at 1 A",
              ddx(lambda t: ic_of_T(t, 10.0, 0.5), 0.0, 1e-3) * 1000 < 0.2)
v.check("10-03.11a", 0.02 / 10 * 1e3)
v.check("10-03.11b", (1.8 - 0.85) / 2e-3)
ib11 = (1.8 - 0.98) / 475
v.check("10-03.11c", ib11 * 1e3)
v.check("10-03.11d", 0.02 / ib11)
v.check("10-03.11e", (5 - 2 - 0.2) / 0.02)
for k_, b in (("10-03.12a", 100), ("10-03.12b", 300)):
    v.check(k_, base_drive(9.0, 330e3, 0, 9.0, b, re=1e3)[1] * 1e3)
v.check("10-03.12c", (base_drive(9.0, 330e3, 0, 9.0, 300, re=1e3)[1] / base_drive(9.0, 330e3, 0, 9.0, 100, re=1e3)[1] - 1) * 100)

# ------------------------------------------------------------------ lab: Monte Carlo of beta and V_BE through Example 3's bias
rng = np.random.default_rng(1003)
betas = rng.uniform(100, 300, 20000)
vbes = 0.7 + rng.uniform(-0.02, 0.02, 20000)
ics_mc = np.array([four_resistor(12, 47e3, 10e3, 1e3, 4.7e3, b, vbe=x)["ic"] for b, x in zip(betas, vbes)])
v.check("Lab 10-03.a", ics_mc.max() / ics_mc.min())
v.check("Lab 10-03.b", ics_mc.std() / ics_mc.mean() * 100)
v.check("Lab 10-03.c", ics_mc.mean() * 1e3)

v.finish()
