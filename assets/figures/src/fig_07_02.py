#!/usr/bin/env python3
"""Figures for chapter 07-02 (first-order RC and RL transients).

Run from anywhere:  python assets/figures/src/fig_07_02.py
Outputs SVGs to assets/figures/07-02/. Schematics use schemdraw; plots use matplotlib.
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

OUT = "assets/figures/07-02"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(ROOT / OUT / name))


# ------------------------------------------------------------------ schematics
def sch_rc_charging(d):
    d += (vs := elm.SourceV().up().label("$V_S$"))
    d += elm.Switch(action="close").right().label("t = 0", loc="top")
    d += elm.Resistor().right().label("R")
    d += elm.Dot().label("$v_C$", loc="right")
    d += elm.Capacitor().down().label("C", loc="bottom")
    d += elm.Line().left().tox(vs.start)
    d += elm.Ground()


def sch_example2(d):
    d += (vs := elm.SourceV().up().label("24 V"))
    d += elm.Switch(action="close").right().label("t = 0\n(opens at 10 ms\nin Ex. 3)", loc="top", fontsize=10)
    d += elm.Resistor().right().label("$R_1$ = 6 kΩ")
    d += (a := elm.Dot().label("A", loc="top"))
    d += elm.Resistor().down().label("$R_2$ = 3 kΩ", loc="top")
    d += (b := elm.Dot())
    d += elm.Line().left().tox(vs.start)
    d += elm.Ground()
    d += elm.Line().right().at(a.center).length(3.5)
    d += elm.Capacitor().down().label("C = 2 µF\n$v_C$", loc="bottom")
    d += elm.Line().left().tox(b.center)


def sch_rl_kick(d):
    d += (vs := elm.SourceV().up().label("12 V"))
    d += elm.Switch(action="open").right().label("t = 0", loc="top")
    d += elm.Resistor().right().label("$R_1$ = 4 Ω")
    d += (a := elm.Dot().label("A", loc="top"))
    d += elm.Inductor().down().label("L = 200 mH\n$i_L$ ↓", loc="top")
    d += (b := elm.Dot())
    d += elm.Line().left().tox(vs.start)
    d += elm.Ground()
    d += elm.Line().right().at(a.center).length(3.5)
    d += elm.Resistor().down().label("$R_2$ = 20 Ω", loc="bottom")
    d += elm.Line().left().tox(b.center)


# ------------------------------------------------------------------ plots
def fig_step_response():
    tt = np.linspace(0, 6, 600)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.9))
    ax1.plot(tt, 1 - np.exp(-tt), color=B)
    for n in range(1, 6):
        y = 1 - math.exp(-n)
        ax1.plot([n], [y], "o", color=O, ms=5)
        ax1.annotate(f"{100 * y:.1f}%", (n, y), textcoords="offset points", xytext=(4, -14), fontsize=9)
    ax1.plot([0, 1], [0, 1], "--", color="0.5", lw=1)
    ax1.text(0.55, 0.92, "initial slope reaches\nthe final value at t = τ", fontsize=8, color="0.35")
    ax1.set_xlabel("t / τ")
    ax1.set_ylabel("$v_C / V_S$")
    ax1.set_title("Charging from 0: $v_C = V_S(1 - e^{-t/τ})$")
    ax2.plot(tt, np.exp(-tt), color=B)
    for n in range(1, 6):
        y = math.exp(-n)
        ax2.plot([n], [y], "o", color=O, ms=5)
        ax2.annotate(f"{100 * y:.1f}%", (n, y), textcoords="offset points", xytext=(4, 6), fontsize=9)
    ax2.plot([0, 1], [1, 0], "--", color="0.5", lw=1)
    ax2.set_xlabel("t / τ")
    ax2.set_ylabel("$v_C / V_0$")
    ax2.set_title("Discharging: $v_C = V_0 e^{-t/τ}$")
    fig.tight_layout()
    save(fig, f"{OUT}/rc-step-response.svg")


def fig_example2_response():
    tau1, tau2, VTh = 4e-3, 6e-3, 8.0
    t = np.linspace(-2e-3, 25e-3, 2700)
    v = np.where(t < 0, 0.0, np.where(t < 10e-3, VTh * (1 - np.exp(-t / tau1)), 0.0))
    v10 = VTh * (1 - math.exp(-10e-3 / tau1))
    v = np.where(t >= 10e-3, v10 * np.exp(-(t - 10e-3) / tau2), v)
    iR1 = np.where((t >= 0) & (t < 10e-3), (24 - v) / 6e3, 0.0)
    iR2 = v / 3e3
    iC = iR1 - iR2
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.6), sharex=True)
    ax1.plot(t * 1e3, v, color=B, lw=2.2, label="$v_C$")
    ax1.axhline(8, ls=":", color="0.5")
    ax1.text(0.3, 8.15, "final value 8 V (if the switch stayed closed)", fontsize=8, color="0.35")
    ax1.axvline(10, ls="--", color="0.6", lw=1)
    ax1.text(10.3, 1.0, "switch opens:\nτ changes 4 ms → 6 ms", fontsize=8, color="0.35")
    ax1.set_ylabel("$v_C$ (V)")
    ax1.set_title("Examples 07-02.2 and 07-02.3: charge with τ = 4 ms, then discharge with τ = 6 ms")
    ax2.plot(t * 1e3, iR1 * 1e3, color=O, label="$i_{R1}$ (jumps)")
    ax2.plot(t * 1e3, iR2 * 1e3, color=G, label=r"$i_{R2}$ (continuous, $\propto v_C$)")
    ax2.plot(t * 1e3, iC * 1e3, color=P, label="$i_C$ (jumps)")
    ax2.axhline(0, color="0.3", lw=0.8)
    ax2.axvline(10, ls="--", color="0.6", lw=1)
    ax2.set_xlabel("t (ms)")
    ax2.set_ylabel("current (mA)")
    ax2.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/example2-response.svg")


def fig_rl_kick():
    t = np.linspace(-5e-3, 40e-3, 2000)
    iL = np.where(t < 0, 3.0, 3.0 * np.exp(-np.clip(t, 0, None) / 10e-3))
    vL = np.where(t < 0, 0.0, -20 * iL)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.0), sharex=True)
    ax1.plot(t * 1e3, iL, color=B, lw=2)
    ax1.set_ylabel("$i_L$ (A)")
    ax1.set_title("Example 07-02.4: inductor current is continuous; inductor voltage jumps to −60 V")
    ax2.plot(t * 1e3, vL, color=O, lw=2)
    ax2.axhline(-12, ls=":", color="0.5")
    ax2.text(20, -16, "supply is only 12 V", fontsize=8, color="0.35")
    ax2.set_ylabel("$v_L$ (V)")
    ax2.set_xlabel("t (ms)")
    fig.tight_layout()
    save(fig, f"{OUT}/rl-kick.svg")


def square_ss(t, T, tau):
    """Periodic steady-state RC response to a 0/1 square wave of period T (high first half)."""
    k = math.exp(-T / (2 * tau))
    vmax, vmin = 1 / (1 + k), k / (1 + k)
    ph = np.mod(t, T)
    return np.where(ph < T / 2, 1 + (vmin - 1) * np.exp(-ph / tau), vmax * np.exp(-(ph - T / 2) / tau))


def fig_square_wave():
    T = 1.0
    t = np.linspace(0, 3 * T, 3000)
    sq = (np.mod(t, T) < T / 2).astype(float)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.3), sharey=True)
    for ax, tau, title in zip(axes, [0.05, 0.5, 5.0], ["τ = T/20: output follows input",
                                                         "τ = T/2: rounded edges",
                                                         "τ = 5T: small ripple about the average"]):
        ax.plot(t, sq, color="0.6", lw=1, label="input")
        ax.plot(t, square_ss(t, T, tau), color=B, lw=2, label="output (steady state)")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("t / T")
    axes[0].set_ylabel("V (for a 0–1 V input)")
    axes[0].legend(loc="upper center", bbox_to_anchor=(1.7, -0.22), ncol=2, fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/square-wave.svg")


def fig_ramp():
    tau, k = 1.0, 1.0
    t = np.linspace(0, 6, 600)
    out = k * (t - tau) + k * tau * np.exp(-t / tau)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(t, k * t, color="0.5", lw=1.2, label="input ramp $mt$")
    ax.plot(t, out, color=B, lw=2, label="output $m(t - τ) + mτe^{-t/τ}$")
    ax.annotate("", xy=(5, 4), xytext=(4, 4), arrowprops=dict(arrowstyle="<->", color=O))
    ax.text(4.1, 4.25, "lag τ", color=O)
    ax.annotate("", xy=(5, 4), xytext=(5, 5), arrowprops=dict(arrowstyle="<->", color=G))
    ax.text(5.1, 4.4, "error mτ", color=G)
    ax.set_xlabel("t / τ")
    ax.set_ylabel("output / (mτ)")
    ax.set_title("Ramp response of a first-order low-pass: it tracks with a delay of τ")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, f"{OUT}/ramp-response.svg")


if __name__ == "__main__":
    schematic("rc-charging-schematic.svg", sch_rc_charging)
    schematic("example2-schematic.svg", sch_example2)
    schematic("rl-kick-schematic.svg", sch_rl_kick)
    fig_step_response()
    fig_example2_response()
    fig_rl_kick()
    fig_square_wave()
    fig_ramp()
    print("07-02 figures written to", OUT)
