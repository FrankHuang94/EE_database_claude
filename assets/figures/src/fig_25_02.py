#!/usr/bin/env python3
"""Figures for chapter 25-02 (lithography).

Run from anywhere:  python assets/figures/src/fig_25_02.py
Outputs
  assets/figures/25-02/pupil-orders.svg       diffraction orders of an 80 nm pitch (ArF, NA 1.35) in pupil coordinates,
                                              on-axis (first orders outside) and dipole at s0 = 0.9 NA (orders 0 and -1 inside)
  assets/figures/25-02/contrast-vs-pitch.svg  aerial-image contrast against pitch, on-axis and ideal dipole (ArF immersion)
  assets/figures/25-02/shot-noise.svg         relative fluctuation of absorbed photons against dose, 10 and 16 nm squares,
                                              13.5 nm and 193 nm, 20% absorption
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import litho as L  # noqa: E402

OUT = "assets/figures/25-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def pupil_orders() -> None:
    lam, na, p = 193.0, 1.35, 80.0
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.4))
    for ax, s0, title in ((axes[0], 0.0, "on-axis illumination"), (axes[1], 0.9 * na, "dipole at 0.9 NA")):
        ax.add_patch(Circle((0, 0), na, fill=False, color=PALETTE[0], lw=1.5))
        for m in (-2, -1, 0, 1, 2):
            s = s0 + m * lam / p
            inside = abs(s) <= na
            ax.plot(s, 0, "o", color=PALETTE[2] if inside else PALETTE[1], ms=8)
            if abs(s) < 4.5:
                ax.annotate(f"m={m}", (s, 0), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=7)
        ax.set_xlim(-4.6, 4.6)
        ax.set_ylim(-1.8, 1.8)
        ax.set_aspect("equal")
        ax.axhline(0, color="0.8", lw=0.5)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("pupil coordinate s = n sin θ")
        ax.text(0, -1.6, "pupil |s| ≤ NA = 1.35", ha="center", fontsize=7, color=PALETTE[0])
        ax.set_yticks([])
    save(fig, f"{OUT}/pupil-orders.svg")


def contrast_vs_pitch() -> None:
    pa = np.linspace(60, 200, 561)
    on = [L.image_contrast(p, 193, 1.35, 1.44) for p in pa]
    dip = [L.image_contrast(p, 193, 1.35, 1.44, poles=L.dipole_for(p, 193)) if 193 / (2 * p) <= 1.35 else 0.0 for p in pa]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(pa, on, color=PALETTE[1], label="on-axis")
    ax.plot(pa, dip, color=PALETTE[0], label="ideal dipole")
    for x, lab in ((193 / 1.35, "λ/NA"), (193 / 2.7, "λ/2NA")):
        ax.axvline(x, color="0.6", ls=":")
        ax.text(x + 1.5, 0.08, lab, fontsize=7)
    ax.set_xlabel("pitch (nm)")
    ax.set_ylabel("image contrast")
    ax.set_ylim(-0.02, 1.08)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/contrast-vs-pitch.svg")


def shot_noise() -> None:
    d = np.logspace(0.5, 2.5, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for lam, ls in ((13.5, "-"), (193, "--")):
        for side, col in ((10, PALETTE[0]), (16, PALETTE[2])):
            n = L.photons_per_nm2(1.0, lam) * d * side**2 * 0.2
            ax.loglog(d, 100 / np.sqrt(n), ls=ls, color=col, label=f"{lam:g} nm, {side} nm square")
    ax.set_xlabel("dose (mJ/cm²)")
    ax.set_ylabel("relative fluctuation (%)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7)
    save(fig, f"{OUT}/shot-noise.svg")


if __name__ == "__main__":
    pupil_orders()
    contrast_vs_pitch()
    shot_noise()
