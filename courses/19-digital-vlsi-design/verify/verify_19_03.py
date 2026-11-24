#!/usr/bin/env python3
"""Verify every number in chapter 19-03 (combinational logic families), its problems and its lab.

Independent routes:
- gate sizing by enumerating every input combination of the switch networks and computing the worst conducting
  resistance, rather than by the rules of thumb;
- Elmore constants as the first moment of the network's transfer function, m1 = [G^-1 C G^-1 b]_k, from the nodal
  matrices (not by the shared-resistance rule), and exact ladder delays by integrating the nodal ODEs;
- pseudo-NMOS levels, pass-transistor levels and the following inverter by root-finding on transistor currents written
  here;
- charge sharing by integrating the two-capacitor transistor ODE to its final state, with and without body effect;
- buffered TG chains by brute force over segment lengths;
- the lab's module is checked against these results; ngspice confirms Examples 3 to 6 (run_spice).
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "19-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import logic as lg  # noqa: E402

v = Verifier.from_files("19-03", ROOT / "chapters" / "19-03-logic-families.md",
                        ROOT / "solutions" / "19-03-solutions.md", LAB / "README.md")
LN2 = math.log(2)
P, F = 1e-12, 1e-15


# ---------------------------------------------------------------- switch networks: worst-case resistance
# A network is ("s", [subnets]) for series, ("p", [subnets]) for parallel, or ("t", input, width).
def conduct(net, inputs, nmos):
    """Resistance of a conducting network (None if open); a transistor of width w has resistance mu_eff/w where
    mu_eff = 1 for NMOS and 2 for PMOS (unit inverter: NMOS width 1, PMOS width 2, equal resistance)."""
    kind = net[0]
    if kind == "t":
        on = inputs[net[1]] if nmos else not inputs[net[1]]
        return (1.0 if nmos else 2.0) / net[2] if on else None
    rs = [conduct(n, inputs, nmos) for n in net[1]]
    if kind == "s":
        return None if any(r is None for r in rs) else sum(rs)
    on = [r for r in rs if r is not None]
    return None if not on else 1.0 / sum(1.0 / r for r in on)


def worst(net, names, nmos):
    vals = []
    for bits in itertools.product([False, True], repeat=len(names)):
        r = conduct(net, dict(zip(names, bits)), nmos)
        if r is not None:
            vals.append(r)
    return max(vals)


def t(name, w):
    return ("t", name, w)


gates = {
    "NAND2": (("s", [t("a", 2), t("b", 2)]), ("p", [t("a", 2), t("b", 2)]), "ab"),
    "NAND3": (("s", [t("a", 3), t("b", 3), t("c", 3)]), ("p", [t("a", 2), t("b", 2), t("c", 2)]), "abc"),
    "NOR2": (("p", [t("a", 1), t("b", 1)]), ("s", [t("a", 4), t("b", 4)]), "ab"),
    "NOR3": (("p", [t("a", 1), t("b", 1), t("c", 1)]), ("s", [t("a", 6), t("b", 6), t("c", 6)]), "abc"),
    "OAI": (("s", [t("a", 2), ("p", [t("b", 2), t("c", 2)])]), ("p", [t("a", 2), ("s", [t("b", 4), t("c", 4)])]),
            "abc"),
}
for name, (pdn, pun, ins) in gates.items():
    v.assert_true(f"{name} worst pull-down equals the unit inverter", abs(worst(pdn, ins, True) - 1) < 1e-12, "")
    v.assert_true(f"{name} worst pull-up equals the unit inverter", abs(worst(pun, ins, False) - 1) < 1e-12, "")


def input_cap(pdn, pun, name):
    def widths(net):
        if net[0] == "t":
            return net[2] if net[1] == name else 0.0
        return sum(widths(n) for n in net[1])
    return widths(pdn) + widths(pun)


for key, gname in (("1a", "NAND2"), ("1c", "NAND3"), ("1e", "NOR2"), ("1g", "NOR3")):
    pdn, pun, _ = gates[gname]
    cap = input_cap(pdn, pun, "a")
    v.check(f"Ex 19-03.{key}", cap)
    v.check(f"Ex 19-03.{key[0]}{chr(ord(key[1]) + 1)}", cap / 3)
    v.assert_true(f"lab sizing {gname}", abs(lg.input_cap_ratio(*(lg.nand_sizes(int(gname[-1])) if gname.startswith("NAND")
                                                               else lg.nor_sizes(int(gname[-1]))))
                                            - cap / 3) < 1e-12, "")

# Problem 1: the OAI gate
pdn, pun, _ = gates["OAI"]
v.check("19-03.1a", 6)
v.check("19-03.1b", 2)
v.check("19-03.1c", 4)
v.check("19-03.1d", 2)
v.check("19-03.1e", input_cap(pdn, pun, "a") / 3)
v.check("19-03.1f", input_cap(pdn, pun, "b") / 3)
v.assert_true("OAI inputs b and c symmetric", input_cap(pdn, pun, "b") == input_cap(pdn, pun, "c"), "")


# ---------------------------------------------------------------- Elmore as a first moment from nodal matrices
def tree_matrices(edges, caps):
    """edges: list of (from_node, to_node, R) with node 0 the source; caps: {node: C}. Returns G, C, b."""
    nodes = sorted(caps)
    idx = {n: i for i, n in enumerate(nodes)}
    g = np.zeros((len(nodes), len(nodes)))
    b = np.zeros(len(nodes))
    for a, c_, r in edges:
        gg = 1 / r
        for x in (a, c_):
            if x != 0:
                g[idx[x], idx[x]] += gg
        if a != 0 and c_ != 0:
            g[idx[a], idx[c_]] -= gg
            g[idx[c_], idx[a]] -= gg
        else:
            b[idx[a or c_]] += gg
    cm = np.diag([caps[n] for n in nodes])
    return g, cm, b, idx


def elmore_moment(edges, caps, node):
    g, cm, b, idx = tree_matrices(edges, caps)
    h0 = np.linalg.solve(g, b)
    m1 = np.linalg.solve(g, cm @ h0)
    return float(m1[idx[node]] / h0[idx[node]])


def exact_50(edges, caps, node):
    """50% crossing of node's step response, by integrating C dv/dt = -G v + b (source steps 0 -> 1)."""
    g, cm, b, idx = tree_matrices(edges, caps)
    a = -np.linalg.solve(cm, g)
    bb = np.linalg.solve(cm, b)
    tau = elmore_moment(edges, caps, node)
    ev = lambda _t, y: y[idx[node]] - 0.5  # noqa: E731
    ev.terminal = True
    sol = solve_ivp(lambda _t, y: a @ y + bb, (0, 20 * tau), np.zeros(len(caps)), events=ev, method="Radau",
                    rtol=1e-11, atol=1e-14, jac=a)
    return float(sol.t_events[0][0])


