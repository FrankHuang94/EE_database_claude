#!/usr/bin/env python3
"""Verify every number in chapter 13-08 (transmission lines in sinusoidal steady state), its solutions and lab.

Independent routes (not the chapter's closed forms):
- input impedances by integrating the phasor telegrapher's equations numerically (solve_ivp) from the load, where
  V = Z_L and I = 1, back to the input, so Z_in = V/I without the tan formula;
- gamma and Z0 by complex square roots, cross-checked against the low-loss formulas;
- standing-wave extrema by sampling |V(d)| computed from the same ODE;
- bandwidths and stub lengths by root finding on the ODE results.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-08-transmission-lines-sinusoidal-steady-state.md",
         COURSE / "solutions" / "13-08-solutions.md"]
lab = COURSE / "labs" / "13-08-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-08", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 1 / math.sqrt(mu0 * e0)
NP_DB = 20 * math.log10(math.e)


def march(ZL, Zs, Yp, length, n_eval=None):
    """Integrate dV/dd = Zs I, dI/dd = Yp V from the load (d = 0, V = ZL, I = 1) to d = length.
    Zs = R' + j w L', Yp = G' + j w C'. Returns (d, V, I) arrays."""
    def f(d, y):
        V = y[0] + 1j * y[1]
        I = y[2] + 1j * y[3]
        dV, dI = Zs * I, Yp * V
        return [dV.real, dV.imag, dI.real, dI.imag]
    y0 = [complex(ZL).real, complex(ZL).imag, 1.0, 0.0]
    t_eval = None if n_eval is None else np.linspace(0, length, n_eval)
    sol = solve_ivp(f, (0, length), y0, rtol=1e-11, atol=1e-13, t_eval=t_eval, method="DOP853")
    V = sol.y[0] + 1j * sol.y[1]
    I = sol.y[2] + 1j * sol.y[3]
    return sol.t, V, I


def lossless(Z0, f, vel=None):
    vel = vel or c0
    w = 2 * math.pi * f
    return 1j * w * Z0 / vel, 1j * w / (Z0 * vel)  # j w L', j w C'


def zin(ZL, Z0, frac_lambda, f=1e9, vel=None):
    vel = vel or c0
    Zs, Yp = lossless(Z0, f, vel)
    _, V, I = march(ZL, Zs, Yp, frac_lambda * vel / f)
    return V[-1] / I[-1]


def gamma(Z, Z0=50.0):
    return (Z - Z0) / (Z + Z0)


# ---------------------------------------------------------------- theory
G2 = brentq(lambda g: (1 + g) / (1 - g) - 2, 0, 0.99)
v.check("T 13-08.a", -20 * math.log10(G2))
v.check("T 13-08.b", -10 * math.log10(1 - G2**2))

# ---------------------------------------------------------------- Example 1
w1 = 2 * math.pi * 1e9
L1 = mu0 / (2 * math.pi) * math.log(3.5)
C1 = 2 * math.pi * 2.25 * e0 / math.log(3.5)
R1 = 3.376454508  # Problem 13-05.13's R' at 1 GHz
G1 = w1 * C1 * 0.0002
g1 = cmath.sqrt((R1 + 1j * w1 * L1) * (G1 + 1j * w1 * C1))
Z01 = cmath.sqrt((R1 + 1j * w1 * L1) / (G1 + 1j * w1 * C1))
v.check("Ex 13-08.1a", G1)
v.check("Ex 13-08.1b", g1.real)
v.check("Ex 13-08.1c", g1.real * NP_DB)
v.check("Ex 13-08.1d", g1.imag)
v.check("Ex 13-08.1e", 2 * math.pi / g1.imag * 100)
v.check("Ex 13-08.1f", Z01.real)
v.check("Ex 13-08.1g", Z01.imag)
Zl = math.sqrt(L1 / C1)
v.assert_true("low-loss alpha matches", abs((R1 / (2 * Zl) + G1 * Zl / 2) / g1.real - 1) < 1e-4)
# the lossy line marched for 1 m: a matched load stays matched and the voltage falls by exp(-alpha)
_, V, I = march(Z01, R1 + 1j * w1 * L1, G1 + 1j * w1 * C1, 1.0)
v.assert_true("marched lossy line: matched load", abs(V[-1] / I[-1] / Z01 - 1) < 1e-8)
v.assert_true("marched lossy line: attenuation", abs(abs(V[-1] / V[0]) - math.exp(g1.real)) < 1e-8)

# ---------------------------------------------------------------- Example 2
z8 = zin(100, 50, 1 / 8)
v.check("Ex 13-08.2a", z8.real)
v.check("Ex 13-08.2b", z8.imag)
v.check("Ex 13-08.2c", zin(100, 50, 1 / 4).real)
v.check("Ex 13-08.2d", zin(100, 50, 1 / 2).real)
v.assert_true("same |Gamma| at every length", abs(abs(gamma(z8)) - 1 / 3) < 1e-9)

# ---------------------------------------------------------------- Example 3
lam = c0 / 1e9
Xs = zin(0, 50, 0.02 / lam).imag
Xo = zin(1e12, 50, 0.05 / lam).imag
v.check("Ex 13-08.3a", Xs)
v.check("Ex 13-08.3b", Xs / w1 * 1e9)
v.check("Ex 13-08.3c", Xo)
v.check("Ex 13-08.3d", -1 / (w1 * Xo) * 1e12)
v.check("Ex 13-08.3e", 50 / c0 * 0.02 * 1e9)
v.check("Ex 13-08.3f", (Xs / w1 / (50 / c0 * 0.02) - 1) * 100)

# ---------------------------------------------------------------- Example 4
d, V, I = march(75, *lossless(50, 1e9), lam, n_eval=40001)
Vp = (V[0] + 50 * I[0]) / 2  # forward-wave phasor at the load
sc = 10 / abs(Vp)             # scale to a 10 V peak forward wave
Vf = np.abs(V) * sc
G4 = abs((V[0] - 50 * I[0]) / 2 / Vp)
v.check("Ex 13-08.4a", G4)
v.check("Ex 13-08.4b", Vf.max() / Vf.min())
v.check("Ex 13-08.4c", -20 * math.log10(G4))
v.check("Ex 13-08.4d", -10 * math.log10(1 - G4**2))
v.check("Ex 13-08.4e", 0.5 * (V[0] * np.conj(I[0])).real * sc**2)
v.check("Ex 13-08.4f", Vf.max())
v.check("Ex 13-08.4g", Vf.min())
v.assert_true("maximum at the load", abs(Vf[0] - Vf.max()) < 1e-9 * Vf.max())

# ---------------------------------------------------------------- Example 5
Z1 = brentq(lambda z: zin(100, z, 0.25, 2.4e9).real - 50, 51, 99, xtol=1e-12)
v.check("Ex 13-08.5a", Z1)
v.check("Ex 13-08.5b", (2 * c0 / 3) / 2.4e9 / 4 * 100)


def gq(f, ZL=100.0, Z1=Z1, f0=2.4e9):
    # electrical length scales with frequency: frac = 0.25 f/f0
    return abs(gamma(zin(ZL, Z1, 0.25 * f / f0, f)))


lo = brentq(lambda f: gq(f) - 0.1, 1.2e9, 2.4e9, xtol=1e3)
hi = brentq(lambda f: gq(f) - 0.1, 2.4e9, 3.6e9, xtol=1e3)
v.check("Ex 13-08.5c", (hi - lo) / 2.4e9 * 100)

# ---------------------------------------------------------------- Example 6 (lossy line, 3 dB, short)
alpha = 3 / NP_DB  # nepers over the whole length 1 m
w6 = 2 * math.pi * 1e9
L6, C6 = 50 / c0, 1 / (50 * c0)
R6 = 2 * 50 * alpha  # alpha = R/(2 Z0) with G = 0 (low loss)
_, V, I = march(0, R6 + 1j * w6 * L6, 1j * w6 * C6, 1.0)
Zin6 = V[-1] / I[-1]
Z06 = cmath.sqrt((R6 + 1j * w6 * L6) / (1j * w6 * C6))
g_in = abs((Zin6 - Z06) / (Zin6 + Z06))
v.check("Ex 13-08.6a", g_in)
v.check("Ex 13-08.6b", -20 * math.log10(g_in))
v.check("Ex 13-08.6c", (1 + g_in) / (1 - g_in))

# ---------------------------------------------------------------- practitioner and simulation
per_m = 21.5 / (100 * 0.3048)
v.check("Prac 13-08.a", per_m)
v.check("Prac 13-08.b", 10 * per_m)
v.check("Prac 13-08.c", -20 * math.log10(G2) + 2 * 10 * per_m)
v.check("Sim 13-08.a", z8.real)
v.check("Sim 13-08.b", z8.imag)
v.check("Sim 13-08.c", zin(100, math.sqrt(5000), 0.25).real)

# ---------------------------------------------------------------- Problems
v.check("13-08.1a", 75 / 2e8 * 1e9)
v.check("13-08.1b", 1 / (75 * 2e8) * 1e12)
v.check("13-08.1c", 2 * math.pi * 1e8 / 2e8)
z2 = zin(25 + 25j, 50, 0.25)
v.check("13-08.2a", z2.real)
v.check("13-08.2b", z2.imag)
for g, keys in ((0.1, "abc"), (0.3, "def")):
    v.check(f"13-08.3{keys[0]}", -20 * math.log10(g))
    v.check(f"13-08.3{keys[1]}", (1 + g) / (1 - g))
    v.check(f"13-08.3{keys[2]}", -10 * math.log10(1 - g * g))
z4 = zin(30 - 40j, 50, 0.3)
v.check("13-08.4a", z4.real)
v.check("13-08.4b", z4.imag)
frac5 = brentq(lambda fr: zin(0, 50, fr).imag - w1 * 10e-9, 0.01, 0.24, xtol=1e-14)
v.check("13-08.5a", 2 * math.pi * frac5)
v.check("13-08.5b", frac5)
v.check("13-08.5c", frac5 * lam * 100)
X6 = -1 / (w1 * 2e-12)
frac6 = brentq(lambda fr: zin(1e12, 50, fr).imag - X6, 0.01, 0.24, xtol=1e-14)
v.check("13-08.6a", X6)
v.check("13-08.6b", frac6 * lam * 100)
# 7: find the load whose standing wave has VSWR 2 and first minimum at 0.1 lambda, by solving for Gamma_L
GL7 = (1 / 3) * cmath.exp(1j * (2 * 2 * math.pi * 0.1 + math.pi))
ZL7 = 50 * (1 + GL7) / (1 - GL7)
d, V, I = march(ZL7, *lossless(50, 1e9), 0.5 * lam, n_eval=50001)
mag = np.abs(V)
v.assert_true("first minimum at 0.1 lambda", abs(d[np.argmin(mag[: len(mag) // 2 + 1])] / lam - 0.1) < 1e-4)
v.assert_true("VSWR 2", abs(mag.max() / mag.min() - 2) < 1e-6)
v.check("13-08.7a", abs(GL7))
v.check("13-08.7b", math.degrees(cmath.phase(GL7)))
v.check("13-08.7c", ZL7.real)
v.check("13-08.7d", ZL7.imag)
# 8: generator 10 V, 50 ohm; Zin of the line is computed, then the power into the line (= load power, lossless)
for ZL, key in ((100, "a"), (50, "b")):
    Zi = zin(ZL, 50, 0.37)
    Iin = 10 / (50 + Zi)
    v.check(f"13-08.8{key}", 0.5 * abs(Iin) ** 2 * Zi.real)
G9 = brentq(lambda g: (1 + g) / (1 - g) - 3, 0, 0.99)
v.check("13-08.9a", -20 * math.log10(G9) + 2 * 10 * per_m)
f0 = 1e9
Zt = math.sqrt(5000)
lo = brentq(lambda f: abs(gamma(zin(100, Zt, 0.25 * f / f0, f))) - 0.05, 0.5e9, 1e9, xtol=1e2)
hi = brentq(lambda f: abs(gamma(zin(100, Zt, 0.25 * f / f0, f))) - 0.05, 1e9, 1.5e9, xtol=1e2)
v.check("13-08.10a", (hi - lo) / f0 * 100)
Zt = math.sqrt(500)
lo = brentq(lambda f: abs(gamma(zin(10, Zt, 0.25 * f / f0, f))) - 0.1, 0.5e9, 1e9, xtol=1e2)
hi = brentq(lambda f: abs(gamma(zin(10, Zt, 0.25 * f / f0, f))) - 0.1, 1e9, 1.5e9, xtol=1e2)
v.check("13-08.10b", (hi - lo) / f0 * 100)
for f, keys in ((1e6, ("a", "b", "c", "d")), (1e8, ("e", None, "f", "g"))):
    w = 2 * math.pi * f
    Zs, Yp = 0.5 + 1j * w * 250e-9, 1j * w * 100e-12
    # characteristic impedance as the input impedance of a long matched-looking line: march a matched load
    g = cmath.sqrt(Zs * Yp)
    Z0 = cmath.sqrt(Zs / Yp)
    _, V, I = march(Z0, Zs, Yp, 2.0)
    v.assert_true(f"Z0 at {f:g} Hz is self-reproducing", abs(V[-1] / I[-1] / Z0 - 1) < 1e-8)
    v.check(f"13-08.11{keys[0]}", g.real)
    if keys[1]:
        v.check(f"13-08.11{keys[1]}", g.real * NP_DB)
    v.check(f"13-08.11{keys[2]}", Z0.real)
    v.check(f"13-08.11{keys[3]}", Z0.imag)
G12 = 0.5 * 100e-12 / 250e-9
v.check("13-08.12a", G12)
gs = [cmath.sqrt((0.5 + 1j * 2 * math.pi * f * 250e-9) * (G12 + 1j * 2 * math.pi * f * 100e-12)) for f in (1e3, 1e6, 1e9)]
v.assert_true("distortionless: alpha independent of frequency", max(abs(g.real - gs[0].real) for g in gs) < 1e-12)
v.check("13-08.12b", gs[0].real)
v.check("13-08.12c", cmath.sqrt((0.5 + 1j * 1e3 * 250e-9) / (G12 + 1j * 1e3 * 100e-12)).real)
v.check("13-08.12d", 2 * math.pi * 1e9 / gs[2].imag)
z13a = zin(20 + 30j, 50, 0.5)
z13b = zin(20 + 30j, 50, 0.25)
v.check("13-08.13a", z13a.real)
v.check("13-08.13b", z13a.imag)
v.check("13-08.13c", z13b.real)
v.check("13-08.13d", z13b.imag)
d, V, I = march(25, *lossless(50, 1e9), 0.5 * lam, n_eval=50001)
scale = 1 / abs((V[0] + 50 * I[0]) / 2)  # forward-wave amplitude 1 V at the load
mag = np.abs(V) * scale
v.check("13-08.14a", mag.min())
v.check("13-08.14b", mag.max())
v.assert_true("minimum at the load", abs(mag[0] - mag.min()) < 1e-9)
v.check("13-08.14c", d[np.argmax(mag)] * 100)
v.check("13-08.14d", abs(I[0]) * scale * 1e3)

# ---------------------------------------------------------------- Lab
if lab.exists():
    # apparent return loss of a short through 1, 3 and 6 dB of line, and quarter-wave bandwidth for a 4:1 step
    Zt = math.sqrt(200 * 50)
    lo = brentq(lambda f: abs(gamma(zin(200, Zt, 0.25 * f / f0, f))) - 0.1, 0.5e9, 1e9, xtol=1e2)
    hi = brentq(lambda f: abs(gamma(zin(200, Zt, 0.25 * f / f0, f))) - 0.1, 1e9, 1.5e9, xtol=1e2)
    v.check("Lab 13-08.a", (hi - lo) / f0 * 100)
    # a short seen through 5 m of RG-58 at 1 GHz, by marching a lossy line with alpha = 0.7054 dB/m
    a5 = per_m / NP_DB
    _, V, I = march(0, 2 * 50 * a5 + 1j * w1 * 50 / c0, 1j * w1 / (50 * c0), 5.0)
    Z05 = cmath.sqrt((2 * 50 * a5 + 1j * w1 * 50 / c0) / (1j * w1 / (50 * c0)))
    v.check("Lab 13-08.b", -20 * math.log10(abs(gamma(V[-1] / I[-1], Z05))))

sys.exit(v.finish())
