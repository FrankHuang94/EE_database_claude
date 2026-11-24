#!/usr/bin/env python3
"""Verify every number in chapter 19-10 (synthesis and static timing analysis), its problems and its lab.

Independent routes:
- Liberty lookups with scipy's RegularGridInterpolator (piecewise-linear on the grid, which is bilinear inside a
  cell), not the lab's interpolation; the table values quoted in the text are checked against the data file;
- arrival and required times on the small graphs by enumerating every path (not by graph propagation);
- technology mapping by enumerating every cover with a separately written matcher, and checking that every cover
  computes the target function by evaluating the cells' Liberty function strings on all input combinations;
- graph-based and path-based timing on real tables re-implemented here and compared with the lab engine;
- clock checks by event-time bookkeeping; CRPR by giving the common clock segment one delay on both sides;
- path sigma from an explicit covariance matrix; the lab module is checked against these results.
"""
from __future__ import annotations

import itertools
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import RegularGridInterpolator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-10-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import sta  # noqa: E402
import techmap  # noqa: E402

v = Verifier.from_files("19-10", ROOT / "chapters" / "19-10-synthesis-and-sta.md",
                        ROOT / "solutions" / "19-10-solutions.md", LAB / "README.md")
LIB = json.loads((LAB / "sky130_hd_subset.json").read_text())


# ---------------------------------------------------------------- Liberty lookups, independently
def table(cell, pin, name, lib=LIB):
    arc = lib["cells"][cell]["arcs"][pin]
    return RegularGridInterpolator((arc["index_1"], arc["index_2"]), np.array(arc[name]), method="linear")


def look(cell, pin, name, slew, load, lib=LIB):
    return float(table(cell, pin, name, lib)([[slew, load]])[0])


inv = LIB["cells"]["inv_1"]["arcs"]["A"]
v.assert_true("Example 1 table values match the library",
              inv["index_1"][2] == 0.0531329 and inv["index_1"][3] == 0.122474 and inv["index_2"][2] == 0.00356533
              and inv["index_2"][3] == 0.00952062 and inv["cell_rise"][2][2] == 0.0566328
              and inv["cell_rise"][2][3] == 0.0903158 and inv["cell_rise"][3][2] == 0.0847049
              and inv["cell_rise"][3][3] == 0.1211221 and inv["cell_rise"][2][5] == 0.4194971
              and inv["index_2"][5] == 0.0678883, "")
ts = (0.080 - 0.0531329) / (0.122474 - 0.0531329)
tc = (0.0050 - 0.00356533) / (0.00952062 - 0.00356533)
v.check("Ex 19-10.1a", ts)
v.check("Ex 19-10.1b", tc)
v.check("Ex 19-10.1c", 1e3 * look("inv_1", "A", "cell_rise", 0.0531329, 0.0050))
v.check("Ex 19-10.1d", 1e3 * look("inv_1", "A", "cell_rise", 0.122474, 0.0050))
d_rise = 1e3 * look("inv_1", "A", "cell_rise", 0.080, 0.0050)
d_fall = 1e3 * look("inv_1", "A", "cell_fall", 0.080, 0.0050)
v.check("Ex 19-10.1e", d_rise)
v.check("Txt 19-10.a", d_rise)
v.check("Txt 19-10.b", d_fall)
loads = inv["index_2"]
v.check("Ex 19-10.1f", np.polyfit([loads[3], loads[5]], [inv["cell_rise"][2][3], inv["cell_rise"][2][5]], 1)[0])
v.check("Ex 19-10.1g", np.polyfit([loads[3], loads[5]], [inv["cell_fall"][2][3], inv["cell_fall"][2][5]], 1)[0])
SS = LIB["other_corners"]["ss_100C_1v60"]
ss_lib = {"cells": SS}
v.check("Txt 19-10.c", look("inv_1", "A", "cell_rise", 0.080, 0.0050, ss_lib) / (d_rise / 1e3))
v.check("Txt 19-10.d", look("inv_1", "A", "cell_fall", 0.080, 0.0050, ss_lib) / (d_fall / 1e3))
v.check("Txt 19-10.e", 2 ** 40)
v.assert_true("lab interpolation agrees", all(
    abs(sta.arc_delay(LIB, c, p, e, s, l)[0] - look(c, p, "cell_" + e, s, l)) < 1e-12
    for c in ("inv_1", "nand2_1", "a22oi_1") for p in LIB["cells"][c]["arcs"] for e in ("rise", "fall")
    for s in (0.02, 0.08, 0.4) for l in (0.001, 0.005, 0.03)), "")

