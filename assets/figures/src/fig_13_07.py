#!/usr/bin/env python3
"""Figures for chapter 13-07 (transmission lines in the time domain).

Run from anywhere:  python assets/figures/src/fig_13_07.py
Outputs SVGs to assets/figures/13-07/:
- bounce.svg: bounce (lattice) diagram for Example 13-07.3 (10 ohm source, 50 ohm line, open end, 1 ns delay)
  beside the receiver voltage it implies.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/13-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_bounce():
    vp, gs, gl = 50 / 60, -2 / 3, 1.0
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.8), gridspec_kw={"width_ratios": [1, 1.3]})
    wave = vp
    for k in range(4):
        t0 = 2 * k
        ax1.annotate("", (1, t0 + 1), (0, t0), arrowprops=dict(arrowstyle="->", color=PALETTE[0], lw=1.2))
        ax1.text(0.42, t0 + 0.35, f"{wave:+.3f} V", fontsize=7, color=PALETTE[0])
        wave_r = wave * gl
        ax1.annotate("", (0, t0 + 2), (1, t0 + 1), arrowprops=dict(arrowstyle="->", color=PALETTE[1], lw=1.2))
        ax1.text(0.55, t0 + 1.28, f"{wave_r:+.3f} V", fontsize=7, color=PALETTE[1])
        wave = wave_r * gs
    ax1.set_xlim(-0.08, 1.08)
    ax1.set_ylim(8.2, -0.2)
    ax1.set_xticks([0, 1], ["source\nΓS = −2/3", "load (open)\nΓL = +1"])
    ax1.set_ylabel("time (ns)")
    ax1.set_title("bounce diagram", fontsize=9)
    t = np.linspace(0, 12, 1200)
    v = np.zeros_like(t)
    for k in range(40):
        v += np.where(t >= 2 * k + 1, 2 * vp * gs**k, 0.0)
    ax2.plot(t, v, color=PALETTE[2], lw=1.6)
    ax2.axhline(1, color="0.5", lw=0.8, ls="--")
    for tk, val in ((1, 1.667), (3, 0.5556), (5, 1.296), (7, 0.8025)):
        ax2.annotate(f"{val}", (tk + 0.1, val), fontsize=7)
    ax2.set_xlabel("time (ns)")
    ax2.set_ylabel("receiver voltage (V)")
    ax2.set_title("receiver voltage: rings at 250 MHz, settles to 1 V", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/bounce.svg")


if __name__ == "__main__":
    fig_bounce()
