#!/usr/bin/env python3
"""Figures for chapter 02-03 (second-order linear ODEs).

Run:  python assets/figures/src/fig_02_03.py  -> assets/figures/02-03/*.svg
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
OUT = "assets/figures/02-03"
B, O, G, P, Y, S = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3], PALETTE[4], PALETTE[5]


def natural(z, t):
    """Response of y'' + 2 z y' + y = 0 with y(0) = 1, y'(0) = 0 (time in units of 1/w0)."""
    if z < 1:
        wd = math.sqrt(1 - z * z)
        return np.exp(-z * t) * (np.cos(wd * t) + z / wd * np.sin(wd * t))
    if z == 1:
        return (1 + t) * np.exp(-t)
    r1, r2 = -z + math.sqrt(z * z - 1), -z - math.sqrt(z * z - 1)
    return (r2 * np.exp(r1 * t) - r1 * np.exp(r2 * t)) / (r2 - r1)


def fig_three_cases():
    t = np.linspace(0, 20, 2000)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for z, c, lab in [(0.2, B, "underdamped, ζ = 0.2"), (1.0, O, "critically damped, ζ = 1"), (3.0, G, "overdamped, ζ = 3")]:
        ax.plot(t, natural(z, t), color=c, lw=2, label=lab)
    ax.plot(t, np.exp(-0.2 * t), color=B, ls=":", lw=1)
    ax.plot(t, -np.exp(-0.2 * t), color=B, ls=":", lw=1, label="envelope ±e^(−ζω₀t)")
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_xlabel("ω₀t")
    ax.set_ylabel("y")
    ax.set_title("Natural response from y(0) = 1, y′(0) = 0")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/three-cases.svg")


def fig_root_locus():
    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    th = np.linspace(math.pi / 2, 3 * math.pi / 2, 200)
    ax.plot(np.cos(th), np.sin(th), color="0.7", ls="--", lw=1, label="|s| = ω₀ (ζ < 1)")
    for z, c in [(0.2, B), (0.5, O), (0.78, P), (1.0, "k"), (2.0, G)]:
        if z < 1:
            s = [complex(-z, math.sqrt(1 - z * z)), complex(-z, -math.sqrt(1 - z * z))]
        elif z == 1:
            s = [complex(-1, 0)]
        else:
            s = [complex(-z + math.sqrt(z * z - 1), 0), complex(-z - math.sqrt(z * z - 1), 0)]
        ax.plot([q.real for q in s], [q.imag for q in s], "x", color=c, ms=10, mew=2, label=f"ζ = {z}")
    z = 0.5
    ax.plot([0, -z], [0, math.sqrt(1 - z * z)], color=O, lw=1)
    ax.annotate("θ, cos θ = ζ", (-0.12, 0.25), color=O, fontsize=9)
    ax.annotate("ω_d", (0.03, math.sqrt(0.75) - 0.05), color=O, fontsize=9)
    ax.annotate("−α = −ζω₀", (-0.62, -0.12), color=O, fontsize=9)
    ax.axhline(0, color="0.5", lw=0.8)
    ax.axvline(0, color="0.5", lw=0.8)
    ax.set_xlim(-4, 0.6)
    ax.set_ylim(-1.3, 1.3)
    ax.set_xlabel("Re s / ω₀")
    ax.set_ylabel("Im s / ω₀")
    ax.set_title("Characteristic roots as ζ grows (ω₀ fixed)")
    ax.legend(fontsize=7, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/root-locus.svg")


def step(z, t):
    return 1 - natural(z, t) - (0 if z >= 1 else 0)


def fig_step_family():
    t = np.linspace(0, 16, 3000)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for z, c in [(0.2, B), (0.5, O), (0.78, P), (1.0, "k"), (2.0, G)]:
        if z < 1:
            wd = math.sqrt(1 - z * z)
            y = 1 - np.exp(-z * t) * (np.cos(wd * t) + z / wd * np.sin(wd * t))
        else:
            y = 1 - natural(z, t)
        ax.plot(t, y, color=c, lw=1.8, label=f"ζ = {z}")
    ax.axhspan(0.98, 1.02, color="0.85", label="±2% band")
    ax.set_xlabel("ω₀t")
    ax.set_ylabel("y / final value")
    ax.set_title("Step responses: ζ ≈ 0.78 settles into ±2% fastest")
    ax.legend(fontsize=8, ncol=2, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/step-family.svg")


def settle(z, tol=0.02):
    t = np.linspace(0, 40, 200001)
    if z < 1:
        wd = math.sqrt(1 - z * z)
        y = 1 - np.exp(-z * t) * (np.cos(wd * t) + z / wd * np.sin(wd * t))
    else:
        y = 1 - natural(z, t)
    idx = np.where(abs(y - 1) > tol)[0]
    return t[idx[-1]]


def fig_overshoot_settling():
    zs = np.linspace(0.05, 0.99, 200)
    os_ = 100 * np.exp(-math.pi * zs / np.sqrt(1 - zs**2))
    zz = np.linspace(0.2, 2.0, 181)
    ts = [settle(z) for z in zz]
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))
    axes[0].plot(zs, os_, color=B, lw=2)
    axes[0].set_xlabel("ζ")
    axes[0].set_ylabel("overshoot (%)")
    axes[0].set_title("Overshoot = exp(−πζ/√(1−ζ²))")
    for z in (0.5, 0.707):
        o = 100 * math.exp(-math.pi * z / math.sqrt(1 - z * z))
        axes[0].plot([z], [o], "o", color=O)
        axes[0].annotate(f"ζ = {z}: {o:.1f}%", (z + 0.03, o + 3), fontsize=8)
    axes[1].plot(zz, ts, color=G, lw=2)
    axes[1].set_xlabel("ζ")
    axes[1].set_ylabel("2% settling time × ω₀")
    axes[1].set_title("Settling time: minimum near ζ = 0.78")
    fig.tight_layout()
    save(fig, f"{OUT}/overshoot-settling.svg")


def fig_pdn():
    L, V0, dI = 25e-12, 0.75, 10.0
    t = np.linspace(0, 40e-9, 4000)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for C, R, c, lab in [(100e-9, 1e-3, B, "C = 100 nF: Z₀ = 15.8 mΩ"), (4.94e-6, 1e-3, G, "C = 4.94 µF: Z₀ = 2.25 mΩ")]:
        w0 = 1 / math.sqrt(L * C)
        a = R / (2 * L)
        wd = math.sqrt(w0**2 - a**2)
        A = R * dI
        Bc = (-dI / C + a * R * dI) / wd
        v = V0 - R * dI + np.exp(-a * t) * (A * np.cos(wd * t) + Bc * np.sin(wd * t))
        ax.plot(t * 1e9, v, color=c, lw=2, label=lab)
    ax.axhline(V0 * 0.97, color=O, ls="--", lw=1, label="−3% limit (0.7275 V)")
    ax.set_xlabel("t (ns)")
    ax.set_ylabel("supply at the die (V)")
    ax.set_title("A 10 A load step on a 0.75 V rail (L = 25 pH, R = 1 mΩ)")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/pdn-droop.svg")


def fig_energy():
    L, C, R = 10e-6, 1e-6, 1.0
    a = R / (2 * L)
    w0 = 1 / math.sqrt(L * C)
    wd = math.sqrt(w0**2 - a**2)
    t = np.linspace(0, 60e-6, 3000)
    v = np.exp(-a * t) * (5 * np.cos(wd * t) + 5 * a / wd * np.sin(wd * t))
    i = C * np.gradient(v, t)
    wc = 0.5 * C * v**2 * 1e6
    wl = 0.5 * L * i**2 * 1e6
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(t * 1e6, wc, color=B, lw=1.6, label="capacitor ½Cv²")
    ax.plot(t * 1e6, wl, color=O, lw=1.6, label="inductor ½Li²")
    ax.plot(t * 1e6, wc + wl, color="k", lw=2, label="total (falls by R i² dt)")
    ax.set_xlabel("t (µs)")
    ax.set_ylabel("energy (µJ)")
    ax.set_title("Energy sloshes between C and L and drains through R")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/energy-exchange.svg")


if __name__ == "__main__":
    fig_three_cases()
    fig_root_locus()
    fig_step_family()
    fig_overshoot_settling()
    fig_pdn()
    fig_energy()
