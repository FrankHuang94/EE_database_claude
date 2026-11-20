#!/usr/bin/env python3
"""Verify every number in chapter 12-05 (feedback: theory and the four topologies), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- every circuit is solved by modified nodal analysis with its controlled source in place;
- return ratios, direct transmissions and asymptotic gains come from superposition in the solved circuit:
  the controlled source is replaced by an independent source s_c, and with input u the output and
  controlling variable are y = a u + b s_c, x = c u + d s_c, so T = -P d, A0 = a, A_inf = a - b c / d;
- the asymptotic-gain formula and Blackman's formula are asserted against direct solutions, not assumed;
- port impedances by test-current injection; bandwidths by root finding on the solved response;
- harmonic distortion by solving the nonlinear loop sample by sample and taking an FFT.
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
files = [COURSE / "chapters" / "12-05-feedback-topologies.md", COURSE / "solutions" / "12-05-solutions.md"]
lab = COURSE / "labs" / "12-05-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("12-05", *files)
TP = 2 * math.pi
par = lambda a, b: a * b / (a + b)  # noqa: E731


# ============================================================ modified nodal analysis (DC, real)
def solve(elems):
    """Solve a linear circuit. Elements:
    ('R', a, b, ohm); ('I', a, b, amps): current leaves a, enters b;
    ('G', d, s, cp, cn, gm): current gm*(v(cp) - v(cn)) leaves d, enters s;
    ('V', p, n, volts): v(p) - v(n) = volts; ('E', p, n, cp, cn, k): v(p) - v(n) = k*(v(cp) - v(cn)).
    Returns (node voltages, branch currents of V/E elements, current leaving p through the source)."""
    nodes = []
    for e in elems:
        for nd in (e[1:3] if e[0] in "RIV" else e[1:5]):
            if nd != "0" and nd not in nodes:
                nodes.append(nd)
    br = [i for i, e in enumerate(elems) if e[0] in "VE"]
    n, m = len(nodes), len(br)
    idx = {nd: i for i, nd in enumerate(nodes)}
    M = np.zeros((n + m, n + m))
    rhs = np.zeros(n + m)

    def stamp(i, j, val):
        if i in idx and j in idx:
            M[idx[i], idx[j]] += val

    for e in elems:
        k = e[0]
        if k == "R":
            a, b, g = e[1], e[2], 1 / e[3]
            stamp(a, a, g); stamp(b, b, g); stamp(a, b, -g); stamp(b, a, -g)
        elif k == "G":
            d, s, cp, cn, gm = e[1:]
            stamp(d, cp, gm); stamp(d, cn, -gm); stamp(s, cp, -gm); stamp(s, cn, gm)
        elif k == "I":
            a, b, amps = e[1:]
            if a in idx:
                rhs[idx[a]] -= amps
            if b in idx:
                rhs[idx[b]] += amps
    for r, i in enumerate(br):
        e = elems[i]
        p, q = e[1], e[2]
        row = n + r
        if p in idx:
            M[idx[p], row] += 1; M[row, idx[p]] += 1
        if q in idx:
            M[idx[q], row] -= 1; M[row, idx[q]] -= 1
        if e[0] == "V":
            rhs[row] = e[3]
        else:
            cp, cn, kk = e[3], e[4], e[5]
            if cp in idx:
                M[row, idx[cp]] -= kk
            if cn in idx:
                M[row, idx[cn]] += kk
    x = np.linalg.solve(M, rhs)
    vol = {nd: x[idx[nd]] for nd in nodes}
    vol["0"] = 0.0
    cur = {i: x[n + r] for r, i in enumerate(br)}
    return vol, cur


def vd(sol, a, b="0"):
    return sol[0][a] - sol[0][b]


def loop(build, out, extra=()):
    """Superposition analysis of a circuit with one controlled source.
    build(u, sc) returns (elements, ctrl) where ctrl = (P, cp, cn): with sc None the controlled source is in
    place; otherwise it is replaced by an independent source of value sc. out(sol) gives the output."""
    def run(u, sc):
        el, ctrl = build(u, sc)
        s = solve(list(el) + list(extra))
        return out(s), s[0][ctrl[1]] - s[0][ctrl[2]], ctrl[0]
    a, c, P = run(1.0, 0.0)
    b, d, _ = run(0.0, 1.0)
    T = -P * d
    A0, Ainf = a, a - b * c / d
    Af = run(1.0, None)[0]
    v.assert_true(f"asymptotic-gain formula matches the direct solution ({Af:.6g})",
                  abs((Ainf * T + A0) / (1 + T) - Af) <= 1e-9 * max(1.0, abs(Af)))
    return dict(T=T, A0=A0, Ainf=Ainf, Af=Af)


def port_z(build, a, b="0", extra=()):
    """Impedance at the port (a, b) with the input zeroed, by test current; and Blackman's three ingredients."""
    test = [("I", b, a, 1.0)]
    el, _ = build(0.0, None)
    Z = vd(solve(list(el) + list(extra) + test), a, b)
    el0, ctrl = build(0.0, 0.0)
    Z0 = vd(solve(list(el0) + list(extra) + test), a, b)

    def T_with(port_extra):
        el1, ctrl1 = build(0.0, 1.0)
        s = solve(list(el1) + list(extra) + list(port_extra))
        return -ctrl1[0] * (s[0][ctrl1[1]] - s[0][ctrl1[2]])
    Tsc, Toc = T_with([("V", a, b, 0.0)]), T_with([])
    v.assert_true(f"Blackman's formula matches the test-source impedance ({Z:.6g})",
                  abs(Z0 * (1 + Tsc) / (1 + Toc) / Z - 1) < 1e-9)
    return dict(Z=Z, Z0=Z0, Tsc=Tsc, Toc=Toc)


