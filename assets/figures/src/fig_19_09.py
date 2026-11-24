#!/usr/bin/env python3
"""Figures for chapter 19-09 (layout, design rules and standard cells).

Run from anywhere:  python assets/figures/src/fig_19_09.py
Outputs
  assets/figures/19-09/aoi22-stick.svg   stick diagram of an AOI22 gate, F = not(AB + CD), with the input order
                                         A-B-D-C (a common Euler path): one p-diffusion strip and one n-diffusion
                                         strip, four vertical poly gates, the electrical node at each diffusion
                                         segment from the two Euler walks, the VDD and GND rails, the metal-2
                                         strap joining the three m regions and the metal-1 output strap F
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/19-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

order = ["A", "B", "D", "C"]
p_nodes = ["m", "VDD", "m", "F", "m"]      # pull-up walk m-A-VDD-B-m-D-F-C-m
n_nodes = ["F", "x", "GND", "y", "F"]      # pull-down walk F-A-x-B-GND-D-y-C-F
M1, M2, POLY = PALETTE[0], PALETTE[3], PALETTE[1]
YP, YN, YVDD, YGND, YM2, YF = 2.85, 1.15, 4.45, -0.45, 3.45, 2.0
fig, ax = plt.subplots(figsize=(7.4, 5.0))
ax.add_patch(plt.Rectangle((0.0, 2.6), 9.0, 0.5, color=PALETTE[4], alpha=0.45))
ax.add_patch(plt.Rectangle((0.0, 0.9), 9.0, 0.5, color=PALETTE[2], alpha=0.45))
ax.text(9.15, YP, "p-diffusion\n(pull-up)", va="center", fontsize=8)
ax.text(9.15, YN, "n-diffusion\n(pull-down)", va="center", fontsize=8)
# power rails (metal 1)
ax.plot([-0.2, 9.0], [YVDD, YVDD], color=M1, lw=6, solid_capstyle="butt")
ax.plot([-0.2, 9.0], [YGND, YGND], color=M1, lw=6, solid_capstyle="butt")
ax.text(9.15, YVDD, "VDD rail", va="center", fontsize=8)
ax.text(9.15, YGND, "GND rail", va="center", fontsize=8)
# poly gates
for i, g in enumerate(order):
    x = 1.5 + 2 * i
    ax.plot([x, x], [0.6, 3.65], color=POLY, lw=3)
    ax.text(x, 3.8, g, ha="center", fontsize=11, color=POLY, weight="bold")
# node labels and contact positions
cx = [0.5 + 2 * i + 0.25 for i in range(5)]
for i, (pn, nn) in enumerate(zip(p_nodes, n_nodes)):
    x = 0.5 + 2 * i - 0.3
    ax.text(x, YP, pn, ha="center", va="center", fontsize=8)
    ax.text(x, YN, nn, ha="center", va="center", fontsize=8)


def contact(x, y):
    ax.plot([x], [y], marker="x", color="black", ms=7, mew=1.6, zorder=5)


# VDD and GND drops to their diffusion regions (metal 1)
ax.plot([cx[1], cx[1]], [YP, YVDD], color=M1, lw=2.5)
contact(cx[1], YP)
ax.plot([cx[2], cx[2]], [YN, YGND], color=M1, lw=2.5)
contact(cx[2], YN)
# node m: three p-diffusion regions joined on metal 2 through metal-1 stubs and vias
for k in (0, 2, 4):
    ax.plot([cx[k], cx[k]], [YP, YM2], color=M1, lw=2.5)
    contact(cx[k], YP)
    ax.add_patch(plt.Rectangle((cx[k] - 0.09, YM2 - 0.09), 0.18, 0.18, fill=False, ec="black", lw=1.2, zorder=5))
ax.plot([cx[0], cx[4]], [YM2, YM2], color=M2, lw=2.5, ls="--")
ax.text(cx[4] + 0.15, YM2 + 0.12, "m (metal 2)", fontsize=8, color=M2)
# output F: p-diffusion F region and both n-diffusion F regions joined on metal 1
ax.plot([cx[0], cx[4] + 0.6], [YF, YF], color=M1, lw=2.5)
for k, y in ((0, YN), (4, YN), (3, YP)):
    ax.plot([cx[k], cx[k]], [y, YF], color=M1, lw=2.5)
    contact(cx[k], y)
ax.text(cx[4] + 0.7, YF, "F", va="center", fontsize=11, weight="bold")
# legend
handles = [plt.Line2D([], [], color=POLY, lw=3, label="poly (gate)"),
           plt.Line2D([], [], color=M1, lw=2.5, label="metal 1"),
           plt.Line2D([], [], color=M2, lw=2.5, ls="--", label="metal 2"),
           plt.Line2D([], [], color="black", marker="x", ls="", ms=7, label="contact to diffusion"),
           plt.Line2D([], [], color="black", marker="s", mfc="none", ls="", ms=6, label="via, metal 1 to metal 2")]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, fontsize=7.5, frameon=False)
ax.set_xlim(-0.4, 10.6)
ax.set_ylim(-0.8, 4.8)
ax.axis("off")
ax.set_title("AOI22, input order A-B-D-C: unbroken diffusion in both networks", fontsize=10)
save(fig, f"{OUT}/aoi22-stick.svg")
