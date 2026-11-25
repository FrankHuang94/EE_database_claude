#!/usr/bin/env python3
"""Figures for chapter 23-07 (SSD controllers and storage systems).

Run from anywhere:  python assets/figures/src/fig_23_07.py
Outputs
  assets/figures/23-07/wa-vs-op.svg   write amplification against over-provisioning (relative to user capacity) under
                                      uniform random writes: the FIFO closed form, simulated FIFO and greedy points
                                      (ssd.simulate_ftl, 32,768 user pages, 64-page blocks), and Desnoyers' (SYSTOR
                                      2012, Table 2) greedy values converted from spare factor
  assets/figures/23-07/ecc-cliff.svg  failure probability of ~1 KiB codewords (8,192 data bits + 14 t parity bits)
                                      against raw bit error rate for t = 20, 40, 60
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import ssd  # noqa: E402

OUT = "assets/figures/23-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# Desnoyers 2012, Table 2: greedy cleaning, analytic A at spare factor Sf
DESNOYERS_GREEDY = ((0.03, 13.624), (0.05, 8.872), (0.07, 6.623), (0.11, 4.430), (0.17, 3.002))


def wa_vs_op() -> None:
    op = np.linspace(0.03, 0.45, 200)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.plot(op * 100, [ssd.wa_fifo(1 + x) for x in op], color=PALETTE[0], label="FIFO closed form")
    pts = (0.05, 0.07, 0.14, 0.28, 0.40)
    ax.plot([x * 100 for x in pts], [ssd.simulate_ftl(32768, x, policy="fifo", writes_per_page=3) for x in pts],
            "o", color=PALETTE[0], ms=5, label="FIFO simulated")
    ax.plot([x * 100 for x in pts], [ssd.simulate_ftl(32768, x, policy="greedy", writes_per_page=3) for x in pts],
            "s", color=PALETTE[1], ms=5, label="greedy simulated")
    ax.plot([(1 / (1 - sf) - 1) * 100 for sf, _ in DESNOYERS_GREEDY], [a for _, a in DESNOYERS_GREEDY], "^",
            color=PALETTE[2], ms=6, label="greedy, Desnoyers 2012")
    ax.set_xlabel("over-provisioning (% of user capacity)")
    ax.set_ylabel("write amplification")
    ax.set_ylim(1, 16)
    ax.legend()
    fig.tight_layout()
    save(fig, f"{OUT}/wa-vs-op.svg")


def ecc_cliff() -> None:
    p = np.logspace(-4.5, -2, 300)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for t, col in ((20, PALETTE[0]), (40, PALETTE[1]), (60, PALETTE[2])):
        n = 8192 + 14 * t
        ax.loglog(p, [max(ssd.codeword_failure(n, t, x), 1e-30) for x in p], color=col, label=f"t = {t}")
    ax.axhline(1e-15, color="0.5", ls=":", lw=1)
    ax.set_ylim(1e-20, 1)
    ax.set_xlabel("raw bit error rate")
    ax.set_ylabel("codeword failure probability")
    ax.legend(loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/ecc-cliff.svg")


if __name__ == "__main__":
    wa_vs_op()
    ecc_cliff()
