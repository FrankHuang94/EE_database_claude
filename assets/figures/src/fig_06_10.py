#!/usr/bin/env python3
"""Figures for chapter 06-10 (the ideal op-amp).

Run from anywhere:  python assets/figures/src/fig_06_10.py
Outputs SVGs to assets/figures/06-10/. All figures are schematics drawn with schemdraw.
"""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets/figures/06-10"
OUT.mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(OUT / name))


def inverting(d, x0, y0, title):
    d += (op := elm.Opamp(leads=True).right().at((x0 + 3.0, y0)).anchor("in1"))
    d += elm.Line().left().at(op.in1).length(0.5)
    d += (n := elm.Dot())
    d += elm.Resistor().left().length(2.2).label("$R_1$")
    d += elm.Dot(open=True).label("$v_{in}$", loc="left")
    d += elm.Line().up().at(n.center).length(1.4)
    d += elm.Resistor().right().tox(op.out).label("$R_2$")
    d += elm.Line().down().toy(op.out)
    d += elm.Dot()
    d += elm.Line().right().at(op.out).length(0.6)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Line().left().at(op.in2).length(0.5)
    d += elm.Ground()
    d += elm.Label().at((x0 + 2.5, y0 - 2.6)).label(title, fontsize=11)


def noninverting(d, x0, y0, title):
    d += (op := elm.Opamp(leads=True).right().at((x0 + 3.5, y0)).anchor("in2"))
    d += elm.Line().left().at(op.in2).length(1.0)
    d += elm.Dot(open=True).label("$v_{in}$", loc="left")
    d += elm.Line().left().at(op.in1).length(0.5)
    d += (n := elm.Dot())
    d += elm.Resistor().left().length(2.4).label("$R_1$")
    d += elm.Ground()
    d += elm.Line().up().at(n.center).length(1.4)
    d += elm.Resistor().right().tox(op.out).label("$R_2$")
    d += elm.Line().down().toy(op.out)
    d += elm.Dot()
    d += elm.Line().right().at(op.out).length(0.6)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Label().at((x0 + 3.0, y0 - 2.6)).label(title, fontsize=11)


def follower(d, x0, y0, title):
    d += (op := elm.Opamp(leads=True).right().at((x0 + 2.0, y0)).anchor("in2"))
    d += elm.Line().left().at(op.in2).length(1.0)
    d += elm.Dot(open=True).label("$v_{in}$", loc="left")
    d += elm.Line().left().at(op.in1).length(0.5)
    d += elm.Line().up().length(1.4)
    d += elm.Line().right().tox(op.out)
    d += elm.Line().down().toy(op.out)
    d += elm.Dot()
    d += elm.Line().right().at(op.out).length(0.6)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Label().at((x0 + 2.0, y0 - 2.6)).label(title, fontsize=11)


def sch_basic(d):
    inverting(d, 0.0, 0.0, "inverting: $v_{out} = -(R_2/R_1)\\,v_{in}$")
    noninverting(d, 9.5, 0.0, "non-inverting: $v_{out} = (1 + R_2/R_1)\\,v_{in}$")
    follower(d, 19.5, 0.0, "follower: $v_{out} = v_{in}$")


def sch_difference(d):
    """Difference amplifier: R1 from v1 to the - input, R2 feedback; R3 from v2 to +, R4 to ground."""
    d += (op := elm.Opamp(leads=True).right().at((4.0, 0)).anchor("in1"))
    d += elm.Line().left().at(op.in1).length(0.5)
    d += (n := elm.Dot())
    d += elm.Resistor().left().length(2.2).label("$R_1$")
    d += elm.Dot(open=True).label("$v_1$", loc="left")
    d += elm.Line().up().at(n.center).length(1.4)
    d += elm.Resistor().right().tox(op.out).label("$R_2$")
    d += elm.Line().down().toy(op.out)
    d += elm.Dot()
    d += elm.Line().right().at(op.out).length(0.6)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Line().left().at(op.in2).length(0.5)
    d += (p := elm.Dot())
    d += elm.Resistor().left().length(2.2).label("$R_3$", loc="bottom")
    d += elm.Dot(open=True).label("$v_2$", loc="left")
    d += elm.Resistor().down().at(p.center).length(1.6).label("$R_4$", loc="bottom")
    d += elm.Ground()
    d += elm.Label().at((4.2, -3.9)).label("$v_{out} = (R_2/R_1)(v_2 - v_1)$ when $R_4/R_3 = R_2/R_1$", fontsize=11)


def sch_inamp(d):
    """Three-op-amp instrumentation amplifier."""
    d += (a1 := elm.Opamp(leads=True).right().at((2.0, 3.0)).anchor("in2"))
    d += (a2 := elm.Opamp(leads=True).right().flip().at((2.0, -3.0)).anchor("in2"))
    d += elm.Line().left().at(a1.in2).length(1.0)
    d += elm.Dot(open=True).label("$v_-$", loc="left")
    d += elm.Line().left().at(a2.in2).length(1.0)
    d += elm.Dot(open=True).label("$v_+$", loc="left")
    # feedback resistors and gain resistor between the two inverting inputs
    d += elm.Line().left().at(a1.in1).length(0.4)
    d += (j1 := elm.Dot())
    d += elm.Line().left().at(a2.in1).length(0.4)
    d += (j2 := elm.Dot())
    d += elm.Resistor().at(j1.center).to(j2.center).label("$R_G$", loc="bottom")
    d += elm.Line().up().at(j1.center).length(1.0)
    d += elm.Resistor().right().tox(a1.out).label("$R$")
    d += elm.Line().down().toy(a1.out)
    d += elm.Line().down().at(j2.center).length(1.0)
    d += elm.Resistor().right().tox(a2.out).label("$R$", loc="bottom")
    d += elm.Line().up().toy(a2.out)
    # difference stage
    d += (a3 := elm.Opamp(leads=True).right().at((10.5, 0.0)).anchor("in1"))
    d += elm.Line().right().at(a1.out).length(0.8)
    d += elm.Resistor().down().toy(a3.in1).label("$R_1$", loc="bottom")
    d += elm.Line().right().tox(a3.in1)
    d += elm.Line().right().at(a2.out).length(0.8)
    d += elm.Resistor().up().toy(a3.in2).label("$R_3$")
    d += elm.Line().right().tox(a3.in2)
    d += elm.Line().up().at((a3.in1[0] - 0.2, a3.in1[1])).length(1.5)
    d += elm.Resistor().right().tox(a3.out).label("$R_2$")
    d += elm.Line().down().toy(a3.out)
    d += elm.Resistor().down().at((a3.in2[0] - 0.2, a3.in2[1])).length(1.5).label("$R_4$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().right().at(a3.out).length(0.6)
    d += elm.Dot(open=True).label("$v_{out}$", loc="right")
    d += elm.Label().at((7.5, -6.6)).label("$v_{out} = (1 + 2R/R_G)(R_2/R_1)(v_+ - v_-)$", fontsize=11)


if __name__ == "__main__":
    schematic("basic-configurations.svg", sch_basic)
    schematic("difference-amplifier.svg", sch_difference)
    schematic("instrumentation-amplifier.svg", sch_inamp)
    print("06-10 figures written to", OUT.relative_to(ROOT))
