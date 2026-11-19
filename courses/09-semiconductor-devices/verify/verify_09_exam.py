#!/usr/bin/env python3
"""Verify every number in the Course 09 final-exam solutions.

Independent routes (not the hand formulas of the solutions):
- carrier densities by solving charge neutrality with root finding, and Fermi-level positions by inverting the
  Boltzmann expressions; the Poisson probability from scipy.stats;
- depletion widths by solving charge balance plus the total potential drop of the step junction;
- the diode saturation current by solving the minority-hole diffusion equation as a boundary-value problem;
- the MOS threshold by root finding on the gate voltage that brings the surface potential to 2 phi_B;
- MOSFET currents by integrating the channel charge and maximizing over V_DS; the short-channel current by
  shooting along the channel with the piecewise velocity model;
- the inverter switching threshold by solving current balance; the ring period by a transition-by-transition
  simulation;
- drift-layer designs by root finding on the breakdown condition; the solar-cell optimum by maximizing power.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.integrate import quad, solve_bvp
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import poisson

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("09-exam", HERE.parent / "exam" / "solutions.md")

Q = C.e
VT = 0.025852
NI = 1e10
EPS = 11.7 * C.epsilon_0 / 100
EOX = 3.9 * C.epsilon_0 / 100
NC, NV, EG = 3.2e19, 1.8e19, 1.12
HC = 1.2398
mun = lambda N: 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)
mup = lambda N: 48 + 402 / (1 + (N / 6.3e16) ** 0.76)

# 1
v.check("X09.1a", 8 / (5.431e-8) ** 3)
acc = (2 / 0.98 + 4 / 0.19) / 6               # mean acceleration per unit force over the six valleys
v.check("X09.1b", 1 / acc)
v.check("X09.1c", brentq(lambda lam: HC / lam - EG, 0.1, 10))


# 2
def neutral(ND, NA):
    n = brentq(lambda n: n - NI ** 2 / n - (ND - NA), 1, 1e20, xtol=1e-6, rtol=1e-14)
    return n, NI ** 2 / n


n0, p0 = neutral(2e16, 0)
v.check("X09.2a", n0)
v.check("X09.2b", p0)
v.check("X09.2c", brentq(lambda e: NI * math.exp(e / VT) - n0, 0, 1))
v.check("X09.2d", brentq(lambda e: NC * math.exp(-e / VT) - n0, 0, 1))
n1, p1 = neutral(2e16, 1.5e16)
v.check("X09.2e", n1)
v.check("X09.2f", p1)
v.check("X09.2g", brentq(lambda e: NI * math.exp(e / VT) - n1, 0, 1))
mean = 1e18 * (20e-7 * 20e-7 * 10e-7)
v.check("X09.2h", mean)
v.check("X09.2i", poisson.pmf(0, mean))
v.check("X09.2j", poisson.std(mean) / mean)

# 3
mu3 = mun(1e16)
rho = 1 / (Q * 1e16 * mu3)
v.check("X09.3a", mu3)
v.check("X09.3b", rho)
v.check("X09.3c", rho / 2e-4)
v.check("X09.3d", 50 * rho / 2e-4 / 1e3)
mp = mup(1e16)
Dp = mp * VT
v.check("X09.3e", mp)
v.check("X09.3f", Dp)
v.check("X09.3g", math.sqrt(Dp * 1e-6) * 1e4)

# 4
tau4 = 1 / (1e-15 * 1.65e7 * 1e13)
v.check("X09.4a", tau4 * 1e6)
dp4 = brentq(lambda d: 1e20 - d / tau4, 0, 1e18)
v.check("X09.4b", dp4)
v.check("X09.4c", dp4 / 1e16)
Efn = brentq(lambda e: NI * math.exp(e / VT) - (1e16 + dp4), 0, 1)
Efp = brentq(lambda e: NI * math.exp(e / VT) - (1e4 + dp4), 0, 1)
v.check("X09.4d", Efn + Efp)
v.check("X09.4e", math.sqrt(Dp * tau4) * 1e4)

# 5
NA5, ND5 = 1e18, 1e16
vbi = brentq(lambda V: NI ** 2 / ND5 * math.exp(V / VT) - NA5, 0, 2)   # p on n side = N_A e^(-Vbi/VT) balance


def width(Vtot):
    xn = brentq(lambda x: Q / (2 * EPS) * (ND5 * x ** 2 + NA5 * (ND5 * x / NA5) ** 2) - Vtot, 0, 1e-2)
    return xn * (1 + ND5 / NA5)


v.check("X09.5a", vbi)
v.check("X09.5b", width(vbi) * 1e4)
W10 = width(vbi + 10)
v.check("X09.5c", W10 * 1e4)
v.check("X09.5d", 2 * (vbi + 10) / W10)
v.check("X09.5e", EPS / W10 * 1e9)

# 6: hole diffusion in the long N side, solved as a BVP: Dp p'' = p/tau, p(0) = pn0, p(10 Lp) = 0
Lp = math.sqrt(Dp * 1e-6)
pn0 = NI ** 2 / 1e16
xs = np.linspace(0, 10 * Lp, 400)
sol = solve_bvp(lambda x, y: np.vstack([y[1], y[0] / Lp ** 2]), lambda a, b: np.array([a[0] - pn0, b[0]]),
                xs, np.vstack([pn0 * np.exp(-xs / Lp), -pn0 / Lp * np.exp(-xs / Lp)]), tol=1e-10)
I0 = Q * 1e-4 * Dp * (-sol.sol(0)[1])
v.check("X09.6a", I0)
v.check("X09.6b", brentq(lambda V: I0 * (math.exp(V / VT) - 1) - 1e-3, 0, 1.5))
v.check("X09.6c", VT / 1e-3)
v.check("X09.6d", 1e-6 / 2 * (1e-3 / VT) * 1e9)
v.check("X09.6e", 15 * (1e17 / 1e16) ** 0.6)

# 7
Dn = mun(1e17) * VT
IS = Q * 1e-6 * NI ** 2 * Dn / quad(lambda x: 1e17, 0, 0.1e-4)[0]   # Gummel number
v.check("X09.7a", Dn)
v.check("X09.7b", IS)
IC = IS * math.exp(0.7 / VT)
v.check("X09.7c", IC * 1e3)
DpE = mup(1e19) * VT
v.check("X09.7d", (Dn * 1e19 * 0.1e-4) / (DpE * 1e17 * 0.1e-4))
tB = (0.1e-4) ** 2 / (2 * Dn)
v.check("X09.7e", tB * 1e12)
v.check("X09.7f", 1 / (2 * math.pi * tB) / 1e9)
v.check("X09.7g", IC / VT * 1e3)

# 8
COX = EOX / 4e-7
NA8 = 5e17
pB = brentq(lambda p: NI * math.exp(p / VT) - NA8, 0, 1)
efev = brentq(lambda e: NV * math.exp(-e / VT) - NA8, 0, 1)
vfb = -(EG - efev)
v.check("X09.8a", COX * 1e9)
v.check("X09.8b", pB)
v.check("X09.8j", 2 * pB)
v.check("X09.8c", efev)
v.check("X09.8d", vfb)
Qd = lambda ps: math.sqrt(2 * Q * NA8 * EPS * ps)
vt = brentq(lambda Vg: brentq(lambda ps: vfb + ps + Qd(ps) / COX - Vg, 1e-12, 5) - 2 * pB, vfb + 0.01, 1.5)
v.check("X09.8e", Qd(2 * pB) / COX)
v.check("X09.8f", vt)
Wd = Qd(2 * pB) / (Q * NA8)
v.check("X09.8g", Wd * 1e7)
cmin = 1 / (1 / COX + Wd / EPS)
v.check("X09.8h", cmin * 1e9)
v.check("X09.8i", cmin / COX)

# 9: integrate the channel charge, maximize over V_DS
W9, L9, mu9, m9, vt9 = 10e-4, 1e-4, 300, 1.25, 0.35
vov = 1.0 - vt9
Id = lambda Vd: W9 / L9 * mu9 * COX * quad(lambda Vc: vov - m9 * Vc, 0, Vd)[0]
r9 = minimize_scalar(lambda Vd: -Id(Vd), bounds=(0, 1), method="bounded", options={"xatol": 1e-10})
v.check("X09.9a", r9.x)
v.check("X09.9b", -r9.fun * 1e3)
h = 1e-6
Isat = lambda vo: W9 / (2 * m9 * L9) * mu9 * COX * vo ** 2
v.check("X09.9c", (Isat(vov + h) - Isat(vov - h)) / (2 * h) * 1e3)
S9 = m9 * VT * math.log(10)
v.check("X09.9d", S9 * 1e3)
v.check("X09.9e", 1e-7 * (W9 / L9) * 10 ** (-vt9 / S9))

# 10: shooting with the piecewise velocity model
COX2 = EOX / 2e-7
mu10, vs10, m10, L10, vov10 = 200.0, 8e6, 1.2, 50e-7, 0.6
Es = 2 * vs10 / mu10
k = 1e-4 * COX2 * mu10


def length(I):
    Vs = (vov10 - 2 * I / (k * Es)) / m10
    return quad(lambda V: (k * (vov10 - m10 * V) - I / Es) / I, 0, Vs)[0], Vs


I10 = brentq(lambda I: length(I)[0] - L10, k * Es * vov10 / 2 * 1e-9, k * Es * vov10 / 2 * (1 - 1e-12), xtol=1e-18)
v.check("X09.10a", Es)
v.check("X09.10b", Es * L10)
v.check("X09.10c", length(I10)[1])
v.check("X09.10d", I10 * 1e3)
dvt = (0.75 + 0.4) * math.exp(-30 / 8)
v.check("X09.10e", dvt * 1e3)
v.check("X09.10f", 10 ** (dvt / 0.075))


# 11: inverter current balance
def isq(vgs, vds, kk, vt_):
    vo = vgs - vt_
    if vo <= 0:
        return 0.0
    return kk * (vo * vds - vds ** 2 / 2) if vds < vo else kk * vo ** 2 / 2


def vout(vin, r, vdd=0.9, vt_=0.25):
    if vin <= vt_:
        return vdd
    if vin >= vdd - vt_:
        return 0.0
    return brentq(lambda vo: r * isq(vin, vo, 1, vt_) - isq(vdd - vin, vdd - vo, 1, vt_), 0, vdd, xtol=1e-14)


v.check("X09.11a", brentq(lambda x: vout(x, 2.5) - x, 0.26, 0.64, xtol=1e-14))
tf, tr = 2e-15 * 0.8 / (2 * 120e-6), 2e-15 * 0.8 / (2 * 90e-6)
v.check("X09.11b", (tf + tr) / 2 * 1e12)
t, falling, back = 0.0, True, []
for i in range(6 * 31):
    t += tf if falling else tr
    falling = not falling
    if (i + 1) % 31 == 0:
        back.append(t)
v.check("X09.11c", 1 / (back[2] - back[0]) / 1e9)
v.check("X09.11d", 0.15 * 1e8 * 2e-15 * 0.8 ** 2 * 2e9)
v.check("X09.11e", (1 / 0.7) ** 2)

# 12
lam = math.sqrt(3 * 6 * 1 / 2 + 6 ** 2 / 8)
v.check("X09.12a", lam)
e12 = math.exp(-24 / (2 * lam))
u1, u2 = 2 * math.sqrt(0.2 * 0.25) * e12, 2 * math.sqrt(0.2 * 0.9) * e12
v.check("X09.12b", e12)
v.check("X09.12c", u1 * 1e3)
v.check("X09.12d", u2 * 1e3)
v.check("X09.12e", (u2 - u1) / 0.65 * 1e3)


def umin_exact(L, lm, a, b):
    x = np.linspace(0, L, 20001)
    return ((a * np.sinh((L - x) / lm) + b * np.sinh(x / lm)) / np.sinh(L / lm)).min()


v.assert_true("approximate DIBL within 5% of the exact barrier minimum",
              abs((umin_exact(24, lam, 0.2, 0.9) - umin_exact(24, lam, 0.2, 0.25)) / (u2 - u1) - 1) < 0.05)
v.check("X09.12f", 2 * 46 + 7)
nf = next(n for n in range(1, 20) if n * 99 >= 300)
v.check("X09.12g", nf)
v.check("X09.12h", nf * 99)
v.check("X09.12i", 0.25e-3 * 500 / 8 * 1e3)


# 13
def drift(V, Ec, er, mu):
    e_ = er * C.epsilon_0 / 100
    N = brentq(lambda n: e_ * Ec ** 2 / (2 * Q * n) - V, 1e10, 1e20, rtol=1e-12)
    W = e_ * Ec / (Q * N)
    return N, W, W / (Q * mu * N)


s13 = drift(1700, 2.0e5, 11.7, 1350)
c13 = drift(1700, 2.5e6, 9.96, 1000)
for ids, d in (("abc", s13), ("def", c13)):
    v.check(f"X09.13{ids[0]}", d[0])
    v.check(f"X09.13{ids[1]}", d[1] * 1e4)
    v.check(f"X09.13{ids[2]}", d[2] * 1e3)
v.check("X09.13g", s13[2] / c13[2])
v.check("X09.13h", math.exp(0.15 / VT))
v.check("X09.13i", 1 / (Q * 9e12 * 1800))

# 14
v.check("X09.14a", 0.6 * 0.905 / HC)
v.check("X09.14b", 2 * 150 / 2.998e8 * 1e6)
v.check("X09.14c", 20 * math.log10(10000 / 3))
Jsc, J0 = 38e-3, 2e-13
voc = brentq(lambda V: Jsc - J0 * (math.exp(V / VT) - 1), 0.3, 1.0, xtol=1e-14)
v.check("X09.14d", voc)
x1 = voc - VT * math.log(1 + (voc - 3 * VT) / VT)
v.check("X09.14e", x1)
r14 = minimize_scalar(lambda V: -V * (Jsc - J0 * (math.exp(V / VT) - 1)), bounds=(0.3, voc), method="bounded",
                      options={"xatol": 1e-12})
v.check("X09.14f", r14.x)
jmp = Jsc - J0 * (math.exp(r14.x / VT) - 1)
v.check("X09.14g", jmp * 1e3)
v.check("X09.14h", r14.x * jmp / (voc * Jsc))
v.check("X09.14i", r14.x * jmp / 0.1 * 100)

# 15
ratio = brentq(lambda x: x ** 3 - 10, 1, 5)
v.check("X09.15a", ratio)
v.check("X09.15b", ratio * 2.84)

v.finish()
