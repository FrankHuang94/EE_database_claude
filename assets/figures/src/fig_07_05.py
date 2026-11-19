#!/usr/bin/env python3
"""Figures for chapter 07-05 (sinusoidal steady state, phasors and impedance).

Run from anywhere:  python assets/figures/src/fig_07_05.py
Outputs SVGs to assets/figures/07-05/: the phasor diagram of Example 07-05.4 (line drops drawn ten
times larger than scale so that they are visible).
"""
from __future__ import annotations

import cmath
import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/07-05"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def arrow(ax, z0, z1, color, label, offset=(0, 0)):
    ax.annotate("", xy=(z1.real, z1.imag), xytext=(z0.real, z0.imag),
                arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.6})
    mid = (z0 + z1) / 2
    ax.text(mid.real + offset[0], mid.imag + offset[1], label, color=color, fontsize=9)


def fig_feeder():
    VL = 23 + 0j
    I = VL / (18.4 + 13.8j)
    k = 10.0                                     # exaggeration of the line drops
    dR = 0.5 * I * k
    dX = 0.3j * I * k
    VS = VL + dR + dX
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    arrow(ax, 0, VL, B, "$\\mathbf{V}_L = 23\\angle 0^\\circ$ V", (0, -0.9))
    arrow(ax, VL, VL + dR, O, "$R\\mathbf{I}$ (×10)", (0.2, -0.6))
    arrow(ax, VL + dR, VS, P, "$jX\\mathbf{I}$ (×10)", (0.3, 0))
    arrow(ax, 0, VS, G, "$\\mathbf{V}_S$", (-1.5, 0.4))
    arrow(ax, 0, I * 12, "0.35", "$\\mathbf{I}$ (scaled), lags 36.9°", (0.5, -0.4))
    ax.axhline(0, color="0.8", lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlim(-1, 30)
    ax.set_ylim(-9, 4)
    ax.set_xlabel("real part (V)")
    ax.set_ylabel("imaginary part (V)")
    fig.tight_layout()
    save(fig, f"{OUT}/feeder-phasors.svg")
    return abs(VS), cmath.phase(VS)


if __name__ == "__main__":
    fig_feeder()
    print("07-05 figures written to", OUT)
