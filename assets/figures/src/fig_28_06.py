#!/usr/bin/env python3
"""Figures for chapter 28-06 (red flags and green flags).

Run from anywhere:  python assets/figures/src/fig_28_06.py
Outputs
  assets/figures/28-06/false-alarms-and-counts.svg  left: probability that a healthy company
                                                    shows at least one red flag against the
                                                    checklist length, for false-positive rates
                                                    of 2%, 5% and 10%; right: binomial count
                                                    distributions for healthy (4% per flag)
                                                    and troubled (30%) companies on a 25-flag
                                                    checklist, with a three-flag threshold
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import flagmodel as fm  # noqa: E402

OUT = "assets/figures/28-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
n = np.arange(0, 81)
for k, f in enumerate((0.02, 0.05, 0.10)):
    ax1.plot(n, [100 * fm.false_alarm(x, f) for x in n], color=PALETTE[k], label=f"{int(100 * f)}% per flag")
ax1.axhline(50, color="0.6", ls=":", lw=1)
ax1.plot([25], [100 * fm.false_alarm(25, 0.04)], "o", color="0.2", ms=4)
ax1.annotate("25 flags at 4%: 64%", (25, 100 * fm.false_alarm(25, 0.04)), xytext=(32, 40), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax1.set_xlim(0, 80)
ax1.set_ylim(0, 102)
ax1.set_xlabel("flags on the checklist")
ax1.set_ylabel("healthy company shows ≥ 1 flag (%)")
ax1.set_title("Long checklists cry wolf", fontsize=10)
ax1.legend(fontsize=8, loc="lower right", title="false-positive rate", title_fontsize=8)
ax1.grid(True, alpha=0.3)

k = np.arange(0, 21)
ax2.bar(k - 0.2, 100 * stats.binom.pmf(k, 25, 0.04), width=0.4, color=PALETTE[3], label="healthy (4% per flag)")
ax2.bar(k + 0.2, 100 * stats.binom.pmf(k, 25, 0.30), width=0.4, color=PALETTE[4], label="troubled (30% per flag)")
ax2.axvline(2.5, color="0.3", ls="--", lw=1)
ax2.text(2.8, 33, "threshold:\n3 or more flags\nratio 13", fontsize=8, color="0.3")
ax2.set_xlim(-0.8, 20)
ax2.set_xticks(range(0, 21, 2))
ax2.set_xlabel("flags shown on a 25-flag checklist")
ax2.set_ylabel("probability (%)")
ax2.set_title("The count separates what single flags cannot", fontsize=10)
ax2.legend(fontsize=8, loc="upper right")
ax2.grid(True, axis="y", alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/false-alarms-and-counts.svg")
