#!/usr/bin/env python3
"""Figures for chapter 04-05 (current, resistance and conduction).

Run from anywhere:  python assets/figures/src/fig_04_05.py
Outputs SVGs to assets/figures/04-05/. Random elements use seed 2026.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/04-05"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
EPS0 = 8.8541878188e-12


def fig_drude():
    rng = np.random.default_rng(2026)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.0))
    ax = axes[0]
    for drift, color, label in ((0.0, B, "no field"), (0.35, O, "field pushes electrons to the left")):
        pos = np.zeros(2)
        path = [pos.copy()]
        for _ in range(60):
            th = rng.uniform(0, 2 * np.pi)
            step = rng.exponential(1.0)
            pos = pos + step * np.array([np.cos(th), np.sin(th)]) + np.array([-drift * step**2, 0.0])
            path.append(pos.copy())
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], "-", color=color, lw=1.0, marker=".", ms=3, label=label)
        ax.plot(path[-1, 0], path[-1, 1], "o", color=color, ms=7)
    ax.plot(0, 0, "ks", ms=6)
    ax.annotate("", xy=(0.95, 0.08), xytext=(0.70, 0.08), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color=G, lw=2))
    ax.text(0.825, 0.12, "field E", color=G, fontsize=10, ha="center", transform=ax.transAxes)
    ax.set_title("Random flights between collisions, plus a slow drift against E", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax.margins(0.08, 0.35)
    ax.set_xticks([])
    ax.set_yticks([])
    ax = axes[1]
    labels = ["drift, 1 A in 1 mm²", "thermal speed (classical, 300 K)", "Fermi speed (copper)", "speed of light"]
    vals = [7.35e-5, 1.168e5, 1.57e6, 2.998e8]
    ax.barh(range(4), vals, color=[O, "0.6", B, G])
    ax.set_xscale("log")
    ax.set_yticks(range(4))
    ax.set_yticklabels(labels, fontsize=8.5)
    for i, val in enumerate(vals):
        ax.text(val * 1.6, i, f"{val:.2g} m/s", va="center", fontsize=8)
    ax.set_xlim(1e-5, 3e10)
    ax.set_xlabel("speed (m/s, log scale)")
    ax.set_title("Electrons race at the Fermi speed but drift at a snail's pace", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/drude-drift.svg")


def fig_wire():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9), gridspec_kw={"width_ratios": [0.8, 1.2]})
    ax = axes[0]
    for x0 in (0, 40):
        ax.add_patch(Rectangle((x0, 0), 20, 40, color="#7F7F7F"))
        ax.add_patch(Rectangle((x0 + 2.5, 2.5), 15, 37.5, color="#D58A3A"))
    ax.add_patch(Rectangle((-10, -10), 80, 10, color="#E8E0F0"))
    ax.add_patch(Rectangle((20, 0), 20, 40, color="#F2EEF7"))
    ax.text(10, 21, "Cu", ha="center", fontsize=10, color="white", weight="bold")
    ax.text(30, 20, "low-k\n2.8", ha="center", fontsize=8)
    ax.annotate("barrier + liner\n2.5 nm", xy=(41.2, 30), xytext=(63, 44), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.text(10, -6, "20 nm", ha="center", fontsize=8)
    ax.text(-4, 20, "40 nm", ha="center", rotation=90, fontsize=8)
    ax.set_xlim(-12, 85)
    ax.set_ylim(-12, 52)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Cross-section: the barrier takes 30% of the area", fontsize=10)
    ax = axes[1]
    rho = 1.68e-8
    Rp = rho / (15e-9 * 37.5e-9)
    Cp = 2 * 2.8 * EPS0 * (40 / 20) + 2 * 2.8 * EPS0 * (20 / 40)
    L = np.logspace(-6, -2, 200)
    t50 = 0.3787 * Rp * Cp * L**2
    ax.loglog(L * 1e6, t50 * 1e12, color=B, lw=2, label="unrepeated wire: 0.379 RC ∝ L²")
    for Lm in (100e-6, 1e-3):
        ax.plot(Lm * 1e6, 0.3787 * Rp * Cp * Lm**2 * 1e12, "o", color=O)
    ax.axhline(10, color="0.5", ls=":", lw=1)
    ax.text(1.3, 13, "10 ps reference", fontsize=8, color="0.3")
    ax.set_xlabel("wire length (µm)")
    ax.set_ylabel("50% delay (ps)")
    ax.set_title("Delay grows as length squared (Example 04-05.6, bulk ρ)", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/wire-rc.svg")


def fig_em():
    years = [2018, 2020, 2022, 2024, 2026, 2028]
    limit = [1.8, 1.1, 0.7, 0.4, 0.3, 0.2]
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    ax.bar(years, limit, width=1.4, color=B)
    for y, l in zip(years, limit):
        ax.text(y, l + 0.04, f"{l}", ha="center", fontsize=9)
    ax.plot([2018, 2028], [2.29, 5.35], "o", color=O, ms=8, label="needed to drive four inverters (2018 and 2028 only)")
    ax.set_ylabel("current density (MA/cm²)")
    ax.set_xlabel("year (projection)")
    ax.set_title("ITRS 2015 projection: tolerable DC current density in minimum Cu lines at 105 °C", fontsize=9)
    ax.legend(fontsize=8)
    ax.set_ylim(0, 6)
    fig.tight_layout()
    save(fig, f"{OUT}/em-limit.svg")


if __name__ == "__main__":
    fig_drude()
    fig_wire()
    fig_em()
