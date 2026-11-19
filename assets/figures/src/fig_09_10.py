#!/usr/bin/env python3
"""Figures for chapter 09-10 (short-channel effects and leakage).

Run from anywhere:  python assets/figures/src/fig_09_10.py
Outputs to assets/figures/09-10/, for the chapter's example NMOS (2 nm EOT, m = 1.2, V_TH = 0.35 V,
mu_ns = 183 cm^2/Vs, v_sat = 8e6 cm/s, W = 1 um):
- velocity-saturation-iv.svg: output characteristics at L = 50 nm, long-channel model vs velocity saturation;
- idsat-vs-length.svg: I_Dsat against L at 0.65 V overdrive, long-channel, velocity-saturation and
  source-injection (B = 1) limits;
- vt-rolloff-dibl.svg: Hu's roll-off model with l_d = 10 nm against L at two drain biases, and the
  subthreshold curves of a 30 nm device at V_DS = 0.05 V and 1.0 V (S = 80 mV/decade).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

EOX = 3.9 * 8.8541878128e-14
COX = EOX / 2e-7
M, VTH, MU, VSAT, W = 1.2, 0.35, 183.0, 8e6, 1e-4
ESAT = 2 * VSAT / MU


def vdsat(vov, L):
    return 1 / (M / vov + 1 / (ESAT * L))


def i_vs(vds, vov, L):
    """Hu's Eq. (6.9.3) below V_Dsat, constant above it (A)."""
    vd = vdsat(vov, L)
    v = np.minimum(vds, vd)
    return W / L * MU * COX * (vov - M * v / 2) * v / (1 + v / (ESAT * L))


def i_long(vds, vov, L):
    vd = vov / M
    v = np.minimum(vds, vd)
    return W / L * MU * COX * (vov - M * v / 2) * v


# ------------------------------------------------------------------ figure 1
fig, ax = plt.subplots(figsize=(6.2, 4.0))
vds = np.linspace(0, 1.0, 300)
L = 50e-7
for i, vgs in enumerate((0.6, 0.8, 1.0)):
    vov = vgs - VTH
    ax.plot(vds, i_long(vds, vov, L) * 1e3, color=PALETTE[i], ls="--", lw=1.2)
    ax.plot(vds, i_vs(vds, vov, L) * 1e3, color=PALETTE[i], label=f"$V_{{GS}}$ = {vgs:.1f} V")
vg = np.linspace(0.36, 1.0, 60)
ax.plot([vdsat(g - VTH, L) for g in vg], [float(i_vs(10, g - VTH, L)) * 1e3 for g in vg], color="k", ls=":", lw=1,
        label="$V_{Dsat}$ with velocity saturation")
ax.set_xlabel("$V_{DS}$ (V)")
ax.set_ylabel(r"$I_D$ (mA/µm)")
ax.set_title("L = 50 nm: long-channel model (dashed) vs velocity saturation (solid)", fontsize=9)
ax.legend(fontsize=8, loc="upper left")
fig.tight_layout()
save(fig, f"{OUT}/velocity-saturation-iv.svg")
plt.close(fig)

# ------------------------------------------------------------------ figure 2
fig, ax = plt.subplots(figsize=(6.2, 4.0))
VOV = 0.65
Ls = np.logspace(np.log10(20e-7), np.log10(2e-4), 200)
ax.loglog(Ls * 1e7, [float(i_long(10, VOV, x)) * 1e3 for x in Ls], color=PALETTE[0], ls="--",
          label=r"long-channel ($\propto 1/L$)")
ax.loglog(Ls * 1e7, [float(i_vs(10, VOV, x)) * 1e3 for x in Ls], color=PALETTE[1], label="velocity saturation")
ax.loglog(Ls * 1e7, np.full_like(Ls, W * 1.6e7 * COX * VOV * 1e3), color=PALETTE[2], ls=":",
          label="source-injection limit, B = 1")
ax.set_xlabel("channel length L (nm)")
ax.set_ylabel(r"$I_{Dsat}$ (mA/µm)")
ax.set_title(r"Saturation current at $V_{ov}$ = 0.65 V", fontsize=9)
ax.legend(fontsize=8, loc="upper right")
fig.tight_layout()
save(fig, f"{OUT}/idsat-vs-length.svg")
plt.close(fig)

# ------------------------------------------------------------------ figure 3
LD, S = 10e-7, 0.080
roll = lambda L, vds: (vds + 0.4) * np.exp(-L / LD)
fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.8))
Lr = np.linspace(15e-7, 100e-7, 200)
for i, vd in enumerate((0.05, 1.0)):
    axs[0].plot(Lr * 1e7, 0.35 - roll(Lr, vd), color=PALETTE[i], label=f"$V_{{DS}}$ = {vd} V")
axs[0].axhline(0.35, color="k", lw=0.8, ls=":")
axs[0].text(70, 0.355, "long-channel $V_{TH}$", fontsize=8)
axs[0].set_xlabel("channel length L (nm)")
axs[0].set_ylabel("$V_{TH}$ (V)")
axs[0].set_title(r"(a) roll-off and DIBL, $l_d$ = 10 nm", fontsize=9)
axs[0].legend(fontsize=8, loc="lower right")
vg = np.linspace(0, 0.6, 200)
for i, vd in enumerate((0.05, 1.0)):
    vt = 0.35 - roll(30e-7, vd)
    axs[1].semilogy(vg, 1e-7 * 10 ** ((vg - vt) / S), color=PALETTE[i], label=f"$V_{{DS}}$ = {vd} V")
axs[1].set_xlabel("$V_{GS}$ (V)")
axs[1].set_ylabel(r"$I_D$ (A), $W/L$ = 1")
axs[1].set_title("(b) subthreshold curves at L = 30 nm, S = 80 mV/decade", fontsize=9)
axs[1].legend(fontsize=8, loc="lower right")
fig.tight_layout()
save(fig, f"{OUT}/vt-rolloff-dibl.svg")
plt.close(fig)
print("figures written to", OUT)
