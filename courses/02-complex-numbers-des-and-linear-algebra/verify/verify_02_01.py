#!/usr/bin/env python3
"""Verify every published number in chapter 02-01 (worked examples, numbers to know,
practitioner lens) and in its problem solutions.

Each value is recomputed from first principles here and compared against the
answer-key tables in the Markdown files at their published precision.
Independent assertions (identities, ODE residuals, numerical ODE solutions) are
checked with v.assert_true().
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier, deg, polar  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-01",
    COURSE / "chapters" / "02-01-complex-numbers-euler-and-phasors.md",
    COURSE / "solutions" / "02-01-solutions.md",
    COURSE / "labs" / "02-01-lab" / "README.md",
)

# =============================================================================== chapter examples
z1, z2 = 3 + 4j, 1 - 2j
v.check("Ex 02-01.1a", z1 + z2)
v.check("Ex 02-01.1b", z1 - z2)
v.check("Ex 02-01.1c", z1 * z2)
v.check("Ex 02-01.1d", z1 / z2)
v.check("Ex 02-01.1e", z1 * z2.conjugate())
v.check("Ex 02-01.1f", z1)
v.check("Ex 02-01.1g", z2)
v.check("Ex 02-01.1h", z1 * z2)
v.check("Ex 02-01.1i", z1 / z2)
v.assert_true("|z1 z2| = |z1||z2|", math.isclose(abs(z1 * z2), abs(z1) * abs(z2)))
v.assert_true("naive arctan gives the wrong quotient angle",
              abs(math.degrees(math.atan((z1 / z2).imag / (z1 / z2).real)) - deg(z1 / z2)) > 90)

v.check("Ex 02-01.2a", (1 + 1j) ** 8)
roots = sorted(np.roots([1, 0, 0, 0, 16]), key=lambda w: (deg(w) % 360))
for ident, w in zip(["Ex 02-01.2b", "Ex 02-01.2c", "Ex 02-01.2d", "Ex 02-01.2e"], roots):
    v.check(ident, complex(w))
v.assert_true("each fourth root satisfies w^4 = -16", all(abs(complex(w) ** 4 + 16) < 1e-9 for w in roots))

V1, V2 = polar(10, 30), polar(5, -110)
v.check("Ex 02-01.3a", V1)
v.check("Ex 02-01.3b", V2)
v.check("Ex 02-01.3c", V1 + V2)
v.check("Ex 02-01.3d", V1 + V2)
t = np.linspace(0, 2 * math.pi, 1000)
direct = 10 * np.cos(t + math.radians(30)) + 5 * np.sin(t - math.radians(20))
S = V1 + V2
v.assert_true("time-domain sum equals phasor-sum sinusoid (Ex 3)",
              np.max(np.abs(direct - abs(S) * np.cos(t + cmath.phase(S)))) < 1e-12)

R, C, f, Vm = 1e3, 100e-9, 1e3, 5.0
w = 2 * math.pi * f
tau = R * C
H = 1 / (1 + 1j * w * tau)
v.check("Ex 02-01.4a", w * tau)
v.check("Ex 02-01.4b", abs(H))
v.check("Ex 02-01.4c", deg(H))
v.check("Ex 02-01.4d", Vm * abs(H))
v.check("Ex 02-01.4e", -deg(H) / 360 / f * 1e6)  # microseconds
v.check("Ex 02-01.4f", 1 / (2 * math.pi * tau) / 1e3)  # kHz
# ODE residual of the steady-state answer, and agreement with a numerical solution from rest
ts = np.linspace(0, 2e-3, 2001)
y = Vm * abs(H) * np.cos(w * ts + cmath.phase(H))
dy = -Vm * abs(H) * w * np.sin(w * ts + cmath.phase(H))
v.assert_true("Ex 4 steady state satisfies RC y' + y = x", np.max(np.abs(tau * dy + y - Vm * np.cos(w * ts))) < 1e-9)
sol = solve_ivp(lambda tt, yy: (Vm * np.cos(w * tt) - yy) / tau, (0, 3e-3), [0.0], rtol=1e-10, atol=1e-12,
                dense_output=True, max_step=1e-6)
tl = np.linspace(2e-3, 3e-3, 500)  # 10+ time constants after start: transient is e^-20 ~ 2e-9 of initial
v.assert_true("Ex 4 numerical ODE solution converges to phasor prediction",
              np.max(np.abs(sol.sol(tl)[0] - Vm * abs(H) * np.cos(w * tl + cmath.phase(H)))) < 1e-6)

R, L, C = 10.0, 20e-3, 100e-6
w = 1000.0
Z = R + 1j * w * L + 1 / (1j * w * C)
v.check("Ex 02-01.5a", Z)
v.check("Ex 02-01.5b", 10 / Z)
w0 = 1 / math.sqrt(L * C)
v.check("Ex 02-01.5c", w0)
I0 = 10 / abs(R + 1j * w0 * L + 1 / (1j * w0 * C))
v.check("Ex 02-01.5d", I0)
v.check("Ex 02-01.5e", w0 * L * I0)
v.check("Ex 02-01.5f", w0 * L / R)

# =============================================================================== numbers to know / practitioner
v.check("N 02-01.a", math.degrees(1))
v.check("N 02-01.b", 2 * math.pi * 50)
v.check("N 02-01.c", 2 * math.pi * 60)
v.check("N 02-01.d", 120 * math.sqrt(2))
v.check("N 02-01.e", 230 * math.sqrt(2))
v.check("N 02-01.f", 100 * 10 ** (-38 / 20))
v.check("N 02-01.g", 20 * math.log10(1 / math.sqrt(2)))
v.check("PL 02-01.a", math.log2(4096))
v.check("PL 02-01.b", 100 * (math.log2(4096) / math.log2(1024) - 1))
# Square M-QAM at equal average power: d_min^2 ∝ 6 Es / (M-1); SNR penalty = ratio of (M-1)
v.check("PL 02-01.c", 10 * math.log10((4096 - 1) / (1024 - 1)))
v.check("PL 02-01.d", 100 * 10 ** (-35 / 20))
# brute-force check of the QAM spacing claim: average energy of a 64x64 vs 32x32 grid of unit spacing
def grid_energy(m):
    lv = np.arange(-(m - 1), m, 2, dtype=float)
    return np.mean(lv ** 2) * 2  # I and Q
ratio_db = 10 * math.log10(grid_energy(64) / grid_energy(32))
v.assert_true("QAM SNR penalty from explicit constellation energies", abs(ratio_db - 10 * math.log10(4095 / 1023)) < 1e-9)

# =============================================================================== problems
for ident, z in [("02-01.1a", -3 + 3j), ("02-01.1b", -2 - 5j), ("02-01.1c", 7j), ("02-01.1d", -4 + 0j)]:
    v.check(ident, z)
v.check("02-01.2a", polar(10, 120))
v.check("02-01.2b", 2 * cmath.exp(-1j * math.pi / 3))
v.check("02-01.2c", polar(5, -90))
v.check("02-01.2d", polar(0.5, 210))
v.check("02-01.3a", 1j ** 7)
v.check("02-01.3b", 1j ** -3)
v.check("02-01.3c", 1 / 1j)
v.check("02-01.3d", (1 + 1j) * (1 - 1j))
v.check("02-01.3e", (1j ** (2026 % 4)))
v.assert_true("j^2026 by exact integer power", sp.I ** 2026 == -1)
v.check("02-01.4a", polar(12, -45))
v.check("02-01.4b", 3 * cmath.exp(1j * math.pi / 2))  # -3 sin x = 3 cos(x + 90°)
v.check("02-01.4c", polar(4, 60 - 90))
v.check("02-01.4d", -150.0)
v.check("02-01.4e", deg(-2j))
xs = np.linspace(0, 10, 101)
v.assert_true("-3 sin x == 3 cos(x + 90°)", np.allclose(-3 * np.sin(xs), 3 * np.cos(xs + math.pi / 2)))
v.assert_true("4 sin(x + 60°) == 4 cos(x - 30°)",
              np.allclose(4 * np.sin(xs + math.radians(60)), 4 * np.cos(xs - math.radians(30))))

a, b = 2 - 3j, -1 + 4j
v.check("02-01.5a", a * b.conjugate())
v.check("02-01.5b", a / b)
v.check("02-01.5c", abs(a + b))
v.check("02-01.5d", a ** 2)
v.check("02-01.5e", (a * b).real)
v.check("02-01.5f", a / b)

# Problems 6 and 7: symbolic proofs
A_, B_, C_, D_ = sp.symbols("a b c d", real=True)
w1, w2 = A_ + sp.I * B_, C_ + sp.I * D_
v.assert_true("P6a |z1 z2|^2 = |z1|^2 |z2|^2",
              sp.simplify(sp.expand((w1 * w2) * sp.conjugate(w1 * w2)) - (A_**2 + B_**2) * (C_**2 + D_**2)) == 0)
v.assert_true("P6c (z1 z2)* = z1* z2*", sp.simplify(sp.conjugate(w1 * w2) - sp.conjugate(w1) * sp.conjugate(w2)) == 0)
th, al, be = sp.symbols("theta alpha beta", real=True)
v.assert_true("P7a cos 3θ = 4cos^3 θ - 3cos θ",
              sp.simplify(sp.re(sp.expand((sp.cos(th) + sp.I * sp.sin(th)) ** 3)) - (4 * sp.cos(th) ** 3 - 3 * sp.cos(th))) == 0)
v.assert_true("P7b sin a sin b product-to-sum",
              sp.simplify(sp.sin(al) * sp.sin(be) - (sp.cos(al - be) - sp.cos(al + be)) / 2) == 0)

r8 = sorted(np.roots([1, 0, 0, 8j]), key=lambda w: ((deg(w) + 30) % 360))  # k = 0, 1, 2 from -30°
for ident, w in zip(["02-01.8a", "02-01.8b", "02-01.8c"], r8):
    v.check(ident, complex(w))
v.assert_true("each cube root satisfies z^3 = -8j", all(abs(complex(w) ** 3 + 8j) < 1e-9 for w in r8))

S9 = polar(4, 60) + polar(3, 90) + polar(2, -135)
v.check("02-01.9a", S9)
v.check("02-01.9b", S9)
direct9 = 4 * np.cos(xs + math.radians(60)) - 3 * np.sin(xs) + 2 * np.cos(xs - math.radians(135))
v.assert_true("P9 time-domain check", np.allclose(direct9, abs(S9) * np.cos(xs + cmath.phase(S9))))

v.check("02-01.10a", 360 * 100e6 * 1.5e-9)
td = 0.05 / 1.5e8
v.check("02-01.10b", td * 1e12)
v.check("02-01.10c", 360 * 2.4e9 * td)
v.check("02-01.10d", 1.5e8 / 2.4e9 * 1e3)

Y11 = polar(10, 30) / (2 * 4j + 8)
v.check("02-01.11", Y11)
ts = np.linspace(0, 5, 501)
y11 = abs(Y11) * np.cos(4 * ts + cmath.phase(Y11))
dy11 = -4 * abs(Y11) * np.sin(4 * ts + cmath.phase(Y11))
v.assert_true("P11 substitution residual", np.max(np.abs(2 * dy11 + 8 * y11 - 10 * np.cos(4 * ts + math.radians(30)))) < 1e-12)
v.assert_true("P11 intermediate 7.071∠75° + 7.071∠-15° = 10∠30°",
              abs(polar(2 * 4 * abs(Y11), 75) + polar(8 * abs(Y11), -15) - polar(10, 30)) < 1e-12)

w = 2 * math.pi * 1000
Z12 = 50 + 1j * w * 0.010
I12 = 20 / Z12
v.check("02-01.12a", Z12)
v.check("02-01.12b", Z12)
v.check("02-01.12c", I12)
v.check("02-01.12d", 50 * abs(I12))
v.check("02-01.12e", w * 0.010 * abs(I12))
v.assert_true("P12 |VR|^2 + |VL|^2 = 20^2", math.isclose((50 * abs(I12)) ** 2 + (w * 0.01 * abs(I12)) ** 2, 400))

R, L, C = 100.0, 1e-3, 10e-9
w0 = 1 / math.sqrt(L * C)
v.check("02-01.13a", w0)
v.check("02-01.13b", w0 / (2 * math.pi) / 1e3)
for f_, ids in [(25e3, ("02-01.13c", "02-01.13d")), (100e3, ("02-01.13e", "02-01.13f"))]:
    w = 2 * math.pi * f_
    Zf = R + 1j * (w * L - 1 / (w * C))
    v.check(ids[0], Zf)
    v.check(ids[1], Zf)

zeta, wn = 0.1, 1000.0
Hf = lambda w: wn**2 / (wn**2 - w**2 + 2j * zeta * wn * w)  # noqa: E731
v.check("02-01.14a", Hf(500))
v.check("02-01.14b", Hf(1000))
v.check("02-01.14c", Hf(2000))
v.check("02-01.14d", wn * math.sqrt(1 - 2 * zeta**2))
v.check("02-01.14e", 1 / (2 * zeta * math.sqrt(1 - zeta**2)))
ws = np.linspace(1, 3000, 3_000_001)
v.assert_true("P14 numerical peak location/value",
              abs(ws[np.argmax(np.abs(Hf(ws)))] - wn * math.sqrt(1 - 2 * zeta**2)) < 0.01
              and abs(np.max(np.abs(Hf(ws))) - 1 / (2 * zeta * math.sqrt(1 - zeta**2))) < 1e-6)

N = 4096
nb = (N // 2) * int(math.log2(N))
v.check("02-01.15a", nb)
v.check("02-01.15b", 4 * nb)
v.check("02-01.15c", 3 * nb)
rng = np.random.default_rng(1)
ok = True
for _ in range(1000):
    a_, b_, c_, d_ = rng.normal(size=4)
    k1, k2, k3 = c_ * (a_ + b_), a_ * (d_ - c_), b_ * (c_ + d_)
    ok &= abs(complex(k1 - k3, k1 + k2) - complex(a_, b_) * complex(c_, d_)) < 1e-12
v.assert_true("P15 three-multiplication form equals direct product (1000 random cases)", ok)

v.check("02-01.16a", 444 - 440)
v.check("02-01.16b", 1 / (444 - 440))
v.check("02-01.16c", (440 + 444) / 2)
tt = np.linspace(0, 1, 100001)
v.assert_true("P16 beat identity", np.allclose(np.cos(2 * np.pi * 440 * tt) + np.cos(2 * np.pi * 444 * tt),
                                               2 * np.cos(2 * np.pi * 2 * tt) * np.cos(2 * np.pi * 442 * tt)))

Vp, Ip = polar(10, 30), polar(2, -15)
v.check("02-01.17a", 0.5 * (Vp * Ip.conjugate()).real)
v.check("02-01.17b", 0.5 * (Vp * Ip).real)
w = 2 * math.pi * 50
tt = np.linspace(0, 1 / 50, 200001)
p = (10 * np.cos(w * tt + math.radians(30))) * (2 * np.cos(w * tt - math.radians(15)))
v.assert_true("P17 numerical average of v·i over one period", abs(np.trapezoid(p, tt) * 50 - 0.5 * (Vp * Ip.conjugate()).real) < 1e-6)

# =============================================================================== lab expected results
v.check("Lab 02-01.A1", deg(-1 - 1j))
th = math.pi
s_, term, n_needed = 0j, 1 + 0j, None
for n in range(60):
    if n > 0:
        term *= 1j * th / n
    s_ += term
    if n_needed is None and abs(s_ - cmath.exp(1j * th)) < 1e-6:
        n_needed = n
v.check("Lab 02-01.B1", n_needed)
v.check("Lab 02-01.C1", abs(polar(10, 30) + polar(5, -60 - 90)))
v.check("Lab 02-01.C2", abs(polar(10, 30) + polar(5, 120 - 90)))
x = 2 * math.pi * 1e3 * 1e3 * 1e-6
Hc = 1 / (1 + 1j * x)
v.check("Lab 02-01.D1", x)
v.check("Lab 02-01.D2", abs(Hc))
v.check("Lab 02-01.D3", 5 * abs(Hc))
v.check("Lab 02-01.D4", deg(Hc))
v.check("Lab 02-01.D5", 5 * abs(1 / (1 + 1j)))
v.check("Lab 02-01.E1", 10 / 2)
v.check("Lab 02-01.E2", (1 / math.sqrt(20e-3 * 100e-6)) * 20e-3 / 2)
H4 = 1 / (1 + 1j * 2 * math.pi * 1e3 * 1e3 * 100e-9)
v.check("Lab 02-01.Q1", 5 * abs(H4) * math.cos(cmath.phase(H4)))

v.finish()
