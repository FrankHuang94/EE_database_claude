#!/usr/bin/env python3
"""Figures for chapter 18-06 (ADC, DAC and PWM).

Run from anywhere:  python assets/figures/src/fig_18_06.py
Outputs
  assets/figures/18-06/sampling-error.svg  DC error of a multiplexed 12-bit input with 100 nF at the pin against the
                                          sample rate, for 1, 10 and 100 kOhm sources (3.3 V swing, C_sh = 3.3 pF;
                                          exact period-by-period recursion of section 3.2), with half an LSB marked
  assets/figures/18-06/pwm-rc.svg          a 10-bit, 62.5 kHz PWM at 50% through RC filters with tau = 0.4 ms and
                                          4.096 ms, from 0 V: the faster filter settles sooner but ripples ten times
                                          more (section 3.6, Example 18-06.6)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs" / "18-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import mcuanalog as ma  # noqa: E402

OUT = "assets/figures/18-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- sampling error against rate
f = np.logspace(1, 6, 300)
fig, ax = plt.subplots(figsize=(7.2, 4.0))
for i, rs in enumerate((1e3, 10e3, 100e3)):
    err = [3.3 - ma.mux_equilibrium(3.3, rs, 100e-9, 3.3e-12, x)[1] for x in f]
    ax.loglog(f, np.array(err) * 1e3, color=PALETTE[i], label=f"R_s = {rs / 1e3:g} kΩ")
ax.axhline(ma.lsb(3.3, 12) / 2 * 1e3, color="grey", linestyle=":", label="half an LSB (12 bits, 3.3 V)")
ax.set_xlabel("sample rate of this channel (Hz)")
ax.set_ylabel("sampled-value error (mV)")
ax.set_title("100 nF at the pin, S/H (3.3 pF) arriving from 0 V each time", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/sampling-error.svg")

# ---------------------------------------------------------------- PWM through RC
T = 16e-6
fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.6), gridspec_kw={"width_ratios": [1.4, 1]})
for i, tau in enumerate((0.4096e-3, 4.096e-3)):
    t, vv = ma.pwm_simulate(3.3, 0.5, T, tau, n_periods=2000, points_per_phase=20)
    axs[0].plot(t * 1e3, vv, color=PALETTE[i], label=f"τ = {tau * 1e3:g} ms")
    t2, v2 = ma.pwm_simulate(3.3, 0.5, T, tau, n_periods=4, v0=1.65 - ma.pwm_ripple_exact(3.3, 0.5, T, tau) / 2,
                             points_per_phase=50)
    axs[1].plot(t2 * 1e6, (v2 - 1.65) * 1e3, color=PALETTE[i],
                label=f"τ = {tau * 1e3:g} ms: {ma.pwm_ripple_exact(3.3, 0.5, T, tau) * 1e3:.1f} mV p-p")
axs[0].axhline(1.65, color="grey", linestyle=":")
axs[0].set_xlabel("time (ms)")
axs[0].set_ylabel("filter output (V)")
axs[0].set_title("settling from 0 V", fontsize=10)
axs[0].legend(fontsize=8)
axs[1].set_xlabel("time (µs), four PWM periods in steady state")
axs[1].set_ylabel("output − 1.65 V (mV)")
axs[1].set_title("ripple", fontsize=10)
axs[1].set_ylim(-20, 34)
axs[1].legend(fontsize=8, loc="upper center", ncol=1)
fig.suptitle("10-bit PWM at 62.5 kHz, 50% duty, through one RC: speed against ripple", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/pwm-rc.svg")