# Problems 1 and 2 (nand2_1, A to Y)
nd = LIB["cells"]["nand2_1"]["arcs"]["A"]
v.assert_true("Problem 1 and 2 table values match", nd["cell_fall"][2][2] == 0.0504824 and nd["cell_fall"][2][3] == 0.0797753
              and nd["cell_fall"][3][2] == 0.0698132 and nd["cell_fall"][3][3] == 0.1038626
              and nd["cell_rise"][2][3] == 0.0970882 and nd["cell_rise"][2][5] == 0.4287654
              and nd["index_2"][2] == 0.00346659 and nd["index_2"][3] == 0.00912787 and nd["index_2"][5] == 0.0632852, "")
v.check("19-10.1a", (0.100 - nd["index_1"][2]) / (nd["index_1"][3] - nd["index_1"][2]))
v.check("19-10.1b", (0.0060 - nd["index_2"][2]) / (nd["index_2"][3] - nd["index_2"][2]))
v.check("19-10.1c", 1e3 * look("nand2_1", "A", "cell_fall", nd["index_1"][2], 0.0060))
v.check("19-10.1d", 1e3 * look("nand2_1", "A", "cell_fall", nd["index_1"][3], 0.0060))
v.check("19-10.1e", 1e3 * look("nand2_1", "A", "cell_fall", 0.100, 0.0060))
slope, icpt = np.polyfit([nd["index_2"][3], nd["index_2"][5]], [nd["cell_rise"][2][3], nd["cell_rise"][2][5]], 1)
v.check("19-10.2a", slope)
v.check("19-10.2b", 1e3 * icpt)
lin = 1e3 * (icpt + slope * 0.030)
bil = 1e3 * look("nand2_1", "A", "cell_rise", nd["index_1"][2], 0.030)
v.check("19-10.2c", lin)
v.check("19-10.2d", lin - bil)
v.check("19-10.2e", 100 * (lin - bil) / bil)
v.assert_true("bilinear value quoted in Problem 2 is 225.05 ps", abs(bil - 225.05) < 0.005, f"{bil}")


# ---------------------------------------------------------------- small graphs by path enumeration
def enumerate_graph(gates, inputs, outputs):
    """gates: {name: (delay, [fanin])}; inputs: {name: arrival}; outputs: {gate: required}.
    Returns arrival (max over paths), required (min over paths) and the list of paths."""
    fanout = {}
    for g, (_, fin) in gates.items():
        for f in fin:
            fanout.setdefault(f, []).append(g)
    paths = []

    def walk(node, path):
        if node in outputs:
            paths.append(path)
        for nxt in fanout.get(node, []):
            walk(nxt, path + [nxt])
    for i in inputs:
        walk(i, [i])
    arrival, required = {}, {}
    for p in paths:
        t = inputs[p[0]]
        times = [t]
        for g in p[1:]:
            t += gates[g][0]
            times.append(t)
        for node, tt in zip(p, times):
            arrival[node] = max(arrival.get(node, -math.inf), tt)
        # required: walk backward from the endpoint
        r = outputs[p[-1]]
        req = [r]
        for g in reversed(p[1:]):
            r -= gates[g][0]
            req.append(r)
        for node, rr in zip(reversed(p), req):
            required[node] = min(required.get(node, math.inf), rr)
    return arrival, required, paths


ex2 = {"G1": (40, ["a", "b"]), "G2": (25, ["c"]), "G3": (60, ["G1", "G2"]), "G4": (45, ["G1", "c"]),
       "G5": (50, ["G3", "G4"])}
