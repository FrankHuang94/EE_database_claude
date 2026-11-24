#!/usr/bin/env python3
"""Verify every number in chapter 21-04 (low-noise amplifiers), its problems and its lab.

Independent routes (the lab module lna.py uses the chapter's closed forms and its own loop solver):
- every noise figure is computed by a small modified-nodal-analysis (MNA) solver written here: each noise
  source (source resistance, channel noise, gate-inductor loss, load resistors) is injected as a current and
  its transfer to the output is solved with numpy, so the halving of the drain noise and the cancellation in
  the wideband LNA are outcomes, not inputs;
- matched element values are found by root-finding on Z_in(f0) = R_s from the MNA input impedance, not from
  w_T L_s = R_s;
- band edges, gate-inductor Q targets and the optimum R1 come from brentq/minimize_scalar on the MNA results;
- ngspice confirms four noise figures and the 50 ohm input (lna_noise.cir, run by run_spice).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "21-04-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import lna as lab  # noqa: E402

v = Verifier.from_files("21-04", ROOT / "chapters" / "21-04-low-noise-amplifiers.md",
                        ROOT / "solutions" / "21-04-solutions.md", LAB / "README.md")
KB, T0, RS = 1.380649e-23, 290.0, 50.0
lg = math.log10
db = lambda x: 10 * lg(x)  # noqa: E731


class Mna:
    """Nodal analysis with admittances, voltage-controlled current sources and current injections."""

    def __init__(self, nodes):
        self.idx = {n: k for k, n in enumerate(nodes)}
        self.y = np.zeros((len(nodes), len(nodes)), dtype=complex)

    def _i(self, n):
        return None if n == "0" else self.idx[n]

    def adm(self, a, b, y):
        for p, q, s in ((a, a, 1), (b, b, 1), (a, b, -1), (b, a, -1)):
            ip, iq = self._i(p), self._i(q)
            if ip is not None and iq is not None:
                self.y[ip, iq] += s * y

    def vccs(self, g, out_from, out_to, cp, cn):
        """Current g (v_cp - v_cn) leaves node out_from and enters node out_to."""
        for o, so in ((out_from, 1), (out_to, -1)):
            io = self._i(o)
            if io is None:
                continue
            for c, sc in ((cp, 1), (cn, -1)):
                ic = self._i(c)
                if ic is not None:
                    self.y[io, ic] += so * sc * g

    def solve(self, inject):
        """inject: {node: current into the node}; returns node voltages."""
        b = np.zeros(len(self.idx), dtype=complex)
        for n, val in inject.items():
            if n != "0":
                b[self.idx[n]] += val
        return dict(zip(self.idx, np.linalg.solve(self.y, b)))


def degen(f, gm, cgs, ls, lgt, rg=0.0, x=1.0):
    """Inductively degenerated LNA. Returns (Z_in, noise factor). Source as a Norton current into 'in'."""
    w = 2 * math.pi * f
    m = Mna(["in", "g", "x", "d"])
    m.adm("in", "0", 1 / RS)
    m.adm("in", "g", 1 / (rg + 1j * w * lgt))
    m.adm("g", "x", 1j * w * cgs)
    m.adm("x", "0", 1 / (1j * w * ls))
    m.vccs(gm, "d", "x", "g", "x")
    m.adm("d", "0", 1e-3)                                  # noiseless load
    sig = m.solve({"in": 1 / RS})                           # 1 V source EMF
    zin = (sig["in"] / (1 / RS - sig["in"] / RS))           # node voltage / current into the LNA
    h_src = sig["d"] * RS                                   # per ampere of source noise current
    s_src = abs(h_src) ** 2 * 4 * KB * T0 / RS
    nd = m.solve({"d": -1.0, "x": 1.0})                     # channel noise flows d -> x
    s_nd = abs(nd["d"]) ** 2 * 4 * KB * T0 * x * gm
    s_rg = 0.0
    if rg > 0:
        yb = 1 / (rg + 1j * w * lgt)                        # series noise voltage -> Norton current yb*vn
        ng = m.solve({"in": -yb, "g": yb})
        s_rg = abs(ng["d"]) ** 2 * 4 * KB * T0 * rg
    return zin, 1 + (s_nd + s_rg) / s_src


def match(f0, gm, ft, rg_of=lambda lgt: 0.0):
    """Find L_s and L_g by root-finding so that Z_in(f0) = R_s (with an optional gate loss depending on L_g)."""
    cgs = gm / (2 * math.pi * ft)

    def resid(p):
        ls, lgt = p[0] * 1e-9, p[1] * 1e-9
        z, _ = degen(f0, gm, cgs, ls, lgt, rg_of(lgt))
        return [z.real - RS, z.imag]
    sol = optimize.fsolve(resid, [0.5, 5.0], xtol=1e-13)
    ls, lgt = sol[0] * 1e-9, sol[1] * 1e-9
    return cgs, ls, lgt, rg_of(lgt)


def cg(gm, x):
    m = Mna(["x", "d"])
    m.adm("x", "0", 1 / RS)
    m.vccs(gm, "d", "x", "0", "x")
    m.adm("d", "0", 1e-3)
    sig = m.solve({"x": 1 / RS})
    s_src = abs(sig["d"] * RS) ** 2 * 4 * KB * T0 / RS
    nd = m.solve({"d": -1.0, "x": 1.0})
    return 1 + abs(nd["d"]) ** 2 * 4 * KB * T0 * x * gm / s_src, 1 / (1 / RS - sig["x"] / RS) * sig["x"]


def ncl(gm1, gm2, r1, r2, x):
    """CG-CS noise-cancelling LNA; output v(d1) - v(d2)."""
    m = Mna(["x", "d1", "d2"])
    m.adm("x", "0", 1 / RS)
    m.vccs(gm1, "d1", "x", "0", "x")
    m.adm("d1", "0", 1 / r1)
    m.vccs(gm2, "d2", "0", "x", "0")
    m.adm("d2", "0", 1 / r2)
    out = lambda sol: sol["d1"] - sol["d2"]  # noqa: E731
    sig = m.solve({"x": 1 / RS})
    gain = out(sig)
    s_src = abs(gain) ** 2 * 4 * KB * T0 * RS
    s = abs(out(m.solve({"d1": -1.0, "x": 1.0}))) ** 2 * 4 * KB * T0 * x * gm1
    s += abs(out(m.solve({"d2": -1.0}))) ** 2 * 4 * KB * T0 * x * gm2
    s += abs(out(m.solve({"d1": 1.0}))) ** 2 * 4 * KB * T0 / r1
    s += abs(out(m.solve({"d2": 1.0}))) ** 2 * 4 * KB * T0 / r2
    return 1 + s / s_src, abs(gain)


# ---------------------------------------------------------------- Example 1
v.check("Ex 21-04.1a", db(1 + RS / RS))
v.check("Ex 21-04.1b", 1 / RS * 1e3)
for x, kf, kn in ((2 / 3, "Ex 21-04.1c", "Ex 21-04.1d"), (1.0, "Ex 21-04.1e", "Ex 21-04.1f")):
    f_cg, z_cg = cg(1 / RS, x)
    v.check(kf, f_cg)
    v.check(kn, db(f_cg))
v.assert_true("CG input is 50 ohm at g_m = 20 mS", abs(cg(0.02, 1)[1] - 50) < 1e-9)

# ---------------------------------------------------------------- Example 2
F0, GM, FT = 2.4e9, 0.04, 12e9
cgs2, ls2, lg2, _ = match(F0, GM, FT)
v.check("Ex 21-04.2a", cgs2 * 1e15)
v.check("Ex 21-04.2b", ls2 * 1e9)
v.check("Ex 21-04.2c", (lg2 + ls2) * 1e9)
v.check("Ex 21-04.2d", lg2 * 1e9)
w0 = 2 * math.pi * F0
v.check("Ex 21-04.2e", 1 / (2 * w0 * RS * cgs2))
# effective transconductance: output current per volt of EMF, from the MNA (load 1 mS, so i = v_d / 1 kohm)
m2 = Mna(["in", "g", "x", "d"])
m2.adm("in", "0", 1 / RS); m2.adm("in", "g", 1 / (1j * w0 * lg2)); m2.adm("g", "x", 1j * w0 * cgs2)  # noqa: E702
m2.adm("x", "0", 1 / (1j * w0 * ls2)); m2.vccs(GM, "d", "x", "g", "x"); m2.adm("d", "0", 1e-3)  # noqa: E702
gm_eff = abs(m2.solve({"in": 1 / RS})["d"]) * 1e-3
v.check("Ex 21-04.2f", gm_eff * 1e3)
z2, f2 = degen(F0, GM, cgs2, ls2, lg2)
v.check("Ex 21-04.2g", f2)
v.check("Ex 21-04.2h", db(f2))
v.check("Ex 21-04.2i", gm_eff * 200)
v.check("Ex 21-04.2j", db(1 + 4 * (f2 - 1)))
v.assert_true("matched input is 50 ohm", abs(z2 - RS) < 1e-6)
v.check("Txt 21-04.a", 20 * lg(1 / (2 * w0 * RS * cgs2)))
v.assert_true("lab closed form matches the MNA (Example 2)", abs(lab.nf_ind_degen(1, GM, F0, FT) - f2) < 1e-9)


# ---------------------------------------------------------------- Example 3: gate-inductor loss, re-matched by root-finding
def nf_q(q, f0=F0, gm=GM, ft=FT):
    w = 2 * math.pi * f0
    cgs, ls, lgt, rg = match(f0, gm, ft, lambda lgt: w * lgt / q)
    _, f = degen(f0, gm, cgs, ls, lgt, rg)
    return f, rg, lgt, ls


for q, kr, kn in ((10, "Ex 21-04.3a", "Ex 21-04.3b"), (15, "Ex 21-04.3c", "Ex 21-04.3f"), (30, "Ex 21-04.3g", "Ex 21-04.3h")):
    fq, rg, lgq, lsq = nf_q(q)
    v.check(kr, rg)
    v.check(kn, db(fq))
    if q == 15:
        v.check("Ex 21-04.3d", lgq * 1e9)
        v.check("Ex 21-04.3e", lsq * 1e9)

# ---------------------------------------------------------------- Example 4: IIP3 vs Q_in
def iip3_dbm(q_in, a_gs):
    vs = a_gs / q_in
    return 10 * lg(vs * vs / (8 * RS) / 1e-3)


cgs24, ls24, lg24, _ = match(F0, GM, 24e9)
q24 = 1 / (2 * w0 * RS * cgs24)
v.check("Ex 21-04.4a", iip3_dbm(1 / (2 * w0 * RS * cgs2), 0.3))
v.check("Ex 21-04.4b", q24)
v.check("Ex 21-04.4c", iip3_dbm(q24, 0.3))
v.check("Ex 21-04.4d", 20 * lg(q24))
v.check("Ex 21-04.4e", iip3_dbm(1 / (2 * w0 * RS * cgs2), 0.3) - iip3_dbm(q24, 0.3))
v.check("Ex 21-04.4f", db(degen(F0, GM, cgs24, ls24, lg24)[1]))

# ---------------------------------------------------------------- Example 5: noise cancelling
X23 = 2 / 3
r1c = 0.1 * 200 * RS
v.check("Ex 21-04.5a", r1c)
f5, g5 = ncl(0.02, 0.1, r1c, 200, X23)
v.check("Ex 21-04.5b", g5)
v.check("Ex 21-04.5c", f5)
v.check("Ex 21-04.5e", db(f5))
v.check("Ex 21-04.5d", db(cg(0.02, X23)[0]) - db(f5))
v.check("Ex 21-04.5f", 0.1 / 10 * 1e3)
v.check("Txt 21-04.b", optimize.brentq(lambda g: ncl(0.02, g, g * 200 * RS, 200, X23)[0] - cg(0.02, X23)[0], 0.005, 0.2) * 1e3)
# direct test: the M1 noise transfer is zero at cancellation
mt = Mna(["x", "d1", "d2"])
mt.adm("x", "0", 1 / RS); mt.vccs(0.02, "d1", "x", "0", "x"); mt.adm("d1", "0", 1 / r1c)  # noqa: E702
mt.vccs(0.1, "d2", "0", "x", "0"); mt.adm("d2", "0", 1 / 200)  # noqa: E702
sol = mt.solve({"d1": -1.0, "x": 1.0})
v.assert_true("M1 channel noise does not reach the output", abs(sol["d1"] - sol["d2"]) < 1e-9)


# ---------------------------------------------------------------- Example 6
def cascade_nf(f1_db, g1_db, f2_db):
    return db(10 ** (f1_db / 10) + (10 ** (f2_db / 10) - 1) / 10 ** (g1_db / 10))


g6 = optimize.brentq(lambda g: cascade_nf(1.0, g, 10.0) - 1.3, 0, 60)
v.check("Ex 21-04.6a", g6)
v.check("Ex 21-04.6b", cascade_nf(1.0, 15, 10))
v.check("Ex 21-04.6c", cascade_nf(1.0, 15, 10) - 1.0)

# ---------------------------------------------------------------- Problems
# Explicit noise powers at the amplifier input (per hertz, units of kT0): source share (1/2)^2 4 R_s, both resistors
# 4 (R_s/2), amplifier excess (F_A - 1) 4 (R_s/2) referred to its 25 ohm source.
rs_, fa_ = 50.0, 1.5
n_source = 0.25 * 4 * rs_
n_total = 4 * (rs_ / 2) + (fa_ - 1) * 4 * (rs_ / 2)
v.check("21-04.1a", db(n_total / n_source))
cg2, ls2p, lg2p, _ = match(5.5e9, 0.03, 40e9)
w5 = 2 * math.pi * 5.5e9
v.check("21-04.2a", cg2 * 1e15)
v.check("21-04.2b", ls2p * 1e9)
v.check("21-04.2c", lg2p * 1e9)
v.check("21-04.2d", 1 / (2 * w5 * RS * cg2))
v.check("21-04.2e", 2 * math.pi * 40e9 / (2 * w5 * RS) * 1e3)
v.check("21-04.2f", db(degen(5.5e9, 0.03, cg2, ls2p, lg2p)[1]))
f3, z3 = cg(0.03, X23)
v.check("21-04.3a", db(f3))
v.check("21-04.3b", z3.real)
gam3 = (z3.real - RS) / (z3.real + RS)
v.check("21-04.3c", gam3)
v.check("21-04.3d", -20 * lg(abs(gam3)))
v.check("21-04.3e", db(cg(0.02, X23)[0]) - db(f3))
for ft, k in ((12e9, "21-04.4a"), (24e9, "21-04.4b")):
    cgsx, lsx, lgx, _ = match(F0, GM, ft)
    mm = Mna(["in", "g", "x", "d"])
    mm.adm("in", "0", 1 / RS); mm.adm("in", "g", 1 / (1j * w0 * lgx)); mm.adm("g", "x", 1j * w0 * cgsx)  # noqa: E702
    mm.adm("x", "0", 1 / (1j * w0 * lsx)); mm.vccs(GM, "d", "x", "g", "x"); mm.adm("d", "0", 1e-3)  # noqa: E702
    v.check(k, abs(mm.solve({"in": 1 / RS})["d"]))
v.check("21-04.5a", optimize.brentq(lambda q: db(nf_q(q)[0]) - 0.8, 8, 100, xtol=1e-6))
# 6: rg = 5 ohm, re-matched by root-finding
cg6, ls6, lg6, _ = match(F0, GM, FT, lambda lgt: 5.0)
f6 = degen(F0, GM, cg6, ls6, lg6, 5.0)[1]
v.check("21-04.6a", db(f6))
shortcut = db(1 + 5 / RS + GM * RS * (F0 / FT) ** 2)
v.check("21-04.6b", shortcut)
v.check("21-04.6c", db(f6) - shortcut)
v.check("21-04.7a", iip3_dbm(2, 0.25))
v.check("21-04.7b", optimize.brentq(lambda q: iip3_dbm(q, 0.25) + 10, 0.5, 5))
g8 = optimize.brentq(lambda g: cascade_nf(1.5, g, 12.0) - 1.7, 0, 60)
v.check("21-04.8a", g8)
v.check("21-04.8b", cascade_nf(1.5, 25, 12))
g9 = optimize.brentq(lambda g: db(ncl(0.02, g, g * 300 * RS, 300, 1.0)[0]) - 1.0, 0.01, 2)
v.check("21-04.9a", g9 * 1e3)
v.check("21-04.9b", g9 / 10 * 1e3)
for r1, k in ((900, "21-04.10a"), (1000, "21-04.10b"), (1100, "21-04.10c")):
    v.check(k, db(ncl(0.02, 0.1, r1, 200, X23)[0]))
opt = optimize.minimize_scalar(lambda r: ncl(0.02, 0.1, r, 200, X23)[0], bounds=(500, 4000), method="bounded",
                               options={"xatol": 1e-6})
v.check("21-04.10d", opt.x)
v.check("21-04.10e", db(opt.fun))
v.check("21-04.10f", 0.02 / 10 * 1000)
v.check("21-04.10g", 0.02 / 10 * opt.x)


# 11: return-loss band from the MNA input impedance
def rl(f):
    z, _ = degen(f, GM, cgs2, ls2, lg2)
    return -20 * lg(abs((z - RS) / (z + RS)))


lo = optimize.brentq(lambda f: rl(f) - 10, 1.5e9, 2.39e9)
hi = optimize.brentq(lambda f: rl(f) - 10, 2.41e9, 4e9)
zlo, _ = degen(lo, GM, cgs2, ls2, lg2)
v.check("21-04.11a", abs(zlo.imag))
v.check("21-04.11b", lo / 1e9)
v.check("21-04.11c", hi / 1e9)
v.check("21-04.11d", (hi - lo) / F0 * 100)
# 12: 5.8 GHz
cg12, ls12, lg12, _ = match(5.8e9, 0.025, 30e9)
v.check("21-04.12a", db(degen(5.8e9, 0.025, cg12, ls12, lg12)[1]))
for q, kr, kn in ((12, "21-04.12b", "21-04.12c"), (40, "21-04.12d", "21-04.12e")):
    fq, rg, _, _ = nf_q(q, 5.8e9, 0.025, 30e9)
    v.check(kr, rg)
    v.check(kn, db(fq))
# 13: cascade with the mixer (noise temperatures; intercepts in mW)
v.check("21-04.13a", db(nf_q(15)[0] + 9 / 100))
v.check("21-04.13b", -10 * lg(1 / 10 ** (iip3_dbm(1 / (2 * w0 * RS * cgs2), 0.3) / 10) + 100 / 10 ** 0.5))

# ---------------------------------------------------------------- practitioner numbers
delta, gam, c = 4 / 3, 2 / 3, 0.395
v.check("Txt 21-04.c", db(1 + 2 * 0.1 * math.sqrt(delta * gam * (1 - c * c) / 5)))
v.check("Txt 21-04.h", db(1 + 2 * 0.2 * math.sqrt(delta * gam * (1 - c * c) / 5)))
v.check("Txt 21-04.d", 2.5e-3 * 1.8 * 1e3)
v.check("Txt 21-04.e", 0.120 * 5.0)
v.check("Txt 21-04.f", 35.2 - 22.1)
v.check("Txt 21-04.g", 30.0 - 21.3)

# ---------------------------------------------------------------- lab README
v.check("Lab 21-04.a", optimize.brentq(lambda q: db(nf_q(q)[0]) - 1.0, 8, 100, xtol=1e-6))
v.check("Lab 21-04.d", db(nf_q(5)[0]))
for g, k in ((0.05, "Lab 21-04.b"), (0.2, "Lab 21-04.c")):
    v.check(k, db(ncl(0.02, g, g * 200 * RS, 200, X23)[0]))

sys.exit(v.finish())
