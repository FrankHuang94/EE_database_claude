#!/usr/bin/env python3
"""Figures for chapter 25-06 (packaging I: wire bond, flip-chip, substrates, SiP and PoP).

Run from anywhere:  python assets/figures/src/fig_25_06.py
Outputs
  assets/figures/25-06/joint-strain-map.svg   shear strain of each joint on a 20 mm die, 150 um bump grid, 13.4 ppm/K
                                              mismatch, 100 K cycle, 70 um joint height (Example 25-06.4)
  assets/figures/25-06/io-scaling.svg         perimeter (60 um pitch) and area-array (150 um pitch) I/O against die size,
                                              with the 1.5 mm crossover marked (Example 25-06.1)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import package as pk  # noqa: E402

OUT = "assets/figures/25-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def strain_map() -> None:
    xy = pk.bump_grid(20, 0.15)
    r = np.hypot(xy[:, 0], xy[:, 1])
    g = pk.shear_strain(13.4, 100, r, 0.070)
    n = int(round(len(g) ** 0.5))
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ext = (xy[:, 0].min(), xy[:, 0].max(), xy[:, 1].min(), xy[:, 1].max())
    im = ax.imshow(g.reshape(n, n), origin="lower", extent=ext, cmap="viridis")
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("joint shear strain (dimensionless)")
    ax.set_xlabel("x from die centre (mm)")
    ax.set_ylabel("y from die centre (mm)")
    ax.set_title("20 mm die, 100 K cycle, 70 µm joints", fontsize=9)
    ax.grid(False)
    save(fig, f"{OUT}/joint-strain-map.svg")


def io_scaling() -> None:
    d = np.logspace(-0.5, 1.5, 200)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.loglog(d, pk.io_perimeter(d, 0.060), color=PALETTE[0], label="perimeter, 60 µm pitch: 4D/p")
    ax.loglog(d, pk.io_area(d, 0.150), color=PALETTE[1], label="area array, 150 µm pitch: (D/p)²")
    dc = pk.crossover(0.150, 0.060)
    ax.axvline(dc, color="k", ls=":", lw=1)
    ax.text(dc * 1.08, 3, f"crossover {dc:.1f} mm", fontsize=8)
    ax.set_xlabel("die edge D (mm)")
    ax.set_ylabel("I/O count")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/io-scaling.svg")


if __name__ == "__main__":
    strain_map()
    io_scaling()