at2, rt2, paths2 = enumerate_graph(ex2, {"a": 0, "b": 20, "c": 10}, {"G5": 180})
v.check("Ex 19-10.2a", at2["G5"])
v.check("Ex 19-10.2b", rt2["G1"])
v.check("Ex 19-10.2c", rt2["c"])
v.check("Ex 19-10.2d", min(rt2[n] - at2[n] for n in at2))
v.check("Ex 19-10.2e", len(paths2))
v.assert_true("Example 2 critical path b-G1-G3-G5", all(rt2[n] - at2[n] == 10 for n in ("b", "G1", "G3", "G5"))
              and all(rt2[n] - at2[n] > 10 for n in ("a", "c", "G2", "G4")), "")

p3 = {"H1": (35, ["p", "q"]), "H2": (50, ["q", "r"]), "H3": (20, ["H1"]), "H4": (45, ["H1", "H2"]),
      "H5": (40, ["H3", "H4"]), "W": (25, ["H2"])}
at3, rt3, paths3 = enumerate_graph(p3, {"p": 0, "q": 10, "r": 30}, {"H5": 150, "W": 120})
v.check("19-10.3a", at3["H5"])
v.check("19-10.3b", rt3["H1"])
v.check("19-10.3c", rt3["q"])
v.check("19-10.3d", min(rt3[n] - at3[n] for n in at3))
v.check("19-10.3e", len(paths3))
fixed = dict(p3, H2=(35, ["q", "r"]))
atf, rtf, _ = enumerate_graph(fixed, {"p": 0, "q": 10, "r": 30}, {"H5": 150, "W": 120})
v.check("19-10.3f", 50 - 35)
v.assert_true("after the fix every slack is non-negative", min(rtf[n] - atf[n] for n in atf) == 0, "")
v.check("19-10.3g", 10 + 35 + 45 + 40)

# Problem 4: edges through unate arcs, by tracking both edges stage by stage
stages = [("neg", 30, 20), ("neg", 40, 35), ("pos", 50, 45)]       # (sense, rise-out, fall-out)
arr = {"rise": 0, "fall": 8}
for sense, dr, df in stages:
    if sense == "neg":
        arr = {"rise": arr["fall"] + dr, "fall": arr["rise"] + df}
    else:
        arr = {"rise": arr["rise"] + dr, "fall": arr["fall"] + df}
v.check("19-10.4a", arr["rise"])
v.check("19-10.4b", arr["fall"])
v.check("19-10.4c", 8 + 30 + 40 + 50)


# ---------------------------------------------------------------- technology mapping by full enumeration
CELLS = ["inv_1", "nand2_1", "and2_1", "nor2_1", "nand3_1", "nand4_1", "a21oi_1", "a22oi_1", "o21ai_1"]
AREA = {c: LIB["cells"][c]["area"] for c in CELLS}
DELAY = {c: round(1e3 * max(look(c, p, "cell_" + e, 0.05, 0.005) for p in LIB["cells"][c]["arcs"]
                            for e in ("rise", "fall")), 1) for c in CELLS}
v.assert_true("mapping delays quoted in Example 3", DELAY["inv_1"] == 63.4 and DELAY["nand2_1"] == 77.1
              and DELAY["nand3_1"] == 92.8 and DELAY["nand4_1"] == 108.4 and DELAY["and2_1"] == 163.0
              and DELAY["o21ai_1"] == 154.8 and DELAY["a21oi_1"] == 168.7 and DELAY["a22oi_1"] == 207.0, str(DELAY))

# Patterns as strings: N(a,b) = NAND, I(a) = INV, leaves $0, $1, ...
PAT = {"inv_1": ["I($0)"], "nand2_1": ["N($0,$1)"], "and2_1": ["I(N($0,$1))"], "nor2_1": ["I(N(I($0),I($1)))"],
       "nand3_1": ["N(I(N($0,$1)),$2)"], "nand4_1": ["N(I(N($0,$1)),I(N($2,$3)))"],
       "a21oi_1": ["I(N(N($0,$1),I($2)))"], "a22oi_1": ["I(N(N($0,$1),N($2,$3)))"],
       "o21ai_1": ["N(N(I($0),I($1)),$2)"]}


