#!/usr/bin/env python3
"""Figures for chapter 10-10 (op-amp application circuits).

Run from anywhere:  python assets/figures/src/fig_10_10.py
Outputs SVGs to assets/figures/10-10/:
- schmitt.svg: a slow, noisy ramp crossing 2.5 V into (a) a plain comparator, which chatters, and (b) the Schmitt
  trigger of Example 10-10.5 (thresholds 2.45 V and 2.55 V), which switches once; seeded noise, 10 mV rms;
- tia.svg: transimpedance magnitude of the photodiode amplifier of Example 10-10.7 (R_F = 100 kOhm, C_in = 14 pF,
  GBW = 10 MHz) without a feedback capacitor and with C_F = 2.105 pF (Butterworth), from the loop equation with a
  single-pole op-amp.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_schmitt():
    rng = np.random.default_rng(1010)
    t = np.linspace(0, 1, 4000)
    vin = 2.3 + 0.4 * t + rng.normal(0, 0.01, t.size)
    plain = np.where(vin > 2.5, 5.0, 0.0)
    out = np.zeros_like(vin)
    state = 0.0
    for i, x in enumerate(vin):
        if state == 0.0 and x > 2.55:
            state = 5.0
        elif state == 5.0 and x < 2.45:
            state = 0.0
        out[i] = state
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 4.8), sharex=True)
    axes[0].plot(t, vin, color="0.4", lw=0.6)
    for th, ls in ((2.5, "-"), (2.45, ":"), (2.55, ":")):
        axes[0].axhline(th, color=PALETTE[1], ls=ls, lw=0.8)
    axes[0].set_ylabel("input (V)")
    axes[1].plot(t, plain, color=PALETTE[0], lw=0.8)
    axes[1].set_ylabel("comparator")
    axes[1].set_ylim(-0.5, 5.5)
    axes[2].plot(t, out, color=PALETTE[2], lw=1.2)
    axes[2].set_ylabel("Schmitt")
    axes[2].set_ylim(-0.5, 5.5)
    axes[2].set_xlabel("time (arbitrary units)")
    fig.tight_layout()
    save(fig, f"{OUT}/schmitt.svg")


def tia(f, cf, rf=100e3, cin=14e-12, gbw=10e6):
    s = 2j * np.pi * f
    a = 2 * np.pi * gbw / s
    zf = rf / (1 + s * rf * cf)
    zin = 1 / (s * cin)
    beta = zin / (zin + zf)
    t = a * beta
    return zf * t / (1 + t)


def fig_tia():
    f = np.logspace(3, 8, 600)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.loglog(f, np.abs(tia(f, 1e-18)) / 1e3, color=PALETTE[1], label="no $C_F$: peaking about 9.4 ×")
    ax.loglog(f, np.abs(tia(f, 2.105e-12)) / 1e3, color=PALETTE[0], label="$C_F$ = 2.105 pF: Butterworth, $-3$ dB at 0.994 MHz")
    ax.axhline(100, color="0.6", ls=":")
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("$|v_o/i_{pd}|$ (kΩ)")
    ax.set_ylim(1, 2000)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/tia.svg")


if __name__ == "__main__":
    fig_schmitt()
    fig_tia()
