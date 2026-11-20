#!/usr/bin/env python3
"""Figures for chapter 11-05 (Fourier series).

Run from anywhere:  python assets/figures/src/fig_11_05.py
Outputs SVGs to assets/figures/11-05/:
- synthesis.svg: partial sums of the +-1 square wave's series with harmonics up to 1, 3, 9 and 99, and a zoom
  on the Gibbs overshoot near the jump (peak 1.179 for every large N);
- spectra.svg: one-sided amplitude spectra 2|c_k| of a +-1 square wave, a triangle wave of amplitude 1 and a
  0-to-1 pulse train with 25% duty (with its sinc envelope and the missing 4th and 8th harmonics);
- pwm-rc.svg: Example 11-05.7, a 3.3 V, 25%-duty, 100 kHz PWM signal through an RC low-pass with a 1 kHz
  corner: the steady-state output ripple around 0.825 V;
- am-avoid.svg: Example 11-05.8, the harmonics of 400, 500 and 600 kHz switching against an AM station at
  1000 kHz.
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

OUT = "assets/figures/11-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def square_partial(theta, N):
    return sum(4 / (math.pi * k) * np.sin(k * theta) for k in range(1, N + 1, 2))


def fig_synthesis():
    th = np.linspace(-np.pi, 3 * np.pi, 4001)
    sq = np.sign(np.sin(th))
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.2), gridspec_kw={"width_ratios": [2.2, 1]})
    axs[0].plot(th / (2 * np.pi), sq, color="0.6", lw=1, label="square wave")
    for N, c in ((1, PALETTE[0]), (3, PALETTE[1]), (9, PALETTE[2]), (99, PALETTE[3])):
        axs[0].plot(th / (2 * np.pi), square_partial(th, N), color=c, lw=1.2, label=f"up to k = {N}")
    axs[0].set_xlabel("t / T₀")
    axs[0].legend(fontsize=8, ncol=3, loc="lower center")
    axs[0].set_ylim(-2.3, 1.45)
    z = np.linspace(-0.05, 0.25, 3001)
    for N, c in ((9, PALETTE[2]), (99, PALETTE[3])):
        axs[1].plot(z, square_partial(z, N), color=c, lw=1.2, label=f"k ≤ {N}")
    axs[1].axhline(1.179, ls="--", color="0.4", lw=1)
    axs[1].text(0.12, 1.2, "1.179", fontsize=9)
    axs[1].set_xlabel("ω₀t (rad), near the jump")
    axs[1].set_title("Gibbs overshoot", fontsize=10)
    axs[1].set_ylim(-0.2, 1.35)
    axs[1].legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/synthesis.svg")


def fig_spectra():
    k = np.arange(1, 16)
    sq = np.where(k % 2 == 1, 4 / (math.pi * k), 0.0)
    tri = np.where(k % 2 == 1, 8 / (math.pi ** 2 * k ** 2), 0.0)
    D = 0.25
    pul = 2 * D * np.abs(np.sinc(k * D))
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.0), sharey=True)
    for ax, s, title in ((axs[0], sq, "square ±1: 4/(πk), odd k"), (axs[1], tri, "triangle: 8/(π²k²), odd k"),
                         (axs[2], pul, "pulse train, 25% duty")):
        ax.stem(k, s, basefmt=" ")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("harmonic k")
    kk = np.linspace(0.01, 15, 600)
    axs[2].plot(kk, 2 * D * np.abs(np.sinc(kk * D)), ls="--", color="0.5", lw=1)
    axs[0].set_ylabel("amplitude 2|cₖ|")
    fig.tight_layout()
    save(fig, f"{OUT}/spectra.svg")


def fig_pwm_rc():
    A, D, f0, fc = 3.3, 0.25, 100e3, 1e3
    T = 1 / f0
    t = np.linspace(0, 3 * T, 3001)
    y = np.full_like(t, A * D)
    for k in range(1, 200):
        ck = A * D * np.sinc(k * D) * np.exp(-1j * math.pi * k * D)
        H = 1 / (1 + 1j * k * f0 / fc)
        y += 2 * np.real(ck * H * np.exp(1j * 2 * math.pi * k * f0 * t))
    x = A * ((t % T) < D * T)
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.0))
    axs[0].plot(t * 1e6, x, color=PALETTE[0])
    axs[0].set_title("PWM input, 3.3 V, 25% duty, 100 kHz", fontsize=10)
    axs[0].set_xlabel("t (µs)")
    axs[0].set_ylabel("V")
    axs[1].plot(t * 1e6, (y - A * D) * 1e3, color=PALETTE[3])
    axs[1].set_title("RC output minus its 0.825 V average", fontsize=10)
    axs[1].set_xlabel("t (µs)")
    axs[1].set_ylabel("mV")
    fig.tight_layout()
    save(fig, f"{OUT}/pwm-rc.svg")


def fig_am():
    fig, ax = plt.subplots(figsize=(8.0, 2.8))
    ax.axvspan(540, 1700, color=PALETTE[1], alpha=0.12)
    ax.text(560, 3.55, "AM broadcast band", fontsize=9)
    ax.axvline(1000, color="k", lw=1.5)
    ax.text(1010, 0.25, "station 1000 kHz", fontsize=9)
    for row, (fs, c) in enumerate(((400, PALETTE[0]), (500, PALETTE[3]), (600, PALETTE[2]))):
        h = np.arange(1, 6) * fs
        h = h[h <= 2000]
        ax.vlines(h, row + 0.6, row + 1.4, color=c, lw=2)
        ax.text(20, row + 0.9, f"{fs} kHz", fontsize=9, color=c)
    ax.set_xlim(0, 2100)
    ax.set_ylim(0, 3.8)
    ax.set_yticks([])
    ax.set_xlabel("frequency (kHz): switching harmonics k·f_sw")
    fig.tight_layout()
    save(fig, f"{OUT}/am-avoid.svg")


if __name__ == "__main__":
    fig_synthesis()
    fig_spectra()
    fig_pwm_rc()
    fig_am()
