#!/usr/bin/env python3
"""Figures for chapter 27-06 (automotive E/E architecture and ADAS compute).

Run from anywhere:  python assets/figures/src/fig_27_06.py
Outputs
  assets/figures/27-06/can-range.svg  left: worst-case response time of the lowest-priority message of
                                      Example 27-06.1 against bus load, as the bit rate is lowered from
                                      1000 to 125 kb/s; right: fraction of driving range lost to 100 W and
                                      500 W compute loads against speed (consumption rising linearly from
                                      140 Wh/km at 20 km/h to 190 Wh/km at 130 km/h, an assumed model)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "27-system-architectures" / "labs" / "27-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import automodel as am  # noqa: E402

OUT = "assets/figures/27-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

MSGS = [(8, 5), (8, 5), (8, 10), (8, 10), (8, 10), (4, 20), (8, 20), (8, 20), (2, 50), (8, 50),
        (8, 100), (8, 100)]
rates = np.linspace(1000, 125, 200)
loads = [100 * am.bus_load(MSGS, r) for r in rates]
resp = [am.can_response_time_ms(len(MSGS) - 1, MSGS, r) for r in rates]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
ax1.plot(loads, resp, color=PALETTE[0])
for r in (500, 250, 125):
    ax1.plot([100 * am.bus_load(MSGS, r)], [am.can_response_time_ms(len(MSGS) - 1, MSGS, r)], "o",
             color=PALETTE[1])
    ax1.annotate(f"{r} kb/s", (100 * am.bus_load(MSGS, r), am.can_response_time_ms(len(MSGS) - 1, MSGS, r)),
                 textcoords="offset points", xytext=(-55, 4), fontsize=8)
ax1.set_xlabel("bus load (%)")
ax1.set_ylabel("worst-case response, lowest priority (ms)")
ax1.set_title("CAN: delay explodes near full load", fontsize=10)
ax1.grid(True, alpha=0.3)

v = np.linspace(20, 130, 111)
e = 140 + (190 - 140) * (v - 20) / (130 - 20)
for k, pc in enumerate((100, 500)):
    ax2.plot(v, [100 * am.range_loss_fraction(pc, ei, vi) for ei, vi in zip(e, v)], color=PALETTE[k + 2],
             label=f"{pc} W compute")
ax2.set_xlabel("speed (km/h)")
ax2.set_ylabel("range lost (%)")
ax2.set_title("Compute costs most range in slow traffic", fontsize=10)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/can-range.svg")
