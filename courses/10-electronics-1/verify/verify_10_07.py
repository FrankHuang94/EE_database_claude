#!/usr/bin/env python3
"""Verify every number in chapter 10-07 (BJT single-stage amplifiers), its solutions and lab.

Independent route: the bias of Example 10-07.1 is solved from Kirchhoff's equations; hybrid-pi parameters are
numerical derivatives of the exponential law; every gain and resistance comes from a modified-nodal-analysis
solution of the small-signal circuit with explicit test sources, not from the chapter's closed forms.
Distortion amplitudes come from an FFT of the exact large-signal laws.
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
v = Verifier.from_files("10-07", COURSE / "chapters" / "10-07-bjt-single-stage-amplifiers.md",
                        COURSE / "solutions" / "10-07-solutions.md",
                        COURSE / "labs" / "10-07-lab" / "README.md")


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


VT = 1.380649e-23 * 300 / 1.602176634e-19


def par(*r):
    return 1 / sum(1 / x for x in r)


def hp(ic, beta, va=math.inf):
    """Hybrid-pi parameters by differentiating i_C = I_S e^(v_BE/V_T)(1 + v_CE/V_A) and i_B = i_C/beta."""
    i_s = ic / math.exp(0.7 / VT)
    h = 1e-6
    gm = (i_s * math.exp((0.7 + h) / VT) - i_s * math.exp((0.7 - h) / VT)) / (2 * h)
    rpi = 1 / (gm / beta)
    ro = math.inf if math.isinf(va) else va / ic
    return gm, rpi, ro


def bjt(c, n, cc, b, e, gm, rpi, ro=math.inf):
    c.G(cc, e, b, e, gm)
    c.R(b, e, rpi)
    if not math.isinf(ro):
        c.R(cc, e, ro)


# ------------------------------------------------------------------ theory
gm1m, rpi1m, _ = hp(1e-3, 100)
v.check("T 10-07.a", gm1m / 1e-3)
v.check("T 10-07.b", gm1m * 50 / 1e-3)
c = MNA(); c.V("b", "0", 1.0); bjt(c, None, "0", "b", "e", gm1m, rpi1m); c.R("e", "0", 1e3)
x = c.solve()
v.check("T 10-07.c", (1 / -x["_i"][0] - rpi1m) / 1e3)     # reflected part of the base input resistance

# ------------------------------------------------------------------ Example 1: bias from Kirchhoff, then the small-signal circuit
A = np.array([[-(1 / 47e3 + 1 / 10e3), 0, -1.0],       # base KCL: (12 - v_b)/47k - v_b/10k - i_b = 0
              [1, -1, 0],                                 # v_b - v_e = 0.7
              [0, 1 / 1e3, -101.0]])                      # emitter KCL: v_e/1k = (beta + 1) i_b
z = np.array([-12 / 47e3, 0.7, 0.0])
vb, ve, ib = np.linalg.solve(A, z)
IC1 = 100 * ib
gm, rpi, _ = hp(IC1, 100)
RB = par(47e3, 10e3)
v.check("Ex 10-07.1a", gm * 1e3)
v.check("Ex 10-07.1b", rpi / 1e3)
v.check("Ex 10-07.1c", RB / 1e3)


def ce_discrete(rsig, rl, re_unbyp=0.0, beta=100, ic=IC1, rb=RB, rc=4.7e3, drive_base=False):
    gm_, rpi_, _ = hp(ic, beta)
    c = MNA()
    if drive_base:
        c.V("b", "0", 1.0)
    else:
        c.V("s", "0", 1.0); c.R("s", "b", rsig)
    c.R("b", "0", rb)
    e = "e" if re_unbyp else "0"
    if re_unbyp:
        c.R("e", "0", re_unbyp)
    bjt(c, None, "c", "b", e, gm_, rpi_)
    c.R("c", "0", rc)
    if rl:
        c.R("c", "0", rl)
    return c.solve()


xb = ce_discrete(None, None, drive_base=True)
v.check("Ex 10-07.1d", 1 / -xb["_i"][0] / 1e3)
v.check("Ex 10-07.1e", xb["c"])
v.check("Ex 10-07.1f", IC1 * 4.7e3 / VT)
v.check("Ex 10-07.1j", IC1 * 4.7e3)
v.check("Ex 10-07.1k", round(IC1 * 1e3, 3) * 1e-3 * 4.7e3 / VT)
v.check("Ex 10-07.1l", IC1 * 1e3)
x1 = ce_discrete(1e3, 10e3)
v.check("Ex 10-07.1g", x1["b"])
v.check("Ex 10-07.1h", x1["c"] / x1["b"])
v.check("Ex 10-07.1i", x1["c"])

# ------------------------------------------------------------------ Example 2
alpha = 100 / 101
v.check("Ex 10-07.2a", alpha / gm)
c = MNA(); c.V("b", "0", 1.0); bjt(c, None, "0", "b", "e", gm, rpi); c.R("e", "0", 100.0)
rin_b = 1 / -c.solve()["_i"][0]
v.check("Ex 10-07.2b", rin_b / 1e3)
v.check("Ex 10-07.2c", par(RB, rin_b) / 1e3)
x2b = ce_discrete(None, None, re_unbyp=100.0, drive_base=True)
v.check("Ex 10-07.2d", x2b["c"])
v.check("Ex 10-07.2e", ce_discrete(1e3, 10e3, re_unbyp=100.0)["c"])
v.check("Ex 10-07.2f", xb["c"] / x2b["c"])
v.check("Ex 10-07.2g", x1["c"] / ce_discrete(1e3, 10e3, re_unbyp=100.0)["c"])

# ------------------------------------------------------------------ Example 3: collector output resistance by test source
gm3, rpi3, ro3 = hp(1e-3, 100, 50)


def rout_c(re, rsig=0.0, gm_=gm3, rpi_=rpi3, ro_=ro3):
    c = MNA()
    c.V("c", "0", 1.0)
    if rsig:
        c.R("b", "0", rsig); base = "b"
    else:
        base = "0"
    e = "e" if re else "0"
    if re:
        c.R("e", "0", re)
    bjt(c, None, "c", base, e, gm_, rpi_, ro_)
    return 1 / -c.solve()["_i"][0]


for key, re in (("Ex 10-07.3a", 0.0), ("Ex 10-07.3b", 1e3), ("Ex 10-07.3c", 10e3), ("Ex 10-07.3d", 1e12)):
    v.check(key, rout_c(re) / 1e3)
v.check("Ex 10-07.3e", rout_c(1e3) / rout_c(0.0))

# ------------------------------------------------------------------ CB input resistance with r_o (test source, MNA)
cbr = MNA()
cbr.V("x", "0", 1.0)                                     # test voltage at the emitter, base grounded
bjt(cbr, None, "c", "0", "x", gm3, rpi3, ro3)
cbr.R("c", "0", 5e3)
rin_cb_ro = 1 / -cbr.solve()["_i"][0]
v.check("T 10-07.p", rin_cb_ro)
v.check("T 10-07.q", (rin_cb_ro / ((100 / 101) / gm3) - 1) * 100)

# ------------------------------------------------------------------ Example 4: common base


def cb(ic, beta, rc, rsig):
    gm_, rpi_, _ = hp(ic, beta)
    c = MNA()
    if rsig is None:
        c.V("e", "0", 1.0)
    else:
        c.V("s", "0", 1.0); c.R("s", "e", rsig)
    bjt(c, None, "c", "0", "e", gm_, rpi_)
    c.R("c", "0", rc)
    x = c.solve()
    rin = 1 / -x["_i"][0] if rsig is None else x["e"] / ((1 - x["e"]) / rsig)
    return x, rin


x4, rin4 = cb(1e-3, 100, 5e3, None)
v.check("Ex 10-07.4a", rin4)
v.check("Ex 10-07.4b", x4["c"])
x4s, _ = cb(1e-3, 100, 5e3, 50.0)
v.check("Ex 10-07.4c", x4s["e"])
v.check("Ex 10-07.4d", x4s["c"])
# current gain: collector current into a short over emitter current
c = MNA(); c.I("0", "e", 1.0); g_, r_, _ = hp(1e-3, 100); bjt(c, None, "c", "0", "e", g_, r_); c.V("c", "0", 0.0)
v.check("Ex 10-07.4e", abs(c.solve()["_i"][0]))       # collector-current magnitude per ampere of emitter current
ie50 = brentq(lambda i: cb(i * 100 / 101, 100, 5e3, None)[1] - 50.0, 1e-5, 1e-2)
v.check("Ex 10-07.4f", ie50 * 1e3)
v.check("Ex 10-07.4g", ie50 * 100 / 101 * 1e3)

# ------------------------------------------------------------------ Example 5: emitter follower


def ef(ic, beta, re, rl, rsig, test=False):
    gm_, rpi_, _ = hp(ic, beta)
    c = MNA()
    c.V("s", "0", 0.0 if test else 1.0); c.R("s", "b", rsig)
    bjt(c, None, "0", "b", "e", gm_, rpi_)
    c.R("e", "0", re)
    if rl:
        c.R("e", "0", rl)
    if test:
        c.I("0", "e", 1.0)
    return c.solve()


x5 = ef(1e-3, 100, 5e3, 1e3, 10e3)
v.check("Ex 10-07.5a", par(5e3, 1e3))
rin5 = x5["b"] / ((1 - x5["b"]) / 10e3)
v.check("Ex 10-07.5b", rin5 / 1e3)
v.check("Ex 10-07.5c", x5["b"])
v.check("Ex 10-07.5d", x5["e"] / x5["b"])
v.check("Ex 10-07.5e", x5["e"])
v.check("Ex 10-07.5f", ef(1e-3, 100, 1e30, None, 10e3, test=True)["e"])
v.check("Ex 10-07.5g", ef(1e-3, 100, 5e3, None, 10e3, test=True)["e"])

# ------------------------------------------------------------------ Example 6
gmb6, rpi6, ro6 = hp(0.5e-3, 100, 50)
c = MNA(); c.V("b", "0", 1.0); bjt(c, None, "c", "b", "0", gmb6, rpi6); c.R("c", "0", 5e3)
v.check("Ex 10-07.6a", gmb6 * 1e3)
v.check("Ex 10-07.6b", c.solve()["c"])
gmm6 = 2 * 0.5e-3 / 0.2
v.check("Ex 10-07.6c", gmm6 * 1e3)
v.check("Ex 10-07.6d", -gmm6 * 5e3)
v.check("Ex 10-07.6e", gmb6 / gmm6)
v.check("Ex 10-07.6f", rpi6 / 1e3)
v.check("Ex 10-07.6g", gmb6 * ro6)
v.check("Ex 10-07.6h", gmm6 * 1 / (0.1 * 0.5e-3))
N = 8192
TH = 2 * np.pi * np.arange(N) / N


def hd2_exp(a):
    cc = np.fft.rfft(np.exp(a / VT * np.cos(TH))) / N
    return abs(cc[2]) / abs(cc[1])


def hd2_sq(a, vov):
    cc = np.fft.rfft((vov + a * np.cos(TH)) ** 2) / N
    return abs(cc[2]) / abs(cc[1])


v.check("Ex 10-07.6i", brentq(lambda a: hd2_exp(a) - 0.01, 1e-5, 5e-3) * 1e3)
v.check("Ex 10-07.6j", brentq(lambda a: hd2_sq(a, 0.2) - 0.01, 1e-4, 0.05) * 1e3)

# ------------------------------------------------------------------ Example 7


def degen_gain(beta, re1):
    gm_, rpi_, _ = hp(1e-3, beta)
    c = MNA(); c.V("b", "0", 1.0); bjt(c, None, "c", "b", "e", gm_, rpi_); c.R("e", "0", re1); c.R("c", "0", 4.7e3)
    x = c.solve()
    return x["c"], 1 / -x["_i"][0]


re1_exact = brentq(lambda r: degen_gain(100, r)[0] + 10, 1, 5e3)
E96 = [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165,
       169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280,
       287, 294, 301, 309, 316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475,
       487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681, 698, 715, 732, 750, 768, 787, 806,
       825, 845, 866, 887, 909, 931, 953, 976]
re1_e96 = min(E96, key=lambda r: abs(r - re1_exact))
v.check("Ex 10-07.7l", re1_exact)
v.check("Ex 10-07.7a", re1_e96)
g100, rin100 = degen_gain(100, float(re1_e96))
g300, rin300 = degen_gain(300, float(re1_e96))
v.check("Ex 10-07.7b", g100)
v.check("Ex 10-07.7c", g300)
v.check("Ex 10-07.7d", (g300 / g100 - 1) * 100)
v.check("Ex 10-07.7e", rin100 / 1e3)
v.check("Ex 10-07.7f", rin300 / 1e3)
v.check("Ex 10-07.7g", hp(1e-3, 100)[1] / 1e3)
v.check("Ex 10-07.7h", hp(1e-3, 300)[1] / 1e3)
v.check("Ex 10-07.7i", re1_exact + (100 / 101) / hp(1e-3, 100)[0])
v.check("Ex 10-07.7j", 300 / 301)
v.check("Ex 10-07.7k", (300 / 301) / hp(1e-3, 300)[0])

# ================================================================== solutions
g, rp, _ = hp(1e-3, 120)
c = MNA(); c.V("b", "0", 1.0); bjt(c, None, "0", "b", "e", g, rp); c.R("e", "0", 220.0)
v.check("10-07.1a", rp / 1e3)
v.check("10-07.1b", 1 / -c.solve()["_i"][0] / 1e3)
c = MNA(); c.V("e", "0", 1.0); bjt(c, None, "0", "0", "e", g, rp)
v.check("10-07.1c", 1 / -c.solve()["_i"][0])
c = MNA(); c.V("e", "0", 1.0); c.R("b", "0", 12e3); bjt(c, None, "0", "b", "e", g, rp)
v.check("10-07.1d", 1 / -c.solve()["_i"][0])

for ic in (1e-3, 0.2e-3):
    g, rp, _ = hp(ic, 100)
    c = MNA(); c.V("b", "0", 1.0); bjt(c, None, "c", "b", "0", g, rp); c.R("c", "0", 2.0 / ic)
    v.check("10-07.2a", -c.solve()["c"])
v.check("10-07.2b", 2 * 2.0 / 0.2)

g, rp, _ = hp(2e-3, 150)
c = MNA(); c.V("e", "0", 1.0); bjt(c, None, "0", "0", "e", g, rp)
re3 = 1 / -c.solve()["_i"][0]
v.check("10-07.3a", re3)
c = MNA(); c.V("b", "0", 1.0); bjt(c, None, "0", "b", "e", g, rp); c.R("e", "0", 500.0)
x = c.solve()
v.check("10-07.3b", x["e"])
v.check("10-07.3c", 1 / -x["_i"][0] / 1e3)
c = MNA(); c.V("b", "0", 0.0); bjt(c, None, "0", "b", "e", g, rp); c.R("e", "0", 500.0); c.I("0", "e", 1.0)
v.check("10-07.3d", c.solve()["e"])

g, rp, _ = hp(2e-3, 100)


def stage4(re1):
    c = MNA(); c.V("b", "0", 1.0); bjt(c, None, "c", "b", "e", g, rp); c.R("e", "0", re1); c.R("c", "0", 2.2e3)
    x = c.solve()
    return x["c"], 1 / -x["_i"][0]


re1_4 = brentq(lambda r: stage4(r)[0] + 10, 1, 5e3)
v.check("10-07.4a", (100 / 101) / g)
v.check("10-07.4b", re1_4 + (100 / 101) / g)
v.check("10-07.4c", re1_4)
v.check("10-07.4d", stage4(re1_4)[1] / 1e3)
v.check("10-07.4e", par(10e3, stage4(re1_4)[1]) / 1e3)

g, rp, ro = hp(0.5e-3, 200, 80)
v.check("10-07.5a", g * 1e3)
v.check("10-07.5b", rp / 1e3)
v.check("10-07.5c", ro / 1e3)
v.check("10-07.5d", rout_c(2e3, gm_=g, rpi_=rp, ro_=ro) / 1e3)
v.check("10-07.5e", rout_c(1e15, gm_=g, rpi_=rp, ro_=ro) / 1e3)

x6, rin6 = cb(0.25e-3, 100, 20e3, None)
v.check("10-07.6a", rin6)
v.check("10-07.6b", x6["c"])
x6s, _ = cb(0.25e-3, 100, 20e3, 1e3)
v.check("10-07.6c", x6s["e"])
v.check("10-07.6d", x6s["c"])

v.check("10-07.7a", ef(1e-3, 100, 1e30, None, 100e3, test=True)["e"])
v.check("10-07.7b", cb(1e-3, 100, 1.0, None)[1])

for (ic, ka, kb, kc) in ((1e-3, "10-07.8a", "10-07.8b", "10-07.8c"), (10e-6, "10-07.8d", "10-07.8e", "10-07.8f")):
    g, rp, _ = hp(ic, 100)
    c = MNA(); c.V("s", "0", 1.0); c.R("s", "b", 1e6); bjt(c, None, "c", "b", "0", g, rp); c.R("c", "0", 1e3)
    v.check(ka, rp / 1e3)
    v.check(kb, c.solve()["b"])
    v.check(kc, ic / 100 * 1e6)

for key, rs in (("10-07.9a", 0.0), ("10-07.9b", 10e3)):
    v.check(key, rout_c(1e3, rsig=rs) / 1e3)

ie10, re10, rl10 = 1e-3, 5e3, 1e3
v.check("10-07.10a", ie10 * par(re10, rl10))
i_needed = brentq(lambda i: i * par(re10, rl10) - 2.0, 1e-4, 0.1)
v.check("10-07.10b", i_needed * 1e3)
v.check("10-07.10c", -(0.7 + i_needed * re10))

for beta, kr, kg, kr0, kg0 in ((100, "10-07.11a", "10-07.11b", "10-07.11e", "10-07.11f"),
                               (300, "10-07.11c", "10-07.11d", "10-07.11g", "10-07.11h")):
    gm_, rpi_, _ = hp(1e-3, beta)
    c = MNA(); c.V("s", "0", 1.0); c.R("s", "b", 10e3); c.R("b", "0", 50e3)
    bjt(c, None, "c", "b", "e", gm_, rpi_); c.R("e", "0", 440.0); c.R("c", "0", 4.7e3)
    x = c.solve()
    v.check(kr, x["b"] / ((1 - x["b"]) / 10e3) / 1e3)
    v.check(kg, x["c"])
    c = MNA(); c.V("s", "0", 1.0); c.R("s", "b", 10e3); c.R("b", "0", 50e3)
    bjt(c, None, "c", "b", "0", gm_, rpi_); c.R("c", "0", 4.7e3)
    x = c.solve()
    v.check(kr0, x["b"] / ((1 - x["b"]) / 10e3) / 1e3)
    v.check(kg0, x["c"])

g2_, rp2_, _ = hp(1e-3, 100)
c = MNA(); c.V("s", "0", 1.0); c.R("s", "b", 50e3); bjt(c, None, "c", "b", "0", g2_, rp2_); c.R("c", "0", 5e3)
v.check("10-07.12a", c.solve()["c"])
g1_, rp1_, _ = hp(0.1e-3, 100)
c = MNA(); c.V("s", "0", 1.0); c.R("s", "b1", 50e3)
bjt(c, None, "0", "b1", "b2", g1_, rp1_)          # follower: collector at signal ground, emitter drives b2
bjt(c, None, "c", "b2", "0", g2_, rp2_); c.R("c", "0", 5e3)
x = c.solve()
v.check("10-07.12b", x["b1"] / ((1 - x["b1"]) / 50e3) / 1e3)
v.check("10-07.12c", x["b2"] / x["b1"])
v.check("10-07.12d", x["b1"])
v.check("10-07.12e", x["c"])

# ================================================================== lab
gm300, rpi300, _ = hp(IC1, 300)
v.check("Lab 10-07.a", rpi300 / 1e3)
rin300b = par(RB, rpi300)
v.check("Lab 10-07.b", rin300b / 1e3)
v.check("Lab 10-07.c", rin300b / (rin300b + 1e3))
v.check("Lab 10-07.d", (ce_discrete(1e3, 10e3, beta=300)["c"] / ce_discrete(1e3, 10e3)["c"] - 1) * 100)
ceil = rout_c(1e15)
v.check("Lab 10-07.e", brentq(lambda r: rout_c(r) - 0.9 * ceil, 1, 1e8) / 1e3)
v.check("Lab 10-07.f", (1e-3 * 101 / 100) * par(5e3, 1e3))
v.check("Lab 10-07.g", hp(1e-3, 100)[0] / (2 * 1e-3 / 0.2))
# Part 3: the base amplitude at which the follower's emitter swing reaches 99% of I_E (R_E || R_L), exponential model
IE0, rpar = 1.0101010101e-3, par(5e3, 1e3)


def emitter_min(vb_amp, n=721):
    th = np.linspace(0, 2 * np.pi, n)
    return min(brentq(lambda uu: IE0 * math.exp((vb_amp * math.sin(t_) - uu) / VT) - IE0 - uu / rpar,
                      -IE0 * rpar - 1e-9, abs(vb_amp) + 1.0, xtol=1e-15) for t_ in th)


v.check("Lab 10-07.h", brentq(lambda a_: emitter_min(a_) + 0.99 * IE0 * rpar, 0.1, 2.0, xtol=1e-6))
# Part 4: EKV g_m/I_D of a fixed-size MOSFET, by differentiating the EKV current numerically
n_e, kn_e = 1.3, 25e-3
ispec_e = 2 * n_e * kn_e * VT ** 2
def ekv_id(vov):
    return ispec_e * math.log1p(math.exp(vov / (2 * n_e * VT))) ** 2
for key, I in (("Lab 10-07.i", 1e-5), ("Lab 10-07.j", 5e-4), ("Lab 10-07.k", 1e-2)):
    vq = brentq(lambda x: ekv_id(x) - I, -1.0, 2.0, xtol=1e-14)
    gmid = (math.log(ekv_id(vq + 1e-6)) - math.log(ekv_id(vq - 1e-6))) / 2e-6
    v.check(key, (1 / VT) / gmid)


# ------------------------------------------------------------------ Example 8: bypass capacitor (complex nodal solve)
gm8, rpi8, _ = hp(IC1, 100)
re8 = (100 / 101) / gm8
v.check("Ex 10-07.8a", re8)
v.check("Ex 10-07.8b", par(1e3, RB) / 101)
# resistance seen by C_E: test source at the emitter with the signal source zeroed (MNA)
cth = MNA(); cth.V("e", "0", 1.0); cth.R("s", "0", 1e3); cth.R("s", "b", 1e-9); cth.R("b", "0", RB)
bjt(cth, None, "c", "b", "e", gm8, rpi8); cth.R("c", "0", par(4.7e3, 10e3)); cth.R("e", "0", 1e3)
rth8 = 1 / -cth.solve()["_i"][0]
v.check("Ex 10-07.8c", rth8)
v.check("Ex 10-07.8d", 1 / (2 * math.pi * 20 * rth8) * 1e6)
v.check("Ex 10-07.8e", 1 / (2 * math.pi * 330e-6 * rth8))
v.check("Ex 10-07.8f", 1 / (2 * math.pi * 330e-6 * 1e3))


def ce_gain_f(f, ce=330e-6):
    """Complex gain v_c/v_s of Example 10-07.1's stage with R_E = 1 kOhm || C_E, coupling capacitors shorted."""
    w = 2 * math.pi * f
    ye = 1 / 1e3 + 1j * w * ce
    # unknowns v_b, v_e, v_c; source 1 V through 1 kOhm into the base node
    Y = np.array([[1 / 1e3 + 1 / RB + 1 / rpi8, -1 / rpi8, 0],
                  [-1 / rpi8 - gm8, 1 / rpi8 + gm8 + ye, 0],
                  [gm8, -gm8, 1 / 4.7e3 + 1 / 10e3]], dtype=complex)
    b = np.array([1 / 1e3, 0, 0], dtype=complex)
    vb, ve, vc = np.linalg.solve(Y, b)
    return vc


