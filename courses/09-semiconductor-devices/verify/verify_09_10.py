#!/usr/bin/env python3
"""Verify every number in chapter 09-10 (short-channel effects and leakage), its solutions and lab.

Independent routes:
- velocity-saturated saturation current by shooting along the channel: for a trial current, integrate
  dx = dV / E(V) from the source (E from the piecewise velocity model) up to the point where the field reaches
  E_sat, and adjust the current until that point lies at x = L; no closed-form V_Dsat is used;
- long-channel saturation current by maximizing the numerically integrated channel current;
- linear-region currents by quadrature of the channel charge with the (1 + E/E_sat) correction;
- series resistance, minimum lengths, thresholds and dopings by root finding;
- the R_ds extraction by least-squares line fits;
- the GIDL field from displacement-field continuity at the oxide-silicon interface, solved for the voltage
  partition by root finding;
- dopant fluctuation by quadrature of the depth-weighted variance, cross-checked by a seeded Monte Carlo of
  random dopant positions.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-10", COURSE / "chapters" / "09-10-short-channel-effects-and-leakage.md",
                        COURSE / "solutions" / "09-10-solutions.md",
                        COURSE / "labs" / "09-10-lab" / "README.md")

Q = C.e
KB = C.k / C.e
VT = KB * 300
NI = 1.0e10
EPS = 11.7 * C.epsilon_0 / 100
EOX = 3.9 * C.epsilon_0 / 100
EG = 1.12


def mu_univ(Vgs, Vt, tox):
    E = (Vgs + Vt + 0.2) / (6 * tox)
    return 540 / (1 + (E / 0.9e6) ** 1.85)


def shoot_isat(vov, m, L, mu, vsat, Cox, W=1e-4):
    """Saturation current by shooting. Below E_sat the piecewise model gives v = mu E/(1 + E/E_sat), so
    I = W Cox (vov - m V) v fixes E(V) = I / (W Cox mu (vov - m V) - I/E_sat). The field reaches E_sat at
    V* where W Cox mu (vov - m V*) = 2 I/E_sat; the channel length needed is x(V*) = int_0^V* dV/E(V)."""
    Es = 2 * vsat / mu
    k = W * Cox * mu

    def length(I):
        Vstar = (vov - 2 * I / (k * Es)) / m
        return quad(lambda V: (k * (vov - m * V) - I / Es) / I, 0, Vstar, epsabs=0, epsrel=1e-12)[0], Vstar

    Imax = k * Es * vov / 2
    I = brentq(lambda I: length(I)[0] - L, Imax * 1e-9, Imax * (1 - 1e-12), xtol=1e-18, rtol=1e-14)
    return I, length(I)[1]


def long_isat(vov, m, L, mu, Cox, W=1e-4):
    f = lambda Vd: -W / L * mu * Cox * quad(lambda V: vov - m * V, 0, Vd, epsabs=0, epsrel=1e-12)[0]
    res = minimize_scalar(f, bounds=(0, 2 * vov / m), method="bounded", options={"xatol": 1e-10})
    return -res.fun


def lin_current(vds, vov, m, L, mu, vsat, Cox, W=1e-4):
    """Integrate I (1 + E/E_sat) dx = W Cox mu (vov - m V) dV along the channel."""
    Es = 2 * vsat / mu
    return W * Cox * mu * quad(lambda V: vov - m * V, 0, vds, epsabs=0, epsrel=1e-12)[0] / (L + vds / Es)


# ------------------------------------------------------------------ Example 09-10.1
COX = EOX / 2e-7
v.check("Ex 09-10.1a", COX * 1e6)
M, VTH, VGS, L50, VSAT = 1.2, 0.35, 1.0, 50e-7, 8e6
VOV = VGS - VTH
v.check("Ex 09-10.1b", (VGS + VTH + 0.2) / (6 * 2e-7) / 1e6)
MU = mu_univ(VGS, VTH, 2e-7)
v.check("Ex 09-10.1c", MU)
ES = 2 * VSAT / MU
v.check("Ex 09-10.1d", ES)
v.check("Ex 09-10.1e", ES * L50)
I1, Vd1 = shoot_isat(VOV, M, L50, MU, VSAT, COX)
v.check("Ex 09-10.1f", Vd1)
v.check("Ex 09-10.1g", VOV / M)
v.check("Ex 09-10.1h", I1 * 1e3)
Il1 = long_isat(VOV, M, L50, MU, COX)
v.check("Ex 09-10.1i", Il1 * 1e3)
v.check("Ex 09-10.1j", 100 * (1 - I1 / Il1))
v.check("Ex 09-10.1k", 1e-4 * 1.0 * 1.6e7 * COX * VOV * 1e3)
v.check("Ex 09-10.1l", 1e-4 * 0.5 * 1.6e7 * COX * VOV * 1e3)
v.check("T 09-10.a", 1.6e7)  # Hu §6.12, quoted
v.check("T 09-10.b", 8e6)    # Hu §6.9, quoted
v.check("T 09-10.c", 0.5)    # Hu §6.12, quoted
v.assert_true("B = 0.5 injection limit equals the velocity-saturation current without the m V_Dsat term",
              abs(0.5 * 1.6e7 * (VOV - M * Vd1) / VOV - I1 / (1e-4 * COX * VOV)) / VSAT < 1e-9)

# ------------------------------------------------------------------ Example 09-10.2
RS = 100.0
v.check("Ex 09-10.2a", RS * I1)
Ihu = I1 / (1 + RS * I1 / VOV)
v.check("Ex 09-10.2b", Ihu * 1e3)
v.check("Ex 09-10.2c", 100 * (1 - Ihu / I1))
Isc = brentq(lambda I: shoot_isat(VOV - I * RS, M, L50, MU, VSAT, COX)[0] - I, 1e-7, I1, xtol=1e-15)
v.check("Ex 09-10.2d", Isc * 1e3)
v.check("Ex 09-10.2e", 100 * (1 - Isc / I1))

# ------------------------------------------------------------------ Example 09-10.3 (Hu's roll-off model)
LD = 10e-7
rolloff = lambda L, vds, ld=LD: (vds + 0.4) * math.exp(-L / ld)
for L, ids in ((50e-7, "abcde"), (30e-7, "fghij"), (20e-7, "klmno")):
    a, b = rolloff(L, 0.05), rolloff(L, 1.0)
    dibl = -(np.gradient([-rolloff(L, x) for x in (0.05, 1.0)], [0.05, 1.0])[0])  # slope of V_t against V_DS
    v.check(f"Ex 09-10.3{ids[0]}", math.exp(-L / LD))
    v.check(f"Ex 09-10.3{ids[1]}", a * 1e3)
    v.check(f"Ex 09-10.3{ids[2]}", b * 1e3)
    v.check(f"Ex 09-10.3{ids[3]}", dibl * 1e3)
    v.check(f"Ex 09-10.3{ids[4]}", 10 ** (b / 0.080))

# ------------------------------------------------------------------ Example 09-10.4
for S, ids in ((0.060, "abc"), (0.070, "def"), (0.090, "ghi")):
    vt = brentq(lambda x: 10 ** (-x / S) - 1e-3, 0, 1)
    v.check(f"Ex 09-10.4{ids[0]}", vt)
    v.check(f"Ex 09-10.4{ids[1]}", 0.7 - vt)
    v.check(f"Ex 09-10.4{ids[2]}", 100 * (0.7 - vt) / 0.7)
m4 = 0.070 / (VT * math.log(10))
S85 = m4 * KB * 358.15 * math.log(10)
v.check("Ex 09-10.4j", S85 * 1e3)
v.check("Ex 09-10.4k", 10 ** (-0.21 / S85) / 10 ** (-0.21 / 0.070))


# ------------------------------------------------------------------ Example 09-10.5 (GIDL fields)
def gidl_fields(Vdg, tox):
    """Solve V_DG = E_g/q + V_ox with eps_ox E_ox = eps_s E_s (displacement continuity) for E_s."""
    Es = brentq(lambda E: EG + (EPS * E / EOX) * tox - Vdg, 0, 1e8)
    return EPS * Es / EOX, Es


for Vdg, ids in ((2.0, "abc"), (1.5, "def")):
    Eo, Es_ = gidl_fields(Vdg, 2e-7)
    v.check(f"Ex 09-10.5{ids[0]}", Eo / 1e6)
    v.check(f"Ex 09-10.5{ids[1]}", Es_ / 1e6)
    v.check(f"Ex 09-10.5{ids[2]}", EG / Es_ * 1e7)
v.check("Ex 09-10.5g", brentq(lambda V: gidl_fields(V, 2e-7)[1] - 1e6, 1.13, 5))
v.check("Ex 09-10.5h", brentq(lambda V: gidl_fields(V, 1.2e-7)[1] - 1e6, 1.13, 5))


# ------------------------------------------------------------------ Example 09-10.6 (dopant fluctuation)
def sigma_weighted(NA, Wd, Wg, Lg, Cox):
    var = quad(lambda x: NA * Wg * Lg * (Q * (1 - x / Wd) / (Cox * Wg * Lg)) ** 2, 0, Wd, epsabs=0, epsrel=1e-12)[0]
    return math.sqrt(var)


NA6, Wd6, Wg6, Lg6 = 5e18, 20e-7, 50e-7, 30e-7
N6 = NA6 * Wg6 * Lg6 * Wd6
v.check("Ex 09-10.6a", N6)
v.check("Ex 09-10.6b", math.sqrt(N6))
v.check("Ex 09-10.6c", 100 / math.sqrt(N6))
v.check("Ex 09-10.6d", Q * NA6 * Wd6 / COX)
v.check("Ex 09-10.6e", Q * math.sqrt(N6) / (COX * Wg6 * Lg6) * 1e3)
s6 = sigma_weighted(NA6, Wd6, Wg6, Lg6, COX)
v.check("Ex 09-10.6f", s6 * 1e3)
rng = np.random.default_rng(20261119)
counts = rng.poisson(N6, 40000)
dv = np.array([Q * np.sum(1 - rng.uniform(0, 1, n)) / (COX * Wg6 * Lg6) for n in counts])
v.assert_true("Monte Carlo dopant spread within 1.5% of the depth-weighted formula", abs(dv.std() / s6 - 1) < 0.015,
              f"MC {dv.std()*1e3:.2f} mV vs {s6*1e3:.2f} mV")

# ------------------------------------------------------------------ Practitioner keys (IRDS 2024 MM01, quoted)
for k_, val in (("P 09-10.a", 82), ("P 09-10.b", 70), ("P 09-10.c", 0.70), ("P 09-10.d", 0.60),
                ("P 09-10.e", 16), ("P 09-10.f", 12)):
    v.check(k_, val)

# ------------------------------------------------------------------ Solutions
E1 = 2 * 8e6 / 200
v.check("09-10.1a", E1)
for vov, k_ in ((0.1, "b"), (0.5, "c"), (1.0, "d")):
    v.check(f"09-10.1{k_}", brentq(lambda L: E1 * L - vov, 0, 1) * 1e7)

# P2: the fully velocity-saturated limit W C v_sat V_ov; the shooting solver is checked to approach the
# short-channel form W C v_sat (V_ov - m E_sat L) at a very short length
for vov, k_ in ((0.4, "a"), (0.8, "b")):
    v.check(f"09-10.2{k_}", 1e-4 * COX * 8e6 * vov * 1e3)
v.check("09-10.2c", (1e-4 * COX * 8e6 * 0.8) / (1e-4 * COX * 8e6 * 0.4))
v.assert_true("shooting current approaches W C v_sat (V_ov - m E_sat L) for E_sat L << V_ov",
              abs(shoot_isat(0.8, 1.2, 1e-7, 183.0, 8e6, COX)[0]
                  / (1e-4 * COX * 8e6 * (0.8 - 1.2 * 2 * 8e6 / 183.0 * 1e-7)) - 1) < 2e-3)

res3 = {}
for L, ids in ((1e-4, "abc"), (200e-7, "def"), (50e-7, "ghi"), (20e-7, "jkl")):
    I, Vd = shoot_isat(0.65, 1.2, L, 183.0, 8e6, COX)
    res3[L] = I
    v.check(f"09-10.3{ids[0]}", Vd)
    v.check(f"09-10.3{ids[1]}", I * 1e3)
    v.check(f"09-10.3{ids[2]}", I / long_isat(0.65, 1.2, L, 183.0, COX))
v.check("09-10.3m", res3[20e-7] / res3[200e-7])

Ep = 2 * 6e6 / 61
v.check("09-10.4a", Ep)
v.check("09-10.4b", Ep * 50e-7)
Ip, Vdp = shoot_isat(0.65, 1.2, 50e-7, 61.0, 6e6, COX)
v.check("09-10.4c", Vdp)
v.check("09-10.4d", Ip * 1e3)
v.check("09-10.4e", Ip / 0.4968e-3)

for vds, ids in ((0.05, "abcd"), (0.1, "efgh")):
    Il = lin_current(vds, 0.65, 1.2, 50e-7, 183.0, 1e30, COX)
    I = lin_current(vds, 0.65, 1.2, 50e-7, 183.0, 8e6, COX)
    v.check(f"09-10.5{ids[0]}", Il * 1e3)
    v.check(f"09-10.5{ids[1]}", Il / I)
    v.check(f"09-10.5{ids[2]}", I * 1e3)
    v.check(f"09-10.5{ids[3]}", vds / I)  # ohms for a 1 um wide device, i.e. ohm um

I0 = 0.4968e-3
v.check("09-10.6a", brentq(lambda R: 1 / (1 + R * I0 / 0.65) - 0.8, 0, 1e4))
I0full = shoot_isat(0.65, 1.2, 50e-7, 183.0, 8e6, COX)[0]
vint = brentq(lambda x: shoot_isat(x, 1.2, 50e-7, 183.0, 8e6, COX)[0] - 0.8 * I0full, 0.2, 0.65)
v.check("09-10.6c", vint)
v.check("09-10.6b", (0.65 - vint) / (0.8 * I0full))

Ld = np.array([0.5, 1.0])
f1 = np.polyfit(Ld, [265.8, 410.6], 1)
f2 = np.polyfit(Ld, [207.9, 280.3], 1)
v.check("09-10.7a", f1[0])
v.check("09-10.7b", f2[0])
v.check("09-10.7f", f1[1])
v.check("09-10.7g", f2[1])
dL = np.roots(f1 - f2)[0]
v.check("09-10.7c", dL)
v.check("09-10.7d", np.polyval(f1, dL))
v.check("09-10.7e", 1 / (10e-4 * f1[0] * 1e4 * 1.0) * 1e6)

# fit DIBL = A exp(-L/l_d) to the two measurements by solving both equations
ld8 = brentq(lambda ld: 0.020 * math.exp(40 / ld) - 0.090 * math.exp(25 / ld), 1, 100)
A8 = 0.020 * math.exp(40 / ld8)
v.check("09-10.8a", ld8)
v.check("09-10.8e", A8)
cpl = lambda L: A8 * math.exp(-L / ld8)
v.check("09-10.8b", (0.05 + 0.4) * cpl(25) * 1e3)
v.check("09-10.8c", (1.0 + 0.4) * cpl(25) * 1e3)
v.check("09-10.8d", brentq(lambda L: cpl(L) - 0.050, 1, 100))
v.assert_true("fitted model reproduces both DIBL measurements",
              abs(cpl(40) - 0.020) < 1e-12 and abs(cpl(25) - 0.090) < 1e-12)

ldf = lambda t, w, x: (t * w * x) ** (1 / 3)
v.check("09-10.9a", ldf(0.7, 0.7, 0.7))
v.check("09-10.9b", ldf(0.7, 1, 1))
prod = brentq(lambda p: ldf(0.9, p, 1) - 0.7, 1e-3, 1)
v.check("09-10.9c", prod)
v.check("09-10.9d", brentq(lambda f: ldf(0.9, f, f) - 0.7, 1e-3, 1))

ioff = lambda vt: 10 ** (-vt / 0.075)
v.check("09-10.10a", ioff(0.27) / ioff(0.20))
v.check("09-10.10b", ioff(0.34) / ioff(0.20))
v.check("09-10.10c", (0.7 - 0.27) / (0.7 - 0.20))
v.check("09-10.10d", (0.7 - 0.34) / (0.7 - 0.20))
v.check("09-10.10e", 0.05 + 0.95 * ioff(0.34) / ioff(0.20))

vts = 0.30 - 0.060 * (0.75 - 0.05)
v.check("09-10.11a", vts)
v.check("09-10.11b", ioff(vts) / ioff(0.30))
m11 = 0.075 / (VT * math.log(10))
S11 = m11 * KB * 358.15 * math.log(10)
v.check("09-10.11c", S11 * 1e3)
vt85 = vts - 0.8e-3 * (358.15 - 300)
v.check("09-10.11d", vt85)
v.check("09-10.11e", 10 ** (-vt85 / S11) / 10 ** (-vts / 0.075))
v.check("09-10.11f", 10 ** (-vt85 / S11) / 10 ** (-0.30 / 0.075))

for tox, ids in ((1.5e-7, "ac"), (3e-7, "bd")):
    v.check(f"09-10.12{ids[0]}", brentq(lambda V: gidl_fields(V, tox)[1] - 0.5e6, 1.13, 5))
    v.check(f"09-10.12{ids[1]}", gidl_fields(1.8, tox)[1] / 1e6)

Ig = 10 * (100e-7 * 20e-7)
v.check("09-10.13a", Ig * 1e9)
v.check("09-10.13b", 1e9 * 1e-9)
v.check("09-10.13c", 1e9 * Ig)
v.check("09-10.13d", 1e9 * (1e-9 + Ig) * 0.75)
v.check("09-10.13e", 1e9 * (10e-9 + 1.2 * Ig) * 0.75)
v.check("09-10.13f", 100 * 10e-9 / (10e-9 + 1.2 * Ig))

COX14 = EOX / 1.5e-7
Wg14 = Lg14 = 40e-7


def dev14(NA):
    pB = brentq(lambda p: NI * math.exp(p / VT) - NA, 0, 1)
    Wd = math.sqrt(2 * EPS * 2 * pB / (Q * NA))
    return pB, Wd, sigma_weighted(NA, Wd, Wg14, Lg14, COX14)


pB14, Wd14, s14 = dev14(1e18)
v.check("09-10.14a", pB14)
v.check("09-10.14b", Wd14 * 1e7)
v.check("09-10.14c", 1e18 * Wg14 * Lg14 * Wd14)
v.check("09-10.14d", s14 * 1e3)
v.check("09-10.14e", s14 * 1e3 * math.sqrt(0.04 * 0.04))
NA30 = brentq(lambda n: dev14(n)[2] - 0.030, 1e17, 1e20, rtol=1e-12)
v.check("09-10.14f", NA30)
Wd30 = dev14(NA30)[1]
v.check("09-10.14h", Wd30 * 1e7)
v.check("09-10.14g", NA30 * Wg14 * Lg14 * Wd30)

Lmin = brentq(lambda L: rolloff(L, 0.7, 8.0) - 0.075, 1, 100)
v.check("09-10.15a", Lmin)
v.check("09-10.15b", Lmin / 8.0)
r9 = rolloff(0.9 * Lmin, 0.7, 8.0)
v.check("09-10.15c", r9 * 1e3)
v.check("09-10.15d", 10 ** (r9 / 0.075) / 10 ** (rolloff(Lmin, 0.7, 8.0) / 0.075))
v.check("09-10.15e", 10 ** (r9 / 0.075))

# ------------------------------------------------------------------ Lab
Ia = shoot_isat(VOV, M, 2e-4, 183.0, 8e6, COX)[0]
Ib = shoot_isat(VOV, M, 20e-7, 183.0, 8e6, COX)[0]
v.check("Lab 09-10.a", Ia * 1e3)
v.check("Lab 09-10.b", Ib * 1e3)
v.check("Lab 09-10.c", Ib / Ia)
v.check("Lab 09-10.d", brentq(lambda L: shoot_isat(VOV, M, L, 183.0, 8e6, COX)[0]
                              / long_isat(VOV, M, L, 183.0, COX) - 0.5, 20e-7, 1e-4, xtol=1e-12) * 1e7)
sh = rolloff(30e-7, 1.0) - rolloff(30e-7, 0.05)
v.check("Lab 09-10.g", sh * 1e3)
v.check("Lab 09-10.e", 10 ** (sh / 0.080))
v.check("Lab 09-10.f", brentq(lambda d: 0.6 - 0.3 - d * 0.070, 0, 20))

v.finish()
