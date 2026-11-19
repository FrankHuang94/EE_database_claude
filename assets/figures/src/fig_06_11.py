#!/usr/bin/env python3
"""Figures for chapter 06-11 (practical DC circuits and measurement).

Run from anywhere:  python assets/figures/src/fig_06_11.py
Outputs SVGs to assets/figures/06-11/. All figures are schematics drawn with schemdraw.
"""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets/figures/06-11"
OUT.mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(OUT / name))


def sch_meters(d):
    """Left: voltmeter (R_in) across a Thevenin source. Right: ammeter (R_A) in series."""
    # voltmeter
    d += (vs := elm.SourceV().up().at((0, 0)).label("$V_{th}$"))
    d += elm.Resistor().right().label("$R_{th}$")
    d += elm.Dot()
    d += elm.Line().right().length(1.0)
    d += (rin := elm.Resistor().down().label("$R_{in}$", loc="bottom"))
    d += elm.Line().left().tox(vs.start)
    d += elm.Rect(corner1=(3.6, -0.5), corner2=(5.4, 3.5)).at((0, 0)).theta(0).linestyle("--")
    d += elm.Label().at((4.5, 3.85)).label("voltmeter", fontsize=11)
    d += elm.Label().at((2.6, -1.3)).label("reads $V_{th}\\,R_{in}/(R_{th} + R_{in})$", fontsize=11)
    # ammeter
    x0 = 9.0
    d += (vs2 := elm.SourceV().up().at((x0, 0)).label("$V_{th}$"))
    d += elm.Resistor().right().label("$R_{th}$")
    d += elm.Line().right().length(0.5)
    d += elm.Resistor().right().label("$R_A$")
    d += elm.Line().down().length(3.0)
    d += elm.Line().left().tox(vs2.start)
    d += elm.Rect(corner1=(x0 + 3.4, 2.3), corner2=(x0 + 6.6, 3.9)).at((0, 0)).theta(0).linestyle("--")
    d += elm.Label().at((x0 + 5.0, 4.25)).label("ammeter", fontsize=11)
    d += elm.Label().at((x0 + 3.2, -1.3)).label("reads $V_{th}/(R_{th} + R_A)$", fontsize=11)


def sch_four_wire(d):
    """Two-wire and four-wire measurement of R."""
    # two-wire: current source I through two leads, voltmeter at the meter's own terminals
    d += (src := elm.SourceI().up().at((0, 0)).label("$I$"))
    d += (t1 := elm.Dot())
    d += elm.Resistor().right().label("$R_{lead}$")
    d += elm.Resistor().down().label("$R$", loc="bottom")
    d += elm.Resistor().left().tox(src.start).label("$R_{lead}$", loc="bottom")
    d += elm.Line().at(t1.center).left().length(2.2)
    d += (vm := elm.MeterV().down().length(3.0))
    d += elm.Line().right().tox(src.start)
    d += elm.Label().at((0.8, -1.4)).label("two-wire: reads $R + 2R_{lead}$", fontsize=11)
    # four-wire: force leads carry I, sense leads at R's own terminals go to a voltmeter
    x0 = 8.5
    d += (src2 := elm.SourceI().up().at((x0, 0)).label("$I$"))
    d += elm.Resistor().right().label("force", loc="top")
    d += (a := elm.Dot())
    d += (r := elm.Resistor().down().label("$R$"))
    d += (b := elm.Dot())
    d += elm.Resistor().left().tox(src2.start).label("force", loc="bottom")
    d += elm.Resistor().at(a.center).right().label("sense", loc="top")
    d += elm.Line().right().length(0.6)
    d += (vm2 := elm.MeterV().down().length(3.0))
    d += elm.Line().left().length(0.6)
    d += elm.Resistor().left().tox(b.center).label("sense", loc="bottom")
    d += elm.Label().at((x0 + 4.0, -1.4)).label("four-wire: sense leads carry almost no current", fontsize=11)


def sch_remote_sense(d):
    """Supply with force and sense connections to a load."""
    d += (sup := elm.Rect(corner1=(-1.8, -0.5), corner2=(2.4, 4.0)).at((0, 0)))
    d += elm.Label().at((-0.6, 1.75)).label("supply\nregulates\nS+ − S−", fontsize=11)
    # force +
    d += elm.Dot().at((2.4, 3.5)).label("OUT+", loc="left", fontsize=10)
    d += elm.Resistor().right().at((2.4, 3.5)).length(4.0).label("$R_{w+}$")
    d += (lp := elm.Dot())
    # sense +
    d += elm.Dot().at((2.4, 2.5)).label("S+", loc="left", fontsize=10)
    d += elm.Line().right().at((2.4, 2.5)).length(3.2).linestyle("--")
    d += elm.Line().up().length(1.0).linestyle("--")
    d += elm.Line().right().tox(lp.center).linestyle("--")
    # load
    d += elm.Line().right().at(lp.center).length(1.0)
    d += (ld := elm.SourceI().down().length(3.0).label("load $I$"))
    d += elm.Line().left().length(1.0)
    d += (ln := elm.Dot())
    # force -
    d += elm.Resistor().left().tox(2.4).label("$R_{w-}$", loc="bottom")
    d += elm.Dot().label("OUT−", loc="left", fontsize=10)
    # sense -
    d += elm.Dot().at((2.4, 1.5)).label("S−", loc="left", fontsize=10)
    d += elm.Line().right().at((2.4, 1.5)).length(3.2).linestyle("--")
    d += elm.Line().down().length(1.0).linestyle("--")
    d += elm.Line().right().tox(ln.center).linestyle("--")
    d += elm.Label().at((3.4, -1.3)).label("dashed: sense wires (almost no current); solid: force wires carry $I$", fontsize=11)


if __name__ == "__main__":
    schematic("meter-models.svg", sch_meters)
    schematic("four-wire.svg", sch_four_wire)
    schematic("remote-sense.svg", sch_remote_sense)
    print("06-11 figures written to", OUT.relative_to(ROOT))
