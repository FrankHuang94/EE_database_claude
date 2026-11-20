#!/usr/bin/env python3
"""Figures for chapter 12-08 (op-amp internals).

Run from anywhere:  python assets/figures/src/fig_12_08.py
Outputs SVGs to assets/figures/12-08/:
- slew.svg: the unity-gain follower step response of Example 12-08.1's two-stage op-amp for a 1 V step up
  and down, from a large-signal model (square-law input pair saturating at I_SS = 20 uA; square-law second
  stage at I_7 = 100 uA that can cut off; C_c = 1.1 pF, C_L = 5 pF, C_1 = 0.2 pF), integrated with Radau,
  with the slew-rate lines I_7/(C_L + C_c) and I_SS/C_c for reference.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
ISS, I7, VOV, LAM, CC, CL, C1 = 20e-6, 100e-6, 0.2, 0.1, 1.1e-12, 5e-12, 0.2e-12


def step(v0, vs):
    k1, k6 = 2 * (ISS / 2) / VOV ** 2, 2 * I7 / VOV ** 2
    R1, R2 = 1 / (LAM * ISS / 2) / 2, 1 / (LAM * I7) / 2
    lim = math.sqrt(2 * ISS / k1)

    def i1(x):
        return math.copysign(ISS, x) if abs(x) >= lim else (k1 / 2) * x * math.sqrt(4 * ISS / k1 - x * x)

    def i6(v1):
        return (k6 / 2) * (VOV + v1) ** 2 - I7 if v1 > -VOV else -I7

    Ci = np.linalg.inv(np.array([[C1 + CC, -CC], [-CC, CL + CC]]))
    x0 = fsolve(lambda x: [-i1(v0 - x[1]) - x[0] / R1, -i6(x[0]) - x[1] / R2], [0.0, v0], xtol=1e-12)
    sol = solve_ivp(lambda t, x: Ci @ np.array([-i1(vs - x[1]) - x[0] / R1, -i6(x[0]) - x[1] / R2]),
                    (0, 0.3e-6), x0, method="Radau", max_step=1e-9, rtol=1e-9, atol=1e-12)
    return sol.t, sol.y[1]


def fig_slew():
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    for (v0, vs), col, lab in (((-0.5, 0.5), PALETTE[0], "rising"), ((0.5, -0.5), PALETTE[1], "falling")):
        t, vo = step(v0, vs)
        ax.plot(t * 1e9, vo, color=col, lw=1.8, label=f"{lab} step")
    t = np.linspace(0, 80e-9, 10)
    ax.plot(t * 1e9 + 8, -0.5 + I7 / (CL + CC) * t, ":", color=PALETTE[0], lw=1, label="I_7/(C_L + C_c) = 16.4 V/µs")
    ax.plot(t * 1e9 + 8, 0.5 - ISS / CC * t, ":", color=PALETTE[1], lw=1, label="I_SS/C_c = 18.2 V/µs")
    ax.set_xlim(0, 200)
    ax.set_ylim(-0.6, 0.6)
    ax.set_xlabel("time (ns)")
    ax.set_ylabel("output (V)")
    ax.legend(fontsize=7.5, loc="center right")
    fig.tight_layout()
    save(fig, f"{OUT}/slew.svg")


if __name__ == "__main__":
    fig_slew()
