#!/usr/bin/env python3
"""Figures for chapter 19-04 (transistor sizing and logical effort).

Run from anywhere:  python assets/figures/src/fig_19_04.py
Outputs
  assets/figures/19-04/stages.svg     delay of an optimally sized inverter chain against the number of stages for
                                      path efforts of 64 and 5000 (p_inv = 1), with the logical-effort optimum marked,
                                      and transistor-level simulations of one to four stages for H = 64 converted to
                                      units of tau = 17.43 ps
  assets/figures/19-04/topologies.svg minimum delay of three 8-input AND topologies (NAND8 + INV, NAND4 + NOR2, and a
                                      NAND2-NOR2-NAND2-INV tree) against the path's electrical effort H
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import effort as ef  # noqa: E402

OUT = "assets/figures/19-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
TAU = 0.6931471805599453 * 12.57e3 * 2e-15

# ---------------------------------------------------------------- figure 1: number of stages
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8))
for ax, f_path, color in ((axes[0], 64, PALETTE[0]), (axes[1], 5000, PALETTE[1])):
    ns = np.arange(1, 12)
    d = [ef.chain_delay(f_path, n) for n in ns]
    ax.plot(ns, d, "o-", color=color, label="logical effort")
    n_cont, n_best = ef.best_stage_count(f_path)
    ax.axvline(n_cont, color="0.6", ls=":", lw=1)
    ax.text(n_cont + 0.2, 45 if f_path == 64 else 2000, f"log$_{{3.59}}$F = {n_cont:.2f}", fontsize=8, color="0.4")
    ax.set_title(f"F = {f_path}", fontsize=10)
    ax.set_xlabel("number of stages N")
    if f_path == 64:
        ax.set_ylim(0, 70)
    else:
        ax.set_yscale("log")
axes[0].set_ylabel("path delay (τ)")
sims = [ef.simulate_chain(s, 128e-15) / TAU for s in ([1], [1, 8], [1, 4, 16], [1, 64 ** 0.25, 8, 64 ** 0.75])]
axes[0].plot([1, 2, 3, 4], sims, "s--", color=PALETTE[2], label="transistor level")
axes[0].legend(loc="upper right", bbox_to_anchor=(1.0, 0.85))
save(fig, f"{OUT}/stages.svg")

# ---------------------------------------------------------------- figure 2: topologies
h = np.logspace(0, 3, 300)
cases = [("NAND8 + INV", [10 / 3, 1], [8, 1]), ("NAND4 + NOR2", [2, 5 / 3], [4, 2]),
         ("NAND2-NOR2-NAND2-INV", [4 / 3, 5 / 3, 4 / 3, 1], [2, 2, 2, 1])]
fig, ax = plt.subplots(figsize=(6.4, 4.0))
for (name, gs, ps), color in zip(cases, PALETTE):
    ax.plot(h, [ef.min_path_delay(gs, ps, [1] * len(gs), x) for x in h], color=color, label=name)
ax.axvline(10, color="0.6", ls=":", lw=1)
ax.text(10.5, 75, "Example 6 (H = 10)", fontsize=8, color="0.4")
ax.set_xscale("log")
ax.set_xlabel("electrical effort H")
ax.set_ylabel("minimum path delay (τ)")
ax.legend(loc="upper left")
save(fig, f"{OUT}/topologies.svg")
