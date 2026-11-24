#!/usr/bin/env python3
"""Figures for chapter 21-01 (S-parameters and network analysis).

Run from anywhere:  python assets/figures/src/fig_21_01.py
Outputs
  assets/figures/21-01/line.svg       |S11| and |S21| (dB) of the 75 ohm line of Example 21-01.3 (an eighth wave at
                                      1 GHz) in a 50 ohm system, from 0 to 8 GHz
  assets/figures/21-01/stability.svg  load-plane map of the transistor of Example 21-01.6 at 500 MHz: loads with
                                      |Gamma_in| > 1 shaded, the stability circle and the unit circle
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
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import sparam  # noqa: E402

OUT = "assets/figures/21-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

f = np.linspace(1e6, 8e9, 1600)
s11 = np.array([sparam.s_line(75, math.pi / 4 * ff / 1e9)[0, 0] for ff in f])
s21 = np.array([sparam.s_line(75, math.pi / 4 * ff / 1e9)[1, 0] for ff in f])
fig, ax = plt.subplots(figsize=(6.0, 3.8))
ax.plot(f / 1e9, 20 * np.log10(np.abs(s11) + 1e-12), color=PALETTE[0], lw=1.4, label=r"$|S_{11}|$")
ax.plot(f / 1e9, 20 * np.log10(np.abs(s21)), color=PALETTE[1], lw=1.4, label=r"$|S_{21}|$")
ax.axvline(1, color="0.6", lw=0.8, ls="--")
ax.text(1.05, -32, "Example 21-01.3\n(1 GHz, θ = 45°)", fontsize=8, color="0.3")
ax.set_ylim(-40, 2)
ax.set_xlabel("frequency (GHz)")
ax.set_ylabel("dB")
ax.legend(fontsize=8, loc="lower right")
ax.set_title("A 75 Ω line in a 50 Ω system: reflection peaks at odd quarter waves", fontsize=10)
save(fig, f"{OUT}/line.svg")

P = lambda m, a: m * cmath.exp(1j * math.radians(a))  # noqa: E731
s500 = np.array([[P(0.85, -60), P(0.03, 60)], [P(9, 120), P(0.7, -25)]])
x = np.linspace(-1.05, 1.05, 421)
gx, gy = np.meshgrid(x, x)
gl = gx + 1j * gy
gin = s500[0, 0] + s500[0, 1] * s500[1, 0] * gl / (1 - s500[1, 1] * gl)
unstable = ((np.abs(gl) < 1) & (np.abs(gin) > 1)).astype(float)
c, r = sparam.stability_circle(s500)
th = np.linspace(0, 2 * np.pi, 600)
fig, ax = plt.subplots(figsize=(5.0, 5.0))
ax.contourf(gx, gy, unstable, levels=[0.5, 1.5], colors=[PALETTE[1]], alpha=0.45)
ax.plot(np.cos(th), np.sin(th), color="k", lw=1.0, label="passive loads (|Γ| = 1)")
arc = c + r * np.exp(1j * th)
ax.plot(arc.real, arc.imag, color=PALETTE[0], lw=1.2, ls="--", label="stability circle")
mu = sparam.stability(s500)["mu"]
ax.add_patch(plt.Circle((0, 0), mu, fill=False, color="0.4", lw=0.8, ls=":"))
ax.text(0.05, -0.08, f"μ = {mu:.3f}", fontsize=8, color="0.3")
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect("equal")
ax.set_xlabel(r"Re $\Gamma_L$")
ax.set_ylabel(r"Im $\Gamma_L$")
ax.legend(fontsize=7, loc="lower left")
ax.set_title("Loads that make the 500 MHz transistor unstable (shaded)", fontsize=10)
save(fig, f"{OUT}/stability.svg")
