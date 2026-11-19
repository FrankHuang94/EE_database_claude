#!/usr/bin/env python3
"""Verify every number in chapter 09-08 (the MOS capacitor), its solutions and lab.

Independent routes:
- band positions and work functions from Boltzmann carrier densities (root finding for E_F);
- depletion widths by root finding on the voltage balance (not the closed-form quadratic root);
- the exact silicon charge Q_s(phi_s) by numerically integrating the first integral of Poisson's
  equation, E^2 = (2/eps) * integral of the space charge over potential (scipy quad), not the closed form F;
- threshold by locating n_s = N_A; inversion charge by integrating the electron density over depth on a
  numerically solved potential profile (solve_ivp), cross-checked against the bulk-charge split;
- capacitances by numerical differentiation of the computed charge with respect to gate voltage;
- extraction by root finding; thin-film values by series-capacitor arithmetic.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad, solve_ivp, trapezoid
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-08", COURSE / "chapters" / "09-08-mos-capacitor.md",
                        COURSE / "solutions" / "09-08-solutions.md",
                        COURSE / "labs" / "09-08-lab" / "README.md")

Q = C.e
VT = C.k * 300 / C.e
NI = 1.0e10
EPS = 11.7 * C.epsilon_0 / 100
EOX = 3.9 * C.epsilon_0 / 100
NC, NV, EG, CHI = 3.2e19, 1.8e19, 1.12, 4.05


def ec_minus_ef_p(NA):
    """E_C - E_F for a p-type body by root finding on p(E_F) = N_A (Boltzmann)."""
    efv = brentq(lambda x: NV * math.exp(-x / VT) - NA, 1e-6, EG)   # E_F - E_V
    return EG - efv


def ec_minus_ef_n(ND):
    return brentq(lambda x: NC * math.exp(-x / VT) - ND, 1e-6, EG)


def vfb_nplus(NA, psig=CHI):
    return psig - (CHI + ec_minus_ef_p(NA))


def depl_width(Vg, Vfb, NA, Cox):
    return brentq(lambda W: Vfb + Q * NA * W ** 2 / (2 * EPS) + Q * NA * W / Cox - Vg, 0, 1e-3, xtol=1e-16)


def phiB(N):
    return VT * math.log(N / NI)


def Qs_exact(phi, NA):
    """Total silicon charge (C/cm^2) from E_s^2 = (2/eps) * integral_0^phi rho_eff dphi (quad)."""
    n0 = NI ** 2 / NA
    f = lambda p: Q * (NA * (1 - math.exp(-p / VT)) + n0 * (math.exp(p / VT) - 1))
    I = quad(f, 0, phi, epsabs=0, epsrel=1e-12, limit=200)[0]
    return -math.copysign(1, phi) * math.sqrt(2 * EPS * abs(I))


def phis_of_Vg(Vg, Vfb, NA, Cox, lo=-1.0, hi=2.0):
    return brentq(lambda p: Vfb + p - Qs_exact(p, NA) / Cox - Vg if abs(p) > 1e-12 else Vfb - Vg, lo, hi, xtol=1e-13)


def inversion_charge_profile(phis, NA):
    """Integrate the electron density over depth: solve d(phi)/dx = -E(phi) from the surface inward."""
    n0 = NI ** 2 / NA
    Ef = lambda p: math.sqrt(2 / EPS * Q * (NA * (p / VT * VT - VT + VT * math.exp(-p / VT))
                                            + n0 * (VT * math.exp(p / VT) - p - VT)))
    # integrate n dx = n dphi / E over phi from phi_s down to a small value
    integrand = lambda p: n0 * (math.exp(p / VT) - 1) / Ef(p) if p > 1e-9 else 0.0
    return Q * quad(integrand, 1e-6, phis, epsabs=0, epsrel=1e-10, limit=400)[0]


# ------------------------------------------------------------------ Example 1
NA, TOX = 1e17, 10e-7
COX = EOX / TOX
v.check("T 09-08.a", EOX)
v.check("Ex 09-08.1a", COX * 1e9)
v.check("Ex 09-08.1f", EG - ec_minus_ef_p(NA))
v.check("Ex 09-08.1b", ec_minus_ef_p(NA))
VFB = vfb_nplus(NA)
v.check("Ex 09-08.1c", VFB)
v.check("Ex 09-08.1d", vfb_nplus(NA, CHI + EG))
v.check("Ex 09-08.1e", -Q * 5e10 / COX * 1e3)

# ------------------------------------------------------------------ Example 2
W0 = depl_width(0.0, VFB, NA, COX)
v.check("Ex 09-08.2a", W0 * 1e7)
v.check("Ex 09-08.2b", Q * NA * W0 ** 2 / (2 * EPS))
pB = phiB(NA)
v.check("Ex 09-08.2c", pB)
# threshold: surface electron density equals N_A
n0 = NI ** 2 / NA
phit = brentq(lambda p: n0 * math.exp(p / VT) - NA, 0.1, 1.5, xtol=1e-14)
v.check("Ex 09-08.2d", phit)
Wmax = math.sqrt(2 * EPS * phit / (Q * NA))
v.check("Ex 09-08.2e", Wmax * 1e4)
Qd = Q * NA * Wmax
v.check("Ex 09-08.2f", Qd)
v.check("Ex 09-08.2g", Qd / COX)
VT0 = VFB + phit + Qd / COX
v.check("Ex 09-08.2h", VT0)
v.check("Ex 09-08.2i", -COX * (2 - VT0))
v.check("Ex 09-08.2j", COX * (2 - VT0) / Q)

# ------------------------------------------------------------------ Example 3 (exact)
v.check("Ex 09-08.3a", -Qs_exact(phit, NA))
ph2 = phis_of_Vg(2.0, VFB, NA, COX, 0.5, 1.5)
v.check("Ex 09-08.3b", ph2)
v.check("Ex 09-08.3c", (ph2 - phit) * 1e3)
Qs2 = Qs_exact(ph2, NA)
v.check("Ex 09-08.3d", Qs2)
Qb2 = -math.sqrt(2 * Q * EPS * NA * (ph2 - VT))
v.check("Ex 09-08.3e", Qb2)
Qi2 = Qs2 - Qb2
v.check("Ex 09-08.3f", Qi2)
v.assert_true("inversion charge by depth integration agrees with the bulk-charge split (2%)",
              abs(inversion_charge_profile(ph2, NA) / abs(Qi2) - 1) < 0.02)
v.check("Ex 09-08.3g", -Qi2 / Q)
v.check("Ex 09-08.3h", 100 * (COX * (2 - VT0) / abs(Qi2) - 1))
v.check("Ex 09-08.3i", 100 * (1 - abs(Qi2) / (COX * (2 - VT0))))


def qinv_of_phi(p):
    return abs(Qs_exact(p, NA)) - math.sqrt(2 * Q * EPS * NA * (p - VT))


h = 1e-5
d10 = (math.log10(qinv_of_phi(ph2 + h)) - math.log10(qinv_of_phi(ph2 - h))) / (2 * h)
v.check("T 09-08.c", 1 / d10 * 1e3)
v.check("T 09-08.b", 2 * VT * math.log(10) * 1e3)

# ------------------------------------------------------------------ Example 4 (C-V)
LD = math.sqrt(EPS * VT / (Q * NA))
v.check("Ex 09-08.4a", LD * 1e7)
dp = 1e-5
Cs_fb = -(Qs_exact(dp, NA) - Qs_exact(-dp, NA)) / (2 * dp)
v.check("Ex 09-08.4b", Cs_fb * 1e9)
Cfb = 1 / (1 / COX + 1 / Cs_fb)
v.check("Ex 09-08.4c", Cfb * 1e9)
v.check("Ex 09-08.4d", Cfb / COX)
v.check("Ex 09-08.4e", EPS / Wmax * 1e9)
Cmin = 1 / (1 / COX + Wmax / EPS)
v.check("Ex 09-08.4f", Cmin * 1e9)
v.check("Ex 09-08.4g", Cmin / COX)


def cmin_ratio(N, Cox):
    W = math.sqrt(2 * EPS * 2 * phiB(N) / (Q * N))
    return (1 / (1 / Cox + W / EPS)) / Cox


Cox_m = 345.3e-9
v.check("Ex 09-08.4h", EOX / Cox_m * 1e7)
v.check("Ex 09-08.4i", brentq(lambda N: cmin_ratio(N, Cox_m) - 0.2242, 1e14, 1e19))

# ------------------------------------------------------------------ Example 5
dV = -1.10 - VFB
v.check("Ex 09-08.5a", dV)
Qox = -COX * dV
v.check("Ex 09-08.5b", Qox)
v.check("Ex 09-08.5c", Qox / Q)
v.check("Ex 09-08.5d", Qox / Q / 1e10)
nsurf = 2 / (5.431e-8) ** 2
v.check("Ex 09-08.5e", nsurf)
v.check("Ex 09-08.5f", nsurf / (Qox / Q))

# ------------------------------------------------------------------ Example 6
Eox = 1.0 / 2e-7
v.check("Ex 09-08.6a", Eox / 1e6)
Wp = EOX * Eox / (Q * 1e20)
v.check("Ex 09-08.6b", Wp * 1e7)
v.check("Ex 09-08.6c", Q * 1e20 * Wp ** 2 / (2 * EPS))
# T_oxe by series capacitances: oxide, poly depletion (eps_s/Wp), inversion layer (eps_s/T_inv)
Ceff = 1 / (2e-7 / EOX + Wp / EPS + 1.5e-7 / EPS)
v.check("Ex 09-08.6d", EOX / Ceff * 1e7)
v.check("Ex 09-08.6e", Ceff / (EOX / 2e-7))
Cmet = 1 / (2e-7 / EOX + 1.5e-7 / EPS)
v.check("Ex 09-08.6f", EOX / Cmet * 1e7)
v.check("Ex 09-08.6g", 100 * (EOX / Ceff - 2e-7) / 2e-7)

# ------------------------------------------------------------------ Example 7
v.check("Ex 09-08.7a", 1e3 * 0.01)
v.check("Ex 09-08.7b", 1e3 * 0.01 / 10)
v.check("Ex 09-08.7c", EOX / 1e-7 * 1e6)
v.check("Ex 09-08.7d", brentq(lambda t: 24 * C.epsilon_0 / t - EOX / 1e-7 * 1e4, 1e-10, 1e-7) * 1e9)
v.check("Ex 09-08.7e", brentq(lambda t: 21.2 * C.epsilon_0 / t - EOX / 1e-7 * 1e4, 1e-10, 1e-7) * 1e9)
Cstack = 1 / (0.5e-7 / EOX + 2e-7 / (21.2 * C.epsilon_0 / 100))
eot = EOX / Cstack * 1e7
v.check("Ex 09-08.7f", eot)
Ccet = 1 / (1 / Cstack + 1.5e-7 / EPS)
cet = EOX / Ccet * 1e7
v.check("Ex 09-08.7g", cet)
v.check("Ex 09-08.7h", cet - 1.0)
v.check("Ex 09-08.7i", 2.5 / eot)
v.check("Ex 09-08.7j", eot + 0.3)
for k_, val in (("P 09-08.a", 1.9), ("P 09-08.b", 0.9), ("P 09-08.c", 1.0), ("P 09-08.d", 0.9)):
    v.check(k_, val)

# ------------------------------------------------------------------ Solutions
v.check("09-08.1d", ec_minus_ef_p(1e16))
v.check("09-08.1a", vfb_nplus(1e16))
v.check("09-08.1e", ec_minus_ef_n(1e17))
v.check("09-08.1f", CHI + ec_minus_ef_n(1e17))
v.check("09-08.1b", CHI + EG - (CHI + ec_minus_ef_n(1e17)))
v.check("09-08.1c", vfb_nplus(1e16, 4.6))
C3 = EOX / 3e-7
v.check("09-08.2a", C3 * 1e9)
Cst = 1 / (0.6e-7 / EOX + 4e-7 / (21.2 * C.epsilon_0 / 100))
v.check("09-08.2b", EOX / Cst * 1e7)
v.check("09-08.2c", Cst * 1e9)
v.check("09-08.2d", 4.6 / 3)
v.check("09-08.2e", Cst / C3)
C5 = EOX / 5e-7
v.check("09-08.3a", C5 * 1e9)
v.check("09-08.3b", C5 * 1.5)
v.check("09-08.3c", C5 * 1.5 / Q)
for Vg, kw, kp in ((-0.5, "09-08.4a", "09-08.4b"), (0.2, "09-08.4c", "09-08.4d")):
    W = depl_width(Vg, VFB, NA, COX)
    v.check(kw, W * 1e7)
    v.check(kp, Q * NA * W ** 2 / (2 * EPS))


def vt_of(N, Cox, psig=CHI):
    p = 2 * phiB(N)
    return vfb_nplus(N, psig) + p + math.sqrt(2 * Q * N * EPS * p) / Cox


for N, kf, kt in ((1e16, "09-08.5a", "09-08.5b"), (1e17, "09-08.5c", "09-08.5d"), (1e18, "09-08.5e", "09-08.5f")):
    v.check(kf, vfb_nplus(N))
    v.check(kt, vt_of(N, C3))
v.check("09-08.6a", brentq(lambda N: vt_of(N, C3) - 0.4, 1e16, 1e19))
v.check("09-08.7a", phiB(1e17))
vfp = CHI + EG - (CHI + ec_minus_ef_n(1e17))
v.check("09-08.7b", vfp)
v.check("09-08.7c", vfp - 2 * phiB(1e17) - math.sqrt(2 * Q * 1e17 * EPS * 2 * phiB(1e17)) / C3)
C2 = EOX / 2e-7
v.check("09-08.8a", C2 * 1e6)
v.check("09-08.8b", C2 * 0.8)
ns8 = C2 * 0.8 / Q
v.check("09-08.8c", ns8)
v.check("09-08.8d", 1 / (Q * ns8 * 250))
v.check("09-08.8e", 10 / (Q * ns8 * 250) / 1e3)
for dvv, kp, kq, ks, kr in ((0.5, "09-08.9a", "09-08.9b", "09-08.9c", "09-08.9d"),
                            (1.5, "09-08.9e", "09-08.9f", "09-08.9g", "09-08.9h")):
    p = phis_of_Vg(VT0 + dvv, VFB, NA, COX, 0.5, 1.5)
    qi = abs(Qs_exact(p, NA)) - math.sqrt(2 * Q * EPS * NA * (p - VT))
    v.check(kp, p)
    v.check(kq, qi)
    v.check(ks, COX * dvv)
    v.check(kr, qi / (COX * dvv))
# 10
N10 = 5e16
v.check("09-08.10a", C5 * 1e9)
vf10 = vfb_nplus(N10)
v.check("09-08.10b", vf10)
v.check("09-08.10c", math.sqrt(EPS * VT / (Q * N10)) * 1e7)
Csfb10 = -(Qs_exact(dp, N10) - Qs_exact(-dp, N10)) / (2 * dp)
v.check("09-08.10d", 1 / (1 / C5 + 1 / Csfb10) * 1e9)
Wd10 = math.sqrt(2 * EPS * 2 * phiB(N10) / (Q * N10))
v.check("09-08.10e", Wd10 * 1e7)
v.check("09-08.10f", 1 / (1 / C5 + Wd10 / EPS) * 1e9)
W010 = depl_width(0.0, vf10, N10, C5)
v.check("09-08.10g", W010 * 1e7)
v.check("09-08.10h", 1 / (1 / C5 + W010 / EPS) * 1e9)
# slope of 1/C^2 from two depletion points
c_at = lambda Vg: 1 / (1 / C5 + depl_width(Vg, vf10, N10, C5) / EPS)
v.check("09-08.10i", (1 / c_at(-0.5) ** 2 - 1 / c_at(-0.7) ** 2) / 0.2)
# 11
Cox11 = 69.06e-12 / 1e-4
v.check("09-08.11a", EOX / Cox11 * 1e7)
v.check("09-08.11b", 5.25 / 69.06)
N11 = brentq(lambda N: cmin_ratio(N, Cox11) * 69.06 - 5.25, 1e14, 1e19)
v.check("09-08.11c", N11)
vf11 = vfb_nplus(N11)
v.check("09-08.11d", vf11)
v.check("09-08.11e", -1.05 - vf11)
v.check("09-08.11f", -Cox11 * (-1.05 - vf11))
v.check("09-08.11g", -Cox11 * (-1.05 - vf11) / Q)
# 12
C20 = EOX / 20e-7
v.check("09-08.12a", C20 * 1e9)
v.check("09-08.12b", C20 * 0.15)
v.check("09-08.12c", C20 * 0.15 / Q)
v.check("09-08.12d", nsurf / (C20 * 0.15 / Q))
# 13
for Np, kw, kp, kt in ((5e19, "09-08.13a", "09-08.13b", "09-08.13c"), (1e20, "09-08.13d", "09-08.13e", "09-08.13f"),
                       (3e20, "09-08.13g", "09-08.13h", "09-08.13i")):
    Wpp = EOX * 5e6 / (Q * Np)
    v.check(kw, Wpp * 1e7)
    v.check(kp, Q * Np * Wpp ** 2 / (2 * EPS))
    Ce = 1 / (1.5e-7 / EOX + Wpp / EPS + 1.5e-7 / EPS)
    v.check(kt, EOX / Ce * 1e7)
# 14
Wdd = depl_width(3.0, VFB, NA, COX)
v.check("09-08.14a", Wdd * 1e4)
v.check("09-08.14b", Q * NA * Wdd ** 2 / (2 * EPS))
v.check("09-08.14c", (1 / (1 / COX + Wdd / EPS)) / COX)
Qf = COX * (3.0 - VT0)
v.check("09-08.14d", Qf)
Jg = Q * NI * Wdd / (2 * 1e-6)
v.check("09-08.14e", Jg)
v.check("09-08.14f", Qf / Jg)
v.check("09-08.14g", Qf / (Q * NI * Wmax / (2 * 1e-6)))
# 15
for cet_, k_ in ((1.0, "09-08.15a"), (0.9, "09-08.15b")):
    v.check(k_, brentq(lambda t: 0.4 + t * 3.9 / 21.2 + 0.3 - cet_, 0, 10))
v.check("09-08.15d", 1.5 * 3.9 / 21.2)
v.check("09-08.15c", brentq(lambda il: il + 1.5 * 3.9 / 21.2 + 0.3 - 0.9, 0, 1))

# ------------------------------------------------------------------ Lab
# (a) phi_s above 2 phi_B where inversion charge equals depletion (bulk) charge
pe = brentq(lambda p: qinv_of_phi(p) - math.sqrt(2 * Q * EPS * NA * (p - VT)), phit, 1.5, xtol=1e-13)
v.check("Lab 09-08.a", (pe - phit) * 1e3)
Vge = VFB + pe - Qs_exact(pe, NA) / COX
v.check("Lab 09-08.b", Vge)
v.check("Lab 09-08.c", VT0 + Qd / COX)
# (d) gate voltage where the exact inversion charge is 1e11 cm^-2 (a current-like threshold)
p11 = brentq(lambda p: qinv_of_phi(p) - Q * 1e11, 0.6, 1.2, xtol=1e-13)
LABD = VFB + p11 - Qs_exact(p11, NA) / COX
v.check("Lab 09-08.d", LABD)
# (e) C-V stretch from 1e11 cm^-2 of positive interface charge at midgap: flat-band shift
v.check("Lab 09-08.e", -Q * 1e11 / COX * 1e3)

v.finish()
