#!/usr/bin/env python3
"""Figures for chapter 03-05 (estimation and hypothesis testing for engineers).

Run:  python assets/figures/src/fig_03_05.py  -> assets/figures/03-05/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.stats import t as tdist

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/03-05"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]

EX6_TIMES = np.array([457, 714, 823, 912, 976, 1182, 1600, 1706], float)   # Example 03-05.6, hours


def fig_coverage():
    rng = np.random.default_rng(3)
    mu, sigma, n, m = 1.1, 0.25, 10, 50
    tq = tdist.ppf(0.975, n - 1)
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    misses = 0
    for k in range(m):
        x = rng.normal(mu, sigma, n)
        half = tq * x.std(ddof=1) / math.sqrt(n)
        lo, hi = x.mean() - half, x.mean() + half
        hit = lo <= mu <= hi
        misses += not hit
        ax.plot([k, k], [lo, hi], color=B if hit else O, lw=1.6)
        ax.plot([k], [x.mean()], "o", color=B if hit else O, ms=2.5)
    ax.axhline(mu, color="k", lw=1, ls="--")
    ax.set_xlabel("repeated experiment (10 measurements each)")
    ax.set_ylabel("95% confidence interval for the mean (mV)")
    ax.set_title(f"50 experiments, 95% t-intervals: {misses} miss the true mean (orange)", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/ci-coverage.svg")


def fig_cpk():
    lsl, usl = 1.17, 1.23
    x = np.linspace(1.16, 1.24, 800)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.7), sharey=True)
    for ax, (mu, title) in zip(axes, ((1.200, "centered: Cp = Cpk = 1.67"), (1.205, "shifted 5 mV: Cp = 1.67, Cpk = 1.39"))):
        f = norm.pdf(x, mu, 0.006)
        ax.plot(x * 1e3, f, color=B)
        for sel in (x > usl, x < lsl):
            ax.fill_between(x[sel] * 1e3, f[sel], color=O, alpha=0.7)
        for lim in (lsl, usl):
            ax.axvline(lim * 1e3, color="0.3", ls="--", lw=1)
        ax.axvline(mu * 1e3, color=G, lw=1)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("LDO output voltage (mV)")
    axes[0].set_ylabel("density")
    axes[0].text(1171, 55, "LSL", fontsize=8)
    axes[0].text(1224, 55, "USL", fontsize=8)
    fig.suptitle("Cp measures spread against the window; Cpk also charges for being off center", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/cpk.svg")


def fig_weibull():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.0))
    tt = np.linspace(1, 3000, 600)
    alpha = 1000.0
    for g, c, lab in ((0.5, O, "γ = 0.5: infant mortality"), (1.0, G, "γ = 1: random (exponential)"), (2.5, B, "γ = 2.5: wear-out")):
        h = (g / alpha) * (tt / alpha) ** (g - 1)
        axes[0].plot(tt, h * 1e3, color=c, label=lab)
    axes[0].set_ylim(0, 6)
    axes[0].set_xlabel("time (h)")
    axes[0].set_ylabel("hazard rate (failures per 1000 h)")
    axes[0].set_title("Weibull hazard, α = 1000 h: the shape sets the trend", fontsize=10)
    axes[0].legend(fontsize=8)
    n = EX6_TIMES.size
    i = np.arange(1, n + 1)
    F = (i - 0.3) / (n + 0.4)
    x, y = np.log(EX6_TIMES), np.log(-np.log(1 - F))
    slope, icpt = np.polyfit(x, y, 1)
    axes[1].plot(x, y, "o", color=B, label="Example 03-05.6 failures (median ranks)")
    xx = np.linspace(x.min() - 0.3, x.max() + 0.3, 50)
    axes[1].plot(xx, slope * xx + icpt, color=O, label=f"least-squares line: γ = {slope:.3f}")
    axes[1].axhline(0, color="0.5", ls=":", lw=0.8)
    axes[1].text(x.min() - 0.25, 0.08, "63.2% failed: t = α", fontsize=8, color="0.3")
    axes[1].set_xlabel("ln t")
    axes[1].set_ylabel("ln(−ln(1 − F))")
    axes[1].set_title("Weibull plot: a straight line means Weibull", fontsize=10)
    axes[1].legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/weibull.svg")


if __name__ == "__main__":
    fig_coverage()
    fig_cpk()
    fig_weibull()
