#!/usr/bin/env python3
"""Figures for chapter 22-11 (electric machines and drives).

Run from anywhere:  python assets/figures/src/fig_22_11.py
Outputs
  assets/figures/22-11/induction-circuit.svg  the induction machine's per-phase equivalent circuit (schemdraw):
                                              R1, jX1, magnetizing jXm, jX2 and R2/s split as R2 + R2(1 − s)/s
  assets/figures/22-11/torque-speed.svg       Example 22-11.4's torque against speed for R2 = 0.4, 1.0 and
                                              2.03 Ω (left) and with constant V/f at 50, 40, 30 and 20 Hz (right)
  assets/figures/22-11/ev-envelope.svg        Example 22-11.8's traction-motor torque and power against speed:
                                              constant torque to 5000 rpm, constant power to 15 000 rpm
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
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-11-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import machines as mc  # noqa: E402

OUT = "assets/figures/22-11"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
VPH = 400 / math.sqrt(3)


def fig_circuit():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += elm.Dot(open=True).at((0, 2.5)).label("$\\mathbf{V}_1$ (+)", loc="left")
    d += elm.Resistor().at((0, 2.5)).to((2, 2.5)).label("$R_1$", loc="top")
    d += elm.Inductor().at((2, 2.5)).to((4, 2.5)).label("$jX_1$", loc="top")
    d += elm.Dot().at((4, 2.5))
    d += elm.Inductor().at((4, 2.5)).to((4, 0)).label("$jX_m$", loc="bottom")
    d += elm.Inductor().at((4, 2.5)).to((6, 2.5)).label("$jX_2$", loc="top")
    d += elm.Resistor().at((6, 2.5)).to((8, 2.5)).label("$R_2$", loc="top")
    d += elm.Line().at((8, 2.5)).to((9, 2.5))
    d += elm.ResistorVar().at((9, 2.5)).to((9, 0)).label("$R_2\\,\\frac{1-s}{s}$", loc="bottom")
    d += elm.Line().at((0, 0)).to((9, 0))
    d += elm.Dot(open=True).at((0, 0)).label("(−)", loc="left")
    d += elm.Dot().at((4, 0))
    d += elm.Label().at((4.5, 3.6)).label("$I_1$ →          $I_2$ → (rotor, referred to stator)")
    d += elm.Label().at((4.5, -0.9)).label("rotor copper loss $3I_2^2R_2 = sP_{ag}$;  mechanical power $3I_2^2R_2(1-s)/s = (1-s)P_{ag}$")
    d.save(str(ROOT / OUT / "induction-circuit.svg"))


def fig_torque_speed():
    s = np.linspace(1e-4, 1, 2000)
    fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.6), sharey=True)
    for r2, col in ((0.4, PALETTE[0]), (1.0, PALETTE[1]), (2.03, PALETTE[2])):
        m = mc.Induction(VPH, 50, 4, 0.5, 1.0, 30.0, r2, 1.0)
        ax[0].plot((1 - s) * 1500, [m.torque(x) for x in s], color=col, label=f"R2 = {r2} Ω")
    ax[0].set_xlabel("speed (rpm), 50 Hz")
    ax[0].set_ylabel("torque (N·m)")
    ax[0].legend(fontsize=8)
    ax[0].set_title("Rotor resistance moves the peak", fontsize=10)
    for f, col in ((50, PALETTE[0]), (40, PALETTE[1]), (30, PALETTE[2]), (20, PALETTE[3])):
        k = f / 50
        m = mc.Induction(VPH * k, f, 4, 0.5, 1.0 * k, 30.0 * k, 0.4, 1.0 * k)
        ns = mc.sync_speed_rpm(f, 4)
        ax[1].plot((1 - s) * ns, [m.torque(x) for x in s], color=col, label=f"{f} Hz")
    ax[1].set_xlabel("speed (rpm), constant V/f")
    ax[1].legend(fontsize=8)
    ax[1].set_title("V/f shifts the curve; R1 erodes the peak", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/torque-speed.svg")


def fig_ev():
    n = np.linspace(1, 15000, 1500)
    t = np.array([mc.ev_envelope(400, 5000, x) for x in n])
    p = t * n * mc.RPM / 1e3
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    ax.plot(n, t, color=PALETTE[0], label="torque (N·m)")
    ax.plot(n, p, color=PALETTE[1], label="power (kW)")
    ax.axvline(5000, color="0.5", ls=":")
    ax.text(5200, 30, "base speed", fontsize=8)
    ax.set_xlabel("motor speed (rpm)")
    ax.legend(fontsize=8)
    ax.set_title("Constant torque, then constant power (field weakening)", fontsize=10)
    save(fig, f"{OUT}/ev-envelope.svg")


if __name__ == "__main__":
    fig_circuit()
    fig_torque_speed()
    fig_ev()
