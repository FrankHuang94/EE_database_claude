#!/usr/bin/env python3
"""Figures for chapter 19-12 (design for test).

Run from anywhere:  python assets/figures/src/fig_19_12.py
Outputs
  assets/figures/19-12/defect-level.svg     Williams-Brown defect level (DPPM, log scale) against fault coverage for
                                            yields of 50, 80 and 95 %
  assets/figures/19-12/random-coverage.svg  stuck-at fault coverage against the number of random patterns for a
                                            circuit whose hardest faults need 11 specific input values (p = 2^-11),
                                            averaged over 20 random seeds, with 1/p marked
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-12-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dft  # noqa: E402

OUT = "assets/figures/19-12"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- defect level
T = np.linspace(0.90, 0.99999, 400)
fig, ax = plt.subplots(figsize=(6.4, 4.0))
for k, y in enumerate((0.5, 0.8, 0.95)):
    ax.semilogy(100 * T, 1e6 * (1 - y ** (1 - T)), color=PALETTE[k], label=f"yield {100 * y:.0f} %")
ax.plot([99, 99.9], [1e6 * dft.defect_level(0.8, 0.99), 1e6 * dft.defect_level(0.8, 0.999)], "o", color=PALETTE[1])
ax.set_xlabel("fault coverage T (%)")
ax.set_ylabel("defect level (DPPM)")
ax.set_title("DL = 1 - Y^(1-T); dots: Example 19-12.1", fontsize=10)
ax.legend()
save(fig, f"{OUT}/defect-level.svg")

# ---------------------------------------------------------------- random-pattern coverage
names = [f"a{k}" for k in range(10)] + ["b0", "b1"]
wide = dft.Circuit(names, [("w", "AND", names[:10]), ("x", "XOR", ["b0", "b1"]), ("out", "OR", ["w", "x"])], ["out"])
n = 20000
curves = np.array([dft.random_coverage(wide, n, seed=s) for s in range(20)])
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.semilogx(np.arange(1, n + 1), 100 * curves.mean(axis=0), color=PALETTE[0], label="mean of 20 seeds")
ax.fill_between(np.arange(1, n + 1), 100 * curves.min(axis=0), 100 * curves.max(axis=0), color=PALETTE[0], alpha=0.2,
                label="range")
ax.axvline(2 ** 11, color=PALETTE[1], ls="--", label="1/p = 2048 for the hardest faults")
ax.set_xlabel("random patterns applied")
ax.set_ylabel("stuck-at fault coverage (%)")
ax.set_title("A 10-input AND behind an OR: 9 easy faults at once, 21 hard ones need thousands", fontsize=9)
ax.legend(fontsize=8, loc="lower right")
save(fig, f"{OUT}/random-coverage.svg")
