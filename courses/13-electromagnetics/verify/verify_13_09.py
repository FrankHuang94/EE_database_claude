#!/usr/bin/env python3
"""Verify every number in chapter 13-09 (the Smith chart and impedance matching), its solutions and lab.

Independent routes (not the chapter's closed forms):
- chart circles by sampling points of constant r or x and fitting circles to them (least squares);
- moves along lines by marching the phasor line equations (solve_ivp), not the tan formula;
- L-networks and stub matches by nodal analysis of the assembled circuit, with element values or positions found
  by root finding on the match condition;
- bandwidths by frequency sweeps and root finding;
- the coax optima by numerical minimization of the loss and maximization of the power.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-09-smith-chart-and-matching.md",
         COURSE / "solutions" / "13-09-solutions.md"]
lab = COURSE / "labs" / "13-09-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-09", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 1 / math.sqrt(mu0 * e0)
eta0 = math.sqrt(mu0 / e0)
Z0 = 50.0


def gam(Z, Zref=Z0):
    return (Z - Zref) / (Z + Zref)


def march_zin(ZL, Zc, frac):
    """Input impedance of a lossless line (impedance Zc, length frac wavelengths) by integrating the line ODEs."""
    k = 2 * math.pi  # per wavelength
    def f(d, y):
        V = y[0] + 1j * y[1]
        I = y[2] + 1j * y[3]
        dV, dI = 1j * k * Zc * I, 1j * k / Zc * V
        return [dV.real, dV.imag, dI.real, dI.imag]
    ZL = complex(ZL)
    if abs(ZL) > 1e9:      # open: start with V = 1, I = 0
        y0 = [1.0, 0.0, 0.0, 0.0]
    else:
        y0 = [ZL.real, ZL.imag, 1.0, 0.0]
    sol = solve_ivp(f, (0, frac), y0, rtol=1e-12, atol=1e-14, method="DOP853")
    V = sol.y[0, -1] + 1j * sol.y[1, -1]
    I = sol.y[2, -1] + 1j * sol.y[3, -1]
    return V / I


def fit_circle(pts):
    """Least-squares circle through complex points: returns centre and radius."""
    x, y = pts.real, pts.imag
    A = np.column_stack([2 * x, 2 * y, np.ones_like(x)])
    b = x**2 + y**2
    cx, cy, k = np.linalg.lstsq(A, b, rcond=None)[0]
    return complex(cx, cy), math.sqrt(k + cx**2 + cy**2)


# ---------------------------------------------------------------- Example 1
z1 = 2 + 1j
G1 = gam(z1 * Z0)
v.check("Ex 13-09.1a", G1.real)
v.check("Ex 13-09.1b", G1.imag)
v.check("Ex 13-09.1c", abs(G1))
v.check("Ex 13-09.1d", math.degrees(cmath.phase(G1)))
v.check("Ex 13-09.1e", (1 + abs(G1)) / (1 - abs(G1)))
cr, rr = fit_circle(np.array([gam((2 + 1j * x) * Z0) for x in np.linspace(-5, 5, 41)]))
v.assert_true("r = 2 circle: centre 2/3, radius 1/3", abs(cr - 2 / 3) < 1e-9 and abs(rr - 1 / 3) < 1e-9)
cx_, rx_ = fit_circle(np.array([gam((r + 1j) * Z0) for r in np.linspace(0, 10, 41)]))
v.assert_true("x = 1 circle: centre 1 + j1, radius 1", abs(cx_ - (1 + 1j)) < 1e-9 and abs(rx_ - 1) < 1e-9)

# ---------------------------------------------------------------- Example 2
Z2 = march_zin(100 + 50j, Z0, 1 / 8)
G2 = gam(Z2)
v.check("Ex 13-09.2a", abs(G2))
v.check("Ex 13-09.2b", math.degrees(cmath.phase(G2)))
v.check("Ex 13-09.2c", Z2.real)
v.check("Ex 13-09.2d", Z2.imag)

# ---------------------------------------------------------------- Example 3
y3 = (1 - G1) / (1 + G1)
v.check("Ex 13-09.3a", y3.real)
v.check("Ex 13-09.3b", y3.imag)
v.assert_true("y = 1/z", abs(y3 - 1 / z1) < 1e-12)

# ---------------------------------------------------------------- Example 4 (L-network by nodal analysis)
f4 = 2.4e9
w4 = 2 * math.pi * f4


def lnet_zin(f, L, C, RL=10.0):
    w = 2 * math.pi * f
    Zs = RL + 1j * w * L          # series inductor next to the low-resistance load
    return 1 / (1 / Zs + 1j * w * C)  # shunt capacitor across the 50 ohm port


# find L and C by solving Re and Im of the match condition
L4 = brentq(lambda L: (1 / (10 + 1j * w4 * L)).real - 1 / 50, 1e-12, 1e-8, xtol=1e-20)
C4 = -(1 / (10 + 1j * w4 * L4)).imag / w4
v.check("Ex 13-09.4a", w4 * L4 / 10)
v.check("Ex 13-09.4b", L4 * 1e9)
v.check("Ex 13-09.4c", C4 * 1e12)
v.assert_true("L-network matches", abs(lnet_zin(f4, L4, C4) - 50) < 1e-9)
lo = brentq(lambda f: abs(gam(lnet_zin(f, L4, C4))) - 0.1, 1e9, f4, xtol=1e2)
hi = brentq(lambda f: abs(gam(lnet_zin(f, L4, C4))) - 0.1, f4, 4e9, xtol=1e2)
v.check("Ex 13-09.4d", (hi - lo) / f4 * 100)

# ---------------------------------------------------------------- Example 5 (single shunt shorted stub)
ZL5 = 25 - 50j
lam5 = c0 / 1e9


def y_at(d):
    return Z0 / march_zin(ZL5, Z0, d)


grid = np.linspace(0.001, 0.499, 499)
vals = np.array([y_at(d).real - 1 for d in grid])
roots = [brentq(lambda d: y_at(d).real - 1, grid[i], grid[i + 1], xtol=1e-14)
         for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0 and abs(vals[i]) < 3]
d1, d2 = sorted(roots)[:2]
b1, b2 = y_at(d1).imag, y_at(d2).imag


def stub_len(b_needed):
    # shorted stub: y = Z0 / Zin(short) ; find the shortest length giving the needed susceptance
    return brentq(lambda l: (Z0 / march_zin(1e-12, Z0, l)).imag - b_needed, 1e-4, 0.4999, xtol=1e-14) \
        if b_needed < 0 else brentq(lambda l: (Z0 / march_zin(1e-12, Z0, l)).imag - b_needed, 0.25 + 1e-4,
                                    0.4999, xtol=1e-14)


l1, l2 = stub_len(-b1), stub_len(-b2)
v.check("Ex 13-09.5a", d1)
v.check("Ex 13-09.5b", d1 * lam5 * 100)
v.check("Ex 13-09.5c", l1)
v.check("Ex 13-09.5d", l1 * lam5 * 100)
v.check("Ex 13-09.5e", d2)
v.check("Ex 13-09.5f", d2 * lam5 * 100)
v.check("Ex 13-09.5g", l2)
v.check("Ex 13-09.5h", l2 * lam5 * 100)
v.check("Ex 13-09.5i", b1)
for d, l in ((d1, l1), (d2, l2)):
    ytot = y_at(d) + Z0 / march_zin(1e-12, Z0, l)
    v.assert_true("stub match gives y = 1", abs(ytot - 1) < 1e-8)

# ---------------------------------------------------------------- Example 6 (Bode-Fano)
for Gm, key in ((0.1, "a"), (10 ** (-10 / 20), "b")):
    dw = brentq(lambda dw: dw * math.log(1 / Gm) - math.pi / (50 * 1e-12), 1, 1e13)
    v.check(f"Ex 13-09.6{key}", dw / (2 * math.pi) / 1e9)
# independent check of the bound itself: build real lossless matches for 50 ohm || 1 pF and integrate ln(1/|G|)
RB, CB = 50.0, 1e-12
def zload_rc(w_):
    return RB / (1 + 1j * w_ * RB * CB)
def refl_series_L(w_, Lm):                     # series inductor in front of the RC load
    z = 1j * w_ * Lm + zload_rc(w_)
    return abs((z - 50) / (z + 50))
def refl_ladder(w_, Lm, Cm):                   # series L, then shunt C, in front of the RC load
    z = 1 / (1 / (1j * w_ * Lm + zload_rc(w_)) + 1j * w_ * Cm)
    return abs((z - 50) / (z + 50))
bound = math.pi / (RB * CB)
for Lm in (0.5e-9, 1.25e-9, 2.5e-9):
    I_bf = quad(lambda w_: math.log(1 / refl_series_L(w_, Lm)), 0, 2e12, limit=400)[0]
    v.assert_true(f"Bode-Fano holds for a series {Lm * 1e9:.2f} nH match", I_bf <= bound * (1 + 1e-6))
I_lad = quad(lambda w_: math.log(1 / refl_ladder(w_, 2.5e-9, 0.5e-12)), 0, 2e12, limit=400)[0]
v.assert_true("Bode-Fano holds for an L-C ladder match", I_lad <= bound * (1 + 1e-6))

# ---------------------------------------------------------------- practitioner (coax optima)
xl = minimize_scalar(lambda x: (1 + x) / math.log(x), bounds=(1.5, 8), method="bounded", options={"xatol": 1e-12}).x
xp = minimize_scalar(lambda x: -math.log(x) / x**2, bounds=(1.01, 5), method="bounded", options={"xatol": 1e-12}).x
Zl, Zp = eta0 / (2 * math.pi) * math.log(xl), eta0 / (2 * math.pi) * math.log(xp)
v.check("Prac 13-09.a", Zl)
v.check("Prac 13-09.b", Zp)
v.check("Prac 13-09.d", eta0 / (2 * math.pi * 1.5) * math.log(xl))
v.check("Prac 13-09.c", math.sqrt(Zl * Zp))
v.check("Sim 13-09.a", lnet_zin(f4, 1.32629e-9, 2.65258e-12).real)
yst = Z0 / march_zin(ZL5, Z0, 0.0631303) + Z0 / march_zin(1e-12, Z0, 0.0897543)
v.check("Sim 13-09.b", (Z0 / yst).real)

# ---------------------------------------------------------------- Problems
G = gam((0.5 - 0.5j) * Z0)
v.check("13-09.1a", G.real)
v.check("13-09.1b", G.imag)
v.check("13-09.1c", abs(G))
v.check("13-09.1d", math.degrees(cmath.phase(G)))
v.check("13-09.1e", (1 + abs(G)) / (1 - abs(G)))
cr, rr = fit_circle(np.array([gam((0.5 + 1j * x) * Z0) for x in np.linspace(-5, 5, 41)]))
cx_, rx_ = fit_circle(np.array([gam((r - 2j) * Z0) for r in np.linspace(0, 10, 41)]))
v.check("13-09.2a", cr.real)
v.check("13-09.2b", rr)
v.check("13-09.2c", cx_.imag)
v.check("13-09.2d", rx_)
G3 = gam((1 + 1j) * Z0)
y = (1 + (-G3)) / (1 - (-G3))
v.check("13-09.3a", y.real)
v.check("13-09.3b", y.imag)
Z4 = march_zin(30 + 40j, Z0, 0.15)
v.check("13-09.4a", Z4.real)
v.check("13-09.4b", Z4.imag)
d5 = brentq(lambda d: march_zin(100 + 100j, Z0, d).imag, 0.01, 0.1, xtol=1e-14)
Z5 = march_zin(100 + 100j, Z0, d5)
GL5 = abs(gam(100 + 100j))
v.check("13-09.5a", d5)
v.check("13-09.5b", Z5.real)
v.check("13-09.5c", (1 + GL5) / (1 - GL5))
w6 = 2 * math.pi * 1e8
# high-pass: shunt L across 200, series C on the 50 ohm side; solve Re{200 || jwL} = 50
L6 = brentq(lambda L: (1 / (1 / 200 + 1 / (1j * w6 * L))).real - 50, 1e-9, 1e-5, xtol=1e-20)
X6 = (1 / (1 / 200 + 1 / (1j * w6 * L6))).imag
C6 = 1 / (w6 * X6)
v.check("13-09.6a", X6 / 50)
v.check("13-09.6b", L6 * 1e9)
v.check("13-09.6c", C6 * 1e12)
v.check("13-09.6d", w6 * L6)
v.assert_true("high-pass L matches", abs(1 / (1 / 200 + 1 / (1j * w6 * L6)) - 1j / (w6 * C6) - 50) < 1e-9)
Ladd = brentq(lambda L: (1 / (10 + 5j + 1j * w4 * L)).real - 1 / 50, 1e-13, 1e-8, xtol=1e-20)
C7 = -(1 / (10 + 5j + 1j * w4 * Ladd)).imag / w4
v.check("13-09.7a", Ladd * 1e9)
v.check("13-09.7b", C7 * 1e12)
ZL8 = 100.0
y8 = lambda d: Z0 / march_zin(ZL8, Z0, d)  # noqa: E731
r1 = brentq(lambda d: y8(d).real - 1, 0.05, 0.25, xtol=1e-14)
r2 = brentq(lambda d: y8(d).real - 1, 0.25, 0.45, xtol=1e-14)


def open_len(b_needed):
    return min(brentq(lambda l: (Z0 / march_zin(1e12, Z0, l)).imag - b_needed, lo_, hi_, xtol=1e-14)
               for lo_, hi_ in ((1e-4, 0.2499), (0.2501, 0.4999))
               if ((Z0 / march_zin(1e12, Z0, lo_)).imag - b_needed) * ((Z0 / march_zin(1e12, Z0, hi_)).imag - b_needed) < 0)


v.check("13-09.8a", r1)
v.check("13-09.8b", open_len(-y8(r1).imag))
v.check("13-09.8c", r2)
v.check("13-09.8d", open_len(-y8(r2).imag))
Ri = math.sqrt(500)
La = brentq(lambda L: (1 / (10 + 1j * w4 * L)).real - 1 / Ri, 1e-13, 1e-8, xtol=1e-20)
Ca = -(1 / (10 + 1j * w4 * La)).imag / w4
Lb = brentq(lambda L: (1 / (Ri + 1j * w4 * L)).real - 1 / 50, 1e-13, 1e-8, xtol=1e-20)
Cb = -(1 / (Ri + 1j * w4 * Lb)).imag / w4


def two_zin(f):
    w = 2 * math.pi * f
    Z = 1 / (1 / (10 + 1j * w * La) + 1j * w * Ca)
    return 1 / (1 / (Z + 1j * w * Lb) + 1j * w * Cb)


v.check("13-09.9a", w4 * La / 10)
lo = brentq(lambda f: abs(gam(two_zin(f))) - 0.1, 1e9, f4, xtol=1e2)
hi = brentq(lambda f: abs(gam(two_zin(f))) - 0.1, f4, 5e9, xtol=1e2)
v.check("13-09.9b", (hi - lo) / f4 * 100)
v.check("13-09.10a", brentq(lambda dw: dw * math.log(10) - math.pi * 10 / 1e-8, 1, 1e13) / (2 * math.pi) / 1e6)
zs = np.array([march_zin(12.5, Z0, d) for d in np.linspace(0, 0.5, 201)])
G11 = abs(gam(12.5))
v.check("13-09.11a", (1 + G11) / (1 - G11))
v.check("13-09.11b", zs.real.min())
v.check("13-09.11c", zs.real.max())
v.check("13-09.12a", xl)
v.check("13-09.12b", Zl)
v.check("13-09.13a", xp)
v.check("13-09.13b", Zp)
v.check("13-09.13c", math.sqrt(Zl * Zp))
ls = brentq(lambda l: (Z0 / march_zin(1e12, Z0, l)).imag - 2, 1e-4, 0.2499, xtol=1e-14)
v.check("13-09.14a", ls)
v.check("13-09.14b", ls * c0 / 2.4e9 * 100)

# ---------------------------------------------------------------- Lab
if lab.exists():
    # three-section binomial-style L cascade 10 -> 50 through geometric intermediate resistances: bandwidth
    Rs = [10 * 5 ** (k / 3) for k in range(4)]
    secs = []
    for Rlow, Rhigh in zip(Rs[:-1], Rs[1:]):
        L = brentq(lambda L: (1 / (Rlow + 1j * w4 * L)).real - 1 / Rhigh, 1e-13, 1e-8, xtol=1e-20)
        C = -(1 / (Rlow + 1j * w4 * L)).imag / w4
        secs.append((L, C))

    def three_zin(f):
        w = 2 * math.pi * f
        Z = 10.0
        for L, C in secs:
            Z = 1 / (1 / (Z + 1j * w * L) + 1j * w * C)
        return Z

    lo = brentq(lambda f: abs(gam(three_zin(f))) - 0.1, 1e9, f4, xtol=1e2)
    hi = brentq(lambda f: abs(gam(three_zin(f))) - 0.1, f4, 6e9, xtol=1e2)
    v.check("Lab 13-09.a", (hi - lo) / f4 * 100)
    # Bode-Fano bound for 50 ohm in parallel with 1 pF at 15 dB return loss
    Gm = 10 ** (-15 / 20)
    v.check("Lab 13-09.b", brentq(lambda dw: dw * math.log(1 / Gm) - math.pi / (50 * 1e-12), 1, 1e13) / (2 * math.pi) / 1e9)

# 15: quarter-wave match of 100 + j100 ohm: find the real-impedance points by marching, then sweep frequency
ZL15 = 100 + 100j
dmax15 = brentq(lambda d: march_zin(ZL15, Z0, d).imag, 0.01, 0.1, xtol=1e-14)
dmin15 = brentq(lambda d: march_zin(ZL15, Z0, d).imag, 0.2, 0.35, xtol=1e-14)
Rmax15, Rmin15 = march_zin(ZL15, Z0, dmax15).real, march_zin(ZL15, Z0, dmin15).real
v.check("13-09.15a", math.sqrt(Z0 * Rmax15))
v.check("13-09.15b", dmin15)
v.check("13-09.15c", math.sqrt(Z0 * Rmin15))
def qw_gamma(fr, d, R):
    z = march_zin(ZL15, Z0, d * fr)                   # line length scales with frequency
    return abs(gam(march_zin(z, math.sqrt(Z0 * R), 0.25 * fr)))
for key, d, R in (("d", dmax15, Rmax15), ("e", dmin15, Rmin15)):
    lo_ = brentq(lambda fr: qw_gamma(fr, d, R) - 0.1, 0.5, 1 - 1e-6, xtol=1e-12)
    hi_ = brentq(lambda fr: qw_gamma(fr, d, R) - 0.1, 1 + 1e-6, 1.5, xtol=1e-12)
    v.check(f"13-09.15{key}", (hi_ - lo_) * 100)

sys.exit(v.finish())
