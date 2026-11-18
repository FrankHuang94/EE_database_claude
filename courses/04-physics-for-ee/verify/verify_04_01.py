#!/usr/bin/env python3
"""Verify every number published in chapter 04-01, its solutions and its lab handout.

Energies and powers are recomputed from first principles; oscillator results by integrating the
equation of motion or sweeping its transfer function numerically; noise results from the
fluctuation-dissipation integral evaluated by quadrature.
"""
from __future__ import annotations

import math
import sys
from math import exp, log, pi, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C = HERE.parent
v = Verifier.from_files("04-01", C / "chapters" / "04-01-mechanics-essentials.md",
                        C / "solutions" / "04-01-solutions.md", C / "labs" / "04-01-lab" / "README.md")
G = 9.80665
KB = 1.380649e-23
QE = 1.602176634e-19
HP = 550 * 0.3048 * 0.45359237 * G          # 550 ft*lbf/s in watts
T300 = 300.0


def osc_params(m, k, b):
    w0 = sqrt(k / m)
    return w0, b / (2 * sqrt(k * m)), m * w0 / b, b / (2 * m)


def half_power(m, k, b):
    # velocity response |X'/F| = w/|k - m w^2 + j b w|, found by root-finding, not by formula
    vel = lambda w: w / math.hypot(k - m * w * w, b * w)  # noqa: E731
    w0 = sqrt(k / m)
    peak = vel(w0)
    lo = brentq(lambda w: vel(w) - peak / sqrt(2), 1e-6 * w0, w0)
    hi = brentq(lambda w: vel(w) - peak / sqrt(2), w0, 100 * w0)
    return lo / (2 * pi), hi / (2 * pi)


# ---------------------------------------------------------------- theory keys
v.check("T 04-01.a", 1.0 * QE)
v.check("T 04-01.b", 3600 * 1000 / 1e6)
v.check("T 04-01.c", G)
v.check("T 04-01.d", quad(lambda t: 1.0, 0, 1)[0] / quad(lambda t: math.sin(pi * t), 0, 1)[0])   # peak/avg of half-sine
v.check("T 04-01.e", HP)
v.check("T 04-01.f", G / (2 * pi * 4000) ** 2 * 1e9)
# work-energy theorem and spring energy by integration
v.assert_true("spring energy = 1/2 k x^2", abs(quad(lambda x: 200 * x, 0, 0.05)[0] - 0.25) < 1e-15)
# SHO energy is constant along the exact solution
tt = np.linspace(0, 1, 7)
w0t = sqrt(1000 / 0.01)
Eosc = 0.5 * 0.01 * (0.01 * w0t * np.sin(w0t * tt)) ** 2 + 0.5 * 1000 * (0.01 * np.cos(w0t * tt)) ** 2
v.assert_true("SHO energy constant", np.allclose(Eosc, 0.05, rtol=1e-12))

# ---------------------------------------------------------------- Example 04-01.1
Wh = 4.5 * 3.87
v.check("Ex 04-01.1a", Wh)
v.check("Ex 04-01.1b", Wh * 3600)
v.check("Ex 04-01.1c", Wh / 1000)
v.check("Ex 04-01.1d", Wh * 3600 / (0.2 * G))
v.check("Ex 04-01.1e", 4.5 * 3600)
v.check("Ex 04-01.1f", 4.5 * 3600 / QE)
v.check("Ex 04-01.1g", 3.87)
v.assert_true("electrons x eV = joules", abs(4.5 * 3600 / QE * 3.87 * QE - Wh * 3600) < 1e-6)

# ---------------------------------------------------------------- Example 04-01.2
v.check("Ex 04-01.2a", sqrt(169e9 / 2329))
v.check("Ex 04-01.2b", 10)
v.check("Ex 04-01.2c", 2 ** 15)

# ---------------------------------------------------------------- Example 04-01.3 (half-sine pulse integrated numerically)
v3 = sqrt(2 * G * 1.5)
dt3 = 0.2e-3
v.check("Ex 04-01.3a", v3)
v.check("Ex 04-01.3b", 0.5 * 0.2 * v3**2)
v.assert_true("KE equals mgh", abs(0.5 * 0.2 * v3**2 - 0.2 * G * 1.5) < 1e-12)
apk3 = brentq(lambda a: quad(lambda t: a * math.sin(pi * t / dt3), 0, dt3)[0] - v3, 1, 1e7)
v.check("Ex 04-01.3c", v3 / dt3)
v.check("Ex 04-01.3d", v3 / dt3 / G)
v.check("Ex 04-01.3e", apk3)
v.check("Ex 04-01.3f", apk3 / G)
v.check("Ex 04-01.3g", 0.2 * v3)
v.check("Ex 04-01.3h", 0.2 * v3 / dt3)
v.check("Ex 04-01.3i", 0.2 * apk3)

