#!/usr/bin/env python3
"""Figures for chapter 13-09 (the Smith chart and impedance matching).

Run from anywhere:  python assets/figures/src/fig_13_09.py
Outputs SVGs to assets/figures/13-09/:
- smith.svg: a Smith chart drawn from its definition (constant-r circles and constant-x arcs clipped to the unit
  disc), with the load z = 2 + j1, its |Gamma| circle, and its image after lambda/8 toward the generator, 1 - j1.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/13-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def gamma(z):
    return (z - 1) / (z + 1)


def fig_smith():
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color="k", lw=1.2)
    xs = np.concatenate([np.linspace(-60, -1e-3, 3000), np.linspace(1e-3, 60, 3000)])
    for r in (0.2, 0.5, 1, 2, 5):
        g = gamma(r + 1j * np.linspace(-60, 60, 6001))
        ax.plot(g.real, g.imag, color="0.6", lw=0.7)
        ax.text(r / (1 + r) - 1 / (1 + r) + 0.01, 0.02, f"{r:g}", fontsize=6, color="0.35")
    for x in (0.2, 0.5, 1, 2, 5):
        for sgn in (1, -1):
            g = gamma(np.linspace(0, 60, 6001) + 1j * sgn * x)
            ax.plot(g.real, g.imag, color="0.6", lw=0.7)
        gl = gamma(1j * x)
        ax.text(gl.real * 1.08, gl.imag * 1.08, f"+j{x:g}", fontsize=6, color="0.35", ha="center", va="center")
        ax.text(gl.real * 1.08, -gl.imag * 1.08, f"−j{x:g}", fontsize=6, color="0.35", ha="center", va="center")
    ax.plot([-1, 1], [0, 0], color="0.6", lw=0.7)
    del xs
    g1 = gamma(2 + 1j)
    g2 = g1 * np.exp(-1j * np.pi / 2)
    ax.plot(abs(g1) * np.cos(th), abs(g1) * np.sin(th), "--", color=PALETTE[2], lw=1.0)
    arc = abs(g1) * np.exp(1j * np.linspace(np.angle(g1), np.angle(g1) - np.pi / 2, 50))
    ax.plot(arc.real, arc.imag, color=PALETTE[1], lw=2.0)
    ax.annotate("", (arc.real[-1], arc.imag[-1]), (arc.real[-3], arc.imag[-3]),
                arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=1.5))
    ax.plot(g1.real, g1.imag, "o", color=PALETTE[0], ms=6)
    ax.plot(g2.real, g2.imag, "s", color=PALETTE[1], ms=6)
    ax.annotate("z = 2 + j1 (load)", (g1.real, g1.imag), (0.35, 0.55), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.annotate("z = 1 − j1 after λ/8\ntoward generator", (g2.real, g2.imag), (0.25, -0.75), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.plot(0, 0, "+", color="k", ms=8)
    ax.text(-1.0, -1.08, "short", fontsize=7)
    ax.text(0.86, -1.08, "open", fontsize=7)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, f"{OUT}/smith.svg")


if __name__ == "__main__":
    fig_smith()
