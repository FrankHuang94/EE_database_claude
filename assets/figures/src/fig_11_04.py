#!/usr/bin/env python3
"""Figures for chapter 11-04 (LTI systems and differential/difference equations).

Run from anywhere:  python assets/figures/src/fig_11_04.py
Outputs SVGs to assets/figures/11-04/:
- dt-impulse.svg: impulse responses of (a) y[n] - 1.5 y[n-1] + 0.56 y[n-2] = x[n] (real roots 0.8 and 0.7,
  Example 11-04.3) and (b) the resonator y[n] - 1.2728 y[n-1] + 0.81 y[n-2] = x[n] (roots 0.9 e^{+-j pi/4},
  Example 11-04.4) with its envelope +-0.9^n / sin(pi/4);
- rlc-impulse.svg: Example 11-04.5, the capacitor-voltage impulse response of a series RLC circuit
  (L = 1 mH, C = 1 uF, R = 20 ohm) with its envelope and first peak;
- eigen.svg: (a) the magnitude of the three-point moving average's frequency response (1 + 2 cos w)/3 with
  the points of Example 11-04.7; (b) an RC low-pass driven at w = 1/tau: steady-state output 0.7071 times the
  input, lagging by 45 degrees.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/11-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_dt_impulse():
    n = np.arange(40)
    d = (n == 0).astype(float)
    ha = lfilter([1], [1, -1.5, 0.56], d)
    c = 2 * 0.9 * math.cos(math.pi / 4)
    hb = lfilter([1], [1, -c, 0.81], d)
    fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.2))
    axs[0].stem(n[:25], ha[:25], linefmt="C0-", markerfmt="C0o", basefmt=" ")
    axs[0].set_title("(a) real roots 0.8 and 0.7", fontsize=10)
    axs[1].stem(n, hb, linefmt="C3-", markerfmt="C3o", basefmt=" ")
    env = 0.9 ** n / math.sin(math.pi / 4)
    axs[1].plot(n, env, ls="--", color="0.5", lw=1)
    axs[1].plot(n, -env, ls="--", color="0.5", lw=1)
    axs[1].set_title("(b) complex roots 0.9 e^(±jπ/4)", fontsize=10)
    for ax in axs:
        ax.set_xlabel("n")
        ax.set_ylabel("h[n]")
    fig.tight_layout()
    save(fig, f"{OUT}/dt-impulse.svg")


def fig_rlc():
    L, C, R = 1e-3, 1e-6, 20.0
    w0 = 1 / math.sqrt(L * C)
    a = R / (2 * L)
    wd = math.sqrt(w0 ** 2 - a ** 2)
    t = np.linspace(0, 0.5e-3, 2001)
    h = w0 ** 2 / wd * np.exp(-a * t) * np.sin(wd * t)
    tp = math.atan(wd / a) / wd
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.plot(t * 1e6, h / 1e3, color=PALETTE[0], label="h(t)")
    ax.plot(t * 1e6, w0 ** 2 / wd * np.exp(-a * t) / 1e3, ls="--", color="0.5", lw=1, label="envelope")
    ax.plot(tp * 1e6, w0 ** 2 / wd * math.exp(-a * tp) * math.sin(wd * tp) / 1e3, "o", color=PALETTE[3])
    ax.set_xlabel("t (µs)")
    ax.set_ylabel("h(t) (10³ s⁻¹)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/rlc-impulse.svg")


def fig_eigen():
    w = np.linspace(0, np.pi, 400)
    H = (1 + 2 * np.cos(w)) / 3
    fig, axs = plt.subplots(1, 2, figsize=(8.6, 3.2))
    axs[0].plot(w / np.pi, np.abs(H), color=PALETTE[0])
    for wk in (0, 1 / 3, 2 / 3):
        axs[0].plot(wk, abs((1 + 2 * math.cos(wk * math.pi)) / 3), "o", color=PALETTE[3])
    axs[0].set_xlabel("ω / π (rad/sample)")
    axs[0].set_ylabel("|H| (gain)")
    axs[0].set_title("(a) three-point average", fontsize=10)
    tau = 1.0
    t = np.linspace(0, 4 * 2 * np.pi, 1200)
    axs[1].plot(t, np.cos(t), color=PALETTE[0], label="input cos(t/τ)")
    axs[1].plot(t, np.cos(t - np.pi / 4) / np.sqrt(2), color=PALETTE[3], label="output 0.707 cos(t/τ − 45°)")
    axs[1].set_xlabel("t / τ")
    axs[1].set_title("(b) RC low-pass at ω = 1/τ (steady state)", fontsize=10)
    axs[1].legend(fontsize=8, loc="lower right")
    axs[1].set_ylim(-1.4, 1.4)
    del tau
    fig.tight_layout()
    save(fig, f"{OUT}/eigen.svg")


if __name__ == "__main__":
    fig_dt_impulse()
    fig_rlc()
    fig_eigen()
