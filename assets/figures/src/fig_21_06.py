#!/usr/bin/env python3
"""Figures for chapter 21-06 (oscillators and VCOs).

Run from anywhere:  python assets/figures/src/fig_21_06.py
Outputs
  assets/figures/21-06/isf.svg      impulse sensitivity function of the Example 21-06.1 oscillator (Q = 11.54, loop
                                    gain 7) extracted by charge kicks in a simulation of its differential equation,
                                    against -sin(theta), with the tank voltage for reference
  assets/figures/21-06/pulling.svg  average oscillator frequency against injection frequency, both relative to the
                                    free-running frequency and in units of the lock range: Adler's prediction and
                                    simulated points (Q = 10, 5% injection, loop gain 3)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import vco  # noqa: E402

OUT = "assets/figures/21-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- ISF
Q = 1 / (1 / 15 + 1 / 50)
th = np.linspace(0, 2 * np.pi, 24, endpoint=False)
g = vco.isf(Q, 1.0, Q / 7.01, th)
x = np.linspace(0, 2 * np.pi, 400)
fig, ax = plt.subplots(figsize=(5.6, 3.9))
ax.plot(np.degrees(x), np.cos(x), color="0.6", lw=1, ls=":", label="tank voltage, v/V = cos θ")
ax.plot(np.degrees(x), -np.sin(x), color=PALETTE[0], lw=1.4, label="ideal tank, Γ = −sin θ")
ax.plot(np.degrees(th), g, "o", color=PALETTE[1], ms=4, label="simulated oscillator (Q = 11.5)")
ax.axhline(0, color="k", lw=0.5)
ax.set_xticks(range(0, 361, 90))
ax.set_xlabel("phase at which the charge arrives, θ (degrees)")
ax.set_ylabel("phase shift per unit charge, Γ(θ)")
ax.set_title("A kick at a zero crossing shifts the phase; one at a peak does not", fontsize=10)
ax.set_ylim(-1.15, 1.75)
ax.legend(fontsize=8, loc="upper center", ncol=2)
save(fig, f"{OUT}/isf.svg")

# ---------------------------------------------------------------- pulling
Qa, Va, r = 10.0, 10.0 / 3, 0.05
w_free = vco.free_running_shift(Qa, 1.0, Va)
amp = math.hypot(*vco.settle(Qa, 1.0, Va))
wL = vco.lock_range(1 / (2 * math.pi), Qa, r) * 2 * math.pi
xs = np.linspace(-4, 4, 801)
ys = np.where(np.abs(xs) <= 1, xs, xs - np.sign(xs) * np.sqrt(np.maximum(xs * xs - 1, 0)))
pts = [-3.0, -2.0, -0.5, 0.5, 1.5, 2.0, 3.0]
sim = []
for m in pts:
    rate, _, _ = vco.injection_beat(Qa, 1.0, Va, r * amp / Qa, w_free + m * wL, cycles=1500, skip=300)
    sim.append(m + rate / wL)
fig, ax = plt.subplots(figsize=(5.6, 3.8))
ax.plot(xs, xs, color="0.7", lw=0.8, ls="--", label="oscillator at the injection frequency")
ax.plot(xs, ys, color=PALETTE[0], lw=1.6, label="Adler's equation")
ax.plot(pts, sim, "o", color=PALETTE[1], ms=5, label="simulated (Q = 10, 5% injection)")
ax.axvspan(-1, 1, color=PALETTE[2], alpha=0.12, lw=0)
ax.text(0, -3.2, "locked", ha="center", fontsize=9)
ax.set_xlabel("injection frequency − free-running frequency (lock ranges)")
ax.set_ylabel("average oscillator frequency shift (lock ranges)")
ax.set_title("Inside the lock range the oscillator follows; outside it is pulled", fontsize=10)
ax.legend(fontsize=8, loc="upper left")
ax.set_xlim(-4, 4); ax.set_ylim(-4, 4)
save(fig, f"{OUT}/pulling.svg")
