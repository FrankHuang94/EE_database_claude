#!/usr/bin/env python3
"""Figures for chapter 04-03 (Gauss's law).

Run from anywhere:  python assets/figures/src/fig_04_03.py
Outputs SVGs to assets/figures/04-03/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Rectangle, Wedge

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/04-03"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
EPS0 = 8.8541878188e-12
KE = 1 / (4 * math.pi * EPS0)
E_CH = 1.602176634e-19


def arrow(ax, x, y, dx, dy, color=B):
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4, mutation_scale=12))


def fig_surfaces():
    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.7))
    # (a) sphere around a point charge
    ax = axes[0]
    ax.add_patch(Circle((0, 0), 1.0, fill=False, ls="--", lw=1.5, color="0.35"))
    ax.plot(0, 0, "o", ms=13, color=O)
    ax.text(0, 0, "+", ha="center", va="center", color="white", fontsize=12, weight="bold")
    for ang in np.arange(0, 360, 45):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        arrow(ax, 0.25 * c, 0.25 * s, 1.15 * c, 1.15 * s)
    ax.text(0, -1.75, "sphere: E radial, same |E|\neverywhere on the surface", ha="center", fontsize=9)
    ax.set_title("Spherical symmetry", fontsize=10)
    # (b) cylinder around a line charge (side view)
    ax = axes[1]
    ax.plot([-1.6, 1.6], [0, 0], color=O, lw=4)
    for xx in np.linspace(-1.4, 1.4, 8):
        ax.text(xx, 0.0, "+", ha="center", va="center", color="white", fontsize=8, weight="bold")
    ax.add_patch(Rectangle((-0.9, -0.8), 1.8, 1.6, fill=False, ls="--", lw=1.5, color="0.35"))
    ax.add_patch(Ellipse((-0.9, 0), 0.35, 1.6, fill=False, ls="--", lw=1.2, color="0.35"))
    ax.add_patch(Ellipse((0.9, 0), 0.35, 1.6, fill=False, ls="--", lw=1.2, color="0.35"))
    for xx in (-0.5, 0.0, 0.5):
        arrow(ax, xx, 0.15, 0, 1.1)
        arrow(ax, xx, -0.15, 0, -1.1)
    ax.text(0, -1.75, "cylinder: flux only through the\ncurved side, none through the ends", ha="center", fontsize=9)
    ax.set_title("Cylindrical symmetry", fontsize=10)
    # (c) pillbox through a sheet
    ax = axes[2]
    ax.plot([0, 0], [-1.4, 1.4], color=O, lw=4)
    for yy in np.linspace(-1.2, 1.2, 7):
        ax.text(0, yy, "+", ha="center", va="center", color="white", fontsize=8, weight="bold")
    ax.add_patch(Rectangle((-0.8, -0.5), 1.6, 1.0, fill=False, ls="--", lw=1.5, color="0.35"))
    ax.add_patch(Ellipse((-0.8, 0), 0.3, 1.0, fill=False, ls="--", lw=1.2, color="0.35"))
    ax.add_patch(Ellipse((0.8, 0), 0.3, 1.0, fill=False, ls="--", lw=1.2, color="0.35"))
    for yy in (-0.25, 0.25):
        arrow(ax, 0.15, yy, 1.2, 0)
        arrow(ax, -0.15, yy, -1.2, 0)
    ax.text(0, -1.75, "pillbox: flux only through the\ntwo flat faces, area A each", ha="center", fontsize=9)
    ax.set_title("Planar symmetry", fontsize=10)
    for ax in axes:
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-2.1, 1.7)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout()
    save(fig, f"{OUT}/gaussian-surfaces.svg")


def fig_sphere():
    Q, R = 1e-8, 0.05
    r = np.linspace(1e-4, 0.15, 600)
    solid = np.where(r < R, KE * Q * r / R**3, KE * Q / r**2)
    shell = np.where(r < R, 0.0, KE * Q / r**2)
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.plot(r * 100, solid / 1e3, color=B, lw=2, label="solid sphere, uniform ρ")
    ax.plot(r * 100, shell / 1e3, color=O, lw=2, ls="--", label="thin shell, same Q")
    ax.axvline(5, color="0.6", ls=":", lw=1)
    for rr in (0.02, 0.05, 0.10):
        val = KE * Q * rr / R**3 if rr < R else KE * Q / rr**2
        ax.plot(rr * 100, val / 1e3, "o", color=B, ms=5)
    ax.text(5.2, 37, "surface, R = 5 cm", fontsize=9, color="0.3")
    ax.set_xlabel("distance from center r (cm)")
    ax.set_ylabel("E (kV/m)")
    ax.set_title("Q = 10 nC: linear inside a solid sphere, zero inside a shell, kQ/r² outside", fontsize=10)
    ax.legend(fontsize=9)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 40)
    fig.tight_layout()
    save(fig, f"{OUT}/sphere-field.svg")


def fig_shell():
    q, a, b = 2e-9, 0.03, 0.04
    fig = plt.figure(figsize=(10.4, 3.9))
    ax = fig.add_axes([0.0, 0.04, 0.36, 0.92])
    ax.add_patch(Wedge((0, 0), b, 0, 360, width=b - a, color="0.8"))
    ax.plot(0, 0, "o", ms=12, color=O)
    ax.text(0, 0, "+", ha="center", va="center", color="white", fontsize=11, weight="bold")
    for ang in np.arange(0, 360, 30):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        ax.text(0.0275 * c, 0.0275 * s, "−", ha="center", va="center", fontsize=9, color=B, weight="bold")
        ax.text(0.0435 * c, 0.0435 * s, "+", ha="center", va="center", fontsize=9, color=O, weight="bold")
        arrow(ax, 0.004 * c, 0.004 * s, 0.020 * c, 0.020 * s, color=G)
        arrow(ax, 0.047 * c, 0.047 * s, 0.012 * c, 0.012 * s, color=G)
    ax.text(0, -0.066, "metal: E = 0; −2 nC on the inner wall,\n+2 nC on the outer surface", ha="center", fontsize=9)
    ax.set_xlim(-0.065, 0.065)
    ax.set_ylim(-0.075, 0.062)
    ax.set_aspect("equal")
    ax.axis("off")
    ax2 = fig.add_axes([0.46, 0.17, 0.52, 0.74])
    r = np.linspace(0.008, 0.10, 800)
    Ein = np.where(r < a, KE * q / r**2, np.where(r < b, 0.0, KE * q / r**2))
    Egnd = np.where(r < a, KE * q / r**2, 0.0)
    ax2.axvspan(a * 100, b * 100, color="0.85", label="metal")
    ax2.plot(r * 100, Ein / 1e3, color=B, lw=2, label="isolated shell")
    ax2.plot(r * 100, Egnd / 1e3, color=O, lw=2, ls="--", label="grounded shell")
    ax2.set_yscale("log")
    ax2.set_ylim(0.5, 400)
    ax2.set_xlabel("distance from the charge r (cm)")
    ax2.set_ylabel("E (kV/m)")
    ax2.set_title("+2 nC inside a conducting shell (Example 04-03.5)", fontsize=10)
    ax2.legend(fontsize=9)
    save(fig, f"{OUT}/conducting-shell.svg")


def fig_depletion():
    es = 11.7 * EPS0
    NA, ND, xn = 1e23, 1e22, 0.3e-6
    xp = ND * xn / NA
    x = np.linspace(-0.12e-6, 0.42e-6, 2000)
    rho = np.where((x > -xp) & (x < 0), -E_CH * NA, np.where((x >= 0) & (x < xn), E_CH * ND, 0.0))
    Ex = np.where((x > -xp) & (x < 0), -E_CH * NA * (x + xp) / es,
                  np.where((x >= 0) & (x < xn), -E_CH * ND * (xn - x) / es, 0.0))
    fig, axes = plt.subplots(2, 1, figsize=(6.8, 5.2), sharex=True)
    ax = axes[0]
    ax.fill_between(x * 1e6, rho / 1e6, step=None, color=B, alpha=0.35)
    ax.plot(x * 1e6, rho / 1e6, color=B, lw=1.5)
    ax.axhline(0, color="0.4", lw=0.8)
    ax.set_ylabel("ρ (C/cm³)")
    ax.set_title(r"Abrupt pn junction: $N_A = 10^{17}$ cm$^{-3}$, $N_D = 10^{16}$ cm$^{-3}$", fontsize=10)
    ax.text(0.01, -0.0125, r"← p side: $-qN_A$ over $x_p$ = 0.03 µm", fontsize=8)
    ax.text(0.08, -0.006, r"n side: $+qN_D$ over $x_n$ = 0.3 µm", fontsize=8)
    ax = axes[1]
    ax.plot(x * 1e6, Ex / 1e5, color=O, lw=2)
    ax.axhline(0, color="0.4", lw=0.8)
    ax.set_xlabel("position x (µm); metallurgical junction at x = 0")
    ax.set_ylabel("E (kV/cm)")
    ax.text(0.02, -44, "peak 46.4 kV/cm at the junction,\npointing from n to p (−x)", fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/depletion-field.svg")


if __name__ == "__main__":
    fig_surfaces()
    fig_sphere()
    fig_shell()
    fig_depletion()
