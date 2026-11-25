#!/usr/bin/env python3
"""Figures for chapter 23-05 (HBM in depth).

Run from anywhere:  python assets/figures/src/fig_23_05.py
Outputs
  assets/figures/23-05/stack-thermal.svg    base-die temperature rise against layer count for a 12.8 x 11 mm stack
                                            (30 um dies, 10 um gaps at 1.5 or 3 W/m-K, or hybrid bonding with no gap;
                                            10 W base die, 1 W per core die; Example 23-05.6's assumptions)
  assets/figures/23-05/hbm-generations.svg  per-stack bandwidth: HBM3 at 6.4 Gb/s (JEDEC), HBM3E at 9.6 Gb/s (SK hynix),
                                            HBM4 at 8 Gb/s (JEDEC), HBM4 at 11.7 Gb/s (Samsung), HBM4E at 14 Gb/s (Samsung)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import hbm  # noqa: E402

OUT = "assets/figures/23-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
AREA = 12.8e-3 * 11e-3


def stack_thermal() -> None:
    n = np.arange(4, 21)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    cases = (("10 µm gaps, 1.5 W/m·K", hbm.layer_resistance(AREA, 30e-6, 150, 10e-6, 1.5), PALETTE[1]),
             ("10 µm gaps, 3 W/m·K", hbm.layer_resistance(AREA, 30e-6, 150, 10e-6, 3.0), PALETTE[0]),
             ("hybrid bonding (no gap)", 30e-6 / (150 * AREA), PALETTE[2]))
    for lab, r, col in cases:
        ax.plot(n, [hbm.base_rise(int(k), r, 10, 1) for k in n], "o-", color=col, ms=3.5, label=lab)
    ax.set_xlabel("core dies in the stack")
    ax.set_ylabel("base-die rise above the lid (K)")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Bond gaps make tall stacks hot (10 W base, 1 W per core die)", fontsize=10)
    save(fig, f"{OUT}/stack-thermal.svg")


def generations() -> None:
    rows = [("HBM3\n6.4 Gb/s", 1024, 6.4e9), ("HBM3E\n9.6 Gb/s", 1024, 9.6e9), ("HBM4\n8 Gb/s (JEDEC)", 2048, 8e9),
            ("HBM4\n11.7 Gb/s", 2048, 11.7e9), ("HBM4E\n14 Gb/s", 2048, 14e9)]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    vals = [hbm.stack_bandwidth(w, r) / 1e12 for _, w, r in rows]
    cols = [PALETTE[0], PALETTE[0], PALETTE[1], PALETTE[1], PALETTE[2]]
    ax.bar([r[0] for r in rows], vals, color=cols)
    for i, val in enumerate(vals):
        ax.text(i, val + 0.05, f"{val:.2f}", ha="center", fontsize=8)
    ax.set_ylabel("bandwidth per stack (TB/s)")
    ax.set_ylim(0, 4.2)
    ax.set_title("1,024-bit stacks (blue), 2,048-bit HBM4 (orange) and HBM4E (green)", fontsize=10)
    ax.tick_params(axis="x", labelsize=8)
    save(fig, f"{OUT}/hbm-generations.svg")


if __name__ == "__main__":
    stack_thermal()
    generations()
