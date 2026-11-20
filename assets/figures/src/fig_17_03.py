#!/usr/bin/env python3
"""Figures for chapter 17-03 (analog modulation).

Run from anywhere:  python assets/figures/src/fig_17_03.py
Outputs
  assets/figures/17-03/fm-spectrum.svg  tone-FM line spectra |J_n(beta)| for beta = 1, 2.405 (carrier null) and 5,
                                        with Carson's bandwidth marked
  assets/figures/17-03/snr-curves.svg   output SNR against the baseband reference gamma for DSB/SSB, tone AM at
                                        100% and tone FM (D = 5): formulas, with Monte Carlo points from the lab's
                                        quadrature-discriminator receiver showing the threshold
Uses labs/17-03-lab/analogmod.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import analogmod as am  # noqa: E402

OUT = "assets/figures/17-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.9), sharey=True)
for ax, beta, col in zip(axes, (1.0, 2.405, 5.0), PALETTE):
    n, a = am.bessel_lines(beta, 9)
    ax.vlines(n, 0, np.abs(a), color=col, lw=2)
    ax.plot(n, np.abs(a), "o", color=col, ms=3)
    half = beta + 1
    ax.axvspan(-half, half, color="0.9", zorder=0)
    ax.set_title(f"β = {beta:g}: Carson ±{half:g} lines", fontsize=9)
    ax.set_xlabel("sideband n (f − f_c in units of f_m)")
    ax.set_xlim(-9.5, 9.5)
axes[0].set_ylabel("|J_n(β)| (carrier = 1 unmodulated)")
fig.suptitle("Tone FM: power moves from the carrier into sidebands; at β = 2.405 the carrier vanishes", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/fm-spectrum.svg")

g = np.linspace(5, 45, 200)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
ax.plot(g, g, color=PALETTE[0], label="DSB-SC and SSB: γ")
ax.plot(g, [am.snr_theory_db("am", x, pm=0.5, ka=1.0) for x in g], color=PALETTE[1], label="AM, tone, 100%: γ/3")
ax.plot(g, [am.snr_theory_db("fm", x, pm=0.5, d=5) for x in g], color=PALETTE[2], label="FM, tone, D = 5: 1.5D²γ")
rng = np.random.default_rng(17)
gs = np.arange(12, 41, 2.0)
sim = [am.simulate_fm_snr(x, rng=rng, if_factor=1.0, n=1 << 19) for x in gs]
ax.plot(gs, sim, "o", color=PALETTE[2], ms=4, label="FM, simulated discriminator")
gth = 10 + 10 * np.log10(12)
ax.axvline(gth, color="0.5", ls=":", lw=0.8)
ax.text(gth + 0.5, 8, "threshold:\n10 dB CNR in 12W", fontsize=8)
ax.set_xlabel("baseband reference γ = S_R/(N₀W) (dB)")
ax.set_ylabel("output SNR (dB)")
ax.set_ylim(0, 65)
ax.set_title("FM trades bandwidth for SNR, but only above threshold")
ax.legend(fontsize=8, loc="upper left")
save(fig, f"{OUT}/snr-curves.svg")
