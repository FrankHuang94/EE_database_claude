#!/usr/bin/env python3
"""Figures for chapter 10-09 (real op-amps).

Run from anywhere:  python assets/figures/src/fig_10_09.py
Outputs SVGs to assets/figures/10-09/:
- gbw.svg: a single-pole open-loop gain (A_0 = 130 dB, GBW = 10 MHz, the TLV9062's typical figures) with the
  closed-loop responses for noise gains of 1, 10 and 100, showing bandwidth = GBW / noise gain;
- slew.svg: step response of a unity-gain follower with a 10 MHz single pole and a 6.5 V/us slew-rate limit,
  for a 50 mV step (linear, exponential) and a 2 V step (slew-limited ramp, then exponential);
- models.svg: schematics (schemdraw) of (a) the single-pole macromodel used in the lab's netlist and
  (b) the DC error model (offset voltage in series with the + input, bias currents at both inputs).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
A0 = 10 ** (130 / 20)
GBW = 10e6
FP = GBW / A0


def fig_gbw():
    f = np.logspace(-1, 8, 600)
    a = A0 / (1 + 1j * f / FP)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.semilogx(f, 20 * np.log10(np.abs(a)), color="k", lw=1.2, label="open loop $A(f)$")
    for g, col in ((1, PALETTE[0]), (10, PALETTE[1]), (100, PALETTE[2])):
        beta = 1 / g
        acl = a / (1 + a * beta)
        ax.semilogx(f, 20 * np.log10(np.abs(acl)), color=col, label=f"noise gain {g}: $f_{{-3dB}}$ = {GBW / g / 1e6:g} MHz")
        ax.plot(GBW / g, 20 * np.log10(g) - 3.01, "o", color=col, ms=4)
    ax.set_ylim(-20, 140)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("gain (dB)")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/gbw.svg")


def step(vstep, sr=6.5e6, fc=10e6, t_end=1.2e-6):
    tau = 1 / (2 * np.pi * fc)

    def rhs(t, y):
        return [np.clip((vstep - y[0]) / tau, -sr, sr)]
    t = np.linspace(0, t_end, 1200)
    sol = solve_ivp(rhs, (0, t_end), [0.0], t_eval=t, max_step=1e-9)
    return sol.t, sol.y[0]


def fig_slew():
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.4))
    t, y = step(0.05)
    a.plot(t * 1e6, y * 1e3, color=PALETTE[0])
    a.set_title("(a) 50 mV step: linear settling, $\\tau$ = 16 ns", fontsize=10)
    a.set_xlabel("time (µs)")
    a.set_ylabel("output (mV)")
    t, y = step(2.0)
    b.plot(t * 1e6, y, color=PALETTE[1], label="slew-limited response")
    b.plot(t * 1e6, 2.0 * (1 - np.exp(-t * 2 * np.pi * 10e6)), color="0.6", ls="--", label="linear (no slew limit)")
    b.set_title("(b) 2 V step: 6.5 V/µs ramp, then settling", fontsize=10)
    b.set_xlabel("time (µs)")
    b.set_ylabel("output (V)")
    b.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/slew.svg")


def fig_models():
    """(a) Single-pole macromodel: G_m v_d into R_p || C_p, unity buffer. (b) DC error model."""
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)

    def title(x, y, text):
        d.add(elm.Label().at((x, y)).label(text, fontsize=12))

    # (a) macromodel
    title(4.0, 4.2, "(a) single-pole macromodel")
    d.add(elm.Dot(open=True).at((0, 2.5)).label("$v_+$", loc="left"))
    d.add(elm.Dot(open=True).at((0, 0)).label("$v_-$", loc="left"))
    d.add(elm.Label().at((0.25, 1.25)).label("$v_d$", fontsize=12))
    d.add(elm.Label().at((0.25, 2.1)).label("+", fontsize=12))
    d.add(elm.Label().at((0.25, 0.4)).label("−", fontsize=12))
    d.add(elm.SourceControlledI().at((2.5, 0)).up().length(2.5).label("$G_mv_d$"))
    d.add(elm.Line().right().length(1.5))
    nx = d.add(elm.Dot().label("$x$", loc="top"))
    d.add(elm.Resistor().down().length(2.5).label("$R_p$", loc="bottom"))
    d.add(elm.Line().at(nx.center).right().length(1.5))
    d.add(elm.Capacitor().down().length(2.5).label("$C_p$", loc="bottom"))
    d.add(elm.Line().at((2.5, 0)).right().length(5.5))
    d.add(elm.Ground().at((4.0, 0)))
    d.add(elm.SourceControlledV().at((8.0, 0)).up().length(2.5).label("$1\\cdot v_x$", loc="bottom"))
    d.add(elm.Line().right().length(1.0))
    d.add(elm.Dot(open=True).label("$v_o$", loc="right"))
    d.add(elm.Label().at((4.75, -1.6)).label(
        "$A_0 = G_mR_p,\\ f_p = 1/(2\\pi R_pC_p),\\ \\mathrm{GBW} = G_m/(2\\pi C_p)$", fontsize=11))
    d.add(elm.Label().at((4.75, -2.3)).label(
        "a current limit $I$ on the source gives SR $= I/C_p$", fontsize=11))

    # (b) DC error model
    x, y = 16.5, 1.3
    title(x - 1.5, 4.2, "(b) DC error model")
    op = d.add(elm.Opamp(leads=True).right().at((x, y)).label("ideal", loc="center", ofst=(0.3, 0)))
    d.add(elm.SourceV().at(op.in2).left().length(1.6).label("$V_{OS}$", loc="top"))
    npl = d.add(elm.Dot())
    d.add(elm.Line().left().length(0.9))
    d.add(elm.Dot(open=True).label("+", loc="left"))
    d.add(elm.SourceI().at(npl.center).down().length(1.8).label("$I_{B+}$", loc="bottom"))
    d.add(elm.Ground())
    d.add(elm.Line().at(op.in1).left().length(5.0))
    nmi = d.add(elm.Dot())
    d.add(elm.Line().left().length(0.8))
    d.add(elm.Dot(open=True).label("−", loc="left"))
    d.add(elm.SourceI().at(nmi.center).down().length(op.in1[1] - op.in2[1] + 1.8).label("$I_{B-}$"))
    d.add(elm.Ground())
    d.add(elm.Line().at(op.out).right().length(0.8))
    d.add(elm.Dot(open=True).label("$v_o$", loc="right"))
    d.add(elm.Label().at((x - 1.5, -2.3)).label(
        "$I_B = (I_{B+} + I_{B-})/2,\\ I_{OS} = I_{B+} - I_{B-}$", fontsize=11))
    d.save(str(ROOT / OUT / "models.svg"))


if __name__ == "__main__":
    fig_gbw()
    fig_slew()
    fig_models()
