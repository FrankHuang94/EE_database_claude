#!/usr/bin/env python3
"""Figures for chapter 27-03 (the smartwatch).

Run from anywhere:  python assets/figures/src/fig_27_03.py
Outputs
  assets/figures/27-03/watch-budget-ble.svg  left: daily rail energy of Example 27-03.1 by item (assumed
                                             parameters); right: average current of the BLE link of
                                             Example 27-03.4 against connection interval, with the
                                             interval-independent floor (sleep plus window widening)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "27-system-architectures" / "labs" / "27-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import watchmodel as wm  # noqa: E402

OUT = "assets/figures/27-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

t_aod = 18 - 1 - 300 * 4 / 3600 - 90 * 6 / 3600 - 0.25
items = [("Workout (1 h)", 150, 1.0), ("Floor (24 h)", 6, 24), ("App use (15 min)", 500, 0.25),
         ("Always-on display", 7, t_aod), ("Time checks (300)", 250, 300 * 4 / 3600),
         ("Notifications (90)", 300, 90 * 6 / 3600), ("Heart rate (18 h)", 2, 18),
         ("Sleep tracking (6 h)", 3, 6)]
names = [n for n, _, _ in items]
energy = np.array([p * h for _, p, h in items])
total = energy.sum()

t_e = wm.ble_airtime_us(0, 1)
q = wm.ble_event_charge_uc(1.2, 250, 3.6, t_e, 150, 4.1, t_e)
floor_ua = 1.5 + 1e3 * 3.6 * 100e-6
T = np.logspace(np.log10(0.0075), np.log10(20), 300)
I = np.array([wm.ble_avg_current_ua(q, t, 1.5, 3.6, 100) for t in T])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
y = np.arange(len(names))[::-1]
ax1.barh(y, energy, color=PALETTE[0])
for yi, e in zip(y, energy):
    ax1.text(e + 3, yi, f"{e:.0f} ({100 * e / total:.1f}%)", va="center", fontsize=8)
ax1.set_yticks(y)
ax1.set_yticklabels(names, fontsize=8)
ax1.set_xlabel("rail energy per day (mWh)")
ax1.set_xlim(0, 200)
ax1.set_title(f"Example 27-03.1: {total:.1f} mWh per day", fontsize=10)

ax2.loglog(T, I, color=PALETTE[1], label="average current")
ax2.axhline(floor_ua, ls="--", color=PALETTE[2], label=f"sleep + widening = {floor_ua:.2f} µA")
for t_mark in (0.03, 0.1, 1.0):
    i_mark = wm.ble_avg_current_ua(q, t_mark, 1.5, 3.6, 100)
    ax2.plot([t_mark], [i_mark], "o", color=PALETTE[1])
    ax2.annotate(f"{1e3 * t_mark:.0f} ms: {i_mark:.1f} µA", (t_mark, i_mark), textcoords="offset points",
                 xytext=(6, 4), fontsize=8)
ax2.set_xlabel("connection interval (s)")
ax2.set_ylabel("average current (µA)")
ax2.set_title("Example 27-03.4: idle BLE link", fontsize=10)
ax2.legend(fontsize=8, loc="upper right")
ax2.grid(True, which="both", alpha=0.3)

fig.tight_layout()
save(fig, f"{OUT}/watch-budget-ble.svg")
