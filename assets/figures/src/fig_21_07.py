#!/usr/bin/env python3
"""Figures for chapter 21-07 (power amplifiers).

Run from anywhere:  python assets/figures/src/fig_21_07.py
Outputs
  assets/figures/21-07/backoff.svg   drain efficiency against output back-off for ideal class A, class B, the
                                     symmetric Doherty and envelope tracking (20 % floor, 85 % modulator), over the
                                     density of a 9.64 dB-PAPR OFDM envelope
  assets/figures/21-07/dpd.svg       output spectra of a Rapp-model PA (p = 2) driven by seeded 16-QAM OFDM with
                                     12 dB between average power and saturation, without and with a fifth-order
                                     indirect-learning predistorter
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import pa  # noqa: E402

OUT = "assets/figures/21-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- efficiency vs back-off
papr = 10 * math.log10(math.log(1e4))
bo = np.linspace(0, 25, 501)
x = 10 ** (-bo / 20)
fig, ax = plt.subplots(figsize=(5.8, 4.0))
u = bo
z = 10 ** ((papr - u) / 10)
dens = (math.log(10) / 10) * z * np.exp(-z)
ax2 = ax.twinx()
ax2.fill_between(u, 0, dens, color="0.85", lw=0)
ax2.set_ylim(0, dens.max() * 2.2)
ax2.set_yticks([])
ax2.text(3.2, dens.max() * 0.12, "OFDM envelope:\nprobability per dB", fontsize=8, color="0.4", ha="center")
ax.set_zorder(ax2.get_zorder() + 1)
ax.patch.set_visible(False)
curves = [("class A", [pa.eta_backoff("A", t) for t in x], PALETTE[3]),
          ("class B", [pa.eta_backoff("B", t) for t in x], PALETTE[0]),
          ("Doherty", [pa.eta_doherty(t) for t in x], PALETTE[1]),
          ("envelope tracking\n(20 % floor, 85 % modulator)", [0.85 * math.pi / 4 * t / max(t, 0.2) for t in x],
           PALETTE[2])]
for name, c, col in curves:
    ax.plot(bo, np.array(c) * 100, color=col, lw=1.6, label=name)
ax.axvline(papr, color="k", lw=0.6, ls=":")
ax.text(papr - 0.3, 92, "average power of a\n9.64 dB-PAPR signal", fontsize=8, ha="right")
ax.set_xlim(0, 25)
ax.set_ylim(0, 100)
ax.set_xlabel("output back-off from peak power (dB)")
ax.set_ylabel("efficiency (%) (ET includes modulator)")
ax.set_title("Efficiency where the signal actually spends its time", fontsize=10)
ax.legend(fontsize=8, loc="upper right")
save(fig, f"{OUT}/backoff.svg")

# ---------------------------------------------------------------- DPD spectra
X = pa.ofdm()
asat = 10 ** (12 / 20)
amp = lambda s: pa.rapp(s, 1.0, asat, 2.0)  # noqa: E731
y0 = amp(X)
y1 = amp(pa.dpd_loop(X, amp, iterations=4, orders=(1, 3, 5)))
fig, ax = plt.subplots(figsize=(5.8, 3.8))
f = np.arange(-512, 512) / 128          # in units of the channel bandwidth
for yy, lab_, col in ((y0, f"no DPD (ACLR {pa.aclr_db(y0):.1f} dBc)", PALETTE[3]),
                      (y1, f"fifth-order DPD (ACLR {pa.aclr_db(y1):.1f} dBc)", PALETTE[0])):
    S = np.fft.fftshift(np.mean(np.abs(np.fft.fft(yy.reshape(-1, 1024), axis=1)) ** 2, axis=0))
    ax.plot(f, 10 * np.log10(S / S.max()), color=col, lw=1.0, label=lab_)
ax.axvspan(0.5, 1.5, color="0.9", lw=0)
ax.text(1.0, -12, "adjacent\nchannel", ha="center", fontsize=8, color="0.35")
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-100, 5)
ax.set_xlabel("frequency offset (channel bandwidths)")
ax.set_ylabel("power spectral density (dB)")
ax.set_title("Predistortion pulls the spectral skirts down", fontsize=10)
ax.legend(fontsize=8, loc="lower center")
save(fig, f"{OUT}/dpd.svg")
