#!/usr/bin/env python3
"""Verify every published number in chapter 07-06 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Independent routes: the chapter uses phasor formulas (S = V I*, P = Vrms Irms cos θ, the PF-correction
formula). Here average power, RMS values and power factors are computed from sampled time waveforms
(the mean of v(t) i(t) and of i(t)^2 over whole periods), harmonic content by FFT, and corrections by
solving for the capacitor that makes the sampled source current reach the target power factor.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-06",
    COURSE / "chapters" / "07-06-ac-power-and-power-factor.md",
    COURSE / "solutions" / "07-06-solutions.md",
    COURSE / "labs" / "07-06-lab" / "README.md",
)
pi, sqrt = math.pi, math.sqrt
N = 200000


def waves(V_rms, Z, f, n=N):
    """Sampled v(t) and i(t) over one period for a sinusoidal V_rms across impedance Z."""
    t = np.linspace(0, 1 / f, n, endpoint=False)
    w = 2 * pi * f
    v_t = sqrt(2) * V_rms * np.cos(w * t)
    I = sqrt(2) * V_rms / Z
    i_t = abs(I) * np.cos(w * t + cmath.phase(I))
    return t, v_t, i_t


def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x) ** 2)))


def pq(v_t, i_t, f, t):
    """Real power from the time average; reactive power from v and i shifted a quarter period."""
    P = float(np.mean(v_t * i_t))
    S = rms(v_t) * rms(i_t)
    return P, S


# ================================================================================ Example 1
w = 2 * pi * 60
Z = 10 + 1j * w * 0.02
t, vt, it = waves(120, Z, 60)
P, S = pq(vt, it, 60, t)
v.check("Ex 07-06.1a", abs(Z))
v.check("Ex 07-06.1b", math.degrees(cmath.phase(Z)))
v.check("Ex 07-06.1c", rms(it))
v.check("Ex 07-06.1d", P)
v.check("Ex 07-06.1e", sqrt(S**2 - P**2))
v.check("Ex 07-06.1f", S)
v.check("Ex 07-06.1g", P / S)
p = vt * it
v.check("Ex 07-06.1h", p.max())
v.check("Ex 07-06.1i", p.min())
v.check("Ex 07-06.1j", float(np.mean(p < 0)) * 100, tol=0.5)

# ================================================================================ Example 2
tt = np.linspace(0, 1, N, endpoint=False)
tri = np.where(tt < 0.25, 4 * tt, np.where(tt < 0.75, 2 - 4 * tt, 4 * tt - 4))
v.check("Ex 07-06.2a", rms(tri))
v.check("Ex 07-06.2b", tri.max() / rms(tri))
i2 = 10 * np.cos(2 * pi * tt) + 3 * np.cos(6 * pi * tt)
v.check("Ex 07-06.2c", rms(i2))
v.check("Ex 07-06.2d", i2.max())
v.check("Ex 07-06.2e", i2.max() / rms(i2))
F = np.fft.rfft(i2) / (N / 2)
v.check("Ex 07-06.2f", abs(F[3]) / abs(F[1]) * 100)

# ================================================================================ Example 3
V, f = 230.0, 50.0
w = 2 * pi * f
# loads as impedances drawing the stated P and PF at 230 V
ZA = V**2 / (10e3 - 1j * 10e3 * math.tan(math.acos(0.75)))      # S = V^2/Z*  ->  Z = V^2/S*
ZB = V**2 / 4e3
t = np.linspace(0, 1 / f, N, endpoint=False)
vt = sqrt(2) * V * np.cos(w * t)


def source_current(C=0.0):
    Y = 1 / ZA + 1 / ZB + 1j * w * C
    I = sqrt(2) * V * Y
    return abs(I) * np.cos(w * t + cmath.phase(I))


it = source_current()
P, S = pq(vt, it, f, t)
v.check("Ex 07-06.3a", S / 1e3)
v.check("Ex 07-06.3b", P / S)
v.check("Ex 07-06.3c", rms(it))
Cc = brentq(lambda C: (lambda i_: float(np.mean(vt * i_)) / (rms(vt) * rms(i_)))(source_current(C)) - 0.95, 0, 4e-4)
v.check("Ex 07-06.3d", w * Cc * V**2 / 1e3)
v.check("Ex 07-06.3e", Cc * 1e6)
i_after = source_current(Cc)
v.check("Ex 07-06.3f", rms(i_after))
v.check("Ex 07-06.3g", (rms(i_after) / rms(it)) ** 2)
v.check("Ex 07-06.3h", P * 0.90 / (P / S) / 1e3)
v.check("Ex 07-06.3i", P / 1e3)
C_unity = minimize_scalar(lambda C: rms(source_current(C)), bounds=(0, 6e-4), method="bounded",
                          options={"xatol": 1e-12}).x       # unity PF minimizes the source current
v.check("Ex 07-06.3j", w * C_unity * V**2 / 1e3)
v.check("Ex 07-06.3k", rms(source_current(C_unity)))
v.check("Ex 07-06.3l", (0.90 / (P / S) - 1) * 100)

# ================================================================================ Example 4
Vth, Zth = 10.0, 50 + 30j
RL = np.linspace(1, 200, 200001)
PL = 0.5 * (Vth / np.abs(Zth + RL)) ** 2 * RL
v.check("Ex 07-06.4a", 0.5 * abs(Vth / (Zth + Zth.conjugate())) ** 2 * Zth.real)
v.check("Ex 07-06.4b", RL[PL.argmax()], tol=0.005)
v.check("Ex 07-06.4c", PL.max())
v.check("Ex 07-06.4d", PL.max() / 0.25 * 100)

# ================================================================================ Example 5
f = 50.0
w = 2 * pi * f
T = 1 / f
t = np.linspace(0, T, 400000, endpoint=False)
vt = 230 * sqrt(2) * np.cos(w * t)
W = 2.5e-3
shape = ((np.abs(t) < W / 2) | (np.abs(t - T) < W / 2)).astype(float) - (np.abs(t - T / 2) < W / 2).astype(float)
Ip = brentq(lambda a: float(np.mean(vt * a * shape)) - 100.0, 0.1, 10)
it = Ip * shape
F = np.fft.rfft(it) / (len(t) / 2)
I1 = abs(F[1]) / sqrt(2)
v.check("Ex 07-06.5a", I1)
v.check("Ex 07-06.5b", Ip)
v.check("Ex 07-06.5c", rms(it))
v.check("Ex 07-06.5d", 230 * rms(it))
v.check("Ex 07-06.5e", 100 / (230 * rms(it)))
v.check("Ex 07-06.5f", sqrt(rms(it) ** 2 - I1**2) / I1 * 100)
v.check("Ex 07-06.5g", abs(F[3]) / abs(F[1]) * 100)
v.assert_true("Ex5 the current's fundamental is in phase with the voltage", abs(cmath.phase(F[1])) < 1e-4)

# ================================================================================ Example 6
Pin = 2000 / 0.94
v.check("Ex 07-06.6a", Pin)
for pf, kS, kI, kn in ((0.95, "b", "c", "f"), (0.70, "d", "e", "g")):
    v.check(f"Ex 07-06.6{kS}", Pin / pf)
    v.check(f"Ex 07-06.6{kI}", Pin / pf / 230)
    v.check(f"Ex 07-06.6{kn}", math.floor(32 / (Pin / pf / 230)))

# ============================================================================== Practitioner lens
v.check("PL 07-06.a", 100 * 0.90 / 0.70)
v.check("PL 07-06.b", 13.5 * 0.90 / 0.87)
v.check("PL 07-06.c", 250 * 0.95 / 0.85)

# ================================================================================ Problems
tt = (np.arange(N) + 0.5) / N                 # midpoint samples of one period
v.check("07-06.1a", rms(tt))
v.check("07-06.1b", rms(np.maximum(np.sin(2 * pi * tt), 0)))
v.check("07-06.1c", rms(np.abs(np.sin(2 * pi * tt))))
# P2: sample peak phasors
f = 1.0
t = np.linspace(0, 1, N, endpoint=False)
vt = 100 * np.cos(2 * pi * t + math.radians(20))
it = 5 * np.cos(2 * pi * t - math.radians(15))
P, S = pq(vt, it, f, t)
v.check("07-06.2a", S)
v.check("07-06.2b", P)
v.check("07-06.2c", sqrt(S**2 - P**2))
v.check("07-06.2d", P / S)
v.check("07-06.2e", np.max(vt * it))
v.check("07-06.2f", np.min(vt * it))
w = 2 * pi * 1e3
t, vt, it = waves(1 * w * 0.01, 1j * w * 0.01, 1e3)
v.check("07-06.3a", abs(float(np.mean(vt * it))), tol=0.5)
v.check("07-06.3b", rms(vt) * rms(it))
# P4
Zl, Z1, Z2 = 0.2 + 0.4j, 20 + 15j, 30.0
Zp = Z1 * Z2 / (Z1 + Z2)
I = 230 / (Zl + Zp)
VL = I * Zp
v.check("07-06.4a", abs(I))
v.check("07-06.4b", math.degrees(cmath.phase(I)))
v.check("07-06.4c", abs(VL))
v.check("07-06.4d", math.degrees(cmath.phase(VL)))
S_src = 230 * I.conjugate()
v.check("07-06.4e", S_src.real)
v.check("07-06.4f", S_src.imag)
S_line, S1, S2 = abs(I) ** 2 * Zl, abs(VL) ** 2 / Z1.conjugate(), abs(VL) ** 2 / Z2
v.check("07-06.4g", S_line.real)
v.check("07-06.4h", S1.real)
v.check("07-06.4i", S1.imag)
v.check("07-06.4j", S2)
v.check("07-06.4k", Zp.real)
v.check("07-06.4l", Zp.imag)
v.check("07-06.4m", S_line.imag)
v.assert_true("P4 complex power balances", abs(S_src - (S_line + S1 + S2)) < 1e-9)
# P5, P6: solve for the capacitor that reaches each target PF from sampled waveforms
V, f, w = 230.0, 50.0, 2 * pi * 50
Zm = V**2 / (5e3 - 1j * 5e3 * math.tan(math.acos(0.70)))
t = np.linspace(0, 1 / f, N, endpoint=False)
vt = sqrt(2) * V * np.cos(w * t)


def i_src(C):
    I = sqrt(2) * V * (1 / Zm + 1j * w * C)
    return abs(I) * np.cos(w * t + cmath.phase(I))


def pf_signed(C):
    I = sqrt(2) * V * (1 / Zm + 1j * w * C)
    pf = float(np.mean(vt * i_src(C))) / (rms(vt) * rms(i_src(C)))
    return pf if cmath.phase(I) < 0 else 2 - pf      # >1 means leading


C95 = brentq(lambda C: pf_signed(C) - 0.95, 0, 3e-4)
v.check("07-06.5a", w * C95 * V**2)
v.check("07-06.5b", C95 * 1e6)
v.check("07-06.5c", rms(i_src(0)))
v.check("07-06.5d", rms(i_src(C95)))
C1 = minimize_scalar(lambda C: rms(i_src(C)), bounds=(0, 6e-4), method="bounded", options={"xatol": 1e-12}).x
C95L = brentq(lambda C: pf_signed(C) - 1.05, 3.1e-4, 6e-4)
v.check("07-06.6a", C1 * 1e6)
v.check("07-06.6b", C95L * 1e6)
v.check("07-06.6c", rms(i_src(C1)))
v.check("07-06.6d", w * C95L * V**2 - w * C1 * V**2)
v.check("07-06.6e", (C1 / C95 - 1) * 100)
v.check("07-06.6f", (1 - rms(i_src(C1)) / rms(i_src(C95))) * 100)
v.assert_true("P6 0.95 leading draws the same current as 0.95 lagging", abs(rms(i_src(C95L)) - rms(i_src(C95))) < 1e-9)
v.check("07-06.7a", 100 * 0.90 / 0.70)
v.check("07-06.7b", 100 * (math.tan(math.acos(0.70)) - math.tan(math.acos(0.90))))
# P8
Zth = 4 + 3j
RL = np.linspace(0.5, 20, 200001)
PL = (20 / np.abs(Zth + RL)) ** 2 * RL
v.check("07-06.8a", 20**2 / (4 * Zth.real))
v.check("07-06.8b", RL[PL.argmax()], tol=5e-4)
v.check("07-06.8c", PL.max())
# P9: synthesize the current, sample, integrate
t = np.linspace(0, 1, N, endpoint=False)
vt = 230 * sqrt(2) * np.cos(2 * pi * t)
it = sqrt(2) * (5 * np.cos(2 * pi * t) + 2 * np.cos(6 * pi * t) + 1 * np.cos(10 * pi * t))
v.check("07-06.9a", rms(it))
v.check("07-06.9b", sqrt(rms(it) ** 2 - 25) / 5 * 100)
v.check("07-06.9c", float(np.mean(vt * it)) / (230 * rms(it)))
v.check("07-06.9d", float(np.mean(vt * it)))
# P10: build a current with fundamental lagging 30 deg and THD 50 % (all in the 3rd harmonic)
it = sqrt(2) * (1 * np.cos(2 * pi * t - pi / 6) + 0.5 * np.cos(6 * pi * t))
v.check("07-06.10a", float(np.mean(vt * it)) / (rms(vt) * rms(it)))
v.check("07-06.10b", math.cos(pi / 6))
v.check("07-06.10c", (math.cos(pi / 6) / (float(np.mean(vt * it)) / (rms(vt) * rms(it))) - 1) * 100)
# P11
v.check("07-06.11a", 1500 / 0.96)
v.check("07-06.11b", 1500 / 0.96 - 1500)
v.check("07-06.11c", 1500 / 0.96 / 0.95)
v.check("07-06.11d", 1500 / 0.96 / 0.95 / 230)
# P12
for V, pf, kL, kp in ((230, 1.0, "a", "b"), (230, 0.8, "c", "d"), (400, 0.8, "e", "f")):
    I = 50e3 / (V * pf)
    v.check(f"07-06.12{kL}", I**2 * 0.05)
    v.check(f"07-06.12{kp}", I**2 * 0.05 / 50e3 * 100)
v.check("07-06.12g", (400 / 230) ** 2)

# ================================================================================ Lab handout
f, T = 50.0, 0.02
t = np.linspace(0, T, 400000, endpoint=False)
vt = 230 * sqrt(2) * np.cos(2 * pi * f * t)
W = 5e-3
shape = ((np.abs(t) < W / 2) | (np.abs(t - T) < W / 2)).astype(float) - (np.abs(t - T / 2) < W / 2).astype(float)
Ip = brentq(lambda a: float(np.mean(vt * a * shape)) - 100.0, 0.1, 10)
v.check("Lab 07-06.a", 100 / (230 * rms(Ip * shape)))

# ---- audit additions: form factor, Example 1 and 2 intermediates, Example 3 and 6 extensions
tt = np.linspace(0, 1, 200000, endpoint=False)
sine = np.cos(2 * pi * tt)
ff = math.sqrt(np.mean(sine ** 2)) / np.mean(np.abs(sine))
v.check("Th 07-06.a", ff)
sq = np.sign(np.cos(2 * pi * tt))
v.check("Th 07-06.b", 100 * (ff * np.mean(np.abs(sq)) / math.sqrt(np.mean(sq ** 2)) - 1))
v.check("Ex 07-06.1k", 2 * pi * 60)
v.check("Ex 07-06.1l", 2 * pi * 60 * 20e-3)
two = 10 * np.cos(2 * pi * tt) + 3 * np.cos(6 * pi * tt)
v.check("Ex 07-06.2g", math.sqrt(np.mean((10 * sine) ** 2)))
v.check("Ex 07-06.2h", math.sqrt(np.mean(two ** 2)) - math.sqrt(np.mean((10 * sine) ** 2)))
vm = 230 * math.sqrt(2) * np.cos(2 * pi * tt)
im = (10e3 / (230 * 0.75)) * math.sqrt(2) * np.cos(2 * pi * tt - math.acos(0.75))
S_motor = math.sqrt(np.mean(vm ** 2)) * math.sqrt(np.mean(im ** 2))
v.check("Ex 07-06.3m", (S_motor + 4e3) / 1e3)
I95, I70 = 2000 / 0.94 / 0.95 / 230, 2000 / 0.94 / 0.70 / 230
v.check("Ex 07-06.6h", math.floor(0.8 * 32 / I95))
v.check("Ex 07-06.6i", math.floor(0.8 * 32 / I70))

v.finish()
