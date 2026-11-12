#!/usr/bin/env python3
"""Figures for chapter 01-05 (integrals).

Run:  python assets/figures/src/fig_01_05.py  -> assets/figures/01-05/*.svg
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
OUT = "assets/figures/01-05"
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]


def fig_riemann():
    f = lambda x: x**2  # noqa: E731
    x = np.linspace(0, 2, 300)
    h = 0.5
    xs = np.arange(4) * h
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.3), sharey=True)
    titles = ["Left: 1.75", "Right: 3.75", "Midpoint: 2.625", "Trapezoid: 2.75"]
    for ax, title, kind in zip(axes, titles, ["L", "R", "M", "T"]):
        ax.plot(x, f(x), color="k", lw=1.5)
        for x0 in xs:
            if kind == "T":
                ax.fill([x0, x0, x0 + h, x0 + h], [0, f(x0), f(x0 + h), 0], color=B, alpha=0.3, ec=B)
            else:
                xe = {"L": x0, "R": x0 + h, "M": x0 + h / 2}[kind]
                ax.bar(x0, f(xe), width=h, align="edge", color=B, alpha=0.3, ec=B)
        ax.set_title(title + "  (exact 2.667)", fontsize=10)
        ax.set_xlabel("x")
    axes[0].set_ylabel("f(x) = x²")
    fig.tight_layout()
    save(fig, f"{OUT}/riemann-sums.svg")


def fig_accumulation():
    t = np.linspace(0, 4, 400)
    f = t**2 - 4
    A = t**3 / 3 - 4 * t
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.5, 5), sharex=True)
    a1.plot(t, f, color=B)
    a1.fill_between(t, f, 0, where=f < 0, color=O, alpha=0.3, label="negative area")
    a1.fill_between(t, f, 0, where=f >= 0, color=G, alpha=0.3, label="positive area")
    a1.axhline(0, color="0.5", lw=0.8)
    a1.set_ylabel("f(t) = t² − 4")
    a1.legend(fontsize=8)
    a2.plot(t, A, color="k")
    a2.axhline(0, color="0.5", lw=0.8)
    a2.plot([2], [-16 / 3], "o", color=O)
    a2.plot([np.sqrt(12)], [0], "o", color=G)
    a2.set_ylabel("A(x) = ∫₀ˣ f(t) dt")
    a2.set_xlabel("x")
    a2.text(2.1, -4.2, "A' = f = 0: minimum", fontsize=8)
    a2.text(3.0, 0.6, "net area back to 0", fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/accumulation-function.svg")


def fig_cap_integral():
    t = np.linspace(0, 4, 4001)  # ms
    i = np.where(t < 1, 10, np.where(t < 3, -5, 0))  # mA
    v = 1 + np.cumsum(i * 1e-3) * (t[1] - t[0]) * 1e-3 / 2e-6
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.5, 4.6), sharex=True)
    a1.step(t, i, where="post", color=O)
    a1.axhline(0, color="0.6", lw=0.8)
    a1.set_ylabel("i (mA)")
    a1.set_title("v_C(t) = v_C(0) + (1/C)∫ i dt,  C = 2 µF")
    a2.plot(t, v, color=B)
    a2.set_ylabel("v_C (V)")
    a2.set_xlabel("t (ms)")
    fig.tight_layout()
    save(fig, f"{OUT}/capacitor-integral.svg")


def fig_rectified():
    th = np.linspace(0, 4 * np.pi, 800)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
    a1.plot(th / np.pi, np.abs(np.sin(th)), color=B)
    a1.axhline(2 / np.pi, color=O, ls="--", label="average 2/π = 0.637")
    a1.set_title("Full-wave rectified |sin θ|")
    a1.legend(fontsize=8)
    hw = np.maximum(np.sin(th), 0)
    a2.plot(th / np.pi, hw, color=B)
    a2.axhline(1 / np.pi, color=O, ls="--", label="average 1/π = 0.318")
    a2.set_title("Half-wave rectified")
    a2.legend(fontsize=8)
    for a in (a1, a2):
        a.set_xlabel("θ / π")
    fig.tight_layout()
    save(fig, f"{OUT}/rectified-averages.svg")


def fig_coulomb():
    t = np.linspace(0, 180, 18001)  # minutes, three hours
    i = np.where((t % 60) < 2, 5.0, 0.5)  # mA
    q = np.cumsum(i) * (t[1] - t[0]) / 60  # mAh
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.5, 4.6), sharex=True)
    a1.plot(t, i, color=O)
    a1.set_ylabel("current (mA)")
    a1.set_title("Coulomb counting: charge = ∫ i dt")
    a2.plot(t, q, color=B, label="∫ i dt")
    a2.plot(t, 0.65 * t / 60, color="k", ls="--", lw=1, label="average 0.65 mA × t")
    a2.set_ylabel("charge used (mAh)")
    a2.set_xlabel("time (min)")
    a2.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/coulomb-counting.svg")


if __name__ == "__main__":
    fig_riemann()
    fig_accumulation()
    fig_cap_integral()
    fig_rectified()
    fig_coulomb()
    print("01-05 figures written")