def ladder(rs, cs):
    edges = [(i, i + 1, r) for i, r in enumerate(rs)]
    caps = {i + 1: c for i, c in enumerate(cs)}
    return edges, caps


# Example 2: NAND-N pull-down (discharge through the stack is the same linear problem as charging)
R, c, cext = 10e3, 0.5e-15, 10e-15
for n, (ka, kb) in zip((1, 2, 3, 4), (("2a", "2b"), ("2c", "2d"), ("2e", "2f"), ("2g", "2h"))):
    e, cp = ladder([R / n] * n, [c * n] * (n - 1) + [c * n + 2 * c * n + cext])
    tau = elmore_moment(e, cp, n)
    v.check(f"Ex 19-03.{ka}", tau / P)
    v.check(f"Ex 19-03.{kb}", LN2 * tau / P)
    v.assert_true(f"lab nand_stack_elmore N={n}", abs(lg.nand_stack_elmore(n, R, c, cext) - tau) < 1e-20, "")
e1, c1 = ladder([R], [3 * c + cext])
e4, c4 = ladder([R / 4] * 4, [c * 4] * 3 + [12 * c + cext])
v.check("Ex 19-03.2i", elmore_moment(e4, c4, 4) / elmore_moment(e1, c1, 1))
nx = brentq(lambda x: R * c * x * (x - 1) / 2 - R * (3 * c * x + cext), 2, 30)
v.check("Lab 19-03.a", nx)
v.check("Lab 19-03.b", R * (3 * c * nx + cext) / P)

