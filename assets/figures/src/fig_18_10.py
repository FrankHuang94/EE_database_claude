#!/usr/bin/env python3
"""Figures for chapter 18-10 (sensors).

Run from anywhere:  python assets/figures/src/fig_18_10.py
Outputs
  assets/figures/18-10/complementary-filter.svg  tilt held at 0 deg, estimated from an accelerometer (0.02 g of noise
                                                per sample), from a gyroscope with a 0.5 deg/s bias, and by a
                                                complementary filter with alpha = 0.98 at 100 Hz (Example 18-10.4)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/18-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

dt, n, alpha = 0.01, 2000, 0.98
rng = np.random.default_rng(1810)
acc = np.degrees(np.arctan2(rng.normal(0, 0.02, n), 1.0))
gyro = 0.5 + rng.normal(0, 0.05, n)
theta_g = np.cumsum(gyro * dt)
fused = np.empty(n)
th = 0.0
for k in range(n):
    th = alpha * (th + gyro[k] * dt) + (1 - alpha) * acc[k]
    fused[k] = th
t = np.arange(n) * dt
fig, ax = plt.subplots(figsize=(8.0, 4.0))
ax.plot(t, acc, color=PALETTE[0], linewidth=0.6, alpha=0.6, label="accelerometer tilt (noisy, no drift)")
ax.plot(t, theta_g, color=PALETTE[1], label="integrated gyroscope (smooth, drifts 0.5 °/s)")
ax.plot(t, fused, color=PALETTE[2], linewidth=1.6, label="complementary filter, α = 0.98 (τ = 0.49 s)")
ax.axhline(0.5 * 0.49, color="grey", linestyle=":", label="predicted bias error bτ = 0.245°")
ax.set_ylim(-4, 10)
ax.set_xlabel("time (s)")
ax.set_ylabel("tilt estimate (°); true tilt 0°")
ax.legend(fontsize=8, loc="upper left")
ax.set_title("Fusing a noisy accelerometer with a drifting gyroscope", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/complementary-filter.svg")
