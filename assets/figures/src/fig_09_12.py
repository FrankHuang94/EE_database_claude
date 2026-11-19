#!/usr/bin/env python3
"""Figures for chapter 09-12 (advanced transistors).

Run from anywhere:  python assets/figures/src/fig_09_12.py
Outputs to assets/figures/09-12/:
- transistor-architectures.svg: schematic cross-sections (current into the page) of a planar bulk MOSFET,
  a FinFET, a gate-all-around nanosheet stack and a CFET (n-sheets over p-sheets); not to scale;
- scale-length-dibl.svg: (a) center potential along a 20 nm double-gate channel (7 nm body, 1 nm oxide) at
  V_DS = 0.05 V and 0.7 V from the scale-length model; (b) DIBL against gate length for 5 nm and 7 nm
  double-gate bodies and a 7 nm single-gate body.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/09-12"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

SI, OX, GATE, SUB = "#9ecae1", "#fdd49e", "#636363", "#c6dbef"
PSI = "#fcbba1"


def rect(ax, x, y, w, h, fc, ec="k", lw=0.6, z=1):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw, zorder=z))


def wrapped_sheet(ax, x, y, w, h, fc, tox=0.12):
    rect(ax, x - tox, y - tox, w + 2 * tox, h + 2 * tox, OX, lw=0.4, z=3)
    rect(ax, x, y, w, h, fc, lw=0.5, z=4)


fig, axs = plt.subplots(1, 4, figsize=(12, 3.6))
for ax in axs:
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_aspect("equal")
    ax.axis("off")

# (a) planar
ax = axs[0]
rect(ax, 0.3, 0.3, 5.4, 2.7, SUB)
rect(ax, 1.5, 3.0, 3.0, 0.15, OX)
rect(ax, 1.5, 3.15, 3.0, 1.2, GATE)
ax.plot([1.5, 4.5], [2.97, 2.97], color=PALETTE[3], lw=2.5)
ax.text(3.0, 1.5, "doped Si body", ha="center", fontsize=8)
ax.text(3.0, 3.6, "gate", ha="center", color="w", fontsize=8)
ax.text(4.6, 2.6, "channel", fontsize=7, color=PALETTE[3])
ax.set_title("(a) planar", fontsize=9)

# (b) FinFET
ax = axs[1]
rect(ax, 0.3, 0.3, 5.4, 1.2, SUB)
rect(ax, 0.3, 1.5, 5.4, 0.6, OX)
rect(ax, 2.45, 1.5, 0.5, 0.6, SUB, lw=0)
rect(ax, 1.0, 2.1, 4.0, 2.9, GATE)
rect(ax, 2.33, 2.1, 0.74, 2.3, OX, z=2)
rect(ax, 2.45, 1.5, 0.5, 2.78, SI, z=3)
ax.text(2.7, 0.8, "Si substrate", ha="center", fontsize=8)
ax.text(1.0, 1.7, "isolation oxide", fontsize=6.5)
ax.text(3.9, 4.4, "gate", ha="center", color="w", fontsize=8)
ax.annotate("fin\n($W_{fin}$, $H_{fin}$)", (2.7, 3.2), xytext=(3.4, 2.5), fontsize=7, color="w",
            arrowprops=dict(arrowstyle="-", color="w", lw=0.6))
ax.set_title("(b) FinFET", fontsize=9)

# (c) nanosheet GAA
ax = axs[2]
rect(ax, 0.3, 0.3, 5.4, 1.2, SUB)
rect(ax, 0.3, 1.5, 5.4, 0.4, OX)
rect(ax, 1.0, 1.9, 4.0, 3.4, GATE)
for k in range(3):
    wrapped_sheet(ax, 1.6, 2.3 + 0.95 * k, 2.8, 0.35, SI)
ax.text(3.0, 0.8, "Si substrate", ha="center", fontsize=8)
ax.text(3.0, 5.0, "gate (all around)", ha="center", color="w", fontsize=7.5)
ax.text(1.15, 3.45, "sheets", fontsize=6.5, color="w", rotation=90)
ax.set_title("(c) nanosheet GAA", fontsize=9)

# (d) CFET
ax = axs[3]
rect(ax, 0.3, 0.3, 5.4, 0.9, SUB)
rect(ax, 0.3, 1.2, 5.4, 0.4, OX)
rect(ax, 1.0, 1.6, 4.0, 4.1, GATE)
for k in range(2):
    wrapped_sheet(ax, 1.6, 2.0 + 0.8 * k, 2.8, 0.32, PSI)
for k in range(2):
    wrapped_sheet(ax, 1.6, 3.9 + 0.8 * k, 2.8, 0.32, SI)
ax.plot([1.0, 5.0], [3.55, 3.55], color="w", lw=0.8, ls="--")
ax.text(4.55, 4.35, "n", color="w", fontsize=9)
ax.text(4.55, 2.45, "p", color="w", fontsize=9)
ax.text(3.0, 0.6, "Si substrate", ha="center", fontsize=8)
ax.set_title("(d) CFET: n over p", fontsize=9)
fig.text(0.5, 0.02, "Cross-sections across the channel (current flows into the page); schematic, not to scale",
         ha="center", fontsize=8)
fig.tight_layout(rect=(0, 0.05, 1, 1))
save(fig, f"{OUT}/transistor-architectures.svg")
plt.close(fig)

# ------------------------------------------------------------------ figure 2
lam_dg = lambda t, tox: math.sqrt(3 * t * tox / 2 + t * t / 8)
lam_sg = lambda t, tox: math.sqrt(3 * t * tox + t * t / 2)


def u_profile(x, L, lam, a, b):
    return (a * np.sinh((L - x) / lam) + b * np.sinh(x / lam)) / np.sinh(L / lam)


def umin(L, lam, a, b):
    x = np.linspace(0, L, 4001)
    return u_profile(x, L, lam, a, b).min()


fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.8))
x = np.linspace(0, 20, 400)
for i, vds in enumerate((0.05, 0.7)):
    axs[0].plot(x, u_profile(x, 20, lam_dg(7, 1), 0.2, 0.2 + vds) * 1e3, color=PALETTE[i], label=f"$V_{{DS}}$ = {vds} V")
axs[0].set_ylim(0, 300)
axs[0].set_xlabel("position along channel x (nm)")
axs[0].set_ylabel(r"$\phi_c - V_G'$ (mV)")
axs[0].set_title("(a) center potential, 20 nm channel, 7 nm double-gate body", fontsize=9)
axs[0].legend(fontsize=8)
Ls = np.linspace(20, 45, 120)
for i, (lam, lab) in enumerate(((lam_dg(5, 1), "double gate, 5 nm"), (lam_dg(7, 1), "double gate, 7 nm"),
                                (lam_sg(7, 1), "single gate, 7 nm"))):
    d = [(umin(L, lam, 0.2, 0.9) - umin(L, lam, 0.2, 0.25)) / 0.65 * 1e3 for L in Ls]
    axs[1].semilogy(Ls, d, color=PALETTE[i], label=lab)
axs[1].set_xlabel("gate length L (nm)")
axs[1].set_ylabel("DIBL (mV/V)")
axs[1].set_title("(b) DIBL from the scale-length model (1 nm oxide)", fontsize=9)
axs[1].legend(fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/scale-length-dibl.svg")
plt.close(fig)
print("figures written to", OUT)
