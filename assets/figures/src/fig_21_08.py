#!/usr/bin/env python3
"""Figures for chapter 21-08 (transceiver architectures).

Run from anywhere:  python assets/figures/src/fig_21_08.py
Outputs
  assets/figures/21-08/freqplan.svg  third-order Butterworth preselector (2.45 GHz, 100 MHz) with the wanted signal,
                                     LO, image and half-IF spurs of the 300 MHz-IF plan of Examples 21-08.1 and 21-08.2
  assets/figures/21-08/jitter.svg    jitter-limited SNR against input frequency for 25, 50 and 100 fs rms, with three
                                     published converter data points (TI ADC32RF55 and ADC12DJ5200RF data sheets, R-390 and R-333;
                                     a 2025 ISSCC sub-sampling front end)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import trx  # noqa: E402

OUT = "assets/figures/21-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- frequency plan
f = np.linspace(2.0e9, 3.3e9, 2000)
fig, ax = plt.subplots(figsize=(5.8, 3.8))
ax.plot(f / 1e9, [-trx.butterworth_bp_atten_db(x, 2.45e9, 100e6, 3) for x in f], color=PALETTE[0], lw=1.6,
        label="3rd-order preselector")
marks = [(2.45, "wanted 2.45", PALETTE[2], -8, "right"), (2.75, "LO 2.75", "k", -8, "left"),
         (2.60, "half-IF 2.60\n(−28 dB)", PALETTE[1], -78, "left"),
         (2.90, "half-IF 2.90\n(−55 dB)", PALETTE[1], -78, "left"),
         (3.05, "image 3.05\n(−62 dB)", PALETTE[3], -94, "left")]
for x, lab_, col, y, ha in marks:
    ax.axvline(x, color=col, lw=1, ls="--")
    ax.text(x + (0.01 if ha == "left" else -0.01), y, lab_, fontsize=7.5, color=col, va="bottom", ha=ha)
ax.set_ylim(-100, 5)
ax.set_xlim(2.0, 3.3)
ax.set_xlabel("frequency (GHz)")
ax.set_ylabel("preselector response (dB)")
ax.set_title("A 300 MHz IF: the image is far, the half-IF spur is not", fontsize=10)
save(fig, f"{OUT}/freqplan.svg")

# ---------------------------------------------------------------- jitter
fin = np.geomspace(1e8, 4e10, 400)
fig, ax = plt.subplots(figsize=(5.8, 3.8))
for sj, col in ((25e-15, PALETTE[2]), (50e-15, PALETTE[0]), (100e-15, PALETTE[3])):
    ax.semilogx(fin / 1e9, [trx.jitter_snr_db(x, sj) for x in fin], color=col, lw=1.4, label=f"{sj*1e15:.0f} fs rms")
pts = [(1.8, 63, "ADC32RF55, 2× avg"), (7.997, 49.6, "ADC12DJ5200RF"), (32, 39, "ISSCC 2025 front end (SNDR > 39 dB)")]
for x, y, lab_ in pts:
    ax.plot(x, y, "o", color="k", ms=4)
    ax.annotate(lab_, (x, y), textcoords="offset points", xytext=(-6, -14), fontsize=7.5, ha="right")
ax.set_xlim(0.1, 40)
ax.set_ylim(30, 90)
ax.set_xlabel("input frequency (GHz)")
ax.set_ylabel("SNR limit (dB)")
ax.set_title("Jitter, not bits, limits SNR at RF", fontsize=10)
ax.legend(fontsize=8, loc="upper right")
save(fig, f"{OUT}/jitter.svg")
