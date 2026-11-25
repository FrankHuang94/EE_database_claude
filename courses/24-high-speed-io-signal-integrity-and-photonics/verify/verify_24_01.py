#!/usr/bin/env python3
"""Verify every number in chapter 24-01 (signal integrity fundamentals), its problems and its lab.

Independent routes (the lab module si.py uses the chapter's closed forms):
- surface resistance as Re(eta_c) of the exact good-conductor wave impedance;
- conductor and dielectric attenuation as Re(gamma) of the exact complex propagation constant;
- mismatch from the S-parameters of an impedance step, and ripple by sweeping a cascaded ABCD model;
- stub notches by minimizing |S21| of an ABCD cascade;
- FEXT checked against the even/odd modal delay difference;
- pulse heights by direct quadrature of the Fourier integral near the peak.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "24-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("24-01", ROOT / "chapters" / "24-01-signal-integrity-fundamentals.md",
                        ROOT / "solutions" / "24-01-solutions.md", LAB / "README.md")
MU0 = 4e-7 * math.pi
EPS0 = 8.8541878128e-12
SIG = 5.8e7
C0 = 2.998e8
NP = 20 / math.log(10)
INCH, MIL = 0.0254, 25.4e-6


# ---------------------------------------------------------------- independent helpers
def rs_exact(f):
    w = 2 * math.pi * f
    eta = np.sqrt(1j * w * MU0 / (SIG + 1j * w * EPS0))
    return float(np.real(eta))


def delta(f):
    return math.sqrt(2 / (2 * math.pi * f * MU0 * SIG))


def alpha_exact(f, rp, gp, z0, eps_r):
    """Re(gamma) for a line with given R', G' and lossless Z0, eps_r."""
    w = 2 * math.pi * f
    lp, cp = z0 * math.sqrt(eps_r) / C0, math.sqrt(eps_r) / (C0 * z0)
    return float(np.real(np.sqrt((rp + 1j * w * lp) * (gp + 1j * w * cp))))


def cond_db_in(f, w, z0, eps_r=4.0):
    return alpha_exact(f, rs_exact(f) / w, 0.0, z0, eps_r) * NP * INCH


def diel_db_in(f, eps_r, tand, z0=50.0):
    w = 2 * math.pi * f
    cp = math.sqrt(eps_r) / (C0 * z0)
    return alpha_exact(f, 0.0, w * cp * tand, z0, eps_r) * NP * INCH


def kr(f, rms):
    return 1 + 2 / math.pi * math.atan(1.4 * (rms / delta(f)) ** 2)


def abcd_line(f, length, z, eps_r):
    b = 2 * math.pi * f * math.sqrt(eps_r) / C0 * length
    return np.array([[np.cos(b), 1j * z * np.sin(b)], [1j * np.sin(b) / z, np.cos(b)]])


def s21_of(m, z0=50.0):
    return 2 / (m[0, 0] + m[0, 1] / z0 + m[1, 0] * z0 + m[1, 1])


def stub_s21(f, length, eps_r, z=50.0):
    y = 1j * np.tan(2 * math.pi * f * math.sqrt(eps_r) / C0 * length) / z
    return abs(s21_of(np.array([[1, 0], [y, 1]])))


# ---------------------------------------------------------------- Example 24-01.1
for ident, rate, bits in (("a", 32e9, 1), ("b", 64e9, 2), ("c", 128e9, 2), ("d", 212.5e9, 2)):
    baud = rate / bits
    v.check(f"Ex 24-01.1{ident}", baud / 1e9)
    if ident != "b":
        v.check(f"Ex 24-01.1{ident}1", baud / 2 / 1e9)
    else:
        v.check("Ex 24-01.1b1", baud / 2 / 1e9)
    if ident in "acd":
        v.check(f"Ex 24-01.1{ident}2", 1 / baud * 1e12)

# ---------------------------------------------------------------- Example 24-01.2
f16, w5 = 16e9, 5 * MIL
v.check("Ex 24-01.2a", delta(f16) * 1e6)
v.check("Ex 24-01.2a1", delta(f16) * 1e6)
v.check("Txt 24-01.a", delta(f16) * 1e6)
v.check("Ex 24-01.2b", rs_exact(f16) * 1e3)
v.check("Txt 24-01.d", rs_exact(1e9) * 1e3)
rp16 = rs_exact(f16) / w5
v.check("Ex 24-01.2c", rp16)
v.check("Ex 24-01.2c1", rp16 * INCH)
v.check("Ex 24-01.2d", alpha_exact(f16, rp16, 0, 50, 4.0))
c16 = cond_db_in(f16, w5, 50)
v.check("Ex 24-01.2d1", c16)
v.check("Ex 24-01.2d2", c16)
v.check("Txt 24-01.e", c16)
v.check("Ex 24-01.2e", 36 * 4 / (5 * 50))
v.check("Txt 24-01.b", NP * rs_exact(1e9) * INCH / (2 * MIL))
v.check("Txt 24-01.c", NP * math.pi * 1e9 * INCH / C0)
v.check("Txt 24-01.i", NP)
k1 = kr(f16, 1e-6)
v.check("Ex 24-01.2f", k1)
v.check("Ex 24-01.2f1", k1)
v.check("Ex 24-01.2g", c16 * k1)

# ---------------------------------------------------------------- Example 24-01.3
d_fr4, d_m6 = diel_db_in(f16, 4.4, 0.014), diel_db_in(f16, 3.4, 0.002)
v.check("Ex 24-01.3a", d_fr4 / (NP * INCH))
v.check("Ex 24-01.3a1", d_fr4)
v.check("Txt 24-01.f", d_fr4)
v.check("Ex 24-01.3a2", math.sqrt(4.4))
v.check("Ex 24-01.3b", d_m6)
v.check("Txt 24-01.g", d_m6)
for ident, val in (("c", c16 + d_fr4), ("c2", c16 + d_fr4), ("c1", c16 + d_m6), ("c3", c16 + d_m6)):
    v.check(f"Ex 24-01.3{ident}", val)
imp_fr4, imp_m6 = 1.289 - d_fr4, 0.336 - d_m6
v.check("Ex 24-01.3d", imp_fr4)
v.check("Ex 24-01.3d1", imp_m6)
v.check("Ex 24-01.3d2", (imp_fr4 + imp_m6) / 2)
v.check("Ex 24-01.3d3", (imp_fr4 + imp_m6) / 2)
w_imp = optimize.brentq(lambda wm: cond_db_in(f16, wm * MIL, 50) - (imp_fr4 + imp_m6) / 2, 1, 100)
v.check("Ex 24-01.3e", w_imp)

# ---------------------------------------------------------------- Example 24-01.4
v.check("Ex 24-01.4a", 9 + 16 + 1.5 + 9.5)
v.check("Ex 24-01.4b", 15 / (c16 + d_fr4))
v.check("Ex 24-01.4c", 15 / (c16 + d_m6))
v.check("Ex 24-01.4d", 15 / ((c16 + d_fr4) * 1.11))
v.check("Ex 24-01.4e", 15 / ((c16 + d_m6) * 1.08))
v.check("Ex 24-01.4f0", 11.5 - 5 - 0.5)
v.check("Ex 24-01.4f", 6 / 1.4)
v.check("Ex 24-01.4g", 16 / 9)

# ---------------------------------------------------------------- Example 24-01.5 (S-parameters of a step)
z1, z2 = 50.0, 42.5
g = (z2 - z1) / (z2 + z1)
t_power = 4 * z1 * z2 / (z1 + z2) ** 2  # transmitted power fraction of an impedance step
v.check("Ex 24-01.5a", g)
v.check("Ex 24-01.5b", -20 * math.log10(abs(g)))
v.check("Ex 24-01.5c", -10 * math.log10(t_power))
v.check("Txt 24-01.l", abs(g))
v.check("Txt 24-01.m", -10 * math.log10(t_power))
v.check("Ex 24-01.5d1", g * g)
fs = np.linspace(0.1e9, 20e9, 40001)
s = np.array([abs(s21_of(abcd_line(fx, 0.1, 42.5, 4.0))) for fx in fs])
v.check("Ex 24-01.5d", 20 * math.log10(s.max() / s.min()))
v.check("Txt 24-01.p", -10 * math.log10(1 - 0.1 ** 2))

# ---------------------------------------------------------------- Example 24-01.6
def notch(length, eps_r, guess):
    return optimize.minimize_scalar(lambda fx: stub_s21(fx, length, eps_r), bracket=(guess * 0.9, guess, guess * 1.1)).x


n16 = notch(1.6e-3, 3.6, 24.7e9)
v.check("Ex 24-01.6a", n16 / 1e9)
v.check("Txt 24-01.h", n16 / 1e9)
v.check("Txt 24-01.o", notch(0.4e-3, 3.6, 98.8e9) / 1e9)
v.check("Txt 24-01.t", notch(1.6e-3, 3.6, 74.1e9) / 1e9)
v.check("Txt 24-01.n", 1.6e-3 / MIL)
lim16 = optimize.brentq(lambda ll: C0 / (4 * ll * math.sqrt(3.6)) - 1.5 * 16e9, 1e-5, 1e-2)
lim53 = optimize.brentq(lambda ll: C0 / (4 * ll * math.sqrt(3.6)) - 1.5 * 53.125e9, 1e-5, 1e-2)
v.check("Ex 24-01.6b", lim16 * 1e3)
v.check("Ex 24-01.6b1", lim16 / MIL)
v.check("Ex 24-01.6c", lim53 * 1e3)
v.check("Ex 24-01.6c1", lim53 / MIL)
v.check("Ex 24-01.6d", n16 / 16e9)
v.check("Ex 24-01.6e", math.sqrt(3.6))

# ---------------------------------------------------------------- Example 24-01.7
vel = C0 / math.sqrt(3.0)
td = 50e-3 / vel
v.check("Ex 24-01.7a", vel)
v.check("Ex 24-01.7b", td * 1e12)
kb = 0.25 * (0.04 + 0.06)
v.check("Ex 24-01.7c", kb)
v.check("Ex 24-01.7d", kb * 0.4 * 1e3)
v.check("Ex 24-01.7e", vel * 30e-12 / 2 * 1e3)
v.check("Ex 24-01.7e1", 2 * td * 1e12)
fext = 0.5 * td * (0.04 - 0.06) * 0.4 / 30e-12
v.check("Ex 24-01.7f", fext * 1e3)
v.check("Ex 24-01.7g", 0.5 * td * (0.04 - 0.06) * 0.4 * 1e12)
v.check("Ex 24-01.7h", 0.5 * td * (0.06 - 0.06) * 0.4 / 30e-12 * 1e3)
v.check("Txt 24-01.s", abs(fext) / (kb * 0.4))
t_e = td * math.sqrt((1 + 0.06) * (1 - 0.04))
t_o = td * math.sqrt((1 - 0.06) * (1 + 0.04))
v.assert_true("FEXT from the modal delay difference agrees within 0.5%",
              abs(0.2 * (t_e - t_o) / 30e-12 / abs(fext) - 1) < 0.005)

# ---------------------------------------------------------------- Example 24-01.8
v.check("Ex 24-01.8a", 0.2e-9 * 8 * 8e-3 / 100e-12 * 1e3)
zt = 0.9 * 0.02 / 2
v.check("Ex 24-01.8b", zt * 1e3)
v.check("Txt 24-01.j", 0.9 * 0.02 * 1e3)
zc = 2 * math.pi * 200e6 * 0.4e-9
v.check("Ex 24-01.8c", zc)
v.check("Ex 24-01.8c1", zc)
v.check("Ex 24-01.8d0", zc / zt)
v.check("Ex 24-01.8d", math.ceil(zc / zt))
v.check("Ex 24-01.8e", optimize.brentq(lambda fx: 2 * math.pi * fx * 0.4e-9 - 1 / (2 * math.pi * fx * 1e-6), 1e5, 1e9) / 1e6)
v.check("Ex 24-01.8f", 18 * 1.0)
v.check("Ex 24-01.8f1", 18 / 31.25)
v.check("Txt 24-01.q", delta(50e9) * 1e6)
v.check("Txt 24-01.r", 2 * math.pi * 500e6 * 0.4e-9)

# ---------------------------------------------------------------- Problems
v.check("24-01.1a", 106.25 / 2)
v.check("24-01.1a1", 106.25 / 4)
v.check("24-01.1a2", 2 / 106.25e9 * 1e12)
v.check("24-01.1b", 25.78125 / 2)
v.check("24-01.1b1", 1 / 25.78125e9 * 1e12)
v.check("24-01.2a", delta(4e9) * 1e6)
v.check("24-01.2a1", rs_exact(4e9) * 1e3)
v.check("24-01.2b", delta(28e9) * 1e6)
v.check("24-01.2b3", delta(28e9) * 1e6)
v.check("24-01.2b1", rs_exact(28e9) * 1e3)
v.check("24-01.2b2", rs_exact(28e9) * 1e3)
rp3 = rs_exact(28e9) / (4 * MIL)
v.check("24-01.3a", rp3)
v.check("24-01.3a1", rp3)
v.check("24-01.3b0", alpha_exact(28e9, rp3, 0, 42.5, 4.0))
c3 = cond_db_in(28e9, 4 * MIL, 42.5)
v.check("24-01.3b", c3)
v.check("24-01.3c", 36 * math.sqrt(28) / (4 * 42.5))
v.check("24-01.3d", 10 * c3)
d4, c4 = diel_db_in(53.125e9, 3.3, 0.0015), cond_db_in(53.125e9, 4 * MIL, 50)
v.check("24-01.4a", d4)
v.check("24-01.4b", c4)
v.check("24-01.4c", d4 + c4)
v.assert_true("Problem 4 total lies within 1.27-1.8 dB/in", 1.27 < d4 + c4 < 1.8)
rms5 = optimize.brentq(lambda r: kr(28e9, r) - 1.5, 1e-9, 5e-6)
v.check("24-01.5a", rms5 * 1e6)
v.check("24-01.5a1", rms5 * 1e6)
v.check("24-01.5b0", 1.4 * (rms5 / delta(4e9)) ** 2)
v.check("24-01.5b", kr(4e9, rms5))
v.check("24-01.6a", cond_db_in(1e9, w5, 50))
v.check("24-01.6a1", diel_db_in(1e9, 4.4, 0.014))
v.check("24-01.6a2", diel_db_in(1e9, 4.4, 0.014))
fx6 = optimize.brentq(lambda fx: cond_db_in(fx, w5, 50) - diel_db_in(fx, 4.4, 0.014), 1e8, 1e11)
v.check("24-01.6b", fx6 / 1e9)
v.check("Lab 24-01.a", fx6 / 1e9)
v.check("24-01.6c0", cond_db_in(fx6, w5, 50))
v.check("24-01.6c", cond_db_in(fx6, w5, 50) + diel_db_in(fx6, 4.4, 0.014))
v.check("24-01.7a", 8.0 + 8.5 + 15.5)
v.check("24-01.7a1", 15.5 - 1.5 - 1.2)
v.check("24-01.7b", 12.8 / 0.7097)
v.check("24-01.7c", 12.8 / 1.0)
g8 = (60 - 50) / 110
v.check("24-01.8a", g8)
v.check("24-01.8b", -20 * math.log10(g8))
v.check("24-01.8c", -10 * math.log10(4 * 60 * 50 / 110 ** 2))
g15 = 10 ** (-15 / 20)
v.check("24-01.8d0", g15)
v.check("24-01.8d", optimize.brentq(lambda z: (50 - z) / (50 + z) - g15, 1, 50))
v.check("24-01.8d1", optimize.brentq(lambda z: (z - 50) / (z + 50) - g15, 50, 500))
td9 = 3 * INCH * math.sqrt(3.6) / C0
v.check("24-01.9a", td9 * 1e12)
v.check("24-01.9b", 1 / (2 * td9) / 1e9)
v.check("24-01.9c", 20 * math.log10((1 + 0.15 ** 2) / (1 - 0.15 ** 2)))
v.check("24-01.9c1", 0.15 ** 2)
v.check("24-01.10a", notch(2.4e-3, 3.7, 16.2e9) / 1e9)
v.check("24-01.10b", notch(0.25e-3, 3.7, 156e9) / 1e9)
l10 = C0 / (4 * 1.5 * 32e9 * math.sqrt(3.7))
v.check("24-01.10c", l10 * 1e3)
v.check("24-01.10c1", l10 / MIL)
v11 = C0 / math.sqrt(3.6)
td11 = 0.1 / v11
v.check("24-01.11a", v11)
v.check("24-01.11a1", td11 * 1e12)
v.check("24-01.11a2", 0.25 * 0.06)
v.check("24-01.11a3", 0.25 * 0.06 * 0.5 * 1e3)
v.check("24-01.11a4", 2 * td11 * 1e12)
v.check("24-01.11a5", 0.0)
v.check("24-01.11b", 0.5 * td11 * (0.03 - 0.05) * 0.5 / 20e-12 * 1e3)
v.check("24-01.11c", optimize.brentq(lambda ll: ll / (2 * v11) * 0.02 / 20e-12 - 0.02, 1e-5, 1) * 1e3)
td12 = 1e-3 / 1.5e8
v.check("24-01.12b0", td12 * 1e12)
v.check("24-01.12b1", 2 * td12 / 30e-12)
t = np.linspace(0, 100e-12, 100001)
ramp = np.clip(t / 30e-12, 0, 1)
ramp_d = np.clip((t - 2 * td12) / 30e-12, 0, 1)
v.check("24-01.12b", 0.03 * (ramp - ramp_d).max() * 1e3)
v.check("24-01.12b2", 0.03 * 1e3)
v.check("24-01.12c", 1.5e8 * 30e-12 / 2 * 1e3)
n13 = 0.1 * 80e-12 / (0.15e-9 * 12e-3)
v.check("24-01.13a", n13)
v.check("24-01.13", math.floor(n13))
zt14 = 0.75 * 0.025 / 40
v.check("24-01.14a", zt14 * 1e3)
v.check("24-01.14b", 2 * math.pi * 100e6 * 15e-12 * 1e3)
v.check("24-01.14b1", 2 * math.pi * 100e6 * 15e-12 / zt14)
v.check("24-01.14c", zt14 / (2 * math.pi * 15e-12) / 1e6)
v.check("24-01.15a", -20 * math.log10(0.5))
v.check("24-01.15b", -20 * math.log10(0.2))
v.check("24-01.15c", 1 - 0.5 ** 2 - 0.2 ** 2)


# ---------------------------------------------------------------- Lab: pulse heights by quadrature
def h_line(f, length, eps_r, tand, w=w5, z0=50.0):
    wv = 2 * np.pi * f
    lp, cp = z0 * math.sqrt(eps_r) / C0, math.sqrt(eps_r) / (C0 * z0)
    rp = np.sqrt(np.pi * f * MU0 / SIG) / w
    zser, ysh = rp + 1j * wv * lp, wv * cp * tand + 1j * wv * cp
    gl, zc = np.sqrt(zser * ysh) * length, np.sqrt(zser / ysh)
    a, b, c, d = np.cosh(gl), zc * np.sinh(gl), np.sinh(gl) / zc, np.cosh(gl)
    return 2 / (a + b / 50 + c * 50 + d)


def pulse_height(eps_r, tand, ui=31.25e-12, length=10 * INCH):
    fgrid = np.linspace(1e6, 400e9, 400001)
    hp = h_line(fgrid, length, eps_r, tand) * ui * np.sinc(fgrid * ui) * np.exp(-1j * np.pi * fgrid * ui)

    def y(tt):
        return 2 * integrate.trapezoid(np.real(hp * np.exp(2j * np.pi * fgrid * tt)), fgrid)

    t0 = length * math.sqrt(eps_r) / C0
    grid = t0 + np.arange(0, 150e-12, 1e-12)
    best = grid[int(np.argmax([y(tt) for tt in grid]))]
    res = optimize.minimize_scalar(lambda tt: -y(tt), bounds=(best - 1e-12, best + 1e-12), method="bounded")
    return -res.fun


v.check("Lab 24-01.b", pulse_height(4.4, 0.014))
v.check("Lab 24-01.c", pulse_height(3.4, 0.002))
v.check("Lab 24-01.d", n16 / 1e9)
v.check("Lab 24-01.e", notch(0.4e-3, 3.6, 98.8e9) / 1e9)
v.check("Lab 24-01.f", kb * 0.4 * 1e3)
v.check("Lab 24-01.g", 0.5 * td * (-0.02) * 0.4 * 1e12)
v.check("Lab 24-01.h", 0.5 * td * (-0.02) * 0.4 / 60e-12 * 1e3)
v.check("Lab 24-01.i", 2 * td * 1e12)

# ---------------------------------------------------------------- stub loss below the notch (shunt open stub, ABCD)
def stub_s21_db(f, f_notch, z0=50.0):
    th = math.pi / 2 * f / f_notch
    zs = -1j * z0 / math.tan(th)  # open stub input impedance
    abcd = np.array([[1, 0], [1 / zs, 1]])
    a, b, c_, d = abcd[0, 0], abcd[0, 1], abcd[1, 0], abcd[1, 1]
    return 20 * math.log10(abs(2 / (a + b / z0 + c_ * z0 + d)))


for key, r in (("u", 1.5), ("v", 2.0), ("w", 3.0)):
    v.check(f"Txt 24-01.{key}", -stub_s21_db(1.0, r))
fn16 = 299792458.0 / (4 * 1.6e-3 * math.sqrt(3.6))
v.check("Txt 24-01.x", -stub_s21_db(16e9, fn16))
g2 = 0.0811 ** 2
lossless = 20 * math.log10((1 + g2) / (1 - g2))
lossy = 20 * math.log10((1 + g2 * 10 ** (-30 / 10)) / (1 - g2 * 10 ** (-30 / 10)))  # A^2 = 10^(-30/10)
v.check("Txt 24-01.y", lossless / lossy)

# ---------------------------------------------------------------- Example 24-01.9: mixed-mode transformation of a skewed pair
f9, dt9 = 53.125e9, 1e-12
w9 = 2 * math.pi * f9
S = np.zeros((4, 4), dtype=complex)  # ports 1..4 -> indices 0..3; line P: 1->2, line N: 3->4
S[1, 0] = S[0, 1] = np.exp(-1j * w9 * 1e-9)
S[3, 2] = S[2, 3] = np.exp(-1j * w9 * (1e-9 + dt9))
M = np.array([[1, 0, -1, 0], [0, 1, 0, -1], [1, 0, 1, 0], [0, 1, 0, 1]]) / math.sqrt(2)  # rows: d1, d2, c1, c2
Smm = M @ S @ np.linalg.inv(M)
sdd21, scd21 = Smm[1, 0], Smm[3, 0]
v.check("Ex 24-01.9b0", math.pi * f9 * dt9)
v.check("Ex 24-01.9b", abs(sdd21))
v.check("Ex 24-01.9b1", 20 * math.log10(abs(sdd21)))
v.check("Ex 24-01.9b2", abs(scd21))
v.check("Ex 24-01.9b3", 20 * math.log10(abs(scd21)))
dt_10 = optimize.brentq(lambda t: abs(np.sin(math.pi * f9 * t)) - 10 ** -0.5, 1e-13, 2.5e-12, xtol=1e-18)
v.check("Ex 24-01.9c", dt_10 * 1e12)
ell = 299792458.0 * dt9 / math.sqrt(3.4)
v.check("Ex 24-01.9d", ell * 1e3)
v.check("Ex 24-01.9d1", ell / 25.4e-6)

# ---------------------------------------------------------------- Problems 24-01.16 and 24-01.17
kb16 = 0.25 * (0.04 + 0.06)
v.check("24-01.16a0", kb16)


def next_peak(ell, v_=1.5e8, tr=30e-12, va=1.0):
    ramp_slope = lambda t: va / tr if 0 <= t <= tr else 0.0  # noqa: E731
    ts = np.linspace(0, tr + 2 * ell / v_, 2001)
    out = [kb16 * 2 / v_ * integrate.quad(lambda z: ramp_slope(t - 2 * z / v_), 0, ell, limit=200,
                                              points=[max(0.0, min(ell, (t - tr) * v_ / 2)),
                                                      max(0.0, min(ell, t * v_ / 2))])[0] for t in ts]
    return max(out)


for key, ell in (("a", 1e-3), ("b", 5e-3)):
    v.check(f"24-01.16{key}0" if key == "b" else "24-01.16a1", 2 * ell / 1.5e8 * 1e12)
    v.check(f"24-01.16{key}", next_peak(ell) * 1e3)
dt17 = 3 * 25.4e-6 * math.sqrt(3.4) / 299792458.0
v.check("24-01.17a", dt17 * 1e12)
for key, f in (("b", 26.5625e9), ("c", 53.125e9)):
    S = np.zeros((4, 4), dtype=complex)
    S[1, 0] = S[0, 1] = 1.0
    S[3, 2] = S[2, 3] = np.exp(-2j * math.pi * f * dt17)
    v.check(f"24-01.17{key}", 20 * math.log10(abs((M @ S @ np.linalg.inv(M))[3, 0])))

sys.exit(v.finish())
