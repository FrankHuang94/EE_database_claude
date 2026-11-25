#!/usr/bin/env python3
"""Figures for chapter 23-02 (SRAM technology).

Run from anywhere:  python assets/figures/src/fig_23_02.py
Outputs
  assets/figures/23-02/vmin-vs-size.svg     Example 23-02.3's Vmin against array size (1 Kib to 1 Gib, 99% yield, no
                                            repair) for threshold mismatch of 25 mV (one fin) and 20.4 mV (nanosheet)
  assets/figures/23-02/bitcell-scaling.svg  reported high-density bitcell areas by node: TSMC N5, N3, N3E, N2 and
                                            the A14 upper bound (an IEDM 2026 abstract); Intel 7, Intel 4 and 18A
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import sramtech as st  # noqa: E402

OUT = "assets/figures/23-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def vmin_vs_size() -> None:
    bits = np.logspace(10, 30, 81, base=2)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for sig, col, lab in ((25.0, PALETTE[0], "σ_VT = 25 mV (one fin)"), (20.4, PALETTE[1], "σ_VT = 20.4 mV (nanosheet)")):
        ax.semilogx(bits, [st.vmin(st.sigma_needed(n), sig) for n in bits], color=col, label=lab)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("array size (bits)")
    ax.set_ylabel("Vmin (V)")
    ax.legend(fontsize=8)
    ax.set_title("Vmin grows slowly with array size; device spread matters more", fontsize=10)
    save(fig, f"{OUT}/vmin-vs-size.svg")


def bitcell_scaling() -> None:
    tsmc = [("N5", 0.021), ("N3", 0.0199), ("N3E", 0.021), ("N2", 0.021)]
    intel = [("Intel 7", 0.0312), ("Intel 4", 0.024), ("18A", 0.021)]
    fig, ax = plt.subplots(1, 2, figsize=(6.4, 3.6), sharey=True, gridspec_kw={"width_ratios": [5, 3]})
    x_t = np.arange(len(tsmc))
    ax[0].plot(x_t, [a for _, a in tsmc], "o-", color=PALETTE[0], label="reported cell")
    ax[0].plot([len(tsmc)], [0.017], "v", color=PALETTE[0], mfc="white", label="A14: reported upper bound")
    ax[0].set_xticks(list(x_t) + [len(tsmc)], [n for n, _ in tsmc] + ["A14"])
    ax[0].set_title("TSMC", fontsize=10)
    ax[0].legend(fontsize=8, loc="upper right")
    x_i = np.arange(len(intel))
    ax[1].plot(x_i, [a for _, a in intel], "s-", color=PALETTE[1])
    ax[1].set_xticks(x_i, [n for n, _ in intel])
    ax[1].set_title("Intel", fontsize=10)
    ax[0].set_ylabel("high-density bitcell area (µm²)")
    ax[0].set_ylim(0.014, 0.034)
    fig.suptitle("The SRAM bitcell stalled at 0.021 µm² from N5 to N2", fontsize=10)
    save(fig, f"{OUT}/bitcell-scaling.svg")


if __name__ == "__main__":
    vmin_vs_size()
    bitcell_scaling()
