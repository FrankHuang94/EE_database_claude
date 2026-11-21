#!/usr/bin/env python3
"""Figures for chapter 18-04 (DMA and data movement).

Run from anywhere:  python assets/figures/src/fig_18_04.py
Outputs
  assets/figures/18-04/buffer-sizing.svg  left: smallest safe block N against the CPU's worst service latency L for two and
                                         three buffers (Example 18-04.2's processing model, 1 MS/s, a = 20 µs,
                                         b = 0.6 µs/sample) and its next power of two; right: worst latency
                                         N/fs + L + a + bN of the power-of-two design
Uses labs/18-04-lab/dmasim.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs" / "18-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dmasim as dm  # noqa: E402

OUT = "assets/figures/18-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fs, a, b = 1e6, 20e-6, 0.6e-6
L = np.linspace(0, 60e-6, 121)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6))
for k, col in ((2, PALETTE[0]), (3, PALETTE[1])):
    nmin = np.array([dm.pingpong_min_block(fs, a, b, x, k) for x in L])
    npow = 2 ** np.ceil(np.log2(nmin))
    a1.plot(L * 1e6, nmin, color=col, label=f"{k} buffers: bound")
    a1.step(L * 1e6, npow, where="post", color=col, ls="--", lw=1, label=f"{k} buffers: next power of two")
    lat = npow / fs + L + a + b * npow
    a2.plot(L * 1e6, lat * 1e6, color=col, label=f"{k} buffers")
a1.axvline(25, color="gray", lw=0.8)
a1.set_xlabel("worst service latency L (µs)")
a1.set_ylabel("block size N (samples)")
a1.set_title("Smallest safe block")
a1.legend(fontsize=7)
a2.axvline(25, color="gray", lw=0.8)
a2.set_xlabel("worst service latency L (µs)")
a2.set_ylabel("worst latency (µs)")
a2.set_title("Latency of the power-of-two design")
a2.legend(fontsize=7)
fig.tight_layout()
save(fig, f"{OUT}/buffer-sizing.svg")
