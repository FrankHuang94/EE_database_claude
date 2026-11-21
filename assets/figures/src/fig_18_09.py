#!/usr/bin/env python3
"""Figures for chapter 18-09 (ultra-low-power design).

Run from anywhere:  python assets/figures/src/fig_18_09.py
Outputs
  assets/figures/18-09/duty-cycle.svg  average current of a node that spends 24 uC per wake-up (Example 18-09.1),
                                      against the wake-up period, for sleep currents of 0.5, 1.5 and 5 uA, with the
                                      battery life of a 220 mAh cell on the right axis; at short periods the wake-ups
                                      dominate, at long periods the sleep current sets a floor
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/18-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

T = np.logspace(-1, 3, 400)              # wake-up period, s
q_wake, t_wake = 24e-6, 5e-3             # charge and duration of each wake-up
fig, ax = plt.subplots(figsize=(7.4, 4.2))
for i, i_sleep in enumerate((0.5e-6, 1.5e-6, 5e-6)):
    i_avg = (q_wake + i_sleep * (T - t_wake)) / T
    ax.loglog(T, i_avg * 1e6, color=PALETTE[i], label=f"sleep {i_sleep * 1e6:g} µA")
    ax.axhline(i_sleep * 1e6, color=PALETTE[i], linestyle=":", linewidth=0.8)
ax.loglog(T, q_wake / T * 1e6, color="grey", linestyle="--", label="wake-ups alone (24 µC each)")
ax.set_xlabel("wake-up period T (s)")
ax.set_ylabel("average current (µA)")
sec = ax.secondary_yaxis("right", functions=(lambda i: 0.220 / np.maximum(i, 1e-9) * 1e6 / 24 / 365,
                                             lambda y: 0.220 / np.maximum(y, 1e-9) * 1e6 / 24 / 365))
sec.set_ylabel("life on 220 mAh (years)")
ax.set_title("Duty cycling: wake-ups dominate at short periods, sleep current at long ones", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/duty-cycle.svg")
