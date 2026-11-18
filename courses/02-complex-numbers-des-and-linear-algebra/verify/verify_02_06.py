#!/usr/bin/env python3
"""Verify every published number in chapter 02-06, its solutions and its lab handout."""
from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import scipy.linalg as sl
import scipy.sparse as sps
import scipy.sparse.linalg as spl
import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "02-06",
    COURSE / "chapters" / "02-06-vectors-matrices-and-linear-systems.md",
    COURSE / "solutions" / "02-06-solutions.md",
    COURSE / "labs" / "02-06-lab" / "README.md",
)


def deg(x):
    return math.degrees(x)


def angle(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return deg(math.acos(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))))


def eliminate(A, b):
    """Exact (Fraction) elimination without row exchanges; returns multipliers, U, c and x."""
    A = [[Fr(x) for x in row] for row in A]
    b = [Fr(x) for x in b]
    n = len(b)
    mult = {}
    for k in range(n - 1):
        for i in range(k + 1, n):
            m = A[i][k] / A[k][k]
            mult[(i + 1, k + 1)] = m
            A[i] = [A[i][j] - m * A[k][j] for j in range(n)]
            b[i] -= m * b[k]
    x = [Fr(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return mult, A, b, x


def solve2_float(a11, a12, a21, a22, b1, b2):
    """2x2 elimination without row exchanges in IEEE double precision (as in Example 02-06.4)."""
    m = a21 / a11
    u22 = a22 - m * a12
    c2 = b2 - m * b1
    x2 = c2 / u22
    return m, (b1 - a12 * x2) / a11, x2


# ---------------------------------------------------------------- theory identities
us, vs, ts = sp.symbols("u1:4"), sp.symbols("v1:4"), sp.Symbol("t", real=True)
U3, V3 = sp.Matrix(us), sp.Matrix(vs)
q = ((U3 - ts * V3).T * (U3 - ts * V3))[0]
disc = sp.discriminant(sp.expand(q), ts)
v.assert_true("Cauchy-Schwarz: discriminant = 4[(u.v)^2 - |u|^2|v|^2]",
              sp.simplify(disc - 4 * ((U3.T * V3)[0] ** 2 - (U3.T * U3)[0] * (V3.T * V3)[0])) == 0)
v.assert_true("|u - v|^2 = |u|^2 - 2u.v + |v|^2",
              sp.expand(((U3 - V3).T * (U3 - V3))[0] - ((U3.T * U3)[0] - 2 * (U3.T * V3)[0] + (V3.T * V3)[0])) == 0)
rng = np.random.default_rng(1)
Am, Bm, Cm = rng.standard_normal((3, 4)), rng.standard_normal((4, 2)), rng.standard_normal((2, 5))
v.assert_true("(AB)^T = B^T A^T and associativity", np.allclose((Am @ Bm).T, Bm.T @ Am.T)
              and np.allclose((Am @ Bm) @ Cm, Am @ (Bm @ Cm)))
v.assert_true("column j of AB is A times column j of B", np.allclose((Am @ Bm)[:, 1], Am @ Bm[:, 1]))
nn = sp.Symbol("n", positive=True, integer=True)
j = sp.Symbol("j", positive=True, integer=True)
v.assert_true("sum_{j=1}^{n-1} j^2 = (n-1)n(2n-1)/6",
              sp.simplify(sp.summation(j**2, (j, 1, nn - 1)) - (nn - 1) * nn * (2 * nn - 1) / 6) == 0)
l21, l31, l32 = sp.symbols("l21 l31 l32")
E21 = sp.eye(3); E21[1, 0] = -l21
E31 = sp.eye(3); E31[2, 0] = -l31
E32 = sp.eye(3); E32[2, 1] = -l32
Lsym = E21.inv() * E31.inv() * E32.inv()
v.assert_true("L = E21^-1 E31^-1 E32^-1 holds the multipliers unchanged",
              Lsym == sp.Matrix([[1, 0, 0], [l21, 1, 0], [l31, l32, 1]]))
v.assert_true("(3,1) entry of E32 E31 E21 is l32 l21 - l31", sp.expand((E32 * E31 * E21)[2, 0] - (l32 * l21 - l31)) == 0)
v.assert_true("machine epsilon is 2^-52", np.finfo(float).eps == 2.0**-52)

# ---------------------------------------------------------------- Example 1
u = np.array([2.0, -1.0, 2.0]); vv = np.array([3.0, 0.0, 4.0])
xh = (u @ vv) / (u @ u)
e = vv - xh * u
v.check("Ex 02-06.1a", u @ vv)
v.check("Ex 02-06.1b", np.linalg.norm(u))
v.check("Ex 02-06.1c", np.linalg.norm(vv))
v.check("Ex 02-06.1d", angle(u, vv))
v.check("Ex 02-06.1e", xh)
v.check("Ex 02-06.1f", np.linalg.norm(e))
v.assert_true("Ex 1: error orthogonal to u and |e| = |v| sin(theta)",
              abs(e @ u) < 1e-12 and abs(np.linalg.norm(e) - 5 * math.sin(math.radians(angle(u, vv)))) < 1e-12)

# ---------------------------------------------------------------- Example 2
R = np.array([[0, -1], [1, 0]]); S = np.array([[2, 0], [0, 1]]); x = np.array([1, 1])
v.assert_true("Ex 2: R rotates (1,0) to (0,1)", np.array_equal(R @ [1, 0], [0, 1]))
SRx, RSx = S @ R @ x, R @ S @ x
v.check("Ex 02-06.2a", SRx[0]); v.check("Ex 02-06.2b", SRx[1])
v.check("Ex 02-06.2c", RSx[0]); v.check("Ex 02-06.2d", RSx[1])
A2 = np.array([[1, 2, 0], [-1, 3, 1]]); B2 = np.array([[2, 1], [0, -1], [4, 2]])
v.check("Ex 02-06.2e", A2.shape[0] * A2.shape[1] * B2.shape[1])
v.check("Ex 02-06.2f", B2.shape[0] * B2.shape[1] * A2.shape[1])
AB2, BA2 = A2 @ B2, B2 @ A2
v.assert_true("Ex 2: AB = [[2,-1],[2,-2]]", np.array_equal(AB2, [[2, -1], [2, -2]]))
v.check("Ex 02-06.2g", AB2[0, 1]); v.check("Ex 02-06.2h", AB2[1, 1]); v.check("Ex 02-06.2i", BA2[0, 1])

# ---------------------------------------------------------------- Example 3
A3 = [[2, 1, -1], [4, 5, -3], [-2, 5, 4]]
mult3, U3n, c3, x3 = eliminate(A3, [1, 5, 20])
v.check("Ex 02-06.3a", float(mult3[(2, 1)])); v.check("Ex 02-06.3b", float(mult3[(3, 1)]))
v.check("Ex 02-06.3c", float(mult3[(3, 2)])); v.check("Ex 02-06.3d", float(U3n[2][2]))
v.check("Ex 02-06.3e", float(x3[0])); v.check("Ex 02-06.3f", float(x3[1])); v.check("Ex 02-06.3g", float(x3[2]))
L3 = np.array([[1, 0, 0], [2, 1, 0], [-1, 2, 1]]); Uu3 = np.array([[2, 1, -1], [0, 3, -1], [0, 0, 5]])
v.assert_true("Ex 3: L U = A", np.array_equal(L3 @ Uu3, np.array(A3)))
x3b = sl.solve_triangular(Uu3, sl.solve_triangular(L3, [0, 3, 6], lower=True))
v.check("Ex 02-06.3h", x3b[0])
v.assert_true("Ex 3: second solution (-0.5, 1, 0)", np.allclose(x3b, [-0.5, 1, 0]))
v.check("Ex 02-06.3i", np.prod(np.diag(Uu3)))
v.assert_true("Ex 3: product of pivots = det A", abs(np.linalg.det(np.array(A3, float)) - 30) < 1e-9)

# ---------------------------------------------------------------- Example 4 (IEEE double precision)
m4, x1n, x2n = solve2_float(1e-17, 1.0, 1.0, 1.0, 1.0, 2.0)
mp, x1p, x2p = solve2_float(1.0, 1.0, 1e-17, 1.0, 2.0, 1.0)
v.check("Ex 02-06.4a", m4, rtol=1e-12)
v.check("Ex 02-06.4b", x1n)
v.check("Ex 02-06.4c", mp, rtol=1e-12)
v.check("Ex 02-06.4d", x1p)
v.assert_true("Ex 4: unpivoted x2 = 1 and the 1 - 1e17 rounds to -1e17", x2n == 1.0 and 1.0 - 1e17 == -1e17)
v.assert_true("Ex 4: spacing of doubles near 1e17 is 16", np.spacing(1e17) == 16.0)
_, x1_12, _ = solve2_float(1e-12, 1.0, 1.0, 1.0, 1.0, 2.0)
true12 = 1 / (1 - 1e-12)
v.check("Ex 02-06.4e", abs(x1_12 - true12) / true12)
v.assert_true("Ex 4: the library (pivoting) solve is exact to rounding",
              abs(np.linalg.solve([[1e-17, 1.0], [1.0, 1.0]], [1.0, 2.0])[0] - 1.0) < 1e-15)

# ---------------------------------------------------------------- Example 5 (stamping, mS / V / mA)
ga, gb, gc, gd, ge = Fr(1), Fr(1, 2), Fr(1), Fr(1, 2), Fr(2)
G5 = [[ga + gb, -ga, -gb], [-ga, ga + gc + gd, -gd], [-gb, -gd, gb + gd + ge]]
mult5, U5, c5, v5 = eliminate(G5, [10, 0, 0])
v.assert_true("Ex 5: exact node voltages 290/27, 130/27, 70/27", v5 == [Fr(290, 27), Fr(130, 27), Fr(70, 27)])
v.assert_true("Ex 5: pivots 3/2, 11/6, 27/11", [U5[0][0], U5[1][1], U5[2][2]] == [Fr(3, 2), Fr(11, 6), Fr(27, 11)])
v.check("Ex 02-06.5a", float(U5[2][2]))
v.check("Ex 02-06.5b", float(v5[0])); v.check("Ex 02-06.5c", float(v5[1])); v.check("Ex 02-06.5d", float(v5[2]))
v.check("Ex 02-06.5e", float(ga * (v5[0] - v5[1])))
Psrc = float(v5[0] * 10)
Pres = float(ga * (v5[0] - v5[1]) ** 2 + gb * (v5[0] - v5[2]) ** 2 + gc * v5[1] ** 2 + gd * (v5[1] - v5[2]) ** 2
             + ge * v5[2] ** 2)
v.assert_true("Ex 5: energy conservation", abs(Psrc - Pres) < 1e-12)
v.assert_true("Ex 5: KCL at node 2", ga * (v5[0] - v5[1]) == gc * v5[1] + gd * (v5[1] - v5[2]))
v.check("Ex 02-06.5f", Psrc)
v.check("Ex 02-06.5g", float(v5[0] / 10))

# ---------------------------------------------------------------- Example 6 (costs at scale; specs from R-040)
n6 = 1e6
dense_flops = 2 / 3 * n6**3
v.check("Ex 02-06.6a", dense_flops)
v.check("Ex 02-06.6b", 8 * n6**2 / 1e12)
nnz6 = 5 * n6
v.check("Ex 02-06.6c", nnz6)
v.check("Ex 02-06.6d", n6**1.5)
fp64_tc = 67e12
v.check("Ex 02-06.6k", dense_flops / fp64_tc / 3600)
v.check("Ex 02-06.6l", 8 * n6**2 / 80e9)
v.check("Ex 02-06.6m", nnz6 * 8 / 1e6)
v.check("Ex 02-06.6n", dense_flops / n6**1.5, tol=0.5e8)
v.check("Ex 02-06.6o", 8 * n6**2 / (nnz6 * 8), tol=0.5e5)
d = 8192
flops = 2 * d * d
wbytes = 2 * d * d
peak = 1979e12 / 2      # NVIDIA lists 1,979 TFLOPS FP16 "with sparsity"; dense is half [R-040]
bw = 3.35e12
v.check("Ex 02-06.6e", flops)
v.check("Ex 02-06.6f", wbytes / 1e6)
v.check("Ex 02-06.6p", 4 * d)
t_mem, t_cmp = wbytes / bw, flops / peak
v.check("Ex 02-06.6g", t_mem * 1e6)
v.check("Ex 02-06.6h", t_cmp * 1e6)
v.check("Ex 02-06.6q", t_cmp / t_mem * 100)
ridge = peak / bw
v.check("Ex 02-06.6i", ridge)
Bsym = sp.Symbol("B", positive=True)
Bsol = sp.solve(sp.Eq(Bsym / (1 + 2 * Bsym / d), ridge), Bsym)[0]
v.check("Ex 02-06.6j", float(Bsol))
v.assert_true("Ex 6: intensity at batch 1 is d/(d+2)", abs(flops / (wbytes + 4 * d) - d / (d + 2)) < 1e-15)

# ---------------------------------------------------------------- numbers to know
v.check("N 02-06.a", 8 * 1e4**2 / 1e6)
v.check("N 02-06.b", np.finfo(float).eps)
v.check("N 02-06.c", ridge)
v.check("N 02-06.d", 4e15 / 19.2e12)
v.check("N 02-06.e", 256 * 256 * 2 * 700e6 / 1e12)
v.assert_true("TPU v1: 256 x 256 = 65,536 MACs", 256 * 256 == 65536)
rmax, rpeak = 2198.40, 2735.82   # PFlop/s, TOP500 Nov 2026 [R-038]
v.check("N 02-06.f", rmax / 1000)
v.check("N 02-06.g", rmax / rpeak * 100)

# ---------------------------------------------------------------- Problems 1-5
a1, b1 = np.array([1.0, -2, 2]), np.array([4.0, 0, -3])
w1 = 2 * a1 - b1
v.check("02-06.1a", w1[0]); v.check("02-06.1b", w1[1]); v.check("02-06.1c", w1[2])
v.check("02-06.1d", a1 @ b1); v.check("02-06.1e", np.linalg.norm(a1)); v.check("02-06.1f", np.linalg.norm(b1))
v.check("02-06.1g", (a1 / np.linalg.norm(a1))[1]); v.check("02-06.1h", angle(a1, b1))
cc = sp.Symbol("c")
csol = sp.solve(sp.Matrix([1, cc, 2]).dot(sp.Matrix([3, -1, cc])), cc)
v.check("02-06.2a", float(csol[0]))
v.check("02-06.2b", angle([1, 1, 1], [1, 0, 0]))
v.check("02-06.2c", angle([1, 1, 1], [1, 1, -1]))
k8 = sp.symbols("k")
v.check("02-06.2d", float(sp.summation(sp.sin(2 * sp.pi * k8 / 8) * sp.cos(2 * sp.pi * k8 / 8), (k8, 0, 7))))
A3p = np.array([[1, 2], [3, -1], [0, 4]])
Ax3 = A3p @ [2, -1]
v.assert_true("P3: column picture equals row picture", np.array_equal(Ax3, 2 * A3p[:, 0] - A3p[:, 1]))
v.check("02-06.3a", Ax3[0]); v.check("02-06.3b", Ax3[1]); v.check("02-06.3c", Ax3[2])
xls, res, rank, _ = np.linalg.lstsq(A3p, [5, 1, 8], rcond=None)
v.assert_true("P3(b): exact solution exists (zero residual)", np.allclose(A3p @ xls, [5, 1, 8]))
v.check("02-06.3d", xls[0]); v.check("02-06.3e", xls[1])
A4, B4 = np.array([[1, 2], [0, 1]]), np.array([[1, 0], [3, 1]])
v.check("02-06.4a", (A4 @ B4)[0, 0]); v.check("02-06.4b", (A4 @ B4)[1, 0]); v.check("02-06.4c", (B4 @ A4)[1, 1])
v.assert_true("P4: (AB)^T = B^T A^T but A^T B^T differs",
              np.array_equal((A4 @ B4).T, B4.T @ A4.T) and not np.array_equal((A4 @ B4).T, A4.T @ B4.T))
v.check("02-06.4d", (A4.T @ B4.T)[0, 0]); v.check("02-06.4e", (A4 @ A4)[0, 1])
b5 = np.array([1.0, 2, 6]); one = np.ones(3)
x5 = (one @ b5) / (one @ one); e5 = b5 - x5 * one
v.check("02-06.5a", x5); v.check("02-06.5b", e5 @ e5); v.check("02-06.5c", np.var(b5))
v.assert_true("P5: projection coefficient onto ones is the mean", x5 == b5.mean())
a5 = np.array([1.0, 2, 2]); x5b = (a5 @ b5) / (a5 @ a5); e5b = b5 - x5b * a5
v.check("02-06.5d", x5b); v.check("02-06.5e", np.linalg.norm(e5b))
v.assert_true("P5(b): error orthogonal and Pythagoras", abs(e5b @ a5) < 1e-12
              and abs(b5 @ b5 - (x5b * a5) @ (x5b * a5) - e5b @ e5b) < 1e-12)

# ---------------------------------------------------------------- Problems 6-10
mult6, U6, _, x6 = eliminate([[1, 1, 2], [3, 4, 5], [2, -2, 1]], [3, 7, 7])
v.check("02-06.6a", float(mult6[(2, 1)])); v.check("02-06.6b", float(mult6[(3, 1)]))
v.check("02-06.6c", float(mult6[(3, 2)])); v.check("02-06.6d", float(U6[2][2]))
v.check("02-06.6e", float(x6[0])); v.check("02-06.6f", float(x6[1])); v.check("02-06.6g", float(x6[2]))
A7 = np.array([[0, 1, 2], [1, 2, 1], [2, 7, 9.0]]); b7 = np.array([1, 0, 4.0])
P7 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
mult7, U7, _, x7 = eliminate(P7 @ A7, P7 @ b7)
L7 = np.array([[1, 0, 0], [0, 1, 0], [2, 3, 1]])
v.assert_true("P7(a): PA = LU", np.allclose(P7 @ A7, L7 @ np.array([[float(z) for z in r] for r in U7])))
v.check("02-06.7a", float(x7[0])); v.check("02-06.7b", float(x7[1])); v.check("02-06.7c", float(x7[2]))
v.check("02-06.7d", float(mult7[(3, 2)]))
Pp, Lp, Up = sl.lu(A7)        # SciPy: A = P L U with partial pivoting
v.assert_true("P7(b): |multipliers| <= 1 with partial pivoting", np.all(np.abs(Lp) <= 1 + 1e-12))
v.check("02-06.7e", Up[0, 0]); v.check("02-06.7f", Up[1, 1]); v.check("02-06.7g", Up[2, 2])
v.check("02-06.7h", Lp[1, 0]); v.check("02-06.7i", Lp[2, 1])
kk, aa, qq = sp.symbols("k a q")
v.check("02-06.8a", float(sp.solve(kk - 6, kk)[0]))
v.check("02-06.8b", float(sp.solve(sp.Matrix([[1, 2], [2, aa]]).det(), aa)[0]))
x8 = np.linalg.solve([[1, 2], [2, 5]], [3, 5])
v.check("02-06.8c", x8[0]); v.check("02-06.8d", x8[1])
v.check("02-06.8e", float(sp.solve(sp.Matrix([[1, 2, 3], [2, 5, 7], [3, 7, qq]]).det(), qq)[0]))
A9 = [[4, 3], [6, 3]]
mult9, U9, _, x9 = eliminate(A9, [10, 12])
v.check("02-06.9a", float(mult9[(2, 1)])); v.check("02-06.9b", float(U9[1][1]))
v.check("02-06.9c", float(x9[0])); v.check("02-06.9d", float(x9[1]))
_, _, _, x9b = eliminate(A9, [1, 0])
v.check("02-06.9e", float(x9b[0]))
Ainv9 = np.linalg.inv(np.array(A9, float))
v.check("02-06.9f", Ainv9[1, 1]); v.check("02-06.9g", Ainv9[0, 1])
Enum = np.array((E32 * E31 * E21).subs({l21: 2, l31: -1, l32: 2}), dtype=float)
v.check("02-06.10a", Enum[1, 0]); v.check("02-06.10b", Enum[2, 0]); v.check("02-06.10c", Enum[2, 1])
v.assert_true("P10: E A = U for Example 3", np.allclose(Enum @ np.array(A3, float), Uu3))
v.check("02-06.10d", np.linalg.inv(Enum)[2, 0])

# ---------------------------------------------------------------- Problems 11-13 (mS, V, mA)
G11 = np.array([[0.5 + 1, -1], [-1, 1 + 0.25]])
v11 = np.linalg.solve(G11, [5, -1])
v.check("02-06.11a", v11[0]); v.check("02-06.11b", v11[1]); v.check("02-06.11c", (v11[0] - v11[1]) / 1)
P_src, P_sink = v11[0] * 5, v11[1] * 1
P_res = v11[0] ** 2 / 2 + (v11[0] - v11[1]) ** 2 / 1 + v11[1] ** 2 / 4
v.check("02-06.11d", P_src); v.check("02-06.11e", P_sink); v.check("02-06.11f", P_res)
v.assert_true("P11: resistor power = delivered - absorbed", abs(P_res - (P_src - P_sink)) < 1e-12)
n_ = 2000
f12 = 2 / 3 * n_**3
v.check("02-06.12a", f12); v.check("02-06.12b", f12 / 50e9); v.check("02-06.12c", 2 * n_**2 / 50e9 * 1e3)
v.check("02-06.12d", f12 / (2 * n_**2))
v.check("02-06.12e", (2 * n_) ** 3 / n_**3); v.check("02-06.12f", (2 * n_) ** 2 / n_**2)
v.check("02-06.12g", 8 * n_**2 / 1e6)
G13 = np.array([[1.5, -1, -0.5], [-1, 2, -1], [-0.5, -1, 1.5]])
v.assert_true("P13: rows sum to zero, rank 2", np.allclose(G13.sum(axis=1), 0) and np.linalg.matrix_rank(G13) == 2)
v13 = np.linalg.solve(G13[:2, :2], [1, 0])
v.check("02-06.13a", v13[0]); v.check("02-06.13b", v13[1]); v.check("02-06.13c", v13[0] / 1)
v.assert_true("P13: R13 = 2k || (1k + 1k)", abs(v13[0] - 1 / (1 / 2 + 1 / 2)) < 1e-12)
M13 = np.array([[1.5, -1, -1], [-1, 2, 0], [1, 0, 0]])
s13 = np.linalg.solve(M13, [0, 0, 2])
v.check("02-06.13d", s13[1]); v.check("02-06.13e", s13[2])

# ---------------------------------------------------------------- Problem 14 (IR drop on a rail)
Rr, Ir, Nt = 0.02, 0.2, 5
T = (2 * np.eye(Nt) - np.eye(Nt, k=1) - np.eye(Nt, k=-1)) / Rr
Gs = T.copy(); Gs[-1, -1] = 1 / Rr
ds = np.linalg.solve(Gs, np.full(Nt, Ir))
dd = np.linalg.solve(T, np.full(Nt, Ir))
v.check("02-06.14a", 1 / Rr)
v.check("02-06.14b", ds[0] * 1e3); v.check("02-06.14f", ds[2] * 1e3); v.check("02-06.14c", ds.max() * 1e3)
v.assert_true("P14: worst drop = R I N(N+1)/2", abs(ds.max() - Rr * Ir * Nt * (Nt + 1) / 2) < 1e-12)
v.check("02-06.14d", dd.max() * 1e3)
v.assert_true("P14: two-pad worst drop at the middle tap", int(np.argmax(dd)) == 2)
v.check("02-06.14e", ds.max() / dd.max())
v.check("02-06.14g", dd[0] / Rr)

# ---------------------------------------------------------------- Problem 15 (edge accelerator)
peak15 = 512 * 2 * 1e9
ops15 = 2 * 1024**2
by15 = 1024**2
v.check("02-06.15a", peak15 / 1e12); v.check("02-06.15b", ops15); v.check("02-06.15c", by15 / 1e6)
v.check("02-06.15d", ops15 / by15)
tm15, tc15 = by15 / 8e9, ops15 / peak15
v.check("02-06.15e", tm15 * 1e6); v.check("02-06.15f", tc15 * 1e6); v.check("02-06.15g", tc15 / tm15 * 100)
v.check("02-06.15h", peak15 / 8e9)
ts15 = by15 / 256e9
v.check("02-06.15i", ts15 * 1e6); v.check("02-06.15j", tc15 / ts15 * 100)
v.check("02-06.15k", peak15 / 256e9); v.check("02-06.15l", tm15 / ts15)

# ---------------------------------------------------------------- lab handout
nlab = 1000
th = 2 * np.pi * 3 * np.arange(nlab) / nlab
v.check("Lab 02-06.a", angle(np.sin(th), np.cos(th)), tol=1e-6)
_, x1_8, _ = solve2_float(1e-8, 1.0, 1.0, 1.0, 1.0, 2.0)
v.check("Lab 02-06.b", abs(x1_8 - 1 / (1 - 1e-8)) * (1 - 1e-8))
_, x1_4, _ = solve2_float(1e-4, 1.0, 1.0, 1.0, 1.0, 2.0)
v.check("Lab 02-06.i", abs(x1_4 - 1 / (1 - 1e-4)) * (1 - 1e-4))


def grid_drop(N, Rg, Ig, pads):
    n = N * N
    idx = lambda r, c: r * N + c  # noqa: E731
    rows, cols, vals = [], [], []
    g = 1 / Rg
    for r in range(N):
        for c in range(N):
            for (r2, c2) in ((r, c + 1), (r + 1, c)):
                if r2 < N and c2 < N:
                    a_, b_ = idx(r, c), idx(r2, c2)
                    rows += [a_, b_, a_, b_]; cols += [a_, b_, b_, a_]; vals += [g, g, -g, -g]
    G = sps.csr_matrix((vals, (rows, cols)), shape=(n, n))
    pad_ids = {idx(r, c) for r, c in pads}
    keep = np.array([k for k in range(n) if k not in pad_ids])
    Gr = G[keep][:, keep].tocsc()
    dsol = np.zeros(n)
    dsol[keep] = spl.spsolve(Gr, np.full(len(keep), Ig))
    return dsol.reshape(N, N), Gr


d1, G1 = grid_drop(20, 0.1, 1e-3, [(0, 0)])
d4, _ = grid_drop(20, 0.1, 1e-3, [(0, 0), (0, 19), (19, 0), (19, 19)])
v.assert_true("Lab: sparse solve agrees with a dense solve", np.allclose(
    np.linalg.solve(G1.toarray(), np.full(G1.shape[0], 1e-3)), d1.ravel()[1:]))
v.assert_true("Lab: one-pad worst drop at the opposite corner", np.unravel_index(d1.argmax(), d1.shape) == (19, 19))
v.check("Lab 02-06.c", d1.max() * 1e3); v.check("Lab 02-06.d", d4.max() * 1e3)
v.check("Lab 02-06.e", d1.max() / d4.max())
v.check("Lab 02-06.f", G1.shape[0]); v.check("Lab 02-06.g", G1.nnz)
rngn = np.random.default_rng(0)   # the notebook draws its noisy signals from default_rng(0) right after creating it
xs = np.sin(th) + 0.5 * rngn.standard_normal(nlab)
ys = 0.8 * np.sin(th + 0.3) + 0.2 + 0.5 * rngn.standard_normal(nlab)
xc, yc = xs - xs.mean(), ys - ys.mean()
v.assert_true("Lab: correlation coefficient = cos(theta) of centered vectors",
              abs(np.corrcoef(xs, ys)[0, 1] - xc @ yc / (np.linalg.norm(xc) * np.linalg.norm(yc))) < 1e-12)
v.check("Lab 02-06.h", np.corrcoef(xs, ys)[0, 1])

v.finish()
