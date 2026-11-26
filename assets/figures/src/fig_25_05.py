#!/usr/bin/env python3
"""Figures for chapter 25-05 (foundries, PDKs and specialty processes).

Run from anywhere:  python assets/figures/src/fig_25_05.py
Outputs
  assets/figures/25-05/back-bias.svg          FD-SOI threshold shift against back-gate voltage (1.2 nm EOT, 7 nm body) for
                                              BOX thicknesses of 10, 20 and 25 nm (series-capacitor coupling)
  assets/figures/25-05/corner-histogram.svg   path-delay histogram from global (15 mV) and local (10 mV) threshold variation,
                                              with typical, slow and fast (+-45 mV threshold only) delays marked
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "25-fabrication-packaging-test-and-reliability" / "labs" / "25-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import foundry as f  # noqa: E402

OUT = "assets/figures/25-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def back_bias() -> None:
    vbg = np.linspace(-3, 3, 61)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for tb, col in zip((10, 20, 25), PALETTE):
        k = f.coupling_formula(1.2, 7, tb)
        ax.plot(vbg, -1000 * k * vbg, color=col, label=f"BOX {tb} nm ({1000*k:.0f} mV/V)")
    ax.axhline(0, color="0.7", lw=0.5)
    ax.axvline(0, color="0.7", lw=0.5)
    ax.set_xlabel("back-gate voltage (V): forward bias > 0 for NMOS")
    ax.set_ylabel("threshold shift (mV)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    save(fig, f"{OUT}/back-bias.svg")


def corner_histogram() -> None:
    dvt = f.simulate_vt(0.015, 0.010)
    d = f.delay(0.75, 0.30 + dvt) / f.delay(0.75, 0.30)
    ss, ff = f.corner_ratio(0.75, 0.30, 0.0, 0.045)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.hist(d, bins=120, color=PALETTE[0], alpha=0.8)
    for x, lab in ((1.0, "TT"), (ss, "SS"), (ff, "FF")):
        ax.axvline(x, color="k", ls=":", lw=1)
        ax.text(x, ax.get_ylim()[1] * 0.92, f" {lab}", fontsize=8)
    ax.set_xlabel("path delay relative to typical (threshold variation only)")
    ax.set_ylabel("paths")
    ax.grid(True, alpha=0.3)
    save(fig, f"{OUT}/corner-histogram.svg")


if __name__ == "__main__":
    back_bias()
    corner_histogram()
