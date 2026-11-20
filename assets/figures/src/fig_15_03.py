#!/usr/bin/env python3
"""Figure for chapter 15-03 (time response and specifications).

Run from anywhere:  python assets/figures/src/fig_15_03.py
Outputs assets/figures/15-03/specs.svg: left, the s-plane region allowed by Example 15-03.3's specifications
(overshoot <= 10%, 2% settling <= 0.4 s by the 4/sigma rule) with the closed-loop poles of s^2 + 25 s + K as K
varies and the design point K = 434; right, standard second-order step responses for several damping ratios.
Uses labs/15-03-lab/specs.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "15-control-systems" / "labs" / "15-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
from specs import step_curve, zeta_from_overshoot  # noqa: E402

OUT = "assets/figures/15-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_specs():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.8))

    zmin = zeta_from_overshoot(0.10)
    th = math.acos(zmin)
    x = np.linspace(-40, 0, 2)
    ymax = 30.0
    # shaded permitted region: left of sigma = -10 and inside the wedge |Im| <= |Re| tan(theta)
    xs = np.linspace(-40, -10, 200)
    a1.fill_between(xs, -np.minimum(-xs * math.tan(th), ymax), np.minimum(-xs * math.tan(th), ymax),
                    color=PALETTE[0], alpha=0.12, lw=0, label="meets both specifications")
    a1.plot(x, -x * math.tan(th), color=PALETTE[0], lw=1)
    a1.plot(x, x * math.tan(th), color=PALETTE[0], lw=1)
    a1.text(-39, 26, f"ζ = {zmin:.3f}\n(10% overshoot)", fontsize=7, color=PALETTE[0], va="top")
    a1.axvline(-10, color=PALETTE[1], lw=1, ls="--")
    a1.text(-9.4, -27, "σ = 10 s⁻¹\n(tₛ ≈ 0.4 s)", fontsize=7, color=PALETTE[1])
    # root locus of s^2 + 25 s + K
    a1.plot([-25, 0], [0, 0], color=PALETTE[2], lw=2.2, label="poles of s² + 25s + K, K > 0")
    a1.plot([-12.5, -12.5], [-ymax, ymax], color=PALETTE[2], lw=2.2)
    a1.plot([0, -25], [0, 0], "x", color=PALETTE[2], ms=7, mew=1.5)
    wd = 12.5 / 0.6 * 0.8
    a1.plot([-12.5, -12.5], [wd, -wd], "o", color="black", ms=5)
    a1.annotate("K = 434\n−12.5 ± j16.7", (-12.5, wd), textcoords="offset points", xytext=(6, 2), fontsize=7)
    a1.axhline(0, color="gray", lw=0.5)
    a1.axvline(0, color="gray", lw=0.5)
    a1.set_xlim(-40, 5)
    a1.set_ylim(-ymax, ymax)
    a1.set_xlabel("Re s (1/s)")
    a1.set_ylabel("Im s (rad/s)")
    a1.set_title("Specifications as an s-plane region", fontsize=9)
    a1.legend(fontsize=7, loc="lower left")

    t = np.linspace(0, 16, 1601)
    for z, col in ((0.2, PALETTE[3]), (0.5, PALETTE[1]), (1 / math.sqrt(2), PALETTE[0]), (1.0, PALETTE[2])):
        a2.plot(t, step_curve([1], [1, 2 * z, 1], t), color=col, label=f"ζ = {z:.3g}")
    a2.axhspan(0.98, 1.02, color="gray", alpha=0.2, lw=0, label="±2% band")
    a2.set_xlabel("ωₙ t")
    a2.set_ylabel("y (unit step)")
    a2.set_title("Standard second-order step responses", fontsize=9)
    a2.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/specs.svg")


if __name__ == "__main__":
    fig_specs()
