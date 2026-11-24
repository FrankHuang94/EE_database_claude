#!/usr/bin/env python3
"""Figures for chapter 21-11 (link budgets).

Run from anywhere:  python assets/figures/src/fig_21_11.py
Outputs
  assets/figures/21-11/wearable.svg  received power of the smartwatch link of Example 21-11.1 against distance (ITU-R
                                     P.1238-13 office NLoS model), with the specification, 1M and Coded sensitivities
                                     and the 90 % shadowing margin
  assets/figures/21-11/margins.svg   outage against margin for lognormal shadowing (8 dB), Rayleigh fading and both
                                     combined (Suzuki), with the 10 % and 1 % design points of Example 21-11.3
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-11-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import linkbudget as lb  # noqa: E402

OUT = "assets/figures/21-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- wearable link
d = np.linspace(4, 30, 300)
pr = -5 - (23.9 * np.log10(d) + 30.13 + 24.0 * math.log10(2.44)) - 5
sm = lb.lognormal_margin_db(5.01, 0.1)
fig, ax = plt.subplots(figsize=(5.8, 3.8))
ax.plot(d, pr, color=PALETTE[0], lw=1.6, label="received power (median)")
ax.plot(d, pr - sm, color=PALETTE[0], lw=1, ls="--", label="90 % level (−6.4 dB shadowing)")
for s, lab_, col in ((-70, "specification minimum, −70 dBm", PALETTE[3]), (-96.5, "typical 1M receiver, −96.5 dBm", PALETTE[1]),
                     (-102, "typical Coded receiver, −102 dBm", PALETTE[2])):
    ax.axhline(s, color=col, lw=1, ls=":")
    ax.text(12 if s == -70 else 29.5, s + 1, lab_, fontsize=7.5, color=col, ha="left" if s == -70 else "right", va="bottom")
ax.set_xlim(4, 30)
ax.set_ylim(-110, -55)
ax.set_xlabel("distance through an office (m)")
ax.set_ylabel("power at the phone (dBm)")
ax.set_title("A watch's 0 dBm Bluetooth link indoors", fontsize=10)
ax.legend(loc="upper right", fontsize=7.5)
save(fig, f"{OUT}/wearable.svg")

# ---------------------------------------------------------------- margins
m = np.linspace(0, 40, 161)
fig, ax = plt.subplots(figsize=(5.8, 3.8))
ax.semilogy(m, [0.5 * math.erfc(x / (8 * math.sqrt(2))) for x in m], color=PALETTE[2], lw=1.4, label="shadowing only (σ = 8 dB)")
ax.semilogy(m, [1 - math.exp(-10 ** (-x / 10)) for x in m], color=PALETTE[3], lw=1.4, label="Rayleigh only")
ax.semilogy(m, [lb.outage_shadow_rayleigh(x, 8) for x in m], color=PALETTE[0], lw=1.8, label="both (Suzuki)")
for p, mc in ((0.1, lb.combined_margin_db(8, 0.1)), (0.01, lb.combined_margin_db(8, 0.01))):
    ax.plot(mc, p, "o", color="k", ms=4)
    ax.annotate(f"{mc:.1f} dB for {p:.0%}", (mc, p), textcoords="offset points", xytext=(6, 4), fontsize=8)
ax.set_xlim(0, 40)
ax.set_ylim(1e-3, 1)
ax.set_xlabel("margin above the threshold (dB)")
ax.set_ylabel("outage probability")
ax.set_title("Combined margins are far below the sum of the parts", fontsize=10)
ax.legend(loc="lower left", fontsize=8)
save(fig, f"{OUT}/margins.svg")
