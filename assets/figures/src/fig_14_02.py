#!/usr/bin/env python3
"""Figures for chapter 14-02 (instruction set architecture).

Run from anywhere:  python assets/figures/src/fig_14_02.py
Outputs SVGs to assets/figures/14-02/:
- formats.svg: the six RV32I instruction formats drawn to scale as 32-bit fields (bit 31 on the left),
  coloured by role: opcode, destination register, source registers, function codes and immediate bits,
  with each immediate field labelled by the immediate bits it holds.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/14-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

COL = {"op": PALETTE[7], "rd": PALETTE[1], "rs": PALETTE[0], "fn": PALETTE[2], "imm": PALETTE[4]}
# (high bit, low bit, label, role) for each field, most significant first
FORMATS = [
    ("R", [(31, 25, "funct7", "fn"), (24, 20, "rs2", "rs"), (19, 15, "rs1", "rs"), (14, 12, "funct3", "fn"),
           (11, 7, "rd", "rd"), (6, 0, "opcode", "op")]),
    ("I", [(31, 20, "imm[11:0]", "imm"), (19, 15, "rs1", "rs"), (14, 12, "funct3", "fn"), (11, 7, "rd", "rd"),
           (6, 0, "opcode", "op")]),
    ("S", [(31, 25, "imm[11:5]", "imm"), (24, 20, "rs2", "rs"), (19, 15, "rs1", "rs"), (14, 12, "funct3", "fn"),
           (11, 7, "imm[4:0]", "imm"), (6, 0, "opcode", "op")]),
    ("B", [(31, 31, "12", "imm"), (30, 25, "imm[10:5]", "imm"), (24, 20, "rs2", "rs"), (19, 15, "rs1", "rs"),
           (14, 12, "funct3", "fn"), (11, 8, "imm[4:1]", "imm"), (7, 7, "11", "imm"), (6, 0, "opcode", "op")]),
    ("U", [(31, 12, "imm[31:12]", "imm"), (11, 7, "rd", "rd"), (6, 0, "opcode", "op")]),
    ("J", [(31, 31, "20", "imm"), (30, 21, "imm[10:1]", "imm"), (20, 20, "11", "imm"), (19, 12, "imm[19:12]", "imm"),
           (11, 7, "rd", "rd"), (6, 0, "opcode", "op")]),
]


def fig_formats():
    fig, ax = plt.subplots(figsize=(9.0, 4.2))
    h, gap = 0.8, 0.35
    for row, (name, fields) in enumerate(FORMATS):
        y = -row * (h + gap)
        assert sum(hi - lo + 1 for hi, lo, _, _ in fields) == 32
        for hi, lo, label, role in fields:
            x0, w = 31 - hi, hi - lo + 1
            ax.add_patch(Rectangle((x0, y), w, h, facecolor=to_rgba(COL[role], 0.30 if role != "op" else 0.18),
                                   edgecolor="black", lw=0.8))
            ax.text(x0 + w / 2, y + h / 2, label, ha="center", va="center", fontsize=7 if w > 1 else 6)
        ax.text(-0.8, y + h / 2, f"{name}-type", ha="right", va="center", fontsize=9, weight="bold")
    for b in (31, 25, 24, 20, 19, 15, 14, 12, 11, 7, 6, 0):
        ax.text(31 - b + 0.5, h + 0.12, str(b), ha="center", va="bottom", fontsize=6.5)
    handles = [Rectangle((0, 0), 1, 1, facecolor=to_rgba(COL[k], 0.3), edgecolor="black") for k in ("op", "rd", "rs", "fn", "imm")]
    ax.legend(handles, ["opcode", "destination rd", "sources rs1, rs2", "function codes", "immediate bits"],
              loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=5, fontsize=7, frameon=False)
    ax.set_xlim(-4.2, 32.2)
    ax.set_ylim(-5 * (h + gap) - 0.15, h + 0.6)
    ax.axis("off")
    ax.set_title("RV32I instruction formats: register fields never move; the sign bit is always bit 31", fontsize=9)
    save(fig, f"{OUT}/formats.svg")


if __name__ == "__main__":
    fig_formats()
