#!/usr/bin/env python3
"""Figures for chapter 19-13 (verification).

Run from anywhere:  python assets/figures/src/fig_19_13.py
Outputs
  assets/figures/19-13/coverage-closure.svg  expected fraction of coverage bins hit against the number of random samples:
                                             16 equal bins (left, with n H_n and the 95 % closure point marked) and
                                             8 bins of which one has probability 0.01 (right)
  assets/figures/19-13/bdd-order.svg         ROBDDs of x1 y1 + x2 y2 + x3 y3 under the interleaved order and with all x
                                             variables first, built with the lab's BDD package
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-13-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import verif  # noqa: E402

OUT = "assets/figures/19-13"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------- coverage closure
def p_all(n, t):
    return sum((-1) ** k * math.comb(n, k) * (1 - k / n) ** t for k in range(n + 1))


fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.6))
t = np.arange(0, 201)
a1.plot(t, 16 * (1 - (1 - 1 / 16) ** t), color=PALETTE[0], label="expected bins covered")
a1b = a1.twinx()
a1b.plot(t, [p_all(16, k) for k in t], color=PALETTE[1], ls="--")
a1b.set_ylabel("P(all 16 covered), dashed", color=PALETTE[1])
a1b.set_ylim(-0.05, 1.05)
mean = verif.expected_to_cover(16)
t95 = next(k for k in t if p_all(16, k) >= 0.95)
a1.axvline(mean, color="0.4", lw=0.8, ls=":")
a1.axvline(t95, color="0.4", lw=0.8, ls=":")
a1.text(mean + 2, 3, f"mean {mean:.2f}", fontsize=8)
a1.text(t95 + 2, 7, f"95 % at {t95}", fontsize=8)
a1.set_xlabel("random samples")
a1.set_ylabel("bins (of 16)")
a1.set_title("16 equally likely bins", fontsize=10)
a1.legend(fontsize=8, loc="lower right")

rare = [0.99 / 7] * 7 + [0.01]
t2 = np.arange(0, 601)
a2.plot(t2, [sum(1 - (1 - p) ** k for p in rare) for k in t2], color=PALETTE[0], label="expected bins covered")
a2.axhline(7, color="0.6", lw=0.8)
mean2 = verif.expected_to_cover_exact(rare)
a2.axvline(mean2, color="0.4", lw=0.8, ls=":")
a2.text(mean2 + 8, 4, f"mean {mean2:.1f}", fontsize=8)
a2.set_xlabel("random samples")
a2.set_ylabel("bins (of 8)")
a2.set_title("7 common bins + 1 bin with p = 0.01", fontsize=10)
a2.set_ylim(0, 8.3)
fig.tight_layout()
save(fig, f"{OUT}/coverage-closure.svg")


# ---------------------------------------------------------------- BDD variable order
def draw(ax, order_names, var_ids, title):
    b = verif.BDD(6)
    v = {name: b.var(var_ids[name]) for name in var_ids}
    f = 0
    for i in (1, 2, 3):
        f = b.OR(f, b.AND(v[f"x{i}"], v[f"y{i}"]))
    nodes, stack = [], [f]
    while stack:
        u = stack.pop()
        if u <= 1 or u in nodes:
            continue
        nodes.append(u)
        stack += list(b.nodes[u][1:])
    levels = {}
    for u in nodes:
        levels.setdefault(b.nodes[u][0], []).append(u)
    W = 6.0
    pos = {}
    for lev, us in levels.items():
        us.sort()
        if len(us) == 1:
            pos[us[0]] = (W / 2 + (-0.9 if lev % 2 == 0 else 0.9), -lev)
        else:
            for k, u in enumerate(us):
                pos[u] = ((k + 1) * W / (len(us) + 1), -lev)
    pos[0], pos[1] = (0.3 * W, -6.4), (0.7 * W, -6.4)
    for u in nodes:
        _, lo, hi = b.nodes[u]
        for child, style in ((lo, "--"), (hi, "-")):
            (x0, y0), (x1, y1) = pos[u], pos[child]
            ax.plot([x0, x1], [y0, y1], style, color="0.35", lw=0.9, zorder=1)
    for u in nodes:
        ax.add_patch(plt.Circle(pos[u], 0.32, color=PALETTE[0], zorder=2))
        ax.text(*pos[u], order_names[b.nodes[u][0]], ha="center", va="center", color="white", fontsize=8, zorder=3)
    for term in (0, 1):
        x, y = pos[term]
        ax.add_patch(plt.Rectangle((x - 0.3, y - 0.3), 0.6, 0.6, color="0.2", zorder=2))
        ax.text(x, y, str(term), ha="center", va="center", color="white", fontsize=9, zorder=3)
    ax.set_xlim(-0.2, W + 0.2)
    ax.set_ylim(-6.9, 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{title}: {len(nodes)} nodes", fontsize=10)


fig, (b1, b2) = plt.subplots(1, 2, figsize=(8.4, 5.0))
inter = ["x1", "y1", "x2", "y2", "x3", "y3"]
sep = ["x1", "x2", "x3", "y1", "y2", "y3"]
draw(b1, inter, {n: inter.index(n) for n in inter}, "interleaved order")
draw(b2, sep, {n: sep.index(n) for n in sep}, "all x first")
fig.text(0.5, 0.02, "solid edge: variable = 1   dashed edge: variable = 0", ha="center", fontsize=8)
save(fig, f"{OUT}/bdd-order.svg")
