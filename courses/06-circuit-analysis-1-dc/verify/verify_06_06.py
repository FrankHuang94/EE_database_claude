#!/usr/bin/env python3
"""Verify every number published in chapter 06-06, its solutions and its lab handout.

Independent routes. The text solves circuits with dependent sources by nodal and mesh analysis
(substituting controlling variables by hand). This script instead uses a sparse-tableau solver
extended with all four dependent sources, whose element laws refer directly to any node voltage
or branch current (no sense sources, no substitution). Port resistances come from explicit test
sources; matrix entries and determinants from short-circuit admittance measurements (drive one
node to 1 V, hold the others at 0 V, read the source currents); singular gains from root-finding
on that determinant.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-06", C_DIR / "chapters" / "06-06-dependent-sources.md",
                        C_DIR / "solutions" / "06-06-solutions.md", C_DIR / "labs" / "06-06-lab" / "README.md")

K_B, Q_E = 1.380649e-23, 1.602176634e-19
VT = K_B * 300.0 / Q_E


def tableau(elements):
    """Sparse tableau with dependent sources. Each element is (name, kind, a, b, value) where
    branch current flows a -> b through the element and branch voltage is v_a - v_b:
      R: v = value * i;  I: i = value;  V: v = value;
      G: i = g * (v_c - v_d) with value = (c, d, g);   E: v = mu * (v_c - v_d) with value = (c, d, mu);
      F: i = beta * i_ctrl with value = (ctrl, beta);  H: v = r * i_ctrl with value = (ctrl, r)."""
    nodes = sorted({n for _, _, a, b, _ in elements for n in (a, b) if n != "0"})
    nn, nb = len(nodes), len(elements)
    idx = {n: k for k, n in enumerate(nodes)}
    bidx = {el[0]: k for k, el in enumerate(elements)}
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

    def node_col(n):
        return None if n == "0" else idx[n]

    for k, (_, kind, _, _, val) in enumerate(elements):
        r = nn + nb + k
        ci, cv = nn + k, nn + nb + k
        if kind == "R":
            M[r, cv], M[r, ci] = 1.0, -val
        elif kind == "I":
            M[r, ci], z[r] = 1.0, val
        elif kind == "V":
            M[r, cv], z[r] = 1.0, val
        elif kind in "GE":
            c, d, gain = val
            M[r, ci if kind == "G" else cv] = 1.0
            for node, sgn in ((c, -1.0), (d, 1.0)):
                if node_col(node) is not None:
                    M[r, node_col(node)] += sgn * gain
        elif kind in "FH":
            ctrl, gain = val
            M[r, ci if kind == "F" else cv] = 1.0
            M[r, nn + bidx[ctrl]] -= gain
        else:
            raise ValueError(kind)
    x = np.linalg.solve(M, z)
    e = {"0": 0.0, **{n: x[idx[n]] for n in nodes}}
    cur = {el[0]: x[nn + k] for k, el in enumerate(elements)}
    vol = {el[0]: x[nn + nb + k] for k, el in enumerate(elements)}
    return e, cur, vol


def P(cur, vol, name):
    return cur[name] * vol[name]


def admittance(elements, nodes, held=()):
    """Short-circuit admittance matrix of a network (independent sources removed by the caller)."""
    n = len(nodes)
    G = np.zeros((n, n))
    for j in range(n):
        els = list(elements) + [(f"Vt{m}", "V", nm, "0", 1.0 if m == j else 0.0) for m, nm in enumerate(nodes)]
        els += [(f"Vh{m}", "V", nm, "0", 0.0) for m, nm in enumerate(held)]
        _, cur, _ = tableau(els)
        for k in range(n):
            G[k, j] = -cur[f"Vt{k}"]
    return G


def port_resistance(elements, a, b="0"):
    """Resistance seen between a and b: inject 1 A from b to a and read v_a - v_b."""
    e, _, _ = tableau(list(elements) + [("Itest", "I", b, a, 1.0)])
    return e[a] - e[b]


# ================================================================ chapter
# ---- Example 06-06.1 (kOhm, mA, V, mS)
ex1_net = [("R1", "R", "1", "0", 2.0), ("R12", "R", "1", "2", 4.0), ("R2", "R", "2", "0", 4.0),
           ("G", "G", "2", "0", ("1", "0", 1.0))]
e1, c1, vb1 = tableau(ex1_net + [("Is", "I", "0", "1", 1.0)])
G1 = admittance(ex1_net, ["1", "2"])
v.check("Ex 06-06.1a", e1["1"])
v.check("Ex 06-06.1b", e1["2"])
v.check("Ex 06-06.1c", e1["2"] / e1["1"])
v.check("Ex 06-06.1d", np.linalg.det(G1))
v.check("Ex 06-06.1e", -P(c1, vb1, "Is"))
v.check("Ex 06-06.1f", -P(c1, vb1, "G"))
v.check("Ex 06-06.1g", sum(P(c1, vb1, r) for r in ("R1", "R12", "R2")))
v.check("Ex 06-06.1h", G1[1, 0])
v.assert_true("Ex 06-06.1 matrix not symmetric", not np.allclose(G1, G1.T))


# ---- Example 06-06.2: degenerated MOSFET, per volt of input (kOhm, mA)
def cs_stage(gm, ro, RD, RS, vin=1.0):
    return [("Vin", "V", "g", "0", vin), ("Gm", "G", "d", "s", ("g", "s", gm)), ("ro", "R", "d", "s", ro),
            ("RD", "R", "d", "0", RD), ("RS", "R", "s", "0", RS)]


e2, c2, _ = tableau(cs_stage(2.0, 50.0, 10.0, 1.0))
v.check("Ex 06-06.2a", e2["d"])
v.check("Ex 06-06.2b", e2["s"])
v.check("Ex 06-06.2c", c2["Gm"])
v.check("Ex 06-06.2h", -e2["d"] / 10.0)               # current from R_D into the drain
v.check("Ex 06-06.2i", c2["Gm"] - (-e2["d"] / 10.0))
v.check("Ex 06-06.2d", -2.0 * 10.0 / (1 + 2.0 * 1.0))
e2n, _, _ = tableau(cs_stage(2.0, 50.0, 10.0, 1e-9))
v.check("Ex 06-06.2e", e2n["d"])
G2 = admittance(cs_stage(2.0, 50.0, 10.0, 1.0)[1:], ["d", "s"], held=["g"])
v.check("Ex 06-06.2f", np.linalg.det(G2))
v.check("Ex 06-06.2g", 1 / (1 / 10.0 + 1 / 50.0))


# ---- Example 06-06.3: bipolar stage (kOhm, mV, uA)
def ce_stage(beta, rpi, RC, RE, Rs, vs):
    els = [("Vs", "V", "in", "0", vs), ("Rs", "R", "in", "b", Rs), ("rpi", "R", "b", "e", rpi),
           ("F", "F", "c", "e", ("rpi", beta)), ("RC", "R", "c", "0", RC)]
    els.append(("RE", "R", "e", "0", RE) if RE > 0 else ("RE", "V", "e", "0", 0.0))
    return els


e3, c3, _ = tableau(ce_stage(100, 2.5, 4.0, 0.1, 1.0, 10.0))
v.check("Ex 06-06.3a", 10.0 / c3["Rs"])
v.check("Ex 06-06.3b", c3["rpi"])                  # mV/kOhm = uA
v.check("Ex 06-06.3c", e3["c"])
v.check("Ex 06-06.3d", e3["c"] / 10.0)
base_net = [("rpi", "R", "b", "e", 2.5), ("F", "F", "c", "e", ("rpi", 100)), ("RC", "R", "c", "0", 4.0),
            ("RE", "R", "e", "0", 0.1)]
v.check("Ex 06-06.3e", port_resistance(base_net, "b"))
e3n, _, _ = tableau(ce_stage(100, 2.5, 4.0, 0.0, 1.0, 10.0))
v.check("Ex 06-06.3f", e3n["c"] / 10.0)


# ---- Example 06-06.4
def miller(mu, Rf=100.0):
    return [("Rf", "R", "n", "o", Rf), ("E", "E", "o", "0", ("n", "0", mu))]


v.check("Ex 06-06.4a", port_resistance(miller(-99.0), "n"))
v.check("Ex 06-06.4b", port_resistance(miller(2.0), "n"))
_, c4, _ = tableau(miller(2.0) + [("Vt", "V", "n", "0", 1.0)])
v.check("Ex 06-06.4c", 1e3 * c4["Vt"])            # mA -> uA, current into the test source's + terminal


# ---- Example 06-06.5: op-amp model (kOhm, V, mA)
def noninv(Aol, Ro=0.1, vs=1.0):
    return [("Vs", "V", "p", "0", vs), ("Rid", "R", "p", "n", 1000.0), ("R1", "R", "n", "0", 1.0),
            ("R2", "R", "n", "o", 9.0), ("RL", "R", "o", "0", 2.0), ("Ro", "R", "o", "x", Ro),
            ("E", "E", "x", "0", ("p", "n", Aol))]


e5, c5, _ = tableau(noninv(1e5))
v.check("Ex 06-06.5a", e5["o"])
v.check("Ex 06-06.5b", 1e6 * (e5["p"] - e5["n"]))
v.check("Ex 06-06.5c", 1e6 * c5["Rid"])           # mA -> nA
v.check("Ex 06-06.5d", 1e6 * (10 - e5["o"]) / 10)
v.check("Ex 06-06.5e", 1e5 / (1 + 1e5 * 0.1))
v.check("Ex 06-06.5f", 1e6 * (10 - 1e5 / (1 + 1e5 * 0.1)) / 10)
Rp5 = 1 / (1 / 2.0 + 1 / (1.0 + 9.0))
A_eff = 1e5 * Rp5 / (Rp5 + 0.1)
v.check("Ex 06-06.5g", A_eff)
v.check("Ex 06-06.5h", 1e6 / (A_eff * 0.1))
v.assert_true("Ex 5: hand loading estimate within 1 ppm of the full solve", abs(1e6 / (A_eff * 0.1) - 1e6 * (10 - e5["o"]) / 10) < 1.0)

# ================================================================ solutions
v.check("06-06.1a", 1e3 * 0.04)
v.check("06-06.1b", 5000 / 1e3)
v.check("06-06.1c", 80)
v.check("06-06.1d", -20)

# ---- Problem 06-06.2 (Ohm, V, A)
p2 = [("Vs", "V", "s", "0", 2.0), ("R1", "R", "s", "x", 1000.0), ("R2", "R", "x", "0", 3000.0),
      ("E", "E", "y", "0", ("x", "0", 10.0)), ("Ro", "R", "y", "L", 100.0), ("RL", "R", "L", "0", 500.0)]
e2p, c2p, vb2p = tableau(p2)
v.check("06-06.2a", e2p["x"])
v.check("06-06.2b", e2p["L"])
v.check("06-06.2c", P(c2p, vb2p, "RL"))
v.check("06-06.2d", -P(c2p, vb2p, "E"))
v.check("06-06.2e", -1e3 * P(c2p, vb2p, "Vs"))

# ---- Problem 06-06.3 (kOhm, mA)
p3_net = [("R1", "R", "1", "0", 5.0), ("R12", "R", "1", "2", 10.0), ("R2", "R", "2", "0", 2.0),
          ("F", "F", "0", "2", ("R1", 4.0))]
e3p, c3p, vb3p = tableau(p3_net + [("Is", "I", "0", "1", 2.0)])
G3 = admittance(p3_net, ["1", "2"])
v.check("06-06.3a", np.linalg.det(G3))
v.check("06-06.3b", e3p["1"])
v.check("06-06.3c", e3p["2"])
v.check("06-06.3d", c3p["R1"])
v.check("06-06.3e", c3p["F"])
v.check("06-06.3f", -P(c3p, vb3p, "Is"))
v.check("06-06.3g", -P(c3p, vb3p, "F"))
v.check("06-06.3h", sum(P(c3p, vb3p, r) for r in ("R1", "R12", "R2")))


# ---- Problem 06-06.4
def ex1_with(g):
    return [("R1", "R", "1", "0", 2.0), ("R12", "R", "1", "2", 4.0), ("R2", "R", "2", "0", 4.0),
            ("G", "G", "2", "0", ("1", "0", g))]


g_sing = brentq(lambda g: np.linalg.det(admittance(ex1_with(g), ["1", "2"])), -3.0, 0.0)
v.check("06-06.4a", g_sing)
v.check("06-06.4b", np.linalg.det(admittance(ex1_with(-1.0), ["1", "2"])))
e4p, _, _ = tableau(ex1_with(-1.0) + [("Is", "I", "0", "1", 1.0)])
v.check("06-06.4c", e4p["1"])
v.check("06-06.4d", e4p["2"])
for g in (-0.5, 0.0, 1.0, 2.0):
    eg, _, _ = tableau(ex1_with(g) + [("Is", "I", "0", "1", 1.0)])
    v.assert_true(f"06-06.4 formulas at g = {g}", abs(eg["2"] / eg["1"] - (0.5 - 2 * g)) < 1e-12
                  and abs(eg["1"] - 1 / (0.625 + 0.5 * g)) < 1e-12)

# ---- Problem 06-06.5 (Ohm, V, A)
p5 = [("V10", "V", "a", "0", 10.0), ("R1", "R", "a", "m", 2.0), ("R2", "R", "m", "0", 4.0),
      ("R3", "R", "m", "c", 6.0), ("H", "H", "0", "c", ("R1", 3.0))]
e5p, c5p, vb5p = tableau(p5)
Rmesh = np.array([[6.0, -4.0], [-4.0 - 3.0, 10.0]])
v.check("06-06.5a", np.linalg.det(Rmesh))
v.check("06-06.5b", c5p["R1"])
v.check("06-06.5c", c5p["R3"])
v.check("06-06.5d", -P(c5p, vb5p, "V10"))
v.check("06-06.5e", -P(c5p, vb5p, "H"))
v.check("06-06.5f", sum(P(c5p, vb5p, r) for r in ("R1", "R2", "R3")))
v.assert_true("06-06.5 mesh matrix reproduces the currents",
              np.allclose(np.linalg.solve(Rmesh, [10.0, 0.0]), [c5p["R1"], c5p["R3"]]))

# ---- Problem 06-06.6 (kOhm, mS)
p6 = [("Vg", "V", "g", "0", 1.0), ("Gm", "G", "d", "0", ("g", "0", 4.0)), ("ro", "R", "d", "0", 25.0),
      ("RD", "R", "d", "0", 5.0), ("RL", "R", "d", "0", 20.0)]
e6p, _, _ = tableau(p6)
v.check("06-06.6a", 4.0 * 25.0)
v.check("06-06.6b", -e6p["d"] / 4.0)
v.check("06-06.6c", e6p["d"])
v.check("06-06.6d", port_resistance([("Vg", "V", "g", "0", 0.0), ("Gm", "G", "d", "0", ("g", "0", 4.0)),
                                     ("ro", "R", "d", "0", 25.0), ("RD", "R", "d", "0", 5.0)], "d"))

# ---- Problem 06-06.7
gm7 = 1e-3 / VT * 1e3                              # mS at 1 mA
v.check("06-06.7a", gm7)
v.check("06-06.7b", 120 / gm7)
v.check("06-06.7c", 60 / gm7)


def ce_gain(beta, RE, Rs):
    e, _, _ = tableau(ce_stage(beta, beta / gm7, 5.0, RE, Rs, 1.0))
    return e["c"]


g120, g60 = ce_gain(120, 0.0, 2.0), ce_gain(60, 0.0, 2.0)
v.check("06-06.7d", g120)
v.check("06-06.7e", g60)
v.check("06-06.7f", 100 * (abs(g120) - abs(g60)) / abs(g120))
h120, h60 = ce_gain(120, 0.2, 2.0), ce_gain(60, 0.2, 2.0)
v.check("06-06.7g", h120)
v.check("06-06.7h", h60)
v.check("06-06.7i", 100 * (abs(h120) - abs(h60)) / abs(h120))
v.check("06-06.7j", port_resistance([("rpi", "R", "b", "e", 120 / gm7), ("F", "F", "c", "e", ("rpi", 120)),
                                     ("RC", "R", "c", "0", 5.0), ("RE", "R", "e", "0", 0.2)], "b"))
v.check("06-06.7k", ce_gain(120, 0.2, 1e-12))

# ---- Problem 06-06.8 (gate held at 0)
p8 = [("Vg", "V", "g", "0", 0.0), ("Gm", "G", "d", "s", ("g", "s", 2.0)), ("ro", "R", "d", "s", 50.0),
      ("RS", "R", "s", "0", 1.0)]
v.check("06-06.8a", port_resistance(p8, "d"))

# ---- Problem 06-06.9 (kOhm, mV)
p9 = [("Vs", "V", "s", "0", 10.0), ("Rs", "R", "s", "n", 10.0), ("Rf", "R", "n", "o", 1000.0),
      ("E", "E", "o", "0", ("n", "0", -200.0))]
e9p, _, _ = tableau(p9)
v.check("06-06.9a", port_resistance(p9[2:], "n"))
v.check("06-06.9b", e9p["n"])
v.check("06-06.9c", e9p["o"])
v.check("06-06.9d", e9p["o"] / 10.0)


# ---- Problem 06-06.10 (kOhm, mA)
def neg_node(Rn):
    e, _, _ = tableau([("I", "I", "0", "n", 1.0), ("R", "R", "n", "0", 10.0),
                       ("G", "G", "0", "n", ("n", "0", 1.0 / Rn))])     # pushes g*v into the node
    return e["n"]


v.check("06-06.10a", neg_node(20.0))
v.check("06-06.10b", neg_node(12.5))
v.check("06-06.10c", 1e3 / 20.0)                   # 1/R_n in uS
v.assert_true("06-06.10 VCCS acts as -20 kOhm",
              abs(port_resistance([("G", "G", "0", "n", ("n", "0", 0.05))], "n") + 20.0) < 1e-9)

# ---- Problem 06-06.11 (kOhm, V)
p11 = [("Vi", "V", "i", "0", 1.0), ("R1", "R", "i", "n", 1.0), ("R2", "R", "n", "o", 10.0),
       ("E", "E", "o", "0", ("0", "n", 1e4))]
e11, c11, _ = tableau(p11)
v.check("06-06.11a", e11["o"])
v.check("06-06.11b", 1e6 * (10 + e11["o"]) / 10)
v.check("06-06.11c", 1e3 * e11["n"])
v.check("06-06.11d", 1.0 / c11["R1"])
v.assert_true("06-06.11 closed form", abs(e11["o"] + 10 / (1 + 11 / 1e4)) < 1e-12)

# ---- Problem 06-06.12 (Ohm, V, A)
p12 = [("V1", "V", "1", "0", 1.0), ("R1", "R", "1", "2", 1000.0), ("R2", "R", "2", "0", 1000.0),
       ("G1", "G", "3", "0", ("2", "0", 0.01)), ("R3", "R", "3", "0", 2000.0)]
e12, c12, _ = tableau(p12)
v.check("06-06.12a", e12["2"])
v.check("06-06.12b", e12["3"])
v.check("06-06.12c", 1e3 * c12["V1"])
v.check("06-06.12d", e12["3"] / e12["1"])

# ---- Problem 06-06.13 (kOhm, mS)
p13 = [("Vg", "V", "g", "0", 1.0), ("Gm", "G", "0", "s", ("g", "s", 2.0)), ("ro", "R", "s", "0", 50.0),
       ("RS", "R", "s", "0", 2.0)]
e13, _, _ = tableau(p13)
v.check("06-06.13a", 1 / (1 / 50.0 + 1 / 2.0))
v.check("06-06.13b", e13["s"])
p13o = [("Vg", "V", "g", "0", 0.0)] + p13[1:]
v.check("06-06.13c", 1e3 * port_resistance(p13o, "s"))


# ---- Problem 06-06.14 (kOhm, mA, V)
def mirror(ro):
    return [("Iref", "I", "0", "r", 0.1), ("Rref", "V", "r", "0", 0.0), ("F", "F", "o", "0", ("Rref", 1.0)),
            ("ro", "R", "o", "0", ro), ("RL", "R", "vdd", "o", 20.0), ("Vdd", "V", "vdd", "0", 5.0)]


for ro, ids in ((100.0, "abc"), (1000.0, "def")):
    em, cm, _ = tableau(mirror(ro))
    v.check(f"06-06.14{ids[0]}", em["o"])
    v.check(f"06-06.14{ids[1]}", cm["RL"])
    v.check(f"06-06.14{ids[2]}", 100 * (cm["RL"] - 0.1) / 0.1)

# ================================================================ lab
v.check("Lab 06-06.a", c3["rpi"])
v.check("Lab 06-06.b", port_resistance(miller(0.5), "n"))
e_lo, _, _ = tableau(noninv(1e3))
e_hi, _, _ = tableau(noninv(1e7))
v.check("Lab 06-06.c", 100 * (10 - e_lo["o"]) / 10)
v.check("Lab 06-06.d", 1e6 * (10 - e_hi["o"]) / 10)
v.check("Lab 06-06.e", 1e5)

# ---- Problems 06-06.15 and 06-06.16 by tableau solves with H and F elements (ohms, volts, amps)
e15, c15, b15 = tableau([("V1", "V", "a", "0", 12.0), ("R4", "R", "a", "n1", 4.0), ("H", "H", "n1", "n2", ("R4", 2.0)),
                         ("R3", "R", "n1", "0", 3.0), ("R6", "R", "n2", "0", 6.0)])
v.check("06-06.15a", e15["n1"])
v.check("06-06.15b", e15["n2"])
v.check("06-06.15c", c15["R4"])
v.check("06-06.15d", P(c15, b15, "H"))
v.assert_true("06-06.15: Tellegen", abs(sum(P(c15, b15, k) for k in c15)) < 1e-9)
e16, c16, b16 = tableau([("V1", "V", "n1", "0", 10.0), ("R2", "R", "n1", "n2", 2.0), ("R3", "R", "n2", "n3", 3.0),
                         ("R4", "R", "n3", "0", 4.0), ("F", "F", "0", "n2", ("R4", 0.5))])
v.check("06-06.16a", c16["R3"])
v.check("06-06.16b", c16["R2"])
v.check("06-06.16c", e16["n2"])
v.check("06-06.16d", -P(c16, b16, "F"))
v.assert_true("06-06.16: Tellegen", abs(sum(P(c16, b16, k) for k in c16)) < 1e-9)

sys.exit(v.finish())
