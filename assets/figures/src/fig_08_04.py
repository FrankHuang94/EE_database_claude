#!/usr/bin/env python3
"""Figures for chapter 08-04 (combinational building blocks).

Run from anywhere:  python assets/figures/src/fig_08_04.py
Outputs SVGs to assets/figures/08-04/: a 4-bit ripple-carry adder with its critical path and the
arrival time of every carry (unit-delay model, computed), and the timing diagram of the multiplexer
hazard of Example 08-04.7 (computed by unit-delay simulation).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def carry_arrivals(n):
    """Unit-delay arrival times: P, G at 1; S_i = max(P_i, C_i) + 1; C_{i+1} = max(G_i, max(P_i, C_i) + 1) + 1."""
    c, out = 0, []
    for _ in range(n):
        s = max(1, c) + 1
        c = max(1, max(1, c) + 1) + 1
        out.append((s, c))
    return out


def fig_rca():
    n = 4
    arr = carry_arrivals(n)
    fig, ax = plt.subplots(figsize=(8.6, 3.2))
    w, gap = 1.6, 0.9
    for k in range(n):
        i = n - 1 - k                      # draw bit 3 on the left, bit 0 on the right
        x = k * (w + gap)
        ax.add_patch(Rectangle((x, 0), w, 1.2, fill=False, ec="k", lw=1.4))
        ax.text(x + w / 2, 0.6, "FA", ha="center", va="center", fontsize=12)
        ax.annotate("", xy=(x + 0.45, 1.2), xytext=(x + 0.45, 1.8), arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(x + 1.15, 1.2), xytext=(x + 1.15, 1.8), arrowprops=dict(arrowstyle="->"))
        ax.text(x + 0.45, 1.9, f"$A_{i}$", ha="center", fontsize=10)
        ax.text(x + 1.15, 1.9, f"$B_{i}$", ha="center", fontsize=10)
        ax.annotate("", xy=(x + w / 2, -0.6), xytext=(x + w / 2, 0), arrowprops=dict(arrowstyle="->"))
        ax.text(x + w / 2, -0.95, f"$S_{i}$ @ {arr[i][0]}", ha="center", fontsize=10)
        # carry into this adder from the right
        xr = x + w + gap
        col = PALETTE[1]
        if i == 0:
            ax.annotate("", xy=(x + w, 0.6), xytext=(x + w + 0.7, 0.6), arrowprops=dict(arrowstyle="->"))
            ax.text(x + w + 0.75, 0.6, "$C_0$ @ 0", va="center", fontsize=10)
        else:
            ax.add_patch(FancyArrowPatch((xr, 0.6), (x + w, 0.6), arrowstyle="->", mutation_scale=12,
                                         color=col, lw=2.2))
            ax.text(x + w + gap / 2, 0.85, f"$C_{i}$ @ {arr[i - 1][1]}", ha="center", fontsize=9, color=col)
    ax.add_patch(FancyArrowPatch((0, 0.6), (-0.8, 0.6), arrowstyle="->", mutation_scale=12, color=PALETTE[1], lw=2.2))
    ax.text(-0.85, 0.95, f"$C_4$ @ {arr[-1][1]}", ha="center", fontsize=10, color=PALETTE[1])
    ax.text(4.5, -1.55, "critical path (orange): $A_0$ → $C_1$ → $C_2$ → $C_3$ → $S_3$, "
            f"{arr[-1][0]} units to $S_3$ and {arr[-1][1]} to $C_4$ = $2n$ and $2n+1$ for $n = 4$",
            ha="center", fontsize=9, color=PALETTE[1])
    ax.set_xlim(-1.5, n * (w + gap) + 0.6)
    ax.set_ylim(-1.8, 2.2)
    ax.axis("off")
    ax.set_title("4-bit ripple-carry adder: arrival times in gate delays")
    save(fig, f"{OUT}/ripple-carry-adder.svg")


def fig_hazard():
    ops = {"not": lambda a: 1 - a, "and": lambda *x: int(all(x)), "or": lambda *x: int(any(x))}
    gates = [("sn", "not", ["s"]), ("t0", "and", ["sn", "d0"]), ("t1", "and", ["s", "d1"]), ("y", "or", ["t0", "t1"])]
    st = {"s": 1, "d0": 1, "d1": 1}
    for _ in range(4):
        for o, op, ins in gates:
            st[o] = ops[op](*(st[i] for i in ins))
    hist = {k: [st[k]] for k in ("s", "sn", "t0", "t1", "y")}
    cur = dict(st)
    for t in range(1, 9):
        nxt = dict(cur)                    # every gate output at t is its function of the inputs at t - 1
        for o, op, ins in gates:
            nxt[o] = ops[op](*(cur[i] for i in ins))
        nxt["s"] = 0 if t >= 2 else 1      # S falls at t = 2 (after a short steady interval)
        cur = nxt
        for k in hist:
            hist[k].append(cur[k])
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    labels = [("s", "$S$"), ("sn", "$\\overline{S}$"), ("t1", "$S D_1$"), ("t0", "$\\overline{S} D_0$"), ("y", "$Y$")]
    for row, (k, lab) in enumerate(labels):
        y0 = (len(labels) - 1 - row) * 1.4
        ts = list(range(len(hist[k]) + 1))
        vals = hist[k] + [hist[k][-1]]
        ax.step(ts, [y0 + 0.9 * v for v in vals], where="post", color=PALETTE[1] if k == "y" else PALETTE[0], lw=2)
        ax.text(-0.3, y0 + 0.4, lab, ha="right", va="center", fontsize=11)
    ax.axvspan(4, 5, color=PALETTE[1], alpha=0.15)
    ax.text(6.9, -0.75, "glitch: 1 unit,\nthe inverter's delay", ha="center", fontsize=9, color=PALETTE[1])
    for t in range(0, 10):
        ax.axvline(t, color="0.9", lw=0.6, zorder=0)
    ax.set_xlim(-1.6, 9)
    ax.set_ylim(-1.2, len(labels) * 1.4)
    ax.set_yticks([])
    ax.set_xlabel("time (gate delays)")
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.set_title("Static-1 hazard in $Y = \\overline{S}D_0 + SD_1$ with $D_0 = D_1 = 1$")
    save(fig, f"{OUT}/mux-hazard.svg")


if __name__ == "__main__":
    fig_rca()
    fig_hazard()
    print("figures written to", OUT)
