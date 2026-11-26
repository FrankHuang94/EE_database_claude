#!/usr/bin/env python3
"""Figures for chapter 26-01 (requirements, specifications and the design process).

Run from anywhere:  python assets/figures/src/fig_26_01.py
Outputs
  assets/figures/26-01/error-budget.svg          Monte Carlo of Example 26-01.3's six-term budget (Gaussian,
                                                 3-sigma bounds 0.40/0.35/0.30/0.25/0.20/0.30 %), independent and
                                                 with reference and drift correlated, with the +/-1.0 % limits,
                                                 the RSS 3-sigma band (0.752 %) and the worst case (1.80 %)
  assets/figures/26-01/decision-sensitivity.svg  Example 26-01.6's weighted scores against the capability weight,
                                                 others rescaled in proportion; ties at 0.423 (A-B) and 0.500 (B-C)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "26-engineering-design-and-professional-practice" / "labs" / "26-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import reqs as r  # noqa: E402

OUT = "assets/figures/26-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def error_budget() -> None:
    b = [0.40, 0.35, 0.30, 0.25, 0.20, 0.30]
    ind = r.mc_budget(b, n=1_000_000)
    cor = r.mc_budget(b, n=1_000_000, groups=[[0, 5]])
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    bins = np.linspace(-1.9, 1.9, 191)
    ax.hist(ind, bins=bins, density=True, histtype="step", lw=1.4, color=PALETTE[0], label="independent")
    ax.hist(cor, bins=bins, density=True, histtype="step", lw=1.4, color=PALETTE[1],
            label="reference and drift correlated")
    for s in (-1, 1):
        ax.axvline(s * 1.0, color="k", lw=1.2, label="limit ±1.0%" if s > 0 else None)
        ax.axvline(s * r.stack_rss(b), color=PALETTE[0], lw=1, ls="--",
                   label="RSS 3σ ±0.752%" if s > 0 else None)
        ax.axvline(s * r.stack_worst(b), color="0.5", lw=1, ls=":", label="worst case ±1.80%" if s > 0 else None)
    ax.set_xlabel("total error (% of full scale)")
    ax.set_ylabel("probability density")
    ax.set_title("Error budget: worst case, RSS and a hidden correlation")
    ax.legend(loc="upper left", fontsize=7, framealpha=1.0)
    save(fig, f"{OUT}/error-budget.svg")


def decision_sensitivity() -> None:
    S = np.array([[5, 2, 5, 5], [4, 4, 3, 3], [3, 5, 2, 2]], dtype=float)
    w = [0.40, 0.25, 0.20, 0.15]
    ws = np.linspace(0, 1, 201)
    sc = r.scores_vs_weight(w, S, 1, ws)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for k, name in enumerate(["A · MCU", "B · MCU + DSP", "C · MCU + NPU"]):
        ax.plot(ws, sc[:, k], color=PALETTE[k], label=name)
    ax.axvline(0.25, color="0.5", ls=":", lw=1)
    ax.text(0.255, 2.15, "base weight 0.25", fontsize=8, color="0.4")
    for (a, bb), off in (((0, 1), (-62, 8)), ((1, 2), (8, -16))):
        wt = r.flip_weight(w, S, 1, a, bb)
        yt = r.scores_vs_weight(w, S, 1, np.array([wt]))[0][a]
        ax.plot([wt], [yt], "ko", ms=4)
        ax.annotate(f"tie {wt:.3f}", (wt, yt), textcoords="offset points", xytext=off, fontsize=8)
    ax.set_xlabel("weight on capability (others rescaled in proportion)")
    ax.set_ylabel("weighted score")
    ax.set_title("Which architecture wins depends on one weight")
    ax.legend(loc="upper right", fontsize=8)
    save(fig, f"{OUT}/decision-sensitivity.svg")


if __name__ == "__main__":
    error_budget()
    decision_sensitivity()