def parse(s):
    s = s.replace(" ", "")

    def p(i):
        if s[i] in "NI":
            kind = s[i]
            i += 2
            a, i = p(i)
            if kind == "N":
                i += 1
                b, i = p(i)
                return (kind, a, b), i + 1
            return (kind, a), i + 1
        if s[i] == "$":
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            return ("$", int(s[i + 1:j])), j
        return ("V", s[i]), i + 1
    return p(0)[0]


def unify(pat, t):
    if pat[0] == "$":
        return [{pat[1]: t}]
    if pat[0] != t[0] or pat[0] == "V":
        return []
    if pat[0] == "I":
        return unify(pat[1], t[1])
    res = []
    for a, b in ((t[1], t[2]), (t[2], t[1])):
        for m1 in unify(pat[1], a):
            for m2 in unify(pat[2], b):
                res.append({**m1, **m2})
    return res


def all_covers(t):
    """Every cover as (area, delay, cells, netlist expression)."""
    if t[0] == "V":
        return [(0.0, 0.0, [], t[1])]
    out, seen = [], set()
    for cell, pats in PAT.items():
        for ps in pats:
            for m in unify(parse(ps), t):
                key = (cell, tuple(sorted(repr(m[k]) for k in m)))   # same leaves on swapped pins = same cover
                if key in seen:
                    continue
                seen.add(key)
                for combo in itertools.product(*[all_covers(m[k]) for k in sorted(m)]):
                    out.append((AREA[cell] + sum(c[0] for c in combo),
                                DELAY[cell] + max([c[1] for c in combo], default=0.0),
                                [cell] + [x for c in combo for x in c[2]],
                                (cell, [c[3] for c in combo])))
    return out


def liberty_eval(cell, args):
    """Evaluate a cell's Liberty function string on input values given in pin order."""
    c = LIB["cells"][cell]
    expr = c["function"]
    env = dict(zip(c["inputs"].keys(), args))
    py = re.sub(r"!", " not ", expr).replace("&", " and ").replace("|", " or ")
    return int(eval(py, {}, env))


def eval_netlist(net, env):
    if isinstance(net, str):
        return env[net]
    cell, kids = net
    return liberty_eval(cell, [eval_netlist(k, env) for k in kids])


def eval_tree(t, env):
    if t[0] == "V":
        return env[t[1]]
    if t[0] == "I":
        return 1 - eval_tree(t[1], env)
    return 1 - (eval_tree(t[1], env) & eval_tree(t[2], env))


def check_covers(name, tstr, target):
    t = parse(tstr)
    names = sorted(set(re.findall(r"[A-E]", tstr)))
    covers = all_covers(t)
    ok = True
    for bits in itertools.product((0, 1), repeat=len(names)):
        env = dict(zip(names, bits))
        ok &= eval_tree(t, env) == target(env)
        ok &= all(eval_netlist(c[3], env) == target(env) for c in covers)
    v.assert_true(f"every cover of {name} computes the function", bool(ok), "")
    return covers


cov3 = check_covers("NOT(ABCD + E)", "I(N(N(I(N(A,B)),I(N(C,D))),I(E)))",
                    lambda e: 1 - ((e["A"] & e["B"] & e["C"] & e["D"]) | e["E"]))
amin = min(cov3, key=lambda c: (round(c[0], 6), c[1]))
dmin = min(cov3, key=lambda c: (round(c[1], 6), c[0]))
v.check("Ex 19-10.3a", amin[0])
v.check("Ex 19-10.3b", amin[1])
v.check("Ex 19-10.3c", dmin[1])
v.check("Ex 19-10.3d", dmin[0])
v.check("Ex 19-10.3e", 100 * (dmin[0] / amin[0] - 1))
v.check("Ex 19-10.3f", 100 * (amin[1] / dmin[1] - 1))
v.check("Ex 19-10.3g", len(cov3))
v.assert_true("minimum-area cover is unique and is and2 + nand4 + inv",
              sum(1 for c in cov3 if abs(c[0] - amin[0]) < 1e-9) == 1
              and sorted(amin[2]) == sorted(["and2_1", "nand4_1", "inv_1"]), "")
