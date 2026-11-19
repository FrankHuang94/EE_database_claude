#!/usr/bin/env python3
"""Verify every number in chapter 10-08 (current sources and current mirrors), its solutions and lab.

Independent routes:
- MOS mirror currents from the large-signal square law with channel-length modulation, solved node by node;
- bipolar mirror currents (basic, scaled, beta helper, Wilson) from exponential transistors with base currents,
  solved as nonlinear Kirchhoff systems (scipy.optimize.fsolve), not from the chapter's ratio formulas;
- output resistances by test-source simulation of the small-signal circuits (modified nodal analysis);
- mismatch by Monte Carlo sampling of threshold (and resistor) differences, checked against the formulas.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("10-08", COURSE / "chapters" / "10-08-current-sources-and-mirrors.md",
                        COURSE / "solutions" / "10-08-solutions.md",
                        COURSE / "labs" / "10-08-lab" / "README.md")
VT = 1.380649e-23 * 300 / 1.602176634e-19


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


K, VTN = 4e-3, 0.5


def ids(vgs, vds, lam, k=K, vtn=VTN):
    vov = vgs - vtn
    if vov <= 0:
        return 0.0
    if vds < vov:
        return k * (vov - vds / 2) * vds * (1 + lam * vds)
    return 0.5 * k * vov * vov * (1 + lam * vds)


def mos_ss(c, d, g, s, gm, ro, gmb=0.0):
    c.G(d, s, g, s, gm)
    if gmb:
        c.G(d, s, "0", s, gmb)       # body at ground
    c.R(d, s, ro)


# ------------------------------------------------------------------ theory
v.check("T 10-08.a", ids(1.0, 1.0, 0.0, k=4 * K) / ids(1.0, 1.0, 0.0))

# ------------------------------------------------------------------ Example 1
lam = 0.1
vgs = brentq(lambda x: (3.3 - x) / 10e3 - ids(x, x, lam), 0.5, 3.3)
iref = (3.3 - vgs) / 10e3
v.check("Ex 10-08.1a", vgs - VTN)
v.check("Ex 10-08.1b", ids(vgs, 2.0, lam) * 1e3)
v.check("Ex 10-08.1c", (ids(vgs, 0.5, lam) / iref - 1) * 100)
v.check("Ex 10-08.1d", (ids(vgs, 3.0, lam) / iref - 1) * 100)
h = 1e-4
v.check("Ex 10-08.1e", 2 * h / (ids(vgs, 2.0 + h, lam) - ids(vgs, 2.0 - h, lam)) / 1e3)
v.check("Ex 10-08.1f", 1 / (lam * iref) / 1e3)
v.check("Ex 10-08.1g", ids(vgs, vgs, lam, k=4 * K) * 1e3)

# ------------------------------------------------------------------ Example 2: bipolar mirrors by Kirchhoff's laws
# Matched transistors share V_BE, so each carries X(1 + V_CE/V_A) of collector current with X = I_S e^(V_BE/V_T)
# common to the pair, and base current X/beta (beta defined without the Early factor). V_BE = 0.7 V sets V_CE1.


def mirror_basic(iref_, beta, vce2, va=50.0, area2=1.0, vbe=0.7):
    # node at Q1's collector/bases: I_ref = X(1 + V_BE/V_A) + X/beta + area2 X/beta
    x = brentq(lambda q: q * (1 + vbe / va) + q / beta + area2 * q / beta - iref_, 0, 1)
    return area2 * x * (1 + vce2 / va)


def mirror_helper(iref_, beta, vce2, va=50.0, vbe=0.7):
    # Q3 supplies both bases (2X/beta) from its emitter; its own base current is that over (beta + 1); V_CE1 = 2 V_BE
    x = brentq(lambda q: q * (1 + 2 * vbe / va) + (2 * q / beta) / (beta + 1) - iref_, 0, 1)
    return x * (1 + vce2 / va)


io = mirror_basic(1e-3, 100, 5.0)
v.check("Ex 10-08.2a", io * 1e3)
v.check("Ex 10-08.2b", (io / 1e-3 - 1) * 100)
ioh = mirror_helper(1e-3, 100, 5.0)
v.check("Ex 10-08.2c", ioh * 1e3)
v.check("Ex 10-08.2d", (ioh / 1e-3 - 1) * 100)
v.check("Ex 10-08.2e", mirror_basic(1e-3, 100, 0.0, va=1e15) * 1e3)
v.check("Ex 10-08.2f", mirror_helper(1e-3, 100, 0.0, va=1e15) * 1e3)
v.check("Ex 10-08.2g", 50.0 / 1e-3 / 1e3)

# ------------------------------------------------------------------ Example 3: degenerated mirror by test source
gm = math.sqrt(2 * K * iref)
ro = 1 / (lam * iref)


def rout_degen(rs, gm_=gm, ro_=ro):
    c = MNA(); c.V("d", "0", 1.0); c.V("g", "0", 0.0); c.R("s", "0", rs); mos_ss(c, "d", "g", "s", gm_, ro_)
    return 1 / -c.solve()["_i"][0]


v.check("Ex 10-08.3a", gm * 1e3)
v.check("Ex 10-08.3b", ro / 1e3)
v.check("Ex 10-08.3c", rout_degen(1e3) / 1e3)
v.check("Ex 10-08.3d", iref * 1e3)


def rout_cascode(gm_, ro_, gmb=0.0):
    c = MNA(); c.V("out", "0", 1.0); c.V("g", "0", 0.0)
    mos_ss(c, "x", "g", "0", gm_, ro_)                 # lower device, gate at signal ground
    mos_ss(c, "out", "g", "x", gm_, ro_, gmb)          # upper device, gate at signal ground
    return 1 / -c.solve()["_i"][0]


rc = rout_cascode(gm, ro)
v.check("Ex 10-08.4a", rc / 1e3)
v.check("Ex 10-08.4b", gm * ro * ro / 1e3)
v.check("Ex 10-08.4c", VTN + 2 * (vgs - VTN))
v.check("Ex 10-08.4d", 2 * (vgs - VTN))
v.check("Ex 10-08.4e", 2.0 / rc * 1e6)
v.check("Ex 10-08.4f", 2.0 / rc / iref * 100)
v.check("Ex 10-08.4g", 2.0 / ro / iref * 100)


def wilson(iref_, beta):
    """Q1 and Q2 share V_BE (collector current X each), Q3 carries Y; no Early effect. Linear in (X, Y):
    Q3's emitter current Y(1 + 1/beta) feeds Q2's collector and both bases, X(1 + 2/beta);
    the reference feeds Q1's collector and Q3's base, X + Y/beta."""
    a = np.array([[-(1 + 2 / beta), 1 + 1 / beta], [1.0, 1 / beta]])
    x, y = np.linalg.solve(a, [0.0, iref_])
    return y


v.check("Ex 10-08.5a", (1 - wilson(1e-3, 100) / 1e-3) * 100)
v.check("Ex 10-08.5b", 100 * 50e3 / 2 / 1e6)
v.check("Ex 10-08.5c", 2 / 100 * 100)                   # first-order base-current error 2/beta

# ------------------------------------------------------------------ Example 6: mismatch
AVT = 3.5   # mV um, illustrative
s10 = AVT / math.sqrt(10)
rng = np.random.default_rng(81)
mc = (2 / 0.2) * rng.normal(0, s10 * 1e-3, 400000)
v.assert_true("Monte Carlo sigma of the ratio matches (2/V_ov) sigma(dV_TH)",
              abs(mc.std() * 100 / ((2 / 0.2) * s10 * 1e-3 * 100) - 1) < 0.01)
v.check("Ex 10-08.6a", s10)
v.check("Ex 10-08.6b", (2 / 0.2) * s10 * 1e-3 * 100)
v.check("Ex 10-08.6c", (2 / 0.4) * s10 * 1e-3 * 100)
need = 0.001 / (2 / 0.2) * 1e3
v.check("Ex 10-08.6d", need)
v.check("Ex 10-08.6e", brentq(lambda a: AVT / math.sqrt(a) - need, 1, 1e6))
v.check("Ex 10-08.6f", 0.2e-3 / VT * 100)

# ------------------------------------------------------------------ Example 7
v7 = brentq(lambda x: 0.5 * K * (x - VTN) ** 2 - 100e-6, 0.5, 3)
R7 = (3.3 - v7) / 100e-6
v.check("Ex 10-08.7a", v7)
v.check("Ex 10-08.7b", R7 / 1e3)
R7r = 25.76e3


def iref7(vdd):
    x = brentq(lambda q: (vdd - q) / R7r - 0.5 * K * (q - VTN) ** 2, 0.5, vdd)
    return (vdd - x) / R7r


v.check("Ex 10-08.7c", sum(r * ids(v7, 1.0, 0.0) for r in (1, 2, 4, 0.5)) * 1e6)
v.check("Ex 10-08.7d", (iref7(3.3) * (1 + 7.5)) * 3.3 * 1e3)
v.check("Ex 10-08.7e", (iref7(3.4) / iref7(3.3) - 1) * 100)
v.check("Ex 10-08.7f", 0.1 / (3.3 - v7) * 100)

# ================================================================== solutions
v.check("10-08.1a", ids(1.0, 1.0, 0.0, k=30 / 10 * K) / ids(1.0, 1.0, 0.0) * 50)
v.check("10-08.1b", 2 * 150)
vov, vth = 0.25, 0.45
v.check("10-08.2a", vov)
v.check("10-08.2b", vth + 2 * vov)
v.check("10-08.2c", 2 * vov)
v.check("10-08.2d", 1.2 - vov - vov)
v.check("10-08.2e", max(0.0, 1.2 - (vth + 2 * vov) - vov))
v.check("10-08.3a", mirror_basic(1e-3, 80, 0.0, va=1e15, area2=3.0) * 1e3)
lam2 = 0.1 * 0.5 / 2
v.check("10-08.4a", lam2)
def sat(lam_, vds):
    return 0.5 * K * 0.04 * (1 + lam_ * vds)


v.check("10-08.4b", (sat(0.1, 1.0) / sat(0.1, 0.0) - 1) * 100)      # first-order error for a 1 V difference
v.check("10-08.4c", (sat(lam2, 1.0) / sat(lam2, 0.0) - 1) * 100)
w_scale = brentq(lambda w: (w / 4.0) - 1.0, 0.1, 100)                 # k_n ~ W/L with L x4 needs W x4
v.check("10-08.4d", w_scale * 4.0)
rs5 = brentq(lambda r: rout_degen(r, 1e-3, 100e3) - 1e6, 1, 1e6)
v.check("10-08.5a", rs5 / 1e3)
v.check("10-08.5b", 100e-6 * rs5)
v.check("10-08.5c", 1e-3 * 100e3 ** 2 / 1e6)
v.check("10-08.6a", rout_cascode(1e-3, 100e3, gmb=0.2e-3) / 1e6)
io7 = mirror_basic(200e-6, 40, 0.0, va=1e15)
v.check("10-08.7a", io7 * 1e6)
v.check("10-08.7b", (io7 / 200e-6 - 1) * 100)
io7h = mirror_helper(200e-6, 40, 0.0, va=1e15)
v.check("10-08.7c", io7h * 1e6)
v.check("10-08.7d", (io7h / 200e-6 - 1) * 100)
s4 = AVT / math.sqrt(4)
v.check("10-08.8a", s4)
v.check("10-08.8b", (2 / 0.15) * s4 * 1e-3 * 100)
v.check("10-08.8c", 3 * (2 / 0.15) * s4 * 1e-3 * 100)
need8 = (0.01 / 3) * 0.15 / 2 * 1e3
v.check("10-08.8d", need8)
v.check("10-08.8e", brentq(lambda a: AVT / math.sqrt(a) - need8, 1, 1e6))


def degen_mc(n=400000, seed=89):
    """Mirror with R_S: solve the linearized output-current error for sampled dV_TH and dR (g_m = 1 mS, 100 uA)."""
    r = np.random.default_rng(seed)
    dvt = r.normal(0, s10 * 1e-3, n)
    dr = r.normal(0, 0.001, n)
    g, rs, i0 = 1e-3, 2e3, 100e-6
    # dI = g(-dVT - I0 rs dR - dI rs)  ->  dI = -g(dVT + I0 rs dR)/(1 + g rs)
    return (-g * (dvt + i0 * rs * dr) / (1 + g * rs)) / i0, (-g * dvt / (1 + g * rs)) / i0, (-g * i0 * rs * dr / (1 + g * rs)) / i0


tot, tpart, rpart = degen_mc()
v.check("10-08.9a", (2 / 0.2) * s10 * 1e-3 * 100)
v.check("10-08.9b", (2 / 0.2) * s10 * 1e-3 * 100 / 3)
v.check("10-08.9c", 2 / 3 * 0.1)
v.check("10-08.9d", math.hypot((2 / 0.2) * s10 * 1e-3 * 100 / 3, 2 / 3 * 0.1))
v.assert_true("Monte Carlo of the degenerated mirror agrees with the RSS total",
              abs(tot.std() * 100 / math.hypot(tpart.std() * 100, rpart.std() * 100) - 1) < 0.01)
v.check("10-08.10a", (1 - wilson(1e-3, 50) / 1e-3) * 100)
v.check("10-08.11a", 9 * 20)
v.check("10-08.11b", 9 * 20e-6 * 1.2 * 1e3)
vg11 = VTN + 0.2
dlnI = (math.log(ids(vg11 + 1e-6, 1.0, 0.0)) - math.log(ids(vg11 - 1e-6, 1.0, 0.0))) / 2e-6
v.check("10-08.11c", dlnI * 5e-3 * 100)                                # first order in the 5 mV shift
v.check("10-08.12a", 1 / (1.8 - 0.7) * 100)
v.check("10-08.12b", 0.09 / (1.8 - 0.7) * 100)

# ================================================================== lab


def casc_ls(vout):
    vg3 = vgs + brentq(lambda q: iref - ids(q, q, lam), 0.5, 3.3)
    vx = brentq(lambda x: ids(vgs, x, lam) - ids(vg3 - x, vout - x, lam), 0.0, vout)
    return ids(vgs, vx, lam)


v.check("Lab 10-08.a", 2e-3 / (casc_ls(2.001) - casc_ls(1.999)) / 1e3)
v.check("Lab 10-08.b", brentq(lambda q: casc_ls(q) - 0.99 * iref, 0.4, 2.0))
rng = np.random.default_rng(1008)
err = (2 / 0.2) * rng.normal(0.0, s10 * 1e-3, 10000)
v.check("Lab 10-08.c", np.mean(np.abs(err) > 0.02) * 100)
v.check("Lab 10-08.d", 2 * norm.sf(0.02 / ((2 / 0.2) * s10 * 1e-3)) * 100)
v.check("Lab 10-08.e", (mirror_basic(1e-3, 20, 0.0, va=1e15) / 1e-3 - 1) * 100)
v.check("Lab 10-08.f", (mirror_helper(1e-3, 20, 0.0, va=1e15) / 1e-3 - 1) * 100)
v.check("Lab 10-08.g", (wilson(1e-3, 20) / 1e-3 - 1) * 100)
v.check("Lab 10-08.h", (iref7(3.3001) - iref7(3.2999)) / 2e-4 / iref7(3.3) * 100)

v.finish()
