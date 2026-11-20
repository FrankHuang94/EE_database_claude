#!/usr/bin/env python3
"""Figures for chapter 11-11 (modulation and filtering applications).

Run from anywhere:  python assets/figures/src/fig_11_11.py
Outputs SVGs to assets/figures/11-11/:
- am.svg: a tone message, its DSB-SC and conventional-AM (m = 0.5) waveforms, and their spectra;
- superhet.svg: Example 11-11.3's frequency plan (station 1000 kHz, LO 1455 kHz, image 1910 kHz, IF 455 kHz);
- families.svg: Example 11-11.4's Butterworth, Chebyshev I and elliptic designs (and a 5th-order Bessel):
  magnitude and group delay.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_am():
    fm, fc = 1.0, 12.0
    t = np.linspace(0, 2, 4000)
    x = np.cos(2 * np.pi * fm * t)
    c = np.cos(2 * np.pi * fc * t)
    fig, axs = plt.subplots(2, 2, figsize=(8.8, 4.6))
    axs[0, 0].plot(t, x * c, color=PALETTE[0], lw=0.8)
    axs[0, 0].plot(t, x, "--", color=PALETTE[3], lw=1)
    axs[0, 0].plot(t, -x, "--", color=PALETTE[3], lw=1)
    axs[0, 0].set_title("DSB-SC: x(t)cos(2πf_c t); the envelope is |x(t)|", fontsize=9)
    env = 1 + 0.5 * x
    axs[0, 1].plot(t, env * c, color=PALETTE[0], lw=0.8)
    axs[0, 1].plot(t, env, "--", color=PALETTE[3], lw=1)
    axs[0, 1].set_title("conventional AM, m = 0.5: the envelope is 1 + m x(t)", fontsize=9)
    for ax in axs[0]:
        ax.set_xlabel("t (message periods)")
        ax.set_yticks([])
    for ax, lines, title in ((axs[1, 0], [(fc - fm, 0.25), (fc + fm, 0.25)], "DSB-SC spectrum: two sidebands"),
                             (axs[1, 1], [(fc - fm, 0.125), (fc, 0.5), (fc + fm, 0.125)],
                              "AM spectrum: carrier plus sidebands")):
        for f, a in lines:
            ax.vlines(f, 0, a, color=PALETTE[0], lw=2)
        ax.set_xlim(fc - 4, fc + 4)
        ax.set_ylim(0, 0.6)
        ax.set_xlabel("frequency (message frequencies), positive side")
        ax.set_title(title, fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/am.svg")


def fig_superhet():
    fig, ax = plt.subplots(figsize=(7.6, 2.6))
    items = [(455, "IF 455", PALETTE[2]), (1000, "station 1000", PALETTE[0]), (1455, "LO 1455", "k"),
             (1910, "image 1910", PALETTE[3])]
    for f, lab, c in items:
        ax.vlines(f, 0, 1, color=c, lw=3 if f != 1455 else 1.5, linestyles="-" if f != 1455 else "--")
        ax.text(f, 1.05, lab, ha="center", fontsize=8)
    ax.annotate("", xy=(1000, 0.5), xytext=(1455, 0.5), arrowprops=dict(arrowstyle="<->", color="0.4"))
    ax.annotate("", xy=(1455, 0.5), xytext=(1910, 0.5), arrowprops=dict(arrowstyle="<->", color="0.4"))
    ax.text(1227, 0.55, "455", ha="center", fontsize=8)
    ax.text(1682, 0.55, "455", ha="center", fontsize=8)
    ax.axvspan(540, 1700, color=PALETTE[1], alpha=0.12)
    ax.text(560, 0.15, "US AM band 540–1700 kHz", fontsize=8)
    ax.set_xlim(300, 2100)
    ax.set_ylim(0, 1.25)
    ax.set_yticks([])
    ax.set_xlabel("frequency (kHz)")
    ax.set_title("both the station and the image are 455 kHz from the LO, so both mix to the IF", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/superhet.svg")


def fig_families():
    wp, ws = 2 * math.pi * 1e3, 2 * math.pi * 1.5e3
    designs = []
    n, wn = signal.buttord(wp, ws, 0.5, 50, analog=True)
    designs.append((f"Butterworth, n = {n}", signal.butter(n, wn, analog=True), PALETTE[0]))
    n, wn = signal.cheb1ord(wp, ws, 0.5, 50, analog=True)
    designs.append((f"Chebyshev I, n = {n}", signal.cheby1(n, 0.5, wn, analog=True), PALETTE[2]))
    n, wn = signal.ellipord(wp, ws, 0.5, 50, analog=True)
    designs.append((f"elliptic, n = {n}", signal.ellip(n, 0.5, 50, wn, analog=True), PALETTE[3]))
    designs.append(("Bessel, n = 5", signal.bessel(5, wp, analog=True, norm="mag"), "0.4"))
    f = np.linspace(10, 3000, 3000)
    w = 2 * math.pi * f
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.4))
    for lab, (b, a), c in designs:
        _, h = signal.freqs(b, a, worN=w)
        axs[0].plot(f / 1e3, 20 * np.log10(np.maximum(np.abs(h), 1e-8)), color=c, label=lab)
        gd = -np.gradient(np.unwrap(np.angle(h)), w) * 1e3
        axs[1].plot(f / 1e3, gd, color=c, label=lab)
    axs[0].axhline(-50, ls=":", color="0.5", lw=1)
    axs[0].axvline(1.5, ls=":", color="0.5", lw=1)
    axs[0].set_ylim(-90, 5)
    axs[0].set_xlabel("frequency (kHz)")
    axs[0].set_ylabel("|H| (dB)")
    axs[0].legend(fontsize=7, loc="lower left")
    axs[0].set_title("one specification, four families", fontsize=9)
    axs[1].set_xlim(0, 1.5)
    axs[1].set_ylim(0, 6)
    axs[1].set_xlabel("frequency (kHz)")
    axs[1].set_ylabel("group delay (ms)")
    axs[1].set_title("selectivity costs delay variation near the edge", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/families.svg")


if __name__ == "__main__":
    fig_am()
    fig_superhet()
    fig_families()
