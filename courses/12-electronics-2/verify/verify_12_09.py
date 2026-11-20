#!/usr/bin/env python3
"""Verify every number in chapter 12-09 (oscillators), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- RC networks (Wien bridge, phase-shift ladder) solved by complex nodal analysis, with the zero-phase
  frequency found by root finding on the imaginary part;
- startup boundaries (Colpitts, cross-coupled LC tank, ring oscillator) from the natural frequencies of each
  circuit's state equations: the critical gain is where the rightmost eigenvalue reaches the imaginary axis;
- the crystal's resonances and load-capacitance frequency from its impedance;
- the Wien oscillator's amplitude by describing function (numerical quadrature) and by integrating its
  nonlinear state equations, with the frequency from zero crossings.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.linalg import eigvals
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "12-09-oscillators.md", COURSE / "solutions" / "12-09-solutions.md"]
lab = COURSE / "labs" / "12-09-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-09", *files)
TP = 2 * math.pi


# ============================================================ RC networks by nodal analysis
def wien_beta(f, R1, C1, R2, C2):
    """v_p / v_out with the series arm (R1 then C1) from out to p and the parallel arm (R2 || C2) to ground."""
    s = 1j * TP * f
    # nodes a (between R1 and C1) and p; out driven at 1 V
    Y = np.array([[1 / R1 + s * C1, -s * C1], [-s * C1, s * C1 + 1 / R2 + s * C2]])
    b = np.array([1 / R1, 0.0])
    return np.linalg.solve(Y, b)[1]


def zero_phase(fun, lo, hi):
    return brentq(lambda f: fun(f).imag, lo, hi, xtol=1e-12, rtol=1e-14)


def ladder(f, R, C, n=3):
    """Unbuffered RC low-pass ladder (series R, shunt C): v_n / v_in by nodal analysis."""
    s = 1j * TP * f
    Y = np.zeros((n, n), complex)
    b = np.zeros(n, complex)
    for k in range(n):
        Y[k, k] += 1 / R + s * C
        if k + 1 < n:
            Y[k, k] += 1 / R
            Y[k, k + 1] -= 1 / R
            Y[k + 1, k] -= 1 / R
    b[0] = 1 / R
    return np.linalg.solve(Y, b)[-1]


R, C = 10e3, 10e-9
f1 = zero_phase(lambda f: wien_beta(f, R, C, R, C), 100, 1e4)
b1 = wien_beta(f1, R, C, R, C).real
v.check("T 12-09.a", b1)
v.check("Ex 12-09.1a", f1)
v.check("Ex 12-09.1b", 1 / b1)
v.check("Ex 12-09.1c", (1 / b1 - 1) * 10)

Rl, Cl = 10e3, 1e-9
f2 = zero_phase(lambda f: ladder(f, Rl, Cl), 1 / (TP * Rl * Cl), 10 / (TP * Rl * Cl))   # brackets x = wRC in 1..10
g2 = ladder(f2, Rl, Cl).real
v.check("T 12-09.b", 1 / g2)
v.check("Ex 12-09.2a", f2 / 1e3)
v.check("Ex 12-09.2b", abs(1 / g2))
# isolated sections: each gives 60 degrees where |1/(1 + j wRC)| has phase -60
x_iso = brentq(lambda x: math.degrees(math.atan(x)) - 60, 0.1, 10)
v.check("Ex 12-09.2c", (1 / abs(1 / (1 + 1j * x_iso))) ** 3)
# the ladder's cubic: recover the polynomial coefficients numerically and compare with 1, 6, 5, 1
ws = np.linspace(0.1, 3, 7)
den = np.array([1 / ladder(w / (TP * Rl * Cl), Rl, Cl) for w in ws])
coef = np.polyfit(1j * ws, den, 3)
v.assert_true("ladder denominator is (sRC)^3 + 5(sRC)^2 + 6 sRC + 1", np.allclose(coef, [1, 5, 6, 1], atol=1e-8))


# ============================================================ LC oscillators from state equations
def colpitts_eigs(gm, L, C1, C2, R):
    """States v_d, v_g, i_L (i_L flows from drain to gate through L); C x' = -G x."""
    C = np.diag([C1, C2, L])
    G = np.array([[1 / R, gm, 1.0],
                  [0.0, 0.0, -1.0],
                  [-1.0, 1.0, 0.0]])
    return eigvals(-G, C)


def critical(fun, lo, hi):
    g = brentq(lambda x: np.max(fun(x).real), lo, hi, xtol=1e-15, rtol=1e-13)
    e = fun(g)
    return g, abs(e[np.argmax(e.real)].imag) / TP     # frequency of the eigenvalue on the axis


