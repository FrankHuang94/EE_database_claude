#!/usr/bin/env python3
"""Figures for chapter 08-05 (Verilog and testbenches).

Run from anywhere:  python assets/figures/src/fig_08_05.py
Outputs SVGs to assets/figures/08-05/: the active and non-blocking regions of one simulation time
step, applied to a three-stage shift register; and expected random-test coverage against the number of
vectors, computed from 1 - (1 - 1/M)^N with the coupon-collector mean marked.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_regions():
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    w, h, y = 2.5, 1.5, 1.0
    boxes = [
        (0.2, "posedge clk\n(the triggering event)", "0.85"),
        (3.2, "ACTIVE region\nevaluate every\nright-hand side:\nd = 1, q1 = 0, q2 = 0", PALETTE[5]),
        (6.2, "NBA region\nupdate all\ntogether:\nq1 = 1, q2 = 0, q3 = 0", PALETTE[4]),
        (9.2, "next time step", "0.85"),
    ]
    for x, text, col in boxes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=col, ec="k", alpha=0.6))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)
    for x in (2.75, 5.75, 8.75):
        ax.annotate("", xy=(x + 0.4, y + h / 2), xytext=(x, y + h / 2), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.annotate("", xy=(8.75, 2.9), xytext=(3.1, 2.9), arrowprops=dict(arrowstyle="<->", color="0.4"))
    ax.text(5.95, 3.05, "one simulation time step", ha="center", fontsize=10)
    ax.text(5.95, 0.45, "q1 <= d;   q2 <= q1;   q3 <= q2;", ha="center", fontsize=10, family="monospace")
    ax.text(5.95, 0.1, "every right-hand side is read before any register changes, so each stage gets its neighbor's old value",
            ha="center", fontsize=9)
    ax.set_xlim(0, 11.9)
    ax.set_ylim(-0.1, 3.3)
    ax.axis("off")
    save(fig, f"{OUT}/scheduler-regions.svg")


def fig_coverage():
    M = 2 ** 16
    x = np.linspace(0, 14, 600)
    cov = 100 * (1 - (1 - 1 / M) ** (x * M))
    H = sum(1.0 / j for j in range(1, M + 1))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(x, cov, color=PALETTE[0], lw=2)
    ax.axvline(1, color=PALETTE[1], lw=1, ls="--")
    ax.text(1.15, 40, "N = M:\n63.2% covered", color=PALETTE[1], fontsize=9)
    ax.axvline(H, color=PALETTE[2], lw=1, ls="--")
    ax.text(H - 0.15, 40, f"expected N to cover\nevery input: {H:.1f} M", color=PALETTE[2], fontsize=9, ha="right")
    ax.set_xlabel("random vectors N, in units of the input-space size M")
    ax.set_ylabel("expected coverage (%)")
    ax.set_ylim(0, 102)
    ax.set_title(f"Random-test coverage, M = 2^16 = {M:,} inputs")
    save(fig, f"{OUT}/random-coverage.svg")


if __name__ == "__main__":
    fig_regions()
    fig_coverage()
    print("figures written to", OUT)
