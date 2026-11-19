#!/usr/bin/env python3
"""Verify every number published in chapter 06-04, its solutions and its lab handout.

Independent routes. The text solves circuits by nodal analysis (by inspection, Cramer's rule,
supernodes, MNA stamps). This script instead uses:
  * the sparse-tableau formulation: unknowns are all node voltages, branch voltages and branch
    currents; equations are KCL from the incidence matrix, KVL (v = A^T e) and each element law;
  * matrix entries, determinants and eigenvalues from short-circuit admittance measurements
    (drive one node to 1 V with every other node held at 0 V and read the source currents),
    never from the "by inspection" rule;
  * nonzero counts from grid edge enumeration and from SciPy's Kronecker-product Laplacian;
  * the diode by bracketing root-finding on its KCL equation and by plain Newton steps.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-04", C_DIR / "chapters" / "06-04-nodal-analysis.md",
                        C_DIR / "solutions" / "06-04-solutions.md", C_DIR / "labs" / "06-04-lab" / "README.md")


def tableau(elements):
    """Sparse-tableau solve. elements: list of (name, kind, a, b, value) with kind R, I or V.
    Branch current i flows from a to b through the element; branch voltage is v_a - v_b.
    I: i = value (so 'I', '0', 'k' pushes current into node k). V: v_a - v_b = value.
    Returns (node voltages dict incl. '0', branch currents dict, branch voltages dict)."""
    nodes = sorted({n for _, _, a, b, _ in elements for n in (a, b) if n != "0"})
    nn, nb = len(nodes), len(elements)
    idx = {n: k for k, n in enumerate(nodes)}
    A = np.zeros((nn, nb))
    for k, (_, _, a, b, _) in enumerate(elements):
        if a != "0":
            A[idx[a], k] += 1.0
        if b != "0":
            A[idx[b], k] -= 1.0
    size = nn + 2 * nb                            # unknowns [e, i, vb]
    M, z = np.zeros((size, size)), np.zeros(size)
    M[:nn, nn:nn + nb] = A                        # KCL: A i = 0
    M[nn:nn + nb, :nn] = -A.T                     # KVL: vb - A^T e = 0
    M[nn:nn + nb, nn + nb:] = np.eye(nb)
    for k, (_, kind, _, _, val) in enumerate(elements):
        r = nn + nb + k
        if kind == "R":
            M[r, nn + nb + k], M[r, nn + k] = 1.0, -val
        elif kind == "I":
            M[r, nn + k], z[r] = 1.0, val
        elif kind == "V":
            M[r, nn + nb + k], z[r] = 1.0, val
        else:
            raise ValueError(kind)
    x = np.linalg.solve(M, z)
    e = {"0": 0.0, **{n: x[idx[n]] for n in nodes}}
    cur = {el[0]: x[nn + k] for k, el in enumerate(elements)}
    vol = {el[0]: x[nn + nb + k] for k, el in enumerate(elements)}
    return e, cur, vol


def absorbed(cur, vol, name):
    return cur[name] * vol[name]


def admittance(resistors, nodes, held=()):
    """Short-circuit admittance matrix of a resistor network: drive node j to 1 V and every
    other listed node to 0 V; G[k, j] is the current source k must push into node k.
    Nodes in `held` are known voltages (fixed by sources) and are held at 0 V as well."""
    n = len(nodes)
    G = np.zeros((n, n))
    for j, nj in enumerate(nodes):
        els = [(f"R{k}", "R", a, b, r) for k, (a, b, r) in enumerate(resistors)]
        els += [(f"V{m}", "V", nm, "0", 1.0 if m == j else 0.0) for m, nm in enumerate(nodes)]
        els += [(f"H{m}", "V", nm, "0", 0.0) for m, nm in enumerate(held)]
        _, cur, _ = tableau(els)
        for k in range(n):
            G[k, j] = -cur[f"V{k}"]               # tableau current is into the + terminal
    return G


# ================================================================ chapter
v.check("T 06-04.a", 50 - 1)
v.check("T 06-04.b", 2 * 120)
L1 = sp.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(100, 100))
lap100 = sp.kron(sp.identity(100), L1) + sp.kron(L1, sp.identity(100))
v.check("T 06-04.c", lap100.shape[0])
v.check("T 06-04.d", 100 * lap100.nnz / lap100.shape[0] ** 2)

# ---- Example 06-04.1
ex1 = [("I1", "I", "0", "1", 4.0), ("I2", "I", "0", "2", 1.0),
       ("R1", "R", "1", "0", 2.0), ("R2", "R", "1", "2", 2.0), ("R3", "R", "2", "0", 4.0)]
e1, c1, vb1 = tableau(ex1)
v.check("Ex 06-04.1a", e1["1"])
v.check("Ex 06-04.1b", e1["2"])
v.check("Ex 06-04.1c", np.linalg.det(admittance([("1", "0", 2.0), ("1", "2", 2.0), ("2", "0", 4.0)], ["1", "2"])))
v.check("Ex 06-04.1d", c1["R1"])
v.check("Ex 06-04.1e", c1["R2"])
v.check("Ex 06-04.1f", c1["R3"])
v.check("Ex 06-04.1g", -absorbed(c1, vb1, "I1") - absorbed(c1, vb1, "I2"))
v.check("Ex 06-04.1h", absorbed(c1, vb1, "R1"))
v.check("Ex 06-04.1i", absorbed(c1, vb1, "R2"))
v.check("Ex 06-04.1j", absorbed(c1, vb1, "R3"))

# ---- Example 06-04.2: the bridge of 06-03 with node a held at 10 V
bridge = [("a", "c", 10.0), ("a", "d", 20.0), ("c", "d", 30.0), ("c", "0", 40.0), ("d", "0", 50.0)]
Gb = admittance(bridge, ["c", "d"], held=["a"])    # node a is known (10 V): held at 0 V for the matrix
v.check("Ex 06-04.2a", Gb[0, 0])
v.check("Ex 06-04.2b", Gb[1, 1])
e2, c2, _ = tableau([(f"R{k}", "R", a, b, r) for k, (a, b, r) in enumerate(bridge)] + [("V", "V", "a", "0", 10.0)])
v.check("Ex 06-04.2c", e2["c"])
v.check("Ex 06-04.2d", e2["d"])
v.check("Ex 06-04.2e", 1e3 * c2["R2"])
v.check("Ex 06-04.2f", -c2["V"])
v.check("Ex 06-04.2g", np.linalg.det(Gb))

# ---- Examples 06-04.3 and 06-04.4
ex3 = [("V12", "V", "1", "0", 12.0), ("V5", "V", "2", "3", 5.0),
       ("R12", "R", "1", "2", 2.0), ("R13", "R", "1", "3", 3.0), ("R2", "R", "2", "0", 4.0), ("R3", "R", "3", "0", 6.0)]
e3, c3, vb3 = tableau(ex3)
v.check("Ex 06-04.3a", e3["2"])
v.check("Ex 06-04.3b", e3["3"])
v.check("Ex 06-04.3c", -c3["V5"])
v.check("Ex 06-04.3d", -absorbed(c3, vb3, "V5"))
v.check("Ex 06-04.3e", -c3["V12"])
v.check("Ex 06-04.3f", -absorbed(c3, vb3, "V12"))
v.check("Ex 06-04.3g", sum(absorbed(c3, vb3, r) for r in ("R12", "R13", "R2", "R3")))
v.check("Ex 06-04.3h", absorbed(c3, vb3, "R12"))
v.check("Ex 06-04.3i", absorbed(c3, vb3, "R13"))
v.check("Ex 06-04.3j", absorbed(c3, vb3, "R2"))
v.check("Ex 06-04.3k", absorbed(c3, vb3, "R3"))
v.check("Ex 06-04.4a", c3["V12"])
v.check("Ex 06-04.4b", c3["V5"])
v.assert_true("Ex 06-04.4 power balance", abs(sum(absorbed(c3, vb3, el[0]) for el in ex3)) < 1e-9)


# ---- Example 06-04.5 and the grids of Problem 06-04.10 and the lab
def grid_elements(n, r_edge, i_load, vdd, bumps):
    els = []
    name = lambda a, c: f"n{a}_{c}"  # noqa: E731
    for a in range(n):
        for c in range(n):
            if c + 1 < n:
                els.append((f"Rh{a}{c}", "R", name(a, c), name(a, c + 1), r_edge))
            if a + 1 < n:
                els.append((f"Rv{a}{c}", "R", name(a, c), name(a + 1, c), r_edge))
            els.append((f"I{a}{c}", "I", name(a, c), "0", i_load))     # load draws current out of the node
    for k, (a, c) in enumerate(bumps):
        els.append((f"B{k}", "V", name(a, c), "0", vdd))
    return els


def grid_solve(n, r_edge, i_load, vdd, bumps):
    els = grid_elements(n, r_edge, i_load, vdd, bumps)
    e, cur, _ = tableau(els)
    volts = np.array([[e[f"n{a}_{c}"] for c in range(n)] for a in range(n)])
    bump_current = -sum(cur[f"B{k}"] for k in range(len(bumps)))
    return volts, bump_current


corners5 = [(0, 0), (0, 4), (4, 0), (4, 4)]
g5, ib5 = grid_solve(5, 0.010, 0.5, 0.80, corners5)
unknown5 = 25 - len(corners5)
v.check("Ex 06-04.5a", unknown5)
# nonzeros: one diagonal entry per unknown plus two per edge joining two unknown nodes
edges5 = [((a, c), (a, c + 1)) for a in range(5) for c in range(4)] + [((a, c), (a + 1, c)) for a in range(4) for c in range(5)]
v.check("Ex 06-04.5b", unknown5 + 2 * sum(1 for p, q in edges5 if p not in corners5 and q not in corners5))
v.check("Ex 06-04.5c", g5.min())
v.check("Ex 06-04.5d", 1e3 * (0.80 - g5.min()))
v.check("Ex 06-04.5e", ib5 - len(corners5) * 0.5)
v.check("Ex 06-04.5f", 100 * (0.80 - g5.min()) / 0.80)
v.assert_true("Ex 06-04.5 worst node is the center", np.unravel_index(np.argmin(g5), g5.shape) == (2, 2))
v.assert_true("Ex 06-04.5 symmetric map", np.allclose(g5, g5.T) and np.allclose(g5, g5[::-1, :]))

# ================================================================ solutions
v.check("06-04.1a", 6 - 1)
v.check("06-04.1b", 2 * 9)
v.check("06-04.1c", (6 - 1) + 2)
v.check("06-04.1d", (6 - 1) - 1)                 # v1 fixed; supernode KCL + constraint replace two KCLs

# ---- Problem 06-04.2 (kΩ, mA, V, mS, mW)
p2r = [("1", "0", 1.0), ("1", "2", 2.0), ("2", "3", 4.0), ("3", "0", 5.0), ("1", "3", 2.5)]
p2 = [(f"R{k}", "R", a, b, r) for k, (a, b, r) in enumerate(p2r)] + [("Ia", "I", "0", "1", 3.0), ("Ib", "I", "3", "0", 1.0)]
e2p, c2p, vb2p = tableau(p2)
v.check("06-04.2a", e2p["1"])
v.check("06-04.2b", e2p["2"])
v.check("06-04.2c", e2p["3"])
for ident, k in zip("defgh", range(5)):
    v.check(f"06-04.2{ident}", c2p[f"R{k}"])
v.check("06-04.2i", -absorbed(c2p, vb2p, "Ia"))
v.check("06-04.2j", sum(absorbed(c2p, vb2p, f"R{k}") for k in range(5)))
v.check("06-04.2k", absorbed(c2p, vb2p, "Ib"))
G2 = admittance(p2r, ["1", "2", "3"])
S = G2[np.ix_([0, 2], [0, 2])] - np.outer(G2[[0, 2], 1], G2[1, [0, 2]]) / G2[1, 1]   # eliminate v2
v.check("06-04.2l", 900 * np.linalg.det(S))
v.assert_true("06-04.2 symmetric", np.allclose(G2, G2.T))
dom = np.diag(G2) - (np.abs(G2).sum(axis=1) - np.abs(np.diag(G2)))
v.assert_true("06-04.2 dominance: rows 1, 3 strict, row 2 equality", dom[0] > 1e-9 and abs(dom[1]) < 1e-12 and dom[2] > 1e-9)

# ---- Problem 06-04.3
p3r = [("1", "0", 3.0), ("1", "2", 6.0), ("2", "0", 3.0)]
p3 = [(f"R{k}", "R", a, b, r) for k, (a, b, r) in enumerate(p3r)] + [("Ia", "I", "0", "1", 2.0), ("Ib", "I", "2", "0", 1.0)]
e3p, c3p, vb3p = tableau(p3)
v.check("06-04.3a", np.linalg.det(admittance(p3r, ["1", "2"])))
v.check("06-04.3b", e3p["1"])
v.check("06-04.3c", e3p["2"])
v.check("06-04.3d", -absorbed(c3p, vb3p, "Ia"))
v.check("06-04.3e", -absorbed(c3p, vb3p, "Ib"))
v.check("06-04.3f", sum(absorbed(c3p, vb3p, f"R{k}") for k in range(3)))
v.check("06-04.3g", c3p["R1"])
v.check("06-04.3h", -c3p["R2"])                   # R2 is listed from node 2 to ground; current flows up

# ---- Problem 06-04.4
p4 = [("VA", "V", "A", "0", 9.0), ("RAB", "R", "A", "B", 1.0), ("RB0", "R", "B", "0", 2.0),
      ("RBC", "R", "B", "C", 1.0), ("RC0", "R", "C", "0", 1.0), ("IC", "I", "0", "C", 2.0)]
e4p, c4p, vb4p = tableau(p4)
v.check("06-04.4a", 3 - 1)                        # nodes A, B, C; A fixed by the source
v.check("06-04.4b", e4p["B"])
v.check("06-04.4c", e4p["C"])
v.check("06-04.4d", -c4p["VA"])
v.check("06-04.4e", -absorbed(c4p, vb4p, "VA"))
v.check("06-04.4f", sum(absorbed(c4p, vb4p, r) for r in ("RAB", "RB0", "RBC", "RC0")))
v.check("06-04.4g", -absorbed(c4p, vb4p, "IC"))

# ---- Problem 06-04.5
p5 = [("I3", "I", "0", "1", 3.0), ("V10", "V", "2", "1", 10.0), ("R4", "R", "1", "0", 4.0), ("R6", "R", "2", "0", 6.0)]
e5p, c5p, vb5p = tableau(p5)
v.check("06-04.5a", e5p["1"])
v.check("06-04.5b", e5p["2"])
v.check("06-04.5c", -c5p["V10"])
v.check("06-04.5d", -absorbed(c5p, vb5p, "V10"))
v.check("06-04.5e", -absorbed(c5p, vb5p, "I3"))
v.check("06-04.5f", c5p["V10"])
v.check("06-04.5g", absorbed(c5p, vb5p, "R4") + absorbed(c5p, vb5p, "R6"))

# ---- Problem 06-04.6 (kΩ, mA)
p6r = [("t", "A", 1.0), ("A", "0", 1.0), ("t", "B", 1.0), ("B", "0", 1.1)]
p6 = [(f"R{k}", "R", a, b, r) for k, (a, b, r) in enumerate(p6r)] + [("V", "V", "t", "0", 5.0), ("RG", "R", "B", "A", 0.1)]
e6p, c6p, _ = tableau(p6)
v.check("06-04.6a", e6p["A"])
v.check("06-04.6b", e6p["B"])
v.check("06-04.6c", c6p["RG"])
e6o, _, _ = tableau(p6[:-1])                      # galvanometer removed
v.check("06-04.6d", 1e3 * (e6o["B"] - e6o["A"]))
e6t, _, _ = tableau([(f"R{k}", "R", a, b, r) for k, (a, b, r) in enumerate(p6r)]
                    + [("V", "V", "t", "0", 0.0), ("It", "I", "A", "B", 1.0)])   # 1 mA test current A -> B
v.check("06-04.6e", e6t["B"] - e6t["A"])
v.check("06-04.6f", -c6p["V"])
v.check("06-04.6g", (e6o["B"] - e6o["A"]) / 0.1)
G6 = admittance(p6r + [("B", "A", 0.1)], ["A", "B"], held=["t"])
v.check("06-04.6h", np.linalg.det(G6))

# ---- Problem 06-04.7
p7 = [("V1", "V", "1", "0", 10.0), ("R1", "R", "1", "2", 2.0), ("R2", "R", "2", "0", 8.0), ("I1", "I", "0", "2", 1.0)]
e7p, c7p, vb7p = tableau(p7)
v.check("06-04.7a", e7p["2"])
v.check("06-04.7b", c7p["V1"])
v.check("06-04.7c", -absorbed(c7p, vb7p, "V1"))
v.check("06-04.7d", absorbed(c7p, vb7p, "R1") + absorbed(c7p, vb7p, "R2"))
v.check("06-04.7e", -absorbed(c7p, vb7p, "I1"))
v.check("06-04.7f", c7p["R2"])

# ---- Problem 06-04.8
G8 = admittance([("1", "2", 1.0)], ["1", "2"])
v.check("06-04.8a", np.linalg.det(G8), tol=1e-12)
e8, _, _ = tableau([("R", "R", "1", "2", 1.0), ("I", "I", "2", "1", 1.0), ("Rbig", "R", "2", "0", 1e6)])
v.check("06-04.8b", e8["1"] - e8["2"])
v.check("06-04.8c", e8["2"], tol=1e-9)
v.check("06-04.8d", e8["1"])
e8b, _, _ = tableau([("R", "R", "1", "2", 1.0), ("I", "I", "2", "1", 1.0), ("Rbig", "R", "2", "0", 1e3)])
v.assert_true("06-04.8 independent of the large resistor", abs(e8b["2"]) < 1e-12 and abs(e8b["1"] - 1) < 1e-12)

# ---- Problem 06-04.9
x9 = {"0": 0.0, "1": 1.0, "2": -1.0, "3": 2.0}
v.check("06-04.9a", sum((x9[a] - x9[b]) ** 2 / r for a, b, r in p2r))
xv = np.array([1.0, -1.0, 2.0])
v.assert_true("06-04.9 matrix form agrees", abs(xv @ G2 @ xv - sum((x9[a] - x9[b]) ** 2 / r for a, b, r in p2r)) < 1e-12)
ev = np.linalg.eigvalsh(G2)
v.check("06-04.9b", ev[0])
v.check("06-04.9c", np.linalg.eigvalsh(G8)[0], tol=1e-12)
v.check("06-04.9d", ev[1])
v.check("06-04.9e", ev[2])
rng = np.random.default_rng(604)
v.assert_true("06-04.9 v^T G v > 0 for random v", all(y @ G2 @ y > 0 for y in rng.normal(size=(1000, 3))))

# ---- Problem 06-04.10 (3 x 3, 20 mOhm, 1 A per node, 0.75 V)
gc, ibc = grid_solve(3, 0.020, 1.0, 0.75, [(1, 1)])
gk, _ = grid_solve(3, 0.020, 1.0, 0.75, [(0, 0)])
gf, _ = grid_solve(3, 0.020, 1.0, 0.75, [(0, 0), (0, 2), (2, 0), (2, 2)])
v.check("06-04.10a", gc[0, 1])
v.check("06-04.10b", gc[0, 0])
v.check("06-04.10c", 1e3 * (0.75 - gc.min()))
v.check("06-04.10d", 1e3 * (0.75 - gk.min()))
v.check("06-04.10e", 1e3 * (0.75 - gf.min()))
v.check("06-04.10f", ibc - 1.0)
v.check("06-04.10g", gk[2, 2])
v.check("06-04.10h", gf[1, 1])
v.check("06-04.10i", gf[0, 1])
v.assert_true("06-04.10 corner-bump worst node is the opposite corner", np.unravel_index(np.argmin(gk), gk.shape) == (2, 2))

# ---- Problem 06-04.11
p11r = [("1", "2", 1.0), ("2", "3", 1.0), ("1", "0", 2.0), ("2", "0", 2.0), ("3", "0", 2.0)]
e11, c11, _ = tableau([(f"R{k}", "R", a, b, r) for k, (a, b, r) in enumerate(p11r)] + [("I", "I", "0", "1", 1.0)])
v.check("06-04.11a", np.linalg.det(admittance(p11r, ["1", "2", "3"])))
v.check("06-04.11b", e11["1"])
v.check("06-04.11c", e11["2"])
v.check("06-04.11d", e11["3"])
v.check("06-04.11e", e11["1"] / 1.0)
v.check("06-04.11f", e11["3"] / e11["1"])
v.assert_true("06-04.11 KCL at node 3", abs(c11["R1"] - c11["R4"]) < 1e-12)

# ---- Problem 06-04.12
csr = lap100.tocsr()
csr.indices = csr.indices.astype(np.int32)
csr.indptr = csr.indptr.astype(np.int32)
v.check("06-04.12a", csr.shape[0])
v.check("06-04.12b", csr.nnz)
v.assert_true("06-04.12 formula N^2 + 4N(N-1)", csr.nnz == 100 ** 2 + 4 * 100 * 99)
v.check("06-04.12c", 100 * csr.nnz / csr.shape[0] ** 2)
dense_bytes = csr.shape[0] ** 2 * np.dtype(np.float64).itemsize
sparse_bytes = csr.data.astype(np.float64).nbytes + csr.indices.nbytes + csr.indptr.nbytes
v.check("06-04.12d", dense_bytes / 1e6)
v.check("06-04.12e", sparse_bytes / 1e6)
v.check("06-04.12f", dense_bytes / sparse_bytes)
v.check("06-04.12g", csr.shape[0] ** 3 / 3)
v.check("06-04.12h", (1000 ** 2) ** 2 * 8 / 1e12)

# ---- Problem 06-04.13: diode, I_S = 1e-14 A, V_T = 25.852 mV
IS, VT = 1e-14, 0.025852
F = lambda x: (x - 5.0) / 1000.0 + IS * np.expm1(x / VT)   # noqa: E731  KCL residual at node 1
dF = lambda x: 1.0 / 1000.0 + IS / VT * np.exp(x / VT)     # noqa: E731
x0 = 0.7
g0 = IS / VT * np.exp(x0 / VT)
v.check("06-04.13a", g0)
v.check("06-04.13b", IS * np.expm1(x0 / VT) - g0 * x0)
x1 = x0 - F(x0) / dF(x0)
x2 = x1 - F(x1) / dF(x1)
v.check("06-04.13c", x1)
v.check("06-04.13d", x2)
vd = brentq(F, 0.3, 0.9, xtol=1e-15)
v.check("06-04.13e", vd)
v.check("06-04.13f", (5.0 - vd))                   # mA through 1 kOhm
v.check("06-04.13g", 1e3 * IS * np.expm1(x0 / VT))
g1 = IS / VT * np.exp(x1 / VT)
v.check("06-04.13h", g1)
v.check("06-04.13i", IS * np.expm1(x1 / VT) - g1 * x1)
v.check("06-04.13j", x0 / VT)
v.assert_true("06-04.13 Newton converges within 1 uV", abs(x2 - F(x2) / dF(x2) - vd) < 1e-6)

# ---- Problem 06-04.14
ext = [("R3", "R", "1", "0", 3.0), ("R1", "R", "1", "2", 1.0), ("R6", "R", "2", "0", 6.0), ("Is", "I", "2", "0", 2.0)]
eth, cth, vbth = tableau([("V", "V", "s", "0", 10.0), ("Rs", "R", "s", "1", 2.0)] + ext)
eno, cno, vbno = tableau([("IN", "I", "0", "1", 5.0), ("Rp", "R", "1", "0", 2.0)] + ext)
v.check("06-04.14a", np.linalg.det(admittance([("1", "0", 2.0), ("1", "0", 3.0), ("1", "2", 1.0), ("2", "0", 6.0)], ["1", "2"])))
v.check("06-04.14b", eth["1"])
v.check("06-04.14c", eth["2"])
v.assert_true("06-04.14 same node voltages", abs(eth["1"] - eno["1"]) < 1e-12 and abs(eth["2"] - eno["2"]) < 1e-12)
v.check("06-04.14d", -cth["V"])
v.check("06-04.14e", -absorbed(cth, vbth, "V"))
v.check("06-04.14f", -absorbed(cno, vbno, "IN"))
v.check("06-04.14g", absorbed(cth, vbth, "Rs"))
v.check("06-04.14h", absorbed(cno, vbno, "Rp"))
p_ext = sum(absorbed(cth, vbth, el[0]) for el in ext)
v.check("06-04.14i", p_ext)
v.check("06-04.14j", cno["Rp"])
v.check("06-04.14k", absorbed(cth, vbth, "R3"))
v.check("06-04.14l", absorbed(cth, vbth, "R1"))
v.check("06-04.14m", absorbed(cth, vbth, "R6"))
v.check("06-04.14n", absorbed(cth, vbth, "Is"))

# ================================================================ lab
n_nodes, n_vsrc = 3, 2
G3 = admittance([("1", "2", 2.0), ("1", "3", 3.0), ("2", "0", 4.0), ("3", "0", 6.0)], ["1", "2", "3"])
b_entries = 1 + 2                                  # V12: node 1 only; V5: nodes 2 and 3
nnz_mna = np.count_nonzero(np.abs(G3) > 1e-12) + 2 * b_entries
v.check("Lab 06-04.a", n_nodes + n_vsrc)
v.check("Lab 06-04.b", (n_nodes + n_vsrc) ** 2 - nnz_mna)
g5c, _ = grid_solve(5, 0.010, 0.5, 0.80, corners5 + [(2, 2)])
v.check("Lab 06-04.c", 1e3 * (0.80 - g5c.min()))
v.check("Lab 06-04.d", 25 - 5)

sys.exit(v.finish())
