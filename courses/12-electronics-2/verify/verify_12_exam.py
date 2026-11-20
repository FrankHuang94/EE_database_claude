#!/usr/bin/env python3
"""Verify every number in the Course 12 final-exam solutions.

Independent routes (not the hand formulas of the solutions):
- the differential pair's gains by solving its small-signal half circuits numerically, and the switching
  point by root finding on the square-law pair's large-signal transfer;
- cascode output resistances by test-current injection in a small-signal nodal model;
- the common-source stage by complex nodal analysis (exact -3 dB by root finding), open-circuit time
  constants by test sources with the other capacitors open;
- loop-gain crossover and phase margin by root finding with unwrapped phase; overshoot by step simulation;
- class B power by averaging sampled device currents; worst dissipation by optimization;
- noise by quadrature and optimization over source resistance.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("12-exam", HERE.parent / "exam" / "solutions.md")
TP = 2 * math.pi
k = 1.380649e-23
kT = k * 300.0
VT = 0.025852


def nodal(nodes, elems, fixed, f=0.0):
    idx = {n: i for i, n in enumerate(nodes)}
    Y = np.zeros((len(nodes),) * 2, complex)
    b = np.zeros(len(nodes), complex)
    fx = dict(fixed)
    fx.setdefault("0", 0.0)
    s = 1j * TP * f

    def add(i, j, val):
        if i not in idx:
            return
        if j in idx:
            Y[idx[i], idx[j]] += val
        else:
            b[idx[i]] -= val * fx[j]

    for e in elems:
        if e[0] in ("R", "C"):
            y = 1 / e[3] if e[0] == "R" else s * e[3]
            add(e[1], e[1], y); add(e[2], e[2], y); add(e[1], e[2], -y); add(e[2], e[1], -y)
        elif e[0] == "G":
            d, sn, cp, cn, gm = e[1:]
            add(d, cp, gm); add(d, cn, -gm); add(sn, cp, -gm); add(sn, cn, gm)
        elif e[0] == "I":
            if e[1] in idx:
                b[idx[e[1]]] -= e[3]
            if e[2] in idx:
                b[idx[e[2]]] += e[3]
    x = np.linalg.solve(Y, b)
    return {n: x[idx[n]] for n in nodes}


# ============================================================ 1 differential pair
kn, Iss, RD, Rss = 2e-3, 200e-6, 10e3, 100e3
gm = math.sqrt(2 * kn * Iss / 2)
pair = [("G", "d1", "s", "g1", "s", gm), ("G", "d2", "s", "g2", "s", gm), ("R", "d1", "0", RD), ("R", "d2", "0", RD),
        ("R", "s", "0", Rss)]
dm = nodal(["d1", "d2", "s"], pair, {"g1": 0.5, "g2": -0.5})
cm = nodal(["d1", "d2", "s"], pair, {"g1": 1.0, "g2": 1.0})
v.check("X12.1a", gm * 1e3)
v.check("X12.1b", abs((dm["d1"] - dm["d2"]).real))
v.check("X12.1c", abs(dm["d1"].real))
v.check("X12.1d", abs(cm["d1"].real))
v.check("X12.1e", 20 * math.log10(abs(dm["d1"].real) / abs(cm["d1"].real)))
v.check("X12.1g", RD / (2 * Rss))
v.check("X12.1h", abs(dm["d1"].real) / abs(cm["d1"].real))


def i_split(vid):
    """Large-signal square-law pair: the source voltage that makes the two currents sum to I_SS."""
    vs = brentq(lambda x: sum((kn / 2) * max(vg - x - 0.5, 0) ** 2 for vg in (vid / 2, -vid / 2)) - Iss, -5, 5,
                xtol=1e-15)
    return (kn / 2) * max(vid / 2 - vs - 0.5, 0) ** 2


v.check("X12.1f", brentq(lambda x: i_split(x) - Iss * (1 - 1e-12), 0.1, 2.0, xtol=1e-12))

# ============================================================ 2 active loads and cascodes
gm2, ro = 1e-3, 100e3
v.check("X12.2a", gm2 * (1 / (1 / ro + 1 / ro)))


def r_out(elems, node, nodes):
    return float(nodal(nodes, list(elems) + [("I", "0", node, 1.0)], {}).get(node).real)


side = [("G", "o", "m", "0", "m", gm2), ("R", "o", "m", ro), ("R", "m", "0", ro)]   # cascode on a source
Rside = r_out(side, "o", ["o", "m"])
v.check("X12.2b", Rside / 1e6)
both = side + [("G", "o", "m2", "0", "m2", gm2), ("R", "o", "m2", ro), ("R", "m2", "0", ro)]
Rtot = r_out(both, "o", ["o", "m", "m2"])
v.check("X12.2c", Rtot / 1e6)
v.check("X12.2d", gm2 * Rtot)

# ============================================================ 3 and 4: common-source stage
g3, RS, RL, Cgs, Cgd, CL = 2e-3, 10e3, 5e3, 100e-15, 20e-15, 100e-15
cs = [("R", "vs", "g", RS), ("C", "g", "0", Cgs), ("C", "g", "d", Cgd), ("G", "d", "0", "g", "0", g3),
      ("R", "d", "0", RL), ("C", "d", "0", CL)]
H = lambda f: nodal(["g", "d"], cs, {"vs": 1.0}, f)["d"]  # noqa: E731
A0 = abs(H(1.0))
v.check("X12.3a", A0)
v.check("X12.3b", (Cgs + Cgd * (1 + A0)) * 1e15)
v.check("X12.3c", 1 / (TP * RS * (Cgs + Cgd * (1 + A0))) / 1e6)
v.check("X12.3d", (CL + Cgd * (1 + 1 / A0)) * 1e15)
v.check("X12.3e", 1 / (TP * RL * (CL + Cgd * (1 + 1 / A0))) / 1e6)
# the right-half-plane zero: the real s > 0 at which the solved output vanishes (pass f = s / (j 2 pi))
sz = brentq(lambda sg: nodal(["g", "d"], cs, {"vs": 1.0}, sg / (1j * TP))["d"].real, 1e10, 1e12, xtol=1e-3)
v.check("X12.3f", sz / TP / 1e9)
f3 = brentq(lambda f: abs(H(f)) - A0 / math.sqrt(2), 1e6, 1e10, xtol=1e-3)
v.check("X12.3g", f3 / 1e6)
res = [("R", "vs", "g", RS), ("G", "d", "0", "g", "0", g3), ("R", "d", "0", RL)]


def seen(a, b_):
    sol = nodal(["g", "d"], res + [("I", b_, a, 1.0)], {"vs": 0.0})
    va = sol[a] if a in sol else 0.0
    vb = sol[b_] if b_ in sol else 0.0
    return float((va - vb).real)


Rgd = seen("g", "d")
b1 = seen("g", "0") * Cgs + Rgd * Cgd + seen("d", "0") * CL
v.check("X12.4a", Rgd / 1e3)
v.check("X12.4b", b1 * 1e9)
v.check("X12.4c", 1 / (TP * b1) / 1e6)
v.check("X12.4d", 100 * Rgd * Cgd / b1)

# ============================================================ 5 feedback
A5, b5 = 2000.0, 0.05
Af = np.linalg.solve(np.array([[A5, -1.0], [1.0, b5]]), np.array([0.0, 1.0]))[1]
v.check("X12.5a", A5 * b5)
v.check("X12.5b", Af)
v.check("X12.5c", 10e3 * (1 + A5 * b5) / 1e6)
v.check("X12.5d", 1e3 / (1 + A5 * b5))
Hcl = lambda f: abs((A5 / (1 + 1j * f / 50e3)) / (1 + b5 * A5 / (1 + 1j * f / 50e3)))  # noqa: E731
v.check("X12.5e", brentq(lambda f: Hcl(f) - Hcl(0) / math.sqrt(2), 1e3, 1e9) / 1e6)

# ============================================================ 6 phase margin
T6 = lambda f: 500 / ((1 + 1j * f / 10e3) * (1 + 1j * f / 8e6))  # noqa: E731
fc6 = brentq(lambda f: abs(T6(f)) - 1, 1e3, 1e9, xtol=1e-6)
ph6 = float(np.degrees(np.unwrap(np.angle([T6(f) for f in np.geomspace(1, fc6, 3000)])))[-1])
v.check("X12.6a", 500 * 10e3 / 1e6)
v.check("X12.6b", 8e6 / (500 * 10e3))
v.check("X12.6c", fc6 / 1e6)
v.check("X12.6d", 180 + ph6)
r6 = 8e6 / 5e6
p = np.roots([1 / r6, 1, 1])
Q6 = abs(p[0]) / abs(2 * p[0].real)
v.check("X12.6e", Q6)
v.check("X12.6f", 1 / (2 * Q6))
t = np.linspace(0, 40, 400001)
_, y = signal.step(signal.lti([1], [1 / r6, 1, 1]), T=t)
v.check("X12.6g", 100 * (float(np.max(y)) - 1))

# ============================================================ 7 Miller compensation
g1, g2, CL7 = 0.4e-3, 4e-3, 3e-12
Cc = 2.2 * (g1 / g2) * CL7
v.check("X12.7a", Cc * 1e12)
v.check("X12.7b", g1 / (TP * Cc) / 1e6)
v.check("X12.7c", g2 / (TP * CL7) / 1e6)
v.check("X12.7d", g2 / (TP * Cc) / 1e6)
v.check("X12.7e", brentq(lambda r: Cc * (1 / g2 - r), 1, 1e4))   # 1/s_z = C_c (1/g_m2 - R_z) vanishes
v.check("X12.7f", brentq(lambda r: 1 / (Cc * (r - 1 / g2)) - g2 / CL7, 260, 1e5))

# ============================================================ 8 class B
SIN = np.sin(TP * (np.arange(65536) + 0.5) / 65536)


def class_b(Vcc, RL_, Vop):
    vo = Vop * SIN
    return float(np.mean(vo ** 2 / RL_)), float(Vcc * np.mean(np.abs(vo) / RL_))


PL, PS = class_b(12, 8, 12)
v.check("X12.8a", PL)
v.check("X12.8b", PS)
v.check("X12.8c", 100 * PL / PS)
w = minimize_scalar(lambda x: -(lambda r: r[1] - r[0])(class_b(12, 8, x)), bounds=(0.1, 12), method="bounded",
                    options={"xatol": 1e-10})
v.check("X12.8d", w.x)
v.check("X12.8e", -w.fun)
v.check("X12.8f", -w.fun / 2)
v.check("X12.8g", brentq(lambda th: 50 + (-w.fun / 2) * (3 + th) - 125, 0, 1e3))

# ============================================================ 9 slew
Iss9, Vov, Cc9, I7, CL9 = 40e-6, 0.2, 2e-12, 150e-6, 8e-12
gm1 = 2 * (Iss9 / 2) / Vov
v.check("X12.9a", gm1 * 1e6)
v.check("X12.9b", gm1 / (TP * Cc9) / 1e6)
v.check("X12.9c", Iss9 / Cc9 / 1e6)
v.check("X12.9d", I7 / (CL9 + Cc9) / 1e6)
v.check("X12.9e", min(Iss9 / Cc9, I7 / (CL9 + Cc9)) / (TP * 2.0) / 1e6)

# ============================================================ 10 oscillators (Colpitts eigenvalues)
from scipy.linalg import eigvals  # noqa: E402


def colpitts(gmx, L, C1, C2, R):
    return eigvals(-np.array([[1 / R, gmx, 1.0], [0.0, 0.0, -1.0], [-1.0, 1.0, 0.0]]), np.diag([C1, C2, L]))


gc = brentq(lambda g: np.max(colpitts(g, 4.7e-6, 1e-9, 4e-9, 1.5e3).real), 1e-5, 1e-1, xtol=1e-15)
e = colpitts(gc, 4.7e-6, 1e-9, 4e-9, 1.5e3)
v.check("X12.10a", abs(e[np.argmax(e.real)].imag) / TP / 1e6)
v.check("X12.10b", gc * 1e3)
v.check("X12.10c", 1 / (2 * 9 * 25e-12) / 1e9)

# ============================================================ 11 and 12 noise
gm11, RD11 = 10e-3, 1e3
S11 = (4 * kT * (2 / 3) * gm11 + 4 * kT / RD11) * RD11 ** 2 / (gm11 * RD11) ** 2
v.check("X12.11a", S11 / (4 * kT))
v.check("X12.11b", math.sqrt(S11) * 1e9)
v.check("X12.11c", math.sqrt(quad(lambda f: S11, 0, 1e6)[0]) * 1e6)
v.check("X12.11d", math.sqrt(quad(lambda x: 4 * kT * 1e3 / (1 + x * x), 0, np.inf)[0] / (TP * 1e3 * 2e-12)) * 1e6)
en, inn = 3e-9, 0.5e-12
F = lambda R: (4 * kT * R + en ** 2 + (inn * R) ** 2) / (4 * kT * R)  # noqa: E731
v.check("X12.12a", F(1e3))
v.check("X12.12b", 10 * math.log10(F(1e3)))
o = minimize_scalar(lambda r: F(math.exp(r)), bounds=(0, 15), method="bounded", options={"xatol": 1e-12})
v.check("X12.12c", math.exp(o.x) / 1e3)
v.check("X12.12d", o.fun)
v.check("X12.12e", 10 * math.log10(o.fun))

# ============================================================ 14 diligence
g14 = 1e-6 / VT
en14 = math.sqrt(2 * 1.602176634e-19 * 1e-6 / g14 ** 2)      # collector shot noise referred to the base
v.check("X12.14a", g14 * 1e6)
v.check("X12.14b", en14 * 1e9)
v.check("X12.14c", (en14 / 0.5e-9) ** 2)
v.check("X12.14d", brentq(lambda i: math.sqrt(2 * 1.602176634e-19 * i / (i / VT) ** 2) - 0.5e-9, 1e-6, 1, xtol=1e-15)
        * 1e3)

sys.exit(v.finish())
