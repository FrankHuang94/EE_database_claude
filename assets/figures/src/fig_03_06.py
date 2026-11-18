#!/usr/bin/env python3
"""Figures for chapter 03-06 (random processes preview: noise).

Run:  python assets/figures/src/fig_03_06.py  -> assets/figures/03-06/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/03-06"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def ar1(rng, n_paths, n, rho):
    """Unit-variance first-order Gauss-Markov (sampled RC-filtered white noise)."""
    x = np.empty((n_paths, n))
    x[:, 0] = rng.standard_normal(n_paths)
    w = rng.standard_normal((n_paths, n)) * math.sqrt(1 - rho**2)
    for k in range(1, n):
        x[:, k] = rho * x[:, k - 1] + w[:, k]
    return x


def fig_ensemble():
    rng = np.random.default_rng(5)
    n, dt, tc = 400, 1.0, 20.0                  # time in units of microseconds; correlation time 20 us
    rho = math.exp(-dt / tc)
    paths = ar1(rng, 4000, n, rho)
    t = np.arange(n) * dt
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.9), gridspec_kw={"width_ratios": [2.2, 1]})
    for i, c in enumerate((B, O, G, P, "0.4")):
        axes[0].plot(t, paths[i] + 4.5 * (2 - i), color=c, lw=1)
    t1 = 150
    axes[0].axvline(t1, color="k", ls="--", lw=1)
    axes[0].text(t1 + 4, 11, "ensemble slice at t₁", fontsize=8)
    axes[0].set_yticks([])
    axes[0].set_xlabel("time (µs)")
    axes[0].set_title("Five sample functions (offset vertically) of one random process", fontsize=10)
    v = paths[:, int(t1 / dt)]
    axes[1].hist(v, bins=40, density=True, color=B, alpha=0.6, orientation="horizontal")
    yy = np.linspace(-4, 4, 200)
    axes[1].plot(norm.pdf(yy), yy, color="k")
    axes[1].set_xlabel("density across 4000 sample functions")
    axes[1].set_ylabel("X(t₁)")
    axes[1].set_title("The slice is a random variable", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/ensemble.svg")


def fig_autocorr_psd():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.9))
    tau = np.linspace(-5e-3, 5e-3, 1001)
    f = np.logspace(0, 5, 400)
    for tc, c in ((1e-3, B), (0.1e-3, O)):
        axes[0].plot(tau * 1e3, np.exp(-np.abs(tau) / tc), color=c, label=f"τc = {tc * 1e3:g} ms")
        S = 4 * tc / (1 + (2 * math.pi * f * tc) ** 2)     # one-sided PSD of a unit-variance process (1/Hz)
        axes[1].loglog(f, S, color=c, label=f"τc = {tc * 1e3:g} ms: corner {1 / (2 * math.pi * tc):.0f} Hz")
    axes[0].set_xlabel("lag τ (ms)")
    axes[0].set_ylabel("R(τ)/R(0)")
    axes[0].set_title("Autocorrelation e^(−|τ|/τc): how long the process remembers", fontsize=10)
    axes[0].legend(fontsize=8)
    axes[1].set_xlabel("frequency (Hz)")
    axes[1].set_ylabel("one-sided PSD (units of σ² per Hz)")
    axes[1].set_title("Its PSD: shorter memory spreads the same power wider", fontsize=10)
    axes[1].legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/autocorr-psd.svg")


def fig_noise_density():
    f = np.logspace(-2, 4, 500)
    ew, fc = 10.0, 100.0                         # nV/sqrt(Hz), 1/f corner (Example 03-06.7)
    e = ew * np.sqrt(1 + fc / f)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.loglog(f, e, color=B, lw=2, label="amplifier: 10 nV/√Hz white, 1/f corner 100 Hz")
    ax.loglog(f, ew * np.ones_like(f), color="0.5", ls=":", lw=1, label="white floor")
    ax.loglog(f, ew * np.sqrt(fc / f), color=O, ls="--", lw=1, label="1/f part: density ∝ 1/√f")
    sel = (f >= 0.1) & (f <= 10)
    ax.fill_between(f[sel], e[sel], 1, color=G, alpha=0.25, label="0.1–10 Hz band")
    ax.set_ylim(3, 1e3)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("voltage noise density (nV/√Hz)")
    ax.set_title("Flicker (1/f) noise: equal power in every decade", fontsize=10)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/noise-density.svg")


if __name__ == "__main__":
    fig_ensemble()
    fig_autocorr_psd()
    fig_noise_density()
