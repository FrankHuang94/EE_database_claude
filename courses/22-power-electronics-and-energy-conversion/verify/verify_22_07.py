#!/usr/bin/env python3
"""Verify every number in chapter 22-07 (converter dynamics and control), its problems and its lab.

Independent routes (the lab module control.py uses the closed-form transfer functions):
- small-signal models are obtained by a numerical Jacobian of the nonlinear averaged state equations, and transfer
  functions are evaluated as C(sI − A)⁻¹B; resonant frequency and Q come from the eigenvalues of A; RHP zeros from
  the numerator of the state-space transfer function (scipy.signal.ss2tf);
- the type-III network is analysed by its impedances and its component values solved by least squares against the
  target transfer function; crossover and phase margin are found by root finding on |T| = 1;
- the current-mode perturbation ratio is measured by simulating one switching cycle's waveform geometry;
- delay phase comes from the argument of exp(−jωt_d); output-impedance peaks from numerical maximisation.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize, signal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("22-07", ROOT / "chapters" / "22-07-converter-dynamics-and-control.md",
                        ROOT / "solutions" / "22-07-solutions.md", LAB / "README.md")


# ---------------------------------------------------------------- averaged models and numerical linearization
def jac(fun, x0, u0, eps=1e-7):
    n, m = len(x0), len(u0)
    f0 = np.array(fun(x0, u0))
    A = np.zeros((n, n))
    B = np.zeros((n, m))
    for i in range(n):
        dx = np.zeros(n)
        dx[i] = eps * max(1.0, abs(x0[i]))
        A[:, i] = (np.array(fun(x0 + dx, u0)) - np.array(fun(x0 - dx, u0))) / (2 * dx[i])
    for j in range(m):
        du = np.zeros(m)
        du[j] = eps * max(1.0, abs(u0[j]))
        B[:, j] = (np.array(fun(x0, u0 + du)) - np.array(fun(x0, u0 - du))) / (2 * du[j])
    return A, B, f0


def buck_avg(L, C, R):
    def f(x, u):                     # x = [iL, v], u = [d, vg, i_inject]
        return [(u[0] * u[1] - x[1]) / L, (x[0] - x[1] / R + u[2]) / C]
    return f


def boost_avg(L, C, R):
    def f(x, u):                     # u = [d, vg]
        return [(u[1] - (1 - u[0]) * x[1]) / L, ((1 - u[0]) * x[0] - x[1] / R) / C]
    return f


def buckboost_avg(L, C, R):
    def f(x, u):                     # inverting buck-boost, v < 0
        return [(u[0] * u[1] + (1 - u[0]) * x[1]) / L, (-(1 - u[0]) * x[0] - x[1] / R) / C]
    return f


def steady(fun, x_guess, u):
    return optimize.fsolve(lambda x: fun(x, u), x_guess, xtol=1e-13)


def tf_eval(A, B, Cm, f, col=0):
    s = 2j * math.pi * f
    return (Cm @ np.linalg.solve(s * np.eye(len(A)) - A, B[:, col]))


def f0_q(A):
    lam = np.linalg.eigvals(A)
    lam = lam[np.argmax(lam.imag)]
    w0 = abs(lam)
    return w0 / (2 * math.pi), w0 / (-2 * lam.real)


def rhp_zero(A, B, Cm, col=0):
    num, _ = signal.ss2tf(A, B[:, [col]], Cm.reshape(1, -1), np.zeros((1, 1)))
    z = np.roots(np.trim_zeros(num[0], "f"))
    z = z[np.abs(z.imag) < 1e-6 * np.abs(z)]
    return z[z.real > 0].real.max() / (2 * math.pi)


CV = np.array([0.0, 1.0])

# ---------------------------------------------------------------- Example 22-07.1
print("Example 22-07.1")
L1, C1, R1, VG1, D1 = 0.6e-6, 62.5e-6, 0.12, 12.0, 0.1
fb = buck_avg(L1, C1, R1)
x1 = steady(fb, [10, 1.2], [D1, VG1, 0])
A1, B1, _ = jac(fb, x1, np.array([D1, VG1, 0.0]))
v.check("Ex 22-07.1a", x1[1] / x1[0])
f01, q1 = f0_q(A1)
v.check("Ex 22-07.1b", f01 / 1e3)
v.check("Ex 22-07.1c", q1)
v.check("Ex 22-07.1d", 20 * math.log10(abs(tf_eval(A1, B1, CV, 1e-3))))
v.check("Ex 22-07.1e", optimize.brentq(lambda f: abs(1 + 2j * math.pi * f * 2e-3 * C1) - math.sqrt(2), 1, 1e9) / 1e6)
g60 = tf_eval(A1, B1, CV, 60e3)
v.check("Ex 22-07.1f", 20 * math.log10(abs(g60)))
v.check("Ex 22-07.1g", math.degrees(cmath.phase(g60)))
v.check("Ex 22-07.1h", abs(g60))
v.check("Ex 22-07.1i", VG1 * (f01 / 60e3) ** 2)

# ---------------------------------------------------------------- Example 22-07.2
print("Example 22-07.2")
L2, C2, VG2, V2, I2 = 1e-6, 22e-6, 3.6, 5.0, 1.5
R2 = V2 / I2
D2 = optimize.brentq(lambda d: VG2 / (1 - d) - V2, 0, 0.99)
fbo = boost_avg(L2, C2, R2)
x2 = steady(fbo, [2, 5], [D2, VG2])
A2, B2, _ = jac(fbo, x2, np.array([D2, VG2]))
v.check("Ex 22-07.2a", D2)
v.check("Ex 22-07.2b", R2)
v.check("Ex 22-07.2c", abs(tf_eval(A2, B2, CV, 1e-3)))
f02, q2 = f0_q(A2)
v.check("Ex 22-07.2d", f02 / 1e3)
v.check("Ex 22-07.2e", q2)
fz2 = rhp_zero(A2, B2, CV)
v.check("Ex 22-07.2f", fz2 / 1e3)
v.check("Ex 22-07.2g", fz2 / 5 / 1e3)
fbo3 = boost_avg(L2, C2, V2 / 3.0)
x3 = steady(fbo3, [4, 5], [D2, VG2])
A3, B3, _ = jac(fbo3, x3, np.array([D2, VG2]))
v.check("Ex 22-07.2h", rhp_zero(A3, B3, CV) / 1e3)

# ---------------------------------------------------------------- Example 22-07.3
print("Example 22-07.3")
FC, PM = 60e3, 60.0
plant = lambda f: tf_eval(A1, B1, CV, f) / 1.0               # V_M = 1, H = 1
php = math.degrees(cmath.phase(plant(FC)))
boost = PM - 90 - php
v.check("Ex 22-07.3a", boost)
# k by root finding on the compensator's phase at crossover
comp_phase = lambda k: math.degrees(cmath.phase((1 + 1j * k) ** 2 / (1 + 1j / k) ** 2))
k3 = optimize.brentq(lambda k: comp_phase(k) - boost, 1.01, 100)
v.check("Ex 22-07.3b", k3)
fz3, fp3 = FC / k3, FC * k3
v.check("Ex 22-07.3c", fz3 / 1e3)
v.check("Ex 22-07.3d", fp3 / 1e3)
gc_needed = 1 / abs(plant(FC))
v.check("Ex 22-07.3l", gc_needed)
shape = lambda f: (1 + 2j * math.pi * f / (2 * math.pi * fz3)) ** 2 / (1 + 2j * math.pi * f / (2 * math.pi * fp3)) ** 2
wI = optimize.brentq(lambda w: abs(w / (2j * math.pi * FC) * shape(FC)) - gc_needed, 1, 1e7)
v.check("Ex 22-07.3e", wI / (2 * math.pi) / 1e3)
v.check("Ex 22-07.3m", abs((1 + 1j * k3) / (1 + 1j / k3)) ** 2)


def network(f, Rin, R2, C1, C2, R3, C3):
    s = 2j * math.pi * f
    zf = (R2 + 1 / (s * C1)) * (1 / (s * C2)) / (R2 + 1 / (s * C1) + 1 / (s * C2))
    zi = Rin * (R3 + 1 / (s * C3)) / (Rin + R3 + 1 / (s * C3))
    return zf / zi


target = lambda f: wI / (2j * math.pi * f) * shape(f)
freqs = np.logspace(2.5, 6, 25)


def resid(p):
    r2, c1, c2, r3, c3 = np.exp(p)
    out = []
    for f in freqs:
        e = network(f, 10e3, r2, c1, c2, r3, c3) / target(f) - 1
        out += [e.real, e.imag]
    return out


sol = optimize.least_squares(resid, np.log([1e3, 1e-8, 1e-9, 500, 1e-9]), xtol=1e-15, ftol=1e-15, gtol=1e-15)
r2s, c1s, c2s, r3s, c3s = np.exp(sol.x)
v.check("Ex 22-07.3n", (c1s + c2s) * 1e9)
v.check("Ex 22-07.3f", c1s * 1e9)
v.check("Ex 22-07.3g", c2s * 1e9)
v.check("Ex 22-07.3h", r2s)
v.check("Ex 22-07.3i", r3s)
v.check("Ex 22-07.3j", c3s * 1e9)
loop = lambda f: network(f, 10e3, r2s, c1s, c2s, r3s, c3s) * plant(f)
fcx = optimize.brentq(lambda f: abs(loop(f)) - 1, 10e3, 200e3, xtol=1e-6)
v.check("Ex 22-07.3o", fcx / 1e3)
v.check("Ex 22-07.3k", 180 + math.degrees(cmath.phase(loop(fcx))))


# ---------------------------------------------------------------- Example 22-07.4 (waveform-geometry simulation)
def next_start(i0, vc, m1, m2, ma, T):
    """One cycle of peak current mode with an artificial ramp: turn off when i + ma t = vc (in amperes)."""
    t_on = (vc - i0) / (m1 + ma)
    return i0 + m1 * t_on - m2 * (T - t_on)


def alpha_sim(m1, m2, ma, T=1.0):
    D = m2 / (m1 + m2)
    i_ss = 5.0
    vc = i_ss + (m1 + ma) * D * T
    eps = 1e-6
    return (next_start(i_ss + eps, vc, m1, m2, ma, T) - next_start(i_ss, vc, m1, m2, ma, T)) / eps


print("Example 22-07.4")
m1, m2 = (5 - 3.3) / 2.2, 3.3 / 2.2                          # A/µs
v.check("Ex 22-07.4a", m2 / (m1 + m2))
v.check("Ex 22-07.4b", m1)
v.check("Ex 22-07.4c", m2)
v.check("Ex 22-07.4d", alpha_sim(m1, m2, 0.0))
a4 = alpha_sim(m1, m2, m2 / 2)
v.check("Ex 22-07.4e", a4)
i = 1.0
for _ in range(5):
    i *= a4
v.check("Ex 22-07.4f", i)
v.check("Ex 22-07.4g", optimize.brentq(lambda ma: abs(alpha_sim(m1, m2, ma)) - 1, 0, m2))
v.check("Ex 22-07.4h", m2 / 2 * 50e-3 * 1e3)

# ---------------------------------------------------------------- Examples 22-07.5 and 22-07.6
print("Examples 22-07.5, 22-07.6")
drp = lambda di, fc, c: di * abs(1 / (2j * math.pi * fc * c))
v.check("Ex 22-07.5a", drp(20, 100e3, 1e-3) * 1e3)
v.check("Ex 22-07.5b", optimize.brentq(lambda c: drp(20, 100e3, c) - 0.02, 1e-6, 1) * 1e3)
v.check("Ex 22-07.5c", optimize.brentq(lambda f: drp(20, f, 1e-3) - 0.02, 1e3, 1e7) / 1e3)
dphase = lambda fc, td: -math.degrees(cmath.phase(cmath.exp(-2j * math.pi * fc * td)) % (2 * math.pi) - 2 * math.pi)
td6 = 1.5 / 500e3
v.check("Ex 22-07.6a", td6 * 1e6)
v.check("Ex 22-07.6b", dphase(50e3, td6))
v.check("Ex 22-07.6c", optimize.brentq(lambda f: dphase(f, td6) - 20, 1, 1e6) / 1e3)
v.check("Ex 22-07.6d", optimize.brentq(lambda f: dphase(f, 1.5e-6) - 20, 1, 1e6) / 1e3)
v.check("Txt 22-07.a", dphase(0.1 / 1e-6, 1e-6))
v.check("Txt 22-07.b", dphase(0.1 / 1e-6, 2e-6))

# ---------------------------------------------------------------- problems
print("Problems")
fp1 = buck_avg(10e-6, 100e-6, 1.2)
xp1 = steady(fp1, [10, 12], [0.25, 48, 0])
Ap1, Bp1, _ = jac(fp1, xp1, np.array([0.25, 48.0, 0.0]))
f0p, qp = f0_q(Ap1)
v.check("22-07.1a", f0p / 1e3)
v.check("22-07.1b", qp)
v.check("22-07.1c", 20 * math.log10(abs(tf_eval(Ap1, Bp1, CV, 1e-3))))
v.check("22-07.2", abs(tf_eval(Ap1, Bp1, CV, f0p, col=2)))
for k, I in (("a", 1), ("b", 5)):
    fq = boost_avg(22e-6, 100e-6, 48 / I)
    xq = steady(fq, [4 * I, 48], [0.75, 12])
    Aq, Bq, _ = jac(fq, xq, np.array([0.75, 12.0]))
    zq = rhp_zero(Aq, Bq, CV)
    v.check(f"22-07.3{k}", zq / 1e3)
v.check("22-07.3c", zq / 5)
b4 = 45 - 90 + 170
v.check("22-07.4a", b4)
v.check("22-07.4b", optimize.brentq(lambda k: comp_phase(k) - b4, 1.01, 100))
fpole = optimize.brentq(lambda f: abs(1 + 2j * math.pi * f * 0.12 * 62.5e-6) - math.sqrt(2), 1, 1e8)
v.check("22-07.5a", fpole / 1e3)
ph5 = math.degrees(cmath.phase(1 / (1 + 2j * math.pi * 60e3 * 0.12 * 62.5e-6)))
v.check("22-07.5b", ph5)
b5 = 60 - 90 - ph5
v.check("22-07.5c", b5)
k5 = optimize.brentq(lambda k: math.degrees(cmath.phase((1 + 1j * k) / (1 + 1j / k))) - b5, 1.01, 100)
v.check("22-07.5d", k5)
v.check("22-07.5e", 60 / k5)
v.check("22-07.5f", 60 * k5)
mb1, mb2 = 12 / 22, 36 / 22
v.check("22-07.6a", mb1)
v.check("22-07.6b", mb2)
v.check("22-07.6c", alpha_sim(mb1, mb2, 0.0))
v.check("22-07.6d", optimize.brentq(lambda ma: abs(alpha_sim(mb1, mb2, ma)) - 1, 0, mb2))
v.check("22-07.6e", alpha_sim(mb1, mb2, mb2 / 2))
v.check("22-07.7", optimize.brentq(lambda c: drp(100, 200e3, c) - 0.03, 1e-6, 1) * 1e3)
v.check("22-07.8a", optimize.brentq(lambda f: dphase(f, 1e-6) - 30, 1, 1e6) / 1e3)
v.check("22-07.8b", 60 - dphase(100e3, 1e-6))
gvg = abs(tf_eval(Ap1, Bp1, CV, 100, col=1))                  # D at low frequency
v.check("22-07.9a", 0.25 / 301 * 1e4 / 1e4)
v.check("22-07.9b", 20 * math.log10(0.25 / 301))
v.assert_true("buck line-to-output gain is D at low frequency", abs(gvg - 0.25) < 1e-3)
fbb = buckboost_avg(10e-6, 100e-6, 6.0)
xbb = steady(fbb, [4, -12], [0.5, 12])
Abb, Bbb, _ = jac(fbb, xbb, np.array([0.5, 12.0]))
v.check("22-07.10b", rhp_zero(Abb, Bbb, CV) / 1e3)
v.check("22-07.10c", abs(tf_eval(Abb, Bbb, CV, 1e-3)))
v.assert_true("buck-boost steady state is −12 V", abs(xbb[1] + 12) < 1e-9)
target11 = lambda f: 5000 / (2j * math.pi * f) * (1 + 1j * f / 12.5e3) ** 2 / (1 + 1j * f / 200e3) ** 2


def resid11(p):
    r2, c1, c2, r3, c3 = np.exp(p)
    out = []
    for f in freqs:
        e = network(f, 20e3, r2, c1, c2, r3, c3) / target11(f) - 1
        out += [e.real, e.imag]
    return out


s11 = optimize.least_squares(resid11, np.log([1e3, 1e-8, 1e-9, 1e3, 1e-9]), xtol=1e-15, ftol=1e-15, gtol=1e-15)
r2b, c1b, c2b, r3b, c3b = np.exp(s11.x)
v.check("22-07.11a", (c1b + c2b) * 1e9)
v.check("22-07.11b", c1b * 1e9)
v.check("22-07.11c", c2b * 1e9)
v.check("22-07.11d", r2b)
v.check("22-07.11e", r3b)
v.check("22-07.11f", c3b * 1e9)
zo12 = lambda f: abs(tf_eval(Ap1, Bp1, CV, f, col=2))
zcl12 = lambda f: abs(tf_eval(Ap1, Bp1, CV, f, col=2) / (1 + 2 * math.pi * 20e3 / (2j * math.pi * f)))
v.check("22-07.12a", zo12(20e3))
v.check("22-07.12b", zcl12(20e3))
v.check("22-07.12c", abs(1 / (2j * math.pi * 20e3 * 100e-6)))
pk = optimize.minimize_scalar(lambda lf: -zcl12(10 ** lf), bounds=(3, 4.5), method="bounded", options={"xatol": 1e-10})
v.check("22-07.12d", -pk.fun)
v.check("22-07.12e", 10 ** pk.x / 1e3)

# ---------------------------------------------------------------- lab
print("Lab")
v.check("Lab 22-07.a", abs(tf_eval(A2, B2, CV, 1e3)))
gz = tf_eval(A2, B2, CV, fz2)
v.check("Lab 22-07.b", abs(gz))
ph = np.unwrap([cmath.phase(tf_eval(A2, B2, CV, f)) for f in np.logspace(1, math.log10(fz2), 4000)])
v.check("Lab 22-07.c", math.degrees(ph[-1]))
zcl = lambda f: abs(tf_eval(A1, B1, CV, f, col=2) / (1 + loop(f)))
pk3 = optimize.minimize_scalar(lambda lf: -zcl(10 ** lf), bounds=(4, 5.2), method="bounded", options={"xatol": 1e-10})
v.check("Lab 22-07.d", -pk3.fun * 1e3)
v.check("Lab 22-07.f", 10 ** pk3.x / 1e3)
est = abs(1 / (2j * math.pi * FC * C1))
v.check("Lab 22-07.e", est * 1e3)
v.check("Lab 22-07.g", (-pk3.fun / est - 1) * 100)

sys.path.insert(0, str(LAB))
import control as ct  # noqa: E402

v.assert_true("lab buck_gvd matches the state-space transfer function",
              abs(ct.buck_gvd(60e3, VG1, L1, C1, R1) / g60 - 1) < 1e-6)
v.assert_true("lab boost_gvd matches the linearized averaged model",
              abs(ct.boost_gvd(100e3, V2, D2, L2, C2, R2) - tf_eval(A2, B2, CV, 100e3)) < 1e-6)
v.assert_true("lab type3_components match the least-squares realization",
              all(abs(a / b - 1) < 1e-6 for a, b in zip(ct.type3_components(10e3, wI, k3, fz3, fp3),
                                                       (c1s, c2s, r2s, r3s, c3s))))
v.assert_true("lab kfactor matches the phase root", abs(ct.kfactor(PM, php)[1] - k3) < 1e-9)
v.assert_true("lab perturbation_ratio matches the waveform simulation",
              abs(ct.perturbation_ratio(m1, m2, m2 / 2) - a4) < 1e-6)

v.finish()
