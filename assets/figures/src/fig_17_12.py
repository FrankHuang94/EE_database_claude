#!/usr/bin/env python3
"""Figures for chapter 17-12 (multiple access, cellular and Wi-Fi).

Run from anywhere:  python assets/figures/src/fig_17_12.py
Outputs
  assets/figures/17-12/random-access.svg  left: throughput of pure and slotted ALOHA against offered load (analytic,
                                          with simulated points); right: CSMA/CA slot success and collision probability
                                          against the number of stations for W = 16 and for the optimal tau = 1/n
  assets/figures/17-12/schedulers.svg     per-user throughput of five Rayleigh users (mean SNR 20, 15, 10, 5, 0 dB)
                                          under round robin, max-SNR and proportional fair, with Jain's index
Uses labs/17-12-lab/access.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-12-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import access as ac  # noqa: E402

OUT = "assets/figures/17-12"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1712)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6))
G = np.linspace(0.01, 3, 300)
a1.plot(G, [ac.aloha(g) for g in G], color=PALETTE[0], label="pure ALOHA, Ge^(−2G)")
a1.plot(G, [ac.slotted_aloha(g) for g in G], color=PALETTE[1], label="slotted ALOHA, Ge^(−G)")
gs = np.array([0.25, 0.5, 1.0, 1.5, 2.0, 2.5])
a1.plot(gs, [ac.simulate_pure_aloha(g, 100_000, rng) for g in gs], "o", color=PALETTE[0], ms=4)
a1.plot(gs, [ac.simulate_slotted_aloha(g, 100_000, rng) for g in gs], "s", color=PALETTE[1], ms=4)
a1.set_xlabel("offered load G (attempts per packet time)")
a1.set_ylabel("throughput S")
a1.set_title("ALOHA peaks at 18% and 37%")
a1.legend(fontsize=7)
n = np.arange(2, 61)
t16 = ac.tau_from_window(16)
a2.plot(n, [ac.slot_outcomes(k, t16)[1] for k in n], color=PALETTE[2], label="success, W = 16")
a2.plot(n, [ac.slot_outcomes(k, t16)[2] for k in n], color=PALETTE[3], label="collision, W = 16")
a2.plot(n, [ac.slot_outcomes(k, 1 / k)[1] for k in n], color=PALETTE[2], ls="--", label="success, τ = 1/n")
a2.axhline(1 / np.e, color="0.6", ls=":", lw=1)
a2.set_xlabel("number of contending stations n")
a2.set_ylabel("probability per slot")
a2.set_title("CSMA/CA: a fixed window collapses as n grows")
a2.legend(fontsize=7)
fig.tight_layout()
save(fig, f"{OUT}/random-access.svg")

res = ac.simulate_schedulers([20, 15, 10, 5, 0], 40_000, rng)
fig, ax = plt.subplots(figsize=(6.6, 3.8))
x = np.arange(5)
w = 0.26
for i, (key, lab) in enumerate((("rr", "round robin"), ("max", "max-SNR"), ("pf", "proportional fair"))):
    ax.bar(x + (i - 1) * w, res[key], w, color=PALETTE[i], label=f"{lab}: sum {res[key].sum():.2f}, Jain {ac.jain(res[key]):.2f}")
ax.set_xticks(x)
ax.set_xticklabels(["20 dB", "15 dB", "10 dB", "5 dB", "0 dB"])
ax.set_xlabel("user (mean SNR)")
ax.set_ylabel("throughput (b/s/Hz)")
ax.set_title("Max-SNR maximizes the sum by starving the edge; PF shares")
ax.legend(fontsize=7)
save(fig, f"{OUT}/schedulers.svg")
