#!/usr/bin/env python3
"""Figures for chapter 07-07 (frequency response and Bode plots).

Run from anywhere:  python assets/figures/src/fig_07_07.py
Outputs SVGs to assets/figures/07-07/: a single real pole with its asymptotes, and the Bode plot of
Example 07-07.2's AC-coupled amplifier with asymptotes.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/07-07"
use_style()
B, O, G = PALETTE[0], PALETTE[1], PALETTE[2]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_single_pole():
    x = np.logspace(-2, 2, 800)
    H = 1 / (1 + 1j * x)
    mag = 20 * np.log10(np.abs(H))
    ph = np.degrees(np.angle(H))
    asym = np.where(x <= 1, 0.0, -20 * np.log10(x))
    ph_line = np.where(x <= 0.1, 0.0, np.where(x >= 10, -90.0, -45 * (1 + np.log10(np.clip(x, 1e-9, None)))))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.2, 4.8), sharex=True)
    a1.semilogx(x, mag, color=B, label="exact")
    a1.semilogx(x, asym, color=O, ls="--", label="asymptotes")
    a1.annotate("−3.01 dB at the corner", xy=(1, -3.01), xytext=(0.03, -22),
                arrowprops={"arrowstyle": "->", "color": "0.3"}, fontsize=8)
    a1.text(12, -12, "−20 dB/decade", fontsize=8, color=O)
    a1.set_ylabel("magnitude (dB)")
    a1.set_ylim(-42, 5)
    a1.legend(fontsize=8, loc="lower left")
    a2.semilogx(x, ph, color=B, label="exact")
    a2.semilogx(x, ph_line, color=O, ls="--", label="straight-line approximation")
    a2.axhline(-45, color="0.7", lw=0.6)
    a2.set_ylabel("phase (°)")
    a2.set_yticks([0, -45, -90])
    a2.set_xlabel(r"$\omega/\omega_p$")
    a2.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/single-pole.svg")


def fig_ac_amplifier():
    fL = 1 / (2 * math.pi * 100e3 * 100e-9)
    fH = 1 / (2 * math.pi * 1e3 * 10e-9)
    f = np.logspace(-1, 6, 1400)
    H = 100 * (1j * f / fL) / ((1 + 1j * f / fL) * (1 + 1j * f / fH))
    mag = 20 * np.log10(np.abs(H))
    ph = np.degrees(np.angle(H))
    asym = np.where(f < fL, 40 + 20 * np.log10(f / fL), np.where(f > fH, 40 - 20 * np.log10(f / fH), 40.0))
    ph_a = np.zeros_like(f)
    for fc, sgn in ((fL, -1), (fH, -1)):
        r = f / fc
        ph_a += sgn * np.where(r <= 0.1, 0.0, np.where(r >= 10, 90.0, 45 * (1 + np.log10(r))))
    ph_a += 90
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.2, 4.8), sharex=True)
    a1.semilogx(f, mag, color=B, label="exact")
    a1.semilogx(f, asym, color=O, ls="--", label="asymptotes")
    for fc, lab in ((fL, "$f_L$ = 15.9 Hz"), (fH, "$f_H$ = 15.9 kHz")):
        a1.axvline(fc, color="0.75", lw=0.6)
        a1.text(fc * 1.2, 5, lab, fontsize=8)
    a1.text(20, 43, "40 dB midband", fontsize=8)
    a1.set_ylabel("magnitude (dB)")
    a1.set_ylim(0, 48)
    a1.legend(fontsize=8, loc="center")
    a2.semilogx(f, ph, color=B, label="exact")
    a2.semilogx(f, ph_a, color=O, ls="--", label="straight-line approximation")
    a2.set_yticks([90, 45, 0, -45, -90])
    a2.set_ylabel("phase (°)")
    a2.set_xlabel("frequency (Hz)")
    a2.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/ac-amplifier-bode.svg")


if __name__ == "__main__":
    fig_single_pole()
    fig_ac_amplifier()
