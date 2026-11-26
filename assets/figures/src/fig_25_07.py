#!/usr/bin/env python3
"""Figures for chapter 25-07 (packaging II: 2.5D, 3D, hybrid bonding and chiplets).

Run from anywhere:  python assets/figures/src/fig_25_07.py
Outputs
  assets/figures/25-07/chiplet-cost.svg        cost per good package against total logic area: one die against four
                                               chiplets (+10% interface area), D0 = 0.1 /cm2, Poisson and negative
                                               binomial (alpha = 2) yields, Example 25-07.9's costs
  assets/figures/25-07/interconnect-ladder.svg connection density 1/p^2 against pitch, with reported pitches from C4
                                               bumps to research wafer-to-wafer hybrid bonding (R-589 to R-593)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import chiplets as c  # noqa: E402

OUT = "assets/figures/25-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def chiplet_cost() -> None:
    areas = np.linspace(100, 1000, 181)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    for alpha, ls, tag in ((None, "-", "Poisson"), (2, "--", "clustered, α = 2")):
        mono = [c.good_package_cost([a], 0.1, 0.30, 3, 50, 0.99, alpha) for a in areas]
        chip = [c.good_package_cost([a / 4 * 1.1] * 4, 0.1, 0.30, 3, 110, 0.99, alpha) for a in areas]
        ax.plot(areas, mono, ls, color=PALETTE[0], label=f"monolithic ({tag})")
        ax.plot(areas, chip, ls, color=PALETTE[1], label=f"4 chiplets ({tag})")
    be = optimize.brentq(lambda a: c.good_package_cost([a], 0.1, 0.30, 3, 50, 0.99)
                         - c.good_package_cost([a / 4 * 1.1] * 4, 0.1, 0.30, 3, 110, 0.99), 100, 1000)
    ax.axvline(be, color="k", ls=":", lw=1)
    ax.text(be + 10, 80, f"Poisson break-even ≈ {be:.0f} mm²", fontsize=8)
    ax.axvline(858, color="0.6", lw=1)
    ax.text(845, 650, "reticle", fontsize=8, ha="right", color="0.4")
    ax.set_xlabel("total logic area (mm²)")
    ax.set_ylabel("cost per good package ($)")
    ax.set_ylim(0, 1000)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7.5, loc="upper left")
    save(fig, f"{OUT}/chiplet-cost.svg")


def ladder() -> None:
    pts = [  # (pitch in um, label, family index)
        (130, "C4 bump", 0), (50, "microbump 3D", 0),
        (55, "EMIB gen 1", 1), (45, "EMIB gen 2", 1), (35, "EMIB-T validated", 1), (25, "EMIB-T test", 1),
        (9, "SoIC / Foveros Direct", 2), (6, "SoIC 2025", 2), (4.5, "SoIC 2029 plan", 2),
        (2, "D2W research (imec)", 3), (1, "D2W research (CEA-Leti)", 3),
        (0.4, "W2W research (imec)", 3), (0.2, "W2W research (imec/EVG)", 3),
    ]
    p = np.logspace(np.log10(0.15), np.log10(200), 100)
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.loglog(p, 1e6 / p**2, color="0.6", lw=1, label="1/p²")
    names = ("bumps", "bridges", "hybrid bonding (products)", "hybrid bonding (research)")
    for k, name in enumerate(names):
        xs = [x for x, _, f in pts if f == k]
        ax.loglog(xs, [1e6 / x**2 for x in xs], "o", color=PALETTE[k], label=name)
    left = {"C4 bump": (-8, -3), "microbump 3D": (-8, 4), "EMIB gen 1": (-8, -10)}
    for x, lab, _ in pts:
        dx, dy = left.get(lab, (6, -6 if lab == "EMIB gen 2" else 2))
        ax.annotate(lab, (x, 1e6 / x**2), textcoords="offset points", xytext=(dx, dy), fontsize=6.5,
                    ha="right" if lab in left else "left")
    ax.invert_xaxis()
    ax.set_xlabel("pitch (µm)")
    ax.set_ylabel("connections per mm²")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=7.5, loc="upper left")
    save(fig, f"{OUT}/interconnect-ladder.svg")


if __name__ == "__main__":
    chiplet_cost()
    ladder()
