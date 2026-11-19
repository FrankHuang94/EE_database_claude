#!/usr/bin/env python3
"""Verify every number in chapter 10-09 (real op-amps), its solutions and lab.

Independent routes:
- closed-loop gains and bandwidths from the complex loop equation v_o = A(s)(v_+ - beta v_o) with a single-pole
  A(s), solved at each frequency; -3 dB points and accuracy limits by root finding on |H(f)|, not GBW/gain;
- slew-limited responses by integrating dv/dt = clip((v_target - v)/tau, +-SR) with scipy's ODE solver;
- settling times by simulation and root finding on the simulated waveform;
- DC errors from the data-sheet values (R-182) with the decibel and unit conversions written out.
"""
from __future__ import annotations

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
v = Verifier.from_files("10-09", COURSE / "chapters" / "10-09-real-op-amps-nonidealities.md",
                        COURSE / "solutions" / "10-09-solutions.md",
                        COURSE / "labs" / "10-09-lab" / "README.md")


def H(f, a0_db, gbw, noise_gain):
    """Non-inverting closed loop with beta = 1/noise_gain; returns v_o/v_in (complex)."""
    a0 = 10 ** (a0_db / 20)
    a = a0 / (1 + 1j * f / (gbw / a0))
    beta = 1 / noise_gain
    return a / (1 + a * beta)


def H_inv(f, a0_db, gbw, r1, r2):
    """Inverting amplifier solved from nodal equations at the inverting input."""
    a0 = 10 ** (a0_db / 20)
    a = a0 / (1 + 1j * f / (gbw / a0))
    # node v_-: (v_in - v_-)/r1 + (v_o - v_-)/r2 = 0, v_o = -a v_-
    m = np.array([[-(1 / r1 + 1 / r2), 1 / r2], [a, 1.0]], dtype=complex)
    vm, vo = np.linalg.solve(m, np.array([-1 / r1, 0.0], dtype=complex))
    return vo


def f3db(fun):
    dc = abs(fun(1e-6))
    return brentq(lambda f: abs(fun(f)) / dc - 1 / math.sqrt(2), 1e-3, 1e10)


def slew_sim(vstep, sr, fc, t_end, n=200001):
    tau = 1 / (2 * math.pi * fc)
    t = np.linspace(0, t_end, n)
    sol = solve_ivp(lambda tt, y: [np.clip((vstep - y[0]) / tau, -sr, sr)], (0, t_end), [0.0], t_eval=t,
                    max_step=t_end / 20000, rtol=1e-10, atol=1e-13)
    return sol.t, sol.y[0]


def settle_time(vstep, sr, fc, tol):
    t, y = slew_sim(vstep, sr, fc, 20 * (vstep / sr + 30 / (2 * math.pi * fc)))
    err = np.abs(vstep - y)
    idx = np.where(err > tol)[0][-1]
    # linear interpolation between the last sample outside tolerance and the next
    t0, t1, e0, e1 = t[idx], t[idx + 1], err[idx], err[idx + 1]
    return t0 + (e0 - tol) / (e0 - e1) * (t1 - t0)


# ------------------------------------------------------------------ theory
x1 = brentq(lambda x: 1 / math.sqrt(1 + x * x) - 0.99, 0, 1)
x01 = brentq(lambda x: 1 / math.sqrt(1 + x * x) - 0.999, 0, 1)
v.check("T 10-09.a", x1)
v.check("T 10-09.b", x01)
v.check("T 10-09.c", 6.5e6 / (2 * math.pi * 10e6))
v.check("T 10-09.d", 40)                  # OPA1611 data sheet, R-182
v.check("T 10-09.e", 80)

# ------------------------------------------------------------------ Example 1
v.check("Ex 10-09.1a", 10 ** (106 / 20))
g_min = abs(H(0.0, 106, 1e9, 1000))
g_typ = abs(H(0.0, 130, 1e9, 1000))
v.check("Ex 10-09.1b", g_min)
v.check("Ex 10-09.1c", (1 - g_min / 1000) * 100)
v.check("Ex 10-09.1d", 1000 / 10 ** (106 / 20) * 100)
v.check("Ex 10-09.1e", g_typ)
v.check("Ex 10-09.1f", (1 - g_typ / 1000) * 100)

# ------------------------------------------------------------------ Example 2
v.check("Ex 10-09.2a", f3db(lambda f: H(f, 130, 10e6, 10)) / 1e6)
v.check("Ex 10-09.2b", f3db(lambda f: H_inv(f, 130, 10e6, 1e3, 10e3)) / 1e6)
v.check("Ex 10-09.2c", f3db(lambda f: H(f, 130, 350e3, 100)) / 1e3)
h1k = H(1e3, 130, 350e3, 100) / H(0.0, 130, 350e3, 100)
v.check("Ex 10-09.2d", (abs(h1k) - 1) * 100)
v.check("Ex 10-09.2e", -math.degrees(np.angle(h1k)))

