#!/usr/bin/env python3
"""Verify chapter 15-10 (state-space introduction): examples, problems and lab answers.

Routes:
- eigenvalues, ranks and singular values with numpy;
- feedback and observer gains from Ackermann's formula (labs/15-10-lab/statespace.py), each checked by the
  eigenvalues it produces and, for canonical forms, by coefficient matching done independently with sympy;
- free and forced responses by the matrix exponential, cross-checked with closed forms and solve_ivp;
- closed-loop step specifications with labs/15-03-lab/specs.py; the servo is confirmed in ngspice.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
for lab in ("15-10-lab", "15-03-lab"):
    sys.path.insert(0, str(ROOT / "labs" / lab))
from eeverify import Verifier  # noqa: E402
import statespace as ss  # noqa: E402
from specs import step_specs  # noqa: E402

CH = ROOT / "chapters" / "15-10-state-space-introduction.md"
v = Verifier.from_files("15-10", CH, ROOT / "solutions" / "15-10-solutions.md", ROOT / "labs" / "15-10-lab" / "README.md")


def eig_sorted(M):
    return np.sort_complex(np.linalg.eigvals(np.asarray(M, float)))


def coeff_match(Asym, Bsym, desired):
    """Solve for k (sympy) so that det(sI - (A - B k)) equals the desired polynomial."""
    s = sp.symbols("s")
    n = Asym.shape[0]
    ks = sp.symbols(f"k1:{n + 1}")
    K = sp.Matrix([ks])
    charp = sp.Poly((s * sp.eye(n) - (Asym - Bsym * K)).det(), s).all_coeffs()
    target = sp.Poly(sp.expand(desired(s)), s).all_coeffs()
    return [float(x) for x in sp.solve([sp.Eq(a, b) for a, b in zip(charp[1:], target[1:])], ks, dict=True)[0].values()]


# ---------------------------------------------------------------------------------------- Example 1
R, Lm, Km, J, Bf = 2.0, 1e-3, 0.05, 2e-5, 1e-5
A1 = np.array([[-R / Lm, -Km / Lm], [Km / J, -Bf / J]])
B1 = np.array([[1 / Lm], [0.0]])
ev = np.sort(np.linalg.eigvals(A1).real)
v.check("Ex 15-10.1a", ev[1])
v.check("Ex 15-10.1b", ev[0])
v.check("Ex 15-10.1c", np.linalg.det(ss.ctrb(A1, B1)))
Ac = np.array([[0, 1], [-126000.0, -2000.5]])
v.assert_true("Ex 1: canonical form has the same eigenvalues", np.allclose(eig_sorted(Ac), eig_sorted(A1)))
num, den = ss.tf_of(A1, B1, [[0, 1]])
v.assert_true("Ex 1: transfer function 2.5e6/(s^2 + 2000.5 s + 126000)",
              np.allclose(den, [1, 2000.5, 126000]) and abs(num[-1] - 2.5e6) < 1e-3)

# ---------------------------------------------------------------------------------------- Example 2
A2 = np.array([[0.0, 1.0], [-2.0, -3.0]])
x1 = expm(A2 * 1.0) @ np.array([1.0, 0.0])
v.check("Ex 15-10.2a", x1[0])
v.check("Ex 15-10.2b", x1[1])
v.assert_true("Ex 2: closed form 2e^-t - e^-2t", abs(x1[0] - (2 * math.exp(-1) - math.exp(-2))) < 1e-12)
sol = solve_ivp(lambda t, x: A2 @ x, (0, 1), [1, 0], rtol=1e-12, atol=1e-14)
v.assert_true("Ex 2: solve_ivp agrees", np.allclose(sol.y[:, -1], x1, atol=1e-9))

# ---------------------------------------------------------------------------------------- Example 3
A3 = np.array([[0.0, 1.0], [0.0, -1.0]])
B3 = np.array([[0.0], [1.0]])
C3 = np.array([[1.0, 0.0]])
p3 = [complex(-2, 2 * math.sqrt(3)), complex(-2, -2 * math.sqrt(3))]
K3 = ss.acker(A3, B3, p3)
v.check("Ex 15-10.3a", K3[0, 0])
v.check("Ex 15-10.3b", K3[0, 1])
v.assert_true("Ex 3: sympy coefficient matching gives the same K",
              np.allclose(coeff_match(sp.Matrix(A3), sp.Matrix(B3), lambda s: s**2 + 4 * s + 16), K3.ravel()))
Acl3 = A3 - B3 @ K3
N3 = -1 / (C3 @ np.linalg.solve(Acl3, B3))[0, 0]
v.check("Ex 15-10.3c", N3)
s3 = step_specs([N3], np.real(np.poly(np.linalg.eigvals(Acl3))), 5)
v.check("Ex 15-10.3f", 100 * s3["overshoot"])
v.check("Ex 15-10.3g", s3["tpeak"])

# ---------------------------------------------------------------------------------------- Example 4
A4 = -1000 * np.eye(2)
B4 = 1000 * np.array([[1.0], [1.0]])
v.check("Ex 15-10.4a", np.linalg.matrix_rank(ss.ctrb(A4, B4)))
# the difference mode: d/dt (v1 - v2) = -1000 (v1 - v2) for any input
dvec = np.array([1.0, -1.0])
v.assert_true("Ex 4: the input has no component along the difference mode", abs(dvec @ B4.ravel()) < 1e-12)
v.check("Ex 15-10.4b", float(dvec @ A4 @ dvec / (dvec @ dvec)))

# ---------------------------------------------------------------------------------------- Example 5
L5 = ss.observer_gain(A3, C3, [-10, -10])
v.check("Ex 15-10.5a", L5[0, 0])
v.check("Ex 15-10.5b", L5[1, 0])
Aclo = np.block([[A3, -B3 @ K3], [L5 @ C3, A3 - B3 @ K3 - L5 @ C3]])
Bclo = np.vstack([B3 * N3, B3 * N3])
Cclo = np.hstack([C3, np.zeros((1, 2))])
v.assert_true("Ex 5: separation (eigenvalues are the union)",
              np.allclose(eig_sorted(Aclo), np.sort_complex(np.concatenate([p3, [-10, -10]])), atol=1e-5))
t = np.linspace(0, 3, 30001)
y, xs = ss.closed_loop_response(Aclo, Bclo, Cclo, [0, 0, 0.5, 0], t, r=0.0)
e = xs[:, 0] - xs[:, 2]
v.check("Ex 15-10.5c", abs(e[np.searchsorted(t, 0.5)]))
k = int(np.argmax(np.abs(y)))
v.check("Ex 15-10.5d", abs(y[k]))
from scipy.optimize import brentq  # noqa: E402
dydt = lambda tt: float((Cclo @ (Aclo @ ss.closed_loop_response(Aclo, Bclo, Cclo, [0, 0, 0.5, 0], [tt], r=0.0)[1][0]))[0])  # noqa: E731
v.check("Ex 15-10.5e", brentq(dydt, t[k - 1], t[k + 1], xtol=1e-12))
yr, _ = ss.closed_loop_response(Aclo, Bclo, Cclo, [0, 0, 0, 0], t[::100], r=1.0)
from scipy import signal  # noqa: E402
_, yref = signal.step(([16.0], [1, 4, 16]), T=t[::100])
v.assert_true("Ex 5: reference response identical to full-state feedback", np.max(np.abs(yr - yref)) < 1e-9)

# ---------------------------------------------------------------------------------------- Example 6
At, Bt, Ct = np.array([[-0.1]]), np.array([[0.05]]), np.array([[1.0]])
Aa, Ba, Br = ss.augment_integral(At, Bt, Ct)
Ka = ss.acker(Aa, Ba, [complex(-0.4, 0.3), complex(-0.4, -0.3)])
v.check("Ex 15-10.6a", Ka[0, 0])
v.assert_true("Ex 6: integral gain is 5 (u = -14 x + 5 xi)", abs(Ka[0, 1] + 5) < 1e-9)
t = np.linspace(0, 40, 4001)
y6, _ = ss.closed_loop_response(Aa - Ba @ Ka, Br, np.array([[1.0, 0.0]]), [0, 0], t, r=1.0)
v.check("Ex 15-10.6b", 100 * step_specs([0.05 * 5], [1, 0.1 + 0.05 * 14, 0.05 * 5], 40)["overshoot"])
v.assert_true("Ex 6: matrix-exponential response matches", abs(100 * (y6.max() - 1) - 1.5165) < 2e-3)
Bd = np.vstack([Bt, [[0.0]]])
y6d, _ = ss.closed_loop_response(Aa - Ba @ Ka, Bd, np.array([[1.0, 0.0]]), [0, 0], t, r=20.0)
k = int(np.argmax(y6d))
f6 = lambda tt: float((np.array([[1.0, 0.0]]) @ ((Aa - Ba @ Ka) @ ss.closed_loop_response(Aa - Ba @ Ka, Bd, np.array([[1.0, 0.0]]), [0, 0], [tt], r=20.0)[1][0] + Bd.ravel() * 20))[0])  # noqa: E731
tp6 = brentq(f6, t[k - 1], t[k + 1], xtol=1e-12)
v.check("Ex 15-10.6c", ss.closed_loop_response(Aa - Ba @ Ka, Bd, np.array([[1.0, 0.0]]), [0, 0], [tp6], r=20.0)[0][0])
v.check("Ex 15-10.6d", tp6)

# ---------------------------------------------------------------------------------------- Problem 1
ev1 = np.sort(np.linalg.eigvals(A2).real)
v.check("15-10.1a", ev1[1])
v.check("15-10.1b", ev1[0])

# ---------------------------------------------------------------------------------------- Problems 2 and 3
Ad = np.diag([-1.0, -2.0])
v.check("15-10.2a", np.linalg.matrix_rank(ss.ctrb(Ad, [[1], [0]])))
# the uncontrollable eigenvalue: eigenvalue of A whose left eigenvector w satisfies w B = 0 (PBH test)
wl, Vl = np.linalg.eig(Ad.T)
v.check("15-10.2b", float(wl[np.argmin([abs(Vl[:, i] @ np.array([1.0, 0.0])) for i in range(2)])].real))
v.assert_true("P2: the input never reaches x2", np.allclose(ss.ctrb(Ad, [[1], [0]])[1], 0))
v.check("15-10.2c", np.linalg.matrix_rank(ss.ctrb(Ad, [[1], [1]])))
v.check("15-10.3a", np.linalg.matrix_rank(ss.obsv(Ad, [[1, 0]])))
v.check("15-10.3b", np.linalg.matrix_rank(ss.obsv(Ad, [[1, 1]])))

# ---------------------------------------------------------------------------------------- Problem 4
A4p = np.array([[0.0, 1.0], [0.0, -2.0]])
K4 = ss.acker(A4p, B3, [complex(-4, 4), complex(-4, -4)])
v.check("15-10.4a", K4[0, 0])
v.check("15-10.4b", K4[0, 1])
Acl4 = A4p - B3 @ K4
N4 = -1 / (C3 @ np.linalg.solve(Acl4, B3))[0, 0]
v.check("15-10.4c", N4)
v.check("15-10.4d", 100 * step_specs([N4], np.real(np.poly(np.linalg.eigvals(Acl4))), 5)["overshoot"])

# ---------------------------------------------------------------------------------------- Problem 5
A5 = np.array([[-1.0, 1.0], [0.0, -2.0]])
K5 = ss.acker(A5, B3, [-3, -4])
v.check("15-10.5a", K5[0, 0])
v.check("15-10.5b", K5[0, 1])
v.assert_true("P5: eigenvalues -3, -4", np.allclose(np.sort(np.linalg.eigvals(A5 - B3 @ K5).real), [-4, -3]))
v.assert_true("P5: sympy coefficient matching agrees",
              np.allclose(coeff_match(sp.Matrix(A5), sp.Matrix(B3), lambda s: (s + 3) * (s + 4)), K5.ravel()))

# ---------------------------------------------------------------------------------------- Problem 6
L6 = ss.observer_gain(A4p, C3, [-20, -20])
v.check("15-10.6a", L6[0, 0])
v.check("15-10.6b", L6[1, 0])

# ---------------------------------------------------------------------------------------- Problem 7
Adi = np.array([[0.0, 1.0], [0.0, 0.0]])
xf = expm(Adi * 2) @ np.array([0.0, 1.0])
v.check("15-10.7a", xf[0])
v.check("15-10.7b", xf[1])
M = np.zeros((3, 3))
M[:2, :2] = Adi
M[:2, 2] = [0, 1]
z = expm(M * 2) @ np.array([0.0, 1.0, 1.0])
v.check("15-10.7c", z[0])
v.check("15-10.7d", z[1])

# ---------------------------------------------------------------------------------------- Problem 8
for tau2, keys in ((1.1, "abc"), (1.01, "fde")):
    A8 = np.diag([-1.0, -1 / tau2])
    B8 = np.array([[1.0], [1 / tau2]])
    sv = np.linalg.svd(ss.ctrb(A8, B8), compute_uv=False)
    v.check(f"15-10.8{keys[0]}", sv[0])
    v.check(f"15-10.8{keys[1]}", sv[1])
    v.check(f"15-10.8{keys[2]}", sv[0] / sv[1])

# ---------------------------------------------------------------------------------------- Problem 9
Aa9, Ba9, Br9 = ss.augment_integral([[-40.0]], [[2000.0]], [[1.0]])
K9 = ss.acker(Aa9, Ba9, [complex(-100, 100), complex(-100, -100)])
v.check("15-10.9a", K9[0, 0])
v.check("15-10.9b", -K9[0, 1])
v.check("15-10.9c", 100 * step_specs([2000 * 10], [1, 40 + 2000 * 0.08, 2000 * 10], 0.2)["overshoot"])

# ---------------------------------------------------------------------------------------- Problem 10
Acl10 = np.block([[A4p, -B3 @ K4], [L6 @ C3, A4p - B3 @ K4 - L6 @ C3]])
ev10 = np.linalg.eigvals(Acl10)
v.check("15-10.10a", complex(ev10[np.argmax(ev10.imag)]))
v.check("15-10.10b", float(np.mean(ev10[np.abs(ev10.imag) < 1e-3].real)))

# ---------------------------------------------------------------------------------------- Problem 11
T = np.array([[1.0, 1.0], [0.0, 1.0]])
A11 = np.linalg.inv(T) @ A2 @ T
v.assert_true("P11: T^-1 A T = [[2, 6], [-2, -5]]", np.allclose(A11, [[2, 6], [-2, -5]]))
n11, d11 = ss.tf_of(A11, np.linalg.inv(T) @ np.array([[0.0], [1.0]]), np.array([[1.0, 0.0]]) @ T)
v.assert_true("P11: transfer function unchanged", np.allclose(d11, [1, 3, 2]) and abs(n11[-1] - 1) < 1e-12)

# ---------------------------------------------------------------------------------------- Problem 12
v.check("15-10.12a", 2)
v.check("15-10.12b", 4)

# ---------------------------------------------------------------------------------------- Lab
w, V = np.linalg.eig(A2)
order = np.argsort(-w.real)
slopes = (V[1] / V[0]).real[order]
v.check("Lab 15-10.a", slopes[0])
v.check("Lab 15-10.b", slopes[1])

sys.exit(v.finish())
