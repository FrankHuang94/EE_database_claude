#!/usr/bin/env python3
"""Figures for chapter 28-03 (maturity scales for silicon).

Run from anywhere:  python assets/figures/src/fig_28_03.py
Outputs
  assets/figures/28-03/maturity-and-fit.svg  left: value multiplier P/(1+r)^(T/12) at maturity
                                             levels L2-L5 for Example 28-03.2's assumed stage
                                             chain at 15% a year; right: zero-failure FIT bound
                                             against devices on a 1000-hour test at 125 C, for a
                                             55 C use junction and 0.7 eV, at 60% and 90%
                                             confidence, with the JESD47G minimum of 231 marked
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import matscale as ms  # noqa: E402

OUT = "assets/figures/28-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
CHAIN = [(0.95, 4.5), (0.80, 6), (0.85, 5), (0.95, 2)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
labels = ["L2\ntape-out", "L3\nfirst silicon", "L4\nengineering\nsamples", "L5\nqualified"]
mult = [ms.value_multiplier(CHAIN[k:], 0.15) for k in range(4)]
bars = ax1.bar(range(4), mult, color=PALETTE[0], width=0.6)
for k, m in enumerate(mult):
    ax1.text(k, m + 0.02, f"{m:.2f}", ha="center", fontsize=9)
ax1.set_xticks(range(4))
ax1.set_xticklabels(labels, fontsize=8)
ax1.set_ylim(0, 1.05)
ax1.set_ylabel("value multiplier (fraction of a released product)")
ax1.set_title("Value rises as risk and waiting fall", fontsize=10)
ax1.grid(True, axis="y", alpha=0.3)

accel = ms.arrhenius_af(0.7, 55, 125)
n = np.logspace(math.log10(50), 4, 200)
for k, c in enumerate((0.6, 0.9)):
    ax2.loglog(n, [ms.fit_upper(x, 1000, 0, accel, c) for x in n], color=PALETTE[k + 1],
               label=f"{int(100 * c)}% confidence")
for c in (0.6, 0.9):
    ax2.plot([231], [ms.fit_upper(231, 1000, 0, accel, c)], "o", color="0.2", ms=4)
ax2.axvline(231, color="0.6", ls=":", lw=1)
ax2.text(240, 3.0, "JESD47G minimum\n231 devices", fontsize=8, color="0.35")
ax2.annotate("51 FIT", (231, ms.fit_upper(231, 1000, 0, accel, 0.6)), xytext=(90, 22), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax2.annotate("128 FIT", (231, ms.fit_upper(231, 1000, 0, accel, 0.9)), xytext=(600, 200), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax2.set_xlabel("devices on a zero-failure 1000-hour test")
ax2.set_ylabel("upper bound on use failure rate (FIT)")
ax2.set_title("What a life test proves (55 °C use, 0.7 eV)", fontsize=10)
ax2.legend(fontsize=8, loc="lower left")
ax2.grid(True, alpha=0.3, which="both")
fig.tight_layout()
save(fig, f"{OUT}/maturity-and-fit.svg")
