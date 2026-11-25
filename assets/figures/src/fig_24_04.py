#!/usr/bin/env python3
"""Figures for chapter 24-04 (DSP-based SerDes and FEC).

Run from anywhere:  python assets/figures/src/fig_24_04.py
Outputs
  assets/figures/24-04/adc-limits.svg   SNR limits of a sampling ADC against input frequency: quantization of a PAM4
                                        signal (full scale 1.5x the outer level) for 5, 6, 7 bits and jitter of 50,
                                        100, 200 fs, with the 106 and 212 Gb/s PAM4 Nyquist frequencies marked
  assets/figures/24-04/mlsd-vs-dfe.svg  BER against SNR on h = (1, 1): ideal-DFE theory, MLSD single-event bound and
                                        a seeded Viterbi simulation
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "24-high-speed-io-signal-integrity-and-photonics" / "labs" / "24-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dsp  # noqa: E402

OUT = "assets/figures/24-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def adc_limits() -> None:
    f = np.logspace(9, 11, 300)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for i, bits in enumerate((5, 6, 7)):
        ax.axhline(dsp.sqnr_db(bits, 3.0), color=PALETTE[i], ls="--", lw=1.2, label=f"{bits}-bit quantization")
    for i, sj in enumerate((50e-15, 100e-15, 200e-15)):
        ax.semilogx(f / 1e9, [dsp.jitter_snr_db(x, sj) for x in f], color=PALETTE[i + 3],
                    label=f"{sj*1e15:.0f} fs jitter")
    for fn, lab in ((26.5625, "106 Gb/s PAM4"), (53.125, "212 Gb/s PAM4")):
        ax.axvline(fn, color="0.6", ls=":", lw=1)
        ax.text(fn * 1.04, 22, lab, fontsize=7, color="0.4", rotation=90)
    ax.set_xscale("log")
    ax.set_xlabel("input frequency (GHz)")
    ax.set_ylabel("SNR limit (dB)")
    ax.set_ylim(20, 55)
    ax.legend(fontsize=7, loc="upper right", ncol=2)
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/adc-limits.svg")


def mlsd_vs_dfe() -> None:
    snr = np.linspace(4, 12, 200)
    s = 10 ** (-snr / 20)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.semilogy(snr, norm.sf(1 / s), color=PALETTE[0], label="ideal DFE, Q(1/σ)")
    ax.semilogy(snr, norm.sf(np.sqrt(2) / s), "--", color=PALETTE[1], label="MLSD single-event bound, Q(√2/σ)")
    sig = np.array([0.32, 0.36, 0.40, 0.44, 0.48])
    ber = []
    for i, sv in enumerate(sig):
        n = 1_000_000 if sv < 0.38 else 200_000  # more symbols where errors are rare
        a = dsp.pam_symbols(n, 2, seed=7)
        y = dsp.channel(a, {0: 1.0, 1: 1.0}, sv, seed=10 + i)
        ber.append(np.mean(dsp.viterbi(y, [1.0, 1.0]) != a))
    ax.semilogy(20 * np.log10(1 / sig), ber, "s", color=PALETTE[1], label="MLSD, simulated Viterbi")
    ax.set_xlabel("SNR = 20 log10(h0/σ) (dB)")
    ax.set_ylabel("BER")
    ax.set_ylim(1e-7, 0.1)
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, f"{OUT}/mlsd-vs-dfe.svg")


if __name__ == "__main__":
    adc_limits()
    mlsd_vs_dfe()
