#!/usr/bin/env python3
"""Figures for chapter 23-06 (NAND flash and 3D NAND).

Run from anywhere:  python assets/figures/src/fig_23_06.py
Outputs
  assets/figures/23-06/ispp.svg  threshold shift after each of 30 ISPP pulses (15 V start, 0.25 V steps, 10 us each)
                                 for the cell of Example 23-06.2 (16 aF coupling, 7 nm oxide), with the per-pulse step
  assets/figures/23-06/rber.svg  raw bit error rate of SLC to QLC in a 6 V window against level sigma
                                 (Gaussian levels, Gray coding, midpoint references; chapter section 3.3)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import nand  # noqa: E402

OUT = "assets/figures/23-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def ispp() -> None:
    shifts = np.array(nand.ispp_shifts())
    k = np.arange(1, len(shifts) + 1)
    steps = np.diff(np.concatenate(([0.0], shifts)))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4))
    ax1.plot(k, shifts, "o-", color=PALETTE[0], ms=3.5)
    ax1.set_xlabel("pulse number")
    ax1.set_ylabel("threshold shift (V)")
    ax1.set_title("cumulative shift")
    ax2.plot(k, steps, "o-", color=PALETTE[1], ms=3.5, label="shift per pulse")
    ax2.axhline(0.25, color=PALETTE[2], ls="--", lw=1, label="pulse step 0.25 V")
    ax2.set_ylim(0, 2.1)
    ax2.set_xlabel("pulse number")
    ax2.set_ylabel("threshold rise from pulse (V)")
    ax2.set_title("per-pulse step")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/ispp.svg")


def rber() -> None:
    sig = np.linspace(0.02, 0.2, 300)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for bits, name, col in ((1, "SLC", PALETTE[0]), (2, "MLC", PALETTE[1]), (3, "TLC", PALETTE[2]),
                            (4, "QLC", PALETTE[3])):
        ax.semilogy(sig, [max(nand.rber(6, bits, s), 1e-30) for s in sig], color=col, label=name)
    ax.axhline(1e-3, color="0.5", ls=":", lw=1)
    ax.set_ylim(1e-15, 1)
    ax.set_xlabel("level standard deviation σ (V)")
    ax.set_ylabel("raw bit error rate")
    ax.legend(loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/rber.svg")


if __name__ == "__main__":
    ispp()
    rber()
