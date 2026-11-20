#!/usr/bin/env python3
"""Figures for chapter 16-11 (DSP hardware architectures).

Run from anywhere:  python assets/figures/src/fig_16_11.py
Outputs
  assets/figures/16-11/cordic.svg   left: the first six CORDIC rotations toward 30 degrees (each step +-arctan 2^-i,
                                    vectors scaled by 1/K so the final vector lands on the unit circle); right: the
                                    worst cos/sin error over angles in [-pi/2, pi/2] against the number of iterations
Uses labs/16-11-lab/hwarch.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "16-digital-signal-processing" / "labs" / "16-11-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import hwarch as hw  # noqa: E402

OUT = "assets/figures/16-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 4.0))
K = hw.cordic_gain(6)
x, y, z = 1.0, 0.0, math.radians(30)
pts = [(x / 1.0, y)]
gain = 1.0
for i in range(6):
    d = 1.0 if z >= 0 else -1.0
    x, y, z = x - d * y * 2.0**-i, y + d * x * 2.0**-i, z - d * math.atan(2.0**-i)
    gain *= math.sqrt(1 + 2.0 ** (-2 * i))
    pts.append((x / gain, y / gain))
t = np.linspace(0, math.pi / 2, 200)
a1.plot(np.cos(t), np.sin(t), color="0.6", lw=0.8)
for k, (px, py) in enumerate(pts):
    a1.annotate("", xy=(px, py), xytext=(0, 0), arrowprops={"arrowstyle": "->", "color": PALETTE[k % len(PALETTE)], "lw": 1.2})
    a1.text(px * 1.04, py * 1.04, str(k), fontsize=8)
a1.plot([0, math.cos(math.pi / 6)], [0, 0.5], ls="--", color="k", lw=0.8)
a1.set_aspect("equal")
a1.set_xlim(0, 1.15)
a1.set_ylim(-0.05, 1.0)
a1.set_title("Rotations by ±arctan 2^-i toward 30° (step numbers)", fontsize=9)
a1.set_xlabel("x")
a1.set_ylabel("y")
th = np.linspace(-math.pi / 2, math.pi / 2, 801)
ns = np.arange(4, 21)
worst = [max(max(abs(hw.cordic_rotate(a, int(n))[0] - math.cos(a)), abs(hw.cordic_rotate(a, int(n))[1] - math.sin(a)))
             for a in th) for n in ns]
a2.semilogy(ns, worst, "o-", color=PALETTE[0], label="worst error over angles")
a2.semilogy(ns, 2.0 ** (1 - ns), "--", color="0.5", label="2^(1-n)")
a2.set_xlabel("iterations n")
a2.set_ylabel("worst |error| in cos or sin")
a2.set_title("About one bit per iteration", fontsize=9)
a2.legend(fontsize=8)
fig.tight_layout(w_pad=2.0)
save(fig, f"{OUT}/cordic.svg")
print("figures written to", OUT)
