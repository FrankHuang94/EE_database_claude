#!/usr/bin/env python3
"""Verify every number in chapter 12-08 (op-amp internals), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- the two-stage op-amp and the folded cascode by complex nodal analysis of their small-signal circuits
  (the folded cascode transistor by transistor: input device, folding source, PMOS cascode, NMOS cascode
  and bottom source), with crossover and phase margin by root finding and unwrapped phase;
- cascode output resistances by injecting a test current into the solved circuit;
- slew rates by integrating a large-signal model through a step: a square-law input pair whose output
  current saturates at its tail current, and a square-law second stage that can cut off.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, fsolve

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "12-08-op-amp-internals.md", COURSE / "solutions" / "12-08-solutions.md"]
lab = COURSE / "labs" / "12-08-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-08", *files)
TP = 2 * math.pi
VT = 0.025852
LAM = 0.1
ro = lambda i: 1 / (LAM * i)  # noqa: E731


# ============================================================ complex nodal analysis
def solve(nodes, elems, fixed, f):
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
            a, c = e[1], e[2]
            y = 1 / e[3] if e[0] == "R" else s * e[3]
            add(a, a, y); add(a, c, -y); add(c, c, y); add(c, a, -y)
        elif e[0] == "G":                       # gm*(v(cp) - v(cn)) leaves d, enters s
            d, sn, cp, cn, gm = e[1:]
            add(d, cp, gm); add(d, cn, -gm); add(sn, cp, -gm); add(sn, cn, gm)
        elif e[0] == "I":                       # amps leave a, enter b
            if e[1] in idx:
                b[idx[e[1]]] -= e[3]
            if e[2] in idx:
                b[idx[e[2]]] += e[3]
    x = np.linalg.solve(Y, b)
    return {n: x[idx[n]] for n in nodes}


def margins(A, lo=1.0, hi=1e11):
    fc = brentq(lambda f: abs(A(f)) - 1, lo, hi, xtol=1e-6, rtol=1e-15)
    fs = np.geomspace(lo, fc, 3000)
    ph = np.degrees(np.unwrap(np.angle([A(f) for f in fs])))[-1]
    return fc, 180 + float(ph)


def two_stage(gm1, R1, C1, gm6, R2, CL, Cc):
    el = [("G", "n1", "0", "in", "0", gm1), ("R", "n1", "0", R1), ("C", "n1", "0", C1),
          ("G", "n2", "0", "n1", "0", gm6), ("R", "n2", "0", R2), ("C", "n2", "0", CL), ("C", "n1", "n2", Cc)]
    return lambda f: solve(["n1", "n2"], el, {"in": 1.0}, f)["n2"]


def mos(d, g, s, gm, r):
    """Small-signal MOSFET: gm*(v_g - v_s) from drain to source, and r_o from drain to source."""
    return [("G", d, s, g, s, gm), ("R", d, s, r)]


def folded(gm1, ro1, ro_src, gmc, roc, gmn, ron, ro_bot, Cf, CL, up=True, down=True):
    el = [("G", "fold", "0", "in", "0", gm1), ("R", "fold", "0", ro1), ("R", "fold", "0", ro_src),
          ("C", "fold", "0", Cf), ("C", "out", "0", CL)]
    if up:
        el += mos("out", "0", "fold", gmc, roc)                    # PMOS cascode, gate at AC ground
    if down:
        el += mos("out", "0", "nb", gmn, ron) + [("R", "nb", "0", ro_bot)]   # NMOS cascode on its source
    return el


def fc_gain(el):
    return lambda f: -solve(["fold", "out", "nb"], el, {"in": 1.0}, f)["out"]   # non-inverting input


def r_test(el, node):
    el = list(el) + [("I", "0", node, 1.0)]
    nodes = sorted({n for e in el for n in (e[1:3] if e[0] in "RCI" else e[1:5])} - {"0", "in"})
    return float(np.real(solve(nodes, el, {"in": 0.0}, 0.0)[node]))


# ============================================================ large-signal slew simulation
def slew(I7, k6, R2, Iss=20e-6, k1=5e-4, R1=500e3, C1=0.2e-12, Cc=1.1e-12, CL=5e-12):
    """Max |dv_out/dt| (V/us) of a unity-gain follower for a +1 V step (-0.5 to 0.5 V) and a -1 V step."""
    Vov6 = math.sqrt(2 * I7 / k6)
    lim = math.sqrt(2 * Iss / k1)

    def i1(vid):                                           # differential output current of the square-law pair
        if abs(vid) >= lim:
            return math.copysign(Iss, vid)
        return (k1 / 2) * vid * math.sqrt(4 * Iss / k1 - vid * vid)

    def i6(v1):                                            # M6 current above its bias, cut off below -V_ov6
        return (k6 / 2) * (Vov6 + v1) ** 2 - I7 if v1 > -Vov6 else -I7

    Cinv = np.linalg.inv(np.array([[C1 + Cc, -Cc], [-Cc, CL + Cc]]))
    rates = []
    for v0, vs in ((-0.5, 0.5), (0.5, -0.5)):
        x0 = fsolve(lambda x: [-i1(v0 - x[1]) - x[0] / R1, -i6(x[0]) - x[1] / R2], [0.0, v0], xtol=1e-12)
        sol = solve_ivp(lambda t, x: Cinv @ np.array([-i1(vs - x[1]) - x[0] / R1, -i6(x[0]) - x[1] / R2]),
                        (0, 2e-6), x0, method="Radau", max_step=1e-9, rtol=1e-9, atol=1e-12)
        v.assert_true(f"follower settles to the step ({vs:+.1f} V)", abs(sol.y[1][-1] - vs) < 2e-3)
        rates.append(float(np.max(np.abs(np.gradient(sol.y[1], sol.t)))) / 1e6)
    return rates


# ============================================================ Example 1
Iss, Vov, I7 = 20e-6, 0.2, 100e-6
gm1 = 2 * (Iss / 2) / Vov
R1 = 1 / (1 / ro(Iss / 2) + 1 / ro(Iss / 2))
gm6 = 2 * I7 / Vov
R2 = 1 / (1 / ro(I7) + 1 / ro(I7))
CL, C1 = 5e-12, 0.2e-12
Cc = 0.22 * CL
A1 = two_stage(gm1, R1, C1, gm6, R2, CL, Cc)
v.check("T 12-08.a", 2 * VT * 1e3)
v.check("Ex 12-08.1a", gm1 * 1e6)
v.check("Ex 12-08.1b", R1 / 1e3)
v.check("Ex 12-08.1c", gm1 * R1)
v.check("Ex 12-08.1d", gm6 * 1e3)
v.check("Ex 12-08.1e", R2 / 1e3)
v.check("Ex 12-08.1f", gm6 * R2)
v.check("Ex 12-08.1g", abs(A1(1e-3)))
v.check("Ex 12-08.1h", 20 * math.log10(abs(A1(1e-3))))
v.check("Ex 12-08.1i", Cc * 1e12)
v.check("Ex 12-08.1j", gm1 / (TP * Cc) / 1e6)
v.check("Ex 12-08.1k", gm6 / (TP * CL) / 1e6)
v.check("Ex 12-08.1l", gm6 / (TP * Cc) / 1e6)
fc1, pm1 = margins(A1)
v.check("Ex 12-08.1m", pm1)
v.check("Ex 12-08.1n", fc1 / 1e6)

# ============================================================ Example 2 and 3: slew
v.check("Ex 12-08.2a", Iss / Cc / 1e6)
v.check("Ex 12-08.2b", I7 / (CL + Cc) / 1e6)
v.check("Ex 12-08.2c", (Iss / Cc) / (gm1 / Cc))
v.check("Ex 12-08.2d", min(Iss / Cc, I7 / (CL + Cc)) / (TP * 1.0) / 1e6)
k1 = 2 * (Iss / 2) / Vov ** 2
k6 = 2 * I7 / Vov ** 2
rise, fall = slew(I7, k6, R2)
v.check("Ex 12-08.2e", rise)
v.check("Ex 12-08.2f", fall)
v.assert_true("simulated slew within 3% of the formulas", abs(rise / (I7 / (CL + Cc) / 1e6) - 1) < 0.03
              and abs(fall / (Iss / Cc / 1e6) - 1) < 0.03)
v.check("Ex 12-08.3a", 2 * VT * gm1 / Cc / 1e6)
v.check("Ex 12-08.3b", Vov / (2 * VT))

# ============================================================ Example 4: folded cascode
gmi = 2 * 50e-6 / Vov
el4 = folded(gmi, ro(50e-6), ro(100e-6), gmi, ro(50e-6), gmi, ro(50e-6), ro(50e-6), 0.5e-12, 2e-12)
Rf = 1 / (1 / ro(50e-6) + 1 / ro(100e-6))
fold_up = [("R", "fold", "0", ro(50e-6)), ("R", "fold", "0", ro(100e-6))] + mos("out", "0", "fold", gmi, ro(50e-6))
fold_dn = mos("out", "0", "nb", gmi, ro(50e-6)) + [("R", "nb", "0", ro(50e-6))]
Rup, Rdn, Rout = r_test(fold_up, "out"), r_test(fold_dn, "out"), r_test(fold_up + fold_dn, "out")
v.check("Ex 12-08.4a", Rf / 1e3)
v.check("Ex 12-08.4b", Rup / 1e6)
v.check("Ex 12-08.4c", Rdn / 1e6)
v.check("Ex 12-08.4d", Rout / 1e6)
v.check("Ex 12-08.4e", gmi * Rout)
v.check("Ex 12-08.4f", 20 * math.log10(gmi * Rout))
A4 = fc_gain(el4)
v.check("Ex 12-08.4g", abs(A4(1e-2)))
v.check("Ex 12-08.4h", gmi / (TP * 2e-12) / 1e6)
v.check("Ex 12-08.4i", 100e-6 / 2e-12 / 1e6)
v.check("Ex 12-08.4j", gmi / (TP * 0.5e-12) / 1e6)
v.check("Ex 12-08.4k", 90 - math.degrees(math.atan((gmi / 2e-12) / (gmi / 0.5e-12))))
fc4, pm4 = margins(A4)
v.check("Ex 12-08.4l", pm4)
v.check("Ex 12-08.4m", fc4 / 1e6)

# ============================================================ Example 5: CMFB
dV = 0.001 * 50e-6 * Rout
v.check("Ex 12-08.5a", dV)
v.check("Ex 12-08.5b", 0.5e-3 * Rout)
v.check("Ex 12-08.5c", dV / (1 + 0.5e-3 * Rout) * 1e3)

# ============================================================ Example 6: rail-to-rail seam
v.check("Ex 12-08.6a", 0.5 + 0.2 + 0.2)
v.check("Ex 12-08.6b", 2.5 - (0.5 + 0.2 + 0.2))
v.check("Ex 12-08.6c", 2 * gm1 / (TP * Cc) / 1e6)
fc6, pm6 = margins(two_stage(2 * gm1, R1, C1, gm6, R2, CL, Cc))
v.check("Ex 12-08.6d", pm6)
v.check("Ex 12-08.6e", fc6 / 1e6)
# constant-gm: a quarter of each tail current halves each pair's g_m (square law), so the sum is unchanged
v.assert_true("quartered currents restore the single-pair g_m", abs(2 * math.sqrt(k1 * Iss / 4) / gm1 - 1) < 1e-12)

# ============================================================ guided exercise and practitioner ratios
v.check("Sim 12-08.a", 200e-6 / (CL + Cc) / 1e6)
r2, f2 = slew(200e-6, 2 * 200e-6 / Vov ** 2, 1 / (2 / ro(200e-6)))
v.check("Sim 12-08.b", r2)
v.check("Sim 12-08.c", f2)
for key, sr, gbw in (("Prac 12-08.a", 6.5e6, 10e6), ("Prac 12-08.b", 0.16e6, 350e3), ("Prac 12-08.c", 27e6, 40e6)):
    v.check(key, sr / (TP * gbw))

# ============================================================ solutions
v.check("12-08.1a", 0.2e-3 * 400e3)
v.check("12-08.1b", 2e-3 * 40e3)
A_p1 = two_stage(0.2e-3, 400e3, 0.1e-12, 2e-3, 40e3, 1e-12, 0.5e-12)
v.check("12-08.1c", abs(A_p1(1e-4)))
v.check("12-08.1d", 20 * math.log10(abs(A_p1(1e-4))))
v.check("12-08.2a", 50e-6 / 2e-12 / 1e6)
v.check("12-08.2b", 2 / (50e-6 / 2e-12) * 1e9)
v.check("12-08.3a", 10e6 / (TP * 2) / 1e3)
v.check("12-08.4a", TP * 20e6 * 0.15 / 1e6)
v.check("12-08.4b", TP * 20e6 * 2 * VT / 1e6)
gmb = 50e-6 / VT
v.check("12-08.5a", gmb * 1e3)
v.check("12-08.5b", brentq(lambda r: 2 * VT * (1 + gmb * r) / (2 * VT) - 4, 1, 1e5, xtol=1e-9))
v.check("12-08.6a", 50e-6 / 2e-12 / 1e6)
v.check("12-08.6b", 200e-6 / 12e-12 / 1e6)
v.check("12-08.6c", brentq(lambda i: i / 12e-12 - 50e-6 / 2e-12, 1e-6, 1e-3, xtol=1e-15) * 1e6)
up7 = [("R", "fold", "0", 50e3)] + mos("out", "0", "fold", 1e-3, 100e3)
dn7 = mos("out", "0", "nb", 1e-3, 100e3) + [("R", "nb", "0", 100e3)]
Rup7, Rdn7, Rout7 = r_test(up7, "out"), r_test(dn7, "out"), r_test(up7 + dn7, "out")
v.check("12-08.7a", Rup7 / 1e6)
v.check("12-08.7b", Rdn7 / 1e6)
v.check("12-08.7c", Rout7 / 1e6)
v.check("12-08.7d", 1e-3 * Rout7)
v.check("12-08.7e", 20 * math.log10(1e-3 * Rout7))
v.check("12-08.8a", 1e-3 / (TP * 3e-12) / 1e6)
v.check("12-08.8b", 1e-3 / (TP * 0.4e-12) / 1e6)
v.check("12-08.8c", 90 - math.degrees(math.atan((1e-3 / 3e-12) / (1e-3 / 0.4e-12))))
v.check("12-08.9a", 0.005 * 100e-6 * Rout7)
v.check("12-08.9b", 0.2e-3 * Rout7)
v.check("12-08.9c", 0.005 * 100e-6 * Rout7 / (1 + 0.2e-3 * Rout7) * 1e3)
v.check("12-08.10a", 0.6 + 0.2 + 0.2)
v.check("12-08.10b", 3.3 - 1.0)
v.check("12-08.10c", (math.sqrt(k1 * Iss) * 2) / math.sqrt(k1 * Iss))
CL11 = 4e-12
Cc11 = 0.22 * CL11
g1 = brentq(lambda g: g / (TP * Cc11) - 20e6, 1e-6, 1e-2, xtol=1e-18)
g6 = 10 * g1
Iss11, I6 = g1 * Vov, g6 * Vov / 2
v.check("12-08.11a", Cc11 * 1e12)
v.check("12-08.11b", g1 * 1e6)
v.check("12-08.11c", g6 * 1e3)
v.check("12-08.11d", Iss11 * 1e6)
v.check("12-08.11e", I6 * 1e6)
v.check("12-08.11f", Iss11 / Cc11 / 1e6)
v.check("12-08.11g", I6 / (CL11 + Cc11) / 1e6)
R1_12 = 1 / (2 / ro(Iss11 / 2))
R2_12 = 1 / (2 / ro(I6))
A12 = two_stage(g1, R1_12, 0.15e-12, g6, R2_12, CL11, Cc11)
v.check("12-08.12a", R1_12 / 1e3)
v.check("12-08.12b", R2_12 / 1e3)
v.check("12-08.12c", abs(A12(1e-4)))
fc12, pm12 = margins(A12)
v.check("12-08.12d", pm12)
v.check("12-08.12e", fc12 / 1e6)
x20 = brentq(lambda x: margins(two_stage(x * g1, R1_12, 0.15e-12, x * g6, R2_12, CL11, Cc11))[0] - 20e6,
             1.0, 1.5, xtol=1e-9)
v.check("12-08.12f", 100 * (x20 - 1))
v.check("12-08.12g", Iss11 / 2 * 1e6)

# ============================================================ lab README
if lab.exists():
    R1h, R2h = 1 / (2 / (1 / (0.05 * Iss / 2))), 1 / (2 / (1 / (0.05 * I7)))
    v.check("Lab 12-08.a", gm1 * R1h * gm6 * R2h)
    fcl, pml = margins(two_stage(gm1, R1, C1, gm6, R2, 10e-12, Cc))
    v.check("Lab 12-08.b", pml)
    v.check("Lab 12-08.c", fcl / 1e6)

sys.exit(v.finish())
