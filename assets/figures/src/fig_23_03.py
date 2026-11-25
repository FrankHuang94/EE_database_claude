#!/usr/bin/env python3
"""Figures for chapter 23-03 (DRAM cells, arrays and refresh).

Run from anywhere:  python assets/figures/src/fig_23_03.py
Outputs
  assets/figures/23-03/signal-vs-cells.svg        read signal against cells per bitline (0.08 fF per cell + 4 fF)
                                                   for 10, 8, 6 and 4 fF cells with a drooped 0.4 V signal, and the
                                                   60 mV sense margin (Example 23-03.2's assumptions)
  assets/figures/23-03/refresh-overhead.svg       DDR4 tRFC1 by density (Micron 16Gb DDR4 data sheet, Rev. H 8/2021)
                                                   and tRFC/tREFI at up to 85 °C (7.8125 µs) and 85-95 °C (3.90625 µs)
  assets/figures/23-03/rowhammer-thresholds.svg   HCfirst for older and newer chips per DRAM type, Kim et al.,
                                                   ISCA 2020 (arXiv 2005.13121)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dramtech as dt  # noqa: E402

OUT = "assets/figures/23-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def signal_vs_cells() -> None:
    n = np.linspace(64, 1100, 300)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for c_s, col in zip((10, 8, 6, 4), PALETTE):
        dv = [dt.charge_sharing_dv(c_s * 1e-15, (k * 0.08 + 4) * 1e-15, 0.4, 0.0) * 1e3 for k in n]
        ax.plot(n, dv, color=col, label=f"C_s = {c_s} fF")
        nmax = dt.max_cells_per_bitline(c_s * 1e-15, 0.4, 0.06, 0.08e-15, 4e-15)
        if nmax < n[-1]:
            ax.plot([nmax], [60], "o", color=col, ms=4)
    ax.axhline(60, color="0.3", ls="--", lw=1)
    ax.text(1090, 63, "sense margin 60 mV", ha="right", va="bottom", fontsize=8, color="0.3")
    for k in (256, 512, 1024):
        ax.axvline(k, color="0.85", lw=0.8, zorder=0)
    ax.set_xlabel("cells per bitline")
    ax.set_ylabel("read signal (mV)")
    ax.set_ylim(0, 260)
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title("Smaller cells force shorter bitlines (drooped 0.4 V signal)", fontsize=10)
    save(fig, f"{OUT}/signal-vs-cells.svg")


def refresh_overhead() -> None:
    dens = np.array([2, 4, 8, 16])
    trfc = np.array([160, 260, 350, 350])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.3))
    a1.bar([str(d) for d in dens], trfc, color=PALETTE[0])
    for i, t in enumerate(trfc):
        a1.text(i, t + 6, f"{t}", ha="center", fontsize=8)
    a1.set_xlabel("DDR4 device density (Gb)")
    a1.set_ylabel("tRFC1 (ns)")
    a1.set_ylim(0, 400)
    a1.set_title("Refresh cycle time", fontsize=10)
    x = np.arange(len(dens))
    w = 0.38
    a2.bar(x - w / 2, 100 * trfc / 7812.5, w, color=PALETTE[2], label="up to 85 °C (64 ms)")
    a2.bar(x + w / 2, 100 * trfc / 3906.25, w, color=PALETTE[1], label="85–95 °C (32 ms)")
    a2.set_xticks(x, [str(d) for d in dens])
    a2.set_xlabel("DDR4 device density (Gb)")
    a2.set_ylabel("tRFC / tREFI (%)")
    a2.set_ylim(0, 11)
    a2.legend(fontsize=8, loc="upper left")
    a2.set_title("Refresh overhead", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/refresh-overhead.svg")


def rowhammer_thresholds() -> None:
    types = ["DDR3", "DDR4", "LPDDR4"]
    old = [69.2, 17.5, 16.8]
    new = [22.4, 10.0, 4.8]
    x = np.arange(3)
    w = 0.38
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.bar(x - w / 2, old, w, color=PALETTE[0], label="older chips")
    ax.bar(x + w / 2, new, w, color=PALETTE[1], label="newer chips")
    for xi, o, nn in zip(x, old, new):
        ax.text(xi - w / 2, o + 1, f"{o:g}k", ha="center", fontsize=8)
        ax.text(xi + w / 2, nn + 1, f"{nn:g}k", ha="center", fontsize=8)
    ax.set_xticks(x, types)
    ax.set_ylabel("HC_first (thousand activations)")
    ax.set_ylim(0, 80)
    ax.legend(fontsize=8)
    ax.set_title("Row-hammer threshold falls with newer chips (Kim et al., ISCA 2020)", fontsize=10)
    save(fig, f"{OUT}/rowhammer-thresholds.svg")


if __name__ == "__main__":
    signal_vs_cells()
    refresh_overhead()
    rowhammer_thresholds()
