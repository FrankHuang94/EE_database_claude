#!/usr/bin/env python3
"""Verify every number in the Course 06 final-exam solutions.

Each value is recomputed independently of the hand method in the solutions: every circuit is solved
by a sparse-tableau solver (independent and dependent sources, op-amps as high-gain VCVSs), the
supernode and supermesh answers by full-circuit solves rather than the reduced equations, superposition
by separate solves with sources zeroed, the Thevenin resistance by a test-source solve, the
maximum-power and efficiency loads by numerical optimization and root-finding, worst cases by corner
search, and the bridge by solving the full bridge circuit.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("06-exam", HERE.parent / "exam" / "solutions.md")
BIG = 1e10


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


def opamp(name, plus, minus, out, A=BIG):
    return (name, "E", out, "0", (plus, minus, A))


# Units: V, kΩ, mA (so kΩ × mA = V and V × mA = mW) unless noted.

# ---- Q1
v.check("X06.1a", 12 * -0.5)
q = 3.0 * 3600
v.check("X06.1b", q)
v.check("X06.1c", 3.7 * q / 3600)
v.check("X06.1d", 3.7 * q / 1e3)
v.check("X06.1e", 3.7 * q / 1.5 / 3600)

# ---- Q2
v.check("X06.2a", brentq(lambda T: 2.000 * (1 + 0.00393 * (T - 20)) - 2.472, 0, 300))
v.check("X06.2b", brentq(lambda V: V ** 2 / 10e3 - 0.25, 0, 1000))
v.check("X06.2c", 1e3 * brentq(lambda I: I ** 2 * 100 - 0.25, 0, 10))
v.check("X06.2d", 4.7 * (1 - 0.05))
v.check("X06.2e", 4.7 * (1 + 0.05))

# ---- Q3
div = [("V", "V", "a", "0", 12.0), ("R1", "R", "a", "m", 8.0), ("R2", "R", "m", "0", 4.0)]
v.check("X06.3a", tableau(div)[0]["m"])
v.check("X06.3b", tableau(div + [("RL", "R", "m", "0", 4.0)])[0]["m"])
vu = tableau(div)[0]["m"]
v.check("X06.3c", brentq(lambda RL: 1 - tableau(div + [("RL", "R", "m", "0", RL)])[0]["m"] / vu - 0.01, 1.0, 1e5))
_, c3, _ = tableau([("I", "I", "0", "p", 6.0), ("Ra", "R", "p", "0", 2.0), ("Rb", "R", "p", "0", 3.0),
                    ("Rc", "R", "p", "0", 6.0)])
v.check("X06.3d", c3["Ra"])
v.check("X06.3e", c3["Rb"])
v.check("X06.3f", c3["Rc"])

# ---- Q4
q4 = [("I1", "I", "0", "1", 3.0), ("R1", "R", "1", "0", 2.0), ("V1", "V", "1", "2", 6.0), ("R2", "R", "2", "0", 4.0),
      ("R3", "R", "2", "3", 2.0), ("R4", "R", "3", "0", 1.0), ("I2", "I", "0", "3", 1.0)]
e4, c4, b4 = tableau(q4)
v.check("X06.4a", e4["1"])
v.check("X06.4b", e4["2"])
v.check("X06.4c", e4["3"])
v.check("X06.4d", -b4["V1"] * c4["V1"])          # delivered = -(absorbed), mW
M = np.array([[1, -1, 0], [0.5, 0.75, -0.5], [0, -0.5, 1.5]])
v.assert_true("Q4: published matrix equation reproduces the solution",
              np.allclose(M @ np.array([e4["1"], e4["2"], e4["3"]]), [6, 3, 1]))

# ---- Q5 (ohms, volts, amps)
q5 = [("V1", "V", "1", "0", 12.0), ("R1", "R", "1", "2", 2.0), ("R4", "R", "2", "0", 4.0), ("R2", "R", "2", "3", 3.0),
      ("I1", "I", "0", "3", 1.0), ("R3", "R", "3", "0", 6.0)]
e5, c5, b5 = tableau(q5)
i1, i2, i3 = c5["R1"], c5["R2"], c5["R3"]          # mesh currents are the currents of unshared branches
v.check("X06.5a", i1)
v.check("X06.5b", i2)
v.check("X06.5c", i3)
v.check("X06.5d", e5["2"])
v.check("X06.5e", -b5["V1"] * c5["V1"])
v.check("X06.5f", -b5["I1"] * c5["I1"])
v.check("X06.5g", sum(b5[n] * c5[n] for n in ("R1", "R2", "R3", "R4")))
v.assert_true("Q5: Tellegen (sum of absorbed powers is zero)", abs(sum(b5[k] * c5[k] for k in b5)) < 1e-9)


# ---- Q6 (kΩ, mA, V)
def amp6(RE, vs=1.0):
    els = [("Vs", "V", "s", "0", vs), ("Rs", "R", "s", "b", 1.0), ("Rpi", "R", "b", "e", 2.5),
           ("F", "F", "c", "e", ("Rpi", 100.0)), ("RC", "R", "c", "0", 4.0), ("RE", "R", "e", "0", RE)]
    return tableau(els)


e6, c6, _ = amp6(0.2)
v.check("X06.6a", e6["b"] / c6["Rpi"])
v.check("X06.6b", e6["c"] / 1.0)
v.check("X06.6c", amp6(1e-9)[0]["c"])

# ---- Q7
def q7(V1, I1):
    return tableau([("V", "V", "1", "0", V1), ("R1", "R", "1", "x", 2.0), ("I", "I", "0", "x", I1),
                    ("R2", "R", "x", "0", 3.0)])[0]["x"]


vV, vI, vT = q7(10.0, 0.0), q7(0.0, 3.0), q7(10.0, 3.0)
v.check("X06.7a", vV)
v.check("X06.7b", vI)
v.check("X06.7c", vT)
v.check("X06.7d", vT ** 2 / 3.0)
v.check("X06.7e", vV ** 2 / 3.0 + vI ** 2 / 3.0)
v.check("X06.7f", q7(20.0, 3.0))


# ---- Q8 (kΩ, mA, V; the CCVS's 2000 V/A is 2 kΩ)
def q8(V1, Itest=0.0, short=False):
    els = [("V", "V", "1", "0", V1), ("R1", "R", "1", "a", 6.0), ("R2", "R", "a", "0", 3.0),
           ("H", "H", "b", "a", ("R2", 2.0)), ("R3", "R", "b", "o", 1.0)]
    if Itest:
        els.append(("It", "I", "0", "o", Itest))
    if short:
        els.append(("Rsc", "R", "o", "0", 1e-9))
    return tableau(els)


voc = q8(12.0)[0]["o"]
rth = q8(0.0, Itest=1.0)[0]["o"] / 1.0
isc = q8(12.0, short=True)[1]["Rsc"]
v.check("X06.8a", voc)
v.check("X06.8b", rth)
v.check("X06.8c", isc)
v.check("X06.8d", minimize_scalar(lambda RL: -tableau([("V", "V", "t", "0", voc), ("R", "R", "t", "o", rth),
                                                        ("RL", "R", "o", "0", RL)])[0]["o"] ** 2 / RL,
                                  bounds=(0.1, 100), method="bounded", options={"xatol": 1e-10}).fun * -1)
v.assert_true("Q8: V_oc / I_sc = R_th", abs(voc / isc - rth) < 1e-6)


# ---- Q9 (ohms, volts, watts)
def pload(RL, Rs=0.5, V=48.0):
    return V ** 2 * RL / (Rs + RL) ** 2


best = minimize_scalar(lambda RL: -pload(RL), bounds=(0.01, 100), method="bounded", options={"xatol": 1e-12})
v.check("X06.9a", best.x)
v.check("X06.9b", -best.fun)
R90 = brentq(lambda RL: RL / (RL + 0.5) - 0.9, 0.01, 100)
v.check("X06.9c", R90)
v.check("X06.9d", pload(R90))
v.check("X06.9e", 100 * pload(R90) / -best.fun)
v.assert_true("Q9: fixed 2 Ω load gets most power from zero source resistance",
              all(pload(2.0, Rs=r) < pload(2.0, Rs=0.0) for r in (0.01, 0.5, 2.0)))

# ---- Q10
o10 = tableau([("V", "V", "i", "0", -0.2), ("R1", "R", "i", "n", 2.2), ("R2", "R", "n", "o", 33.0),
               opamp("U", "0", "n", "o")])[0]["o"]
v.check("X06.10a", o10 / -0.2)
v.check("X06.10b", o10)
v.check("X06.10c", brentq(lambda r2: tableau([("V", "V", "p", "0", 1.0), ("R1", "R", "n", "0", 1.0),
                                              ("R2", "R", "n", "o", r2), opamp("U", "p", "n", "o")])[0]["o"] - 16,
                          1, 100))
v.check("X06.10d", 20.0 / 1)
v.check("X06.10e", 20.0 / 2)
v.check("X06.10f", tableau([("Va", "V", "a", "0", 0.5), ("Vb", "V", "b", "0", -1.0), ("Ra", "R", "a", "s", 20.0),
                            ("Rb", "R", "b", "s", 10.0), ("Rf", "R", "s", "o", 20.0), opamp("U", "0", "s", "o")])[0]["o"])


# ---- Q11
def diffamp(v1, v2, R1, R2, R3, R4):
    return tableau([("V1", "V", "a", "0", v1), ("V2", "V", "b", "0", v2), ("R1", "R", "a", "n", R1),
                    ("R2", "R", "n", "o", R2), ("R3", "R", "b", "p", R3), ("R4", "R", "p", "0", R4),
                    opamp("U", "p", "n", "o")])[0]["o"]


v.check("X06.11a", diffamp(2.5, 2.52, 10, 50, 10, 50))
cm = diffamp(2.5, 2.5, 10, 50, 10, 50.5)
v.check("X06.11b", 1e3 * cm)
v.check("X06.11c", cm / 2.5)
v.check("X06.11d", 5 / (cm / 2.5))
v.check("X06.11e", 20 * math.log10(5 / (cm / 2.5)))
v.check("X06.11f", 20 * math.log10((1 + 5) / (4 * 0.01)))
worst = max(abs(diffamp(1.0, 1.0, *(r * (1 + s * 0.01) for r, s in zip((10, 50, 10, 50), sg))))
            for sg in itertools.product((-1, 1), repeat=4))
v.assert_true("Q11: corner search within 2% of (1 + G)/(4t)", abs(5 / worst / 150 - 1) < 0.02)


# ---- Q12 (kΩ, mA, V; 100 nA = 1e-4 mA)
def q12(vs=0.0, vos=0.0, ibp=0.0, ibm=0.0, A=BIG):
    """Bias currents flow INTO the pins; vos in series with the + input."""
    els = [("Vs", "V", "s", "0", vs), ("Rs", "R", "s", "p", 5.0), ("Vos", "V", "q", "p", vos),
           ("R1", "R", "n", "0", 1.0), ("R2", "R", "n", "o", 49.0),
           ("Ip", "I", "p", "0", ibp), ("Im", "I", "n", "0", ibm), opamp("U", "q", "n", "o", A)]
    return tableau(els)[0]["o"]


g12 = q12(vs=1.0, A=2e4)
v.check("X06.12a", g12)
v.check("X06.12b", 100 * (1 - g12 / 50))
v.check("X06.12c", q12(vs=0.02, A=2e4))
t_os, t_m, t_p = q12(vos=2e-3), q12(ibm=1e-4), q12(ibp=1e-4)
v.check("X06.12d", 1e3 * t_os)
v.check("X06.12e", 1e3 * t_m)
v.check("X06.12f", 1e3 * t_p)
v.check("X06.12g", 1e3 * max(abs(q12(vos=a * 2e-3, ibm=b * 1e-4, ibp=c * 1e-4))
                             for a, b, c in itertools.product((-1, 1), repeat=3)))
signed = max(abs(q12(vos=a * 2e-3, ibm=1e-4, ibp=1e-4)) for a in (-1, 1))
v.check("X06.12h", 1e3 * signed)
v.check("X06.12i", 100 * signed / q12(vs=0.02, A=2e4))

# ---- Q13 (V, Ω)
r13 = tableau([("V", "V", "a", "0", 3.3), ("R", "R", "a", "m", 220e3), ("Rin", "R", "m", "0", 10e6)])[0]["m"]
v.check("X06.13a", r13)
v.check("X06.13b", 100 * (r13 / 3.3 - 1))
v.check("X06.13c", r13 * (1 + 220e3 / 10e6))
i13 = tableau([("V", "V", "a", "0", 5.0), ("RA", "R", "a", "b", 2.5), ("RL", "R", "b", "0", 100.0)])[1]["RL"]
v.check("X06.13d", 1e3 * i13)
v.check("X06.13e", 100 * (i13 / 0.05 - 1))
v.check("X06.13f", 1e3 * i13 * 2.5)
v.check("X06.13g", 1e3 * (0.001 * 1.000 + 2 * 0.001))


# ---- Q14 (ohms, volts)
def bridge(x, lead=0.0):
    els = [("V", "V", "ex", "0", 5.0), ("L1", "R", "ex", "t", lead if lead else 1e-12),
           ("Ra", "R", "t", "l", 350.0), ("Rb", "R", "l", "u", 350.0), ("Rc", "R", "t", "r", 350.0),
           ("Rg", "R", "r", "u", 350.0 * (1 + x)), ("L2", "R", "u", "0", lead if lead else 1e-12)]
    e = tableau(els)[0]
    return e["r"] - e["l"], e["t"] - e["u"]


vo14 = bridge(1e-3)[0]
v.check("X06.14a", 1e3 * vo14)
v.check("X06.14b", 1e3 * 5 * 1e-3 / 4)
v.check("X06.14c", 100 * (vo14 / (5 * 1e-3 / 4) - 1))
G14 = 1 + 2 * 24.7e3 / 24.7
v.check("X06.14d", G14)
v.check("X06.14e", G14 * vo14)
v.check("X06.14f", 1e3 * 2.5 * G14 / 10 ** (100 / 20))
v.check("X06.14g", 100 * (2.5 * G14 / 1e5) / (G14 * vo14))
vbr = bridge(0.0, lead=0.5)[1]
v.check("X06.14h", vbr)
v.check("X06.14i", 100 * (vbr / 5 - 1))

v.finish()
