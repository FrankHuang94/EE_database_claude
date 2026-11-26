#!/usr/bin/env python3
"""Figures for chapter 28-10 (conversation scenarios).

Run from anywhere:  python assets/figures/src/fig_28_10.py
Outputs
  assets/figures/28-10/conversation-arcs.svg  left: posterior probability answer by answer for
                                              three illustrative meetings from a prior of 0.4
                                              (likelihood ratios assumed); right: the number of
                                              the chapter's 26 scenarios in each domain of live
                                              check
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-10-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import convo as cv  # noqa: E402

OUT = "assets/figures/28-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
meetings = [
    ("strong (Example 28-10.26)", [3, 2, 0.5, 1, 3]),
    ("mixed", [3, 0.4, 1, 2, 0.5]),
    ("evasive", [0.5, 1, 0.5, 1, 0.6]),
]
for k, (name, ratios) in enumerate(meetings):
    path = cv.trajectory(0.4, ratios)
    ax1.plot(range(len(path)), [100 * p for p in path], "o-", color=PALETTE[k], label=name)
    ax1.text(len(path) - 1 + 0.1, 100 * path[-1], f"{100 * path[-1]:.0f}%", va="center", fontsize=8,
             color=PALETTE[k])
ax1.axhline(40, color="0.6", ls=":", lw=1)
ax1.set_xticks(range(6))
ax1.set_xticklabels(["prior", "1", "2", "3", "4", "5"])
ax1.set_xlim(-0.2, 5.8)
ax1.set_ylim(0, 100)
ax1.set_xlabel("answers scored")
ax1.set_ylabel("probability the claim holds (%)")
ax1.set_title("How a meeting moves belief", fontsize=10)
ax1.legend(fontsize=8, loc="upper left")
ax1.grid(True, alpha=0.3)

groups = [("accelerators and CPUs", 2), ("memory, links and optics", 3), ("analog and RF", 2),
          ("power and packaging", 2), ("embedded", 1), ("teams and schedules", 4),
          ("deals and economics", 8), ("reliability and debriefs", 4)]
y = np.arange(len(groups))
ax2.barh(y, [n for _, n in groups], color=PALETTE[3], height=0.6)
for k, (_, n) in enumerate(groups):
    ax2.text(n + 0.1, k, str(n), va="center", fontsize=8)
ax2.set_yticks(y)
ax2.set_yticklabels([g for g, _ in groups], fontsize=8)
ax2.invert_yaxis()
ax2.set_xlim(0, 9.5)
ax2.set_xlabel("scenarios using this kind of live check (of 26)")
ax2.set_title("Where the 26 scenarios draw their checks", fontsize=10)
ax2.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/conversation-arcs.svg")
