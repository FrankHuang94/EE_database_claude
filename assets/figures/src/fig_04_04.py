#!/usr/bin/env python3
"""Figures for chapter 04-04 (electric potential, capacitance and dielectrics).

Run from anywhere:  python assets/figures/src/fig_04_04.py
Outputs SVGs to assets/figures/04-04/.
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

OUT = "assets/figures/04-04"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
EPS0 = 8.8541878188e-12
KE = 1 / (4 * math.pi * EPS0)


def fig_equipotentials():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
    ax = axes[0]
    x = np.linspace(-3, 3, 500)
    X, Y = np.meshgrid(x, x)
    V = np.zeros_like(X)
    Ex, Ey = np.zeros_like(X), np.zeros_like(X)
    for q, x0 in ((1.0, -1.0), (-1.0, 1.0)):
        dx, dy = X - x0, Y
        r = np.hypot(dx, dy) + 1e-9
        V += q / r
        Ex += q * dx / r**3
        Ey += q * dy / r**3
    levels = [-2, -1, -0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5, 1, 2]
    cs = ax.contour(X, Y, V, levels=levels, colors=[B], linewidths=1.0, linestyles="solid")
    ax.clabel(cs, fontsize=7, fmt="%g")
    ax.streamplot(X, Y, Ex, Ey, color="0.6", density=0.9, linewidth=0.7, arrowsize=0.8)
    for q, x0 in ((1, -1), (-1, 1)):
        ax.plot(x0, 0, "o", ms=12, color=O if q > 0 else B)
        ax.text(x0, 0, "+" if q > 0 else "−", ha="center", va="center", color="white", fontsize=11, weight="bold")
    ax.set_aspect("equal")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_title("Dipole: equipotentials (blue, labels in units of 2k·q/d)\ncross the field lines (gray) at right angles", fontsize=9)
    ax.set_xlabel("x (units of d/2)")
    ax.set_ylabel("y")
    ax = axes[1]
    R, Vs = 0.05, 1000.0
    r = np.linspace(0.001, 0.2, 800)
    Vr = np.where(r < R, Vs, Vs * R / r)
    Er = np.where(r < R, 0.0, Vs * R / r**2)
    ax.plot(r * 100, Vr, color=B, lw=2, label="potential V (V)")
    ax.set_xlabel("distance from center r (cm)")
    ax.set_ylabel("V (V)", color=B)
    ax2 = ax.twinx()
    ax2.plot(r * 100, Er / 1e3, color=O, lw=2, ls="--", label="field E (kV/m)")
    ax2.set_ylabel("E (kV/m)", color=O)
    ax2.grid(False)
    ax.axvspan(0, 5, color="0.9")
    ax.text(0.4, 300, "metal:\nV constant,\nE = 0", fontsize=9)
    ax.set_title("Conducting sphere, R = 5 cm, at 1 kV: V = V₀R/r and E = V₀R/r² outside", fontsize=9)
    ax.set_ylim(0, 1100)
    ax2.set_ylim(0, 22)
    fig.tight_layout()
    save(fig, f"{OUT}/equipotentials.svg")


def fig_dielectric():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9), gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axes[0]
    ax.add_patch(Rectangle((0, 0), 0.25, 4, color=O))
    ax.add_patch(Rectangle((3.75, 0), 0.25, 4, color=B))
    ax.add_patch(Rectangle((1.0, 0), 2.0, 4, color="#E8E0F0"))
    for yy in np.linspace(0.35, 3.65, 7):
        ax.text(0.125, yy, "+", ha="center", va="center", color="white", fontsize=10, weight="bold")
        ax.text(3.875, yy, "−", ha="center", va="center", color="white", fontsize=10, weight="bold")
        ax.text(1.12, yy, "−", ha="center", va="center", color=B, fontsize=9, weight="bold")
        ax.text(2.88, yy, "+", ha="center", va="center", color=O, fontsize=9, weight="bold")
    for yy in (0.8, 2.0, 3.2):
        ax.annotate("", xy=(0.95, yy), xytext=(0.3, yy), arrowprops=dict(arrowstyle="-|>", color=G, lw=2.2))
        ax.annotate("", xy=(3.7, yy), xytext=(3.05, yy), arrowprops=dict(arrowstyle="-|>", color=G, lw=2.2))
        ax.annotate("", xy=(2.7, yy), xytext=(1.3, yy), arrowprops=dict(arrowstyle="-|>", color=G, lw=0.9))
    for yy in (1.4, 2.6):
        ax.add_patch(plt.matplotlib.patches.Ellipse((2.0, yy), 0.5, 0.22, color="0.55"))
        ax.text(1.87, yy, "−", ha="center", va="center", fontsize=7, color="white")
        ax.text(2.13, yy, "+", ha="center", va="center", fontsize=7, color="white")
    ax.text(2.0, -0.45, "dielectric: aligned dipoles leave bound charge\nat its faces, weakening E inside by ε_r", ha="center", fontsize=8.5)
    ax.text(0.12, 4.25, "+σ_f", ha="center", fontsize=9)
    ax.text(3.88, 4.25, "−σ_f", ha="center", fontsize=9)
    ax.set_xlim(-0.3, 4.3)
    ax.set_ylim(-1.0, 4.6)
    ax.axis("off")
    ax.set_title("Free charge on the plates, bound charge on the dielectric", fontsize=10)
    ax = axes[1]
    mats = ["air gap", "SiOCH low-k\n(2.7–2.9)", "SiO₂", "Al₂O₃", "HfO₂ / ZrO₂", "Si", "class 2\nBaTiO₃ MLCC"]
    k = [1.0, 2.8, 3.9, 9.0, 25.0, 11.7, 2500.0]
    lo = [1.0, 2.7, 3.9, 9.0, 25.0, 11.7, 1000.0]
    hi = [1.0, 2.9, 3.9, 9.0, 25.0, 11.7, 4000.0]
    order = np.argsort(k)
    ys = np.arange(len(k))
    for yy, i in zip(ys, order):
        ax.plot([lo[i], hi[i]], [yy, yy], color=B, lw=6, solid_capstyle="round")
        ax.plot(k[i], yy, "o", color=O if i in (0, 1) else B, ms=6)
    ax.set_yticks(ys)
    ax.set_yticklabels([mats[i] for i in order], fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xlim(0.8, 6000)
    ax.set_xlabel("relative permittivity ε_r (log scale)")
    ax.set_title("Low-k for wiring, high-k for gates and DRAM, ferroelectrics for MLCCs", fontsize=9.5)
    fig.tight_layout()
    save(fig, f"{OUT}/dielectrics.svg")


def fig_coax():
    b, Ebd = 2e-3, 3e6
    ratio = np.linspace(0.02, 0.98, 500)
    Vmax = Ebd * ratio * b * np.log(1 / ratio)
    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    ax.plot(ratio, Vmax, color=B, lw=2)
    ax.axvline(1 / math.e, color=O, ls="--", lw=1.2)
    ax.plot(1 / math.e, Ebd * b / math.e, "o", color=O)
    ax.plot(0.25, Ebd * 0.25 * b * math.log(4), "s", color=G)
    ax.text(1 / math.e + 0.02, 2250, "a/b = 1/e: 2207 V", fontsize=9, color=O)
    ax.text(0.27, 1900, "a/b = 1/4\n(Example 04-04.5): 2079 V", fontsize=8.5, color=G)
    ax.set_xlabel("inner radius / outer radius, a/b")
    ax.set_ylabel("voltage before breakdown (V)")
    ax.set_title("Air coax with b = 2 mm: too thin concentrates the field, too thick shrinks the gap", fontsize=9.5)
    ax.set_ylim(0, 2500)
    fig.tight_layout()
    save(fig, f"{OUT}/coax-optimum.svg")


def fig_charge_sharing():
    C1 = C2 = 1e-6
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.6))
    for R, ls in ((10.0, "-"), (1000.0, "--")):
        tau = R * C1 * C2 / (C1 + C2)
        t = np.linspace(0, 2.5e-3, 5001)
        v1 = 5 + 5 * np.exp(-t / tau)
        v2 = 5 - 5 * np.exp(-t / tau)
        i = 10 / R * np.exp(-t / tau)
        Eloss = (10**2 / R) * (tau / 2) * (1 - np.exp(-2 * t / tau))     # integral of i^2 R, closed form
        axes[0].plot(t * 1e3, v1, color=O, ls=ls, label=f"C1, R = {R:g} Ω")
        axes[0].plot(t * 1e3, v2, color=B, ls=ls, label=f"C2, R = {R:g} Ω")
        axes[1].plot(t * 1e3, Eloss * 1e6, color=G, ls=ls, label=f"R = {R:g} Ω")
    axes[0].set_xlabel("time (ms)")
    axes[0].set_ylabel("capacitor voltage (V)")
    axes[0].set_title("1 µF at 10 V shares charge with 1 µF at 0 V", fontsize=10)
    axes[0].legend(fontsize=8, ncol=2)
    axes[1].axhline(25, color="0.5", ls=":", lw=1)
    axes[1].set_xlabel("time (ms)")
    axes[1].set_ylabel("energy dissipated in R (µJ)")
    axes[1].set_title("Half the energy is lost, 25 µJ, whatever R is", fontsize=10)
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/charge-sharing.svg")


if __name__ == "__main__":
    fig_equipotentials()
    fig_dielectric()
    fig_coax()
    fig_charge_sharing()
