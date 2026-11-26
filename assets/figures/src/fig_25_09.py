#!/usr/bin/env python3
"""Figures for chapter 25-09 (reliability physics).

Run from anywhere:  python assets/figures/src/fig_25_09.py
Outputs
  assets/figures/25-09/tddb-models.svg  E, 1/E and power-law breakdown models fitted through 10 s at 10 MV/cm and
                                        100 s at 9 MV/cm (Example 25-09.4), extrapolated down to 2.5 MV/cm
  assets/figures/25-09/em-exponent.svg  local current exponent (2 + x)/(1 + x) of the two-phase electromigration
                                        model against j/j*
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import reliability as r  # noqa: E402

OUT = "assets/figures/25-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def tddb() -> None:
    f = r.tddb_fit(10, 10, 9, 100)
    e = np.linspace(2.5, 10.5, 200)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    for name, col, lab in (("E", PALETTE[0], "E model"), ("power", PALETTE[1], "power law"),
                           ("1/E", PALETTE[2], "1/E model")):
        ax.semilogy(e, [f[name](x) for x in e], color=col, label=lab)
    ax.semilogy([10, 9], [10, 100], "ko", ms=4, label="stress data")
    ax.axhline(10 * 3.15576e7, color="0.5", ls=":", lw=1)
    ax.text(2.6, 10 * 3.15576e7 * 2, "10 years", fontsize=8, color="0.3")
    ax.set_xlabel("oxide field (MV/cm)")
    ax.set_ylabel("characteristic breakdown life (s)")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/tddb-models.svg")


def em_exponent() -> None:
    x = np.logspace(-2, 2, 200)
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.semilogx(x, [r.local_exponent(v) for v in x], color=PALETTE[0])
    ax.axhline(2, color="0.6", ls=":", lw=1)
    ax.axhline(1, color="0.6", ls=":", lw=1)
    ax.text(0.012, 1.93, "nucleation-limited", fontsize=8)
    ax.text(12, 1.05, "growth-limited", fontsize=8)
    ax.set_xlabel("current density j / j*")
    ax.set_ylabel("local exponent n")
    ax.set_ylim(0.9, 2.1)
    ax.grid(True, which="both", alpha=0.25)
    save(fig, f"{OUT}/em-exponent.svg")


if __name__ == "__main__":
    tddb()
    em_exponent()
