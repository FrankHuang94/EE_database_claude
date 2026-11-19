#!/usr/bin/env python3
"""Figures for chapter 10-09 (real op-amps).

Run from anywhere:  python assets/figures/src/fig_10_09.py
Outputs SVGs to assets/figures/10-09/:
- gbw.svg: a single-pole open-loop gain (A_0 = 130 dB, GBW = 10 MHz, the TLV9062's typical figures) with the
  closed-loop responses for noise gains of 1, 10 and 100, showing bandwidth = GBW / noise gain;
- slew.svg: step response of a unity-gain follower with a 10 MHz single pole and a 6.5 V/us slew-rate limit,
  for a 50 mV step (linear, exponential) and a 2 V step (slew-limited ramp, then exponential).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
A0 = 10 ** (130 / 20)
GBW = 10e6
FP = GBW / A0


def fig_gbw():
    f = np.logspace(-1, 8, 600)
    a = A0 / (1 + 1j * f / FP)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.semilogx(f, 20 * np.log10(np.abs(a)), color="k", lw=1.2, label="open loop $A(f)$")
    for g, col in ((1, PALETTE[0]), (10, PALETTE[1]), (100, PALETTE[2])):
        beta = 1 / g
        acl = a / (1 + a * beta)
        ax.semilogx(f, 20 * np.log10(np.abs(acl)), color=col, label=f"noise gain {g}: $f_{{-3dB}}$ = {GBW / g / 1e6:g} MHz")
        ax.plot(GBW / g, 20 * np.log10(g) - 3.01, "o", color=col, ms=4)
    ax.set_ylim(-20, 140)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("gain (dB)")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/gbw.svg")


def step(vstep, sr=6.5e6, fc=10e6, t_end=1.2e-6):
    tau = 1 / (2 * np.pi * fc)

    def rhs(t, y):
        return [np.clip((vstep - y[0]) / tau, -sr, sr)]
    t = np.linspace(0, t_end, 1200)
    sol = solve_ivp(rhs, (0, t_end), [0.0], t_eval=t, max_step=1e-9)
    return sol.t, sol.y[0]


def fig_slew():
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.4))
    t, y = step(0.05)
    a.plot(t * 1e6, y * 1e3, color=PALETTE[0])
    a.set_title("(a) 50 mV step: linear settling, $\\tau$ = 16 ns", fontsize=10)
    a.set_xlabel("time (µs)")
    a.set_ylabel("output (mV)")
    t, y = step(2.0)
    b.plot(t * 1e6, y, color=PALETTE[1], label="slew-limited response")
    b.plot(t * 1e6, 2.0 * (1 - np.exp(-t * 2 * np.pi * 10e6)), color="0.6", ls="--", label="linear (no slew limit)")
    b.set_title("(b) 2 V step: 6.5 V/µs ramp, then settling", fontsize=10)
    b.set_xlabel("time (µs)")
    b.set_ylabel("output (V)")
    b.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/slew.svg")


if __name__ == "__main__":
    fig_gbw()
    fig_slew()
