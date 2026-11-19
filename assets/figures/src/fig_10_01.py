#!/usr/bin/env python3
"""Figures for chapter 10-01 (diodes and diode circuits).

Run from anywhere:  python assets/figures/src/fig_10_01.py
Outputs SVGs to assets/figures/10-01/:
- diode-models.svg: the exponential, piecewise-linear, constant-drop and ideal models, and the load line of
  Example 10-01.1;
- rectifier-ripple.svg: the half-wave peak rectifier of Example 10-01.4 (output, source and diode current);
- linear-supply.svg: schematic of a transformer, bridge, reservoir capacitor and Zener shunt regulator;
- wave-shaping.svg: the limiter of Example 10-01.7 (exponential against constant-drop) and the clamp and
  doubler waveforms.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

VT = 0.025852
IS = 1e-15


def fig_models():
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.6))
    v = np.linspace(0, 0.85, 600)
    i_exp = IS * (np.exp(v / VT) - 1) * 1e3
    a.plot(v, i_exp, color=PALETTE[0], label="exponential ($I_S$ = 10$^{-15}$ A)")
    # piecewise-linear fit through 0.1 mA and 1 mA points of the exponential
    v1, v2 = VT * math.log(0.1e-3 / IS), VT * math.log(1e-3 / IS)
    rd = (v2 - v1) / 0.9e-3
    vd0 = v2 - rd * 1e-3
    a.plot(v, np.where(v > vd0, (v - vd0) / rd * 1e3, 0), color=PALETTE[1], ls="--",
           label=f"piecewise-linear ($V_{{D0}}$ = {vd0:.3f} V, $r_D$ = {rd:.0f} Ω)")
    a.plot([0, 0.7, 0.7], [0, 0, 2], color=PALETTE[2], ls=":", label="constant drop (0.7 V)")
    a.plot([0, 0, 0], [0, 0, 2], color="0.3", lw=2.5, label="ideal")
    a.set_xlim(-0.05, 0.85)
    a.set_ylim(-0.05, 2)
    a.set_xlabel("$v_D$ (V)")
    a.set_ylabel("$i_D$ (mA)")
    a.legend(fontsize=7, loc="upper left")
    a.set_title("(a) four diode models", fontsize=10)
    # load line, Example 10-01.1
    V, R = 5.0, 4.3e3
    vv = np.linspace(0.55, 0.78, 400)
    b.plot(vv, IS * (np.exp(vv / VT) - 1) * 1e3, color=PALETTE[0], label="diode: $i_D = I_S(e^{v_D/V_T}-1)$")
    b.plot(vv, (V - vv) / R * 1e3, color=PALETTE[3], label="load line: $i_D = (5 - v_D)/4.3$ kΩ")
    vq = brentq(lambda x: IS * (math.exp(x / VT) - 1) - (V - x) / R, 0.5, 0.9)
    b.plot(vq, (V - vq) / R * 1e3, "o", color="k", ms=5)
    b.annotate(f"Q: {vq:.4f} V, {(V - vq) / R * 1e3:.4f} mA", (vq, (V - vq) / R * 1e3), (0.58, 1.6),
               fontsize=8, arrowprops=dict(arrowstyle="->", color="0.4"))
    b.set_xlim(0.55, 0.78)
    b.set_ylim(0, 2)
    b.set_xlabel("$v_D$ (V)")
    b.set_ylabel("$i_D$ (mA)")
    b.legend(fontsize=7, loc="upper left")
    b.set_title("(b) the operating point of Example 10-01.1", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/diode-models.svg")


def fig_rectifier():
    Vs, f, R, C, VD = 12.0, 60.0, 1e3, 470e-6, 0.7
    w, T = 2 * math.pi * f, 1 / f
    toff = brentq(lambda t: -C * w * Vs * math.sin(w * t) + (Vs * math.cos(w * t) - VD) / R, 0, T / 4)
    voff = Vs * math.cos(w * toff) - VD
    ton = brentq(lambda t: voff * math.exp(-(t - toff) / (R * C)) - (Vs * math.cos(w * t) - VD), 0.75 * T,
                 T + 0.999 * toff)
    t = np.linspace(-0.25 * T, 2.25 * T, 4000)
    tm = np.mod(t - toff, T) + toff        # map into [toff, toff + T)
    on = tm >= ton
    vo = np.where(on, Vs * np.cos(w * tm) - VD, voff * np.exp(-(tm - toff) / (R * C)))
    iD = np.where(on, -C * w * Vs * np.sin(w * tm) + vo / R, 0.0)
    fig, (a, b) = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True, gridspec_kw=dict(height_ratios=[1.6, 1]))
    a.plot(t * 1e3, Vs * np.cos(w * t) - VD, color="0.6", lw=1, label="$v_S - 0.7$ V")
    a.plot(t * 1e3, vo, color=PALETTE[0], label="$v_O$")
    a.set_ylim(-13, 13)
    a.set_ylabel("voltage (V)")
    a.legend(fontsize=8, loc="lower left")
    ins = a.inset_axes([0.62, 0.08, 0.36, 0.42])
    ins.plot(t * 1e3, vo, color=PALETTE[0])
    ins.plot(t * 1e3, Vs * np.cos(w * t) - VD, color="0.6", lw=1)
    ins.set_xlim(14.5, 17.5)
    ins.set_ylim(10.8, 11.4)
    ins.tick_params(labelsize=7)
    ins.set_title(f"ripple {voff - (Vs * math.cos(w * ton) - VD):.3f} V", fontsize=7)
    b.plot(t * 1e3, iD * 1e3, color=PALETTE[1])
    b.set_ylabel("$i_D$ (mA)")
    b.set_xlabel("time (ms)")
    b.text(0.02, 0.75, "diode conducts for about 4% of each cycle", transform=b.transAxes, fontsize=8, color="0.3")
    fig.tight_layout()
    save(fig, f"{OUT}/rectifier-ripple.svg")


def fig_supply():
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += (src := elm.SourceSin().up().label("120 V rms\n60 Hz", loc="left"))
    d += elm.Line().right().length(1)
    d += (t := elm.Transformer(t1=4, t2=4).anchor("p1").label("step-down", loc="top"))
    d += elm.Line().left().at(t.p2).tox(src.start)
    d += elm.Line().right().at(t.s1).length(1.2)
    d += (top := elm.Dot())
    d += elm.Line().right().at(t.s2).length(1.2)
    d += (bot := elm.Dot())
    # bridge drawn as a diamond
    d += (d1 := elm.Diode().theta(45).at(bot.center).label("D1", loc="bottom"))
    d += (d2 := elm.Diode().theta(-45).at(top.center).label("D2", loc="top"))
    d += elm.Diode().theta(135).at(bot.center).reverse().label("D3", loc="top")
    d += elm.Line().at(top.center).to(bot.center).color("white").zorder(0)
    d += (pos := elm.Dot().at(d2.end))
    d += elm.Line().right().at(pos.center).length(1.5)
    d += (n1 := elm.Dot())
    d += elm.Capacitor(polar=True).down().label("$C$", loc="bottom").length(3)
    d += (g1 := elm.Dot())
    d += elm.Resistor().right().at(n1.center).label("$R$")
    d += (n2 := elm.Dot())
    d += elm.Zener().down().reverse().label("$V_Z$", loc="bottom").length(3)
    d += (g2 := elm.Dot())
    d += elm.Line().right().at(n2.center).length(1.5)
    d += elm.Dot(open=True).label("$V_O$", loc="right")
    d += elm.Line().right().at(g2.center).length(1.5)
    d += elm.Dot(open=True)
    d += elm.Line().left().at(g2.center).to(g1.center)
    d += elm.Line().left().at(g1.center).tox(d1.end)
    d += elm.Diode().at(d1.end).to((d1.end[0], d1.end[1] + 0.001)).color("white").zorder(0)
    d += elm.Diode().theta(45).at((d1.end[0] - 0.0, d1.end[1])).to(pos.center).reverse().label("D4", loc="bottom")
    d.save(str(ROOT / OUT / "linear-supply.svg"))


def fig_wave_shaping():
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.5))
    vin = np.linspace(-3, 3, 601)
    vout = np.array([brentq(lambda v: 2 * IS * math.sinh(v / VT) - (x - v) / 1e3, -abs(x) - 1e-9, abs(x) + 1e-9)
                     if abs(x) > 1e-12 else 0.0 for x in vin])
    a.plot(vin, vout, color=PALETTE[0], label="exponential diodes")
    a.plot(vin, np.clip(vin, -0.7, 0.7), color=PALETTE[2], ls="--", label="constant-drop model")
    a.set_xlabel("$v_I$ (V)")
    a.set_ylabel("$v_O$ (V)")
    a.legend(fontsize=8, loc="upper left")
    a.set_title("(a) back-to-back diode limiter, $R$ = 1 kΩ", fontsize=10)
    t = np.linspace(0, 2e-3, 800)
    vi = 5 * np.sin(2 * math.pi * 1e3 * t)
    b.plot(t * 1e3, vi, color="0.6", lw=1, label="input, 5 V peak")
    b.plot(t * 1e3, vi + 5 - 0.7, color=PALETTE[0], label="clamped (steady state)")
    b.axhline(2 * 5 - 1.4, color=PALETTE[1], ls="--", label="doubler output, 8.6 V")
    b.set_xlabel("time (ms)")
    b.set_ylabel("voltage (V)")
    b.legend(fontsize=7, loc="lower right")
    b.set_title("(b) clamp and voltage doubler", fontsize=10)
    fig.tight_layout()
    save(fig, f"{OUT}/wave-shaping.svg")


if __name__ == "__main__":
    fig_models()
    fig_rectifier()
    fig_supply()
    fig_wave_shaping()
