#!/usr/bin/env python3
"""Figures for chapter 06-03 (Kirchhoff's laws, series/parallel and dividers).

Run from anywhere:  python assets/figures/src/fig_06_03.py
Outputs SVGs to assets/figures/06-03/. All five figures are schematics drawn with schemdraw.
"""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets/figures/06-03"
OUT.mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(OUT / name))


def sch_series_parallel(d):
    # series: source, R1, R2 in one loop
    d += (v := elm.SourceV().up().label("$v$"))
    d += elm.Resistor().right().label("$R_1$").label("$v_1$", loc="bottom", fontsize=11)
    d += elm.Resistor().down().label("$R_2$", loc="bottom").label("$v_2$", loc="top", fontsize=11)
    d += elm.Line().left().tox(v.start)
    d += elm.Label().at((1.5, -1.3)).label("series: one current $i$", fontsize=11)
    # parallel: source with R1 and R2 across it
    d += (v2 := elm.SourceV().up().at((7.0, 0)).label("$v$"))
    d += elm.Line().right().length(1.5)
    d += (n1 := elm.Dot())
    d += elm.Resistor().down().label("$R_1$\n$i_1$", loc="bottom")
    d += (n2 := elm.Dot())
    d += elm.Line().left().tox(v2.start)
    d += elm.Line().right().at(n1.center).length(2.0)
    d += elm.Resistor().down().label("$R_2$\n$i_2$", loc="bottom")
    d += elm.Line().left().tox(n2.center)
    d += elm.Label().at((9.2, -1.3)).label("parallel: one voltage $v$", fontsize=11)


def sch_example2(d):
    d += (v := elm.SourceV().up().label("24 V"))
    d += elm.Resistor().right().label("$R_1$ = 4 Ω")
    d += (p := elm.Dot())
    d += elm.Resistor().down().label("$R_2$ = 12 Ω", loc="bottom")
    d += (q := elm.Dot())
    d += elm.Line().left().tox(v.start)
    d += elm.Line().right().at(p.center).length(2.5)
    d += elm.Resistor().down().length(1.5).label("$R_3$ = 2 Ω", loc="bottom")
    d += elm.Resistor().down().length(1.5).label("$R_4$ = 4 Ω", loc="bottom")
    d += elm.Line().left().tox(q.center)


def sch_wheatstone(d):
    d += (v := elm.SourceV().up().length(4).label("$V$"))
    d += elm.Line().right().length(2)
    d += (top := elm.Dot())
    d += elm.Resistor().down().length(2).label("$R_1$", loc="bottom")
    d += (a := elm.Dot().label("A", loc="left"))
    d += elm.Resistor().down().length(2).label("$R_2$", loc="bottom")
    d += (bot := elm.Dot())
    d += elm.Line().left().tox(v.start)
    d += elm.Line().right().at(top.center).length(3)
    d += elm.Resistor().down().length(2).label("$R_3$", loc="bottom")
    d += (b := elm.Dot().label("B", loc="right"))
    d += elm.Resistor().down().length(2).label("$R_4$", loc="bottom")
    d += elm.Line().left().tox(bot.center)
    d += elm.Gap().at(a.center).to(b.center).label(["+", "$v_{out}$", "−"])


def sch_delta_wye(d):
    # delta: triangle a (top), b (bottom left), c (bottom right)
    a, b, c = (1.5, 2.6), (0.0, 0.0), (3.0, 0.0)
    d += elm.Resistor().endpoints(a, b).label("$R_{ab}$", loc="top")
    d += elm.Resistor().endpoints(b, c).label("$R_{bc}$", loc="bottom")
    d += elm.Resistor().endpoints(c, a).label("$R_{ca}$", loc="top")
    for pt, name, loc in ((a, "a", "top"), (b, "b", "left"), (c, "c", "right")):
        d += elm.Dot(open=True).at(pt).label(name, loc=loc)
    # wye: center n, legs to a', b', c'
    n = (8.0, 1.0)
    a2, b2, c2 = (8.0, 3.4), (6.0, -0.6), (10.0, -0.6)
    d += elm.Resistor().endpoints(a2, n).label("$R_a$", loc="bottom")
    d += elm.Resistor().endpoints(n, b2).label("$R_b$", loc="top")
    d += elm.Resistor().endpoints(n, c2).label("$R_c$", loc="bottom")
    d += elm.Dot().at(n)
    for pt, name, loc in ((a2, "a", "top"), (b2, "b", "left"), (c2, "c", "right")):
        d += elm.Dot(open=True).at(pt).label(name, loc=loc)
    d += elm.Label().at((4.6, 1.2)).label("⇔", fontsize=22)


def sch_bridge_network(d):
    d += (v := elm.SourceV().up().length(4).label("10 V"))
    d += elm.Line().right().length(2.5)
    d += (a := elm.Dot().label("a", loc="top"))
    d += elm.Line().left().length(1.2)
    d += elm.Resistor().down().length(2).label("10 Ω", loc="bottom")
    d += (c := elm.Dot().label("c", loc="left"))
    d += elm.Resistor().down().length(2).label("40 Ω", loc="bottom")
    d += (bl := elm.Dot())
    d += elm.Line().right().at(a.center).length(1.2)
    d += elm.Resistor().down().length(2).label("20 Ω", loc="bottom")
    d += (dd := elm.Dot().label("d", loc="right"))
    d += elm.Resistor().down().length(2).label("50 Ω", loc="bottom")
    d += (br := elm.Dot())
    d += elm.Resistor().at(c.center).to(dd.center).label("30 Ω", loc="top")
    d += elm.Line().at(br.center).to(bl.center)
    d += elm.Line().left().at(bl.center).tox(v.start)
    d += elm.Label().at((2.5, -0.4)).label("b", fontsize=12)


if __name__ == "__main__":
    schematic("series-parallel.svg", sch_series_parallel)
    schematic("series-parallel-example.svg", sch_example2)
    schematic("wheatstone-bridge.svg", sch_wheatstone)
    schematic("delta-wye.svg", sch_delta_wye)
    schematic("bridge-network.svg", sch_bridge_network)
    print("06-03 figures written to", OUT.relative_to(ROOT))
