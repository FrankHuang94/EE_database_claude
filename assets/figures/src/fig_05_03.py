#!/usr/bin/env python3
"""Figures for chapter 05-03 (SciPy, SymPy and Matplotlib).

Run from anywhere:  python assets/figures/src/fig_05_03.py
Outputs SVGs to assets/figures/05-03/.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/05-03"
use_style()
B, O, G = PALETTE[0], PALETTE[1], PALETTE[2]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_axes_choice():
    fc = 1e3
    f = np.logspace(0, 6, 400)
    mag = 1 / np.sqrt(1 + (f / fc) ** 2)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    ax.plot(f / 1e3, mag, color=B, lw=2)
    ax.set_xlabel("frequency (kHz)")
    ax.set_ylabel("|H| (V/V)")
    ax.set_title("Linear axes: everything interesting is squeezed near zero", fontsize=9.5)
    ax = axes[1]
    ax.semilogx(f, 20 * np.log10(mag), color=B, lw=2, label="RC low-pass, f_c = 1 kHz")
    ax.axvline(fc, color=O, ls="--", lw=1)
    ax.axhline(-3.01, color=O, ls="--", lw=1)
    ax.annotate("−3 dB at f_c", (fc, -3.01), xytext=(1.6e3, 3), fontsize=8, color=O)
    ax.plot(f[f >= fc], -20 * np.log10(f[f >= fc] / fc), color=G, ls=":", lw=2, label="−20 dB per decade asymptote")
    ax.set_ylim(-65, 8)
    ax.set_xlabel("frequency (Hz, log scale)")
    ax.set_ylabel("|H| (dB)")
    ax.set_title("Log frequency and dB: corner and slope are readable", fontsize=9.5)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/axes-choice.svg")


if __name__ == "__main__":
    fig_axes_choice()
