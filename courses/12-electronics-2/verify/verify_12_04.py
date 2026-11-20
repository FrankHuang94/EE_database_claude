#!/usr/bin/env python3
"""Verify every number in chapter 12-04 (high-frequency analysis methods), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- the resistance seen by each capacitor by injecting a test current in the solved DC small-signal circuit,
  with the other capacitors removed (open) or replaced by a near-short, as each method requires;
- b1 and b2 from the poles of the full circuit (generalized eigenvalues of G + sC), not from the sums;
- corner frequencies and peaks by root finding and bounded optimization on the solved response;
- the follower's Q and natural frequency from its solved poles.
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
files = [COURSE / "chapters" / "12-04-high-frequency-analysis-methods.md", COURSE / "solutions" / "12-04-solutions.md"]
lab = COURSE / "labs" / "12-04-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-04", *files)
TP = 2 * math.pi


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




def coeffs(nodes, elems, fixed):
    """Normalized denominator coefficients b1, b2 from the circuit's poles (eigenvalues of G + sC)."""
    G, C, *_ = matrices(nodes, elems, fixed)
    lam = eigvals(G, -C)
    lam = lam[np.isfinite(lam)]
    b1 = float(np.real(-np.sum(1 / lam)))
    b2 = float(np.real(sum(1 / (lam[i] * lam[k]) for i in range(len(lam)) for k in range(i + 1, len(lam)))))
    return b1, b2


def seen(nodes, resistive, a, b, shorts=()):
    """Resistance between nodes a and b of the resistive/controlled-source circuit, other capacitors open,
    the listed node pairs shorted (by a 1e-6 ohm resistor)."""
    el = list(resistive) + [("R", p, q, 1e-6) for p, q in shorts] + [("I", b, a, 1.0)]
    r = response(nodes, el, {}, 0.0)
    va = r[a] if a in r else 0.0
    vb = r[b] if b in r else 0.0
    return float(np.real(va - vb))


# ============================================================ Example 1: OCTC of a common-source stage
gm, Cgs, Cgd, CL, RS, RL = 1e-3, 2 / 3 * 20 * 0.5 * 10e-15 + 6e-15, 6e-15, 100e-15, 10e3, 20e3
res = [("R", "g", "0", RS), ("G", "d", "0", "g", "0", gm), ("R", "d", "0", RL)]
Rgs0 = seen(["g", "d"], res, "g", "0")
Rgd0 = seen(["g", "d"], res, "g", "d")
RL0 = seen(["g", "d"], res, "d", "0")
v.check("Ex 12-04.1a", Rgs0 / 1e3)
v.check("Ex 12-04.1b", Rgs0 * Cgs * 1e9)
v.check("Ex 12-04.1c", Rgd0 / 1e3)
v.check("Ex 12-04.1d", Rgd0 * Cgd * 1e9)
v.check("Ex 12-04.1e", RL0 * CL * 1e9)
taus = [Rgs0 * Cgs, Rgd0 * Cgd, RL0 * CL]
cs_full = res + [("C", "g", "0", Cgs), ("C", "g", "d", Cgd), ("C", "d", "0", CL)]
b1, b2 = coeffs(["g", "d"], cs_full, {})
v.assert_true("sum of open-circuit time constants equals b1 of the full circuit", abs(sum(taus) / b1 - 1) < 1e-9)
v.check("Ex 12-04.1f", b1 * 1e9)
v.check("Ex 12-04.1g", 1 / (TP * b1) / 1e6)
v.check("Ex 12-04.1h", 100 * taus[2] / b1)
v.check("Ex 12-04.1i", 100 * taus[1] / b1)
v.check("Ex 12-04.1j", Rgd0 / Rgs0)

