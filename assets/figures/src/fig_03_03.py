#!/usr/bin/env python3
"""Figures for chapter 03-03 (expectation, variance and functions of random variables).

Run:  python assets/figures/src/fig_03_03.py  -> assets/figures/03-03/*.svg
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
OUT = "assets/figures/03-03"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]

VT = 1.380649e-23 * 300 / 1.602176634e-19      # thermal voltage at 300 K
SIG_V, N_SUB = 0.025, 1.4                      # Example 03-03.6
S = SIG_V / (N_SUB * VT)                       # standard deviation of ln(I/I0)


def fig_lognormal():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    dv = np.linspace(-0.1, 0.1, 500)
    axes[0].plot(dv * 1e3, norm.pdf(dv, 0, SIG_V) / 1e3, color=B)
    axes[0].set_xlabel("threshold-voltage shift ΔV_TH (mV)")
    axes[0].set_ylabel("density (1/mV)")
    axes[0].set_title("Gaussian input: σ = 25 mV", fontsize=10)
    x = np.linspace(1e-3, 6, 2000)
    f = np.exp(-np.log(x) ** 2 / (2 * S * S)) / (x * S * math.sqrt(2 * math.pi))
    axes[1].plot(x, f, color=O)
    med, mean = 1.0, math.exp(S * S / 2)
    axes[1].axvline(med, color="0.4", ls=":", lw=1)
    axes[1].axvline(mean, color=G, ls="--", lw=1)
    axes[1].text(med - 0.05, 0.25 * f.max(), "median = I₀", ha="right", fontsize=8)
    axes[1].text(mean + 0.08, 0.80 * f.max(), f"mean = {mean:.3f} I₀", fontsize=8, color=G)
    axes[1].set_xlabel("off-current I_off / I₀")
    axes[1].set_ylabel("density")
    axes[1].set_title("Exponential map → log-normal output, skewed right", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/lognormal-leakage.svg")


def fig_papr_ccdf():
    xdb = np.linspace(0, 14, 600)
    x = 10 ** (xdb / 10)
    sine = np.where(x < 2, (2 / math.pi) * np.arccos(np.sqrt(np.minimum(x, 2) / 2)), 0.0)
    real_g = 2 * norm.sf(np.sqrt(x))
    cplx_g = np.exp(-x)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.semilogy(xdb, np.maximum(sine, 1e-12), color=G, lw=2, label="sinusoid (peak at 3.01 dB)")
    ax.semilogy(xdb, cplx_g, color=B, lw=2, label="complex Gaussian (OFDM limit): e^(−x)")
    ax.semilogy(xdb, real_g, color=O, lw=2, label="real Gaussian: 2Q(√x)")
    ax.axhline(1e-4, color="0.5", ls=":", lw=0.8)
    for v, c in ((10 * math.log10(math.log(1e4)), B), (10 * math.log10(norm.isf(5e-5) ** 2), O)):
        ax.plot([v], [1e-4], "o", color=c, ms=4)
        ax.annotate(f"{v:.2f} dB", (v, 1e-4), xytext=(4, 6), textcoords="offset points", fontsize=8, color=c)
    ax.set_ylim(1e-6, 1.5)
    ax.set_xlim(0, 14)
    ax.set_xlabel("instantaneous power above average, x (dB)")
    ax.set_ylabel("P(power > x · average)")
    ax.set_title("CCDF of instantaneous power: PAPR is a probability statement", fontsize=10)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/papr-ccdf.svg")


def snr_db(n_bits, k):
    granular = k * k / (3 * 4.0**n_bits)
    clip = 2 * ((1 + k * k) * norm.sf(k) - k * norm.pdf(k))
    return 10 * np.log10(1 / (granular + clip)), 10 * np.log10(1 / granular)


def fig_adc_loading():
    k = np.linspace(2, 8, 600)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for n_bits, c in ((8, B), (10, O), (12, G)):
        total, gran = snr_db(n_bits, k)
        ax.plot(k, total, color=c, lw=2, label=f"N = {n_bits}: granular + clipping")
        ax.plot(k, gran, color=c, lw=1, ls="--")
        i = int(np.argmax(total))
        ax.plot([k[i]], [total[i]], "o", color=c, ms=4)
        ax.annotate(f"k ≈ {k[i]:.1f}", (k[i], total[i]), xytext=(4, 5), textcoords="offset points", fontsize=8, color=c)
    ax.set_ylim(20, 75)
    ax.set_xlabel("loading factor k = full scale / σ")
    ax.set_ylabel("signal-to-noise ratio (dB)")
    ax.set_title("ADC with a Gaussian input: too little headroom clips, too much wastes bits", fontsize=10)
    ax.text(6.2, 22.5, "dashed: granular noise only", fontsize=8, color="0.3")
    ax.legend(fontsize=8, loc="lower right", bbox_to_anchor=(1.0, 0.08))
    fig.tight_layout()
    save(fig, f"{OUT}/adc-loading.svg")


if __name__ == "__main__":
    fig_lognormal()
    fig_papr_ccdf()
    fig_adc_loading()
