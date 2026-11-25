#!/usr/bin/env python3
"""Figures for chapter 23-01 (the memory hierarchy and the memory wall).

Run from anywhere:  python assets/figures/src/fig_23_01.py
Outputs
  assets/figures/23-01/memory-wall.svg       peak FLOPS, DRAM bandwidth and interconnect bandwidth growing at 3.0, 1.6
                                             and 1.4 times every two years (Gholami et al.'s 20-year fit), normalized
                                             to 1 at year 0, with the ridge point (FLOPS / DRAM bandwidth)
  assets/figures/23-01/decode-intensity.svg  decode arithmetic intensity against batch size for Example 23-01.7's
                                             model at 4k, 32k and 128k contexts, with each curve's KV-cache limit and
                                             the 625 FLOP/B ridge point
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import memwall as mw  # noqa: E402

OUT = "assets/figures/23-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def memory_wall() -> None:
    years = np.linspace(0, 20, 201)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    for rate, col, lab in ((3.0, PALETTE[0], "peak FLOPS, 3.0× / 2 yr"), (1.6, PALETTE[1], "DRAM bandwidth, 1.6× / 2 yr"),
                           (1.4, PALETTE[2], "interconnect bandwidth, 1.4× / 2 yr")):
        ax.semilogy(years, mw.growth(rate, years), color=col, label=lab)
    ax.semilogy(years, mw.growth(3.0, years) / mw.growth(1.6, years), "--", color=PALETTE[3],
                label="ridge point (FLOPS / DRAM bandwidth)")
    ax.set_xlabel("years")
    ax.set_ylabel("growth (normalized to 1 at year 0)")
    ax.legend(fontsize=8)
    ax.set_title("The memory wall: compute outgrows bandwidth (fit of Gholami et al., 2024)", fontsize=10)
    save(fig, f"{OUT}/memory-wall.svg")


def decode_intensity() -> None:
    m = mw.Transformer(params=70e9, weight_bytes=1, layers=80, q_heads=64, kv_heads=8, head_dim=128, kv_bytes=1)
    batch = np.unique(np.logspace(0, 3, 300).astype(int))
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    for ctx, col in ((4096, PALETTE[0]), (32_768, PALETTE[1]), (131_072, PALETTE[2])):
        ax.semilogx(batch, [m.intensity(ctx, int(b)) for b in batch], color=col, label=f"{ctx // 1024}k context")
        ax.axhline(m.intensity_limit(ctx), color=col, ls=":", lw=0.9)
    ax.axhline(mw.ridge_point(5e15, 8e12), color=PALETTE[7], ls="--", label="ridge point, 625 FLOP/B (FP8 dense)")
    ax.set_yscale("log")
    ax.set_xlabel("batch size (sequences)")
    ax.set_ylabel("arithmetic intensity (FLOP/B)")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Decode intensity saturates at the KV-cache limit (dotted), far below the ridge", fontsize=10)
    save(fig, f"{OUT}/decode-intensity.svg")


if __name__ == "__main__":
    memory_wall()
    decode_intensity()
