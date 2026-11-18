#!/usr/bin/env python3
"""Figures for chapter 04-02 (charge, Coulomb's law and electric fields).

Run from anywhere:  python assets/figures/src/fig_04_02.py
Outputs SVGs to assets/figures/04-02/. The ESD schematic uses schemdraw; plots use matplotlib.
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

OUT = "assets/figures/04-02"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
EPS0 = 8.8541878188e-12
KE = 1 / (4 * math.pi * EPS0)


def field(charges, X, Y):
    Ex, Ey = np.zeros_like(X), np.zeros_like(Y)
    for q, (x0, y0) in charges:
        dx, dy = X - x0, Y - y0
        r3 = (dx**2 + dy**2) ** 1.5
        Ex += KE * q * dx / r3
        Ey += KE * q * dy / r3
    return Ex, Ey


def fig_field_lines():
    x = np.linspace(-3, 3, 400)
    X, Y = np.meshgrid(x, x)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))
    for ax, charges, title in (
        (axes[0], [(1.0, (-1, 0)), (-1.0, (1, 0))], "Dipole: lines leave + and end on −"),
        (axes[1], [(1.0, (-1, 0)), (1.0, (1, 0))], "Two like charges: a null midway"),
    ):
        Ex, Ey = field(charges, X, Y)
        mag = np.hypot(Ex, Ey)
        ax.streamplot(X, Y, Ex, Ey, color=np.log10(mag), cmap="viridis", density=1.4, linewidth=0.9, arrowsize=0.9)
        for q, (x0, y0) in charges:
            ax.plot(x0, y0, "o", ms=13, color=O if q > 0 else B)
            ax.text(x0, y0, "+" if q > 0 else "−", ha="center", va="center", color="white", fontsize=12, weight="bold")
        ax.set_aspect("equal")
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("x (arbitrary units)")
        ax.set_ylabel("y")
    fig.tight_layout()
    save(fig, f"{OUT}/field-lines.svg")


def fig_distributions():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    # disk on axis versus infinite sheet and point charge
    z = np.logspace(-2, 2, 400)                      # z/R
    disk = 1 - z / np.sqrt(z**2 + 1)                  # in units of sigma/(2 eps0)
    point = (np.pi * 1**2) / (2 * np.pi * z**2)       # Q = sigma pi R^2 -> kQ/z^2 in units of sigma/(2 eps0)
    ax = axes[0]
    ax.loglog(z, disk, color=B, lw=2, label="uniform disk, exact")
    ax.loglog(z, np.ones_like(z), color=O, ls="--", label="infinite sheet σ/(2ε₀)")
    ax.loglog(z, point, color=G, ls=":", lw=2, label="point charge πR²σ")
    ax.set_ylim(1e-4, 3)
    ax.set_xlabel("distance on axis z / R")
    ax.set_ylabel("E / (σ/2ε₀)")
    ax.set_title("A disk looks like a sheet up close, a point far away", fontsize=10)
    ax.legend(fontsize=8, loc="lower left")
    # finite line on its bisector versus infinite line and point
    y = np.logspace(-2, 2, 400)                       # y/(L/2)
    finite = (1 / y) * 1 / np.sqrt(y**2 + 1)          # in units of lambda/(2 pi eps0 (L/2))
    infinite = 1 / y
    pointl = 1 / y**2                                 # kQ/y^2 with Q = lambda L, in the same units
    ax = axes[1]
    ax.loglog(y, finite, color=B, lw=2, label="finite line, exact")
    ax.loglog(y, infinite, color=O, ls="--", label="infinite line λ/(2πε₀y)")
    ax.loglog(y, pointl, color=G, ls=":", lw=2, label="point charge λL")
    ax.set_xlabel("distance from the bisected line, y / (L/2)")
    ax.set_ylabel("E / (λ/(2πε₀ · L/2))")
    ax.set_title("A line looks infinite up close, a point far away", fontsize=10)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/continuous-distributions.svg")


def fig_hbm():
    fig = plt.figure(figsize=(10.4, 3.6))
    ax = fig.add_axes([0.0, 0.05, 0.42, 0.9])
    ax.axis("off")
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(canvas=ax, show=False)
    d += (c := elm.Capacitor().down().label("C = 100 pF\ncharged to 2 kV", loc="top"))
    d += elm.Line().right().length(1.5)
    d += elm.Line().up().length(0.0)
    d.push()
    d += elm.Line().right().at(c.start).length(1.5)
    d += elm.Switch(action="close").right().label("discharge", loc="top")
    d += elm.Resistor().right().label("R = 1.5 kΩ")
    d += (dut := elm.Line().down().toy(c.end))
    d += elm.Line().left().tox(c.end)
    d.pop()
    d.draw()
    ax.text(0.92, 0.5, "device\npin", transform=ax.transAxes, ha="center", va="center", fontsize=10, color="0.3")
    ax2 = fig.add_axes([0.5, 0.17, 0.47, 0.75])
    t = np.linspace(0, 1e-6, 2000)
    i = 2000 / 1500 * np.exp(-t / 150e-9)
    ax2.plot(t * 1e9, i, color=B, lw=2)
    ax2.axvline(150, color="0.5", ls=":", lw=1)
    ax2.text(160, 1.0, "RC = 150 ns", fontsize=9, color="0.3")
    ax2.set_xlabel("time (ns)")
    ax2.set_ylabel("discharge current (A)")
    ax2.set_title("Idealized human-body-model discharge: 1.333 A peak", fontsize=10)
    save(fig, f"{OUT}/hbm-discharge.svg")


if __name__ == "__main__":
    fig_field_lines()
    fig_distributions()
    fig_hbm()
