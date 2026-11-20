#!/usr/bin/env python3
"""Figure for chapter 16-04 (the FFT algorithm).

Run from anywhere:  python assets/figures/src/fig_16_04.py
Outputs assets/figures/16-04/flowgraph.svg: the 8-point radix-2 decimation-in-time signal-flow graph, inputs in
bit-reversed order, three stages of butterflies (spans 1, 2, 4) with their twiddle factors W8^k on the lower input
of each butterfly, and outputs in natural order. The butterfly connectivity is generated from the same loop
structure as labs/16-04-lab/fft.py (fft_dit).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import fft  # noqa: E402

OUT = "assets/figures/16-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_flowgraph():
    N = 8
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    xs = [0, 2.2, 4.4, 6.6]
    y = lambda r: N - 1 - r  # noqa: E731  (row 0 at the top)
    stage = 0
    size = 2
    while size <= N:
        half = size // 2
        x0, x1 = xs[stage], xs[stage + 1]
        for start in range(0, N, size):
            for j in range(half):
                k = j * (N // size)
                p, q = start + j, start + j + half
                col = PALETTE[0] if k in (0, 2) else PALETTE[3]
                ax.plot([x0, x1], [y(p), y(p)], color="k", lw=0.8)
                ax.plot([x0, x1], [y(q), y(q)], color="k", lw=0.8)
                ax.plot([x0, x1], [y(p), y(q)], color=col, lw=0.8)
                ax.plot([x0, x1], [y(q), y(p)], color=col, lw=0.8)
                ax.text(x0 + 0.08, y(q) - 0.32, f"W$_8^{k}$", fontsize=7, color=col)
                ax.text(x1 - 0.18, y(q) + 0.12, "−1", fontsize=6, color="gray")
        stage += 1
        size *= 2
    for r in range(N):
        for x in xs:
            ax.plot(x, y(r), "o", color="k", ms=3)
        ax.text(xs[0] - 0.25, y(r), f"x[{fft.bit_reverse(r, 3)}]", ha="right", va="center", fontsize=8)
        ax.text(xs[-1] + 0.25, y(r), f"X[{r}]", ha="left", va="center", fontsize=8)
    for s in range(3):
        ax.text((xs[s] + xs[s + 1]) / 2, N - 0.35, f"stage {s + 1} (span {2 ** s})", ha="center", fontsize=8)
    ax.text(xs[-1] / 2, -1.0, "blue: twiddle 1 or −j (no multiplier)    pink: non-trivial twiddle    −1: the lower output subtracts",
            ha="center", fontsize=7)
    ax.set_xlim(-1.2, xs[-1] + 1.0)
    ax.set_ylim(-1.3, N + 0.1)
    ax.axis("off")
    fig.tight_layout()
    save(fig, f"{OUT}/flowgraph.svg")


if __name__ == "__main__":
    fig_flowgraph()
