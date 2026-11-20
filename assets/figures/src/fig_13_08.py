#!/usr/bin/env python3
"""Figures for chapter 13-08 (transmission lines in sinusoidal steady state).

Run from anywhere:  python assets/figures/src/fig_13_08.py
Outputs SVGs to assets/figures/13-08/:
- standing-waves.svg: voltage magnitude along a lossless 50 ohm line (forward wave 1 V) for a short, an open,
  a matched load, 100 ohm and 25 ohm, over one wavelength from the load.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/13-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_standing():
    d = np.linspace(0, 1, 801)
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    for i, (name, ZL) in enumerate((("short", 0.0), ("open", 1e12), ("matched", 50.0), ("100 Ω (VSWR 2)", 100.0),
                                    ("25 Ω (VSWR 2)", 25.0))):
        g = (ZL - 50) / (ZL + 50)
        ax.plot(d, np.abs(1 + g * np.exp(-4j * np.pi * d)), color=PALETTE[i], lw=1.6, label=name)
    ax.set_xlabel("distance from the load (wavelengths)")
    ax.set_ylabel("|V| (forward wave = 1 V)")
    ax.set_xlim(1, 0)
    ax.set_ylim(0, 2.1)
    ax.legend(fontsize=7, loc="upper right", ncol=2)
    save(fig, f"{OUT}/standing-waves.svg")


if __name__ == "__main__":
    fig_standing()
