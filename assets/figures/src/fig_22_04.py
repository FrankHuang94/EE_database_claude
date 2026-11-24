#!/usr/bin/env python3
"""Figures for chapter 22-04 (isolated converters).

Run from anywhere:  python assets/figures/src/fig_22_04.py
Outputs
  assets/figures/22-04/flyback.svg   (a) a flyback converter: primary switched from the bus, coupled secondary with
                                     diode and output capacitor; (b) the transformer model: ideal transformer with
                                     magnetizing inductance across the primary and series leakage inductance
The schematics use schemdraw.
"""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

OUT = Path(__file__).resolve().parents[3] / "assets/figures/22-04"
OUT.mkdir(parents=True, exist_ok=True)


def _winding(d, x, y_top, y_bot, up=False):
    """A coupled-inductor winding drawn vertically between y_top and y_bot at x."""
    if up:
        d += elm.Inductor2(loops=3).at((x, y_bot)).to((x, y_top))
    else:
        d += elm.Inductor2(loops=3).at((x, y_top)).to((x, y_bot))


def _core(d, x, y_top, y_bot):
    for dx in (-0.1, 0.1):
        d += elm.Line().at((x + dx, y_top)).to((x + dx, y_bot)).color("gray")


def draw():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    # (a) flyback, primary on the left, isolated secondary on the right
    d += elm.Label().at((3.0, 4.2)).label("(a) flyback converter")
    d += elm.Dot().at((0, 3)).label("$V_{in}$", loc="left")
    d += elm.Line().at((0, 3)).to((1.5, 3))
    _winding(d, 1.5, 3, 1)
    d += elm.Label().at((1.0, 2.0)).label("$N_1$")
    d += elm.Dot(radius=0.07).at((1.25, 2.85))          # dot at the primary's top
    d += elm.Dot().at((1.5, 1)).label("drain", loc="left")
    d += elm.Switch().at((1.5, 1)).to((1.5, -0.6)).label("S", loc="bottom")
    d += elm.Ground().at((1.5, -0.6))
    _core(d, 2.2, 3, 1)
    _winding(d, 2.9, 3, 1, up=True)
    d += elm.Label().at((3.6, 2.0)).label("$N_2$")
    d += elm.Dot(radius=0.07).at((3.15, 1.15))          # dot at the secondary's bottom: opposite polarity
    d += elm.Diode().at((2.9, 3)).to((4.9, 3)).label("D", loc="top")
    d += elm.Dot().at((4.9, 3)).label("$V$", loc="top")
    d += elm.Capacitor().at((4.9, 3)).to((4.9, 1)).label("$C$", loc="bottom")
    d += elm.Line().at((4.9, 3)).to((6.1, 3))
    d += elm.Resistor().at((6.1, 3)).to((6.1, 1)).label("$R$", loc="bottom")
    d += elm.Line().at((2.9, 1)).to((6.1, 1))
    d += elm.GroundChassis().at((4.9, 1))
    d += elm.Label().at((3.0, -1.9)).label("$V = (V_{in}/n)\\,D/(1-D)$, $n = N_1/N_2$")
    d += elm.Label().at((3.0, -2.5)).label("dots mark opposite polarity; the two grounds are isolated")
    # (b) transformer model referred to the primary
    x = 8.8
    d += elm.Label().at((x + 2.9, 4.2)).label("(b) transformer model")
    d += elm.Dot().at((x, 3)).label("primary", loc="left")
    d += elm.Inductor().at((x, 3)).to((x + 2, 3)).label("$L_{lk}$", loc="top")
    d += elm.Dot().at((x + 2, 3))
    d += elm.Inductor().at((x + 2, 3)).to((x + 2, 1)).label("$L_m$", loc="bottom")
    d += elm.Dot().at((x + 2, 1))
    d += elm.Line().at((x, 1)).to((x + 3.4, 1))
    d += elm.Dot().at((x, 1))
    d += elm.Line().at((x + 2, 3)).to((x + 3.4, 3))
    _winding(d, x + 3.4, 3, 1)
    _core(d, x + 4.1, 3, 1)
    _winding(d, x + 4.8, 3, 1, up=True)
    d += elm.Label().at((x + 4.1, 3.5)).label("ideal  $n$ : 1")
    d += elm.Line().at((x + 4.8, 3)).to((x + 5.8, 3))
    d += elm.Dot().at((x + 5.8, 3)).label("secondary", loc="right")
    d += elm.Line().at((x + 4.8, 1)).to((x + 5.8, 1))
    d += elm.Dot().at((x + 5.8, 1))
    d += elm.Label().at((x + 2.9, 0.2)).label("$L_m$ stores the flyback's energy")
    d += elm.Label().at((x + 2.9, -0.4)).label("the clamp must absorb $L_{lk}$'s energy")
    d.save(str(OUT / "flyback.svg"))


if __name__ == "__main__":
    draw()
