#!/usr/bin/env python3
"""Figures for chapter 19-11 (floorplan, place and route, signoff).

Run from anywhere:  python assets/figures/src/fig_19_11.py
Outputs
  assets/figures/19-11/quadratic-placement.svg  Example 19-11.3: four movable cells pulled by springs to three pads;
                                                the quadratic optimum
  assets/figures/19-11/steiner.svg              Example 19-11.5's four-pin net: bounding box (HPWL), rectilinear
                                                minimum spanning tree and rectilinear Steiner minimum tree
  assets/figures/19-11/h-tree.svg               a two-level H-tree feeding 16 sinks in a square of side D, with equal
                                                source-to-sink path lengths
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-11-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import pnr  # noqa: E402

OUT = "assets/figures/19-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- quadratic placement (Example 3)
pads = {"P0": (0, 0), "P1": (10, 0), "P2": (5, 6)}
nets = [("P0", 0, 1), (0, 1, 1), (1, 2, 1), (2, "P1", 1), (1, 3, 1), (3, "P2", 2)]
pos = pnr.quadratic_place(4, nets, pads)
names = "ABCD"
fig, ax = plt.subplots(figsize=(6.4, 4.2))
pt = lambda p: pads[p] if isinstance(p, str) else tuple(pos[p])
for a, b, w in nets:
    (x0, y0), (x1, y1) = pt(a), pt(b)
    ax.plot([x0, x1], [y0, y1], color="0.5", lw=1.0 + 1.5 * (w - 1), zorder=1)
for n, (x, y) in pads.items():
    ax.plot(x, y, "s", ms=11, color=PALETTE[1], zorder=2)
    ax.annotate(n, (x, y), textcoords="offset points", xytext=(8, -12), fontsize=9)
for k, (x, y) in enumerate(pos):
    ax.plot(x, y, "o", ms=12, color=PALETTE[0], zorder=2)
    ax.annotate(f"{names[k]} ({x:.1f}, {y:.1f})", (x, y), textcoords="offset points", xytext=(9, 6), fontsize=9)
ax.set_xlim(-1, 12.5)
ax.set_ylim(-1, 7)
ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Quadratic placement: fixed pads (squares), movable cells (circles); D-P2 has weight 2", fontsize=10)
save(fig, f"{OUT}/quadratic-placement.svg")

# ---------------------------------------------------------------- Steiner vs spanning tree (Example 5)
pins = [(0, 0), (4, 6), (6, 2), (2, 8)]


def draw_l(ax, p, q, color, lw):
    """Rectilinear connection: horizontal first, then vertical."""
    ax.plot([p[0], q[0], q[0]], [p[1], p[1], q[1]], color=color, lw=lw)


fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.8), sharey=True)
xs, ys = [p[0] for p in pins], [p[1] for p in pins]
axes[0].add_patch(plt.Rectangle((min(xs), min(ys)), max(xs) - min(xs), max(ys) - min(ys), fill=False, ls="--",
                                color=PALETTE[2], lw=1.5))
axes[0].set_title(f"bounding box: HPWL = {pnr.hpwl(pins)}", fontsize=10)
for i, j in pnr.rmst_edges(pins):
    draw_l(axes[1], pins[i], pins[j], PALETTE[0], 2)
axes[1].set_title(f"spanning tree: {pnr.rmst_length(pins)}", fontsize=10)
spts = pnr.rsmt_points(pins)
for i, j in pnr.rmst_edges(spts):
    draw_l(axes[2], spts[i], spts[j], PALETTE[1], 2)
for p in spts[len(pins):]:
    axes[2].plot(*p, "D", ms=7, color=PALETTE[1])
axes[2].set_title(f"Steiner tree: {pnr.rsmt_length(pins)}", fontsize=10)
for ax in axes:
    for p in pins:
        ax.plot(*p, "o", ms=8, color="k")
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 9)
    ax.set_aspect("equal")
    ax.grid(True, lw=0.3)
save(fig, f"{OUT}/steiner.svg")

# ---------------------------------------------------------------- H-tree, two levels (16 sinks)
fig, ax = plt.subplots(figsize=(4.8, 4.8))


def h(ax, cx, cy, size, level, lw):
    """One H of total width and height `size` centred at (cx, cy); recurse at its four tips."""
    half = size / 2
    ax.plot([cx - half, cx + half], [cy, cy], color=PALETTE[0], lw=lw)
    for sx in (-1, 1):
        ax.plot([cx + sx * half] * 2, [cy - half, cy + half], color=PALETTE[0], lw=lw)
    tips = [(cx + sx * half, cy + sy * half) for sx in (-1, 1) for sy in (-1, 1)]
    if level == 1:
        for x, y in tips:
            ax.plot(x, y, "o", ms=6, color=PALETTE[1])
        return
    for x, y in tips:
        h(ax, x, y, size / 2, level - 1, lw * 0.7)


D = 1.0
ax.add_patch(plt.Rectangle((0, 0), D, D, fill=False, color="0.6"))
h(ax, 0.5, 0.5, D / 2, 2, 3.0)
ax.plot(0.5, 0.5, "*", ms=14, color="k")
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("H-tree: 16 sinks (dots), equal paths from the source (star)", fontsize=10)
save(fig, f"{OUT}/h-tree.svg")
