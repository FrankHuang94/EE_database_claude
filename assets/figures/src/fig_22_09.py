#!/usr/bin/env python3
"""Figures for chapter 22-09 (batteries, charging and fuel gauging).

Run from anywhere:  python assets/figures/src/fig_22_09.py
Outputs
  assets/figures/22-09/cell-model.svg    the equivalent-circuit cell model: OCV source V_OC(z), series R0 and an
                                         R1 || C1 branch, with the SOC state integrating the current (schemdraw)
  assets/figures/22-09/pulse.svg         the teaching cell's terminal voltage for a 0.5 A, 40 s load pulse and the
                                         40 s rest after it, with the OCV (which falls with the charge drawn)
  assets/figures/22-09/cccv.svg          CC/CV charging of the teaching cell at 1C and 2C: current, terminal voltage
                                         and SOC against time (resistive quasi-static model, R = 0.30 ohm)
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "22-power-electronics-and-energy-conversion" / "labs" / "22-09-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import battery as bt  # noqa: E402

OUT = "assets/figures/22-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_model():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += elm.SourceV().at((0, 0)).to((0, 2.4)).label("$V_{OC}(z)$", loc="left")
    d += elm.Resistor().at((0, 2.4)).to((2.4, 2.4)).label("$R_0$", loc="top")
    d += elm.Line().at((2.4, 2.4)).to((2.4, 3.2))
    d += elm.Line().at((2.4, 2.4)).to((2.4, 1.6))
    d += elm.Resistor().at((2.4, 3.2)).to((4.8, 3.2)).label("$R_1$", loc="top")
    d += elm.Capacitor().at((2.4, 1.6)).to((4.8, 1.6)).label("$C_1$", loc="bottom")
    d += elm.Line().at((4.8, 3.2)).to((4.8, 1.6))
    d += elm.Line().at((4.8, 2.4)).to((6.4, 2.4))
    d += elm.Dot(open=True).at((6.4, 2.4)).label("$v$ (+)", loc="right")
    d += elm.Line().at((0, 0)).to((6.4, 0))
    d += elm.Dot(open=True).at((6.4, 0)).label("(−)", loc="right")
    d += elm.Label().at((3.6, 4.1)).label("$v_1$ across $R_1 \\parallel C_1$, $\\tau_1 = R_1C_1$")
    d += elm.Label().at((3.2, -0.8)).label("$dz/dt = -i/Q$ (discharge current $i$ out of +)")
    d += elm.Label().at((3.2, -1.4)).label("$v = V_{OC}(z) - iR_0 - v_1$")
    d.save(str(ROOT / OUT / "cell-model.svg"))


def fig_pulse():
    q, z0 = 1080.0, 0.5 / 0.9
    i_of_t = lambda t: 0.5 if 1.0 <= t < 41.0 else 0.0
    t, z, v1, v = bt.simulate_cell(i_of_t, 81.0, q, z0, n=1621)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.plot(t, bt.ocv_linear(z), color=PALETTE[1], ls="--", label="OCV")
    ax.plot(t, v, color=PALETTE[0], label="terminal voltage")
    ax.annotate("$IR_0$ drop", (1.5, 3.70), (6, 3.72), fontsize=8, arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.annotate("$R_1C_1$ sag", (15, 3.665), (14, 3.70), fontsize=8, arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.annotate("relaxation", (55, 3.772), (55, 3.74), fontsize=8, arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.set_xlabel("time (s)")
    ax.set_ylabel("voltage (V)")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("0.5 A for 40 s, then rest: instant drop, slow sag, slow recovery", fontsize=10)
    save(fig, f"{OUT}/pulse.svg")


def _cccv_trace(i_cc, q=1080.0, r=0.30, i_term=0.03, dt=1.0):
    ts, iz, vz, zz = [], [], [], []
    z, t = 0.0, 0.0
    while True:
        i = min(i_cc, (4.20 - float(bt.ocv_linear(z))) / r)
        ts.append(t), iz.append(i), vz.append(float(bt.ocv_linear(z)) + i * r), zz.append(z)
        if i <= i_term:
            break
        z += dt * i / q
        t += dt
    return np.array(ts), np.array(iz), np.array(vz), np.array(zz)


def fig_cccv():
    fig, ax = plt.subplots(3, 1, figsize=(6.0, 5.6), sharex=True)
    for i_cc, lab, col in ((0.3, "1C (0.3 A)", PALETTE[0]), (0.6, "2C (0.6 A)", PALETTE[1])):
        t, i, v, z = _cccv_trace(i_cc)
        ax[0].plot(t / 60, i * 1e3, color=col, label=lab)
        ax[1].plot(t / 60, v, color=col)
        ax[2].plot(t / 60, z * 100, color=col)
    ax[0].axhline(30, color="0.5", ls=":")
    ax[0].text(1, 45, "termination 30 mA", fontsize=8)
    ax[0].set_ylabel("current (mA)")
    ax[0].legend(fontsize=8)
    ax[1].set_ylabel("terminal (V)")
    ax[2].set_ylabel("SOC (%)")
    ax[2].set_xlabel("time (min)")
    ax[0].set_title("CC/CV: doubling the current saves 26 of 68 minutes, not half", fontsize=10)
    save(fig, f"{OUT}/cccv.svg")


if __name__ == "__main__":
    fig_model()
    fig_pulse()
    fig_cccv()
