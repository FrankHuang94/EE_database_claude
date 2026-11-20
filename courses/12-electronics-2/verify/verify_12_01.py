#!/usr/bin/env python3
"""Verify every number in chapter 12-01 (differential pairs), its solutions and lab.

Independent routes (not the closed forms of the chapter):
- large-signal splits by solving the device equations with the tail constraint for the shared emitter or
  source node (root finding on Kirchhoff's current law), never from tanh or the square-law formula;
- small-signal gains, common-mode gains and CMRR by modified nodal analysis of the full two-transistor
  circuit with its tail resistance and any mismatch, not by half-circuits;
- offsets by solving for the differential input that balances a mismatched circuit, and offset
  sensitivities by finite differences of that solution; the RSS budget is checked by Monte Carlo;
- drift by evaluating the bipolar offset at two temperatures; the CML pole by root finding on |H|.
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
v = Verifier.from_files("12-01", COURSE / "chapters" / "12-01-differential-pairs.md",
                        COURSE / "solutions" / "12-01-solutions.md",
                        COURSE / "labs" / "12-01-lab" / "README.md")
K_B, Q_E = 1.380649e-23, 1.602176634e-19
VT = K_B * 300 / Q_E                     # 25.852 mV, the course value
VTN = 0.5
db = lambda r: 20 * math.log10(abs(r))
rng = np.random.default_rng(1201)


# ============================================================ large-signal solvers
def bjt_split(vid, IEE, IS1=1e-15, IS2=1e-15, vt=VT):
    """Collector currents of a BJT pair (alpha = 1): find the emitter node so the two currents sum to IEE."""
    f = lambda ve: IS1 * math.exp((vid / 2 - ve) / vt) + IS2 * math.exp((-vid / 2 - ve) / vt) - IEE
    ve = brentq(f, -2.0, 2.0, xtol=1e-15)
    return IS1 * math.exp((vid / 2 - ve) / vt), IS2 * math.exp((-vid / 2 - ve) / vt)


def mos_split(vid, ISS, kn1, kn2=None, vtn1=VTN, vtn2=VTN, vic=1.0):
    """Drain currents of a MOS pair in saturation (or cutoff): find the source node from KCL."""
    kn2 = kn1 if kn2 is None else kn2
    sq = lambda k, vov: 0.5 * k * max(vov, 0.0) ** 2
    f = lambda vs: sq(kn1, vic + vid / 2 - vs - vtn1) + sq(kn2, vic - vid / 2 - vs - vtn2) - ISS
    vs = brentq(f, -5.0, vic + abs(vid) + 1.0, xtol=1e-15)
    return sq(kn1, vic + vid / 2 - vs - vtn1), sq(kn2, vic - vid / 2 - vs - vtn2)


def mna_pair(gm1, gm2, RD1, RD2, RSS, vg1, vg2):
    """Small-signal node voltages (d1, d2, s) of a pair with transconductances gm1, gm2 (drain currents
    gm*(vg - vs) flowing from drain to source), drain loads RD1, RD2 to AC ground and RSS from s to ground."""
    G = np.zeros((3, 3))
    b = np.zeros(3)
    G[0, 0] += 1 / RD1
    G[1, 1] += 1 / RD2
    G[2, 2] += 1 / RSS
    for d, gm, vg in ((0, gm1, vg1), (1, gm2, vg2)):
        # current gm*(vg - vs) leaves the drain node and enters the source node
        G[d, 2] -= gm
        b[d] -= gm * vg
        G[2, 2] += gm
        b[2] += gm * vg
    return np.linalg.solve(G, b)


# ============================================================ theory
v.check("T 12-01.a", 2 * VT * 1e3)
v.check("T 12-01.b", 1e-3 / 300 * 1e6)
v.check("T 12-01.c", 1.6 / 0.3)                                   # TLV9062 max/typ offset [R-182]
v.check("T 12-01.d", brentq(lambda x: (lambda a, c: (a - c) / 1e-3)(*bjt_split(x, 1e-3)) - 0.9, 1e-3, 0.3,
                            xtol=1e-12) * 1e3)

# ============================================================ Example 1: BJT pair, 1 mA, 5 kOhm
I1 = 1e-3
a0, b0 = bjt_split(0.0, I1)
a10, b10 = bjt_split(0.010, I1)
a50, b50 = bjt_split(0.050, I1)
v.check("Ex 12-01.1a", a0 * 1e3)
v.check("Ex 12-01.1b", a10 * 1e3)
v.check("Ex 12-01.1c", b10 * 1e3)
v.check("Ex 12-01.1d", a50 * 1e3)
v.check("Ex 12-01.1e", b50 * 1e3)
h = 1e-7
slope = ((lambda p: p[0] - p[1])(bjt_split(h, I1)) - (lambda p: p[0] - p[1])(bjt_split(-h, I1))) / (2 * h)
v.check("Ex 12-01.1f", slope * 1e3)                                 # d(ic1 - ic2)/dvid = one transistor's g_m
gm1 = slope
v.check("Ex 12-01.1g", gm1 * 5e3)
v.check("Ex 12-01.1h", brentq(lambda x: bjt_split(x, I1)[0] / I1 - 0.9, 1e-4, 0.3, xtol=1e-12) * 1e3)
v.check("Ex 12-01.1i", brentq(lambda x: (lambda p: (p[0] - p[1]) / I1)(bjt_split(x, I1)) - 0.9, 1e-4, 0.3,
                              xtol=1e-12) * 1e3)
u99 = brentq(lambda u: math.tanh(u) / u - 0.99, 0.01, 1.0, xtol=1e-14)
v.check("Ex 12-01.1j", u99)
lin_dev = lambda x: (lambda p: (p[0] - p[1]))(bjt_split(x, I1)) / (gm1 * x) - 0.99
v.check("Ex 12-01.1k", brentq(lin_dev, 1e-4, 0.03, xtol=1e-12) * 1e3)
v.check("Ex 12-01.1l", gm1 * 0.010 * 1e3)
v.check("Ex 12-01.1m", (a10 - b10) * 1e3)
v.check("Ex 12-01.1n", 100 * (1 - (a10 - b10) / (gm1 * 0.010)))

# ============================================================ Example 2: MOS pair, 2 mA/V^2, 200 uA, 10 kOhm
kn2, ISS2, RD2_, VDD2 = 2e-3, 200e-6, 10e3, 1.8
d0 = mos_split(0.0, ISS2, kn2)[0]
vov2 = brentq(lambda x: 0.5 * kn2 * x * x - d0, 1e-3, 2.0, xtol=1e-14)   # overdrive that gives the balanced I_D
v.check("Ex 12-01.2a", vov2)
gm2 = ((lambda p: p[0] - p[1])(mos_split(h, ISS2, kn2)) - (lambda p: p[0] - p[1])(mos_split(-h, ISS2, kn2))) / (
    2 * h)
v.check("Ex 12-01.2b", gm2 * 1e3)
v.check("Ex 12-01.2c", gm2 * RD2_)
vsw = brentq(lambda x: mos_split(x, ISS2, kn2)[1] - 1e-12, 0.1, 1.0, xtol=1e-12)   # where Q2 just turns off
v.check("Ex 12-01.2d", vsw)
i1, i2 = mos_split(0.2, ISS2, kn2)
v.check("Ex 12-01.2e", i1 * 1e6)
v.check("Ex 12-01.2f", i2 * 1e6)
v.check("Ex 12-01.2l", VDD2 - i1 * RD2_)
v.assert_true("M1 would be in triode: drain below gate minus V_TN for any V_IC above 1 V", VDD2 - i1 * RD2_ < 1.0 + 0.1 - VTN)


def saturated(vic, vdd=VDD2, RD=RD2_, ISS=ISS2, kn=kn2, vtail=0.2):
    """All three transistors saturated at common-mode input vic (balanced)?"""
    vs = brentq(lambda s: kn * max(vic - s - VTN, 0) ** 2 - ISS, -3, vic, xtol=1e-14)
    vd = vdd - ISS / 2 * RD
    return (vs >= vtail - 1e-12) and (vd >= vic - VTN - 1e-12)


v.check("Ex 12-01.2g", brentq(lambda x: 1.0 if saturated(x) else -1.0, 0.6, 1.2, xtol=1e-9))
v.check("Ex 12-01.2h", brentq(lambda x: 1.0 if saturated(x) else -1.0, 1.2, 1.79, xtol=1e-9))
v.check("Ex 12-01.2i", gm2 * 0.2 * 1e6)
v.check("Ex 12-01.2j", 100 * (gm2 * 0.2 / (i1 - i2) - 1))
v.check("Ex 12-01.2k", 100 * 0.2 / vov2)

# ============================================================ Example 3: CMRR by MNA
RSS3 = 50e3
nd = mna_pair(gm2, gm2, RD2_, RD2_, RSS3, 0.5, -0.5)                  # vid = 1, differential drive
Ad_se = abs(nd[0])
v.check("Ex 12-01.3a", Ad_se)
nc = mna_pair(gm2, gm2, RD2_, RD2_, RSS3, 1.0, 1.0)                    # vic = 1
Acm = abs(nc[0])
v.check("Ex 12-01.3b", Acm)
v.check("Ex 12-01.3c", Ad_se / Acm)
v.check("Ex 12-01.3d", db(Ad_se / Acm))
ncm = mna_pair(gm2, gm2, RD2_ + 50, RD2_ - 50, RSS3, 1.0, 1.0)         # 1% (100 Ohm) load mismatch, split +-50
ndm = mna_pair(gm2, gm2, RD2_ + 50, RD2_ - 50, RSS3, 0.5, -0.5)
Acmdm = abs(ncm[0] - ncm[1])
v.check("Ex 12-01.3e", Acmdm)
cmrr_diff = abs(ndm[0] - ndm[1]) / Acmdm
v.check("Ex 12-01.3f", cmrr_diff)
v.check("Ex 12-01.3g", db(cmrr_diff))
v.check("Ex 12-01.3h", cmrr_diff / (Ad_se / Acm))


# ============================================================ Example 4: offset budget
def mos_offset(dvt=0.0, dk=0.0, dR=0.0, ISS=ISS2, kn=kn2, RD=RD2_):
    """Differential input that zeroes v_od for a pair with threshold, current-factor and load mismatch
    (each split +-1/2 between the two sides)."""
    def vod(x):
        a, b = mos_split(x, ISS, kn * (1 + dk / 2), kn * (1 - dk / 2), VTN + dvt / 2, VTN - dvt / 2)
        return a * RD * (1 + dR / 2) - b * RD * (1 - dR / 2)
    return brentq(vod, -0.2, 0.2, xtol=1e-15)


sens = lambda **kw: abs(mos_offset(**{k: 1e-4 * x for k, x in kw.items()})) / 1e-4   # numerical d(VOS)/d(param)
s_vt, s_k, s_R = 3.5e-3 / math.sqrt(20 * 0.5), 0.005, 0.01
c_vt = sens(dvt=1.0) * s_vt
c_R = sens(dR=1.0) * s_R
c_k = sens(dk=1.0) * s_k
v.check("Ex 12-01.4a", c_vt * 1e3)
v.check("Ex 12-01.4b", c_R * 1e3)
v.check("Ex 12-01.4c", c_k * 1e3)
sig = math.sqrt(c_vt ** 2 + c_R ** 2 + c_k ** 2)
v.check("Ex 12-01.4d", sig * 1e3)
v.check("Ex 12-01.4e", 3 * sig * 1e3)
# Monte Carlo: the RSS of first-order terms predicts the spread of the exact nonlinear offset
N = 4000
mc = np.array([mos_offset(rng.normal(0, s_vt), rng.normal(0, s_k), rng.normal(0, s_R)) for _ in range(N)])
v.assert_true("Monte Carlo sigma within 4% of the RSS budget", abs(mc.std() / sig - 1) < 0.04)


def bjt_offset(dIS=0.0, dR=0.0, vt=VT):
    def vod(x):
        a, b = bjt_split(x, 1e-3, 1e-15 * (1 + dIS / 2), 1e-15 * (1 - dIS / 2), vt)
        return a * (1 + dR / 2) - b * (1 - dR / 2)
    return brentq(vod, -0.2, 0.2, xtol=1e-15)


v.check("Ex 12-01.4f", abs(bjt_offset(dIS=1e-4)) / 1e-4 * 0.01 * 1e3)
c_vt4 = sens(dvt=1.0) * 3.5e-3 / math.sqrt(40 * 1.0)                 # W and L doubled: 4x area
c_k4 = sens(dk=1.0) * s_k / 2
v.check("Ex 12-01.4g", c_vt4 * 1e3)
v.check("Ex 12-01.4i", c_k4 * 1e3)
v.check("Ex 12-01.4h", math.sqrt(c_vt4 ** 2 + c_R ** 2 + c_k4 ** 2) * 1e3)
# half the overdrive at the same current: four times the current factor (W x4, same L), so 4x area
sens_h = lambda **kw: abs(mos_offset(kn=4 * kn2, **{k: 1e-4 * x for k, x in kw.items()})) / 1e-4
sig_half = math.sqrt((sens_h(dvt=1.0) * 3.5e-3 / math.sqrt(80 * 0.5)) ** 2 + (sens_h(dR=1.0) * s_R) ** 2
                     + (sens_h(dk=1.0) * s_k / 2) ** 2)
v.check("Ex 12-01.4j", sig_half * 1e3)

# ============================================================ Example 5: drift
dIS5 = brentq(lambda d: abs(bjt_offset(dIS=d)) - 1e-3, 1e-4, 0.2, xtol=1e-14)   # I_S mismatch giving 1.0 mV
vos300 = abs(bjt_offset(dIS=dIS5))
VT350 = K_B * 350 / Q_E
vos350 = abs(bjt_offset(dIS=dIS5, vt=VT350))
v.check("Ex 12-01.5a", (vos350 - vos300) / 50 * 1e6)
v.check("Ex 12-01.5b", vos350 * 1e3)
v.check("Ex 12-01.5c", (vos350 - vos300) * 1e3)
# ratio trim: choose the load mismatch that nulls the offset at 300 K; it then stays null at 350 K
dR5 = brentq(lambda d: bjt_offset(dIS=dIS5, dR=d), -0.2, 0.2, xtol=1e-15)
v.assert_true("ratio trim nulls the offset at 350 K too", abs(bjt_offset(dIS=dIS5, dR=dR5, vt=VT350)) < 1e-9)
v.check("Ex 12-01.5d", 30e-6 / 300 * 1e6)

# ============================================================ Example 6: CML buffer
ISS6, RD6, kn6, CL6 = 4e-3, 100.0, 100e-3, 100e-15
v.check("Ex 12-01.6a", ISS6 * RD6)
d6 = mos_split(0.0, ISS6, kn6)[0]
v.check("Ex 12-01.6b", brentq(lambda x: 0.5 * kn6 * x * x - d6, 1e-3, 2.0, xtol=1e-14))
v.check("Ex 12-01.6c", brentq(lambda x: mos_split(x, ISS6, kn6)[1] - 1e-12, 0.05, 1.0, xtol=1e-12))
v.check("Ex 12-01.6d", brentq(lambda f: abs(1 / (1 + 2j * math.pi * f * 1e9 * RD6 * CL6)) - 1 / math.sqrt(2),
                              0.1, 1e3, xtol=1e-10))
v.check("Ex 12-01.6e", ISS6 * 1.8 * 1e3)

# ============================================================ solutions
# 1: BJT pair, 2 mA, 2 kOhm, beta = 100
gmP1 = ((lambda p: p[0] - p[1])(bjt_split(h, 2e-3)) - (lambda p: p[0] - p[1])(bjt_split(-h, 2e-3))) / (2 * h)
v.check("12-01.1a", gmP1 * 1e3)
nP1 = mna_pair(gmP1, gmP1, 2e3, 2e3, 1e12, 0.5, -0.5)
v.check("12-01.1b", abs(nP1[0] - nP1[1]))
v.check("12-01.1c", abs(nP1[0]))
# input resistance: drive vid = 1 V across two bases, each with r_pi = beta/g_m to the emitter node
rpi = 100 / gmP1
v.check("12-01.1d", 1.0 / (1.0 / (2 * rpi)) / 1e3)
# 2
d02 = mos_split(0.0, 100e-6, 1e-3)[0]
v.check("12-01.2a", brentq(lambda x: 0.5e-3 * x * x - d02, 1e-3, 2.0, xtol=1e-14))
gmP2 = ((lambda p: p[0] - p[1])(mos_split(h, 100e-6, 1e-3)) - (lambda p: p[0] - p[1])(mos_split(-h, 100e-6, 1e-3))) / (
    2 * h)
v.check("12-01.2b", gmP2 * 1e3)
v.check("12-01.2c", brentq(lambda x: mos_split(x, 100e-6, 1e-3)[1] - 1e-13, 0.1, 1.0, xtol=1e-12))
# 3
v.check("12-01.3a", bjt_split(0.025, 1e-3)[0] * 1e3)
# 4
nd4 = mna_pair(1e-3, 1e-3, 1e4, 1e4, 1e5, 0.5, -0.5)
nc4 = mna_pair(1e-3, 1e-3, 1e4, 1e4, 1e5, 1.0, 1.0)
v.check("12-01.4a", abs(nd4[0]) / abs(nc4[0]))
v.check("12-01.4b", db(abs(nd4[0]) / abs(nc4[0])))
# 5
a5, b5 = mos_split(0.1, 100e-6, 1e-3)
v.check("12-01.5a", (a5 - b5) * 1e6)
v.check("12-01.5b", a5 * 1e6)
v.check("12-01.5c", b5 * 1e6)
# 6
v.check("12-01.6a", brentq(lambda x: 0.5 * 4e-3 * x * x - mos_split(0.0, 400e-6, 4e-3)[0], 1e-3, 2.0, xtol=1e-14))
sat6 = lambda x: saturated(x, vdd=3.3, RD=5e3, ISS=400e-6, kn=4e-3, vtail=0.25)
v.check("12-01.6b", brentq(lambda x: 1.0 if sat6(x) else -1.0, 0.6, 1.5, xtol=1e-9))
v.check("12-01.6c", brentq(lambda x: 1.0 if sat6(x) else -1.0, 1.5, 3.29, xtol=1e-9))
# 7: V_ov = 0.2 V (choose kn with ISS = 100 uA: kn = ISS/Vov^2)
kn7 = 100e-6 / 0.2 ** 2
load7 = abs(mos_offset(dR=0.02, ISS=100e-6, kn=kn7, RD=1e4))
v.check("12-01.7a", load7 * 1e3)
same7 = abs(mos_offset(dR=0.02, dvt=-1.5e-3, ISS=100e-6, kn=kn7, RD=1e4))
v.check("12-01.7b", same7 * 1e3)
v.check("12-01.7c", math.hypot(load7, 1.5e-3) * 1e3)
# 8
# exact offset for I_S2 = 1.05 I_S1: zero output needs equal currents, solve directly
ex8 = brentq(lambda x: (lambda p: p[0] - p[1])(bjt_split(x, 1e-3, 1e-15, 1.05e-15)), -0.1, 0.1, xtol=1e-15)
v.check("12-01.8a", abs(ex8) * 1e3)
v.check("12-01.8b", VT * 0.05 * 1e3)
v.check("12-01.8c", abs(ex8) / 300 * 1e6)
v.check("12-01.8d", 100 * (VT * 0.05 / abs(ex8) - 1))
# 9: g_m mismatch by MNA
g9 = 1e-3
n9c = mna_pair(g9 * 1.005, g9 * 0.995, 1e4, 1e4, 1e5, 1.0, 1.0)
n9d = mna_pair(g9 * 1.005, g9 * 0.995, 1e4, 1e4, 1e5, 0.5, -0.5)
cm9 = abs(n9d[0] - n9d[1]) / abs(n9c[0] - n9c[1])
v.check("12-01.9a", cm9)
v.check("12-01.9b", db(cm9))
# 10: degenerated pair: small-signal transconductance per side from a numerical solve with R_E
gm10 = ((lambda p: p[0] - p[1])(bjt_split(h, 1e-3)) - (lambda p: p[0] - p[1])(bjt_split(-h, 1e-3))) / (2 * h)
v.check("12-01.10a", gm10 * 1e3)


def bjt_split_degen(vid, IEE, RE):
    """Pair with RE in each emitter: unknowns are the two currents; v_BE + i*RE equal on both sides."""
    def f(ic1):
        ic2 = IEE - ic1
        return (VT * math.log(ic1 / 1e-15) + ic1 * RE) - (VT * math.log(ic2 / 1e-15) + ic2 * RE) - vid
    ic1 = brentq(f, 1e-12, IEE - 1e-12, xtol=1e-18)
    return ic1, IEE - ic1


Gd = ((lambda p: p[0] - p[1])(bjt_split_degen(h, 1e-3, 500)) - (lambda p: p[0] - p[1])(
    bjt_split_degen(-h, 1e-3, 500))) / (2 * h)
v.check("12-01.10b", Gd * 1e3)                                    # d(ic1-ic2)/dvid is the per-side value
v.check("12-01.10c", gm10 / Gd)
# 11
WL11 = brentq(lambda a: 3.5 / math.sqrt(a) - 0.5, 1, 1e4, xtol=1e-12)
v.check("12-01.11a", WL11)
v.check("12-01.11b", 2 / 3 * WL11 * 10)
# 12: 1% compression found from the solved transfer (Vov = 0.3162 V: kn = 2 mA/V^2, ISS = 200 uA)
comp = lambda x: (lambda p: p[0] - p[1])(mos_split(x, ISS2, kn2)) / (gm2 * x) - 0.99
x12 = brentq(comp, 0.01, 0.3, xtol=1e-14)
v.check("12-01.12a", x12 / vov2)
v.check("12-01.12b", x12 * 1e3)
# 13: CML for 50 Ohm, 300 mV
I13 = brentq(lambda i: i * 50 - 0.3, 1e-4, 1, xtol=1e-15)
v.check("12-01.13a", I13 * 1e3)
v.check("12-01.13b", brentq(lambda x: 0.5 * 150e-3 * x * x - mos_split(0.0, I13, 150e-3)[0], 1e-3, 2, xtol=1e-14))
v.check("12-01.13c", brentq(lambda x: mos_split(x, I13, 150e-3)[1] - 1e-12, 0.05, 1.0, xtol=1e-12))
v.check("12-01.13d", brentq(lambda f: abs(1 / (1 + 2j * math.pi * f * 1e9 * 50 * 200e-15)) - 1 / math.sqrt(2),
                            0.1, 1e3, xtol=1e-10))
v.check("12-01.13e", I13 * 1.0 * 1e3)
# 14
z14 = 5 / 2.086
v.check("12-01.14a", z14)
v.check("12-01.14b", 100 * (norm.cdf(z14) - norm.cdf(-z14)))
v.check("12-01.14c", 100 * (1 - (norm.cdf(z14) - norm.cdf(-z14))))

# ============================================================ lab
LAB = Path(COURSE / "labs" / "12-01-lab" / "README.md")
if LAB.exists():
    v.check("Lab 12-01.a", sig * 1e3)
    v.check("Lab 12-01.b", mc.std() * 1e3, rtol=0.04)
    v.check("Lab 12-01.c", sig_half * 1e3)

sys.exit(v.finish())
