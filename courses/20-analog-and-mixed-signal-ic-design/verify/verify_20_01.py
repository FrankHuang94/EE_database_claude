#!/usr/bin/env python3
"""Verify every number in chapter 20-01 (analog design fundamentals, the g_m/I_D method), its problems and its lab.

Independent routes:
- the drain current is computed from V_GS by solving the charge-potential relation 2q + ln q = V_P/V_T for q and
  applying I_D = I_spec (q^2 + q)/(1 + lambda_c q); g_m comes from a central finite difference of I_D(V_GS), not
  from the closed-form g_m/I_D expressions of the chapter;
- the charge-sheet current integral is checked by numerical quadrature of the drift-diffusion integrand;
- operating points with a target g_m/I_D are found by root-finding on V_GS with the numerical g_m;
- the closed forms and the lab module (gmid.py) are then asserted to agree with these numerical results;
- ngspice confirms the level-1 intrinsic-gain measurement of the lab netlist (gain.cir).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import gmid as gm_lab  # noqa: E402

v = Verifier.from_files("20-01", ROOT / "chapters" / "20-01-analog-design-fundamentals-gm-id.md",
                        ROOT / "solutions" / "20-01-solutions.md", LAB / "README.md")

KB, QE = 1.380649e-23, 1.602176634e-19
MU, COX, N, VTH, VSAT, VAL = 350e-4, 8.6e-3, 1.3, 0.45, 8e4, 8e6
U, PS = 1e-6, 1e-12


def vt_of(temp):
    return KB * temp / QE


class Dev:
    """An independent implementation of the chapter's model for one transistor."""

    def __init__(self, w, length, temp=300.0, mu=MU, vth=VTH, vsat=VSAT, n=N, vel_sat=True):
        self.w, self.l, self.temp, self.mu, self.vth, self.n = w, length, temp, mu, vth, n
        self.vt = vt_of(temp)
        self.ispec = 2 * n * mu * COX * (w / length) * self.vt ** 2
        self.lam = mu * self.vt / (vsat * length) if vel_sat else 0.0

    def q_of_vgs(self, vgs):
        vp = (vgs - self.vth) / self.n
        return brentq(lambda q: 2 * q + math.log(q) - vp / self.vt, 1e-40, 1e6, xtol=1e-40, rtol=1e-15)

    def i_d(self, vgs):
        q = self.q_of_vgs(vgs)
        return self.ispec * (q * q + q) / (1 + self.lam * q)

    def g_m(self, vgs, h=1e-6):
        return (self.i_d(vgs + h) - self.i_d(vgs - h)) / (2 * h)

    def gmid(self, vgs):
        return self.g_m(vgs) / self.i_d(vgs)

    def vgs_for_current(self, i):
        return brentq(lambda x: self.i_d(x) - i, self.vth - 1.0, self.vth + 3.0, xtol=1e-15)

    def vgs_for_gmid(self, target):
        return brentq(lambda x: self.gmid(x) - target, self.vth - 0.6, self.vth + 2.5, xtol=1e-13)

    def f_t(self, vgs):
        return self.g_m(vgs) / (2 * math.pi * (2 / 3) * self.w * self.l * COX)

    def gain(self, vgs):
        return self.gmid(vgs) * VAL * self.l


VT300 = vt_of(300.0)

# ---------------------------------------------------------------- the charge-sheet integral, by quadrature
# I_D L / (mu W) = integral over the channel potential of (-Q_i) dV_ch; with q as the variable this is
# 2 n C_ox V_T^2 integral (2q + 1) dq from q_d to q_s. Check against the closed form for one case.
qs, qd = 1.7, 0.2
integ = quad(lambda q: 2 * N * COX * VT300 * q * VT300 * (2 + 1 / q), qd, qs)[0]
v.assert_true("charge-sheet integral equals the closed form",
              abs(integ - 2 * N * COX * VT300 ** 2 * ((qs * qs + qs) - (qd * qd + qd))) < 1e-12 * integ, "")

