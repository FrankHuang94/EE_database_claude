#!/usr/bin/env python3
"""Figure for chapter 15-06 (root locus).

Run from anywhere:  python assets/figures/src/fig_15_06.py
Outputs assets/figures/15-06/loci.svg: the root loci of Example 15-06.2 (three poles), Example 15-06.3 (the same
with a zero at -1) and Example 15-06.6 (the PD servo, a circle), each with its zeta ray and design point.
Uses labs/15-06-lab/rlocus.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "15-control-systems" / "labs" / "15-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
from rlocus import locus  # noqa: E402

OUT = "assets/figures/15-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def panel(ax, N, D, Kmax, zeta, design, title, xlim, ylim):
    Ks = np.concatenate([np.linspace(0, 1, 400), np.logspace(0, math.log10(Kmax), 20000)])
    R = locus(N, D, Ks)
    for b in range(R.shape[1]):
        ax.plot(R[:, b].real, R[:, b].imag, color=PALETTE[0], lw=1.6)
    poles = np.roots(D)
    ax.plot(poles.real, poles.imag, "x", color="black", ms=7, mew=1.5)
    if len(N) > 1:
        z = np.roots(N)
        ax.plot(z.real, z.imag, "o", mfc="white", mec="black", ms=6)
    r = np.linspace(0, 30, 2)
    ax.plot(-zeta * r, math.sqrt(1 - zeta**2) * r, color=PALETTE[1], ls="--", lw=1)
    ax.plot(design.real, design.imag, "o", color=PALETTE[1], ms=5)
    ax.plot(design.real, -design.imag, "o", color=PALETTE[1], ms=5)
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color="gray", lw=0.5)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Re s")
    ax.set_title(title, fontsize=8.5)


def fig_loci():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.6))
    panel(axs[0], [1], [1, 6, 8, 0], 200, 0.5, complex(-2 / 3, 2 / math.sqrt(3)),
          "K/[s(s+2)(s+4)]  (ζ = 0.5 at K = 8.30)", (-7, 2), (-5, 5))
    axs[0].set_ylabel("Im s")
    panel(axs[1], [1, 1], [1, 6, 8, 0], 2000, 0.5, complex(-2.5674683748524227, 4.446985672070691),
          "K(s+1)/[s(s+2)(s+4)]  (ζ = 0.5 at K = 22.8)", (-7, 2), (-7, 7))
    panel(axs[2], [1, 8], [1, 4, 0], 400, 1 / math.sqrt(2), complex(-4, 4),
          "K(s+8)/[s(s+4)]  (ζ = 0.707 at K = 4)", (-16, 2), (-8, 8))
    fig.tight_layout()
    save(fig, f"{OUT}/loci.svg")


if __name__ == "__main__":
    fig_loci()
