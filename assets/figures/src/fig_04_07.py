#!/usr/bin/env python3
"""Figures for chapter 04-07 (Faraday's law, Lenz's law and inductance).

Run from anywhere:  python assets/figures/src/fig_04_07.py
Outputs SVGs to assets/figures/04-07/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/04-07"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
MU0 = 1.25663706127e-6
RHO_CU = 1.68e-8


def dipole_flux(m, R, z):
    # flux of a point dipole on the axis of a loop of radius R at axial distance z: mu0 m R^2 / (2 (R^2+z^2)^1.5)
    return MU0 * m * R**2 / (2 * (R**2 + z**2) ** 1.5)


def fig_faraday():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    m, R, v = 1.0, 0.01, 1.0
    t = np.linspace(-0.05, 0.05, 2001)
    phi = dipole_flux(m, R, v * t)
    emf = -np.gradient(phi, t)
    ax.plot(t * 1e3, phi * 1e6, color=B, lw=2, label="flux through the loop (µWb)")
    ax2 = ax.twinx()
    ax2.plot(t * 1e3, emf * 1e3, color=O, lw=2, ls="--", label="EMF = −dΦ/dt (mV)")
    ax2.grid(False)
    ax.set_xlabel("time (ms); magnet passes the loop at t = 0")
    ax.set_ylabel("flux (µWb)", color=B)
    ax2.set_ylabel("EMF (mV)", color=O)
    ax.set_title("A magnet passing through a loop: EMF reverses as flux peaks", fontsize=10)
    ax = axes[1]
    f = np.logspace(1, 10, 300)
    d = np.sqrt(RHO_CU / (np.pi * f * MU0))
    ax.loglog(f, d * 1e3, color=G, lw=2)
    for ff, label in ((60, "60 Hz: 8.4 mm"), (1e6, "1 MHz: 65 µm"), (1e9, "1 GHz: 2.1 µm")):
        dd = math.sqrt(RHO_CU / (math.pi * ff * MU0)) * 1e3
        ax.plot(ff, dd, "o", color=O)
        ax.text(ff * 1.6, dd * 1.25, label, fontsize=8)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("skin depth in copper (mm)")
    ax.set_title("Skin depth δ = √(ρ/(πfµ)) falls as 1/√f", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/faraday-and-skin.svg")


def fig_gap():
    N, A, lc, mur, Bs = 20, 4e-5, 0.05, 2000, 0.39
    g = np.linspace(0, 1.5e-3, 300)
    Rt = lc / (mur * MU0 * A) + g / (MU0 * A)
    L = N**2 / Rt
    Isat = Bs * A * Rt / N
    U = 0.5 * L * Isat**2
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.8))
    ax = axes[0]
    ax.semilogy(g * 1e3, L * 1e6, color=B, lw=2, label="inductance (µH)")
    ax.semilogy(g * 1e3, Isat, color=O, lw=2, ls="--", label="saturation current at 100 °C (A)")
    ax.axvline(0.5, color="0.6", ls=":", lw=1)
    ax.set_xlabel("air gap (mm)")
    ax.set_title("A gap trades inductance for saturation current", fontsize=10)
    ax.legend(fontsize=8)
    ax = axes[1]
    ax.plot(g * 1e3, U * 1e3, color=G, lw=2)
    ax.plot(0.5, 0.5 * N**2 / (lc / (mur * MU0 * A) + 5e-4 / (MU0 * A)) * (Bs * A * (lc / (mur * MU0 * A) + 5e-4 / (MU0 * A)) / N) ** 2 * 1e3,
            "o", color=O)
    ax.set_xlabel("air gap (mm)")
    ax.set_ylabel("energy stored at saturation (mJ)")
    ax.set_title("…and stores far more energy, almost all of it in the gap", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/gapped-inductor.svg")


def fig_transformer():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.add_patch(Rectangle((0, 0), 6, 4, fill=False, lw=10, ec="0.55"))
    for x0, n, color, label in ((0, 6, B, "N₁ turns"), (6, 3, O, "N₂ turns")):
        ys = np.linspace(0.8, 3.2, n)
        for y in ys:
            ax.plot([x0 - 0.45, x0 + 0.45], [y, y + 0.25], color=color, lw=2.2)
        ax.text(x0 + (-1.9 if x0 == 0 else 0.7), 2.0, label, color=color, fontsize=10, va="center")
    ax.annotate("", xy=(4.0, 4.0), xytext=(2.0, 4.0), arrowprops=dict(arrowstyle="-|>", color=G, lw=2))
    ax.annotate("", xy=(2.0, 0.0), xytext=(4.0, 0.0), arrowprops=dict(arrowstyle="-|>", color=G, lw=2))
    ax.annotate("", xy=(6, 1.3), xytext=(6, 2.7), arrowprops=dict(arrowstyle="-|>", color=G, lw=2))
    ax.annotate("", xy=(0, 2.7), xytext=(0, 1.3), arrowprops=dict(arrowstyle="-|>", color=G, lw=2))
    ax.text(3, 2.0, "shared flux Φ\n\nv₁ = N₁ dΦ/dt\nv₂ = N₂ dΦ/dt\n\nv₂/v₁ = N₂/N₁", ha="center", va="center", fontsize=10)
    ax.set_xlim(-2.2, 8.2)
    ax.set_ylim(-0.6, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Ideal transformer: one flux links both windings", fontsize=10)
    save(fig, f"{OUT}/transformer.svg")


if __name__ == "__main__":
    fig_faraday()
    fig_gap()
    fig_transformer()
