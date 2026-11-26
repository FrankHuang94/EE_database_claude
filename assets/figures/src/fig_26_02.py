#!/usr/bin/env python3
"""Figures for chapter 26-02 (design reviews, documentation and standards bodies).

Run from anywhere:  python assets/figures/src/fig_26_02.py
Outputs
  assets/figures/26-02/reviewers.svg  left: fraction of defects found against the number of reviewers for
                                      independent reviewers (p = 0.35) and for reviewers sharing a 30 % blind
                                      spot (p = 0.5 on the rest); right: Example 26-02.2's expected total cost
                                      (20 defects, $10k per reviewer, $10k per escape), minimum at 5 reviewers
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "26-engineering-design-and-professional-practice" / "labs" / "26-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import reviews as r  # noqa: E402

OUT = "assets/figures/26-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def reviewers() -> None:
    ks = np.arange(1, 11)
    ind = [100 * r.p_found(0.35, k) for k in ks]
    mix = [100 * r.p_found_mix([(0.7, 0.5), (0.3, 0.0)], k) for k in ks]
    cost = [r.review_cost(k, 20, 0.35, 1e4, 1e4) / 1e3 for k in ks]
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.6))
    ax[0].plot(ks, ind, marker="o", color=PALETTE[0], label="independent, p = 0.35")
    ax[0].plot(ks, mix, marker="s", color=PALETTE[1], label="30% blind spot, p = 0.5 on the rest")
    ax[0].axhline(70, color="0.5", ls=":", lw=1)
    ax[0].text(6.2, 66, "ceiling 70%", fontsize=8, color="0.4")
    ax[0].set_xlabel("number of reviewers")
    ax[0].set_ylabel("defects found (%)")
    ax[0].set_ylim(30, 102)
    ax[0].legend(fontsize=8, loc="lower right")
    ax[0].set_title("More reviewers, or different ones?")
    ax[1].plot(ks, cost, marker="o", color=PALETTE[2])
    kmin = int(np.argmin(cost)) + 1
    ax[1].plot([kmin], [min(cost)], "ko", ms=5)
    ax[1].annotate(f"minimum at {kmin} (${min(cost):.1f}k)", (kmin, min(cost)), textcoords="offset points",
                   xytext=(-30, 32), fontsize=8,
                   arrowprops={"arrowstyle": "-", "color": "0.5", "lw": 0.8})
    ax[1].set_xlabel("number of reviewers")
    ax[1].set_ylabel("expected total cost ($ thousand)")
    ax[1].set_title("Example 26-02.2: a flat optimum")
    fig.tight_layout()
    save(fig, f"{OUT}/reviewers.svg")


if __name__ == "__main__":
    reviewers()
