#!/usr/bin/env python3
"""Figures for chapter 13-02 (electrostatic boundary-value problems).

Run from anywhere:  python assets/figures/src/fig_13_02.py
Outputs SVGs to assets/figures/13-02/:
- trough.svg: equipotentials of the square trough (top at 1 V, other sides grounded) from the separation-of-
  variables series, 0.1 V apart, with the 0.25 V centre marked.
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

OUT = "assets/figures/13-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def series(x, y, nterms=300):
    """Trough potential for a unit square, top at 1 V, evaluated without overflow."""
    V = np.zeros_like(x)
    for n in range(1, 2 * nterms, 2):
        ky, kb = n * math.pi * y, n * math.pi
        V += 4 / (n * math.pi) * np.exp(ky - kb) * (1 - np.exp(-2 * ky)) / (1 - math.exp(-2 * kb)) * np.sin(n * math.pi * x)
    return V


def fig_trough():
    x, y = np.meshgrid(np.linspace(0, 1, 301), np.linspace(0, 0.999, 300))
    V = series(x, y)
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    levels = np.round(np.arange(0.1, 1.0, 0.1), 2)
    cs = ax.contour(x, y, V, levels=levels, colors=PALETTE[0], linewidths=1.1)
    yc = np.linspace(0, 0.999, 2000)                 # place each label on the centre line x = a/2
    vc = series(np.full_like(yc, 0.5), yc)
    ax.clabel(cs, fmt="%.1f V", fontsize=7, manual=[(0.5, float(np.interp(lv, vc, yc))) for lv in levels])
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color="k", lw=1.5)
    ax.plot([0, 1], [1, 1], color=PALETTE[1], lw=3)
    ax.text(0.5, 1.025, "1 V", ha="center", fontsize=8, color=PALETTE[1])
    ax.plot(0.5, 0.5, "o", color=PALETTE[2], ms=5)
    ax.annotate("centre: 0.25 V", (0.5, 0.5), (0.6, 0.47), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.text(0.5, -0.07, "grounded", ha="center", fontsize=8)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.1, 1.08)
    ax.set_aspect("equal")
    ax.set_xlabel("x / a")
    ax.set_ylabel("y / a")
    fig.tight_layout()
    save(fig, f"{OUT}/trough.svg")


if __name__ == "__main__":
    fig_trough()
