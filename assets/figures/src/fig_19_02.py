#!/usr/bin/env python3
"""Figures for chapter 19-02 (the CMOS inverter: dynamic behavior and delay).

Run from anywhere:  python assets/figures/src/fig_19_02.py
Outputs
  assets/figures/19-02/step-response.svg   output of a step-driven inverter discharging 20 fF (kn = 200 uA/V^2,
                                           VDD = 1.2 V, VTN = 0.35 V, lambda = 0): the exact square-law curve,
                                           integrated numerically, against the RC model with R_eq = 12.57 kOhm,
                                           with the end of saturation and both 50% crossings marked
  assets/figures/19-02/supply-scaling.svg  delay, energy and energy-delay product against supply (VT = 0.35 V),
                                           each normalized to its value at 1.2 V, for alpha = 1.3 and alpha = 2,
                                           with the EDP minima 3 VT / (3 - alpha) marked
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
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import delay as dl  # noqa: E402

OUT = "assets/figures/19-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- figure 1: step response against the RC model
C, K, VDD, VT = 20e-15, 200e-6, 1.2, 0.35
VOV = VDD - VT
t = np.linspace(0, 600e-12, 1201)
sol = solve_ivp(lambda _t, y: [-dl.i_nmos(K, VOV, y[0]) / C], (0, t[-1]), [VDD], t_eval=t, rtol=1e-10, atol=1e-14,
                max_step=1e-13)
req = dl.r_eq(K, VDD, VT)
rc = VDD * np.exp(-t / (req * C))
t_exact = dl.tp_step_exact(C, K, VDD, VT)
t_rc = dl.tp_rc(req, C)
t_sat = C * VT / (0.5 * K * VOV ** 2)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.plot(t * 1e12, sol.y[0], color=PALETTE[0], label="exact (square law)")
ax.plot(t * 1e12, rc, color=PALETTE[1], ls="--", label=f"RC model, $R_{{eq}}$ = {req / 1e3:.2f} kΩ")
ax.axhline(VDD / 2, color="0.6", lw=0.8)
ax.axhline(VOV, color="0.8", lw=0.8, ls=":")
ax.text(590, VOV + 0.02, "$V_{ov}$: NMOS leaves saturation", ha="right", fontsize=8, color="0.4")
ax.plot([t_sat * 1e12], [VOV], "o", color=PALETTE[0], ms=4)
ax.plot([t_exact * 1e12], [VDD / 2], "o", color=PALETTE[0], ms=5)
ax.plot([t_rc * 1e12], [VDD / 2], "s", color=PALETTE[1], ms=5)
ax.annotate(f"{t_exact * 1e12:.1f} ps", (t_exact * 1e12, VDD / 2), (t_exact * 1e12 - 95, VDD / 2 - 0.22),
            arrowprops=dict(arrowstyle="->", color=PALETTE[0]), color=PALETTE[0], fontsize=9)
ax.annotate(f"{t_rc * 1e12:.1f} ps", (t_rc * 1e12, VDD / 2), (t_rc * 1e12 + 40, VDD / 2 + 0.15),
            arrowprops=dict(arrowstyle="->", color=PALETTE[1]), color=PALETTE[1], fontsize=9)
ax.set_xlabel("time after the input step (ps)")
ax.set_ylabel("$V_{out}$ (V)")
ax.set_xlim(0, 600)
ax.set_ylim(0, 1.3)
ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.9))
save(fig, f"{OUT}/step-response.svg")

# ---------------------------------------------------------------- figure 2: delay, energy and EDP against supply
VTS = 0.35
v = np.linspace(0.45, 1.6, 600)
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8), sharey=True)
for ax, alpha in zip(axes, (1.3, 2.0)):
    d = dl.delay_vs_supply(v, VTS, alpha) / dl.delay_vs_supply(1.2, VTS, alpha)
    e = (v / 1.2) ** 2
    ax.plot(v, d, color=PALETTE[0], label="delay")
    ax.plot(v, e, color=PALETTE[2], label="energy")
    ax.plot(v, d * e, color=PALETTE[1], lw=2, label="EDP")
    vopt = dl.edp_optimal_vdd(VTS, alpha)
    ax.axvline(vopt, color=PALETTE[1], ls=":", lw=1)
    ax.text(vopt + 0.03, 3.3, f"EDP min\n{vopt:.3f} V", color=PALETTE[1], fontsize=8)
    ax.set_title(f"α = {alpha:g}", fontsize=10)
    ax.set_xlabel("$V_{DD}$ (V)")
    ax.set_ylim(0, 4)
    ax.set_xlim(0.45, 1.6)
axes[0].set_ylabel("relative to 1.2 V")
axes[0].legend(loc="upper right")
save(fig, f"{OUT}/supply-scaling.svg")
print("t_exact", t_exact, "t_rc", t_rc, "t_sat", t_sat, math.isclose(req, 12572.8, rel_tol=1e-4))
