#!/usr/bin/env python3
"""Figures for chapter 02-01 (complex numbers, Euler's formula, phasors).

Run from anywhere:  python assets/figures/src/fig_02_01.py
Outputs SVGs to assets/figures/02-01/.
"""
from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/02-01"
use_style()
B, O, G, P, Y = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3], PALETTE[4]


def arrow(ax, z, color, label=None, start=0j, lw=2.0, **kw):
    ax.annotate("", xy=(z.real, z.imag), xytext=(start.real, start.imag),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0, mutation_scale=14))
    if label:
        kw.setdefault("fontsize", 10)
        ax.text(z.real, z.imag, label, color=color, **kw)


def axes_plane(ax, lim):
    ax.axhline(0, color="0.3", lw=0.8)
    ax.axvline(0, color="0.3", lw=0.8)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("Real axis")
    ax.set_ylabel("Imaginary axis (j)")


# 1. Complex plane: z = 3 + j4 and its conjugate ------------------------------------------
def fig_complex_plane():
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    axes_plane(ax, 5.8)
    z = 3 + 4j
    arrow(ax, z, B, "  z = 3 + j4 = 5∠53.13°", va="bottom")
    arrow(ax, z.conjugate(), O, "  z* = 3 − j4 = 5∠−53.13°", va="top")
    ax.plot([3, 3], [0, 4], ls="--", color="0.5", lw=1)
    ax.plot([0, 3], [4, 4], ls="--", color="0.5", lw=1)
    ax.text(3.05, -0.45, "x = Re{z} = 3", fontsize=9, color="0.25")
    ax.text(-0.2, 4.15, "y = Im{z} = 4", fontsize=9, color="0.25", ha="right")
    th = np.linspace(0, math.atan2(4, 3), 60)
    ax.plot(1.3 * np.cos(th), 1.3 * np.sin(th), color=B, lw=1.2)
    ax.text(1.45, 0.55, "θ", color=B, fontsize=12)
    ax.text(1.2, 2.25, "r = |z| = 5", color=B, fontsize=10, rotation=53)
    ax.set_title("A complex number as a point (or arrow) in the plane")
    save(fig, f"{OUT}/complex-plane.svg")


# 2. Rotating phasor and its projection -----------------------------------------------------
def fig_rotating_phasor():
    A, phi = 1.0, math.radians(30)
    wt0 = math.radians(40)  # snapshot angle ωt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.0), gridspec_kw={"width_ratios": [1, 1.7]})
    t = np.linspace(0, 2 * np.pi, 300)
    ax1.plot(np.cos(t), np.sin(t), color="0.75", lw=1)
    axes_plane(ax1, 1.35)
    z0 = cmath.rect(A, phi)
    zt = cmath.rect(A, phi + wt0)
    arrow(ax1, z0, "0.55", "  V = A∠φ  (snapshot at t = 0)", va="bottom", fontsize=9)
    arrow(ax1, zt, B, r"  $\mathbf{V}e^{j\omega t}$", va="bottom")
    ax1.plot([zt.real, zt.real], [0, zt.imag], ls="--", color=O, lw=1.2)
    ax1.plot([zt.real], [0], "o", color=O)
    ax1.text(zt.real, -0.22, r"Re$\{\mathbf{V}e^{j\omega t}\}$", color=O, ha="center", fontsize=9)
    ax1.annotate("", xy=(-0.55, 0.95), xytext=(0.2, 1.12),
                 arrowprops=dict(arrowstyle="-|>", color="0.4", connectionstyle="arc3,rad=0.25"))
    ax1.text(-0.55, 1.15, "rotates at ω rad/s", fontsize=9, color="0.3")
    ax1.set_title("Phasor rotating in the complex plane")
    wt = np.linspace(0, 4 * np.pi, 600)
    ax2.plot(np.degrees(wt), A * np.cos(wt + phi), color=O, label="v(t) = A cos(ωt + φ)")
    ax2.plot([math.degrees(wt0)], [A * math.cos(wt0 + phi)], "o", color=O)
    ax2.axhline(0, color="0.3", lw=0.8)
    ax2.set_xlabel("ωt (degrees)")
    ax2.set_ylabel("v(t) / A")
    ax2.set_xticks(range(0, 721, 90))
    ax2.set_title("…and its shadow on the real axis is the sinusoid (φ = 30°)")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/rotating-phasor.svg")


