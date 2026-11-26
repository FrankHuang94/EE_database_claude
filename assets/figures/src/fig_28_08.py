#!/usr/bin/env python3
"""Figures for chapter 28-08 (post-acquisition integration risk).

Run from anywhere:  python assets/figures/src/fig_28_08.py
Outputs
  assets/figures/28-08/synergy-and-register.svg  left: present value of a $50M-a-year,
                                                 five-year synergy plan at 10% against
                                                 integration delay, for 60%, 80% and 100%
                                                 realization; right: expected loss by risk
                                                 for Example 28-08.6's register (assumed)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "28-technical-diligence-and-leadership-fluency" / "labs" / "28-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import integrate as ig  # noqa: E402

OUT = "assets/figures/28-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
d = np.linspace(0, 3, 121)
for k, rho in enumerate((1.0, 0.8, 0.6)):
    ax1.plot(d, [ig.synergy_value(50, 5, 0.10, delay=x, realization=rho) for x in d],
             color=PALETTE[k], label=f"{int(100 * rho)}% realized")
ax1.plot([1], [ig.synergy_value(50, 5, 0.10, 1, 0.8)], "o", color="0.2", ms=4)
ax1.annotate("1 year late, 80%:\n$138M (−27%)", (1, ig.synergy_value(50, 5, 0.10, 1, 0.8)),
             xytext=(1.55, 141), fontsize=8, arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
ax1.set_xlim(0, 3)
ax1.set_ylim(0, 200)
ax1.set_xlabel("integration delay (years)")
ax1.set_ylabel("present value of synergies ($M)")
ax1.set_title("Delay and partial realization compound", fontsize=10)
ax1.legend(fontsize=8, loc="lower left")
ax1.grid(True, alpha=0.3)

names = ["flow\nmigration", "key\narchitects", "program\nwrite-off", "license\ndispute", "customer\ndefection"]
risks = [(0.30, 40), (0.20, 60), (0.50, 10), (0.10, 150), (0.25, 20)]
el = [p * i for p, i in risks]
bars = ax2.bar(range(5), el, color=[PALETTE[3]] * 3 + [PALETTE[4]] + [PALETTE[3]], width=0.6)
for k, ((p, i), e) in enumerate(zip(risks, el)):
    ax2.text(k, e + 0.4, f"{int(100 * p)}% × {i}", ha="center", fontsize=8)
ax2.set_xticks(range(5))
ax2.set_xticklabels(names, fontsize=8)
ax2.set_ylim(0, 18)
ax2.set_ylabel("expected loss ($M)")
ax2.set_title("The unlikely risk carries the most expected loss", fontsize=10)
ax2.grid(True, axis="y", alpha=0.3)
fig.tight_layout()
save(fig, f"{OUT}/synergy-and-register.svg")
