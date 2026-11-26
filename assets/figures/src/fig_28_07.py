#!/usr/bin/env python3
"""Figures for chapter 28-07 (evaluating engineering teams).

Run from anywhere:  python assets/figures/src/fig_28_07.py
Outputs
  assets/figures/28-07/shrinkage-and-bench.svg  left: posterior mean and 90% credible band of
                                                a team's first-silicon success rate against
                                                the number of projects in its record, from a
                                                Beta prior with mean 14% [R-621] and weight 10,
                                                for a team that always succeeds and one that
                                                succeeds half the time; right: probability of
                                                losing a capability against years for one, two
                                                and three owners at 12% a year (assumed)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import teameval as te  # noqa: E402

OUT = "assets/figures/28-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
A0, B0 = te.prior_params(0.14, 10)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
n = np.arange(0, 21)
for k, (frac, lab) in enumerate(((1.0, "succeeds on every project"), (0.5, "succeeds on half"))):
    s = frac * n  # half-success record treated as its expected count (Beta allows fractions)
    m = np.array([te.posterior_mean(A0, B0, si, ni) for si, ni in zip(s, n)])
    lo, hi = map(np.array, zip(*[te.credible_interval(A0, B0, si, ni) for si, ni in zip(s, n)]))
    ax1.plot(n, 100 * m, color=PALETTE[k], label=lab)
    ax1.fill_between(n, 100 * lo, 100 * hi, color=PALETTE[k], alpha=0.15)
ax1.axhline(14, color="0.5", ls=":", lw=1)
ax1.text(14.5, 16, "prior mean 14%", fontsize=8, color="0.4")
ax1.plot([5], [100 * te.posterior_mean(A0, B0, 4, 5)], "o", color="0.2", ms=4)
ax1.annotate("4 of 5: 36%", (5, 36), xytext=(7, 22), fontsize=8,
             arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax1.set_xlim(0, 20)
ax1.set_xticks(range(0, 21, 4))
ax1.set_ylim(0, 100)
ax1.set_xlabel("projects in the team's record")
ax1.set_ylabel("estimated first-silicon success (%)")
ax1.set_title("Short records move estimates a little", fontsize=10)
ax1.legend(fontsize=8, loc="upper left")
ax1.grid(True, alpha=0.3)

yrs = np.linspace(0, 5, 201)
for k in (1, 2, 3):
    ax2.plot(yrs, [100 * te.capability_loss(te.horizon_rate(0.12, y), k) for y in yrs],
             color=PALETTE[k + 1], label=f"{k} owner{'s' if k > 1 else ''}")
ax2.axvline(2, color="0.6", ls=":", lw=1)
ax2.text(2.1, 52, "two-year\nintegration", fontsize=8, color="0.4")
ax2.set_xlim(0, 5)
ax2.set_ylim(0, 100)
ax2.set_xlabel("years")
ax2.set_ylabel("probability of losing the capability (%)")
ax2.set_title("Bench depth at 12% annual departures", fontsize=10)
ax2.legend(fontsize=8, loc="upper left")
ax2.grid(True, alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/shrinkage-and-bench.svg")
