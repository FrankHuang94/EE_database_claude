#!/usr/bin/env python3
"""Figures for chapter 20-10 (PLLs and jitter).

Run from anywhere:  python assets/figures/src/fig_20_10.py
Outputs
  assets/figures/20-10/bode.svg      open-loop gain and phase of the loop of Example 20-10.2, with crossover and margin
  assets/figures/20-10/noise.svg     output phase noise of that loop: reference (-150 dBc/Hz x N^2) and VCO
                                     (-120 dBc/Hz at 1 MHz, -20 dB/decade) contributions and their sum
  assets/figures/20-10/mash.svg      phase-error spectra of a MASH 1-1-1 divider for 123/500 (spurs) and for a busy
                                     fraction, with the formula of section 3.6
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
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-10-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import pll  # noqa: E402

OUT = "assets/figures/20-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
ICP, KV, N = 500e-6, 2 * np.pi * 500e6, 100
R, C1, C2 = pll.design_third_order(2e6, 10, ICP, KV, N)
fc, pm = pll.crossover_and_pm(ICP, KV, N, R, C1, C2)

# ---------------------------------------------------------------- figure 2: Bode
f = np.logspace(4, 8, 2000)
g = pll.open_loop(2 * np.pi * f, ICP, KV, N, R, C1, C2)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 4.8), sharex=True)
a1.semilogx(f, 20 * np.log10(np.abs(g)), color=PALETTE[0], lw=1.4)
a1.axhline(0, color="0.5", lw=0.7)
a1.axvline(fc, color="0.5", lw=0.7, ls=":")
a1.set_ylabel("|G| (dB)")
a1.set_title("Open loop of Example 20-10.2: crossover 2 MHz", fontsize=9)
ph = np.degrees(np.angle(g))
ph = np.where(ph > 0, ph - 360, ph)
a2.semilogx(f, ph, color=PALETTE[1], lw=1.4)
a2.axhline(-180, color="0.5", lw=0.7)
a2.axvline(fc, color="0.5", lw=0.7, ls=":")
a2.annotate(f"phase margin {pm:.1f}°", xy=(fc, -180 + pm), xytext=(fc * 2.5, -150), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.7))
for fz in (1 / (2 * np.pi * R * C1), (C1 + C2) / (2 * np.pi * R * C1 * C2)):
    a2.axvline(fz, color="0.75", lw=0.6, ls="--")
a2.set_ylabel("phase (°)")
a2.set_xlabel("frequency (Hz)")
a2.set_ylim(-190, -100)
save(fig, f"{OUT}/bode.svg")

# ---------------------------------------------------------------- figure 3: noise split
f = np.logspace(3, 9, 3000)
href, hvco = pll.closed_loop(2 * np.pi * f, ICP, KV, N, R, C1, C2)
lref = 10 ** (-150 / 10) * N ** 2 * np.abs(href / N) ** 2
lvco = 10 ** (-120 / 10) * (1e6 / f) ** 2 * np.abs(hvco) ** 2
fig, ax = plt.subplots(figsize=(6.4, 3.9))
ax.semilogx(f, 10 * np.log10(lref), color=PALETTE[0], lw=1.2, label="reference × N², low-pass")
ax.semilogx(f, 10 * np.log10(lvco), color=PALETTE[1], lw=1.2, label="VCO, high-pass")
ax.semilogx(f, 10 * np.log10(lref + lvco), color="0.15", lw=1.6, ls="--", label="total")
ax.semilogx(f, -120 + 20 * np.log10(1e6 / f), color=PALETTE[1], lw=0.7, ls=":", label="free-running VCO")
ax.axvline(fc, color="0.6", lw=0.7)
ax.set_ylim(-170, -80)
ax.set_xlabel("offset frequency (Hz)")
ax.set_ylabel("phase noise (dBc/Hz)")
ax.legend(fontsize=7, loc="lower left")
save(fig, f"{OUT}/noise.svg")

# ---------------------------------------------------------------- figure 4: MASH spectra
fref = 50e6
fig, ax = plt.subplots(figsize=(6.4, 3.9))
for k, mod, lab, col in ((123, 500, "fraction 123/500 (period 1000)", PALETTE[1]),
                         (2 ** 23 + 12345, 2 ** 25, "busy fraction", PALETTE[0])):
    c = pll.mash_sequence(k, mod, 2 ** 18)
    phi = 2 * np.pi * np.cumsum(c - c.mean())
    phi -= phi.mean()
    ff, p = signal.welch(phi, fs=fref, window="blackmanharris", nperseg=2 ** 15, return_onesided=False)
    sel = ff > 0
    ax.semilogx(ff[sel], 10 * np.log10(p[sel] + 1e-30), color=col, lw=0.6, label=lab)
fs_ = np.logspace(4, math.log10(fref / 2), 400)
ax.semilogx(fs_, 10 * np.log10(pll.divider_phase_psd(fs_, fref, 3)), color="0.1", lw=1.2, ls="--", label="formula, §3.6")
ax.set_xlim(3e4, fref / 2)
ax.set_ylim(-200, -40)
ax.set_xlabel("offset frequency (Hz)")
ax.set_ylabel("divider phase noise (dBc/Hz)")
ax.legend(fontsize=7, loc="lower right")
save(fig, f"{OUT}/mash.svg")
print("figures written to", OUT)