# ============================================================ Example 2: zero-value time constants
Rgd_gs = seen(["g", "d"], res, "g", "d", shorts=[("g", "0")])
RL_gs = seen(["g", "d"], res, "d", "0", shorts=[("g", "0")])
RL_gd = seen(["g", "d"], res, "d", "0", shorts=[("g", "d")])
Rgd_L = seen(["g", "d"], res, "g", "d", shorts=[("d", "0")])
v.check("Ex 12-04.2a", Rgd_gs / 1e3)
v.check("Ex 12-04.2b", RL_gd)
zv = Rgs0 * Cgs * (Rgd_gs * Cgd + RL_gs * CL) + Rgd0 * Cgd * RL_gd * CL
v.assert_true("zero-value sum equals b2 of the full circuit", abs(zv / b2 - 1) < 1e-6)
v.check("Ex 12-04.2c", b2)
v.check("Ex 12-04.2d", b1 / b2 / TP / 1e6)
v.check("Ex 12-04.2e", Rgd0 * RL_gd)
v.assert_true("pair symmetry R_gd0 R_L^gd = R_L0 R_gd^L", abs(Rgd0 * RL_gd / (RL0 * Rgd_L) - 1) < 1e-6)

# ============================================================ Example 3: SCTC of a discrete amplifier
Rsig, RG, CC1, RSS, CSb, gm3, RD, RLo, CC2 = 1e3, 1e6, 0.1e-6, 2e3, 10e-6, 4e-3, 5e3, 10e3, 1e-6
base = [("R", "vs", "a", Rsig), ("R", "g", "0", RG), ("G", "d", "sn", "g", "sn", gm3), ("R", "sn", "0", RSS),
        ("R", "d", "0", RD), ("R", "o", "0", RLo)]
nodes3 = ["a", "g", "sn", "d", "o"]
gnd = [("R", "vs", "0", 1e-6)]
R1s = seen(nodes3 + ["vs"], base + gnd, "a", "g", shorts=[("sn", "0"), ("d", "o")])
RSb = seen(nodes3 + ["vs"], base + gnd, "sn", "0", shorts=[("a", "g"), ("d", "o")])
R2s = seen(nodes3 + ["vs"], base + gnd, "d", "o", shorts=[("a", "g"), ("sn", "0")])
w = [1 / (R1s * CC1), 1 / (RSb * CSb), 1 / (R2s * CC2)]
v.check("Ex 12-04.3a", w[0])
v.check("Ex 12-04.3b", RSb)
v.check("Ex 12-04.3c", w[1])
v.check("Ex 12-04.3d", w[2])
v.check("Ex 12-04.3e", sum(w))
v.check("Ex 12-04.3f", sum(w) / TP)
amp3 = base + [("C", "a", "g", CC1), ("C", "sn", "0", CSb), ("C", "d", "o", CC2)]
H3 = lambda f: response(nodes3, amp3, {"vs": 1.0}, f)["o"]
Amid = abs(H3(1e6))
fL = brentq(lambda f: abs(H3(f)) - Amid / math.sqrt(2), 1, 1e4, xtol=1e-9)
v.check("Ex 12-04.3g", fL)
v.check("Ex 12-04.3h", 100 * (sum(w) / TP / fL - 1))
v.check("Ex 12-04.3i", 100 * w[1] / sum(w))


# ============================================================ Example 4: pole splitting
def two_stage(R1, C1, gm2, R2, C2, Cc):
    el = [("R", "n1", "0", R1), ("C", "n1", "0", C1), ("G", "n2", "0", "n1", "0", gm2), ("R", "n2", "0", R2),
          ("C", "n2", "0", C2)]
    if Cc > 0:
        el.append(("C", "n1", "n2", Cc))
    return el


def poles_of(el):
    G, C, *_ = matrices(["n1", "n2"], el, {})
    lam = eigvals(G, -C)
    return np.sort(np.abs(lam[np.isfinite(lam)].real)) / TP


