#!/usr/bin/env python3
"""Figures for chapter 06-01 (charge, current, voltage, power and the lumped circuit abstraction).

Run from anywhere:  python assets/figures/src/fig_06_01.py
Outputs SVGs to assets/figures/06-01/. Schematics use schemdraw; plots use matplotlib.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/06-01"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(ROOT / OUT / name))


# ------------------------------------------------------------------ schematics
def fig_passive_sign():
    """A two-terminal element with + at the top terminal and the current reference entering it."""
    from matplotlib.patches import FancyArrowPatch, Rectangle
    fig, ax = plt.subplots(figsize=(3.6, 4.4))
    ax.set_xlim(-2.2, 2.6)
    ax.set_ylim(-0.6, 6.4)
    ax.axis("off")
    ax.plot([0, 0], [5.6, 4.0], color="k", lw=2)                      # top lead
    ax.plot([0, 0], [2.0, 0.4], color="k", lw=2)                      # bottom lead
    ax.add_patch(Rectangle((-0.75, 2.0), 1.5, 2.0, fill=False, lw=2))
    ax.text(0, 3.0, "element", ha="center", va="center", fontsize=11)
    for y, name in ((5.6, "A"), (0.4, "B")):
        ax.plot(0, y, "o", ms=9, mfc="white", mec="k", mew=2)
        ax.text(-0.35, y, f"terminal {name}", ha="right", va="center", fontsize=10)
    ax.add_patch(FancyArrowPatch((0, 5.35), (0, 4.35), arrowstyle="-|>", mutation_scale=20, color=O, lw=2))
    ax.text(0.25, 4.85, "$i$", color=O, fontsize=15, va="center")
    ax.text(1.25, 3.85, "+", fontsize=18, ha="center", va="center", color=B)
    ax.text(1.25, 2.15, "−", fontsize=18, ha="center", va="center", color=B)
    ax.text(1.25, 3.0, "$v$", fontsize=16, ha="center", va="center", color=B)
    ax.text(0.2, -0.35, "absorbed power  $p = v\\,i$", ha="center", fontsize=11)
    save(fig, f"{OUT}/passive-sign-convention.svg")


def sch_two_sources(d):
    """Example 06-01.2: 12 V with 2 ohm and 6 V with 3 ohm feed node A; 6 ohm load to ground."""
    d += (v1 := elm.SourceV().up().label("$V_1$ = 12 V"))
    d += elm.Resistor().right().label("$R_1$ = 2 Ω").label("$i_1$ →", loc="bottom", fontsize=11)
    d += (a := elm.Dot().label("A", loc="top"))
    d += elm.Resistor().down().label("$R_3$ = 6 Ω", loc="bottom").label("$i_3$ ↓", loc="top", fontsize=11)
    d += (g := elm.Dot())
    d += elm.Line().left().tox(v1.start)
    d += elm.Ground().at(g.center)
    d += elm.Resistor().right().at(a.center).label("$R_2$ = 3 Ω").label("← $i_2$", loc="bottom", fontsize=11)
    d += (v2 := elm.SourceV().down().reverse().label("$V_2$ = 6 V", loc="bottom"))
    d += elm.Line().left().tox(g.center)


# ------------------------------------------------------------------ plots
def fig_lumped_vs_edge():
    """Far-end voltage of a 1 ns line, 10 ohm driver, open load, for three edge rates (bounce diagram)."""
    rs, z0, td, rl = 10.0, 50.0, 1e-9, 1e6
    gs, gl = (rs - z0) / (rs + z0), (rl - z0) / (rl + z0)
    tau = z0 / (rs + z0)
    t = np.linspace(0, 40e-9, 8001)
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    for tr, col, lab in ((0.1e-9, O, "0.1 ns edge"), (6e-9, G, "6 ns edge"), (20e-9, B, "20 ns edge")):
        v = np.zeros_like(t)
        for k in range(200):
            v += tau * (1 + gl) * (gl * gs) ** k * np.clip((t - (2 * k + 1) * td) / tr, 0, 1)
        ax.plot(t * 1e9, v, color=col, label=lab)
    ax.axhline(1.0, color="0.5", lw=0.8, ls="--")
    ax.set_xlabel("time (ns)")
    ax.set_ylabel("far-end voltage (V)")
    ax.set_xlim(0, 40)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    save(fig, f"{OUT}/lumped-vs-edge.svg")


def fig_wearable_profile():
    """Example 06-01.4: sleep 2 uA, sensing 1.2 mA for 20 ms each second, radio 8 mA for 3 ms every 10 s."""
    t = np.linspace(0, 10.0, 200001)
    i = np.full_like(t, 2e-6)
    for k in range(10):
        i += np.where((t >= k + 0.5) & (t < k + 0.52), 1.2e-3, 0.0)
    i += np.where((t >= 9.70) & (t < 9.703), 8e-3, 0.0)
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.semilogy(t, i * 1e6, color=B, lw=1.0, label="supply current")
    ax.axhline(28.4, color=O, ls="--", lw=1.2, label="average 28.4 µA")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("current (µA)")
    ax.set_ylim(1, 2e4)
    ax.set_xlim(0, 10)
    ax.text(9.62, 9500, "radio\n8 mA, 3 ms", ha="right", fontsize=9)
    ax.text(0.55, 1700, "sensing\n1.2 mA, 20 ms", fontsize=9)
    ax.text(5.0, 2.6, "sleep 2 µA", fontsize=9, ha="center")
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.62), fontsize=9, framealpha=0.95)
    ax.grid(True, which="both", alpha=0.25)
    save(fig, f"{OUT}/wearable-current-profile.svg")


if __name__ == "__main__":
    fig_passive_sign()
    schematic("two-sources-and-load.svg", sch_two_sources)
    fig_lumped_vs_edge()
    fig_wearable_profile()
    print("06-01 figures written to", OUT)
