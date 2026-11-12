#!/usr/bin/env python3
"""Figures for chapter 01-03 (derivatives).

Run:  python assets/figures/src/fig_01_03.py  -> assets/figures/01-03/*.svg
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
OUT = "assets/figures/01-03"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_secants():
    x = np.linspace(0, 3.6, 300)
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(x, x**2, color="k", lw=2, label="y = x²")
    a = 2.0
    for h, col in [(1.5, P), (0.8, O), (0.3, G)]:
        m = ((a + h) ** 2 - a**2) / h
        ax.plot(x, a**2 + m * (x - a), color=col, lw=1, label=f"secant, h = {h}: slope {m:.1f}")
        ax.plot([a + h], [(a + h) ** 2], "o", color=col, ms=5)
    ax.plot(x, a**2 + 4 * (x - a), color=B, lw=2, ls="--", label="tangent: slope 4 (limit)")
    ax.plot([a], [a**2], "o", color="k")
    ax.set_xlim(0, 3.6)
    ax.set_ylim(-1, 13)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Secant slopes approach the tangent slope as h → 0")
    fig.tight_layout()
    save(fig, f"{OUT}/secant-to-tangent.svg")


def fig_cap_ind():
    t = np.linspace(0, 8, 2001)  # ms
    # capacitor: triangle-ish voltage of Problem 01-03.7
    v = np.interp(t, [0, 2, 5, 6, 8], [0, 10, 10, 0, 0])
    i = np.where(t < 2, 50, np.where(t < 5, 0, np.where(t < 6, -100, 0)))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7, 4.8), sharex=True)
    a1.plot(t, v, color=B)
    a1.set_ylabel("v_C (V)")
    a1.set_title("Capacitor, C = 10 µF: i = C dv/dt")
    a2.step(t, i, where="post", color=O)
    a2.set_ylabel("i_C (mA)")
    a2.set_xlabel("t (ms)")
    a2.axhline(0, color="0.6", lw=0.8)
    for x0, y0, txt in [(1, 55, "+50 mA"), (5.5, -92, "−100 mA")]:
        a2.text(x0, y0, txt, ha="center", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/capacitor-derivative.svg")


def fig_sine_derivative():
    t = np.linspace(0, 2, 400)  # ms
    w = 2 * math.pi  # rad/ms at 1 kHz
    v = 5 * np.sin(w * t)
    i = 1e-6 * 5 * (w * 1e3) * np.cos(w * t) * 1e3  # mA
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(t, v, color=B, label="v(t) = 5 sin(2π·1000 t)  (V)")
    ax2 = ax.twinx()
    ax2.plot(t, i, color=O, label="i(t) = C dv/dt  (mA), C = 1 µF")
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("v (V)", color=B)
    ax2.set_ylabel("i (mA)", color=O)
    ax.set_ylim(-6, 6)
    ax2.set_ylim(-36, 36)
    lines = ax.get_lines() + ax2.get_lines()
    ax.legend(lines, [ln.get_label() for ln in lines], fontsize=8, loc="lower left")
    ax.set_title("Differentiating a sinusoid: scale by ω, shift 90° earlier")
    fig.tight_layout()
    save(fig, f"{OUT}/sinusoid-derivative.svg")


def fig_diode_tangent():
    VT, Is = 0.02585, 1e-14
    V = np.linspace(0.62, 0.69, 300)
    I = Is * np.exp(V / VT) * 1e3
    V0 = VT * math.log(1e-3 / Is)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(V, I, color=B, label="diode I(V)")
    ax.plot(V, 1 + (V - V0) / VT, color=O, ls="--", label="tangent at 1 mA: slope g_d = I/V_T = 38.7 mS")
    ax.plot([V0], [1], "o", color="k")
    ax.set_ylim(0, 3)
    ax.set_xlabel("V (V)")
    ax.set_ylabel("I (mA)")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Linearizing the diode: the small-signal conductance")
    fig.tight_layout()
    save(fig, f"{OUT}/diode-tangent.svg")


def fig_numdiff():
    hs = np.logspace(-16, -1, 400)
    x = 1.0
    fwd = np.abs((np.sin(x + hs) - np.sin(x)) / hs - math.cos(x))
    cen = np.abs((np.sin(x + hs) - np.sin(x - hs)) / (2 * hs) - math.cos(x))
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.loglog(hs, np.maximum(fwd, 1e-17), ".", ms=3, color=B, label="forward difference")
    ax.loglog(hs, np.maximum(cen, 1e-17), ".", ms=3, color=O, label="central difference")
    ax.set_xlabel("step h")
    ax.set_ylabel("|error| in d/dx sin x at x = 1")
    ax.legend(fontsize=8)
    ax.set_title("Truncation falls with h; rounding grows as h shrinks")
    fig.tight_layout()
    save(fig, f"{OUT}/numerical-derivative-error.svg")


if __name__ == "__main__":
    fig_secants()
    fig_cap_ind()
    fig_sine_derivative()
    fig_diode_tangent()
    fig_numdiff()
    print("01-03 figures written")