def block_gain(A, beta):
    """Ideal feedback structure solved as two linear equations: y = A e, e = x - beta y (x = 1)."""
    e, y = np.linalg.solve(np.array([[A, -1.0], [1.0, beta]]), np.array([0.0, 1.0]))
    return y, e


# ============================================================ Example 1
A, beta = 1e5, 0.01
Af1, e1 = block_gain(A, beta)
v.check("Ex 12-05.1a", A * beta)
v.check("Ex 12-05.1b", Af1)
v.check("Ex 12-05.1c", 100 * (1 - Af1 * beta))
v.assert_true("error signal is x/(1 + T)", abs(e1 * (1 + A * beta) - 1) < 1e-12)
h = 1e-6
sens = (block_gain(A * (1 + h), beta)[0] / Af1 - 1) / h     # dAf/Af per dA/A, numerically
v.check("Ex 12-05.1d", 10 * sens)             # percent change for a 10% change in A
Af09 = block_gain(0.9 * A, beta)[0]
v.check("Ex 12-05.1e", Af09)
v.check("Ex 12-05.1f", 100 * (Af09 / Af1 - 1))


# ============================================================ Example 2: bandwidth extension
def closed_bw(A0, fp, beta, hi=1e12):
    H = lambda f: abs((A0 / (1 + 1j * f / fp)) / (1 + beta * A0 / (1 + 1j * f / fp)))  # noqa: E731
    return H(0.0), brentq(lambda f: H(f) - H(0.0) / math.sqrt(2), fp * 1e-3, hi, xtol=1e-9, rtol=1e-14)


A0, fp = 1e5, 10.0
g2, bw2 = closed_bw(A0, fp, 0.1)
v.check("Ex 12-05.2a", A0 * fp / 1e6)
v.check("Ex 12-05.2b", g2)
v.check("Ex 12-05.2c", bw2 / 1e3)
v.assert_true("gain-bandwidth product unchanged by feedback", abs(g2 * bw2 / (A0 * fp) - 1) < 1e-9)


# ============================================================ Example 3: series-shunt op-amp amplifier
def ninv(Rid, Ro, Aol, R1, R2, src=True):
    def build(u, sc):
        el = [("R", "p", "n", Rid), ("R", "x", "o", Ro), ("R", "o", "n", R2), ("R", "n", "0", R1)]
        el.append(("E", "x", "0", "p", "n", Aol) if sc is None else ("V", "x", "0", sc))
        if src:
            el.append(("V", "p", "0", u))
        return el, (Aol, "p", "n")
    return build


