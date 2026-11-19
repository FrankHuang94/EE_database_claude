#!/usr/bin/env python3
"""Figures for chapter 09-13 (compound and wide-bandgap semiconductors).

Run from anywhere:  python assets/figures/src/fig_09_13.py
Outputs to assets/figures/09-13/:
- material-properties.svg: band gap, electron mobility and breakdown field for Si, GaAs, InP, GaN and 4H-SiC.
  Si/GaAs/InP from the Levinshtein-Rumyantsev handbook (mobility upper limits, approximate breakdown fields);
  GaN gap from Vurgaftman's Varshni parameters at 300 K; 4H-SiC gap and mobility from Burin et al., and its
  breakdown field computed at 1e16 cm^-3 from Hatakeyama's c-axis ionization fits (chapter Example 09-13.2).
  GaN mobility and breakdown field are not shown (not confirmed in a primary source for this build).
- breakdown-baliga.svg: (a) breakdown voltage against doping for Si and 4H-SiC from the ionization integral;
  (b) ideal specific on-resistance against breakdown voltage (triangular-field drift layer).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid, trapezoid
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-13"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

Q, E0 = 1.602176634e-19, 8.8541878128e-14
EPS_SI, EPS_SIC = 11.7 * E0, 9.96 * E0
an_si = lambda F: 3.318e5 * np.exp(-1.174e6 / F)
ap_si = lambda F: np.where(F < 5.3e5, 2e6 * np.exp(-1.97e6 / F), 5.6e5 * np.exp(-1.32e6 / F))
an_sic = lambda F: 1.76e8 * np.exp(-3.3e7 / F)
ap_sic = lambda F: 3.41e8 * np.exp(-2.5e7 / F)
mun = lambda N: 92 + 1268 / (1 + (N / 1.3e17) ** 0.91)


def ion_integral(Em, N, eps, an, ap):
    W = eps * Em / (Q * N)
    x = np.linspace(0, W, 8001)
    F = np.maximum(Em * (1 - x / W), 1e3)
    a, b = an(F), ap(F)
    inner = cumulative_trapezoid(a - b, x, initial=0)
    return trapezoid(a * np.exp(np.clip(-inner, -700, 700)), x)


def breakdown(N, eps, an, ap, lo, hi):
    Em = brentq(lambda E: ion_integral(E, N, eps, an, ap) - 1, lo, hi, xtol=10.0)
    W = eps * Em / (Q * N)
    return Em, W, Em * W / 2


SI = (EPS_SI, an_si, ap_si, 1.0e5, 1.5e6)
SIC = (EPS_SIC, an_sic, ap_sic, 1.2e6, 4e6)

# ------------------------------------------------------------------ figure 1
mats = ["Si", "GaAs", "InP", "GaN", "4H-SiC"]
eg = [1.12, 1.424, 1.344, 3.435, 3.26]
mob = [1400, 8500, 5400, np.nan, 1000]
ebd = [3e5, 4e5, 5e5, np.nan, breakdown(1e16, *SIC)[0]]
fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
cols = [PALETTE[i % len(PALETTE)] for i in range(5)]
axs[0].bar(mats, eg, color=cols)
axs[0].set_ylabel("band gap (eV)")
axs[0].set_title("(a) band gap at 300 K", fontsize=9)
axs[1].bar(mats, mob, color=cols)
axs[1].set_yscale("log")
axs[1].set_ylabel("electron mobility (cm²/V·s)")
axs[1].set_title("(b) electron mobility (low doping)", fontsize=9)
axs[1].text(3, 1100, "n/c", ha="center", fontsize=8)
axs[2].bar(mats, ebd, color=cols)
axs[2].set_yscale("log")
axs[2].set_ylabel("breakdown field (V/cm)")
axs[2].set_title("(c) breakdown field", fontsize=9)
axs[2].text(3, 3.5e5, "n/c", ha="center", fontsize=8)
for ax in axs:
    ax.tick_params(axis="x", labelsize=8)
fig.text(0.5, 0.01, "n/c: not confirmed in a primary source for this build. SiC field computed at 1e16 cm⁻³.",
         ha="center", fontsize=7.5)
fig.tight_layout(rect=(0, 0.04, 1, 1))
save(fig, f"{OUT}/material-properties.svg")
plt.close(fig)

# ------------------------------------------------------------------ figure 2
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.9))
Ns = np.logspace(14, 17, 13)
NsC = np.logspace(15, 17, 9)
axs[0].loglog(Ns, [breakdown(n, *SI)[2] for n in Ns], "o-", color=PALETTE[0], ms=3.5, label="Si")
axs[0].loglog(NsC, [breakdown(n, *SIC)[2] for n in NsC], "s-", color=PALETTE[1], ms=3.5, label="4H-SiC")
axs[0].set_xlabel("doping of the lightly doped side (cm⁻³)")
axs[0].set_ylabel("breakdown voltage (V)")
axs[0].set_title("(a) avalanche breakdown, one-sided junction", fontsize=9)
axs[0].legend(fontsize=8)


def design(V, mat, Nlo, Nhi, mu=None):
    N = brentq(lambda n: breakdown(n, *mat)[2] - V, Nlo, Nhi, rtol=1e-5)
    Em, W, _ = breakdown(N, *mat)
    m = mun(N) if mu is None else mu
    return W / (Q * m * N)


Vs = np.array([400, 600, 900, 1200, 1700, 2500, 3300])
axs[1].loglog(Vs, [design(V, SI, 5e12, 5e15) * 1e3 for V in Vs], "o-", color=PALETTE[0], ms=3.5, label="Si")
axs[1].loglog(Vs, [design(V, SIC, 5e14, 5e17, 1000) * 1e3 for V in Vs], "s-", color=PALETTE[1], ms=3.5,
              label="4H-SiC")
axs[1].set_xlabel("blocking voltage (V)")
axs[1].set_ylabel("ideal R_on,sp (mΩ·cm²)")
axs[1].set_title("(b) Baliga's unipolar limit", fontsize=9)
axs[1].legend(fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/breakdown-baliga.svg")
plt.close(fig)
print("figures written to", OUT)
