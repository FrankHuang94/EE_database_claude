#!/usr/bin/env python3
"""Figures for chapter 13-04 (Maxwell's equations and time-varying fields).

Run from anywhere:  python assets/figures/src/fig_13_04.py
Outputs SVGs to assets/figures/13-04/:
- conduction-vs-displacement.svg: sigma / (omega eps) against frequency for copper, seawater, doped and
  intrinsic silicon, and a laminate with a constant loss tangent of 0.02.
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

OUT = "assets/figures/13-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
EPS0 = 8.8541878128e-12


def fig_ratio():
    f = np.logspace(3, 13, 500)
    mats = [("copper", 5.8e7, 1.0), ("doped Si (0.5 Ω·cm)", 200.0, 11.7), ("seawater", 4.0, 81.0),
            ("intrinsic Si (2.3 × 10⁵ Ω·cm)", 1 / 2.3e3, 11.7)]
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    for i, (name, sig, er) in enumerate(mats):
        ax.loglog(f, sig / (2 * math.pi * f * er * EPS0), color=PALETTE[i], lw=1.6, label=name)
    ax.loglog(f, np.full_like(f, 0.02), "--", color=PALETTE[4], lw=1.4, label="laminate, tan δ = 0.02")
    ax.axhline(1, color="k", lw=0.9)
    ax.text(2e3, 8, "conduction dominates", fontsize=7.5)
    ax.text(2e3, 0.06, "displacement dominates", fontsize=7.5)
    ax.set_xlim(1e3, 1e13)
    ax.set_ylim(1e-5, 1e15)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("σ / ωε")
    ax.legend(fontsize=7, loc="upper right")
    save(fig, f"{OUT}/conduction-vs-displacement.svg")


if __name__ == "__main__":
    fig_ratio()
