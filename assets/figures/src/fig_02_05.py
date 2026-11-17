#!/usr/bin/env python3
"""Figures for chapter 02-05 (the Laplace transform for ODEs).

Run:  python assets/figures/src/fig_02_05.py  -> assets/figures/02-05/*.svg
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
OUT = "assets/figures/02-05"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_s_plane():
    """Pole positions (insets) and the time-domain modes they produce."""
    fig, ax = plt.subplots(figsize=(8.0, 5.6))
    ax.axhline(0, color="0.4", lw=1)
    ax.axvline(0, color="0.4", lw=1)
    ax.set_xlim(-3.6, 2.3)
    ax.set_ylim(-0.6, 3.6)
    ax.set_xlabel("Re s = σ (decay rate, 1/s)")
    ax.set_ylabel("Im s = ω (oscillation, rad/s)")
    ax.set_title("Where a pole sits decides what its mode does: e^(σt)·cos(ωt) (each inset scaled to fit)")
    ax.axvspan(0, 2.3, color=O, alpha=0.06)
    ax.text(1.2, 3.35, "unstable\n(right half-plane)", ha="center", color=O, fontsize=9)
    ax.text(-1.7, 3.35, "stable (left half-plane)", ha="center", color=G, fontsize=9)
    t = np.linspace(0, 6, 300)
    for (sig, w) in [(-2.4, 0), (-1.2, 0), (0, 0), (0.3, 0), (-2.4, 2.2), (-1.2, 2.2), (0, 2.2), (0.3, 2.2)]:
        ax.plot([sig], [w], "x", color="k", ms=9, mew=2)
        x0 = sig - 0.45 if sig <= -1 else (-0.62 if sig == 0 else 0.42)
        inset = ax.inset_axes([x0, w + 0.18, 0.9, 0.75], transform=ax.transData)
        if sig >= 0:
            ax.annotate("", xy=(sig, w + 0.05), xytext=(x0 + 0.45, w + 0.18), arrowprops=dict(arrowstyle="-", color="0.6", lw=0.8))
        yv = np.exp(sig * t) * np.cos(w * t)
        yv = yv / np.max(np.abs(yv))
        inset.plot(t, yv, color=B if sig < 0 else (P if sig == 0 else O), lw=1.4)
        inset.set_xticks([])
        inset.set_yticks([])
        inset.set_ylim(-1.15, 1.15)
        for sp_ in inset.spines.values():
            sp_.set_color("0.7")
    fig.tight_layout()
    save(fig, f"{OUT}/s-plane-modes.svg")


def fig_pulse():
    tau, T, V = 1.0, 2.0, 5.0
    t = np.linspace(-0.5, 7, 2000)
    step1 = np.where(t >= 0, V * (1 - np.exp(-t / tau)), 0.0)
    step2 = np.where(t >= T, -V * (1 - np.exp(-(t - T) / tau)), 0.0)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.plot(t, np.where((t >= 0) & (t < T), V, 0.0), color="0.6", lw=1.2, label="input: 5 V pulse, 2 ms")
    ax.plot(t, step1, color=B, ls="--", lw=1.2, label="response to the step at 0")
    ax.plot(t, step2, color=O, ls="--", lw=1.2, label="response to the step −5 V at 2 ms")
    ax.plot(t, step1 + step2, color="k", lw=2, label="total (time-shift property)")
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("v (V)")
    ax.set_title("RC (τ = 1 ms) driven by a pulse = two shifted step responses")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/pulse-response.svg")


def fig_convolution():
    tau = 1.0
    t = np.linspace(0, 6, 1201)
    dt = t[1] - t[0]
    h = np.exp(-t / tau) / tau
    x = np.where(t < 2, 5.0, 0.0)
    y = np.convolve(x, h)[: len(t)] * dt
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.2))
    axes[0].plot(t, h, color=B, lw=2)
    axes[0].set_title("impulse response h(t) = e^(−t/τ)/τ")
    axes[1].plot(t, x, color="0.4", lw=2)
    axes[1].set_title("input x(t)")
    axes[2].plot(t, y, color="k", lw=2)
    axes[2].set_title("output y = h * x  ⇔  Y = H·X")
    for ax in axes:
        ax.set_xlabel("t (ms)")
    fig.tight_layout()
    save(fig, f"{OUT}/convolution.svg")


if __name__ == "__main__":
    fig_s_plane()
    fig_pulse()
    fig_convolution()
