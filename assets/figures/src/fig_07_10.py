#!/usr/bin/env python3
"""Figures for chapter 07-10 (two-port networks).

Run from anywhere:  python assets/figures/src/fig_07_10.py
Outputs SVGs to assets/figures/07-10/: the two-port sign conventions, and the twin-T notch built by
adding y-parameters (Problem 07-10.8).
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

OUT = "assets/figures/07-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_conventions():
    fig, ax = plt.subplots(figsize=(6.2, 2.6))
    ax.add_patch(plt.Rectangle((3, 0.3), 3, 2.4, fill=False, lw=1.6))
    ax.text(4.5, 1.5, "linear two-port\n(no independent sources)", ha="center", va="center", fontsize=10)
    for x0, x1, xt, side in ((0.6, 3, 0.6, "1"), (6, 8.4, 8.4, "2")):
        ax.plot([x0, x1], [2.4, 2.4], color="k", lw=1.2)
        ax.plot([x0, x1], [0.6, 0.6], color="k", lw=1.2)
        ax.plot([xt], [2.4], "o", mfc="white", mec="k")
        ax.plot([xt], [0.6], "o", mfc="white", mec="k")
        xm = (x0 + x1) / 2
        direction = 1 if side == "1" else -1
        ax.annotate("", xy=(xm + 0.35 * direction, 2.4), xytext=(xm - 0.35 * direction, 2.4),
                    arrowprops={"arrowstyle": "-|>", "color": PALETTE[1], "lw": 1.4})
        ax.text(xm, 2.6, f"$I_{side}$", ha="center", color=PALETTE[1], fontsize=11)
        ax.annotate("", xy=(xm - 0.35 * direction, 0.6), xytext=(xm + 0.35 * direction, 0.6),
                    arrowprops={"arrowstyle": "-|>", "color": PALETTE[1], "lw": 1.4})
        ax.text(xt + (-0.35 if side == "1" else 0.35), 1.5, f"$V_{side}$", ha="center", va="center", fontsize=11)
        ax.text(xt + (-0.35 if side == "1" else 0.35), 2.15, "+", ha="center", fontsize=11)
        ax.text(xt + (-0.35 if side == "1" else 0.35), 0.75, "−", ha="center", fontsize=11)
    ax.text(1.8, 0.05, "port 1", ha="center", fontsize=9, color="0.3")
    ax.text(7.2, 0.05, "port 2", ha="center", fontsize=9, color="0.3")
    ax.set_xlim(-0.2, 9.2)
    ax.set_ylim(-0.2, 3.0)
    ax.axis("off")
    fig.tight_layout()
    save(fig, f"{OUT}/two-port-conventions.svg")


def fig_twin_t():
    R, C = 10e3, 10e-9
    f0 = 1 / (2 * math.pi * R * C)
    f = np.logspace(math.log10(f0 / 20), math.log10(f0 * 20), 2000)

    def yT(Za, Zb, Zc):
        return np.linalg.inv(np.array([[Za + Zc, Zc], [Zc, Zb + Zc]]))

    g = []
    for ff in f:
        s = 2j * math.pi * ff
        y = yT(R, R, 1 / (s * 2 * C)) + yT(1 / (s * C), 1 / (s * C), R / 2)
        g.append(-y[1, 0] / y[1, 1])
    g = np.array(g)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.semilogx(f, 20 * np.log10(np.maximum(np.abs(g), 1e-6)), color=PALETTE[0])
    ax.axvline(f0, color="0.7", lw=0.6)
    ax.text(f0 * 1.1, -55, "$f_0$ = 1.59 kHz", fontsize=8)
    ax.set_ylim(-60, 2)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("open-circuit gain (dB)")
    fig.tight_layout()
    save(fig, f"{OUT}/twin-t-notch.svg")


if __name__ == "__main__":
    fig_conventions()
    fig_twin_t()
