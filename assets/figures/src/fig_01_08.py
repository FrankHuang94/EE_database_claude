#!/usr/bin/env python3
"""Figures for chapter 01-08 (sequences, series and Taylor expansions).

Run:  python assets/figures/src/fig_01_08.py  -> assets/figures/01-08/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import iv

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/01-08"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def taylor_sin(x, deg):
    return sum((-1) ** k * x ** (2 * k + 1) / math.factorial(2 * k + 1) for k in range(deg // 2 + 1))


def fig_taylor():
    x = np.linspace(-2 * np.pi, 2 * np.pi, 600)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, np.sin(x), color="k", lw=2, label="sin x")
    for deg, col in [(1, P), (3, O), (5, G), (9, B)]:
        ax.plot(x, taylor_sin(x, deg), color=col, lw=1.2, label=f"degree {deg}")
    ax.set_ylim(-2.5, 2.5)
    ax.set_xlabel("x (rad)")
    ax.legend(fontsize=8, loc="lower left", ncol=2)
    ax.set_title("Taylor polynomials of sin x: accurate near 0, spreading outward with degree")
    fig.tight_layout()
    save(fig, f"{OUT}/taylor-sine.svg")


def fig_radius():
    x = np.linspace(-0.95, 1.6, 500)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, np.log1p(x), color="k", lw=2, label="ln(1 + x)")
    for N, col in [(2, P), (5, O), (12, G), (25, B)]:
        s = sum((-1) ** (k + 1) * x**k / k for k in range(1, N + 1))
        ax.plot(x, s, color=col, lw=1.2, label=f"{N} terms")
    ax.axvline(1, color="0.5", ls=":")
    ax.text(1.03, -1.6, "radius of\nconvergence", fontsize=8)
    ax.set_ylim(-2, 2)
    ax.set_xlabel("x")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("ln(1 + x): the series converges only for −1 < x ≤ 1")
    fig.tight_layout()
    save(fig, f"{OUT}/radius-of-convergence.svg")


def fig_bounces():
    Vl, gs, gl = 50 / 60, -2 / 3, 1.0
    k = np.arange(1, 13)
    partial = np.cumsum([Vl * (1 + gl) * (gs * gl) ** (n - 1) for n in k])
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.step(np.r_[0, k], np.r_[0, partial], where="post", color=B, label="far-end voltage after each arrival")
    ax.axhline(1.0, color=O, ls="--", label="geometric-series limit = DC value 1 V")
    ax.set_xlabel("arrival number")
    ax.set_ylabel("V")
    ax.legend(fontsize=8)
    ax.set_title("Reflections on a line: a geometric series")
    fig.tight_layout()
    save(fig, f"{OUT}/bounce-series.svg")


def fig_distortion():
    VT = 0.02585
    A = np.logspace(-4, np.log10(0.05), 200)
    xr = A / VT
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.loglog(A * 1e3, 100 * xr / 4, color=B, ls="--", label="Taylor: HD2 ≈ A/(4V_T)")
    ax.loglog(A * 1e3, 100 * iv(2, xr) / iv(1, xr), color=B, label="exact HD2 (Bessel)")
    ax.loglog(A * 1e3, 100 * xr**2 / 24, color=O, ls="--", label="Taylor: HD3 ≈ A²/(24V_T²)")
    ax.loglog(A * 1e3, 100 * iv(3, xr) / iv(1, xr), color=O, label="exact HD3")
    ax.set_xlabel("drive amplitude A (mV)")
    ax.set_ylabel("harmonic / fundamental (%)")
    ax.legend(fontsize=8)
    ax.set_title("Distortion of an exponential (diode/BJT) device")
    fig.tight_layout()
    save(fig, f"{OUT}/exponential-distortion.svg")


def fig_approx():
    x = np.logspace(-3, -0.3, 200)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.loglog(x, np.abs(x - np.sin(x)) / np.sin(x), color=B, label="sin x ≈ x   (error ≈ x²/6)")
    ax.loglog(x, np.abs((1 + x / 2) - np.sqrt(1 + x)) / np.sqrt(1 + x), color=O, label="√(1+x) ≈ 1 + x/2   (≈ x²/8)")
    ax.loglog(x, np.abs((1 + x) - np.exp(x)) / np.exp(x), color=G, label="eˣ ≈ 1 + x   (≈ x²/2)")
    ax.loglog(x, np.abs((1 - x) - 1 / (1 + x)) * (1 + x), color=P, label="1/(1+x) ≈ 1 − x   (≈ x²)")
    ax.set_xlabel("x")
    ax.set_ylabel("relative error")
    ax.legend(fontsize=8)
    ax.set_title("First-order approximations: error grows as x²")
    fig.tight_layout()
    save(fig, f"{OUT}/approximation-errors.svg")


if __name__ == "__main__":
    fig_taylor()
    fig_radius()
    fig_bounces()
    fig_distortion()
    fig_approx()
    print("01-08 figures written")
