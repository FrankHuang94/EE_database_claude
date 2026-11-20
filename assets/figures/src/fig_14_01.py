#!/usr/bin/env python3
"""Figures for chapter 14-01 (performance, power and the iron law).

Run from anywhere:  python assets/figures/src/fig_14_01.py
Outputs SVGs to assets/figures/14-01/:
- amdahl.svg: left, Amdahl speedup against processor count for parallel fractions 0.5, 0.9, 0.95 and 0.99,
  with Gustafson's scaled speedup for a 10% serial fraction; right, energy per task against clock frequency
  for the core of Problem 14-01.11, split into dynamic and leakage parts.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/14-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_amdahl():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.0, 3.6))
    N = np.unique(np.round(np.logspace(0, np.log10(1024), 200)).astype(int))
    for k, p in enumerate((0.5, 0.9, 0.95, 0.99)):
        S = 1 / ((1 - p) + p / N)
        ax.plot(N, S, color=PALETTE[k], label=f"p = {p}")
        ax.axhline(1 / (1 - p), color=PALETTE[k], lw=0.6, ls=":")
    ax.plot(N, 0.1 + 0.9 * N, color="0.3", ls="--", lw=1.0, label="Gustafson, σ = 0.1")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xlabel("processors N")
    ax.set_ylabel("speedup")
    ax.set_title("Amdahl: the serial part sets the ceiling")
    ax.legend(fontsize=7, loc="upper left")
    f = np.linspace(0.2, 4.0, 400)
    V = 0.3 + 0.2 * f
    Ed = V**2
    El = 0.5 * V / f
    bx.plot(f, Ed, color=PALETTE[0], label="dynamic")
    bx.plot(f, El, color=PALETTE[1], label="leakage")
    bx.plot(f, Ed + El, color="0.15", label="total")
    i = int(np.argmin(Ed + El))
    bx.axvline(f[i], color="0.5", ls="--", lw=0.8)
    bx.set_xlabel("clock frequency (GHz)")
    bx.set_ylabel("energy per task (J)")
    bx.set_title("DVFS: an energy-optimal clock")
    bx.legend(fontsize=7)
    bx.set_ylim(0, 1.6)
    fig.tight_layout()
    save(fig, f"{OUT}/amdahl.svg")


if __name__ == "__main__":
    fig_amdahl()
