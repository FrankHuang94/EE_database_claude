#!/usr/bin/env python3
"""Figures for chapter 04-09 (waves and optics basics).

Run from anywhere:  python assets/figures/src/fig_04_09.py
Outputs SVGs to assets/figures/04-09/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.special import j1

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/04-09"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_interference():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.8))
    ax = axes[0]
    lam, d, a, L = 633e-9, 0.2e-3, 0.04e-3, 1.0
    y = np.linspace(-0.012, 0.012, 4000)
    th = y / L
    beta = np.pi * a * np.sin(th) / lam
    env = np.sinc(beta / np.pi) ** 2
    I = np.cos(np.pi * d * np.sin(th) / lam) ** 2 * env
    ax.plot(y * 1e3, I, color=B, lw=1.2, label="two slits, 0.2 mm apart")
    ax.plot(y * 1e3, env, color=O, ls="--", lw=1.2, label="single-slit envelope (0.04 mm wide)")
    ax.set_xlabel("position on a screen 1 m away (mm)")
    ax.set_ylabel("relative intensity")
    ax.set_title("Young's fringes: spacing λL/d = 3.165 mm at 633 nm", fontsize=10)
    ax.legend(fontsize=8, loc="upper right")
    ax = axes[1]
    x = np.linspace(0, 1, 400)
    for t, alpha in zip(np.linspace(0, 0.5, 6), np.linspace(1, 0.25, 6)):
        ax.plot(x, np.sin(3 * np.pi * x) * np.cos(2 * np.pi * t), color=G, alpha=alpha, lw=1.5)
    for xn in (0, 1 / 3, 2 / 3, 1):
        ax.plot(xn, 0, "o", color=O, ms=6)
    ax.text(0.34, -1.25, "nodes (never move)", color=O, fontsize=8)
    ax.set_ylim(-1.4, 1.2)
    ax.set_xlabel("position along the string, x / L")
    ax.set_ylabel("displacement")
    ax.set_title("Third standing-wave mode: λ = 2L/3, snapshots over half a period", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/interference-and-standing-waves.svg")


def fig_diffraction():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    u = np.linspace(-10, 10, 3000)
    slit = np.sinc(u / np.pi) ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        airy = np.where(np.abs(u) < 1e-9, 1.0, (2 * j1(u) / u) ** 2)
    ax.plot(u / np.pi, slit, color=B, lw=1.5, label="slit: first zero at sin θ = λ/a")
    ax.plot(u / np.pi, airy, color=O, lw=1.5, ls="--", label="circular aperture (Airy): 1.22 λ/D")
    ax.set_xlabel("sin θ in units of λ/(aperture width)")
    ax.set_ylabel("relative intensity")
    ax.set_title("Diffraction spreads light by about λ / aperture", fontsize=10)
    ax.legend(fontsize=8)
    ax = axes[1]
    NA = np.linspace(0.2, 1.4, 300)
    for lam, color, name in ((193, B, "193 nm (ArF DUV)"), (13.5, O, "13.5 nm (EUV)")):
        ax.semilogy(NA, 0.25 * lam / NA, color=color, lw=2, label=f"{name}, k₁ = 0.25 limit")
        ax.semilogy(NA, 0.32 * lam / NA, color=color, lw=1, ls=":")
    ax.plot([0.33, 0.55], [13, 8], "s", color=G, ms=7, label="ASML EUV: 13 nm at NA 0.33, 8 nm at 0.55")
    ax.set_xlabel("numerical aperture NA")
    ax.set_ylabel("critical dimension CD (nm)")
    ax.set_title("Rayleigh: CD = k₁λ/NA (dotted: k₁ = 0.32)", fontsize=10)
    ax.legend(fontsize=7.5, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/diffraction-and-lithography.svg")


def fig_fiber():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.6))
    ax = axes[0]
    ax.axhline(0, color="0.3", lw=1)
    ax.add_patch(Rectangle((-2, -2), 4, 2, color="#DDEBF6"))
    ax.text(-1.9, -1.85, "glass, n = 1.5", fontsize=8)
    ax.text(-1.9, 1.75, "air, n = 1", fontsize=8)
    for th1, color in ((20, B), (40, G)):
        t1 = math.radians(th1)
        t2 = math.asin(math.sin(t1) / 1.5)
        ax.plot([-2 * math.sin(t1), 0], [2 * math.cos(t1), 0], color=color, lw=1.8)
        ax.plot([0, 2 * math.sin(t2)], [0, -2 * math.cos(t2)], color=color, lw=1.8)
        ax.plot([0, 2 * math.sin(t1)], [0, 2 * math.cos(t1)], color=color, lw=0.8, ls=":")
    ax.plot([0, 0], [-2, 2], color="0.6", ls="--", lw=0.8)
    ax.text(-1.95, -0.6, "Snell: n₁ sin θ₁ = n₂ sin θ₂\n(dotted: weak reflection)", fontsize=8)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Refraction bends light toward the normal in glass", fontsize=10)
    ax = axes[1]
    ax.add_patch(Rectangle((0, -1.0), 10, 2.0, color="#E8E0F0"))
    ax.add_patch(Rectangle((0, -0.4), 10, 0.8, color="#C9DDF0"))
    ax.text(9.6, 0.7, "cladding n₂", fontsize=8, ha="right")
    ax.text(9.6, -0.15, "core n₁ > n₂", fontsize=8, ha="right")
    xs = [0]
    ys = [0]
    x, yv, slope = 0.0, 0.0, 0.25
    while x < 10:
        x_next = x + (0.4 * np.sign(slope) - yv) / slope
        x_next = min(x_next, 10)
        xs.append(x_next)
        ys.append(yv + slope * (x_next - x))
        x, yv, slope = x_next, ys[-1], -slope
    ax.plot(xs, ys, color=O, lw=1.6)
    ax.plot([-1.5, 0], [-0.27, 0], color=O, lw=1.6)
    ax.plot([-1.5, 0], [0.27, 0], color="0.5", lw=0.8, ls="--")
    ax.text(-1.4, 0.45, "acceptance\ncone: NA", fontsize=7.5)
    ax.set_xlim(-1.8, 10.2)
    ax.set_ylim(-1.3, 1.3)
    ax.axis("off")
    ax.set_title("Optical fiber: total internal reflection traps light in the core", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/refraction-and-fiber.svg")


if __name__ == "__main__":
    fig_interference()
    fig_diffraction()
    fig_fiber()
