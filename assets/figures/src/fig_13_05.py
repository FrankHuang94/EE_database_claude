#!/usr/bin/env python3
"""Figures for chapter 13-05 (plane waves in lossless and lossy media).

Run from anywhere:  python assets/figures/src/fig_13_05.py
Outputs SVGs to assets/figures/13-05/:
- skin-depth.svg: skin depth of copper and aluminium against frequency (left axis), with copper's surface
  resistance (right axis), from the good-conductor formulas.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/13-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
MU0 = 4e-7 * math.pi


def fig_skin():
    f = np.logspace(1, 11, 400)
    fig, ax = plt.subplots(figsize=(5.8, 3.7))
    for i, (name, sig) in enumerate((("copper", 5.8e7), ("aluminium", 3.5e7))):
        ax.loglog(f, 1e6 / np.sqrt(np.pi * f * MU0 * sig), color=PALETTE[i], lw=1.8, label=f"skin depth, {name}")
    for fm, lab in ((60, "60 Hz: 8.5 mm"), (1e6, "1 MHz: 66 µm"), (1e9, "1 GHz: 2.1 µm")):
        d = 1e6 / math.sqrt(math.pi * fm * MU0 * 5.8e7)
        ax.plot(fm, d, "o", color=PALETTE[0], ms=4)
        ax.annotate(lab, (fm, d), (fm * 1.8, d * 1.6), fontsize=7.5)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("skin depth (µm)")
    ax2 = ax.twinx()
    ax2.loglog(f, np.sqrt(np.pi * f * MU0 / 5.8e7) * 1e3, "--", color=PALETTE[2], lw=1.4, label="copper R_s (right axis)")
    ax2.set_ylabel("surface resistance (mΩ per square)")
    lines = ax.get_lines()[:2] + ax2.get_lines()
    ax.legend(lines, [ln.get_label() for ln in lines], fontsize=7, loc="upper center")
    save(fig, f"{OUT}/skin-depth.svg")


if __name__ == "__main__":
    fig_skin()