# ------------------------------------------------------------------ Example 3: full-power bandwidth by simulation


def fpbw(sr, vp, fc=1e12):
    """Highest frequency at which a vp sine passes a slew-limited follower without its slope being clipped."""
    def clipped(f):
        tt = np.linspace(0, 1 / f, 4001)
        slope = np.abs(2 * np.pi * f * vp * np.cos(2 * np.pi * f * tt))
        return slope.max() - sr
    return brentq(clipped, 1, 1e10)


v.check("Ex 10-09.3a", fpbw(27e6, 10) / 1e3)
v.check("Ex 10-09.3b", fpbw(27e6, 0.5) / 1e6)
v.check("Ex 10-09.3c", fpbw(6.5e6, 2.5) / 1e3)
v.check("Ex 10-09.3d", fpbw(0.16e6, 2.5) / 1e3)
# largest step whose initial slope stays below SR
v.check("Ex 10-09.3e", brentq(lambda s: s * 2 * math.pi * 10e6 - 6.5e6, 1e-6, 10) * 1e3)

# ------------------------------------------------------------------ Example 4
v.check("Ex 10-09.4a", 2 / 10 ** (110 / 20) * 1e6)
v.check("Ex 10-09.4b", 2 / 10 ** (80 / 20) * 1e6)
v.check("Ex 10-09.4c", 2 / 10 ** (57 / 20) * 1e3)
v.check("Ex 10-09.4d", 0.1 * 5)
v.check("Ex 10-09.4e", 0.1 * 80)

# ------------------------------------------------------------------ Example 5
fs = 2e-3 * 5
v.check("Ex 10-09.5a", fs * 1e3)
os333 = 10e-6 + 0.05e-6 * (125 - 25)
v.check("Ex 10-09.5b", os333 * 1e6)
v.check("Ex 10-09.5c", os333 * 100 * 1e3)
v.check("Ex 10-09.5d", os333 / fs * 100)
v.check("Ex 10-09.5e", 2.0)
v.check("Ex 10-09.5f", 2e-3 * 100 * 1e3)
v.check("Ex 10-09.5g", 2e-3 / fs * 100)

# ------------------------------------------------------------------ Example 6
v.check("Ex 10-09.6a", 15 - 0.6)
v.check("Ex 10-09.6b", 15 - 2)
v.check("Ex 10-09.6c", 0.06)
v.check("Ex 10-09.6d", 3.3 - 0.06)
v.check("Ex 10-09.6e", 3.3 - 1.4)

# ------------------------------------------------------------------ Example 7
v.check("Ex 10-09.7a", x01)
f_needed = 1e3 / x01
v.check("Ex 10-09.7b", f_needed / 1e3)
gbw_needed = brentq(lambda g: f3db(lambda f: H(f, 200, g, 100)) - f_needed, 1e5, 1e9)
v.check("Ex 10-09.7c", gbw_needed / 1e6)
v.check("Ex 10-09.7d", 2 * math.pi * 1e3 * 2 / 1e6)
v.check("Ex 10-09.7e", f3db(lambda f: H(f, 130, 10e6, 100)) / 1e3)
v.check("Ex 10-09.7f", (abs(H(1e3, 130, 10e6, 100) / H(0.0, 130, 10e6, 100)) - 1) * 100)
v.check("Ex 10-09.7g", (abs(H(1e3, 130, 350e3, 100) / H(0.0, 130, 350e3, 100)) - 1) * 100)

# ================================================================== solutions
v.check("10-09.1a", f3db(lambda f: H_inv(f, 200, 5e6, 1e3, 4e3)) / 1e6)
v.check("10-09.1b", f3db(lambda f: H(f, 200, 5e6, 4)) / 1e6)
v.check("10-09.1c", f3db(lambda f: H(f, 200, 5e6, 1)) / 1e6)
v.check("10-09.2a", 10 ** (90 / 20))
v.check("10-09.2b", 1 / 10 ** (90 / 20) * 1e6)
v.check("10-09.2c", 10 ** (-100 / 20) * 1e6)
v.check("10-09.3a", fpbw(1e6, 5) / 1e3)
v.check("10-09.3b", 2 * math.pi * 20e3 * 10 / 1e6)
g4 = abs(H(0.0, 100, 1e6, 50))
v.check("10-09.4a", g4)
v.check("10-09.4b", (1 - g4 / 50) * 100)
v.check("10-09.4c", f3db(lambda f: H(f, 200, 1e6, 50)) / 1e3)
h4 = H(10e3, 200, 1e6, 50) / H(0.0, 200, 1e6, 50)
v.check("10-09.4d", (abs(h4) - 1) * 100)
v.check("10-09.4e", -math.degrees(np.angle(h4)))
tau5 = 1 / (2 * math.pi * 5e6)
v.check("10-09.5a", tau5 * 1e9)
v.check("10-09.5b", 2e6 * tau5 * 1e3)
v.check("10-09.5c", (4 - 2e6 * tau5) / 2e6 * 1e6)
v.check("10-09.5d", tau5 * math.log(2e6 * tau5 / 4e-3) * 1e9)
ts5 = settle_time(4.0, 2e6, 5e6, 4e-3)
v.check("10-09.5e", ts5 * 1e6)
v.check("10-09.5f", settle_time(4e-3 * 0 + 1e-3, 1e12, 5e6, 1e-6) * 1e9)
v.assert_true("simulated slewing-plus-settling agrees with the piecewise formula",
              abs(ts5 - ((4 - 2e6 * tau5) / 2e6 + tau5 * math.log(2e6 * tau5 / 4e-3))) < 2e-10)
