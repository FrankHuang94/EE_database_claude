#!/usr/bin/env python3
"""Figures for chapter 24-01 (signal integrity fundamentals).

Run from anywhere:  python assets/figures/src/fig_24_01.py
Outputs
  assets/figures/24-01/loss-vs-frequency.svg  loss per inch of a 5-mil, 50 ohm smooth-copper trace from 0.1 to 60 GHz:
                                              conductor (sqrt f), FR-4-class and Megtron 6 dielectric (f) and the
                                              totals, with TI's tabulated model values at 8 and 16 GHz
  assets/figures/24-01/via-stub.svg           |S21| of a through via with a 1.6 mm open stub and with a 0.4 mm
                                              back-drilled stub in eps_r = 3.6, from the ABCD model
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import si  # noqa: E402

OUT = "assets/figures/24-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def loss_vs_frequency() -> None:
    f = np.logspace(8, np.log10(60e9), 300)
    w = 5 * si.MIL
    cond = np.array([si.conductor_loss_db_per_in(x, w, 50) for x in f])
    fr4 = np.array([si.dielectric_loss_db_per_in(x, 4.4, 0.014) for x in f])
    m6 = np.array([si.dielectric_loss_db_per_in(x, 3.4, 0.002) for x in f])
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.loglog(f / 1e9, cond, color=PALETTE[0], ls="--", label="conductor, 5 mil, 50 Ω")
    ax.loglog(f / 1e9, fr4, color=PALETTE[1], ls=":", label="FR-4-class dielectric")
    ax.loglog(f / 1e9, m6, color=PALETTE[2], ls=":", label="Megtron 6 dielectric")
    ax.loglog(f / 1e9, cond + fr4, color=PALETTE[1], label="FR-4-class total")
    ax.loglog(f / 1e9, cond + m6, color=PALETTE[2], label="Megtron 6 total")
    ax.plot([8, 16], [0.686, 1.289], "s", color=PALETTE[1], label="TI table, FR4 [1]")
    ax.plot([8, 16], [0.189, 0.336], "o", color=PALETTE[2], label="TI table, Megtron 6 [1]")
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("loss (dB/in)")
    ax.set_ylim(5e-3, 10)
    ax.legend(fontsize=7, loc="upper left")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/loss-vs-frequency.svg")


def via_stub() -> None:
    f = np.linspace(1e9, 120e9, 4000)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for length, col in ((1.6e-3, PALETTE[0]), (0.4e-3, PALETTE[3])):
        s = np.abs(si.s21(si.stub_abcd(f, length, 50, 3.6)))
        ax.plot(f / 1e9, 20 * np.log10(np.maximum(s, 1e-4)), color=col,
                label=f"{length*1e3:.1f} mm stub (notch {si.stub_notch(length, 3.6)/1e9:.1f} GHz)")
    for fn, lab in ((16, "16 GHz"), (53.125, "53 GHz")):
        ax.axvline(fn, color="0.5", ls=":", lw=1)
        ax.text(fn + 0.8, -38, lab, fontsize=7, color="0.4")
    ax.set_xlabel("frequency (GHz)")
    ax.set_ylabel("|S21| (dB)")
    ax.set_ylim(-40, 2)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, alpha=0.3)
    save(fig, f"{OUT}/via-stub.svg")


if __name__ == "__main__":
    loss_vs_frequency()
    via_stub()
