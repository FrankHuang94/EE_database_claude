#!/usr/bin/env python3
"""Verify every number in chapter 12-10 (noise in circuits), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- integrated noise by numerical quadrature of each spectrum (white, 1/f, filtered);
- kT/C by integrating the RC-filtered thermal spectrum, and by simulating the RC circuit's stochastic
  differential equation (Euler-Maruyama, fixed seed) driven by the resistor's noise current;
- the common-source stage's input-referred noise from the solved circuit's noise-to-output transfer
  functions, divided by its solved gain;
- noise figure and the optimum source resistance by bounded optimization;
- the flicker-corner fit by solving the two data-sheet points simultaneously.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "12-10-noise-in-circuits.md", COURSE / "solutions" / "12-10-solutions.md"]
lab = COURSE / "labs" / "12-10-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-10", *files)
k, q = 1.380649e-23, 1.602176634e-19
T = 300.0
kT = k * T
TP = 2 * math.pi
VT = 0.025852


def white(S, f1, f2):
    return quad(lambda f: S, f1, f2)[0]


def thermal(R, temp=T):
    return 4 * k * temp * R                      # V^2/Hz


def ktc_integral(R, C, temp=T):
    """Integrate the resistor's noise through the RC low-pass; substitute x = 2 pi f R C."""
    val, _ = quad(lambda x: thermal(R, temp) / (1 + x * x), 0, np.inf)
    return val / (TP * R * C)


# ============================================================ theory numbers
v.check("T 12-10.a", 4 * kT)
v.check("T 12-10.b", 1 / (2 * (1e-3 / VT)))
v.check("T 12-10.c", 100 * (math.sqrt(1 + (1 / 3) ** 2) - 1))   # a source 3x smaller raises the RMS total ~5%

# ============================================================ Example 1
v.check("Ex 12-10.1a", math.sqrt(thermal(1e3)) * 1e9)
v.check("Ex 12-10.1b", math.sqrt(thermal(50)) * 1e9)
v.check("Ex 12-10.1c", math.sqrt(white(thermal(1e3), 0, 20e3)) * 1e9)

# ============================================================ Example 2
i_sh = math.sqrt(2 * q * 1e-3)
v.check("Ex 12-10.2a", i_sh * 1e12)
v.check("Ex 12-10.2b", i_sh * 1e3 * 1e9)
v.check("Ex 12-10.2c", i_sh * 1e3 / math.sqrt(thermal(1e3)))
v.check("Ex 12-10.2d", brentq(lambda R: 4 * kT / R - 2 * q * 1e-3, 1, 1e4))   # resistor with the same current noise

# ============================================================ Example 3: white plus 1/f
Sw, fc = (5e-9) ** 2, 1e5
wh = white(Sw, 1, 1e6)
fl = quad(lambda u: Sw * fc, 0, math.log(1e6))[0]   # integrate S_w f_c / f over ln f
v.check("Ex 12-10.3a", math.sqrt(wh) * 1e6)
v.check("Ex 12-10.3b", math.sqrt(fl) * 1e6)
tot = quad(lambda lf: Sw * (1 + fc / math.exp(lf)) * math.exp(lf), 0, math.log(1e6), limit=200)[0]
v.check("Ex 12-10.3c", math.sqrt(tot) * 1e6)


# ============================================================ Example 4: common-source stage, by nodal noise transfer
def cs_input_noise(gm, gamma, RD):
    """Output noise PSD from the drain noise current and R_D's noise current (both into the drain node,
    whose resistance is R_D), divided by the squared gain g_m R_D found from the same node equation."""
    z_out = RD                                   # drain node impedance (r_o neglected)
    gain = gm * z_out
    out_psd = (4 * kT * gamma * gm + 4 * kT / RD) * z_out ** 2
    return out_psd / gain ** 2


S4 = cs_input_noise(5e-3, 2 / 3, 2e3)
part_t = (4 * kT * (2 / 3) * 5e-3) * (2e3) ** 2 / (5e-3 * 2e3) ** 2
v.check("Ex 12-10.4a", part_t / (4 * kT))
v.check("Ex 12-10.4b", (S4 - part_t) / (4 * kT))
v.check("Ex 12-10.4c", S4 / (4 * kT))
v.check("Ex 12-10.4d", math.sqrt(S4) * 1e9)
v.check("Ex 12-10.4e", 100 * part_t / S4)
v.check("Ex 12-10.4f", S4 / (S4 - part_t))

