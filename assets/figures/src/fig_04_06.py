#!/usr/bin/env python3
"""Figures for chapter 04-06 (magnetic fields and forces).

Run from anywhere:  python assets/figures/src/fig_04_06.py
Outputs SVGs to assets/figures/04-06/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/04-06"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
E_CH = 1.602176634e-19
U = 1.66053906892e-27
MU0 = 1.25663706127e-6


def fig_analyzer():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.0))
    ax = axes[0]
    V, Bf = 1e4, 0.5
    for m_u, color, name in ((10, G, "¹⁰B⁺"), (11, B, "¹¹B⁺"), (49, O, "BF₂⁺ (49 u)")):
        m = m_u * U
        r = math.sqrt(2 * m * V / E_CH) / Bf
        th = np.linspace(0, math.pi, 200)
        ax.plot(r * (1 - np.cos(th)) * 100, r * np.sin(th) * 100, color=color, lw=2, label=f"{name}: r = {r*100:.2f} cm")
    ax.annotate("", xy=(0, -1.5), xytext=(0, -5), arrowprops=dict(arrowstyle="-|>", color="0.3", lw=1.5))
    ax.text(0.6, -4.5, "ions enter at 10 keV", fontsize=8, color="0.3")
    ax.text(31, 6, "B = 0.5 T\n(out of page)", fontsize=9, ha="center")
    for xx in np.arange(4, 42, 6):
        for yy in np.arange(2, 22, 6):
            ax.plot(xx, yy, ".", color="0.75", ms=3)
    ax.set_xlim(-3, 45)
    ax.set_ylim(-6, 24)
    ax.set_aspect("equal")
    ax.set_xlabel("x (cm)")
    ax.set_ylabel("y (cm)")
    ax.set_title("Analyzer magnet: r = √(2mV/q)/B sorts ions by mass", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax = axes[1]
    r = np.linspace(0.001, 0.1, 500)
    ax.plot(r * 100, MU0 * 1.0 / (2 * np.pi * r) * 1e6, color=B, lw=2, label="long wire, 1 A: µ₀I/(2πr)")
    R = 0.05
    ax.plot(r * 100, MU0 * 2 * R**2 / (2 * (R**2 + r**2) ** 1.5) * 1e6, color=O, lw=2, ls="--",
            label="loop R = 5 cm, 2 A, on axis (z = horizontal)")
    ax.axhline(50, color="0.5", ls=":", lw=1)
    ax.text(6.5, 54, "Earth's field ≈ 50 µT", fontsize=8, color="0.3")
    ax.set_ylim(0, 120)
    ax.set_xlabel("distance r or z (cm)")
    ax.set_ylabel("B (µT)")
    ax.set_title("Fields of everyday currents are tens of microtesla", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/lorentz-and-fields.svg")


def fig_ampere():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.7))
    ax = axes[0]
    a, I = 1e-3, 10.0
    r = np.linspace(0, 6e-3, 600)
    Bw = np.where(r < a, MU0 * I * r / (2 * np.pi * a**2), MU0 * I / (2 * np.pi * np.maximum(r, 1e-12)))
    ax.plot(r * 1e3, Bw * 1e3, color=B, lw=2)
    ax.axvspan(0, 1, color="0.9")
    ax.text(0.15, 0.3, "inside\nthe wire", fontsize=8)
    ax.set_xlabel("r (mm)")
    ax.set_ylabel("B (mT)")
    ax.set_title("10 A in a 1 mm-radius wire: linear inside, 1/r outside", fontsize=10)
    ax = axes[1]
    a, b, c = 0.5e-3, 2e-3, 2.3e-3
    r = np.linspace(1e-5, 3.5e-3, 800)
    Ienc = np.where(r < a, I * r**2 / a**2, np.where(r < b, I, np.where(r < c, I * (1 - (r**2 - b**2) / (c**2 - b**2)), 0.0)))
    ax.plot(r * 1e3, MU0 * Ienc / (2 * np.pi * r) * 1e3, color=O, lw=2)
    ax.axvspan(0, a * 1e3, color="0.9")
    ax.axvspan(b * 1e3, c * 1e3, color="0.9")
    ax.text(2.6, 1.6, "outside:\nB = 0", fontsize=8)
    ax.set_xlabel("r (mm)")
    ax.set_ylabel("B (mT)")
    ax.set_title("Coax with ±10 A: the field stays between the conductors", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/ampere-fields.svg")


def fig_hall():
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.add_patch(Rectangle((0, 0), 6, 2, color="#D8E6F2", ec=B, lw=1.5))
    for x in np.linspace(0.5, 5.5, 6):
        ax.text(x, 1.82, "−", ha="center", va="center", color=B, fontsize=12, weight="bold")
        ax.text(x, 0.18, "+", ha="center", va="center", color=O, fontsize=11, weight="bold")
    ax.add_patch(FancyArrowPatch((-1.2, 1.0), (-0.1, 1.0), arrowstyle="-|>", mutation_scale=15, color="0.2", lw=2))
    ax.text(-1.2, 1.25, "current I", fontsize=9)
    ax.annotate("", xy=(2.1, 1.55), xytext=(3.4, 1.0), arrowprops=dict(arrowstyle="-|>", color=B, lw=1.5,
                                                                     connectionstyle="arc3,rad=0.3"))
    ax.text(3.5, 0.75, "electrons drift left,\nforce −e v × B pushes them up", fontsize=8, color=B)
    for x in (4.6, 5.2):
        ax.plot(x, 1.35, "o", ms=9, mfc="white", mec=G)
        ax.plot(x, 1.35, "x", color=G, ms=5)
    ax.text(5.65, 1.27, "B into page", fontsize=8, color=G)
    ax.plot([3, 3], [2, 2.6], color="0.3")
    ax.plot([3, 3], [0, -0.6], color="0.3")
    ax.text(3.1, 2.45, "−", fontsize=12)
    ax.text(3.1, -0.65, "+", fontsize=12)
    ax.text(3.6, -0.35, "Hall voltage V_H = IB/(n e t)", fontsize=9)
    ax.set_xlim(-1.5, 8)
    ax.set_ylim(-1, 3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Hall effect in an n-type bar: charge builds up until eE_H balances e v_d B", fontsize=10)
    save(fig, f"{OUT}/hall-effect.svg")


def fig_materials():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    H = np.linspace(-1, 1, 400)
    for Hc, Bs, color, name in ((0.05, 0.45, B, "soft (ferrite core)"), (0.55, 1.2, O, "hard (permanent magnet)")):
        up = Bs * np.tanh((H + Hc) / 0.15)
        down = Bs * np.tanh((H - Hc) / 0.15)
        ax.plot(H, up, color=color, lw=2, label=name)
        ax.plot(H, down, color=color, lw=2)
    ax.axhline(0, color="0.5", lw=0.6)
    ax.axvline(0, color="0.5", lw=0.6)
    ax.set_xlabel("applied field H (arbitrary units)")
    ax.set_ylabel("flux density B (T, schematic)")
    ax.set_title("Hysteresis: soft materials switch easily, hard ones stay magnetized", fontsize=9.5)
    ax.legend(fontsize=8, loc="upper left")
    ax = axes[1]
    names = ["MnZn ferrite N87\n100 °C", "MnZn ferrite N87\n25 °C", "Kool Mµ\n(FeSiAl powder)", "High Flux\n(NiFe powder)",
             "grain-oriented\nSi steel"]
    vals = [0.39, 0.49, 1.05, 1.5, 1.65]
    err = [0, 0, 0, 0, 0.15]
    ax.barh(range(5), vals, xerr=err, color=[O, O, G, G, B], capsize=4)
    for i, val in enumerate(vals):
        ax.text(val + 0.05 + err[i], i, f"{val:g} T" if i < 4 else "1.5–1.8 T", va="center", fontsize=8)
    ax.set_yticks(range(5))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlim(0, 2.3)
    ax.set_xlabel("saturation flux density (T)")
    ax.set_title("Core materials: ferrite saturates early and loses 20% when hot", fontsize=9.5)
    fig.tight_layout()
    save(fig, f"{OUT}/magnetic-materials.svg")


if __name__ == "__main__":
    fig_analyzer()
    fig_ampere()
    fig_hall()
    fig_materials()
