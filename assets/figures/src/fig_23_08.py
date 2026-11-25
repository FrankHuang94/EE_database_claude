#!/usr/bin/env python3
"""Figures for chapter 23-08 (emerging memories).

Run from anywhere:  python assets/figures/src/fig_23_08.py
Outputs
  assets/figures/23-08/mram-delta.svg  room-temperature thermal stability factor needed for at most one expected flip
                                       in 10 years, against array size, for operation at 25, 85 and 150 C
                                       (f0 = 1e9 /s, temperature-independent barrier)
  assets/figures/23-08/emem-map.svg    best industry-demonstrated endurance against cell write energy, from
                                       Hellenbrand, Teck and MacManus-Driscoll, MRS Communications 14 (2024), Table 2;
                                       bars show the ranges the table gives (PCM set/reset energies, NOR endurance)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import emem  # noqa: E402

OUT = "assets/figures/23-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
YEARS10 = 10 * 365.25 * 86400


def mram_delta() -> None:
    n = np.logspace(3, 12, 200)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for t_c, col in ((25, PALETTE[0]), (85, PALETTE[1]), (150, PALETTE[2])):
        ax.semilogx(n, [emem.delta_at(emem.delta_required(x, YEARS10), t_c, 25) for x in n], color=col,
                    label=f"operating at {t_c} °C")
    ax.set_xlabel("bits in the array")
    ax.set_ylabel("Δ needed at 25 °C")
    ax.legend()
    fig.tight_layout()
    save(fig, f"{OUT}/mram-delta.svg")


def emem_map() -> None:
    # (label, energy low J, energy high J, endurance low, endurance high)
    rows = (("FeRAM (energy projected)", 100e-15, 100e-15, 1e15, 1e15),
            ("PCM", 1.5e-12, 9e-12, 1e7, 1e7),
            ("ReRAM", 5e-15, 5e-15, 1e12, 1e12),
            ("STT-MRAM", 0.7e-12, 0.7e-12, 1e16, 1e16),
            ("NOR flash", 100e-12, 100e-12, 1e4, 1e6),
            ("DRAM", 10e-15, 10e-15, 1e16, 1e16),
            ("SRAM", 1e-15, 1e-15, 1e16, 1e16))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for k, (lab, e1, e2, n1, n2) in enumerate(rows):
        col = PALETTE[k % len(PALETTE)]
        ex, ny = np.sqrt(e1 * e2), np.sqrt(n1 * n2)
        ax.errorbar([ex], [ny], xerr=[[ex - e1], [e2 - ex]], yerr=[[ny - n1], [n2 - ny]], fmt="o", color=col,
                    ms=6, capsize=3, label=lab)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(3e-16, 1e-9)
    ax.set_ylim(1e3, 1e17)
    ax.set_xlabel("cell write energy (J)")
    ax.set_ylabel("endurance (cycles)")
    ax.legend(fontsize=7, loc="lower left", ncol=2)
    fig.tight_layout()
    save(fig, f"{OUT}/emem-map.svg")


if __name__ == "__main__":
    mram_delta()
    emem_map()
