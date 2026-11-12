#!/usr/bin/env python3
"""Figures for chapter 01-06 (techniques of integration).

Run:  python assets/figures/src/fig_01_06.py  -> assets/figures/01-06/*.svg
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

use_style()
OUT = "assets/figures/01-06"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_elmore():
    t = np.linspace(0, 5, 400)
    h = np.exp(-t)
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(t, h, color=B, label="impulse response e^(−t/τ)/τ (scaled)")
    ax.plot(t, 1 - h, color="0.5", ls=":", label="step response 1 − e^(−t/τ)")
    ax.axvline(1, color=O, ls="--", lw=1)
    ax.axvline(math.log(2), color=G, ls="--", lw=1)
    ax.text(1.05, 0.85, "centroid (Elmore delay) = τ", color=O, fontsize=9)
    ax.text(0.66, 0.15, "50 % point = τ ln 2", color=G, fontsize=9, ha="right")
    ax.set_xlabel("t / τ")
    ax.legend(fontsize=8, loc="center right")
    ax.set_title("The first moment of an impulse response, by parts")
    fig.tight_layout()
    save(fig, f"{OUT}/elmore-centroid.svg")


def fig_partial_fractions():
    t = np.linspace(0, 3, 400)
    a = 10 / 3 * np.exp(-2 * t)
    b = -10 / 3 * np.exp(-5 * t)
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(t, a, color=B, ls="--", label="(10/3) e^(−2t)  from 10/3 ÷ (s + 2)")
    ax.plot(t, b, color=O, ls="--", label="−(10/3) e^(−5t)  from −10/3 ÷ (s + 5)")
    ax.plot(t, a + b, color="k", label="sum: h(t)")
    tp = math.log(2.5) / 3
    ax.plot([tp], [10 / 3 * (math.exp(-2 * tp) - math.exp(-5 * tp))], "o", color="k")
    ax.axhline(0, color="0.6", lw=0.8)
    ax.set_xlabel("t (s)")
    ax.legend(fontsize=8)
    ax.set_title("Partial fractions split a response into simple exponentials")
    fig.tight_layout()
    save(fig, f"{OUT}/partial-fraction-modes.svg")


def fig_fourier():
    t = np.linspace(0, 2, 4000)
    sq = np.sign(np.sin(2 * np.pi * t))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={"width_ratios": [1.6, 1]})
    a1.plot(t, sq, color="0.6", lw=1, label="square wave")
    for N, col in [(1, B), (3, O), (21, G)]:
        s = sum(4 / (n * np.pi) * np.sin(2 * np.pi * n * t) for n in range(1, N + 1, 2))
        a1.plot(t, s, color=col, lw=1.2, label=f"harmonics up to {N}")
    a1.set_xlabel("t / T")
    a1.legend(fontsize=8, loc="lower left")
    a1.set_title("Partial Fourier sums (note the Gibbs overshoot)")
    n = np.arange(1, 12, 2)
    a2.bar(n, 4 / (n * np.pi), color=B)
    a2.set_xlabel("harmonic n")
    a2.set_ylabel("amplitude b_n = 4/(nπ)")
    a2.set_title("Square-wave spectrum")
    fig.tight_layout()
    save(fig, f"{OUT}/square-wave-fourier.svg")


def fig_orthogonality():
    x = np.linspace(0, 2 * np.pi, 800)
    y = np.sin(3 * x) * np.sin(5 * x)
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    ax.plot(x, y, color=B)
    ax.fill_between(x, y, 0, where=y >= 0, color=G, alpha=0.3)
    ax.fill_between(x, y, 0, where=y < 0, color=O, alpha=0.3)
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_xlabel("x")
    ax.set_title("sin 3x · sin 5x: positive and negative areas cancel over a period")
    fig.tight_layout()
    save(fig, f"{OUT}/orthogonality.svg")


def fig_enbw():
    f = np.linspace(0, 6, 600)
    H2 = 1 / (1 + f**2)
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(f, H2, color=B, label="|H(f)|² of a one-pole filter")
    ax.fill_between(f, H2, color=B, alpha=0.2)
    ax.plot([0, np.pi / 2, np.pi / 2], [1, 1, 0], color=O, lw=2, label="brick wall of equal area: width (π/2) f_c")
    ax.set_xlabel("f / f_c")
    ax.set_ylabel("power gain")
    ax.legend(fontsize=8)
    ax.set_title("Equivalent noise bandwidth = ∫₀^∞ |H|² df")
    fig.tight_layout()
    save(fig, f"{OUT}/noise-bandwidth.svg")


if __name__ == "__main__":
    fig_elmore()
    fig_partial_fractions()
    fig_fourier()
    fig_orthogonality()
    fig_enbw()
    print("01-06 figures written")
