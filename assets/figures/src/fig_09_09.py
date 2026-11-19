#!/usr/bin/env python3
"""Figures for chapter 09-09 (the long-channel MOSFET).

Run from anywhere:  python assets/figures/src/fig_09_09.py
Outputs assets/figures/09-09/mosfet-channel-iv.svg for the chapter's transistor (W = 10 um, L = 1 um,
4 nm oxide, N_A = 5e17 cm^-3, V_TH = 0.4 V, m = 1.246, mu = 315.1 cm^2/Vs, V_GS = 1.2 V):
(a) channel potential along the channel and (b) inversion charge along the channel for several V_DS, from
current continuity; (c) output characteristics for several V_GS (bulk-charge model) with the V_Dsat locus.
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

OUT = "assets/figures/09-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

M, VT0, MU, COX, W, L = 1.2464636770172024, 0.4, 315.10796454504873, 8.63283312333e-7, 10e-4, 1e-4
K = W / L * MU * COX


def profile(vgs, vds, n=400):
    """V_c(x) from I dx = W mu C q dV with q = vov - m V: closed-form inverse of x(V)."""
    vov = vgs - VT0
    I = K * (vov - M * vds / 2) * vds
    V = np.linspace(0, vds, n)
    x = W * MU * COX * (vov * V - M * V ** 2 / 2) / I
    return x, V, vov - M * V


fig, axs = plt.subplots(1, 3, figsize=(11.5, 3.6))
vov = 1.2 - VT0
vdsat = vov / M
for i, vds in enumerate((0.2, 0.4, vdsat * 0.9999)):
    x, V, qq = profile(1.2, vds)
    lab = f"$V_{{DS}}$ = {vds:.2f} V" if i < 2 else f"$V_{{DS}} = V_{{Dsat}}$ = {vdsat:.3f} V"
    axs[0].plot(x / L, V, color=PALETTE[i], label=lab)
    axs[1].plot(x / L, qq / vov, color=PALETTE[i], label=lab)
axs[0].set_xlabel("position along channel $x/L$")
axs[0].set_ylabel("channel potential $V_c$ (V)")
axs[0].set_title("(a) channel potential")
axs[0].legend(fontsize=7, loc="upper left")
axs[1].set_xlabel("position along channel $x/L$")
axs[1].set_ylabel(r"$|Q_{inv}| / C_{ox}V_{ov}$")
axs[1].set_title("(b) inversion charge")
axs[1].set_ylim(0, 1.05)
vds = np.linspace(0, 1.5, 300)
for i, vgs in enumerate((0.8, 1.0, 1.2)):
    vo = vgs - VT0
    vs = vo / M
    idv = np.where(vds < vs, K * (vo - M * vds / 2) * vds, K * vo ** 2 / (2 * M))
    axs[2].plot(vds, idv * 1e3, color=PALETTE[i], label=f"$V_{{GS}}$ = {vgs:.1f} V")
vg = np.linspace(0.45, 1.25, 50)
axs[2].plot((vg - VT0) / M, K * (vg - VT0) ** 2 / (2 * M) * 1e3, color="k", ls=":", lw=1, label="$V_{DS} = V_{Dsat}$")
axs[2].set_xlabel("$V_{DS}$ (V)")
axs[2].set_ylabel("$I_D$ (mA)")
axs[2].set_title("(c) output characteristics")
axs[2].legend(fontsize=7, loc="center right")
fig.tight_layout()
save(fig, f"{OUT}/mosfet-channel-iv.svg")
plt.close(fig)
print("figures written to", OUT)
