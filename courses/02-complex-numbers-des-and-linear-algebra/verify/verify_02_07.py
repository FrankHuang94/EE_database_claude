#!/usr/bin/env python3
"""Verify every published number in chapter 02-07, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import scipy.linalg as sl
import sympy as sp
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-07",
    COURSE / "chapters" / "02-07-determinants-inverses-and-vector-spaces.md",
    COURSE / "solutions" / "02-07-solutions.md",
    COURSE / "labs" / "02-07-lab" / "README.md",
)
M = sp.Matrix


def f(x):
    return float(x)


def incidence(branches, n_nodes):
    A = np.zeros((len(branches), n_nodes))
    for k, (s, t) in enumerate(branches):
        A[k, s], A[k, t] = 1, -1
    return A


# ---------------------------------------------------------------- theory identities
a, b, c, d = sp.symbols("a b c d")
v.assert_true("2x2 determinant ad - bc", M([[a, b], [c, d]]).det() == a * d - b * c)
v.assert_true("2x2 inverse formula", sp.simplify(M([[a, b], [c, d]]).inv() - M([[d, -b], [-c, a]]) / (a * d - b * c))
              == sp.zeros(2, 2))
rng = np.random.default_rng(7)
A4, B4 = rng.standard_normal((4, 4)), rng.standard_normal((4, 4))
v.assert_true("det(AB) = det A det B; det A^T = det A; det(cA) = c^n det A",
              np.isclose(np.linalg.det(A4 @ B4), np.linalg.det(A4) * np.linalg.det(B4))
              and np.isclose(np.linalg.det(A4.T), np.linalg.det(A4))
              and np.isclose(np.linalg.det(3 * A4), 3**4 * np.linalg.det(A4)))
P, L, U = sl.lu(A4)
v.assert_true("det = +/- product of pivots", np.isclose(abs(np.linalg.det(A4)), abs(np.prod(np.diag(U)))))
v.assert_true("(AB)^-1 = B^-1 A^-1", np.allclose(np.linalg.inv(A4 @ B4), np.linalg.inv(B4) @ np.linalg.inv(A4)))
Asym = sp.Matrix(3, 3, sp.symbols("m0:9"))
x1, x2, x3 = sp.symbols("x1:4")
xs = M([x1, x2, x3])
X2 = sp.eye(3); X2[:, 1] = xs
v.assert_true("Cramer derivation: det X_i = x_i and A X_i = B_i",
              X2.det() == x2 and (Asym * X2)[:, 1] == Asym * xs)
v.assert_true("adjugate formula A^-1 = adj(A)/det A",
              sp.simplify(M([[2, 1, -1], [4, 5, -3], [-2, 5, 4]]).adjugate() / 30
                          - M([[2, 1, -1], [4, 5, -3], [-2, 5, 4]]).inv()) == sp.zeros(3, 3))
Ar = rng.standard_normal((6, 3)); br = rng.standard_normal(6)
xh = np.linalg.solve(Ar.T @ Ar, Ar.T @ br)
v.assert_true("normal equations match lstsq; residual orthogonal to columns",
              np.allclose(xh, np.linalg.lstsq(Ar, br, rcond=None)[0]) and np.allclose(Ar.T @ (br - Ar @ xh), 0))
tt, bb = sp.symbols("t b", real=True)
v.assert_true("20! value", math.factorial(20) == 2432902008176640000)

# ---------------------------------------------------------------- Example 1
A1 = M([[2, 1, -1], [4, 5, -3], [-2, 5, 4]])
v.check("Ex 02-07.1a", f(M([[3, 1], [2, 4]]).det()))
cof = sum(A1[0, j] * A1.cofactor(0, j) for j in range(3))
v.check("Ex 02-07.1b", f(cof))
v.check("Ex 02-07.1c", f((2 * A1).det()))
v.check("Ex 02-07.1d", f(A1.T.det()))
v.check("Ex 02-07.1e", f(A1.inv().det()))

# ---------------------------------------------------------------- Example 2 (ladder)
K = M([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
Ki = K.inv()
v.check("Ex 02-07.2a", f(K.det()))
v.check("Ex 02-07.2b", f(Ki[0, 0])); v.check("Ex 02-07.2c", f(Ki[1, 1]))
v.check("Ex 02-07.2d", f(Ki[2, 0])); v.check("Ex 02-07.2h", f(Ki[1, 0]))
v.assert_true("Ex 2: K pivots 2, 3/2, 4/3", K.LUdecomposition()[1].diagonal() == M([[2, sp.Rational(3, 2), sp.Rational(4, 3)]]))
bK = M([1, 2, 3])
cram = []
for i in range(3):
    Bi = K.copy(); Bi[:, i] = bK
    cram.append(Bi.det() / K.det())
v.assert_true("Ex 2: Cramer determinants 10, 16, 14", [cr * 4 for cr in cram] == [10, 16, 14])
v.check("Ex 02-07.2e", f(cram[0])); v.check("Ex 02-07.2f", f(cram[1])); v.check("Ex 02-07.2g", f(cram[2]))
v.assert_true("Ex 2: Cramer agrees with K^-1 b", M(cram) == Ki * bK)
v.assert_true("Ex 2: driving-point checks 1 || 3 = 0.75 and 2 || 2 = 1", Ki[0, 0] == sp.Rational(3, 4) and Ki[1, 1] == 1)

# ---------------------------------------------------------------- Example 3 (rank and complete solution)
A3 = M([[1, 2, 0, 1], [2, 4, 1, 4], [3, 6, 2, 7]])
v.check("Ex 02-07.3a", A3.rank())
v.check("Ex 02-07.3b", len(A3.nullspace()))
b3 = (3, 8, 13)
v.check("Ex 02-07.3c", b3[0] - 2 * b3[1] + b3[2])
xp = M([3, 0, 2, 0])
v.assert_true("Ex 3: A x_p = b and special solutions in N(A)",
              A3 * xp == M(b3) and A3 * M([-2, 1, 0, 0]) == sp.zeros(3, 1) and A3 * M([-1, 0, -2, 1]) == sp.zeros(3, 1))
v.check("Ex 02-07.3d", f(xp[0])); v.check("Ex 02-07.3e", f(xp[2]))
v.assert_true("Ex 3: (1,0,0) not in C(A)", A3.rank() < A3.row_join(M([1, 0, 0])).rank())

# ---------------------------------------------------------------- Example 4 (least squares)
T = np.array([0, 20, 40, 60, 80.0]); V = np.array([0.402, 0.598, 0.801, 0.997, 1.205])
A = np.c_[np.ones(5), T]
c4, d4 = np.linalg.solve(A.T @ A, A.T @ V)
e4 = V - A @ np.array([c4, d4])
v.assert_true("Ex 4: normal-equation sums 200, 12000, 4.003, 200.22",
              np.allclose([T.sum(), (T**2).sum(), V.sum(), (T * V).sum()], [200, 12000, 4.003, 200.22]))
v.check("Ex 02-07.4a", d4 * 1e3)
v.check("Ex 02-07.4b", c4)
v.check("Ex 02-07.4c", math.sqrt(e4 @ e4 / 5) * 1e3)
v.check("Ex 02-07.4d", (1.0 - c4) / d4)
v.check("Ex 02-07.4e", e4 @ e4)
v.assert_true("Ex 4: residuals (2.4, -2.1, 0.4, -4.1, 3.4) mV, orthogonal to both columns",
              np.allclose(e4 * 1e3, [2.4, -2.1, 0.4, -4.1, 3.4]) and np.allclose(A.T @ e4, 0, atol=1e-12))
v.assert_true("Ex 4: regression formula agrees",
              np.isclose(d4, ((T - T.mean()) * (V - V.mean())).sum() / ((T - T.mean()) ** 2).sum()))

# ---------------------------------------------------------------- Example 5 (incidence and resistance matrix)
br5 = [(1, 2), (1, 3), (2, 0), (2, 3), (3, 0)]
A5 = incidence(br5, 4)
g5 = np.array([1, 0.5, 1, 0.5, 2.0])
rank5 = np.linalg.matrix_rank(A5)
v.check("Ex 02-07.5a", rank5)
v.check("Ex 02-07.5b", len(br5) - rank5)
A5r = A5[:, 1:]
G5 = A5r.T @ np.diag(g5) @ A5r
v.assert_true("Ex 5: A^T C A reproduces 02-06's G",
              np.allclose(G5, [[1.5, -1, -0.5], [-1, 2.5, -0.5], [-0.5, -0.5, 3]]))
v.assert_true("Ex 5: loops a+d-b and d+e-c lie in N(A^T)",
              np.allclose(A5.T @ [1, -1, 0, 1, 0], 0) and np.allclose(A5.T @ [0, 0, -1, 1, 1], 0))
v.check("Ex 02-07.5c", np.linalg.det(G5))
R5 = np.linalg.inv(G5)
v.check("Ex 02-07.5d", R5[0, 0]); v.check("Ex 02-07.5e", R5[1, 0]); v.check("Ex 02-07.5f", R5[2, 0])
v.check("Ex 02-07.5g", R5[1, 1]); v.check("Ex 02-07.5h", R5[2, 2]); v.check("Ex 02-07.5i", R5[2, 1])
v.assert_true("Ex 5: R symmetric, positive; 10 mA at node 1 gives 02-06's voltages",
              np.allclose(R5, R5.T) and np.all(R5 > 0) and np.allclose(R5[:, 0] * 10, [290 / 27, 130 / 27, 70 / 27]))
par = lambda x, y: x * y / (x + y)  # noqa: E731
v.assert_true("Ex 5: R33 by series-parallel = 0.5 || (1 + 3 || 2)", np.isclose(R5[2, 2], par(0.5, 1 + par(3, 2))))

# ---------------------------------------------------------------- Problems 1-6
v.check("02-07.1a", f(M([[4, -2], [3, 1]]).det()))
v.check("02-07.1b", f(M([[1, 2, 0], [3, -1, 2], [0, 4, 1]]).det()))
v.check("02-07.1c", f(M([[2, 7, -3], [0, -1, 5], [0, 0, 4]]).det()))
d0 = 4
v.check("02-07.2a", 3**3 * d0); v.check("02-07.2b", d0); v.check("02-07.2c", 1 / d0)
v.check("02-07.2d", d0**2); v.check("02-07.2e", -d0); v.check("02-07.2f", (-1) ** 3 * d0)
A_3 = M([[3, 5], [1, 2]])
v.check("02-07.3a", f(A_3.det())); v.check("02-07.3b", f(A_3.inv()[0, 1])); v.check("02-07.3c", f(A_3.inv()[1, 0]))
k = sp.Symbol("k")
v.check("02-07.3d", f(sp.solve(M([[2, k], [4, 6]]).det(), k)[0]))
V4 = M([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
v.check("02-07.4a", f(V4.det()))
v.assert_true("P4: (1,2,3) - 2(4,5,6) + (7,8,9) = 0", V4 * M([1, -2, 1]) == sp.zeros(3, 1))
v.check("02-07.4b", -2)
v.check("02-07.4c", f(M([[1, 1, 0], [0, 1, 1], [1, 0, 1]]).det()))
A_5 = M([[1, 2, 0], [0, 1, 3], [2, 4, 1]])
A5i = A_5.inv()
v.check("02-07.5a", f(A_5.det()))
v.check("02-07.5b", f(A5i[0, 0])); v.check("02-07.5c", f(A5i[0, 2]))
v.check("02-07.5d", f(A5i[1, 2])); v.check("02-07.5e", f(A5i[2, 0]))
v.assert_true("P5: A A^-1 = I", A_5 * A5i == sp.eye(3))
A_6 = M([[1, 1, 1], [2, -1, 1], [1, 2, -1]]); b_6 = M([6, 3, 2])
x6 = []
for i in range(3):
    Bi = A_6.copy(); Bi[:, i] = b_6
    x6.append(Bi.det() / A_6.det())
v.check("02-07.6a", f(A_6.det()))
v.check("02-07.6b", f(x6[0])); v.check("02-07.6c", f(x6[1])); v.check("02-07.6d", f(x6[2]))
v.check("02-07.6e", math.factorial(20) / 1e9 / (365.25 * 86400))
v.check("02-07.6f", 2 / 3 * 20**3)

# ---------------------------------------------------------------- Problems 7-10
A_7 = M([[1, 3, 1, 2], [2, 6, 4, 8], [0, 0, 2, 4]])
ns7 = A_7.nullspace()
v.check("02-07.7a", A_7.rank()); v.check("02-07.7b", len(ns7))
v.assert_true("P7: rref and special solutions", A_7.rref()[0] == M([[1, 3, 0, 0], [0, 0, 1, 2], [0, 0, 0, 0]])
              and ns7[0] == M([-3, 1, 0, 0]) and ns7[1] == M([0, 0, -2, 1]))
v.check("02-07.7c", f(ns7[0][0])); v.check("02-07.7d", f(ns7[1][2]))
A_8 = M([[1, 1, 2], [2, 3, 5], [1, 2, 3]])
cond = lambda bvec: bvec[0] - bvec[1] + bvec[2]  # noqa: E731
v.check("02-07.8a", cond((4, 9, 5)))
v.assert_true("P8: particular and null solutions", A_8 * M([3, 1, 0]) == M([4, 9, 5])
              and A_8 * M([-1, -1, 1]) == sp.zeros(3, 1) and A_8.rank() == 2)
v.check("02-07.8b", 3); v.check("02-07.8c", 1)
v.check("02-07.8d", cond((1, 0, 0)))
v.assert_true("P8: (1,0,0) not solvable", A_8.rank() < A_8.row_join(M([1, 0, 0])).rank())
v.check("02-07.9a", f(abs(M([[3, 1], [1, 4]]).det()) / 2))
v.check("02-07.9b", f(M([[1, 1, 1], [0, 2, 1], [0, 0, 3]]).det()))
v.check("02-07.9c", f(M([[2, 1], [0, 3]]).det()) * math.pi)
t10 = np.arange(4.0); y10 = np.array([1, 3, 4, 4.0])
A10 = np.c_[np.ones(4), t10]
c10 = np.linalg.solve(A10.T @ A10, A10.T @ y10)
e10 = y10 - A10 @ c10
v.check("02-07.10a", c10[0]); v.check("02-07.10b", c10[1]); v.check("02-07.10c", e10 @ e10)
v.check("02-07.10d", (A10.T @ A10)[1, 1]); v.check("02-07.10e", (A10.T @ y10)[1])
v.assert_true("P10: residuals orthogonal", np.allclose(A10.T @ e10, 0))

# ---------------------------------------------------------------- Problems 11-13 (circuits)
G11 = np.array([[1.5, -1], [-1, 1.25]])
R11 = np.linalg.inv(G11)
v.check("02-07.11a", np.linalg.det(G11))
v.check("02-07.11b", R11[0, 0]); v.check("02-07.11c", R11[0, 1]); v.check("02-07.11d", R11[1, 1])
v11 = R11 @ [5, -1]
v.check("02-07.11e", v11[0]); v.check("02-07.11f", v11[1])
v.assert_true("P11: R11 = 2 || 5 and R22 = 4 || 3", np.isclose(R11[0, 0], par(2, 5)) and np.isclose(R11[1, 1], par(4, 3)))
Y12 = np.array([[1 + 2, -1], [-1, 1 + 1.0]])
Z12 = np.linalg.inv(Y12)
v.check("02-07.12a", np.linalg.det(Y12))
v.check("02-07.12b", Z12[0, 0]); v.check("02-07.12c", Z12[1, 0]); v.check("02-07.12d", Z12[1, 1])
v.assert_true("P12: Z11 = 0.5 || 2, Z22 = 1 || 1.5", np.isclose(Z12[0, 0], par(0.5, 2)) and np.isclose(Z12[1, 1], par(1, 1.5)))
br13 = [(1, 2), (1, 3), (2, 3), (2, 0), (3, 0)]
A13 = incidence(br13, 4)
rank13 = np.linalg.matrix_rank(A13)
v.check("02-07.13a", rank13); v.check("02-07.13b", len(br13) - rank13)
A13r = A13[:, 1:]
Gb = A13r.T @ np.eye(5) @ A13r
vb = np.linalg.solve(Gb, [1, 0, 0])
v.check("02-07.13c", vb[0]); v.check("02-07.13d", vb[1]); v.check("02-07.13e", vb[1] - vb[2])
Gu = A13r.T @ np.diag([1, 1, 1, 1, 0.5]) @ A13r
vu = np.linalg.solve(Gu, [1, 0, 0])
v.assert_true("P13: unbalanced voltages 13/11, 7/11, 8/11", np.allclose(vu, [13 / 11, 7 / 11, 8 / 11]))
v.check("02-07.13f", vu[0]); v.check("02-07.13g", vu[1]); v.check("02-07.13h", vu[2])
v.check("02-07.13i", vu[2] - vu[1]); v.check("02-07.13j", vu[0] / 1)

# ---------------------------------------------------------------- Problem 14 (exponential fit)
t14 = np.arange(5.0); v14 = np.array([5.00, 3.05, 1.85, 1.12, 0.68])
A14 = np.c_[np.ones(5), t14]
a14, b14 = np.linalg.solve(A14.T @ A14, A14.T @ np.log(v14))
v.check("02-07.14a", b14); v.check("02-07.14b", math.exp(a14)); v.check("02-07.14c", -1 / b14)
(p_V0, p_tau), _ = curve_fit(lambda t_, V0, tau: V0 * np.exp(-t_ / tau), t14, v14, p0=(5.0, 2.0),
                             xtol=1e-14, ftol=1e-14)
v.check("02-07.14d", p_V0); v.check("02-07.14e", p_tau)
v.check("02-07.14f", (p_tau - (-1 / b14)) / (-1 / b14) * 100, tol=0.05)

# ---------------------------------------------------------------- Problem 15 (low rank)
uv = M([1, 2, 3]) * M([[4, 5]])
v.check("02-07.15a", uv.rank())
dd, rr = 4096, 8
v.check("02-07.15b", dd * dd); v.check("02-07.15c", 2 * dd * rr); v.check("02-07.15d", dd * dd / (2 * dd * rr))
v.check("02-07.15e", dd * dd * 2 / 2**20); v.check("02-07.15f", 2 * dd * rr * 2 / 2**10)
Bm, Am = rng.standard_normal((50, 3)), rng.standard_normal((3, 50))
v.assert_true("P15: rank(BA) <= r", np.linalg.matrix_rank(Bm @ Am) <= 3)

# ---------------------------------------------------------------- numbers to know
v.check("N 02-07.a", math.factorial(20))
n_ = 1000
v.check("N 02-07.b", (2 * n_**3) / (2 / 3 * n_**3))
# Sourced constants (R-041 to R-044): recorded values, re-stated here so that the key is checked against the log
SOURCED = {"N 02-07.c": 8, "N 02-07.d": 4, "N 02-07.e": 8, "N 02-07.f": 8, "N 02-07.g": 10000, "N 02-07.h": 3}
for key, val in SOURCED.items():
    v.check(key, val)
v.check("N 02-07.i", 3 + 1)   # three coordinates plus one clock offset

# ---------------------------------------------------------------- lab handout
sq = np.array([[0, 0], [1, 0], [1, 1], [0, 1.0]]) @ np.array([[1, 2], [3, 4.0]]).T
x_, y_ = sq[:, 0], sq[:, 1]
v.check("Lab 02-07.a", 0.5 * abs(x_ @ np.roll(y_, -1) - y_ @ np.roll(x_, -1)))
v.check("Lab 02-07.b", math.factorial(12) // math.factorial(9))
rng2 = np.random.default_rng(11)
u1, u2, w1, w2 = (rng2.standard_normal(6) for _ in range(4))
Mn = np.outer(u1, w1) + np.outer(u2, w2) + 1e-13 * rng2.standard_normal((6, 6))
v.check("Lab 02-07.c", np.linalg.matrix_rank(Mn, tol=1e-10))
for deg, key in ((2, "Lab 02-07.d"), (4, "Lab 02-07.e")):
    cpoly = np.polyfit(T, V, deg)
    v.check(key, float(np.sum((np.polyval(cpoly, T) - V) ** 2)))

# audit additions -------------------------------------------------------------
# Example 02-07.4 noise estimate with m - 2 degrees of freedom
_T = np.array([0, 20, 40, 60, 80.0]); _V = np.array([0.402, 0.598, 0.801, 0.997, 1.205])
_A4 = np.c_[np.ones(5), _T]
_x4, _ssr4, *_ = np.linalg.lstsq(_A4, _V, rcond=None)
v.check("Ex 02-07.4f", math.sqrt(_ssr4[0] / 3) * 1e3)
# Example 02-07.6 QR least squares (numpy QR, sign-normalized to positive diagonal)
_A6 = np.array([[1, 0], [1, 1], [1, 2.0]]); _b6 = np.array([1, 2, 4.0])
_Q6, _R6 = np.linalg.qr(_A6)
_sg = np.sign(np.diag(_R6)); _Q6 = _Q6 * _sg; _R6 = (_R6.T * _sg).T
v.check("Ex 02-07.6a", _R6[0, 0]); v.check("Ex 02-07.6b", _R6[1, 1])
_qb = _Q6.T @ _b6
v.check("Ex 02-07.6c", _qb[0]); v.check("Ex 02-07.6d", _qb[1])
_x6 = np.linalg.solve(_R6, _qb)
v.check("Ex 02-07.6e", _x6[1]); v.check("Ex 02-07.6f", _x6[0])
v.assert_true("QR agrees with the normal equations", np.allclose(_x6, np.linalg.solve(_A6.T @ _A6, _A6.T @ _b6)))
# 16 subspaces: test closure numerically on samples
_rng = np.random.default_rng(0)
def _closed(member, sampler):
    pts = [sampler() for _ in range(20)]
    if not member(np.zeros(3)):
        return False
    return all(member(a + b) and member(-2.5 * a) for a in pts for b in pts)
_sets = [
    (lambda x: abs(x[0] + 2 * x[1] - x[2]) < 1e-9, lambda: (lambda u, w: np.array([u, w, u + 2 * w]))(*_rng.standard_normal(2))),
    (lambda x: abs(x[0] + 2 * x[1] - x[2] - 1) < 1e-9, lambda: (lambda u, w: np.array([u, w, u + 2 * w - 1]))(*_rng.standard_normal(2))),
    (lambda x: np.linalg.norm(np.cross(x, [1, 2, 3])) < 1e-9, lambda: _rng.standard_normal() * np.array([1, 2, 3.0])),
    (lambda x: x[0] >= -1e-12, lambda: np.abs(_rng.standard_normal(3))),
    (lambda x: (abs(x[1]) < 1e-12 and abs(x[2]) < 1e-12) or (abs(x[0]) < 1e-12 and abs(x[2]) < 1e-12),
     lambda: np.array([_rng.standard_normal(), 0, 0]) if _rng.random() < 0.5 else np.array([0, _rng.standard_normal(), 0])),
    (lambda x: abs(x[0] - x[1]) < 1e-9 and abs(x[1] - x[2]) < 1e-9, lambda: _rng.standard_normal() * np.ones(3)),
]
v.check("02-07.16a", sum(_closed(m_, s_) for m_, s_ in _sets))
v.check("02-07.16b", 3 - np.linalg.matrix_rank(np.array([[1, 2, -1.0]])))
v.check("02-07.17a", np.linalg.det(np.array([[0, 2, 1], [1, 1, 1], [2, 0, 3.0]])))
_a18 = np.array([1, 2, 2.0]); _P = np.outer(_a18, _a18) / (_a18 @ _a18)
v.check("02-07.18a", _P[0, 0]); v.check("02-07.18b", _P[1, 1]); v.check("02-07.18c", np.trace(_P))
v.check("02-07.18d", (_P @ np.array([1, 0, 0.0]))[1])
v.assert_true("P^2 = P, P^T = P, (I-P)b perpendicular to a", np.allclose(_P @ _P, _P) and np.allclose(_P, _P.T) and abs(((np.eye(3) - _P) @ np.array([1, 0, 0.0])) @ _a18) < 1e-12)
_M19 = _rng.standard_normal((5, 3)) @ _rng.standard_normal((3, 7))
_r19 = np.linalg.matrix_rank(_M19)
v.check("02-07.19a", 7 - _r19); v.check("02-07.19b", 5 - _r19)
_Atri = np.array([[1, -1, 0], [0, 1, -1], [-1, 0, 1.0]])
v.check("02-07.19c", np.linalg.matrix_rank(_Atri))
v.assert_true("triangle: (1,1,1) in N(A) and N(A^T)", np.allclose(_Atri @ np.ones(3), 0) and np.allclose(_Atri.T @ np.ones(3), 0))
_A20 = np.array([[1, 1], [2, 0], [2, 1.0]]); _b20 = np.array([3, 3, 3.0])
_Q20, _R20 = np.linalg.qr(_A20); _sg = np.sign(np.diag(_R20)); _Q20 = _Q20 * _sg; _R20 = (_R20.T * _sg).T
v.check("02-07.20a", _R20[0, 0]); v.check("02-07.20b", _R20[0, 1])
_x20 = np.linalg.solve(_R20, _Q20.T @ _b20)
v.check("02-07.20c", _x20[0]); v.check("02-07.20d", _x20[1])
v.check("02-07.20e", np.linalg.norm(_b20 - _A20 @ _x20))

v.finish()