gmc, f4 = critical(lambda g: colpitts_eigs(g, 1e-6, 1e-9, 1e-9, 1e3), 1e-5, 1e-1)
v.check("Ex 12-09.4a", f4 / 1e6)
v.check("Ex 12-09.4b", gmc * 1e3)


def tank_eigs(gm, L, C, Rp):
    """Differential LC tank with parallel loss Rp and the cross-coupled pair's conductance -gm/2."""
    C_ = np.diag([C, L])
    G = np.array([[1 / Rp - gm / 2, 1.0], [-1.0, 0.0]])
    return eigvals(-G, C_)


L3, C3, Q3 = 2e-9, 2e-12, 10
f30 = 1 / (TP * math.sqrt(L3 * C3))
Rp3 = Q3 * TP * f30 * L3
gm3, f3 = critical(lambda g: tank_eigs(g, L3, C3, Rp3), 1e-5, 1.0)
v.check("Ex 12-09.3a", f3 / 1e9)
v.check("Ex 12-09.3b", Rp3)
v.check("Ex 12-09.3c", gm3 * 1e3)
v.check("Ex 12-09.3d", np.max(np.abs(tank_eigs(0, L3, 2.4e-12, 1e30).imag)) / TP / 1e9)
v.check("Ex 12-09.3e", np.max(np.abs(tank_eigs(0, L3, 1.6e-12, 1e30).imag)) / TP / 1e9)


# ============================================================ crystal
def crystal_z(f, Lm, Cm, Rm, C0, CL=None):
    s = 1j * TP * f
    zm = Rm + s * Lm + 1 / (s * Cm)
    z = 1 / (1 / zm + s * C0)
    return z if CL is None else z + 1 / (s * CL)


fs, Cm, Rm, C0 = 10e6, 25e-15, 20.0, 5e-12
Lm = brentq(lambda L: (TP * fs) ** 2 * L * Cm - 1, 1e-6, 1.0, xtol=1e-18)
fs_x = brentq(lambda f: (TP * f * Lm - 1 / (TP * f * Cm)), 9e6, 11e6, xtol=1e-9)
fp_x = brentq(lambda f: (1 / crystal_z(f, Lm, Cm, 1e-9, C0)).imag, fs * 1.0001, fs * 1.01, xtol=1e-6)
fL_x = brentq(lambda f: crystal_z(f, Lm, Cm, 1e-9, C0, 10e-12).imag, fs * 1.00001, fs * 1.002, xtol=1e-6)
v.check("Ex 12-09.5a", Lm * 1e3)
v.check("Ex 12-09.5b", TP * fs_x * Lm / Rm)
v.check("Ex 12-09.5c", (fp_x - fs_x) / 1e3)
v.check("Ex 12-09.5d", fL_x - fs_x)
v.check("Ex 12-09.5e", (fL_x - fs_x) / fs_x * 1e6)
v.check("Ex 12-09.5f", fs * Cm / (2 * (C0 + 10e-12)))


# ============================================================ ring oscillators
def ring_eigs(A, N, tau):
    """N inverting single-pole stages in a loop: tau x_k' = -x_k - A x_{k-1}."""
    M = -np.eye(N)
    for k in range(N):
        M[k, k - 1] += -A
    return np.linalg.eigvals(M / tau)


v.check("Ex 12-09.6a", 1 / (2 * 5 * 20e-12) / 1e9)
v.check("Ex 12-09.6b", 5 * 2e-15 * 0.8 ** 2 * 5e9 * 1e6)
A3, f36 = critical(lambda a: ring_eigs(a, 3, 10e-12), 1.01, 10)
v.check("Ex 12-09.6c", f36 / 1e9)
v.check("Ex 12-09.6d", A3)

# ============================================================ Wien oscillator with a tanh amplifier
G, Vs = 3.3, 1.0


def df(a, fn):
    val, _ = quad(lambda th: fn(a * math.sin(th)) * math.sin(th), 0, TP, limit=400)
    return val / (math.pi * a)


a_df = brentq(lambda a: df(a, lambda x: Vs * math.tanh(G * x / Vs)) - 3, 1e-3, 10, xtol=1e-12)


def wien_rhs(t, x):
    vc1, vp = x
    vo = Vs * math.tanh(G * vp / Vs)
    i = (vo - vc1 - vp) / R
    return [i / C, (i - vp / R) / C]


