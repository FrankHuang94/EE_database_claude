#!/usr/bin/env python3
"""Verify every number in the Course 10 final-exam solutions.

Independent routes (not the hand formulas of the solutions):
- diode and bias circuits by Kirchhoff's equations solved with numpy or root finding on the device laws;
- the rectifier ripple by integrating the capacitor's discharge between peaks (exponential decay over half a cycle);
- small-signal gains and resistances by modified nodal analysis of the hybrid-pi circuits with test sources;
- cascades by nodal analysis with Norton-form stages; op-amp results from the complex single-pole loop;
- the Schmitt thresholds by sweeping an ideal comparator; the TIA from numpy.roots of its loop polynomial, with
  the feedback capacitor found in picofarad units.
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

v = Verifier.from_files("10-exam", HERE.parent / "exam" / "solutions.md")
VT = 1.380649e-23 * 300 / 1.602176634e-19


def par(*r):
    return 1 / sum(1 / x for x in r)


def db(x):
    return 20 * math.log10(abs(x))


class MNA:
    """Node 0 is ground. Elements are stamped into G x = b with extra rows for voltage sources."""

    def __init__(self):
        self.res, self.vccs, self.vsrc, self.isrc = [], [], [], []
        self.nodes = {"0"}

    def _n(self, *ns):
        self.nodes.update(ns)

    def R(self, a, b, r):
        self._n(a, b); self.res.append((a, b, r))

    def G(self, op, on, cp, cn, g):        # current g (v_cp - v_cn) flows from op to on through the element
        self._n(op, on, cp, cn); self.vccs.append((op, on, cp, cn, g))

    def V(self, p, n, val):
        self._n(p, n); self.vsrc.append((p, n, val))

    def I(self, p, n, val):                # current val flows from p to n through the source (into node n)
        self._n(p, n); self.isrc.append((p, n, val))

    def mos(self, d, g, s, b, gm, gmb=0.0, ro=math.inf):
        self.G(d, s, g, s, gm)
        if gmb:
            self.G(d, s, b, s, gmb)
        if not math.isinf(ro):
            self.R(d, s, ro)

    def solve(self):
        names = sorted(self.nodes - {"0"})
        idx = {n: i for i, n in enumerate(names)}
        n, m = len(names), len(self.vsrc)
        A = np.zeros((n + m, n + m)); z = np.zeros(n + m)

        def add(r, c, val):
            if r in idx and c in idx:
                A[idx[r], idx[c]] += val
        for a, b, r in self.res:
            g = 1 / r
            add(a, a, g); add(b, b, g); add(a, b, -g); add(b, a, -g)
        for op, on, cp, cn, g in self.vccs:
            add(op, cp, g); add(op, cn, -g); add(on, cp, -g); add(on, cn, g)
        for p, nn, val in self.isrc:
            if p in idx: z[idx[p]] -= val
            if nn in idx: z[idx[nn]] += val
        for k, (p, nn, val) in enumerate(self.vsrc):
            if p in idx: A[idx[p], n + k] += 1; A[n + k, idx[p]] += 1
            if nn in idx: A[idx[nn], n + k] -= 1; A[n + k, idx[nn]] -= 1
            z[n + k] = val
        x = np.linalg.solve(A, z)
        out = {name: x[i] for name, i in idx.items()}
        out["0"] = 0.0
        out["_i"] = x[n:]                  # source currents (from + through the source to -)
        return out


def bjt(c, cc, b, e, gm, rpi, ro=math.inf):
    c.G(cc, e, b, e, gm)
    c.R(b, e, rpi)
    if not math.isinf(ro):
        c.R(cc, e, ro)


def mos(c, d, g, s, gm, gmb=0.0, ro=math.inf, body="0"):
    c.G(d, s, g, s, gm)
    if gmb:
        c.G(d, s, body, s, gmb)
    if not math.isinf(ro):
        c.R(d, s, ro)


# 1
i1 = brentq(lambda i: 3 - 1e3 * i - 0.7, 0, 1)
v.check("X10.1a", i1 * 1e3)
v.check("X10.1b", 1 / ((i1 / VT)))

# 2: peak, then exponential discharge for a half cycle; ripple from the decay (small-ripple limit checked)
vpk_t = 12 * math.sqrt(2)
vp = vpk_t - 2 * 0.7
v.check("X10.2a", vpk_t)
v.check("X10.2b", vp)
tau = 500 * 1000e-6
exact_drop = vp * (1 - math.exp(-(1 / 120) / tau))
v.assert_true("small-ripple formula within 1% of the exponential discharge", abs(exact_drop / (vp / (120 * tau)) - 1) < 0.01)
vr = vp * (1 / 120) / tau
v.check("X10.2c", vr)
v.check("X10.2d", vp - vr / 2)
v.check("X10.2e", (vp - vr / 2) / 500 * 1e3)

# 3
r3 = brentq(lambda r: (8 - 5.1) / r - 21e-3, 1, 1e4)
v.check("X10.3a", r3)
iz = (10 - 5.1) / r3
v.check("X10.3b", iz * 1e3)
v.check("X10.3c", iz * 5.1)

# 4: solve KVL around gate-source with the square law
k, vtn = 2e-3, 0.5
vgs = brentq(lambda x: 3 - x - 2e3 * 0.5 * k * (x - vtn) ** 2, vtn, 3)
idq = 0.5 * k * (vgs - vtn) ** 2
v.check("X10.4a", vgs - vtn)
v.check("X10.4b", vgs)
v.check("X10.4c", idq * 1e3)
v.check("X10.4d", 9 - 3e3 * idq)
v.check("X10.4e", 2e3 * idq)
v.check("X10.4f", 9 - 5e3 * idq)
v.assert_true("Q4 transistor saturated", 9 - 5e3 * idq > vgs - vtn)
vgs2 = brentq(lambda x: 3 - x - 2e3 * 0.5 * k * (x - 0.55) ** 2, 0.55, 3)
id2 = 0.5 * k * (vgs2 - 0.55) ** 2
v.check("X10.4g", id2 * 1e3)
v.check("X10.4h", (id2 / idq - 1) * 100)

# 5: four-resistor bias as a linear system (unknowns v_b, v_e, i_b)
A = np.array([[-(1 / 33e3 + 1 / 10e3), 0, -1.0], [1, -1, 0], [0, 1 / 1e3, -121.0]])
vb, ve, ib = np.linalg.solve(A, np.array([-10 / 33e3, 0.7, 0.0]))
ic5, ie5 = 120 * ib, 121 * ib
v.check("X10.5a", 10 * 10 / 43)
v.check("X10.5b", par(33e3, 10e3) / 1e3)
v.check("X10.5c", ie5 * 1e3)
v.check("X10.5d", ic5 * 1e3)
v.check("X10.5e", 10 - 3.3e3 * ic5)
v.check("X10.5f", ve)
v.check("X10.5g", 10 - 3.3e3 * ic5 - ve)

# 6
gmb_, rpi_, ro_b = ic5 / VT, 120 / (ic5 / VT), 80 / ic5
gmm = (0.5 * k * ((vgs - vtn) + 1e-7) ** 2 - 0.5 * k * ((vgs - vtn) - 1e-7) ** 2) / 2e-7
rom = 1 / (0.05 * idq)
v.check("X10.6a", gmb_ * 1e3)
v.check("X10.6b", rpi_ / 1e3)
v.check("X10.6c", ro_b / 1e3)
v.check("X10.6d", gmb_ * ro_b)
v.check("X10.6e", gmm * 1e3)
v.check("X10.6f", rom / 1e3)
v.check("X10.6g", gmm * rom)
v.check("X10.6h", gmb_ / ic5)
v.check("X10.6i", gmm / idq)


# 7: cascade by nodal analysis (Norton-form stages)
def chain(stages, rsig, rl):
    n = len(stages)
    G = np.zeros((n + 1, n + 1)); I = np.zeros(n + 1)
    G[0, 0] += 1 / rsig; I[0] = 1 / rsig
    for j, (ri, a, ro) in enumerate(stages):
        G[j, j] += 1 / ri; G[j + 1, j + 1] += 1 / ro; G[j + 1, j] -= a / ro
    G[n, n] += 1 / rl
    return np.linalg.solve(G, I)[-1]


g7a = chain([(20e3, -40, 4e3)], 5e3, 1e3)
g7b = chain([(20e3, -40, 4e3), (200e3, 0.98, 50)], 5e3, 1e3)
v.check("X10.7a", g7a)
v.check("X10.7b", db(g7a))
v.check("X10.7c", g7b)
v.check("X10.7d", db(g7b))

# 8
c = MNA(); c.V("g", "0", 1.0); mos(c, "d", "g", "0", gmm, ro=rom); c.R("d", "0", 3e3); c.R("d", "0", 10e3)
v.check("X10.8a", c.solve()["d"])
c = MNA(); c.V("g", "0", 1.0); mos(c, "d", "g", "s", gmm, body="s"); c.R("s", "0", 2e3); c.R("d", "0", 3e3); c.R("d", "0", 10e3)
v.check("X10.8b", c.solve()["d"])
c = MNA(); c.V("g", "0", 0.0); c.V("vdd", "0", 0.0); mos(c, "vdd", "g", "s", gmm, gmb=0.2 * gmm); c.I("0", "s", 1.0)
v.check("X10.8c", c.solve()["s"])
c = MNA(); c.V("g", "0", 1.0); c.V("vdd", "0", 0.0); mos(c, "vdd", "g", "s", gmm, gmb=0.2 * gmm); c.R("s", "0", 1e15)
v.check("X10.8d", c.solve()["s"])

# 9
rth = par(33e3, 10e3)
c = MNA(); c.V("s", "0", 1.0); c.R("s", "b", 1e3); c.R("b", "0", rth); bjt(c, "c", "b", "0", gmb_, rpi_, ro_b)
c.R("c", "0", 3.3e3); c.R("c", "0", 10e3)
x = c.solve()
v.check("X10.9a", x["b"] / ((1 - x["b"]) / 1e3) / 1e3)
v.check("X10.9b", x["b"])
v.check("X10.9c", x["c"] / x["b"])
v.check("X10.9d", x["c"])
v.check("X10.9e", (120 / 121) / gmb_)
c = MNA(); c.V("b", "0", 1.0); bjt(c, "0", "b", "e", gmb_, rpi_); c.R("e", "0", 100.0)
rinb = 1 / -c.solve()["_i"][0]
v.check("X10.9f", rinb / 1e3)
v.check("X10.9g", par(rth, rinb) / 1e3)
c = MNA(); c.V("b", "0", 1.0); bjt(c, "c", "b", "e", gmb_, rpi_); c.R("e", "0", 100.0); c.R("c", "0", 3.3e3); c.R("c", "0", 10e3)
v.check("X10.9h", c.solve()["c"])
c = MNA(); c.V("s", "0", 1.0); c.R("s", "b", 1e3); c.R("b", "0", rth); bjt(c, "c", "b", "e", gmb_, rpi_)
c.R("e", "0", 100.0); c.R("c", "0", 3.3e3); c.R("c", "0", 10e3)
v.check("X10.9i", c.solve()["c"])

# 10
c = MNA(); c.V("d", "0", 1.0); c.V("g", "0", 0.0); mos(c, "d", "g", "0", 1e-3, ro=50e3)
v.check("X10.10a", 1 / -c.solve()["_i"][0] / 1e3)
c = MNA(); c.V("o", "0", 1.0); c.V("g", "0", 0.0); mos(c, "x", "g", "0", 1e-3, ro=50e3); mos(c, "o", "g", "x", 1e-3, ro=50e3)
v.check("X10.10b", 1 / -c.solve()["_i"][0] / 1e6)
v.check("X10.10c", 0.2)
v.check("X10.10d", 0.45 + 2 * 0.2)
v.check("X10.10e", 2 * 0.2)
rng = np.random.default_rng(10)
s_vt = 3.5e-3 / math.sqrt(20)
mc = (2 / 0.2) * rng.normal(0, s_vt, 400000)
v.assert_true("Monte Carlo spread matches (2/V_ov) sigma(dV_TH)", abs(mc.std() / ((2 / 0.2) * s_vt) - 1) < 0.01)
v.check("X10.10f", (2 / 0.2) * s_vt * 100)
v.check("X10.10g", brentq(lambda a: (2 / 0.2) * 3.5e-3 / math.sqrt(a) - 0.002, 1, 1e6))


# 11
def H(f, a0_db, gbw, ng):
    a0 = 10 ** (a0_db / 20)
    a = a0 / (1 + 1j * f / (gbw / a0))
    return a / (1 + a / ng)


g11 = abs(H(0.0, 100, 5e6, 20))
v.check("X10.11a", g11)
v.check("X10.11b", (1 - g11 / 20) * 100)
v.check("X10.11c", brentq(lambda f: abs(H(f, 200, 5e6, 20)) / 20 - 1 / math.sqrt(2), 1, 1e8) / 1e3)
v.check("X10.11d", brentq(lambda f: 2 * math.pi * f * 3 - 2e6, 1, 1e8) / 1e3)
v.check("X10.11e", 0.5e-3 * 20 * 1e3)


# 12
def thresholds(r1, r2, vref, vdd):
    xs = np.linspace(0, vdd, 330001)
    vo, up = 0.0, None
    for x_ in xs:
        if (x_ * r2 + vo * r1) / (r1 + r2) > vref:
            up, vo = x_, vdd
            break
    for x_ in xs[::-1]:
        if (x_ * r2 + vo * r1) / (r1 + r2) < vref:
            return up, x_
    return up, None


r1 = brentq(lambda r: 3.3 * r / 100e3 - 0.05, 1, 1e6)
v.check("X10.12a", r1 / 1e3)
up, down = thresholds(r1, 100e3, 1.65, 3.3)
v.check("X10.12b", up)
v.check("X10.12c", down)


def loop(rf, cin_pf, cf_pf, gbw):
    wt = 2 * math.pi * gbw
    ct, cf = (cin_pf + cf_pf) * 1e-12, cf_pf * 1e-12
    r = np.roots([rf * ct, 1 + wt * rf * cf, wt])
    w0 = math.sqrt(abs(r[0] * r[1]))
    return w0 / (-(r[0] + r[1]).real), w0 / (2 * math.pi)


q0, f0 = loop(200e3, 10, 1e-9, 20e6)
v.check("X10.12d", f0 / 1e6)
v.check("X10.12e", q0)
cf = brentq(lambda cc: loop(200e3, 10, cc, 20e6)[0] - 1 / math.sqrt(2), 1e-4, 100, xtol=1e-12)
v.check("X10.12f", cf)
v.check("X10.12g", loop(200e3, 10, cf, 20e6)[1] / 1e6)

# 14
itot = 5e-6 / 1.2
v.check("X10.14a", itot * 1e6)
v.check("X10.14b", itot / 2 * 1e6)
v.check("X10.14c", (itot / 2) / (1.3 * VT) * 1e6)

v.finish()
