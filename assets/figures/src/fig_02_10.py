#!/usr/bin/env python3
"""Figures for chapter 02-10 (numerical methods for engineers).

Run:  python assets/figures/src/fig_02_10.py  -> assets/figures/02-10/*.svg
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
OUT = "assets/figures/02-10"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_stability_regions():
    x = np.linspace(-4.5, 2.5, 700)
    y = np.linspace(-3.5, 3.5, 700)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    regions = [
        ("forward Euler: |1 + z| ≤ 1", np.abs(1 + Z), B),
        ("RK4", np.abs(1 + Z + Z**2 / 2 + Z**3 / 6 + Z**4 / 24), G),
        ("backward Euler: |1/(1 − z)| ≤ 1", np.abs(1 / (1 - Z)), O),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.0), sharey=True)
    for ax, (name, R, col) in zip(axes, regions):
        ax.contourf(X, Y, (R <= 1).astype(float), levels=[0.5, 1.5], colors=[col], alpha=0.25)
        ax.contour(X, Y, R, levels=[1.0], colors=[col], linewidths=1.5)
        ax.axhline(0, color="0.4", lw=0.8)
        ax.axvline(0, color="0.4", lw=0.8)
        ax.set_aspect("equal")
        ax.set_xlabel("Re(hλ)")
        ax.set_title(name, fontsize=10)
    axes[0].set_ylabel("Im(hλ)")
    axes[0].plot([-2], [0], "x", color="k")
    axes[0].annotate("hλ = −2: edge", (-2, 0), xytext=(-4.3, 1.4), fontsize=8,
                     arrowprops=dict(arrowstyle="-", color="0.5"))
    axes[1].plot([-2.785], [0], "x", color="k")
    axes[1].annotate("−2.785", (-2.785, 0), xytext=(-4.3, -1.6), fontsize=8,
                     arrowprops=dict(arrowstyle="-", color="0.5"))
    axes[2].text(-4.2, 2.6, "stable on the whole left\nhalf-plane (A-stable);\ntrapezoidal: exactly Re z ≤ 0",
                 fontsize=8, color="0.3")
    fig.suptitle("Shaded: |R(hλ)| ≤ 1, where a decaying mode is integrated stably", fontsize=11)
    fig.tight_layout()
    save(fig, f"{OUT}/stability-regions.svg")


def diode_problem():
    IS, R, Vs = 1e-14, 1e3, 5.0
    VT = 1.380649e-23 * 300.15 / 1.602176634e-19
    f = lambda v: (Vs - v) / R - IS * (math.exp(v / VT) - 1)  # noqa: E731
    fp = lambda v: -1 / R - IS / VT * math.exp(v / VT)  # noqa: E731
    vcrit = VT * math.log(VT / (math.sqrt(2) * IS))

    def pnjlim(vnew, vold):
        if vnew > vcrit and abs(vnew - vold) > 2 * VT:
            if vold > 0:
                arg = (vnew - vold) / VT
                return vold + VT * (2 + math.log(arg - 2)) if arg > 0 else vold - VT * (2 + math.log(2 - arg))
            return VT * math.log(vnew / VT)
        return vnew
    return f, fp, pnjlim


def fig_newton():
    f, fp, pnjlim = diode_problem()
    from scipy.optimize import brentq
    vstar = brentq(f, 0, 1, xtol=1e-15)
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    for v0, lim, col, lab in ((0.7, False, B, "plain Newton from 0.7 V"), (0.6, False, O, "plain Newton from 0.6 V"),
                              (0.6, True, G, "with junction limiting, from 0.6 V")):
        v, errs = v0, [abs(v0 - vstar)]
        for _ in range(40):
            vn = v - f(v) / fp(v)
            if lim:
                vn = pnjlim(vn, v)
            v = vn
            errs.append(max(abs(v - vstar), 1e-17))
            if abs(v - vstar) < 1e-15:
                break
        ax.semilogy(range(len(errs)), errs, "o-", color=col, ms=3.5, lw=1.2, label=lab)
    ax.set_xlabel("iteration k")
    ax.set_ylabel("|v_k − v*| (V)")
    ax.set_ylim(1e-17, 2)
    ax.legend(fontsize=8)
    ax.set_title("Diode circuit (Example 02-10.2): quadratic convergence near the root, a slow crawl after overshoot",
                 fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/newton-convergence.svg")


def fig_order():
    def run(step, h):
        y = 1.0
        for _ in range(round(1 / h)):
            y = step(y, h)
        return y
    euler = lambda y, h: y + h * (-y)  # noqa: E731
    heun = lambda y, h: y + h / 2 * (-y + -(y - h * y))  # noqa: E731

    def rk4(y, h):
        k1 = -y; k2 = -(y + h / 2 * k1); k3 = -(y + h / 2 * k2); k4 = -(y + h * k3)
        return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    hs = np.array([0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625])
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for step, col, name, p in ((euler, B, "Euler", 1), (heun, O, "Heun (RK2)", 2), (rk4, G, "RK4", 4)):
        err = [abs(run(step, h) - math.exp(-1)) for h in hs]
        ax.loglog(hs, err, "o-", color=col, label=f"{name}: slope {p}")
    ax.set_xlabel("step h")
    ax.set_ylabel("|error| at t = 1")
    ax.invert_xaxis()
    ax.legend(fontsize=8)
    ax.set_title("y' = −y: error falls as h^p (Example 02-10.4)", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/order.svg")


if __name__ == "__main__":
    fig_stability_regions()
    fig_newton()
    fig_order()
