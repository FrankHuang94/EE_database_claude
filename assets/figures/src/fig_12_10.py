#!/usr/bin/env python3
"""Figures for chapter 12-10 (noise in circuits).

Run from anywhere:  python assets/figures/src/fig_12_10.py
Outputs SVGs to assets/figures/12-10/:
- flicker.svg: Example 12-10.3's amplifier noise, a 5 nV/rtHz white floor with a 100 kHz flicker corner:
  the spectral density S_w(1 + f_c/f) (left) and the RMS noise integrated from 1 Hz up to f (right), with the
  white and flicker parts separately; the integrals are evaluated in closed form at each upper limit.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
SW, FC = (5e-9) ** 2, 1e5


def fig_flicker():
    f = np.logspace(0, 6, 400)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.8, 3.4))
    a1.loglog(f, np.sqrt(SW * (1 + FC / f)) * 1e9, color=PALETTE[0], lw=1.8, label="total")
    a1.loglog(f, np.full_like(f, np.sqrt(SW) * 1e9), "--", color=PALETTE[2], lw=1, label="white floor")
    a1.loglog(f, np.sqrt(SW * FC / f) * 1e9, ":", color=PALETTE[1], lw=1.2, label="1/f part")
    a1.axvline(FC, color="0.6", lw=0.8)
    a1.text(FC * 0.6, 900, "corner f_c", fontsize=8, color="0.35", ha="right")
    a1.set_xlabel("frequency (Hz)")
    a1.set_ylabel("noise density (nV/√Hz)")
    a1.legend(fontsize=8)
    wh = SW * (f - 1)
    fl = SW * FC * np.log(f)
    a2.semilogx(f, np.sqrt(wh + fl) * 1e6, color=PALETTE[0], lw=1.8, label="total")
    a2.semilogx(f, np.sqrt(wh) * 1e6, "--", color=PALETTE[2], lw=1, label="white only")
    a2.semilogx(f, np.sqrt(fl) * 1e6, ":", color=PALETTE[1], lw=1.2, label="1/f only")
    a2.set_xlabel("upper limit (Hz), from 1 Hz")
    a2.set_ylabel("integrated RMS noise (µV)")
    a2.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/flicker.svg")


if __name__ == "__main__":
    fig_flicker()
