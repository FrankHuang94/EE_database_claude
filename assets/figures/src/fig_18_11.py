#!/usr/bin/env python3
"""Figures for chapter 18-11 (hardware security).

Run from anywhere:  python assets/figures/src/fig_18_11.py
Outputs
  assets/figures/18-11/cpa.svg  correlation of each of the 256 key-byte guesses with simulated AES first-round leakage
                               (Hamming weight of the S-box output plus noise of 3 Hamming-weight units, 1000 traces),
                               unprotected and with a fresh first-order Boolean mask per trace; the true key (0x2B)
                               stands out only without the mask
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs" / "18-11-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import hwsec as hs  # noqa: E402

OUT = "assets/figures/18-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def correlations(p, leak):
    hyp = hs.HW[hs.SBOX[np.bitwise_xor.outer(np.arange(256), p)]].astype(float)
    hyp -= hyp.mean(axis=1, keepdims=True)
    l = leak - leak.mean()
    return hyp @ l / (np.sqrt((hyp ** 2).sum(axis=1)) * np.sqrt((l ** 2).sum()))


fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.6), sharey=True)
for ax, masked, title in zip(axs, (False, True), ("unprotected", "first-order masking")):
    p, leak = hs.simulate_traces(0x2B, 1000, 3.0, masked=masked)
    r = correlations(p, leak)
    ax.bar(np.arange(256), r, width=1.0, color=PALETTE[0])
    ax.bar([0x2B], [r[0x2B]], width=3.0, color=PALETTE[1], label="true key 0x2B")
    ax.axhline(4.5 / np.sqrt(1000), color="grey", linestyle=":", linewidth=0.8)
    ax.axhline(-4.5 / np.sqrt(1000), color="grey", linestyle=":", linewidth=0.8)
    ax.set_title(f"{title}, 1000 traces", fontsize=10)
    ax.set_xlabel("key-byte guess")
    ax.legend(fontsize=8)
axs[0].set_ylabel("correlation with measured leakage")
fig.suptitle("Correlation power analysis: the right guess stands out unless the data are masked", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/cpa.svg")
