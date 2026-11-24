#!/usr/bin/env python3
"""Figures for chapter 20-04 (low-dropout regulators).

Run from anywhere:  python assets/figures/src/fig_20_04.py
Outputs
  assets/figures/20-04/loop.svg   loop-gain magnitude and phase of the running design at 100 uA, 1 mA, 10 mA and 100 mA
                                  (1 uF, 5 mOhm ESR), crossover marked
  assets/figures/20-04/psrr.svg   PSRR against frequency at 100 mA and 100 uA with the gate tracking the supply (k = 1)
                                  and with a ground-referenced gate (k = 0)
"""
from __future__ import annotations

import math
import sys
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import ldo as m  # noqa: E402

OUT = "assets/figures/20-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
reg = m.design()
f = np.logspace(0, 9, 1801)
s = 2j * np.pi * f


def fmt_hz(x: float) -> str:
    return f"{x / 1e6:.3g} MHz" if x >= 1e6 else f"{x / 1e3:.3g} kHz"


# ---------------------------------------------------------------- figure 2: loop gain across load
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.6, 5.6), sharex=True)
labels = {100e-6: "100 µA", 1e-3: "1 mA", 10e-3: "10 mA", 100e-3: "100 mA"}
for (il, lab), col in zip(labels.items(), PALETTE):
    loop, *_ = reg.transfer(il)
    hv = np.array([loop(x) for x in s])
    mg = m.margins(loop)
    ax1.semilogx(f, 20 * np.log10(np.abs(hv)), color=col,
                 label=f"{lab}: $f_c$ = {fmt_hz(mg['fc'])}, PM = {mg['pm']:.1f}°")
    ax2.semilogx(f, np.degrees(np.unwrap(np.angle(hv))), color=col)
    ax1.plot(mg["fc"], 0, "o", color=col, ms=4)
ax1.axhline(0, color="0.6", lw=0.8)
ax1.set_ylabel("$|L|$ (dB)")
ax1.set_ylim(-80, 80)
ax1.legend(loc="lower left", fontsize=8)
ax1.set_title("Running design: 1 µF output capacitor, 5 mΩ ESR")
ax2.axhline(-180, color="0.6", lw=0.8)
ax2.set_ylabel("phase of $L$ (°)")
ax2.set_xlabel("frequency (Hz)")
save(fig, f"{OUT}/loop.svg")

# ---------------------------------------------------------------- figure 3: PSRR
fig, ax = plt.subplots(figsize=(6.6, 4.2))
cases = ((100e-3, 1.0, PALETTE[0], "-"), (100e-3, 0.0, PALETTE[1], "--"),
         (100e-6, 1.0, PALETTE[2], "-"), (100e-6, 0.0, PALETTE[3], "--"))
for il, k, col, ls in cases:
    _, _, _, psrr_inv, _ = replace(reg, k_gate=k).transfer(il)
    vals = np.array([-20 * math.log10(abs(psrr_inv(x))) for x in s])
    ax.semilogx(f, vals, color=col, ls=ls, label=f"{labels[il]}, $k$ = {k:.0f}")
ax.set_xlabel("ripple frequency (Hz)")
ax.set_ylabel("PSRR (dB)")
ax.set_ylim(0, 140)
ax.legend(loc="upper left")
ax.set_title("Supply rejection: gate tracking the supply ($k$ = 1) or not ($k$ = 0)")
save(fig, f"{OUT}/psrr.svg")
print("figures written to", OUT)
