#!/usr/bin/env python3
"""Figures for chapter 06-06 (dependent sources).

Run from anywhere:  python assets/figures/src/fig_06_06.py
Outputs SVGs to assets/figures/06-06/. All figures are schematics drawn with schemdraw.
"""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets/figures/06-06"
OUT.mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(OUT / name))


def sch_four_sources(d):
    """The four dependent sources, each between two terminals, with its law."""
    items = [("VCVS", elm.SourceControlledV, "$v = \\mu\\, v_x$"),
             ("VCCS", elm.SourceControlledI, "$i = g\\, v_x$"),
             ("CCVS", elm.SourceControlledV, "$v = r\\, i_x$"),
             ("CCCS", elm.SourceControlledI, "$i = \\beta\\, i_x$")]
    for k, (name, cls, law) in enumerate(items):
        x = 3.2 * k
        d += elm.Dot(open=True).at((x, 0))
        d += cls().up().at((x, 0)).length(3).label(law, loc="bottom", ofst=0.25)
        d += elm.Dot(open=True)
        d += elm.Label().at((x, 3.8)).label(name, fontsize=13)


def sch_ex1(d):
    """Example 06-06.1: 1 mA into node 1, 2 kOhm to ground, 4 kOhm to node 2, 4 kOhm and a VCCS g*v1 from node 2 to ground."""
    d += (i1 := elm.SourceI().up().length(3).label("1 mA"))
    d += elm.Line().right().length(2.0)
    d += (n1 := elm.Dot().label("$v_1$", loc="top"))
    d += elm.Resistor().down().length(3).label("2 kΩ", loc="bottom")
    d += (g1 := elm.Dot())
    d += elm.Line().left().tox(i1.start)
    d += elm.Resistor().right().at(n1.center).length(3.5).label("4 kΩ")
    d += (n2 := elm.Dot().label("$v_2$", loc="top"))
    d += elm.Resistor().down().length(3).label("4 kΩ", loc="bottom")
    d += (g2 := elm.Dot())
    d += elm.Line().left().tox(g1.center)
    d += elm.Line().right().at(n2.center).length(2.5)
    d += elm.SourceControlledI().down().length(3).label("$g\\,v_1$\n$g$ = 1 mS", loc="bottom")
    d += elm.Line().left().tox(g2.center)
    d += elm.Ground().at(g1.center)


def sch_models(d):
    """Small-signal models: MOSFET (VCCS g_m v_gs with r_o) and BJT (r_pi, CCCS beta i_b)."""
    # MOSFET: gate open (no gate current), v_gs marked between G and S
    d += elm.Dot(open=True).at((0, 3)).label("G", loc="left")
    d += elm.Dot(open=True).at((0, 0)).label("S", loc="left")
    d += elm.Gap().at((0, 0)).to((0, 3)).label(["−", "$v_{gs}$", "+"])
    d += elm.Line().at((0, 0)).right().length(4.4)
    d += elm.SourceControlledI().at((2.2, 0)).up().length(3).reverse().label("$g_m v_{gs}$", loc="top")
    d += elm.Resistor().at((4.4, 0)).up().length(3).label("$r_o$", loc="bottom")
    d += elm.Line().at((2.2, 3)).right().length(2.2)
    d += elm.Line().at((4.4, 3)).right().length(0.8)
    d += elm.Dot(open=True).label("D", loc="right")
    d += elm.Label().at((2.6, -0.9)).label("MOSFET", fontsize=12)
    # BJT: base current i_b flows through r_pi; collector current beta*i_b
    x0 = 8.5
    d += elm.Dot(open=True).at((x0, 3)).label("B", loc="left")
    d += elm.Resistor().at((x0, 3)).down().length(3).label("$r_\\pi$", loc="bottom")
    d += elm.Label().at((x0 - 0.75, 2.2)).label("$i_b\\downarrow$", fontsize=12)
    d += elm.Dot(open=True).at((x0, 0)).label("E", loc="left")
    d += elm.Line().at((x0, 0)).right().length(2.4)
    d += elm.SourceControlledI().at((x0 + 2.4, 0)).up().length(3).reverse().label("$\\beta\\, i_b$", loc="bottom")
    d += elm.Line().at((x0 + 2.4, 3)).right().length(0.8)
    d += elm.Dot(open=True).label("C", loc="right")
    d += elm.Label().at((x0 + 1.2, -0.9)).label("BJT", fontsize=12)


def sch_opamp(d):
    """Example 06-06.5: op-amp as a VCVS with R_id and R_o in a non-inverting amplifier."""
    d += elm.Dot(open=True).at((-2.0, 0)).label("$v_s$", loc="left")
    d += elm.Line().right().length(2.0)
    d += (p := elm.Dot().label("$v_+$", loc="bottom"))
    d += elm.Resistor().up().length(2.5).label("$R_{id}$ = 1 MΩ", loc="bottom")
    d += (n := elm.Dot().label("$v_-$", loc="top"))
    d += elm.Resistor().left().length(2.5).label("$R_1$ = 1 kΩ")
    d += elm.Line().down().length(0.8)
    d += elm.Ground()
    d += elm.Resistor().right().at(n.center).length(4.0).label("$R_2$ = 9 kΩ")
    d += (out := elm.Dot().label("$v_{out}$", loc="top"))
    d += elm.Resistor().down().length(3.0).label("$R_L$\n2 kΩ", loc="bottom")
    d += elm.Ground()
    d += elm.Resistor().right().at(out.center).length(3.0).label("$R_o$ = 100 Ω")
    d += (x := elm.Dot())
    d += elm.SourceControlledV().down().length(3.0).reverse().label("$A(v_+ - v_-)$\n$A = 10^5$", loc="bottom")   # + at the top
    d += elm.Ground()
    del p, x


if __name__ == "__main__":
    schematic("four-dependent-sources.svg", sch_four_sources)
    schematic("vccs-example.svg", sch_ex1)
    schematic("small-signal-models.svg", sch_models)
    schematic("opamp-vcvs-model.svg", sch_opamp)
    print("06-06 figures written to", OUT.relative_to(ROOT))
