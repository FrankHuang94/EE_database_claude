#!/usr/bin/env python3
"""Figure for chapter 15-01 (modeling dynamic systems).

Run from anywhere:  python assets/figures/src/fig_15_01.py
Outputs
  assets/figures/15-01/thermal.svg          left, Example 15-01.3's two-node junction and case temperatures after a
                                            100 W step; right, Example 15-01.4's heat balance (heat generated with
                                            leakage against heat removed for R = 0.5 K/W and the critical 0.628 K/W)
  assets/figures/15-01/analogues.svg        the mass-spring-damper's force-voltage (series RLC) and force-current
                                            (parallel RLC) analogue circuits
  assets/figures/15-01/motor-circuit.svg    the DC motor's armature circuit with its back-EMF source
  assets/figures/15-01/thermal-network.svg  the two-node junction / heat-sink thermal network of Example 15-01.3
Uses labs/15-01-lab/plants.py; the schematics use schemdraw.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "15-control-systems" / "labs" / "15-01-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import plants  # noqa: E402

OUT = "assets/figures/15-01"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_thermal():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6))
    A, B = plants.thermal_two_node(0.15, 0.35, 5.0, 300.0)
    ts = np.logspace(-2, 3.2, 400)
    xs = np.array([plants.step(A, B, 100.0, t) for t in ts])
    a1.semilogx(ts, 30 + xs[:, 0], color=PALETTE[0], label="junction $T_J$")
    a1.semilogx(ts, 30 + xs[:, 1], color=PALETTE[1], label="case / heat sink $T_C$")
    a1.axhline(80, color="gray", lw=0.6, ls=":")
    a1.annotate("fast: τ ≈ 0.74 s (≈ $R_{JC}C_J$)", (0.8, 42), fontsize=7)
    a1.annotate("slow: τ ≈ 107 s (≈ $R_{CA}C_H$)", (60, 52), fontsize=7)
    a1.set_xlabel("time after the 100 W step (s)")
    a1.set_ylabel("temperature (°C)")
    a1.set_title("Two thermal time scales", fontsize=9)
    a1.legend(fontsize=7, loc="upper left")

    T = np.linspace(25, 140, 400)
    gen = 60 + 5 * np.exp((T - 25) / 30)
    a2.plot(T, gen, color=PALETTE[2], label="heat generated $P_d + P_L(T)$")
    for Rth, ls in ((0.5, "-"), (0.628, "--")):
        a2.plot(T, (T - 25) / Rth, color=PALETTE[0], ls=ls, label=f"heat removed, R = {Rth} K/W")
    for Teq, mk in ((64.25, "o"), (124.9, "s")):
        a2.plot(Teq, (Teq - 25) / 0.5, marker=mk, color="black", ms=5, ls="none")
    a2.annotate("stable", (64.25, (64.25 - 25) / 0.5), textcoords="offset points", xytext=(6, -12), fontsize=7)
    a2.annotate("unstable", (124.9, (124.9 - 25) / 0.5), textcoords="offset points", xytext=(-48, 6), fontsize=7)
    a2.set_xlabel("chip temperature T (°C)")
    a2.set_ylabel("heat flow (W)")
    a2.set_ylim(0, 250)
    a2.set_title("Leakage feedback: equilibria and runaway", fontsize=9)
    a2.legend(fontsize=7, loc="upper left")
    fig.tight_layout()
    save(fig, f"{OUT}/thermal.svg")


def save_schem(d, rel):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(path))
    print(f"wrote {rel}")


def fig_analogues():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    # force-voltage: one loop carrying the velocity v as current
    d += (src := elm.SourceV().up().label("$F(t)$", loc="left"))
    d += elm.Inductor().right().label("$L = m$", loc="top")
    d += elm.Resistor().right().label("$R = b$", loc="top")
    d += elm.Capacitor().down().label("$C = 1/k$", loc="right")
    d += elm.Line().left().tox(src.start)
    d += elm.Label().at((3.0, -1.2)).label("force–voltage: series RLC, loop current = velocity v")
    # force-current: one node whose voltage is the velocity
    x0 = 11.0
    d += (isrc := elm.SourceI().at((x0, 0)).up().label("$F(t)$", loc="left"))
    d += (top := elm.Line().right().length(2.0))
    d += elm.Capacitor().down().label("$C = m$", loc="right")
    d += elm.Line().at(top.end).right().length(2.0)
    d += elm.Resistor().down().label("$R = 1/b$", loc="right")
    d += elm.Line().at((x0 + 4.0, 3.0)).right().length(2.0)
    d += elm.Inductor().down().label("$L = 1/k$", loc="right")
    d += elm.Line().left().tox(isrc.start)
    d += elm.Label().at((x0 + 3.0, -1.2)).label("force–current: parallel RLC, node voltage = velocity v")
    save_schem(d, f"{OUT}/analogues.svg")


def fig_motor_circuit():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += (src := elm.SourceV().up().label("$v_a$", loc="left"))
    d += elm.Resistor().right().label("$R$", loc="top")
    d += elm.Inductor().right().label("$L$", loc="top").label("$i$ →", loc="bottom")
    d += elm.SourceV().down().reverse().label("$e_b = K_e\\omega$", loc="right")
    d += elm.Line().left().tox(src.start)
    d += elm.Label().at((3.0, -1.1)).label("torque on the rotor: $\\tau_{em} = K_t i$;  $J\\dot\\omega = K_t i - b\\omega - \\tau_L$")
    save_schem(d, f"{OUT}/motor-circuit.svg")


def fig_thermal_network():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    d += (p := elm.SourceI().up())
    d += elm.Line().right().length(2.5)
    d += (j := elm.Dot())
    d += elm.Capacitor().down()
    d += elm.Resistor().at(j.center).right().length(4.5).label("$R_{JC}$ = 0.15 K/W", loc="top", ofst=0.25)
    d += (c := elm.Dot())
    d += elm.Capacitor().down()
    d += elm.Resistor().at(c.center).right().length(4.5).label("$R_{CA}$ = 0.35 K/W", loc="top", ofst=0.25)
    d += elm.SourceV().down().reverse()
    d += elm.Line().left().tox(p.start)
    d += elm.Ground().at(p.start)
    x0, y0 = p.start
    for txt, dx, dy in (("$P$", -1.0, 1.5), ("$T_J$", 2.3, 3.55), ("$C_J$ = 5 J/K", 3.9, 1.5), ("$T_C$", 6.8, 3.55),
                        ("$C_H$ = 300 J/K", 8.6, 1.5), ("$T_A$ = 30 °C", 13.1, 1.5)):
        d += elm.Label().at((x0 + dx, y0 + dy)).label(txt)
    d += elm.Label().at((x0 + 6.0, y0 - 1.4)).label("heat flow ↔ current, temperature ↔ voltage (ground = 0 °C reference)")
    save_schem(d, f"{OUT}/thermal-network.svg")


if __name__ == "__main__":
    fig_thermal()
    fig_analogues()
    fig_motor_circuit()
    fig_thermal_network()
