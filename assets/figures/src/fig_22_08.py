#!/usr/bin/env python3
"""Figures for chapter 22-08 (PMICs and power management for SoCs).

Run from anywhere:  python assets/figures/src/fig_22_08.py
Outputs
  assets/figures/22-08/light-load-efficiency.svg  efficiency against load of Example 22-08.2's buck in forced PWM and
                                                  in PFM, with the 119 mA crossover marked
  assets/figures/22-08/dvs-ramp.svg               a 0.2 mV/µs DVS ramp on Example 22-07.3's closed-loop buck: reference
                                                  and output (top) and the output's lead over the reference (bottom),
                                                  from a state-space simulation of the averaged converter and network
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import pmic  # noqa: E402

OUT = "assets/figures/22-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_light_load():
    i = np.logspace(-5, 0, 400)
    po = 1.8 * i
    e_pwm = 100 * po / (po + pmic.pwm_loss(i, 20e-3, 0.2))
    e_pfm = 100 * po / (po + pmic.pfm_loss(i, 3.6, 1e-6, 0.12, 0.6))
    ix = pmic.pfm_pwm_crossover(20e-3, 0.2, 3.6, 1e-6, 0.12, 0.6)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.semilogx(i * 1e3, e_pwm, color=PALETTE[0], label="forced PWM")
    ax.semilogx(i * 1e3, e_pfm, color=PALETTE[1], label="PFM")
    ax.semilogx(i * 1e3, np.maximum(e_pwm, e_pfm), color="0.15", lw=2.4, alpha=0.35, label="auto (best of both)")
    ax.axvline(ix * 1e3, color="0.5", ls=":")
    ax.text(ix * 1e3 * 1.15, 20, f"crossover {ix * 1e3:.0f} mA", fontsize=8)
    ax.set_xlabel("load current (mA)")
    ax.set_ylabel("efficiency (%)")
    ax.set_ylim(0, 100)
    ax.legend(fontsize=8, loc="lower left", bbox_to_anchor=(0.0, 0.25))
    ax.set_title("3.6 V to 1.8 V buck: PFM wins at light load, PWM at heavy load", fontsize=10)
    save(fig, f"{OUT}/light-load-efficiency.svg")


def fig_dvs():
    vg, vm, lb, cb, rl = 12.0, 1.0, 0.6e-6, 62.5e-6, 0.12
    r1, r2, c1, c2, r3, c3 = 10e3, 992.3005, 11.236714e-9, 0.6740832e-9, 599.89353, 1.0519160e-9
    t0, t1, slew = 0.1e-3, 1.1e-3, 200.0
    vref = lambda t: 1.0 + slew * min(max(t - t0, 0.0), t1 - t0)

    def f(t, y):
        il, vo, v3, v1, v2 = y
        vr = vref(t)
        i_r3 = (vo - vr - v3) / r3
        i_in = (vo - vr) / r1 + i_r3
        i_r2 = (v2 - v1) / r2
        return [(vg * (vr - v2) / vm - vo) / lb, (il - vo / rl) / cb, i_r3 / c3, i_r2 / c1, (i_in - i_r2) / c2]
    y0 = [1.0 / rl, 1.0, 0.0, 1.0 - vm / vg, 1.0 - vm / vg]
    t = np.linspace(0, 1.4e-3, 2801)
    sol = integrate.solve_ivp(f, (0, 1.4e-3), y0, method="Radau", t_eval=t, rtol=1e-9, atol=1e-12, max_step=2e-6)
    vr = np.array([vref(x) for x in t])
    fig, ax = plt.subplots(2, 1, figsize=(6.0, 4.6), sharex=True)
    ax[0].plot(t * 1e3, vr, color=PALETTE[1], ls="--", label="reference")
    ax[0].plot(t * 1e3, sol.y[1], color=PALETTE[0], label="output")
    ax[0].set_ylabel("voltage (V)")
    ax[0].legend(fontsize=8)
    ax[1].plot(t * 1e3, (sol.y[1] - vr) * 1e3, color=PALETTE[0])
    lead = pmic.ramp_lead(slew, 1 / (r1 * (c1 + c2)), vm, vg)
    ax[1].axhline(lead * 1e3, color="0.5", ls=":")
    ax[1].text(0.45, lead * 1e3 + 2, f"S(1 − V_M/V_g)/ω_I = {lead * 1e3:.1f} mV", fontsize=8)
    ax[1].set_ylabel("output − reference (mV)")
    ax[1].set_xlabel("time (ms)")
    ax[1].set_ylim(-8, 32)
    ax[0].set_title("A 0.2 mV/µs DVS ramp on the type-III buck: the output leads", fontsize=10)
    save(fig, f"{OUT}/dvs-ramp.svg")


if __name__ == "__main__":
    fig_light_load()
    fig_dvs()
