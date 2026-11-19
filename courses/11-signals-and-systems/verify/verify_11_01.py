#!/usr/bin/env python3
"""Verify every number in chapter 11-01 (signals: classification and operations), its solutions and lab.

Independent routes:
- fundamental periods by brute-force search: the smallest T on a fine grid (CT) or the smallest integer N (DT) for
  which the signal repeats to rounding error;
- energies and powers by numerical integration (scipy quad) or long direct sums and windowed averages, not by the
  closed forms the text uses;
- time transformations by evaluating the composed functions on a dense grid, reading off supports and values, and
  integrating the result;
- impulse integrals with sympy's DiracDelta and, separately, by replacing the impulse with narrow unit-area pulses
  and extrapolating the width to zero;
- DT frequency equivalences by generating the sample sequences and comparing them.
Data-sheet values (R-184, R-059, R-141) are quoted.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("11-01", COURSE / "chapters" / "11-01-signals-classification-and-operations.md",
                        COURSE / "solutions" / "11-01-solutions.md",
                        COURSE / "labs" / "11-01-lab" / "README.md")


# --------------------------------------------------------------------------- helpers
def ct_period(f, tmax, dt=1e-4, tol=1e-6, probe=None):
    """Smallest T in (0, tmax] with max |f(t+T) - f(t)| < tol over probe points (grid search, then refine)."""
    if probe is None:
        probe = np.linspace(0, 7.3, 400)
    left = False
    for T in np.arange(dt, tmax + dt, dt):
        mis = np.max(np.abs(f(probe + T) - f(probe)))
        if not left:
            left = mis > 0.1  # first move away from T = 0, where the mismatch is trivially small
            continue
        if mis < 1e-2:
            # refine around the candidate with a bracketing minimization of the mismatch
            from scipy.optimize import minimize_scalar
            res = minimize_scalar(lambda s: np.max(np.abs(f(probe + s) - f(probe))), bounds=(T - dt, T + dt),
                                  method="bounded", options={"xatol": 1e-12})
            if res.fun < tol:
                return res.x
    return None


def dt_period(x, nmax=2000):
    n = np.arange(0, 400)
    for N in range(1, nmax + 1):
        if np.max(np.abs(x(n + N) - x(n))) < 1e-9:
            return N
    return None


def energy_ct(f, a=-np.inf, b=np.inf, points=None):
    return quad(lambda t: abs(f(t)) ** 2, a, b, limit=400, points=points)[0]


def power_window(f, T, pts=4_000_001):
    """(1/2T) * integral of f^2 over [-T, T], by the trapezoid rule on a dense grid."""
    tt = np.linspace(-T, T, pts)
    return np.trapezoid(f(tt) ** 2, tt) / (2 * T)


def u(t):
    return np.where(np.asarray(t) > 0, 1.0, 0.0)


def r(t):
    t = np.asarray(t, dtype=float)
    return np.where(t > 0, t, 0.0)


def support(y, t):
    nz = np.nonzero(np.abs(y) > 1e-12)[0]
    return t[nz[0]], t[nz[-1]]


# --------------------------------------------------------------------------- theory and practitioner
v.check("T 11-01.a", math.sqrt(power_window(lambda t: np.cos(2 * np.pi * t), 50.0)))
ads_vref, ads_gain, ads_rms, ads_pp = 2.42, 6, 0.9e-6, 5.6e-6  # R-184, table 3 at 500 SPS
fs_sine_rms = math.sqrt(quad(lambda t: (ads_vref / ads_gain * math.sin(2 * math.pi * t)) ** 2, 0, 1)[0])
v.check("T 11-01.b", fs_sine_rms)
v.check("T 11-01.c", 20 * math.log10(fs_sine_rms / ads_rms))
v.check("T 11-01.d", math.log2(2 * ads_vref / ads_gain / ads_pp))
v.check("T 11-01.e", len(range(-2 ** 23, 2 ** 23)))
v.check("T 11-01.f", 24 * 500 / 1e3)
v.check("T 11-01.g", math.log2(len([-3, -1, 1, 3])))
v.check("T 11-01.h", 42.7 / 0.9)
v.check("T 11-01.i", ads_vref / ads_gain)
v.check("T 11-01.j", 2 * ads_vref / ads_gain)
levels = np.array([-1, -1 / 3, 1 / 3, 1])  # PAM4 levels in units of V_tx (R-184)
v.check("T 11-01.k", 20 * math.log10((levels[-1] - levels[0]) / np.min(np.diff(levels))))

# --------------------------------------------------------------------------- Example 1
v.check("Ex 11-01.1a", ct_period(lambda t: 3 * np.cos(4 * np.pi * t), 2))
v.check("Ex 11-01.1b", ct_period(lambda t: 2 * np.sin(6 * np.pi * t + np.pi / 4), 2))
x1 = lambda t: 3 * np.cos(4 * np.pi * t) + 2 * np.sin(6 * np.pi * t + np.pi / 4)  # noqa: E731
T0 = ct_period(x1, 3)
v.check("Ex 11-01.1c", T0)
v.check("Ex 11-01.1d", 1 / T0)
v.assert_true("x2 = cos 2t + cos pi t has no period up to 60 s", ct_period(lambda t: np.cos(2 * t) + np.cos(np.pi * t),
                                                                            60, dt=1e-3, tol=1e-4) is None)
v.check("Ex 11-01.1e", dt_period(lambda n: np.cos(0.3 * np.pi * n)))
v.assert_true("cos(0.5 n) has no period up to 2000", dt_period(lambda n: np.cos(0.5 * n)) is None)
v.check("Ex 11-01.1f", dt_period(lambda n: np.cos(np.pi * n / 4) + np.sin(np.pi * n / 6)))
v.check("Ex 11-01.1g", power_window(lambda t: np.cos(2 * t) + np.cos(np.pi * t), 2000.0), rtol=2e-3)

# --------------------------------------------------------------------------- Example 2
vt = lambda t: 5 * np.exp(-2 * t)  # noqa: E731
E2 = energy_ct(vt, 0, np.inf)
v.check("Ex 11-01.2a", E2)
v.check("Ex 11-01.2b", E2 / 1000 * 1e3)
frac = energy_ct(vt, 0, 0.5) / E2
v.check("Ex 11-01.2c", 100 * frac)
v.check("Ex 11-01.2f", 100 * (1 - frac))
from scipy.optimize import brentq  # noqa: E402
v.check("Ex 11-01.2d", brentq(lambda t1: energy_ct(vt, 0, t1) / E2 - 0.99, 0.1, 5, xtol=1e-12))
v.check("Ex 11-01.2e", sum(0.8 ** (2 * n) for n in range(2000)))

# --------------------------------------------------------------------------- Example 3
vsum = lambda t: 3 + 4 * np.cos(100 * np.pi * t) + 2 * np.cos(300 * np.pi * t + 1)  # noqa: E731
P3 = quad(lambda t: vsum(t) ** 2, 0, 0.02, limit=400)[0] / 0.02
v.check("Ex 11-01.3a", P3)
v.check("Ex 11-01.3b", math.sqrt(P3))
v.check("Ex 11-01.3c", P3 / 50)
w = lambda t: 4 * np.cos(100 * np.pi * t) + 3 * np.cos(100 * np.pi * t + np.pi / 3)  # noqa: E731
Pw = quad(lambda t: w(t) ** 2, 0, 0.02, limit=400)[0] / 0.02
v.check("Ex 11-01.3d", Pw)
v.check("Ex 11-01.3e", math.sqrt(Pw))
tt = np.linspace(0, 0.02, 200001)
v.check("Ex 11-01.3i", np.max(np.abs(w(tt))))
cre = quad(lambda s: w(s) * math.cos(100 * math.pi * s), 0, 0.02, limit=200)[0] / 0.01
cim = -quad(lambda s: w(s) * math.sin(100 * math.pi * s), 0, 0.02, limit=200)[0] / 0.01
v.check("Ex 11-01.3j", math.degrees(math.atan2(cim, cre)))
v.check("Ex 11-01.3h", 3 * math.sin(math.pi / 3))
v.check("Ex 11-01.3k", 16 / 2 + 9 / 2)
v.check("Ex 11-01.3l", Pw - (16 / 2 + 9 / 2))
v.check("Ex 11-01.3m", quad(lambda t: (7 * np.cos(100 * np.pi * t)) ** 2, 0, 0.02)[0] / 0.02)
v.check("Ex 11-01.3n", quad(lambda t: (1 * np.cos(100 * np.pi * t)) ** 2, 0, 0.02)[0] / 0.02)
nn = np.arange(0, 4000)
v.check("Ex 11-01.3f", np.mean(np.cos(np.pi * nn / 2) ** 2))
v.check("Ex 11-01.3g", np.mean(np.cos(np.pi * nn) ** 2))


# --------------------------------------------------------------------------- Example 4
def x4(t):
    return r(t) - r(t - 1) - u(t - 2)


tg = np.linspace(-1, 5, 600001)
y4 = x4(4 - 2 * tg)
s0, s1 = support(y4, tg)
v.check("Ex 11-01.4a", s0, tol=1e-4)
v.check("Ex 11-01.4b", s1, tol=1e-4)
dy = np.diff(y4) / np.diff(tg)
corner = tg[1:][np.nonzero(np.abs(dy + 2) < 1e-6)[0][0]]  # first point of the slope -2 ramp
v.check("Ex 11-01.4c", corner, tol=1e-4)
v.check("Ex 11-01.4d", float(x4(4 - 2 * 1.25)))
v.check("Ex 11-01.4e", float(x4(4 - 2 * 1.75)))
Ex4 = energy_ct(lambda t: float(x4(t)), -1, 3, points=[0, 1, 2])
Ey4 = energy_ct(lambda t: float(x4(4 - 2 * t)), 0, 3, points=[1, 1.5, 2])
v.check("Ex 11-01.4f", Ex4)
v.check("Ex 11-01.4g", Ey4)
ystep = u(tg - 1) - 2 * r(tg - 1.5) + 2 * r(tg - 2)
mask = (np.abs(tg - 1) > 1e-3) & (np.abs(tg - 2) > 1e-3)
v.assert_true("step-ramp form of y matches x(4 - 2t)", np.max(np.abs(ystep[mask] - y4[mask])) < 1e-9)
wrong = x4(8 - 2 * tg)
v.assert_true("wrong order lands on [3, 4]", np.allclose(support(wrong, tg), (3, 4), atol=1e-4))

# --------------------------------------------------------------------------- Example 5
xc = lambda t: math.exp(-t) if t > 0 else 0.0  # noqa: E731
xe = lambda t: 0.5 * (xc(t) + xc(-t))  # noqa: E731
xo = lambda t: 0.5 * (xc(t) - xc(-t))  # noqa: E731
v.check("Ex 11-01.5a", energy_ct(xc, 0, np.inf))
v.check("Ex 11-01.5b", 2 * energy_ct(xe, 0, np.inf))
v.check("Ex 11-01.5c", 2 * energy_ct(xo, 0, np.inf))
xd = {0: 1.0, 1: 2.0, 2: 3.0}
ns = range(-2, 3)
xe_d = {n: 0.5 * (xd.get(n, 0) + xd.get(-n, 0)) for n in ns}
xo_d = {n: 0.5 * (xd.get(n, 0) - xd.get(-n, 0)) for n in ns}
v.check("Ex 11-01.5d", xe_d[-2])
v.check("Ex 11-01.5e", xo_d[-2])
v.check("Ex 11-01.5f", sum(val ** 2 for val in xd.values()))
v.check("Ex 11-01.5g", sum(val ** 2 for val in xe_d.values()))
v.check("Ex 11-01.5h", sum(val ** 2 for val in xo_d.values()))

# --------------------------------------------------------------------------- Example 6 (sympy DiracDelta)
t = sp.symbols("t", real=True)
v.check("Ex 11-01.6a", float(sp.integrate((t ** 2 + 1) * sp.DiracDelta(t - 2), (t, -sp.oo, sp.oo))))
v.check("Ex 11-01.6b", float(sp.integrate(sp.exp(-t) * sp.DiracDelta(2 * t - 4), (t, -sp.oo, sp.oo))))
v.check("Ex 11-01.6c", float(sp.integrate(sp.cos(sp.pi * t) * sp.DiracDelta(t - 3), (t, -1, 1))))
# derivative of x4: integrate it against a test function and compare with -f(2) + int_0^1 f
wgt = float(x4(2 + 1e-9) - x4(2 - 1e-9))  # the jump of x at t = 2 is the impulse weight in x'
v.check("Ex 11-01.6d", wgt)
C, V = 2e-6, 5.0
# a capacitor charged through a small R: charge, stored and supplied energy, as R -> 0
for R in (1.0, 0.01):
    tau = R * C
    q = quad(lambda s: V / R * math.exp(-s / tau), 0, 50 * tau)[0]
    supplied = quad(lambda s: V * V / R * math.exp(-s / tau), 0, 50 * tau)[0]
v.check("Ex 11-01.6e", q * 1e6)
v.check("Ex 11-01.6f", 0.5 * C * V ** 2 * 1e6)
v.check("Ex 11-01.6g", supplied * 1e6)

# --------------------------------------------------------------------------- Example 7
fs = 10e3
n = np.arange(0, 200)
seq = lambda f: np.cos(2 * np.pi * f / fs * n)  # noqa: E731
v.check("Ex 11-01.7a", 2 * np.pi * 3e3 / fs)
N0 = dt_period(lambda k: np.cos(2 * np.pi * 3e3 / fs * k))
v.check("Ex 11-01.7b", N0)
v.check("Ex 11-01.7c", N0 / fs * 1e3)
v.check("Ex 11-01.7d", N0 / fs * 3e3)
v.check("Ex 11-01.7m", 1 / 3e3 * 1e3)
aliases = [f for f in range(1000, 25000, 1000) if f != 3000 and np.max(np.abs(seq(f) - seq(3000))) < 1e-9]
for key, f in zip("efgh", aliases):
    v.check(f"Ex 11-01.7{key}", f / 1e3)
v.assert_true("exactly four cosine aliases below 25 kHz", len(aliases) == 4)
v.assert_true("7 kHz sine gives the negated 3 kHz sine",
              np.max(np.abs(np.sin(2 * np.pi * 7e3 / fs * n) + np.sin(2 * np.pi * 3e3 / fs * n))) < 1e-9)
v.check("Ex 11-01.7o", fs / 2 / 1e3)
fe = 500
v.check("Ex 11-01.7i", 2 * np.pi * 60 / fe)
N60 = dt_period(lambda k: np.cos(2 * np.pi * 60 / fe * k))
v.check("Ex 11-01.7j", N60)
v.check("Ex 11-01.7n", N60 / fe * 1e3)
ne = np.arange(0, 500)
al60 = [f for f in range(1, 1000) if f != 60 and
        np.max(np.abs(np.cos(2 * np.pi * f / fe * ne) - np.cos(2 * np.pi * 60 / fe * ne))) < 1e-9]
v.check("Ex 11-01.7k", al60[0])
v.check("Ex 11-01.7l", al60[1])
v.check("Ex 11-01.7p", al60[2])
v.assert_true("only 440, 560 and 940 Hz below 1 kHz", len(al60) == 3)

# --------------------------------------------------------------------------- Problems
v.check("11-01.1a", power_window(lambda s: 2 * np.cos(5 * s), 3000.0), rtol=1e-3)
v.check("11-01.1b", energy_ct(lambda s: math.exp(-3 * abs(s)), -np.inf, np.inf, points=None))
Nw = 200000
v.check("11-01.1c", (Nw + 1) / (2 * Nw + 1))
v.check("11-01.1d", sum((-0.5) ** (2 * k) for k in range(500)))
v.check("11-01.1e", power_window(lambda s: (s > 0).astype(float), 1000.0))
v.assert_true("t u(t): windowed power grows with T", power_window(lambda s: s * (s > 0), 100.0)
              > 10 * power_window(lambda s: s * (s > 0), 10.0))

v.check("11-01.2a", ct_period(lambda s: np.cos(10 * np.pi * s) + np.sin(4 * np.pi * s), 3))
v.check("11-01.2b", ct_period(lambda s: np.cos(3 * s) ** 2, 3))
v.check("11-01.2c", ct_period(lambda s: np.real(np.exp(5j * s) + np.exp(7j * s)) + np.imag(np.exp(5j * s) + np.exp(7j * s)),
                              8, dt=1e-3))
v.check("11-01.2d", dt_period(lambda k: np.exp(2j * np.pi * k / 5) + np.exp(3j * np.pi * k / 4)))
v.assert_true("cos(n/6) is not periodic", dt_period(lambda k: np.cos(k / 6)) is None)
v.check("11-01.2e", dt_period(lambda k: np.cos(1.2 * np.pi * k)))


def pulse_sift(f, a, t0, d):
    """int f(t) * (1/d) rect((a t - c)/d) dt, a unit-area pulse in the variable a*t centred where a t0 - c = 0."""
    lo, hi = sorted([t0 - d / (2 * abs(a)), t0 + d / (2 * abs(a))])
    return quad(f, lo, hi)[0] / d


def extrap(f, a, t0):
    d1, d2 = 1e-2, 5e-3
    s1, s2 = pulse_sift(f, a, t0, d1), pulse_sift(f, a, t0, d2)
    return s2 + (s2 - s1) / 3  # Richardson: error is O(d^2)


v.check("11-01.3a", extrap(lambda s: math.exp(-3 * s), 1, 1))
v.check("11-01.3b", extrap(lambda s: math.sin(math.pi * s), 4, 0.5))
v.check("11-01.3c", float(sp.integrate(t ** 3 * sp.DiracDelta(t + 2), (t, 0, 5))))
kk = np.arange(-50, 51)
v.check("11-01.3d", float(np.sum((kk ** 2 + 1) * (kk == 3))))
v.check("11-01.3e", float(np.sum(2.0 ** kk * (kk >= 0) * (kk == -2))))


def x_p4(s):
    s = np.asarray(s, dtype=float)
    return np.where((s >= -1) & (s <= 1), s + 1, 0.0)


tg = np.linspace(-6, 6, 1200001)
Ex_p4 = quad(lambda s: float(x_p4(s)) ** 2, -1, 1)[0]
v.check("11-01.4a", Ex_p4)
for keys, fun, at in (("bcde", lambda s: x_p4(2 * s + 1), -0.25), ("fghi", lambda s: x_p4(1 - s / 2), 3.0),
                      ("jklm", lambda s: x_p4(-s - 1), -0.5)):
    yy = fun(tg)
    a0, a1 = support(yy, tg)
    v.check(f"11-01.4{keys[0]}", a0, tol=1e-4)
    v.check(f"11-01.4{keys[1]}", a1, tol=1e-4)
    v.check(f"11-01.4{keys[2]}", float(fun(at)))
    v.check(f"11-01.4{keys[3]}", quad(lambda s: float(fun(s)) ** 2, a0 - 0.1, a1 + 0.1, points=[a0, a1], limit=200)[0])

tm = np.linspace(-1, 6, 700001)  # milliseconds
xtz = 3 * (r(tm) - r(tm - 1) - r(tm - 4) + r(tm - 5))  # volts, slope 3 V/ms
v.assert_true("trapezoid is 3 V on the flat top and 0 after", abs(xtz[np.searchsorted(tm, 2.5)] - 3) < 1e-9
              and abs(xtz[-1]) < 1e-9)
v.check("11-01.5a", np.max(np.diff(xtz) / np.diff(tm)) * 1e3)
E5 = np.trapezoid(xtz ** 2, tm)
v.check("11-01.5b", E5)
v.check("11-01.5c", E5 * 1e-3 / 50 * 1e3)
win = (tm >= 0) & (tm <= 5)
v.check("11-01.5d", np.trapezoid(xtz[win], tm[win]) / 5)
v.check("11-01.5e", math.sqrt(np.trapezoid(xtz[win] ** 2, tm[win]) / 5))

xp6 = lambda s: float(0 < s < 2)  # noqa: E731
v.check("11-01.6a", quad(lambda s: xp6(s) ** 2, -1, 3, points=[0, 2])[0])
v.check("11-01.6b", quad(lambda s: (0.5 * (xp6(s) + xp6(-s))) ** 2, -3, 3, points=[-2, 0, 2])[0])
v.check("11-01.6c", quad(lambda s: (0.5 * (xp6(s) - xp6(-s))) ** 2, -3, 3, points=[-2, 0, 2])[0])
ts = np.linspace(-5, 5, 1001)
fx = np.cos(ts) + np.sin(ts) + np.sin(ts) * np.cos(ts)
v.assert_true("even part of (b) is cos t", np.allclose(0.5 * (fx + fx[::-1]), np.cos(ts)))
xq = lambda k: 0.5 ** k if k >= 0 else 0.0  # noqa: E731
v.check("11-01.6d", 0.5 * (xq(-2) + xq(2)))
v.check("11-01.6e", 0.5 * (xq(-2) - xq(2)))
v.check("11-01.6f", sum(xq(k) ** 2 for k in range(200)))
v.check("11-01.6g", sum((0.5 * (xq(k) + xq(-k))) ** 2 for k in range(-200, 201)))
v.check("11-01.6h", sum((0.5 * (xq(k) - xq(-k))) ** 2 for k in range(-200, 201)))

xc7 = lambda s: (2 + 3 * np.exp(1j * 100 * np.pi * s) + 3 * np.exp(-1j * 100 * np.pi * s)  # noqa: E731
                 + 1j * np.exp(1j * 300 * np.pi * s) - 1j * np.exp(-1j * 300 * np.pi * s))
v.assert_true("x of Problem 7 is real", np.max(np.abs(np.imag(xc7(np.linspace(0, 0.1, 999))))) < 1e-12)
xr7 = lambda s: np.real(xc7(s))  # noqa: E731
T7 = ct_period(xr7, 0.05, dt=1e-5, probe=np.linspace(0, 0.07, 300))
v.check("11-01.7a", T7 * 1e3)
P7 = quad(lambda s: xr7(s) ** 2, 0, T7, limit=200)[0] / T7
v.check("11-01.7b", P7)
v.check("11-01.7c", math.sqrt(P7))
y7 = lambda s: 5 * np.cos(10 * s) * np.cos(30 * s)  # noqa: E731
T7y = ct_period(y7, 1)
v.check("11-01.7d", T7y)
P7y = quad(lambda s: y7(s) ** 2, 0, T7y, limit=200)[0] / T7y
v.check("11-01.7e", P7y)
v.check("11-01.7f", math.sqrt(P7y))

xd8 = {0: 1, 1: 2, 2: 3, 3: 4}
g8 = lambda k: xd8.get(k, 0)  # noqa: E731
v.check("11-01.8a", sum(val ** 2 for val in xd8.values()))
v.check("11-01.8b", g8(4 - 2))
rev = {k: g8(1 - k) for k in range(-10, 11) if g8(1 - k)}
v.check("11-01.8c", min(rev))
v.check("11-01.8d", max(rev))
v.check("11-01.8e", rev[-2])
dec = [g8(2 * k) for k in range(-10, 11)]
v.check("11-01.8f", g8(2 * 1))
v.check("11-01.8g", sum(d * d for d in dec))
interp = {k: (g8(k // 2) if k % 2 == 0 else 0) for k in range(-10, 21)}
v.check("11-01.8h", interp[6])
v.check("11-01.8i", sum(val * val for val in interp.values()))
v.check("11-01.8j", sum(g8(2 * k + 1) ** 2 for k in range(-10, 11)))

tt9 = np.linspace(0, 10, 2000001)
env = np.abs(2 * np.exp((-1 + 2j * np.pi) * tt9))
t10 = tt9[np.argmax(env <= 0.2)]
v.check("11-01.9a", t10)
v.check("11-01.9b", t10 * 1.0)
v.check("11-01.9c", dt_period(lambda k: np.exp(1j * np.pi * k / 4)))
v.check("11-01.9d", brentq(lambda s: 0.9 ** s - 0.1, 1, 100, xtol=1e-12))
v.check("11-01.9e", next(k for k in range(1000) if abs((0.9 * np.exp(1j * np.pi / 4)) ** k) < 0.1))


def principal(w):
    """The frequency in [0, pi] giving the same real cosine sequence, found by search on a fine grid."""
    k = np.arange(0, 64)
    grid = np.linspace(0, np.pi, 3141593)
    target = np.cos(w * k)
    best = grid[np.argmin(np.abs(np.cos(np.outer(grid[::1000], k[:8])) - target[:8]).max(axis=1))] * 0 \
        + grid[::1000][np.argmin(np.abs(np.cos(np.outer(grid[::1000], k[:8])) - target[:8]).max(axis=1))]
    lo, hi = max(best - 2e-3, 0), min(best + 2e-3, np.pi)
    from scipy.optimize import minimize_scalar
    res = minimize_scalar(lambda s: np.max(np.abs(np.cos(s * k) - target)), bounds=(lo, hi), method="bounded",
                          options={"xatol": 1e-12})
    return res.x


v.check("11-01.10a", principal(3.5 * np.pi))
v.check("11-01.10b", principal(7.0))
v.check("11-01.10c", principal(2 * np.pi * 26e3 / 10e3) / (2 * np.pi) * 10e3 / 1e3)
v.check("11-01.10d", principal(2 * np.pi * 1e3 / 10e3))
v.assert_true("9 and 11 kHz give the same samples as 1 kHz",
              all(abs(principal(2 * np.pi * f / 10e3) - 0.2 * np.pi) < 1e-6 for f in (9e3, 11e3)))

idx = np.arange(1_000_000)  # one second in 1 us steps
iled = np.where(idx % 10_000 < 100, 50e-3, 0.0)  # 100 us on in every 10 ms
D = np.mean(iled > 0)
v.check("11-01.11a", 100 * D)
Iavg, Irms = np.mean(iled), math.sqrt(np.mean(iled ** 2))
v.check("11-01.11b", Iavg * 1e3)
v.check("11-01.11c", Irms * 1e3)
v.check("11-01.11d", np.mean(3.0 * iled) * 1e3)
v.check("11-01.11e", np.mean(iled ** 2 * 2.0) * 1e6)
v.check("11-01.11f", 200e-3 / Iavg)
v.check("11-01.11g", 3.0 * np.max(iled) * 1e3)
v.check("11-01.11h", np.max(iled) / Irms)
v.check("11-01.11i", np.max(iled) / Iavg)


def x12(s):
    return 2 * u(s + 1) - 3 * u(s - 1) + r(s - 2)


for key, at in zip("abcd", (0, 1.5, 3, 5)):
    v.check(f"11-01.12{key}", float(x12(at)))
v.check("11-01.12e", quad(lambda s: float(x12(s)) * math.exp(-s), -1, 60, points=[1, 2], limit=200)[0])
v.check("11-01.12e", 2 * math.e - 3 / math.e + quad(lambda s: math.exp(-s), 2, np.inf)[0])

v.check("11-01.13a", float(sp.integrate(sp.exp(t) * sp.DiracDelta(t ** 2 - 4), (t, -sp.oo, sp.oo))))
# (b) by a narrow pulse in g = t^2 - pi^2 around the root t = pi
dg = 1e-4
lo, hi = math.sqrt(math.pi ** 2 - dg / 2), math.sqrt(math.pi ** 2 + dg / 2)
v.check("11-01.13b", quad(lambda s: math.cos(s), lo, hi)[0] / dg)

fe = 500
for key, f in (("a", 50), ("b", 60), ("e", 150), ("f", 180)):
    v.check(f"11-01.14{key}", dt_period(lambda k, f=f: np.cos(2 * np.pi * f / fe * k)))


def block_kills(f, N):
    k = np.arange(N)
    return abs(np.sum(np.cos(2 * np.pi * f / fe * k))) < 1e-9 and abs(np.sum(np.sin(2 * np.pi * f / fe * k))) < 1e-9


Nb = next(N for N in range(1, 1000) if block_kills(50, N) and block_kills(60, N))
v.check("11-01.14c", Nb)
v.check("11-01.14d", Nb / fe * 1e3)
v.assert_true("the 50-sample block removes 150 and 180 Hz", block_kills(150, Nb) and block_kills(180, Nb))
v.check("11-01.14g", next(f for f in range(1, 250) if block_kills(f, Nb)))

# --------------------------------------------------------------------------- Lab
v.check("Lab 11-01.a", quad(lambda s: s * s + 1, 1.95, 2.05)[0] / 0.1)
e1 = quad(lambda s: s * s + 1, 1.95, 2.05)[0] / 0.1 - 5
e2 = quad(lambda s: s * s + 1, 1.975, 2.025)[0] / 0.05 - 5
v.check("Lab 11-01.b", e1 / e2)
v.check("Lab 11-01.c", power_window(lambda s: np.cos(2 * np.pi * s), 10.125))
v.check("Lab 11-01.d", Ey4 / Ex4)
Tg = np.arange(1.0, 30.0, 1e-3)
pr = np.linspace(0, 2 * np.pi * 7, 300)
mis = np.array([np.max(np.abs(np.cos(2 * (pr + T)) + np.cos(np.pi * (pr + T)) - np.cos(2 * pr) - np.cos(np.pi * pr)))
                for T in Tg])
Tnear = Tg[np.argmin(mis)]
v.check("Lab 11-01.e", Tnear, tol=0.5)
v.check("Lab 11-01.f", 2 * round(Tnear) - 2 * np.pi * round(2 * round(Tnear) / (2 * np.pi)))
v.check("Lab 11-01.g", power_window(lambda s: np.cos(2 * np.pi * s), 10.125) - 0.5)

sys.exit(v.finish())
