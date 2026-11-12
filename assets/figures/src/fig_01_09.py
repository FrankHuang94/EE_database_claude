#!/usr/bin/env python3
"""Figures for chapter 01-09 (multivariable calculus I).

Run:  python assets/figures/src/fig_01_09.py  -> assets/figures/01-09/*.svg
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

use_style()
OUT = "assets/figures/01-09"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_power_contours():
    V = np.linspace(0.5, 1.1, 200)
    f = np.linspace(0.5, 3.0, 200)
    VV, FF = np.meshgrid(V, f)
    Pw = 1.0 * VV**2 * FF  # aC = 1 nF, f in GHz -> W
    fig, ax = plt.subplots(figsize=(6.5, 4.4))
    cs = ax.contour(VV, FF, Pw, levels=[0.25, 0.5, 1.0, 1.5, 2.0, 3.0], colors=[B])
    ax.clabel(cs, fmt="%.2f W", fontsize=8)
    sV, sf = 0.6, 2.5  # plotted ranges: steepest ascent in the plot's scaled coordinates
    for v0, f0 in [(0.8, 2.0), (0.6, 1.0), (1.0, 2.5)]:
        gx, gy = 2 * v0 * f0, v0**2
        du, dw = gx * sV, gy * sf  # gradient with respect to scaled coordinates
        n = 0.12 / np.hypot(du, dw)
        ax.annotate("", xy=(v0 + du * n * sV, f0 + dw * n * sf), xytext=(v0, f0),
                    arrowprops=dict(arrowstyle="->", color=O, lw=1.5))
        ax.plot([v0], [f0], "o", color=O, ms=4)
    ax.set_xlabel("supply voltage V (V)")
    ax.set_ylabel("clock frequency f (GHz)")
    ax.set_title("Contours of P = αCV²f, with gradient directions (orange)")
    fig.tight_layout()
    save(fig, f"{OUT}/power-contours.svg")


def fig_mosfet():
    k, vth, va = 2e-3, 0.5, 10.0
    I = lambda vg, vd: 0.5 * k * (vg - vth) ** 2 * (1 + vd / va)  # noqa: E731
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.8))
    vg = np.linspace(0.5, 1.0, 200)
    a1.plot(vg, I(vg, 1.0) * 1e6, color=B, label="I_D at V_DS = 1 V")
    gm = k * 0.3 * 1.1
    a1.plot(vg, (I(0.8, 1.0) + gm * (vg - 0.8)) * 1e6, color=O, ls="--", label="slope g_m = ∂I_D/∂V_GS")
    a1.plot([0.8], [I(0.8, 1.0) * 1e6], "o", color="k")
    a1.set_ylim(0, 300)
    a1.set_xlabel("V_GS (V)")
    a1.set_ylabel("I_D (µA)")
    a1.legend(fontsize=8)
    vd = np.linspace(0.3, 2.0, 200)
    for vgs, col in [(0.7, P), (0.8, B), (0.9, G)]:
        a2.plot(vd, I(vgs, vd) * 1e6, color=col, label=f"V_GS = {vgs} V")
    go = 0.5 * k * 0.09 / va
    a2.plot(vd, (I(0.8, 1.0) + go * (vd - 1.0)) * 1e6, color=O, ls="--", label="slope g_o = ∂I_D/∂V_DS")
    a2.plot([1.0], [I(0.8, 1.0) * 1e6], "o", color="k")
    a2.set_xlabel("V_DS (V)")
    a2.legend(fontsize=8, loc="upper left")
    fig.suptitle("Partial derivatives of a MOSFET's drain current (saturation, square law)", fontsize=11)
    fig.tight_layout()
    save(fig, f"{OUT}/mosfet-partials.svg")


def fig_gradient_descent():
    x = np.linspace(-2.5, 2.5, 200)
    y = np.linspace(-1.5, 1.5, 200)
    XX, YY = np.meshgrid(x, y)
    Z = XX**2 + 4 * YY**2
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.contour(XX, YY, Z, levels=[0.25, 1, 2, 4, 8, 12], colors="0.7")
    for eta, col, lab in [(0.1, B, "η = 0.10: steady"), (0.23, O, "η = 0.23: zig-zag")]:
        p = np.array([2.0, 1.0])
        path = [p.copy()]
        for _ in range(12):
            p = p - eta * np.array([2 * p[0], 8 * p[1]])
            path.append(p.copy())
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], "o-", color=col, ms=3, lw=1, label=lab)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(fontsize=8)
    ax.set_title("Gradient descent on f = x² + 4y² from (2, 1)")
    fig.tight_layout()
    save(fig, f"{OUT}/gradient-descent.svg")


def fig_lagrange():
    f1 = np.linspace(0.01, 3.2, 200)
    f2 = np.linspace(0.01, 3.2, 200)
    F1, F2 = np.meshgrid(f1, f2)
    Pw = 0.1 * F1**3 + 0.4 * F2**3
    fig, ax = plt.subplots(figsize=(5.8, 5))
    cs = ax.contour(F1, F2, Pw, levels=[0.6, 1.2, 2.0, 3.0], colors=[B])
    ax.clabel(cs, fmt="%.1f W", fontsize=8)
    ax.plot(f1, 3 - f1, color=O, lw=2, label="constraint f₁ + f₂ = 3 GHz")
    ax.plot([2], [1], "o", color="k")
    ax.annotate("optimum (2, 1):\nP = 1.2 W, tangent to the line", xy=(2, 1), xytext=(2.05, 1.8), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 3.2)
    ax.set_xlabel("f₁, efficient core (GHz)")
    ax.set_ylabel("f₂, other core (GHz)")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title("Lagrange: the best point is where a contour touches the constraint")
    fig.tight_layout()
    save(fig, f"{OUT}/lagrange-cores.svg")


def fig_waterfill():
    N = [1, 3]
    mu = 5
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    ax.bar([1, 2], N, color="0.6", width=0.6, label="noise level N_i")
    ax.bar([1, 2], [mu - n for n in N], bottom=N, color=B, alpha=0.6, width=0.6, label="power P_i = μ − N_i")
    ax.axhline(mu, color=O, ls="--", label="water level μ = 5")
    ax.set_xticks([1, 2], ["channel 1", "channel 2"])
    ax.set_ylabel("mW")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Water-filling: total power 6 mW")
    fig.tight_layout()
    save(fig, f"{OUT}/water-filling.svg")


if __name__ == "__main__":
    fig_power_contours()
    fig_mosfet()
    fig_gradient_descent()
    fig_lagrange()
    fig_waterfill()
    print("01-09 figures written")
