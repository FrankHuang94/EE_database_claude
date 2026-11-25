#!/usr/bin/env python3
"""Figures for chapter 24-09 (linear-drive and co-packaged optics).

Run from anywhere:  python assets/figures/src/fig_24_09.py
Outputs
  assets/figures/24-09/power-ladder.svg  watts per 800 Gb/s port (and pJ/bit) for retimed pluggables (16-18 W)
                                         and Broadcom's Humboldt, Bailly and Davisson CPO (6.4, 5.5, 3.5 W)
  assets/figures/24-09/zero-failure.svg  95% upper bound on failure rate (FIT) against zero-failure device-hours
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import cpo  # noqa: E402

OUT = "assets/figures/24-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def power_ladder() -> None:
    names = ["Pluggable\n(18 W)", "Pluggable\n(16 W)", "Humboldt\nCPO", "Bailly\nCPO", "Davisson\nCPO"]
    watts = [18, 16, 6.4, 5.5, 3.5]
    colors = [PALETTE[1], PALETTE[1], PALETTE[0], PALETTE[0], PALETTE[0]]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    bars = ax.bar(names, watts, color=colors)
    for b, w in zip(bars, watts):
        ax.text(b.get_x() + b.get_width() / 2, w + 0.3, f"{w:g} W\n{cpo.pj_per_bit(w, 800):.1f} pJ/b",
                ha="center", fontsize=7)
    ax.set_ylabel("watts per 800 Gb/s port")
    ax.set_ylim(0, 22)
    sec = ax.secondary_yaxis("right", functions=(lambda w: w / 0.8, lambda e: e * 0.8))
    sec.set_ylabel("pJ/bit")
    ax.grid(True, axis="y", alpha=0.3)
    save(fig, f"{OUT}/power-ladder.svg")


def zero_failure() -> None:
    hours = np.logspace(5, 8.5, 200)
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.loglog(hours, [cpo.fit_bound(h) for h in hours], color=PALETTE[0], label="0 failures")
    ax.loglog(hours, [cpo.fit_bound(h, 1) for h in hours], color=PALETTE[2], ls="--", label="1 failure")
    for h, lab in ((1e6, "1 M h"), (15e6, "15 M h"), (50e6, "50 M h")):
        ax.plot([h], [cpo.fit_bound(h)], "o", color=PALETTE[1])
        ax.annotate(f"{lab}: {cpo.fit_bound(h):.0f} FIT", (h, cpo.fit_bound(h)), textcoords="offset points",
                    xytext=(6, 6), fontsize=7)
    ax.axhline(100, color="0.6", ls=":", lw=1)
    ax.set_xlabel("device-hours tested")
    ax.set_ylabel("95% upper bound on failure rate (FIT)")
    ax.legend(fontsize=7)
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/zero-failure.svg")


if __name__ == "__main__":
    power_ladder()
    zero_failure()
