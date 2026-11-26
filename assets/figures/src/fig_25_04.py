#!/usr/bin/env python3
"""Figures for chapter 25-04 (yield models and die cost).

Run from anywhere:  python assets/figures/src/fig_25_04.py
Outputs
  assets/figures/25-04/wafer-map.svg     10.1 mm die sites on a 294 mm usable diameter (exact best grid), with dies killed by
                                         40 random defects and by a cluster of 40 defects (seeded, illustrative)
  assets/figures/25-04/yield-models.svg  Poisson, Murphy and negative-binomial (alpha = 3 and 1) yield against A*D0
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import yieldcost as y  # noqa: E402

OUT = "assets/figures/25-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def wafer_map() -> None:
    n, ox, oy = y.dpw_exact(294, 10.1, 10.1)
    sites = y.die_sites(294, 10.1, 10.1, ox, oy)
    rng = np.random.default_rng(4)
    r = 147 * np.sqrt(rng.random(40))
    th = 2 * np.pi * rng.random(40)
    rand = np.column_stack([r * np.cos(th), r * np.sin(th)])
    clus = np.column_stack([60 + rng.normal(0, 9, 40), -40 + rng.normal(0, 9, 40)])
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    ax.add_patch(Circle((0, 0), 150, fill=False, lw=1.2))
    ax.add_patch(Circle((0, 0), 147, fill=False, lw=0.5, ls=":"))
    for sx, sy in sites:
        hit_r = np.any((rand[:, 0] >= sx) & (rand[:, 0] < sx + 10.1) & (rand[:, 1] >= sy) & (rand[:, 1] < sy + 10.1))
        hit_c = np.any((clus[:, 0] >= sx) & (clus[:, 0] < sx + 10.1) & (clus[:, 1] >= sy) & (clus[:, 1] < sy + 10.1))
        col = PALETTE[1] if hit_c else (PALETTE[3] if hit_r else "#dfe8f1")
        ax.add_patch(Rectangle((sx, sy), 10.1, 10.1, facecolor=col, edgecolor="white", lw=0.4))
    ax.plot(rand[:, 0], rand[:, 1], "k.", ms=3, label="random defects")
    ax.plot(clus[:, 0], clus[:, 1], "kx", ms=3, label="clustered defects")
    ax.set_xlim(-160, 160)
    ax.set_ylim(-160, 160)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend(loc="lower left", fontsize=7, frameon=False)
    ax.set_title(f"{n} dies; pink: killed by random defects, orange: by the cluster", fontsize=8)
    save(fig, f"{OUT}/wafer-map.svg")


def yield_models() -> None:
    x = np.linspace(0.01, 3, 300)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot(x, [y.y_poisson(v) for v in x], color=PALETTE[0], label="Poisson")
    ax.plot(x, [y.y_murphy(v) for v in x], color=PALETTE[2], ls="--", label="Murphy")
    ax.plot(x, [y.y_negbin(v, 3) for v in x], color=PALETTE[1], label="negative binomial, α = 3")
    ax.plot(x, [y.y_negbin(v, 1) for v in x], color=PALETTE[3], ls="-.", label="negative binomial, α = 1 (Seeds)")
    ax.set_xlabel("A·D₀ (expected killer defects per die)")
    ax.set_ylabel("yield")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/yield-models.svg")


if __name__ == "__main__":
    wafer_map()
    yield_models()
