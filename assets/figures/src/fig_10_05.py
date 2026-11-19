#!/usr/bin/env python3
"""Figures for chapter 10-05 (amplifier fundamentals).

Run from anywhere:  python assets/figures/src/fig_10_05.py
Outputs SVGs to assets/figures/10-05/:
- amplifier-models.svg: the four unilateral amplifier models (voltage, current, transconductance,
  transresistance), each with its input resistance, controlled source and output resistance;
- ce-transfer.svg: the large-signal transfer characteristic v_C(v_BE) of the common-emitter stage of
  Example 10-04.1 (I_S = 1e-15 A, R_C = 5 kOhm, V_CC = 10 V, V_CE,sat = 0.2 V), with the bias point,
  its tangent (slope -g_m R_C) and the cutoff and saturation limits.
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

OUT = "assets/figures/10-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
VT = 1.380649e-23 * 300 / 1.602176634e-19


def model(d, x0, y0, title, in_label, src, src_label, series_out):
    """One two-port model with its input port at (x0, y0) (top terminal) and height 3."""
    h = 3.0
    d += elm.Label().at((x0 + 3.2, y0 + 1.1)).label(title, fontsize=13)
    d += elm.Dot(open=True).at((x0, y0)).label(in_label, loc="left")
    d += elm.Line().at((x0, y0)).right().length(1.2)
    d += elm.Resistor().down().length(h).label("$R_i$", loc="bottom")
    d += elm.Line().left().length(1.2)
    d += elm.Dot(open=True)
    xo = x0 + 3.6
    if series_out:      # Thevenin output: controlled voltage source in series with R_o
        d += src.at((xo, y0 - h)).up().length(h).label(src_label, loc="bottom")
        d += elm.Resistor().right().length(2.2).label("$R_o$", loc="top")
        d += elm.Dot(open=True).label("$v_o$", loc="right")
        d += elm.Line().at((xo, y0 - h)).right().length(2.2)
        d += elm.Dot(open=True)
    else:               # Norton output: controlled current source in parallel with R_o
        d += src.at((xo, y0 - h)).up().length(h).label(src_label, loc="bottom")
        d += elm.Line().right().length(1.6)
        d += elm.Resistor().down().length(h).label("$R_o$", loc="bottom")
        d += elm.Line().left().length(1.6)
        d += elm.Line().at((xo + 1.6, y0)).right().length(1.0)
        d += elm.Dot(open=True).label("$i_o$ (into load)", loc="right")
        d += elm.Line().at((xo + 1.6, y0 - h)).right().length(1.0)
        d += elm.Dot(open=True)


def fig_models():
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    model(d, 0, 0, "(a) voltage amplifier", "$v_i$", elm.SourceControlledV(), "$A_{vo}v_i$", True)
    model(d, 10, 0, "(b) current amplifier", "$i_i\\rightarrow$", elm.SourceControlledI(), "$A_{is}i_i$", False)
    model(d, 0, -5.5, "(c) transconductance amplifier", "$v_i$", elm.SourceControlledI(), "$G_mv_i$", False)
    model(d, 10, -5.5, "(d) transresistance amplifier", "$i_i\\rightarrow$", elm.SourceControlledV(), "$R_mi_i$", True)
    d.save(str(ROOT / OUT / "amplifier-models.svg"))


def fig_transfer():
    i_s, rc, vcc, vsat = 1e-15, 5e3, 10.0, 0.2
    vbe = np.linspace(0.60, 0.76, 800)
    vc = np.maximum(vcc - rc * i_s * np.exp(vbe / VT), vsat)
    vq = VT * math.log(1e-3 / i_s)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(vbe, vc, color=PALETTE[0], label="$v_C$ (exponential transistor)")
    t = np.linspace(vq - 0.03, vq + 0.03, 10)
    ax.plot(t, 5 - (1e-3 / VT) * rc * (t - vq), color=PALETTE[1], ls="--",
            label="tangent at Q: slope $-g_mR_C$ = $-193$")
    ax.plot(vq, 5, "o", color="k", ms=5)
    ax.annotate("Q (1 mA, 5 V)", (vq, 5), xytext=(vq - 0.07, 3.0), fontsize=9,
                arrowprops=dict(arrowstyle="->", color="0.3"))
    ax.axhline(vsat, color="0.6", ls=":")
    ax.text(0.605, 0.45, "saturation ($V_{CE,sat}$ = 0.2 V)", fontsize=8, color="0.3")
    ax.text(0.605, 9.4, "cutoff: $v_C \\approx V_{CC}$", fontsize=8, color="0.3")
    ax.set_xlim(0.60, 0.76)
    ax.set_ylim(0, 10.5)
    ax.set_xlabel("$v_{BE}$ (V)")
    ax.set_ylabel("$v_C$ (V)")
    ax.legend(fontsize=8, loc="lower left", bbox_to_anchor=(0.0, 0.12))
    fig.tight_layout()
    save(fig, f"{OUT}/ce-transfer.svg")


if __name__ == "__main__":
    fig_models()
    fig_transfer()