# ---------------------------------------------------------------- section 3 text values
sq = Dev(1e-6, 1e-6)
v.check("Txt 20-01.a", sq.ispec / U)
v.check("Txt 20-01.b", 1 / (N * VT300))
v.check("Txt 20-01.j", 1 / VT300)
d015 = Dev(1e-6, 0.15e-6)
v.check("Txt 20-01.c", d015.lam)
v.check("Txt 20-01.m", Dev(1e-6, 0.5e-6).lam)
v.check("Txt 20-01.l", MU * VT300 / VSAT * 1e9)
v.check("Txt 20-01.d", 3 * VSAT / (4 * math.pi * 0.15e-6) / 1e9)
v.check("Txt 20-01.n", 1 / (1.4 * VT300))
v.check("Txt 20-01.o", 1 / (1.2 * VT300))
v.check("Txt 20-01.p", 4 * VT300 * 1e3)
v.check("Txt 20-01.q", 3.9 * 8.8541878128e-12 / 4.148e-9 * 1e3)
v.assert_true("current within 2% of saturation at 4 V_T", abs(math.exp(-4)) < 0.02, "")
# overdrive at IC = 1 and IC = 0.1 (long-channel relation, source charge)
for ic, key_units, key_mv in ((1.0, "Txt 20-01.g", "Txt 20-01.h"), (0.1, None, "Txt 20-01.i")):
    qq = brentq(lambda q: q * q + q - ic, 1e-9, 10)
    vov = N * VT300 * (2 * qq + math.log(qq))
    if key_units:
        v.check(key_units, vov / (N * VT300))
    v.check(key_mv, vov * 1e3)
# g_m/I_D at IC = 1 as a share of the weak-inversion maximum (long channel)
dl = Dev(1e-6, 1e-6, vel_sat=False)
vg1 = dl.vgs_for_current(dl.ispec * 1.0)
v.check("Txt 20-01.k", 100 * dl.gmid(vg1) * N * VT300)
# the f_T limit is approached at very high inversion
v.assert_true("f_T tends to 3 v_sat/(4 pi L)",
              abs(d015.f_t(VTH + N * VT300 * (2 * 1e5 + math.log(1e5))) / (3 * VSAT / (4 * math.pi * 0.15e-6)) - 1) < 0.01, "")
# long-channel f_T equals 09-09's 3 mu V_ov / (4 pi n L^2) deep in strong inversion
dlong = Dev(1e-6, 1e-6, vel_sat=False)
vgs_s = VTH + 0.6
v.assert_true("long-channel f_T is 3 mu V_T q / (2 pi L^2)",
              abs(dlong.f_t(vgs_s) / (3 * MU * VT300 * dlong.q_of_vgs(vgs_s) / (2 * math.pi * 1e-12)) - 1) < 1e-6, "")
vgs_deep = VTH + 3.0   # deep strong inversion: the ln q term is a small part of the overdrive
v.assert_true("long-channel f_T approaches 09-09's 3 mu V_ov/(4 pi n L^2)",
              abs(dlong.f_t(vgs_deep) / (3 * MU * 3.0 / (4 * math.pi * N * 1e-12)) - 1) < 0.05, "")


# ---------------------------------------------------------------- Example 1
d1 = Dev(10e-6, 0.5e-6)
d1l = Dev(10e-6, 0.5e-6, vel_sat=False)
v.check("Ex 20-01.1a", d1.ispec / U)
ic1 = 20e-6 / d1.ispec
v.check("Ex 20-01.1b", ic1)
vg1l = d1l.vgs_for_current(20e-6)
v.check("Ex 20-01.1c", d1l.gmid(vg1l))
vg1 = d1.vgs_for_current(20e-6)
gmid1 = d1.gmid(vg1)
v.check("Ex 20-01.1d", gmid1)
v.check("Ex 20-01.1e", gmid1 * 20e-6 / U)
v.check("Ex 20-01.1f", (vg1 - VTH) * 1e3)
v.check("Ex 20-01.1g", 2 / (vg1 - VTH))
v.check("Ex 20-01.1h", d1l.gmid(vg1l) / (1 / (N * VT300)))

# ---------------------------------------------------------------- Example 2
gm2 = 2 * math.pi * 100e6 * 2e-12
v.check("Ex 20-01.2a", gm2 / U)
id2 = gm2 / 15
v.check("Ex 20-01.2b", id2 / U)
ref = Dev(1e-6, 0.5e-6)                      # per-micrometre reference device
vg2 = ref.vgs_for_gmid(15)
j2 = ref.i_d(vg2) / 1e-6                     # A/m
v.check("Ex 20-01.2c", ref.i_d(vg2) / ref.ispec)
v.check("Ex 20-01.2d", j2)
w2 = id2 / j2
v.check("Ex 20-01.2e", w2 / U)
cgg2 = (2 / 3) * w2 * 0.5e-6 * COX
v.check("Ex 20-01.2f", cgg2 * 1e15)
v.check("Ex 20-01.2g", ref.f_t(vg2) / 1e9)
w2sq = id2 * 2 * N * 0.5e-6 / (MU * COX * (2 / 15) ** 2)
v.check("Ex 20-01.2h", w2sq / U)
v.check("Ex 20-01.2i", ref.gain(vg2))
v.check("Ex 20-01.2j", 100 * cgg2 / 2e-12)
v.check("Ex 20-01.2k", ref.f_t(vg2) / 100e6)
v.assert_true("the sized device reproduces g_m", abs(Dev(w2, 0.5e-6).g_m(vg2) / gm2 - 1) < 1e-6, "")

