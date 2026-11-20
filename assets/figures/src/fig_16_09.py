#!/usr/bin/env python3
"""Figures for chapter 16-09 (multirate DSP).

Run from anywhere:  python assets/figures/src/fig_16_09.py
Outputs
  assets/figures/16-09/cic.svg         the sinc4 (N = 4, R = 32) CIC response at f_MOD = 12.8 MHz of Example 16-09.5,
                                       0 to 1.6 MHz, with the bands that alias onto 0-20 kHz shaded around each
                                       multiple of the 400 kHz output rate
  assets/figures/16-09/multistage.svg  Example 16-09.4: the three half-band stages' responses, each plotted against
                                       frequency at its own input rate, with the 20 kHz passband and their stopband edges
Uses labs/16-09-lab/multirate.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import multirate as mr  # noqa: E402

OUT = "assets/figures/16-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fm = 12.8e6
f = np.linspace(1, 1.6e6, 20000)
H = mr.cic_response(f, 32, 4, fm)
fig, ax = plt.subplots(figsize=(7.0, 3.8))
for k in range(1, 5):
    ax.axvspan((k * 400e3 - 20e3) / 1e3, (k * 400e3 + 20e3) / 1e3, color=PALETTE[1], alpha=0.25, lw=0)
ax.plot(f / 1e3, 20 * np.log10(np.maximum(H, 1e-12)), color=PALETTE[0])
ax.axvspan(0, 20, color=PALETTE[2], alpha=0.25, lw=0)
ax.text(30, -20, "passband 0-20 kHz", fontsize=8)
ax.text(330, -15, "bands that alias\nonto 0-20 kHz", fontsize=8)
ax.set_ylim(-160, 5)
ax.set_xlim(0, 1600)
ax.set_xlabel("frequency (kHz) at the 12.8 MHz modulator rate")
ax.set_ylabel("magnitude (dB)")
ax.set_title("sinc4 CIC, decimation by 32: nulls exactly where aliases come from")
save(fig, f"{OUT}/cic.svg")

stages = []
for F, fp in ((384e3, 20e3), (192e3, 20e3), (96e3, 20e3)):
    fst = F / 2 - fp
    for K in range(40):
        n = 4 * K + 3
        h = signal.remez(n, [0, fp, fst, F / 2], [1, 0], fs=F, grid_density=64)
        _, Hs = signal.freqz(h, worN=np.linspace(2 * np.pi * fst / F, np.pi, 2000))
        _, Hp = signal.freqz(h, worN=np.linspace(0, 2 * np.pi * fp / F, 2000))
        if np.max(np.abs(Hs)) <= 1e-4 and np.max(np.abs(np.abs(Hp) - 1)) <= 1e-4:
            break
    stages.append((F, fst, n, h))
fig, axes = plt.subplots(1, 3, figsize=(10.0, 3.4), sharey=True)
for ax, (F, fst, n, h), col in zip(axes, stages, PALETTE):
    w, Hh = signal.freqz(h, worN=4000)
    ax.plot(w * F / (2 * np.pi) / 1e3, 20 * np.log10(np.maximum(np.abs(Hh), 1e-9)), color=col)
    ax.axvline(20, color="0.4", lw=0.8, ls="--")
    ax.axvline(fst / 1e3, color="0.4", lw=0.8, ls=":")
    ax.set_title(f"{F / 1e3:.0f} → {F / 2e3:.0f} kHz: {n} taps", fontsize=9)
    ax.set_xlabel("frequency (kHz)")
    ax.set_ylim(-120, 5)
axes[0].set_ylabel("magnitude (dB)")
fig.suptitle("Three half-band stages: only the last one is sharp", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/multistage.svg")
print("figures written to", OUT)
