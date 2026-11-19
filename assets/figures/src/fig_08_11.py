#!/usr/bin/env python3
"""Figures for chapter 08-11 (memories and programmable logic).

Run from anywhere:  python assets/figures/src/fig_08_11.py
Outputs SVGs to assets/figures/08-11/:
- memory-array.svg: the organization of a 64K x 16 memory as a 1024 x 1024 cell array with a row
  decoder, wordlines, bitlines and sixteen 64:1 column multiplexers (Example 08-11.1);
- break-even.svg: cost per unit of an ASIC (fixed NRE plus unit cost) and of an FPGA against volume,
  with the break-even volume N/(f - a) of Example 08-11.7 (hypothetical numbers).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def arrow(ax, p, q, color="black", lw=1.3):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, lw=lw, color=color,
                                 shrinkA=0, shrinkB=0))


def fig_array():
    words, width = 64 * 1024, 16
    rows = cols = int(math.isqrt(words * width))
    assert rows * cols == words * width and cols % width == 0
    per_row = cols // width
    rbits, cbits = int(math.log2(rows)), int(math.log2(per_row))
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.set_aspect("equal")
    ax.axis("off")
    # cell array
    ax.add_patch(Rectangle((3.5, 3.0), 7.0, 5.0, fill=False, lw=1.6))
    for k in range(1, 8):                               # a few wordlines
        y = 3.0 + k * 5.0 / 8
        ax.plot([3.5, 10.5], [y, y], color=PALETTE[0], lw=0.7, alpha=0.6)
    for k in range(1, 14):                              # a few bitlines
        x = 3.5 + k * 7.0 / 14
        ax.plot([x, x], [3.0, 8.0], color=PALETTE[2], lw=0.7, alpha=0.6)
    yw = 3.0 + 5 * 5.0 / 8
    ax.plot([3.5, 10.5], [yw, yw], color=PALETTE[0], lw=2.4)
    ax.text(7.0, 8.25, f"{rows} × {cols} bit cells ({rows * cols // 1024} kbit)", ha="center", fontsize=10)
    ax.text(10.6, yw, "selected\nwordline", va="center", fontsize=8.5, color=PALETTE[0])
    # row decoder
    ax.add_patch(Rectangle((1.6, 3.0), 1.4, 5.0, fill=False, lw=1.6))
    ax.text(2.3, 5.5, f"row\ndecoder\n{rbits} to\n{rows}", ha="center", va="center", fontsize=8)
    arrow(ax, (3.0, yw), (3.5, yw), PALETTE[0])
    arrow(ax, (0.2, 5.5), (1.6, 5.5))
    ax.text(0.15, 5.85, f"A[{rbits + cbits - 1}:{cbits}]", fontsize=8.5)
    # column multiplexers
    ax.add_patch(Rectangle((3.5, 1.6), 7.0, 0.9, fill=False, lw=1.6))
    ax.text(7.0, 2.05, f"sense amplifiers and {width} column multiplexers ({per_row}:1)", ha="center",
            va="center", fontsize=8)
    for k in range(1, 14):
        x = 3.5 + k * 7.0 / 14
        ax.plot([x, x], [2.5, 3.0], color=PALETTE[2], lw=0.7, alpha=0.6)
    ax.text(10.6, 2.75, "bitlines", fontsize=8.5, color=PALETTE[2])
    arrow(ax, (0.2, 2.05), (3.5, 2.05))
    ax.text(0.15, 2.35, f"A[{cbits - 1}:0]", fontsize=8.5)
    arrow(ax, (7.0, 1.6), (7.0, 0.6))
    ax.text(7.2, 0.9, f"data out: {width} bits", fontsize=9)
    ax.set_title(f"A {words // 1024}K × {width} memory: {rbits} row-address bits, {cbits} column-address bits",
                 fontsize=10.5)
    save(fig, f"{OUT}/memory-array.svg")


def fig_breakeven():
    nre, a, f = 5e6, 5.0, 50.0
    v = np.logspace(3, 7, 300)
    asic = a + nre / v
    vstar = nre / (f - a)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.loglog(v, asic, color=PALETTE[0], label="ASIC: USD 5 per unit + USD 5 M NRE spread over volume")
    ax.loglog(v, np.full_like(v, f), color=PALETTE[1], label="FPGA: USD 50 per unit")
    ax.axvline(vstar, color="0.5", ls=":", lw=1)
    ax.annotate(f"break-even\n{vstar:,.0f} units", (vstar, f), textcoords="offset points", xytext=(10, 25),
                fontsize=9)
    ax.set_xlabel("volume (units)")
    ax.set_ylabel("cost per unit (USD)")
    ax.set_title("FPGA or ASIC: fixed versus variable cost (hypothetical numbers)", fontsize=10.5)
    ax.legend(fontsize=8.5, loc="upper right")
    save(fig, f"{OUT}/break-even.svg")


if __name__ == "__main__":
    fig_array()
    fig_breakeven()
    print("figures written to", OUT)