# ---------------------------------------------------------------- Example 3
l3 = 50 / (15 * VAL)
v.check("Ex 20-01.3a", l3 / U)
d3 = Dev(1e-6, l3)
vg3 = d3.vgs_for_gmid(15)
v.check("Ex 20-01.3b", d3.f_t(vg3) / 1e9)
v.check("Ex 20-01.3c", d3.i_d(vg3) / 1e-6)
v.assert_true("gain at the minimum length is 50", abs(d3.gain(vg3) - 50) < 1e-6, "")
fts = {}
for length, kg, kf in ((0.15e-6, "Ex 20-01.3d", "Ex 20-01.3e"), (1e-6, "Ex 20-01.3f", "Ex 20-01.3g")):
    dd = Dev(1e-6, length)
    vg = dd.vgs_for_gmid(15)
    v.check(kg, dd.gain(vg))
    fts[length] = dd.f_t(vg)
    v.check(kf, fts[length] / 1e9)
v.check("Ex 20-01.3h", fts[0.15e-6] / fts[1e-6])
v.check("Ex 20-01.3i", (1 / 0.15) ** 2)

# ---------------------------------------------------------------- Example 4
d4 = Dev(1e-6, 0.15e-6)
res4 = {}
for target, ki, kf, kp in ((25, "Ex 20-01.4a", "Ex 20-01.4b", "Ex 20-01.4c"), (15, "Ex 20-01.4d", None, "Ex 20-01.4e"),
                           (10, "Ex 20-01.4f", "Ex 20-01.4g", "Ex 20-01.4h"), (5, "Ex 20-01.4i", "Ex 20-01.4j", "Ex 20-01.4k")):
    vg = d4.vgs_for_gmid(target)
    res4[target] = d4.f_t(vg)
    v.check(ki, d4.i_d(vg) / d4.ispec)
    if kf:
        v.check(kf, res4[target] / 1e9)
    v.check(kp, target * res4[target] / 1e9)
v.check("Ex 20-01.4p", res4[5] / res4[10])
v.assert_true("product changes by less than 5% from 10 to 5 S/A", abs(5 * res4[5] / (10 * res4[10]) - 1) < 0.05, "")
opt = minimize_scalar(lambda vg: -d4.gmid(vg) * d4.f_t(vg), bounds=(VTH - 0.2, VTH + 1.0), method="bounded",
                      options={"xatol": 1e-9})
vgo = opt.x
v.check("Ex 20-01.4l", d4.i_d(vgo) / d4.ispec)
v.check("Ex 20-01.4m", d4.gmid(vgo))
v.check("Ex 20-01.4n", d4.f_t(vgo) / 1e9)
v.check("Ex 20-01.4o", d4.gmid(vgo) * d4.f_t(vgo) / 1e9)
v.check("Txt 20-01.e", d4.i_d(vgo) / d4.ispec)
v.check("Txt 20-01.f", d4.gmid(vgo))
# without velocity saturation the product has no interior maximum: it keeps rising with current
d4l = Dev(1e-6, 0.15e-6, vel_sat=False)
prods = [d4l.gmid(VTH + x) * d4l.f_t(VTH + x) for x in (-0.1, 0.0, 0.1, 0.3, 0.6, 1.0)]
v.assert_true("long-channel product is monotone", all(b > a for a, b in zip(prods, prods[1:])), "")

