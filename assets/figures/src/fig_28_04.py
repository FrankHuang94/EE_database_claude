#!/usr/bin/env python3
"""Figures for chapter 28-04 (domain question banks I).

Run from anywhere:  python assets/figures/src/fig_28_04.py
Outputs
  assets/figures/28-04/decode-and-links.svg  left: decode attainable throughput as a share of
                                             peak against batch for Example 28-04.2's assumed
                                             accelerator (2 PFLOP/s, 8 TB/s, ridge 250 FLOP/byte)
                                             with 8-bit and 4-bit weights; right: energy per bit
                                             across the link hierarchy on a log scale, from UCIe
                                             targets [R-524], 200 Gb/s-class SerDes analog power
                                             [R-509] and NVIDIA's per-port optics claim at an
                                             assumed 1.6 Tb/s port [R-543]
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import qbank as qb  # noqa: E402

OUT = "assets/figures/28-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
F, BW = 2e15, 8e12

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
batch = np.linspace(1, 200, 400)
for k, (b_w, name) in enumerate(((1, "8-bit weights"), (0.5, "4-bit weights"))):
    share = [100 * qb.attainable(qb.decode_intensity(b, b_w), F, BW) / F for b in batch]
    ax1.plot(batch, share, color=PALETTE[k], label=name)
    br = qb.batch_at_ridge(F, BW, b_w)
    ax1.plot([br], [100], "o", color=PALETTE[k], ms=4)
    ax1.annotate(f"ridge at batch {br:g}", (br, 100), xytext=((135, 84), (3, 88))[k], fontsize=8,
                 arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax1.axvline(16, color="0.6", ls=":", lw=1)
ax1.text(20, 4, "batch 16:\n12.8% (8-bit)\n25.6% (4-bit)", fontsize=8, color="0.35")
ax1.set_xlim(0, 200)
ax1.set_ylim(0, 108)
ax1.set_xlabel("decode batch (sequences)")
ax1.set_ylabel("attainable share of peak (%)")
ax1.set_title("Decode is memory-bound until the batch is large", fontsize=10)
ax1.legend(fontsize=8, loc="lower right")
ax1.grid(True, alpha=0.3)

links = [
    ("UCIe advanced package\n(target)", 0.25, "0.25"),
    ("UCIe standard package\n(target)", 0.5, "0.5"),
    ("200G-class SerDes\n(analog only)", 3.0, "2–3"),
    ("CPO port\n(5 W at 1.6 Tb/s)", qb.port_pj_per_bit(5, 1.6e12), "3.1"),
    ("Pluggable port\n(25 W at 1.6 Tb/s)", qb.port_pj_per_bit(25, 1.6e12), "15.6"),
]
y = np.arange(len(links))
for k, (name, e, lab) in enumerate(links):
    ax2.barh(k, e, color=PALETTE[2 if k < 2 else (3 if k == 2 else 4)], height=0.55)
    if k == 2:
        ax2.plot([2.0, 3.0], [k, k], color="0.2", lw=2)
    ax2.text(e * 1.15, k, lab, va="center", fontsize=8)
ax2.set_yticks(y)
ax2.set_yticklabels([n for n, _, _ in links], fontsize=8)
ax2.set_xscale("log")
ax2.set_xlim(0.1, 60)
ax2.set_xlabel("energy per bit (pJ/bit, log scale)")
ax2.set_title("Energy per bit across the link hierarchy", fontsize=10)
ax2.grid(True, axis="x", alpha=0.3, which="both")
fig.tight_layout()
save(fig, f"{OUT}/decode-and-links.svg")
