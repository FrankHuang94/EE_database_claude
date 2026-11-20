#!/usr/bin/env python3
"""Figures for chapter 16-07 (IIR filter design).

Run from anywhere:  python assets/figures/src/fig_16_07.py
Outputs
  assets/figures/16-07/warping.svg     the bilinear transform's frequency map at fs = 48 kHz: the digital frequency
                                       that each analog frequency lands on, against the identity line, with the
                                       prewarped band edges of the running example (4 and 5 kHz) marked
  assets/figures/16-07/iir-vs-fir.svg  the running specification (48 kHz; 0.1 dB to 4 kHz; 60 dB from 5 kHz) met by an
                                       elliptic (order 8), a Chebyshev I (order 14) and a Butterworth (order 38) IIR
                                       filter and by the 137-tap equiripple FIR of 16-06: magnitude in dB and
                                       passband group delay in samples
Uses labs/16-07-lab/iirdesign.py and labs/16-06-lab/firdesign.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
LABS = ROOT / "courses" / "16-digital-signal-processing" / "labs"
sys.path.insert(0, str(LABS / "16-07-lab"))
sys.path.insert(0, str(LABS / "16-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import iirdesign as iir  # noqa: E402
import firdesign as fd  # noqa: E402

OUT = "assets/figures/16-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
fs = 48000.0

# ------------------------------------------------------------------------------------------------ warping
fa = np.linspace(0, 60000, 2001)
fdig = np.array([iir.unwarp(2 * np.pi * f, fs) for f in fa])
fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(fa / 1000, fdig / 1000, color=PALETTE[0], label="bilinear: f_d = (f_s/π) arctan(π f_a / f_s)")
ax.plot([0, 24], [0, 24], color="0.5", ls="--", lw=0.8, label="no warping (f_d = f_a)")
ax.axhline(24, color="0.3", lw=0.8, ls=":")
ax.text(41, 22.6, "Nyquist, 24 kHz", fontsize=8, color="0.3")
for f, lab in ((4000, "4 kHz"), (5000, "5 kHz")):
    Wa = iir.prewarp(f, fs) / (2 * np.pi)
    ax.plot([Wa / 1000, Wa / 1000], [0, f / 1000], color=PALETTE[1], lw=0.8)
    ax.plot([0, Wa / 1000], [f / 1000, f / 1000], color=PALETTE[1], lw=0.8)
ax.annotate("prewarped edges\n4.094 and 5.186 kHz", xy=(5.19, 5.0), xytext=(14, 6), fontsize=8,
            arrowprops={"arrowstyle": "->", "color": "0.3"})
W20 = iir.unwarp(2 * np.pi * 20000, fs)
ax.plot([20], [W20 / 1000], "o", color=PALETTE[2])
ax.annotate("an analog 20 kHz edge\nlands at 14.03 kHz", xy=(20, W20 / 1000), xytext=(26, 11), fontsize=8,
            arrowprops={"arrowstyle": "->", "color": "0.3"})
ax.set_xlim(0, 60)
ax.set_ylim(0, 26)
ax.set_xlabel("analog frequency f_a (kHz)")
ax.set_ylabel("digital frequency f_d (kHz)")
ax.set_title("The bilinear transform squeezes the whole analog axis below Nyquist")
ax.legend(loc="lower right", fontsize=8)
save(fig, f"{OUT}/warping.svg")

# ------------------------------------------------------------------------------------------------ IIR vs FIR
w = np.linspace(1e-4, np.pi, 6001)
f = w * fs / (2 * np.pi) / 1000
designs = [("elliptic, order 8", signal.ellip(8, 0.1, 60, 4000, fs=fs, output="sos"), PALETTE[0]),
           ("Chebyshev I, order 14", signal.cheby1(14, 0.1, 4000, fs=fs, output="sos"), PALETTE[1]),
           ("Butterworth, order 38", None, PALETTE[2])]
zb, pb, kb = iir.bilinear(*iir.butter_analog(38, 0.1, iir.prewarp(4000, fs)), fs)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8))
for lab, sos, col in designs:
    if sos is None:
        H = iir.response(zb, pb, kb, w)
        gd = iir.group_delay(zb, pb, w)
    else:
        _, H = signal.sosfreqz(sos, worN=w)
        z, p, k = signal.sos2zpk(sos)
        gd = iir.group_delay(z, p, w)
    a1.plot(f, 20 * np.log10(np.maximum(np.abs(H), 1e-9)), color=col, lw=1.0, label=lab)
    m = f <= 4.0
    a2.plot(f[m], gd[m], color=col, lw=1.2, label=lab)
dp, ds = fd.deltas(0.1, 60)
hfir = fd.remez_lowpass(137, 2 * np.pi * 4000 / fs, 2 * np.pi * 5000 / fs, dp, ds)
_, Hf = signal.freqz(hfir, 1, worN=w)
a1.plot(f, 20 * np.log10(np.maximum(np.abs(Hf), 1e-9)), color=PALETTE[3], lw=0.8, label="FIR equiripple, 137 taps")
a2.plot([0, 4], [68, 68], color=PALETTE[3], lw=1.2, label="FIR, 68 samples")
a1.plot([5, 24], [-60, -60], color="k", lw=1.2)
a1.set_xlim(0, 12)
a1.set_ylim(-100, 5)
a1.set_xlabel("frequency (kHz)")
a1.set_ylabel("magnitude (dB)")
a1.set_title("Four filters, one specification")
a1.legend(loc="upper right", fontsize=7)
a2.set_xlim(0, 4.0)
a2.set_ylim(0, 120)
a2.set_xlabel("frequency (kHz)")
a2.set_ylabel("group delay (samples)")
a2.set_title("Passband group delay")
a2.legend(loc="upper left", fontsize=7)
fig.tight_layout(w_pad=2.0)
save(fig, f"{OUT}/iir-vs-fir.svg")
print("figures written to", OUT)
