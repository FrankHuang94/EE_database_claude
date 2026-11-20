#!/usr/bin/env python3
"""Figures for chapter 16-02 (DTFT and z-transform for DSP).

Run from anywhere:  python assets/figures/src/fig_16_02.py
Outputs
  assets/figures/16-02/notch.svg       Example 16-02.2: pole-zero plot (left) and gain in dB from 0 to 150 Hz at
                                       fs = 1 kHz (right) of 50 Hz notches with r = 0.9 and 0.98, with the
                                       20-point moving average of 16-01 for comparison
  assets/figures/16-02/phase-family.svg  Problem 16-02.9: the minimum-, linear- and maximum-phase FIR filters with
                                       zeros at 0.5 and 2 (one magnitude response): impulse responses, partial
                                       energy and group delay
Uses labs/16-02-lab/pz.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import pz  # noqa: E402

OUT = "assets/figures/16-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_notch():
    fs = 1000.0
    w0 = 2 * math.pi * 50 / fs
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8), gridspec_kw={"width_ratios": [1, 1.6]})
    t = np.linspace(0, 2 * math.pi, 400)
    a1.plot(np.cos(t), np.sin(t), color="gray", lw=0.7)
    for r, col in ((0.9, PALETTE[3]), (0.98, PALETTE[0])):
        b, a = pz.notch(w0, r)
        z, p, _ = pz.zpk(b, a)
        a1.plot(p.real, p.imag, "x", color=col, ms=8, mew=1.5, label=f"poles, r = {r}")
    a1.plot(np.cos([w0, -w0]), np.sin([w0, -w0]), "o", mfc="none", color="k", ms=8, label="zeros (both notches)")
    a1.set_xlim(0.6, 1.1)
    a1.set_ylim(-0.45, 0.45)
    a1.set_aspect("equal")
    a1.set_xlabel("Re z")
    a1.set_ylabel("Im z")
    a1.set_title("z-plane near z = 1 (ω0 = 0.1π)", fontsize=9)
    a1.legend(fontsize=7, loc="lower left")
    f = np.linspace(0.05, 150, 6000)
    w = 2 * np.pi * f / fs
    for r, col in ((0.9, PALETTE[3]), (0.98, PALETTE[0])):
        b, a = pz.notch(w0, r)
        a2.plot(f, 20 * np.log10(np.maximum(np.abs(pz.freq_resp(b, a, w)), 1e-5)), color=col, label=f"notch, r = {r}")
    ma = np.abs(np.sin(20 * w / 2) / (20 * np.sin(w / 2)))
    a2.plot(f, 20 * np.log10(np.maximum(ma, 1e-5)), color="gray", ls=":", label="20-point moving average (16-01)")
    a2.axhline(-3, color="k", lw=0.5, ls="--")
    a2.set_ylim(-50, 3)
    a2.set_xlabel("frequency (Hz), fs = 1 kHz")
    a2.set_ylabel("gain (dB)")
    a2.set_title("50 Hz notches: width set by the pole radius", fontsize=9)
    a2.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/notch.svg")


def fig_phase_family():
    fam = (("minimum phase (2, −2, 0.5)", [2, -2, 0.5], PALETTE[0]),
           ("linear phase (1, −2.5, 1)", [1, -2.5, 1], PALETTE[2]),
           ("maximum phase (0.5, −2, 2)", [0.5, -2, 2], PALETTE[3]))
    w = np.linspace(0.001, math.pi, 600)
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(10.4, 3.2))
    for k, (name, h, col) in enumerate(fam):
        a1.stem(np.arange(3) + 0.12 * (k - 1), h, linefmt=col, markerfmt="o", basefmt=" ", label=name)
        pe = pz.partial_energy(h)
        a2.plot(range(3), pe / pe[-1], "o-", color=col, label=name)
        a3.plot(w, pz.group_delay(h, [1], w), color=col, label=name)
    a1.axhline(0, color="gray", lw=0.5)
    a1.set_xlabel("n")
    a1.set_ylabel("h[n]")
    a1.set_title("impulse responses", fontsize=9)
    a2.set_xlabel("n")
    a2.set_ylabel("fraction of total energy")
    a2.set_title("partial energy (same total)", fontsize=9)
    a2.set_xticks([0, 1, 2])
    a2.legend(fontsize=6.5, loc="lower right")
    a3.set_xlabel("ω (rad/sample)")
    a3.set_ylabel("group delay (samples)")
    a3.set_title("group delay (identical |H|)", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/phase-family.svg")


if __name__ == "__main__":
    fig_notch()
    fig_phase_family()