# Example 5 and Problem 10: ladders, Elmore against exact
e12, c12 = ladder([5e3] * 12, [2e-15] * 12)
tau12 = elmore_moment(e12, c12, 12)
ex12 = exact_50(e12, c12, 12)
v.check("Ex 19-03.5a", LN2 * tau12 / P)
v.check("Ex 19-03.5b", ex12 / P)
v.check("Ex 19-03.5c", 100 * (1 - LN2 * tau12 / ex12))
v.assert_true("lab ladder_step_50 matches", abs(lg.ladder_step_50([5e3] * 12, [2e-15] * 12) - ex12) < 1e-4 * ex12, "")
for n, kr, kd, ke in ((1, "10a", "10h", None), (2, "Lab 19-03.c", None, None), (4, "10b", "10d", "10f"),
                      (12, "10c", "10e", "10g")):
    en, cn = ladder([1.0 / n] * n, [1.0 / n] * n)
    tn = elmore_moment(en, cn, n)
    xn = exact_50(en, cn, n)
    v.check(kr if kr.startswith("Lab") else f"19-03.{kr}", xn / (LN2 * tn))
    if kd:
        v.check(f"19-03.{kd}", xn)
    if ke:
        v.check(f"19-03.{ke}", LN2 * tn)
    v.assert_true(f"Elmore closed form, n = {n}", abs(tn - (n + 1) / (2 * n)) < 1e-12, "")

# Problem 3: the branching tree
edges = [(0, 1, 1e3), (1, 2, 2e3), (1, 3, 3e3)]
caps = {1: 10e-15, 2: 20e-15, 3: 30e-15}
v.check("19-03.3a", elmore_moment(edges, caps, 2) / P)
v.check("19-03.3b", LN2 * elmore_moment(edges, caps, 2) / P)
v.check("19-03.3c", elmore_moment(edges, caps, 3) / P)
v.check("19-03.3d", LN2 * elmore_moment(edges, caps, 3) / P)

# Problem 4: input ordering (internal nodes charged, or already discharged and so absent from the moment)
e4a, c4a = ladder([R / 3] * 3, [1.5e-15, 1.5e-15, 20e-15])
ta = elmore_moment(e4a, c4a, 3)
e4b, c4b = ladder([R / 3] * 3, [1e-30, 1e-30, 20e-15])
tb = elmore_moment(e4b, c4b, 3)
v.check("19-03.4a", ta / P)
v.check("19-03.4b", LN2 * ta / P)
v.check("19-03.4c", tb / P)
v.check("19-03.4d", LN2 * tb / P)
v.check("19-03.4e", 100 * (1 - tb / ta))


# ---------------------------------------------------------------- transistor currents
def idn(k, vt, vgs, vds):
    vov = vgs - vt
    if vov <= 0 or vds <= 0:
        return 0.0
    return k * (vov * vds - vds * vds / 2) if vds < vov else k * vov * vov / 2


def vol_pseudo(kn, kp, vdd, vt):
    return brentq(lambda x: idn(kn, vt, vdd, x) - idn(kp, vt, vdd, vdd - x), 1e-9, vdd - 1e-9, xtol=1e-15)


vol = vol_pseudo(200e-6, 50e-6, 1.2, 0.35)
iload = idn(50e-6, 0.35, 1.2, 1.2 - vol)
v.check("Ex 19-03.3a", vol)
v.check("Ex 19-03.3b", iload * 1e6)
v.check("Ex 19-03.3c", 1.2 * iload * 1e6)
v.check("Ex 19-03.3d", brentq(lambda r: vol_pseudo(200e-6, 200e-6 / r, 1.2, 0.35) - 0.1, 1.5, 20, xtol=1e-13))
v.check("Ex 19-03.3e", 5e4 * 1.2 * iload)
v.check("Ex 19-03.3f", iload / (200e-6 * 0.85))
v.assert_true("PMOS load saturated", 1.2 - vol > 0.85, f"V_SD = {1.2 - vol:.3f} V")
v.assert_true("lab pseudo_nmos_vol matches", abs(lg.pseudo_nmos_vol(200e-6, 50e-6, 1.2, 0.35, 0.35) - vol) < 1e-12, "")

kp5 = brentq(lambda kp: vol_pseudo(150e-6, kp, 1.0, 0.3) - 0.15, 1e-6, 1e-4, xtol=1e-16)
v.check("19-03.5a", kp5 * 1e6)
v.check("19-03.5b", idn(kp5, 0.3, 1.0, 1.0) * 1.0 * 1e6)
v.check("19-03.5c", vol_pseudo(300e-6, kp5, 1.0, 0.3))


def vt_b(vt0, gb, phi2, vsb):
    return vt0 + gb * (math.sqrt(phi2 + vsb) - math.sqrt(phi2))


