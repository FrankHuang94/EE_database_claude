#!/usr/bin/env python3
"""Figures for chapter 25-11 (test: ATE, wafer sort, burn-in and binning).

Run from anywhere:  python assets/figures/src/fig_25_11.py
Outputs
  assets/figures/25-11/guard-band.svg  escapes and overkill (ppm) against guard band for Fmax ~ N(3.0, 0.15) GHz,
                                       a 3.0 GHz limit and 20 MHz tester error (Example 25-11.6)
  assets/figures/25-11/burn-in.svg     cumulative failures of a weak subpopulation (scale 100 h) against
                                       use-equivalent hours for Weibull shapes 0.3, 0.5 and 0.8, with 1,200 h marked
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-11-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import testcost as t  # noqa: E402

OUT = "assets/figures/25-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def guard() -> None:
    g = np.linspace(0, 0.08, 60)
    eo = [t.escapes_overkill(3.0, x, 3.0, 0.15, 0.02) for x in g]
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.semilogy(1000 * g, [1e6 * e for e, _ in eo], color=PALETTE[0], label="escapes (bad parts shipped)")
    ax.semilogy(1000 * g, [1e6 * o for _, o in eo], color=PALETTE[1], label="overkill (good parts rejected)")
    ax.axhline(100, color="0.6", ls=":", lw=1)
    ax.set_xlabel("guard band (MHz)")
    ax.set_ylabel("parts per million")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/guard-band.svg")


def burn() -> None:
    h = np.logspace(0, 5, 200)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for b, col in zip((0.3, 0.5, 0.8), PALETTE):
        ax.semilogx(h, [t.weak_fail(x, 100, b) for x in h], color=col, label=f"Weibull shape {b}")
    ax.axvline(1200, color="k", ls=":", lw=1)
    ax.text(1300, 0.05, "24 h at AF 50", fontsize=8)
    ax.set_xlabel("use-equivalent hours")
    ax.set_ylabel("fraction of weak parts failed")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/burn-in.svg")


if __name__ == "__main__":
    guard()
    burn()