R1, C1, gm2, R2, C2 = 50e3, 50e-15, 4e-3, 12.5e3, 1e-12
p0 = poles_of(two_stage(R1, C1, gm2, R2, C2, 0.0))
v.check("Ex 12-04.4a", p0[1] / 1e6)
v.check("Ex 12-04.4b", p0[0] / 1e6)
el4 = two_stage(R1, C1, gm2, R2, C2, 1e-12)
b14, b24 = coeffs(["n1", "n2"], el4, {})
v.check("Ex 12-04.4c", b14 * 1e6)
v.check("Ex 12-04.4d", 1 / (TP * b14) / 1e3)
v.check("Ex 12-04.4e", b24)
v.check("Ex 12-04.4f", b14 / b24 / TP / 1e6)
p4 = poles_of(el4)
v.check("Ex 12-04.4g", p4[0] / 1e3)
v.check("Ex 12-04.4h", p4[1] / 1e6)
v.check("Ex 12-04.4i", brentq(lambda sg: gm2 - sg * 1e-12, 1, 1e16) / TP / 1e6)
s1 = 1 / (TP * gm2 * R1 * R2 * 1e-12)
s2 = gm2 * 1e-12 / (C1 * C2 + 1e-12 * (C1 + C2)) / TP
v.check("Ex 12-04.4j", s1 / 1e3)
v.check("Ex 12-04.4k", s2 / 1e6)
v.check("Ex 12-04.4l", max(abs(s1 / p4[0] - 1), abs(s2 / p4[1] - 1)) * 100)
p01 = poles_of(two_stage(R1, C1, gm2, R2, C2, 0.1e-12))
v.check("Ex 12-04.4m", p01[0] / 1e3)
v.check("Ex 12-04.4n", p01[1] / 1e6)


# ============================================================ Example 5: follower peaking
def fol_el(RS_, CL_, gm_=gm, cgs=Cgs, cgd=Cgd):
    return [("R", "vs", "g", RS_), ("C", "g", "0", cgd), ("C", "g", "o", cgs), ("G", "0", "o", "g", "o", gm_),
            ("C", "o", "0", CL_)]


def q_f0(RS_, CL_, gm_=gm, cgs=Cgs, cgd=Cgd):
    G, C, *_ = matrices(["g", "o"], fol_el(RS_, CL_, gm_, cgs, cgd), {"vs": 0.0})
    lam = eigvals(G, -C)
    lam = lam[np.isfinite(lam)]
    w0 = math.sqrt(abs(np.prod(lam)))
    return w0 / abs(np.sum(lam).real), w0 / TP                 # Q = w0 / (sum of -poles)


Sig = Cgs * Cgd + Cgd * 1e-12 + Cgs * 1e-12
v.check("Ex 12-04.5a", Sig * 1e30)
q30, f30 = q_f0(30e3, 1e-12)
q10, f10 = q_f0(10e3, 1e-12)
v.check("Ex 12-04.5b", q30)
v.check("Ex 12-04.5c", f30 / 1e6)
v.check("Ex 12-04.5d", q10)
v.check("Ex 12-04.5e", f10 / 1e6)
for RS_, kpk, kf in ((30e3, "5f", "5g"), (10e3, "5h", None)):
    pk = minimize_scalar(lambda lf: -abs(response(["g", "o"], fol_el(RS_, 1e-12), {"vs": 1.0}, 10 ** lf)["o"]),
                         bounds=(7, 10.5), method="bounded", options={"xatol": 1e-10})
    v.check(f"Ex 12-04.{kpk}", 20 * math.log10(-pk.fun))
    if kf:
        v.check(f"Ex 12-04.{kf}", 10 ** pk.x / 1e6)
v.check("Ex 12-04.5i", brentq(lambda R: q_f0(R, 1e-12)[0] - 1 / math.sqrt(2), 100, 30e3, xtol=1e-6) / 1e3)

