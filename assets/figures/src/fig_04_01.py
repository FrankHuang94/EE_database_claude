#!/usr/bin/env python3
"""Figures for chapter 04-01 (mechanics essentials for EE).

Run from anywhere:  python assets/figures/src/fig_04_01.py
Outputs SVGs to assets/figures/04-01/. The analogy figure draws the mechanical sketch with
matplotlib patches and the circuit with schemdraw; plots use matplotlib.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/04-01"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# Example 04-01.5: m = 10 g, k_s = 1000 N/m, b = 0.4 N*s/m
M5, K5, B5 = 0.01, 1000.0, 0.4


def fig_energy():
    w0 = math.sqrt(K5 / M5)
    t = np.linspace(0, 0.06, 3000)
    x = 0.01 * np.cos(w0 * t)                                   # 1 cm amplitude, undamped
    v = -0.01 * w0 * np.sin(w0 * t)
    K = 0.5 * M5 * v**2 * 1e3
    U = 0.5 * K5 * x**2 * 1e3
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    ax = axes[0]
    ax.plot(t * 1e3, K, color=O, label="kinetic $\\frac{1}{2}m\\dot{x}^2$")
    ax.plot(t * 1e3, U, color=B, label="potential $\\frac{1}{2}k_s x^2$")
    ax.plot(t * 1e3, K + U, color="k", lw=1.2, ls="--", label="total (constant)")
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("energy (mJ)")
    ax.set_title("Undamped: energy sloshes between the two stores", fontsize=10)
    ax.set_ylim(0, 64)
    ax.legend(fontsize=8, loc="upper center", ncol=3)
    # damped ring-down (Example 04-01.5)
    alpha = B5 / (2 * M5)
    wd = math.sqrt(w0**2 - alpha**2)
    t2 = np.linspace(0, 0.25, 4000)
    x2 = np.exp(-alpha * t2) * (np.cos(wd * t2) + alpha / wd * np.sin(wd * t2))
    ax = axes[1]
    ax.plot(t2 * 1e3, x2, color=B, lw=1.4, label="x(t)/x(0)")
    ax.plot(t2 * 1e3, np.exp(-alpha * t2), color=O, ls="--", lw=1.2, label="envelope e^(−αt), 1/α = 50 ms")
    ax.plot(t2 * 1e3, -np.exp(-alpha * t2), color=O, ls="--", lw=1.2)
    ax.set_xlabel("time (ms)")
    ax.set_ylabel("displacement (normalized)")
    ax.set_title("Damped (Q = 7.906): released from rest", fontsize=10)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/oscillator-energy.svg")


def fig_analogy():
    # left: mechanical sketch (matplotlib); right: series RLC (schemdraw)
    fig = plt.figure(figsize=(10.4, 3.6))
    ax = fig.add_axes([0.0, 0.0, 0.44, 1.0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0.4, 0.8), 0.35, 4.4, color="0.75"))            # wall
    for yy in np.linspace(1.0, 5.0, 9):
        ax.plot([0.4, 0.1], [yy, yy - 0.3], color="0.5", lw=1)
    # spring (top) from wall to mass
    xs = np.linspace(0.75, 5.0, 200)
    ys = 4.0 + 0.3 * (2 / np.pi) * np.arcsin(np.sin(np.linspace(0, 12 * np.pi, 200)))   # zigzag
    ys[:15] = 4.0
    ys[-15:] = 4.0
    ax.plot(xs, ys, color=B, lw=1.6)
    ax.text(2.9, 4.55, "spring $k_s$", ha="center", fontsize=11, color=B)
    # dashpot (bottom)
    ax.plot([0.75, 2.4], [2.0, 2.0], color=O, lw=1.6)
    ax.plot([2.4, 2.4], [1.6, 2.4], color=O, lw=1.6)
    ax.plot([2.2, 3.6, 3.6, 2.2], [2.5, 2.5, 1.5, 1.5], color=O, lw=1.6)
    ax.plot([3.6, 5.0], [2.0, 2.0], color=O, lw=1.6)
    ax.text(2.9, 2.75, "damper $b$", ha="center", fontsize=11, color=O)
    ax.add_patch(plt.Rectangle((5.0, 1.2), 2.0, 3.6, fill=False, lw=2, color="k"))
    ax.text(6.0, 3.0, "mass\n$m$", ha="center", va="center", fontsize=12)
    ax.annotate("", xy=(9.3, 3.0), xytext=(7.0, 3.0), arrowprops=dict(arrowstyle="->", lw=1.6))
    ax.text(8.15, 3.25, "force $F(t)$", ha="center", fontsize=11)
    ax.annotate("", xy=(7.3, 0.6), xytext=(5.0, 0.6), arrowprops=dict(arrowstyle="->", lw=1.2, color="0.3"))
    ax.text(6.15, 0.15, "displacement $x$", ha="center", fontsize=10, color="0.3")
    ax.text(5.0, 5.6, "$m\\ddot x + b\\dot x + k_s x = F(t)$", ha="center", fontsize=12)

    ax2 = fig.add_axes([0.48, 0.12, 0.52, 0.86])
    ax2.axis("off")
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(canvas=ax2, show=False)
    d += (src := elm.SourceV().up().label("$v(t)$ ↔ $F(t)$"))
    d += elm.Inductor().right().label("$L$ ↔ $m$")
    d += elm.Resistor().right().label("$R$ ↔ $b$")
    d += elm.Capacitor().down().label("$C$ ↔ $1/k_s$", loc="bottom")
    d += elm.Line().left().tox(src.start)
    d += elm.CurrentLabelInline(direction="in").at(src).label("$i$ ↔ $\\dot x$")
    d.draw()
    fig.text(0.74, 0.0, "$L\\,di/dt + Ri + q/C = v(t)$,  with $q$ ↔ $x$", ha="center", va="bottom", fontsize=12)
    save(fig, f"{OUT}/msd-rlc-analogy.svg")


def fig_accel():
    g = 9.80665
    f = np.logspace(1, 5, 1200)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    q = 1 / math.sqrt(2)
    for f0, c in ((1e3, B), (4e3, O), (16e3, G)):
        w0, w = 2 * math.pi * f0, 2 * math.pi * f
        H = 1 / np.sqrt((w0**2 - w**2) ** 2 + (w0 * w / q) ** 2)        # |x/a| in s^2
        ax.loglog(f, H * g * 1e9, color=c, lw=2, label=f"$f_0$ = {f0 / 1e3:g} kHz: {g / w0**2 * 1e9:.4g} nm per g")
    ax.set_xlabel("frequency of the acceleration (Hz)")
    ax.set_ylabel("proof-mass deflection per g (nm)")
    ax.set_title("Accelerometer, Q = 0.707: flat below $f_0$ at $a/\\omega_0^2$, falling as $1/f^2$ above", fontsize=10)
    ax.set_ylim(1e-3, 1e3)
    ax.legend(fontsize=8, loc="lower left")
    ax.text(3e3, 2e2, "4× the bandwidth costs\n16× the deflection", fontsize=8, color="0.3")
    fig.tight_layout()
    save(fig, f"{OUT}/accelerometer-response.svg")


if __name__ == "__main__":
    fig_energy()
    fig_analogy()
    fig_accel()
