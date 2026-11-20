#!/usr/bin/env python3
"""Figures for chapter 11-07 (the discrete-time Fourier transform).

Run from anywhere:  python assets/figures/src/fig_11_07.py
Outputs SVGs to assets/figures/11-07/:
- periodic.svg: |X(e^{jw})| of 0.8^n u[n] over -3pi..3pi (period 2pi; the band -pi..pi shaded);
- ma5.svg: Example 11-07.2, the five-point moving average: |H| with nulls at 0.4pi and 0.8pi, and its
  constant group delay of 2 samples;
- windowing.svg: Example 11-07.4, a 21-tap low-pass (cutoff pi/4) from the truncated ideal impulse response,
  with a rectangular and a Hamming window: taps and magnitude responses in dB;
- resolution.svg: Example 11-07.7, tones at 1000 and 1050 Hz sampled at 8 kHz, observed for 64 and 512
  samples: the magnitude of the windowed DTFT.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_periodic():
    w = np.linspace(-3 * np.pi, 3 * np.pi, 3001)
    X = np.abs(1 / (1 - 0.8 * np.exp(-1j * w)))
    fig, ax = plt.subplots(figsize=(7.4, 2.8))
    ax.axvspan(-1, 1, color=PALETTE[1], alpha=0.12)
    ax.plot(w / np.pi, X, color=PALETTE[0])
    ax.set_xlabel("ω / π (rad/sample)")
    ax.set_ylabel("|X(e^jω)|")
    ax.set_title("0.8ⁿu[n]: the spectrum repeats every 2π; one period (shaded) says everything", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/periodic.svg")


def fig_ma5():
    w = np.linspace(1e-4, np.pi, 2000)
    H = np.sin(5 * w / 2) / (5 * np.sin(w / 2))
    fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.0))
    axs[0].plot(w / np.pi, np.abs(H), color=PALETTE[0])
    for wz in (0.4, 0.8):
        axs[0].axvline(wz, ls=":", color="0.5", lw=1)
    axs[0].set_xlabel("ω / π")
    axs[0].set_ylabel("|H(e^jω)|")
    axs[0].set_title("five-point average: nulls at 0.4π, 0.8π", fontsize=10)
    phase = np.unwrap(np.angle(np.exp(-2j * w) * H))
    gd = -np.gradient(phase, w)
    near_null = (np.abs(w - 0.4 * np.pi) < 0.02) | (np.abs(w - 0.8 * np.pi) < 0.02)
    gd[near_null] = np.nan                        # the phase jumps by pi where H changes sign
    axs[1].plot(w / np.pi, gd, color=PALETTE[3])
    axs[1].set_ylim(0, 4)
    axs[1].set_xlabel("ω / π")
    axs[1].set_ylabel("group delay (samples)")
    axs[1].set_title("linear phase: constant delay of 2 samples", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/ma5.svg")


def fig_windowing():
    n = np.arange(-10, 11)
    h = np.where(n == 0, 0.25, np.sin(np.pi * n / 4) / (np.pi * np.where(n == 0, 1, n)))
    hw = h * np.hamming(21)
    w = np.linspace(0, np.pi, 3000)
    fig, axs = plt.subplots(1, 2, figsize=(8.8, 3.2))
    axs[0].stem(n, h, linefmt="C0-", markerfmt="C0o", basefmt=" ", label="rectangular")
    axs[0].plot(n, hw, "s", color=PALETTE[3], ms=4, label="Hamming")
    axs[0].set_xlabel("n")
    axs[0].set_title("taps: sin(πn/4)/(πn), n = −10…10", fontsize=10)
    axs[0].legend(fontsize=8)
    for hh, c, lab in ((h, PALETTE[0], "rectangular"), (hw, PALETTE[3], "Hamming")):
        H = np.array([np.sum(hh * np.cos(ww * n)) for ww in w])
        axs[1].plot(w / np.pi, 20 * np.log10(np.maximum(np.abs(H), 1e-6)), color=c, label=lab)
    axs[1].set_ylim(-90, 5)
    axs[1].axvline(0.25, ls=":", color="0.5", lw=1)
    axs[1].set_xlabel("ω / π")
    axs[1].set_ylabel("|H| (dB)")
    axs[1].legend(fontsize=8)
    axs[1].set_title("windowing trades ripple for transition width", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/windowing.svg")


def fig_resolution():
    fs = 8000.0
    f = np.linspace(800, 1250, 4000)
    fig, ax = plt.subplots(figsize=(7.4, 3.0))
    for N, c in ((64, PALETTE[0]), (512, PALETTE[3])):
        n = np.arange(N)
        x = np.cos(2 * np.pi * 1000 * n / fs) + np.cos(2 * np.pi * 1050 * n / fs)
        X = np.array([abs(np.sum(x * np.exp(-2j * np.pi * ff * n / fs))) for ff in f]) / N
        ax.plot(f, X, color=c, label=f"N = {N} ({N / fs * 1e3:g} ms)")
    for ft in (1000, 1050):
        ax.axvline(ft, ls=":", color="0.5", lw=1)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("|X| / N")
    ax.legend(fontsize=8)
    ax.set_title("two tones 50 Hz apart: resolved only with a long enough record", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/resolution.svg")


if __name__ == "__main__":
    fig_periodic()
    fig_ma5()
    fig_windowing()
    fig_resolution()
