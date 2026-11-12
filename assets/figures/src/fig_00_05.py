#!/usr/bin/env python3
"""Figures for chapter 00-05: schedule-risk distribution for a three-phase chip project.

Run:  python assets/figures/src/fig_00_05.py  -> assets/figures/00-05/schedule-risk.svg
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
PHASES = [(20, 26, 40), (10, 12, 20), (12, 14, 20)]  # (min, most likely, max) weeks


def fig_schedule():
    rng = np.random.default_rng(3)
    total = sum(rng.triangular(a, m, b, 400_000) for a, m, b in PHASES)
    mode_sum = sum(m for _, m, _ in PHASES)
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.hist(total, bins=120, density=True, color=PALETTE[0], alpha=0.75)
    for xv, lab, col in [(mode_sum, f"sum of most-likely\n= {mode_sum} weeks", PALETTE[1]),
                         (total.mean(), f"mean = {total.mean():.1f} weeks", PALETTE[2]),
                         (np.quantile(total, 0.8), f"80th percentile\n= {np.quantile(total, 0.8):.1f} weeks", PALETTE[3])]:
        ax.axvline(xv, color=col, lw=2)
        ax.text(xv + 0.4, ax.get_ylim()[1] * 0.85, lab, color=col, fontsize=8, va="top")
    ax.set_xlabel("total project duration (weeks)")
    ax.set_ylabel("probability density")
    ax.set_title("Why chip schedules slip: right-skewed task durations add up\n"
                 "(verification, physical design and fab, each triangular)")
    save(fig, "assets/figures/00-05/schedule-risk.svg")


if __name__ == "__main__":
    fig_schedule()
    print("00-05 figures written")
