#!/usr/bin/env python3
"""Figures for chapter 10-08 (current sources and current mirrors).

Run from anywhere:  python assets/figures/src/fig_10_08.py
Outputs SVGs to assets/figures/10-08/:
- mirror-characteristics.svg: output current against output voltage for a basic NMOS mirror and a cascode
  mirror with the same reference (k_n = 4 mA/V^2, V_TN = 0.5 V, lambda = 0.1 1/V, I_ref = 0.2463 mA as in
  Example 10-02.5), solved with the large-signal square law (triode and saturation, channel-length modulation;
  body effect ignored), showing compliance voltage and output resistance;
- mismatch.svg: standard deviation of the current ratio of two mirror transistors against gate area for three
  overdrives, from sigma(dI/I) = (2/V_ov) sigma(dV_TH) with sigma(dV_TH) = A_VT/sqrt(WL), using an illustrative
  A_VT = 3.5 mV um (a process parameter; foundries publish their own);
- mirror-schematics.svg: schematics (schemdraw) of (a) the basic NMOS mirror, (b) the NMOS cascode mirror,
  (c) the bipolar Wilson mirror and (d) the Widlar current source.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/10-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
K, VTN, LAM = 4e-3, 0.5, 0.1


def ids(vgs, vds):
    vov = vgs - VTN
    if vov <= 0:
        return 0.0
    if vds < vov:
        return K * (vov - vds / 2) * vds * (1 + LAM * vds)
    return 0.5 * K * vov * vov * (1 + LAM * vds)


VGS1 = brentq(lambda v: (3.3 - v) / 10e3 - ids(v, v), 0.5, 3.3)
IREF = (3.3 - VGS1) / 10e3
# cascode reference: M3 (diode) sits on M1 and carries I_ref with its source at V_GS1
VG3 = VGS1 + brentq(lambda v: IREF - ids(v, v), 0.5, 3.3)


def basic(vout):
    return ids(VGS1, vout)


def cascode(vout):
    # find the middle node V_X where M2's current equals M4's
    def f(vx):
        return ids(VGS1, vx) - ids(VG3 - vx, vout - vx)
    if vout <= 1e-9:
        return 0.0
    vx = brentq(f, 0.0, vout)
    return ids(VGS1, vx)


def fig_characteristics():
    v = np.linspace(0, 3.0, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(v, [basic(x) * 1e3 for x in v], color=PALETTE[0], label="basic mirror")
    ax.plot(v, [cascode(x) * 1e3 for x in v], color=PALETTE[1], label="cascode mirror")
    ax.axhline(IREF * 1e3, color="0.6", ls=":")
    ax.text(2.05, IREF * 1e3 - 0.022, "$I_{ref}$ = 0.246 mA", fontsize=8, color="0.3")
    ax.axvline(VGS1 - VTN, color=PALETTE[0], ls="--", lw=0.8)
    ax.axvline(VTN + 2 * (VGS1 - VTN), color=PALETTE[1], ls="--", lw=0.8)
    ax.text(VGS1 - VTN + 0.03, 0.03, "$V_{ov}$", fontsize=8, color=PALETTE[0])
    ax.text(VTN + 2 * (VGS1 - VTN) + 0.03, 0.03, "$V_{TN} + 2V_{ov}$", fontsize=8, color=PALETTE[1])
    ax.set_xlabel("output voltage $V_{out}$ (V)")
    ax.set_ylabel("output current (mA)")
    ax.set_ylim(0, 0.32)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/mirror-characteristics.svg")


def fig_mismatch():
    area = np.logspace(0, 4, 200)          # um^2
    avt = 3.5                               # mV um, illustrative
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    for vov, col in ((0.1, PALETTE[0]), (0.2, PALETTE[1]), (0.4, PALETTE[2])):
        ax.loglog(area, 2 / vov * avt / np.sqrt(area) * 1e-3 * 100, color=col, label=f"$V_{{ov}}$ = {vov} V")
    ax.axhline(0.1, color="0.6", ls=":")
    ax.text(1.2, 0.115, "0.1%", fontsize=8, color="0.3")
    ax.set_xlabel("gate area $WL$ ($\\mu$m²)")
    ax.set_ylabel("$\\sigma(\\Delta I/I)$ (%)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/mismatch.svg")


def fig_schematics():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)

    # (a) basic NMOS mirror
    d += elm.Label().at((1.6, 6.2)).label("(a) basic MOS mirror", fontsize=12)
    d += (m1 := elm.NFet(bulk=False).right().at((0.0, 1.0)))
    d += (m2 := elm.NFet(bulk=False).right().reverse().at((3.2, 1.0)))
    d += elm.Line().at(m1.gate).to(m2.gate)
    d += elm.Line().at(m1.drain).up().length(0.6)
    d += (n1 := elm.Dot())
    d += elm.Line().at(n1.center).right().tox(m1.gate[0] + 0.4)
    d += elm.Line().down().toy(m1.gate[1])
    d += elm.Dot().at((m1.gate[0] + 0.4, m1.gate[1]))
    d += elm.SourceI().at(n1.center).up().length(1.6).reverse().label("$I_{ref}$", loc="bottom")
    d += elm.Vdd().label("$V_{DD}$")
    d += elm.Line().at(m2.drain).up().length(1.0)
    d += elm.Dot(open=True).label("$I_{out}$ (to load)", loc="right")
    d += elm.Line().at(m1.source).down().length(0.4)
    d += elm.Ground()
    d += elm.Line().at(m2.source).down().length(0.4)
    d += elm.Ground()
    d += elm.Label().at((m1.drain[0] - 0.6, m1.drain[1] - 0.6)).label("M1", fontsize=10)
    d += elm.Label().at((m2.drain[0] + 0.6, m2.drain[1] - 0.6)).label("M2", fontsize=10)

    # (b) NMOS cascode mirror
    x0 = 7.5
    d += elm.Label().at((x0 + 1.6, 6.2)).label("(b) cascode MOS mirror", fontsize=12)
    d += (b1 := elm.NFet(bulk=False).right().at((x0, 0.0)))
    d += (b2 := elm.NFet(bulk=False).right().reverse().at((x0 + 3.2, 0.0)))
    d += elm.Line().at(b1.gate).to(b2.gate)
    d += elm.Line().at(b1.drain).up().length(0.5)
    d += (bn := elm.Dot())
    d += elm.Line().at(bn.center).right().tox(b1.gate[0] + 0.4)
    d += elm.Line().down().toy(b1.gate[1])
    d += elm.Dot().at((b1.gate[0] + 0.4, b1.gate[1]))
    d += elm.Line().at(bn.center).up().length(0.6)
    d += (b3 := elm.NFet(bulk=False).right().anchor("source"))
    d += elm.Line().at(b2.drain).up().length(1.1)
    d += (b4 := elm.NFet(bulk=False).right().reverse().anchor("source"))
    d += elm.Line().at(b3.gate).to(b4.gate)
    d += elm.Line().at(b3.drain).up().length(0.5)
    d += (tn := elm.Dot())
    d += elm.Line().at(tn.center).right().tox(b3.gate[0] + 0.4)
    d += elm.Line().down().toy(b3.gate[1])
    d += elm.Dot().at((b3.gate[0] + 0.4, b3.gate[1]))
    d += elm.SourceI().at(tn.center).up().length(1.2).reverse().label("$I_{ref}$", loc="bottom")
    d += elm.Vdd().label("$V_{DD}$")
    d += elm.Line().at(b4.drain).up().length(0.8)
    d += elm.Dot(open=True).label("$I_{out}$", loc="right")
    d += elm.Line().at(b1.source).down().length(0.4)
    d += elm.Ground()
    d += elm.Line().at(b2.source).down().length(0.4)
    d += elm.Ground()
    for m, lab, dx in ((b1, "M1", -0.6), (b2, "M2", 0.6), (b3, "M3", -0.6), (b4, "M4", 0.6)):
        d += elm.Label().at((m.drain[0] + dx, m.drain[1] - 0.6)).label(lab, fontsize=10)

    # (c) bipolar Wilson mirror
    x1 = 15.0
    d += elm.Label().at((x1 + 1.6, 6.2)).label("(c) Wilson mirror (bipolar)", fontsize=12)
    d += (q1 := elm.BjtNpn().right().reverse().at((x1, 0.0)))
    d += (q2 := elm.BjtNpn().right().at((x1 + 3.2, 0.0)))
    d += elm.Line().at(q1.base).to(q2.base)
    d += elm.Line().at(q2.collector).up().length(0.5)
    d += (xn := elm.Dot())
    d += elm.Line().at(xn.center).left().tox(q2.base[0] - 0.4)
    d += elm.Line().down().toy(q2.base[1])
    d += elm.Dot().at((q2.base[0] - 0.4, q2.base[1]))
    d += (q3 := elm.BjtNpn().right().at((xn.center[0], xn.center[1] + 1.2)).anchor("emitter"))
    d += elm.Line().at(xn.center).to(q3.emitter)
    d += elm.Line().at(q1.collector).up().toy(q3.base[1])
    d += (an := elm.Dot())
    d += elm.Line().at(an.center).to(q3.base)
    d += elm.SourceI().at(an.center).up().length(1.4).reverse().label("$I_{ref}$", loc="bottom")
    d += elm.Vdd().label("$V_{CC}$")
    d += elm.Line().at(q3.collector).up().length(0.8)
    d += elm.Dot(open=True).label("$I_{out}$", loc="right")
    d += elm.Line().at(q1.emitter).down().length(0.4)
    d += elm.Ground()
    d += elm.Line().at(q2.emitter).down().length(0.4)
    d += elm.Ground()
    for q, lab, dx in ((q1, "Q1", -0.6), (q2, "Q2", 0.7), (q3, "Q3", 0.7)):
        d += elm.Label().at((q.collector[0] + dx, q.collector[1] - 0.5)).label(lab, fontsize=10)

    # (d) Widlar source
    x2 = 22.5
    d += elm.Label().at((x2 + 1.6, 6.2)).label("(d) Widlar source", fontsize=12)
    d += (w1 := elm.BjtNpn().right().reverse().at((x2, 1.0)))
    d += (w2 := elm.BjtNpn().right().at((x2 + 3.2, 1.0)))
    d += elm.Line().at(w1.base).to(w2.base)
    d += elm.Line().at(w1.collector).up().length(0.6)
    d += (wn := elm.Dot())
    d += elm.Line().at(wn.center).right().tox(w1.base[0] + 0.4)
    d += elm.Line().down().toy(w1.base[1])
    d += elm.Dot().at((w1.base[0] + 0.4, w1.base[1]))
    d += elm.SourceI().at(wn.center).up().length(1.6).reverse().label("$I_{ref}$", loc="bottom")
    d += elm.Vdd().label("$V_{CC}$")
    d += elm.Line().at(w2.collector).up().length(1.0)
    d += elm.Dot(open=True).label("$I_{out}$", loc="right")
    d += elm.Line().at(w1.emitter).down().length(1.2)
    d += elm.Ground()
    d += elm.Resistor().at(w2.emitter).down().length(1.2).label("$R_E$", loc="bottom")
    d += elm.Ground()
    d += elm.Label().at((w1.collector[0] - 0.6, w1.collector[1] - 0.5)).label("Q1", fontsize=10)
    d += elm.Label().at((w2.collector[0] + 0.7, w2.collector[1] - 0.5)).label("Q2", fontsize=10)
    d.save(str(ROOT / OUT / "mirror-schematics.svg"))


if __name__ == "__main__":
    fig_schematics()
    fig_characteristics()
    fig_mismatch()
