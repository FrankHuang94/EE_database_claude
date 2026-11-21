#!/usr/bin/env python3
"""Figures for chapter 18-05 (GPIO, UART, SPI, I²C).

Run from anywhere:  python assets/figures/src/fig_18_05.py
Outputs
  assets/figures/18-05/uart-sampling.svg  an 8N1 frame (byte 0x4B) as sent by a sender 4% slow, on time and 4% fast,
                                         with the receiver's sampling instants (start edge detected one 16x tick
                                         late, then one sample per bit at its centre); the stop-bit sample is where
                                         mismatch fails first (chapter section 3.3)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/18-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

byte = 0x4B
bits = [0] + [(byte >> i) & 1 for i in range(8)] + [1]          # start, data LSB first, stop
delta = 1 / 16
samples = delta + 0.5 + np.arange(10)                            # receiver bit times
fig, axs = plt.subplots(3, 1, figsize=(8.8, 4.6), sharex=True)
for ax, r, label in zip(axs, (1.04, 1.00, 0.96), ("sender 4% slow (r = 1.04)", "on time (r = 1.00)", "sender 4% fast (r = 0.96)")):
    edges = np.arange(11) * r
    ax.step(np.concatenate(([-0.5], edges, [11.5])), np.concatenate(([1], bits, [1, 1])), where="post", color=PALETTE[0])
    for k, sp in enumerate(samples):
        inside = edges[k] <= sp < edges[k + 1]
        ax.plot([sp], [bits[k]], marker="o" if inside else "x", ms=7, color=PALETTE[2] if inside else PALETTE[1])
    ax.plot([], [], "o", color=PALETTE[2], label="sample inside its bit")
    ax.set_yticks([0, 1])
    ax.set_ylabel("line")
    ax.set_title(label, fontsize=9, loc="left")
    ax.set_ylim(-0.3, 1.4)
axs[-1].set_xlabel("time (receiver bit times from the falling start edge); dots: receiver samples at the intended bit")
fig.suptitle("UART 8N1 frame (0x4B) and the receiver's samples: the last sample drifts most", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/uart-sampling.svg")
