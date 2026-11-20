#!/usr/bin/env python3
"""Figures for chapter 16-03 (the DFT and its properties).

Run from anywhere:  python assets/figures/src/fig_16_03.py
Outputs
  assets/figures/16-03/dft-samples.svg   left: the DTFT magnitude of a 16-sample Hann pulse with its 16-point DFT and
                                         a 64-point zero-padded DFT on it; right: 1024-point DFTs at fs = 48 kHz of
                                         unit cosines at 3 kHz (on bin 64) and 1 kHz (bin 21.33), bins 0 to 80
  assets/figures/16-03/circular.svg      Example 16-03.3: linear convolution of (1, 2, 3) with (1, 1) and the 3-point
                                         circular convolution, with the wrapped sample marked
Uses labs/16-03-lab/dft.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dft  # noqa: E402

OUT = "assets/figures/16-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_samples():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.8, 3.6))
    pulse = np.hanning(18)[1:-1]
    w = np.linspace(0, 2 * np.pi, 2000, endpoint=False)
    a1.plot(w, np.abs(dft.dtft(pulse, w)), color="gray", lw=1.2, label="DTFT")
    X64 = np.fft.fft(pulse, 64)
    a1.plot(2 * np.pi * np.arange(64) / 64, np.abs(X64), ".", color=PALETTE[3], ms=5, label="64-point DFT (zero-padded)")
    X16 = np.fft.fft(pulse)
    a1.plot(2 * np.pi * np.arange(16) / 16, np.abs(X16), "o", color=PALETTE[0], ms=6, mfc="none", mew=1.4, label="16-point DFT")
    a1.set_xlabel("ω (rad/sample)")
    a1.set_ylabel("|X|")
    a1.set_title("the DFT samples the DTFT; padding samples it more finely", fontsize=9)
    a1.legend(fontsize=7)
    fs, N = 48_000.0, 1024
    n = np.arange(N)
    k = np.arange(81)
    for f, col, lab in ((3000, PALETTE[0], "3 kHz: on bin 64"), (1000, PALETTE[3], "1 kHz: bin 21.33 (leaks)")):
        X = np.abs(np.fft.fft(np.cos(2 * math.pi * f * n / fs)))[:81] / (N / 2)
        a2.stem(k, 20 * np.log10(np.maximum(X, 1e-6)), linefmt=col, markerfmt=".", basefmt=" ", bottom=-120, label=lab)
    a2.set_ylim(-60, 5)
    a2.set_xlabel("bin k (46.875 Hz per bin)")
    a2.set_ylabel("|X[k]| relative to N/2 (dB)")
    a2.set_title("on-bin and off-bin tones, N = 1024, fs = 48 kHz", fontsize=9)
    a2.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/dft-samples.svg")


def fig_circular():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 2.8), sharey=True)
    lin = np.convolve([1, 2, 3], [1, 1])
    a1.stem(range(4), lin, linefmt=PALETTE[0], basefmt=" ")
    a1.stem([3], [lin[3]], linefmt=PALETTE[3], markerfmt="o", basefmt=" ")
    a1.set_xticks(range(5))
    a1.set_xlim(-0.5, 4.5)
    a1.set_title("linear: (1, 3, 5, 3)", fontsize=9)
    a1.set_xlabel("n")
    circ = np.real(dft.circ_conv([1, 2, 3], [1, 1], 3))
    a2.bar([0], [1], color=PALETTE[0], width=0.15, label="from n = 0")
    a2.bar([0], [3], bottom=[1], color=PALETTE[3], width=0.15, label="wrapped from n = 3")
    a2.stem([1, 2], circ[1:], linefmt=PALETTE[0], basefmt=" ")
    a2.set_xticks(range(3))
    a2.set_xlim(-0.5, 2.5)
    a2.set_title("3-point circular: (4, 3, 5)", fontsize=9)
    a2.set_xlabel("n")
    a2.legend(fontsize=7, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/circular.svg")


if __name__ == "__main__":
    fig_samples()
    fig_circular()
