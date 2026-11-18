#!/usr/bin/env python3
"""Verify every number in the Course 02 final-exam solutions.

Each value is recomputed independently (numpy, scipy, sympy), not copied from the solutions.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import expm, lu
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("02-exam", HERE.parent / "exam" / "solutions.md")
deg = math.degrees
t, s = sp.symbols("t s", positive=True)

# 1 · complex arithmetic
z1, z2 = 3 + 4j, 1 - 1j
v.check("X02.1a", abs(z1))
v.check("X02.1b", deg(cmath.phase(z1)))
v.check("X02.1c", (z1 * z2).real)
v.check("X02.1d", (z1 * z2).imag)
v.check("X02.1e", (z1 / z2).real)
v.check("X02.1f", (z1 / z2).imag)
roots = np.roots([1, 0, 0, -8j])
v.assert_true("cube roots satisfy z^3 = 8j", np.allclose(roots**3, 8j))
r30 = [r for r in roots if abs(deg(cmath.phase(r)) - 30) < 1e-6][0]
r270 = [r for r in roots if abs(deg(cmath.phase(r)) + 90) < 1e-6][0]
v.check("X02.1g", r30.real)
v.check("X02.1h", r270.imag)
tt = np.linspace(0, 2 * np.pi, 2001)
wave = 10 * np.cos(tt + np.radians(30)) + 5 * np.sin(tt)
v.check("X02.1i", wave.max())
v.check("X02.1j", deg(np.angle(np.sum(wave * np.exp(-1j * tt)))), tol=1e-6)
v.assert_true("roots sum to zero", abs(roots.sum()) < 1e-12)

# 2 · series RLC phasor analysis
w, R, L, C = 1000.0, 100.0, 0.1, 20e-6
Z = R + 1j * w * L + 1 / (1j * w * C)
I = 10 / Z
VC = I / (1j * w * C)
v.check("X02.2a", abs(Z))
v.check("X02.2b", deg(cmath.phase(Z)))
v.check("X02.2c", abs(I) * 1e3)
v.check("X02.2d", deg(cmath.phase(I)))
v.check("X02.2e", abs(VC))
v.check("X02.2f", deg(cmath.phase(VC)))
P_src = 0.5 * 10 * abs(I) * math.cos(cmath.phase(Z))
v.check("X02.2g", P_src)
v.assert_true("source power equals resistor power", abs(P_src - 0.5 * abs(I) ** 2 * R) < 1e-12)
w0 = brentq(lambda x: x * L - 1 / (x * C), 100, 5000)
v.check("X02.2h", w0)
v.check("X02.2i", abs(10 / (R + 1j * w0 * L + 1 / (1j * w0 * C))) * 1e3)

# 3 · first-order step response (numerical ODE as an independent check)
tau = 2e3 * 10e-6
sol = solve_ivp(lambda tt_, y: [(5 - y[0]) / tau], (0, 0.1), [1.0], rtol=1e-11, atol=1e-13, dense_output=True)
v.check("X02.3a", tau * 1e3)
v.check("X02.3b", sol.sol(0.01)[0])
v.check("X02.3c", brentq(lambda x: sol.sol(x)[0] - 4, 1e-3, 0.09) * 1e3)
# forward-Euler factor 1 - h/tau: stability edge and sign change
v.check("X02.3d", brentq(lambda h: abs(1 - h / tau) - 1, 1e-3, 0.1) * 1e3)
v.check("X02.3e", brentq(lambda h: 1 - h / tau, 1e-3, 0.03) * 1e3)

# 4 · first-order methods
y = sp.Function("y")
ysol = sp.dsolve(sp.Eq(t * y(t).diff(t) + 3 * y(t), t), y(t), ics={y(1): 0}).rhs
v.check("X02.4a", float(ysol.subs(t, 2)))
k, tau4 = 2.0, 0.5            # V/ms and ms
vr = solve_ivp(lambda x, yy: [(k * x - yy[0]) / tau4], (0, 10), [0.0], rtol=1e-11, atol=1e-13, dense_output=True)
v.check("X02.4b", vr.sol(1.0)[0])
v.check("X02.4c", k * 10 - vr.sol(10.0)[0])
v.check("X02.4d", (k * 10 - vr.sol(10.0)[0]) / k)
yy_ = sp.symbols("yy")
v.check("X02.4e", 1 / abs(float(sp.diff(1 - yy_**2, yy_).subs(yy_, 1))))
v.check("X02.4f", solve_ivp(lambda x, q: [1 - q[0] ** 2], (0, 1), [0.0], rtol=1e-12, atol=1e-14).y[0, -1])

# 5 · second-order RLC step response
L5, C5, R5 = 1e-6, 1e-6, 0.5
w05, a5 = 1 / math.sqrt(L5 * C5), R5 / (2 * L5)
z5 = a5 / w05
roots5 = np.roots([L5 * C5, R5 * C5, 1])
wd5 = abs(roots5[0].imag)
v.check("X02.5a", w05)
v.check("X02.5b", -roots5[0].real)
v.check("X02.5c", z5)
v.check("X02.5d", math.sqrt(L5 / C5) / R5)
v.check("X02.5e", wd5)
v.check("X02.5f", a5 / wd5)
st = solve_ivp(lambda x, q: [q[1] / C5, (1 - q[0] - R5 * q[1]) / L5], (0, 8e-6), [0.0, 0.0],
               rtol=1e-11, atol=1e-14, dense_output=True)
res = minimize_scalar(lambda x: -st.sol(x)[0], bounds=(2e-6, 4.5e-6), method="bounded", options={"xatol": 1e-13})
v.check("X02.5g", res.x * 1e6)
v.check("X02.5h", (-res.fun - 1) * 100)
v.check("X02.5i", -res.fun)
v.check("X02.5j", 4 / a5 * 1e6)
v.check("X02.5k", brentq(lambda r: r / (2 * L5) - w05, 0.1, 10))

# 6 · forced response and resonance
y6 = sp.dsolve(sp.Eq(y(t).diff(t, 2) + 4 * y(t), 3 * sp.cos(2 * t)), y(t),
               ics={y(0): 0, y(t).diff(t).subs(t, 0): 0}).rhs
v.assert_true("resonant solution is (3/4) t sin 2t", sp.simplify(y6 - sp.Rational(3, 4) * t * sp.sin(2 * t)) == 0)
v.check("X02.6a", float(y6.subs(t, sp.pi / 4)))
v.check("X02.6b", float(sp.limit(y6 / (t * sp.sin(2 * t)), t, 1)))
p6 = lambda om: (1j * om) ** 2 + 2 * (1j * om) + 5  # noqa: E731
v.check("X02.6c", abs(10 / p6(2)))
v.check("X02.6d", deg(cmath.phase(10 / p6(2))))
pk = minimize_scalar(lambda om: abs(p6(om)), bounds=(0.1, 3), method="bounded", options={"xatol": 1e-12})
v.check("X02.6e", pk.x)
v.check("X02.6f", 10 / pk.fun)
f0, L6, Q6 = 10e6, 1e-6, 50
w06 = 2 * math.pi * f0
C6 = brentq(lambda c: 1 / (2 * math.pi * math.sqrt(L6 * c)) - f0, 1e-12, 1e-9, xtol=1e-20)
R6 = w06 * L6 / Q6
v.check("X02.6g", C6 * 1e12)
v.check("X02.6h", R6)
# half-power band edges of the series RLC current, found numerically
Y6 = lambda f: abs(1 / (R6 + 1j * 2 * math.pi * f * L6 + 1 / (1j * 2 * math.pi * f * C6)))  # noqa: E731
edge = lambda f: Y6(f) - (1 / R6) / math.sqrt(2)  # noqa: E731
v.check("X02.6i", (brentq(edge, f0, 1.1 * f0) - brentq(edge, 0.9 * f0, f0)) / 1e3, rtol=1e-6)
v.check("X02.6j", 2 * L6 / R6 * 1e6)
v.check("X02.6k", 2 * L6 / R6 * f0)

# 7 · Laplace transform
Y7 = (s**2 + 3 * s + 4) / (s * (s + 1) * (s + 2))
y7 = sp.inverse_laplace_transform(Y7, s, t)
v.assert_true("Laplace solution satisfies the ODE",
              sp.simplify(sp.diff(y7, t, 2) + 3 * sp.diff(y7, t) + 2 * y7 - 4) == 0)
v.check("X02.7a", float(y7.subs(t, 1)))
v.check("X02.7b", float(sp.limit(s * Y7, s, sp.oo)))
v.check("X02.7c", float(sp.limit(s * Y7, s, 0)))
poles = np.roots([1, 2, 10])
v.check("X02.7d", poles[0].real)
v.check("X02.7e", abs(poles[0].imag))
v.check("X02.7f", 2 / (2 * math.sqrt(10)))
v.check("X02.7g", abs(poles[0]))
v.check("X02.7h", 10 / 10)
h7 = sp.inverse_laplace_transform(10 / (s**2 + 2 * s + 10), s, t)
v.assert_true("impulse response is (10/3) e^-t sin 3t",
              abs(float(h7.subs(t, 0.7)) - 10 / 3 * math.exp(-0.7) * math.sin(2.1)) < 1e-12)
pulse = solve_ivp(lambda x, q: [(1.0 if x < 2 else 0.0) - q[0]], (0, 3), [0.0], rtol=1e-11, atol=1e-13,
                  max_step=1e-3, dense_output=True)
v.check("X02.7i", pulse.sol(3.0)[0])
v.check("X02.7j", pulse.sol(2.0)[0])

# 8 · vectors and products
a8, b8 = np.array([1, 2, 2, 0.0]), np.array([2, 0, 1, 2.0])
p8 = (a8 @ b8) / (a8 @ a8) * a8
v.check("X02.8a", a8 @ b8)
v.check("X02.8b", np.linalg.norm(a8))
v.check("X02.8c", np.linalg.norm(b8))
v.check("X02.8d", deg(math.acos(a8 @ b8 / (np.linalg.norm(a8) * np.linalg.norm(b8)))))
v.check("X02.8e", p8[0])
v.check("X02.8f", p8[1])
v.check("X02.8g", np.linalg.norm(b8 - p8))
v.assert_true("residual orthogonal to a", abs((b8 - p8) @ a8) < 1e-12)
A8, B8 = np.array([[1, 2], [0, 1]]), np.array([[1, 0], [3, 1]])
v.check("X02.8h", (A8 @ B8)[0, 0])
v.check("X02.8i", (B8 @ A8)[1, 1])
v.assert_true("(AB)^T = B^T A^T", np.array_equal((A8 @ B8).T, B8.T @ A8.T))

# 9 · nodal analysis, LU and reciprocity (stamped from the resistor list)
G = np.zeros((3, 3))
for (j, kk), r in {(0, -1): 1.0, (0, 1): 2.0, (1, -1): 2.0, (1, 2): 1.0, (2, -1): 1.0}.items():
    g = 1 / r                      # mS for r in kOhm
    G[j, j] += g
    if kk >= 0:
        G[kk, kk] += g
        G[j, kk] -= g
        G[kk, j] -= g
Pm, Lm, Um = lu(G)
v.assert_true("no row exchanges were needed", np.allclose(Pm, np.eye(3)))
v.check("X02.9a", Um[1, 1])
v.check("X02.9b", Um[2, 2])
v.check("X02.9c", Lm[2, 1])
v.check("X02.9d", np.linalg.det(G))
v1 = np.linalg.solve(G, [1, 0, 0])
v3 = np.linalg.solve(G, [0, 0, 1])
for key, val in zip(("X02.9e", "X02.9f", "X02.9g"), v1):
    v.check(key, val)
v.check("X02.9h", 1 * v1[0])
pr = v1[0] ** 2 / 1 + (v1[0] - v1[1]) ** 2 / 2 + v1[1] ** 2 / 2 + (v1[1] - v1[2]) ** 2 / 1 + v1[2] ** 2 / 1
v.assert_true("power balance", abs(pr - v1[0]) < 1e-12)
for key, val in zip(("X02.9i", "X02.9j", "X02.9k"), v3):
    v.check(key, val)
Rm = np.linalg.inv(G) * 1e3        # Ohm
v.assert_true("reciprocity: R symmetric", np.allclose(Rm, Rm.T))
v.check("X02.9l", Rm[0, 0])
v.check("X02.9m", Rm[2, 2])
v.check("X02.9n", 2 / 3 * 3000**3)
v.check("X02.9o", 2 * 3000**2)

# 10 · rank, null space and least squares
A10 = sp.Matrix([[1, 2, 1], [2, 4, 3], [3, 6, 4]])
v.check("X02.10a", float(A10.det()))
v.check("X02.10b", A10.rank())
ns = A10.nullspace()
v.assert_true("null space is the line through (-2, 1, 0)", len(ns) == 1 and list(ns[0] / ns[0][1]) == [-2, 1, 0])
xs = sp.symbols("x1:4")
gen = sp.linsolve((A10, sp.Matrix([1, 3, 4])), *xs)
v.assert_true("(0,0,1) + c(-2,1,0) solves Ax = (1,3,4)",
              A10 * sp.Matrix([0 - 2 * 7, 7, 1]) == sp.Matrix([1, 3, 4]) and gen != sp.EmptySet)
v.assert_true("Ax = (1,3,5) is inconsistent", sp.linsolve((A10, sp.Matrix([1, 3, 5])), *xs) == sp.EmptySet)
X10 = np.c_[np.ones(4), np.arange(4.0)]
y10 = np.array([1, 3, 4, 4.0])
coef, ssr, *_ = np.linalg.lstsq(X10, y10, rcond=None)
v.check("X02.10c", coef[0])
v.check("X02.10d", coef[1])
v.check("X02.10e", ssr[0])
v.assert_true("residual orthogonal to columns", np.allclose(X10.T @ (y10 - X10 @ coef), 0))

# 11 · two-state Markov chain
M = np.array([[0.9, 0.2], [0.1, 0.8]])
ev = np.sort(np.linalg.eigvals(M).real)
v.check("X02.11a", ev[0])
xinf = np.linalg.matrix_power(M, 2000) @ np.array([0, 1.0])
v.check("X02.11b", xinf[0])
v.check("X02.11c", xinf @ np.array([10, 0.1]))
v.check("X02.11d", (np.linalg.matrix_power(M, 5) @ np.array([0, 1.0]))[0])
kk = next(n for n in range(1, 200) if abs((np.linalg.matrix_power(M, n) @ [0, 1.0])[0] - xinf[0]) <= 0.01)
v.check("X02.11e", kk)
M2 = np.array([[0.7, 0.2], [0.3, 0.8]])
x2inf = np.linalg.matrix_power(M2, 2000) @ np.array([0, 1.0])
v.check("X02.11f", x2inf[0])
v.check("X02.11g", x2inf @ np.array([10, 0.1]))
v.check("X02.11h", np.sort(np.linalg.eigvals(M2).real)[0])

# 12 · symmetric matrices and SVD
K12 = np.array([[2, -1], [-1, 2.0]])
lk = np.linalg.eigvalsh(K12)
v.check("X02.12a", lk[0])
v.check("X02.12b", lk[1])
v.check("X02.12c", lu(K12)[2][1, 1])
H = np.array([[3, 0], [4, 5.0]])
U12, sv, Vt12 = np.linalg.svd(H)
v.check("X02.12d", sv[0])
v.check("X02.12e", sv[1])
v.check("X02.12f", np.linalg.cond(H))
v.check("X02.12g", 10 * math.log10(sv[0] ** 2))
v.check("X02.12h", 10 * math.log10(sv[1] ** 2))
v.assert_true("u1 = (1, 3)/sqrt(10) up to sign", np.allclose(abs(U12[:, 0]), np.array([1, 3]) / math.sqrt(10)))
v.assert_true("rank-1 error equals sigma2",
              abs(np.linalg.norm(H - sv[0] * np.outer(U12[:, 0], Vt12[0]), 2) - sv[1]) < 1e-12)

# 13 · state space (built from R, L, C; time in microseconds)
R13, L13, C13 = 4.0, 1e-6, 1e-6 / 3
A13 = np.array([[0, 1 / C13], [-1 / L13, -R13 / L13]]) * 1e-6
B13 = np.array([0, 1 / L13]) * 1e-6
v.assert_true("A = [[0, 3], [-1, -4]] per us", np.allclose(A13, [[0, 3], [-1, -4]]))
v.check("X02.13a", np.trace(A13))
v.check("X02.13b", np.linalg.det(A13))
x0 = np.array([1.0, 0.0])
x1 = expm(A13 * 1.0) @ x0
v.check("X02.13c", x1[0])
v.check("X02.13d", x1[1])
mn = minimize_scalar(lambda x: (expm(A13 * x) @ x0)[1], bounds=(0.1, 3), method="bounded", options={"xatol": 1e-12})
v.check("X02.13e", mn.x)
v.check("X02.13f", mn.fun)
Cc = np.array([1.0, 0.0])
v.check("X02.13g", Cc @ np.linalg.solve(-A13, B13))
zd = np.sort(np.linalg.eigvals(expm(A13 * 0.1)).real)
v.check("X02.13h", zd[1])
v.check("X02.13i", zd[0])
lam13 = np.linalg.eigvals(A13).real
v.check("X02.13j", min(2 / abs(lam13)))

# 14 · numerical methods
v.check("X02.14a", 1.0 - float(np.nextafter(np.float32(1), np.float32(0))))
v.check("X02.14b", (1.0 - float(np.nextafter(np.float32(1), np.float32(0)))) / 2)
xx = sp.Rational(1, 10**4)
v.check("X02.14c", float(sp.N(1 - sp.cos(xx), 30)), rtol=1e-4)
v.assert_true("float32 1 - cos(1e-4) is exactly 0", float(np.float32(1) - np.cos(np.float32(1e-4))) == 0.0)
v.assert_true("float32 2 sin^2(x/2) is accurate",
              abs(float(2 * np.sin(np.float32(5e-5)) ** 2) / float(1 - sp.cos(xx)) - 1) < 1e-6)
from scipy.optimize import brentq as _bq14  # noqa: E402
f14 = lambda x_: x_**3 - 2 * x_ - 5  # noqa: E731
fp14 = lambda x_: 3 * x_**2 - 2  # noqa: E731
r14 = _bq14(f14, 2, 3, xtol=1e-15)
xs14 = [2.0]
for _ in range(3):
    xs14.append(xs14[-1] - f14(xs14[-1]) / fp14(xs14[-1]))
e = [x - r14 for x in xs14]
v.check("X02.14w", r14)
v.check("X02.14d", xs14[2])
v.check("X02.14e", xs14[3])
v.check("X02.14f", e[1])
v.check("X02.14g", e[2])
v.check("X02.14h", e[3])
v.check("X02.14i", e[2] / e[1] ** 2)
v.check("X02.14j", e[3] / e[2] ** 2)
v.check("X02.14k", 6 * r14 / (2 * fp14(r14)))
v.check("X02.14u", e[0])
v.check("X02.14v", e[1] / e[0] ** 2)
v.check("X02.14l", math.ceil(math.log2(0.5 / 1e-8)))
order = math.log2(3.2e-5 / 2.0e-6)
v.check("X02.14m", order)
v.check("X02.14n", 2.0e-6 / 2**order)
hmax = 2 / 1000
v.check("X02.14o", hmax * 1e3)
v.check("X02.14p", 5 / hmax)
h14 = 10e-3
v.check("X02.14q", 1 / (1 - h14 * -1000))
v.check("X02.14r", (1 + h14 * -1000 / 2) / (1 - h14 * -1000 / 2))
v.check("X02.14s", 1 / (1 + h14))
v.check("X02.14t", (1 - h14 / 2) / (1 + h14 / 2))
v.assert_true("trapezoidal slow factor matches exp(-0.01) to 6 digits", abs((1 - h14 / 2) / (1 + h14 / 2) - math.exp(-0.01)) < 1e-6)

# 15 · conditioning
K15 = np.array([[2, 1], [1, 0.5005]])
kap = np.linalg.cond(K15)
v.check("X02.15a", kap)
v.check("X02.15b", kap * 2.0**-11)
v.check("X02.15c", kap * 2.0**-24)
v.check("X02.15d", kap * 2.0**-53)
_l15 = np.linalg.eigvalsh(K15)
v.check("X02.15e", _l15[1]); v.check("X02.15f", _l15[0])

sys.exit(v.finish())
