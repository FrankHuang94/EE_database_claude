#!/usr/bin/env python3
"""Figures for chapter 19-07 (sequential circuits, timing and clocking).

Run from anywhere:  python assets/figures/src/fig_19_07.py
Outputs
  assets/figures/19-07/metastability.svg   node voltages of the lab's cross-coupled inverter pair (10 fF per node,
                                           k = 200 uA/V^2, VDD = 1.2 V) released from 0.6 V with offsets of 1 mV,
                                           1 uV and 1 nV, and the resolution time against log(1/offset) with slope
                                           tau = 100 ps
  assets/figures/19-07/pipelining.svg      cycle time, throughput and overhead share against pipeline depth for 2000 ps
                                           of logic and 60 ps of overhead per stage
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import timing as tm  # noqa: E402

OUT = "assets/figures/19-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def traj(dv0, k=200e-6, c=10e-15, vdd=1.2, vt=0.35):
    def f(_t, x):
        a, b = x
        return [(tm.i_sq(k, vdd - b - vt, vdd - a) - tm.i_sq(k, b - vt, a)) / c,
                (tm.i_sq(k, vdd - a - vt, vdd - b) - tm.i_sq(k, a - vt, b)) / c]
    t = np.linspace(0, 2.6e-9, 2001)
    s = solve_ivp(f, (0, t[-1]), [vdd / 2 + dv0 / 2, vdd / 2 - dv0 / 2], t_eval=t, method="LSODA", rtol=1e-12,
                  atol=1e-18)
    return t, s.y


fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.8))
for dv0, color, lab in ((1e-3, PALETTE[0], "1 mV"), (1e-6, PALETTE[1], "1 µV"), (1e-9, PALETTE[2], "1 nV")):
    t, y = traj(dv0)
    axes[0].plot(t * 1e12, y[0], color=color, label=lab)
    axes[0].plot(t * 1e12, y[1], color=color, ls="--")
axes[0].set_xlabel("time (ps)")
axes[0].set_ylabel("node voltages (V)")
axes[0].legend(title="initial offset", loc="center right")
offs = np.logspace(-9, -3, 7)
tr = [tm.resolve_time(o) for o in offs]
axes[1].semilogx(1 / offs, np.array(tr) * 1e12, "o-", color=PALETTE[0])
axes[1].set_xlabel("1 / initial offset (1/V)")
axes[1].set_ylabel("time to reach 0.9 V (ps)")
axes[1].set_title(f"slope = τ ln 10 per decade, τ = {tm.tau_small_signal() * 1e12:.0f} ps", fontsize=9)
save(fig, f"{OUT}/metastability.svg")

n = np.arange(1, 33)
tc = 2000 / n + 60
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(n, 1e3 / tc, color=PALETTE[0], label="throughput (GHz)")
ax.plot(n, 1e3 / (2000 + 60 * 0) * n, color="0.7", ls=":", label="ideal (no overhead)")
ax2 = ax.twinx()
ax2.plot(n, 100 * 60 / tc, color=PALETTE[1], ls="--", label="overhead share (%)")
ax2.set_ylabel("overhead share of the cycle (%)", color=PALETTE[1])
ax.set_xlabel("pipeline stages N")
ax.set_ylabel("throughput (GHz)")
ax.set_ylim(0, 12)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left")
save(fig, f"{OUT}/pipelining.svg")
