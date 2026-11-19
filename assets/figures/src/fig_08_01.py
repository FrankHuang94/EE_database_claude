#!/usr/bin/env python3
"""Figures for chapter 08-01 (number systems and codes).

Run from anywhere:  python assets/figures/src/fig_08_01.py
Outputs SVGs to assets/figures/08-01/: the 4-bit two's-complement wheel with its overflow seam, and the
spacing of representable values in FP16, bfloat16 and the two FP8 formats, computed by decoding every
bit pattern of each format from its field definition.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_wheel():
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    n = 4
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, color="0.75", lw=1))
    for u in range(2 ** n):
        s = u - 2 ** n if u >> (n - 1) else u
        ang = math.pi / 2 - 2 * math.pi * u / 2 ** n
        x, y = math.cos(ang), math.sin(ang)
        ax.plot(x, y, "o", ms=11, color=PALETTE[0] if s >= 0 else PALETTE[1])
        ax.text(1.27 * x, 1.27 * y, f"{u:04b}\n{s:+d}", ha="center", va="center", fontsize=9)
    seam = math.pi / 2 - 2 * math.pi * 7.5 / 2 ** n
    ax.plot([0, 1.12 * math.cos(seam)], [0, 1.12 * math.sin(seam)], "k--", lw=1.2)
    ax.text(-0.40, -0.30, "overflow seam\n(+7 to −8)", fontsize=9, ha="center")
    ax.annotate("", xy=(0.38, 0.62), xytext=(-0.38, 0.62),
                arrowprops=dict(arrowstyle="->", color="0.3", connectionstyle="arc3,rad=-0.35"))
    ax.text(0, 0.30, "adding 1 moves\nclockwise", fontsize=9, ha="center")
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("4-bit two's complement on the modulo-16 wheel")
    save(fig, f"{OUT}/twos-complement-wheel.svg")


def positive_values(e, m, kind):
    bias = 2 ** (e - 1) - 1
    vals = []
    for E in range(2 ** e):
        for F in range(2 ** m):
            if kind == "ieee" and E == 2 ** e - 1:
                continue
            if kind == "e4m3" and E == 2 ** e - 1 and F == 2 ** m - 1:
                continue
            v = (Fraction(F, 2 ** m) * Fraction(2) ** (1 - bias) if E == 0
                 else (1 + Fraction(F, 2 ** m)) * Fraction(2) ** (E - bias))
            if v > 0:
                vals.append(float(v))
    return np.array(sorted(vals))


def fig_spacing():
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    fmts = [("FP16 (E5M10)", 5, 10, "ieee", PALETTE[0]), ("bfloat16 (E8M7)", 8, 7, "ieee", PALETTE[3]),
            ("FP8 E5M2", 5, 2, "ieee", PALETTE[2]), ("FP8 E4M3", 4, 3, "e4m3", PALETTE[1])]
    for name, e, m, kind, color in fmts:
        v = positive_values(e, m, kind)
        keep = (v >= 1e-5) & (v <= 1e5)
        v = v[keep]
        ax.step(v[:-1], np.diff(v) / v[:-1], where="post", color=color, label=name, lw=1.4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-5, 1e5)
    ax.set_xlabel("magnitude $x$")
    ax.set_ylabel("relative gap to the next value")
    ax.set_title("Range and precision: relative spacing of representable values")
    ax.set_ylim(2e-4, 4)
    ax.legend(loc="center", bbox_to_anchor=(0.5, 0.48), ncol=2, fontsize=8)
    ax.text(2e-4, 1.6e-3, "normal numbers: the relative gap swings between $2^{-m}$ and $2^{-(m+1)}$",
            fontsize=8, ha="left")
    ax.text(1.3e-5, 1.6, "subnormals: the gap is fixed, so the\nrelative gap grows as x falls toward 0", fontsize=8)
    save(fig, f"{OUT}/format-spacing.svg")


if __name__ == "__main__":
    fig_wheel()
    fig_spacing()
    print("figures written to", OUT)