def pass_level(vdd, vt0, gb, phi2):
    """Integrate the pass transistor charging a capacitor for a long time; return the final level."""
    k, cap = 200e-6, 10e-15
    rhs = lambda _t, y: [idn(k, vt_b(vt0, gb, phi2, y[0]), vdd - y[0], vdd - y[0]) / cap]  # noqa: E731
    sol = solve_ivp(rhs, (0, 1e-2), [0.0], method="LSODA", rtol=1e-12, atol=1e-15)
    return float(sol.y[0][-1])


vh = pass_level(1.2, 0.35, 0.4, 0.8)
v.check("Ex 19-03.4a", vh)
v.check("Ex 19-03.4b", vt_b(0.35, 0.4, 0.8, vh))
v.check("Lab 19-03.d", pass_level(1.2, 0.35, 0.6, 0.8))
v.assert_true("lab nmos_pass_high matches", abs(lg.nmos_pass_high(1.2, 0.35, 0.4, 0.8) - vh) < 1e-6, "")
vo = brentq(lambda x: idn(200e-6, 0.35, 1.2 - vh, 1.2 - x) - idn(200e-6, 0.35, vh, x), 1e-9, 1.2, xtol=1e-16)
iinv = idn(200e-6, 0.35, vh, vo)
v.check("Ex 19-03.4c", vo * 1e3)
v.check("Ex 19-03.4d", iinv * 1e6)
v.check("Ex 19-03.4e", 1.2 * iinv * 1e6)
vh6 = pass_level(1.0, 0.3, 0.5, 0.7)
v.check("19-03.6a", vh6)
v.check("19-03.6b", 1.0 - vh6)
v.assert_true("next PMOS stays on", 1.0 - vh6 > 0.3, "")


# ---------------------------------------------------------------- TG chains: brute force over segment lengths
def buffered(n, m, r, cc, tbuf):
    segs = n // m
    e, cp = ladder([r] * m, [cc] * m)
    return segs * LN2 * elmore_moment(e, cp, m) + (segs - 1) * tbuf


v.check("Ex 19-03.5d", minimize_scalar(lambda m: LN2 * 10e-12 * 12 * (m + 1) / 2 + (12 / m - 1) * 30e-12,
                                       bounds=(1, 12), method="bounded", options={"xatol": 1e-10}).x)
v.check("Ex 19-03.5e", buffered(12, 3, 5e3, 2e-15, 30e-12) / P)
v.check("Ex 19-03.5f", buffered(12, 2, 5e3, 2e-15, 30e-12) / P)
v.check("Ex 19-03.5g", buffered(12, 4, 5e3, 2e-15, 30e-12) / P)
v.check("Ex 19-03.5h", LN2 * tau12 / buffered(12, 3, 5e3, 2e-15, 30e-12))
best = min((buffered(12, m, 5e3, 2e-15, 30e-12), m) for m in (1, 2, 3, 4, 6, 12))
v.assert_true("m = 3 is the best divisor of 12", best[1] == 3, str(best))
for tb, key in ((10e-12, "Lab 19-03.e"), (100e-12, "Lab 19-03.f")):
    v.check(key, minimize_scalar(lambda m: LN2 * 10e-12 * 12 * (m + 1) / 2 + (12 / m - 1) * tb, bounds=(1, 12),
                                 method="bounded", options={"xatol": 1e-10}).x)
e16, c16 = ladder([4e3] * 16, [3e-15] * 16)
t16 = LN2 * elmore_moment(e16, c16, 16)
v.check("19-03.7a", t16 / P)
v.check("19-03.7b", minimize_scalar(lambda m: LN2 * 12e-12 * 16 * (m + 1) / 2 + (16 / m - 1) * 25e-12,
                                    bounds=(1, 16), method="bounded", options={"xatol": 1e-10}).x)
v.check("19-03.7c", buffered(16, 2, 4e3, 3e-15, 25e-12) / P)
v.check("19-03.7d", buffered(16, 4, 4e3, 3e-15, 25e-12) / P)
v.check("19-03.7e", buffered(16, 8, 4e3, 3e-15, 25e-12) / P)
v.check("19-03.7f", t16 / buffered(16, 2, 4e3, 3e-15, 25e-12))
v.assert_true("lab tg_chain_buffered matches",
              abs(lg.tg_chain_buffered(16, 2, 4e3, 3e-15, 25e-12) - buffered(16, 2, 4e3, 3e-15, 25e-12)) < 1e-18, "")


