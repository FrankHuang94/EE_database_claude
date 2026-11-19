#!/usr/bin/env python3
"""Verify every number published in chapter 06-05, its solutions and its lab handout.

Independent routes. The text solves circuits by mesh analysis (matrices by inspection, Cramer's
rule, supermeshes, loop analysis). This script instead:
  * re-solves every circuit with the sparse-tableau formulation (all node voltages, branch
    voltages and branch currents as unknowns), never forming a mesh equation;
  * builds mesh matrices from branch mesh-incidence vectors (R = sum of R_b m_b m_b^T) only to
    check determinants, eigenvalues and cofactors that the text quotes;
  * gets effective resistances from the pseudo-inverse of the graph Laplacian (and checks
    Foster's theorem), bipartiteness by breadth-first 2-colouring, and planarity of the cube
    drawing by testing every pair of edge segments for crossings.
"""
from __future__ import annotations

import sys
from collections import deque
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-05", C_DIR / "chapters" / "06-05-mesh-analysis.md",
                        C_DIR / "solutions" / "06-05-solutions.md", C_DIR / "labs" / "06-05-lab" / "README.md")


def tableau(elements):
    """Sparse-tableau solve. elements: (name, kind, a, b, value), kind R, I or V. Branch current
    flows from a to b through the element; branch voltage is v_a - v_b. I: i = value. V: v_a - v_b = value."""
    nodes = sorted({n for _, _, a, b, _ in elements for n in (a, b) if n != "0"})
    nn, nb = len(nodes), len(elements)
    idx = {n: k for k, n in enumerate(nodes)}
    A = np.zeros((nn, nb))
    for k, (_, _, a, b, _) in enumerate(elements):
        if a != "0":
            A[idx[a], k] += 1.0
        if b != "0":
            A[idx[b], k] -= 1.0
    size = nn + 2 * nb
    M, z = np.zeros((size, size)), np.zeros(size)
    M[:nn, nn:nn + nb] = A
    M[nn:nn + nb, :nn] = -A.T
    M[nn:nn + nb, nn + nb:] = np.eye(nb)
    for k, (_, kind, _, _, val) in enumerate(elements):
        r = nn + nb + k
        if kind == "R":
            M[r, nn + nb + k], M[r, nn + k] = 1.0, -val
        elif kind == "I":
            M[r, nn + k], z[r] = 1.0, val
        else:
            M[r, nn + nb + k], z[r] = 1.0, val
    x = np.linalg.solve(M, z)
    e = {"0": 0.0, **{n: x[idx[n]] for n in nodes}}
    cur = {el[0]: x[nn + k] for k, el in enumerate(elements)}
    vol = {el[0]: x[nn + nb + k] for k, el in enumerate(elements)}
    return e, cur, vol


def P(cur, vol, name):
    """Power absorbed by an element (passive convention)."""
    return cur[name] * vol[name]


def absorbed_total(cur, vol, names):
    return sum(P(cur, vol, n) for n in names)


def mesh_matrix(resistors, n_mesh):
    """R = sum R_b m_b m_b^T from (ohms, {mesh: sign}) entries."""
    R = np.zeros((n_mesh, n_mesh))
    for r, signs in resistors:
        m = np.array([signs.get(k, 0) for k in range(n_mesh)], dtype=float)
        R += r * np.outer(m, m)
    return R


def r_eff(edges, n_nodes, a, b):
    """Effective resistance between nodes a and b from the Laplacian pseudo-inverse."""
    L = np.zeros((n_nodes, n_nodes))
    for p, q, r in edges:
        g = 1.0 / r
        L[p, p] += g; L[q, q] += g; L[p, q] -= g; L[q, p] -= g
    Lp = np.linalg.pinv(L)
    return Lp[a, a] + Lp[b, b] - 2 * Lp[a, b]


def is_bipartite(n_nodes, edges):
    adj = {k: [] for k in range(n_nodes)}
    for p, q in edges:
        adj[p].append(q); adj[q].append(p)
    colour = {0: 0}; queue = deque([0])
    while queue:
        n = queue.popleft()
        for m in adj[n]:
            if m not in colour:
                colour[m] = 1 - colour[n]; queue.append(m)
            elif colour[m] == colour[n]:
                return False
    return True


