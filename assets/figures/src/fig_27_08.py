#!/usr/bin/env python3
"""Figures for chapter 27-08 (edge AI and IoT).

Run from anywhere:  python assets/figures/src/fig_27_08.py
Outputs
  assets/figures/27-08/lora-life.svg  left: time on air of a 20-byte LoRa packet (125 kHz, CR 4/5,
                                      8-symbol preamble, explicit header, CRC) against spreading
                                      factor, with the packets per hour a 1% duty cycle allows;
                                      right: battery life with self-discharge against reporting
                                      interval for SF7 and SF12, with Example 27-08.4's assumed
                                      node (2.6 Ah at 3.6 V, 80% usable, 1%/year self-discharge,
                                      10 uW sleep)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "27-system-architectures" / "labs" / "27-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import edgemodel as em  # noqa: E402

OUT = "assets/figures/27-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

sfs = np.arange(7, 13)
toa = np.array([em.lora_time_on_air_s(20, sf) for sf in sfs])
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0))
ax1.bar(sfs, 1e3 * toa, color=PALETTE[0], width=0.6, label="time on air")
ax1.set_yscale("log")
ax1.set_xlabel("spreading factor")
ax1.set_ylabel("time on air of a 20-byte packet (ms)")
ax1.set_title("Each SF step doubles the airtime", fontsize=10)
ax1.grid(True, alpha=0.3, which="both", axis="y")
axr = ax1.twinx()
axr.plot(sfs, [em.max_messages(36, t) for t in toa], "o-", color=PALETTE[1], label="packets per hour at 1%")
axr.set_yscale("log")
axr.set_ylabel("packets per hour at 1% duty cycle")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = axr.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, fontsize=8, loc="center left")

V = 3.3
usable = 0.8 * 2.6 * 3.6 * 3600
sd_day = 0.01 * 2.6 * 3.6 * 3600 / 365


def msg(sf):
    t = em.lora_time_on_air_s(20, sf)
    ts = em.lora_symbol_s(sf, 125e3)
    return t * 0.029 * V + 2 * 5 * ts * 0.0108 * V + 0.005 * V * 0.05


minutes = np.logspace(0, np.log10(24 * 60), 200)
for k, sf in enumerate((7, 12)):
    life = [usable / ((1440 / m) * msg(sf) + 10e-6 * 86400 + sd_day) / 365 for m in minutes]
    ax2.plot(minutes, life, color=PALETTE[k + 2], label=f"SF{sf}")
ax2.axvline(15, color="0.5", ls=":", lw=1)
ax2.text(16, 1.2, "15 min", fontsize=8, color="0.4")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel("reporting interval (min)")
ax2.set_ylabel("battery life with self-discharge (years)")
ax2.set_title("Life is set by SF, interval and the cell", fontsize=10)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3, which="both")
fig.tight_layout()
save(fig, f"{OUT}/lora-life.svg")