# ---------------------------------------------------------------- charge sharing by simulation
def share(cl, cas, vdd=1.2, vt0=0.35, gb=0.0, phi2=0.8, k=200e-6):
    """Output precharged to vdd; a chain of internal nodes (capacitances cas, top first) at 0 V, joined to the
    output and to each other by NMOS with gates at vdd. Integrate to the final state."""
    caps = [cl] + list(cas)

    def rhs(_t, y):
        dq = np.zeros(len(y))
        for i in range(len(cas)):
            hi, lo = (i, i + 1) if y[i] >= y[i + 1] else (i + 1, i)
            cur = idn(k, vt_b(vt0, gb, phi2, y[lo]), vdd - y[lo], y[hi] - y[lo])
            dq[hi] -= cur
            dq[lo] += cur
        return dq / np.array(caps)
    sol = solve_ivp(rhs, (0, 1e-2), [vdd] + [0.0] * len(cas), method="LSODA", rtol=1e-12, atol=1e-15)
    return sol.y[:, -1]


f3 = share(10e-15, [3e-15])
f12 = share(10e-15, [12e-15])
v.check("Ex 19-03.6a", 1.2 * 10 / 13)
v.check("Ex 19-03.6b", f3[0])
v.check("Ex 19-03.6c", f12[0])
bnd = brentq(lambda r: 1.2 / (1 + r) - 0.85, 0.1, 1.0, xtol=1e-14)
v.check("Ex 19-03.6d", bnd)
lo_, hi_ = share(10e-15, [0.95 * bnd * 10e-15]), share(10e-15, [1.05 * bnd * 10e-15])
v.assert_true("simulation: cut-off below the boundary, equalized above",
              abs(lo_[1] - 0.85) < 1e-4 < lo_[0] - lo_[1] and abs(hi_[0] - hi_[1]) < 1e-4, f"{lo_} {hi_}")
v.check("Ex 19-03.6f", (10e-15 * (1.2 - f3[0])) / F)
v.check("Ex 19-03.6g", 1.2 - f3[0])
v.assert_true("charge conserved, 3 fF", abs(10e-15 * (1.2 - f3[0]) - 3e-15 * f3[1]) < 1e-21, "")
v.assert_true("lab charge_sharing matches", abs(lg.charge_sharing(1.2, 0.35, 10e-15, 3e-15) - f3[0]) < 1e-6, "")
v.check("Ex 19-03.6e", 10e-15 * 0.1 / 1e-9 * 1e6)
v.check("Lab 19-03.g", share(10e-15, [0.35 / 0.85 * 10e-15])[0])
v.check("Lab 19-03.h", brentq(lambda ca: 1.2 * 10 / (10 + ca) - 0.6, 5, 19, xtol=1e-12))
v.check("Lab 19-03.i", (share(10e-15, [1e-15])[0] - share(10e-15, [3e-15])[0]) / 2)

s8 = share(12e-15, [2e-15, 2e-15])
v.check("19-03.8a", 1.2 * 12 / 16)
v.check("19-03.8b", s8[0])
s8b = share(6e-15, [2e-15, 2e-15])
v.check("19-03.8c", s8b[0])
v.check("19-03.8d", 1.2 - s8[0])
v.check("19-03.8e", 1.2 - s8b[0])
v.check("19-03.9a", 5e-15 * 0.15 / 20e-9 * 1e9)
v.check("19-03.9b", 1 / (2 * 5e-15 * 0.15 / 20e-9) / 1e6)

s11 = share(10e-15, [3e-15], gb=0.4)
v.check("19-03.11a", s11[1])
v.check("19-03.11b", brentq(lambda r: 1.2 / (1 + r) - s11[1], 0.1, 2.0, xtol=1e-14))
v.check("19-03.11c", s11[0])

# ---------------------------------------------------------------- counts
v.check("19-03.2a", 2 * 4)
v.check("19-03.2b", 4 + 1)
v.check("19-03.2c", 4 + 2)
v.check("19-03.2d", 4 + 2 + 2)
v.check("19-03.12a", 3 + 2 + 2)
v.check("19-03.12b", 6 + 2)

# practitioner lens: SKY130 inv_1 widths [R-315]
v.check("Txt 19-03.a", 1.0 / 0.65)

sys.exit(v.finish())