def segments_cross(p1, p2, p3, p4):
    """True if open segments p1-p2 and p3-p4 properly intersect."""
    def orient(a, b, c):
        return np.sign((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
    if len({tuple(p1), tuple(p2)} & {tuple(p3), tuple(p4)}):
        return False                                   # sharing an endpoint is not a crossing
    return orient(p1, p2, p3) * orient(p1, p2, p4) < 0 and orient(p3, p4, p1) * orient(p3, p4, p2) < 0


# ================================================================ chapter
v.check("T 06-05.a", 120 - 50 + 1)

# ---- Example 06-05.1
ex1 = [("V1", "V", "a", "0", 20.0), ("R1", "R", "a", "m", 2.0), ("R2", "R", "m", "0", 4.0),
       ("R3", "R", "m", "c", 4.0), ("V2", "V", "c", "0", 8.0)]
e1, c1, vb1 = tableau(ex1)
R1m = mesh_matrix([(2, {0: 1}), (4, {0: 1, 1: -1}), (4, {1: 1})], 2)
v.check("Ex 06-05.1a", np.linalg.det(R1m))
v.check("Ex 06-05.1b", -c1["V1"])
v.check("Ex 06-05.1c", c1["V2"])
v.check("Ex 06-05.1d", c1["R2"])
v.check("Ex 06-05.1e", -P(c1, vb1, "V1"))
v.check("Ex 06-05.1f", P(c1, vb1, "V2"))
v.check("Ex 06-05.1g", absorbed_total(c1, vb1, ["R1", "R2", "R3"]))
v.check("Ex 06-05.1h", P(c1, vb1, "R1"))
v.check("Ex 06-05.1i", P(c1, vb1, "R2"))
v.check("Ex 06-05.1j", P(c1, vb1, "R3"))
v.check("Ex 06-05.1k", e1["m"])

# ---- Example 06-05.2
bridge = [("Rac", "R", "a", "c", 10.0), ("Rad", "R", "a", "d", 20.0), ("Rcd", "R", "c", "d", 30.0),
          ("Rcb", "R", "c", "0", 40.0), ("Rdb", "R", "d", "0", 50.0), ("V", "V", "a", "0", 10.0)]
e2, c2, _ = tableau(bridge)
R2m = mesh_matrix([(10, {0: 1, 1: -1}), (40, {0: 1, 2: -1}), (20, {1: 1}), (30, {1: 1, 2: -1}), (50, {2: 1})], 3)
v.check("Ex 06-05.2a", np.linalg.det(R2m))
v.check("Ex 06-05.2b", -c2["V"])
v.check("Ex 06-05.2c", c2["Rad"])                 # mesh 2 alone runs through R_ad
v.check("Ex 06-05.2d", c2["Rdb"])                 # mesh 3 alone runs through R_db
v.check("Ex 06-05.2e", 1e3 * c2["Rcd"])
v.check("Ex 06-05.2f", e2["c"])
cof = [np.linalg.det(np.delete(np.delete(R2m, 0, 0), k, 1)) * (-1) ** k for k in range(3)]
v.check("Ex 06-05.2g", cof[0])
v.check("Ex 06-05.2h", cof[1])
v.check("Ex 06-05.2i", cof[2])

# ---- Example 06-05.3
ex3 = [("V", "V", "a", "0", 36.0), ("R1", "R", "a", "t", 4.0), ("Is", "I", "0", "t", 3.0),
       ("R2", "R", "t", "r", 2.0), ("R3", "R", "r", "0", 6.0)]
e3, c3, vb3 = tableau(ex3)
v.check("Ex 06-05.3a", c3["R1"])
v.check("Ex 06-05.3b", c3["R2"])
v.check("Ex 06-05.3c", e3["t"])
v.check("Ex 06-05.3d", -P(c3, vb3, "Is"))
v.check("Ex 06-05.3e", -P(c3, vb3, "V"))
v.check("Ex 06-05.3f", absorbed_total(c3, vb3, ["R1", "R2", "R3"]))

# ---- Example 06-05.4
v.check("Ex 06-05.4a", (4 - 1) - 2)
v.check("Ex 06-05.4b", e1["m"])
dual = [("G1", "R", "1", "0", 1 / 2), ("G12", "R", "1", "2", 1 / 4), ("G2", "R", "2", "0", 1 / 4),
        ("I1", "I", "0", "1", 20.0), ("I2", "I", "2", "0", 8.0)]
ed, _, _ = tableau(dual)
v.check("Ex 06-05.4c", ed["1"])
v.check("Ex 06-05.4d", ed["2"])

# ---- Example 06-05.5
r_tr, Rm, Rg, Rs = 0.020, 2.5, 0.010, 1000.0
ex5 = [("V", "V", "s", "0", 5.0), ("r1", "R", "s", "p", r_tr), ("Rm", "R", "p", "g", Rm),
       ("r2", "R", "s", "q", r_tr), ("Rs", "R", "q", "g", Rs), ("Rg", "R", "g", "0", Rg)]
e5, c5, _ = tableau(ex5)
R5m = mesh_matrix([(r_tr + Rm, {0: 1, 1: -1}), (Rg, {0: 1}), (r_tr + Rs, {1: 1})], 2)
v.check("Ex 06-05.5a", R5m[0, 0])
v.check("Ex 06-05.5b", R5m[1, 1])
v.check("Ex 06-05.5c", np.linalg.det(R5m))
v.check("Ex 06-05.5d", -c5["V"])
v.check("Ex 06-05.5e", 1e3 * c5["Rs"])
v.check("Ex 06-05.5f", 1e3 * e5["g"])
lsb12 = 5.0 / 2 ** 12
v.check("Ex 06-05.5g", 1e3 * lsb12)
v.check("Ex 06-05.5h", e5["g"] / lsb12)
ex5s = [("V", "V", "s", "0", 5.0), ("r1", "R", "s", "p", r_tr), ("Rm", "R", "p", "gm", Rm), ("Rg1", "R", "gm", "0", Rg),
        ("r2", "R", "s", "q", r_tr), ("Rs", "R", "q", "gs", Rs), ("Rg2", "R", "gs", "0", Rg)]
e5s, _, _ = tableau(ex5s)
v.check("Ex 06-05.5i", 1e6 * e5s["gs"])
v.check("Ex 06-05.5j", e5["g"] / e5s["gs"])

# ================================================================ solutions
v.check("06-05.1a", 13 - 8 + 1)
v.check("06-05.1b", 8 - 1)
v.check("06-05.1c", (13 - 8 + 1) - 1)
v.check("06-05.1d", (8 - 1) - 2)
v.check("06-05.1e", (2 - 1) - 1)
for k in range(1, 8):                             # ladder counts agree for every k
    n, b = k + 2, 2 * k + 1
    v.assert_true(f"06-05.1c ladder k={k}", b - n + 1 == k and (n - 1) - 1 == k)

# ---- Problem 06-05.2: nodes: top rail of each mesh joined in a row; build an equivalent circuit
p2 = [("V12", "V", "x1", "0", 12.0), ("R1", "R", "x1", "n1", 1.0), ("R3s", "R", "n1", "0", 3.0),
      ("R2", "R", "n1", "n2", 2.0), ("R6s", "R", "n2", "0", 6.0), ("R4", "R", "n2", "x3", 4.0),
      ("V6", "V", "0", "x3", 6.0)]
# mesh 3 runs n2 -> x3 -> (through V6 from x3 to 0) -> back up R6s; V6 with + at 0 is a rise going x3 -> 0
e2p, c2p, vb2p = tableau(p2)
v.check("06-05.2a", c2p["R1"])
v.check("06-05.2b", c2p["R2"])
v.check("06-05.2c", c2p["R4"])
R2p = mesh_matrix([(1, {0: 1}), (3, {0: 1, 1: -1}), (2, {1: 1}), (6, {1: 1, 2: -1}), (4, {2: 1})], 3)
v.check("06-05.2d", np.linalg.det(R2p))
v.check("06-05.2e", c2p["R3s"])
v.check("06-05.2f", c2p["R6s"])
v.check("06-05.2g", -P(c2p, vb2p, "V12") - P(c2p, vb2p, "V6"))

# ---- Problem 06-05.3
p3 = [("V10", "V", "a", "0", 10.0), ("R2", "R", "a", "m", 2.0), ("R3", "R", "m", "0", 3.0),
      ("R5", "R", "m", "c", 5.0), ("V5", "V", "0", "c", 5.0)]
e3p, c3p, vb3p = tableau(p3)
v.check("06-05.3a", np.linalg.det(mesh_matrix([(2, {0: 1}), (3, {0: 1, 1: -1}), (5, {1: 1})], 2)))
v.check("06-05.3b", c3p["R2"])
v.check("06-05.3c", c3p["R5"])
v.check("06-05.3d", c3p["R3"])
v.check("06-05.3e", -P(c3p, vb3p, "V10"))
v.check("06-05.3f", -P(c3p, vb3p, "V5"))
v.check("06-05.3g", absorbed_total(c3p, vb3p, ["R2", "R3", "R5"]))

# ---- Problem 06-05.4: current source 2 A (with 4 Ohm in series) on mesh 1's outer branch
p4 = [("Is", "I", "0", "u", 2.0), ("R4", "R", "u", "m", 4.0), ("R6", "R", "m", "0", 6.0),
      ("R3", "R", "m", "c", 3.0), ("V12", "V", "0", "c", 12.0)]
e4p, c4p, vb4p = tableau(p4)
v.check("06-05.4a", c4p["R3"])
v.check("06-05.4b", c4p["Is"] - c4p["R3"])
v.check("06-05.4c", e4p["u"])                     # rise across the source along its arrow
v.check("06-05.4d", -P(c4p, vb4p, "Is"))
v.check("06-05.4e", -P(c4p, vb4p, "V12"))
v.check("06-05.4f", absorbed_total(c4p, vb4p, ["R4", "R6", "R3"]))

# ---- Problem 06-05.5
p5 = [("V20", "V", "a", "0", 20.0), ("R2", "R", "a", "t", 2.0), ("Is", "I", "0", "t", 2.0),
      ("R4", "R", "t", "u", 4.0), ("R3", "R", "u", "0", 3.0), ("R6", "R", "u", "0", 6.0)]
e5p, c5p, vb5p = tableau(p5)
v.check("06-05.5a", c5p["R2"])
v.check("06-05.5b", c5p["R4"])
v.check("06-05.5c", c5p["R6"])
v.check("06-05.5d", e5p["t"])
v.check("06-05.5e", -P(c5p, vb5p, "Is"))
v.check("06-05.5f", absorbed_total(c5p, vb5p, ["R2", "R4", "R3", "R6"]))

# ---- Problem 06-05.6
p6 = [("VA", "V", "ea", "0", 12.6), ("rA", "R", "ea", "top", 0.05), ("VB", "V", "eb", "0", 12.0),
      ("rB", "R", "top", "eb", 0.08), ("RL", "R", "top", "0", 1.2)]
e6p, c6p, vb6p = tableau(p6)
v.check("06-05.6a", np.linalg.det(mesh_matrix([(0.05, {0: 1}), (0.08, {0: 1, 1: -1}), (1.2, {1: 1})], 2)))
v.check("06-05.6b", c6p["rA"])
v.check("06-05.6c", c6p["RL"])
v.check("06-05.6d", c6p["rB"])
v.check("06-05.6e", e6p["top"])
v.check("06-05.6f", P(c6p, vb6p, "RL"))
v.check("06-05.6g", -P(c6p, vb6p, "VA"))
v.check("06-05.6h", P(c6p, vb6p, "VB"))
v.check("06-05.6i", P(c6p, vb6p, "rA"))
v.check("06-05.6j", P(c6p, vb6p, "rB"))
_, c6n, _ = tableau(p6[:-1])
v.check("06-05.6k", c6n["rA"])

# ---- Problem 06-05.7 (kOhm, mA)
p7 = [("VA", "V", "A", "0", 9.0), ("RAB", "R", "A", "B", 1.0), ("RB0", "R", "B", "0", 2.0),
      ("RBC", "R", "B", "C", 1.0), ("RC0", "R", "C", "0", 1.0), ("IC", "I", "0", "C", 2.0)]
e7p, c7p, _ = tableau(p7)
v.check("06-05.7a", 3 - 1)
v.check("06-05.7b", -c7p["VA"])
v.check("06-05.7c", c7p["RBC"])
v.check("06-05.7d", c7p["RBC"] - c7p["RC0"])     # mesh 3 current = mesh 2 current minus R_C0's downward current
v.check("06-05.7e", e7p["B"])
v.check("06-05.7f", e7p["C"])

# ---- Problem 06-05.8
i2vec = np.array([c2p["R1"], c2p["R2"], c2p["R4"]])
v.check("06-05.8a", i2vec @ R2p @ i2vec)
v.assert_true("06-05.8 i^T R i = i^T v", abs(i2vec @ R2p @ i2vec - i2vec @ np.array([12.0, 0.0, 6.0])) < 1e-9)
ev = np.linalg.eigvalsh(R2p)
v.check("06-05.8b", ev[0])
v.check("06-05.8c", ev[1])
v.check("06-05.8d", ev[2])

# ---- Problem 06-05.9: the dual of Example 06-05.3
dual3 = [("I36", "I", "0", "1", 36.0), ("G4", "R", "1", "0", 1 / 4), ("V3", "V", "2", "1", 3.0),
         ("G2", "R", "2", "0", 1 / 2), ("G6", "R", "2", "0", 1 / 6)]
ed3, _, _ = tableau(dual3)
v.check("06-05.9a", ed3["1"])
v.check("06-05.9b", ed3["2"])

# ---- Problem 06-05.10 (kOhm, mA)
p10 = [("V", "V", "t", "0", 5.0), ("R1", "R", "t", "A", 1.0), ("R2", "R", "A", "0", 1.0),
       ("R3", "R", "t", "B", 1.0), ("R4", "R", "B", "0", 1.1), ("RG", "R", "A", "B", 0.1)]
_, c10, _ = tableau(p10)
R10 = mesh_matrix([(1.0, {0: 1, 1: -1}), (1.0, {0: 1, 2: -1}), (1.0, {1: 1}), (0.1, {1: -1, 2: 1}), (1.1, {2: 1})], 3)
v.check("06-05.10a", np.linalg.det(R10))
v.check("06-05.10b", -c10["V"])
v.check("06-05.10c", c10["R3"])
v.check("06-05.10d", c10["R4"])
v.check("06-05.10e", c10["RG"])

# ---- Problem 06-05.11 (kOhm, mA)
p11 = [("V", "V", "s", "0", 10.0), ("S1", "R", "s", "n1", 1.0), ("H1", "R", "n1", "0", 2.0),
       ("S2", "R", "n1", "n2", 1.0), ("H2", "R", "n2", "0", 2.0), ("S3", "R", "n2", "n3", 1.0), ("H3", "R", "n3", "0", 2.0)]
e11, c11, _ = tableau(p11)
R11 = mesh_matrix([(1, {0: 1}), (2, {0: 1, 1: -1}), (1, {1: 1}), (2, {1: 1, 2: -1}), (1, {2: 1}), (2, {2: 1})], 3)
v.check("06-05.11a", np.linalg.det(R11))
v.check("06-05.11b", c11["S1"])
v.check("06-05.11c", c11["S2"])
v.check("06-05.11d", c11["S3"])
v.check("06-05.11e", e11["n3"])
v.check("06-05.11f", e11["n1"])
v.check("06-05.11g", e11["n2"])
v.check("06-05.11h", 10.0 / c11["S1"])

# ---- Problem 06-05.12: K3,3
k33 = [("Vs", "V", "1", "x", 10.0), ("Rs", "R", "x", "4", 1.0)]
k33 += [(f"R{a}{b}", "R", str(a), "0" if b == 6 else str(b), 1.0)      # node 6 is the reference
        for a in (1, 2, 3) for b in (4, 5, 6) if (a, b) != (1, 4)]
_, c12, _ = tableau(k33)
v.check("06-05.12a", 9 - 6 + 1)
v.check("06-05.12b", c12["R25"])                # link 2-5 carries loop L25 alone, referenced 2 -> 5
v.check("06-05.12c", -c12["Vs"])
v.check("06-05.12d", -10.0 * c12["Vs"])
v.check("06-05.12e", 10.0 / -c12["Vs"])
v.check("06-05.12f", 10.0 / -c12["Vs"] - 1.0)
k33_edges = [(a - 1, b - 1, 1.0) for a in (1, 2, 3) for b in (4, 5, 6)]
re = [r_eff(k33_edges, 6, p, q) for p, q, _ in k33_edges]
v.check("06-05.12g", re[0])
v.assert_true("06-05.12 Foster's theorem, K3,3", abs(sum(re) - 5) < 1e-9)
v.assert_true("06-05.12 K3,3 nonplanar (bipartite, b > 2n - 4)",
              is_bipartite(6, [(p, q) for p, q, _ in k33_edges]) and len(k33_edges) > 2 * 6 - 4)

# ---- Problem 06-05.13: the cube
cube = [(x, x ^ (1 << k), 1.0) for x in range(8) for k in range(3) if x ^ (1 << k) > x]
pos = {0: (0, 0), 1: (3, 0), 3: (3, 3), 2: (0, 3), 4: (1, 1), 5: (2, 1), 7: (2, 2), 6: (1, 2)}   # square in square
crossings = sum(segments_cross(pos[a], pos[b], pos[c], pos[d]) for (a, b, _), (c, d, _) in combinations(cube, 2))
v.assert_true("06-05.13 square-in-square drawing has no crossings", crossings == 0)
v.check("06-05.13a", len(cube) - 8 + 1)
v.check("06-05.13b", 2 * 8 - 4)
v.assert_true("06-05.13 cube plus antipodal edge is bipartite with 13 edges",
              is_bipartite(8, [(a, b) for a, b, _ in cube] + [(0, 7)]) and len(cube) + 1 > 2 * 8 - 4)
v.check("06-05.13c", r_eff(cube, 8, 0, 7))
v.check("06-05.13d", r_eff(cube, 8, 0, 1))
v.check("06-05.13e", r_eff(cube, 8, 0, 3))
v.assert_true("06-05.13 Foster's theorem, cube", abs(sum(r_eff(cube, 8, a, b) for a, b, _ in cube) - 7) < 1e-9)

# ---- Problem 06-05.14
off = 0.005 * 4.0
lsb16 = 5.0 / 2 ** 16
v.check("06-05.14a", 1e3 * off)
v.check("06-05.14b", off / lsb12)
v.check("06-05.14c", 1e6 * lsb16)
v.check("06-05.14d", off / lsb16)
v.check("06-05.14e", 1e6 * 0.005 * 0.002)
v.check("06-05.14f", 0.005 * 0.002 / lsb16)

# ================================================================ lab
v.check("Lab 06-05.a", R2m.max())
v.check("Lab 06-05.b", (4 - 1) - 2)


def shared_offset(Im):
    els = [("V", "V", "s", "0", 5.0), ("r1", "R", "s", "p", r_tr), ("Im", "I", "p", "g", Im),
           ("r2", "R", "s", "q", r_tr), ("Rs", "R", "q", "g", Rs), ("Rg", "R", "g", "0", Rg)]
    e, _, _ = tableau(els)
    return e["g"]


v.check("Lab 06-05.c", 1e3 * shared_offset(3.0))
v.check("Lab 06-05.d", shared_offset(3.0) / lsb12)
v.check("Lab 06-05.e", (shared_offset(3.0) - shared_offset(0.0)) / 3.0 / lsb12)
v.check("Lab 06-05.f", Rg * 5.0 / (r_tr + Rs + Rg) / lsb12)

sys.exit(v.finish())
