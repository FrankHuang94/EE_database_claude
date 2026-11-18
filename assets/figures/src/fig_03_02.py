#!/usr/bin/env python3
"""Figures for chapter 03-02 (random variables and distributions).

Run:  python assets/figures/src/fig_03_02.py  -> assets/figures/03-02/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom, norm, poisson

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/03-02"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_binomial_poisson():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.8), sharey=True)
    for ax, (n, p, title) in zip(axes, ((12_000, 1e-4, "n = 12,000, p = 10⁻⁴ (λ = 1.2)"),
                                        (12, 0.1, "n = 12, p = 0.1 (λ = 1.2)"))):
        k = np.arange(0, 8)
        ax.bar(k - 0.18, binom.pmf(k, n, p), width=0.36, color=B, label="binomial")
        ax.bar(k + 0.18, poisson.pmf(k, n * p), width=0.36, color=O, label="Poisson, λ = np")
        ax.set_xlabel("number of events k")
        ax.set_title(title, fontsize=10)
        ax.set_xticks(k)
    axes[0].set_ylabel("probability")
    axes[0].legend(fontsize=8)
    fig.suptitle("Poisson is the binomial in the limit of many trials and a small probability each", fontsize=11)
    fig.tight_layout()
    save(fig, f"{OUT}/binomial-poisson.svg")


def fig_qfunction():
    x = np.linspace(0.5, 8, 400)
    q = norm.sf(x)
    upper = np.exp(-x**2 / 2) / (x * math.sqrt(2 * math.pi))
    chern = 0.5 * np.exp(-x**2 / 2)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    xx = np.linspace(-4, 4, 600)
    axes[0].plot(xx, norm.pdf(xx), color=B)
    sel = xx >= 2
    axes[0].fill_between(xx[sel], norm.pdf(xx[sel]), color=O, alpha=0.5)
    axes[0].annotate("Q(2) = 0.02275:\narea beyond 2σ", (2.5, 0.02), xytext=(2.1, 0.22), fontsize=8,
                     arrowprops=dict(arrowstyle="-", color="0.5"))
    axes[0].set_xlabel("z = (x − μ)/σ")
    axes[0].set_ylabel("standard normal PDF")
    axes[0].set_title("Q(z) is the upper-tail area", fontsize=10)
    axes[1].semilogy(x, q, color=B, lw=2, label="Q(x)")
    axes[1].semilogy(x, upper, "--", color=O, label="e^(−x²/2)/(x√(2π)) (upper bound)")
    axes[1].semilogy(x, chern, ":", color=G, label="½e^(−x²/2) (Chernoff bound)")
    for xv, lab in ((3, "1.35e-3"), (4.5, "3.4e-6"), (6, "9.9e-10"), (7.034, "1e-12")):
        axes[1].plot([xv], [norm.sf(xv)], "o", color="k", ms=3.5)
        axes[1].annotate(lab, (xv, norm.sf(xv)), xytext=(-40, -12), textcoords="offset points", fontsize=7)
    axes[1].set_xlabel("x")
    axes[1].set_ylim(1e-16, 1)
    axes[1].legend(fontsize=7, loc="lower left")
    axes[1].set_title("Q(x) falls faster than any exponential", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/q-function.svg")


def fig_bathtub():
    UI, DJ, RJ = 31.25, 8.0, 1.2              # ps, Example 03-02.7
    t = np.linspace(0, UI, 2000)
    # dual-Dirac convention of section 3.8: near each eye edge, BER = Q((distance beyond the
    # inner Dirac)/RJ); the edges' crossing distributions sit at 0 and UI, each with Diracs at ±DJ/2
    ber = np.minimum(0.5, norm.sf((t - DJ / 2) / RJ) + norm.sf((UI - t - DJ / 2) / RJ))
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.semilogy(t, np.maximum(ber, 1e-18), color=B, lw=2)
    ax.axhline(1e-12, color="0.5", ls=":", lw=0.8)
    TJ = DJ + 2 * norm.isf(1e-12) * RJ
    ax.annotate("", xy=(TJ / 2, 1e-12), xytext=(UI - TJ / 2, 1e-12),
                arrowprops=dict(arrowstyle="<->", color=O))
    ax.text(UI / 2, 2e-12, f"eye opening at 10⁻¹²: {UI - TJ:.2f} ps", ha="center", fontsize=8, color=O)
    ax.set_ylim(1e-17, 1)
    ax.set_xlabel("sampling instant within the unit interval (ps)")
    ax.set_ylabel("bit error rate")
    ax.set_title("Bathtub curve, dual-Dirac jitter: DJ = 8 ps, RJ = 1.2 ps rms, 32 GT/s (Example 03-02.7)", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/bathtub.svg")


if __name__ == "__main__":
    fig_binomial_poisson()
    fig_qfunction()
    fig_bathtub()
