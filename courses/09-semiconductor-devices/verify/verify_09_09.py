#!/usr/bin/env python3
"""Verify every number in chapter 09-09 (the long-channel MOSFET), its solutions and lab.

Independent routes:
- drain current by numerical quadrature of the local channel charge over channel potential (current
  continuity), not from the closed-form parabola;
- saturation by maximizing the computed current over V_DS; the exact bulk-charge model by the same shooting
  with the square-root local charge;
- body effect from the threshold condition with the source-body bias added to the band bending;
- channel-length modulation and transconductances by numerical differentiation;
- C_gs by integrating the channel charge along the computed channel profile and differentiating with V_GS;
- f_T from the hybrid-pi current gain crossing unity.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad, solve_ivp, trapezoid
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-09", COURSE / "chapters" / "09-09-long-channel-mosfet.md",
                        COURSE / "solutions" / "09-09-solutions.md",
                        COURSE / "labs" / "09-09-lab" / "README.md")

Q = C.e
KB = C.k / C.e
VT = KB * 300
NI = 1.0e10
EPS = 11.7 * C.epsilon_0 / 100
EOX = 3.9 * C.epsilon_0 / 100


def mu_univ(Vgs, Vt, tox):
    E = (Vgs + Vt + 0.2) / (6 * tox)
    return 540 / (1 + (E / 0.9e6) ** 1.85)


def channel_current(Vds, qloc, W, L, mu, Cox):
    """I_D = (W/L) mu C_ox * integral_0^Vds q(V) dV by numerical quadrature (current continuity along the
    channel turns dx into dV); qloc(V) is the local inversion charge divided by C_ox, in volts."""
    return W / L * mu * Cox * quad(qloc, 0, Vds, epsabs=0, epsrel=1e-12, limit=200)[0]


# ------------------------------------------------------------------ device
W, L, TOX, NA, VT0, VGS = 10e-4, 1e-4, 4e-7, 5e17, 0.4, 1.2
COX = EOX / TOX
v.check("Ex 09-09.1i", COX * 1e9)
pB = brentq(lambda p: NI * math.exp(p / VT) - NA, 0, 1)          # E_i - E_F where p = N_A
v.check("Ex 09-09.1a", pB)
Wd = math.sqrt(2 * EPS * 2 * pB / (Q * NA))
v.check("Ex 09-09.1b", Wd * 1e7)
m = 1 + (EPS / Wd) / COX
v.check("Ex 09-09.1c", m)
gam = math.sqrt(2 * Q * NA * EPS) / COX
v.check("Ex 09-09.1d", gam)
Eeff = (VGS + VT0 + 0.2) / (6 * TOX)
v.check("Ex 09-09.1e", Eeff / 1e6)
MU = mu_univ(VGS, VT0, TOX)
v.check("Ex 09-09.1f", MU)
VOV = VGS - VT0
qm = lambda Vc, vov=VOV, mm=m: vov - mm * Vc
I_small = channel_current(1e-4, qm, W, L, MU, COX)
v.check("Ex 09-09.1g", 1e-4 / I_small)
I01 = channel_current(0.1, qm, W, L, MU, COX)
v.check("Ex 09-09.1h", 0.1 / I01)

# ------------------------------------------------------------------ saturation
def isat_m(vov, mm, Wd_=W, L_=L, mu=MU, Cox=COX):
    res = minimize_scalar(lambda Vd: -channel_current(Vd, lambda Vc: vov - mm * Vc + 1e-9, Wd_, L_, mu, Cox),
                          bounds=(0.05 * vov / mm, 0.9999 * vov / mm), method="bounded", options={"xatol": 1e-8})
    return -res.fun, res.x


Idsat, Vdsat = isat_m(VOV, m)
v.check("Ex 09-09.2a", Vdsat)
v.check("Ex 09-09.2b", Idsat * 1e3)
Isq, _ = isat_m(VOV, 1.0)
v.check("Ex 09-09.2c", Isq * 1e3)
v.check("Ex 09-09.2d", 100 * (Isq / Idsat - 1))
v.check("Ex 09-09.2e", channel_current(0.3, qm, W, L, MU, COX) * 1e3)
v.check("Ex 09-09.2f", Vdsat / L)
v.check("Ex 09-09.2g", 1.6e7 / MU)
v.check("Ex 09-09.2i", (1.6e7 / MU) / (Vdsat / L))
v.check("Ex 09-09.2h", Idsat / 10 * 1e6)

# ------------------------------------------------------------------ body effect
def vt_body(Vsb, NA_=NA, Cox=COX, vt0=VT0):
    p = VT * math.log(NA_ / NI)
    return vt0 + math.sqrt(2 * Q * NA_ * EPS) / Cox * (math.sqrt(2 * p + Vsb) - math.sqrt(2 * p))


v.check("Ex 09-09.3a", vt_body(1.0))
alpha = (vt_body(1e-6) - vt_body(0)) / 1e-6
v.check("Ex 09-09.3b", alpha)
v.check("Ex 09-09.3c", VT0 + alpha)
v.check("Ex 09-09.3d", isat_m(VGS - vt_body(1.0), 1.0)[0] * 1e3)

# ------------------------------------------------------------------ exact bulk charge
VFB = VT0 - 2 * pB - gam * math.sqrt(2 * pB)
v.check("Ex 09-09.4a", VFB)
qb = lambda Vc, vg=VGS, vfb=VFB, g=gam, p=pB: vg - vfb - 2 * p - Vc - g * math.sqrt(2 * p + Vc)
Vds_b = brentq(qb, 0, 2, xtol=1e-14)
v.check("Ex 09-09.4b", Vds_b)
Ib = channel_current(Vds_b * (1 - 1e-7), lambda Vc: qb(Vc) + 1e-9, W, L, MU, COX)
v.check("Ex 09-09.4c", Ib * 1e3)
v.check("Ex 09-09.4d", 100 * (1 - Idsat / Ib))

# ------------------------------------------------------------------ CLM
def id_clm(Vds):
    dL = math.sqrt(2 * EPS * (Vds - Vdsat) / (Q * NA))
    return Idsat / (1 - dL / L), dL


Id12, dL = id_clm(1.2)
v.check("Ex 09-09.5a", dL * 1e7)
v.check("Ex 09-09.5b", 100 * dL / L)
v.check("Ex 09-09.5c", Id12 * 1e3)
h = 1e-4
gds = (id_clm(1.2 + h)[0] - id_clm(1.2 - h)[0]) / (2 * h)
v.check("Ex 09-09.5d", gds * 1e6)
v.check("Ex 09-09.5e", 1 / gds / 1e3)
v.check("Ex 09-09.5f", gds / Idsat)

# ------------------------------------------------------------------ small signal
hv = 1e-4
gm = (isat_m(VOV + hv, m)[0] - isat_m(VOV - hv, m)[0]) / (2 * hv)
v.check("Ex 09-09.6a", gm * 1e3)
v.check("Ex 09-09.6b", gm / Idsat)
v.check("Ex 09-09.6c", 1 / VT)
v.check("Ex 09-09.6i", (1 / VT) / (gm / Idsat))
v.check("Ex 09-09.6d", (m - 1) * gm * 1e3)
v.check("Ex 09-09.6e", W * L * COX * 1e15)


def channel_charge(vov, mm=m):
    """Total inversion charge W * integral of C_ox (vov - m V_c) dx along the saturated channel."""
    I, Vd = isat_m(vov, mm)
    sol = solve_ivp(lambda x, y: [I / (W * MU * COX * max(vov - mm * y[0], 1e-9))], [0, L * 0.999999], [0.0],
                    dense_output=True, rtol=1e-11, atol=1e-14, max_step=L / 400)
    xs = np.linspace(0, L * 0.999999, 4001)
    Vc = sol.sol(xs)[0]
    return W * trapezoid(COX * np.maximum(vov - mm * Vc, 0), xs)


Cgs = (channel_charge(VOV + 1e-3) - channel_charge(VOV - 1e-3)) / 2e-3
v.check("Ex 09-09.6f", Cgs * 1e15)
fT = brentq(lambda f: gm / (2 * math.pi * f * Cgs) - 1, 1e6, 1e12)
v.check("Ex 09-09.6g", fT / 1e9)
v.check("Ex 09-09.6h", gm / gds)

# ------------------------------------------------------------------ subthreshold
S = m * VT * math.log(10)
v.check("Ex 09-09.7a", S * 1e3)
v.check("T 09-09.a", VT * math.log(10) * 1e3)
v.check("T 09-09.b", 1 / (m * VT))
v.check("Ex 09-09.7b", VT0 / S)
v.check("Ex 09-09.7c", 1e-7 * (W / L) * 10 ** (-VT0 / S) * 1e12)
v.check("Ex 09-09.7d", (W / L) * MU * COX * (m - 1) * VT ** 2 * 1e6)
# cross-check: integrate n(x) = (ni^2/NA) exp(phi(x)/VT) through the depletion profile phi = phis (1 - x/W)^2 at phis = 2 phi_B
phis = 2 * pB
Wdep = math.sqrt(2 * EPS * phis / (Q * NA))
Qinv = Q * quad(lambda x: NI**2 / NA * math.exp(phis * (1 - x / Wdep) ** 2 / VT), 0, Wdep, epsabs=0, epsrel=1e-10, limit=400)[0]
pref_num = (W / L) * MU * VT * Qinv
v.assert_true("numerical weak-inversion charge reproduces the closed-form prefactor within 5%",
              abs(pref_num / ((W / L) * MU * COX * (m - 1) * VT ** 2) - 1) < 0.05, f"{pref_num:.4e}")
v.check("Ex 09-09.7e", 1e8 * 100e-9)
v.check("Ex 09-09.7f", 10 ** (0.15 / S))
for k_, val in (("P 09-09.a", 0.15), ("P 09-09.b", 0.84), ("P 09-09.c", 1e-5), ("P 09-09.d", 10), ("P 09-09.e", 155.6),
                ("P 09-09.f", 100), ("P 09-09.g", 288.4), ("P 09-09.h", 125), ("P 09-09.i", 60)):
    v.check(k_, val)   # quoted IRDS/Hu values (R-170, R-171)
v.check("P 09-09.j", 288.4 - 155.6)
v.check("P 09-09.k", (288.4 - 155.6) / math.log10(10e-9 / 100e-12))
for k_, val in ():
    v.check(k_, val)

# ------------------------------------------------------------------ Solutions
K = 1e-3
v.check("09-09.1a", channel_current(0.2, lambda Vc: 1.0 - Vc, 1.0, 1.0, K, 1.0) * 1e3)
v.check("09-09.1b", isat_m(1.0, 1.0, 1.0, 1.0, K, 1.0)[0] * 1e3)
C2 = EOX / 2e-7
v.check("09-09.2a", C2 * 1e6)
v.check("09-09.2b", brentq(lambda wl: 1e-4 / channel_current(1e-4, lambda Vc: 0.7 - Vc, wl, 1.0, 300, C2) - 100, 1, 1000))
v.check("09-09.3a", 315.1 / 100)
p4 = VT * math.log(1e18 / NI)
v.check("09-09.4a", p4)
W4 = math.sqrt(2 * EPS * 2 * p4 / (Q * 1e18))
v.check("09-09.4b", W4 * 1e7)
m4 = 1 + EPS / W4 / C2
v.check("09-09.4c", m4)
v.check("09-09.4d", isat_m(0.6, m4)[1])
C5 = EOX / 5e-7
v.check("09-09.5a", C5 * 1e9)
v.check("09-09.5b", math.sqrt(2 * Q * 1e17 * EPS) / C5)
v.check("09-09.5c", (vt_body(1e-6, 1e17, C5, 0) - vt_body(0, 1e17, C5, 0)) / 1e-6)
for vsb, k_ in ((0.5, "09-09.5d"), (1, "09-09.5e"), (2, "09-09.5f")):
    v.check(k_, vt_body(vsb, 1e17, C5, 0))
for vg, ke, km in ((0.8, "09-09.6a", "09-09.6b"), (1.2, "09-09.6c", "09-09.6d"), (1.8, "09-09.6e", "09-09.6f")):
    v.check(ke, (vg + 0.35 + 0.2) / (6 * 2e-7) / 1e6)
    v.check(km, mu_univ(vg, 0.35, 2e-7))
ia = isat_m(1.8 - 0.35, 1.0, 1.0, 1.0, mu_univ(1.8, 0.35, 2e-7), 1.0)[0]
ib = isat_m(0.8 - 0.35, 1.0, 1.0, 1.0, mu_univ(0.8, 0.35, 2e-7), 1.0)[0]
v.check("09-09.6g", ia / ib)
v.check("09-09.6h", ((1.8 - 0.35) / (0.8 - 0.35)) ** 2)
W7 = brentq(lambda w: isat_m(VOV, m, w, 0.5e-4)[0] - 1e-3, 1e-5, 1e-2)
v.check("09-09.7a", W7 * 1e4)
v.check("09-09.7b", (VOV / m) / 0.5e-4)
v.check("09-09.7c", (1.6e7 / MU) / ((VOV / m) / 0.5e-4))
dL8 = math.sqrt(2 * EPS * 0.5 / (Q * 5e17))
v.check("09-09.8a", dL8 * 1e7)
for Lx, k_ in ((0.5e-4, "09-09.8b"), (1e-4, "09-09.8c"), (2e-4, "09-09.8d")):
    v.check(k_, 100 * dL8 / Lx)
for vov, k_ in ((0.1, "09-09.9a"), (0.2, "09-09.9b"), (0.5, "09-09.9c")):
    I0 = isat_m(vov, 1.0, 1.0, 1.0, 1.0, 1.0)[0]
    g0 = (isat_m(vov + 1e-5, 1.0, 1.0, 1.0, 1.0, 1.0)[0] - isat_m(vov - 1e-5, 1.0, 1.0, 1.0, 1.0, 1.0)[0]) / 2e-5
    v.check(k_, g0 / I0)
v.check("09-09.9d", 1 / (1.3 * VT))
v.check("09-09.9e", brentq(lambda vov: 2 / vov - 1 / (1.3 * VT), 0.01, 1) * 1e3)
for Lx, k_ in ((2e-4, "09-09.10a"), (1e-4, "09-09.10b"), (0.5e-4, "09-09.10c")):
    v.check(k_, 3 * 300 * 0.5 / (4 * math.pi * 1.2 * Lx ** 2) / 1e9)
S11a, S11b = 1.1 * VT * math.log(10), 1.3 * VT * math.log(10)
v.check("09-09.11a", S11a * 1e3)
v.check("09-09.11b", S11b * 1e3)
v.check("09-09.11c", 1e-7 * 10 * 10 ** (-0.3 / S11b))
v.check("09-09.11d", 10 ** (0.15 / S11b))
T12 = 358.15
S12 = 1.3 * KB * T12 * math.log(10)
v.check("09-09.12a", S12 * 1e3)
vt12 = 0.3 - 1e-3 * (T12 - 300)
v.check("09-09.12b", vt12)
Ioff300 = 1e-6 * 10 ** (-0.3 / S11b)
Ioff85 = 1e-6 * 10 ** (-vt12 / S12)
v.check("09-09.12c", Ioff85)
v.check("09-09.12d", Ioff85 / Ioff300)
Cgs13 = (2 / 3) * W * L * COX + 2e-15
v.check("09-09.13a", Cgs13 * 1e15)
v.check("09-09.13b", 2e-15 * 11 * 1e15)
v.check("09-09.13c", (Cgs13 + 22e-15) * 1e15)
NA14 = 2e18
p14 = VT * math.log(NA14 / NI)
W14 = math.sqrt(2 * EPS * 2 * p14 / (Q * NA14))
m14 = 1 + EPS / W14 / COX
g14 = math.sqrt(2 * Q * NA14 * EPS) / COX
v.check("09-09.14a", m14)
v.check("09-09.14b", g14)
v.check("09-09.14c", VOV / m14)
vfb14 = VT0 - 2 * p14 - g14 * math.sqrt(2 * p14)
qb14 = lambda Vc: VGS - vfb14 - 2 * p14 - Vc - g14 * math.sqrt(2 * p14 + Vc)
vs14 = brentq(qb14, 0, 2, xtol=1e-14)
v.check("09-09.14d", vs14)
Ib14 = channel_current(vs14 * (1 - 1e-7), lambda Vc: qb14(Vc) + 1e-9, W, L, MU, COX)
Im14 = isat_m(VOV, m14)[0]
v.check("09-09.14e", 100 * (1 - Im14 / Ib14))
kp = 272.0e-6
WL15 = brentq(lambda wl: wl * kp / (2 * 1.25) * 0.2 ** 2 - 100e-6, 1, 1000)
v.check("09-09.15a", WL15)
gm15 = 2 * 100e-6 / 0.2
v.check("09-09.15b", gm15 * 1e3)
v.check("09-09.15g", gm15 / 100e-6)
v.check("09-09.15c", 1 / (0.04 * 100e-6) / 1e3)
v.check("09-09.15d", gm15 / (0.04 * 100e-6))
Cgs15 = (2 / 3) * WL15 * (1e-4) ** 2 * COX
v.check("09-09.15e", Cgs15 * 1e15)
v.check("09-09.15f", gm15 / (2 * math.pi * Cgs15) / 1e9)

# ------------------------------------------------------------------ Lab
# EKV-style interpolation I = 2 m K V_T^2 ln^2(1 + e^{V_ov/(2 m V_T)}): g_m/I_D falls to half of 1/(m V_T)
gmid = lambda vov: (lambda x: (math.exp(x) / (1 + math.exp(x))) / math.log(1 + math.exp(x)))(vov / (2 * m * VT)) / (m * VT)
v.check("Lab 09-09.a", brentq(lambda vov: gmid(vov) - 0.5 / (m * VT), -0.2, 1.0) * 1e3)
v.check("Lab 09-09.b", gmid(0.0))

v.finish()
