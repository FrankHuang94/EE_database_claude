#!/usr/bin/env python3
"""Figures for chapter 11-03 (convolution).

Run from anywhere:  python assets/figures/src/fig_11_03.py
Outputs SVGs to assets/figures/11-03/:
- superposition.svg: Example 11-03.1 as superposition: x = [1, 2, 3] and h = [1, -1, 2]; each input sample
  launches a scaled, shifted copy of h, and the copies add to y = [1, 1, 3, 1, 6];
- flip-slide.svg: Example 11-03.3, the CT convolution of x(t) = 1 on [0, 2) with h(t) = 3 on [0, 1): the
  flipped, shifted h(t - tau) against x(tau) at t = 0.5, 1.5 and 2.5, and the trapezoidal result;
- rc.svg: Example 11-03.4 and 11-03.5: a 5 V, 2 ms pulse through an RC low-pass (tau = 1 ms) computed by
  convolution, and the impulse response of two identical RC stages in cascade, (t / tau^2) exp(-t / tau);
- abs-sums.svg: Example 11-03.6, partial sums of |h[n]| for h = (-0.8)^n (converges to 5) and h = 1/(n + 1)
  (grows like ln n).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_superposition():
    x = [1, 2, 3]
    h = np.array([1, -1, 2])
    n = np.arange(-1, 7)
    fig, axs = plt.subplots(1, 5, figsize=(9.0, 2.6), sharey=True)
    for k, ax in enumerate(axs[:3]):
        part = np.zeros(len(n))
        for j, hv in enumerate(h):
            part[n == k + j] = x[k] * hv
        ax.stem(n, part, linefmt=f"C{k}-", markerfmt=f"C{k}o", basefmt=" ")
        ax.set_title(f"x[{k}] h[n − {k}]", fontsize=10)
    axs[3].axis("off")
    axs[3].text(0.5, 0.5, "sum", ha="center", va="center", fontsize=13)
    y = np.convolve(x, h)
    yy = np.zeros(len(n))
    yy[1:6] = y
    axs[4].stem(n, yy, linefmt="k-", markerfmt="ko", basefmt=" ")
    axs[4].set_title("y[n] = (x ∗ h)[n]", fontsize=10)
    for ax in axs:
        ax.set_xlabel("n")
        ax.set_ylim(-3.5, 7)
    fig.tight_layout()
    save(fig, f"{OUT}/superposition.svg")


def fig_flip_slide():
    tau = np.linspace(-2, 5, 2001)
    x = ((tau >= 0) & (tau < 2)).astype(float)

    def h(t):
        return 3.0 * ((t >= 0) & (t < 1))

    fig, axs = plt.subplots(1, 4, figsize=(9.6, 2.8))
    for ax, t in zip(axs[:3], (0.5, 1.5, 2.5)):
        hf = h(t - tau)
        ax.fill_between(tau, 0, np.minimum(x * 3, hf) * (x > 0), color=PALETTE[2], alpha=0.35, lw=0)
        ax.plot(tau, x, color=PALETTE[0], label="x(τ)")
        ax.plot(tau, hf, color=PALETTE[3], label="h(t − τ)")
        ax.axvline(t, color="0.6", ls=":", lw=1)
        ax.set_title(f"t = {t}", fontsize=10)
        ax.set_xlabel("τ")
        ax.set_xlim(-1.5, 4)
        ax.set_ylim(-0.2, 3.5)
    axs[0].legend(fontsize=8, loc="upper right")
    t = np.linspace(-1, 4.5, 1101)
    y = np.clip(np.minimum.reduce([3 * t, np.full_like(t, 3.0), 3 * (3 - t)]), 0, None)
    axs[3].plot(t, y, color="k")
    for tt in (0.5, 1.5, 2.5):
        axs[3].plot(tt, np.interp(tt, t, y), "o", color=PALETTE[2])
    axs[3].set_title("y(t) = (x ∗ h)(t)", fontsize=10)
    axs[3].set_xlabel("t")
    axs[3].set_ylim(-0.2, 3.5)
    fig.tight_layout()
    save(fig, f"{OUT}/flip-slide.svg")


def fig_rc():
    tau = 1e-3
    dt = 1e-6
    t = np.arange(0, 8e-3, dt)
    x = 5.0 * (t < 2e-3)
    h = np.exp(-t / tau) / tau
    y = np.convolve(x, h)[: len(t)] * dt
    h2 = t / tau ** 2 * np.exp(-t / tau)
    fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.2))
    axs[0].plot(t * 1e3, x, color=PALETTE[0], label="x(t): 5 V for 2 ms")
    axs[0].plot(t * 1e3, y, color=PALETTE[3], label="y = x ∗ h")
    axs[0].set_xlabel("t (ms)")
    axs[0].set_ylabel("V")
    axs[0].set_title("(a) RC low-pass, τ = 1 ms", fontsize=10)
    axs[0].legend(fontsize=8)
    axs[1].plot(t * 1e3, h * 1e-3, color=PALETTE[0], label="one stage: e^(−t/τ)/τ")
    axs[1].plot(t * 1e3, h2 * 1e-3, color=PALETTE[3], label="two stages: (t/τ²) e^(−t/τ)")
    axs[1].set_xlabel("t (ms)")
    axs[1].set_ylabel("h(t) (1/ms)")
    axs[1].set_title("(b) cascade = convolution of impulse responses", fontsize=10)
    axs[1].legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/rc.svg")


def fig_abs_sums():
    n = np.arange(0, 2001)
    s1 = np.cumsum(np.abs((-0.8) ** n))
    s2 = np.cumsum(1.0 / (n + 1))
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.semilogx(n + 1, s1, color=PALETTE[0], label="h[n] = (−0.8)ⁿ: sum → 5 (stable)")
    ax.semilogx(n + 1, s2, color=PALETTE[3], label="h[n] = 1/(n + 1): sum grows like ln n (unstable)")
    ax.axhline(5, color="0.5", ls="--", lw=1)
    ax.set_xlabel("number of terms")
    ax.set_ylabel("partial sum of |h[n]|")
    ax.legend(fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/abs-sums.svg")


if __name__ == "__main__":
    fig_superposition()
    fig_flip_slide()
    fig_rc()
    fig_abs_sums()