# ---------------------------------------------------------------- Example 04-01.4
w4 = 4500 * 2 * pi / 60
P4 = 310 * w4
v.check("Ex 04-01.4a", w4)
v.check("Ex 04-01.4b", P4 / 1e3)
v.check("Ex 04-01.4c", P4 / HP)
v.check("Ex 04-01.4d", P4 / 0.94 / 400)

# ---------------------------------------------------------------- Example 04-01.5 (ring-down measured on a simulated waveform)
m5, k5, b5 = 0.01, 1000.0, 0.4
w05, z5, Q5, a5 = osc_params(m5, k5, b5)
v.check("Ex 04-01.5a", w05)
v.check("Ex 04-01.5b", w05 / (2 * pi))
v.check("Ex 04-01.5c", z5)
v.check("Ex 04-01.5d", Q5)
sol = solve_ivp(lambda t, y: [y[1], (-k5 * y[0] - b5 * y[1]) / m5], (0, 0.3), [1.0, 0.0], rtol=1e-11, atol=1e-14, dense_output=True)
ts = np.linspace(0, 0.3, 300001)
xs = sol.sol(ts)[0]
pk = np.nonzero((xs[1:-1] > xs[:-2]) & (xs[1:-1] > xs[2:]))[0] + 1
alpha_meas = np.polyfit(ts[pk], np.log(xs[pk]), 1)[0] * -1
v.check("Ex 04-01.5e", alpha_meas)
v.check("Ex 04-01.5f", 1 / alpha_meas * 1e3)
v.check("Ex 04-01.5g", (1 / alpha_meas) * (w05 / (2 * pi)))
f1, f2 = half_power(m5, k5, b5)
v.check("Ex 04-01.5h", f1)
v.check("Ex 04-01.5i", f2)
v.check("Ex 04-01.5j", f2 - f1)
# capacitor gain at f0: |k_s X / F| at w0
v.assert_true("spring-force gain at f0 equals Q", abs(k5 / math.hypot(k5 - m5 * w05**2, b5 * w05) - Q5) < 1e-9)

# ---------------------------------------------------------------- Example 04-01.6
m6, f06, Q6 = 5e-9, 4000.0, 1 / sqrt(2)
w06 = 2 * pi * f06
k6, b6 = m6 * w06**2, m6 * w06 / Q6
H = lambda f: 1 / math.hypot(w06**2 - (2 * pi * f) ** 2, 2 * pi * f * w06 / Q6)  # noqa: E731
v.check("Ex 04-01.6a", k6)
v.check("Ex 04-01.6b", b6)
v.check("Ex 04-01.6c", G * H(0) * 1e9)
v.check("Ex 04-01.6d", G * H(0) * 1e12 / 1000)
bw6 = brentq(lambda f: H(f) - H(0) / sqrt(2), 1, 1e5)
v.check("Ex 04-01.6e", bw6 / 1e3)
v.check("Ex 04-01.6f", H(1000) / H(0))
v.check("Ex 04-01.6g", brentq(lambda f0: G / (2 * pi * f0) ** 2 - 2 * G * H(0), 100, 1e4) / 1e3)

# ---------------------------------------------------------------- Example 04-01.7
Fn = sqrt(4 * KB * T300 * b6)
an = Fn / m6
v.check("Ex 04-01.7a", Fn)
v.check("Ex 04-01.7b", an)
v.check("Ex 04-01.7c", an / G * 1e6)
v.check("Ex 04-01.7d", an / G * 1e6 * sqrt(100))
# equipartition from the fluctuation-dissipation integral (numerical quadrature of 4kTb |H|^2)
def fd_integral(fun, x_res):
    # integrate over [0, inf) with the resonance as a break point in the finite part
    # rescale to u = x/x_res so the integrand is O(1)-shaped, and use relative tolerance only
    g_ = lambda u: fun(u * x_res) * x_res  # noqa: E731
    scale = g_(1.0)
    h_ = lambda u: g_(u) / scale  # noqa: E731
    lo = quad(h_, 0, 20, points=[1.0], limit=500, epsabs=0, epsrel=1e-11)[0]
    hi = quad(h_, 20, np.inf, limit=500, epsabs=0, epsrel=1e-11)[0]
    return (lo + hi) * scale


