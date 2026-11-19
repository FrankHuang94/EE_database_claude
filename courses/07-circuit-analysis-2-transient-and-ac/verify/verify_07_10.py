#!/usr/bin/env python3
"""Verify every published number in chapter 07-10 (worked examples, numbers to know, practitioner
lens), its problem solutions and its lab handout.

Independent routes: the chapter uses closed-form parameter formulas, conversion tables and ABCD
products. Here each network is a list of elements solved by modified nodal analysis (MNA), and its
parameters are *measured* by numerically applying the defining tests (a test current with the
other port open for z; a test voltage with the other port shorted for y; mixed for h). S-parameters
are measured by terminating both ports in 50 ohm and driving through 50 ohm. Conversions are checked
against these measurements rather than against each other. ngspice netlists in labs/07-10-lab are
run separately by tools/run_spice.py.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import fsolve

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files(
    "07-10",
    COURSE / "chapters" / "07-10-two-port-networks.md",
    COURSE / "solutions" / "07-10-solutions.md",
    COURSE / "labs" / "07-10-lab" / "README.md",
)
pi = math.pi
dB = lambda z: 20 * math.log10(abs(z))  # noqa: E731
deg = lambda z: math.degrees(cmath.phase(z))  # noqa: E731
Z0 = 50.0


def mna(elements, w, extra=()):
    """Solve at angular frequency w. Elements: ("R"|"L"|"C"|"Y", a, b, value) two-terminal (Y = admittance),
    ("I", a, b, value) current source pushing value from a to b through itself (i.e. into node b),
    ("V", a, b, value) voltage source V(a)-V(b)=value, ("G", a, b, gm, (c, d)) VCCS: current gm*(Vc-Vd)
    flowing from a to b through the source. Returns (node voltages dict, list of V-source currents
    flowing from a through the source to b)."""
    elements = list(elements) + list(extra)
    nodes = sorted({n for e in elements for n in e[1:3] if n != "0"}
                   | {n for e in elements if e[0] == "G" for n in e[4] if n != "0"})
    idx = {n: i for i, n in enumerate(nodes)}
    vs = [e for e in elements if e[0] == "V"]
    N, M = len(nodes), len(vs)
    A = np.zeros((N + M, N + M), complex)
    b = np.zeros(N + M, complex)

    def stamp(a_, b_, y):
        for p, sp in ((a_, 1), (b_, -1)):
            if p == "0":
                continue
            for q, sq in ((a_, 1), (b_, -1)):
                if q != "0":
                    A[idx[p], idx[q]] += sp * sq * y

    for e in elements:
        k = e[0]
        if k == "R":
            stamp(e[1], e[2], 1 / e[3])
        elif k == "L":
            stamp(e[1], e[2], 1 / (1j * w * e[3]))
        elif k == "C":
            stamp(e[1], e[2], 1j * w * e[3])
        elif k == "Y":
            stamp(e[1], e[2], e[3])
        elif k == "I":
            if e[1] != "0":
                b[idx[e[1]]] -= e[3]
            if e[2] != "0":
                b[idx[e[2]]] += e[3]
        elif k == "G":
            c, d = e[4]
            for p, sp in ((e[1], 1), (e[2], -1)):
                if p == "0":
                    continue
                for q, sq in ((c, 1), (d, -1)):
                    if q != "0":
                        A[idx[p], idx[q]] += sp * sq * e[3]
    for j, e in enumerate(vs):
        r = N + j
        for p, sp in ((e[1], 1), (e[2], -1)):
            if p != "0":
                A[idx[p], r] += sp
                A[r, idx[p]] += sp
        b[r] = e[3]
    x = np.linalg.solve(A, b)
    V = {n: x[idx[n]] for n in nodes}
    V["0"] = 0.0
    return V, [x[N + j] for j in range(M)]


def z_params(net, w):
    """Measured: 1 A into port 1 (node p1) with port 2 open, then into port 2."""
    V, _ = mna(net, w, [("I", "0", "p1", 1.0)])
    z11, z21 = V["p1"], V["p2"]
    V, _ = mna(net, w, [("I", "0", "p2", 1.0)])
    return np.array([[z11, V["p1"]], [z21, V["p2"]]])


def y_params(net, w):
    """Measured: 1 V at one port, the other shorted by a 0 V source; port currents flow into the network."""
    _, I = mna(net, w, [("V", "p1", "0", 1.0), ("V", "p2", "0", 0.0)])
    y11, y21 = -I[0], -I[1]
    _, I = mna(net, w, [("V", "p1", "0", 0.0), ("V", "p2", "0", 1.0)])
    return np.array([[y11, -I[0]], [y21, -I[1]]])


def s_params(net, w):
    """Measured: drive port 1 with 2 V behind 50 ohm (incident voltage 1 V), port 2 terminated in 50 ohm."""
    out = np.zeros((2, 2), complex)
    for drive, other, col in (("p1", "p2", 0), ("p2", "p1", 1)):
        V, _ = mna(net, w, [("V", "src", "0", 2.0), ("R", "src", drive, Z0), ("R", other, "0", Z0)])
        out[col, col] = V[drive] - 1.0
        out[1 - col, col] = V[other]
    return out


def T_network(Za, Zb, Zc):
    return [("Y", "p1", "m", 1 / Za), ("Y", "m", "p2", 1 / Zb), ("Y", "m", "0", 1 / Zc)]


# ================================================================================ Example 1
T1 = T_network(10, 20, 30)
zT = z_params(T1, 1.0)
yT = y_params(T1, 1.0)
v.check("Ex 07-10.1a", np.linalg.det(zT).real)
v.check("Ex 07-10.1b", yT[0, 0].real)
v.check("Ex 07-10.1c", yT[0, 1].real)
v.check("Ex 07-10.1d", yT[1, 1].real)
v.assert_true("y measured equals inverse of z measured", np.allclose(yT, np.linalg.inv(zT)))
v.check("Ex 07-10.1e", -1 / yT[0, 1].real)
v.check("Ex 07-10.1f", 1 / (yT[0, 0] + yT[0, 1]).real)
v.check("Ex 07-10.1g", 1 / (yT[1, 1] + yT[0, 1]).real)
Pi = [("R", "p1", "0", 55.0), ("R", "p2", "0", 110.0), ("R", "p1", "p2", 1100 / 30)]
v.assert_true("Pi equivalent has the same z-parameters", np.allclose(z_params(Pi, 1.0), zT))

# ================================================================================ Example 2 (transistor)
rpi, gm, ro, RL = 2.5e3, 40e-3, 50e3, 5e3
Q = [("R", "p1", "0", rpi), ("G", "p2", "0", gm, ("p1", "0")), ("R", "p2", "0", ro)]
# h-parameters measured: h11, h21 with output shorted and 1 A into port 1; h22 with input open
V, I = mna(Q, 1.0, [("I", "0", "p1", 1.0), ("V", "p2", "0", 0.0)])
h11, h21 = V["p1"], -I[0]
_, I = mna(Q, 1.0, [("V", "p2", "0", 1.0)])  # input open, 1 V at the output
h22 = -I[0]
v.check("Ex 07-10.2a", h11.real)
v.check("Ex 07-10.2b", h21.real)
v.check("Ex 07-10.2c", h22.real * 1e6)
V, I = mna(Q, 1.0, [("V", "p1", "0", 1.0), ("R", "p2", "0", RL)])
v.check("Ex 07-10.2e", V["p2"].real)
v.check("Ex 07-10.2f", (1 / -I[0]).real)
Vi, Ii = mna(Q, 1.0, [("I", "0", "p1", 1.0), ("R", "p2", "0", RL)])
v.check("Ex 07-10.2d", (-Vi["p2"] / RL).real)  # I2 into port 2 = -V2/RL, with I1 = 1 A
V, _ = mna(Q, 1.0, [("V", "s", "0", 1.0), ("R", "s", "p1", 1e3), ("R", "p2", "0", RL)])
v.check("Ex 07-10.2g", V["p2"].real)
_, I = mna(Q, 1.0, [("R", "p1", "0", 1e3), ("V", "p2", "0", 1.0)])
v.check("Ex 07-10.2h", (1 / -I[0]).real / 1e3)

# ================================================================================ Example 3 (unbuffered cascade by MNA)
R3, C3 = 1e3, 100e-9
w3 = 1 / (R3 * C3)
v.check("Ex 07-10.3a", w3 / (2 * pi) / 1e3)
one = mna([("V", "p1", "0", 1.0), ("R", "p1", "a", R3), ("C", "a", "0", C3)], w3)[0]["a"]
two = mna([("V", "p1", "0", 1.0), ("R", "p1", "a", R3), ("C", "a", "0", C3), ("R", "a", "b", R3), ("C", "b", "0", C3)],
          w3)[0]["b"]
v.check("Ex 07-10.3b", abs(one))
v.check("Ex 07-10.3c", abs(two))
v.check("Ex 07-10.3d", dB(two))
v.check("Ex 07-10.3e", deg(two))
v.check("Ex 07-10.3f", dB(one**2))
v.check("Ex 07-10.3g", dB(one**2) - dB(two))

# ================================================================================ Example 4 (terminated T)
V, I = mna(T1, 1.0, [("V", "p1", "0", 1.0), ("R", "p2", "0", 100.0)])
v.check("Ex 07-10.4a", (1 / -I[0]).real)
v.check("Ex 07-10.4b", V["p2"].real)
zz = zT.real
v.check("Ex 07-10.4c", zz[0, 0] / zz[1, 0])
v.check("Ex 07-10.4d", np.linalg.det(zz) / zz[1, 0])
v.check("Ex 07-10.4e", 1 / zz[1, 0])
v.check("Ex 07-10.4f", zz[1, 1] / zz[1, 0])
_, I = mna(T1, 1.0, [("R", "p1", "0", 50.0), ("V", "p2", "0", 1.0)])
v.check("Ex 07-10.4g", (1 / -I[0]).real)  # 1 V at port 2, port 1 closed by the 50 ohm source

# ================================================================================ Example 5 (transformer, amplifier)
n5 = 3.0
Tm = np.array([[n5, 0], [0, 1 / n5]]) @ np.array([[1, 2], [0, 1]])
Zin5 = (Tm[0, 0] * 100 + Tm[0, 1]) / (Tm[1, 0] * 100 + Tm[1, 1])
v.check("Ex 07-10.5a", Zin5)
v.assert_true("matches n^2 (2 + 100)", abs(Zin5 - n5**2 * 102) < 1e-9)
v.check("Ex 07-10.5b", np.linalg.det(Tm))
# VCVS gain 20: model the output as a Thevenin source 20*V1 behind 100 ohm using a VCCS + resistor (Norton)
Amp = [("R", "p1", "0", 1e4), ("G", "0", "p2", 20 / 100.0, ("p1", "0")), ("R", "p2", "0", 100.0)]
zA = z_params(Amp, 1.0).real
v.check("Ex 07-10.5c", zA[1, 0] / 1e3)
A5, B5, C5, D5 = zA[0, 0] / zA[1, 0], np.linalg.det(zA) / zA[1, 0], 1 / zA[1, 0], zA[1, 1] / zA[1, 0]
v.check("Ex 07-10.5d", A5)
v.check("Ex 07-10.5e", B5)
v.check("Ex 07-10.5f", C5 * 1e6)
v.check("Ex 07-10.5g", D5)
v.check("Ex 07-10.5h", A5 * D5 - B5 * C5, tol=1e-9)
V, _ = mna(Amp, 1.0, [("V", "s", "0", 1.0), ("R", "s", "p1", 1e3), ("R", "p2", "0", 1e3)])
v.check("Ex 07-10.5i", V["p2"].real)

# ================================================================================ Example 6 (S-parameters by termination)
S_ser = s_params([("R", "p1", "p2", 25.0)], 1.0)
v.check("Ex 07-10.6a", abs(S_ser[0, 0]))
v.check("Ex 07-10.6b", abs(S_ser[1, 0]))
v.check("Ex 07-10.6c", -dB(S_ser[1, 0]))
v.check("Ex 07-10.6d", -dB(S_ser[0, 0]))
v.check("Ex 07-10.6e", (1 - abs(S_ser[0, 0]) ** 2 - abs(S_ser[1, 0]) ** 2) * 100)
w1g = 2 * pi * 1e9
S_sh = s_params([("C", "p1", "0", 1e-12), ("R", "p1", "p2", 1e-9)], w1g)
v.check("Ex 07-10.6f", abs(S_sh[1, 0]))
v.check("Ex 07-10.6g", deg(S_sh[1, 0]))
v.check("Ex 07-10.6h", -dB(S_sh[1, 0]))
v.check("Ex 07-10.6i", abs(S_sh[0, 0]))
v.check("Ex 07-10.6j", deg(S_sh[0, 0]))
v.check("Ex 07-10.6k", -dB(S_sh[0, 0]))
v.check("Ex 07-10.6l", abs(S_sh[0, 0]) ** 2 + abs(S_sh[1, 0]) ** 2)

# ================================================================================ Problems
T_ser = np.array([[1, 50], [0, 1]])
T_sh = np.array([[1, 0], [0.01, 1]])
v.check("07-10.1a", np.linalg.det(T_ser @ T_sh))
Pi2 = [("R", "p1", "0", 100.0), ("R", "p2", "0", 200.0), ("R", "p1", "p2", 50.0)]
y2 = y_params(Pi2, 1.0).real
z2 = z_params(Pi2, 1.0).real
v.check("07-10.2a", y2[0, 0])
v.check("07-10.2b", y2[0, 1])
v.check("07-10.2c", y2[1, 1])
v.check("07-10.2d", z2[0, 0])
v.check("07-10.2e", z2[0, 1])
v.check("07-10.2f", z2[1, 1])
v.check("07-10.3a", np.linalg.det(np.array([[2, 10], [0.1, 1]])))
v.check("07-10.3b", np.linalg.det(np.array([[1, 5], [0.2, 3]])))
v.check("07-10.3c", np.linalg.det(np.array([[50, 0.5], [-0.5, 0.01]])))
# P4: h of the T, measured
V, I = mna(T1, 1.0, [("I", "0", "p1", 1.0), ("V", "p2", "0", 0.0)])
v.check("07-10.4a", V["p1"].real)
v.check("07-10.4c", (-I[0]).real)
V, I = mna(T1, 1.0, [("V", "p2", "0", 1.0)])
v.check("07-10.4b", V["p1"].real)
v.check("07-10.4d", (-I[0]).real)
# P5: solve the defining h equations numerically under each port test (no conversion formulas used)
h11_, h12_, h21_, h22_ = 2000.0, 2e-4, 150.0, 20e-6


def h_solve(cond, h12=h12_):
    """Unknowns (V1, I1, V2, I2). Rows: V1 - h11 I1 - h12 V2 = 0; I2 - h21 I1 - h22 V2 = 0; plus two
    test conditions given as (row coefficients, value) pairs."""
    A = [[1, -h11_, -h12, 0], [0, -h21_, -h22_, 1]] + [c for c, _ in cond]
    b = [0, 0] + [val for _, val in cond]
    return np.linalg.solve(np.array(A, float), np.array(b, float))


yM = np.array([[h_solve([([1, 0, 0, 0], 1.0), ([0, 0, 1, 0], 0.0)])[k] for k in (1, 3)],
               [h_solve([([1, 0, 0, 0], 0.0), ([0, 0, 1, 0], 1.0)])[k] for k in (1, 3)]]).T
zM = np.array([[h_solve([([0, 1, 0, 0], 1.0), ([0, 0, 0, 1], 0.0)])[k] for k in (0, 2)],
               [h_solve([([0, 1, 0, 0], 0.0), ([0, 0, 0, 1], 1.0)])[k] for k in (0, 2)]]).T
v.check("07-10.5a", np.linalg.det(np.array([[h11_, h12_], [h21_, h22_]])))
v.check("07-10.5b", yM[0, 0] * 1e3)
v.check("07-10.5c", yM[0, 1] * 1e6)
v.check("07-10.5d", yM[1, 0] * 1e3)
v.check("07-10.5e", yM[1, 1] * 1e6)
v.check("07-10.5f", zM[0, 0])
v.check("07-10.5g", zM[0, 1])
v.check("07-10.5h", zM[1, 0] / 1e6)
v.check("07-10.5i", zM[1, 1] / 1e3)
# terminated in 10 k: V1 = 1 and V2 = -ZL I2
x5 = h_solve([([1, 0, 0, 0], 1.0), ([0, 0, 1, 1e4], 0.0)])
v.check("07-10.5j", x5[2])
v.check("07-10.5k", 1 / x5[1])
x5b = h_solve([([1, 0, 0, 0], 1.0), ([0, 0, 1, 1e4], 0.0)], h12=0.0)
v.check("07-10.5l", 1 / x5b[1])
# P6
three = mna([("V", "p1", "0", 1.0), ("R", "p1", "a", R3), ("C", "a", "0", C3), ("R", "a", "b", R3), ("C", "b", "0", C3),
             ("R", "b", "c", R3), ("C", "c", "0", C3)], w3)[0]["c"]
v.check("07-10.6a", abs(three))
v.check("07-10.6b", dB(three))
v.check("07-10.6c", deg(three))
v.check("07-10.6d", dB(one**3))
v.check("07-10.6e", dB(one**3) - dB(three))
# P7: L-match by MNA
w7 = 2 * pi * 1e8
L7, C7 = 20 / w7, 1 / (w7 * 25)
v.check("07-10.7a", L7 * 1e9)
v.check("07-10.7b", C7 * 1e12)


def zin7(w):
    _, I = mna([("V", "p1", "0", 1.0), ("C", "p1", "0", C7), ("L", "p1", "q", L7), ("R", "q", "0", 10.0)], w)
    return 1 / -I[0]


v.check("07-10.7c", zin7(w7).real)
g110 = (zin7(2 * pi * 110e6) - 50) / (zin7(2 * pi * 110e6) + 50)
v.check("07-10.7d", abs(g110))
v.check("07-10.7e", -dB(g110))
# P8: twin-T as one netlist (independent of adding y)
R8, C8 = 10e3, 10e-9
f08 = 1 / (2 * pi * R8 * C8)
v.check("07-10.8a", f08 / 1e3)


def twin_t(f):
    w = 2 * pi * f
    net = [("V", "p1", "0", 1.0), ("R", "p1", "a", R8), ("R", "a", "p2", R8), ("C", "a", "0", 2 * C8),
           ("C", "p1", "b", C8), ("C", "b", "p2", C8), ("R", "b", "0", R8 / 2)]
    return mna(net, w)[0]["p2"]


v.check("07-10.8b", abs(twin_t(f08)), tol=1e-9)
v.check("07-10.8c", abs(twin_t(f08 / 2)))
v.assert_true("symmetric about f0", abs(abs(twin_t(f08 / 2)) - abs(twin_t(2 * f08))) < 1e-12)
v.check("07-10.8d", dB(twin_t(f08 / 2)))
v.check("07-10.8e", abs(twin_t(0.9 * f08)))
v.check("07-10.8f", dB(twin_t(0.9 * f08)))
# P9: attenuator
K9 = 10 ** (6 / 20)
Rsh, Rse = Z0 * (K9 + 1) / (K9 - 1), Z0 * (K9**2 - 1) / (2 * K9)
v.check("07-10.9a", Rsh)
v.check("07-10.9b", Rse)
att = [("R", "p1", "0", Rsh), ("R", "p1", "p2", Rse), ("R", "p2", "0", Rsh)]
za = z_params(att, 1.0).real
v.check("07-10.9c", za[0, 0] / za[1, 0])
v.check("07-10.9d", 1 / za[1, 0])
A9, B9, C9, D9 = za[0, 0] / za[1, 0], np.linalg.det(za) / za[1, 0], 1 / za[1, 0], za[1, 1] / za[1, 0]
v.check("07-10.9e", A9 * D9 - B9 * C9)
v.assert_true("attenuator symmetric: A = D", abs(A9 - D9) < 1e-12)
Sa = s_params(att, 1.0)
v.check("07-10.9f", abs(Sa[0, 0]), tol=1e-9)
v.check("07-10.9g", abs(Sa[1, 0]))
v.check("07-10.9h", dB(Sa[1, 0]))
v.check("07-10.9i", (1 - abs(Sa[1, 0]) ** 2 - abs(Sa[0, 0]) ** 2) * 100)
# P10: hybrid-pi with C_mu, input admittance by MNA
w10 = 2 * pi * 1e6
HP = [("R", "p1", "0", rpi), ("C", "p1", "0", 10e-12), ("C", "p1", "p2", 1e-12), ("G", "p2", "0", gm, ("p1", "0")),
      ("R", "p2", "0", ro)]
y10 = y_params(HP, w10)
v.assert_true("not reciprocal: y12 != y21", abs(y10[0, 1] - y10[1, 0]) > 1e-3)
_, I = mna(HP, w10, [("V", "p1", "0", 1.0), ("R", "p2", "0", RL)])
Yin = -I[0]
v.check("07-10.10a", Yin.real * 1e3)
v.check("07-10.10b", Yin.imag * 1e3)
v.check("07-10.10c", Yin.imag / w10 * 1e12)
v.check("07-10.10d", 1 / Yin.real)
v.check("07-10.10e", (10e-12 + 1e-12 * (1 + gm * ro * RL / (ro + RL))) * 1e12)
# P11
w5 = 2 * pi * 5e9
nets = {"a": [("C", "p1", "0", 1e-12), ("R", "p1", "p2", 1e-9)],
        "b": [("R", "p1", "p2", 10.0)],
        "c": [("R", "p1", "m", 10.0), ("C", "m", "0", 1e-12), ("R", "m", "p2", 1e-9)]}
Sa_ = s_params(nets["a"], w5)
v.check("07-10.11a", abs(Sa_[0, 0]))
v.check("07-10.11b", deg(Sa_[0, 0]))
v.check("07-10.11c", abs(Sa_[1, 0]))
v.check("07-10.11d", deg(Sa_[1, 0]))
v.check("07-10.11e", -dB(Sa_[1, 0]))
v.check("07-10.11f", -dB(Sa_[0, 0]))
Sb_ = s_params(nets["b"], w5)
v.check("07-10.11g", abs(Sb_[0, 0]))
v.check("07-10.11h", abs(Sb_[1, 0]))
v.check("07-10.11i", -dB(Sb_[1, 0]))
v.check("07-10.11j", -dB(Sb_[0, 0]))
Sc_ = s_params(nets["c"], w5)
v.check("07-10.11k", abs(Sc_[0, 0]))
v.check("07-10.11l", deg(Sc_[0, 0]))
v.check("07-10.11m", abs(Sc_[1, 0]))
v.check("07-10.11n", deg(Sc_[1, 0]))
v.check("07-10.11o", -dB(Sc_[1, 0]))
v.check("07-10.11p", -dB(Sc_[0, 0]))
v.check("07-10.11q", abs(Sc_[1, 1]))
v.check("07-10.11r", (1 - abs(Sc_[0, 0]) ** 2 - abs(Sc_[1, 0]) ** 2) * 100)
v.check("07-10.11s", abs(Sa_[0, 0]) ** 2 * 100, tol=0.5)
# P12
ZL12 = 25 + 25j
G12 = s_params([("Y", "p1", "0", 1 / ZL12), ("R", "p1", "p2", 1e12)], 1.0)[0, 0]
v.check("07-10.12a", abs(G12))
v.check("07-10.12b", deg(G12))
v.check("07-10.12c", -dB(G12))
v.check("07-10.12d", -10 * math.log10(1 - abs(G12) ** 2))
v.check("07-10.12e", (1 + abs(G12)) / (1 - abs(G12)))

# ================================================================================ Numbers to know and practitioner lens
v.check("N 07-10.a", 10 ** (-10 / 10) * 100)
v.check("N 07-10.b", 10 ** (-20 / 10) * 100)
VT25 = 1.380649e-23 * 298.15 / 1.602176634e-19
v.check("PL 07-10.a", 1e-3 / VT25 * 1e3)
v.check("PL 07-10.b", 100 / (1e-3 / VT25) / 1e3)
v.check("PL 07-10.c", 10 ** (129 / 20) / 1e6, tol=0.05)
v.check("PL 07-10.d", 106.25 / 2 / 2)
v.check("PL 07-10.e", 10 ** (-28 / 20))
v.check("PL 07-10.f", 10 ** (-28 / 10) * 100)
v.check("PL 07-10.g", 28 + 2 * 4)
v.check("PL 07-10.h", 2 * 6.875 + 2 * 1.6 + 11.55)
v.check("PL 07-10.i", 10 ** (-40 / 20), tol=1e-12)
v.check("PL 07-10.j", 64 / 2 / 2)
v.check("PL 07-10.k", 8.0 + 8.5 + 15.5)
v.check("PL 07-10.l", 15.5 / 1.0)
v.check("PL 07-10.m", 15.5 / 0.1875, tol=0.5)
# cascaded matched sections: S21 multiplies, so insertion losses in dB add (two matched attenuators)
two_pads = [("R", "p1", "0", Rsh), ("R", "p1", "x", Rse), ("R", "x", "0", Rsh / 2),  # the two inner shunts merge
            ("R", "x", "p2", Rse), ("R", "p2", "0", Rsh)]
Scas = s_params(two_pads, 1.0)
v.assert_true("two matched 6 dB pads give 12 dB", abs(dB(Scas[1, 0]) + 12.0) < 1e-9)

# ================================================================================ Lab handout
S10 = s_params([("C", "p1", "0", 1e-12), ("R", "p1", "p2", 1e-9)], 2 * pi * 10e9)
v.check("Lab 07-10.a", abs(S10[1, 0]))
v.check("Lab 07-10.b", abs(S10[0, 0]))

# ---- Section 3.10 (audit addition): mismatch numbers and the 20-to-50 ohm L-section, by root-finding
G20 = (20 - 50) / (20 + 50)
v.check("Th 07-10.a", G20)
v.check("Th 07-10.b", -20 * np.log10(abs(G20)))
tl = np.linspace(0, 1, 100001)   # standing wave along one wavelength: |1 + G e^{-j 4 pi x}|
env = np.abs(1 + G20 * np.exp(-4j * pi * tl))
v.check("Th 07-10.c", env.max() / env.min())
# delivered power from a 1 V-peak, 50 ohm source into 20 ohm, relative to the available power 1/(8*50)
v.check("Th 07-10.d", 100 * (0.5 * abs(1 / (50 + 20)) ** 2 * 20) / (1 / (8 * 50)))
v.check("Th 07-10.e", -10 * np.log10((0.5 * abs(1 / (50 + 20)) ** 2 * 20) / (1 / (8 * 50))))
w9 = 2 * pi * 900e6


def zin_l(X, Bs):
    return 1 / (1j * Bs + 1 / (20 + 1j * X))


Xs, Bs = fsolve(lambda q: [zin_l(q[0], q[1] / 1e3).real - 50, zin_l(q[0], q[1] / 1e3).imag], [20.0, 20.0])
Bs /= 1e3
v.check("Th 07-10.g", Xs)
v.check("Th 07-10.f", Xs / 20)
v.check("Th 07-10.i", 1 / Bs)
v.check("Th 07-10.h", Xs / w9 * 1e9)
v.check("Th 07-10.j", Bs / w9 * 1e12)
v.check("PL 07-10.n", 1 / 0.1875)
v.check("Th 07-10.k", zin_l(Xs, Bs).real)

v.finish()
