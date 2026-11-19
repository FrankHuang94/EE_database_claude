#!/usr/bin/env python3
"""Figures for chapter 08-02 (Boolean algebra and logic gates).

Run from anywhere:  python assets/figures/src/fig_08_02.py
Outputs SVGs to assets/figures/08-02/: the standard gate symbols with their truth tables, and static CMOS
NAND2 and NOR2 gates at transistor level. Both are drawn with schemdraw; the truth tables are computed.
"""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm
import schemdraw.logic as logic

ROOT = Path(__file__).resolve().parents[3]
OUT = "assets/figures/08-02"

FUNCS = {
    "AND": lambda a, b: a & b, "OR": lambda a, b: a | b, "NAND": lambda a, b: 1 - (a & b),
    "NOR": lambda a, b: 1 - (a | b), "XOR": lambda a, b: a ^ b, "XNOR": lambda a, b: 1 - (a ^ b),
}


def save_schem(d, rel):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(path))
    print(f"wrote {rel}")


def table_text(f):
    lines = ["A B | Y"]
    for a in (0, 1):
        for b in (0, 1):
            lines.append(f"{a} {b} | {f(a, b)}")
    return "\n".join(lines)


def fig_gates():
    schemdraw.config(fontsize=11, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    elems = [("NOT", logic.Not, None), ("BUF", logic.Buf, None)] + [
        (name, getattr(logic, name.capitalize()), f) for name, f in FUNCS.items()]
    for k, (name, cls, f) in enumerate(elems):
        col, row = k % 4, k // 4
        x, y = col * 4.6, -row * 4.2
        g = cls().at((x, y)).anchor("in1")
        d += g
        d += elm.Label().at((x + 1.2, y + 1.1)).label(name, fontsize=12)
        if f is None:
            txt = "A | Y\n0 | " + ("1" if name == "NOT" else "0") + "\n1 | " + ("0" if name == "NOT" else "1")
        else:
            txt = table_text(f)
        d += elm.Label().at((x + 1.2, y - 1.9)).label(txt, fontsize=9, font="monospace")
    return save_schem(d, f"{OUT}/gate-symbols.svg")


def fet(d, cls, top, gate_left, label):
    """A vertical FET whose top terminal (nMOS drain, pMOS source) sits at `top`; returns the element."""
    e = cls(bulk=False).at(top).right()
    if gate_left:
        e = e.reverse()
    d += e
    gx, gy = e.gate
    d += elm.Label().at((gx - 0.35 if gate_left else gx + 0.35, gy)).label(label)
    return e


def fig_cmos():
    schemdraw.config(fontsize=12, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    # ---------------- NAND2: two pMOS in parallel on top, two nMOS in series below
    d += elm.Line().at((-1.5, 6)).to((1.5, 6))
    d += elm.Vdd().at((0, 6)).label("$V_{DD}$")
    pa = fet(d, elm.PFet, (-1.5, 6), True, "A")
    pb = fet(d, elm.PFet, (1.5, 6), False, "B")
    d += elm.Line().at(pa.drain).to(pb.drain)
    d += elm.Dot().at((0, pa.drain[1]))
    d += elm.Line().at((0, pa.drain[1])).to((0, 3.8))
    na = fet(d, elm.NFet, (0, 3.8), True, "A")
    nb = fet(d, elm.NFet, na.source, True, "B")
    d += elm.Ground().at(nb.source)
    d += elm.Line().at(pb.drain).to((3.4, pb.drain[1]))
    d += elm.Dot(open=True).at((3.4, pb.drain[1])).label("$Y = \\overline{AB}$", loc="right")
    d += elm.Label().at((0.6, -0.6)).label("NAND2: pMOS in parallel, nMOS in series", fontsize=11)
    # ---------------- NOR2: two pMOS in series on top, two nMOS in parallel below
    x0 = 9.5
    d += elm.Vdd().at((x0, 6)).label("$V_{DD}$")
    qa = fet(d, elm.PFet, (x0, 6), True, "A")
    qb = fet(d, elm.PFet, qa.drain, True, "B")
    out = qb.drain
    d += elm.Dot().at(out)
    d += elm.Line().at(out).to((x0, out[1] - 0.4))
    d += elm.Line().at((x0 - 1.5, out[1] - 0.4)).to((x0 + 1.5, out[1] - 0.4))
    ma = fet(d, elm.NFet, (x0 - 1.5, out[1] - 0.4), True, "A")
    mb = fet(d, elm.NFet, (x0 + 1.5, out[1] - 0.4), False, "B")
    d += elm.Line().at(ma.source).to(mb.source)
    d += elm.Ground().at((x0, ma.source[1]))
    d += elm.Line().at(out).to((x0 + 3.4, out[1]))
    d += elm.Dot(open=True).at((x0 + 3.4, out[1])).label("$Y = \\overline{A + B}$", loc="right")
    d += elm.Label().at((x0 + 0.6, -0.6)).label("NOR2: pMOS in series, nMOS in parallel", fontsize=11)
    return save_schem(d, f"{OUT}/cmos-nand-nor.svg")


if __name__ == "__main__":
    fig_gates()
    fig_cmos()