# ============================================================ Example 6: OCTC of a cascode (r_o neglected)
Cx = Cgs + 10e-15
resc = [("R", "g", "0", RS), ("G", "x", "0", "g", "0", gm), ("G", "o", "x", "0", "x", gm), ("R", "o", "0", RL)]
nc = ["g", "x", "o"]
Rx = seen(nc, resc + [("R", "x", "0", 1e12)], "x", "0")
Rgd1 = seen(nc, resc, "g", "x")
tc = [seen(nc, resc, "g", "0") * Cgs, Rgd1 * Cgd, Rx * Cx, seen(nc, resc, "o", "0") * (Cgd + CL)]
v.check("Ex 12-04.6a", Rgd1 / 1e3)
v.check("Ex 12-04.6b", tc[1] * 1e9)
v.check("Ex 12-04.6c", tc[2] * 1e9)
v.check("Ex 12-04.6d", tc[3] * 1e9)
v.check("Ex 12-04.6e", sum(tc) * 1e9)
v.check("Ex 12-04.6f", 1 / (TP * sum(tc)) / 1e6)
casc = resc + [("C", "g", "0", Cgs), ("C", "g", "x", Cgd), ("C", "x", "0", Cx), ("C", "o", "0", Cgd + CL)]
Hc = lambda f: response(nc, [("R", "vs", "g", RS)] + casc[1:], {"vs": 1.0}, f)["o"]
Ac = abs(Hc(1.0))
f3c = brentq(lambda f: abs(Hc(f)) - Ac / math.sqrt(2), 1e6, 1e10, xtol=1)
v.check("Ex 12-04.6g", 100 * (1 - 1 / (TP * sum(tc)) / f3c))
v.check("Ex 12-04.6h", 100 * tc[3] / sum(tc))

# ============================================================ solutions
lad = [("R", "s", "A", 1e3), ("R", "A", "B", 1e3)]
RA = seen(["A", "B"], [("R", "A", "0", 1e3), ("R", "A", "B", 1e3)], "A", "0")
RB = seen(["A", "B"], [("R", "A", "0", 1e3), ("R", "A", "B", 1e3)], "B", "0")
v.check("12-04.1a", RA / 1e3)
v.check("12-04.1b", RB / 1e3)
v.check("12-04.1c", (RA + RB) * 1e-9 * 1e6)
v.check("12-04.1d", 1 / (TP * (RA + RB) * 1e-9) / 1e3)
ladder = [("R", "vs", "A", 1e3), ("C", "A", "0", 1e-9), ("R", "A", "B", 1e3), ("C", "B", "0", 1e-9)]
G1, C1m, *_ = matrices(["A", "B"], ladder, {"vs": 0.0})
pl1 = np.sort(np.abs(eigvals(G1, -C1m).real)) / TP
v.check("12-04.1e", pl1[0] / 1e3)
v.check("12-04.1f", pl1[1] / 1e3)
HL = lambda f: response(["A", "B"], ladder, {"vs": 1.0}, f)["B"]
f3L = brentq(lambda f: abs(HL(f)) - 1 / math.sqrt(2), 1, 1e7, xtol=1e-6)
v.check("12-04.1g", f3L / 1e3)
v.check("12-04.1h", 100 * (1 - 1 / (TP * (RA + RB) * 1e-9) / f3L))
res2 = [("R", "g", "0", 2e3), ("G", "d", "0", "g", "0", 5e-3), ("R", "d", "0", 10e3)]
v.check("12-04.2a", seen(["g", "d"], res2, "g", "d") / 1e3)
res3 = [("R", "g", "0", 5e3), ("G", "d", "0", "g", "0", 2e-3), ("R", "d", "0", 10e3)]
t3 = [seen(["g", "d"], res3, "g", "0") * 50e-15, seen(["g", "d"], res3, "g", "d") * 10e-15,
      seen(["g", "d"], res3, "d", "0") * 50e-15]
