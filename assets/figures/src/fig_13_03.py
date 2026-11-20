#!/usr/bin/env python3
"""Figures for chapter 13-03 (magnetostatics and inductance).

Run from anywhere:  python assets/figures/src/fig_13_03.py
Outputs SVGs to assets/figures/13-03/:
- coax-field.svg: flux density against radius for a coaxial cable carrying 1 A (inner radius 0.5 mm, outer
  conductor 1.75 to 2.0 mm), from Ampere's law with the enclosed current.
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

OUT = "assets/figures/13-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
MU0 = 4e-7 * math.pi
A, B, C, I = 0.5e-3, 1.75e-3, 2.0e-3, 1.0


def i_enc(r):
    """Enclosed current: uniform in the inner conductor, uniform return in the outer conductor."""
    inner = I * np.clip(r / A, 0, 1) ** 2
    outer = -I * np.clip((r**2 - B**2) / (C**2 - B**2), 0, 1)
    return inner + outer


def fig_coax():
    r = np.linspace(1e-6, 2.6e-3, 2000)
    Bf = MU0 * i_enc(r) / (2 * math.pi * r)
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for lo, hi in ((0, A), (B, C)):
        ax.axvspan(lo * 1e3, hi * 1e3, color=PALETTE[3], alpha=0.18, lw=0)
    ax.plot(r * 1e3, Bf * 1e3, color=PALETTE[0], lw=1.8)
    ax.plot([0.25, 0.5, 1.0], [0.2, 0.4, 0.2], "o", color=PALETTE[1], ms=4)
    ax.annotate("0.4 mT at the surface", (0.5, 0.4), (0.7, 0.36), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate("∝ ρ inside", (0.25, 0.2), (0.01, 0.31), fontsize=8)
    ax.annotate("∝ 1/ρ in the dielectric", (1.0, 0.2), (1.05, 0.25), fontsize=8)
    ax.text(0.25, 0.03, "inner\nconductor", ha="center", fontsize=7)
    ax.text(1.875, 0.03, "outer\nconductor", ha="center", fontsize=7)
    ax.text(2.3, 0.08, "zero outside", ha="center", fontsize=8)
    ax.set_xlabel("radius ρ (mm)")
    ax.set_ylabel("flux density B (mT)")
    ax.set_xlim(0, 2.6)
    ax.set_ylim(0, 0.45)
    save(fig, f"{OUT}/coax-field.svg")


if __name__ == "__main__":
    fig_coax()
