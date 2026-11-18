#!/usr/bin/env python3
"""Verify every published number in chapter 02-09, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-09",
    COURSE / "chapters" / "02-09-systems-of-odes-and-matrix-exponential.md",
    COURSE / "solutions" / "02-09-solutions.md",
    COURSE / "labs" / "02-09-lab" / "README.md",
)
M = sp.Matrix
t, s = sp.symbols("t s")
rng = np.random.default_rng(9)


def thermal_model(Rdh=0.5, Rha=1.5, Cd=2.0, Ch=50.0):
    A = np.array([[-1 / (Rdh * Cd), 1 / (Rdh * Cd)], [1 / (Rdh * Ch), -(1 / Rdh + 1 / Rha) / Ch]])
    return A, np.array([1 / Cd, 0.0])


# ---------------------------------------------------------------- theory identities
A4 = rng.standard_normal((4, 4))
h = 1e-6
v.assert_true("d/dt e^{At} = A e^{At} (finite difference at t = 0.7)",
              np.allclose((expm(A4 * (0.7 + h)) - expm(A4 * (0.7 - h))) / (2 * h), A4 @ expm(A4 * 0.7), rtol=1e-6, atol=1e-6))
v.assert_true("e^{A(t+s)} = e^{At} e^{As}; inverse e^{-At}",
              np.allclose(expm(A4 * 1.3), expm(A4 * 0.5) @ expm(A4 * 0.8)) and np.allclose(expm(A4) @ expm(-A4), np.eye(4)))
B4 = rng.standard_normal((4, 4))
v.assert_true("e^{A+B} != e^A e^B for non-commuting A, B", not np.allclose(expm(A4 + B4), expm(A4) @ expm(B4)))
v.assert_true("det e^{At} = e^{tr(A) t}", np.isclose(np.linalg.det(expm(A4 * 0.9)), math.exp(np.trace(A4) * 0.9)))
Asym = M([[0, 1], [-2, -3]])
v.assert_true("L{e^{At}} = (sI - A)^-1 (2x2 example)",
              sp.simplify(sp.laplace_transform((Asym * t).exp(), t, s, noconds=True) - (s * sp.eye(2) - Asym).inv()) == sp.zeros(2, 2))
x0v = rng.standard_normal(4); u0 = 0.7; Bv = rng.standard_normal(4)
A4s = A4 - 4 * np.eye(4)                 # make it stable for the forced-response check
xss = -np.linalg.solve(A4s, Bv * u0)
ivp = solve_ivp(lambda tt, x: A4s @ x + Bv * u0, (0, 1.5), x0v, rtol=1e-11, atol=1e-13)
v.assert_true("constant-input solution x = xss + e^{At}(x0 - xss)",
              np.allclose(ivp.y[:, -1], xss + expm(A4s * 1.5) @ (x0v - xss), atol=1e-8))
T_ = 0.3
Bd = np.linalg.solve(A4s, (expm(A4s * T_) - np.eye(4)) @ Bv)
xk = x0v.copy()
for _ in range(5):
    xk = expm(A4s * T_) @ xk + Bd * u0
v.assert_true("ZOH discretization is exact at the samples", np.allclose(xk, xss + expm(A4s * 1.5) @ (x0v - xss)))
lam_, al_, w0_ = sp.symbols("lambda alpha omega_0")
R_, L_, C_ = sp.symbols("R L C", positive=True)
Arlc = M([[0, 1 / C_], [-1 / L_, -R_ / L_]])
v.assert_true("series RLC state matrix: char poly lambda^2 + (R/L) lambda + 1/(LC)",
              sp.expand((lam_ * sp.eye(2) - Arlc).det() - (lam_**2 + R_ / L_ * lam_ + 1 / (L_ * C_))) == 0)

# ---------------------------------------------------------------- Example 1 (RLC state space)
A1 = np.array([[0, 1e6], [-100, -5000.0]]); B1 = np.array([0, 100.0]); C1 = np.array([1.0, 0])
ev1 = np.linalg.eigvals(A1)
v.check("Ex 02-09.1a", abs(ev1[0].imag))
v.check("Ex 02-09.1b", -C1 @ np.linalg.solve(A1, B1))
H1 = sp.simplify((M([[1, 0]]) * (s * sp.eye(2) - M([[0, 10**6], [-100, -5000]])).inv() * M([0, 100]))[0])
v.assert_true("Ex 1: H(s) = 1e8/(s^2 + 5000 s + 1e8)", sp.simplify(H1 - 10**8 / (s**2 + 5000 * s + 10**8)) == 0)

# ---------------------------------------------------------------- Example 2 (coupled capacitors, tau = 1)
A2 = np.array([[-2, 1], [1, -2.0]])
x2 = lambda tt: expm(A2 * tt) @ [1.0, 0.0]  # noqa: E731
tpk = math.log(3) / 2
v.assert_true("Ex 2: v2 peak where derivative vanishes", abs((A2 @ x2(tpk))[1]) < 1e-12)
v.check("Ex 02-09.2a", tpk)
v.check("Ex 02-09.2b", x2(tpk)[1])
v.check("Ex 02-09.2c", x2(1.0)[0]); v.check("Ex 02-09.2d", x2(1.0)[1])
v.assert_true("Ex 2: closed form 0.5(e^-t + e^-3t), 0.5(e^-t - e^-3t)",
              np.allclose(x2(0.8), [0.5 * (math.exp(-0.8) + math.exp(-2.4)), 0.5 * (math.exp(-0.8) - math.exp(-2.4))]))

# ---------------------------------------------------------------- Example 3
E3 = expm(A2)
v.check("Ex 02-09.3a", E3[0, 0]); v.check("Ex 02-09.3b", E3[0, 1])
wt = 1.3
v.assert_true("Ex 3(b): exp of rotation generator is the rotation by omega t",
              np.allclose(expm(np.array([[0, -wt], [wt, 0]])), [[math.cos(wt), -math.sin(wt)], [math.sin(wt), math.cos(wt)]]))
EJ = (M([[-1, 1], [0, -1]]) * t).exp()
v.assert_true("Ex 3(c): Jordan block exponential", sp.simplify(EJ - M([[sp.exp(-t), t * sp.exp(-t)], [0, sp.exp(-t)]])) == sp.zeros(2, 2))
v.check("Ex 02-09.3c", float(EJ[0, 1].subs(t, 1)))

# ---------------------------------------------------------------- Example 4
mats = {"A1": [[-2, 1], [1, -2]], "A2": [[1, 2], [2, 1]], "A3": [[-1, -4], [1, -1]], "A4": [[0, 1], [-4, 0]]}
tr = {k: np.trace(np.array(m, float)) for k, m in mats.items()}
de = {k: np.linalg.det(np.array(m, float)) for k, m in mats.items()}
v.check("Ex 02-09.4a", de["A2"])
v.check("Ex 02-09.4b", tr["A3"] ** 2 - 4 * de["A3"])
v.assert_true("Ex 4: eigenvalues as tabulated",
              np.allclose(sorted(np.linalg.eigvals(np.array(mats["A1"], float))), [-3, -1])
              and np.allclose(sorted(np.linalg.eigvals(np.array(mats["A2"], float))), [-1, 3])
              and np.allclose(np.sort_complex(np.linalg.eigvals(np.array(mats["A3"], float))), [-1 - 2j, -1 + 2j])
              and np.allclose(np.sort_complex(np.linalg.eigvals(np.array(mats["A4"], float))), [-2j, 2j]))

# ---------------------------------------------------------------- Example 5 (thermal)
A5, B5 = thermal_model()
P5 = 10.0
xss5 = -np.linalg.solve(A5, B5 * P5)
v.check("Ex 02-09.5a", xss5[0]); v.check("Ex 02-09.5b", xss5[1])
w5, V5 = np.linalg.eig(A5); w5, V5 = np.real(w5), np.real(V5)
order = np.argsort(-w5)            # fast (more negative) last
taus = -1 / w5
v.check("Ex 02-09.5c", taus.min()); v.check("Ex 02-09.5d", taus.max())
Td = lambda tt: (xss5 + expm(A5 * tt) @ (-xss5))[0]  # noqa: E731
v.check("Ex 02-09.5e", Td(1.0)); v.check("Ex 02-09.5f", Td(10.0)); v.check("Ex 02-09.5g", Td(100.0))
c5 = np.linalg.solve(V5, -xss5)
Rf = -(c5 * V5[0]) / P5
fast, slow = np.argmin(taus), np.argmax(taus)
v.check("Ex 02-09.5h", Rf[fast]); v.check("Ex 02-09.5i", Rf[slow])
v.assert_true("Ex 5: Foster R sum = 2 K/W and Zth matches the state solution",
              np.isclose(Rf.sum(), 2.0) and np.isclose(P5 * sum(r * (1 - math.exp(-37.0 / q)) for r, q in zip(Rf, taus)), Td(37.0)))
v.assert_true("Ex 5: die amplitudes -4.616 and -15.38", np.allclose(sorted(c5 * V5[0]), [-15.384, -4.616], atol=1e-3))

# ---------------------------------------------------------------- Example 6 (sampling)
v.check("Ex 02-09.6a", math.exp(-0.5)); v.check("Ex 02-09.6b", math.exp(-1.5))
v.check("Ex 02-09.6c", min(np.linalg.eigvals(np.eye(2) + A2 * 0.5)))
v.check("Ex 02-09.6d", min(np.linalg.eigvals(np.eye(2) + A2 * 1.0)))
v.check("Ex 02-09.6e", 2 / 3)
v.assert_true("Ex 6: exact discrete eigenvalues e^{lambda T}", np.allclose(sorted(np.linalg.eigvals(expm(A2 * 0.5))), [math.exp(-1.5), math.exp(-0.5)]))

# ---------------------------------------------------------------- numbers to know
v.check("N 02-09.a", math.log(100))

# ---------------------------------------------------------------- Problems 1-4
R, L, C = 1e3, 10e-3, 100e-9
Ap1 = np.array([[-1 / (R * C), -1 / C], [1 / L, 0]])
v.check("02-09.1a", np.trace(Ap1)); v.check("02-09.1b", np.linalg.det(Ap1))
v.check("02-09.1c", abs(np.linalg.eigvals(Ap1)[0].imag)); v.check("02-09.1d", 1 / math.sqrt(L * C))
v.assert_true("P1: DC steady state vC = 0, iL = is", np.allclose(-np.linalg.solve(Ap1, np.array([1 / C, 0]) * 1e-3), [0, 1e-3]))
Ap2 = np.array([[0, 1, 0], [0, 0, 1], [-6, -11, -6.0]])
v.assert_true("P2: eigenvalues -1, -2, -3", np.allclose(sorted(np.linalg.eigvals(Ap2).real), [-3, -2, -1]))
v.check("02-09.2a", np.trace(Ap2)); v.check("02-09.2b", np.linalg.det(Ap2))
v.assert_true("P3(b): e^{Nt} = I + Nt", sp.simplify((M([[0, 1], [0, 0]]) * t).exp() - M([[1, t], [0, 1]])) == sp.zeros(2, 2))
v.check("02-09.3a", np.linalg.det(expm(np.array([[1, 2], [3, 4.0]]))))
v.assert_true("P4: classifications", (9 - 8 > 0) and (1 - 16 < 0) and (4 - 4 == 0))

# ---------------------------------------------------------------- Problems 5-12
x5 = expm(np.array([[1, 2], [2, 1.0]])) @ [1, 0]
v.check("02-09.5a", x5[0]); v.check("02-09.5b", x5[1])
x6 = expm(np.array([[-1, -4], [1, -1.0]]) * 0.5) @ [1, 0]
v.check("02-09.6a", x6[0]); v.check("02-09.6b", x6[1])
v.assert_true("P6: closed form e^-t (cos 2t, 0.5 sin 2t)", np.allclose(x6, math.exp(-0.5) * np.array([math.cos(1), 0.5 * math.sin(1)])))
v.check("02-09.7a", 0.5); v.check("02-09.7b", (expm(np.array([[-2, 1], [0, -2.0]]) * 0.5) @ [0, 1])[0])
E8 = expm(np.array([[0, 1], [-2, -3.0]]))
v.check("02-09.8a", E8[0, 0]); v.check("02-09.8b", E8[0, 1])
v.assert_true("P8: entries 2e^-1 - e^-2 and e^-1 - e^-2", np.isclose(E8[0, 0], 2 * math.exp(-1) - math.exp(-2))
              and np.isclose(E8[0, 1], math.exp(-1) - math.exp(-2)))
B9 = np.array([1.0, 0.0])
xss9 = -np.linalg.solve(A2, B9)
v.check("02-09.9a", xss9[0]); v.check("02-09.9b", xss9[1])
v.check("02-09.9c", (xss9 + expm(A2) @ (-xss9))[1])
H10 = sp.simplify((M([[0, 1]]) * (s * sp.eye(2) - M([[-2, 1], [1, -2]])).inv() * M([1, 0]))[0])
v.assert_true("P10: H(s) = 1/((s+1)(s+3))", sp.simplify(H10 - 1 / ((s + 1) * (s + 3))) == 0)
v.check("02-09.10a", abs(complex(H10.subs(s, sp.I))))
kk = sp.Symbol("k")
v.check("02-09.11a", float(sp.solve(M([[-1, kk], [1, -2]]).det(), kk)[0]))
tau12, T12 = 2e-3, 0.5e-3
v.check("02-09.12a", math.exp(-T12 / tau12)); v.check("02-09.12b", 1 - math.exp(-T12 / tau12))
v.check("02-09.12c", 1 - T12 / tau12); v.check("02-09.12d", 2 * tau12 * 1e3)

# ---------------------------------------------------------------- Problems 13-15
Lr = 1e-6
Cm = np.array([[1.1e-9, -0.1e-9], [-0.1e-9, 1.1e-9]])
A13 = np.block([[np.zeros((2, 2)), -np.linalg.inv(Cm)], [np.eye(2) / Lr, np.zeros((2, 2))]])
ev13 = np.linalg.eigvals(A13)
fr = np.sort(np.unique(np.round(np.abs(ev13.imag) / (2 * math.pi), 3)))
v.assert_true("P13: purely imaginary eigenvalues", np.max(np.abs(ev13.real)) < 1e-3 * np.max(np.abs(ev13.imag)))
v.check("02-09.13a", fr[-1] / 1e6); v.check("02-09.13b", fr[0] / 1e6)
Rf14 = [0.2, 0.5, 1.3]; tf14 = [1e-3, 50e-3, 2.0]
Z14 = sum(r * (1 - math.exp(-10e-3 / q)) for r, q in zip(Rf14, tf14))
v.check("02-09.14a", sum(Rf14)); v.check("02-09.14b", Z14); v.check("02-09.14c", 50 * Z14); v.check("02-09.14d", 100 / Z14)
tau15, d15 = 50e-3, 1e-3
abar = math.exp(-d15 / tau15)
v.check("02-09.15a", abar); v.check("02-09.15b", (abar - 1) * (1 / tau15) / (-1 / tau15))
v.check("02-09.15c", math.log(100) / (d15 / tau15))
hk, ok = 0.0, True
for k in range(1, 200):
    hk = abar * hk + (1 - abar)
    ok &= abs(hk - (1 - math.exp(-k * d15 / tau15))) < 1e-12
v.assert_true("P15: sampled step response equals the continuous one at every sample", ok)

# ---------------------------------------------------------------- lab handout
v.check("Lab 02-09.a", sum(r * (1 - math.exp(-0.1 / q)) for r, q in zip(Rf, taus)))
v.check("Lab 02-09.b", 20 * math.log(100))
v.check("Lab 02-09.c", 2 / np.max(np.abs(w5)))
v.check("Lab 02-09.d", 2 * math.pi / 2)

v.finish()