b3 = ninv(1e6, 100.0, 1e5, 1e3, 99e3)
L3 = loop(b3, lambda s: s[0]["o"])
v.check("Ex 12-05.3a", 1e6 * (1 + 1e5 * 0.01) / 1e9)
v.check("Ex 12-05.3b", 100 / (1 + 1e5 * 0.01))
v.check("Ex 12-05.3c", L3["Af"])
Zin3 = port_z(ninv(1e6, 100.0, 1e5, 1e3, 99e3, src=False), "p")
v.check("Ex 12-05.3d", Zin3["Z"] / 1e9)
v.assert_true("series mixing: loop broken with the input open (T_oc = 0)", abs(Zin3["Toc"]) < 1e-9)
Zo3 = port_z(b3, "o")
v.check("Ex 12-05.3e", Zo3["Z"])
v.assert_true("shunt sampling: loop killed with the output shorted (T_sc ~ 0)", abs(Zo3["Tsc"]) < 1e-6)
v.assert_true("full-circuit impedances within 0.2% of the topology-rule estimates",
              abs(Zin3["Z"] / 1.001e9 - 1) < 2e-3 and abs(Zo3["Z"] / (100 / 1001) - 1) < 2e-3)


# ============================================================ Example 4: shunt-shunt common-source stage
def cs_shunt(gm, RD, RF, RS, ro=None, src=True):
    def build(u, sc):
        el = [("R", "g", "0", RS), ("R", "g", "d", RF), ("R", "d", "0", RD)]
        if ro is not None:
            el.append(("R", "d", "0", ro))
        el.append(("G", "d", "0", "g", "0", gm) if sc is None else ("I", "d", "0", sc))
        if src:
            el.append(("I", "0", "g", u))
        return el, (gm, "g", "0")
    return build


b4 = cs_shunt(4e-3, 10e3, 50e3, 10e3)
L4 = loop(b4, lambda s: s[0]["d"])
Rin4 = port_z(cs_shunt(4e-3, 10e3, 50e3, 10e3, src=False), "g")
Rout4 = port_z(cs_shunt(4e-3, 10e3, 50e3, 10e3, src=False), "d")
v.check("Ex 12-05.4a", Rout4["Z0"] / 1e3)
v.check("Ex 12-05.4b", L4["T"])
v.check("Ex 12-05.4c", L4["Ainf"] / 1e3)
v.check("Ex 12-05.4d", L4["A0"] / 1e3)
v.check("Ex 12-05.4e", L4["Af"] / 1e3)
v.check("Ex 12-05.4f", 100 * (L4["Ainf"] / L4["Af"] - 1))
v.check("Ex 12-05.4g", Rin4["Z0"] / 1e3)
v.check("Ex 12-05.4h", Rin4["Z"] / 1e3)
v.check("Ex 12-05.4i", Rout4["Z"] / 1e3)
v.check("Ex 12-05.4j", L4["A0"] / (1 + L4["T"]))
v.assert_true("input and output: T_sc = 0 and T_oc = T", abs(Rin4["Tsc"]) < 1e-9 and abs(Rout4["Tsc"]) < 1e-9
              and abs(Rin4["Toc"] / L4["T"] - 1) < 1e-9 and abs(Rout4["Toc"] / L4["T"] - 1) < 1e-9)

# ============================================================ Example 5: gain spread
lo, hi_ = block_gain(5e4, 0.01)[0], block_gain(2e5, 0.01)[0]
v.check("Ex 12-05.5a", lo)
v.check("Ex 12-05.5b", hi_)
v.check("Ex 12-05.5c", 100 * (hi_ / lo - 1))
v.check("Ex 12-05.5d", 100 * (1 - lo * 0.01))


# ============================================================ Example 6: degeneration as series-series
def degen(gm, Rs, ro=None):
    """Gate driven by u, drain shorted to ground by a 0 V source (its current is the output)."""
    def build(u, sc):
        el = [("V", "gt", "0", u), ("R", "s", "0", Rs), ("V", "d", "0", 0.0)]
        if ro is not None:
            el.append(("R", "d", "s", ro))
        el.append(("G", "d", "s", "gt", "s", gm) if sc is None else ("I", "d", "s", sc))
        return el, (gm, "gt", "s")
    return build


def drain_current(s):
    # the 0 V source's branch current leaves d into the source; the current into the drain is its negative
    return -[val for i, val in s[1].items()][-1]


