#!/usr/bin/env python3
"""Figures for chapter 25-01 (process flow overview: FEOL, MOL and BEOL).

Run from anywhere:  python assets/figures/src/fig_25_01.py
Outputs
  assets/figures/25-01/stack-cross-section.svg  schematic cross-section: STI and a nanosheet transistor (FEOL),
                                                silicide and contacts (MOL), and a tiered BEOL stack (not to scale)
  assets/figures/25-01/deal-grove.svg           oxide thickness against time, wet and dry, (100) Si, 900/1000/1100 C
  assets/figures/25-01/wire-tiers.svg           RC delay against length for local, intermediate and global tiers,
                                                with the time-of-flight line (eps_r = 3.0)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import process as p  # noqa: E402

OUT = "assets/figures/25-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def box(ax, x, y, w, h, fc, ec="black", lw=0.6, **kw):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, **kw))


def stack_cross_section() -> None:
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    si, ox, metal, gate, epi = "#d9d9d9", "#f2efe6", "#c87533", "#5b7fb0", "#a9c9a4"
    # FEOL: substrate, STI, nanosheet transistor
    box(ax, 0, 0, 10, 2.0, si)
    ax.text(5, 0.7, "silicon substrate", ha="center", fontsize=8)
    for x in (0.2, 8.6):
        box(ax, x, 1.2, 1.2, 0.8, ox)
        ax.text(x + 0.6, 1.55, "STI", ha="center", fontsize=7)
    box(ax, 0, 2.0, 10, 1.9, ox, lw=0.3)                       # ILD0 around the device
    box(ax, 2.1, 2.0, 1.4, 1.5, epi)                            # source epi
    box(ax, 6.5, 2.0, 1.4, 1.5, epi)                            # drain epi
    ax.text(2.8, 2.15, "S", ha="center", fontsize=7)
    ax.text(7.2, 2.15, "D", ha="center", fontsize=7)
    box(ax, 3.7, 2.0, 2.6, 1.9, gate)                           # gate wraps the sheets
    box(ax, 3.5, 2.0, 0.2, 1.9, "white", lw=0.4)                # outer and inner spacers
    box(ax, 6.3, 2.0, 0.2, 1.9, "white", lw=0.4)
    for y in (2.25, 2.7, 3.15):
        box(ax, 3.5, y, 3.0, 0.22, si, lw=0.5)                  # nanosheet channels run S to D through the spacers
    ax.text(5.0, 3.62, "metal gate", ha="center", fontsize=7, color="white")
    # MOL: silicide and contacts
    for x in (2.1, 6.5):
        box(ax, x, 3.5, 1.4, 0.08, "#555555", lw=0)            # silicide
        box(ax, x + 0.45, 3.58, 0.5, 1.02, metal)               # trench contacts reach M0
    box(ax, 4.8, 3.9, 0.4, 0.7, metal)                          # gate contact reaches M0
    box(ax, 0, 3.9, 10, 0.6, ox, lw=0.3, zorder=0)
    # BEOL tiers: (y, thickness, line width, pitch)
    tiers = [(4.6, 0.25, 0.25, 0.5), (5.15, 0.25, 0.25, 0.5), (5.7, 0.25, 0.25, 0.5),
             (6.35, 0.45, 0.5, 1.0), (7.15, 0.45, 0.5, 1.0), (8.0, 0.8, 1.2, 2.5), (9.35, 0.8, 1.2, 2.5)]
    for y, h, w, pitch in tiers:
        box(ax, 0, y - 0.05, 10, h + 0.1, ox, lw=0.2, zorder=0)
        for x in np.arange(0.15, 10 - w, pitch):
            box(ax, x, y, w, h, metal, lw=0.4)
    # vias joining each layer to the one above (a few, where lines overlap)
    for (y0, h0, w0, p0), (y1, h1, w1, p1) in zip(tiers[:-1], tiers[1:]):
        xs = np.arange(0.15, 10 - w1, p1)[::2]
        for x in xs:
            box(ax, x + w1 / 2 - 0.08, y0 + h0, 0.16, y1 - (y0 + h0), metal, lw=0.3)
    box(ax, 0, 10.2, 10, 0.25, "#bbbbbb", lw=0.4)               # passivation
    ax.text(5, 10.27, "passivation and pads", ha="center", fontsize=7)
    # brackets
    def bracket(y0, y1, text):
        ax.plot([10.25, 10.4, 10.4, 10.25], [y0, y0, y1, y1], color="black", lw=0.8)
        ax.text(10.55, (y0 + y1) / 2, text, va="center", fontsize=8)
    bracket(0.0, 3.9, "FEOL\n(transistors)")
    bracket(3.5, 4.5, "MOL (contacts)")
    bracket(4.55, 5.95, "BEOL local\n(M0–M2)")
    bracket(6.3, 7.65, "intermediate")
    bracket(7.95, 10.2, "global\n(thick)")
    ax.set_xlim(-0.2, 12.6)
    ax.set_ylim(-0.2, 10.7)
    ax.set_aspect("auto")
    ax.axis("off")
    save(fig, f"{OUT}/stack-cross-section.svg")


def deal_grove() -> None:
    t = np.logspace(-2, 2, 300)
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for amb, ls in (("wet", "-"), ("dry", "--")):
        for tc, col in zip((900, 1000, 1100), (PALETTE[0], PALETTE[1], PALETTE[2])):
            ax.loglog(t, [p.oxide_thickness(ti, tc, amb) for ti in t], ls=ls, color=col, label=f"{amb}, {tc} °C")
    ax.set_xlabel("oxidation time (h)")
    ax.set_ylabel("oxide thickness (µm)")
    ax.set_ylim(1e-3, 5)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7, ncol=2)
    save(fig, f"{OUT}/deal-grove.svg")


def wire_tiers() -> None:
    tiers = {"local (20 × 40 nm)": (20, 40, 2, 4.5), "intermediate (40 × 80 nm)": (40, 80, 2, 2.8),
             "global (400 × 800 nm)": (400, 800, 2, 1.9)}
    L = np.logspace(1, 4, 200)
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for (name, geo), col in zip(tiers.items(), PALETTE):
        r = p.wire_r_per_um(*geo)
        ax.loglog(L / 1000, [p.rc_delay(r, 0.2e-15, length) * 1e12 for length in L], color=col, label=name)
    ax.loglog(L / 1000, [p.time_of_flight(length, 3.0) * 1e12 for length in L], "k:", label="time of flight (εr = 3.0)")
    ax.set_xlabel("wire length (mm)")
    ax.set_ylabel("50% delay (ps)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7)
    save(fig, f"{OUT}/wire-tiers.svg")


if __name__ == "__main__":
    stack_cross_section()
    deal_grove()
    wire_tiers()
