#!/usr/bin/env python3
"""Figures for chapter 28-09 (the business <-> engineering translation table).

Run from anywhere:  python assets/figures/src/fig_28_09.py
Outputs
  assets/figures/28-09/die-cost-and-tornado.svg  left: cost per good die on an $18,500
                                                 300 mm wafer [R-575] against die area with
                                                 0.1 defects per cm^2 (assumed), and the
                                                 elasticity of cost to area; right: tornado of
                                                 gross-margin change for +/-10% in each driver
                                                 for a 100 mm^2 die selling at $90 (assumed)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import translate as tr  # noqa: E402

OUT = "assets/figures/28-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
A = np.linspace(20, 800, 300)
ax1.plot(A, [tr.die_cost(a, 18500, whole=False) for a in A], color=PALETTE[0], label="cost per good die")
ax1.set_xlabel("die area (mm²)")
ax1.set_ylabel("cost per good die ($)", color=PALETTE[0])
ax1.set_xlim(0, 800)
ax1.set_ylim(0, 1000)
ax1.grid(True, alpha=0.3)
ax1b = ax1.twinx()
ax1b.plot(A, [tr.elasticity(a) for a in A], color=PALETTE[1], ls="--", label="elasticity")
ax1b.set_ylabel("elasticity d ln C / d ln A (dashed)", color=PALETTE[1])
ax1b.set_ylim(0.8, 2.4)
ax1.set_title("Die cost grows faster than area", fontsize=10)

base = dict(asp=90, area=100, wafer=18500, d0=0.001, pkg=8)
labels = {"asp": "selling price", "area": "die area", "wafer": "wafer price", "pkg": "package and test",
          "d0": "defect density"}
_, up = tr.tornado(base, 0.10)
_, dn = tr.tornado(base, -0.10)
order = sorted(up, key=lambda k: max(abs(up[k]), abs(dn[k])))
y = np.arange(len(order))
ax2.barh(y, [up[k] for k in order], color=PALETTE[2], height=0.6, label="+10%")
ax2.barh(y, [dn[k] for k in order], color=PALETTE[3], height=0.6, label="−10%")
ax2.set_yticks(y)
ax2.set_yticklabels([labels[k] for k in order], fontsize=8)
ax2.axvline(0, color="0.3", lw=0.8)
ax2.set_xlabel("change in gross margin (percentage points)")
ax2.set_title("Which knob moves margin (base 55.6%)", fontsize=10)
ax2.legend(fontsize=8, loc="lower right")
ax2.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/die-cost-and-tornado.svg")
