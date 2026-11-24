#!/usr/bin/env python3
"""Figures for chapter 21-04 (low-noise amplifiers).

Run from anywhere:  python assets/figures/src/fig_21_04.py
Outputs
  assets/figures/21-04/gate-q.svg           noise figure of Example 21-04.2's LNA (2.4 GHz, g_m = 40 mS,
                                            f_T = 12 GHz, gamma/alpha = 1) against the gate inductor's Q, with the
                                            input re-matched at each Q; the lossless value and Example 21-04.3's
                                            three cases marked
  assets/figures/21-04/noise-cancelling.svg noise figure of the CG-CS noise-cancelling LNA (R2 = 200 ohm,
                                            R1 at cancellation, gamma/alpha = 2/3) against g_m2, with the
                                            common-gate limit 1 + gamma/alpha
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import lna  # noqa: E402

OUT = "assets/figures/21-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
db = lambda x: 10 * math.log10(x)  # noqa: E731
F0, GM, FT = 2.4e9, 0.04, 12e9


def nf_q(q):
    _, rg = lna.design_with_gate_q(F0, GM, FT, q)
    return db(lna.nf_ind_degen(1, GM, F0, FT, rg=rg))


qs = np.logspace(math.log10(5), 2.3, 300)
fig, ax = plt.subplots(figsize=(6.0, 3.8))
ax.plot(qs, [nf_q(q) for q in qs], color=PALETTE[0], lw=1.6, label="re-matched LNA")
ax.axhline(db(lna.nf_ind_degen(1, GM, F0, FT)), color="0.4", lw=0.9, ls="--")
ax.text(5.5, db(lna.nf_ind_degen(1, GM, F0, FT)) - 0.14, "ideal inductor, 0.33 dB", fontsize=8, color="0.3")
for q in (10, 15, 30):
    ax.plot([q], [nf_q(q)], "o", color="k", ms=4)
    ax.annotate(f"Q = {q}: {nf_q(q):.2f} dB", (q, nf_q(q)), textcoords="offset points", xytext=(6, 4), fontsize=8)
ax.set_xscale("log")
ax.set_ylim(0, 2.4)
ax.set_xlabel("gate inductor Q")
ax.set_ylabel("noise figure (dB)")
ax.set_title("The gate inductor, not the transistor, sets the noise figure", fontsize=10)
save(fig, f"{OUT}/gate-q.svg")

g2 = np.linspace(0.02, 0.3, 300)
fig, ax = plt.subplots(figsize=(6.0, 3.8))
ax.plot(g2 * 1e3, [db(lna.nf_noise_cancelling(2 / 3, g, 200)) for g in g2], color=PALETTE[1], lw=1.6,
        label="noise-cancelling LNA (R1 at cancellation)")
ax.axhline(db(lna.nf_common_gate(2 / 3, 0.02)), color=PALETTE[0], lw=1.2, ls="--",
           label="common gate alone, 1 + γ/α")
ax.plot([100], [db(lna.nf_noise_cancelling(2 / 3, 0.1, 200))], "o", color="k", ms=4)
ax.annotate("Example 21-04.5", (100, db(lna.nf_noise_cancelling(2 / 3, 0.1, 200))), textcoords="offset points",
            xytext=(6, 6), fontsize=8)
ax.set_ylim(0, 3)
ax.set_xlabel("g_m2 of the common-source path (mS)")
ax.set_ylabel("noise figure (dB)")
ax.legend(fontsize=8, loc="upper right")
ax.set_title("Cancelling the matching device's noise: current buys noise figure", fontsize=10)
save(fig, f"{OUT}/noise-cancelling.svg")
