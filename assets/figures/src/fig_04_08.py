#!/usr/bin/env python3
"""Figures for chapter 04-08 (energy in fields and Maxwell's equations, preview).

Run from anywhere:  python assets/figures/src/fig_04_08.py
Outputs SVGs to assets/figures/04-08/.
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

OUT = "assets/figures/04-08"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
MU0 = 1.25663706127e-6
C = 299792458.0


def fig_displacement():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    ax.plot([-3, -0.25], [0, 0], color="0.2", lw=2)
    ax.plot([0.25, 3], [0, 0], color="0.2", lw=2)
    ax.add_patch(Rectangle((-0.25, -1.2), 0.12, 2.4, color=O))
    ax.add_patch(Rectangle((0.13, -1.2), 0.12, 2.4, color=B))
    for y in np.linspace(-1.0, 1.0, 5):
        ax.annotate("", xy=(0.12, y), xytext=(-0.12, y), arrowprops=dict(arrowstyle="-|>", color=G, lw=1.2))
    ax.annotate("", xy=(-1.4, 0.18), xytext=(-2.6, 0.18), arrowprops=dict(arrowstyle="-|>", color="0.2", lw=1.5))
    ax.text(-2.6, 0.35, "conduction current i", fontsize=8.5)
    ax.text(0.45, 1.25, "growing E:\ndisplacement current\nε₀ dΦ_E/dt = i", fontsize=8.5, color=G)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(-1.8 + 0.18 * np.cos(th), 0.9 * np.sin(th), color=P, lw=1.2, ls="--")
    ax.text(-2.95, -1.85, "dashed loop: same ∮B·dl whether its surface\ncuts the wire or passes through the gap", fontsize=7.5, color=P)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2.1, 2.1)
    ax.axis("off")
    ax.set_title("A charging capacitor: Ampère's law needs the displacement current", fontsize=9.5)
    ax = axes[1]
    R, I = 0.05, 1.0
    r = np.linspace(0, 0.15, 500)
    Bf = np.where(r < R, MU0 * I * r / (2 * np.pi * R**2), MU0 * I / (2 * np.pi * np.maximum(r, 1e-9)))
    ax.plot(r * 100, Bf * 1e6, color=G, lw=2)
    ax.axvspan(0, 5, color="0.92")
    ax.text(0.5, 0.5, "between the\nplates", fontsize=8)
    for rr in (0.03, 0.05, 0.10):
        val = MU0 * I * rr / (2 * np.pi * R**2) if rr < R else MU0 * I / (2 * np.pi * rr)
        ax.plot(rr * 100, val * 1e6, "o", color=O)
    ax.set_xlabel("distance from the axis r (cm)")
    ax.set_ylabel("B (µT)")
    ax.set_title("1 A charging 5 cm-radius plates: B circles the gap like a wire", fontsize=9.5)
    fig.tight_layout()
    save(fig, f"{OUT}/displacement-current.svg")


def fig_wave():
    fig = plt.figure(figsize=(7.0, 3.8))
    ax = fig.add_subplot(projection="3d")
    x = np.linspace(0, 2, 400)
    E = np.cos(2 * np.pi * x)
    ax.plot(x, np.zeros_like(x), E, color=B, lw=2, label="E (vertical)")
    ax.plot(x, -E, np.zeros_like(x), color=O, lw=2, label="B (horizontal), |B| = |E|/c")
    for xi in np.linspace(0, 2, 21):
        ei = math.cos(2 * math.pi * xi)
        ax.plot([xi, xi], [0, 0], [0, ei], color=B, lw=0.6, alpha=0.6)
        ax.plot([xi, xi], [0, -ei], [0, 0], color=O, lw=0.6, alpha=0.6)
    ax.plot([0, 2.3], [0, 0], [0, 0], color="0.3", lw=1)
    ax.text(2.35, 0, 0, "propagation,\nS = E × B / µ₀", fontsize=8)
    ax.set_xlabel("x (wavelengths)")
    ax.set_yticks([])
    ax.set_zticks([])
    ax.view_init(elev=18, azim=-60)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("A plane electromagnetic wave: E, B and the direction of travel are mutually perpendicular", fontsize=9)
    save(fig, f"{OUT}/plane-wave.svg")


def fig_poynting_and_loss():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.8))
    ax = axes[0]
    ax.add_patch(Rectangle((0, -0.25), 6, 0.5, color="#D58A3A"))
    for x in np.linspace(0.6, 5.4, 5):
        ax.annotate("", xy=(x + 0.5, 0), xytext=(x - 0.1, 0), arrowprops=dict(arrowstyle="-|>", color="white", lw=1.2))
        for s in (1, -1):
            ax.annotate("", xy=(x, s * 0.3), xytext=(x, s * 1.3), arrowprops=dict(arrowstyle="-|>", color=G, lw=1.6))
    ax.text(0.1, 1.45, "Poynting vector S points into the wire", color=G, fontsize=9)
    ax.text(0.1, -1.85, "E along the wire (white), B circling it: S = E × B / µ₀;\nthe total flux into the surface equals I²R", fontsize=8.5)
    ax.text(6.15, 0.0, "I →", fontsize=10, va="center")
    ax.set_xlim(-0.3, 7)
    ax.set_ylim(-2.2, 1.8)
    ax.axis("off")
    ax.set_title("Energy reaches a resistor through the space around it", fontsize=10)
    ax = axes[1]
    fh = np.array([0.1, 1, 2, 5, 10])
    dk_h = np.array([4.24, 4.17, 4.04, 3.92, 3.92])
    df_h = np.array([0.0150, 0.0161, 0.0210, 0.0250, 0.0250])
    fr = np.array([2.5, 10])
    df_r = np.array([0.0031, 0.0037])
    alpha = lambda f, dk, df: 20 / math.log(10) * math.pi * f * 1e9 * np.sqrt(dk) * df / C
    ax.loglog(fh, alpha(fh, dk_h, df_h), "o-", color=O, label="FR-4 class (Isola 370HR)")
    ax.loglog(fr, alpha(fr, 3.66, df_r), "s-", color=B, label="low-loss (Rogers RO4350B, Dk 3.66)")
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("dielectric loss (dB per meter)")
    ax.set_title("Dielectric loss grows with frequency × loss tangent", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/poynting-and-loss.svg")


if __name__ == "__main__":
    fig_displacement()
    fig_wave()
    fig_poynting_and_loss()
