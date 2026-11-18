#!/usr/bin/env python3
"""Figures for chapter 02-07 (determinants, inverses, rank, vector spaces, least squares).

Run:  python assets/figures/src/fig_02_07.py  -> assets/figures/02-07/*.svg
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/02-07"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def arrow(ax, start, end, color, lw=2.0, ls="-"):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=13))


def fig_det_area():
    r1 = np.array([3.0, 1.0])
    r2 = np.array([2.0, 4.0])
    r2e = r2 - (2 / 3) * r1          # one elimination step: row 2 minus (2/3) row 1
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2), sharey=True)
    for ax, (a, b), title in ((axes[0], (r1, r2), "rows (3, 1) and (2, 4): area |det| = 10"),
                              (axes[1], (r1, r2e), "after R2 − (2/3)R1: rows (3, 1), (0, 10/3): area 10")):
        poly = Polygon([(0, 0), tuple(a), tuple(a + b), tuple(b)], closed=True, facecolor=B, alpha=0.18,
                       edgecolor=B, lw=1.2)
        ax.add_patch(poly)
        arrow(ax, (0, 0), tuple(a), O)
        arrow(ax, (0, 0), tuple(b), G)
        ax.text(a[0] + 0.1, a[1] - 0.35, "row 1", color=O, fontsize=9)
        ax.text(b[0] - 0.95, b[1] + 0.1, "row 2", color=G, fontsize=9)
        ax.set_aspect("equal")
        ax.set_xlim(-0.6, 5.6)
        ax.set_ylim(-0.6, 5.6)
        ax.set_title(title, fontsize=10)
    axes[1].annotate("", xy=tuple(r2e), xytext=tuple(r2),
                     arrowprops=dict(arrowstyle="->", color="0.5", lw=1, ls="--"))
    axes[1].text(0.9, 4.2, "shear: row 2 slides\nparallel to row 1", fontsize=8, color="0.35")
    axes[1].plot([0, r1[0], r1[0] + r2e[0], r2e[0], 0], [0, r1[1], r1[1] + r2e[1], r2e[1], 0], color="0.6",
                 lw=0.6, ls=":")
    fig.suptitle("An elimination step is a shear: the area (the determinant) is unchanged", fontsize=11)
    fig.tight_layout()
    save(fig, f"{OUT}/det-area.svg")


def fig_least_squares():
    T = np.array([0, 20, 40, 60, 80.0])
    V = np.array([0.402, 0.598, 0.801, 0.997, 1.205])
    X = np.c_[np.ones(5), T]
    c, d = np.linalg.solve(X.T @ X, X.T @ V)
    res = V - (c + d * T)
    fig = plt.figure(figsize=(12.0, 3.9))
    ax1 = fig.add_subplot(1, 3, 1)
    tt = np.linspace(-5, 85, 50)
    ax1.plot(tt, c + d * tt, color=B, label=f"fit: V = {c:.4f} + {d*1e3:.3f} mV/°C · T")
    ax1.plot(T, V, "o", color="k", ms=5, label="calibration data")
    ax1.set_xlabel("temperature T (°C)")
    ax1.set_ylabel("sensor output V (V)")
    ax1.legend(fontsize=8, loc="upper left")
    ax1.set_title("Least-squares line (Example 02-07.4)", fontsize=10)
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.axhline(0, color="0.5", lw=1)
    ax2.vlines(T, 0, res * 1e3, color=O, lw=2)
    ax2.plot(T, res * 1e3, "o", color=O)
    ax2.set_xlabel("temperature T (°C)")
    ax2.set_ylabel("residual (mV)")
    ax2.set_title("Residuals: sum 0, orthogonal to T", fontsize=10)
    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    s = np.linspace(-1, 1.6, 2)
    S1, S2 = np.meshgrid(s, s)
    a1 = np.array([1.0, 0.0, 0.0])
    a2 = np.array([0.3, 1.0, 0.0])
    Xp = S1 * a1[0] + S2 * a2[0]
    Yp = S1 * a1[1] + S2 * a2[1]
    ax3.plot_surface(Xp, Yp, 0 * Xp, alpha=0.15, color=B)
    b = np.array([1.0, 0.9, 1.1])
    p = np.array([1.0, 0.9, 0.0])
    ax3.plot([0, b[0]], [0, b[1]], [0, b[2]], color="k", lw=2)
    ax3.plot([0, p[0]], [0, p[1]], [0, p[2]], color=G, lw=2.4)
    ax3.plot([p[0], b[0]], [p[1], b[1]], [p[2], b[2]], color=O, lw=2, ls="--")
    ax3.scatter(*b, color="k", s=18)
    ax3.scatter(*p, color=G, s=18)
    ax3.text(b[0] + 0.05, b[1], b[2] + 0.05, "b (data)", color="k", fontsize=9)
    ax3.text(p[0] + 0.08, p[1] - 0.1, 0, "p = Ax̂", color=G, fontsize=9)
    ax3.text(p[0] + 0.06, p[1], 0.55, "e = b − p\nperpendicular\nto the plane", color=O, fontsize=8)
    ax3.set_xlim(-1, 1.6)
    ax3.set_ylim(-1, 1.6)
    ax3.set_zlim(0, 1.3)
    ax3.text(-0.9, 1.4, 0, "column space C(A)", color=B, fontsize=8)
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_zticks([])
    ax3.set_title("Projection onto the column space", fontsize=10)
    ax3.view_init(elev=20, azim=-60)
    fig.tight_layout()
    save(fig, f"{OUT}/least-squares.svg")


def fig_circuit_graph():
    pos = {1: (0.0, 1.0), 2: (2.0, 1.0), 3: (4.0, 1.0), 0: (2.0, -0.9)}
    branches = [("a", 1, 2, "1 mS"), ("b", 1, 3, "0.5 mS"), ("c", 2, 0, "1 mS"), ("d", 2, 3, "0.5 mS"),
                ("e", 3, 0, "2 mS")]
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    # highlight loop a-d-b (1 -> 2 -> 3 -> 1)
    ax.add_patch(Polygon([(0.25, 1.12), (3.75, 1.12), (3.6, 2.2), (0.4, 2.2)], closed=True, facecolor=P,
                         alpha=0.08, edgecolor="none"))
    ax.text(2.0, 1.45, "loop 1 → 2 → 3 → 1\n(a, d, then b reversed)", ha="center", fontsize=8, color=P)
    for name, s, e, g in branches:
        (x0, y0), (x1, y1) = pos[s], pos[e]
        rad = -0.55 if name == "b" else 0.0
        arr = FancyArrowPatch((x0, y0), (x1, y1), connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                              mutation_scale=16, lw=1.8, color=B, shrinkA=14, shrinkB=14)
        ax.add_patch(arr)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        if name == "b":
            mx, my = 2.0, 2.4
        elif name == "c":
            mx += 0.45
        elif name == "e":
            mx, my = mx + 0.55, my + 0.1
        else:
            my -= 0.25
        ax.text(mx, my, f"{name}: {g}", ha="center", va="center", fontsize=9, color=B,
                bbox=dict(facecolor="white", edgecolor="none", pad=1))
    for n, (x, y) in pos.items():
        ax.add_patch(plt.Circle((x, y), 0.17, color="white", ec="k", lw=1.5, zorder=3))
        ax.text(x, y, str(n), ha="center", va="center", fontsize=11, zorder=4)
    ax.text(2.0, -1.3, "node 0 = ground", ha="center", fontsize=9, color="0.35")
    ax.set_xlim(-0.6, 4.6)
    ax.set_ylim(-1.5, 2.7)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Example 02-06.5's circuit as a graph: 4 nodes, 5 branches", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/circuit-graph.svg")


if __name__ == "__main__":
    fig_det_area()
    fig_least_squares()
    fig_circuit_graph()
