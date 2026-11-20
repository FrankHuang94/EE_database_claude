#!/usr/bin/env python3
"""Figures for chapter 17-06 (bandpass digital modulation and BER).

Run from anywhere:  python assets/figures/src/fig_17_06.py
Outputs
  assets/figures/17-06/constellations.svg  QPSK, 8-PSK, 16-QAM and 64-QAM at the same Es/N0 = 20 dB: ideal points
                                           and received clouds (Gray labels shown for QPSK and 16-QAM)
  assets/figures/17-06/ber-curves.svg      approximate BER (SER / log2 M with Gray coding) against Eb/N0 for BPSK/QPSK,
                                           8-PSK, 16-, 64- and 256-QAM
Uses labs/17-06-lab/modulation.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import modulation as md  # noqa: E402

OUT = "assets/figures/17-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(6)

sets = [("QPSK", md.psk(4)), ("8-PSK", md.psk(8)), ("16-QAM", md.qam(16)), ("64-QAM", md.qam(64))]
fig, axes = plt.subplots(1, 4, figsize=(9.6, 2.7))
for ax, (name, (pts, lab)) in zip(axes, sets):
    pts = pts / math.sqrt(md.es(pts))
    if name == "QPSK":
        pts = pts * np.exp(1j * math.pi / 4)
    idx = rng.integers(0, len(pts), 3000)
    r = md.awgn(pts[idx], 20.0, 1.0, rng)
    ax.plot(r.real, r.imag, ".", ms=1, color=PALETTE[0], alpha=0.3)
    ax.plot(pts.real, pts.imag, "o", ms=3, color=PALETTE[1])
    if name in ("QPSK", "16-QAM"):
        k = int(math.log2(len(pts)))
        for p, l in zip(pts, lab):
            ax.annotate(format(int(l), f"0{k}b"), (p.real, p.imag), textcoords="offset points", xytext=(0, 5), fontsize=6, ha="center")
    ax.set_aspect("equal")
    ax.set_title(f"{name}, d_min = {md.dmin(pts):.2f}", fontsize=9)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_xlabel("I")
axes[0].set_ylabel("Q")
fig.suptitle("Same average energy, Es/N0 = 20 dB: more points, smaller distance, overlapping clouds", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/constellations.svg")

eb = np.linspace(0, 30, 301)
lin = 10 ** (eb / 10)
fig, ax = plt.subplots(figsize=(6.6, 4.0))
from scipy.stats import norm  # noqa: E402
ax.semilogy(eb, norm.sf(np.sqrt(2 * lin)), color=PALETTE[0], label="BPSK, QPSK")
ax.semilogy(eb, [md.ser_psk_craig(8, 3 * x) / 3 for x in lin], color=PALETTE[1], label="8-PSK")
for (m, col) in ((16, PALETTE[2]), (64, PALETTE[3]), (256, PALETTE[4])):
    k = math.log2(m)
    ax.semilogy(eb, [md.ser_qam(m, k * x) / k for x in lin], color=col, label=f"{m}-QAM")
ax.set_ylim(1e-7, 0.5)
ax.set_xlabel("Eb/N0 (dB)")
ax.set_ylabel("bit-error rate (Gray, high-SNR approximation)")
ax.set_title("Each extra two bits per symbol costs about 5 dB of Eb/N0")
ax.legend(fontsize=8)
save(fig, f"{OUT}/ber-curves.svg")
