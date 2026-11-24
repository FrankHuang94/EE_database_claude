#!/usr/bin/env python3
"""Figures for chapter 21-05 (mixers).

Run from anywhere:  python assets/figures/src/fig_21_05.py
Outputs
  assets/figures/21-05/irr.svg     image-rejection ratio of a quadrature receiver against gain error (0-5 %) and
                                   phase error (0-5 degrees), exact formula, with 30, 40 and 50 dB contours
  assets/figures/21-05/hr-lo.svg   one period of a square-wave LO and of the harmonic-reject composite LO (weights
                                   1, sqrt 2, 1 at -45, 0, +45 degrees), and their harmonic amplitudes to the 9th
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import mixer  # noqa: E402

OUT = "assets/figures/21-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

eps = np.linspace(0.0005, 0.05, 200)
th = np.linspace(0.05, 5, 200)
E, TH = np.meshgrid(eps, th)
a = 1 + E
c = np.cos(np.radians(TH))
irr = 10 * np.log10((1 + 2 * a * c + a * a) / (1 - 2 * a * c + a * a))
fig, ax = plt.subplots(figsize=(5.6, 4.2))
cs = ax.contour(E * 100, TH, irr, levels=[25, 30, 35, 40, 45, 50], colors=[PALETTE[0]] * 6, linewidths=1.1)
ax.clabel(cs, fmt="%d dB", fontsize=8)
ax.plot([1], [1], "o", color="k", ms=4)
ax.annotate("1 %, 1°: 40 dB", (1, 1), textcoords="offset points", xytext=(6, 6), fontsize=8)
ax.plot([2], [2], "o", color="k", ms=4)
ax.annotate("Example 21-05.3", (2, 2), textcoords="offset points", xytext=(6, 6), fontsize=8)
ax.set_xlabel("gain error ε (%)")
ax.set_ylabel("phase error θ (degrees)")
ax.set_title("Image rejection is set by I/Q matching", fontsize=10)
save(fig, f"{OUT}/irr.svg")

t = np.linspace(0, 1, 2000, endpoint=False)
sq = np.sign(np.cos(2 * np.pi * t))
hr = sum(w * np.sign(np.cos(2 * np.pi * t - math.radians(ph))) for ph, w in mixer.hr_weights())
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2))
ax1.plot(t, sq, color=PALETTE[0], lw=1.2, label="square wave")
ax1.plot(t, hr / (2 + math.sqrt(2)), color=PALETTE[1], lw=1.2, label="harmonic-reject LO (scaled)")
ax1.set_xlabel("time (LO periods)")
ax1.set_ylabel("LO")
ax1.legend(fontsize=7, loc="lower left")
hs = mixer.composite_lo_harmonics([(0.0, 1.0)], nmax=9)
hh = mixer.composite_lo_harmonics(mixer.hr_weights(), nmax=9)
n = np.arange(1, 10, 2)
ax2.bar(n - 0.2, [hs[k] for k in n], width=0.4, color=PALETTE[0], label="square wave")
ax2.bar(n + 0.2, [hh[k] for k in n], width=0.4, color=PALETTE[1], label="harmonic-reject")
ax2.set_xticks(n)
ax2.set_xlabel("harmonic")
ax2.set_ylabel("relative amplitude")
ax2.legend(fontsize=7)
fig.suptitle("Three weighted phases cancel the 3rd and 5th harmonics", fontsize=10)
save(fig, f"{OUT}/hr-lo.svg")