# ---------------------------------------------------------------- Example 5
vgs5 = d1.vgs_for_current(20e-6)
v.assert_true("gate voltage of Example 5 is 0.516 V", abs(vgs5 - 0.516) < 0.0005, f"{vgs5}")
v.check("Ex 20-01.5a", Dev(10e-6, 0.5e-6, vth=VTH + 0.05).i_d(vgs5) / U)
v.check("Ex 20-01.5b", Dev(10e-6, 0.5e-6, vth=VTH - 0.05).i_d(vgs5) / U)
g5 = {}
for temp, ki, kg, km in ((233.15, "Ex 20-01.5c", "Ex 20-01.5d", "Ex 20-01.5e"),
                         (373.15, "Ex 20-01.5f", "Ex 20-01.5g", "Ex 20-01.5h")):
    dt = Dev(10e-6, 0.5e-6, temp=temp, mu=MU * (temp / 300) ** -1.5)
    vg = dt.vgs_for_current(20e-6)
    v.check(ki, 20e-6 / dt.ispec)
    v.check(kg, dt.gmid(vg))
    g5[temp] = dt.g_m(vg)
    v.check(km, g5[temp] / U)
v.check("Ex 20-01.5i", 100 * (1 - g5[373.15] / g5[233.15]))
v.check("Ex 20-01.5j", 100 * (1 - 233.15 / 373.15))
v.check("Ex 20-01.5k", 100 * (1 - (233.15 / 373.15) ** 0.75))


# ---------------------------------------------------------------- problems
def ic_at(dev, vgs):
    return dev.i_d(vgs) / dev.ispec


# P1: long channel
p1 = Dev(5e-6, 1e-6, vel_sat=False)
v.check("20-01.1a", p1.ispec / U)
g1 = {}
for cur, ki, kg, kq in ((0.2e-6, "20-01.1b", "20-01.1c", "20-01.1h"), (4e-6, "20-01.1d", "20-01.1e", "20-01.1i"),
                        (200e-6, "20-01.1f", "20-01.1g", "20-01.1j")):
    vg = p1.vgs_for_current(cur)
    v.check(ki, cur / p1.ispec)
    g1[cur] = p1.gmid(vg)
    v.check(kg, g1[cur])
    v.check(kq, p1.q_of_vgs(vg))
v.check("20-01.1k", g1[0.2e-6] / g1[200e-6])
# P2
v.check("20-01.2a", 1 / (N * vt_of(233.15)))
v.check("20-01.2b", 1 / (N * vt_of(398.15)))
v.check("20-01.2c", 100 * (1 - vt_of(233.15) / vt_of(398.15)))
# P3
p3 = Dev(20e-6, 0.5e-6)
vg3b = p3.vgs_for_current(20e-6)
v.check("20-01.3a", 20e-6 / p3.ispec)
v.check("20-01.3b", p3.gmid(vg3b))
v.check("20-01.3c", 100 * (p3.gmid(vg3b) / gmid1 - 1))
# P4: long channel overdrives from the charge relation
for ic, key in ((0.01, "20-01.4a"), (0.1, "20-01.4b"), (1, "20-01.4c"), (10, "20-01.4d"), (100, "20-01.4e")):
    vg = dl.vgs_for_current(dl.ispec * ic)
    v.check(key, (vg - VTH) * 1e3)
v.check("20-01.4f", ic_at(dl, VTH))
# P5
r5 = Dev(1e-6, 0.5e-6)
vg5 = r5.vgs_for_gmid(20)
v.check("20-01.5a", 1e-3 / 20 / U)
v.check("20-01.5b", ic_at(r5, vg5))
j5 = r5.i_d(vg5) / 1e-6
v.check("20-01.5c", j5)
w5 = 50e-6 / j5
v.check("20-01.5d", w5 / U)
v.check("20-01.5e", r5.f_t(vg5) / 1e9)
v.check("20-01.5f", r5.gain(vg5))
v.check("20-01.5g", (2 / 3) * w5 * 0.5e-6 * COX * 1e15)
# P6
l6a, l6b = 100 / (20 * VAL), 100 / (12 * VAL)
v.check("20-01.6a", l6a / U)
v.check("20-01.6b", l6b / U)
da, db = Dev(1e-6, l6a), Dev(1e-6, l6b)
v.check("20-01.6c", da.f_t(da.vgs_for_gmid(20)) / 1e9)
v.check("20-01.6d", db.f_t(db.vgs_for_gmid(12)) / 1e9)
v.check("20-01.6e", l6b / l6a)
v.check("20-01.6f", 100 * (1 - 12 / 20))
# P7
for length, kl, kf in ((0.15e-6, "20-01.7a", "20-01.7c"), (60e-9, "20-01.7b", "20-01.7d")):
    dd = Dev(1e-6, length)
    v.check(kl, dd.lam)
    v.check(kf, dd.f_t(VTH + N * VT300 * (2 * 1e5 + math.log(1e5))) / 1e9)
