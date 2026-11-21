#!/usr/bin/env python3
"""Figures for chapter 17-10 (OFDM).

Run from anywhere:  python assets/figures/src/fig_17_10.py
Outputs
  assets/figures/17-10/subcarriers.svg  amplitude spectra of five adjacent OFDM subcarriers (sinc((f - k df) T)) and
                                        their sum, with each subcarrier's centre marked: every sinc is zero at every
                                        other subcarrier's centre
  assets/figures/17-10/papr-ccdf.svg    PAPR CCDF by Monte Carlo for OFDM with 300 and 3276 subcarriers (4x oversampled),
                                        DFT-spread OFDM with 300 subcarriers, and the Nyquist-sample approximation
Uses labs/17-10-lab/ofdm.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-10-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import ofdm as of  # noqa: E402

OUT = "assets/figures/17-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1710)

# ------------------------------------------------------------------ overlapping orthogonal spectra
f = np.linspace(-4, 4, 2001)  # frequency in units of the subcarrier spacing
fig, ax = plt.subplots(figsize=(6.8, 3.6))
for i, k in enumerate(range(-2, 3)):
    ax.plot(f, np.sinc(f - k), color=PALETTE[i % len(PALETTE)], lw=1.2)
    ax.plot([k], [1], "o", color=PALETTE[i % len(PALETTE)], ms=4)
ax.plot(f, sum(np.sinc(f - k) for k in range(-2, 3)), color="0.4", ls="--", lw=1, label="sum of the five")
for k in range(-2, 3):
    ax.axvline(k, color="0.85", lw=0.8, zorder=0)
ax.axhline(0, color="0.6", lw=0.8)
ax.set_xlabel("frequency (units of the subcarrier spacing Δf = 1/T)")
ax.set_ylabel("amplitude spectrum")
ax.set_title("Overlapping but orthogonal: each sinc is zero at the other subcarriers' centres")
ax.legend(fontsize=8, loc="upper right")
save(fig, f"{OUT}/subcarriers.svg")

# ------------------------------------------------------------------ PAPR CCDF
g = np.linspace(4, 14, 201)
fig, ax = plt.subplots(figsize=(6.6, 4.6))
for nsc, nfft, col in ((300, 1200, PALETTE[0]), (3276, 4096, PALETTE[1])):
    p = of.ofdm_papr(nsc, 20000 if nsc == 300 else 4000, rng, nfft=nfft)
    ax.semilogy(g, [np.mean(p > x) for x in g], color=col, label=f"OFDM, {nsc} subcarriers (simulated)")
    ax.semilogy(g, of.papr_ccdf_theory(g, nsc), color=col, ls=":", lw=1, label=f"approximation, N = {nsc}")
pd = of.dfts_papr(300, 20000, rng)
ax.semilogy(g, [np.mean(pd > x) for x in g], color=PALETTE[2], label="DFT-spread OFDM, 300 subcarriers")
ax.set_ylim(1e-4, 1)
ax.set_xlim(4, 14)
ax.set_xlabel("PAPR threshold γ (dB)")
ax.set_ylabel("P(PAPR > γ)")
ax.set_title("OFDM needs about 11 dB of headroom at 1e-3; DFT-spread saves about 3 dB")
ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2)
fig.tight_layout()
save(fig, f"{OUT}/papr-ccdf.svg")