def degen_out(gm, Rs, ro):
    """Same device with the drain as a port (no short), gate grounded."""
    def build(u, sc):
        el = [("R", "s", "0", Rs), ("R", "d", "s", ro), ("R", "gt", "0", 1.0)]
        el.append(("G", "d", "s", "gt", "s", gm) if sc is None else ("I", "d", "s", sc))
        return el, (gm, "gt", "s")
    return build


def degen_short(gm, Rs, ro):
    def build(u, sc):
        el = [("V", "gt", "0", u), ("R", "s", "0", Rs), ("R", "d", "s", ro), ("V", "d", "0", 0.0)]
        el.append(("G", "d", "s", "gt", "s", gm) if sc is None else ("I", "d", "s", sc))
        return el, (gm, "gt", "s")
    return build


def short_current(s):
    # branch order: V(gt), V(d); the drain short is the second V element
    keys = sorted(s[1])
    return -s[1][keys[1]]


L6i = loop(degen(2e-3, 1e3), drain_current)
v.check("Ex 12-05.6a", L6i["T"])
v.check("Ex 12-05.6b", L6i["Af"] * 1e3)
L6 = loop(degen_short(2e-3, 1e3, 50e3), short_current)
v.check("Ex 12-05.6c", L6["Af"] * 1e3)
Z6 = port_z(degen_out(2e-3, 1e3, 50e3), "d")
v.check("Ex 12-05.6d", Z6["Z0"] / 1e3)
v.check("Ex 12-05.6e", Z6["Tsc"])
v.check("Ex 12-05.6f", Z6["Z"] / 1e3)
v.assert_true("series sampling: T_oc = 0 at the drain", abs(Z6["Toc"]) < 1e-9)

# ============================================================ practitioner numbers (TLV9062, R-182)
Amin = 10 ** (104 / 20)
v.check("Prac 12-05.a", Amin * 0.01)
v.check("Prac 12-05.b", 100 * (1 - block_gain(Amin, 0.01)[0] * 0.01))
fp_tlv = 10e6 / Amin
v.check("Prac 12-05.c", Amin / abs(1 + 1j * 100e3 / fp_tlv) * 0.01)


# ============================================================ simulation: harmonic reduction (Part 4)
def hd2(a1, c, beta, Y=1.0, N=4096):
    """Second-harmonic ratio of y = a1 (e + c e^2) at fundamental amplitude Y, open loop and with e = x - beta y."""
    cs = np.cos(TP * np.arange(N) / N)

    def harm(y):
        F = np.fft.rfft(y) / N * 2
        return abs(F[1]), abs(F[2])

    def op(E):
        e = E * cs
        return a1 * (e + c * e * e)

    def cl(X):
        Aq, Bq = beta * a1 * c, 1 + beta * a1          # beta a1 c e^2 + (1 + beta a1) e - x = 0
        e = (-Bq + np.sqrt(Bq * Bq + 4 * Aq * X * cs)) / (2 * Aq)
        return a1 * (e + c * e * e)

    Eo = brentq(lambda E: harm(op(E))[0] - Y, 1e-9, 1.0, xtol=1e-18)
    Xmax = 0.9 * (1 + beta * a1) ** 2 / (4 * beta * a1 * c)    # keeps the quadratic's discriminant positive
    Xc = brentq(lambda X: harm(cl(X))[0] - Y, 1e-9, Xmax, xtol=1e-16)
    ho, hc = harm(op(Eo)), harm(cl(Xc))
    v.assert_true("closed-loop residual of the nonlinear loop is zero",
                  float(np.max(np.abs(cl(Xc) - a1 * ((Xc * cs - beta * cl(Xc)) + c * (Xc * cs - beta * cl(Xc)) ** 2)))) < 1e-9)
    return ho[1] / ho[0], hc[1] / hc[0]


ol, clp = hd2(1000.0, 5.0, 0.099)
v.check("Sim 12-05.a", 100 * ol)
v.check("Sim 12-05.b", 1000 * 0.099)
v.check("Sim 12-05.c", 100 * clp)
v.check("Sim 12-05.d", ol / clp)
v.check("Sim 12-05.e", 1 + 1000 * 0.099)