x2 = fd_integral(lambda f: 4 * KB * T300 * b6 / ((k6 - m6 * (2 * pi * f) ** 2) ** 2 + (b6 * 2 * pi * f) ** 2), f06)
v.assert_true("integral of 4kTb|H|^2 equals kT/k_s", abs(x2 / (KB * T300 / k6) - 1) < 1e-6)
v.check("Ex 04-01.7e", sqrt(x2) * 1e12)
v.check("Ex 04-01.7f", brentq(lambda mm: sqrt(4 * KB * T300 * w06 / (mm * Q6)) / G * 1e6 - 10, 1e-10, 1e-6) * 1e9)

# ================================================================ solutions
v.check("04-01.2a", 3.6e6 / QE)
v.check("04-01.2b", 75 * 3600 / 1e3)
v.check("04-01.2c", 2.5 * G)
v.check("04-01.2d", 1.12 * QE)
# pendulum: small-angle period from integrating the exact nonlinear equation at a tiny amplitude
th = solve_ivp(lambda t, y: [y[1], -G / 1.0 * math.sin(y[0])], (0, 4), [1e-4, 0.0], rtol=1e-12, atol=1e-16, dense_output=True)
crossings = [brentq(lambda t: th.sol(t)[0], a, a + 0.25) for a in (0.4, 1.4)]
v.check("04-01.3a", 2 * (crossings[1] - crossings[0]))
v.check("04-01.4a", G + 2)
v.check("04-01.4b", (G + 2) / G)
v.check("04-01.4c", G - 1.5)
v.check("04-01.4d", (G - 1.5) / G)
v.check("04-01.4e", 0.0)
v.check("04-01.5a", 0.5 * 200 * 0.05**2)
v.check("04-01.5b", sqrt(2 * 0.25 / 0.02))
v.check("04-01.5c", sqrt(2 * 0.9 * 0.25 / 0.02))
v.check("04-01.6a", 1000 * G * 2 / 1e3)
v.check("04-01.6b", (1000 - 800) * G * 2 / 1e3)
v.check("04-01.6c", (1000 - 800) * G * 2 / 0.85 / 1e3)
vf = 2 * 3 / 3
v.check("04-01.7a", vf)
v.check("04-01.7b", 0.5 * 2 * 3**2)
v.check("04-01.7c", 0.5 * 3 * vf**2)
v.check("04-01.7d", 0.5 * 2 * 9 - 0.5 * 3 * vf**2)
v.check("04-01.7e", (0.5 * 2 * 9 - 0.5 * 3 * vf**2) / (0.5 * 2 * 9) * 100)
Idisk = quad(lambda r: r * r * 100 / (pi * 0.3**2) * 2 * pi * r, 0, 0.3)[0]   # integral of r^2 dm
w8 = 20000 * 2 * pi / 60
E8 = 0.5 * Idisk * w8**2
v.check("04-01.8a", Idisk)
v.check("04-01.8b", w8)
v.check("04-01.8c", E8 / 1e6)
v.check("04-01.8d", E8 / 3.6e6)
v.check("04-01.8e", E8 / 50e3)
v.check("04-01.8f", (1 - 0.25) * 100)
w9 = sqrt(200 / 0.5)
v.check("04-01.9a", w9)
v.check("04-01.9b", w9 / (2 * pi))
v.check("04-01.9c", 2 * pi / w9)
v.check("04-01.9d", 0.03 * w9)
v.check("04-01.9e", 0.03 * w9**2)
v.check("04-01.9f", 0.5 * 200 * 0.03**2)
a10 = log(2) / (500 / 1e5)
Q10 = 2 * pi * 1e5 / (2 * a10)
v.check("04-01.10a", a10)
v.check("04-01.10b", Q10)
v.check("04-01.10c", 2 * pi / Q10 * 100)
v.check("04-01.10d", 1e5 / Q10)
v.check("04-01.11a", 1 / (1 / 100 + 1 / 300))
v.check("04-01.11b", 100 + 300)
v.check("04-01.11c", 1 / 100 + 1 / 300)
for key, f0 in (("a", 1e3), ("b", 4e3), ("c", 16e3)):
    v.check(f"04-01.12{key}", G / (2 * pi * f0) ** 2 * 1e9)
