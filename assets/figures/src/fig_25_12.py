#!/usr/bin/env python3
"""Figures for chapter 25-12 (post-silicon validation and bring-up).

Run from anywhere:  python assets/figures/src/fig_25_12.py
Outputs
  assets/figures/25-12/shmoo.svg          synthetic shmoo (pass/fail over 0.55-0.95 V and 1.5-4.5 GHz) from the
                                          alpha-power model fitted to 3.0 GHz at 0.75 V, 30 MHz noise, with boundary
  assets/figures/25-12/bug-discovery.svg  Goel-Okumoto curve a = 120, b = ln2/4 per week with the two data points
                                          of Example 25-12.3 (60 at week 4, 90 at week 8)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-12-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import postsi as p  # noqa: E402

OUT = "assets/figures/25-12"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def shmoo() -> None:
    k = p.fit_k(3.0, 0.75)
    volts = np.linspace(0.55, 0.95, 33)
    freqs = np.linspace(1.5, 4.5, 41)
    grid = p.shmoo(k, volts, freqs)
    vv, ff = np.meshgrid(volts, freqs)
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.scatter(vv[grid], ff[grid], s=7, marker="s", color=PALETTE[2], label="pass")
    ax.scatter(vv[~grid], ff[~grid], s=7, marker="s", color="0.75", label="fail")
    vf = np.linspace(0.55, 0.95, 200)
    ax.plot(vf, [p.fmax(x, k) for x in vf], color="k", lw=1.2, label="alpha-power boundary")
    ax.plot([0.681], [2.5], "o", color=PALETTE[1], ms=6, label="spec point (2.5 GHz, 0.681 V)")
    ax.set_xlabel("supply voltage (V)")
    ax.set_ylabel("frequency (GHz)")
    ax.legend(fontsize=7.5, loc="upper left")
    save(fig, f"{OUT}/shmoo.svg")


def bugs() -> None:
    b = math.log(2) / 4
    t = np.linspace(0, 30, 200)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.plot(t, 120 * (1 - np.exp(-b * t)), color=PALETTE[0], label="Goel–Okumoto fit")
    ax.plot([4, 8], [60, 90], "o", color=PALETTE[1], label="bug counts")
    ax.axhline(120, color="0.6", ls=":", lw=1)
    ax.text(0.5, 123, "expected total 120", fontsize=8)
    ax.set_xlabel("weeks of validation")
    ax.set_ylabel("cumulative bugs found")
    ax.set_ylim(0, 135)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="lower right")
    save(fig, f"{OUT}/bug-discovery.svg")


if __name__ == "__main__":
    shmoo()
    bugs()
