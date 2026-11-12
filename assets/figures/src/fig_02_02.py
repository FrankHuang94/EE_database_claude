#!/usr/bin/env python3
"""Figures for chapter 02-02 (first-order linear ODEs).

Run:  python assets/figures/src/fig_02_02.py  -> assets/figures/02-02/*.svg
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
OUT = "assets/figures/02-02"
B, O, G, P, Y = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3], PALETTE[4]


def _field(ax, f, t_range, y_range, n=19):
    t = np.linspace(*t_range, n)
    y = np.linspace(*y_range, n)
    T, Yg = np.meshgrid(t, y)
    S = f(T, Yg)
    # draw unit-length segments in screen-scaled coordinates
    sx = (t_range[1] - t_range[0]) / n * 0.4
    sy = (y_range[1] - y_range[0]) / n * 0.4
    ang = np.arctan2(S * sx / sy, 1.0)
    dt = sx * np.cos(ang)
    dy = sy * np.sin(ang)
    for i in range(n):
        for k in range(n):
            ax.plot([T[i, k] - dt[i, k], T[i, k] + dt[i, k]], [Yg[i, k] - dy[i, k], Yg[i, k] + dy[i, k]],
                    color="0.6", lw=0.8)


def fig_direction_fields():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0))
    # left: linear relaxation y' = (1 - y)/tau, tau = 1
    ax = axes[0]
    _field(ax, lambda t, y: (1 - y), (0, 5), (-0.5, 2.5))
    t = np.linspace(0, 5, 300)
    for y0, c in [(-0.5, B), (0.0, O), (2.5, G), (1.8, P)]:
        ax.plot(t, 1 + (y0 - 1) * np.exp(-t), color=c, lw=2)
    ax.axhline(1, color="k", ls="--", lw=1)
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_xlabel("t / τ")
    ax.set_ylabel("y")
    ax.set_title("y′ = (1 − y)/τ: every solution relaxes to 1")
    # right: logistic y' = y(1 - y)
    ax = axes[1]
    _field(ax, lambda t, y: y * (1 - y), (0, 10), (-0.2, 1.4))
    t = np.linspace(0, 10, 300)
    for y0, c in [(0.01, B), (0.1, O), (1.4, G)]:
        ax.plot(t, 1 / (1 + (1 / y0 - 1) * np.exp(-t)), color=c, lw=2)
    ax.axhline(1, color="k", ls="--", lw=1)
    ax.axhline(0, color="k", ls=":", lw=1)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.2, 1.4)
    ax.set_xlabel("r t")
    ax.set_ylabel("N / K")
    ax.set_title("Logistic y′ = r y(1 − y/K): S-curves")
    fig.tight_layout()
    save(fig, f"{OUT}/direction-fields.svg")


def fig_transient_steady():
    tau = 1 / (2 * math.pi * 1e3)
    w = 2 * math.pi * 2e3
    A = 1 / math.sqrt(1 + (w * tau) ** 2)
    phi = math.atan(w * tau)
    t = np.linspace(0, 2e-3, 2000)
    ss = A * np.cos(w * t - phi)
    tr = -A * math.cos(phi) * np.exp(-t / tau)
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(t * 1e3, np.cos(w * t), color="0.7", lw=1, label="input cos ωt (1 V, 2 kHz)")
    ax.plot(t * 1e3, ss, color=B, ls="--", lw=1.5, label="steady state (phasor answer)")
    ax.plot(t * 1e3, tr, color=O, ls=":", lw=2, label="transient −0.2 e^(−t/τ) V")
    ax.plot(t * 1e3, ss + tr, color="k", lw=2, label="total response, v(0) = 0")
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("v (V)")
    ax.set_title("RC low-pass (f_c = 1 kHz) switched onto a 2 kHz cosine")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/transient-plus-steady.svg")


def fig_ramp():
    tau, S = 200e-6, 0.5e3
    t = np.linspace(0, 1.2e-3, 600)
    vin = S * t
    vout = S * (t - tau) + S * tau * np.exp(-t / tau)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(t * 1e3, vin, color="0.5", lw=1.5, label="input ramp, 0.5 V/ms")
    ax.plot(t * 1e3, vout, color=B, lw=2, label="RC output, τ = 200 µs")
    ax.plot(t * 1e3, S * (t - tau), color=O, ls="--", lw=1, label="asymptote S(t − τ)")
    t1 = 1.0e-3
    ax.annotate("", xy=(t1 * 1e3, S * t1), xytext=(t1 * 1e3, S * (t1 - tau)),
                arrowprops=dict(arrowstyle="<->", color=G))
    ax.text(t1 * 1e3 + 0.02, S * (t1 - tau / 2), "error Sτ = 0.1 V", color=G, va="center")
    ax.annotate("", xy=((t1 - tau) * 1e3, S * (t1 - tau) + 0.005), xytext=(t1 * 1e3, S * (t1 - tau) + 0.005),
                arrowprops=dict(arrowstyle="<->", color=P))
    ax.text((t1 - tau / 2) * 1e3, S * (t1 - tau) + 0.03, "lag τ", color=P, ha="center")
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("v (V)")
    ax.set_title("A first-order system tracks a ramp with a constant lag τ")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/ramp-tracking.svg")


def fig_thermal_runaway():
    Ta, Pd, PL0, T0, Tc = 35.0, 80.0, 10.0, 25.0, 30.0
    T = np.linspace(30, 140, 500)
    gen = Pd + PL0 * np.exp((T - T0) / Tc)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(T, gen, color="k", lw=2, label="heat generated P_dyn + P_leak(T)")
    for R, c, lab in [(0.25, B, "removed, R_th = 0.25 K/W"), (0.329, O, "removed, R_th = 0.329 K/W (critical)"),
                      (0.40, P, "removed, R_th = 0.40 K/W")]:
        ax.plot(T, (T - Ta) / R, color=c, lw=1.6, label=lab)
    ax.plot([64.25], [(64.25 - Ta) / 0.25], "o", color=G, ms=7)
    ax.annotate("stable\n64.25 °C", (64.25, (64.25 - Ta) / 0.25), xytext=(45, 200), color=G,
                arrowprops=dict(arrowstyle="->", color=G))
    ax.plot([124.94], [(124.94 - Ta) / 0.25], "o", mfc="white", color=G, ms=7)
    ax.annotate("unstable\n124.9 °C", (124.94, (124.94 - Ta) / 0.25), xytext=(108, 430), color=G,
                arrowprops=dict(arrowstyle="->", color=G))
    ax.set_xlim(30, 140)
    ax.set_ylim(0, 500)
    ax.set_xlabel("junction temperature T (°C)")
    ax.set_ylabel("power (W)")
    ax.set_title("Thermal runaway: equilibria where generation meets removal")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/thermal-runaway.svg")


def fig_euler():
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    t = np.linspace(0, 6, 400)
    ax.plot(t, np.exp(-t), color="k", lw=2, label="exact e^(−t/τ)")
    for h, c in [(0.5, B), (1.5, O), (2.5, P)]:
        n = int(round(6 / h)) + 1
        tt = np.arange(n) * h
        yy = (1 - h) ** np.arange(n)
        ax.plot(tt, yy, "o-", color=c, lw=1.2, ms=4, label=f"Euler, h = {h}τ")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_xlim(0, 6)
    ax.set_ylim(-2.5, 2.5)
    ax.set_xlabel("t / τ")
    ax.set_ylabel("y")
    ax.set_title("Euler's method on y′ = −y/τ: stable only for h < 2τ")
    ax.legend(loc="lower left", fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/euler-stability.svg")


if __name__ == "__main__":
    fig_direction_fields()
    fig_transient_steady()
    fig_ramp()
    fig_thermal_runaway()
    fig_euler()
