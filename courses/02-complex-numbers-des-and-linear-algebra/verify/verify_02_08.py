#!/usr/bin/env python3
"""Verify every published number in chapter 02-08, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-08",
    COURSE / "chapters" / "02-08-eigenvalues-and-eigenvectors.md",
    COURSE / "solutions" / "02-08-solutions.md",
    COURSE / "labs" / "02-08-lab" / "README.md",
)
M = sp.Matrix
lam = sp.Symbol("lambda")
rng = np.random.default_rng(3)


def f(x):
    return float(x)


def mode_freqs(L, C, Cc):
    caps = np.linalg.eigvalsh(np.array([[C + Cc, -Cc], [-Cc, C + Cc]]))
    return np.sort(1 / (2 * np.pi * np.sqrt(L * caps)))[::-1]   # in-phase (higher) first


# ---------------------------------------------------------------- theory identities
a, b, c, d = sp.symbols("a b c d")
v.assert_true("2x2 characteristic polynomial = lambda^2 - tr lambda + det",
              sp.expand((M([[a, b], [c, d]]) - lam * sp.eye(2)).det() - (lam**2 - (a + d) * lam + (a * d - b * c))) == 0)
R4 = rng.standard_normal((4, 4))
w4 = np.linalg.eigvals(R4)
v.assert_true("sum of eigenvalues = trace, product = det", np.isclose(w4.sum(), np.trace(R4)) and np.isclose(w4.prod(), np.linalg.det(R4)))
v.assert_true("A and A^T share eigenvalues", np.allclose(np.sort_complex(w4), np.sort_complex(np.linalg.eigvals(R4.T))))
S4 = R4 + R4.T
ws, Qs = np.linalg.eigh(S4)
v.assert_true("spectral theorem: real eigenvalues, Q^T Q = I, S = Q L Q^T",
              np.allclose(Qs.T @ Qs, np.eye(4)) and np.allclose(Qs @ np.diag(ws) @ Qs.T, S4))
U4, s4, Vt4 = np.linalg.svd(R4)
v.assert_true("SVD: singular values^2 = eig(A^T A); prod sigma = |det|; sum sigma^2 = ||A||_F^2",
              np.allclose(np.sort(s4**2), np.sort(np.linalg.eigvalsh(R4.T @ R4)))
              and np.isclose(np.prod(s4), abs(np.linalg.det(R4))) and np.isclose((s4**2).sum(), (R4**2).sum()))
A2r = (U4[:, :2] * s4[:2]) @ Vt4[:2]
v.assert_true("Eckart-Young: rank-2 truncation error equals sigma_3", np.isclose(np.linalg.norm(R4 - A2r, 2), s4[2]))
th_ = sp.Symbol("theta", real=True)
Rth = M([[sp.cos(th_), -sp.sin(th_)], [sp.sin(th_), sp.cos(th_)]])
v.assert_true("rotation eigenvalues e^{+-j theta}",
              set(sp.simplify(e.rewrite(sp.exp)) for e in Rth.eigenvals()) == {sp.exp(sp.I * th_), sp.exp(-sp.I * th_)}
              or all(sp.simplify(sp.Abs(e) - 1) == 0 for e in Rth.eigenvals()))
al, w0 = sp.symbols("alpha omega_0", positive=True)
v.assert_true("companion matrix polynomial = lambda^2 + 2 alpha lambda + w0^2",
              sp.expand((M([[0, 1], [-w0**2, -2 * al]]) - lam * sp.eye(2)).det() - (lam**2 + 2 * al * lam + w0**2)) == 0)
Pr = rng.random((4, 4)); Pr = Pr / Pr.sum(axis=0)
v.assert_true("column-stochastic matrix has eigenvalue 1, none larger", np.isclose(np.max(np.abs(np.linalg.eigvals(Pr))), 1.0)
              and np.any(np.isclose(np.linalg.eigvals(Pr), 1.0)))

# ---------------------------------------------------------------- Example 1
A1 = M([[4, 1], [2, 3]])
ev1 = sorted(A1.eigenvals().keys(), reverse=True)
v.check("Ex 02-08.1a", f(ev1[0])); v.check("Ex 02-08.1b", f(ev1[1]))
X1 = M([[1, 1], [1, -2]])
A5 = X1 * sp.diag(5**5, 2**5) * X1.inv()
v.assert_true("Ex 1: X Lambda^5 X^-1 = A^5", A5 == A1**5)
v.check("Ex 02-08.1c", f(A5[0, 0])); v.check("Ex 02-08.1d", f(A5[0, 1])); v.check("Ex 02-08.1e", f(A5.trace()))

# ---------------------------------------------------------------- Example 2 (Markov chain)
r = sp.Rational
P = M([[r(90, 100), r(10, 100), r(1, 100)], [r(8, 100), r(80, 100), r(1, 100)], [r(2, 100), r(10, 100), r(98, 100)]])
v.assert_true("Ex 2: columns sum to 1", all(sum(P[:, j]) == 1 for j in range(3)))
pi = (P - sp.eye(3)).nullspace()[0]
pi = pi / sum(pi)
v.assert_true("Ex 2: pi = (5/28, 3/28, 5/7)", list(pi) == [r(5, 28), r(3, 28), r(5, 7)])
v.check("Ex 02-08.2a", f(pi[0])); v.check("Ex 02-08.2b", f(pi[1])); v.check("Ex 02-08.2c", f(pi[2]))
Ist = np.array([5.0, 0.5, 0.002])
iavg = float(np.dot(Ist, [f(x) for x in pi]))
v.check("Ex 02-08.2d", iavg)
v.check("Ex 02-08.2e", 100 / iavg)
others = np.roots([1, -(f(P.trace()) - 1), f(P.det())])
v.assert_true("Ex 2: trace/det shortcut matches the full eigenvalues",
              np.allclose(np.sort(others), np.sort(np.linalg.eigvals(np.array(P, dtype=float)))[:2]))
l2, l3 = sorted(others, reverse=True)
v.check("Ex 02-08.2f", l2); v.check("Ex 02-08.2g", l3)
v.check("Ex 02-08.2h", math.log(0.01) / math.log(l2))
v.check("Ex 02-08.2i", 5 * f(pi[0]) / iavg * 100, tol=0.5)

# ---------------------------------------------------------------- Example 3
ev3 = np.linalg.eigvals(np.array([[0, 1], [-1e8, -5000.0]]))
v.check("Ex 02-08.3a", abs(ev3[0].imag))
v.assert_true("Ex 3: real part -2500", np.allclose(ev3.real, -2500))
th = math.radians(30)
R30 = 0.95 * np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
ev3b = np.linalg.eigvals(R30)
v.check("Ex 02-08.3b", ev3b[0].real); v.check("Ex 02-08.3c", abs(ev3b[0].imag))
v.check("Ex 02-08.3d", 360 / math.degrees(abs(np.angle(ev3b[0]))))
v.check("Ex 02-08.3e", np.linalg.norm(np.linalg.matrix_power(R30, 12) @ [1.0, 0.0]))

# ---------------------------------------------------------------- Example 4 (ladder)
K = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2.0]])
wK, QK = np.linalg.eigh(K)
v.check("Ex 02-08.4a", wK[0]); v.check("Ex 02-08.4b", wK[1]); v.check("Ex 02-08.4c", wK[2])
v.assert_true("Ex 4: eigenvalues 2 - sqrt2, 2, 2 + sqrt2", np.allclose(wK, [2 - math.sqrt(2), 2, 2 + math.sqrt(2)]))
q = [np.array([1, math.sqrt(2), 1]) / 2, np.array([1, 0, -1]) / math.sqrt(2), np.array([1, -math.sqrt(2), 1]) / 2]
v.assert_true("Ex 4: stated eigenvectors are orthonormal eigenvectors",
              all(np.allclose(K @ qi, li * qi) for qi, li in zip(q, wK)) and np.allclose(np.array(q) @ np.array(q).T, np.eye(3)))
Kinv11 = sum(qi[0] ** 2 / li for qi, li in zip(q, wK))
v.check("Ex 02-08.4d", Kinv11)
v.assert_true("Ex 4: equals (K^-1)_11 from 02-07", np.isclose(Kinv11, np.linalg.inv(K)[0, 0]))
v.check("Ex 02-08.4e", wK[2] / wK[0])

# ---------------------------------------------------------------- Example 5 (coupled resonators)
f5s, f5a = mode_freqs(1e-6, 1e-9, 0.1e-9)
v.check("Ex 02-08.5a", f5s / 1e6); v.check("Ex 02-08.5b", f5a / 1e6)
v.check("Ex 02-08.5c", (f5s - f5a) / 1e3)
v.check("Ex 02-08.5d", f5s / f5a)
v.check("Ex 02-08.5e", 1 / (2 * (f5s - f5a)) * 1e6)
v.assert_true("Ex 5: in-phase frequency equals the uncoupled 1/(2 pi sqrt(LC))",
              np.isclose(f5s, 1 / (2 * math.pi * math.sqrt(1e-15))))

# ---------------------------------------------------------------- Example 6 (SVD)
H = np.array([[2, 2], [-1, 1.0]])
U6, s6, Vt6 = np.linalg.svd(H)
v.check("Ex 02-08.6a", s6[0]); v.check("Ex 02-08.6b", s6[1])
H1 = s6[0] * np.outer(U6[:, 0], Vt6[0])
v.assert_true("Ex 6: rank-1 approximation is [[2, 2], [0, 0]]", np.allclose(H1, [[2, 2], [0, 0]]))
v.check("Ex 02-08.6c", np.linalg.norm(H - H1, 2))
v.check("Ex 02-08.6d", s6[0] / s6[1])
v.check("Ex 02-08.6e", 10 * math.log10(s6[0] ** 2 / s6[1] ** 2))
v.assert_true("Ex 6: prod sigma = |det H| = 4", np.isclose(s6.prod(), 4))

# ---------------------------------------------------------------- numbers to know
v.check("N 02-08.a", math.log(0.01) / math.log(0.9))
for key, val in {"N 02-08.b": 2, "N 02-08.c": 4, "N 02-08.d": 0.85}.items():   # sourced constants (R-045, R-047)
    v.check(key, val)

# ---------------------------------------------------------------- Problems 1-6
e1 = M([[5, 2], [2, 2]]).eigenvects()
vals1 = sorted([e[0] for e in e1], reverse=True)
v.check("02-08.1a", f(vals1[0])); v.check("02-08.1b", f(vals1[1]))
vecs = [e[2][0] for e in e1]
v.check("02-08.1c", f(vecs[0].dot(vecs[1])))
T2 = M([[3, 1, 4], [0, -1, 5], [0, 0, 2]])
v.check("02-08.2a", f(T2.trace())); v.check("02-08.2b", f(T2.det()))
v.check("02-08.2c", f(max((T2 + 2 * sp.eye(3)).eigenvals().keys())))
Pp = M([[1, 1], [1, 1]]) / 2
v.check("02-08.3a", f(max(Pp.eigenvals()))); v.check("02-08.3b", f(min(Pp.eigenvals())))
v.check("02-08.3c", f(min(M([[0, 1], [1, 0]]).eigenvals())))
v.check("02-08.3d", f(max(sp.im(e) for e in M([[0, -1], [1, 0]]).eigenvals())))
A4p = M([[1, 1], [0, 1]]) * sp.diag(2, 3) * M([[1, 1], [0, 1]]).inv()
v.check("02-08.4a", f(A4p[0, 1])); v.check("02-08.4b", f(A4p[1, 1]))
A5p = M([[2, 0, 0], [1, 3, 1], [1, 1, 3]])
ev5 = A5p.eigenvects()
mult = {e[0]: (e[1], len(e[2])) for e in ev5}
v.assert_true("P5: eigenvalue 2 has algebraic and geometric multiplicity 2", mult[2] == (2, 2) and mult[4] == (1, 1))
v.check("02-08.5a", 2); v.check("02-08.5b", 4); v.check("02-08.5c", mult[2][1])
v.check("02-08.5d", f(A5p.trace())); v.check("02-08.5e", f(A5p.det()))
A6p = M([[3, 1], [0, 3]])
v.assert_true("P6: one independent eigenvector", len(A6p.eigenvects()[0][2]) == 1)
v.check("02-08.6a", f((A6p**4)[0, 1]))
v.assert_true("P6: (A^k)_12 = k 3^(k-1) for k = 1..8", all((A6p**k)[0, 1] == k * 3 ** (k - 1) for k in range(1, 9)))

# ---------------------------------------------------------------- Problems 7-12
P7 = M([[r(1, 2), r(1, 4)], [r(1, 2), r(3, 4)]])
v.check("02-08.7a", f(min(P7.eigenvals())))
pi7 = (P7 - sp.eye(2)).nullspace()[0]; pi7 = pi7 / sum(pi7)
v.check("02-08.7b", f(pi7[0]))
u10 = P7**10 * M([1, 0])
v.check("02-08.7c", f(u10[0] - pi7[0]))
v.assert_true("P7: closed form", u10 == M(pi7) + r(2, 3) * r(1, 4) ** 10 * M([1, -1]))
A8 = np.array([[1.2, -0.8], [1, 0.0]])
ev8 = np.linalg.eigvals(A8)
v.check("02-08.8a", abs(ev8[0].imag)); v.check("02-08.8b", abs(ev8[0]))
ang8 = math.degrees(abs(np.angle(ev8[0])))
v.check("02-08.8c", ang8); v.check("02-08.8d", 360 / ang8)
S9 = np.array([[2, 1], [1, 2.0]])
w9 = np.linalg.eigvalsh(S9)
v.check("02-08.9a", w9[1]); v.check("02-08.9b", w9[0])
v.check("02-08.9c", 1 / math.sqrt(w9[1])); v.check("02-08.9d", 1 / math.sqrt(w9[0]))
bb = sp.Symbol("b", real=True)
v.check("02-08.10a", f(sp.solve(M([[2, -1], [-1, bb]]).det(), bb)[0]))
w10 = sorted(M([[1, 2], [2, 1]]).eigenvals().keys())
v.check("02-08.10b", f(w10[1])); v.check("02-08.10c", f(w10[0]))
xv = M([1, -1])
v.check("02-08.10d", f((xv.T * M([[1, 2], [2, 1]]) * xv)[0]))
x_, y_ = sp.symbols("x y")
fxy = x_**2 + x_ * y_ + y_**2 - 3 * x_
sol = sp.solve([sp.diff(fxy, x_), sp.diff(fxy, y_)], [x_, y_])
v.check("02-08.11a", f(sol[x_])); v.check("02-08.11b", f(sol[y_])); v.check("02-08.11c", f(fxy.subs(sol)))
v.assert_true("P11: Hessian positive definite", all(e > 0 for e in sp.hessian(fxy, (x_, y_)).eigenvals()))
s12 = np.linalg.svd(np.ones((2, 2)), compute_uv=False)
v.check("02-08.12a", s12[0]); v.check("02-08.12b", np.linalg.matrix_rank(np.ones((2, 2))))
s12b = np.linalg.svd(np.diag([3.0, -2.0]), compute_uv=False)
v.check("02-08.12c", s12b[0]); v.check("02-08.12d", s12b[1]); v.check("02-08.12e", s12b[0] / s12b[1])
Qr, _ = np.linalg.qr(rng.standard_normal((5, 5)))
v.check("02-08.12f", float(np.max(np.abs(np.linalg.svd(Qr, compute_uv=False)))))
v.assert_true("P12: all singular values of an orthogonal matrix are 1", np.allclose(np.linalg.svd(Qr, compute_uv=False), 1))

# ---------------------------------------------------------------- Problems 13-15
f13s, f13a = mode_freqs(4.7e-6, 220e-12, 22e-12)
v.check("02-08.13a", f13s / 1e6); v.check("02-08.13b", f13a / 1e6)
v.check("02-08.13c", (f13s - f13a) / 1e3); v.check("02-08.13d", 1 / (2 * (f13s - f13a)) * 1e6)
v.check("02-08.13e", f13s / f13a - 1)
A14 = np.array([[2, 4], [1, 2.1], [3, 5.9]])
s14 = np.linalg.svd(A14, compute_uv=False)
v.check("02-08.14a", s14[0]); v.check("02-08.14b", s14[1])
v.check("02-08.14c", s14[0] ** 2 / (s14**2).sum() * 100)
v.assert_true("P14: A^T A = [[14, 27.8], [27.8, 55.22]]", np.allclose(A14.T @ A14, [[14, 27.8], [27.8, 55.22]]))
Cv = np.array([[4, 2.4], [2.4, 4.0]])
w15, Q15 = np.linalg.eigh(Cv)
v.check("02-08.15a", w15[1]); v.check("02-08.15b", w15[0])
v.check("02-08.15c", w15[1] / w15.sum() * 100)
v.check("02-08.15d", math.sqrt(w15[1])); v.check("02-08.15e", math.sqrt(w15[0]))
q2 = np.array([1, -1]) / math.sqrt(2)
sig_proj = q2 @ np.array([1.0, -1.0])                 # signal (s, -s) with s = 1
noise_sd = math.sqrt(q2 @ Cv @ q2)
gain = (sig_proj / noise_sd) / (1 / 2.0)
v.check("02-08.15f", gain)
gain_unc = (sig_proj / math.sqrt(q2 @ (4 * np.eye(2)) @ q2)) / (1 / 2.0)
v.check("02-08.15g", gain_unc)
v.check("02-08.15h", gain / gain_unc)

# ---------------------------------------------------------------- lab handout
Pf = np.array(P, dtype=float)
pif = np.array([f(x) for x in pi])
u = np.array([1.0, 0, 0]); first = None
for k in range(1, 400):
    u = Pf @ u
    if np.max(np.abs(u - pif)) < 0.01:
        first = k
        break
v.check("Lab 02-08.a", first)
R102 = 1.02 * np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
v.check("Lab 02-08.b", np.linalg.norm(np.linalg.matrix_power(R102, 12) @ [1.0, 0.0]))
n20 = 20
K20 = 2 * np.eye(n20) - np.eye(n20, k=1) - np.eye(n20, k=-1)
w20 = np.linalg.eigvalsh(K20)
v.check("Lab 02-08.c", w20[0]); v.check("Lab 02-08.d", w20[-1])
v.assert_true("Lab: ladder eigenvalues 2 - 2cos(k pi/21)",
              np.allclose(w20, [2 - 2 * math.cos(k * math.pi / 21) for k in range(1, 21)]))
xs = np.linspace(0, 1, 80); ys = np.linspace(0, 1, 60)
img = (np.outer(np.sin(np.pi * ys), np.sin(np.pi * xs)) + 0.5 * np.outer(np.cos(3 * ys), xs**2)
       + 0.25 * np.outer(ys, np.cos(5 * xs)))
v.check("Lab 02-08.e", np.linalg.matrix_rank(img))

v.finish()
