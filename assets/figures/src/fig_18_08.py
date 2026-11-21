#!/usr/bin/env python3
"""Figures for chapter 18-08 (boot, bootloaders and firmware update).

Run from anywhere:  python assets/figures/src/fig_18_08.py
Outputs
  assets/figures/18-08/power-cut-outcomes.svg  for each installation scheme of the lab's model (six-sector images),
                                              the outcome of cutting power during each flash operation in turn:
                                              the new image boots, the old image boots, or nothing boots
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs" / "18-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import bootsim as bs  # noqa: E402

OUT = "assets/figures/18-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

schemes = [("inplace", "in place (one slot)"), ("overwrite", "overwrite (two slots)"), ("swap", "swap via scratch")]
colors = {2: PALETTE[2], 1: PALETTE[0], None: PALETTE[1]}
fig, axs = plt.subplots(len(schemes), 1, figsize=(9.0, 3.9), sharex=True)
for ax, (s, label) in zip(axs, schemes):
    total = bs.count_ops(s, 6)
    outcomes = [bs.run_with_cut(s, 6, k) for k in range(total)]
    for k, o in enumerate(outcomes):
        ax.barh(0, 1, left=k, color=colors[o], edgecolor="white")
    ax.set_yticks([])
    counts = {name: sum(1 for o in outcomes if o == val) for name, val in (("new", 2), ("old", 1), ("bricked", None))}
    ax.set_title(f"{label}: {total} operations; new {counts['new']}, old {counts['old']}, bricked {counts['bricked']}",
                 fontsize=9, loc="left")
handles = [Patch(color=colors[val], label=name)
           for val, name in ((2, "new image boots"), (1, "old image boots"), (None, "nothing boots"))]
axs[0].legend(handles=handles, fontsize=8, ncol=3, loc="upper right", bbox_to_anchor=(1.0, 2.0))
axs[-1].set_xlabel("flash operation during which power fails")
axs[-1].set_xticks(np.arange(0, 70, 10))
fig.tight_layout()
save(fig, f"{OUT}/power-cut-outcomes.svg")
