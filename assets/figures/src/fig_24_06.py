#!/usr/bin/env python3
"""Figures for chapter 24-06 (die-to-die links, memory PHYs and scale-up fabrics).

Run from anywhere:  python assets/figures/src/fig_24_06.py
Outputs
  assets/figures/24-06/wire-step.svg      receiver step response of Example 24-06.1's 2 mm wire (40-section RC ladder,
                                          exact eigen solution) for 50 and 25 ohm drivers, with the 32 GT/s UI marked
  assets/figures/24-06/energy-ladder.svg  energy per bit of link types against reach (log scale), from the chapter's table
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import d2d  # noqa: E402

OUT = "assets/figures/24-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def wire_step() -> None:
    t = np.linspace(0, 150e-12, 500)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for i, ron in enumerate((50, 25)):
        g, c = d2d.ladder(ron, 50, 200e-15, 50e-15)
        x = d2d.step_response(g, c, 0.5)
        t10, t90 = (d2d.crossing(x, 40, f * 0.5) for f in (0.1, 0.9))
        ax.plot(t * 1e12, [x(ti)[-1] for ti in t], color=PALETTE[i],
                label=f"{ron} Ω driver: 10–90% rise {(t90 - t10) * 1e12:.1f} ps")
    ax.axvline(31.25, color="0.5", ls=":", lw=1)
    ax.text(32.5, 0.05, "32 GT/s UI", fontsize=8, color="0.4")
    ax.set_xlabel("time after the driver's step (ps)")
    ax.set_ylabel("receiver voltage (V)")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, alpha=0.3)
    save(fig, f"{OUT}/wire-step.svg")


def energy_ladder() -> None:
    rows = [  # (label, reach in mm for plotting, low pJ/b, high pJ/b)
        ("UCIe-3D (target)", 0.01, 0.015, 0.05),
        ("UCIe-A (target)", 2, 0.25, 0.25),
        ("UCIe-S, BoW (targets)", 20, 0.25, 1.0),
        ("NVLink (2023 claim)", 500, 1.3, 1.3),
        ("Long-reach 224G SerDes", 1000, 2.0, 3.0),
    ]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for i, (lab, reach, lo, hi) in enumerate(rows):
        ax.plot([reach, reach], [lo, hi], color=PALETTE[i], lw=6, solid_capstyle="round")
        ax.plot(reach, np.sqrt(lo * hi), "o", color=PALETTE[i], label=lab)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("typical reach (mm, illustrative placement)")
    ax.set_ylabel("energy per bit (pJ/b)")
    ax.set_ylim(0.01, 5)
    ax.legend(fontsize=7, loc="upper left")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/energy-ladder.svg")


if __name__ == "__main__":
    wire_step()
    energy_ladder()
