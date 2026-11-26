#!/usr/bin/env python3
"""Figures for chapter 28-02 (validating claims).

Run from anywhere:  python assets/figures/src/fig_28_02.py
Outputs
  assets/figures/28-02/peak-and-efficiency.svg  left: roofline of Example 28-02.1's NPU
                                                (78.6 TOPS dense INT8, 64 GB/s assumed) against
                                                arithmetic intensity, with the 157 TOPS headline;
                                                right: efficiency against supply voltage along a
                                                linear voltage-frequency line from (0.60 V,
                                                400 MHz) to (0.90 V, 1.0 GHz), dynamic power only,
                                                anchored at Example 28-02.3's 80 TOPS at 4.0 W
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import claimcheck as cc  # noqa: E402

OUT = "assets/figures/28-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
peak = cc.peak_ops(cc.NPU_MACS, cc.NPU_CLOCK)
inten = np.logspace(0, 4, 300)
ax1.loglog(inten, [cc.roofline_ops(peak, cc.NPU_BW, x) / 1e12 for x in inten], color=PALETTE[0],
           label="roofline, dense INT8")
ax1.axhline(2 * peak / 1e12, color=PALETTE[1], ls="--", lw=1.2, label='"up to 157 TOPS" headline')
ridge = peak / cc.NPU_BW
ax1.axvline(ridge, color="0.6", ls=":", lw=1)
ax1.text(ridge * 1.08, 1.2, f"ridge {ridge:.0f} ops/byte", fontsize=8, color="0.35")
ax1.plot([300], [cc.roofline_ops(peak, cc.NPU_BW, 300) / 1e12], "o", color="0.2", ms=4)
ax1.annotate("19.2 TOPS at\n300 ops/byte", (300, 19.2), xytext=(15, 30), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax1.set_ylim(0.05, 400)
ax1.set_xlabel("arithmetic intensity (ops/byte)")
ax1.set_ylabel("attainable throughput (TOPS)")
ax1.set_title("Delivered throughput sits under the roofline", fontsize=10)
ax1.legend(fontsize=8, loc="lower right")
ax1.grid(True, alpha=0.3, which="both")

volts = np.linspace(0.60, 0.90, 61)
freqs = 0.4e9 + (volts - 0.60) / 0.30 * 0.6e9
power = [cc.scale_dynamic_power(4.0, 0.60, 0.4e9, vv, ff) for vv, ff in zip(volts, freqs)]
tops = 80 * freqs / 0.4e9
eff = tops / np.array(power)
ax2.plot(volts, eff, color=PALETTE[2], label="efficiency (TOPS/W)")
ax2.plot([0.60], [20], "o", color="0.2", ms=4)
ax2.annotate("20 TOPS/W at 80 TOPS\n(0.60 V, 400 MHz)", (0.60, 20), xytext=(0.66, 18.5), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax2.plot([0.90], [200 / 22.5], "o", color="0.2", ms=4)
ax2.annotate("8.9 TOPS/W at 200 TOPS\n(0.90 V, 1.0 GHz)", (0.90, 200 / 22.5), xytext=(0.70, 10.0), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax2.set_xlabel("supply voltage (V)")
ax2.set_ylabel("efficiency (TOPS/W)")
ax2.set_ylim(6, 22)
ax2.set_title("Peak and best efficiency are different points", fontsize=10)
ax2.grid(True, alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/peak-and-efficiency.svg")
