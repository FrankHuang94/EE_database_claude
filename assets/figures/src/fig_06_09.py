#!/usr/bin/env python3
"""Figures for chapter 06-09 (maximum power transfer).

Run from anywhere:  python assets/figures/src/fig_06_09.py
Outputs SVGs to assets/figures/06-09/. Both figures are matplotlib plots.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/06-09"
use_style()
B, O, G = PALETTE[0], PALETTE[1], PALETTE[2]


def fig_power_efficiency():
    """Load power (normalized to the maximum) and efficiency against R_L/R_th."""
    r = np.logspace(-2, 2, 400)
    p = 4 * r / (1 + r) ** 2
    eta = r / (1 + r)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.semilogx(r, p, color=B, label="load power / maximum")
    ax.semilogx(r, eta, color=O, ls="--", label="efficiency")
    ax.axvline(1, color="0.5", lw=0.8)
    ax.annotate("matched: 100% of max power,\n50% efficiency", (1, 1.0), xytext=(0.03, 0.75), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("power delivery lives here:\n95% efficient, 19% of max power", (19, 0.19), xytext=(1.6, 0.35),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.set_xlabel("load resistance / source resistance, $R_L/R_{th}$")
    ax.set_ylabel("fraction")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="center left", fontsize=8)
    save(fig, f"{OUT}/power-and-efficiency.svg")


def fig_coax():
    """Normalized conductor loss and peak-power capacity of air coax against Z0 (fixed outer diameter)."""
    z0 = np.linspace(10, 140, 600)
    x = np.exp(z0 / 60.0)                        # b/a for air dielectric
    loss = (1 + x) / np.log(x)
    power = np.log(x) / x ** 2
    loss_n = loss / loss.min()
    power_n = power / power.max()
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(z0, loss_n, color=B, label="conductor loss (relative to minimum)")
    ax.plot(z0, power_n, color=O, ls="--", label="peak power capacity (relative to maximum)")
    for z, lab, y, ha in ((30.0, "30 Ω\nmax power", 1.9, "left"), (76.7, "77 Ω\nmin loss", 1.9, "left"),
                          (50.0, "50 Ω", 1.9, "left"), (75.0, "75 Ω", 1.55, "right")):
        ax.axvline(z, color="0.6", lw=0.7, ls=":")
        ax.text(z + 1 if ha == "left" else z - 1, y, lab, fontsize=8, ha=ha)
    ax.set_xlim(10, 140)
    ax.set_ylim(0, 2.2)
    ax.set_xlabel("characteristic impedance $Z_0$ (Ω), air dielectric")
    ax.set_ylabel("relative value")
    ax.legend(loc="lower right", fontsize=8)
    save(fig, f"{OUT}/coax-optima.svg")


if __name__ == "__main__":
    fig_power_efficiency()
    fig_coax()
    print("06-09 figures written to", OUT)
