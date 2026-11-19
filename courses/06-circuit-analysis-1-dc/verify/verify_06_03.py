#!/usr/bin/env python3
"""Verify every number published in chapter 06-03, its solutions and its lab handout.

Independent routes: every network is solved by a general nodal solver written here (a
conductance matrix built from the branch list), not by series-parallel reduction or delta-wye
conversion as in the text; equation counts come from the rank of the incidence matrix and of
the loop matrix; bridge outputs from the exact divider expressions evaluated numerically.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-03", C_DIR / "chapters" / "06-03-kirchhoffs-laws.md",
                        C_DIR / "solutions" / "06-03-solutions.md", C_DIR / "labs" / "06-03-lab" / "README.md")


def nodal(resistors, vsrc=None, isrc=None):
    """Solve a network: resistors [(a, b, R)], one voltage source (plus, minus, V) and/or current
    sources [(into_node, amps)]. Ground is "0". Returns node voltages and the source current
    delivered out of the voltage source's + terminal."""
    nodes = sorted({n for a, b, _ in resistors for n in (a, b) if n != "0"}
                   | ({vsrc[0], vsrc[1]} - {"0"} if vsrc else set()))
    idx = {n: k for k, n in enumerate(nodes)}
    m = len(nodes) + (1 if vsrc else 0)
    A = np.zeros((m, m))
    z = np.zeros(m)
    for a, b, r in resistors:
        for p, q in ((a, b), (b, a)):
            if p != "0":
                A[idx[p], idx[p]] += 1 / r
                if q != "0":
                    A[idx[p], idx[q]] -= 1 / r
    for node, amps in (isrc or []):
        z[idx[node]] += amps
    if vsrc:
        p, q, val = vsrc
        k = len(nodes)
        if p != "0":
            A[idx[p], k] -= 1      # source current j flows out of the + terminal into node p
            A[k, idx[p]] += 1
        if q != "0":
            A[idx[q], k] += 1
            A[k, idx[q]] -= 1
        z[k] = val
    x = np.linalg.solve(A, z)
    volts = {"0": 0.0, **{n: x[idx[n]] for n in nodes}}
    i_out = x[-1] if vsrc else 0.0                                          # current out of the + terminal
    return volts, i_out


def current(volts, a, b, r):
    return (volts[a] - volts[b]) / r


# ---------------------------------------------------------------- theory
v.check("T 06-03.a", 1 / (1 / 12 + 1 / 6))
# an equal wye of R_Y between two terminals gives 2 R_Y; the equal delta of 30 gives 30 || 60 = 20 -> R_Y = 10
volts_d, _ = nodal([("a", "0", 30.0), ("0", "c", 30.0), ("c", "a", 30.0)], isrc=[("a", 1.0)])
v.check("T 06-03.b", volts_d["a"] / 2)

# ---------------------------------------------------------------- examples
v.check("Ex 06-03.1a", 3 + (-0.5) - 1)
v.check("Ex 06-03.1b", 12 - 5)
ex2 = [("a", "p", 4.0), ("p", "0", 12.0), ("p", "m", 2.0), ("m", "0", 4.0)]
vv, i2 = nodal(ex2, vsrc=("a", "0", 24.0))
v.check("Ex 06-03.2a", 24 / i2)
v.check("Ex 06-03.2b", i2)
v.check("Ex 06-03.2c", vv["p"])
v.check("Ex 06-03.2d", current(vv, "p", "0", 12.0))
v.check("Ex 06-03.2e", current(vv, "p", "m", 2.0))
v.check("Ex 06-03.2f", vv["m"])
v.check("Ex 06-03.2g", 24 * i2)
v.assert_true("Example 06-03.2 power balance", abs(24 * i2 - sum(current(vv, a, b, r) ** 2 * r for a, b, r in ex2)) < 1e-9)
div = [("b", "o", 100e3), ("o", "0", 33e3)]
for key, vin in (("a", 12.6), ("b", 10.5)):
    vd, _ = nodal(div, vsrc=("b", "0", vin))
    v.check(f"Ex 06-03.3{key}", vd["o"])
