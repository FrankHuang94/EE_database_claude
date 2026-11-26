#!/usr/bin/env python3
"""Figures for chapter 27-05 (the PC SoC).

Run from anywhere:  python assets/figures/src/fig_27_05.py
Outputs
  assets/figures/27-05/residency-turbo.svg  left: battery life against deep-idle residency for the laptop of
                                            Example 27-05.1 (8% active, the rest shallow or deep idle, 3.0 W
                                            platform, 70 Wh); right: package power and its exponentially
                                            weighted average during a 60 s task that turbos at 64 W until the
                                            average reaches the 28 W limit, for time constants of 28 s and 56 s
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "27-system-architectures" / "labs" / "27-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import pcsoc as pc  # noqa: E402

OUT = "assets/figures/27-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
deep = np.linspace(0.0, 0.92, 93)
life = [pc.battery_hours(70, pc.residency_power_w([(0.08, 5.0), (0.92 - d, 1.2), (d, 0.25)]) + 3.0) for d in deep]
ax1.plot(100 * deep, life, color=PALETTE[0])
ax1.plot([70], [pc.battery_hours(70, 0.839 + 3.0)], "o", color=PALETTE[1])
ax1.annotate("Example 27-05.1 (70%)", (70, pc.battery_hours(70, 3.839)), textcoords="offset points",
             xytext=(-120, 8), fontsize=8)
ax1.set_xlabel("deep-idle residency (%)")
ax1.set_ylabel("battery life (h)")
ax1.set_title("Video playback: deep idle sets battery life", fontsize=10)
ax1.grid(True, alpha=0.3)

dt = 0.01
t = np.arange(0, 60, dt)
for k, tau in enumerate((28.0, 56.0)):
    a = 1 - np.exp(-dt / tau)
    y, ys, ps = 5.0, [], []
    for _ in t:
        p = 64.0 if y < 28.0 else 28.0
        y = y + a * (p - y)
        ys.append(y)
        ps.append(p)
    ax2.plot(t, ps, color=PALETTE[2 * k], lw=1.0, ls="--", label=f"package power, τ = {tau:.0f} s")
    ax2.plot(t, ys, color=PALETTE[2 * k + 1], label=f"averaged power, τ = {tau:.0f} s")
ax2.axhline(28, color="k", lw=0.8)
ax2.set_xlabel("time (s)")
ax2.set_ylabel("power (W)")
ax2.set_ylim(0, 70)
ax2.set_title("Turbo under a 28 W averaged limit", fontsize=10)
ax2.legend(fontsize=7, loc="center right")
ax2.grid(True, alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/residency-turbo.svg")
