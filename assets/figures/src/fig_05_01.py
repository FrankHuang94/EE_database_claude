#!/usr/bin/env python3
"""Figures for chapter 05-01 (Python fundamentals for engineers).

Run from anywhere:  python assets/figures/src/fig_05_01.py
Outputs SVGs to assets/figures/05-01/.
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

OUT = "assets/figures/05-01"
use_style()
B, O, G = PALETTE[0], PALETTE[1], PALETTE[2]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_float_spacing():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    x = np.logspace(-6, 18, 400)
    ax.loglog(x, np.spacing(x), color=B, lw=2, label="gap to the next float")
    ax.loglog(x, x * 2.0**-52, color=O, ls="--", lw=1.2, label="x · 2⁻⁵² (machine epsilon × x)")
    for val, txt in ((1.0, "at 1: 2.2×10⁻¹⁶"), (2.0**53, "at 2⁵³ ≈ 9×10¹⁵: gap of 2")):
        ax.plot(val, np.spacing(val), "o", color=G)
        ax.annotate(txt, (val, np.spacing(val)), xytext=(8, -14), textcoords="offset points", fontsize=8)
    ax.set_xlabel("magnitude of the number")
    ax.set_ylabel("spacing between adjacent float64 values")
    ax.set_title("Floats have about 16 significant digits at every scale", fontsize=9.5)
    ax.legend(fontsize=8, loc="upper left")
    ax = axes[1]
    from fractions import Fraction
    n_values = np.unique(np.logspace(0, 6, 60).astype(int))
    tenth = Fraction(0.1)                                 # the exact value of the float nearest 0.1
    acc, rep = [], []
    for n in map(int, n_values):
        total = 0.0
        for _ in range(n):
            total += 0.1
        acc.append(abs(float(Fraction(total) - n * tenth)))          # rounding in the additions
        rep.append(float(n * tenth - Fraction(n, 10)))               # 0.1 is not exactly a float
    acc = np.array(acc)
    ax.loglog(n_values, np.where(acc > 0, acc, np.nan), "o-", color=B, ms=3, lw=1.2,
              label="rounding in the additions (total += 0.1)")
    ax.loglog(n_values, rep, color=O, lw=1.5, ls="--", label="representation: N × (float(0.1) − 0.1)")
    ax.set_xlabel("number of additions N")
    ax.set_ylabel("error in the sum")
    ax.set_title("Two error sources when adding 0.1 N times", fontsize=9.5)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/float-spacing.svg")


if __name__ == "__main__":
    fig_float_spacing()
