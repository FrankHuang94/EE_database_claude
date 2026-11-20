#!/usr/bin/env python3
"""Figures for chapter 16-08 (filter structures and implementation).

Run from anywhere:  python assets/figures/src/fig_16_08.py
Outputs
  assets/figures/16-08/pole-grid.svg      the pole positions a biquad can realize in the first quadrant of the unit
                                          disc when its coefficients have 5 fractional bits: direct form (a1, a2
                                          quantized) against the coupled form (r cos θ and r sin θ quantized)
  assets/figures/16-08/section-order.svg  peak gain (dB) at the output of each section of the order-8 elliptic
                                          filter of 16-07, for SciPy's ordering and for the reverse ordering
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/16-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

B = 5
q = 2.0 ** -B
fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2))
t = np.linspace(0, np.pi / 2, 200)
# direct form: z^2 + a1 z + a2 with a1 = -2 r cos(th), a2 = r^2, both on the grid q; complex roots only
pts = []
for a2 in np.arange(0, 1, q):
    for a1 in np.arange(-2, 0 + q / 2, q):
        disc = a1 * a1 - 4 * a2
        if disc < 0:
            r = np.sqrt(a2)
            c = -a1 / (2 * r) if r > 0 else 1.0
            if abs(c) <= 1:
                pts.append((r * c, r * np.sqrt(1 - c * c)))
pts = np.array(pts)
axes[0].plot(pts[:, 0], pts[:, 1], ".", ms=2.5, color=PALETTE[0])
axes[0].set_title(f"Direct form: a1, a2 with {B} fractional bits")
c = np.arange(0, 1 + q / 2, q)
C, S = np.meshgrid(c, c)
inside = C**2 + S**2 < 1
axes[1].plot(C[inside], S[inside], ".", ms=2.5, color=PALETTE[1])
axes[1].set_title(f"Coupled form: r cos θ, r sin θ with {B} bits")
for ax in axes:
    ax.plot(np.cos(t), np.sin(t), color="0.4", lw=0.8)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.02)
    ax.set_aspect("equal")
    ax.set_xlabel("Re z")
    ax.set_ylabel("Im z")
axes[0].annotate("sparse near z = 1:\nlow-frequency poles\nare hard to place", xy=(0.97, 0.12), xytext=(0.30, 0.30),
                 fontsize=8, arrowprops={"arrowstyle": "->", "color": "0.3"},
                 bbox={"boxstyle": "round", "fc": "white", "ec": "0.6"})
fig.tight_layout(w_pad=2.0)
save(fig, f"{OUT}/pole-grid.svg")

fs = 48000.0
sos = signal.ellip(8, 0.1, 60, 4000, fs=fs, output="sos")
w = np.linspace(0, np.pi, 50001)


def peaks(S):
    out, H = [], np.ones_like(w, dtype=complex)
    for sec in S:
        _, Hs = signal.freqz(sec[:3], sec[3:], worN=w)
        H = H * Hs
        out.append(20 * np.log10(np.abs(H).max()))
    return out


fig, ax = plt.subplots(figsize=(6.0, 3.6))
k = np.arange(1, 5)
ax.plot(k, peaks(sos), "o-", color=PALETTE[0], label="poles far from the circle first (SciPy's order)")
ax.plot(k, peaks(sos[::-1]), "s-", color=PALETTE[1], label="reversed: sharpest section first")
ax.axhline(0, color="0.5", lw=0.8, ls="--")
ax.set_xticks(k)
ax.set_xlabel("output of section")
ax.set_ylabel("peak gain from the input (dB)")
ax.set_title("Same filter, different internal headroom")
ax.legend(fontsize=8, loc="upper right")
save(fig, f"{OUT}/section-order.svg")
print("figures written to", OUT)