# ============================================================ Example 5: kT/C
C1 = 1e-12
v.check("Ex 12-10.5a", math.sqrt(ktc_integral(1e3, C1)) * 1e6)
for bits, ids in ((12, ("Ex 12-10.5b", "Ex 12-10.5c", "Ex 12-10.5d")), (16, ("Ex 12-10.5e", "Ex 12-10.5f", "Ex 12-10.5g"))):
    lsb = 1.0 / 2 ** bits
    qn = math.sqrt(quad(lambda e: e * e / lsb, -lsb / 2, lsb / 2)[0])   # uniform quantization error's RMS
    v.check(ids[0], lsb * 1e6)
    v.check(ids[1], qn * 1e6)
    v.check(ids[2], brentq(lambda c: ktc_integral(1e3, c) - qn ** 2, 1e-15, 1e-9, xtol=1e-18) * 1e12)
# SDE check: dv = -v/(RC) dt + sqrt(2kT/R)/C dW, sampled long after the start
rng = np.random.default_rng(12010)
R_s, C_s = 1e3, 1e-12
tau = R_s * C_s
dt = tau / 50
nsteps, nwalk = 2000, 40000
vv = np.zeros(nwalk)
amp = math.sqrt(2 * kT / R_s) / C_s * math.sqrt(dt)
for _ in range(nsteps):
    vv += -vv / tau * dt + amp * rng.standard_normal(nwalk)
v.assert_true("simulated RC capacitor variance within 4% of the integrated kT/C",
              abs(np.var(vv) / ktc_integral(R_s, C_s) - 1) < 0.04)
v.assert_true("kT/C integral independent of R (1 k vs 100 k)",
              abs(ktc_integral(1e3, C1) / ktc_integral(1e5, C1) - 1) < 1e-9)


# ============================================================ Example 6: noise figure
def noise_factor(Rs, en, inn):
    return (thermal(Rs) + en ** 2 + (inn * Rs) ** 2) / thermal(Rs)


en, inn = 1e-9, 1e-12
v.check("Ex 12-10.6a", thermal(50))
v.check("Ex 12-10.6b", noise_factor(50, en, inn))
v.check("Ex 12-10.6c", 10 * math.log10(noise_factor(50, en, inn)))
opt = minimize_scalar(lambda r: noise_factor(math.exp(r), en, inn), bounds=(0, 15), method="bounded",
                      options={"xatol": 1e-12})
Ropt = math.exp(opt.x)
v.check("Ex 12-10.6d", Ropt / 1e3)
v.check("Ex 12-10.6e", opt.fun)
v.check("Ex 12-10.6f", 10 * math.log10(opt.fun))
v.check("Ex 12-10.6g", Ropt / 50)
v.check("Ex 12-10.6h", math.sqrt(Ropt / 50))
v.check("Ex 12-10.6i", 10 * math.log10(noise_factor(50, en, inn)) - 10 * math.log10(opt.fun))

# ============================================================ practitioner (R-182, R-183)
v.check("Prac 12-10.a", (1.1e-9) ** 2 / (4 * kT))
v.check("Prac 12-10.b", (10e-9) ** 2 / (4 * kT) / 1e3)
# S_w (1 + f_c/f) at 1 kHz and 10 kHz is linear in a = S_w and b = S_w f_c
a_fit, b_fit = np.linalg.solve(np.array([[1.0, 1 / 1e3], [1.0, 1 / 1e4]]), np.array([16.0 ** 2, 10.0 ** 2]))
sw, fcfit = a_fit, b_fit / a_fit
v.check("Prac 12-10.c", math.sqrt(sw))
v.check("Prac 12-10.d", fcfit / 1e3)

# ============================================================ guided exercise
v.assert_true("kT/C is 64.36 uV at 1 pF for R from 1 k to 100 k",
              all(abs(math.sqrt(ktc_integral(R, 1e-12)) * 1e6 - 64.36) < 0.005 for R in (1e3, 1e4, 1e5)))

