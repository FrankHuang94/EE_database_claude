#!/usr/bin/env python3
"""Figures for chapter 16-10 (quantization and fixed-point effects).

Run from anywhere:  python assets/figures/src/fig_16_10.py
Outputs
  assets/figures/16-10/loading.svg       SQNR of a Gaussian signal against the loading factor L (full scale over
                                         sigma) at 12 and 16 bits: granular noise only (dashed) and with clipping
  assets/figures/16-10/limit-cycles.svg  zero-input response of the second-order Q1.15 section of Example 16-10.5
                                         (a1 = -1.6, a2 = 0.9) from (0.9, -0.9) with wrap-around and with saturation
Uses labs/16-10-lab/quant.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-10-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import quant as q  # noqa: E402

OUT = "assets/figures/16-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

L = np.linspace(2.5, 8, 400)
fig, ax = plt.subplots(figsize=(6.4, 3.8))
for B, col in ((12, PALETTE[0]), (16, PALETTE[1])):
    D = 2.0 ** (1 - B)
    s2 = 1 / L**2
    clip = 2 * s2 * ((1 + L**2) * norm.sf(L) - L * norm.pdf(L))
    tot = 10 * np.log10(s2 / (D * D / 12 + clip))
    gran = 10 * np.log10(s2 / (D * D / 12))
    ax.plot(L, tot, color=col, label=f"{B} bits, with clipping")
    ax.plot(L, gran, color=col, ls="--", lw=0.8, label=f"{B} bits, rounding only")
    i = int(np.argmax(tot))
    ax.plot(L[i], tot[i], "o", color=col)
ax.set_xlabel("loading factor L = full scale / σ")
ax.set_ylabel("SQNR (dB)")
ax.set_ylim(20, 100)
ax.set_title("Back off too little and clipping dominates; too much and rounding does")
ax.legend(fontsize=8, loc="lower right")
save(fig, f"{OUT}/loading.svg")

w = q.second_order_zero_input(-1.6, 0.9, 0.9, -0.9, "wrap", 300)
s = q.second_order_zero_input(-1.6, 0.9, 0.9, -0.9, "saturate", 300)
fig, ax = plt.subplots(figsize=(7.0, 3.4))
ax.plot(np.array(w) / 32768, color=PALETTE[1], lw=0.8, label="wrap-around: sustained full-scale oscillation")
ax.plot(np.array(s) / 32768, color=PALETTE[0], lw=1.2, label="saturation: decays (to a 3 LSB limit cycle)")
ax.set_xlabel("sample")
ax.set_ylabel("output (full scale = 1)")
ax.set_title("Zero input, stable poles (radius 0.95): only the arithmetic differs")
ax.legend(fontsize=8, loc="upper right")
save(fig, f"{OUT}/limit-cycles.svg")
print("figures written to", OUT)
