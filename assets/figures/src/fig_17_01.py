#!/usr/bin/env python3
"""Figures for chapter 17-01 (random processes and power spectral density).

Run from anywhere:  python assets/figures/src/fig_17_01.py
Outputs
  assets/figures/17-01/wk-pairs.svg       two Wiener-Khinchin pairs: the exponential autocorrelation of
                                          RC-filtered noise with its Lorentzian PSD, and band-limited white
                                          noise (sinc autocorrelation) with its rectangular PSD
  assets/figures/17-01/nrz-psd.svg        Welch estimates of simulated polar and unipolar NRZ against
                                          A^2 T sinc^2(fT); the unipolar DC line appears as a narrow spike
  assets/figures/17-01/noise-folding.svg  Example 17-01.5: the continuous Lorentzian (tau_c = 0.1 us), the
                                          folded density after sampling at 1 MS/s, and a Welch estimate of
                                          the exact AR(1) samples
Uses labs/17-01-lab/randproc.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import randproc as rp  # noqa: E402

OUT = "assets/figures/17-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ 1. Wiener-Khinchin pairs
tau_c = 1.0  # normalized: tau in units of tau_c, f in units of 1/tau_c
B = 0.5  # band-limited white noise of bandwidth B/tau_c, same power sigma^2 = 1
tau = np.linspace(-6, 6, 1201)
f = np.linspace(-1.5, 1.5, 1201)
R_exp = np.exp(-np.abs(tau) / tau_c)
S_lor = rp.lorentzian_two_sided(f, 1.0, tau_c)
R_bl = np.sinc(2 * B * tau)
S_rect = np.where(np.abs(f) < B, 1 / (2 * B), 0.0)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.2))
a1.plot(tau, R_exp, color=PALETTE[0], label="RC-filtered: $e^{-|τ|/τ_c}$")
a1.plot(tau, R_bl, color=PALETTE[1], label="band-limited: sinc(2Bτ)")
a1.axhline(0, color="0.6", lw=0.5)
a1.set_xlabel("lag τ / τ_c")
a1.set_ylabel("R(τ) / σ²")
a1.set_title("Autocorrelation")
a1.set_ylim(-0.3, 1.6)
a1.legend(fontsize=8, loc="upper right")
a2.plot(f, S_lor, color=PALETTE[0], label="Lorentzian $2τ_c/(1+(2πfτ_c)^2)$")
a2.plot(f, S_rect, color=PALETTE[1], label="flat, |f| < B")
a2.set_xlabel("frequency f · τ_c")
a2.set_ylabel("S(f) / (σ² τ_c)")
a2.set_title("Two-sided PSD (equal areas)")
a2.set_ylim(0, 2.9)
a2.legend(fontsize=8, loc="upper right")
fig.tight_layout()
save(fig, f"{OUT}/wk-pairs.svg")

# ------------------------------------------------------------------ 2. NRZ spectra
rng = np.random.default_rng(17)
sps, nbits = 16, 1 << 16
T = 1.0  # symbol period; sample rate sps/T
fs = sps / T
bits = rng.integers(0, 2, nbits)
polar = rp.pam_waveform(2.0 * bits - 1.0, sps)
unipolar = rp.pam_waveform(1.0 * bits, sps)
fig, ax = plt.subplots(figsize=(6.8, 3.6))
for x, A2, col, lab in ((polar, 1.0, PALETTE[0], "polar ±A"), (unipolar, 0.25, PALETTE[1], "unipolar 0/A")):
    fw, G = rp.psd_welch(x, fs, nperseg=1024)
    ax.plot(fw * T, 10 * np.log10(G / 2 + 1e-30), color=col, lw=0.9, label=f"{lab}: Welch estimate")
    ax.plot(fw * T, 10 * np.log10(rp.nrz_psd(fw, A2, T) + 1e-30), color=col, ls="--", lw=0.8,
            label=f"{lab}: $A^2T\\,$sinc$^2(fT)$ × {A2:g}")
ax.set_xlim(0, 4)
ax.set_ylim(-50, 30)
ax.set_xlabel("frequency × bit period, fT")
ax.set_ylabel("two-sided PSD (dB re A²T)")
ax.set_title("Nulls at multiples of the bit rate; unipolar adds a DC line")
ax.annotate("DC line (half the power,\nspread over one Welch bin)", xy=(0.02, 10), xytext=(0.5, 8), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.6))
ax.legend(fontsize=7, loc="upper right")
save(fig, f"{OUT}/nrz-psd.svg")

# ------------------------------------------------------------------ 3. noise folding (Example 17-01.5)
sigma2, tc, fs = 1e-6, 0.1e-6, 1e6
x = rp.ou_samples(1 << 18, sigma2, tc, 1 / fs, np.random.default_rng(5))
fw, Gw = rp.psd_welch(x, fs, nperseg=1024)
fc = np.logspace(3, 7.3, 400)
G_cont = 2 * rp.lorentzian_two_sided(fc, sigma2, tc)
fa = np.linspace(1e3, fs / 2, 200)
G_fold = 2 * rp.aliased_density(fa, sigma2, tc, fs, terms=4000)
fig, ax = plt.subplots(figsize=(6.6, 3.6))
ax.loglog(fc, G_cont, color=PALETTE[2], label="continuous noise, one-sided (corner 1.59 MHz)")
ax.loglog(fa, G_fold, color=PALETTE[0], lw=1.6, label="after sampling at 1 MS/s: folded sum")
ax.loglog(fw[1:], Gw[1:], color=PALETTE[1], lw=0.6, alpha=0.8, label="Welch estimate of the AR(1) samples")
ax.axvline(fs / 2, color="0.5", ls=":", lw=0.8)
ax.text(fs / 2 * 1.08, 1.0e-13, "Nyquist\n500 kHz", fontsize=8)
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("one-sided density (V²/Hz)")
ax.set_ylim(1e-15, 1e-11)
ax.set_title("All the noise lands in band: density × 5, total power unchanged")
ax.legend(fontsize=8, loc="lower left")
save(fig, f"{OUT}/noise-folding.svg")
