#!/usr/bin/env python3
"""Figures for chapter 28-05 (domain question banks II).

Run from anywhere:  python assets/figures/src/fig_28_05.py
Outputs
  assets/figures/28-05/backoff-and-battery.svg  left: ideal class-B and symmetric Doherty
                                                drain efficiency against output back-off,
                                                with published GaN Doherty results at 6 dB
                                                back-off [R-385]; right: battery life of
                                                Example 28-05.6's node on a 225 mAh CR2032
                                                against the MCU wake interval, for the
                                                CoreMark and while(1) current figures at
                                                25 C and the CoreMark figure at 85 C [R-310]
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import bankcheck as bc  # noqa: E402

OUT = "assets/figures/28-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
bo = np.linspace(0, 12, 481)
ax1.plot(bo, [100 * bc.eff_class_b(x) for x in bo], color=PALETTE[0], label="class B (ideal)")
ax1.plot(bo, [100 * bc.eff_doherty(x) for x in bo], color=PALETTE[1], label="symmetric Doherty (ideal)")
ax1.plot([6.02, 6.02], [38.5, 46.5], lw=7, color="0.35", solid_capstyle="butt",
         label="published GaN MMIC Doherty, 6 dB")
ax1.axvline(8, color="0.6", ls=":", lw=1)
ax1.text(8.2, 72, "8 dB PAPR:\n62.5% Doherty\n31.3% class B", fontsize=8, color="0.35")
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 85)
ax1.set_xlabel("output back-off from peak (dB)")
ax1.set_ylabel("drain efficiency (%)")
ax1.set_title("Peak efficiency is not average efficiency", fontsize=10)
ax1.legend(fontsize=8, loc="lower left")
ax1.grid(True, alpha=0.3)


def node(period, ua_per_mhz=101, sleep=2.21):
    ev = [(ua_per_mhz * 32, 0.002, period), (5100, 0.001, 10), (5300, 0.001, 10)]
    return bc.avg_current_ua(sleep, ev)


T = np.logspace(-1, 2, 200)
cases = [
    (dict(), "101 µA/MHz (CoreMark), 25 °C"),
    (dict(ua_per_mhz=55), "55 µA/MHz (while(1)), 25 °C"),
    (dict(sleep=4.71), "101 µA/MHz (CoreMark), 85 °C"),
]
for k, (kw, lab) in enumerate(cases):
    ax2.semilogx(T, [bc.battery_years(225, node(t, **kw)) for t in T], color=PALETTE[k + 2], label=lab)
ax2.axvline(1, color="0.6", ls=":", lw=1)
ax2.text(1.1, 0.5, "Example 28-05.6\n(1 s wake)", fontsize=8, color="0.35")
ax2.set_xlabel("MCU wake interval (s)")
ax2.set_ylabel("CR2032 life before derating (years)")
ax2.set_title("Battery life depends on code, duty cycle and temperature", fontsize=10)
ax2.legend(fontsize=8, loc="upper left")
ax2.grid(True, alpha=0.3, which="both")
fig.tight_layout()
save(fig, f"{OUT}/backoff-and-battery.svg")