amid = abs(ce_gain_f(1e6))
v.assert_true("midband gain equals Example 10-07.1's overall gain", abs(amid - abs(x1["c"])) < 1e-3)
v.check("Ex 10-07.8g", brentq(lambda f: abs(ce_gain_f(f)) - amid / math.sqrt(2), 1.0, 1e3, xtol=1e-9))
rcoup = 1e3 + par(RB, rpi8)
v.check("Ex 10-07.8h", 1 / (2 * math.pi * 20 * rcoup) * 1e6)
v.check("Ex 10-07.8i", 1 / (2 * math.pi * 10e-6 * rcoup))
v.check("Ex 10-07.8j", rcoup / rth8)
v.check("Ex 10-07.8k", (1 / (2 * math.pi * 330e-6 * rth8)) / (1 / (2 * math.pi * 330e-6 * 1e3)))


# ------------------------------------------------------------------ Problem 13: partial bypass (test source, MNA)
cth2 = MNA(); cth2.V("x", "0", 1.0); cth2.R("x", "0", 900.0); cth2.R("x", "e", 100.0)
cth2.R("s", "0", 1e3); cth2.R("s", "b", 1e-9); cth2.R("b", "0", RB)
bjt(cth2, None, "c", "b", "e", gm8, rpi8); cth2.R("c", "0", par(4.7e3, 10e3))
rth13 = 1 / -cth2.solve()["_i"][0]
v.check("10-07.13a", rth13)
c13 = 1 / (2 * math.pi * 20 * rth13)
v.check("10-07.13b", c13 * 1e6)
e6 = [10e-6, 15e-6, 22e-6, 33e-6, 47e-6, 68e-6, 100e-6, 150e-6]
pick = min(c for c in e6 if 1 / (2 * math.pi * c * rth13) <= 20)
v.check("10-07.13c", pick * 1e6)
v.check("10-07.13d", 1 / (2 * math.pi * pick * rth13))
v.check("10-07.13e", rth13 / rth8)
v.check("10-07.13f", 1 / (2 * math.pi * 68e-6 * rth13))

