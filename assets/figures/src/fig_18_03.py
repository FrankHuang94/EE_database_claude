#!/usr/bin/env python3
"""Figures for chapter 18-03 (interrupts, exceptions and timers).

Run from anywhere:  python assets/figures/src/fig_18_03.py
Outputs
  assets/figures/18-03/critical-instant.svg  the worst case for interrupt C of Example 18-03.3: a 8 µs critical section
                                            in main code, then A, B and C all requested at t = 0; drawn from the lab's
                                            discrete-event simulator (labs/18-03-lab/irqtime.py)
  assets/figures/18-03/pwm-modes.svg         edge-aligned and center-aligned PWM: counter, compare level and output, for
                                            the same counter clock, compare value and auto-reload
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs" / "18-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import irqtime as it  # noqa: E402

OUT = "assets/figures/18-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- critical instant
irqs = [it.Irq("A", 5, 50, 0), it.Irq("B", 10, 200, 1), it.Irq("C", 20, 1000, 2)]
trace = []
worst = it.simulate(irqs, 120, blocking_at=0.0, blocking_len=8.0, trace=trace)
fig, ax = plt.subplots(figsize=(8.6, 2.8))
rows = {"main (critical section)": 3, "A (highest)": 2, "B": 1, "C (lowest)": 0}
ax.broken_barh([(0, 8)], (3 - 0.35, 0.7), facecolors="gray", alpha=0.6)
col = {"A": PALETTE[0], "B": PALETTE[1], "C": PALETTE[2]}
lab = {"A": "A (highest)", "B": "B", "C": "C (lowest)"}
for name, a, b in trace:
    if a < 120:
        ax.broken_barh([(a, b - a)], (rows[lab[name]] - 0.35, 0.7), facecolors=col[name])
for t in (0, 50, 100):
    ax.annotate("", xy=(t, 2.45), xytext=(t, 2.9), arrowprops=dict(arrowstyle="->", color=PALETTE[0]))
ax.axvline(worst["C"], color=PALETTE[2], ls="--", lw=1)
ax.text(worst["C"] + 1, 0.4, f"C done at {worst['C']:.0f} µs", fontsize=8, color=PALETTE[2])
ax.set_yticks(list(rows.values()))
ax.set_yticklabels(list(rows))
ax.set_xlabel("time (µs); A, B and C all requested at t = 0, arrows mark A's requests")
ax.set_xlim(0, 120)
ax.set_title("The critical instant: blocking, then every higher-priority request at once")
fig.tight_layout()
save(fig, f"{OUT}/critical-instant.svg")

# ---------------------------------------------------------------- PWM modes
arr, ccr = 9, 6          # small numbers so the steps are visible
t = np.arange(0, 3 * (arr + 1))
edge = t % (arr + 1)
fig, axs = plt.subplots(2, 2, figsize=(8.6, 4.0), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
axs[0, 0].step(t, edge, where="post", color=PALETTE[0])
axs[0, 0].axhline(ccr, color=PALETTE[1], ls="--")
axs[0, 0].set_title(f"edge-aligned: period = ARR + 1 = {arr + 1} counts")
axs[1, 0].step(t, (edge < ccr).astype(int), where="post", color="black")
axs[1, 0].set_ylabel("output")
axs[0, 0].set_ylabel("counter")
period_c = 2 * arr
up_down = np.array([k % period_c if k % period_c <= arr else period_c - k % period_c for k in range(len(t))])
axs[0, 1].step(t, up_down, where="post", color=PALETTE[0])
axs[0, 1].axhline(ccr, color=PALETTE[1], ls="--")
axs[0, 1].set_title(f"center-aligned: period = 2 × ARR = {period_c} counts")
axs[1, 1].step(t, (up_down < ccr).astype(int), where="post", color="black")
for a in axs[1]:
    a.set_xlabel("timer clock ticks")
    a.set_yticks([0, 1])
fig.suptitle(f"PWM from one timer: compare value {ccr} (dashed), ARR = {arr}", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/pwm-modes.svg")
