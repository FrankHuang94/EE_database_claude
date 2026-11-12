#!/usr/bin/env python3
"""Verify every published number in chapter 01-07, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.constants import elementary_charge, epsilon_0
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "01-07",
    COURSE / "chapters" / "01-07-applications-of-integration.md",
    COURSE / "solutions" / "01-07-solutions.md",
    COURSE / "labs" / "01-07-lab" / "README.md",
)
x, t = sp.symbols("x t", real=True)


def avg(f, T=1.0, pts=None):
    return quad(f, 0, T, points=pts, limit=200)[0] / T


def rms(f, T=1.0, pts=None):
    return math.sqrt(quad(lambda s: f(s) ** 2, 0, T, points=pts, limit=200)[0] / T)


sine = lambda s: math.sin(2 * math.pi * s)  # noqa: E731
square = lambda s: 1.0 if (s % 1) < 0.5 else -1.0  # noqa: E731
tri = lambda s: float(np.interp(s % 1, [0, 0.25, 0.75, 1], [0, 1, -1, 0]))  # noqa: E731
FF = math.pi / (2 * math.sqrt(2))

# ---------------------------------------------------------------- theory identities
phi = sp.symbols("phi", real=True)
w = sp.symbols("omega", positive=True)
Vm, Im = sp.symbols("V_m I_m", positive=True)
P_sym = sp.integrate(Vm * sp.cos(w * t) * Im * sp.cos(w * t - phi), (t, 0, 2 * sp.pi / w)) / (2 * sp.pi / w)
v.assert_true("P = (Vm Im / 2) cos(phi)", sp.simplify(P_sym - Vm * Im / 2 * sp.cos(phi)) == 0)
L_, I_ = sp.symbols("L I", positive=True)
v.assert_true("w_L = 1/2 L I^2", sp.integrate(L_ * x, (x, 0, I_)) == L_ * I_**2 / 2)
D = sp.symbols("Delta", positive=True)
v.assert_true("uniform variance = Delta^2/12", sp.integrate(x**2 / D, (x, -D / 2, D / 2)) == D**2 / 12)
v.assert_true("6.02N + 1.76: 20 log10(2) = 6.02, 20 log10 sqrt(1.5) = 1.76",
              round(20 * math.log10(2), 2) == 6.02 and round(20 * math.log10(math.sqrt(1.5)), 2) == 1.76)
v.assert_true("Gaussian coverage 68.27 / 95.45 / 99.73",
              [round(100 * (norm.cdf(k) - norm.cdf(-k)), 2) for k in (1, 2, 3)] == [68.27, 95.45, 99.73])
v.assert_true("1 eV = 1.602e-19 J", round(elementary_charge * 1e19, 3) == 1.602)
v.assert_true("crest factors sqrt2, 1, sqrt3", math.isclose(1 / rms(sine), math.sqrt(2), rel_tol=1e-9)
              and math.isclose(1 / rms(tri, pts=[0.25, 0.75]), math.sqrt(3), rel_tol=1e-9))
v.assert_true("MTBF 1e6 h ≈ 114 years", round(1e6 / 8766) == 114)
v.assert_true("10,000 units at 1e-6/h: 10 failures per 1000 h, one per ~4 days",
              math.isclose(1e4 * 1e-6 * 1000, 10) and round(100 / 24) == 4)
v.assert_true("Q5: P(X<0.5) for f = 2x is 0.25", sp.integrate(2 * x, (x, 0, sp.Rational(1, 2))) == sp.Rational(1, 4))
v.assert_true("Q6: survival past the mean = 1/e", math.isclose(math.exp(-1), 0.3679, abs_tol=5e-5))

# ---------------------------------------------------------------- examples
v.check("Ex 01-07.1a", rms(square, pts=[0.5]))
v.check("Ex 01-07.1b", rms(sine))
v.check("Ex 01-07.1c", rms(tri, pts=[0.25, 0.75]))
pwm = lambda s: 12.0 if (s % 1) < 0.25 else 0.0  # noqa: E731
v.check("Ex 01-07.1d", avg(pwm, pts=[0.25]))
v.check("Ex 01-07.1e", rms(pwm, pts=[0.25]))

rip = lambda s: 5 + 0.2 * sine(s)  # noqa: E731
v.check("Ex 01-07.2a", rms(rip))
v.check("Ex 01-07.2b", rms(rip) ** 2 / 10)
v.assert_true("ripple adds 0.08 % heating", round(100 * (rms(rip) ** 2 / 25 - 1), 2) == 0.08)
meter = lambda f, pts=None: FF * avg(lambda s: abs(f(s)), pts=pts)  # noqa: E731
v.check("Ex 01-07.2c", meter(square, [0.5]))
v.check("Ex 01-07.2d", 100 * (meter(square, [0.5]) / rms(square, pts=[0.5]) - 1))
v.check("Ex 01-07.2e", meter(tri, [0.25, 0.75]) * 1.0)
v.check("Ex 01-07.2f", 100 * (meter(tri, [0.25, 0.75]) / rms(tri, pts=[0.25, 0.75]) - 1))

W = 2 * math.pi
pav = avg(lambda s: 170 * math.cos(W * s) * 10 * math.cos(W * s - math.pi / 6))
v.check("Ex 01-07.3a", pav)
S3 = rms(lambda s: 170 * math.cos(W * s)) * rms(lambda s: 10 * math.cos(W * s))
v.check("Ex 01-07.3b", S3)
v.check("Ex 01-07.3c", pav / S3)

v.check("Ex 01-07.4a", 0.5 * 10 * (2.7**2 - 1.35**2))
v.check("Ex 01-07.4b", 0.5 * 10 * 2.7**2)
v.check("Ex 01-07.4c", 100 * (1 - (1.35 / 2.7) ** 2))
v.check("Ex 01-07.4d", 0.300 * 3.85)
v.check("Ex 01-07.4e", 0.300 * 3.85 * 3600)

N = 12
snr = 20 * math.log10(2**N * math.sqrt(1.5))
v.check("Ex 01-07.5a", snr)
v.check("Ex 01-07.5b", (68 - 1.76) / 6.02)
v.assert_true("6.02N + 1.76 vs exact at N = 12 within 0.01 dB", abs(6.02 * 12 + 1.76 - snr) < 0.01)

# ---------------------------------------------------------------- problems
fw = lambda s: abs(10 * sine(s))  # noqa: E731
hw = lambda s: max(10 * sine(s), 0.0)  # noqa: E731
saw = lambda s: 4 * (s % 1)  # noqa: E731
v.check("01-07.1a", avg(fw, pts=[0.5]))
v.check("01-07.1b", rms(fw, pts=[0.5]))
v.check("01-07.1c", avg(hw, pts=[0.5]))
v.check("01-07.1d", rms(hw, pts=[0.5]))
v.check("01-07.1e", avg(saw))
v.check("01-07.1f", rms(saw))
v.check("01-07.1g", 1 / rms(sine))
v.check("01-07.1h", 1 / rms(tri, pts=[0.25, 0.75]))

p5 = lambda s: 5.0 if (s % 1) < 0.2 else 0.0  # noqa: E731
v.check("01-07.2a", avg(p5, pts=[0.2]))
v.check("01-07.2b", rms(p5, pts=[0.2]))
v.check("01-07.2c", rms(p5, pts=[0.2]) ** 2 / 10)
v.check("01-07.2d", avg(p5, pts=[0.2]) ** 2 / 10)

v.check("01-07.3a", 0.5 * 470e-6 * 400**2)
v.check("01-07.3b", 0.5 * 10e-6 * 20**2 * 1e3)

v.check("01-07.4a", math.sqrt(quad(lambda e: e * e / 1.0, -0.5, 0.5)[0]))
v.check("01-07.4b", 1 - quad(lambda tt: 1e-6 * math.exp(-1e-6 * tt), 0, 8760)[0])

i5 = lambda s: 10 * sine(s) + 3 * math.sin(3 * W * s) + math.sin(5 * W * s)  # noqa: E731
v.check("01-07.5a", rms(i5))
v.check("01-07.5b", 100 * math.sqrt(3**2 + 1**2) / 10)
v.check("01-07.5c", rms(i5) ** 2 * 0.1)
v.check("01-07.5d", rms(lambda s: 10 * sine(s)) ** 2 * 0.1)
v.assert_true("harmonic current delivers no power from a sinusoidal source",
              abs(avg(lambda s: math.sin(W * s) * math.sin(3 * W * s))) < 1e-12)

p6 = avg(lambda s: 325 * math.cos(W * s) * 8 * math.cos(W * s - math.pi / 4))
S6 = (325 / math.sqrt(2)) * (8 / math.sqrt(2))
v.check("01-07.6a", p6)
v.check("01-07.6b", S6)
v.check("01-07.6c", p6 / S6)
v.check("01-07.6d", S6 * math.sin(math.pi / 4))

E7 = 0.5 * 1 * (5**2 - 2.5**2)
v.check("01-07.7a", E7)
v.check("01-07.7b", E7 / 0.5)
v.assert_true("P7 v(t) = sqrt(25 - t) reaches 2.5 V at 18.75 s", math.isclose(math.sqrt(25 - 18.75), 2.5))

v.check("01-07.8a", 1e-9 * 5 * 1e9)
v.check("01-07.8b", 1 / elementary_charge)
Q, A = 10e-9, 1e-4
F = Q**2 / (2 * epsilon_0 * A)
v.check("01-07.8c", F)
v.check("01-07.8d", quad(lambda d: F, 1e-3, 2e-3)[0])
E = lambda d: Q**2 * d / (2 * epsilon_0 * A)  # noqa: E731
v.check("01-07.8e", E(1e-3))
v.check("01-07.8f", E(2e-3))
v.assert_true("work = energy increase", math.isclose(E(2e-3) - E(1e-3), F * 1e-3, rel_tol=1e-12))

pdf = lambda r, sig: math.exp(-((r - 1e4) ** 2) / (2 * sig * sig)) / (sig * math.sqrt(2 * math.pi))  # noqa: E731
v.check("01-07.9a", 100 * quad(lambda r: pdf(r, 50), 1e4 - 100, 1e4 + 100)[0])
v.check("01-07.9b", 100 * quad(lambda r: pdf(r, 50), 1e4 - 50, 1e4 + 50)[0])
v.check("01-07.9c", 100 * quad(lambda r: pdf(r, 25), 1e4 - 50, 1e4 + 50)[0])

lam = 1000 * 2e-7
v.check("01-07.10a", lam)
v.check("01-07.10b", 1 / lam)
v.check("01-07.10c", math.exp(-lam * 720))
lm = sp.symbols("lambda", positive=True)
v.assert_true("exponential mean = 1/lambda", sp.integrate(t * lm * sp.exp(-lm * t), (t, 0, sp.oo)) == 1 / lm)

v.check("01-07.11a", 6.02 * 16 + 1.76)
v.check("01-07.11b", 6.02 * 10 + 1.76)
v.check("01-07.11c", (70 - 1.76) / 6.02)
v.check("01-07.11d", 10 * math.log10(4))

tau = 1e-3
i2t = quad(lambda tt: (50 * math.exp(-tt / tau)) ** 2, 0, np.inf)[0]
v.check("01-07.12a", i2t)
v.check("01-07.12b", i2t / 50**2 * 1e3)
v.assert_true("2 A²s fuse survives, 1 A²s blows", 1 < i2t < 2)

Vq = lambda xx: 4.2 - 0.6 * xx - 0.3 * xx**2  # noqa: E731
Qc = 3.0
v.check("01-07.13a", Qc * quad(Vq, 0, 1)[0])
v.check("01-07.13b", quad(Vq, 0, 1)[0])
v.check("01-07.13c", (Vq(0) + Vq(1)) / 2)
xs = brentq(lambda xx: Vq(xx) - 3.5, 0, 1)
v.check("01-07.13d", (1 - xs) * 3000)
v.check("01-07.13e", Qc * quad(Vq, 0, xs)[0])
v.check("01-07.13f", Qc * quad(Vq, xs, 1)[0])
v.assert_true("3.3 V cut-off gains >15 % energy over 3.5 V",
              Qc * quad(Vq, 0, 1)[0] / (Qc * quad(Vq, 0, xs)[0]) > 1.15)

I0, Dpp, Duty = 2.0, 0.6, 0.3
ms_tri = quad(lambda s: (Dpp * (np.interp(s, [0, 0.3, 1], [-0.5, 0.5, -0.5]))) ** 2, 0, 1, points=[0.3])[0]
v.assert_true("triangular ripple mean square = Delta^2/12", math.isclose(ms_tri, Dpp**2 / 12, rel_tol=1e-9))
Irms = math.sqrt(I0**2 + ms_tri)
v.check("01-07.14a", Irms)
v.check("01-07.14b", Irms**2 * 0.02 * 1e3)
v.check("01-07.14c", math.sqrt(Duty) * Irms)

v.check("01-07.15a", 100 * 2 * norm.sf(3))
v.check("01-07.15b", 2 * norm.sf(6))
mean_abs = 2 * quad(lambda z: z * norm.pdf(z), 0, np.inf)[0]
v.check("01-07.15c", mean_abs)
v.check("01-07.15d", FF * mean_abs)
v.check("01-07.15e", 100 * (FF * mean_abs - 1))

# ---------------------------------------------------------------- lab handout
v.check("Lab 01-07.a", rms(lambda s: 10 * math.cos(W * s - math.pi / 6)))
v.check("Lab 01-07.b", 6.02 * 10 + 1.76 + 20 * math.log10(0.5))
tt = np.linspace(0, 1, 200000, endpoint=False)
pulse = np.where(np.abs(np.sin(2 * np.pi * tt)) > 0.9, np.sign(np.sin(2 * np.pi * tt)), 0.0)
v.check("Lab 01-07.c", 100 * (FF * np.abs(pulse).mean() / math.sqrt((pulse**2).mean()) - 1))
v.check("Lab 01-07.d", 0.5 * 170 * 10 * math.cos(math.pi / 3))
v.check("Lab 01-07.e", 17 * math.sin(math.pi / 3) / (2 * math.pi * 60) * 1e3)
x_only = 14.722 * math.tan(math.pi / 3)
z_only = math.hypot(14.722, x_only)
v.check("Lab 01-07.f", x_only)
v.check("Lab 01-07.g", z_only)
v.check("Lab 01-07.h", 0.5 * 170**2 * 14.722 / z_only**2)

# ---------------------------------------------------------------- audit additions (§3.7, Problems 16-19)
from scipy.integrate import quad as _quad  # noqa: E402

v.check("T 01-07.a", _quad(lambda x: x - x * x, 0, 1)[0])
v.check("T 01-07.b", _quad(lambda x: x * x, 0, 1)[0] / _quad(lambda x: x, 0, 1)[0])
v.check("01-07.1i", rms(lambda s: 4 * (s % 1.0) - 2))
e0 = 8.854187817e-12
k16 = e0 * 1e-6 * 25 / 2
v.check("01-07.16a", k16 / (2e-6) ** 2 * 1e6)
v.check("01-07.16b", k16)
W16 = _quad(lambda x: k16 / x**2, 2e-6, 4e-6)[0]
v.check("01-07.16c", W16 * 1e12)
v.check("01-07.16d", k16 / 2e-6 * 1e12)
v.check("01-07.16e", k16 / 4e-6 * 1e12)
v.check("01-07.16f", e0 * 1e-6 / 2e-6 * 1e12)
v.check("01-07.16g", e0 * 1e-6 / 4e-6 * 1e12)
dQ = 5 * (e0 * 1e-6 / 2e-6 - e0 * 1e-6 / 4e-6)
v.check("01-07.16h", dQ * 1e12)
v.check("01-07.16i", 5 * dQ * 1e12)
v.assert_true("energy balance: W + released = source", math.isclose(W16 + (k16 / 2e-6 - k16 / 4e-6), 5 * dQ, rel_tol=1e-9))
A17 = _quad(lambda x: math.sqrt(x) - x * x, 0, 1)[0]
v.check("01-07.17a", A17)
v.check("01-07.17b", _quad(lambda x: x * (math.sqrt(x) - x * x), 0, 1)[0] / A17)
v.check("01-07.17c", _quad(lambda y: y * (math.sqrt(y) - y * y), 0, 1)[0] / A17)
V18 = _quad(lambda z: math.pi * (2 + z / 100) ** 2, 0, 50)[0]
v.check("01-07.18a", V18)
v.check("01-07.18b", math.pi * 2.5**2 * 50)
v.check("01-07.18c", 100 * V18 / (math.pi * 2.5**2 * 50))
v.assert_true("frustum formula agrees", math.isclose(V18, math.pi * 50 / 3 * (6.25 + 5 + 4)))
L19 = _quad(lambda x: math.sqrt(1 + math.sinh(x / 500) ** 2), -100, 100)[0]
v.check("01-07.19a", L19)
v.check("01-07.19b", 100 * (L19 / 200 - 1))
sag = 500 * (math.cosh(0.2) - 1)
v.check("01-07.19c", sag)
v.check("01-07.19d", 200 * (1 + 8 / 3 * (sag / 200) ** 2), tol=0.01)

v.finish()
