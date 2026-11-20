#!/usr/bin/env python3
"""Verify every number in chapter 12-02 (active loads, cascodes and multistage amplifiers), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- every gain, output resistance and transconductance by modified nodal analysis of the complete small-signal
  circuit: output resistances by a test current, open-circuit gains with the output unloaded, short-circuit
  transconductances with the output grounded through an ammeter, loaded gains with the load in the matrix;
- DC levels, common-mode limits and currents from the square law solved for the operating point;
- the follower's gain from its small-signal circuit with an explicit body-effect source;
- offsets referred to the input by applying an input offset and finding the input that nulls the output.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "12-02-active-loads-cascodes-multistage.md", COURSE / "solutions" / "12-02-solutions.md"]
lab = COURSE / "labs" / "12-02-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-02", *files)
db = lambda r: 20 * math.log10(abs(r))
VT0 = 0.5


# ============================================================ small-signal nodal solver
def solve(nodes, elems, fixed):
    """Unknown nodes, elements and fixed node voltages ('0' is ground). Elements:
    ('R', a, b, ohms); ('I', a, b, amps): current from a to b through the source (leaves a, enters b);
    ('G', d, s, cp, cn, gm): current gm*(v(cp) - v(cn)) leaves d and enters s;
    ('M', d, g, s, gm, ro[, gmb]): MOSFET, drain current gm*vgs + gmb*vbs + vds/ro with the body at ground."""
    idx = {n: i for i, n in enumerate(nodes)}
    G = np.zeros((len(nodes), len(nodes)))
    b = np.zeros(len(nodes))
    fx = dict(fixed)
    fx.setdefault("0", 0.0)

    def add(i, j, val):
        if i not in idx:
            return
        if j in idx:
            G[idx[i], idx[j]] += val
        else:
            b[idx[i]] -= val * fx[j]

    def cond(a, c, g):
        add(a, a, g); add(a, c, -g); add(c, c, g); add(c, a, -g)

    def vccs(d, s, cp, cn, gm):
        add(d, cp, gm); add(d, cn, -gm); add(s, cp, -gm); add(s, cn, gm)

    for e in elems:
        if e[0] == "R":
            cond(e[1], e[2], 1 / e[3])
        elif e[0] == "I":
            if e[1] in idx:
                b[idx[e[1]]] -= e[3]
            if e[2] in idx:
                b[idx[e[2]]] += e[3]
        elif e[0] == "G":
            vccs(*e[1:])
        elif e[0] == "M":
            d, g, s, gm, ro = e[1:6]
            vccs(d, s, g, s, gm)
            cond(d, s, 1 / ro)
            if len(e) > 6:
                vccs(d, s, "0", s, e[6])           # body at small-signal ground
    sol = np.linalg.solve(G, b)
    return {n: sol[idx[n]] for n in nodes}


def gm_ro(I, vov, lam):
    """g_m by differentiating the square law numerically at the bias point; r_o = 1/(lam*I)."""
    k = 2 * I / vov ** 2
    h = 1e-6
    gm = (0.5 * k * (vov + h) ** 2 - 0.5 * k * (vov - h) ** 2) / (2 * h)
    return gm, 1 / (lam * I)


def rout_test(elems, nodes, out, fixed):
    r = solve(nodes, elems + [("I", "0", out, 1.0)], fixed)      # 1 A pushed into the output
    return r[out]


# ============================================================ theory
gmT, roT = gm_ro(100e-6, 0.2, 0.1)
v.check("T 12-02.a", gmT * 0.9 / 100e-6)
shift = solve(["o"], [("R", "o", "0", roT), ("R", "o", "0", roT), ("I", "0", "o", 1e-6)], {})["o"]
v.check("T 12-02.b", shift * 1e3)
v.check("T 12-02.c", (gmT * roT) ** 2 / 2)
v.check("T 12-02.d", 130 - 104)
v.check("T 12-02.e", 10 ** (26 / 20))
v.check("T 12-02.f", 10 ** (130 / 20))
v.check("T 12-02.g", shift / 50 * 1e3)
v.check("T 12-02.h", 10e6 / 10 ** (130 / 20))                        # GBW / A_OL [R-182]

# ============================================================ Example 1
gm1, ro1 = gm_ro(100e-6, 0.2, 0.1)
RD = 0.9 / 100e-6
v.check("Ex 12-02.1a", gm1 * 1e3)
v.check("Ex 12-02.1b", RD / 1e3)
cs = lambda load_elems: abs(solve(["o"], [("G", "o", "0", "in", "0", gm1)] + load_elems, {"in": 1.0})["o"])
v.check("Ex 12-02.1c", cs([("R", "o", "0", RD)]))
v.check("Ex 12-02.1d", ro1 / 1e3)
v.check("Ex 12-02.1e", cs([("R", "o", "0", RD), ("R", "o", "0", ro1)]))
v.check("Ex 12-02.1f", cs([("R", "o", "0", ro1)]))
A_act = cs([("R", "o", "0", ro1), ("R", "o", "0", ro1)])           # r_o1 and the PMOS load's r_o2
v.check("Ex 12-02.1g", A_act)
v.check("Ex 12-02.1h", db(A_act))
RDneed = brentq(lambda R: cs([("R", "o", "0", R), ("R", "o", "0", ro1)]) - A_act, 1e3, 1e7, xtol=1e-6)
v.check("Ex 12-02.1i", 100e-6 * RDneed)

# ============================================================ Example 2: five-transistor OTA
gm, ro = gm_ro(100e-6, 0.2, 0.1)
RSS = 1 / (0.1 * 200e-6)
v.check("Ex 12-02.2a", gm * 1e3)
v.check("Ex 12-02.2b", ro / 1e3)
v.check("Ex 12-02.2c", RSS / 1e3)
v.check("Ex 12-02.2d", gm * (ro * ro / (ro + ro)))                 # the hand formula's value, for the key
v.check("Ex 12-02.2e", 1 / (2 * gm * RSS))
v.check("Ex 12-02.2f", gm * (ro / 2) * 2 * gm * RSS)
v.check("Ex 12-02.2g", db(gm * (ro / 2) * 2 * gm * RSS))


def ota(v1, v2, RSS=RSS, gms=(gm, gm, gm, gm), ros=(ro, ro, ro, ro), extra=()):
    g1, g2, g3, g4 = gms
    r1, r2, r3, r4 = ros
    el = [("M", "a", "g1", "s", g1, r1), ("M", "out", "g2", "s", g2, r2),
          ("M", "a", "a", "0", g3, r3), ("M", "out", "a", "0", g4, r4), ("R", "s", "0", RSS)] + list(extra)
    return solve(["s", "a", "out"], el, {"g1": v1, "g2": v2})


Ad_full = abs(ota(0.5, -0.5)["out"])
Acm_full = abs(ota(1.0, 1.0)["out"])
v.check("Ex 12-02.2k", Ad_full)
v.check("Ex 12-02.2l", Acm_full)
v.check("Ex 12-02.2m", Ad_full / Acm_full)
v.check("Ex 12-02.2n", db(Ad_full / Acm_full))
v.assert_true("hand estimates within 3% of the full circuit",
              abs(Ad_full / 50 - 1) < 0.03 and abs(Acm_full / 0.01 - 1) < 0.03 and abs(Ad_full / Acm_full / 5000 - 1) < 0.03)
# DC level: V_SG3 for 100 uA at the PMOS's k (set by 100 uA at 0.2 V overdrive)
kp = 2 * 100e-6 / 0.2 ** 2
VSG3 = brentq(lambda x: 0.5 * kp * (x - VT0) ** 2 - 100e-6, VT0 + 1e-6, 2.0, xtol=1e-14)
v.check("Ex 12-02.2h", 1.8 - VSG3)
kn = kp
vic_min = brentq(lambda vic: (vic - VT0 - math.sqrt(2 * 100e-6 / kn)) - 0.2, 0.5, 1.8, xtol=1e-12)  # tail V_DS = 0.2
v.check("Ex 12-02.2i", vic_min)
vic_max = brentq(lambda vic: (1.8 - VSG3) - (vic - VT0), 0.5, 2.5, xtol=1e-12)            # M1 drain = gate - V_TN
v.check("Ex 12-02.2j", vic_max)
v.check("Ex 12-02.2o", gm * RSS)
v.check("Ex 12-02.2p", (gm * (ro / 2) * 2 * gm * RSS) / (gm * RSS))
v.check("Ex 12-02.2q", 1 / gm / 1e3)

# ============================================================ Example 3: cascode
cas = [("M", "x", "in", "0", gm, ro), ("M", "out", "0", "x", gm, ro)]
Rcas = rout_test(cas, ["x", "out"], "out", {"in": 0.0})
v.check("Ex 12-02.3a", Rcas / 1e6)
Aoc = solve(["x", "out"], cas, {"in": 1.0})["out"]
v.check("Ex 12-02.3b", Aoc)
v.check("Ex 12-02.3c", db(Aoc))
# short-circuit transconductance: output held at 0 V, measure the current into the output node
r_sc = solve(["x"], [("M", "x", "in", "0", gm, ro), ("M", "out", "0", "x", gm, ro)], {"in": 1.0, "out": 0.0})
Gm = abs(gm * (0 - r_sc["x"]) + (0 - r_sc["x"]) / ro)            # M2's drain current with v_out = 0
v.check("Ex 12-02.3d", Gm * 1e3)
pload = [("M", "out", "0", "y", gm, ro), ("M", "y", "0", "0", gm, ro)]
A_cl = solve(["x", "out", "y"], cas + pload, {"in": 1.0})["out"]
v.check("Ex 12-02.3e", abs(A_cl))
v.check("Ex 12-02.3f", db(A_cl))
A_sl = solve(["x", "out"], cas + [("R", "out", "0", ro)], {"in": 1.0})["out"]
v.check("Ex 12-02.3g", abs(A_sl))
v.check("Ex 12-02.3h", db(A_sl))

# ============================================================ Example 4: telescopic
# differential half-circuit: input device (gate driven by v_id/2), NMOS cascode, PMOS cascode load; v_od = 2 v_o
half = solve(["x", "out", "y"], cas + pload, {"in": 0.5})
v.check("Ex 12-02.4a", abs(2 * half["out"]))
vmin, vmax = 0.2 + 0.2 + 0.2, 1.8 - 0.2 - 0.2                    # tail, input, cascode | PMOS cascode, PMOS source
v.check("Ex 12-02.4b", vmax - vmin)
v.check("Ex 12-02.4c", 2 * (vmax - vmin))
v.check("Ex 12-02.4d", (1.8 - 0.2) - 0.2)
v.check("Ex 12-02.4e", ((1.8 - 0.2) - 0.2) / (vmax - vmin))
v.check("Ex 12-02.4f", (1.2 - 0.4) - 0.6)

# ============================================================ Example 5: two stages
gm6, ro6 = gm_ro(400e-6, 0.2, 0.1)
v.check("Ex 12-02.5a", gm6 * 1e3)
v.check("Ex 12-02.5b", ro6 / 1e3)
A2 = abs(solve(["o"], [("M", "o", "in", "0", gm6, ro6), ("R", "o", "0", ro6)], {"in": 1.0})["o"])
v.check("Ex 12-02.5c", A2)
v.check("Ex 12-02.5d", 50 * A2)
v.check("Ex 12-02.5e", db(50 * A2))
# refer a 10 mV second-stage offset: the input that nulls the output of the cascade (gain 50 then A2)
vin_null = brentq(lambda x: (50 * x + 10e-3) * A2, -1, 1, xtol=1e-15)
v.check("Ex 12-02.5f", abs(vin_null) * 1e3)

# ============================================================ Example 6: DC levels
k6n = 2 * 400e-6 / 0.2 ** 2
I_direct = 0.5 * k6n * (1.1 - VT0) ** 2
v.check("Ex 12-02.6a", I_direct * 1e3)
v.check("Ex 12-02.6b", I_direct / 400e-6)
k4 = 2 * 100e-6 / 0.2 ** 2
k6 = brentq(lambda k: 0.5 * k * 0.2 ** 2 - 400e-6, 1e-6, 1, xtol=1e-15)
v.check("Ex 12-02.6c", k6 / k4)
dVSG = math.sqrt(2 * 400e-6 / k6) - math.sqrt(2 * 380e-6 / k6)     # large-signal change for 400 -> 380 uA
v.check("Ex 12-02.6d", dVSG * 1e3)
v.check("Ex 12-02.6e", dVSG / 50 * 1e3)
kf = 4e-3
vgs_f = brentq(lambda x: 0.5 * kf * (x - VT0) ** 2 - 100e-6, VT0 + 1e-6, 3, xtol=1e-14)
v.check("Ex 12-02.6f", vgs_f)
gmf = math.sqrt(2 * kf * 100e-6)
fol = lambda ro_, gmb: solve(["s"], [("M", "vdd", "in", "s", gmf, ro_, gmb), ("R", "s", "0", ro_)],
                             {"in": 1.0, "vdd": 0.0})["s"]
v.check("Ex 12-02.6g", fol(1e15, 0.2 * gmf))
v.check("Ex 12-02.6h", fol(100e3, 0.2 * gmf))

# ============================================================ solutions
v.check("12-02.1a", (lambda g, r: g * r)(*gm_ro(1e-3, 0.15, 0.2)))
gP2, rn = gm_ro(50e-6, 0.25, 0.1)
rp = 1 / (0.15 * 50e-6)
v.check("12-02.2a", gP2 * 1e3)
v.check("12-02.2b", rn / 1e3)
v.check("12-02.2c", rp / 1e3)
v.check("12-02.2d", rout_test([("R", "o", "0", rn), ("R", "o", "0", rp)], ["o"], "o", {}) / 1e3)
v.check("12-02.2e", abs(solve(["o"], [("M", "o", "in", "0", gP2, rn), ("R", "o", "0", rp)], {"in": 1.0})["o"]))
R3 = rout_test([("M", "x", "in", "0", 2e-3, 20e3), ("M", "out", "0", "x", 2e-3, 20e3)], ["x", "out"], "out", {"in": 0})
v.check("12-02.3a", R3 / 1e3)
v.check("12-02.3b", R3 / 20e3)
g4, r4 = gm_ro(50e-6, 0.2, 0.2)
v.check("12-02.4a", g4 * 1e3)
v.check("12-02.4b", r4 / 1e3)
RSS4 = 1 / (0.2 * 100e-6)
d4 = abs(ota(0.5, -0.5, RSS=RSS4, gms=(g4,) * 4, ros=(r4,) * 4)["out"])
v.check("12-02.4c", g4 * (r4 / 2))
v.assert_true("Problem 4 hand gain within 2% of the full OTA", abs(d4 / (g4 * r4 / 2) - 1) < 0.02)
v.check("12-02.4d", db(g4 * r4 / 2))
# short-circuit output current for 2 mV: output grounded, current into it from M2 and M4
sc = solve(["s", "a"], [("M", "a", "g1", "s", g4, r4), ("M", "out", "g2", "s", g4, r4), ("M", "a", "a", "0", g4, r4),
                        ("M", "out", "a", "0", g4, r4), ("R", "s", "0", RSS4)], {"g1": 1e-3, "g2": -1e-3, "out": 0.0})
# KCL at the grounded output: the short supplies the drain currents of M4 and M2 (each into its drain)
i_d4 = g4 * (sc["a"] - 0) + (0 - 0) / r4
i_d2 = g4 * (-1e-3 - sc["s"]) + (0 - sc["s"]) / r4
i_out = i_d2 + i_d4
v.check("12-02.4e", abs(i_out) * 1e6)                             # full circuit; published as g_m*v_id
v.check("12-02.5a", RSS4 / 1e3)
v.check("12-02.5b", 1 / (2 * g4 * RSS4))
v.check("12-02.5c", (g4 * r4 / 2) * 2 * g4 * RSS4)
v.check("12-02.5d", db((g4 * r4 / 2) * 2 * g4 * RSS4))
v.check("12-02.5e", db(20))
v.check("12-02.5f", db((g4 * r4 / 2) * 2 * g4 * RSS4 * 20))
cm5 = [abs(ota(0.5, -0.5, RSS=R, gms=(g4,) * 4, ros=(r4,) * 4)["out"]) / abs(ota(1, 1, RSS=R, gms=(g4,) * 4,
                                                                                ros=(r4,) * 4)["out"]) for R in (RSS4, 20 * RSS4)]
v.assert_true("full-circuit CMRR rises about 26 dB with a 20x tail", abs(db(cm5[1] / cm5[0]) - 26.02) < 0.5)
A6 = solve(["x", "out"], [("M", "x", "in", "0", 1e-3, 50e3), ("M", "out", "0", "x", 1e-3, 50e3)], {"in": 1.0})["out"]
v.check("12-02.6a", abs(A6))
v.check("12-02.7a", 1.2 - 5 * 0.15)
v.check("12-02.7b", 2 * (1.2 - 5 * 0.15))
v.check("12-02.7c", 1.2 - 2 * 0.15)
st1 = abs(solve(["o"], [("G", "o", "0", "in", "0", 1e-3), ("R", "o", "0", 50e3), ("R", "o", "0", 50e3)], {"in": 1})["o"])
st2 = abs(solve(["o"], [("G", "o", "0", "in", "0", 40e-3), ("R", "o", "0", 10e3)], {"in": 1})["o"])
v.check("12-02.8a", st1)
v.check("12-02.8b", st2)
v.check("12-02.8c", st1 * st2)
v.check("12-02.8d", db(st1 * st2))
st1u = abs(solve(["o"], [("G", "o", "0", "in", "0", 1e-3), ("R", "o", "0", 50e3)], {"in": 1})["o"])
v.check("12-02.8e", st1u * st2)
v.check("12-02.8f", db(st1u / st1))
# offsets: null the output of a three-stage cascade with offsets added at each stage's input
cascade = lambda x, o1, o2, o3: (((x + o1) * 20 + o2) * 50 + o3)
v.check("12-02.9a", abs(brentq(lambda x: cascade(x, 2e-3, 10e-3, 20e-3), -1, 1, xtol=1e-15)) * 1e3)
sens9 = [abs(brentq(lambda x: cascade(x, *o), -1, 1, xtol=1e-15)) for o in ((2e-3, 0, 0), (0, 10e-3, 0), (0, 0, 20e-3))]
v.check("12-02.9b", math.sqrt(sum(s_ ** 2 for s_ in sens9)) * 1e3)
vov10 = brentq(lambda x: 0.5 * 2e-3 * x * x - 50e-6, 1e-4, 2, xtol=1e-15)
v.check("12-02.10a", vov10)
v.check("12-02.10b", VT0 + vov10)
v.check("12-02.10c", 0.6 + vov10)
k11 = 2 * 400e-6 / 0.2 ** 2                  # M6 carries 400 uA at the balanced V_SG (g_m6 = 4 mA/V)
d11 = math.sqrt(2 * 450e-6 / k11) - math.sqrt(2 * 400e-6 / k11)
g11 = gm_ro(400e-6, 0.2, 0.1)[0]
v.check("12-02.11a", 50e-6 / g11 * 1e3)       # the small-signal estimate dI/g_m, as published
v.check("12-02.11b", 50e-6 / g11 / 50 * 1e3)
v.assert_true("large-signal shift within 5% of the small-signal estimate", abs(d11 / (50e-6 / g11) - 1) < 0.05)
g12, r12 = 1e-3, 20e3
a12 = abs(solve(["o"], [("M", "o", "in", "0", g12, r12), ("R", "o", "0", r12)], {"in": 1})["o"])
v.check("12-02.12a", a12)
cas12 = [("M", "x", "in", "0", g12, r12), ("M", "out", "0", "x", g12, r12)]
R12 = rout_test(cas12, ["x", "out"], "out", {"in": 0})
v.check("12-02.12b", R12 / 1e3)
r_sc12 = solve(["x"], cas12, {"in": 1.0, "out": 0.0})
v.check("12-02.12c", abs(g12 * (0 - r_sc12["x"]) - r_sc12["x"] / r12) * 1e3)
b12 = abs(solve(["x", "out"], cas12 + [("R", "out", "0", r12)], {"in": 1})["out"])
c12 = abs(solve(["x", "out", "y"], cas12 + [("M", "out", "0", "y", g12, r12), ("M", "y", "0", "0", g12, r12)],
                {"in": 1})["out"])
v.check("12-02.12d", b12)
v.check("12-02.12e", c12)
v.check("12-02.12f", db(c12))
v.check("12-02.12g", 4 * 0.15)
v.check("12-02.12h", c12 / 0.6)
v.check("12-02.12i", a12 / 0.3)
v.check("12-02.12j", b12 / 0.45)

# ============================================================ lab
if lab.exists():
    Ad5 = abs(ota(0.5, -0.5, RSS=500e3)["out"])
    Acm5 = abs(ota(1.0, 1.0, RSS=500e3)["out"])
    v.check("Lab 12-02.a", db(Ad5 / Acm5))
    v.check("Lab 12-02.b", Acm5)
    A1f = abs(ota(0.5, -0.5)["out"])
    v.check("Lab 12-02.c", abs(brentq(lambda x: (A1f * x + 10e-3) * A2, -1, 1, xtol=1e-15)) * 1e3)
    v.check("Lab 12-02.d", db(abs(ota(0.5, -0.5, RSS=10e3)["out"]) / abs(ota(1.0, 1.0, RSS=10e3)["out"])))

sys.exit(v.finish())
