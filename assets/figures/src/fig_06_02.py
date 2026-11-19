#!/usr/bin/env python3
"""Figures for chapter 06-02 (circuit elements and Ohm's law).

Run from anywhere:  python assets/figures/src/fig_06_02.py
Outputs SVGs to assets/figures/06-02/. Schematics use schemdraw; plots use matplotlib.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/06-02"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(ROOT / OUT / name))


def fig_iv_characteristics():
    """Five small i-v panels: resistor, short, open, ideal voltage source, ideal current source."""
    fig, axes = plt.subplots(1, 5, figsize=(11.0, 2.6))
    v = np.linspace(-1, 1, 3)
    panels = [
        ("resistor\n$i = v/R$", lambda ax: ax.plot(v, 0.7 * v, color=B, lw=2.2)),
        ("short circuit\n$v = 0$", lambda ax: ax.plot([0, 0], [-1, 1], color=B, lw=2.2)),
        ("open circuit\n$i = 0$", lambda ax: ax.plot([-1, 1], [0, 0], color=B, lw=2.2)),
        ("voltage source\n$v = v_s$", lambda ax: ax.plot([0.55, 0.55], [-1, 1], color=B, lw=2.2)),
        ("current source\n$i = i_s$", lambda ax: ax.plot([-1, 1], [0.55, 0.55], color=B, lw=2.2)),
    ]
    for ax, (title, draw) in zip(axes, panels):
        ax.axhline(0, color="0.6", lw=0.8)
        ax.axvline(0, color="0.6", lw=0.8)
        draw(ax)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("$v$", fontsize=10, labelpad=2)
        ax.set_ylabel("$i$", fontsize=10, rotation=0, labelpad=8)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.tight_layout()
    save(fig, f"{OUT}/iv-characteristics.svg")


def sch_practical_source(d):
    d += (vs := elm.SourceV().up().label("$V_{oc}$"))
    d += elm.Resistor().right().label("$R_{int}$")
    d += elm.Dot(open=True).label("+", loc="top")
    d += elm.Line().right().length(1.5)
    d += elm.Resistor().down().label("$R_L$", loc="bottom")
    d += elm.Line().left().length(1.5)
    d += elm.Dot(open=True).label("−", loc="bottom")
    d += elm.Line().left().tox(vs.start)


def fig_load_line():
    """Terminal line of a 3.90 V, 0.40 ohm source with load lines for 10 ohm and 1 ohm."""
    voc, rint = 3.90, 0.40
    v = np.linspace(0, 4.2, 200)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.plot(v, np.clip((voc - v) / rint, 0, None), color=B, lw=2, label="source: $i = (V_{oc} - v)/R_{int}$")
    for rl, col in ((10.0, O), (1.0, G)):
        ax.plot(v, v / rl, color=col, lw=1.6, ls="--", label=f"load {rl:g} Ω: $i = v/R_L$")
        vop = voc * rl / (rl + rint)
        ax.plot(vop, vop / rl, "o", color=col, ms=7)
        offset = (-175, 16) if rl > 5 else (-95, 12)
        ax.annotate(f"{vop:.3f} V, {vop / rl:.3f} A", (vop, vop / rl), textcoords="offset points",
                    xytext=offset, fontsize=9, color=col, arrowprops=dict(arrowstyle="-", color=col, lw=0.8))
    ax.annotate("$V_{oc}$ = 3.90 V", (voc, 0), textcoords="offset points", xytext=(-10, 70), fontsize=9,
                arrowprops=dict(arrowstyle="-", color="0.4", lw=0.8))
    ax.annotate("$I_{sc}$ = 9.75 A", (0, voc / rint), textcoords="offset points", xytext=(8, -4), fontsize=9)
    ax.set_xlim(0, 4.2)
    ax.set_ylim(0, 10.5)
    ax.set_xlabel("terminal voltage $v$ (V)")
    ax.set_ylabel("current delivered $i$ (A)")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.3)
    save(fig, f"{OUT}/practical-source.svg")


def sch_parallel_cells(d):
    d += (va := elm.SourceV().up().label("4.20 V"))
    d += elm.Resistor().up().label("50 mΩ")
    d += (top_a := elm.Line().right().length(3))
    d += (tp := elm.Dot().label("+", loc="top"))
    d += elm.Line().right().length(3)
    d += elm.Resistor().down().label("50 mΩ", loc="bottom")
    d += elm.SourceV().down().reverse().label("3.60 V", loc="bottom")
    d += elm.Line().left().length(3)
    d += (bm := elm.Dot())
    d += elm.Line().left().tox(va.start)
    d += elm.Line().down().at(tp.center).length(0.6)
    d += elm.Switch().down().label("optional\nload", loc="bottom", fontsize=10)
    d += elm.Resistor().down().length(1.8).label("1 Ω", loc="bottom")
    d += elm.Line().down().toy(bm.center)


if __name__ == "__main__":
    fig_iv_characteristics()
    schematic("practical-source-schematic.svg", sch_practical_source)
    fig_load_line()
    schematic("parallel-cells.svg", sch_parallel_cells)
    print("06-02 figures written to", OUT)
