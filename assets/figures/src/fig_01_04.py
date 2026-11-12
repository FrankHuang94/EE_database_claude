#!/usr/bin/env python3
"""Figures for chapter 01-04 (applications of derivatives).

Run:  python assets/figures/src/fig_01_04.py  -> assets/figures/01-04/*.svg
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
OUT = "assets/figures/01-04"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_mpt():
    r = np.linspace(0.01, 5, 500)  # R_L / R_s
    p = r / (1 + r) ** 2 / 0.25  # normalized to P_max
    eta = r / (1 + r)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(r, p, color=B, label="load power / P_max")
    ax.plot(r, eta, color=O, ls="--", label="efficiency R_L/(R_s + R_L)")
    ax.axvline(1, color="0.6", lw=0.8)
    ax.plot([1], [1], "o", color=B)
    ax.text(1.08, 0.3, "R_L = R_s:\nmax power,\n50 % efficiency", fontsize=9)
    ax.set_xlabel("R_L / R_s")
    ax.set_ylim(0, 1.08)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Maximum power transfer: a flat optimum")
    fig.tight_layout()
    save(fig, f"{OUT}/max-power-transfer.svg")


def fig_energy():
    A, Bc = 1.0, 0.05
    V = np.linspace(0.12, 1.1, 400)
    vs = (Bc / (2 * A)) ** (1 / 3)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(V, A * V**2, color=B, ls="--", label="switching energy  A·V²")
    ax.plot(V, Bc / V, color=O, ls="--", label="leakage energy  B/V")
    ax.plot(V, A * V**2 + Bc / V, color="k", label="total")
    ax.plot([vs], [A * vs**2 + Bc / vs], "o", color=G)
    ax.annotate(f"minimum at V* = {vs:.3f} V", xy=(vs, A * vs**2 + Bc / vs), xytext=(0.45, 0.8),
                arrowprops=dict(arrowstyle="->", color="0.3"), fontsize=9)
    ax.set_ylim(0, 1.3)
    ax.set_xlabel("supply voltage V (V)")
    ax.set_ylabel("energy per operation (pJ)")
    ax.legend(fontsize=8, loc="upper center")
    ax.set_title("A stylized minimum-energy point")
    fig.tight_layout()
    save(fig, f"{OUT}/minimum-energy-point.svg")


def fig_newton():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 4))
    x = np.linspace(0.8, 3.2, 300)
    a1.plot(x, x**2 - 2, color="k", lw=1.5, label="f(x) = x² − 2")
    a1.axhline(0, color="0.6", lw=0.8)
    xk = 3.0
    a1.text(xk, -0.6, "x0 = 3", color=B, ha="center", fontsize=9)
    for k, (col, dy) in enumerate(zip([B, O], [-0.6, 0.5])):
        fk, dk = xk**2 - 2, 2 * xk
        xn = xk - fk / dk
        a1.plot([xk, xn], [fk, 0], color=col, lw=1.2)
        a1.plot([xk, xk], [0, fk], color=col, lw=0.8, ls=":")
        a1.plot([xk], [fk], "o", color=col, ms=5)
        a1.text(xn - 0.08 * k, dy, f"x{k + 1} = {xn:.4f}", color=col, ha="center", fontsize=9)
        xk = xn
    a1.plot([math.sqrt(2)], [0], "*", color=G, ms=10, label="root √2 = 1.4142")
    a1.set_ylim(-1.2, 7.5)
    a1.set_xlabel("x")
    a1.set_title("Newton: follow the tangent to zero")
    a1.legend(fontsize=8, loc="upper left")
    # convergence comparison
    xs = math.sqrt(2)
    xk, errs_n = 3.0, []
    for _ in range(7):
        xk = (xk + 2 / xk) / 2
        errs_n.append(max(abs(xk - xs), 1e-17))
    a, b, errs_b = 1.0, 3.0, []
    for _ in range(40):
        m = (a + b) / 2
        a, b = (m, b) if m * m < 2 else (a, m)
        errs_b.append(max(abs((a + b) / 2 - xs), 1e-17))
    a2.semilogy(range(1, 8), errs_n, "o-", color=B, label="Newton")
    a2.semilogy(range(1, 41), errs_b, ".-", color=O, label="bisection")
    a2.axhline(2.2e-16, color="0.6", ls="--", lw=0.8)
    a2.text(25, 5e-16, "double precision", fontsize=8, color="0.4")
    a2.set_xlabel("iteration")
    a2.set_ylabel("|error| in √2")
    a2.legend(fontsize=8)
    a2.set_title("Quadratic versus linear convergence")
    fig.tight_layout()
    save(fig, f"{OUT}/newton-method.svg")


def fig_linearization():
    x = np.linspace(2.5, 6.5, 300)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(x, np.sqrt(x), color="k", label="f(x) = √x")
    ax.plot(x, 2 + (x - 4) / 4, color=B, ls="--", label="L(x) = 2 + (x − 4)/4")
    ax.plot([4], [2], "o", color=B)
    ax.set_xlabel("x")
    ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Linearization: accurate near the point, drifting away from it")
    fig.tight_layout()
    save(fig, f"{OUT}/linearization.svg")


def fig_repeated():
    tau1 = 1.0
    t = np.linspace(0, 6, 400)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for tau2, col in [(3.0, P), (2.0, O), (1.3, G)]:
        h = (np.exp(-t / tau1) - np.exp(-t / tau2)) / (tau1 - tau2)
        ax.plot(t, h, color=col, label=f"τ₂ = {tau2:g} τ₁")
    ax.plot(t, t * np.exp(-t), color="k", lw=2, label="limit τ₂ → τ₁:  (t/τ²) e^(−t/τ)")
    ax.set_xlabel("t / τ₁")
    ax.set_ylabel("h(t)·τ₁")
    ax.legend(fontsize=8)
    ax.set_title("Two RC stages: equal time constants by L'Hôpital")
    fig.tight_layout()
    save(fig, f"{OUT}/repeated-time-constant.svg")


if __name__ == "__main__":
    fig_mpt()
    fig_energy()
    fig_newton()
    fig_linearization()
    fig_repeated()
    print("01-04 figures written")
