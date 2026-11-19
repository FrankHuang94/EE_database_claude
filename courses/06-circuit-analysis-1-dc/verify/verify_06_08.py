#!/usr/bin/env python3
"""Verify every number published in chapter 06-08, its solutions and its lab handout.

Independent routes. The text finds equivalents by series-parallel reduction, open/short-circuit
tests, test sources and Millman's theorem. This script instead gets every equivalent from two
sparse-tableau solves (the solver of verify_06_06.py, with dependent sources) of the complete
circuit with two different load resistors attached, fitting the terminal line v = V_th - R_th i
through the two operating points, and checks the result against a third load. PoE and
constant-power answers come from root-finding on the load's own law.
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
v = Verifier.from_files("06-08", C_DIR / "chapters" / "06-08-thevenin-and-norton.md",
                        C_DIR / "solutions" / "06-08-solutions.md", C_DIR / "labs" / "06-08-lab" / "README.md")


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


def equivalent(network, a, b="0", loads=(1.0, 7.0, 31.0)):
    """Thevenin (V_th, R_th) of `network` at terminals a-b from loaded solves; checks a third load."""
    pts = []
    for RL in loads:
        e, cur, _ = tableau(list(network) + [("RLOAD", "R", a, b, RL)])
        pts.append((e[a] - e[b], cur["RLOAD"]))
    (v1, i1), (v2, i2), (v3, i3) = pts
    Rth = -(v2 - v1) / (i2 - i1)
    Vth = v1 + Rth * i1
    assert abs(v3 - (Vth - Rth * i3)) < 1e-9 * max(1.0, abs(Vth)), "network is not linear at its terminals"
    return Vth, Rth


par = lambda *r: 1 / sum(1 / x for x in r)  # noqa: E731

# ================================================================ chapter
ex1 = [("V", "V", "s", "0", 12.0), ("R1", "R", "s", "m", 6.0), ("R2", "R", "m", "0", 3.0), ("R3", "R", "m", "a", 1.0)]
Vth1, Rth1 = equivalent(ex1, "a")
v.check("Ex 06-08.1a", Vth1)
v.check("Ex 06-08.1b", Rth1)
v.check("Ex 06-08.1c", Vth1 / Rth1)
v.check("Ex 06-08.1d", tableau(ex1 + [("RL", "R", "a", "0", 1.0)])[0]["a"])
v.check("Ex 06-08.1e", tableau(ex1 + [("RL", "R", "a", "0", 3.0)])[0]["a"])

ex2 = [("V", "V", "t", "0", 5.0), ("R1", "R", "t", "A", 1.0), ("R2", "R", "A", "0", 1.0),
       ("R3", "R", "t", "B", 1.0), ("R4", "R", "B", "0", 1.1)]
Vth2, Rth2 = equivalent(ex2, "B", "A")
v.check("Ex 06-08.2a", 1e3 * Vth2)
v.check("Ex 06-08.2b", Rth2)
v.check("Ex 06-08.2c", tableau(ex2 + [("RG", "R", "B", "A", 0.1)])[1]["RG"])
v.check("Ex 06-08.2d", tableau(ex2 + [("RG", "R", "B", "A", 0.05)])[1]["RG"])
v.check("Ex 06-08.2e", Vth2 / Rth2)

ex3 = [("Vs", "V", "s", "0", 1.0), ("Rs", "R", "s", "x", 1.0), ("Rf", "R", "x", "o", 9.0),
       ("Ro", "R", "o", "e", 2.0), ("E", "E", "e", "0", ("x", "0", -10.0))]
Vth3, Rth3 = equivalent(ex3, "o")
v.check("Ex 06-08.3a", Vth3)
v.check("Ex 06-08.3b", tableau(ex3)[0]["x"])
v.check("Ex 06-08.3c", Rth3)
v.check("Ex 06-08.3d", Vth3 / Rth3)


def poe(Vp, Rc, Ppse):
    I = Ppse / Vp
    return I, Vp - I * Rc, Ppse - I * I * Rc


I4, V4, P4 = poe(52.0, 6.25, 90.0)
v.check("Ex 06-08.4a", I4)
v.check("Ex 06-08.4b", V4)
v.check("Ex 06-08.4c", P4)
v.check("Ex 06-08.4d", 90.0 - P4)
v.check("Ex 06-08.4e", 100 * (90.0 - P4) / 90.0)
_, Vt1, Pt1 = poe(44.0, 20.0, 15.4)
_, Vt2, Pt2 = poe(50.0, 12.5, 30.0)
_, _, Pt3 = poe(50.0, 6.25, 60.0)
v.check("Ex 06-08.4f", Pt1)
v.check("Ex 06-08.4g", Vt1)
v.check("Ex 06-08.4h", Pt2)
v.check("Ex 06-08.4i", Vt2)
v.check("Ex 06-08.4j", Pt3)
RL_grid = np.logspace(-2, 3, 200001)
v.check("Ex 06-08.4k", (52.0 ** 2 * RL_grid / (6.25 + RL_grid) ** 2).max(), tol=0.05)
v.check("Ex 06-08.4l", I4 * 6.25)

# Example 06-08.5: readings, then recovery by a least-squares line through (1/R, 1/v)
Vt, Rt = 0.300, 200.0
loads5 = np.array([10.0, 1e4])
readings = Vt * loads5 / (Rt + loads5)
v.check("Ex 06-08.5a", 1e3 * readings[0])
v.check("Ex 06-08.5b", 1e3 * readings[1])
slope, intercept = np.polyfit(1 / loads5, 1 / readings, 1)
v.check("Ex 06-08.5c", 1 / intercept)
v.check("Ex 06-08.5d", slope / intercept)
v.check("Ex 06-08.5e", 100 * (Vt - readings[1]) / Vt)
v.check("Ex 06-08.5f", slope)
v.check("Ex 06-08.5g", intercept)

# ================================================================ solutions
v.check("06-08.1a", 9.0 / 3.0)
v.check("06-08.1b", 0.020 * 250)
v.check("06-08.1c", 2.4 / 8e-3)

p2 = [("V", "V", "s", "0", 12.0), ("R4", "R", "s", "a", 4.0), ("I", "I", "0", "a", 2.0)]
Vth_p2, Rth_p2 = equivalent(p2, "a")
v.check("06-08.2a", Vth_p2)
v.check("06-08.2b", Rth_p2)
v.check("06-08.2c", tableau(p2 + [("R6", "R", "a", "0", 6.0)])[0]["a"])

src3 = [("V", "V", "s", "0", 5.0), ("R", "R", "s", "a", 50.0)]
for ids, RL in (("ab", 50.0), ("cd", 450.0), ("ef", 4950.0)):
    vl = tableau(src3 + [("RL", "R", "a", "0", RL)])[0]["a"]
    v.check(f"06-08.3{ids[0]}", vl)
    v.check(f"06-08.3{ids[1]}", 100 * (5.0 - vl) / 5.0)
v.check("06-08.3g", brentq(lambda k: 50 / (50 + 50 * k) - 0.01, 1, 1000))

p4 = [("V", "V", "e", "0", 2.5), ("R1", "R", "e", "l", 350.0), ("R2", "R", "l", "0", 350.7),
      ("R3", "R", "e", "r", 350.0), ("R4", "R", "r", "0", 350.0)]
Vth_p4, Rth_p4 = equivalent(p4, "l", "r", loads=(100.0, 1000.0, 5000.0))
v.check("06-08.4a", 1e3 * Vth_p4)
v.check("06-08.4b", Rth_p4)
vin = tableau(p4 + [("Rin", "R", "l", "r", 10000.0)])[0]
v.check("06-08.4c", 1e3 * (vin["l"] - vin["r"]))
v.check("06-08.4d", 100 * (1 - (vin["l"] - vin["r"]) / Vth_p4))
v.check("06-08.4e", 1e-3 * brentq(lambda R: Rth_p4 / (Rth_p4 + R) - 1e-3, 1e3, 1e7))

p5 = [("Vs", "V", "s", "0", 1.0), ("Rs", "R", "s", "b", 1.0), ("rpi", "R", "b", "e", 2.5),
      ("F", "F", "0", "e", ("rpi", 100.0)), ("RE", "R", "e", "0", 1.0)]
Vth_p5, Rth_p5 = equivalent(p5, "e", loads=(0.05, 0.3, 2.0))
v.check("06-08.5a", Vth_p5)
v.check("06-08.5b", 1e3 * Rth_p5)
v.check("06-08.5c", tableau(p5 + [("RL", "R", "e", "0", 0.1)])[0]["e"])
v.check("06-08.5d", 1e3 * (2.5 + 1.0) / 101)

v.check("06-08.6a", 1e3 * (3.70 - 3.58) / 2)
cell = [("V", "V", "s", "0", 3.70), ("R", "R", "s", "a", 0.060), ("I", "I", "a", "0", 5.0)]
ec, cc, vc = tableau(cell)
v.check("06-08.6b", ec["a"])
v.check("06-08.6c", P(cc, vc, "R"))
v.check("06-08.6d", P(cc, vc, "I"))

meter = 10000.0
sens = [("V", "V", "s", "0", 5.0), ("R", "R", "s", "a", 5.0)]
r1 = tableau(sens + [("M", "R", "a", "0", meter)])[0]["a"]
r2 = tableau(sens + [("M", "R", "a", "0", meter), ("L", "R", "a", "0", 10.0)])[0]["a"]
v.assert_true("06-08.7 readings as published", abs(r1 - 4.99750) < 5e-6 and abs(r2 - 3.33222) < 5e-6)
sl, ic = np.polyfit([1 / meter, 1 / par(10.0, meter)], [1 / 4.99750, 1 / 3.33222], 1)
v.check("06-08.7a", 1 / ic)
v.check("06-08.7b", sl / ic)
v.check("06-08.7c", 10.0 * (4.99750 / 3.33222 - 1))

for ids, (Vp, Rc, Pp) in (("abcd", (44.0, 20.0, 15.4)), ("efgh", (50.0, 12.5, 30.0))):
    I, Vpd, Ppd = poe(Vp, Rc, Pp)
    v.check(f"06-08.8{ids[0]}", I)
    v.check(f"06-08.8{ids[1]}", Vpd)
    v.check(f"06-08.8{ids[2]}", Ppd)
    v.check(f"06-08.8{ids[3]}", 100 * Ppd / Pp)
vpd = brentq(lambda x: x * (50.0 - x) / 6.25 - 25.5, 25.0, 50.0)
v.check("06-08.8i", vpd)
v.check("06-08.8j", 25.5 / vpd)
v.check("06-08.8k", 50.0 * 25.5 / vpd)
v.check("06-08.8l", (25.5 / vpd) ** 2 * 6.25)

f9 = lambda x: x * (12.0 - x) / 1.0 - 20.0  # noqa: E731
v.check("06-08.9a", brentq(f9, 6.0, 12.0))
v.check("06-08.9b", brentq(f9, 0.0, 6.0))
xs = np.linspace(0, 12, 120001)
pw = xs * (12 - xs)
v.check("06-08.9c", pw.max())
v.check("06-08.9d", xs[np.argmax(pw)])

mos = [("Vg", "V", "g", "0", 1.0), ("Gm", "G", "d", "s", ("g", "s", 2.0)), ("ro", "R", "d", "s", 50.0),
       ("RS", "R", "s", "0", 1.0)]
esc, csc, _ = tableau(mos + [("Vsc", "V", "d", "0", 0.0)])
v.check("06-08.10a", esc["s"])
v.check("06-08.10b", csc["Vsc"])          # convention: out of the drain through the short
VN, RN = equivalent(mos, "d", loads=(1.0, 10.0, 100.0))
v.check("06-08.10c", par(RN, 10.0))
v.check("06-08.10d", tableau(mos + [("RD", "R", "d", "0", 10.0)])[0]["d"])
v.assert_true("06-08.10 R_N equals Problem 06-06.8", abs(RN - 151.0) < 1e-9)


def cascade(Rin):
    return tableau([("Vs", "V", "s", "0", 1.0), ("Rsrc", "R", "s", "i", 10.0), ("Rin", "R", "i", "0", Rin),
                    ("E", "E", "x", "0", ("i", "0", 10.0)), ("Ro", "R", "x", "o", 0.1), ("RL", "R", "o", "0", 1.0)])[0]["o"]


v.check("06-08.11a", cascade(100.0))
v.check("06-08.11b", cascade(10000.0))

dacnet = [("V2", "V", "b2", "0", 4.0), ("V1", "V", "b1", "0", 0.0), ("V0", "V", "b0", "0", 4.0),
          ("R2", "R", "b2", "o", 1.0), ("R1", "R", "b1", "o", 2.0), ("R0", "R", "b0", "o", 4.0)]
Vd, Rd = equivalent(dacnet, "o")
v.check("06-08.12a", Rd)
v.check("06-08.12b", Vd)
v.check("06-08.12c", tableau(dacnet + [("RL", "R", "o", "0", 4.0)])[0]["o"])


# ================================================================ lab
def ex1_original(RL):
    e, cur, vol = tableau(ex1 + [("RL", "R", "a", "0", RL)])
    return e["a"], sum(P(cur, vol, r) for r in ("R1", "R2", "R3"))


va, pin = ex1_original(1.0)
v.check("Lab 06-08.a", pin)                      # kOhm, mA, V -> mW
_, cth, vth = tableau([("V", "V", "s", "0", Vth1), ("R", "R", "s", "a", Rth1), ("RL", "R", "a", "0", 1.0)])
v.check("Lab 06-08.b", P(cth, vth, "R"))
_, cn, vn = tableau([("I", "I", "0", "a", Vth1 / Rth1), ("R", "R", "a", "0", Rth1), ("RL", "R", "a", "0", 1.0)])
v.check("Lab 06-08.c", P(cn, vn, "R"))
v.check("Lab 06-08.d", brentq(lambda x: x * (52.0 - x) / 6.25 - 100.0, 26.0, 52.0))
ex3b = [el if el[0] != "Rf" else ("Rf", "R", "x", "o", 99.0) for el in ex3]
v.check("Lab 06-08.e", equivalent(ex3b, "o")[1])
v.check("Lab 06-08.f", 52.0 ** 2 / (4 * 3.125))

# ---- Problem 06-08.13 (kΩ, mA, V, mW): equivalents from loaded solves, then each circuit's internal power
orig = [("V", "V", "s", "0", 10.0), ("Rs", "R", "s", "o", 2.0), ("Rp", "R", "o", "0", 2.0)]
Vt13, Rt13 = equivalent(orig, "o")
v.check("06-08.13a", Vt13)
v.check("06-08.13b", Rt13)
v.check("06-08.13c", Vt13 / Rt13)
forms = {"orig": orig,
         "thev": [("V", "V", "s", "0", Vt13), ("Rs", "R", "s", "o", Rt13)],
         "nort": [("I", "I", "0", "o", Vt13 / Rt13), ("Rp", "R", "o", "0", Rt13)]}
res13 = {}
for name, net in forms.items():
    e, cur, vol = tableau(net + [("RL", "R", "o", "0", 4.0)])
    src = [k for k in cur if k in ("V", "I")][0]
    p_src = -P(cur, vol, src)
    p_int = sum(P(cur, vol, k) for k in cur if k not in (src, "RL"))
    res13[name] = (e["o"], P(cur, vol, "RL"), p_src, p_int)
v.assert_true("06-08.13: all three forms give the load the same voltage and power",
              max(abs(r[0] - 4.0) + abs(r[1] - 4.0) for r in res13.values()) < 1e-9)
v.check("06-08.13d", res13["orig"][0])
v.check("06-08.13e", res13["orig"][1])
v.check("06-08.13f", res13["orig"][3])
v.check("06-08.13g", res13["thev"][3])
v.check("06-08.13h", res13["nort"][3])
v.check("06-08.13i", 100 * res13["orig"][1] / res13["orig"][2])
v.check("06-08.13j", 100 * res13["thev"][1] / res13["thev"][2])
v.check("06-08.13k", 100 * res13["nort"][1] / res13["nort"][2])

sys.exit(v.finish())
