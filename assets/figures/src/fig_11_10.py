#!/usr/bin/env python3
"""Figures for chapter 11-10 (sampling, aliasing and reconstruction).

Run from anywhere:  python assets/figures/src/fig_11_10.py
Outputs SVGs to assets/figures/11-10/:
- spectra.svg: a band-limited spectrum, its sampled copies with f_s > 2 f_M, and overlapping copies with f_s < 2 f_M;
- folding.svg: apparent frequency against input frequency at 48 kHz, with Example 11-10.1's tones;
- zoh.svg: Example 11-10.4, a zero-order-hold staircase and the hold's |sinc| weighting of the tone and images;
- bandpass.svg: Example 11-10.6, a 60-80 MHz band and its mirror sampled at 56 MHz;
- ads1292r.svg: Example 11-10.7, RC, sinc^3 and combined responses up to 260 kHz.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def tri(f, fM):
    return np.clip(1 - np.abs(f) / fM, 0, None) * (1 + 0.3 * np.cos(4 * np.pi * f / fM))


def fig_spectra():
    fM = 1.0
    f = np.linspace(-5, 5, 4001)
    fig, axs = plt.subplots(3, 1, figsize=(7.2, 5.4), sharex=True)
    axs[0].fill_between(f, tri(f, fM), color=PALETTE[0], alpha=0.6)
    axs[0].set_title("original spectrum, band-limited to f_M", fontsize=9)
    for ax, fs, lab in ((axs[1], 2.6, "f_s = 2.6 f_M > 2 f_M: copies separated"),
                        (axs[2], 1.6, "f_s = 1.6 f_M < 2 f_M: copies overlap (aliasing)")):
        total = np.zeros_like(f)
        for k in range(-4, 5):
            c = tri(f - k * fs, fM)
            total += c
            ax.plot(f, c, color=PALETTE[0] if k == 0 else "0.55", lw=1)
        if fs < 2:
            over = np.zeros_like(f)
            for k in range(-4, 5):
                for m in range(k + 1, 5):
                    over = np.maximum(over, np.minimum(tri(f - k * fs, fM), tri(f - m * fs, fM)))
            ax.fill_between(f, over, color=PALETTE[3], alpha=0.5)
        else:
            ax.plot([-fs / 2, -fs / 2, fs / 2, fs / 2], [0, 1.4, 1.4, 0], "--", color=PALETTE[2], lw=1.2)
        ax.set_title(lab, fontsize=9)
    for ax in axs:
        ax.set_yticks([])
        ax.set_ylim(0, 1.5)
    axs[2].set_xlabel("frequency / f_M")
    fig.tight_layout()
    save(fig, f"{OUT}/spectra.svg")


def fig_folding():
    fs = 48.0
    f = np.linspace(0, 110, 2201)
    fa = np.abs(((f + fs / 2) % fs) - fs / 2)
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.plot(f, fa, color=PALETTE[0])
    for f0 in (30, 50, 96.5):
        a = abs(((f0 + fs / 2) % fs) - fs / 2)
        ax.plot([f0], [a], "o", color=PALETTE[3])
        ax.annotate(f"{f0:g} → {a:g} kHz", (f0, a), textcoords="offset points", xytext=(4, 6), fontsize=8)
    for k in range(1, 5):
        ax.axvline(k * fs / 2, ls=":", color="0.7", lw=0.8)
    ax.set_xlabel("input frequency (kHz)")
    ax.set_ylabel("apparent frequency (kHz)")
    ax.set_ylim(0, 27)
    ax.set_title("folding at f_s = 48 kHz: the apparent frequency zigzags between 0 and 24 kHz", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/folding.svg")


def fig_zoh():
    fs, f0 = 48e3, 20e3
    T = 1 / fs
    t = np.linspace(0, 12 * T, 2000)
    n = np.arange(13)
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.2))
    axs[0].plot(t * 1e6, np.cos(2 * np.pi * f0 * t), color="0.6", lw=1, label="20 kHz tone")
    axs[0].step(n * T * 1e6, np.cos(2 * np.pi * f0 * n * T), where="post", color=PALETTE[0], label="zero-order hold")
    axs[0].plot(n * T * 1e6, np.cos(2 * np.pi * f0 * n * T), "o", color=PALETTE[3], ms=3)
    axs[0].set_xlabel("t (µs)")
    axs[0].legend(fontsize=7, loc="lower left")
    axs[0].set_title("a staircase lags the samples by T/2", fontsize=9)
    f = np.linspace(0, 150e3, 3000)
    axs[1].plot(f / 1e3, 20 * np.log10(np.maximum(np.abs(np.sinc(f / fs)), 1e-6)), color=PALETTE[0])
    for fx in (20e3, 28e3, 68e3):
        axs[1].plot([fx / 1e3], [20 * np.log10(abs(np.sinc(fx / fs)))], "o", color=PALETTE[3])
    axs[1].set_ylim(-40, 2)
    axs[1].set_xlabel("frequency (kHz)")
    axs[1].set_ylabel("|sinc(f/f_s)| (dB)")
    axs[1].set_title("hold weighting: tone −2.64 dB, images −5.56 and −13.27 dB", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/zoh.svg")


def fig_bandpass():
    fs = 56.0
    fig, ax = plt.subplots(figsize=(7.6, 2.8))
    for k in range(-2, 3):
        for lo, hi, c in ((60, 80, PALETTE[0]), (-80, -60, PALETTE[2])):
            a, b = lo + k * fs, hi + k * fs
            if b < -5 or a > 100:
                continue
            ax.fill_between([a, b], [0, 1] if lo > 0 else [1, 0], color=c, alpha=0.9 if k == 0 else 0.35)
    for z in range(0, 4):
        ax.axvline(z * fs / 2, ls=":", color="0.6", lw=0.8)
    ax.axvspan(0, fs / 2, color=PALETTE[1], alpha=0.12)
    ax.set_xlim(-5, 100)
    ax.set_yticks([])
    ax.set_xlabel("frequency (MHz)")
    ax.set_title("60–80 MHz (solid, ramp marks orientation) sampled at 56 MHz: a copy lands upright at 4–24 MHz",
                 fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/bandpass.svg")


def fig_ads():
    fDR, fM, N = 500.0, 128e3, 256
    f = np.linspace(10, 260e3, 200000)
    s3 = np.abs(np.sin(np.pi * f / fDR) / (N * np.sin(np.pi * f / fM))) ** 3
    rc = 1 / np.abs(1 + 1j * f / 8.4e3)
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ax.plot(f / 1e3, 20 * np.log10(np.maximum(s3, 1e-12)), color="0.7", lw=0.6, label="sinc³ (nulls every 500 Hz)")
    ax.plot(f / 1e3, 20 * np.log10(rc), color=PALETTE[2], label="RC, 8.4 kHz")
    env = 20 * np.log10(np.maximum(np.minimum(1, (fDR / (np.pi * np.abs(((f + fM / 2) % fM) - fM / 2) + 1e-9)) ** 3)
                                   * rc, 1e-12))
    ax.plot(f / 1e3, env, color=PALETTE[3], lw=1.2, label="combined (envelope)")
    ax.set_ylim(-140, 5)
    ax.set_xlabel("input frequency (kHz)")
    ax.set_ylabel("gain (dB)")
    ax.legend(fontsize=7, loc="lower right")
    ax.set_title("the sinc³ passband returns at 128 and 256 kHz; only the RC filter is left there", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/ads1292r.svg")


if __name__ == "__main__":
    fig_spectra()
    fig_folding()
    fig_zoh()
    fig_bandpass()
    fig_ads()
