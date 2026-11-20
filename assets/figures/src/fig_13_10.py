#!/usr/bin/env python3
"""Figures for chapter 13-10 (waveguides and resonators).

Run from anywhere:  python assets/figures/src/fig_13_10.py
Outputs SVGs to assets/figures/13-10/:
- dispersion.svg: frequency against phase constant for the first modes of air-filled WR-90 (22.86 x 10.16 mm),
  with the light line and the recommended band shaded.
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

OUT = "assets/figures/13-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
C0 = 299792458.0
A, B = 0.02286, 0.01016


def fig_dispersion():
    f = np.linspace(0, 20e9, 2000)
    k = 2 * math.pi * f / C0
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.axhspan(8.2, 12.4, color=PALETTE[4], alpha=0.15, lw=0)
    ax.text(10, 10.1, "recommended band\n8.2–12.4 GHz", fontsize=7)
    ax.plot(k, f / 1e9, "k--", lw=1, label="light line (free space)")
    for i, (m, n, name) in enumerate(((1, 0, "TE10"), (2, 0, "TE20"), (0, 1, "TE01"), (1, 1, "TE11/TM11"))):
        kc = math.sqrt((m * math.pi / A) ** 2 + (n * math.pi / B) ** 2)
        mask = k > kc
        ax.plot(np.sqrt(k[mask] ** 2 - kc**2), f[mask] / 1e9, color=PALETTE[i], lw=1.7,
                label=f"{name}, cutoff {kc * C0 / (2 * math.pi) / 1e9:.2f} GHz")
    ax.set_xlabel("phase constant β (rad/m)")
    ax.set_ylabel("frequency (GHz)")
    ax.set_xlim(0, 420)
    ax.set_ylim(0, 20)
    ax.legend(fontsize=7, loc="lower right")
    save(fig, f"{OUT}/dispersion.svg")


if __name__ == "__main__":
    fig_dispersion()
