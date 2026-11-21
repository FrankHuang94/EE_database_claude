#!/usr/bin/env python3
"""Figures for chapter 17-02 (noise and SNR in communication systems).

Run from anywhere:  python assets/figures/src/fig_17_02.py
Outputs
  assets/figures/17-02/noise-floor.svg  kT0 B + NF against bandwidth for NF = 0, 5 and 10 dB, with published
                                        sensitivity levels placed at their occupied bandwidths (GPS L1 C/A minimum
                                        power, NR base-station and UE REFSENS, Wi-Fi 20 MHz minimum sensitivities)
  assets/figures/17-02/cascade.svg      left: cumulative cascade noise figure, stage by stage, for Example 17-02.3's
                                        two orderings; right: cascade NF of a 1 dB LNA ahead of a 23 dB-NF ADC
                                        against LNA gain (Problem 17-02.13)
Uses labs/17-02-lab/noisebudget.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import noisebudget as nb  # noqa: E402

OUT = "assets/figures/17-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------ 1. noise floor and published sensitivities
B = np.logspace(2, 9, 300)
fig, ax = plt.subplots(figsize=(6.8, 4.0))
for nf, col in ((0, PALETTE[2]), (5, PALETTE[0]), (10, PALETTE[1])):
    ax.semilogx(B, nb.ktb_dbm(1.0) + 10 * np.log10(B) + nf, color=col, label=f"kT₀B + NF, NF = {nf} dB")
points = [
    (2.046e6, -128.5, "GPS L1 C/A minimum (−128.5 dBm)"),
    (4.5e6, -101.7, "NR base station REFSENS, 25 RB"),
    (9.36e6, -95.8, "NR phone REFSENS, n78 10 MHz"),
    (17.5e6, -82.0, "Wi-Fi 20 MHz, BPSK 1/2"),
    (17.5e6, -57.0, "Wi-Fi 20 MHz, 256-QAM 5/6"),
]
for (bw, p, lab), mk in zip(points, ("v", "s", "D", "o", "^")):
    ax.plot(bw, p, mk, color="0.15", ms=6, label=lab)
ax.set_xlabel("noise bandwidth (Hz)")
ax.set_ylabel("power (dBm)")
ax.set_ylim(-160, -40)
ax.set_title("Sensitivity sits above kT₀B + NF by the required SNR; GPS sits below")
ax.legend(fontsize=7, loc="upper left")
save(fig, f"{OUT}/noise-floor.svg")

# ------------------------------------------------------------------ 2. cascades
L = 1.5
cable = (10 ** (L / 10), 10 ** (-L / 10))
lna = (10 ** 0.06, 10 ** 2.02)
rx = (10 ** 0.8, 1.0)
orders = {"cable, LNA, receiver": [cable, lna, rx], "LNA, cable, receiver": [lna, cable, rx]}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.4))
for (name, st), col in zip(orders.items(), (PALETTE[1], PALETTE[0])):
    cum = [10 * np.log10(nb.friis(st[: i + 1])[0]) for i in range(len(st))]
    a1.plot([1, 2, 3], cum, "o-", color=col, label=f"{name}: {cum[-1]:.2f} dB")
a1.set_xticks([1, 2, 3], ["after stage 1", "after stage 2", "after stage 3"])
a1.set_ylabel("cascade noise figure (dB)")
a1.set_ylim(0, 3)
a1.set_title("Example 17-02.3: LNA at the antenna")
a1.legend(fontsize=7, loc="lower right")
g = np.linspace(0, 40, 401)
nfc = 10 * np.log10(10 ** 0.1 + (10 ** 2.3 - 1) / 10 ** (g / 10))
a2.plot(g, nfc, color=PALETTE[0])
a2.axhline(2, color="0.5", ls=":", lw=0.8)
g2 = 10 * np.log10((10 ** 2.3 - 1) / (10 ** 0.2 - 10 ** 0.1))
a2.plot(g2, 2, "o", color=PALETTE[1])
a2.annotate(f"{g2:.2f} dB of gain\nfor a 2 dB cascade", xy=(g2, 2), xytext=(g2 - 3, 9), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.6))
a2.set_xlabel("LNA gain (dB)")
a2.set_ylabel("cascade noise figure (dB)")
a2.set_ylim(0, 24)
a2.set_title("1 dB LNA ahead of a 23 dB-NF ADC")
fig.tight_layout()
save(fig, f"{OUT}/cascade.svg")