v.check("04-01.12d", G / (2 * pi * 16e3) ** 2 * 1e12 / 1000)
an13 = 20e-6 * G
w013 = 2 * pi * 2000
m13 = brentq(lambda mm: sqrt(4 * KB * T300 * w013 / (mm * 2.0)) - an13, 1e-12, 1e-6)
v.check("04-01.13a", an13)
v.check("04-01.13b", m13 * 1e9)
v.check("04-01.13c", m13 * w013**2)
v.check("04-01.13d", G / w013**2 * 1e9)
v.check("04-01.13e", sqrt(1000 / 2))
# the integral identity used in Problem 14, checked by quadrature for several parameter sets
for (mm, kk, bb) in ((1.0, 4.0, 0.3), (2e-9, 0.5, 1e-5), (0.01, 1000, 0.4)):
    w_res = sqrt(kk / mm)
    I = fd_integral(lambda w: 1 / ((kk - mm * w * w) ** 2 + (bb * w) ** 2), w_res)
    v.assert_true("integral pi/(2kb)", abs(I / (pi / (2 * kk * bb)) - 1) < 1e-6)
v.check("04-01.14a", sqrt(KB * T300 / 1.0) * 1e12)
v.check("04-01.14b", sqrt(KB * T300 / 1000.0) * 1e12)
v15 = sqrt(2 * G * 1.2)
d15 = brentq(lambda d: (pi / 2) * v15 / d - 1500 * G, 1e-6, 1)
v.check("04-01.15a", v15)
v.check("04-01.15b", d15 * 1e3)
# stopping distance by integrating the half-sine deceleration twice
apk15 = 1500 * G
vel15 = lambda t: v15 - quad(lambda s: apk15 * math.sin(pi * s / d15), 0, t)[0]  # noqa: E731
v.check("04-01.15c", quad(vel15, 0, d15)[0] * 1e3)
beta = -0.035
v.check("04-01.16a", beta * (-10 - 25) ** 2)
v.check("04-01.16b", beta * (60 - 25) ** 2)
v.check("04-01.16c", -beta * 35**2 * 1e-6 * 86400)
v.check("04-01.16d", -beta * 35**2 * 1e-6 * 365.25 * 86400 / 60)
v.check("04-01.16e", beta * (32 - 25) ** 2)
v.check("04-01.16f", -beta * 7**2 * 1e-6 * 30 * 86400)
# practitioner figures: quartz motional branch from C1 = 3.7 fF, Rs = 50 kOhm (Micro Crystal CM7V-T1A)
wq = 2 * pi * 32768
v.check("T 04-01.g", 160 / (an / G * 1e6))
v.check("T 04-01.h", -beta * 60**2)
v.check("T 04-01.i", 1 / (wq**2 * 3.7e-15))
v.check("T 04-01.j", 1 / (wq * 50e3 * 3.7e-15))
v.check("T 04-01.k", 160 * sqrt(80) / 1000)

# ================================================================ lab handout
v.check("Lab 04-01.a", (1 + (2 * pi / 200) ** 2) ** 20000)
wd5 = sqrt(w05**2 - a5**2)
v.check("Lab 04-01.b", 1 - exp(-2 * a5 * 2 * pi / wd5))
v.check("Lab 04-01.c", 2 * pi / Q5)
delta = a5 * 2 * pi / wd5
v.check("Lab 04-01.d", delta)
v.check("Lab 04-01.e", pi / delta)
v.assert_true("exact Q from decrement", abs(sqrt(4 * pi**2 + delta**2) / (2 * delta) - Q5) < 1e-9)


def bw_ratio(Q):
    Hq = lambda r: 1 / math.hypot(1 - r * r, r / Q)  # noqa: E731
    return brentq(lambda r: Hq(r) - 1 / sqrt(2), 1e-3, 10)


v.check("Lab 04-01.f", bw_ratio(0.5))
v.check("Lab 04-01.g", bw_ratio(2.0))
pk2 = -minimize_scalar(lambda r: -1 / math.hypot(1 - r * r, r / 2.0), bounds=(0.1, 2), method="bounded", options={"xatol": 1e-10}).fun
v.check("Lab 04-01.h", pk2)
apk6 = apk3
v.check("Lab 04-01.i", apk6 / w06**2 * 1e6)
a_in = lambda t: apk6 * math.sin(pi * t / dt3) if t < dt3 else 0.0  # noqa: E731
sh = solve_ivp(lambda t, y: [y[1], -a_in(t) - b6 / m6 * y[1] - k6 / m6 * y[0]], (0, 1.5e-3), [0.0, 0.0],
               max_step=5e-8, rtol=1e-10, atol=1e-18)
v.check("Lab 04-01.j", np.max(np.abs(sh.y[0])) * 1e6)
v.check("Lab 04-01.k", sqrt(KB * T300 / k6) * 1e12)
v.check("Lab 04-01.l", brentq(lambda Q: ((2 * pi / Q) - (1 - exp(-2 * pi / Q))) / (1 - exp(-2 * pi / Q)) - 0.1, 5, 200))

sys.exit(v.finish())
