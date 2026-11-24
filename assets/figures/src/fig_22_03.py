#!/usr/bin/env python3
"""Figures for chapter 22-03 (boost, buck-boost and other topologies).

Run from anywhere:  python assets/figures/src/fig_22_03.py
Outputs
  assets/figures/22-03/topologies.svg   (a) boost, (b) inverting buck-boost and (c) SEPIC drawn with the same
                                        parts (switch S, diode D, inductors L, capacitors C, load R)
The schematics use schemdraw.
"""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets/figures/22-03"
OUT.mkdir(parents=True, exist_ok=True)


def draw():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    # ---------------- (a) boost
    d += elm.Label().at((3.2, 3.6)).label("(a) boost: V = V_in/(1 − D)")
    d += elm.Dot().at((0, 2)).label("$V_{in}$", loc="left")
    d += elm.Inductor().right().length(2.0).label("$L$", loc="top")
    d += (n := elm.Dot())
    d += elm.Switch().down().length(2.0).label("S", loc="bottom")
    d += elm.Ground()
    d += elm.Diode().at(n.center).right().length(2.0).label("D", loc="top")
    d += (o := elm.Dot().label("$V$", loc="top"))
    d += elm.Capacitor().down().length(2.0).label("$C$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().at(o.center).right().length(1.2)
    d += elm.Resistor().down().length(2.0).label("$R$", loc="bottom")
    d += elm.Ground()
    # ---------------- (b) inverting buck-boost
    x = 9.0
    d += elm.Label().at((x + 3.2, 3.6)).label("(b) buck-boost: V = −D·V_in/(1 − D)")
    d += elm.Dot().at((x, 2)).label("$V_{in}$", loc="left")
    d += elm.Switch().right().length(2.0).label("S", loc="top")
    d += (n2 := elm.Dot())
    d += elm.Inductor().down().length(2.0).label("$L$", loc="bottom")
    d += elm.Ground()
    d += elm.Diode().at(n2.center).right().length(2.0).reverse().label("D", loc="top")
    d += (o2 := elm.Dot().label("$V$ < 0", loc="top"))
    d += elm.Capacitor().down().length(2.0).label("$C$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().at(o2.center).right().length(1.2)
    d += elm.Resistor().down().length(2.0).label("$R$", loc="bottom")
    d += elm.Ground()
    # ---------------- (c) SEPIC
    y = -3.6
    d += elm.Label().at((5.2, y + 1.6)).label("(c) SEPIC: V = D·V_in/(1 − D)")
    d += elm.Dot().at((0, y)).label("$V_{in}$", loc="left")
    d += elm.Inductor().right().length(2.0).label("$L_1$", loc="top")
    d += (a := elm.Dot())
    d += elm.Switch().down().length(2.0).label("S", loc="bottom")
    d += elm.Ground()
    d += elm.Capacitor().at(a.center).right().length(2.0).label("$C_1$", loc="top")
    d += (b := elm.Dot())
    d += elm.Inductor().down().length(2.0).label("$L_2$", loc="bottom")
    d += elm.Ground()
    d += elm.Diode().at(b.center).right().length(2.0).label("D", loc="top")
    d += (o3 := elm.Dot().label("$V$ > 0", loc="top"))
    d += elm.Capacitor().down().length(2.0).label("$C$", loc="bottom")
    d += elm.Ground()
    d += elm.Line().at(o3.center).right().length(1.2)
    d += elm.Resistor().down().length(2.0).label("$R$", loc="bottom")
    d += elm.Ground()
    d.save(str(OUT / "topologies.svg"))


if __name__ == "__main__":
    draw()
