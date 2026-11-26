#!/usr/bin/env python3
"""Figures for chapter 25-08 (thermal engineering).

Run from anywhere:  python assets/figures/src/fig_25_08.py
Outputs
  assets/figures/25-08/spreading.svg        spreading resistance of a 3 mm copper lid (35 mm radius, isothermal base)
                                            against source radius: finite-volume solution, 45-degree estimate and the
                                            two one-dimensional limits
  assets/figures/25-08/coldplate-budget.svg junction temperature against power at 45 C inlet and 2 L/min for
                                            junction-to-coolant resistances of 0.025, 0.035 and 0.045 K/W
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import thermal as th  # noqa: E402

OUT = "assets/figures/25-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def spreading() -> None:
    b, t, k = 35e-3, 3e-3, 400
    a = np.linspace(3e-3, 30e-3, 19)
    fd = [th.spreader_fd(x, b, t, k, 280, 40) for x in a]
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.semilogy(a * 1e3, np.array(fd) * 1e3, "o-", color=PALETTE[0], ms=3, label="exact (finite volume)")
    ax.semilogy(a * 1e3, [th.r45_disk(x, t, k, b) * 1e3 for x in a], "--", color=PALETTE[1], label="45° estimate")
    ax.semilogy(a * 1e3, [t / (k * math.pi * x**2) * 1e3 for x in a], ":", color=PALETTE[2], label="1D through source")
    ax.axhline(t / (k * math.pi * b**2) * 1e3, color=PALETTE[3], ls="-.", lw=1, label="1D through whole lid")
    ax.set_xlabel("source (die) radius a (mm)")
    ax.set_ylabel("resistance (mK/W)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/spreading.svg")


def coldplate() -> None:
    p = np.linspace(500, 2600, 100)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for r, col in zip((0.025, 0.035, 0.045), PALETTE):
        ax.plot(p, [th.junction(x, 45, 2 / 6e4, r) for x in p], color=col, label=f"{r} K/W")
    ax.axhline(105, color="k", ls=":", lw=1)
    ax.text(520, 107, "105 °C limit", fontsize=8)
    ax.set_xlabel("GPU power (W)")
    ax.set_ylabel("junction temperature (°C)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, title="junction to coolant", title_fontsize=8)
    save(fig, f"{OUT}/coldplate-budget.svg")


if __name__ == "__main__":
    spreading()
    coldplate()
