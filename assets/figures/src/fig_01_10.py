#!/usr/bin/env python3
"""Figures for chapter 01-10 (multivariable calculus II).

Run:  python assets/figures/src/fig_01_10.py  -> assets/figures/01-10/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, Wedge

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/01-10"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_power_map():
    x = np.linspace(0, 10, 200)
    y = np.linspace(0, 10, 200)
    XX, YY = np.meshgrid(x, y)
    p = 0.2 + 0.02 * XX * YY
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    im = ax.pcolormesh(XX, YY, p, shading="auto", cmap="inferno")
    fig.colorbar(im, ax=ax, label="power density (W/mm²)")
    ax.set_aspect("equal")
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_title("p(x, y) = 0.2 + 0.02xy: total ∬ p dA = 70 W")
    fig.tight_layout()
    save(fig, f"{OUT}/die-power-map.svg")


def fig_polar_element():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.2))
    a1.add_patch(Wedge((0, 0), 1.3, 25, 40, width=0.25, color=B, alpha=0.5))
    for r in (1.05, 1.3):
        t = np.linspace(0, np.pi / 2, 100)
        a1.plot(r * np.cos(t), r * np.sin(t), color="0.7", lw=0.8)
    for ang in (25, 40):
        a1.plot([0, 1.6 * math.cos(math.radians(ang))], [0, 1.6 * math.sin(math.radians(ang))], color="0.6", lw=0.8)
    a1.text(1.38, 0.62, "dA ≈ (r dθ)(dr)", fontsize=10)
    a1.text(0.45, 0.12, "dθ", fontsize=10)
    a1.annotate("dr", xy=(1.17, 0.68), xytext=(1.0, 1.05), fontsize=10, arrowprops=dict(arrowstyle="->"))
    a1.set_xlim(0, 2)
    a1.set_ylim(0, 1.6)
    a1.set_aspect("equal")
    a1.set_title("Polar area element: dA = r dr dθ")
    a1.set_xlabel("x")
    a1.set_ylabel("y")
    r = np.linspace(0, 2.5, 300)
    a2.plot(r, np.exp(-2 * r**2), color=B, label="intensity e^(−2r²/w²)")
    a2.plot(r, 1 - np.exp(-2 * r**2), color=O, label="power inside radius r")
    a2.axvline(1, color="0.6", ls=":")
    a2.text(1.03, 0.9, "r = w: 86.5 %", fontsize=9)
    a2.set_xlabel("r / w")
    a2.legend(fontsize=8, loc="center right")
    a2.set_title("A Gaussian beam: enclosed power by a polar integral")
    fig.tight_layout()
    save(fig, f"{OUT}/polar-and-gaussian-beam.svg")


def fig_wafer():
    d, s = 300.0, 25.0  # large dies drawn so they are visible
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.add_patch(Circle((0, 0), d / 2, fill=False, lw=1.5, color="k"))
    full = part = 0
    for i in np.arange(-d / 2, d / 2, s):
        for j in np.arange(-d / 2, d / 2, s):
            corners = [(i, j), (i + s, j), (i, j + s), (i + s, j + s)]
            inside = sum(math.hypot(cx, cy) <= d / 2 for cx, cy in corners)
            if inside == 4:
                ax.add_patch(Rectangle((i, j), s, s, fc=B, ec="white", alpha=0.7))
                full += 1
            elif inside > 0:
                ax.add_patch(Rectangle((i, j), s, s, fc=O, ec="white", alpha=0.35))
                part += 1
    ax.set_xlim(-160, 160)
    ax.set_ylim(-160, 160)
    ax.set_aspect("equal")
    ax.set_title(f"300 mm wafer, 25 mm dies: {full} whole, {part} lost at the edge", fontsize=10)
    ax.axis("off")
    fig.tight_layout()
    save(fig, f"{OUT}/wafer-edge-loss.svg")


def fig_fields():
    x = np.linspace(-2, 2, 13)
    XX, YY = np.meshgrid(x, x)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4.4))
    a1.quiver(XX, YY, 2 * XX * YY, XX**2, color=B)
    a1.set_title("Conservative: F = ∇(x²y) = (2xy, x²)\nline integrals depend only on the end points")
    U, V = -YY, XX
    a2.quiver(XX, YY, U, V, color=O)
    t = np.linspace(0, 2 * np.pi, 200)
    a2.plot(1.5 * np.cos(t), 1.5 * np.sin(t), color="k", lw=1)
    a2.set_title("Rotational: F = (−y, x), curl = 2\n∮ F·dr around the circle = 2 × enclosed area")
    for a in (a1, a2):
        a.set_aspect("equal")
        a.set_xlabel("x")
        a.set_ylabel("y")
    fig.tight_layout()
    save(fig, f"{OUT}/vector-fields.svg")


if __name__ == "__main__":
    fig_power_map()
    fig_polar_element()
    fig_wafer()
    fig_fields()
    print("01-10 figures written")
