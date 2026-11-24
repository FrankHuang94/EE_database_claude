#!/usr/bin/env python3
"""Figures for chapter 20-12 (why analog does not scale like digital).

Run from anywhere:  python assets/figures/src/fig_20_12.py
Outputs
  assets/figures/20-12/power.svg   power of the kT/C-limited buffer of Example 20-12.2 (74 dB, 100 MHz, gm/ID 15)
                                   against supply: swing 80% of V_DD, and swing V_DD - 0.3 V; a CV^2 curve for contrast
  assets/figures/20-12/stack.svg   small-signal output resistance of a single short-channel NMOS sink and of a cascode
                                   against output voltage (the square-law model of stack.cir)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-12-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import scaling  # noqa: E402

OUT = "assets/figures/20-12"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- power against supply
vdd = np.linspace(0.45, 3.3, 300)
p_prop = np.array([scaling.thermal_power(74, 1e8, v)[3] for v in vdd])
eta_fixed = (vdd - 0.3) / vdd
p_head = np.array([scaling.thermal_power(74, 1e8, v, eta=e)[3] for v, e in zip(vdd, eta_fixed)])
ref = scaling.thermal_power(74, 1e8, 1.8)[3]
fig, ax = plt.subplots(figsize=(6.0, 4.0))
ax.semilogy(vdd, p_prop * 1e6, color=PALETTE[0], lw=1.4, label="analog, swing = 0.8 V$_{DD}$")
ax.semilogy(vdd, p_head * 1e6, color=PALETTE[1], lw=1.4, label="analog, swing = V$_{DD}$ − 0.3 V")
ax.semilogy(vdd, ref * 1e6 * (vdd / 1.8) ** 2, color="0.5", lw=1.0, ls="--", label=r"digital $CV^2f$ (same at 1.8 V)")
for v in (1.8, 0.8):
    ax.plot(v, scaling.thermal_power(74, 1e8, v)[3] * 1e6, "o", color=PALETTE[0], ms=4)
ax.set_xlabel("supply voltage $V_{DD}$ (V)")
ax.set_ylabel("power (µW)")
ax.set_ylim(3, 3000)
ax.legend(fontsize=8)
ax.set_title("74 dB, 100 MHz kT/C-limited buffer: power rises as the supply falls", fontsize=10)
save(fig, f"{OUT}/power.svg")

# ---------------------------------------------------------------- cascode output resistance
v = np.linspace(0.12, 0.8, 400)
h = 1e-5
r1 = [2 * h / (scaling.level1_id(0.55, x + h) - scaling.level1_id(0.55, x - h)) for x in v]
r2 = [2 * h / (scaling.cascode_current(x + h)[0] - scaling.cascode_current(x - h)[0]) for x in v]
fig, ax = plt.subplots(figsize=(6.0, 4.0))
ax.semilogy(v, np.array(r1) / 1e3, color=PALETTE[1], lw=1.4, label="single transistor")
ax.semilogy(v, np.array(r2) / 1e3, color=PALETTE[0], lw=1.4, label="cascode")
ax.axvline(0.35, color="0.5", lw=0.8, ls="--")
ax.text(0.36, 12, "cascode saturated\nabove ≈ 0.35 V", fontsize=8, color="0.3")
ax.set_xlabel("output voltage (V), 0.8 V supply")
ax.set_ylabel("output resistance (kΩ)")
ax.set_ylim(5, 2e4)
ax.legend(fontsize=8, loc="upper left")
ax.set_title("A cascode multiplies output resistance only above its headroom", fontsize=10)
save(fig, f"{OUT}/stack.svg")
