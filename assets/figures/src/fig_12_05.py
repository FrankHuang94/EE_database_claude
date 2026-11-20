#!/usr/bin/env python3
"""Figures for chapter 12-05 (feedback: theory and the four topologies).

Run from anywhere:  python assets/figures/src/fig_12_05.py
Outputs SVGs to assets/figures/12-05/:
- bandwidth-extension.svg: the closed-loop magnitude response of Example 12-05.2's single-pole amplifier
  (A0 = 1e5, pole at 10 Hz) open loop and with beta = 0.001, 0.01, 0.1 and 1, computed from
  A(jf)/(1 + beta A(jf)); every curve meets the same gain-bandwidth asymptote A0 f_p / f.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
A0, FP = 1e5, 10.0


def fig_bandwidth_extension():
    f = np.logspace(0, 7, 600)
    A = A0 / (1 + 1j * f / FP)
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.semilogx(f, 20 * np.log10(np.abs(A)), color="0.25", lw=2, label="open loop")
    for k, beta in enumerate((1e-3, 1e-2, 1e-1, 1.0)):
        H = A / (1 + beta * A)
        ax.semilogx(f, 20 * np.log10(np.abs(H)), color=PALETTE[k], lw=1.8, label=f"β = {beta:g}")
        fb = FP * (1 + beta * A0)
        ax.plot(fb, 20 * np.log10(abs(A0 / (1 + beta * A0))) - 3.0103, "o", color=PALETTE[k], ms=4)
    ax.semilogx(f, 20 * np.log10(A0 * FP / f), ":", color="0.5", lw=1, label="GBW asymptote")
    ax.set_xlim(1, 1e7)
    ax.set_ylim(-10, 110)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("gain (dB)")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/bandwidth-extension.svg")


if __name__ == "__main__":
    fig_bandwidth_extension()
