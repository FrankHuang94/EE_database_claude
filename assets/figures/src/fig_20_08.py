#!/usr/bin/env python3
"""Figures for chapter 20-08 (oversampling and sigma-delta converters).

Run from anywhere:  python assets/figures/src/fig_20_08.py
Outputs
  assets/figures/20-08/spectra.svg    output spectra of the lab's first- and second-order 1-bit modulators (-6 dBFS,
                                      65,536 points, Hann window) with 20 and 40 dB/decade guides and the OSR-64 band edge
  assets/figures/20-08/sqnr_osr.svg   SQNR against OSR: linear model (lines) and simulation (points), first and second
                                      order, -6 dBFS
  assets/figures/20-08/ntf.svg        |NTF| of (1 - z^-1)^L for L = 1, 2, 4 and of the Lee-rule (peak 1.5) NTFs for L = 3, 4
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dsm  # noqa: E402

OUT = "assets/figures/20-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
N = 2 ** 16


def sine(osr, amp=0.5):
    m = int(N / (2 * osr) / 3) | 1
    return amp * np.sin(2 * np.pi * m * np.arange(N) / N), m


# ---------------------------------------------------------------- figure 2: spectra
x, m = sine(64)
f = np.arange(N // 2 + 1) / N
win = np.hanning(N)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
for y, col, lab in ((dsm.mod1(x)[0], PALETTE[1], "first order"), (dsm.mod2(x)[0], PALETTE[0], "second order")):
    p = np.abs(np.fft.rfft(y * win)) ** 2
    ref = np.abs(np.fft.rfft(np.sin(2 * np.pi * m * np.arange(N) / N) * win)).max() ** 2
    ax.semilogx(f[1:], 10 * np.log10(p[1:] / ref + 1e-30), color=col, lw=0.4, label=lab)
ff = np.array([3e-4, 3e-3])
ax.semilogx(ff, [-140, -120], color="0.2", ls="--", lw=1.0)
ax.semilogx(ff, [-175, -135], color="0.2", ls="--", lw=1.0)
ax.text(2.2e-4, -137, "20 dB/decade", fontsize=7, color="0.2", ha="right")
ax.text(2.2e-4, -172, "40 dB/decade", fontsize=7, color="0.2", ha="right")
ax.axvline(1 / 128, color="0.5", lw=0.8)
ax.text(1 / 128 * 1.08, -165, "band edge, OSR 64", fontsize=7, color="0.3", rotation=90, va="bottom")
ax.set_xlim(f[1], 0.5)
ax.set_ylim(-180, 5)
ax.set_xlabel("frequency / $f_s$")
ax.set_ylabel("power (dBFS, per bin)")
ax.set_title("1-bit modulators, −6 dBFS sine: noise pushed out of band")
leg = ax.legend(loc="lower right", fontsize=8)
for line in leg.get_lines():
    line.set_linewidth(2.0)
save(fig, f"{OUT}/spectra.svg")

# ---------------------------------------------------------------- figure 3: SQNR against OSR
osrs = [16, 32, 64, 128, 256]
fig, ax = plt.subplots(figsize=(6.2, 4.0))
grid = np.logspace(np.log10(16), np.log10(256), 50)
for order, col in ((1, PALETTE[1]), (2, PALETTE[0])):
    ax.semilogx(grid, [dsm.sqnr_formula(order, o, 0.5) for o in grid], color=col, lw=1.2, label=f"L = {order}, linear model")
    sims = []
    for o in osrs:
        xx, mm = sine(o)
        y = dsm.mod1(xx)[0] if order == 1 else dsm.mod2(xx)[0]
        sims.append(dsm.inband_sqnr(y, mm, o))
    ax.semilogx(osrs, sims, "o", color=col, ms=5, label=f"L = {order}, simulated")
ax.set_xticks(osrs)
ax.set_xticklabels([str(o) for o in osrs])
ax.xaxis.set_minor_formatter(plt.NullFormatter())
ax.set_xlabel("oversampling ratio")
ax.set_ylabel("SQNR (dB), −6 dBFS")
ax.set_title("9 and 15 dB per octave: model against simulation")
ax.legend(fontsize=8)
save(fig, f"{OUT}/sqnr_osr.svg")

# ---------------------------------------------------------------- figure 4: NTF magnitudes
w = np.linspace(1e-4, np.pi, 4000)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
for order, col in ((1, PALETTE[0]), (2, PALETTE[1]), (4, "0.35")):
    _, h = signal.freqz(np.poly(np.ones(order)), [1.0], worN=w)
    ax.semilogx(w / (2 * np.pi), 20 * np.log10(np.abs(h)), lw=1.0, ls=":", color=col,
                label=f"$(1 - z^{{-1}})^{order}$, peak {2 ** order}")
for order, col in ((3, PALETTE[2]), (4, PALETTE[3])):
    b, a = dsm.lee_ntf(order)
    _, h = signal.freqz(b, a, worN=w)
    ax.semilogx(w / (2 * np.pi), 20 * np.log10(np.abs(h)), lw=1.4, color=col, label=f"L = {order}, Lee rule (peak 1.5)")
ax.axhline(20 * math.log10(1.5), color="0.5", lw=0.6, ls="--")
ax.axvline(1 / 128, color="0.5", lw=0.8)
ax.set_xlim(1e-3, 0.5)
ax.set_ylim(-120, 30)
ax.set_xlabel("frequency / $f_s$")
ax.set_ylabel("|NTF| (dB)")
ax.set_title("Noise transfer functions: limiting the peak gain costs in-band suppression")
ax.legend(fontsize=7, loc="lower right")
save(fig, f"{OUT}/ntf.svg")
print("figures written to", OUT)
