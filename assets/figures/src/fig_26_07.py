#!/usr/bin/env python3
"""Figures for chapter 26-07 (engineering ethics).

Run from anywhere:  python assets/figures/src/fig_26_07.py
Outputs
  assets/figures/26-07/export-thresholds.svg  the October 2023 ECCN 3A090 criteria drawn as regions of total
                                              processing performance (TPP) and performance density, with the
                                              four chips of Example 26-07.5 (an aid to reading the rule text)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "26-engineering-design-and-professional-practice" / "labs" / "26-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import safety as s  # noqa: E402

OUT = "assets/figures/26-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def main() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    xmax, ymax = 10000, 12
    # 3A090.a: TPP >= 4800 (any density), or TPP >= 1600 with density >= 5.92
    ax.add_patch(Rectangle((4800, 0), xmax - 4800, ymax, color=PALETTE[1], alpha=0.25, lw=0))
    ax.add_patch(Rectangle((1600, 5.92), 4800 - 1600, ymax - 5.92, color=PALETTE[1], alpha=0.25, lw=0))
    # 3A090.b: 2400 <= TPP < 4800 with 1.6 <= density < 5.92, or TPP >= 1600 with 3.2 <= density < 5.92
    ax.add_patch(Rectangle((2400, 1.6), 4800 - 2400, 5.92 - 1.6, color=PALETTE[0], alpha=0.2, lw=0))
    ax.add_patch(Rectangle((1600, 3.2), 2400 - 1600, 5.92 - 3.2, color=PALETTE[0], alpha=0.2, lw=0))
    ax.text(7000, 9.5, "3A090.a", ha="center", fontsize=9)
    ax.text(3600, 3.4, "3A090.b", ha="center", fontsize=9)
    ax.text(700, 1.0, "neither", ha="center", fontsize=9)
    chips = {"A": (1000, 8, 800), "B": (250, 16, 600), "C": (200, 8, 800), "D": (50, 8, 100)}
    for name, (tops, bits, area) in chips.items():
        t = s.tpp(tops, bits)
        d = s.performance_density(t, area)
        ax.plot([t], [d], "ko", ms=5)
        ax.annotate(name, (t, d), xytext=(5, 4), textcoords="offset points", fontsize=9)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xlabel("total processing performance, TPP (TOPS × bit length)")
    ax.set_ylabel("performance density (TPP per mm²)")
    ax.set_title("ECCN 3A090 criteria (Oct 2023 text), datacenter chips")
    fig.tight_layout()
    save(fig, f"{OUT}/export-thresholds.svg")


if __name__ == "__main__":
    main()
