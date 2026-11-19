#!/usr/bin/env python3
"""Figures for chapter 09-05 (PN junction electrostatics).

Run from anywhere:  python assets/figures/src/fig_09_05.py
Outputs SVGs to assets/figures/09-05/:
- junction-profiles.svg: step junction N_A = 1e17 / N_D = 1e16 cm^-3 at zero bias: (a) space charge in the
  depletion approximation with the exact (numerical Poisson) charge overlaid, (b) field, (c) potential,
  (d) band diagram with flat Fermi level;
- width-field-cv.svg: depletion width and peak field against reverse bias for that junction and for a
  P+N junction (1e19 / 5e15), and the 1/C^2 against voltage plot of the P+N junction (area 100 um x 100 um).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

Q = 1.602176634e-19
VT = 1.380649e-23 * 300 / Q
NI = 1e10
EPS = 11.7 * 8.8541878128e-14


def poisson(NA, ND, L=1.2e-4, n=6001):
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
    nn, pp = NI * np.exp(psi / VT), NI * np.exp(-psi / VT)
    return x, psi, Q * (pp - nn + Nnet)


def fig_profiles():
    NA, ND = 1e17, 1e16
    Vbi = VT * math.log(NA * ND / NI**2)
    W = math.sqrt(2 * EPS * Vbi * (1 / NA + 1 / ND) / Q)
    xn, xp = W * NA / (NA + ND), W * ND / (NA + ND)
    x, psi, rho = poisson(NA, ND)
    xu = x * 1e4
    rho_d = np.where((x > -xp) & (x < 0), -Q * NA, np.where((x > 0) & (x < xn), Q * ND, 0.0))
    E_d = np.where((x > -xp) & (x <= 0), -Q * NA * (x + xp) / EPS, np.where((x > 0) & (x < xn), -Q * ND * (xn - x) / EPS, 0.0))
    E_num = -np.gradient(psi, x)
    fig, axes = plt.subplots(2, 2, figsize=(8.6, 5.6), sharex=True)
    a, b, c, d = axes.ravel()
    a.plot(xu, rho_d / Q, color=PALETTE[0], label="depletion approximation")
    a.plot(xu, rho / Q, color=PALETTE[1], ls="--", label="exact (Poisson)")
    a.set_ylabel("ρ/q (cm$^{-3}$)")
    a.set_title("(a) space charge", fontsize=9)
    a.legend(fontsize=7)
    b.plot(xu, E_d / 1e3, color=PALETTE[0])
    b.plot(xu, E_num / 1e3, color=PALETTE[1], ls="--")
    b.set_ylabel("field (kV/cm)")
    b.set_title("(b) electric field", fontsize=9)
    c.plot(xu, psi - psi[0], color=PALETTE[1])
    c.set_ylabel("potential (V)")
    c.set_xlabel("x (µm)")
    c.set_title("(c) potential (zero deep in the p side)", fontsize=9)
    Eg = 1.12
    Ec = -psi + VT * math.log(3.2e19 / NI) * 0 + 0.5658
    d.plot(xu, Ec, color=PALETTE[0], label="$E_C$")
    d.plot(xu, Ec - Eg, color=PALETTE[2], label="$E_V$")
    d.axhline(0, color="0.4", ls=":", label="$E_F$")
    d.set_ylabel("energy (eV, $E_F$ = 0)")
    d.set_xlabel("x (µm)")
    d.set_title("(d) band diagram", fontsize=9)
    d.legend(fontsize=7, loc="upper right")
    for ax in axes.ravel():
        ax.set_xlim(-0.2, 0.5)
    save(fig, f"{OUT}/junction-profiles.svg")


def fig_width():
    VR = np.linspace(0, 20, 200)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.5))
    for (NA, ND), col, lab in (((1e17, 1e16), PALETTE[0], "1e17 / 1e16"), ((1e19, 5e15), PALETTE[1], "P$^+$N, 1e19 / 5e15")):
        Vbi = VT * math.log(NA * ND / NI**2)
        W = np.sqrt(2 * EPS * (Vbi + VR) * (1 / NA + 1 / ND) / Q)
        a1.plot(VR, W * 1e4, color=col, label=lab)
        ax2 = a1
        a1.plot(VR, 2 * (Vbi + VR) / W / 1e5, color=col, ls="--")
    a1.set_xlabel("reverse bias (V)")
    a1.set_ylabel("W (µm, solid);  peak field (100 kV/cm, dashed)")
    a1.legend(fontsize=7)
    NA, ND, A = 1e19, 5e15, 1e-4
    Vbi = VT * math.log(NA * ND / NI**2)
    VA = -VR
    C = EPS * A / np.sqrt(2 * EPS * (Vbi - VA) * (1 / NA + 1 / ND) / Q)
    a2.plot(VA, 1 / C**2 / 1e23, color=PALETTE[1])
    a2.axvline(Vbi, color="0.6", ls=":")
    Vext = np.linspace(-20, Vbi - 1e-6, 50)
    Cext = EPS * A / np.sqrt(2 * EPS * (Vbi - Vext) * (1 / NA + 1 / ND) / Q)
    a2.plot(Vext, 1 / Cext**2 / 1e23, color=PALETTE[1], ls=":")
    a2.set_xlabel("applied voltage $V_A$ (V)")
    a2.set_ylabel("$1/C^2$ ($10^{23}$ F$^{-2}$)")
    a2.set_title("C–V plot: slope gives N, intercept gives $V_{bi}$", fontsize=9)
    save(fig, f"{OUT}/width-field-cv.svg")


if __name__ == "__main__":
    fig_profiles()
    fig_width()
    print("09-05 figures written to", OUT)
