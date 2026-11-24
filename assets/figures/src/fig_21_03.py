#!/usr/bin/env python3
"""Figures for chapter 21-03 (noise figure and linearity).

Run from anywhere:  python assets/figures/src/fig_21_03.py
Outputs
  assets/figures/21-03/intercept.svg      output fundamental and IM3 against input power for a differential-pair
                                          (tanh) amplifier with 15 dB gain and IIP3 = -10 dBm, computed by two-tone
                                          FFTs, with the slope-1 and slope-3 extrapolations, IP3, the 1 dB point,
                                          a 3 dB noise figure floor in 1 MHz and the SFDR
  assets/figures/21-03/noise-circles.svg  source-reflection plane for the device of Example 21-03.3: Gamma_opt, the
                                          1.0 and 1.5 dB noise circles, the 50 ohm point and the conjugate-match point
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import rfnl  # noqa: E402

OUT = "assets/figures/21-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

G_DB, IIP3 = 15.0, -10.0
a_ip3 = rfnl.amp_from_dbm(IIP3)
scale = a_ip3 / 2                    # tanh(x): x_IIP3 = 2
gain_v = 10 ** (G_DB / 20)
fs, n, f1, f2 = 64e6, 6400, 9e6, 10e6
pins = np.arange(-60, 1, 1.0)
fund, im3 = [], []
for p in pins:
    a = rfnl.amp_from_dbm(p)
    f, sp = rfnl.tones(lambda v: gain_v * scale * np.tanh(v / scale), [a, a], [f1, f2], fs, n)
    i9, i8 = np.argmin(abs(f - f1)), np.argmin(abs(f - f2 + 2e6))
    fund.append(rfnl.dbm_from_amp(sp[i9]))
    im3.append(rfnl.dbm_from_amp(max(sp[i8], 1e-12)))
fund, im3 = np.array(fund), np.array(im3)
x = np.linspace(-60, 0, 2)
floor_in = rfnl.KT0_DBM_HZ + 60 + 3.0
floor_out = floor_in + G_DB
p_sfdr = (2 * IIP3 + floor_in) / 3

fig, ax = plt.subplots(figsize=(6.2, 4.4))
ax.plot(pins, fund, color=PALETTE[0], lw=1.6, label="fundamental (per tone)")
ax.plot(pins, im3, color=PALETTE[1], lw=1.6, label="third-order product")
ax.plot(x, x + G_DB, color=PALETTE[0], lw=0.8, ls="--")
ax.plot(x, 3 * x - 2 * IIP3 + G_DB, color=PALETTE[1], lw=0.8, ls="--")
ax.plot([IIP3], [IIP3 + G_DB], "o", color="k", ms=5)
ax.annotate("IP3", (IIP3, IIP3 + G_DB), textcoords="offset points", xytext=(-26, 6), fontsize=8)
ax.axhline(floor_out, color="0.4", lw=0.9, ls=":")
ax.text(-59, floor_out + 2, "output noise floor (NF 3 dB, 1 MHz)", fontsize=8, color="0.3")
ax.annotate("", xy=(p_sfdr, floor_out), xytext=(p_sfdr, p_sfdr + G_DB),
            arrowprops=dict(arrowstyle="<->", color="0.25", lw=0.9))
ax.text(p_sfdr + 1, (floor_out + p_sfdr + G_DB) / 2, "SFDR", fontsize=8, color="0.25")
ax.set_xlim(-60, 0)
ax.set_ylim(-110, 20)
ax.set_xlabel("input power per tone (dBm)")
ax.set_ylabel("output power (dBm)")
ax.legend(fontsize=8, loc="upper left")
ax.set_title("Slope 1, slope 3 and the intercept nobody reaches", fontsize=10)
save(fig, f"{OUT}/intercept.svg")

P = lambda m, d: m * cmath.exp(1j * math.radians(d))  # noqa: E731
gopt, gconj = P(0.45, 60), P(0.6, -40)
th = np.linspace(0, 2 * np.pi, 400)
fig, ax = plt.subplots(figsize=(4.8, 4.8))
ax.plot(np.cos(th), np.sin(th), color="k", lw=1.0)
for nf, col in ((1.0, PALETTE[0]), (1.5, PALETTE[2])):
    c, r = rfnl.noise_circle(nf, 0.8, 8.0, gopt)
    z = c + r * np.exp(1j * th)
    ax.plot(z.real, z.imag, color=col, lw=1.3, label=f"NF = {nf:.1f} dB")
ax.plot([gopt.real], [gopt.imag], "o", color="k", ms=5)
ax.annotate("Γ_opt (0.80 dB)", (gopt.real, gopt.imag), textcoords="offset points", xytext=(6, 4), fontsize=8)
ax.plot([0], [0], "s", color="0.3", ms=5)
ax.annotate("50 Ω (1.07 dB)", (0, 0), textcoords="offset points", xytext=(6, -12), fontsize=8)
ax.plot([gconj.real], [gconj.imag], "^", color=PALETTE[1], ms=6)
ax.annotate("power match (2.04 dB)", (gconj.real, gconj.imag), textcoords="offset points", xytext=(-40, -14),
            fontsize=8)
ax.set_aspect("equal")
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.set_xlabel("Re Γ_s")
ax.set_ylabel("Im Γ_s")
ax.legend(fontsize=8, loc="lower left")
ax.set_title("Noise circles: the cost of leaving Γ_opt", fontsize=10)
save(fig, f"{OUT}/noise-circles.svg")
