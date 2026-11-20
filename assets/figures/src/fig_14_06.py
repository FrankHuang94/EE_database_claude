#!/usr/bin/env python3
"""Figures for chapter 14-06 (pipelining and hazards).

Run from anywhere:  python assets/figures/src/fig_14_06.py
Outputs SVGs to assets/figures/14-06/:
- pipeline.svg: a pipeline diagram (instructions against clock cycles) for
  lw x5,0(x10); add x6,x5,x7; beq x6,x6,L; sub; or; L: xor; ebreak on the five-stage pipeline of §3.2: the add
  stalls one cycle in ID (load-use), the beq is resolved in EX and taken, so the two wrong-path instructions are
  flushed. The last instruction completes in cycle 12 = 5 + 4 + 1 + 2 x 1, the model of §3.5; the verify
  script runs the same sequence on the Verilog core.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/14-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# (instruction, [(cycle, label, kind)]) with kind: normal, stall, flushed
ROWS = [
    ("lw   x5, 0(x10)",  [(1, "IF", "n"), (2, "ID", "n"), (3, "EX", "n"), (4, "MEM", "n"), (5, "WB", "n")]),
    ("add  x6, x5, x7",  [(2, "IF", "n"), (3, "ID", "n"), (4, "ID", "s"), (5, "EX", "n"), (6, "MEM", "n"), (7, "WB", "n")]),
    ("beq  x6, x6, L",   [(3, "IF", "n"), (4, "IF", "s"), (5, "ID", "n"), (6, "EX", "n"), (7, "MEM", "n"), (8, "WB", "n")]),
    ("sub  (wrong path)", [(5, "IF", "f"), (6, "ID", "f")]),
    ("or   (wrong path)", [(6, "IF", "f")]),
    ("L: xor x8, x6, x5", [(7, "IF", "n"), (8, "ID", "n"), (9, "EX", "n"), (10, "MEM", "n"), (11, "WB", "n")]),
    ("ebreak",           [(8, "IF", "n"), (9, "ID", "n"), (10, "EX", "n"), (11, "MEM", "n"), (12, "WB", "n")]),
]
COL = {"IF": PALETTE[0], "ID": PALETTE[2], "EX": PALETTE[1], "MEM": PALETTE[4], "WB": PALETTE[3]}


def fig_pipeline():
    n = len(ROWS)
    assert max(c for _, cells in ROWS for c, _, _ in cells) == 5 + 4 + 1 + 2 * 1  # model: N + 4 + S + 2T with N = 5
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    for r, (name, cells) in enumerate(ROWS):
        y = n - 1 - r
        for c, lab, kind in cells:
            if kind == "f":
                ax.add_patch(Rectangle((c - 1, y), 1, 0.8, facecolor="0.88", edgecolor="0.5", hatch="xx", lw=0.6))
                ax.text(c - 0.5, y + 0.4, lab, ha="center", va="center", fontsize=7, color="0.45")
            elif kind == "s":
                ax.add_patch(Rectangle((c - 1, y), 1, 0.8, facecolor="white", edgecolor=COL[lab], hatch="///", lw=0.8))
                ax.text(c - 0.5, y + 0.4, "stall", ha="center", va="center", fontsize=6.5)
            else:
                ax.add_patch(Rectangle((c - 1, y), 1, 0.8, facecolor=COL[lab], alpha=0.35, edgecolor="black", lw=0.6))
                ax.text(c - 0.5, y + 0.4, lab, ha="center", va="center", fontsize=7.5)
        ax.text(-0.2, y + 0.4, name, ha="right", va="center", family="monospace", fontsize=7.5)
    for c in range(1, 13):
        ax.text(c - 0.5, n + 0.05, str(c), ha="center", va="bottom", fontsize=7.5)
    ax.text(6.5, n + 0.55, "clock cycle", ha="center", va="bottom", fontsize=8)
    ax.annotate("load-use: add is held in ID for one cycle\n(and beq in IF); x5 then comes from MEM/WB", xy=(3.6, n - 1.6), xytext=(8.6, n - 1.1),
                fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.annotate("beq taken in EX: the two\nyounger instructions are flushed", xy=(5.6, 2.4), xytext=(8.6, 2.9),
                fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.7))
    ax.set_xlim(-4.2, 12.2)
    ax.set_ylim(-0.3, n + 1.0)
    ax.axis("off")
    save(fig, f"{OUT}/pipeline.svg")


if __name__ == "__main__":
    fig_pipeline()
