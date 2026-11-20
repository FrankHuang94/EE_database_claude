#!/usr/bin/env python3
"""Figures for chapter 13-01 (vector calculus refresher).

Run from anywhere:  python assets/figures/src/fig_13_01.py
Outputs SVGs to assets/figures/13-01/:
- curl.svg: two azimuthal fields on the same grid: rho phi_hat (rigid rotation, curl 2 z_hat everywhere) and
  phi_hat/rho (the field outside a wire, curl-free away from the axis), with a small square loop drawn in each.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/13-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_curl():
    g = np.linspace(-2, 2, 15)
    X, Y = np.meshgrid(g, g)
    R = np.hypot(X, Y)
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.0))
    for ax, (title, U, V) in zip(axes, (("ρ φ̂: curl = 2 ẑ everywhere", -Y, X),
                                         ("φ̂/ρ: curl = 0 away from the axis", -Y / np.maximum(R, 0.3) ** 2,
                                          X / np.maximum(R, 0.3) ** 2))):
        mask = R > (0.25 if "everywhere" in title else 0.6)
        ax.quiver(X[mask], Y[mask], U[mask], V[mask], color=PALETTE[0], angles="xy", width=0.004)
        ax.plot([1.0, 1.5, 1.5, 1.0, 1.0], [-0.25, -0.25, 0.25, 0.25, -0.25], color=PALETTE[1], lw=1.5)
        ax.set_title(title, fontsize=9)
        ax.set_aspect("equal")
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, f"{OUT}/curl.svg")


if __name__ == "__main__":
    fig_curl()
