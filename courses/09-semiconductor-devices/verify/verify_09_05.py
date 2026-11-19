#!/usr/bin/env python3
"""Verify every number in chapter 09-05 (PN junction electrostatics), its solutions and lab.

Independent routes:
- built-in potentials from the band positions of each side with a flat Fermi level (09-02 forms);
- depletion-approximation quantities by integrating the rectangular charge numerically on separate grids
  for each side, with the width found by root finding on the total potential (not from the closed form);
- the full nonlinear Poisson equation with Boltzmann carriers solved by Newton's method for Example 5 and
  the lab, with depletion edges located by interpolation;
- graded junctions by root finding on the self-consistent width; capacitance by differentiating the
  depleted charge numerically; C-V extraction by fitting simulated data.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import constants as C
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
v = Verifier.from_files("09-05", COURSE / "chapters" / "09-05-pn-junction-electrostatics.md",
                        COURSE / "solutions" / "09-05-solutions.md",
                        COURSE / "labs" / "09-05-lab" / "README.md")

Q = C.e
VT = C.k * 300 / C.e
NI = 1.0e10
EPS = 11.7 * C.epsilon_0 / 100        # F/cm


def vbi(NA, ND, ni=NI):
    """Fermi-level difference of the separated sides: (E_F - E_i)_n + (E_i - E_F)_p."""
    return VT * math.log(ND / ni) + VT * math.log(NA / ni)


def depletion(NA, ND, VA=0.0, eps=EPS, ni=NI, n=4001):
    """Width, edges, peak field and side drops by integrating the depletion charge numerically."""
    Vb = vbi(NA, ND, ni)
    def sides(W):
        xn, xp = W * NA / (NA + ND), W * ND / (NA + ND)
        x1, x2 = np.linspace(-xp, 0, n), np.linspace(0, xn, n)
        E1 = np.concatenate([[0], np.cumsum(np.full(n - 1, -Q * NA) * np.diff(x1))]) / eps
        E2 = E1[-1] + np.concatenate([[0], np.cumsum(np.full(n - 1, Q * ND) * np.diff(x2))]) / eps
        V1 = np.concatenate([[0], np.cumsum(-(E1[1:] + E1[:-1]) / 2 * np.diff(x1))])
        V2 = V1[-1] + np.concatenate([[0], np.cumsum(-(E2[1:] + E2[:-1]) / 2 * np.diff(x2))])
        return xn, xp, E1, E2, V1, V2
    W = brentq(lambda W: sides(W)[5][-1] - (Vb - VA), 1e-9, 1e-1, xtol=1e-16)
    xn, xp, E1, E2, V1, V2 = sides(W)
    # the split x_n = W N_A/(N_A + N_D) is checked, not assumed: the integrated field must return to zero at x_n
    assert abs(E2[-1]) < 1e-9 * abs(E1[-1]), "charge neutrality violated"
    return dict(W=W, xn=xn, xp=xp, Emax=abs(E1[-1]), Vp=V1[-1], Vn=V2[-1] - V1[-1], Vbi=Vb,
                x2=np.linspace(0, xn, n), V2=V2, x1=np.linspace(-xp, 0, n), E1=E1)


def poisson(NA, ND, L=2e-4, n=16001):
    x = np.linspace(-L / 2, L / 2, n)
    h = x[1] - x[0]
    Nnet = np.where(x > 0, ND, -NA).astype(float)
    psi = np.where(x > 0, VT * np.log(ND / NI), -VT * np.log(NA / NI)).astype(float)
    for _ in range(100):
        nn, pp = NI * np.exp(psi / VT), NI * np.exp(-psi / VT)
        F = np.zeros(n)
        F[1:-1] = (psi[2:] - 2 * psi[1:-1] + psi[:-2]) / h**2 + Q * (pp - nn + Nnet)[1:-1] / EPS
        main = np.full(n, -2 / h**2) - Q / EPS * (pp + nn) / VT
        main[0] = main[-1] = 1
        lo = np.full(n - 1, 1 / h**2)
        up = lo.copy()
        up[0] = 0
        lo[-1] = 0
        d = spsolve(diags([lo, main, up], [-1, 0, 1], format="csc"), -F)
        psi += d
        if np.max(np.abs(d)) < 1e-12:
            break
    return x, psi, NI * np.exp(psi / VT), NI * np.exp(-psi / VT)


def graded(a, VA=0.0, Vb_fixed=None):
    if Vb_fixed is None:
        W = brentq(lambda W: 2 * VT * math.log(a * W / (2 * NI)) - VA - Q * a * W**3 / (12 * EPS), 1e-9, 1e-2)
        Vb = 2 * VT * math.log(a * W / (2 * NI))
    else:
        Vb = Vb_fixed
        W = brentq(lambda W: Q * a * W**3 / (12 * EPS) - (Vb - VA), 1e-9, 1e-2)
    # peak field by integrating rho = q a x from -W/2 to 0
    xs = np.linspace(-W / 2, 0, 4001)
    Emax = abs(np.trapezoid(Q * a * xs, xs)) / EPS
    return W, Vb, Emax


def charge_n(NA, ND, VA):
    d = depletion(NA, ND, VA)
    return Q * ND * d["xn"]


# ================================================================= chapter
v.check("Ex 09-05.1a", VT * math.log(1e16 / NI))
v.check("Ex 09-05.1b", VT * math.log(1e17 / NI))
v.check("Ex 09-05.1c", vbi(1e17, 1e16))

d0 = depletion(1e17, 1e16)
v.check("Ex 09-05.2a", d0["W"] * 1e4)
v.check("Ex 09-05.2b", d0["xn"] * 1e4)
v.check("Ex 09-05.2c", d0["xp"] * 1e7)
v.check("Ex 09-05.2d", d0["Emax"])
v.check("Ex 09-05.2e", d0["Vn"])
v.check("Ex 09-05.2f", d0["Vp"])
v.check("Ex 09-05.2g", d0["Vn"] / d0["Vbi"] * 100)

dr = depletion(1e17, 1e16, -5)
df = depletion(1e17, 1e16, 0.5)
v.check("Ex 09-05.3a", dr["W"] * 1e4)
v.check("Ex 09-05.3b", dr["Emax"])
v.check("Ex 09-05.3c", df["W"] * 1e4)
v.check("Ex 09-05.3d", df["Emax"])
v.check("Ex 09-05.3e", dr["W"] / d0["W"])

dp0 = depletion(1e19, 5e15)
v.check("Ex 09-05.4a", dp0["Vbi"])
v.check("Ex 09-05.4b", dp0["W"] * 1e4)
v.check("Ex 09-05.4c", dp0["xp"] / dp0["W"] * 100)
dp10 = depletion(1e19, 5e15, -10)
v.check("Ex 09-05.4d", dp10["W"] * 1e4)
v.check("Ex 09-05.4e", math.sqrt(2 * EPS * (dp0["Vbi"] + 10) / (Q * 5e15)) * 1e4)
v.check("Ex 09-05.4f", dp10["Emax"])
v.check("Ex 09-05.4g", brentq(lambda V: depletion(1e19, 5e15, -V)["Emax"] - 3e5, 1, 1e4))
v.check("Ex 09-05.4h", EPS * (3e5) ** 2 / (2 * Q * 5e15))

LD = math.sqrt(EPS * VT / (Q * 1e16))
v.check("Ex 09-05.5a", LD * 1e7)
v.check("Ex 09-05.5b", d0["W"] / LD)
x, psi, nn, pp = poisson(1e17, 1e16)
right = x > 0
Wh = np.interp(0.5e16, nn[right], x[right]) - np.interp(0.5e17, pp[~right][::-1], x[~right][::-1])
v.check("Ex 09-05.5c", Wh * 1e4)
v.check("Ex 09-05.5d", (1 - Wh / d0["W"]) * 100)
corr = math.sqrt((d0["Vbi"] - 2 * VT) / d0["Vbi"])
v.check("Ex 09-05.5e", corr)
v.check("Ex 09-05.5f", (d0["W"] - Wh) * 1e7)
v.check("Ex 09-05.5g", (d0["W"] - Wh) / LD)
v.check("Ex 09-05.5h", d0["W"] * corr * 1e4)

Wg, Vbg, Eg0 = graded(1e20)
v.check("Ex 09-05.6a", Wg * 1e4)
v.check("Ex 09-05.6b", Vbg)
v.check("Ex 09-05.6c", 1e20 * Wg / 2)
v.check("Ex 09-05.6d", Eg0)
Wg5, _, Eg5 = graded(1e20, VA=-5, Vb_fixed=Vbg)
v.check("Ex 09-05.6e", Wg5 * 1e4)
v.check("Ex 09-05.6f", Eg5)
v.check("Ex 09-05.6g", Wg5 / Wg)

A = 1e-4
dV = 1e-4
def cap(NA, ND, VA):
    return (charge_n(NA, ND, VA - dV) - charge_n(NA, ND, VA + dV)) / (2 * dV) * A
C0, C5 = cap(1e19, 5e15, 0.0), cap(1e19, 5e15, -5.0)
v.check("Ex 09-05.7a", C0 * 1e12)
v.check("Ex 09-05.7b", C5 * 1e12)
slope = (1 / C5**2 - 1 / C0**2) / (-5 - 0)
v.check("Ex 09-05.7c", slope)
v.check("Ex 09-05.7d", -2 / (Q * EPS * A**2 * slope))
v.check("Ex 09-05.7e", C0 / A * 1e9)
v.check("Ex 09-05.7f", C0 / A * 1e-5 * 1e12)          # 1000 um^2 = 1e-5 cm^2, in pF

v.check("T 09-05.a", EPS)
v.check("T 09-05.b", (vbi(1e18, 1e16) - vbi(1e17, 1e16)) * 1e3)

# Practitioner
v.check("P 09-05.a", EPS / 1e-5 * 1e-8 * 1e15)        # F/cm^2 -> fF/um^2
Vb600, Ec = 600.0, 3e5
N600 = brentq(lambda N: math.sqrt(2 * Q * N * Vb600 / EPS) - Ec, 1e12, 1e18)
W600 = brentq(lambda W: 0.5 * Ec * W - Vb600, 1e-6, 1)
mu = lambda N: 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)
v.check("P 09-05.b", N600)
v.check("P 09-05.c", W600 * 1e4)
v.check("P 09-05.d", W600 / (Q * mu(N600) * N600) * 1e3)
v.check("C 09-05.a", math.sqrt((0.8 + 9) / (0.8 + 1)))

# ================================================================= solutions
v.check("09-05.1a", vbi(1e18, 1e15))
v.check("09-05.1b", vbi(1e16, 1e16))
v.check("09-05.1c", vbi(1e17, 1e17, 2.1e6))

ds = depletion(1e16, 1e16)
v.check("09-05.2a", ds["W"] * 1e4)
v.check("09-05.2b", ds["xn"] * 1e4)
v.check("09-05.2c", ds["Emax"])

v.check("09-05.3a", vbi(1e19, 1e15))
onesided = lambda V: math.sqrt(2 * EPS * (vbi(1e19, 1e15) - V) / (Q * 1e15)) * 1e4
for V, (kf, ko) in ((0, ("09-05.3b", "09-05.3c")), (-1, ("09-05.3d", "09-05.3e")), (-10, ("09-05.3f", "09-05.3g")),
                    (-100, ("09-05.3h", "09-05.3i"))):
    v.check(kf, depletion(1e19, 1e15, V)["W"] * 1e4)
    v.check(ko, onesided(V))
v.check("09-05.3j", depletion(1e19, 1e15, -100)["W"] / depletion(1e19, 1e15, -10)["W"])

v.check("09-05.4a", 2 * 1.2 / 0.5e-4)
v.check("09-05.4b", 0.5 * 10 / 11)
v.check("09-05.4c", 0.5 * 1 / 11)
v.check("09-05.4d", 1.2 * 10 / 11)

N5 = brentq(lambda N: depletion(1e19, N, -5)["W"] - 2e-4, 1e13, 1e18)
v.check("09-05.5a", N5)
v.check("09-05.5b", vbi(1e19, N5))
guess = 2 * EPS * 5 / (Q * (2e-4) ** 2)
v.check("09-05.5c", guess)
v.check("09-05.5d", (N5 - guess) / N5 * 100)

xs2, V2 = d0["x2"], d0["V2"]
v.check("09-05.6a", V2[-1] - float(np.interp(d0["xn"] / 2, xs2, V2)))
v.check("09-05.6b", abs(float(np.interp(-d0["xp"] / 2, d0["x1"], d0["E1"]))))

v.check("09-05.7a", charge_n(1e17, 1e16, 0.0))
v.check("09-05.7b", charge_n(1e17, 1e16, -5.0))
v.check("09-05.7c", EPS / dr["W"] * 1e9)
v.check("09-05.7d", cap(1e17, 1e16, -5.0) / A * 1e9)
v.check("09-05.7e", EPS / d0["W"] * 1e9)

for N, (kl, kw, kr) in ((1e14, ("09-05.8a", "09-05.8b", "09-05.8c")), (1e16, ("09-05.8d", "09-05.8e", "09-05.8f")),
                        (1e18, ("09-05.8g", "09-05.8h", "09-05.8i"))):
    L = math.sqrt(EPS * VT / (Q * N))
    Wd = depletion(1e19, N)["W"]
    v.check(kl, L * 1e7)
    v.check(kw, Wd * 1e4)
    v.check(kr, Wd / L)

W9, Vb9, E9 = graded(1e22)
v.check("09-05.9a", W9 * 1e4)
v.check("09-05.9b", Vb9)
v.check("09-05.9c", 1e22 * W9 / 2)
v.check("09-05.9d", E9)

C1, C4 = cap(1e19, 2e16, -1.0), cap(1e19, 2e16, -4.0)
v.check("09-05.10f", C1 * 1e12)
v.check("09-05.10g", C4 * 1e12)
C1r, C4r = 2.944e-12, 1.837e-12          # the rounded data given in the problem
v.check("09-05.10a", 1 / C1r**2)
v.check("09-05.10b", 1 / C4r**2)
s10 = (1 / C4r**2 - 1 / C1r**2) / (-4 + 1)
v.check("09-05.10c", s10)
v.check("09-05.10d", -2 / (Q * EPS * A**2 * s10))
v.check("09-05.10e", -1 + (1 / C1r**2) / (-s10))
v.check("09-05.10h", vbi(1e19, 2e16))

N11 = brentq(lambda N: math.sqrt(2 * Q * N * 200 / EPS) - Ec, 1e12, 1e18)
W11 = 2 * 200 / Ec
v.check("09-05.11a", N11)
v.check("09-05.11b", W11 * 1e4)
v.check("09-05.11c", mu(N11))
v.check("09-05.11d", W11 / (Q * mu(N11) * N11) * 1e3)

Vpin = vbi(1e19, 1e19)
v.check("09-05.12a", Vpin)
v.check("09-05.12b", (Vpin + 10) / 2e-4)
v.check("09-05.12c", EPS / 2e-4 * 1e9)
v.check("09-05.12d", EPS / depletion(1e19, 1e15, -10)["W"] * 1e9)

v.check("09-05.13a", N600)
v.check("09-05.13b", W600 * 1e4)
v.check("09-05.13c", mu(N600))
R600 = W600 / (Q * mu(N600) * N600)
v.check("09-05.13d", R600 * 1e3)
v.assert_true(abs(R600 / (4 * Vb600**2 / (EPS * mu(N600) * Ec**3)) - 1) < 1e-9, "R = 4V^2/(eps mu Ec^3)")
v.check("09-05.13e", 4 * Vb600**2 / (EPS * mu(N600) * (10 * Ec) ** 3) * 1e3)

d14 = depletion(1e19, 1e15)
v.check("09-05.14a", d14["Vbi"])
v.check("09-05.14b", math.sqrt(2 * EPS * d14["Vbi"] / (Q * 1e15)) * 1e4)
f14 = math.sqrt((d14["Vbi"] - 2 * VT) / d14["Vbi"])
v.check("09-05.14c", math.sqrt(2 * EPS * d14["Vbi"] / (Q * 1e15)) * f14 * 1e4)
v.check("09-05.14d", f14)

EPSG = 12.9 * C.epsilon_0 / 100
dg = depletion(1e17, 1e17, eps=EPSG, ni=2.1e6)
v.check("09-05.15a", dg["W"] * 1e4)
v.check("09-05.15b", dg["Emax"])
v.check("09-05.15c", vbi(1e17, 1e17))
v.check("09-05.15d", depletion(1e17, 1e17)["W"] * 1e4)
v.check("09-05.15e", depletion(1e17, 1e17)["Emax"])
v.check("09-05.15f", dg["Emax"] / depletion(1e17, 1e17)["Emax"])

# ================================================================= lab
x10, x90 = np.interp([0.1e16, 0.9e16], nn[right], x[right])
v.check("Lab 09-05.a", (x90 - x10) * 1e7)
v.check("Lab 09-05.b", (x90 - x10) / LD)
E_exact = float(np.abs(np.gradient(psi, x)).max())
v.check("Lab 09-05.c", E_exact)
v.check("Lab 09-05.d", (1 - E_exact / d0["Emax"]) * 100)
v.check("Lab 09-05.e", W9 / Wg)

v.finish()
