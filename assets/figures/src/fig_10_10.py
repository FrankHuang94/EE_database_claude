#!/usr/bin/env python3
"""Figures for chapter 10-10 (op-amp application circuits).

Run from anywhere:  python assets/figures/src/fig_10_10.py
Outputs SVGs to assets/figures/10-10/:
- schmitt.svg: a slow, noisy ramp crossing 2.5 V into (a) a plain comparator, which chatters, and (b) the Schmitt
  trigger of Example 10-10.5 (thresholds 2.45 V and 2.55 V), which switches once; seeded noise, 10 mV rms;
- tia.svg: transimpedance magnitude of the photodiode amplifier of Example 10-10.7 (R_F = 100 kOhm, C_in = 14 pF,
  GBW = 10 MHz) without a feedback capacitor and with C_F = 2.105 pF (Butterworth), from the loop equation with a
  single-pole op-amp.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_schmitt():
    rng = np.random.default_rng(1010)
    t = np.linspace(0, 1, 4000)
    vin = 2.3 + 0.4 * t + rng.normal(0, 0.01, t.size)
    plain = np.where(vin > 2.5, 5.0, 0.0)
    out = np.zeros_like(vin)
    state = 0.0
    for i, x in enumerate(vin):
        if state == 0.0 and x > 2.55:
            state = 5.0
        elif state == 5.0 and x < 2.45:
            state = 0.0
        out[i] = state
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 4.8), sharex=True)
    axes[0].plot(t, vin, color="0.4", lw=0.6)
    for th, ls in ((2.5, "-"), (2.45, ":"), (2.55, ":")):
        axes[0].axhline(th, color=PALETTE[1], ls=ls, lw=0.8)
    axes[0].set_ylabel("input (V)")
    axes[1].plot(t, plain, color=PALETTE[0], lw=0.8)
    axes[1].set_ylabel("comparator")
    axes[1].set_ylim(-0.5, 5.5)
    axes[2].plot(t, out, color=PALETTE[2], lw=1.2)
    axes[2].set_ylabel("Schmitt")
    axes[2].set_ylim(-0.5, 5.5)
    axes[2].set_xlabel("time (arbitrary units)")
    fig.tight_layout()
    save(fig, f"{OUT}/schmitt.svg")


def tia(f, cf, rf=100e3, cin=14e-12, gbw=10e6):
    s = 2j * np.pi * f
    a = 2 * np.pi * gbw / s
    zf = rf / (1 + s * rf * cf)
    zin = 1 / (s * cin)
    beta = zin / (zin + zf)
    t = a * beta
    return zf * t / (1 + t)


def fig_tia():
    f = np.logspace(3, 8, 600)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.loglog(f, np.abs(tia(f, 1e-18)) / 1e3, color=PALETTE[1], label="no $C_F$: peaking about 9.4 ×")
    ax.loglog(f, np.abs(tia(f, 2.105e-12)) / 1e3, color=PALETTE[0], label="$C_F$ = 2.105 pF: Butterworth, $-3$ dB at 0.994 MHz")
    ax.axhline(100, color="0.6", ls=":")
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("$|v_o/i_{pd}|$ (kΩ)")
    ax.set_ylim(1, 2000)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/tia.svg")


def fig_circuits():
    """Schematics of the chapter's circuits (schemdraw): difference amplifier, superdiode, two-diode inverting
    rectifier, non-inverting Schmitt trigger, transimpedance amplifier and relaxation oscillator."""
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)

    def title(x, y, text):
        d.add(elm.Label().at((x, y)).label(text, fontsize=12))

    # (a) difference amplifier
    x, y = 2.5, 10.0
    title(x + 1.0, y + 3.0, "(a) difference amplifier")
    op = d.add(elm.Opamp(leads=True).right().at((x, y)))
    d.add(elm.Line().at(op.in1).left().length(0.5))
    n1 = d.add(elm.Dot())
    d.add(elm.Resistor().left().length(2.0).label("$R_1$"))
    d.add(elm.Dot(open=True).label("$v_1$", loc="left"))
    d.add(elm.Line().at(n1.center).up().length(1.5))
    d.add(elm.Resistor().right().tox(op.out[0] + 0.5).label("$R_2 = KR_1$"))
    d.add(elm.Line().down().toy(op.out[1]))
    d.add(elm.Line().at(op.out).right().length(0.5))
    d.add(elm.Dot(open=True).label("$v_o$", loc="right"))
    d.add(elm.Line().at(op.in2).left().length(0.5))
    n2 = d.add(elm.Dot())
    d.add(elm.Resistor().left().length(2.0).label("$R_3$", loc="bottom"))
    d.add(elm.Dot(open=True).label("$v_2$", loc="left"))
    d.add(elm.Resistor().at(n2.center).down().length(1.6).label("$R_4 = KR_3$", loc="bottom"))
    d.add(elm.Ground())

    # (b) superdiode: v_in into +, the diode inside the loop, feedback from v_o to -
    x, y = 12.0, 10.0
    title(x + 1.0, y + 3.0, "(b) superdiode")
    op = d.add(elm.Opamp(leads=True).right().at((x, y)))
    d.add(elm.Line().at(op.in2).left().length(1.2))
    d.add(elm.Dot(open=True).label("$v_{in}$", loc="left"))
    d.add(elm.Diode().at(op.out).right().length(1.6))
    no = d.add(elm.Dot())
    d.add(elm.Line().right().length(0.8))
    d.add(elm.Dot(open=True).label("$v_o$", loc="right"))
    d.add(elm.Resistor().at(no.center).down().length(1.6).label("$R_L$", loc="bottom"))
    d.add(elm.Ground())
    d.add(elm.Line().at(op.in1).left().length(0.5))
    d.add(elm.Line().up().length(1.2))
    d.add(elm.Line().right().tox(no.center[0]))
    d.add(elm.Line().down().toy(no.center[1]))

    # (c) two-diode inverting rectifier
    x, y = 21.5, 10.0
    title(x + 1.0, y + 3.5, "(c) two-diode inverting rectifier")
    op = d.add(elm.Opamp(leads=True).right().at((x, y)))
    d.add(elm.Line().at(op.in1).left().length(0.5))
    nn = d.add(elm.Dot())
    d.add(elm.Resistor().left().length(2.0).label("$R$"))
    d.add(elm.Dot(open=True).label("$v_{in}$", loc="left"))
    d.add(elm.Line().at(op.in2).left().length(0.5))
    d.add(elm.Ground())
    d.add(elm.Line().at(op.out).right().length(0.4))
    na = d.add(elm.Dot())
    d.add(elm.Diode().right().length(1.4).label("$D_2$", loc="bottom"))
    nv = d.add(elm.Dot())
    d.add(elm.Line().right().length(0.6))
    d.add(elm.Dot(open=True).label("$v_o$", loc="right"))
    d.add(elm.Line().at(nn.center).up().length(1.2))
    d.add(elm.Diode().right().tox(na.center[0]).label("$D_1$"))
    d.add(elm.Line().down().toy(na.center[1]))
    d.add(elm.Line().at((nn.center[0], nn.center[1] + 1.2)).up().length(1.0))
    d.add(elm.Resistor().right().tox(nv.center[0]).label("$R_F$"))
    d.add(elm.Line().down().toy(nv.center[1]))

    # (d) non-inverting Schmitt trigger
    x, y = 2.5, 2.5
    title(x + 1.0, y + 3.0, "(d) non-inverting Schmitt trigger")
    op = d.add(elm.Opamp(leads=True).right().at((x, y)))
    d.add(elm.Line().at(op.in1).left().length(1.2))
    d.add(elm.Dot(open=True).label("$V_{ref}$", loc="left"))
    d.add(elm.Line().at(op.in2).left().length(0.5))
    npl = d.add(elm.Dot())
    d.add(elm.Resistor().left().length(2.0).label("$R_1$"))
    d.add(elm.Dot(open=True).label("$v_{in}$", loc="left"))
    d.add(elm.Line().at(npl.center).down().length(1.4))
    d.add(elm.Resistor().right().tox(op.out[0] + 0.5).label("$R_2$", loc="bottom"))
    d.add(elm.Line().up().toy(op.out[1]))
    d.add(elm.Line().at(op.out).right().length(0.5))
    d.add(elm.Dot(open=True).label("$v_o$ (0 or $V_{DD}$)", loc="right"))

    # (e) transimpedance amplifier
    x, y = 12.5, 2.5
    title(x + 1.0, y + 3.8, "(e) photodiode TIA")
    op = d.add(elm.Opamp(leads=True).right().at((x, y)))
    d.add(elm.Line().at(op.in1).left().length(0.8))
    nt = d.add(elm.Dot())
    d.add(elm.Photodiode().down().length(1.6).reverse().label("$C_{in}$", loc="bottom"))
    d.add(elm.Ground())
    d.add(elm.Line().at(op.in2).left().length(0.5))
    d.add(elm.Ground())
    d.add(elm.Line().at(nt.center).up().length(1.2))
    d.add(elm.Resistor().right().tox(op.out[0] + 0.5).label("$R_F$"))
    d.add(elm.Line().down().toy(op.out[1]))
    d.add(elm.Line().at((nt.center[0], nt.center[1] + 1.2)).up().length(1.2))
    d.add(elm.Capacitor().right().tox(op.out[0] + 0.5).label("$C_F$"))
    d.add(elm.Line().down().length(1.2))
    d.add(elm.Line().at(op.out).right().length(1.0))
    d.add(elm.Dot(open=True).label("$v_o$", loc="right"))

    # (f) relaxation oscillator
    x, y = 22.0, 2.5
    title(x + 1.0, y + 3.0, "(f) relaxation oscillator")
    op = d.add(elm.Opamp(leads=True).right().at((x, y)))
    d.add(elm.Line().at(op.in1).left().length(2.4))
    nc = d.add(elm.Dot())
    d.add(elm.Capacitor().down().length(1.6).label("$C$", loc="bottom"))
    d.add(elm.Ground())
    d.add(elm.Line().at(nc.center).up().length(1.4))
    d.add(elm.Resistor().right().tox(op.out[0] + 0.6).label("$R$"))
    d.add(elm.Line().down().toy(op.out[1]))
    d.add(elm.Line().at(op.out).right().length(0.6))
    nout = d.add(elm.Dot())
    d.add(elm.Line().right().length(0.6))
    d.add(elm.Dot(open=True).label("$v_o = \\pm V_s$", loc="right"))
    d.add(elm.Line().at(op.in2).left().length(0.6))
    npp = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.0))
    d.add(elm.Resistor().down().length(1.4).label("$R_1$", loc="bottom"))
    d.add(elm.Ground())
    d.add(elm.Line().at(nout.center).down().length(2.3))
    d.add(elm.Resistor().left().tox(npp.center[0]).label("$R_2$", loc="bottom"))
    d.add(elm.Line().up().toy(npp.center[1]))
    d.save(str(ROOT / OUT / "circuits.svg"))


if __name__ == "__main__":
    fig_circuits()
    fig_schmitt()
    fig_tia()