v.check("10-09.6a", 250e-9 * 100e3 * 1e3)
v.check("10-09.6b", 500e-6 * 11 * 1e3)
v.check("10-09.6c", (250e-9 * 100e3 + 500e-6 * 11) * 1e3)
v.check("10-09.6d", 175e-9 * 100e3 * 1e3)
v.check("10-09.6e", (175e-9 * 100e3 + 500e-6 * 11) * 1e3)
v.check("10-09.7a", 0.53 * 100)
v.check("10-09.7b", 2.0 + 1.6)
psrr_100k = 100 - 20 * math.log10(100e3 / 100)
v.check("10-09.8a", psrr_100k)
v.check("10-09.8b", 0.1 * 10 ** (-psrr_100k / 20) * 1e3)
v.check("10-09.9a", 2.5 / 1e3 * 1e3)
v.check("10-09.9b", 5e-3 * 100)
v.check("10-09.9c", 2 * math.pi * 10e3 * 10e-9 * 2 * 1e3)
tol10 = 2 * 1e-4
g10 = brentq(lambda g: settle_time(2.0, 4e6, g, tol10) - 1e-6, 1e5, 1e9, xtol=1e-3)
tau10 = 1 / (2 * math.pi * g10)
v.check("10-09.10a", g10 / 1e6)
v.check("10-09.10b", tau10 * 1e9)
v.check("10-09.10c", 4e6 * tau10 * 1e3)
v.check("10-09.10d", (2 - 4e6 * tau10) / 4e6 * 1e6)
v.check("10-09.10e", tau10 * math.log(4e6 * tau10 / tol10) * 1e9)
v.check("10-09.10f", brentq(lambda g: settle_time(2.0, 1e15, g, tol10) - 1e-6, 1e5, 1e9, xtol=1e-3) / 1e6)
v.check("10-09.11a", 0.1 * 50)
v.check("10-09.11b", 0.1 * 50 / 70)
v.assert_true("only the OPA333's guaranteed drift meets 0.0714 uV/C", 0.05 < 0.1 * 50 / 70 < 0.53 < 4.0)
v.check("10-09.12a", 1.8 - 1.4)
v.check("10-09.12b", (1.8 - 1.4) / 1.8 * 100)

# ================================================================== lab
dc = abs(H(0.0, 130, 10e6, 10))
v.check("Lab 10-09.a", brentq(lambda f: abs(H(f, 130, 10e6, 10)) / dc - 0.999, 1, 1e7) / 1e3)
SR, tau, f0, vp = 6.5e6, 1 / (2 * math.pi * 10e6), 800e3, 2.5
T = 1 / f0
tt = np.linspace(0, 20 * T, 40001)
sol = solve_ivp(lambda t, y: [np.clip((vp * math.sin(2 * math.pi * f0 * t) - y[0]) / tau, -SR, SR)], (0, 20 * T), [0.0],
                t_eval=tt, max_step=T / 4000, rtol=1e-9, atol=1e-12)
v.check("Lab 10-09.b", sol.y[0][tt > 15 * T].max())
v.check("Lab 10-09.c", vp * abs(H(f0, 200, 10e6, 1)))


def budget(vos, drift, ib, cmrr_db, psrr):
    terms = [vos, drift * 100, ib * 175, 2.5 * 10 ** (-cmrr_db / 20), 0.1 * psrr]
    return sum(abs(x) for x in terms), math.sqrt(sum(x * x for x in terms))


w1, r1 = budget(10e-6, 0.05e-6, 200e-12, 106, 5e-6)
w2, r2 = budget(1.6e-3, 0.53e-6, 0.5e-12, 80, 80e-6)
v.check("Lab 10-09.d", w1 * 1e6)
v.check("Lab 10-09.e", r1 * 1e6)
v.check("Lab 10-09.f", w2 * 1e3)
v.check("Lab 10-09.g", r2 * 1e3)
v.check("Lab 10-09.h", 10 / 0.538)
v.check("Lab 10-09.i", 0.35 / 0.017)
v.check("Lab 10-09.j", 40 / 3.6)

v.finish()
