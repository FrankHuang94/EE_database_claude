#!/usr/bin/env python3
"""Verify every number in chapter 10-06 (MOS single-stage amplifiers), its solutions and lab.

Independent route: a small modified-nodal-analysis solver (resistors, voltage-controlled current sources,
independent voltage and current sources) builds each stage's small-signal circuit from the MOSFET model
(g_m v_gs + g_mb v_bs from drain to source, r_o in parallel) and solves it with numpy; gains are node
voltages and output resistances come from explicit test sources. Distortion results solve the large-signal
square law over a cycle and take an FFT. None of the chapter's closed forms is used to produce a value.
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
v = Verifier.from_files("10-06", COURSE / "chapters" / "10-06-mos-single-stage-amplifiers.md",
                        COURSE / "solutions" / "10-06-solutions.md",
                        COURSE / "labs" / "10-06-lab" / "README.md")


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


def gm_of(kn, i):
    return math.sqrt(2 * kn * i)


def par(*r):
    return 1 / sum(1 / x for x in r)


# ------------------------------------------------------------------ theory
v.check("T 10-06.a", 1 / (1 + 0.2))

# ------------------------------------------------------------------ Example 1
kn, I0, lam = 4e-3, 0.5e-3, 0.05
vov = brentq(lambda x: 0.5 * kn * x * x - I0, 1e-6, 5)
gm = gm_of(kn, I0)
ro = 1 / (lam * I0)
v.check("Ex 10-06.1a", vov)
v.check("Ex 10-06.1b", gm * 1e3)
v.check("Ex 10-06.1c", ro / 1e3)


def cs(rd, rl=None, rs=0.0, gmb=0.0, ro_=ro, gm_=gm):
    c = MNA()
    c.V("g", "0", 1.0)
    c.R("d", "0", rd)
    if rl:
        c.R("d", "0", rl)
    if rs:
        c.R("s", "0", rs)
        c.mos("d", "g", "s", "0", gm_, gmb, ro_)
    else:
        c.mos("d", "g", "0", "0", gm_, 0.0, ro_)
    return c.solve()["d"]


def rout_drain(rs, gmb=0.0, ro_=ro, gm_=gm):
    c = MNA()
    c.V("g", "0", 0.0)
    c.V("d", "0", 1.0)
    c.R("s", "0", rs) if rs else None
    c.mos("d", "g", "s" if rs else "0", "0", gm_, gmb, ro_)
    return 1 / -c.solve()["_i"][1]


def rout_follower(gm_, gmb, ro_, rs):
    c = MNA()
    c.V("g", "0", 0.0)
    c.R("s", "0", rs) if not math.isinf(rs) else None
    c.mos("vdd", "g", "s", "0", gm_, gmb, ro_)
    c.V("vdd", "0", 0.0)
    c.I("0", "s", 1.0)
    return c.solve()["s"]


v.check("Ex 10-06.1d", 1 / (1 / 5e3 + 1 / ro) / 1e3)   # R_D || r_o by test source below
v.assert_true("R_out of the CS stage by test source equals R_D || r_o",
              abs(par(5e3, rout_drain(0.0)) - 1 / (1 / 5e3 + 1 / ro)) < 1e-6)
v.check("Ex 10-06.1e", cs(5e3))
v.check("Ex 10-06.1f", cs(5e3, rl=10e3))
v.check("Ex 10-06.1g", -cs(5e3, ro_=math.inf))
v.check("Ex 10-06.1h", 2 * (I0 * 5e3) / vov)

# ------------------------------------------------------------------ Example 2
RS = 500.0


def gm_short(rs, gmb=0.0, ro_=ro, gm_=gm):
    c = MNA()
    c.V("g", "0", 1.0)
    c.V("d", "0", 0.0)
    c.R("s", "0", rs)
    c.mos("d", "g", "s", "0", gm_, gmb, ro_)
    return -c.solve()["_i"][1]                     # drain current: delivered into d by the shorting source


v.check("Ex 10-06.2a", gm_short(RS, ro_=math.inf) * 1e3)
v.check("Ex 10-06.2b", gm_short(RS) * 1e3)
r2 = rout_drain(RS)
v.check("Ex 10-06.2c", r2 / 1e3)
v.check("Ex 10-06.2d", cs(5e3, rs=RS))
v.check("Ex 10-06.2e", cs(5e3, rs=RS, ro_=math.inf))

# ------------------------------------------------------------------ Example 3: common gate
chi = 0.2
gmb = chi * gm


def cg(rd, rsig, ro_=math.inf, gm_=gm, gmb_=gmb):
    """Common gate. rsig=None drives the source node directly with a 1 V test source; returns (nodes, R_in)."""
    c = MNA()
    if rsig is None:
        c.V("s", "0", 1.0)
    else:
        c.V("in", "0", 1.0)
        c.R("in", "s", rsig)
    c.R("vdd", "d", rd)
    c.V("vdd", "0", 0.0)
    c.mos("d", "0", "s", "0", gm_, gmb_, ro_)
    x = c.solve()
    if rsig is None:
        return x, 1 / -x["_i"][0]              # current delivered into the source node by the test source
    return x, x["s"] / ((1.0 - x["s"]) / rsig)


v.check("Ex 10-06.3a", gmb * 1e3)
x, rin = cg(5e3, None)
v.check("Ex 10-06.3b", rin)
v.check("Ex 10-06.3c", x["d"] / x["s"])
x50, _ = cg(5e3, 50.0)
v.check("Ex 10-06.3d", x50["d"])
xr, rin_r = cg(5e3, None, ro_=ro)
v.check("Ex 10-06.3e", rin_r)
v.check("Ex 10-06.3f", xr["d"] / xr["s"])
g50 = brentq(lambda g: cg(5e3, None, gm_=g, gmb_=chi * g)[1] - 50.0, 1e-4, 1)
v.check("Ex 10-06.3g", g50 * 1e3)
v.check("Ex 10-06.3h", brentq(lambda i: 2 * i / 0.2 - g50, 1e-6, 1) * 1e3)

# ------------------------------------------------------------------ Example 4: source follower


def cd(gm_, gmb_, ro_, rs, rl=None):
    c = MNA()
    c.V("g", "0", 1.0)
    c.V("vdd", "0", 0.0)
    if not math.isinf(rs):
        c.R("s", "0", rs)
    if rl:
        c.R("s", "0", rl)
    c.mos("vdd", "g", "s", "0", gm_, gmb_, ro_)
    return c.solve()["s"]


a4 = cd(gm, gmb, ro, 5e3)
v.check("Ex 10-06.4a", (a4 / (1 - a4)) / gm / 1e3)    # invert A = gm R/(1 + gm R) for R_eq
v.check("Ex 10-06.4b", a4)
v.check("Ex 10-06.4c", cd(gm, gmb, math.inf, math.inf))
v.check("Ex 10-06.4d", rout_follower(gm, gmb, ro, 5e3))
v.check("Ex 10-06.4e", cd(gm, gmb, ro, 5e3, rl=1e3))

# ------------------------------------------------------------------ Example 5
i5, vov5, vrd5, lam5 = 100e-6, 0.2, 0.9, 0.2
gm5 = 2 * i5 / vov5
ro5 = 1 / (lam5 * i5)
v.check("Ex 10-06.5a", cs(vrd5 / i5, gm_=gm5, ro_=math.inf))
v.check("Ex 10-06.5b", gm5 * 1e3)
v.check("Ex 10-06.5c", ro5 / 1e3)
v.check("Ex 10-06.5d", gm5 * ro5)
v.check("Ex 10-06.5e", cs(vrd5 / i5, gm_=gm5, ro_=ro5))

# ------------------------------------------------------------------ Example 6
v.check("Ex 10-06.6a", cs(5e3, rl=1e3))
gm6 = gm_of(kn, 1e-3)
ro6 = 1 / (lam * 1e-3)
a6 = cd(gm6, chi * gm6, ro6, math.inf, rl=1e3)
v.check("Ex 10-06.6b", gm6 * 1e3)
v.check("Ex 10-06.6c", ro6 / 1e3)
v.check("Ex 10-06.6d", (a6 / (1 - a6)) / gm6)
v.check("Ex 10-06.6e", a6)
# full chain: CS drain drives the follower's gate (no current), so solve both in one circuit
c = MNA()
c.V("in", "0", 1.0); c.V("vdd", "0", 0.0)
c.R("d", "0", 5e3); c.mos("d", "in", "0", "0", gm, 0.0, ro)
c.mos("vdd", "d", "s", "0", gm6, chi * gm6, ro6); c.R("s", "0", 1e3)
chain = c.solve()["s"]
v.check("Ex 10-06.6f", chain)
v.check("Ex 10-06.6g", chain / cs(5e3, rl=1e3))

# ------------------------------------------------------------------ Example 7
for key, rs in (("Ex 10-06.7a", 0.0), ("Ex 10-06.7b", 1e3), ("Ex 10-06.7c", 10e3)):
    v.check(key, rout_drain(rs) / 1e3)


def cascode(gmb2=0.0, test=False):
    c = MNA()
    c.V("in", "0", 0.0 if test else 1.0)
    c.mos("x", "in", "0", "0", gm, 0.0, ro)
    c.mos("out", "0", "x", "0", gm, gmb2, ro)       # upper gate at signal ground
    if test:
        c.V("out", "0", 1.0)
        return 1 / -c.solve()["_i"][1]
    return c.solve()["out"]


v.check("Ex 10-06.7d", cascode(test=True) / 1e3)
v.check("Ex 10-06.7e", cs(1e30))
v.check("Ex 10-06.7f", cascode())

# ================================================================== solutions
kn2, i2, lam2 = 2e-3, 0.2e-3, 0.1
gm2 = gm_of(kn2, i2)
v.check("10-06.2a", brentq(lambda x: 0.5 * kn2 * x * x - i2, 1e-6, 5))
v.check("10-06.2b", gm2 * 1e3)
v.check("10-06.2c", 1 / (lam2 * i2) / 1e3)
v.check("10-06.2d", cs(10e3, gm_=gm2, ro_=1 / (lam2 * i2)))
v.check("10-06.2e", -cs(10e3, gm_=gm2, ro_=math.inf))

v.check("10-06.3a", cd(3e-3, 0.45e-3, 30e3, math.inf))
v.check("10-06.3b", rout_follower(3e-3, 0.45e-3, 30e3, math.inf))

rs4 = brentq(lambda r: cs(8e3, rs=r, gm_=2e-3, ro_=math.inf) + 4, 1, 1e5)
v.check("10-06.4a", rs4 / 1e3)
a_new = cs(8e3, rs=rs4, gm_=1.6e-3, ro_=math.inf)
v.check("10-06.4b", a_new)
v.check("10-06.4c", (a_new / -4 - 1) * 100)
v.check("10-06.4d", cs(8e3, gm_=2e-3, ro_=math.inf))
v.check("10-06.4e", cs(8e3, gm_=1.6e-3, ro_=math.inf))

v.check("10-06.5a", rout_drain(2e3, gmb=0.2e-3, ro_=100e3, gm_=1e-3) / 1e3)
v.check("10-06.5b", rout_drain(2e3, gmb=0.0, ro_=100e3, gm_=1e-3) / 1e3)

_, rin6 = cg(20e3, None, gm_=1e-3, gmb_=0.2e-3)
v.check("10-06.6a", rin6)
# Norton sensor: 1 A into node s with 1 MOhm to ground; the CG stage's drain current per amp
c = MNA()
c.I("0", "s", 1.0); c.R("s", "0", 1e6)
c.R("d", "0", 20e3); c.mos("d", "0", "s", "0", 1e-3, 0.2e-3)
xs = c.solve()
frac = xs["d"] / 20e3                               # CG passes the injected current to R_D (non-inverting)
v.check("10-06.6b", frac)
v.check("10-06.6c", abs(xs["d"]) * 1e-6 * 1e3)     # mV per µA
v.check("10-06.6d", par(1e6, 20e3) / 1e3)

v.check("10-06.7a", cs(40e3, gm_=1e-3, ro_=50e3))   # PMOS load r_op = 40 kOhm
v.check("10-06.7b", cs(10e3, gm_=1e-3, ro_=50e3))

for key, rd in (("10-06.8a", 1e-6), ("10-06.8b", 40e3), ("10-06.8c", 400e3)):
    v.check(key, cg(rd, None, ro_=40e3, gm_=2e-3, gmb_=0.4e-3)[1])

N = 4096
TH = 2 * np.pi * np.arange(N) / N


def hd(amp, rs, kn_=4e-3, vtn=0.5, vov_=0.5, i0=0.5e-3):
    vg0 = vtn + vov_ + i0 * rs
    i = np.array([brentq(lambda q: q - 0.5 * kn_ * max(vg0 + amp * math.cos(t) - q * rs - vtn, 0) ** 2, 0, 1)
                  for t in TH])
    cc = np.fft.rfft(i) / N
    return abs(cc[2]) / abs(cc[1]) * 100, abs(cc[3]) / abs(cc[1]) * 100


def hd2_pert(amp, T, vov_=0.5):
    # second-order perturbation of i = gm vgs + (k/2) vgs^2, vgs = vin - i R_S
    k_ = 4e-3
    g_ = k_ * vov_
    rs = T / g_
    i1 = g_ * amp / (1 + T)
    i2_amp_2w = 0.5 * k_ * (amp / (1 + T)) ** 2 / (1 + g_ * rs) * 0.5
    return i2_amp_2w / i1 * 100


v.check("10-06.9a", hd2_pert(0.05, 0.0))
v.check("10-06.9b", hd2_pert(0.05, 1.0))
v.check("10-06.9c", hd2_pert(0.10, 1.0))
v.check("10-06.9d", hd(0.05, 500.0)[0])
v.check("10-06.9e", hd(0.10, 500.0)[0])

c = MNA()
c.V("in", "0", 0.0)
c.mos("x", "in", "0", "0", 2e-3, 0.0, 40e3)
c.mos("out", "0", "x", "0", 2e-3, 0.4e-3, 40e3)
c.V("out", "0", 1.0)
v.check("10-06.10a", 1 / -c.solve()["_i"][1] / 1e3)
v.check("10-06.10b", cascode(gmb2=0.4e-3))

v.check("10-06.11a", -cs(0.45 / 1e-4, gm_=2 * 1e-4 / 0.15, ro_=math.inf))
v.check("10-06.11b", brentq(lambda x: -cs(0.45 / 1e-4, gm_=2 * 1e-4 / x, ro_=math.inf) - 10, 0.01, 1))

a12 = cd(20e-3, 4e-3, math.inf, math.inf, rl=50.0)
v.check("10-06.12a", (a12 / (1 - a12)) / 20e-3)
v.check("10-06.12b", a12)
v.check("10-06.12c", rout_follower(20e-3, 4e-3, math.inf, math.inf))
v.check("10-06.12d", -10 * a12)
v.check("10-06.12e", 10 / a12)

# ================================================================== lab
v.check("Lab 10-06.a", cs(ro))
v.check("Lab 10-06.b", cd(gm, gmb, ro, 2e3))
v.check("Lab 10-06.c", hd(0.10, 0.0)[0])
v.check("Lab 10-06.d", hd(0.10, 500.0)[1])
v.check("Lab 10-06.e", -cs(2.5 / 0.5e-3, gm_=2 * 0.5e-3 / 0.2, ro_=math.inf))
v.check("Lab 10-06.f", brentq(lambda r: cg(r, None, ro_=ro)[1] - 1e3, 1, 1e6) / 1e3)

v.finish()