v.assert_true("minimum-delay cover is inv + nand2 + nand4 + inv", sorted(dmin[2]) == sorted(["inv_1", "nand2_1", "nand4_1", "inv_1"]), "")
a21 = [c for c in cov3 if c[2][0] == "a21oi_1"]
v.check("Ex 19-10.3h", min(c[1] for c in a21))
nodeN = all_covers(parse("N(N(I(N(A,B)),I(N(C,D))),I(E))"))
v.check("Ex 19-10.3i", min(c[1] for c in nodeN))
v.check("Ex 19-10.3j", len(re.findall(r"[NI]\(", "I(N(N(I(N(A,B)),I(N(C,D))),I(E)))")))
lab_tree = techmap.INV(techmap.NAND(techmap.NAND(techmap.INV(techmap.NAND(techmap.IN("A"), techmap.IN("B"))),
                                                 techmap.INV(techmap.NAND(techmap.IN("C"), techmap.IN("D")))),
                                    techmap.INV(techmap.IN("E"))))
la, ld = techmap.min_area(lab_tree, AREA), techmap.min_delay(lab_tree, DELAY)
v.assert_true("lab dynamic program finds both optima", abs(la[0] - amin[0]) < 1e-9 and abs(ld[0] - dmin[1]) < 1e-9, "")

cov5a = check_covers("NOT(AB + CD)", "I(N(N(A,B),N(C,D)))", lambda e: 1 - ((e["A"] & e["B"]) | (e["C"] & e["D"])))
cov5b = check_covers("(A + B)C", "I(N(N(I(A),I(B)),C))", lambda e: (e["A"] | e["B"]) & e["C"])
v.check("19-10.5a", min(c[0] for c in cov5a))
v.check("19-10.5b", min(c[1] for c in cov5a))
by = {tuple(sorted(c[2])): c for c in cov5a}
v.check("19-10.5c", by[tuple(sorted(["inv_1", "nand2_1", "nand2_1", "nand2_1"]))][1])
v.check("19-10.5d", by[tuple(sorted(["and2_1", "nand2_1", "nand2_1"]))][1])
v.check("19-10.5e", min(c[0] for c in cov5b))
v.check("19-10.5f", min(c[1] for c in cov5b))
v.assert_true("both Problem 5 trees have three covers", len(cov5a) == 3 and len(cov5b) == 3, "")
v.check("19-10.5g", len(cov5a))
by5b = {tuple(sorted(c[2])): c for c in cov5b}
v.check("19-10.5h", by5b[tuple(sorted(["inv_1", "nand2_1", "nand2_1", "inv_1", "inv_1"]))][1])
v.check("19-10.5i", by5b[tuple(sorted(["and2_1", "nand2_1", "inv_1", "inv_1"]))][1])


# ---------------------------------------------------------------- clocked checks on a timeline
def setup_check(T, L1, L2, tcq, tpd, tsu, U=0.0, n_cycles=1):
    launch_edge, capture_edge = 0.0, n_cycles * T
    data_at_d = launch_edge + L1 + tcq + tpd
    latest_ok = capture_edge + L2 - tsu - U
    return latest_ok - data_at_d


def hold_check(L1, L2, tcq, tcd, th, U=0.0, hold_edge=0.0):
    data_changes = 0.0 + L1 + tcq + tcd
    must_stay_until = hold_edge + L2 + th + U
    return data_changes - must_stay_until


s4 = setup_check(2.0, 0.30, 0.36, 0.307, 1.20, 0.103, 0.10)
v.check("Ex 19-10.4a", s4)
v.check("Ex 19-10.4b", 1e3 / (2.0 - s4))
v.check("Ex 19-10.4c", hold_check(0.30, 0.36, 0.307, 0.08, -0.047, 0.05))
v.check("Ex 19-10.4d", setup_check(2.0, 0.30, 0.76, 0.307, 1.20, 0.103, 0.10))
v.check("Ex 19-10.4e", hold_check(0.30, 0.76, 0.307, 0.08, -0.047, 0.05))
dfx = LIB["cells"]["dfxtp_1"]
v.assert_true("flip-flop values quoted from the library", abs(dfx["clk_to_q"]["cell_rise"][2][2] - 0.307) < 0.0005
              and abs(dfx["setup"]["fall"][0][0] - 0.103) < 0.0005 and abs(dfx["hold"]["fall"][0][0] + 0.047) < 0.0005
              and abs(dfx["setup"]["rise"][0][0] - 0.051) < 0.0005 and abs(dfx["hold"]["rise"][0][0] + 0.029) < 0.0005, "")
