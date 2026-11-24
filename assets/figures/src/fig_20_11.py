#!/usr/bin/env python3
"""Figures for chapter 20-11 (layout, matching and PVT variation).

Run from anywhere:  python assets/figures/src/fig_20_11.py
Outputs
  assets/figures/20-11/pelgrom.svg   sigma(dV_T) of a pair against gate area for A_VT = 3.5 mV um: Pelgrom's law and a
                                     seeded Monte Carlo of independent unit cells
  assets/figures/20-11/gmid.svg      mirror current mismatch and pair offset against gm/ID (Example 20-11.2 values)
  assets/figures/20-11/ci.svg        95% confidence limits on a Monte Carlo estimate of sigma against the number of runs
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "20-analog-and-mixed-signal-ic-design" / "labs" / "20-11-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import matching  # noqa: E402

OUT = "assets/figures/20-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(2011)

# ---------------------------------------------------------------- figure 2: Pelgrom
area = np.logspace(-1, 3, 200)
pts = np.array([0.25, 1, 4, 16, 64, 256])
mc = [matching.mc_pair(3.5, a, 1, 64, 4000, rng).std(ddof=1) for a in pts]
fig, ax = plt.subplots(figsize=(6.0, 4.0))
ax.loglog(area, 3.5 / np.sqrt(area), color=PALETTE[0], lw=1.4, label=r"$A_{VT}/\sqrt{WL}$, $A_{VT}$ = 3.5 mV·µm")
ax.loglog(pts, mc, "o", color=PALETTE[1], label="Monte Carlo, 4000 pairs each")
for a, txt in ((1, "1 µm²"), (100, "100 µm²")):
    ax.annotate(f"{3.5 / math.sqrt(a):.2f} mV at {txt}", (a, 3.5 / math.sqrt(a)), textcoords="offset points",
                xytext=(8, 8), fontsize=8)
ax.set_xlabel("gate area WL (µm²)")
ax.set_ylabel(r"$\sigma(\Delta V_T)$ (mV)")
ax.legend(fontsize=8)
ax.set_title("Pelgrom's law: four times the area halves the mismatch", fontsize=10)
save(fig, f"{OUT}/pelgrom.svg")

# ---------------------------------------------------------------- figure 3: gm/ID
svt, sb = 3.5e-3 / math.sqrt(10), 0.01 / math.sqrt(10)
g = np.linspace(3, 25, 300)
fig, ax = plt.subplots(figsize=(6.0, 4.0))
ax.plot(g, [matching.mirror_sigma(k, svt, sb) * 100 for k in g], color=PALETTE[0], lw=1.4,
        label=r"mirror $\sigma(\Delta I/I)$ (%)")
ax.plot(g, [matching.pair_offset_sigma(k, svt, sb) * 1e3 for k in g], color=PALETTE[1], lw=1.4,
        label=r"pair $\sigma(V_{os})$ (mV)")
ax.axhline(svt * 1e3, color="0.5", lw=0.8, ls="--")
ax.text(24.5, svt * 1e3 - 0.12, r"$\sigma(\Delta V_T)$", ha="right", fontsize=8, color="0.4")
ax.set_xlabel(r"$g_m/I_D$ (V$^{-1}$)")
ax.set_ylabel("mismatch")
ax.set_ylim(0, 3)
ax.legend(fontsize=8, loc="upper left")
ax.set_title(r"10 µm × 1 µm devices: mirrors want low $g_m/I_D$, pairs want high", fontsize=10)
save(fig, f"{OUT}/gmid.svg")

# ---------------------------------------------------------------- figure 4: confidence interval on sigma
n = np.unique(np.round(np.logspace(1, 4, 120)).astype(int))
lo, hi = np.array([matching.sigma_ci(k) for k in n]).T
fig, ax = plt.subplots(figsize=(6.0, 4.0))
ax.semilogx(n, hi, color=PALETTE[0], lw=1.4, label="upper 95% limit")
ax.semilogx(n, lo, color=PALETTE[1], lw=1.4, label="lower 95% limit")
ax.axhline(1, color="0.5", lw=0.8)
for k in (100, 1000):
    a, b = matching.sigma_ci(k)
    ax.plot([k, k], [a, b], color="0.3", lw=0.8, marker="_", ms=10)
    ax.annotate(f"{k} runs: {a:.3f}–{b:.3f}", (k, b), textcoords="offset points", xytext=(6, 4), fontsize=8)
ax.set_xlabel("number of Monte Carlo runs")
ax.set_ylabel("true σ / estimated σ")
ax.set_ylim(0.6, 1.6)
ax.legend(fontsize=8)
ax.set_title("How well a Monte Carlo pins down σ", fontsize=10)
save(fig, f"{OUT}/ci.svg")
