#!/usr/bin/env python3
"""Figures for chapter 11-06 (the continuous-time Fourier transform).

Run from anywhere:  python assets/figures/src/fig_11_06.py
Outputs SVGs to assets/figures/11-06/:
- series-to-transform.svg: a unit pulse of width 1 repeated with periods 2, 4 and 8; the scaled Fourier
  coefficients T0 c_k plotted at their frequencies k/T0 fill in the envelope sinc(f) as the period grows;
- pairs.svg: three transform pairs: (a) a 1 us rectangular pulse and its sinc spectrum (Example 11-06.2);
  (b) e^{-at}u(t) with a = 1000/s and |X(f)| (Example 11-06.1); (c) Gaussians of two widths and their
  transforms (time scaling);
- sinc3.svg: Example 11-06.4, the magnitude of the ADS1292R's third-order sinc filter at 500 SPS in dB,
  with the -3 dB point at 131 Hz, notches at multiples of 500 Hz, and the 60 Hz and 250 Hz points;
- rise-time.svg: Example 11-06.7, normalized step responses of a single-pole system and a Gaussian system
  with the same -3 dB bandwidth, and of an ideal low-pass filter (overshoot 1.0895).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erf, sici

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_series_to_transform():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 2.9), sharey=True)
    f = np.linspace(-4, 4, 2001)
    for ax, T0 in zip(axs, (2, 4, 8)):
        k = np.arange(-4 * T0, 4 * T0 + 1)
        ck_T0 = np.sinc(k / T0)                      # T0 c_k = sinc(k / T0) for a unit pulse of width 1
        ax.plot(f, np.sinc(f), ls="--", color="0.6", lw=1)
        ax.stem(k / T0, ck_T0, basefmt=" ")
        ax.set_title(f"period T₀ = {T0}", fontsize=10)
        ax.set_xlabel("frequency k/T₀")
    axs[0].set_ylabel("T₀ · c_k")
    fig.tight_layout()
    save(fig, f"{OUT}/series-to-transform.svg")


def fig_pairs():
    fig, axs = plt.subplots(2, 3, figsize=(9.6, 5.0))
    t = np.linspace(-2, 3, 2001)
    axs[0, 0].plot(t, ((t >= 0) & (t < 1)).astype(float), color=PALETTE[0])
    axs[0, 0].set_title("(a) 1 µs pulse", fontsize=10)
    axs[0, 0].set_xlabel("t (µs)")
    f = np.linspace(-4, 4, 2001)
    axs[1, 0].plot(f, np.abs(np.sinc(f)), color=PALETTE[0])
    axs[1, 0].set_xlabel("f (MHz)")
    axs[1, 0].set_ylabel("|X(f)| (µs)")
    a = 1000.0
    tt = np.linspace(-1e-3, 5e-3, 2001)
    axs[0, 1].plot(tt * 1e3, np.where(tt >= 0, np.exp(-a * tt), 0), color=PALETTE[3])
    axs[0, 1].set_title("(b) e^(−at)u(t), a = 1000/s", fontsize=10)
    axs[0, 1].set_xlabel("t (ms)")
    ff = np.linspace(-1000, 1000, 2001)
    axs[1, 1].plot(ff, 1e3 / np.sqrt(a ** 2 + (2 * np.pi * ff) ** 2), color=PALETTE[3])
    axs[1, 1].set_xlabel("f (Hz)")
    axs[1, 1].set_ylabel("|X(f)| (ms)")
    tg = np.linspace(-4, 4, 2001)
    fg = np.linspace(-1.5, 1.5, 2001)
    for s, c in ((0.5, PALETTE[2]), (1.0, PALETTE[1])):
        axs[0, 2].plot(tg, np.exp(-tg ** 2 / (2 * s ** 2)), color=c, label=f"σ = {s}")
        axs[1, 2].plot(fg, s * math.sqrt(2 * math.pi) * np.exp(-2 * math.pi ** 2 * s ** 2 * fg ** 2), color=c)
    axs[0, 2].set_title("(c) Gaussians: narrow ↔ wide", fontsize=10)
    axs[0, 2].legend(fontsize=8)
    axs[0, 2].set_xlabel("t")
    axs[1, 2].set_xlabel("f")
    fig.tight_layout()
    save(fig, f"{OUT}/pairs.svg")


def fig_sinc3():
    f = np.linspace(1, 2000, 4000)
    H = np.abs(np.sinc(f / 500)) ** 3
    db = 20 * np.log10(np.maximum(H, 1e-9))
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ax.plot(f, db, color=PALETTE[0])
    ax.axhline(-3.01, ls=":", color="0.5", lw=1)
    for fx, lab, pos in ((60, "60 Hz", (20, -38)), (131, "131 Hz, −3 dB", (230, -8)), (250, "250 Hz", (330, -26))):
        ax.plot(fx, 20 * math.log10(abs(np.sinc(fx / 500)) ** 3), "o", color=PALETTE[3])
        ax.annotate(lab, (fx, 20 * math.log10(abs(np.sinc(fx / 500)) ** 3)), pos, fontsize=8,
                    arrowprops={"arrowstyle": "-", "color": "0.5"})
    ax.set_ylim(-100, 5)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("|H| (dB)")
    ax.set_title("third-order sinc filter at 500 SPS: notches at 500, 1000, 1500 Hz", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/sinc3.svg")


def fig_rise():
    f3 = 1.0
    t = np.linspace(-1.5, 2.0, 3001)
    tau = 1 / (2 * math.pi * f3)
    sp = np.where(t >= 0, 1 - np.exp(-np.maximum(t, 0) / tau), 0.0)
    sigma = 0.13250518 / f3
    ga = 0.5 * (1 + erf(t / (math.sqrt(2) * sigma)))
    W = 2 * math.pi * f3
    lp = 0.5 + sici(W * t)[0] / math.pi
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ax.plot(t, sp, color=PALETTE[0], label="single pole (causal): t_r = 0.350/f₃dB")
    ax.plot(t, ga, color=PALETTE[3], label="Gaussian (centred): t_r = 0.340/f₃dB")
    ax.plot(t, lp, color=PALETTE[2], label="ideal low-pass: overshoot 1.0895")
    ax.axhline(0.1, ls=":", color="0.6", lw=1)
    ax.axhline(0.9, ls=":", color="0.6", lw=1)
    ax.set_xlabel("t × f₃dB")
    ax.set_ylabel("step response")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/rise-time.svg")


if __name__ == "__main__":
    fig_series_to_transform()
    fig_pairs()
    fig_sinc3()
    fig_rise()
