#!/usr/bin/env python3
"""Figure for chapter 15-08 (PID control).

Run from anywhere:  python assets/figures/src/fig_15_08.py
Outputs assets/figures/15-08/windup.svg: Example 15-08.4's thermal loop (Kp = 14 W/K, Ki = 5 W/(K s),
actuator limited to +/-10 W, 4 K setpoint step); left, temperature without anti-windup, with back-calculation
(Tt = Ti), with clamping and with no actuator limit; right, the actuator power and, dashed, the integral term
Ki*z without anti-windup and with back-calculation.
Uses labs/15-08-lab/pid.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "15-control-systems" / "labs" / "15-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import pid  # noqa: E402

OUT = "assets/figures/15-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_windup():
    P1, Kp, Ki = ([0.5], [10, 1]), 14.0, 5.0
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.6))
    cases = (("none", 10, "no anti-windup", PALETTE[3]), ("back", 10, "back-calculation", PALETTE[0]),
             ("clamp", 10, "clamping", PALETTE[2]), ("none", 1e9, "no actuator limit", "gray"))
    for aw, lim, lab, col in cases:
        t, y, u, ur = pid.simulate(P1, Kp, Ki, umin=-lim, umax=lim, aw=aw, r=lambda t: 4.0, t_end=60, dt=2e-3)
        ls = ":" if lim > 100 else "-"
        a1.plot(t, y, color=col, ls=ls, label=lab)
        if lim < 100:
            a2.plot(t, u, color=col, label=f"u, {lab}")
            if aw in ("none", "back"):
                a2.plot(t, ur - Kp * (4.0 - y), color=col, ls="--", lw=0.9, label=f"$K_iz$, {lab}")
    a1.axhline(4.0, color="k", lw=0.6)
    a1.set_xlabel("t (s)")
    a1.set_ylabel("temperature rise (K)")
    a1.set_title("Example 15-08.4: 4 K step, actuator limited to ±10 W", fontsize=9)
    a1.legend(fontsize=7, loc="lower right")
    a2.axhline(8.0, color="k", lw=0.6, ls=":")
    a2.text(28, 5.6, "8 W needed in steady state", fontsize=7)
    a2.set_ylim(-12, 40)
    a2.set_xlabel("t (s)")
    a2.set_ylabel("power (W)")
    a2.set_title("actuator power and integral term (the latter clipped at 40 W)", fontsize=9)
    a2.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/windup.svg")


if __name__ == "__main__":
    fig_windup()