# ------------------------------------------------------------------ Problem 14: full discrete design (KVL solve, then MNA)
A14 = np.array([[1 / 56e3 + 1 / 12e3, 0.0, 1.0], [0.0, 1 / 1.2e3, -151.0], [1.0, -1.0, 0.0]])
z14 = np.array([9 / 56e3, 0.0, 0.7])
vb14, ve14, ib14 = np.linalg.solve(A14, z14)
v.check("10-07.14a", 9 * 12 / 68)
v.check("10-07.14b", par(56e3, 12e3) / 1e3)
v.check("10-07.14c", ve14 / 1.2e3 * 1e3)
ic14 = 150 * ib14
v.check("10-07.14d", ic14 * 1e3)
v.check("10-07.14e", 9 - ic14 * 3.3e3)
v.check("10-07.14f", ve14)
v.check("10-07.14g", 9 - ic14 * 3.3e3 - ve14)
gm14, rpi14, ro14 = hp(ic14, 150, 100)
v.check("10-07.14h", gm14 * 1e3)
v.check("10-07.14i", rpi14 / 1e3)
v.check("10-07.14j", ro14 / 1e3)
c14 = MNA(); c14.V("s", "0", 1.0); c14.R("s", "b", 600.0); c14.R("b", "0", par(56e3, 12e3))
bjt(c14, None, "c", "b", "0", gm14, rpi14, ro14); c14.R("c", "0", 3.3e3); c14.R("c", "0", 10e3)
x14 = c14.solve()
v.check("10-07.14k", par(par(56e3, 12e3), rpi14) / 1e3)
v.check("10-07.14l", x14["c"] / x14["b"])
v.check("10-07.14m", x14["b"])
v.check("10-07.14n", x14["c"])
v.check("10-07.14o", (1 - x14["b"]) * 100)

# ------------------------------------------------------------------ Problem 15: CB input resistance with r_o (MNA)
for key, rc in (("10-07.15a", 1e-6), ("10-07.15b", 5e3), ("10-07.15c", 50e3)):
    c15 = MNA(); c15.V("x", "0", 1.0); bjt(c15, None, "c", "0", "x", gm3, rpi3, ro3); c15.R("c", "0", rc)
    v.check(key, 1 / -c15.solve()["_i"][0])
c15 = MNA(); c15.V("x", "0", 1.0); bjt(c15, None, "c", "0", "x", gm3, rpi3, ro3); c15.R("c", "0", 1e15)
v.check("10-07.15d", 1 / -c15.solve()["_i"][0] / 1e3)

v.finish()