sol = solve_ivp(wien_rhs, (0, 0.2), [0.0, 1e-3], max_step=2e-6, rtol=1e-10, atol=1e-12)
t, vp = sol.t, sol.y[1]
late = t > 0.15
k = np.where((vp[:-1] < 0) & (vp[1:] >= 0) & late[:-1])[0]
tz = t[k] - vp[k] * (t[k + 1] - t[k]) / (vp[k + 1] - vp[k])
f_sim = 1 / float(np.mean(np.diff(tz)))
amp_sim = float(np.max(vp[late]))
v.check("Sim 12-09.a", f_sim)
v.check("Sim 12-09.b", 100 * (f_sim / f1 - 1))
v.check("Sim 12-09.c", a_df)
v.assert_true("describing-function amplitude within 0.2% of the simulated amplitude", abs(amp_sim / a_df - 1) < 2e-3)

# ============================================================ solutions
v.check("12-09.1a", 10 * 0.12)
v.check("12-09.1b", 1 / 0.12)
f_p2 = zero_phase(lambda f: wien_beta(f, 4.7e3, 22e-9, 4.7e3, 22e-9), 100, 1e4)
v.check("12-09.2a", f_p2)
v.check("12-09.2b", 1 / wien_beta(f_p2, 4.7e3, 22e-9, 4.7e3, 22e-9).real - 1)
v.check("12-09.3a", 1 / (2 * 7 * 15e-12) / 1e9)
f_p4 = zero_phase(lambda f: wien_beta(f, 10e3, 10e-9, 10e3, 20e-9), 100, 1e4)
b_p4 = wien_beta(f_p4, 10e3, 10e-9, 10e3, 20e-9).real
v.check("12-09.4a", f_p4)
v.check("12-09.4b", b_p4)
v.check("12-09.4c", 1 / b_p4)
f_ref = zero_phase(lambda f: ladder(f, 1e3, 10e-9), 1 / (TP * 1e3 * 10e-9), 10 / (TP * 1e3 * 10e-9))
R5 = 1e3 * f_ref / 10e3                       # the ladder's frequency scales as 1/R at fixed C
v.check("12-09.5a", R5)
v.check("12-09.5b", abs(1 / ladder(10e3, R5, 10e-9).real))
gm6, f6 = critical(lambda g: colpitts_eigs(g, 10e-6, 2e-9, 8e-9, 2e3), 1e-5, 1e-1)
v.check("12-09.6a", 2e-9 * 8e-9 / 10e-9 * 1e9)
v.check("12-09.6b", f6 / 1e6)
v.check("12-09.6c", gm6 * 1e3)
f70 = 1 / (TP * math.sqrt(1e-9 * 1e-12))
Rp7 = 15 * TP * f70 * 1e-9
gm7, f7 = critical(lambda g: tank_eigs(g, 1e-9, 1e-12, Rp7), 1e-5, 1.0)
v.check("12-09.7a", f7 / 1e9)
v.check("12-09.7b", Rp7)
v.check("12-09.7c", gm7 * 1e3)
w8 = TP * 5e9
z8 = 1 + 1j * w8 * 2e-9                      # series R-L; its parallel equivalent's resistance is 1/Re(1/z)
v.check("12-09.8a", w8 * 2e-9 / 1.0)
v.check("12-09.8b", 1 / (1 / z8).real)
v.check("12-09.8c", (w8 * 2e-9) ** 2 * 1.0)
Lm9 = brentq(lambda L: (TP * 32768) ** 2 * L * 2e-15 - 1, 1.0, 1e6, xtol=1e-9)
v.check("12-09.9a", Lm9)
v.check("12-09.9b", TP * 32768 * Lm9 / 40e3)
fL10 = brentq(lambda f: crystal_z(f, Lm, Cm, 1e-9, C0, 10e-12).imag, fs * 1.00001, fs * 1.002, xtol=1e-7)
fL12 = brentq(lambda f: crystal_z(f, Lm, Cm, 1e-9, C0, 12e-12).imag, fs * 1.00001, fs * 1.002, xtol=1e-7)
v.check("12-09.10a", fL10 - fL12)
v.check("12-09.10b", (fL10 - fL12) / fs * 1e6)
v.check("12-09.10c", fs * Cm / 2 * (1 / (C0 + 10e-12) - 1 / (C0 + 12e-12)))
A5, f5 = critical(lambda a: ring_eigs(a, 5, 10e-12), 1.01, 10)
v.check("12-09.11a", f5 / 1e9)
v.check("12-09.11b", A5)
fund = df(0.5, lambda x: math.copysign(1.0, x)) * 0.5
v.check("12-09.12a", fund)
v.check("12-09.12b", fund * b1)

# ============================================================ lab README (ngspice Wien oscillator)
if lab.exists():
    v.check("Lab 12-09.a", f_sim)
    v.check("Lab 12-09.b", amp_sim)

sys.exit(v.finish())