vd, i3 = nodal(div, vsrc=("b", "0", 12.6))
v.check("Ex 06-03.3c", i3 * 1e6)
vl, _ = nodal(div + [("o", "0", 1e6)], vsrc=("b", "0", 12.6))
v.check("Ex 06-03.3d", vl["o"])
v.check("Ex 06-03.3e", 100 * (1 - vl["o"] / vd["o"]))
vt, _ = nodal([("0", "o", 100e3), ("o", "0", 33e3)], isrc=[("o", 1.0)])   # test current into the output, source shorted
v.check("Ex 06-03.3f", vt["o"] / 1e3)
dR = 350 * 2.0 * 1000e-6
v.check("Ex 06-03.4a", dR)
vb, _ = nodal([("e", "l", 350.0), ("l", "0", 350 + dR), ("e", "r", 350.0), ("r", "0", 350.0)], vsrc=("e", "0", 2.5))
out4 = vb["l"] - vb["r"]
v.check("Ex 06-03.4b", out4 * 1e3)
v.check("Ex 06-03.4c", 2.5 / 4 * dR / 350 * 1e3)
v.check("Ex 06-03.4d", 100 * (2.5 / 4 * dR / 350 / out4 - 1))
v.check("Ex 06-03.4e", vb["l"] ** 2 / (350 + dR) * 1e3)                    # the gauge itself
xs = 2.0 * 1000e-6
vf, _ = nodal([("e", "l", 350 * (1 - xs)), ("l", "0", 350 * (1 + xs)), ("e", "r", 350 * (1 + xs)), ("r", "0", 350 * (1 - xs))], vsrc=("e", "0", 2.5))
v.check("Ex 06-03.4f", (vf["l"] - vf["r"]) * 1e3)
ex5 = [("a", "c", 10.0), ("a", "d", 20.0), ("c", "d", 30.0), ("c", "0", 40.0), ("d", "0", 50.0)]
v.check("Ex 06-03.5a", 10 * 20 / 60)
v5, i5 = nodal(ex5, vsrc=("a", "0", 10.0))
v.check("Ex 06-03.5b", 10 / i5)
v.check("Ex 06-03.5c", i5)
v.check("Ex 06-03.5d", v5["c"])
v.check("Ex 06-03.5e", v5["d"])
v.check("Ex 06-03.5f", current(v5, "c", "d", 30.0) * 1e3)

# ---------------------------------------------------------------- solutions
inc = np.array([[1, 1, 0, 0, 0, -1], [-1, 0, 1, 1, 0, 0], [0, -1, -1, 0, 1, 0], [0, 0, 0, -1, -1, 1]])   # 4 nodes x 6 branches
rank = np.linalg.matrix_rank(inc)
v.check("06-03.1a", rank)
v.check("06-03.1b", inc.shape[1] - rank)
v.check("06-03.1c", 2 * inc.shape[1])
v.check("06-03.2a", 1 + 2.2 + 4.7)
v.check("06-03.2b", 1 / (3 / 1e3))
v.check("06-03.2c", 1 / (1 / 2 + 1 / 3) + 1.8)
v.check("06-03.2d", 1 / (1 / 10 + 1 / 15 + 1 / 30))
v3, _ = nodal([("s", "o", 6.8e3), ("o", "0", 3.3e3)], vsrc=("s", "0", 5.0))
v.check("06-03.3a", v3["o"])
vi, _ = nodal([("n", "0", 470.0), ("n", "0", 1000.0)], isrc=[("n", 10e-3)])
v.check("06-03.3b", vi["n"] / 470 * 1e3)
v.check("06-03.4a", 10.0 * (3.30 / 0.800 - 1))
v.check("06-03.4b", 0.8 * (1 + 31.6 / 10.0))
v.check("06-03.4c", 0.8 * (1 + 30.9 / 10.0))
outs = [0.8 * (1 + 31.6 * a / (10.0 * b)) for a in (0.99, 1.01) for b in (0.99, 1.01)]
v.check("06-03.4d", max(outs))
v.check("06-03.4e", min(outs))
for keys, rm in ((("a", "b"), 10e6), (("c", "d"), 1e6)):
    vm, _ = nodal([("s", "o", 100e3), ("o", "0", 100e3), ("o", "0", rm)], vsrc=("s", "0", 10.0))
    v.check(f"06-03.5{keys[0]}", vm["o"])
    v.check(f"06-03.5{keys[1]}", 100 * (1 - vm["o"] / 5.0))
p6 = [("a", "p", 2.0), ("p", "q", 6.0), ("p", "q", 3.0), ("q", "0", 1.0)]
v6, i6 = nodal(p6, vsrc=("a", "0", 12.0))
v.check("06-03.6a", 12 / i6)
v.check("06-03.6b", i6)
v.check("06-03.6c", current(v6, "p", "q", 6.0))
v.check("06-03.6d", current(v6, "p", "q", 3.0))
v.check("06-03.6e", current(v6, "a", "p", 2.0) ** 2 * 2.0)
v.check("06-03.6f", (v6["p"] - v6["q"]) ** 2 / 3.0)
v.check("06-03.7a", 1000 * 1372.5 / 1000)
v7, _ = nodal([("e", "A", 1000.0), ("A", "0", 1372.5), ("e", "B", 1000.0), ("B", "0", 1373.5)], vsrc=("e", "0", 5.0))
v.check("06-03.7b", (v7["A"] - v7["B"]) * 1e3)
v8, _ = nodal([("e", "A", 1000.0), ("A", "0", 1010.0), ("e", "B", 1000.0), ("B", "0", 1000.0)], vsrc=("e", "0", 10.0))
v.check("06-03.8a", (v8["A"] - v8["B"]) * 1e3)
v.check("06-03.8b", 10 / 4 * 0.010 * 1e3)


def r_between(resistors, a, b):
    """Resistance between a and b: ground b, inject 1 A at a."""
    grounded = [(("0" if x == b else x), ("0" if y == b else y), r) for x, y, r in resistors]
    vv_, _ = nodal(grounded, isrc=[(a, 1.0)])
    return vv_[a]