# ============================================================ solutions
# 1
y1 = block_gain(5000, 0.1)[0]
v.check("12-05.1a", 5000 * 0.1)
v.check("12-05.1b", y1)
v.check("12-05.1c", 100 * (1 - y1 * 0.1))
# 2
T2 = brentq(lambda T: 1 / (1 + T) - 1e-4, 1, 1e6, xtol=1e-9)
v.check("12-05.2a", T2)
v.check("12-05.2b", T2 / 0.1)
# 3
A03 = 10 ** (130 / 20)
v.check("12-05.3a", A03)
fp3 = 10e6 / A03
v.check("12-05.3b", fp3)
v.check("12-05.3c", closed_bw(A03, fp3, 0.01)[1] / 1e3)
v.check("12-05.3d", closed_bw(A03, fp3, 1.0)[1] / 1e6)
# 5
T5 = brentq(lambda T: block_gain(3 * T / 0.01, 0.01)[0] / block_gain(T / 0.01, 0.01)[0] - 1 - 5e-4, 1, 1e6,
            xtol=1e-9)
v.check("12-05.5a", T5)
v.check("12-05.5b", T5 / 0.01)
# 6
v.check("12-05.6a", 2e5 * 0.1)
v.check("12-05.6b", 2e6 * (1 + 2e4) / 1e9)
v.check("12-05.6c", 50 / (1 + 2e4) * 1e3)
b6_open, b6_short = ninv(2e6, 50.0, 2e5, 1e3, 9e3, src=False), ninv(2e6, 50.0, 2e5, 1e3, 9e3)
v.assert_true("problem 6: full-circuit input and output resistances within 1% of the estimates",
              abs(port_z(b6_open, "p")["Z"] / 40.002e9 - 1) < 1e-2
              and abs(port_z(b6_short, "o")["Z"] / (50 / 20001) - 1) < 1e-2)


# 7: photodiode TIA, ideal op-amp output (E source with zero output resistance)
def tia(A, RF, RS, src=True):
    def build(u, sc):
        el = [("R", "n", "0", RS), ("R", "n", "o", RF), ("R", "pp", "0", 1.0)]
        el.append(("E", "o", "0", "pp", "n", A) if sc is None else ("V", "o", "0", sc))
        if src:
            el.append(("I", "0", "n", u))
        return el, (A, "pp", "n")
    return build


L7 = loop(tia(1e4, 100e3, 1e6), lambda s: s[0]["o"])
Z7 = port_z(tia(1e4, 100e3, 1e6, src=False), "n")
v.check("12-05.7a", L7["T"])
v.check("12-05.7b", L7["Ainf"] / 1e3)
v.assert_true("problem 7: direct transmission is zero", abs(L7["A0"]) < 1e-12)
v.check("12-05.7c", L7["Af"] / 1e3)
v.check("12-05.7d", Z7["Z0"] / 1e3)
v.check("12-05.7e", Z7["Z"])


# 8: inverting amplifier with R_id and R_o
def inv(A, Rid, Ro, R1, R2):
    def build(u, sc):
        el = [("V", "vs", "0", u), ("R", "vs", "n", R1), ("R", "n", "pp", Rid), ("V", "pp", "0", 0.0),
              ("R", "n", "o", R2), ("R", "x", "o", Ro)]
        el.append(("E", "x", "0", "pp", "n", A) if sc is None else ("V", "x", "0", sc))
        return el, (A, "pp", "n")
    return build


L8 = loop(inv(1e3, 10e3, 1e3, 1e3, 10e3), lambda s: s[0]["o"])
v.check("12-05.8a", 1e3 * 1e3 / 11e3)
v.check("12-05.8b", L8["T"])
v.check("12-05.8c", L8["Ainf"])
v.check("12-05.8d", L8["A0"])
v.check("12-05.8e", L8["Af"])
v.check("12-05.8f", 100 * (1 - L8["Af"] / -10))


# 9: source follower
def follower(gm, ro, RL, src=True):
    def build(u, sc):
        el = [("R", "s", "0", ro), ("R", "s", "0", RL), ("V", "gt", "0", u if src else 0.0)]
        el.append(("G", "0", "s", "gt", "s", gm) if sc is None else ("I", "0", "s", sc))
        return el, (gm, "gt", "s")
    return build


