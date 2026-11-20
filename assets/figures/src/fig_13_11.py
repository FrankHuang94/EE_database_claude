#!/usr/bin/env python3
"""Figures for chapter 13-11 (radiation and antenna fundamentals).

Run from anywhere:  python assets/figures/src/fig_13_11.py
Outputs SVGs to assets/figures/13-11/:
- patterns.svg: elevation power patterns of a Hertzian dipole (sin^2) and a half-wave dipole (polar, linear scale),
  beside the array factor of 8 isotropic elements at lambda/2, at broadside and steered to 30 degrees (dB).
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

OUT = "assets/figures/13-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_patterns():
    fig = plt.figure(figsize=(8.0, 3.5))
    ax1 = fig.add_subplot(1, 2, 1, projection="polar")
    th = np.linspace(1e-4, 2 * np.pi - 1e-4, 1440)
    hz = np.sin(th) ** 2
    hw = (np.cos(np.pi / 2 * np.cos(th)) / np.sin(th)) ** 2
    ax1.plot(th, hz, color=PALETTE[0], lw=1.6, label="Hertzian (HPBW 90°)")
    ax1.plot(th, hw / hw.max(), color=PALETTE[1], lw=1.6, label="half-wave (HPBW 78°)")
    ax1.set_theta_zero_location("N")
    ax1.set_yticklabels([])
    ax1.set_title("dipole power patterns (axis vertical)", fontsize=9, pad=18)
    ax1.legend(fontsize=7, loc="lower center", bbox_to_anchor=(0.5, -0.32))
    ax2 = fig.add_subplot(1, 2, 2)
    t = np.linspace(-np.pi / 2, np.pi / 2, 3001)
    n = np.arange(8)
    for i, th0 in enumerate((0, 30)):
        beta = -np.pi * np.sin(np.radians(th0))
        af = np.abs(np.exp(1j * n[None, :] * (np.pi * np.sin(t)[:, None] + beta)).sum(axis=1) / 8) ** 2
        ax2.plot(np.degrees(t), 10 * np.log10(af + 1e-12), color=PALETTE[2 + i], lw=1.5,
                 label=f"8 elements, λ/2, steered {th0}°")
    ax2.set_ylim(-35, 2)
    ax2.set_xlabel("angle from broadside (°)")
    ax2.set_ylabel("array factor |AF|² (dB)")
    ax2.legend(fontsize=7, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/patterns.svg")


if __name__ == "__main__":
    fig_patterns()
