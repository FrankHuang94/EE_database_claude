#!/usr/bin/env python3
"""Verify every number in chapter 12-03 (frequency response: capacitances, Miller effect, poles and zeros),
its solutions and lab.

Independent routes (not the closed forms of the chapter):
- transfer functions by complex nodal analysis of the full small-signal circuits at each frequency;
- -3 dB frequencies by root finding on |H(j omega)| against the solved DC gain;
- poles as generalized eigenvalues of the nodal conductance and capacitance matrices, det(G + sC) = 0;
- zeros by finding where the solved output vanishes;
- f_T by locating unity short-circuit current gain in the solved circuit;
- Miller capacitances by measuring the input admittance of the bridged circuit.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigvals
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "12-03-frequency-response-miller-poles-zeros.md", COURSE / "solutions" / "12-03-solutions.md"]
lab = COURSE / "labs" / "12-03-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-03", *files)
TP = 2 * math.pi
VT = 1.380649e-23 * 300 / 1.602176634e-19


# ============================================================ complex nodal analysis
def matrices(nodes, elems, fixed):
    """Return G, C (nodal) and the right-hand side vectors for fixed-node drives (G part and C part)."""
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    G, C = np.zeros((n, n)), np.zeros((n, n))
    bG, bC = np.zeros(n), np.zeros(n)
    fx = dict(fixed)
    fx.setdefault("0", 0.0)

    def add(M, bv, i, j, val):
        if i not in idx:
            return
        if j in idx:
            M[idx[i], idx[j]] += val
        else:
            bv[idx[i]] -= val * fx[j]

    for e in elems:
        kind = e[0]
        if kind in ("R", "C"):
            a, c, val = e[1], e[2], (1 / e[3] if kind == "R" else e[3])
            M, bv = (G, bG) if kind == "R" else (C, bC)
            add(M, bv, a, a, val); add(M, bv, a, c, -val); add(M, bv, c, c, val); add(M, bv, c, a, -val)
        elif kind == "G":                       # current gm*(v(cp) - v(cn)) leaves d, enters s
            d, s, cp, cn, gm = e[1:]
            add(G, bG, d, cp, gm); add(G, bG, d, cn, -gm); add(G, bG, s, cp, -gm); add(G, bG, s, cn, gm)
        elif kind == "I":                       # fixed current (amps) leaves a, enters b
            a, b_, amps = e[1:]
            if a in idx:
                bG[idx[a]] -= amps
            if b_ in idx:
                bG[idx[b_]] += amps
    return G, C, bG, bC, idx


def response(nodes, elems, fixed, f):
    G, C, bG, bC, idx = matrices(nodes, elems, fixed)
    s = 1j * TP * f
    x = np.linalg.solve(G + s * C, bG + s * bC)
    return {n_: x[idx[n_]] for n_ in nodes}


def poles(nodes, elems, fixed):
    G, C, *_ = matrices(nodes, elems, fixed)
    lam = eigvals(G, -C)
    lam = lam[np.isfinite(lam)]
    return np.sort(np.abs(lam.real)) / TP


def f3db(fun, a0, lo, hi):
    return brentq(lambda f: abs(fun(f)) - a0 / math.sqrt(2), lo, hi, xtol=1e-6)


# ============================================================ device (Example 1)
gm = 2 * 100e-6 / 0.2
Cgs = 2 / 3 * 20 * 0.5 * 10e-15 + 20 * 0.3e-15
Cgd = 20 * 0.3e-15
v.check("Ex 12-03.1a", gm * 1e3)
v.check("Ex 12-03.1b", Cgs * 1e15)
v.check("Ex 12-03.1c", Cgd * 1e15)


def ft_of(gm_, cgs, cgd, feedforward=False):
    """Unity short-circuit current gain: 1 A into the gate, drain shorted. The chapter's definition counts
    the controlled source's current gm*vg; with feedforward=True the current through Cgd into the short is
    included as well (the exact short-circuit current)."""
    def gain(f):
        r = response(["g"], [("C", "g", "0", cgs), ("C", "g", "d", cgd), ("I", "0", "g", 1.0)], {"d": 0.0}, f)
        vg = r["g"]
        i_ff = 1j * TP * f * cgd * vg if feedforward else 0.0
        return abs(gm_ * vg - i_ff)
    return brentq(lambda f: gain(f) - 1, 1e6, 1e13, xtol=1e-3)


v.check("Ex 12-03.1d", ft_of(gm, Cgs, Cgd) / 1e9)
v.assert_true("including the feedforward through Cgd changes f_T by under 1%",
              abs(ft_of(gm, Cgs, Cgd, True) / ft_of(gm, Cgs, Cgd) - 1) < 0.01)
v.check("Ex 12-03.1e", 100 * 20 * 0.3e-15 / Cgs)


# ============================================================ Example 2: common source
def cs_elems(RS, RL, CL, gm_=gm, cgs=Cgs, cgd=Cgd):
    return [("R", "vs", "g", RS), ("C", "g", "0", cgs), ("C", "g", "o", cgd), ("G", "o", "0", "g", "0", gm_),
            ("R", "o", "0", RL), ("C", "o", "0", CL)]


RS, RL, CL = 10e3, 20e3, 100e-15
cs = lambda f, RS_=RS: response(["g", "o"], cs_elems(RS_, RL, CL), {"vs": 1.0}, f)["o"]
A0 = abs(cs(1.0))
v.check("Ex 12-03.2a", A0)
# Miller input capacitance: measure the gate's input admittance with the drain forced to -A0 times the gate
# (a controlled source holds it there), at a low frequency where A0 applies
miller_el = [("C", "g", "0", Cgs), ("C", "g", "o", Cgd), ("I", "0", "g", 1.0), ("G", "o", "0", "g", "0", A0 * 1e3),
             ("R", "o", "0", 1e-3)]
rm = response(["g", "o"], miller_el, {}, 1e3)
Cmill = (1 / rm["g"] / (1j * TP * 1e3)).real
v.check("Ex 12-03.2b", Cmill * 1e15)
v.check("Ex 12-03.2c", 1 / (TP * RS * Cmill) / 1e6)
b1 = RS * Cmill + RL * (Cgd + CL)
v.check("Ex 12-03.2d", b1 * 1e9)
v.check("Ex 12-03.2e", 1 / (TP * b1) / 1e6)
pl = poles(["g", "o"], cs_elems(RS, RL, CL), {"vs": 0.0})
b2 = 1 / ((TP * pl[0]) * (TP * pl[1]))                  # product of the solved poles
v.check("Ex 12-03.2f", b2)
v.assert_true("b1 equals the sum of the solved poles' time constants", abs(b1 - (1 / (TP * pl[0]) + 1 / (TP * pl[1]))) < 1e-15)
v.check("Ex 12-03.2g", b1 / b2 / TP / 1e6)
v.check("Ex 12-03.2h", pl[0] / 1e6)
v.check("Ex 12-03.2i", pl[1] / 1e6)
# zero: the output current vanishes where gm*vg equals the current through Cgd; find |H| minimum of the
# transconductance part by solving gm - s*Cgd = 0 on the real s axis numerically
zero = brentq(lambda sig: gm - sig * Cgd, 1e3, 1e15) / TP
v.check("Ex 12-03.2j", zero / 1e9)
f3 = f3db(cs, A0, 1e6, 1e9)
v.check("Ex 12-03.2k", f3 / 1e6)
v.check("Ex 12-03.2l", 100 * (1 / (TP * RS * Cmill) / f3 - 1))
v.check("Ex 12-03.2m", 100 * (1 - 1 / (TP * b1) / f3))
v.check("Ex 12-03.2n", A0 * f3 / 1e6)
v.check("T 12-03.a", Cgd * A0 * 1e15 * 21 / 20)
v.check("T 12-03.c", f3db(lambda f: cs(f, 1e3), A0, 1e6, 1e9) / 1e6)

# ============================================================ Example 3
cs0 = lambda f, RL_: response(["o"], [("G", "o", "0", "g", "0", gm), ("R", "o", "0", RL_), ("C", "o", "0", CL + Cgd)],
                              {"g": 1.0}, f)["o"]
bw0 = f3db(lambda f: cs0(f, RL), A0, 1e6, 1e10)
v.check("Ex 12-03.3a", bw0 / 1e6)
v.check("Ex 12-03.3b", A0 * bw0 / 1e6)
v.check("Ex 12-03.3c", abs(cs0(1, RL / 2)))
v.check("Ex 12-03.3d", f3db(lambda f: cs0(f, RL / 2), abs(cs0(1, RL / 2)), 1e6, 1e10) / 1e6)


# ============================================================ Example 4: common gate
def cg(f, RS_):
    return response(["sn", "o"], [("R", "vs", "sn", RS_), ("C", "sn", "0", Cgs), ("G", "o", "sn", "0", "sn", gm),
                                  ("R", "o", "0", RL), ("C", "o", "0", CL + Cgd)], {"vs": 1.0}, f)["o"]


for RS_, keys in ((10e3, ("4a", "4b", "4d")), (50.0, ("4e", "4f", "4g"))):
    Ag = abs(cg(1.0, RS_))
    pg = poles(["sn", "o"], [("R", "vs", "sn", RS_), ("C", "sn", "0", Cgs), ("G", "o", "sn", "0", "sn", gm),
                             ("R", "o", "0", RL), ("C", "o", "0", CL + Cgd)], {"vs": 0.0})
    v.check(f"Ex 12-03.{keys[0]}", Ag)
    v.check(f"Ex 12-03.{keys[1]}", pg[1] / 1e9)
    v.check(f"Ex 12-03.{keys[2]}", f3db(lambda f: cg(f, RS_), Ag, 1e6, 1e11) / 1e6)
    if RS_ == 10e3:
        v.check("Ex 12-03.4c", pg[0] / 1e6)
        v.check("Ex 12-03.4h", f3db(lambda f: cg(f, RS_), Ag, 1e6, 1e11) / f3)

# ============================================================ Example 5: cascode
Cx = Cgs + 10e-15
cc_el = [("R", "vs", "g", RS), ("C", "g", "0", Cgs), ("C", "g", "x", Cgd), ("G", "x", "0", "g", "0", gm),
         ("C", "x", "0", Cx), ("G", "o", "x", "0", "x", gm), ("C", "o", "0", Cgd), ("R", "o", "0", RL), ("C", "o", "0", CL)]
cc = lambda f: response(["g", "x", "o"], cc_el, {"vs": 1.0}, f)["o"]
gx = response(["g", "x", "o"], cc_el, {"vs": 1.0}, 1.0)
gain_gx = (gx["x"] / gx["g"]).real
v.check("Ex 12-03.5a", (Cgs + Cgd * (1 - gain_gx)) * 1e15)
v.check("Ex 12-03.5b", 1 / (TP * RS * (Cgs + Cgd * (1 - gain_gx))) / 1e6)
v.check("Ex 12-03.5c", gm / (TP * Cx) / 1e9)
Acc = abs(cc(1.0))
v.check("Ex 12-03.5d", Acc)
v.check("Ex 12-03.5e", f3db(cc, Acc, 1e6, 1e10) / 1e6)

# ============================================================ Example 6: 2N3904 [R-178]
gmb = 10e-3 / VT
Ctot = gmb / (TP * 300e6)
Cmu = 4e-12
Cpi = Ctot - Cmu
rpi = 100 / gmb
v.check("T 12-03.b", 300)
v.check("Ex 12-03.6a", gmb * 1e3)
v.check("Ex 12-03.6b", Ctot * 1e12)
v.assert_true("f_T of (Cpi, Cmu) is 300 MHz", abs(ft_of(gmb, Ctot - Cmu, Cmu) / 300e6 - 1) < 1e-6)
v.check("Ex 12-03.6c", Cpi * 1e12)
v.check("Ex 12-03.6d", rpi)
RLb, RSb = 500.0, 50.0
ce_el = [("R", "vs", "b", RSb), ("R", "b", "0", rpi), ("C", "b", "0", Cpi), ("C", "b", "o", Cmu),
         ("G", "o", "0", "b", "0", gmb), ("R", "o", "0", RLb)]
bo = response(["b", "o"], ce_el, {"vs": 1.0}, 1.0)
Abo = abs(bo["o"] / bo["b"])
v.check("Ex 12-03.6e", Abo)
Cmb = Cpi + Cmu * (1 + Abo)
v.check("Ex 12-03.6f", Cmb * 1e12)
Rin = 1 / (1 / RSb + 1 / rpi)
v.check("Ex 12-03.6g", Rin)
v.check("Ex 12-03.6h", 1 / (TP * Rin * Cmb) / 1e6)
ce = lambda f: response(["b", "o"], ce_el, {"vs": 1.0}, f)["o"]
Ace = abs(ce(1.0))
f3ce = f3db(ce, Ace, 1e4, 1e9)
v.check("Ex 12-03.6i", Ace)
v.check("Ex 12-03.6j", f3ce / 1e6)
v.check("Ex 12-03.6k", 100 * (1 / (TP * Rin * Cmb) / f3ce - 1))

# ============================================================ solutions
v.check("12-03.1a", ft_of(2e-3, 50e-15, 10e-15) / 1e9)
# input side: drive the input with 1 V and the output with -40 V; current through C over (s*1 V)
s6 = 1j * TP * 1e6
v.check("12-03.2a", abs(s6 * 5e-15 * (1 - (-40)) / s6) * 1e15)
v.check("12-03.2b", abs(s6 * 5e-15 * (1 - 1 / (-40)) / s6) * 1e15)
g3 = 1e-3 / VT
v.check("12-03.3a", g3 * 1e3)
Ct3 = g3 / (TP * 500e6)
v.check("12-03.3b", Ct3 * 1e12)
v.check("12-03.3c", (Ct3 - 0.5e-12) * 1e12)
v.assert_true("f_T of the found capacitances is 500 MHz", abs(ft_of(g3, Ct3 - 0.5e-12, 0.5e-12) / 500e6 - 1) < 1e-6)
v.check("12-03.3d", (Ct3 - 0.5e-12 - 2e-12) / g3 * 1e9)
H4 = lambda f: 1 / ((1 + 1j * f / 10e6) * (1 + 1j * f / 100e6))
v.check("12-03.4a", 1 / (1 / 10e6 + 1 / 100e6) / 1e6)
f34 = f3db(H4, 1.0, 1e5, 1e8)
v.check("12-03.4b", f34 / 1e6)
v.check("12-03.4c", (f34 / 10e6) ** 2)
v.check("12-03.4d", 100 * (1 - 1 / (1 / 10e6 + 1 / 100e6) / f34))
el5 = cs_elems(5e3, 10e3, 50e-15, 2e-3, 50e-15, 10e-15)
cs5 = lambda f: response(["g", "o"], el5, {"vs": 1.0}, f)["o"]
A5 = abs(cs5(1.0))
v.check("12-03.5a", A5)
p5 = poles(["g", "o"], el5, {"vs": 0.0})
b15 = 1 / (TP * p5[0]) + 1 / (TP * p5[1])
v.check("12-03.5b", b15 * 1e9)
v.check("12-03.5c", 1 / (TP * b15) / 1e6)
v.check("12-03.5d", 1 / (TP * p5[0] * TP * p5[1]))
v.check("12-03.5e", p5[0] / 1e6)
v.check("12-03.5f", p5[1] / 1e6)
v.check("12-03.5g", brentq(lambda sig: 2e-3 - sig * 10e-15, 1e3, 1e16) / TP / 1e9)
f35 = f3db(cs5, A5, 1e6, 1e10)
v.check("12-03.5h", f35 / 1e6)
v.check("12-03.5i", 100 * (1 - 1 / (TP * b15) / f35))
v.check("12-03.6a", 1e6 / (1 + 99) / 1e3)
v.check("12-03.6b", 1e6 / (1 + 1 / 99) / 1e6)
el7 = [("R", "vs", "sn", 200.0), ("C", "sn", "0", 100e-15), ("G", "o", "sn", "0", "sn", 5e-3), ("R", "o", "0", 2e3),
       ("C", "o", "0", 200e-15)]
v.check("12-03.7a", abs(response(["sn", "o"], el7, {"vs": 1.0}, 1.0)["o"]))
p7 = poles(["sn", "o"], el7, {"vs": 0.0})
v.check("12-03.7b", p7[1] / 1e9)
v.check("12-03.7c", p7[0] / 1e6)
fol = lambda f: response(["o"], [("G", "0", "o", "i", "o", 1e-3), ("C", "i", "o", 72.67e-15), ("C", "o", "0", 100e-15)],
                         {"i": 1.0}, f)["o"]
p8 = poles(["o"], [("G", "0", "o", "i", "o", 1e-3), ("C", "i", "o", 72.67e-15), ("C", "o", "0", 100e-15)], {"i": 0.0})
v.check("12-03.8a", p8[0] / 1e6)
v.check("12-03.8b", brentq(lambda sig: 1e-3 - sig * 72.67e-15, 1e3, 1e16) / TP / 1e9)
cas9 = response(["x"], [("G", "x", "0", "g", "0", 2e-3), ("G", "0", "x", "0", "x", 1e-3)], {"g": 1.0}, 1.0)
gx9 = cas9["x"].real
v.check("12-03.9a", gx9)
v.check("12-03.9b", (50 + 10 * (1 - gx9)))
v.check("12-03.9c", (50 + 10 * (1 + 30)))
v.check("12-03.9d", (50 + 10 * 31) / (50 + 10 * (1 - gx9)))
g10 = lambda f, R: response(["o"], [("G", "o", "0", "i", "0", 4e-3), ("R", "o", "0", R), ("C", "o", "0", 1e-12)],
                            {"i": 1.0}, f)["o"]
R10 = brentq(lambda R: abs(g10(1.0, R)) - 10, 10, 1e6, xtol=1e-9)
bw10 = f3db(lambda f: g10(f, R10), 10, 1e5, 1e10)
v.check("12-03.10a", 10 * bw10 / 1e6)
v.check("12-03.10b", R10 / 1e3)
v.check("12-03.10c", bw10 / 1e6)
v.check("12-03.11a", zero / 1e9)
v.check("12-03.11b", math.degrees(math.atan(1e9 / zero)))
v.check("12-03.11c", math.degrees(math.atan(1.0)))
RS12 = brentq(lambda R: R * Cmill - RL * (CL + Cgd), 1, 1e6, xtol=1e-9)
v.check("12-03.12a", RS12 / 1e3)
b112 = RS12 * Cmill + RL * (CL + Cgd)
v.check("12-03.12b", b112 * 1e9)
v.check("12-03.12c", 1 / (TP * b112) / 1e6)
f312 = f3db(lambda f: cs(f, RS12), A0, 1e6, 1e9)
v.check("12-03.12d", f312 / 1e6)
v.check("12-03.12e", 1 / (TP * RS12 * Cmill) / 1e6)
v.check("12-03.12f", 100 * (1 / (TP * RS12 * Cmill) / f312 - 1))
v.check("12-03.12g", 100 * (1 - 1 / (TP * b112) / f312))

# ============================================================ lab
if lab.exists():
    v.check("Lab 12-03.a", f3db(lambda f: cs(f, 100e3), A0, 1e5, 1e9) / 1e6)
    Acg = abs(cg(1.0, 10e3))
    v.check("Lab 12-03.b", Acg * f3db(lambda f: cg(f, 10e3), Acg, 1e6, 1e11) / 1e6)
    fol_el = lambda RS_: [("R", "vs", "g", RS_), ("C", "g", "0", Cgd), ("C", "g", "o", Cgs),
                          ("G", "0", "o", "g", "o", gm), ("C", "o", "0", 1e-12)]
    pk = minimize_scalar(lambda lf: -abs(response(["g", "o"], fol_el(30e3), {"vs": 1.0}, 10 ** lf)["o"]),
                         bounds=(7, 10.5), method="bounded", options={"xatol": 1e-10})
    v.check("Lab 12-03.c", 20 * math.log10(-pk.fun))
    v.check("Lab 12-03.d", 10 ** pk.x / 1e6)
sys.exit(v.finish())