L9 = loop(follower(2e-3, 20e3, 10e3), lambda s: s[0]["s"])
Z9 = port_z(follower(2e-3, 20e3, 10e3, src=False), "s")
v.check("12-05.9a", L9["T"])
v.check("12-05.9b", L9["Af"])
v.check("12-05.9c", Z9["Z0"] / 1e3)
v.check("12-05.9d", Z9["Z"])
v.assert_true("problem 9: R_out = 1/g_m || r_o || R_L", abs(Z9["Z"] * (2e-3 + 1 / 20e3 + 1 / 10e3) - 1) < 1e-12)
# 10
b10 = brentq(lambda b: closed_bw(2000, 50e3, b)[1] - 10e6, 1e-3, 0.5, xtol=1e-15)
v.check("12-05.10a", 2000 * b10)
v.check("12-05.10b", b10)
v.check("12-05.10c", closed_bw(2000, 50e3, b10)[0])
v.check("12-05.10d", 2000 * 50e3 / 1e6)
# 11
b11 = cs_shunt(4e-3, 10e3, 50e3, 10e3, ro=40e3)
L11 = loop(b11, lambda s: s[0]["d"])
Zi11 = port_z(cs_shunt(4e-3, 10e3, 50e3, 10e3, ro=40e3, src=False), "g")
Zo11 = port_z(cs_shunt(4e-3, 10e3, 50e3, 10e3, ro=40e3, src=False), "d")
v.check("12-05.11a", par(10e3, 40e3) / 1e3)
v.check("12-05.11b", L11["T"])
v.check("12-05.11c", L11["Ainf"] / 1e3)
v.check("12-05.11d", L11["A0"] / 1e3)
v.check("12-05.11e", L11["Af"] / 1e3)
v.check("12-05.11f", Zi11["Z0"] / 1e3)
v.check("12-05.11g", Zi11["Z"] / 1e3)
v.check("12-05.11h", Zo11["Z0"] / 1e3)
v.check("12-05.11i", Zo11["Z"] / 1e3)
# 12
v.check("12-05.12a", L6["Ainf"] * 1e3)
v.check("12-05.12b", L6["T"])
v.assert_true("problem 12: direct transmission is zero", abs(L6["A0"]) < 1e-15)
v.check("12-05.12c", L6["Af"] * 1e3)
v.assert_true("problem 12: G_m = g_m/(1 + g_m R_S + R_S/r_o)", abs(L6["Af"] * (1 + 2 + 1e3 / 50e3) / 2e-3 - 1) < 1e-12)
# 13
T13 = brentq(lambda T: 1 / (1 + T) - 5e-4, 1, 1e6, xtol=1e-9)
A013 = T13 * 20
fp13 = brentq(lambda f: closed_bw(A013, f, 1 / 20)[1] - 1e6, 1, 1e5, xtol=1e-9)
v.check("12-05.13a", T13)
v.check("12-05.13b", A013)
v.check("12-05.13c", fp13)
v.check("12-05.13d", A013 * fp13 / 1e6)
# 14: an amplifier with 1% HD2 at 1 V placed in a loop with T = 49
c14 = 2 * 0.01 / (1.0 / 1000)              # HD2 = c E / 2 at e amplitude E = Y / a1 (checked by the simulation)
ol14, cl14 = hd2(1000.0, c14, 49 / 1000)
v.assert_true("problem 14: open-loop HD2 is 1%", abs(ol14 - 0.01) < 1e-4)
v.check("12-05.14a", ol14 / cl14)
v.check("12-05.14b", 100 * cl14)
v.check("12-05.14c", 10 * 10)

# ============================================================ lab README
if lab.exists():
    A0l, f1, f2 = 1e4, 1e3, 1e6
    w1, w2 = TP * f1, TP * f2

    def cl_poles(b):
        return np.roots([1 / (w1 * w2), 1 / w1 + 1 / w2, 1 + A0l * b])

    # the poles meet where the discriminant of the closed-loop denominator vanishes
    bm = brentq(lambda b: (1 / w1 + 1 / w2) ** 2 - 4 * (1 + A0l * b) / (w1 * w2), 1e-6, 1.0, xtol=1e-15)
    v.check("Lab 12-05.a", bm)
    v.check("Lab 12-05.b", float(np.abs(cl_poles(bm)[0].real)) / TP / 1e3)
    p = cl_poles(0.1)
    wn = math.sqrt(abs(p[0] * p[1]))
    v.check("Lab 12-05.c", wn / abs(p[0].real + p[1].real))
    v.check("Lab 12-05.d", 100 * (1 - block_gain(1e3, 0.01)[0] * 0.01))

sys.exit(v.finish())