# ============================================================ solutions
v.check("12-10.1a", math.sqrt(thermal(1e4)) * 1e9)
v.check("12-10.1b", math.sqrt(thermal(1e4, 77.0)) * 1e9)
v.check("12-10.2a", math.sqrt(thermal(1e3) + thermal(3e3)) * 1e9)
v.check("12-10.2b", math.sqrt((4 * kT / 1e3 + 4 * kT / 3e3) * (1e3 * 3e3 / 4e3) ** 2) * 1e9)   # currents add, x R_par^2
i3 = math.sqrt(2 * q * 10e-9)
v.check("12-10.3a", i3 * 1e15)
v.check("12-10.3b", math.sqrt(white(i3 ** 2, 0, 1e3)) * 1e12)
v.check("12-10.4a", math.sqrt(ktc_integral(1e3, 10e-12)) * 1e6)
v.check("12-10.4b", brentq(lambda c: ktc_integral(1e3, c) - (10e-6) ** 2, 1e-13, 1e-9, xtol=1e-18) * 1e12)
Sw5, fc5 = (10e-9) ** 2, 1e3
fl5 = quad(lambda lf: Sw5 * fc5, math.log(0.1), math.log(10))[0]
wh5 = white(Sw5, 0.1, 10)
v.check("12-10.5a", math.sqrt(fl5) * 1e9)
v.check("12-10.5b", math.sqrt(wh5) * 1e9)
v.check("12-10.5c", math.sqrt(fl5 + wh5) * 1e9)
gm6 = 100e-6 / VT
v.check("12-10.6a", gm6 * 1e3)
Seq6 = 2 * q * 100e-6 / gm6 ** 2               # collector shot noise referred to the base
v.check("12-10.6b", Seq6 / (4 * kT))
v.check("12-10.6c", math.sqrt(Seq6) * 1e9)
v.check("12-10.6d", math.sqrt(2 * q * 1e-6) * 1e12)
Req7 = (2e-9) ** 2 / (4 * kT)
g7 = brentq(lambda g: 4 * kT * (2 / 3) / g - (2e-9) ** 2, 1e-5, 1, xtol=1e-15)
v.check("12-10.7a", Req7)
v.check("12-10.7b", g7 * 1e3)
v.check("12-10.7c", g7 * 0.2 / 2 * 1e6)
v.check("12-10.8a", math.sqrt(2 ** 2 + (10 / 10) ** 2))
v.check("12-10.8b", math.sqrt(2 ** 2 + (10 / 3) ** 2))
en9, in9, R9 = 5e-9, 2e-12, 1e4
S9 = thermal(R9) + en9 ** 2 + (in9 * R9) ** 2
v.check("12-10.9a", math.sqrt(thermal(R9)) * 1e9)
v.check("12-10.9b", in9 * R9 * 1e9)
v.check("12-10.9c", math.sqrt(S9) * 1e9)
v.check("12-10.9d", 10 * math.log10(noise_factor(R9, en9, in9)))
opt9 = minimize_scalar(lambda r: noise_factor(math.exp(r), en9, in9), bounds=(0, 15), method="bounded",
                       options={"xatol": 1e-12})
v.check("12-10.9e", math.exp(opt9.x) / 1e3)
v.check("12-10.9f", opt9.fun)
v.check("12-10.9g", 10 * math.log10(opt9.fun))
lsb10 = 2.0 / 2 ** 14
qn10 = math.sqrt(quad(lambda e: e * e / lsb10, -lsb10 / 2, lsb10 / 2)[0])
v.check("12-10.10a", lsb10 * 1e6)
v.check("12-10.10b", qn10 * 1e6)
v.check("12-10.10c", brentq(lambda c: ktc_integral(1e3, c) - qn10 ** 2, 1e-14, 1e-9, xtol=1e-18) * 1e12)
Req11 = (1.5e-9) ** 2 / (4 * kT)
gm11 = brentq(lambda g: (2 / 3) / g - 0.9 * Req11, 1e-5, 1, xtol=1e-15)
RD11 = brentq(lambda r: 1 / (gm11 ** 2 * r) - 0.1 * Req11, 1, 1e7, xtol=1e-9)
v.assert_true("problem 11 design meets 1.5 nV/rtHz", abs(math.sqrt(cs_input_noise(gm11, 2 / 3, RD11)) / 1.5e-9 - 1) < 1e-9)
v.check("12-10.11a", Req11)
v.check("12-10.11b", gm11 * 1e3)
v.check("12-10.11c", RD11 / 1e3)
v.check("12-10.11d", gm11 * RD11)
nb = quad(lambda f: 1 / (1 + (f / 10e3) ** 2), 0, np.inf)[0]
v.check("12-10.12a", nb / 1e3)
v.check("12-10.12b", math.sqrt(white((4e-9) ** 2, 0, nb)) * 1e9)

# ============================================================ lab README (ngspice at its default 27 C)
if lab.exists():
    T27 = 300.15
    v.check("Lab 12-10.a", math.sqrt(ktc_integral(10e3, 1e-12, T27)) * 1e6)
    v.check("Lab 12-10.b", math.sqrt(thermal(10e3, T27)) * 1e9)

sys.exit(v.finish())
