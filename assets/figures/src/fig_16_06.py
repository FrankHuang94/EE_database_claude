#!/usr/bin/env python3
"""Figures for chapter 16-06 (FIR filter design).

Run from anywhere:  python assets/figures/src/fig_16_06.py
Outputs
  assets/figures/16-06/gibbs.svg          amplitude response of the truncated ideal half-band low-pass (cutoff pi/2)
                                          with a rectangular window for M = 20 and M = 100, and with a Hamming window
                                          for M = 20: the overshoot does not shrink with M, the taper removes it
  assets/figures/16-06/kaiser-vs-pm.svg   Examples 16-06.3 and 16-06.5: the Kaiser-window design (175 taps) and the
                                          equiripple design (137 taps) for the 48 kHz spec (pass 0-4 kHz within
                                          0.1 dB, stop above 5 kHz by 60 dB), magnitude in dB with the spec mask,
                                          and the passband ripple on an expanded scale
Uses labs/16-06-lab/firdesign.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import firdesign as fd  # noqa: E402

OUT = "assets/figures/16-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------------------------ Gibbs
w = np.linspace(0, np.pi, 4001)
fig, ax = plt.subplots(figsize=(7.0, 3.8))
for M, name, col, lab in ((20, "rect", PALETTE[0], "rectangular, M = 20"),
                          (100, "rect", PALETTE[1], "rectangular, M = 100"),
                          (20, "hamming", PALETTE[2], "Hamming, M = 20")):
    h = fd.ideal_lowpass(M, np.pi / 2) * fd.window(name, M)
    ax.plot(w / np.pi, fd.amplitude(h, w), color=col, label=lab)
ax.axhline(1.0895, color="0.5", lw=0.8, ls="--")
ax.text(0.02, 1.105, "1.0895 (Gibbs limit)", fontsize=8, color="0.35")
ax.axvline(0.5, color="0.5", lw=0.8, ls=":")
ax.set_xlabel("frequency ω/π")
ax.set_ylabel("amplitude response A(ω)")
ax.set_xlim(0, 1)
ax.set_ylim(-0.15, 1.18)
ax.set_title("Truncating the ideal low-pass: the overshoot stays, a taper removes it")
ax.legend(loc="lower left", fontsize=8)
save(fig, f"{OUT}/gibbs.svg")

# ------------------------------------------------------------------------------------------- Kaiser vs PM
fs = 48000.0
wp, ws = 2 * np.pi * 4000 / fs, 2 * np.pi * 5000 / fs
dp, ds = fd.deltas(0.1, 60)
hk = fd.window_lowpass(174, wp, ws, "kaiser", fd.kaiser_beta(60))
hp = fd.remez_lowpass(137, wp, ws, dp, ds)
w = np.linspace(0, np.pi, 8001)
f = w * fs / (2 * np.pi) / 1000
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6), gridspec_kw={"width_ratios": [1.6, 1]})
for h, col, lab in ((hk, PALETTE[0], "Kaiser window, 175 taps"), (hp, PALETTE[1], "equiripple, 137 taps")):
    A = np.abs(fd.amplitude(h, w))
    a1.plot(f, 20 * np.log10(np.maximum(A, 1e-9)), color=col, lw=1.0, label=lab)
    a2.plot(f, 20 * np.log10(np.maximum(A, 1e-9)), color=col, lw=1.2, label=lab)
a1.plot([5, 24], [-60, -60], color="k", lw=1.2)
a1.plot([0, 4], [-0.1, -0.1], color="k", lw=1.2)
a1.set_xlim(0, 24)
a1.set_ylim(-110, 5)
a1.set_xlabel("frequency (kHz)")
a1.set_ylabel("magnitude (dB)")
a1.set_title("Spec: 0.1 dB to 4 kHz, 60 dB above 5 kHz")
a1.legend(loc="upper right", fontsize=8)
pk = 20 * np.log10(1 + dp)
a2.axhline(pk, color="k", lw=0.8, ls="--")
a2.axhline(20 * np.log10(1 - dp), color="k", lw=0.8, ls="--")
a2.set_xlim(0, 4.2)
a2.set_ylim(-0.07, 0.07)
a2.set_xlabel("frequency (kHz)")
a2.set_ylabel("magnitude (dB)")
a2.set_title("Passband, expanded")
fig.tight_layout(w_pad=2.0)
save(fig, f"{OUT}/kaiser-vs-pm.svg")
print("figures written to", OUT)
