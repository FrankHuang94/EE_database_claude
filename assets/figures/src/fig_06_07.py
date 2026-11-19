#!/usr/bin/env python3
"""Figures for chapter 06-07 (linearity and superposition).

Run from anywhere:  python assets/figures/src/fig_06_07.py
Outputs SVGs to assets/figures/06-07/. All figures are schematics drawn with schemdraw.
"""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "assets/figures/06-07"
OUT.mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(OUT / name))


def one_circuit(d, x0, vsrc, isrc, title):
    """12 V (or short) - 4 ohm - node a - 6 ohm to ground, with 2 A (or open) into a."""
    if vsrc:
        d += (v := elm.SourceV().up().at((x0, 0)).length(3).label("12 V"))
    else:
        d += (v := elm.Line().up().at((x0, 0)).length(3))
        d += elm.Label().at((x0 + 0.55, 1.5)).label("short", fontsize=10)
    d += elm.Resistor().right().length(2.5).label("$R_1$ = 4 Ω")
    d += (a := elm.Dot().label("a", loc="top"))
    d += elm.Resistor().down().length(3).label("$R_2$\n6 Ω", loc="bottom")
    d += elm.Line().left().tox(v.start)
    d += elm.Line().right().at(a.center).length(2.0)
    if isrc:
        d += elm.SourceI().down().length(3).reverse().label("2 A", loc="bottom")
    else:
        d += elm.Gap().down().length(3).label(["", "open", ""], loc="bottom")
    d += elm.Line().left().length(2.0)
    d += elm.Label().at((x0 + 2.25, -1.0)).label(title, fontsize=12)


def sch_superposition(d):
    one_circuit(d, 0.0, True, True, "both sources: $v_a$ = 12 V")
    one_circuit(d, 8.5, True, False, "12 V alone: $v_a'$ = 7.2 V")
    one_circuit(d, 17.0, False, True, "2 A alone: $v_a''$ = 4.8 V")
    d += elm.Label().at((6.9, 1.5)).label("=", fontsize=22)
    d += elm.Label().at((15.4, 1.5)).label("+", fontsize=22)


def sch_ladder(d):
    """Example 06-07.4: three sections of 1 kOhm series and 1 kOhm shunt, with unit-output currents and voltages."""
    d += (v := elm.SourceV().up().length(3).label("$v_{in}$ = 13 V"))
    nodes = []
    labels = [("8 mA", "5 V"), ("3 mA", "2 V"), ("1 mA", "1 V")]
    for k, (cur, volt) in enumerate(labels):
        d += elm.Resistor().right().length(3.2).label("1 kΩ", fontsize=11).label(f"→ {cur}", loc="bottom", fontsize=11)
        d += (n := elm.Dot())
        d += elm.Label().at((n.center[0] + 0.15, n.center[1] + 0.45)).label(volt, fontsize=12, halign="left")
        nodes.append(n)
    shunt_i = ["5 mA", "2 mA", "1 mA"]
    for n, si in zip(nodes, shunt_i):
        d += elm.Resistor().down().at(n.center).length(3).label(f"1 kΩ\n{si}", loc="bottom", fontsize=11)
    d += elm.Line().at((nodes[-1].center[0], 0)).tox(v.start)
    d += elm.Label().at((nodes[-1].center[0] + 0.9, 3.0)).label("$v_{out}$", fontsize=12)


def sch_dac(d):
    """Example 06-07.5: 3-bit binary-weighted DAC: bit lines (0 or 4 V) through 1k, 2k, 4k into a 4k load."""
    xs = [0.0, 2.5, 5.0]
    for x, r, name in zip(xs, ("1 kΩ", "2 kΩ", "4 kΩ"), ("$b_2$ (MSB)", "$b_1$", "$b_0$ (LSB)")):
        d += elm.Dot(open=True).at((x, 5.0)).label(f"{name}\n0 or 4 V", loc="top", fontsize=11)
        d += elm.Resistor().down().at((x, 5.0)).length(2.5).label(r, loc="bottom")
    d += elm.Line().at((0.0, 2.5)).right().length(7.5)
    d += (o := elm.Dot().label("$v_o$", loc="right"))
    d += elm.Resistor().down().at((7.5, 2.5)).length(2.5).label("$R_L$\n4 kΩ", loc="bottom")
    d += elm.Ground()
    del o


if __name__ == "__main__":
    schematic("superposition-split.svg", sch_superposition)
    schematic("unit-output-ladder.svg", sch_ladder)
    schematic("binary-weighted-dac.svg", sch_dac)
    print("06-07 figures written to", OUT.relative_to(ROOT))
