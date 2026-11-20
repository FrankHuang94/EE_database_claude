#!/usr/bin/env python3
"""Figures for chapter 17-04 (baseband digital transmission).

Run from anywhere:  python assets/figures/src/fig_17_04.py
Outputs
  assets/figures/17-04/raised-cosine.svg  raised-cosine pulses and spectra for roll-off 0 (sinc), 0.22, 0.5 and 1
  assets/figures/17-04/rc-eyes.svg        eye diagrams of random NRZ through a 5 GHz one-pole channel at 10, 25 and
                                          45 Gb/s, with the worst-case opening 1 - 2r marked at the sampling instant
Uses labs/17-04-lab/baseband.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "17-communication-systems" / "labs" / "17-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import baseband as bb  # noqa: E402

OUT = "assets/figures/17-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

t = np.linspace(-5, 5, 2001)
f = np.linspace(-1.2, 1.2, 1201)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.2))
for a, col in zip((0.0, 0.22, 0.5, 1.0), PALETTE):
    a1.plot(t, bb.raised_cosine(t, a), color=col, lw=1, label=f"α = {a:g}")
    a2.plot(f, bb.raised_cosine_spectrum(f, a), color=col, lw=1.2, label=f"α = {a:g}")
a1.plot(np.arange(-5, 6), np.zeros(11), "k.", ms=4)
a1.axhline(0, color="0.6", lw=0.5)
a1.set_xlabel("t / T")
a1.set_ylabel("h(t)")
a1.set_title("Zeros at every other sampling instant")
a1.legend(fontsize=7)
a2.axvline(0.5, color="0.5", ls=":", lw=0.8)
a2.set_xlabel("f T")
a2.set_ylabel("H(f) / T")
a2.set_title("Roll-off odd-symmetric about 1/(2T)")
fig.tight_layout()
save(fig, f"{OUT}/raised-cosine.svg")

tau = 1 / (2 * math.pi * 5e9)
rng = np.random.default_rng(4)
fig, axes = plt.subplots(1, 3, figsize=(8.4, 2.9), sharey=True)
for ax, rate, col in zip(axes, (10e9, 25e9, 45e9), PALETTE):
    T = 1 / rate
    sps = 64
    a = rng.choice([-1.0, 1.0], 600)
    y = bb.rc_channel(bb.waveform(a, sps), tau / (T / sps))
    tr = bb.fold_eye(y[sps * 20:], sps, offset=0, span=2)
    tt = np.arange(1, 2 * sps + 1) / sps  # sample i covers the end of slot i
    for row in tr[:250]:
        ax.plot(tt, row, color=col, lw=0.3, alpha=0.4)
    r = math.exp(-T / tau)
    ax.vlines([1.0], [-(1 - 2 * r)], [1 - 2 * r], color="k", lw=1.5)
    ax.set_title(f"{rate / 1e9:.0f} Gb/s: worst eye {1 - 2 * r:.3f}", fontsize=9)
    ax.set_xlabel("time (bits); sampled at bit end")
axes[0].set_ylabel("received signal")
fig.suptitle("NRZ through a 5 GHz one-pole channel: the eye closes near 45 Gb/s", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/rc-eyes.svg")
