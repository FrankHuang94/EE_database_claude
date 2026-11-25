#!/usr/bin/env python3
"""Figures for chapter 23-09 (compute-in-memory and near-memory computing).

Run from anywhere:  python assets/figures/src/fig_23_09.py
Outputs
  assets/figures/23-09/cim-snr.svg      compute SNR (1/sigma^2, zero-mean products) and effective bits against relative
                                        device variation from 0.1% to 20%, with 4-, 6- and 8-bit levels marked
  assets/figures/23-09/adc-ceiling.svg  ADC-limited TOPS/W against input and weight precision (bit-serial inputs,
                                        bit-sliced weights) for 256-row arrays with 8-bit ADCs at Walden figures of
                                        merit of 1, 5 and 20 fJ per conversion step
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import cim  # noqa: E402

OUT = "assets/figures/23-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def cim_snr() -> None:
    sigma = np.logspace(-3, math.log10(0.2), 200)
    snr = 10 * np.log10(1 / sigma ** 2)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.semilogx(sigma * 100, [cim.enob(s) for s in snr], color=PALETTE[0])
    for b, col in ((4, PALETTE[1]), (6, PALETTE[2]), (8, PALETTE[3])):
        ax.axhline(b, color=col, ls=":", lw=1, label=f"{b} effective bits")
    ax.set_xlabel("relative device variation σ (%)")
    ax.set_ylabel("effective bits of the dot product")
    ax.legend(loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/cim-snr.svg")


def adc_ceiling() -> None:
    bits = np.arange(1, 9)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for fom, col in ((1e-15, PALETTE[0]), (5e-15, PALETTE[1]), (20e-15, PALETTE[2])):
        ax.semilogy(bits, [cim.tops_per_watt(cim.adc_energy_per_mac(fom, 8, 256, int(b), int(b))) for b in bits], "o-",
                    color=col, ms=4, label=f"ADC FoM {fom*1e15:.0f} fJ/step")
    ax.set_xlabel("input and weight bits")
    ax.set_ylabel("ADC-limited TOPS/W")
    ax.legend()
    fig.tight_layout()
    save(fig, f"{OUT}/adc-ceiling.svg")


if __name__ == "__main__":
    cim_snr()
    adc_ceiling()