# P8
p8 = Dev(1e-6, 1e-6, vel_sat=False)
q8 = p8.q_of_vgs(VTH + 0.2)
v.check("20-01.8a", q8)
v.check("20-01.8b", p8.f_t(VTH + 0.2) / 1e9)
f8b = 3 * MU * 0.2 / (4 * math.pi * N * 1e-12)
v.check("20-01.8c", f8b / 1e9)
v.check("20-01.8d", 100 * (f8b / p8.f_t(VTH + 0.2) - 1))
v.check("20-01.8e", N * VT300 * math.log(q8) * 1e3)
# P9
vg9 = d1.vgs_for_current(0.5e-6)
v.check("20-01.9a", 0.5e-6 / d1.ispec)
v.check("20-01.9b", vg9)
v.check("20-01.9g", (VTH - vg9) * 1e3)
up = Dev(10e-6, 0.5e-6, vth=VTH + 0.03).i_d(vg9)
dn = Dev(10e-6, 0.5e-6, vth=VTH - 0.03).i_d(vg9)
v.check("20-01.9c", up / U)
v.check("20-01.9d", dn / U)
v.check("20-01.9h", up / 0.5e-6)
v.check("20-01.9i", dn / 0.5e-6)
v.check("20-01.9e", math.exp(-0.03 / (N * VT300)))
v.check("20-01.9f", math.exp(0.03 / (N * VT300)))
# P10
gm10 = {}
for temp, kl, km, ki, kb in ((233.15, "20-01.10a", "20-01.10b", "20-01.10g", "20-01.10h"),
                             (300.0, "20-01.10c", "20-01.10d", "20-01.10k", "20-01.10i"),
                             (398.15, "20-01.10e", "20-01.10f", "20-01.10l", "20-01.10j")):
    dt = Dev(10e-6, 0.5e-6, temp=temp, mu=MU * (temp / 300) ** -1.5)
    lim = 1e-6 / (N * vt_of(temp))
    gm10[temp] = dt.g_m(dt.vgs_for_current(1e-6))
    v.check(kl, lim / U)
    v.check(km, gm10[temp] / U)
    v.check(ki, 1e-6 / dt.ispec)
    v.check(kb, 100 * (1 - gm10[temp] / lim))
v.check("20-01.10m", 100 * (1 - gm10[398.15] / gm10[233.15]))
# P11
d11 = Dev(1e-6, 0.3e-6)
o11 = minimize_scalar(lambda vg: -d11.gmid(vg) * d11.f_t(vg), bounds=(VTH - 0.2, VTH + 1.0), method="bounded",
                      options={"xatol": 1e-9}).x
v.check("20-01.11a", ic_at(d11, o11))
v.check("20-01.11b", d11.gmid(o11))
v.check("20-01.11c", d11.f_t(o11) / 1e9)
pk11 = d11.gmid(o11) * d11.f_t(o11)
v.check("20-01.11d", pk11 / 1e9)
v.check("20-01.11e", d11.lam)
v.check("20-01.11f", math.log((d4.gmid(vgo) * d4.f_t(vgo)) / pk11) / math.log(2))
# P12: g_m/I_D at IC = 10, found from V_GS
for dd, key in ((Dev(1e-6, 0.15e-6), "20-01.12a"), (Dev(1e-6, 0.15e-6, vel_sat=False), "20-01.12b")):
    vg = dd.vgs_for_current(10 * dd.ispec)
    v.check(key, dd.gmid(vg))
# P13
d13 = Dev(1e-6, 0.15e-6)
vg13 = brentq(lambda x: d13.f_t(x) - 10e9, VTH - 0.4, VTH + 0.5, xtol=1e-14)
g13 = d13.gmid(vg13)
v.check("20-01.13a", ic_at(d13, vg13))
v.check("20-01.13b", g13)
i13 = 2e-3 / g13
v.check("20-01.13c", i13 / U)
w13 = i13 / (d13.i_d(vg13) / 1e-6)
v.check("20-01.13d", w13 / U)
vg8 = d13.vgs_for_gmid(8)
w8 = 250e-6 / (d13.i_d(vg8) / 1e-6)
v.check("20-01.13e", 2e-3 / 8 / U)
v.check("20-01.13f", w8 / U)
v.check("20-01.13g", d13.f_t(vg8) / 1e9)
v.check("20-01.13h", 250e-6 / i13)
v.check("20-01.13i", 100 * (1 - i13 / 250e-6))
v.check("20-01.13j", w13 / w8)
# P14
a14 = {}
r14 = Dev(1e-6, 0.5e-6)
for gi, ki, kw, ka in ((25, "20-01.14a", "20-01.14b", "20-01.14c"), (10, "20-01.14d", "20-01.14e", "20-01.14f")):
    vg = r14.vgs_for_gmid(gi)
    cur = 500e-6 / gi
    w = cur / (r14.i_d(vg) / 1e-6)
    a14[gi] = w * 0.5e-6
    v.check(ki, cur / U)
    v.check(kw, w / U)
    v.check(ka, a14[gi] * 1e12)
