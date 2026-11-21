#!/usr/bin/env python3
"""Figures for chapter 17-11 (MIMO and beamforming).

Run from anywhere:  python assets/figures/src/fig_17_11.py
Outputs
  assets/figures/17-11/array-factor.svg  array factor (dB) of an 8-element ULA: d = lambda/2 at broadside and steered
                                         to 30 deg, and d = lambda steered to 30 deg showing the grating lobe at -30 deg
  assets/figures/17-11/capacity.svg      ergodic capacity against SNR for N x N i.i.d. Rayleigh MIMO (N = 1, 2, 4, 8,
                                         Monte Carlo) with the unfaded SISO curve log2(1 + rho)
Uses labs/17-11-lab/mimo.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-11-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import mimo as mm  # noqa: E402

OUT = "assets/figures/17-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1711)

th = np.linspace(-90, 90, 3601)
fig, ax = plt.subplots(figsize=(6.8, 4.2))
for (dl, steer, col, lab) in ((0.5, 0, PALETTE[0], "d = λ/2, broadside"), (0.5, 30, PALETTE[1], "d = λ/2, steered to 30°"), (1.0, 30, PALETTE[3], "d = λ, steered to 30° (grating lobe)")):
    af = mm.array_factor(8, dl, th, steer)
    ax.plot(th, 20 * np.log10(np.maximum(af, 1e-4)), color=col, lw=1.2, label=lab)
ax.axhline(-3, color="0.6", ls=":", lw=1)
ax.set_ylim(-40, 2)
ax.set_xlim(-90, 90)
ax.set_xlabel("angle from broadside (degrees)")
ax.set_ylabel("|array factor| (dB)")
ax.set_title("8 elements: 9 dB of gain, a 12.8° beam, and grating lobes if d > λ/(1 + |sin θ0|)")
ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3)
fig.tight_layout()
save(fig, f"{OUT}/array-factor.svg")

snr_db = np.arange(-5, 31, 2.5)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
ax.plot(snr_db, np.log2(1 + 10 ** (snr_db / 10)), color="0.3", ls="--", label="SISO, no fading")
for n, col in ((1, PALETTE[1]), (2, PALETTE[0]), (4, PALETTE[2]), (8, PALETTE[4])):
    c = [mm.ergodic_capacity_mc(n, n, 10 ** (x / 10), 20_000, rng) for x in snr_db]
    ax.plot(snr_db, c, "o-", ms=3, color=col, label=f"{n}×{n} Rayleigh (ergodic)")
ax.set_xlabel("SNR ρ (dB)")
ax.set_ylabel("capacity (b/s/Hz)")
ax.set_title("Capacity grows with min(Nt, Nr): about N bits/s/Hz per 3 dB at high SNR")
ax.legend(fontsize=8, loc="upper left")
save(fig, f"{OUT}/capacity.svg")
