#!/usr/bin/env python3
"""Figures for chapter 08-06 (latches, flip-flops and sequential timing).

Run from anywhere:  python assets/figures/src/fig_08_06.py
Outputs SVGs to assets/figures/08-06/: the butterfly curve of two cross-coupled square-law inverters
(computed), and a register-to-register timing diagram showing the setup and hold windows.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

VDD, VT = 1.8, 0.45
BN, BP = 250e-6 * 0.65 / 0.15, 100e-6 * 1.0 / 0.15


def i_n(vin, vout):
    vov = vin - VT
    if vov <= 0:
        return 0.0
    return BN * (vov * vout - vout ** 2 / 2) if vout < vov else 0.5 * BN * vov ** 2


def i_p(vin, vout):
    vov, vsd = VDD - vin - VT, VDD - vout
    if vov <= 0:
        return 0.0
    return BP * (vov * vsd - vsd ** 2 / 2) if vsd < vov else 0.5 * BP * vov ** 2


def vtc(vin):
    f = lambda vo: i_p(vin, vo) - i_n(vin, vo)
    if f(0.0) <= 0:
        return 0.0
    if f(VDD) >= 0:
        return VDD
    return brentq(f, 0.0, VDD)


def fig_butterfly():
    vm = brentq(lambda x: 0.5 * BN * (x - VT) ** 2 - 0.5 * BP * (VDD - x - VT) ** 2, VT, VDD - VT)
    vin = np.linspace(0, VDD, 901)
    vout = np.array([vtc(x) for x in vin])
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    ax.plot(vin, vout, color=PALETTE[0], lw=2, label="inverter 1: $V_2 = f(V_1)$")
    ax.plot(vout, vin, color=PALETTE[1], lw=2, label="inverter 2: $V_1 = f(V_2)$")
    ax.plot([0, VDD], [0, VDD], color="0.7", lw=0.8, ls=":")
    for (x, y), lab in (((0, VDD), "stable: Q = 0"), ((VDD, 0), "stable: Q = 1"), ((vm, vm), f"unstable: $V_M$ = {vm:.3f} V")):
        ax.plot(x, y, "ko", ms=6)
        ax.annotate(lab, (x, y), xytext=(x + (0.12 if x < 1 else -0.9), y + (-0.18 if y > 1 else 0.12)), fontsize=9)
    ax.set_xlabel("$V_1$ (V)")
    ax.set_ylabel("$V_2$ (V)")
    ax.set_xlim(-0.05, VDD + 0.05)
    ax.set_ylim(-0.05, VDD + 0.05)
    ax.set_aspect("equal")
    ax.legend(fontsize=8, loc="lower left")
    ax.set_title("Two cross-coupled inverters")
    save(fig, f"{OUT}/butterfly.svg")


def fig_timing():
    T = 10.0
    tpcq, tpd, tsu, th, tccq, tcd = 1.0, 6.0, 1.5, 0.8, 0.6, 1.2
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    t = np.linspace(-2, 12.5, 2000)
    clk = ((t % T) < T / 2).astype(float)
    ax.step(t, 3.0 + 0.8 * clk, where="post", color="k", lw=1.5)
    ax.text(-2.4, 3.4, "CLK", ha="right", va="center")
    # data at R2's input: old value until tccq + tcd, unstable until tpcq + tpd, then new value
    y = 1.6
    ax.fill_between([tccq + tcd, tpcq + tpd], y - 0.35, y + 0.35, color="0.85")
    ax.plot([-2, tccq + tcd], [y + 0.35, y + 0.35], "k", lw=1.2)
    ax.plot([-2, tccq + tcd], [y - 0.35, y - 0.35], "k", lw=1.2)
    ax.plot([tpcq + tpd, 12.5], [y + 0.35, y + 0.35], "k", lw=1.2)
    ax.plot([tpcq + tpd, 12.5], [y - 0.35, y - 0.35], "k", lw=1.2)
    ax.text(-2.4, y, "D of R2", ha="right", va="center")
    ax.text((tccq + tcd + tpcq + tpd) / 2, y, "changing", ha="center", va="center", fontsize=9)
    ax.text(-1.0, y, "old", ha="center", va="center", fontsize=9)
    ax.text(9.0, y, "new", ha="center", va="center", fontsize=9)
    # setup window before the next edge, hold window after the launch edge
    ax.axvspan(T - tsu, T, ymin=0.05, ymax=0.62, color=PALETTE[1], alpha=0.25)
    ax.text(T - tsu / 2, 0.55, "$t_{setup}$", ha="center", fontsize=9, color=PALETTE[1])
    ax.axvspan(0, th, ymin=0.05, ymax=0.62, color=PALETTE[2], alpha=0.25)
    ax.text(th / 2, 0.55, "$t_{hold}$", ha="center", fontsize=9, color=PALETTE[2])
    ax.annotate("", xy=(tpcq + tpd, 0.15), xytext=(0, 0.15), arrowprops=dict(arrowstyle="<->", color=PALETTE[0]))
    ax.text((tpcq + tpd) / 2, -0.15, "$t_{pcq} + t_{pd}$: must end before $T_c - t_{setup}$", ha="center", fontsize=9,
            color=PALETTE[0])
    ax.annotate("", xy=(tccq + tcd, 1.05), xytext=(0, 1.05), arrowprops=dict(arrowstyle="<->", color=PALETTE[2]))
    ax.text(tccq + tcd + 0.1, 0.92, "$t_{ccq} + t_{cd}$: must exceed $t_{hold}$", fontsize=9, color=PALETTE[2])
    ax.set_xlim(-3.5, 12.5)
    ax.set_ylim(-0.5, 4.1)
    ax.set_yticks([])
    ax.set_xticks([0, T])
    ax.set_xticklabels(["edge 0\n(R1 launches)", "edge 1\n(R2 captures)"])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ax.set_title("Register-to-register timing: setup and hold")
    save(fig, f"{OUT}/setup-hold.svg")


if __name__ == "__main__":
    fig_butterfly()
    fig_timing()
    print("figures written to", OUT)
