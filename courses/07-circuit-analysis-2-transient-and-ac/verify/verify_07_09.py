#!/usr/bin/env python3
"""Verify every published number in chapter 07-09 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Independent routes: the chapter uses the dot rule, reflected impedance and closed-form transformer
formulas. Here coupled coils are written with an inductance matrix in terms of currents entering
the dotted terminals; frequency responses come from solving (R + jwL) i = v, one key result is
confirmed by integrating the differential equations into steady state and extracting the phasor with
a lock-in; energies come from integrating p = v1 i1 + v2 i2 along a current ramp; optima (turns ratio,
maximum efficiency) come from numerical search; and yearly energies from summing an hourly profile.
ngspice netlists in labs/07-09-lab are run separately by tools/run_spice.py.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-09",
    COURSE / "chapters" / "07-09-mutual-inductance-and-transformers.md",
    COURSE / "solutions" / "07-09-solutions.md",
    COURSE / "labs" / "07-09-lab" / "README.md",
)
pi = math.pi
deg = lambda z: math.degrees(cmath.phase(z))  # noqa: E731


def coil_voltages(L1, L2, M, di1, di2, s1=1, s2=1):
    """Voltages of two coupled coils; s = +1 if that coil's current enters its dot, -1 if it leaves.
    Convert to dot-entering currents, apply the inductance matrix, convert back."""
    Lm = np.array([[L1, M], [M, L2]])
    d = np.array([s1 * di1, s2 * di2])
    vd = Lm @ d  # voltages positive at the dots, for currents entering the dots
    return s1 * vd[0], s2 * vd[1]


def energy_by_power(L1, L2, M, I1, I2, n=4001):
    """Integrate p = v1 i1 + v2 i2 while both currents ramp linearly from 0 to (I1, I2) in 1 s."""
    t = np.linspace(0, 1, n)
    i1, i2 = I1 * t, I2 * t
    v1 = L1 * I1 + M * I2
    v2 = M * I1 + L2 * I2
    return np.trapezoid(v1 * i1 + v2 * i2, t)


# ================================================================================ Example 1
L1, L2, k = 10e-3, 40e-3, 0.5
M = k * math.sqrt(L1 * L2)
v.check("Ex 07-09.1a", M * 1e3)
va = coil_voltages(L1, L2, M, 100, -50)
v.check("Ex 07-09.1b", va[0])
v.check("Ex 07-09.1c", va[1])
# reversed dot on coil 2: coil 2's current now leaves its (new) dot -> s2 = -1, and its own derivative sign flips
vr = coil_voltages(L1, L2, M, 100, -50, s1=1, s2=-1)
v.check("Ex 07-09.1d", vr[0])
v.check("Ex 07-09.1e", vr[1])
v.check("Ex 07-09.1f", energy_by_power(L1, L2, M, 2, 1) * 1e3)
v.check("Ex 07-09.1g", energy_by_power(L1, L2, -M, 2, 1) * 1e3)


# ================================================================================ Example 2
def coupled_solve(Vs, R1, L1, L2, M, ZL, w):
    """Currents entering the dots: i1 (primary), j2 (secondary, = -I2 of the chapter)."""
    Z = np.array([[R1 + 1j * w * L1, 1j * w * M], [1j * w * M, ZL + 1j * w * L2]])
    i1, j2 = np.linalg.solve(Z, [Vs, 0])
    return i1, -j2


w2 = 2 * pi * 1e3
I1, I2 = coupled_solve(10, 10, L1, L2, M, 100, w2)
Zin = 10 / I1 - 10
v.check("Ex 07-09.2a", Zin.real)
v.check("Ex 07-09.2b", (Zin - 1j * w2 * L1).imag)
v.check("Ex 07-09.2c", Zin.imag)
v.check("Ex 07-09.2d", abs(I1))
v.check("Ex 07-09.2e", deg(I1))
v.check("Ex 07-09.2f", abs(I2))
v.check("Ex 07-09.2g", deg(I2))
Ps = 0.5 * (10 * I1.conjugate()).real
v.check("Ex 07-09.2h", Ps)
v.check("Ex 07-09.2i", 0.5 * abs(I2) ** 2 * 100)
v.check("Ex 07-09.2j", 0.5 * abs(I1) ** 2 * 10)
# lock-in confirmation: integrate L di/dt = v - R i with the inductance matrix
Lmat = np.array([[L1, M], [M, L2]])
Rm = np.diag([10.0, 100.0])
Linv = np.linalg.inv(Lmat)
T2 = 1e-3
sol = solve_ivp(lambda t, x: Linv @ (np.array([10 * math.cos(w2 * t), 0.0]) - Rm @ x), (0, 60 * T2), [0, 0],
                method="DOP853", rtol=1e-10, atol=1e-13, dense_output=True, max_step=T2 / 200)
tt = np.linspace(40 * T2, 60 * T2, 40000, endpoint=False)
ph1 = 2 * np.mean(sol.sol(tt)[0] * np.exp(-1j * w2 * tt))
v.assert_true("lock-in I1 matches the phasor solution", abs(ph1 - I1) < 1e-5)

# ================================================================================ Example 3 (matching by search)
Rs, RLs = 200.0, 8.0
v.check("Ex 07-09.3a", (10 / (Rs + RLs)) ** 2 * RLs * 1e3)
best = minimize_scalar(lambda n: -(10 / (Rs + n * n * RLs)) ** 2 * n * n * RLs, bounds=(1, 20), method="bounded",
                       options={"xatol": 1e-10})
v.check("Ex 07-09.3b", best.x, tol=0.01)
v.check("Ex 07-09.3c", -best.fun * 1e3)
v.check("Ex 07-09.3d", -best.fun / ((10 / (Rs + RLs)) ** 2 * RLs))

# ================================================================================ Example 4 (tests)


def from_tests(S, Vh, Vl, Voc, Ioc, Poc, Vsc, Psc):
    Ih = S / Vh
    Soc = complex(Poc, math.sqrt((Voc * Ioc) ** 2 - Poc**2))
    Yoc = Soc.conjugate() / Voc**2  # admittance of Rc || jXm from S = V^2 Y*
    Rc, Xm = 1 / Yoc.real, -1 / Yoc.imag
    Zsc = complex(Psc / Ih**2, math.sqrt((Vsc / Ih) ** 2 - (Psc / Ih**2) ** 2))
    return Ih, Rc, Xm, Zsc


S4, Vh4, Vl4 = 50e3, 7200.0, 240.0
Ih4, Rc4, Xm4, Z4 = from_tests(S4, Vh4, Vl4, 240, 1.0, 90, 180, 497)
v.check("Ex 07-09.4a", Ih4)
v.check("Ex 07-09.4b", S4 / Vl4)
v.check("Ex 07-09.4c", Rc4)
v.check("Ex 07-09.4d", Xm4)
v.check("Ex 07-09.4e", Z4.real)
v.check("Ex 07-09.4f", Z4.imag)
v.check("Ex 07-09.4o", 180 / Vh4 * 100)


def eta(x, S, Pc, Pcu, pf=1.0):
    return x * S * pf / (x * S * pf + Pc + x * x * Pcu)


v.check("Ex 07-09.4g", 90 + 0.5**2 * 497)
v.check("Ex 07-09.4h", eta(0.5, S4, 90, 497) * 100)
mx = minimize_scalar(lambda x: -eta(x, S4, 90, 497), bounds=(0.01, 2), method="bounded", options={"xatol": 1e-12})
v.check("Ex 07-09.4i", mx.x)
v.check("Ex 07-09.4j", -mx.fun * 100)
v.check("Ex 07-09.4k", eta(1, S4, 90, 497) * 100)
th = math.acos(0.8)
v.check("Ex 07-09.4l", Ih4 * (Z4.real * 0.8 + Z4.imag * 0.6))
v.check("Ex 07-09.4m", Ih4 * (Z4.real * 0.8 + Z4.imag * 0.6) / Vh4 * 100)
Vs_exact = Vh4 + Ih4 * cmath.exp(-1j * th) * Z4
v.check("Ex 07-09.4n", (abs(Vs_exact) - Vh4) / Vh4 * 100)

# ================================================================================ Example 5 (hourly sum)
hours = [0.7] * 8 + [0.2] * 16
v.check("Ex 07-09.5a", np.mean(np.square(hours)))
for core, cu, iw, ie in ((90, 497, "b", "c"), (30, 560, "d", "e")):
    loss_h = [core + x * x * cu for x in hours]
    v.check(f"Ex 07-09.5{iw}", np.mean(loss_h))
    v.check(f"Ex 07-09.5{ie}", sum(loss_h) * 365 / 1000)
eG = sum(90 + x * x * 497 for x in hours)
eA = sum(30 + x * x * 560 for x in hours)
v.check("Ex 07-09.5f", (eG - eA) / eG * 100)
v.check("Ex 07-09.5g", 30 + 560)
v.check("Ex 07-09.5h", 90 + 497)


# ================================================================================ Example 6 (turns by sampling)
def turns_needed(Vrms, f, A, Bm):
    """Sample v = N A dB/dt for B = Bm sin(wt) over a period and solve RMS(v) = Vrms for N."""
    t = np.linspace(0, 1 / f, 20001, endpoint=False)
    dBdt = Bm * 2 * pi * f * np.cos(2 * pi * f * t)
    return Vrms / (A * math.sqrt(np.mean(dBdt**2)))


v.check("Ex 07-09.6a", turns_needed(230, 50, 1e-4, 0.2), tol=50)
v.check("Ex 07-09.6b", turns_needed(230, 100e3, 1e-4, 0.2))

# ================================================================================ Problems
p1 = coil_voltages(5e-3, 20e-3, 6e-3, 200, 100)
v.check("07-09.1a", 6e-3 / math.sqrt(5e-3 * 20e-3))
v.check("07-09.1b", p1[0])
v.check("07-09.1c", p1[1])
p1b = coil_voltages(5e-3, 20e-3, 6e-3, 200, 100, s1=1, s2=-1)
# coil 2's current leaves its dot: its own term keeps its sign in its passive convention, mutual flips
v.check("07-09.1d", p1b[0])
v.check("07-09.1e", p1b[1])
Mp2 = brentq(lambda m: (20 + 30 + 2 * m) - 70, 0, 30)
v.check("07-09.2a", Mp2)
v.check("07-09.2b", Mp2 / math.sqrt(20 * 30))
v.assert_true("opposing series gives 30 mH", abs((20 + 30 - 2 * Mp2) - 30) < 1e-9)
v.check("07-09.3a", 120 / 10)
v.check("07-09.3b", 12 / 12)
# near-ideal transformer: k = 1 - 1e-12, magnetizing reactance far above the reflected load
L2i = 100.0
L1i, Mi = 100 * L2i, (1 - 1e-12) * math.sqrt(100 * L2i * L2i)
wi = 2 * pi * 60
I1i, I2i = np.linalg.solve(np.array([[1j * wi * L1i, 1j * wi * Mi], [1j * wi * Mi, 1j * wi * L2i + 12]]),
                           np.array([120.0, 0.0]))
v.check("07-09.3c", abs(I1i))
v.assert_true("P3 secondary current is 1 A", abs(abs(I2i) - 1.0) < 1e-6)
v.check("07-09.3d", 120 / 0.1)
# P4: minimize energy numerically over i2 (opposing fluxes)
w4 = lambda i2: 0.5 * 1e-3 * 4 + 0.5 * 4e-3 * i2**2 - 1.5e-3 * 2 * i2  # noqa: E731
r4 = minimize_scalar(w4, bounds=(-5, 5), method="bounded", options={"xatol": 1e-12})
v.check("07-09.4a", r4.x)
v.check("07-09.4b", r4.fun * 1e3)
v.check("07-09.4c", 1.5 / math.sqrt(1 * 4))
# P5: T-equivalent and shorted secondary by matrix solve (secondary voltage forced to zero)
# T arms from open-circuit tests on the coupled pair (drive one coil, other open), at 1 kHz
w5 = 2 * pi * 1e3
Lm5 = np.array([[10e-3, 10e-3], [10e-3, 40e-3]])
z11 = (1j * w5 * Lm5 @ np.array([1.0, 0.0]))[0] / 1.0          # V1/I1 with I2 = 0
z21 = (1j * w5 * Lm5 @ np.array([1.0, 0.0]))[1] / 1.0          # V2/I1 with I2 = 0
z22 = (1j * w5 * Lm5 @ np.array([0.0, 1.0]))[1] / 1.0          # V2/I2 with I1 = 0
v.check("07-09.5a", ((z11 - z21) / (1j * w5)).real * 1e3, tol=0.5)
v.check("07-09.5b", ((z22 - z21) / (1j * w5)).real * 1e3)
v.check("07-09.5c", (z21 / (1j * w5)).real * 1e3)
wq = 2 * pi * 1e3
Zsh = np.array([[1j * wq * 10e-3, 1j * wq * 10e-3], [1j * wq * 10e-3, 1j * wq * 40e-3]])
i_sh = np.linalg.solve(Zsh, [1.0, 0.0])
v.check("07-09.5d", (1 / i_sh[0]).imag)
# P6
w6 = 2 * pi * 10e3
I1_6, _ = coupled_solve(1.0, 0.0, 1e-9, 1e-3, 0.5e-3, 50.0, w6)
Zr6 = 1 / I1_6 - 1j * w6 * 1e-9
v.check("07-09.6a", Zr6.real)
v.check("07-09.6b", Zr6.imag)
v.check("07-09.6c", abs(Zr6))
# P7 by search
b7 = minimize_scalar(lambda n: -(1 / (600 + n * n * 50)) ** 2 * n * n * 50, bounds=(1, 10), method="bounded",
                     options={"xatol": 1e-12})
v.check("07-09.7a", b7.x)
v.check("07-09.7b", -b7.fun * 1e3)
v.check("07-09.7c", (1 / 650) ** 2 * 50 * 1e3)
# P8
Ih8, Rc8, Xm8, Z8 = from_tests(10e3, 2400, 240, 240, 0.8, 60, 48, 180)
v.check("07-09.8a", Ih8)
v.check("07-09.8b", Rc8)
v.check("07-09.8c", Xm8)
v.check("07-09.8d", Z8.real)
v.check("07-09.8e", Z8.imag)
# P9
m9 = minimize_scalar(lambda x: -eta(x, 10e3, 60, 180), bounds=(0.01, 2), method="bounded", options={"xatol": 1e-12})
v.check("07-09.9a", m9.x)
v.check("07-09.9b", -m9.fun * 100)
for x, i1_, i8 in ((0.25, "c", "d"), (0.5, "e", "f"), (1.0, "g", "h")):
    v.check(f"07-09.9{i1_}", eta(x, 10e3, 60, 180, 1.0) * 100)
    v.check(f"07-09.9{i8}", eta(x, 10e3, 60, 180, 0.8) * 100)
# P10
for kva, e16, e29, ia, ib, ic in ((167, 0.9933, 0.9946, "a", "b", "c"), (25, 0.9895, 0.9900, "d", "e", "f")):
    P = kva * 1e3 * 0.5
    l16, l29 = P * (1 / e16 - 1), P * (1 / e29 - 1)
    v.check(f"07-09.10{ia}", l16)
    v.check(f"07-09.10{ib}", l29)
    v.check(f"07-09.10{ic}", (l16 - l29) / l16 * 100)
# P11
for s, ia, ie in ((0.6, "a", "b"), (-0.6, "c", "d")):
    v.check(f"07-09.11{ia}", Ih8 * (Z8.real * 0.8 + Z8.imag * s) / 2400 * 100)
    Vs11 = 2400 + Ih8 * complex(0.8, -s) * Z8
    v.check(f"07-09.11{ie}", (abs(Vs11) - 2400) / 2400 * 100)
# P12: wireless link, solved with the coupled-coil matrix and a 1 A primary drive
Lw, fw = 24e-6, 360e3
ww = 2 * pi * fw
Ct = 1 / (ww**2 * Lw)
v.check("07-09.12a", Ct * 1e9)


def link(kk, tuned=True):
    Mw = kk * Lw
    Z2 = 0.2 + 5 + (1 / (1j * ww * Ct) if tuned else 0)
    # primary driven by 1 A: secondary current from row 2, primary voltage from row 1
    j2 = -1j * ww * Mw * 1.0 / (Z2 + 1j * ww * Lw)
    Vp = (0.2 + 1j * ww * Lw) * 1.0 + 1j * ww * Mw * j2
    Zr = Vp - (0.2 + 1j * ww * Lw)
    eta_ = (0.5 * abs(j2) ** 2 * 5) / (0.5 * Vp.real)
    return Zr, eta_


for kk, ir, ie in ((0.25, "b", "c"), (0.1, "d", "e"), (0.03, "f", "g")):
    Zr, e = link(kk)
    v.check(f"07-09.12{ir}", Zr.real)
    v.check(f"07-09.12{ie}", e * 100)
Zu, eu = link(0.25, tuned=False)
v.check("07-09.12h", Zu.real)
v.check("07-09.12i", Zu.imag)
v.check("07-09.12j", eu * 100)
# P13
v.check("07-09.13a", turns_needed(120, 60, 2e-4, 0.25))
v.check("07-09.13b", turns_needed(120, 100e3, 2e-4, 0.25))
v.check("07-09.13c", 120 / (10 * math.sqrt(np.mean((0.25 * 2 * pi * 1e5 * np.cos(np.linspace(0, 2 * pi, 20001)[:-1])) ** 2))) * 1e4)

# ================================================================================ Practitioner lens (section 9)
P50 = 50e3 * 0.5
v.check("PL 07-09.a", P50 * (1 / 0.9911 - 1))
v.check("PL 07-09.b", P50 * (1 / 0.9915 - 1))
v.check("PL 07-09.c", (P50 * (1 / 0.9911 - 1) - P50 * (1 / 0.9915 - 1)) / (P50 * (1 / 0.9911 - 1)) * 100)
P75 = 75e3 * 0.35
v.check("PL 07-09.d", P75 * (1 / 0.986 - 1))
v.check("PL 07-09.e", P75 * (1 / 0.9888 - 1))
v.check("PL 07-09.f", (1 - (1 / 0.9888 - 1) / (1 / 0.986 - 1)) * 100)
v.check("PL 07-09.g", 48000 / 45000 * 100)
v.check("PL 07-09.h", 7.5 * 20)
v.check("PL 07-09.i", 800e3 / 50e3)
v.check("PL 07-09.j", 400e3 / 50e3)

# ================================================================================ Lab handout
I1l, I2l = coupled_solve(10, 10, 10e-3, 40e-3, 0.99 * math.sqrt(10e-3 * 40e-3), 100, w2)
v.check("Lab 07-09.a", 0.5 * abs(I2l) ** 2 * 100)
v.check("Lab 07-09.b", (10 / I1l - 10).real)

# Section 3.4 series-connection example: M from aiding and opposing measurements of a 9 mH / 4 mH pair
def series_L(M, sign):
    Lm = np.array([[9e-3, M], [M, 4e-3]])
    d = np.array([1.0, sign])
    return d @ Lm @ d


Mser = brentq(lambda M: series_L(M, 1.0) - 21e-3, 0, 6e-3)
v.assert_true("series example: opposing connection reads 5 mH", abs(series_L(Mser, -1.0) - 5e-3) < 1e-12)
v.check("Th 07-09.a", Mser * 1e3)
v.check("Th 07-09.b", Mser / math.sqrt(9e-3 * 4e-3))

v.finish()