delta = [("a", "b", 10.0), ("b", "c", 20.0), ("c", "a", 30.0)]
for key, (term, others) in zip("abc", (("a", ("b", "c")), ("b", ("a", "c")), ("c", ("a", "b")))):
    # wye resistor at a terminal = (R_xy + R_xz - R_yz)/2 from the three pairwise delta resistances
    rxy = r_between(delta, term, others[0])
    rxz = r_between(delta, term, others[1])
    ryz = r_between(delta, others[0], others[1])
    v.check(f"06-03.9{key}", (rxy + rxz - ryz) / 2)
wye = [("a", "n", 10.0), ("b", "n", 20.0), ("c", "n", 30.0)]
# delta resistor between x and y: drive x with 1 A, ground y, short the third terminal to y
for key, (x, y, z) in zip("def", (("a", "b", "c"), ("b", "c", "a"), ("c", "a", "b"))):
    # Y->Delta via short-circuit admittance: the delta element between x and y equals -1/Y_xy
    nodes = ["a", "b", "c", "n"]
    Gw = np.zeros((4, 4))
    for p, q, r in wye:
        ip, iq = nodes.index(p), nodes.index(q)
        Gw[ip, ip] += 1 / r
        Gw[iq, iq] += 1 / r
        Gw[ip, iq] -= 1 / r
        Gw[iq, ip] -= 1 / r
    # eliminate the internal node n (Schur complement) to get the 3x3 terminal admittance matrix
    Y = Gw[:3, :3] - np.outer(Gw[:3, 3], Gw[3, :3]) / Gw[3, 3]
    v.check(f"06-03.9{key}", -1 / Y[nodes.index(x), nodes.index(y)])
v.check("06-03.9g", r_between(delta, "a", "b"))
g10 = np.array([1 / 0.020, 1 / 0.025, 1 / 0.030])
vw, _ = nodal([("p", "0", 0.020), ("p", "0", 0.025), ("p", "0", 0.030)], isrc=[("p", 6.0)])
for key, r in zip("abc", (0.020, 0.025, 0.030)):
    v.check(f"06-03.10{key}", vw["p"] / r)
v.check("06-03.10d", vw["p"] ** 2 / 0.020)
a11, t11, V11 = 2.0 * 500e-6, 5e-4, 2.5
q11, _ = nodal([("e", "l", 350.0), ("l", "0", 350 * (1 + a11 + t11)), ("e", "r", 350.0), ("r", "0", 350.0)], vsrc=("e", "0", V11))
v.check("06-03.11a", (q11["l"] - q11["r"]) * 1e3)
v.check("06-03.11b", (q11["l"] - q11["r"]) / (V11 * 2.0 / 4) * 1e6)
for key, t in (("c", t11), ("d", 0.0)):
    h11, _ = nodal([("e", "l", 350 * (1 + t)), ("l", "0", 350 * (1 + a11 + t)), ("e", "r", 350.0), ("r", "0", 350.0)], vsrc=("e", "0", V11))
    v.check(f"06-03.11{key}", (h11["l"] - h11["r"]) * 1e3)
ladder = [("n1", "n2", 10e3), ("n2", "n3", 10e3), ("n3", "n4", 10e3),
          ("n1", "0", 20e3), ("n2", "0", 20e3), ("n3", "0", 20e3), ("n4", "0", 20e3), ("n4", "0", 20e3)]
vlad, iin = nodal(ladder, vsrc=("n1", "0", 5.0))
v.check("06-03.12a", 5.0 / iin / 1e3)
v.check("06-03.12b", iin * 1e3)
v.check("06-03.12c", vlad["n4"] / 20e3 * 1e3)
v.check("06-03.12d", (vlad["n1"] + vlad["n3"] + vlad["n4"]) / 20e3 * 1e3)
net13 = [("a", "c", 6.0), ("a", "d", 12.0), ("c", "d", 6.0), ("c", "0", 12.0), ("d", "0", 6.0)]
v13, _ = nodal(net13, isrc=[("a", 1.0)])
v.check("06-03.13a", v13["a"])
v.check("06-03.13b", current(v13, "c", "d", 6.0))
v.check("06-03.14a", 1.5 * int(np.ceil(7 / 1.5)))
v.check("06-03.14b", 2 - 0.5 + 1)
v14, _ = nodal([("0", "o", 1.0), ("0", "o", 1.0)], isrc=[("o", 1.0)])       # sources shorted: R seen at o
v.check("06-03.14c", v14["o"])

# ---------------------------------------------------------------- lab
v.check("Lab 06-03.a", 4 - 1)
v.check("Lab 06-03.b", 6 - 4 + 1)
rs = 100e3 * 33e3 / 133e3
v.check("Lab 06-03.c", rs * (1 / 1e-3 - 1) / 1e6)
x = 2.0 * 5000e-6
v.check("Lab 06-03.d", 100 * (2.5 * ((1 + x) / (2 + x) - 0.5) / (2.5 * x / 4) - 1))

sys.exit(v.finish())