v.check("20-01.14g", a14[25] / a14[10])
v.check("20-01.14h", math.sqrt(a14[25] / a14[10]))
v.check("20-01.14i", 100 * (1 - 20 / 50))
# P15
d15 = Dev(1e-6, 0.15e-6)
vg15 = d15.vgs_for_gmid(22)
v.check("20-01.15a", ic_at(d15, vg15))
v.check("20-01.15b", d15.f_t(vg15) / 1e9)
v.check("20-01.15c", d15.gain(vg15))

# ---------------------------------------------------------------- lab
KP, VTO, WL1 = 200e-6, 0.45, 10.0
for lam, kg, kgm, kva in ((0.1, "Lab 20-01.a", "Lab 20-01.c", "Lab 20-01.d"), (0.05, "Lab 20-01.b", None, None)):
    vov = brentq(lambda x: KP / 2 * WL1 * x ** 2 * (1 + lam * (VTO + x)) - 20e-6, 1e-6, 2, xtol=1e-15)
    vds = VTO + vov
    gmx = KP * WL1 * vov * (1 + lam * vds)
    gds = lam * KP / 2 * WL1 * vov ** 2
    rf = 1e9
    v.check(kg, (gmx - 1 / rf) / (gds + 1 / rf))
    if kgm:
        v.check(kgm, gmx / 20e-6)
        v.check(kva, (1 + lam * vds) / lam)
for ic, key in ((0.01, "Lab 20-01.e"), (1, "Lab 20-01.f"), (100, "Lab 20-01.g")):
    v.check(key, dl.gmid(dl.vgs_for_current(dl.ispec * ic)))
dsh = Dev(1e-6, 0.15e-6)
v.check("Lab 20-01.h", dsh.gmid(dsh.vgs_for_current(dsh.ispec * 100)))
v.check("Lab 20-01.i", 2 * N * VT300 * 1e3)
for length, ki, kg in ((0.5e-6, "Lab 20-01.j", "Lab 20-01.l"), (1e-6, "Lab 20-01.k", "Lab 20-01.m")):
    dd = Dev(1e-6, length)
    o = minimize_scalar(lambda vg: -dd.gmid(vg) * dd.f_t(vg), bounds=(VTH - 0.2, VTH + 2.0), method="bounded",
                        options={"xatol": 1e-9}).x
    v.check(ki, ic_at(dd, o))
    v.check(kg, dd.gmid(o))
dt125 = Dev(10e-6, 0.5e-6, temp=398.15, mu=MU * (398.15 / 300) ** -1.5)
v.check("Lab 20-01.n", dt125.g_m(dt125.vgs_for_current(20e-6)) / U)

# ---------------------------------------------------------------- the lab module agrees with this implementation
proc = gm_lab.Process()
v.assert_true("lab g_m/I_D matches (Example 1)",
              abs(gm_lab.gm_over_id(ic1, proc.n, proc.vt, proc.lam(0.5e-6)) - gmid1) < 1e-6, "")
i_lab, w_lab, ic_lab = gm_lab.size_for_gm(gm2, 15, proc, 0.5e-6)
v.assert_true("lab sizing matches (Example 2)", abs(w_lab / w2 - 1) < 1e-6, "")
v.assert_true("lab f_T matches (Example 4 peak)", abs(gm_lab.ft(d4.i_d(vgo) / d4.ispec, proc, 0.15e-6) / d4.f_t(vgo) - 1) < 1e-6, "")
v.assert_true("lab drain current matches", abs(gm_lab.drain_current(0.52, proc, 10e-6, 0.5e-6) / d1.i_d(0.52) - 1) < 1e-9, "")
v.assert_true("closed-form g_m/I_D (long channel) matches the numerical one",
              abs(2 / (N * VT300 * (1 + math.sqrt(1 + 4 * ic1))) - d1l.gmid(vg1l)) < 1e-6, "")

sys.exit(v.finish())