v.check("12-04.3a", t3[0] * 1e9)
v.check("12-04.3b", t3[1] * 1e9)
v.check("12-04.3c", t3[2] * 1e9)
b13, b23 = coeffs(["g", "d"], res3 + [("C", "g", "0", 50e-15), ("C", "g", "d", 10e-15), ("C", "d", "0", 50e-15)], {})
v.check("12-04.3d", b13 * 1e9)
v.check("12-04.3e", 1 / (TP * b13) / 1e6)
v.check("12-04.3f", 100 * t3[1] / b13)
v.check("12-04.4a", seen(["g", "d"], res3, "g", "d", shorts=[("g", "0")]) / 1e3)
v.check("12-04.4b", seen(["g", "d"], res3, "d", "0", shorts=[("g", "d")]))
v.check("12-04.4c", b23)
w5 = [1 / ((600 + 10e3) * 1e-6), 1 / ((2e3 + 8e3) * 10e-6)]
v.check("12-04.5a", w5[0])
v.check("12-04.5b", w5[1])
v.check("12-04.5c", sum(w5))
v.check("12-04.5d", sum(w5) / TP)
R6 = seen(["sn"], [("R", "sn", "0", 1e3), ("G", "0", "sn", "0", "sn", 10e-3)], "sn", "0")
v.check("12-04.6a", R6)
v.check("12-04.6b", brentq(lambda C: 1 / (TP * R6 * C) - 20, 1e-7, 1e-2, xtol=1e-15) * 1e6)
el7 = two_stage(100e3, 0.1e-12, 2e-3, 50e3, 2e-12, 2e-12)
b17, b27 = coeffs(["n1", "n2"], el7, {})
p7 = poles_of(el7)
v.check("12-04.7a", b17 * 1e6)
v.check("12-04.7b", b27)
v.check("12-04.7c", p7[0] / 1e3)
v.check("12-04.7d", p7[1] / 1e6)
v.check("12-04.7e", 1 / (TP * 2e-3 * 100e3 * 50e3 * 2e-12) / 1e3)
v.check("12-04.7f", 2e-3 * 2e-12 / (0.1e-12 * 2e-12 + 2e-12 * 2.1e-12) / TP / 1e6)
v.check("12-04.7g", 2e-3 / (TP * 2e-12) / 1e6)
v.check("12-04.8a", (100e-15 * 10e-15 + 10e-15 * 2e-12 + 100e-15 * 2e-12) * 1e30)
q8, f8 = q_f0(20e3, 2e-12, 2e-3, 100e-15, 10e-15)
v.check("12-04.8b", q8)
v.check("12-04.8c", f8 / 1e6)
v.check("12-04.9a", Rgd0 * RL_gd)
cg_res = [("R", "sn", "0", 10e3), ("G", "o", "sn", "0", "sn", gm), ("R", "o", "0", RL)]
t10 = [seen(["sn", "o"], cg_res, "sn", "0") * Cgs, seen(["sn", "o"], cg_res, "o", "0") * 106e-15]
v.check("12-04.10a", t10[0] * 1e9)
v.check("12-04.10b", t10[1] * 1e9)
v.check("12-04.10c", sum(t10) * 1e9)
v.check("12-04.10d", 1 / (TP * sum(t10)) / 1e6)
cg_full = [("R", "vs", "sn", 10e3), ("C", "sn", "0", Cgs), ("G", "o", "sn", "0", "sn", gm), ("R", "o", "0", RL),
           ("C", "o", "0", 106e-15)]
Hcg = lambda f: response(["sn", "o"], cg_full, {"vs": 1.0}, f)["o"]
f3cg = brentq(lambda f: abs(Hcg(f)) - abs(Hcg(1.0)) / math.sqrt(2), 1e6, 1e11, xtol=1)
v.check("12-04.10e", 100 * (1 - 1 / (TP * sum(t10)) / f3cg))

# ============================================================ lab
if lab.exists():
    RSb100 = seen(nodes3 + ["vs"], base + gnd, "sn", "0", shorts=[("a", "g"), ("d", "o")])
    w100 = [1 / (R1s * CC1), 1 / (RSb100 * 100e-6), 1 / (R2s * CC2)]
    v.check("Lab 12-04.a", sum(w100) / TP)
    amp100 = base + [("C", "a", "g", CC1), ("C", "sn", "0", 100e-6), ("C", "d", "o", CC2)]
    H100 = lambda f: response(nodes3, amp100, {"vs": 1.0}, f)["o"]
    A100 = abs(H100(1e6))
    v.check("Lab 12-04.b", brentq(lambda f: abs(H100(f)) - A100 / math.sqrt(2), 0.1, 1e4, xtol=1e-9))
    for RS_, CL_, key in ((100e3, 1e-12, "c"), (10e3, 0.1e-12, "d")):
        pk = minimize_scalar(lambda lf: -abs(response(["g", "o"], fol_el(RS_, CL_), {"vs": 1.0}, 10 ** lf)["o"]),
                             bounds=(6, 11), method="bounded", options={"xatol": 1e-10})
        v.check(f"Lab 12-04.{key}", 20 * math.log10(-pk.fun))
sys.exit(v.finish())