s6 = setup_check(1.5, 0.25, 0.20, 0.307, 0.85, 0.051, 0.08)
v.check("19-10.6a", s6)
v.check("19-10.6b", 1e3 / (1.5 - s6))
v.check("19-10.6c", hold_check(0.25, 0.20, 0.307, 0.10, -0.029, 0.04))
v.check("19-10.6d", setup_check(1.5, 0.25, 0.20, 0.307, 0.85, 0.103, 0.08))
# I/O: input delay is an arrival at the port; output delay sets the required time at the port
v.check("19-10.7a", (2.5 - 0.7 - 0.1) - (0.6 + 1.0))
v.check("19-10.7b", setup_check(2.5, 0.0, 0.3, 0.6, 1.5, 0.1, 0.1))
v.check("19-10.7c", (2.5 - 0.7 - 0.1) - (0.3 + 0.3 + 1.2))
v.check("19-10.8a", setup_check(1.5, 0, 0, 0.30, 2.5, 0.10))
v.check("19-10.8b", setup_check(1.5, 0, 0, 0.30, 2.5, 0.10, n_cycles=2))
v.check("19-10.8c", hold_check(0, 0, 0.30, 0.4, 0.05, hold_edge=1.5))
v.check("19-10.8d", hold_check(0, 0, 0.30, 0.4, 0.05, hold_edge=0.0))


# OCV: the common segment given ONE delay on both sides (CRPR) vs derated separately
def ocv_setup(T, common, lb, cb, tcq, tpd, tsu, kl, ke, crpr):
    if crpr:
        c_launch = c_capture = common * kl          # any single value cancels
    else:
        c_launch, c_capture = common * kl, common * ke
    return (T + c_capture + cb * ke - tsu) - (c_launch + (lb + tcq + tpd) * kl)


def ocv_hold(common, lb, cb, tcq, tcd, th, ke, kl, crpr):
    if crpr:
        c_launch = c_capture = common * ke
    else:
        c_launch, c_capture = common * ke, common * kl
    return (c_launch + (lb + tcq + tcd) * ke) - (c_capture + cb * kl + th)


v.check("Ex 19-10.5a", ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.0, 1.0, False))
v.check("Ex 19-10.5b", ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.08, 0.92, False))
v.check("Ex 19-10.5c", ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.08, 0.92, True)
        - ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.08, 0.92, False))
v.check("Ex 19-10.5d", ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.08, 0.92, True))
v.check("Ex 19-10.5e", ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.0, 1.0, False)
        - ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.08, 0.92, False))
v.assert_true("lab OCV formula agrees", all(abs(sta.ocv_setup_slack(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.08, 0.92, c)
                                                - ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1.08, 0.92, c)) < 1e-12
                                            for c in (True, False)), "")
v.check("19-10.9a", ocv_hold(0.50, 0.10, 0.30, 0.25, 0.05, 0.02, 1.0, 1.0, False))
v.check("19-10.9b", ocv_hold(0.50, 0.10, 0.30, 0.25, 0.05, 0.02, 0.92, 1.08, False))
v.check("19-10.9c", ocv_hold(0.50, 0.10, 0.30, 0.25, 0.05, 0.02, 0.92, 1.08, True)
        - ocv_hold(0.50, 0.10, 0.30, 0.25, 0.05, 0.02, 0.92, 1.08, False))
v.check("19-10.9d", ocv_hold(0.50, 0.10, 0.30, 0.25, 0.05, 0.02, 0.92, 1.08, True))


# ---------------------------------------------------------------- statistics with a covariance matrix
def sigma_path(n, s, rho):
    cov = np.full((n, n), rho * s * s)
    np.fill_diagonal(cov, s * s)
    one = np.ones(n)
    return math.sqrt(one @ cov @ one)