# 3. Multiplication = scale and rotate ------------------------------------------------------
def fig_multiplication():
    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    z1, z2 = 3 + 4j, 1 - 2j
    p = z1 * z2
    ax.axhline(0, color="0.3", lw=0.8)
    ax.axvline(0, color="0.3", lw=0.8)
    arrow(ax, z1, B, "  z₁ = 5∠53.13°", va="bottom")
    arrow(ax, z2, O, "  z₂ = 2.236∠−63.43°", va="top", ha="right")
    arrow(ax, p, G)
    ax.text(p.real + 0.6, p.imag - 1.3, "z₁z₂ = 11.18∠−10.30°", color=G, fontsize=10, ha="right")
    arrow(ax, 1j * z1, P)
    ax.text(-4.0, 3.5, "j·z₁ = 5∠143.13°", color=P, fontsize=10, ha="center")
    ax.set_xlim(-7.5, 12)
    ax.set_ylim(-4, 6)
    ax.set_aspect("equal")
    ax.set_xlabel("Real axis")
    ax.set_ylabel("Imaginary axis (j)")
    ax.set_title("Multiplying: magnitudes multiply, angles add\n(multiplying by j is a 90° rotation)")
    save(fig, f"{OUT}/multiplication-rotation.svg")


# 4. Euler's formula from Taylor partial sums ------------------------------------------------
def fig_euler_taylor():
    theta = 2.0
    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(t), np.sin(t), color="0.8", lw=1, label="unit circle")
    s, term, pts = 0j, 1 + 0j, [0j]
    for n in range(0, 14):
        if n > 0:
            term *= 1j * theta / n
        s += term
        pts.append(s)
    pts = np.array(pts)
    ax.plot(pts.real, pts.imag, "-o", color=B, ms=3.5, lw=1.2, label=r"partial sums $S_0, S_1, S_2, \ldots$")
    for k in range(1, 6):
        ax.text(pts[k].real + 0.06, pts[k].imag + 0.06, f"$S_{k - 1}$", fontsize=9, color=B)
    e = cmath.exp(1j * theta)
    ax.plot([e.real], [e.imag], "*", color=O, ms=14, label=r"$e^{j2} = \cos 2 + j\sin 2$")
    ax.axhline(0, color="0.3", lw=0.8)
    ax.axvline(0, color="0.3", lw=0.8)
    ax.set_aspect("equal")
    ax.set_xlim(-2.4, 1.6)
    ax.set_ylim(-1.6, 2.6)
    ax.set_xlabel("Real axis")
    ax.set_ylabel("Imaginary axis (j)")
    ax.set_title(r"Taylor partial sums of $e^{j\theta}$ ($\theta$ = 2 rad)" + "\nspiral in onto the unit circle")
    ax.legend(loc="lower left", fontsize=8)
    save(fig, f"{OUT}/euler-taylor.svg")


# 5. Fourth roots of −16 --------------------------------------------------------------------
def fig_roots():
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(2 * np.cos(t), 2 * np.sin(t), color="0.8", lw=1)
    for k in range(4):
        w = cmath.rect(2, math.radians(45 + 90 * k))
        arrow(ax, w, B, f"  w{'₀₁₂₃'[k]} = 2∠{45 + 90 * k}°  ", fontsize=9,
              ha="left" if w.real > 0 else "right", va="bottom" if w.imag > 0 else "top")
    axes_plane(ax, 3.0)
    ax.set_title("The four fourth roots of −16\n(equally spaced by 360°/4 on a circle of radius 2)")
    save(fig, f"{OUT}/fourth-roots.svg")


