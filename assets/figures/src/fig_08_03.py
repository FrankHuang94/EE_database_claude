#!/usr/bin/env python3
"""Figures for chapter 08-03 (logic minimization).

Run from anywhere:  python assets/figures/src/fig_08_03.py
Outputs SVGs to assets/figures/08-03/: the three-variable cube with the implicants of Example 08-03.1
drawn as subcubes, and Karnaugh maps of Examples 08-03.2 and 08-03.4 with their groups.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def proj(a, b, c):
    """Oblique projection of the cube corner (A, B, C)."""
    return (b * 2.0 + a * 0.9, c * 2.0 + a * 0.7)


def fig_cube():
    on = {1, 3, 4, 5, 7}
    fig, ax = plt.subplots(figsize=(5.0, 4.4))
    corners = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    for p in corners:
        for k in range(3):
            q = list(p)
            q[k] = 1 - q[k]
            q = tuple(q)
            if p < q:
                (x1, y1), (x2, y2) = proj(*p), proj(*q)
                ax.plot([x1, x2], [y1, y2], color="0.75", lw=1, zorder=1)
    # implicant C: the face C = 1 (minterms 1, 3, 5, 7)
    face = [proj(0, 0, 1), proj(0, 1, 1), proj(1, 1, 1), proj(1, 0, 1)]
    ax.fill([x for x, _ in face], [y for _, y in face], color=PALETTE[5], alpha=0.35, zorder=0)
    # implicant AB': the edge from 100 to 101
    (x1, y1), (x2, y2) = proj(1, 0, 0), proj(1, 0, 1)
    ax.plot([x1, x2], [y1, y2], color=PALETTE[1], lw=5, alpha=0.7, zorder=2)
    for a, b, c in corners:
        m = 4 * a + 2 * b + c
        x, y = proj(a, b, c)
        ax.plot(x, y, "o", ms=13, color=PALETTE[0] if m in on else "white", mec="k", zorder=3)
        ax.text(x + 0.12, y - 0.32, f"{a}{b}{c}\n$m_{m}$", fontsize=8, zorder=4)
    ax.text(1.5, 2.95, "face $C$ (4 minterms, 1 literal)", color=PALETTE[0], fontsize=9)
    ax.text(1.05, -0.55, "edge $A\\overline{B}$ (2 minterms, 2 literals)", color=PALETTE[1], fontsize=9)
    ax.set_xlim(-0.5, 3.6)
    ax.set_ylim(-0.8, 3.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("$F = \\sum m(1, 3, 4, 5, 7) = C + A\\overline{B}$ on the 3-cube")
    save(fig, f"{OUT}/three-cube.svg")


GRAY = ["00", "01", "11", "10"]


def draw_map(ax, on, dc, groups, title):
    for r, ab in enumerate(GRAY):
        for c, cd in enumerate(GRAY):
            m = int(ab + cd, 2)
            val = "1" if m in on else "X" if m in dc else "0"
            ax.add_patch(plt.Rectangle((c, 3 - r), 1, 1, fill=False, ec="0.4", lw=0.8))
            ax.text(c + 0.5, 3 - r + 0.5, val, ha="center", va="center", fontsize=13,
                    color="k" if val != "0" else "0.6")
            ax.text(c + 0.92, 3 - r + 0.08, str(m), ha="right", va="bottom", fontsize=6.5, color="0.45")
    for (x0, y0, w, h), color, label, lpos in groups:
        ax.add_patch(FancyBboxPatch((x0 + 0.08, y0 + 0.08), w - 0.16, h - 0.16,
                                    boxstyle="round,pad=0.0,rounding_size=0.3", fill=False, ec=color, lw=2.2))
        if label:
            ax.text(*lpos, label, color=color, fontsize=10, ha="center")
    ax.set_xticks([0.5, 1.5, 2.5, 3.5])
    ax.set_xticklabels(GRAY)
    ax.set_yticks([3.5, 2.5, 1.5, 0.5])
    ax.set_yticklabels(GRAY)
    ax.xaxis.tick_top()
    ax.set_xlabel("$CD$")
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("$AB$")
    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(-0.75, 4.2)
    ax.set_aspect("equal")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=10, pad=24)


def fig_kmaps():
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.4))
    blue, orange, green = PALETTE[0], PALETTE[1], PALETTE[2]
    # Example 08-03.2: BD in the middle, B'D' as the four corners (drawn as four corner pieces)
    corners = [((-0.1, 3, 0.75, 1.1), orange, "", None), ((3.35, 3, 0.75, 1.1), orange, "", None),
               ((-0.1, -0.1, 0.75, 1.1), orange, "", None), ((3.35, -0.1, 0.75, 1.1), orange, "", None)]
    draw_map(axes[0], {0, 2, 5, 7, 8, 10, 13, 15}, set(),
             [((1, 1, 2, 2), blue, "$BD$", (2.0, -0.55))] + corners,
             "Example 08-03.2: $BD + \\overline{B}\\,\\overline{D}$")
    axes[0].text(0.55, -0.55, "$\\overline{B}\\,\\overline{D}$ (corners)", color=orange, fontsize=10, ha="center")
    # Example 08-03.4: A (bottom two rows), BD, BC
    draw_map(axes[1], {5, 6, 7, 8, 9}, set(range(10, 16)),
             [((0, 0, 4, 2), green, "$A$", (0.5, -0.55)), ((1, 1, 2, 2), blue, "", None),
              ((2, 1.05, 2, 1.9), orange, "", None)],
             "Example 08-03.4 with don't cares: $A + BD + BC$")
    axes[1].text(1.7, -0.55, "$BD$", color=blue, fontsize=10)
    axes[1].text(3.0, -0.55, "$BC$", color=orange, fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/kmap-groups.svg")


if __name__ == "__main__":
    fig_cube()
    fig_kmaps()
    print("figures written to", OUT)