v.check("Ex 19-10.6a", 16 * (50 + 3 * 2.5))
v.check("Ex 19-10.6b", 800 + 3 * sigma_path(16, 2.5, 0.0))
v.check("Ex 19-10.6c", sigma_path(16, 2.5, 0.3))
v.check("Ex 19-10.6d", 800 + 3 * sigma_path(16, 2.5, 0.3))
v.check("Ex 19-10.6e", 16 * 57.5 - (800 + 3 * sigma_path(16, 2.5, 0.3)))
v.check("Ex 19-10.6f", 16 * 57.5 - (800 + 3 * sigma_path(16, 2.5, 0.0)))
v.assert_true("rho = 1 recovers the flat derate", abs(800 + 3 * sigma_path(16, 2.5, 1.0) - 920) < 1e-9, "")
v.assert_true("lab path sigma agrees", abs(sta.path_sigma([2.5] * 16, 0.3) - sigma_path(16, 2.5, 0.3)) < 1e-12, "")
eff = lambda n, rho: 100 * 3 * sigma_path(n, 0.04, rho) / n     # 3 sigma over the mean, mean per stage = 1
v.check("19-10.10a", 300 * 0.04)
v.check("19-10.10b", eff(4, 0.0))
v.check("19-10.10c", eff(16, 0.0))
v.check("19-10.10d", eff(64, 0.0))
v.check("19-10.10e", next(n for n in range(1, 100) if eff(n, 0.0) <= 4 + 1e-9))
v.check("19-10.10f", eff(16, 0.2))
v.check("19-10.10g", eff(64, 0.2))
v.check("19-10.10h", 100 * 3 * 0.04 * math.sqrt(0.2))          # the limit of eff(n, 0.2), checked below
v.assert_true("correlated derate approaches its limit", abs(eff(2000, 0.2) - 100 * 3 * 0.04 * math.sqrt(0.2)) < 0.01, "")

# Problem 11: graph-based vs path-based with a linear slew model
inputs = {"A": (100, 20), "B": (60, 120)}
g_out = {k: (t + 30 + 0.3 * s, 25 + 0.2 * s) for k, (t, s) in inputs.items()}
gba = max(t for t, _ in g_out.values()) + 40 + 0.3 * max(s for _, s in g_out.values())
pba = {k: t + 40 + 0.3 * s for k, (t, s) in g_out.items()}
v.check("19-10.11a", gba)
v.check("19-10.11b", pba["A"])
v.check("19-10.11c", pba["B"])
v.check("19-10.11d", gba - max(pba.values()))

# Problem 12: corner scaling of clock and data
tt = hold_check(0.20, 0.60, 0.25, 0.20, 0.02)
ss = hold_check(0.20 * 1.5, 0.60 * 1.5, 0.25 * 1.3, 0.20 * 1.3, 0.02 * 1.3)
v.check("19-10.12a", tt)
v.check("19-10.12b", ss)
v.check("19-10.12c", -ss)
v.check("19-10.12d", -ss / 1.3)
v.check("19-10.12e", tt - ss / 1.3)
v.assert_true("the fixed path passes at the slow corner", abs(hold_check(0.30, 0.90, 0.325, 0.26 - ss, 0.026)) < 1e-12, "")


# ---------------------------------------------------------------- lab: real-table timing, re-implemented here
def edges_in(sense, oe):
    return {"negative_unate": ["fall" if oe == "rise" else "rise"], "positive_unate": [oe]}.get(sense, ["rise", "fall"])


def my_gba(insts, start_slew, out_load):
    """insts: ordered list of (cell, {pin: net}, out). Returns {(net, edge): (arrival, slew)}."""
    loads = {}
    for cell, pins, _ in insts:
        for p, n in pins.items():
            loads[n] = loads.get(n, 0.0) + LIB["cells"][cell]["inputs"][p]
    st = {("x0", "rise"): (0.0, start_slew), ("x0", "fall"): (0.0, start_slew)}
    for cell, pins, out in insts:
        c = loads.get(out, 0.0) + (out_load if out not in loads else 0.0)
        for oe in ("rise", "fall"):
            cand = []
            for p, n in pins.items():
                for ie in edges_in(LIB["cells"][cell]["arcs"][p]["sense"], oe):
                    t, s = st[(n, ie)]
                    cand.append((t + look(cell, p, "cell_" + oe, s, c), look(cell, p, oe + "_transition", s, c)))
            st[(out, oe)] = (max(x[0] for x in cand), max(x[1] for x in cand))
    return st, loads


