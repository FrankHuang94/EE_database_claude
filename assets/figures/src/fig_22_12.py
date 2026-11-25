#!/usr/bin/env python3
"""Figures for chapter 22-12 (power systems fundamentals).

Run from anywhere:  python assets/figures/src/fig_22_12.py
Outputs
  assets/figures/22-12/frequency-response.svg  frequency deviation after losing 1.8 GW from 50 GW of synchronous
                                               generation with H = 4 s and H = 2 s (5% droop, 5 s governor lag,
                                               1000 MW/Hz load damping), with the initial RoCoF tangents
  assets/figures/22-12/power-angle.svg         Example 22-12.4's real power and the reactive power at both ends
                                               against the angle between the buses
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-12-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import grid  # noqa: E402

OUT = "assets/figures/22-12"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_frequency():
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for h, col in ((4, PALETTE[0]), (2, PALETTE[1])):
        t, df = grid.frequency_response(1800, h, 50e3, t_end=30, n=3001)
        ax.plot(t, 60 + df, color=col, label=f"H = {h} s")
        tt = np.linspace(0, 1.0, 10)
        ax.plot(tt, 60 - grid.rocof(1800, h, 50e3) * tt, color=col, ls=":", lw=1)
    ax.axhline(60 + grid.droop_df(1800, [(50e3, 0.05)], d_load=1000.0), color="0.5", ls="--", lw=1)
    ax.text(18, 59.91, "droop settling", fontsize=8)
    ax.set_xlabel("time after losing 1.8 GW (s)")
    ax.set_ylabel("frequency (Hz)")
    ax.legend(fontsize=8)
    ax.set_title("Less inertia: faster fall, deeper nadir, same final value", fontsize=10)
    save(fig, f"{OUT}/frequency-response.svg")


def fig_power_angle():
    d = np.linspace(0, 120, 500)
    vals = np.array([grid.two_bus(1.0, 0.98, 0.1, x) for x in d])
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.plot(d, vals[:, 0], color=PALETTE[0], label="P (pu)")
    ax.plot(d, vals[:, 1], color=PALETTE[1], label="Q leaving bus 1 (pu)")
    ax.plot(d, vals[:, 2], color=PALETTE[2], label="Q arriving at bus 2 (pu)")
    ax.axvline(10, color="0.5", ls=":")
    ax.text(12, -3.0, "Example 22-12.4: 10°", fontsize=8)
    ax.axvline(90, color="0.5", ls=":")
    ax.text(70, -7.5, "stability limit 90°", fontsize=8)
    ax.set_xlabel("angle δ between the buses (°)")
    ax.set_ylabel("per unit on 100 MVA")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Angle drives real power; the line consumes reactive power", fontsize=10)
    save(fig, f"{OUT}/power-angle.svg")


if __name__ == "__main__":
    fig_frequency()
    fig_power_angle()
