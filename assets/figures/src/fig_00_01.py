#!/usr/bin/env python3
"""Figures for chapter 00-01 (the map of electrical engineering).

Run:  python assets/figures/src/fig_00_01.py  -> assets/figures/00-01/*.svg
Data: WSTS 2025 market by segment, research log R-016 (as of Nov 2026).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
SEGMENTS = {  # US$ billions, 2025, WSTS (R-016)
    "Logic": 299.547, "Memory": 230.042, "Analog": 86.519, "Micro (MPU/MCU)": 84.867,
    "Optoelectronics": 43.042, "Discretes": 30.728, "Sensors": 20.894,
}


def fig_market():
    names, vals = list(SEGMENTS), list(SEGMENTS.values())
    total = sum(vals)
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    bars = ax.barh(names[::-1], vals[::-1], color=PALETTE[0])
    for b, val in zip(bars, vals[::-1]):
        ax.text(b.get_width() + 4, b.get_y() + b.get_height() / 2, f"${val:.0f} B ({100 * val / total:.1f}%)",
                va="center", fontsize=9)
    ax.set_xlim(0, 380)
    ax.set_xlabel("2025 sales (US$ billions)")
    ax.set_title(f"Global semiconductor market by segment, 2025: ${total:.1f} B\n(WSTS; research log R-016)")
    ax.grid(axis="y", visible=False)
    save(fig, "assets/figures/00-01/market-by-segment.svg")


if __name__ == "__main__":
    fig_market()
    print("00-01 figures written")
