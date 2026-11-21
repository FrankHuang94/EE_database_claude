#!/usr/bin/env python3
"""Figures for chapter 19-09 (layout, design rules and standard cells).

Run from anywhere:  python assets/figures/src/fig_19_09.py
Outputs
  assets/figures/19-09/aoi22-stick.svg   stick diagram of an AOI22 gate, F = not(AB + CD), with the input order
                                         A-B-D-C (a common Euler path): one p-diffusion strip and one n-diffusion
                                         strip, four vertical poly gates, and the electrical node at each diffusion
                                         segment from the two Euler walks
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
fig, ax = plt.subplots(figsize=(7.0, 4.2))
ax.add_patch(plt.Rectangle((0.3, 2.6), 8.4, 0.5, color=PALETTE[4], alpha=0.5))
ax.add_patch(plt.Rectangle((0.3, 0.9), 8.4, 0.5, color=PALETTE[2], alpha=0.5))
ax.text(8.9, 2.85, "p-diffusion\n(pull-up)", va="center", fontsize=8)
ax.text(8.9, 1.15, "n-diffusion\n(pull-down)", va="center", fontsize=8)
for i, g in enumerate(order):
    x = 1.5 + 2 * i
    ax.plot([x, x], [0.5, 3.5], color=PALETTE[1], lw=3)
    ax.text(x, 3.65, g, ha="center", fontsize=11, color=PALETTE[1], weight="bold")
for i, (pn, nn) in enumerate(zip(p_nodes, n_nodes)):
    x = 0.5 + 2 * i
    ax.text(x, 2.85, pn, ha="center", va="center", fontsize=8)
    ax.text(x, 1.15, nn, ha="center", va="center", fontsize=8)
ax.set_xlim(0, 10.2)
ax.set_ylim(0.2, 4.0)
ax.axis("off")
ax.set_title("AOI22, input order A-B-D-C: unbroken diffusion in both networks", fontsize=10)
save(fig, f"{OUT}/aoi22-stick.svg")
