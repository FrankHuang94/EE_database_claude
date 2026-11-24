#!/usr/bin/env python3
"""Figures for chapter 20-09 (DACs).

Run from anywhere:  python assets/figures/src/fig_20_09.py
Outputs
  assets/figures/20-09/segmentation.svg  DNL of one seeded 14-bit DAC (sigma_u = 0.5%) built binary and 6 + 8 segmented,
                                         from the same unit errors' statistics; the INL is statistically the same
  assets/figures/20-09/zout_sfdr.svg     single-ended HD2 and differential HD3 against output frequency for a 12-bit
                                         DAC into 25 ohm whose cells have 1 fF of code-dependent capacitance
  assets/figures/20-09/pulses.svg        NRZ, RZ and mixed-mode pulse responses from DC to 2 fs, with the first
                                         Nyquist zone shaded and an example signal and image at 0.4 and 0.6 fs
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import dac  # noqa: E402

OUT = "assets/figures/20-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- figure 2: segmentation
fig, axs = plt.subplots(2, 1, figsize=(6.6, 4.6), sharex=True)
for ax, (m, title, col) in zip(axs, ((0, "binary", PALETTE[1]), (6, "6 + 8 segmented", PALETTE[0]))):
    lv = dac.cs_levels(14, m, 0.005, np.random.default_rng(2090))
    _, dnl = dac.inl_dnl(lv)
    ax.plot(np.arange(1, 2 ** 14), dnl, color=col, lw=0.4)
    ax.set_ylabel("DNL (LSB)")
    ax.set_title(f"14-bit current-steering DAC, σ_u = 0.5%: {title}", fontsize=9)
    ax.set_ylim(-1.6, 1.6)
axs[-1].set_xlabel("code")
save(fig, f"{OUT}/segmentation.svg")

# ---------------------------------------------------------------- figure 3: SFDR against frequency
N = 4095
freqs = np.logspace(6, 9.3, 40)
hd2, hd3 = [], []
for f in freqs:
    x = 25 * 2 * math.pi * f * 1e-15
    se = lambda s, x=x: (N * (1 + s) / 2) / (1 + N * (1 + s) / 2 * x)  # noqa: E731
    df = lambda s, x=x, se=se: se(s) - (N * (1 - s) / 2) / (1 + N * (1 - s) / 2 * x)  # noqa: E731
    hd2.append(dac.harmonics(se)[2])
    hd3.append(dac.harmonics(df)[3])
fig, ax = plt.subplots(figsize=(6.2, 3.9))
ax.semilogx(freqs / 1e6, hd2, color=PALETTE[1], lw=1.4, label="single-ended HD2")
ax.semilogx(freqs / 1e6, hd3, color=PALETTE[0], lw=1.4, label="differential HD3 (HD2 cancels)")
ax.set_xlabel("output frequency (MHz)")
ax.set_ylabel("harmonic (dBc)")
ax.set_title("12-bit DAC into 25 Ω, 1 fF code-dependent capacitance per cell", fontsize=9)
ax.set_ylim(-140, 0)
ax.legend(fontsize=8)
save(fig, f"{OUT}/zout_sfdr.svg")

# ---------------------------------------------------------------- figure 4: pulse responses
f = np.linspace(1e-4, 2, 2001)
fig, ax = plt.subplots(figsize=(6.6, 3.9))
ax.axvspan(0, 0.5, color="0.93", zorder=0)
for mode, col, lab in (("nrz", PALETTE[0], "NRZ"), ("rz", PALETTE[1], "RZ (half period)"), ("mix", PALETTE[2], "mixed mode")):
    ax.plot(f, 20 * np.log10(dac.zoh_gain(f, mode) + 1e-12), color=col, lw=1.4, label=lab)
for x0, txt, dx, dy in ((0.4, "signal", -0.2, -5), (0.6, "image", 0.04, -5)):
    y0 = 20 * math.log10(dac.zoh_gain(x0))
    ax.plot([x0], [y0], "o", color=PALETTE[0], ms=5)
    ax.annotate(txt, xy=(x0, y0), xytext=(x0 + dx, y0 + dy), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6))
ax.text(0.03, -33, "first Nyquist zone", fontsize=8, color="0.3")
ax.set_ylim(-35, 2)
ax.set_xlim(0, 2)
ax.set_xlabel("frequency / $f_s$")
ax.set_ylabel("gain (dB, NRZ DC = 0)")
ax.legend(fontsize=8, loc="upper right")
save(fig, f"{OUT}/pulses.svg")
print("figures written to", OUT)