# 6. Phasor sum (Example 02-01.3) -----------------------------------------------------------
def fig_phasor_sum():
    V1, V2 = cmath.rect(10, math.radians(30)), cmath.rect(5, math.radians(-110))
    S = V1 + V2
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"width_ratios": [1, 1.6]})
    ax1.axhline(0, color="0.3", lw=0.8)
    ax1.axvline(0, color="0.3", lw=0.8)
    arrow(ax1, V1, B, "  V₁ = 10∠30°", va="bottom")
    arrow(ax1, V1 + V2, O, start=V1)
    ax1.text((V1 + V2 / 2).real + 0.3, (V1 + V2 / 2).imag, "V₂ = 5∠−110°", color=O, fontsize=10)
    arrow(ax1, S, G)
    ax1.text(1.0, -1.2, "V₁ + V₂ = 6.957∠2.48°", color=G, fontsize=10)
    ax1.set_xlim(-1, 12)
    ax1.set_ylim(-3, 7)
    ax1.set_aspect("equal")
    ax1.set_xlabel("Real (V)")
    ax1.set_ylabel("Imaginary (V)")
    ax1.set_title("Head-to-tail phasor addition")
    wt = np.linspace(0, 4 * np.pi, 800)
    v1 = 10 * np.cos(wt + math.radians(30))
    v2 = 5 * np.sin(wt - math.radians(20))
    ax2.plot(np.degrees(wt), v1, color=B, lw=1.2, label="v₁ = 10 cos(ωt + 30°)")
    ax2.plot(np.degrees(wt), v2, color=O, lw=1.2, label="v₂ = 5 sin(ωt − 20°)")
    ax2.plot(np.degrees(wt), v1 + v2, color=G, lw=2.4, label="v₁ + v₂ (computed point by point)")
    ax2.plot(np.degrees(wt), abs(S) * np.cos(wt + cmath.phase(S)), "k--", lw=1.0,
             label="6.957 cos(ωt + 2.48°) (from phasors)")
    ax2.set_xticks(range(0, 721, 90))
    ax2.set_xlabel("ωt (degrees)")
    ax2.set_ylabel("Voltage (V)")
    ax2.set_title("The time-domain sum matches the phasor sum")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/phasor-sum.svg")


# 7. RC low-pass: transient then steady state (Example 02-01.4) ------------------------------
def fig_rc_steady_state():
    R, C, f, Vm = 1e3, 100e-9, 1e3, 5.0
    tau, w = R * C, 2 * math.pi * f
    sol = solve_ivp(lambda t, y: (Vm * np.cos(w * t) - y) / tau, (0, 3e-3), [0.0],
                    max_step=1e-6, rtol=1e-9, atol=1e-12, dense_output=True)
    t = np.linspace(0, 3e-3, 1500)
    H = 1 / (1 + 1j * w * tau)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(t * 1e3, Vm * np.cos(w * t), color=B, lw=1.2, label="input 5 cos(2π·1000 t) V")
    ax.plot(t * 1e3, sol.sol(t)[0], color=O, lw=2.2, label="output, ODE solved numerically from rest")
    ax.plot(t * 1e3, Vm * abs(H) * np.cos(w * t + cmath.phase(H)), "k--", lw=1.0,
            label="phasor prediction 4.234 cos(2π·1000 t − 32.14°) V")
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("RC low-pass (R = 1 kΩ, C = 100 nF): the start-up transient dies out (τ = 0.1 ms),\n"
                 "leaving exactly the sinusoidal steady state the phasor method predicts")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8)
    save(fig, f"{OUT}/rc-steady-state.svg")


if __name__ == "__main__":
    fig_complex_plane()
    fig_rotating_phasor()
    fig_multiplication()
    fig_euler_taylor()
    fig_roots()
    fig_phasor_sum()
    fig_rc_steady_state()
    print("02-01 figures written to", OUT)
