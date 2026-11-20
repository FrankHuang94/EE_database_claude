#!/usr/bin/env python3
"""Figures for chapter 16-05 (spectral analysis and windowing).

Run from anywhere:  python assets/figures/src/fig_16_05.py
Outputs
  assets/figures/16-05/windows.svg       spectra (dB, normalized to the main-lobe peak) of the rectangular, Hann,
                                         Blackman and 4-term Blackman-Harris windows, 0 to 16 bins from the tone
  assets/figures/16-05/adc-spectrum.svg  Example 16-05.5's coherent 16,384-point ADC spectrum in dBFS, with the
                                         fundamental and harmonics 2 to 5 marked at their aliased bins
Uses labs/16-05-lab/spectral.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import spectral as sp  # noqa: E402

OUT = "assets/figures/16-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_windows():
    N, P = 64, 64 * 128
    nu = np.arange(P) * N / P
    sel = nu <= 16
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    for name, col, lab in (("rect", "gray", "rectangular"), ("hann", PALETTE[0], "Hann"),
                           ("blackman", PALETTE[2], "Blackman"), ("bh4", PALETTE[3], "Blackman–Harris (4-term)")):
        W = np.abs(np.fft.fft(sp.window(name, N), P))
        ax.plot(nu[sel], 20 * np.log10(np.maximum(W[sel] / W[0], 1e-9)), color=col, lw=1.1, label=lab)
    ax.set_ylim(-140, 5)
    ax.set_xlim(0, 16)
    ax.set_xlabel("distance from the tone (bins)")
    ax.set_ylabel("window spectrum (dB)")
    ax.set_title("Lower sidelobes cost a wider main lobe", fontsize=9)
    ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/windows.svg")


def fig_adc():
    fs, N = 100e6, 16384
    M = sp.coherent_bin(10e6, fs, N)
    A = 10 ** (-1 / 20)
    a3, a2, q = 4e-4 / A**2, 2 * 10 ** (-90 / 20) / A, 2 / 2**12
    rng = np.random.default_rng(1605)
    n = np.arange(N)
    x = A * np.sin(2 * np.pi * M * n / N + 0.7)
    y = x + a2 * x**2 + a3 * x**3 + rng.normal(scale=2.0e-4, size=N)
    yq = np.clip(np.round(y / q) * q, -1, 1 - q)
    X = np.abs(np.fft.fft(yq))[:N // 2 + 1] / (N / 2)   # amplitude relative to a full-scale (amplitude 1) sine
    f = np.arange(N // 2 + 1) * fs / N / 1e6
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    ax.plot(f, 20 * np.log10(np.maximum(X, 1e-9)), color=PALETTE[0], lw=0.5)
    m = sp.adc_metrics(yq, M)
    for h, b in zip([1] + list(range(2, 6)), [M] + m["harm_bins"]):
        ax.annotate("fundamental" if h == 1 else f"HD{h}", (b * fs / N / 1e6, 20 * np.log10(X[b])),
                    textcoords="offset points", xytext=(4, 6), fontsize=7, color=PALETTE[3])
    ax.set_ylim(-150, 5)
    ax.set_xlabel("frequency (MHz), fs = 100 MS/s, N = 16,384")
    ax.set_ylabel("dBFS")
    ax.set_title(f"Coherent ADC test: SNR {m['snr']:.1f} dB, SINAD {m['sinad']:.1f} dB, SFDR {m['sfdr']:.1f} dB, ENOB {m['enob']:.2f}",
                 fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/adc-spectrum.svg")


if __name__ == "__main__":
    fig_windows()
    fig_adc()
