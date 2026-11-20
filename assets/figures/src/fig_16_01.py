#!/usr/bin/env python3
"""Figures for chapter 16-01 (discrete-time signals and systems review).

Run from anywhere:  python assets/figures/src/fig_16_01.py
Outputs
  assets/figures/16-01/ema-vs-ma.svg   Example 16-01.3: impulse responses (left) and step responses (right) of the
                                       EMA with alpha = 1/16 and the 31-point moving average, which have the same
                                       white-noise variance gain (1/31), with the 1% band
  assets/figures/16-01/ma-hum.svg      Example 16-01.2: gain in dB of the 20- and 100-point moving averages at
                                       fs = 1 kHz from 0 to 250 Hz, with 50 and 60 Hz marked
Uses labs/16-01-lab/dtsys.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dtsys as ds  # noqa: E402

OUT = "assets/figures/16-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_ema_vs_ma():
    a = 1 / 16
    n = np.arange(100)
    h_ema = ds.impulse([a], [1, -(1 - a)], len(n))
    h_ma = ds.impulse(np.full(31, 1 / 31), [1], len(n))
    s_ema = ds.step([a], [1, -(1 - a)], len(n))
    s_ma = ds.step(np.full(31, 1 / 31), [1], len(n))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.4))
    a1.stem(n, h_ema, linefmt=PALETTE[0], markerfmt="o", basefmt=" ", label="EMA, α = 1/16")
    a1.stem(n, h_ma, linefmt=PALETTE[3], markerfmt="s", basefmt=" ", label="31-point moving average")
    for coll in a1.collections + a1.lines:
        coll.set_alpha(0.8)
    a1.set_xlabel("n (samples)")
    a1.set_ylabel("h[n]")
    a1.set_title("impulse responses: geometric tail against a finite window", fontsize=9)
    a1.legend(fontsize=7)
    a2.plot(n, s_ema, "o-", color=PALETTE[0], ms=2.5, label="EMA")
    a2.plot(n, s_ma, "s-", color=PALETTE[3], ms=2.5, label="moving average")
    a2.axhspan(0.99, 1.01, color="gray", alpha=0.2, lw=0)
    a2.axvline(30, color=PALETTE[3], ls=":", lw=0.8)
    a2.axvline(71, color=PALETTE[0], ls=":", lw=0.8)
    a2.text(31, 0.35, "MA exact\nat n = 30", fontsize=7, color=PALETTE[3])
    a2.text(72, 0.55, "EMA within\n1% at n = 71", fontsize=7, color=PALETTE[0])
    a2.set_xlabel("n (samples)")
    a2.set_ylabel("step response")
    a2.set_title("same noise reduction (1/31), different settling", fontsize=9)
    a2.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/ema-vs-ma.svg")


def fig_ma_hum():
    fs = 1000.0
    f = np.linspace(0.01, 500, 20001)
    w = 2 * np.pi * f / fs
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    for N, col in ((20, PALETTE[0]), (100, PALETTE[3])):
        g = ds.ma_gain(N, w)
        ax.plot(f, 20 * np.log10(np.maximum(g, 1e-6)), color=col, label=f"N = {N}: nulls every {fs / N:.0f} Hz")
    for f0, lab, dx, ha in ((50, "50 Hz", -1.5, "right"), (60, "60 Hz", 1.5, "left")):
        ax.axvline(f0, color="k", ls=":", lw=0.8)
        ax.text(f0 + dx, -57, lab, fontsize=7, ha=ha)
    ax.set_xlim(0, 250)
    ax.set_ylim(-60, 5)
    ax.set_xlabel("frequency (Hz), fs = 1 kHz")
    ax.set_ylabel("gain (dB)")
    ax.set_title("Moving averages as hum filters (Example 16-01.2)", fontsize=9)
    ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/ma-hum.svg")


if __name__ == "__main__":
    fig_ema_vs_ma()
    fig_ma_hum()
