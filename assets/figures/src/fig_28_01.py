#!/usr/bin/env python3
"""Figures for chapter 28-01 (a framework for evaluating a chip company's technology).

Run from anywhere:  python assets/figures/src/fig_28_01.py
Outputs
  assets/figures/28-01/evidence-and-voi.svg  left: posterior probability against prior for
                                             likelihood ratios 0.25, 0.5, 2, 4 and 16 (Bayes'
                                             rule in odds form); right: the expected value of
                                             sample information of Example 28-01.6's test
                                             (gain 500, loss 200, prior 0.4) against its
                                             sensitivity for specificities 0.7 to 0.99, with
                                             the EVPI of 120 as a ceiling
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dilmodel as dm  # noqa: E402

OUT = "assets/figures/28-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
priors = np.linspace(0.005, 0.995, 199)
for k, lr in enumerate((0.25, 0.5, 2, 4, 16)):
    ax1.plot(priors, [dm.posterior(p, [lr]) for p in priors], color=PALETTE[k % len(PALETTE)],
             label=f"LR = {lr:g}")
ax1.plot(priors, priors, color="0.5", ls="--", lw=1, label="no evidence")
ax1.plot([0.2], [0.8], "o", color="0.2", ms=4)
ax1.annotate("20% to 80% needs LR = 16", (0.2, 0.8), xytext=(0.03, 0.93), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax1.set_xlabel("prior probability")
ax1.set_ylabel("posterior probability")
ax1.set_title("Evidence moves belief by its likelihood ratio", fontsize=10)
ax1.legend(fontsize=8, loc="lower right")
ax1.grid(True, alpha=0.3)

sens = np.linspace(0.5, 1.0, 101)
for k, spec in enumerate((0.7, 0.8, 0.9, 0.99)):
    ax2.plot(sens, [dm.evsi(0.4, 500, -200, a, spec)[0] for a in sens], color=PALETTE[k % len(PALETTE)],
             label=f"specificity {spec:g}")
evpi = dm.buy_or_pass(0.4, 500, -200)[1]
ax2.axhline(evpi, color="0.5", ls="--", lw=1)
ax2.text(0.51, evpi + 3, f"EVPI = {evpi:.0f}", fontsize=8, color="0.3")
ax2.plot([0.8], [dm.evsi(0.4, 500, -200, 0.8, 0.9)[0]], "o", color="0.2", ms=4)
ax2.annotate("Example 28-01.6:\nEVSI = 68", (0.8, 68), xytext=(0.84, 22), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax2.set_xlim(0.5, 1.0)
ax2.set_ylim(0, 135)
ax2.set_xlabel("test sensitivity")
ax2.set_ylabel("EVSI (\\$ million)")
ax2.set_title("A test is worth what it can change", fontsize=10)
ax2.legend(fontsize=8, loc="upper left", bbox_to_anchor=(0.0, 0.80))
ax2.grid(True, alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/evidence-and-voi.svg")
