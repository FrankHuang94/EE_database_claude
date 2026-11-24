#!/usr/bin/env python3
"""Figures for chapter 20-07 (Nyquist ADCs: flash, SAR and pipeline).

Run from anywhere:  python assets/figures/src/fig_20_07.py
Outputs
  assets/figures/20-07/sar_energy.svg   switching energy drawn from V_REF for every code of a 10-bit differential SAR,
                                        conventional versus monotonic switching (lab Part 2)
  assets/figures/20-07/pipeline.svg     (a) 1.5-bit stage residue with ideal and offset comparators; (b) DNL of the
                                        10-bit pipeline for first-stage gains 0.99 and 1.01 (lab Part 3)
  assets/figures/20-07/ti_spurs.svg     spectra of a two-channel interleaved ADC with offset, gain and skew mismatch
                                        (Example 20-07.7, lab Part 4)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import nyq  # noqa: E402

OUT = "assets/figures/20-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- figure 2: SAR switching energy per code
n = 10
codes = np.arange(2 ** n)
ec = np.array([2 * nyq.conventional_energy(n, (c + 0.5) / 2 ** n) for c in codes])
em = np.array([nyq.monotonic_energy(n, ((c + 0.5) / 2 ** n - 0.5) * 2) for c in codes])
fig, ax = plt.subplots(figsize=(6.6, 3.8))
ax.plot(codes, ec, color=PALETTE[0], lw=0.6, label=f"conventional (average {ec.mean():.1f})")
ax.plot(codes, em, color=PALETTE[1], lw=0.6, label=f"monotonic (average {em.mean():.1f})")
ax.set_xlabel("output code")
ax.set_ylabel(r"energy from $V_{REF}$ ($C_uV_{REF}^2$)")
ax.set_title("10-bit differential SAR: switching energy per conversion")
ax.set_xlim(0, 1023)
ax.set_ylim(0, 1800)
ax.legend(loc="upper right", fontsize=8)
save(fig, f"{OUT}/sar_energy.svg")

# ---------------------------------------------------------------- figure 3: pipeline redundancy and gain error
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.0, 3.4))
v = np.linspace(-1, 1, 4001)
for off, col, ls, lw, lab in ((0.2, PALETTE[1], "-", 2.0, "upper threshold +0.2 V"),
                             (0.0, PALETTE[0], "--", 1.0, "ideal thresholds")):
    d = np.where(v > 0.25 + off, 1, np.where(v < -0.25, -1, 0))
    r = 2 * v - d
    a1.plot(v, np.where(np.abs(np.diff(d, prepend=d[0])) > 0, np.nan, r), color=col, ls=ls, lw=lw, label=lab)
a1.axhspan(-1, 1, color="0.92", zorder=0)
a1.text(-0.95, 1.08, "next stage's input range", fontsize=7, color="0.3")
a1.set_xlabel(r"$v_{in}$ (V), $V_{REF}$ = 1 V")
a1.set_ylabel("residue (V)")
a1.set_ylim(-1.3, 1.3)
a1.set_title("(a) 1.5-bit stage residue", fontsize=9)
a1.legend(loc="lower right", fontsize=7)
x = np.linspace(-0.99999, 0.99999, 2000001)
for g1, col in ((0.99, PALETTE[2]), (1.01, PALETTE[3])):
    g = np.ones(8)
    g[0] = g1
    c = (nyq.pipeline(x, gains=g) + 511.5).astype(int)
    cnt = np.bincount(c, minlength=1024).astype(float)[4:-4]          # end codes: range compression, not DNL
    a2.plot(np.arange(4, 1020), cnt / cnt.mean() - 1, color=col, lw=0.8, label=f"stage-1 gain {g1}")
a2.set_xlabel("output code")
a2.set_ylabel("DNL (LSB)")
a2.set_title("(b) 10-bit pipeline, interstage gain error", fontsize=9)
a2.set_ylim(-1.2, 1.2)
a2.legend(loc="lower center", fontsize=7)
save(fig, f"{OUT}/pipeline.svg")

# ---------------------------------------------------------------- figure 4: interleaving spurs
N, fs, m, amp = 4096, 1e9, 1001, 0.8
cases = (("offset mismatch 1 mV", np.array([-0.5e-3, 0.5e-3]), np.ones(2), np.zeros(2), N // 2),
         ("gain mismatch 1%", np.zeros(2), np.array([1, 1.01]), np.zeros(2), N // 2 - m),
         ("timing skew 1 ps", np.zeros(2), np.ones(2), np.array([0, 1e-12]), N // 2 - m))
fig, axs = plt.subplots(3, 1, figsize=(6.6, 5.6), sharex=True)
for ax, (name, o, g, s, b) in zip(axs, cases):
    xx, fin = nyq.ti_capture(2, fs, N, m, amp, o, g, s)
    p = nyq.power_spectrum(xx)
    f = np.arange(p.size) * fs / N / 1e6
    ax.plot(f, 10 * np.log10(p / p[m] + 1e-30), color=PALETTE[0], lw=0.7)
    ax.annotate(f"{nyq.spur_dbc(p, m, b):.1f} dBc at {f[b]:.1f} MHz", xy=(f[b], nyq.spur_dbc(p, m, b)),
                xytext=(f[b] - 230 if b == N // 2 else f[b] + 40, -25), arrowprops=dict(arrowstyle="->", lw=0.7),
                fontsize=8)
    ax.set_ylim(-100, 10)
    ax.set_ylabel("dBc")
    ax.set_title(name, fontsize=9)
axs[-1].set_xlabel(f"frequency (MHz); $f_s$ = 1 GS/s, $f_{{in}}$ = {fin / 1e6:.2f} MHz, 0.8 V")
save(fig, f"{OUT}/ti_spurs.svg")
print("figures written to", OUT)
