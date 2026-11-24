#!/usr/bin/env python3
"""Figures for chapter 21-12 (modem baseband and standards).

Run from anywhere:  python assets/figures/src/fig_21_12.py
Outputs
  assets/figures/21-12/ranging.svg  time-of-flight profiles (inverse FFT of the channel's frequency samples) of a 12 m path
                                    plus a half-amplitude reflection at 20 m, as seen by a 72 MHz Bluetooth Channel
                                    Sounding sweep and by a 499.2 MHz UWB channel
  assets/figures/21-12/doppler.svg  Doppler shift at 2 GHz for a user under the ground track of a 600 km satellite pass,
                                    against time from closest approach
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-12-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import modem as m  # noqa: E402

OUT = "assets/figures/21-12"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- ranging resolution
fig, ax = plt.subplots(figsize=(5.8, 3.8))
for bw, step, col, lab_ in ((72e6, 1e6, PALETTE[1], "Bluetooth CS sweep, 72 MHz"), (499.2e6, 1e6, PALETTE[0], "UWB channel, 499.2 MHz")):
    fr = 6e9 + np.arange(int(round(bw / step))) * step
    h = np.exp(-1j * 4 * np.pi * fr * 12 / m.C0) + 0.5 * np.exp(-1j * 4 * np.pi * fr * 20 / m.C0)
    n = len(fr) * 16
    prof = np.abs(np.fft.ifft(h * np.hanning(len(fr)), n))
    dist = np.arange(n) / (n * step) * m.C0 / 2
    ax.plot(dist, prof / prof.max(), color=col, lw=1.5, label=lab_)
for d, txt in ((12, "direct path, 12 m"), (20, "reflection, 20 m")):
    ax.axvline(d, color="0.5", lw=0.8, ls=":")
    ax.text(d + 0.3, 1.02, txt, fontsize=7.5, color="0.35")
ax.set_xlim(0, 35)
ax.set_ylim(0, 1.12)
ax.set_xlabel("distance (m)")
ax.set_ylabel("normalized time-of-flight profile")
ax.set_title("Bandwidth sets how well ranging separates reflections", fontsize=10)
ax.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.0, 0.92))
save(fig, f"{OUT}/ranging.svg")

# ---------------------------------------------------------------- Doppler over a pass
h, f = 600e3, 2e9
v = math.sqrt(m.GM / (m.R_E + h))
w = v / (m.R_E + h)
t = np.linspace(-450, 450, 1801)
th = w * t
sx, sy = (m.R_E + h) * np.sin(th), (m.R_E + h) * np.cos(th)
rng_ = np.hypot(sx, sy - m.R_E)
elev = np.degrees(np.arctan2(sy - m.R_E, np.abs(sx)))
rr = np.gradient(rng_, t)
fd = -f * rr / m.C0
vis = elev > 10
fig, ax = plt.subplots(figsize=(5.8, 3.8))
ax.plot(t[vis], fd[vis] / 1e3, color=PALETTE[0], lw=1.6)
ax.axhline(0, color="0.6", lw=0.8)
ax.set_xlabel("time from closest approach (s), elevation above 10°")
ax.set_ylabel("Doppler at 2 GHz (kHz)")
ax.set_title(f"A 600 km pass overhead: ±45 kHz over {(t[vis][-1] - t[vis][0]) / 60:.1f} minutes above 10°", fontsize=10)
save(fig, f"{OUT}/doppler.svg")
