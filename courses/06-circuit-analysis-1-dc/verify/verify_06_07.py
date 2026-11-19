#!/usr/bin/env python3
"""Verify every number published in chapter 06-07, its solutions and its lab handout.

Independent routes. The text uses superposition, source transformations, Millman's theorem and the
unit-output method. This script instead solves every circuit once, with all sources present, by a
sparse-tableau solver (the same one as verify_06_06.py, with dependent sources), and checks the
partial responses by re-solving with sources set to zero. Diode circuits are solved by bracketing
root-finding; the error-budget probability by numerical convolution of the error densities (not by
Monte Carlo); the ladder's golden-ratio limit by iterating the infinite-ladder recursion.
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
v = Verifier.from_files("06-07", C_DIR / "chapters" / "06-07-linearity-and-superposition.md",
                        C_DIR / "solutions" / "06-07-solutions.md", C_DIR / "labs" / "06-07-lab" / "README.md")


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


IS, VT = 1e-14, 0.025852


def diode_node(Vs, I, R=1000.0):
    return brentq(lambda x: (Vs - x) / R + I - IS * np.expm1(x / VT), -1.0, 1.0, xtol=1e-15)


# ================================================================ chapter
# RSS of uniform limits in standard deviations: limit e has sigma e/sqrt(3)
v.check("T 06-07.a", np.sqrt(3.0))


# ---- Example 06-07.1
def ex1(V=12.0, I=2.0):
    return [("V", "V", "s", "0", V), ("R1", "R", "s", "a", 4.0), ("R2", "R", "a", "0", 6.0), ("I", "I", "0", "a", I)]


e_all, c_all, vb_all = tableau(ex1())
e_v, c_v, vb_v = tableau(ex1(I=0.0))
e_i, c_i, vb_i = tableau(ex1(V=0.0))
v.check("Ex 06-07.1a", e_v["a"])
v.check("Ex 06-07.1b", e_i["a"])
v.check("Ex 06-07.1c", e_all["a"])
v.check("Ex 06-07.1d", c_v["R1"])
v.check("Ex 06-07.1e", c_all["R1"], tol=1e-12)
v.check("Ex 06-07.1f", c_all["R2"])
v.check("Ex 06-07.1g", P(c_all, vb_all, "R2"))
v.check("Ex 06-07.1h", P(c_v, vb_v, "R2") + P(c_i, vb_i, "R2"))
v.check("Ex 06-07.1i", P(c_all, vb_all, "R2") - P(c_v, vb_v, "R2") - P(c_i, vb_i, "R2"))
v.check("Ex 06-07.1j", 1 / (1 / 4.0 + 1 / 6.0))
v.check("Ex 06-07.1k", -P(c_all, vb_all, "I"))
v.assert_true("Ex 06-07.1 R1 single-source powers add to 11.52 W",
              abs(P(c_v, vb_v, "R1") + P(c_i, vb_i, "R1") - 11.52) < 1e-9 and abs(P(c_all, vb_all, "R1")) < 1e-12)


# ---- Example 06-07.2: CCVS 3*ix in series with 1 ohm from a to ground
def ex2(V=10.0, I=2.0, ccvs=3.0):
    return [("V", "V", "s", "0", V), ("R1", "R", "s", "a", 2.0), ("I", "I", "0", "a", I),
            ("R3", "R", "a", "m", 1.0), ("H", "H", "m", "0", ("R1", ccvs))]


v.check("Ex 06-07.2a", tableau(ex2(I=0.0))[0]["a"])
v.check("Ex 06-07.2b", tableau(ex2(I=0.0))[1]["R1"])
v.check("Ex 06-07.2c", tableau(ex2(V=0.0))[0]["a"])
v.check("Ex 06-07.2d", tableau(ex2(V=0.0))[1]["R1"])
v.check("Ex 06-07.2e", tableau(ex2())[0]["a"])
v.check("Ex 06-07.2f", tableau(ex2())[1]["R1"])
v.check("Ex 06-07.2g", tableau(ex2(V=0.0, ccvs=0.0))[0]["a"])

# ---- Example 06-07.3: two practical sources in parallel across 2 ohm
e3, c3, _ = tableau([("Va", "V", "ea", "0", 12.0), ("Ra", "R", "ea", "l", 4.0), ("Vb", "V", "eb", "0", 6.0),
                     ("Rb", "R", "eb", "l", 3.0), ("RL", "R", "l", "0", 2.0)])
e3o, _, _ = tableau([("Va", "V", "ea", "0", 12.0), ("Ra", "R", "ea", "l", 4.0), ("Vb", "V", "eb", "0", 6.0),
                     ("Rb", "R", "eb", "l", 3.0)])                     # open circuit: the Thevenin voltage
v.check("Ex 06-07.3a", 12.0 / 4.0 + 6.0 / 3.0)
_, csc, _ = tableau([("Va", "V", "ea", "0", 12.0), ("Ra", "R", "ea", "l", 4.0), ("Vb", "V", "eb", "0", 6.0),
                     ("Rb", "R", "eb", "l", 3.0), ("Vsc", "V", "l", "0", 0.0)])
v.assert_true("Ex 06-07.3 short-circuit current is the Norton total", abs(csc["Vsc"] - 5.0) < 1e-12)
v.check("Ex 06-07.3b", e3o["l"] / csc["Vsc"])
v.check("Ex 06-07.3c", e3o["l"])
v.check("Ex 06-07.3d", c3["RL"])
v.check("Ex 06-07.3e", e3["l"])
v.check("Ex 06-07.3f", c3["Ra"])
v.check("Ex 06-07.3g", c3["Rb"])


# ---- Example 06-07.4: ladder of 1k series and 1k shunt
def ladder(n, vin=1.0, rs=1.0, rh=1.0):
    els = [("Vin", "V", "n0", "0", vin)]
    for k in range(1, n + 1):
        els += [(f"S{k}", "R", f"n{k - 1}", f"n{k}", rs), (f"H{k}", "R", f"n{k}", "0", rh)]
    return els


e4, c4, _ = tableau(ladder(3))
v.check("Ex 06-07.4a", 1.0 / e4["n3"])
v.check("Ex 06-07.4b", e4["n3"])
v.check("Ex 06-07.4c", 10.0 * e4["n3"])
v.check("Ex 06-07.4d", 1.0 / c4["S1"])
r = 1.0
for _ in range(200):                               # infinite ladder: R_in = R + R || R_in
    r = 1.0 + 1.0 / (1.0 + 1.0 / r)
v.check("Ex 06-07.4e", r)
v.assert_true("Ex 06-07.4 Fibonacci node voltages and currents",
              np.allclose([e4["n3"], e4["n2"], e4["n1"]], np.array([1, 2, 5]) / 13) and abs(c4["S1"] - 8 / 13) < 1e-12)


# ---- Example 06-07.5: binary-weighted DAC
def dac(code, R=(1.0, 2.0, 4.0), RL=4.0, vref=4.0):
    bits = [(code >> k) & 1 for k in range(len(R) - 1, -1, -1)]
    els = [(f"V{k}", "V", f"b{k}", "0", vref * b) for k, b in enumerate(bits)]
    els += [(f"R{k}", "R", f"b{k}", "o", r) for k, r in enumerate(R)] + [("RL", "R", "o", "0", RL)]
    return tableau(els)[0]["o"]


v.check("Ex 06-07.5a", 1 + 0.5 + 0.25 + 0.25)
v.check("Ex 06-07.5b", dac(1))
v.check("Ex 06-07.5c", dac(4))
v.assert_true("Ex 06-07.5 ideal staircase", np.allclose([dac(c) for c in range(8)], 0.5 * np.arange(8)))
mis = (1.01, 2.0, 4.0)
v.check("Ex 06-07.5d", dac(3, mis))
v.check("Ex 06-07.5e", dac(4, mis))
v.check("Ex 06-07.5f", dac(4, mis) - dac(3, mis))
v.check("Ex 06-07.5g", (dac(4, mis) - dac(3, mis)) / 0.5 - 1)

# ================================================================ solutions
v.check("06-07.1a", 2.0 * 12.0 / 5.0)


def p2(V1=10.0, V2=15.0):
    return [("V1", "V", "s1", "0", V1), ("R1", "R", "s1", "a", 5.0), ("V2", "V", "s2", "0", V2),
            ("R2", "R", "s2", "a", 10.0), ("R3", "R", "a", "0", 10.0)]


v.check("06-07.2a", tableau(p2(V2=0.0))[0]["a"])
v.check("06-07.2b", tableau(p2(V1=0.0))[0]["a"])
v.check("06-07.2c", tableau(p2())[0]["a"])

e3p, c3p, _ = tableau([("V", "V", "s", "0", 24.0), ("R6", "R", "s", "n", 6.0), ("R3", "R", "n", "0", 3.0),
                       ("R2", "R", "n", "l", 2.0), ("RL", "R", "l", "0", 4.0)])
v.check("06-07.3a", 24.0 / 6.0)
v.check("06-07.3b", 1 / (1 / 6.0 + 1 / 3.0))
v.check("06-07.3c", c3p["RL"])
v.check("06-07.3d", e3p["l"])


def p4(V=6.0, I1=1.0, I2=0.5):
    return [("V", "V", "s", "0", V), ("R3", "R", "s", "a", 3.0), ("R6", "R", "a", "0", 6.0),
            ("I1", "I", "0", "a", I1), ("I2", "I", "a", "0", I2)]


parts4 = [tableau(p4(I1=0.0, I2=0.0)), tableau(p4(V=0.0, I2=0.0)), tableau(p4(V=0.0, I1=0.0))]
full4 = tableau(p4())
v.check("06-07.4a", parts4[0][0]["a"])
v.check("06-07.4b", parts4[1][0]["a"])
v.check("06-07.4c", parts4[2][0]["a"])
v.check("06-07.4d", full4[0]["a"])
v.check("06-07.4e", P(full4[1], full4[2], "R6"))
v.check("06-07.4f", sum(P(c, vb, "R6") for _, c, vb in parts4))
v.check("06-07.4g", full4[1]["R3"])


def p5(V=6.0, I=1.0, g=0.25):
    return [("V", "V", "s", "0", V), ("R1", "R", "s", "n1", 2.0), ("R2", "R", "n1", "n2", 2.0),
            ("R3", "R", "n2", "0", 4.0), ("I", "I", "0", "n2", I), ("G", "G", "n2", "0", ("n1", "0", g))]


v.check("06-07.5a", tableau(p5(I=0.0))[0]["n1"])
v.check("06-07.5b", tableau(p5(I=0.0))[0]["n2"])
v.check("06-07.5c", tableau(p5(V=0.0))[0]["n1"])
v.check("06-07.5d", tableau(p5(V=0.0))[0]["n2"])
v.check("06-07.5e", tableau(p5())[0]["n1"])
v.check("06-07.5f", tableau(p5())[0]["n2"])
v.check("06-07.5g", tableau(p5(V=0.0, g=0.0))[0]["n1"])
v.check("06-07.5h", tableau(p5(V=0.0, g=0.0))[0]["n2"])

e6, c6, _ = tableau([("Vin", "V", "i", "0", 1.0), ("S1", "R", "i", "m", 1.0), ("H1", "R", "m", "0", 2.0),
                     ("S2", "R", "m", "o", 3.0), ("H2", "R", "o", "0", 6.0)])
v.check("06-07.6a", e6["o"])
v.check("06-07.6b", 12.0 * e6["o"])
v.check("06-07.6c", 1.0 / c6["S1"])

bats = [(12.6, 0.05), (12.4, 0.06), (12.2, 0.08)]


def p7(load=True):
    els = []
    for k, (vb, rb) in enumerate(bats):
        els += [(f"V{k}", "V", f"e{k}", "0", vb), (f"R{k}", "R", f"e{k}", "bus", rb)]
    if load:
        els.append(("RL", "R", "bus", "0", 0.5))
    return tableau(els)


e7, c7, _ = p7()
v.check("06-07.7a", e7["bus"])
v.check("06-07.7b", c7["R0"])
v.check("06-07.7c", c7["R1"])
v.check("06-07.7d", c7["R2"])
v.check("06-07.7e", c7["RL"])
e7n, c7n, _ = p7(load=False)
v.check("06-07.7f", e7n["bus"])
v.check("06-07.7g", c7n["R0"])
v.check("06-07.7h", -c7n["R1"])
v.check("06-07.7i", -c7n["R2"])

err = np.array([10.0, -4.0, 6.0, 3.0])
v.check("06-07.8a", np.abs(err).sum())
v.check("06-07.8b", 100 * np.abs(err).sum() / 2500)
v.check("06-07.8c", np.linalg.norm(err))
v.check("06-07.8d", 100 * np.linalg.norm(err) / 2500)
v.check("06-07.8e", np.linalg.norm([1.0, -4.0, 6.0, 3.0]))

v.check("06-07.9a", np.hypot(4, 3))
v.check("06-07.9b", 4 + 3)
v.check("06-07.9c", 4 - 3)
v.check("06-07.9d", np.hypot(4, 3) * np.sqrt(1e4))
v.check("06-07.9e", np.hypot(2, 3))

d4 = lambda c, R=(1.0, 2.0, 4.0, 8.0): dac(c, R, RL=8.0)  # noqa: E731
v.check("06-07.10a", d4(1))
v.check("06-07.10b", d4(15))
m4 = (1.005, 2.0, 4.0, 8.0)
v.check("06-07.10c", d4(7, m4))
v.check("06-07.10d", d4(8, m4))
v.check("06-07.10e", (d4(8, m4) - d4(7, m4)) / 0.25 - 1)
v.check("06-07.10f", (d4(8, m4) - 2.0) / 0.25)


def p11(sig=0.05, off=0.002, A=1e5):
    return tableau([("Vs", "V", "x", "0", sig), ("Vos", "V", "p", "x", off), ("R1", "R", "n", "0", 1.0),
                    ("R2", "R", "n", "o", 10.0), ("E", "E", "o", "0", ("p", "n", A))])[0]["o"]


v.check("06-07.11a", p11(sig=1.0, off=0.0))
v.check("06-07.11b", 1e3 * p11(off=0.0))
v.check("06-07.11c", 1e3 * p11(sig=0.0))
v.check("06-07.11d", 1e3 * p11())

vb12 = diode_node(5.0, 1e-3)
v5 = diode_node(5.0, 0.0)
vI = diode_node(0.0, 1e-3)
v.check("06-07.12a", vb12)
v.check("06-07.12b", v5)
v.check("06-07.12c", vI)
v.check("06-07.12d", v5 + vI)
rd = VT / (IS * np.expm1(v5 / VT) + IS)
v.check("06-07.12e", v5 + 1e-3 / (1 / 1000.0 + 1 / rd))
v.check("06-07.12f", 1e3 * IS * np.expm1(vb12 / VT))
v.check("06-07.12g", rd)

# ================================================================ lab
v.check("Lab 06-07.a", -P(c_all, vb_all, "V"), tol=1e-12)
v.check("Lab 06-07.b", rd)
lim = np.array([2.0, 3.0, 6.0])
v.check("Lab 06-07.c", lim.sum())
v.check("Lab 06-07.d", np.linalg.norm(lim))
v.check("Lab 06-07.e", np.sqrt((lim ** 2 / 3).sum()))
# exact probability P(|U1 + U2 + U3| > 7) by convolving the uniform densities on a fine grid
dx = 1e-4
x = np.arange(-11.0, 11.0 + dx / 2, dx)
dens = None
for e in lim:
    u = np.where(np.abs(np.arange(-e, e + dx / 2, dx)) <= e, 1.0 / (2 * e), 0.0)
    dens = u if dens is None else np.convolve(dens, u) * dx
grid = np.linspace(-lim.sum(), lim.sum(), dens.size)
v.check("Lab 06-07.f", 100 * dens[np.abs(grid) > 7.0].sum() * (grid[1] - grid[0]))
e_l, c_l, vb_l = tableau(ex1(I=3.0))
v.check("Lab 06-07.g", P(c_l, vb_l, "V"))

sys.exit(v.finish())