def my_pba(insts, start_slew, out_load, end):
    st, loads = my_gba(insts, start_slew, out_load)
    drivers = {}
    for cell, pins, out in insts:
        for p, n in pins.items():
            drivers.setdefault(n, []).append((cell, p, out))
    best = {}

    def walk(net, edge, t, s):
        if net == end:
            best[edge] = max(best.get(edge, -1.0), t)
            return
        for cell, p, out in drivers.get(net, []):
            c = loads.get(out, 0.0) + (out_load if out not in loads else 0.0)
            for oe in ("rise", "fall"):
                if edge in edges_in(LIB["cells"][cell]["arcs"][p]["sense"], oe):
                    walk(out, oe, t + look(cell, p, "cell_" + oe, s, c), look(cell, p, oe + "_transition", s, c))
    walk("x0", "rise", 0.0, start_slew)
    walk("x0", "fall", 0.0, start_slew)
    return best


def chain_insts(n):
    return [("inv_1", {"A": "x0" if k == 1 else f"n{k - 1}"}, f"n{k}") for k in range(1, n + 1)]


for slew, key_r, key_f in ((0.01, "Lab 19-10.b", "Lab 19-10.c"), (0.5, "Lab 19-10.d", "Lab 19-10.e")):
    st, _ = my_gba(chain_insts(4), slew, 0.01)
    v.check(key_r, 1e3 * st[("n4", "rise")][0])
    v.check(key_f, 1e3 * st[("n4", "fall")][0])


def diamond_insts(n):
    out = []
    for k in range(n):
        out += [("inv_1", {"A": f"x{k}"}, f"a{k}"), ("buf_1", {"A": f"x{k}"}, f"b{k}"),
                ("nand2_1", {"A": f"a{k}", "B": f"b{k}"}, f"x{k + 1}")]
    return out


st10, _ = my_gba(diamond_insts(10), 0.05, 0.005)
pb10 = my_pba(diamond_insts(10), 0.05, 0.005, "x10")
v.check("Lab 19-10.f", 1e3 * st10[("x10", "rise")][0])
v.check("Lab 19-10.g", 1e3 * pb10["rise"])
v.check("Lab 19-10.h", 2 ** 10)
v.assert_true("graph-based bounds path-based for every edge", all(st10[("x10", e)][0] >= pb10[e] - 1e-12 for e in pb10), "")
nl = sta.Netlist(LIB, {"x0": (0.0, 0.0, 0.05)}, {"y": ("x10", 0.005)})
for k, (cell, pins, out) in enumerate(diamond_insts(10)):
    nl.add(f"u{k}", cell, pins, out)
at_lab, _ = nl.analyze()
pb_lab = nl.path_based("x0", "x10")
v.assert_true("lab engine agrees with the re-implementation", abs(at_lab[("x10", "rise")] - st10[("x10", "rise")][0]) < 1e-12
              and abs(pb_lab["rise"] - pb10["rise"]) < 1e-12 and nl.count_paths("x0", "x10") == 1024, "")
# extrapolation beyond the last load point, along the last segment of the 0.0531329 ns row
extrap = (inv["cell_rise"][2][6] + (0.25 - inv["index_2"][6]) * (inv["cell_rise"][2][6] - inv["cell_rise"][2][5])
          / (inv["index_2"][6] - inv["index_2"][5]))
v.check("Lab 19-10.a", extrap)
v.assert_true("lab extrapolation agrees", abs(sta.arc_delay(LIB, "inv_1", "A", "rise", 0.0531329, 0.25)[0] - extrap) < 1e-12, "")
# derate at which Example 5's slack reaches zero, symmetric derates 1 +/- d, by bisection
def zero_derate(crpr):
    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        if ocv_setup(2.0, 0.40, 0.20, 0.22, 0.30, 1.10, 0.10, 1 + mid, 1 - mid, crpr) > 0:
            lo = mid
        else:
            hi = mid
    return 100 * lo


v.check("Lab 19-10.i", zero_derate(False))
v.check("Lab 19-10.j", zero_derate(True))

sys.exit(v.finish())
