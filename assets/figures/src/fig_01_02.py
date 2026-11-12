#!/usr/bin/env python3
"""Figures for chapter 01-02 (limits and continuity).

Run:  python assets/figures/src/fig_01_02.py  -> assets/figures/01-02/*.svg
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/01-02"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_sinc():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
    x = np.linspace(-4 * np.pi, 4 * np.pi, 2001)
    x = x[x != 0]
    a1.plot(x, np.sin(x) / x, color=B)
    a1.plot([0], [1], "o", mfc="white", mec=B, ms=7, zorder=5)
    a1.annotate("undefined at x = 0,\nbut the limit is 1", xy=(0, 1), xytext=(3, 0.8),
                arrowprops=dict(arrowstyle="->", color="0.3"), fontsize=9)
    a1.axhline(0, color="0.6", lw=0.8)
    a1.set_xlabel("x (rad)")
    a1.set_title("sin(x)/x")
    # unit-circle squeeze geometry
    th = 0.7
    t = np.linspace(0, np.pi / 2, 200)
    a2.plot(np.cos(t), np.sin(t), color="0.5")
    a2.fill([0, math.cos(th), 1], [0, math.sin(th), 0], color=B, alpha=0.25, label="small triangle: ½ sin θ")
    ts = np.linspace(0, th, 100)
    a2.fill(np.r_[0, np.cos(ts)], np.r_[0, np.sin(ts)], color=O, alpha=0.25, label="sector: ½ θ")
    a2.fill([0, 1, 1], [0, 0, math.tan(th)], color=G, alpha=0.15, label="large triangle: ½ tan θ")
    a2.plot([0, 1, 1, 0], [0, 0, math.tan(th), 0], color=G, lw=1)
    a2.plot([0, math.cos(th)], [0, math.sin(th)], color=B, lw=1)
    a2.plot([math.cos(th), math.cos(th)], [0, math.sin(th)], color=B, lw=1, ls="--")
    a2.text(0.2, 0.06, "θ", fontsize=11)
    a2.text(math.cos(th) + 0.02, math.sin(th) / 2 - 0.05, "sin θ", fontsize=9, color=B)
    a2.text(1.02, math.tan(th) / 2, "tan θ", fontsize=9, color=G)
    a2.set_aspect("equal")
    a2.set_xlim(-0.05, 1.35)
    a2.set_ylim(-0.05, 1.05)
    a2.set_title("Unit circle: ½ sin θ ≤ ½ θ ≤ ½ tan θ")
    a2.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/sinc-and-squeeze.svg")


def fig_discontinuities():
    fig, ax = plt.subplots(1, 4, figsize=(12, 3.2))
    x = np.linspace(0, 4, 400)
    # removable
    ax[0].plot(x, x + 1, color=B)
    ax[0].plot([2], [3], "o", mfc="white", mec=B, ms=7)
    # jump
    xl, xr = x[x < 2], x[x >= 2]
    ax[1].plot(xl, 0 * xl, color=B)
    ax[1].plot(xr, 0 * xr + 1, color=B)
    ax[1].plot([2], [0], "o", mfc="white", mec=B, ms=7)
    ax[1].plot([2], [1], "o", color=B, ms=7)
    ax[1].set_ylim(-0.3, 1.3)
    ax[1].set_title("Jump\nunit step u(x−2)")
    # infinite
    xl = np.linspace(0, 1.9, 200)
    xr = np.linspace(2.1, 4, 200)
    ax[2].plot(xl, 1 / (xl - 2), color=B)
    ax[2].plot(xr, 1 / (xr - 2), color=B)
    ax[2].axvline(2, color="0.6", ls="--", lw=0.8)
    ax[2].set_ylim(-10, 10)
    ax[2].set_title("Infinite\n1/(x−2)")
    # oscillatory
    xo = np.linspace(-0.4, 0.4, 20001)
    xo = xo[xo != 0]
    ax[3].plot(xo, np.sin(1 / xo), color=B, lw=0.6)
    ax[3].set_title("Oscillatory\nsin(1/x) near 0")
    ax[0].set_title("Removable\nhole at x = 2")
    for a in ax:
        a.set_xlabel("x")
    fig.tight_layout()
    save(fig, f"{OUT}/discontinuities.svg")


def fig_switch():
    R, C, V = 10e3, 100e-9, 5.0
    tau = R * C
    t = np.linspace(-1e-3, 5e-3, 1201)
    v = np.where(t < 0, 0.0, V * (1 - np.exp(-np.clip(t, 0, None) / tau)))
    i = np.where(t < 0, 0.0, V / R * np.exp(-np.clip(t, 0, None) / tau))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6))
    a1.plot(t * 1e3, v, color=B)
    a1.axhline(V, color="0.6", ls="--", lw=0.8)
    a1.text(3.2, 4.6, "limit as t→∞: 5 V", fontsize=9)
    a1.set_xlabel("t (ms)")
    a1.set_ylabel("v_C (V)")
    a1.set_title("Capacitor voltage: continuous at t = 0")
    tl, tr = t[t < 0], t[t >= 0]
    a2.plot(tl * 1e3, 0 * tl, color=O)
    a2.plot(tr * 1e3, V / R * np.exp(-tr / tau) * 1e3, color=O)
    a2.plot([0], [0], "o", mfc="white", mec=O, ms=6)
    a2.plot([0], [0.5], "o", color=O, ms=6)
    a2.annotate("i(0⁻) = 0", xy=(0, 0), xytext=(0.6, 0.05), fontsize=9)
    a2.annotate("i(0⁺) = 0.5 mA", xy=(0, 0.5), xytext=(0.6, 0.45), fontsize=9)
    a2.set_xlabel("t (ms)")
    a2.set_ylabel("i_C (mA)")
    a2.set_title("Capacitor current: jumps at t = 0")
    fig.tight_layout()
    save(fig, f"{OUT}/switch-one-sided-limits.svg")


def fig_asymptotes():
    x = np.logspace(-2, 2, 400)
    mag = 20 * np.log10(1 / np.sqrt(1 + x**2))
    asym = np.where(x < 1, 0.0, -20 * np.log10(x))
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.semilogx(x, mag, color=B, label="exact |H|")
    ax.semilogx(x, asym, color=O, ls="--", label="asymptotes: 0 dB and −20 dB/decade")
    ax.plot([1], [-3.01], "o", color=B)
    ax.annotate("−3.01 dB at f = f_c", xy=(1, -3.01), xytext=(1.6, 2), fontsize=9,
                arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.set_xlabel("f / f_c")
    ax.set_ylabel("|H| (dB)")
    ax.set_ylim(-42, 6)
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("Low-pass magnitude and its limits")
    fig.tight_layout()
    save(fig, f"{OUT}/lowpass-asymptotes.svg")


def fig_bisection():
    VT, Is = 0.02585, 1e-14

    def g(v):
        return (5 - v) / 1000 - Is * (np.exp(v / VT) - 1)

    V = np.linspace(0, 0.75, 400)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.5, 5.2), sharex=True,
                                 gridspec_kw={"height_ratios": [1.3, 1]})
    a1.plot(V, g(V) * 1e3, color=B, label="g(V): KCL mismatch at the diode node")
    a1.axhline(0, color="0.5", lw=0.8)
    a1.set_ylim(-6, 6)
    a1.set_ylabel("g(V) (mA)")
    a1.legend(fontsize=8, loc="lower left")
    a1.set_title("Bisection: each step keeps the half that still changes sign")
    a, b = 0.0, 1.0
    for k in range(8):
        a2.plot([a, b], [k, k], color=O, lw=3, solid_capstyle="butt")
        a2.text(min(b, 1.0) + 0.01, k, f"[{a:.4f}, {b:.4f}]", fontsize=7, va="center")
        m = (a + b) / 2
        if g(m) > 0:
            a = m
        else:
            b = m
    a2.axvline(0.69249, color=B, ls="--", lw=0.8)
    a2.set_xlim(0, 1.3)
    a2.invert_yaxis()
    a2.set_ylabel("iteration")
    a2.set_xlabel("V (V)")
    fig.tight_layout()
    save(fig, f"{OUT}/bisection.svg")


if __name__ == "__main__":
    fig_sinc()
    fig_discontinuities()
    fig_switch()
    fig_asymptotes()
    fig_bisection()
    print("01-02 figures written")
