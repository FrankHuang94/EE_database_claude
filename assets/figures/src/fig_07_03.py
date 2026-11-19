#!/usr/bin/env python3
"""Figures for chapter 07-03 (second-order RLC transients).

Run from anywhere:  python assets/figures/src/fig_07_03.py
Outputs SVGs to assets/figures/07-03/. Schematics use schemdraw; waveforms come from integrating each
circuit's state equations with scipy (the same models the chapter and its verify script use).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import schemdraw
import schemdraw.elements as elm
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/07-03"
use_style()
B, O, G, P = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3]
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def schematic(name: str, build) -> None:
    schemdraw.config(fontsize=13, bgcolor="white")
    d = schemdraw.Drawing(show=False)
    build(d)
    d.save(str(ROOT / OUT / name))


def simulate(A, g, x0, t):
    A, g = np.asarray(A, float), np.asarray(g, float)
    s = solve_ivp(lambda _t, x: A @ x + g, (t[0], t[-1]), np.asarray(x0, float), t_eval=t,
                  rtol=1e-9, atol=1e-12, max_step=(t[-1] - t[0]) / 4000)
    return s.y


# ------------------------------------------------------------------ schematics
def sch_series_parallel(d):
    # series RLC (left): capacitor charged to V0, a switch, R and L in one loop carrying i
    d += (c := elm.Capacitor().up().at((0, 0)).label("C\n$v_C$", loc="bottom"))
    d += elm.Switch(action="close").right().label("t = 0", loc="top")
    d += elm.Resistor().right().label("R\n$i$ →", loc="top")
    d += elm.Inductor().down().label("L", loc="bottom")
    d += elm.Line().left().tox(c.start)
    # parallel RLC (right): one voltage v across all three, inductor current referenced downward
    x0 = 10.0
    d += elm.Line().right().at((x0, 3)).length(6)
    d += elm.Dot().at((x0, 3)).label("$v$", loc="left")
    d += elm.Resistor().down().at((x0, 3)).label("R", loc="bottom")
    d += elm.Inductor().down().at((x0 + 3, 3)).label("L\n$i_L$ ↓", loc="bottom")
    d += elm.Capacitor().down().at((x0 + 6, 3)).label("C", loc="bottom")
    d += elm.Line().right().at((x0, 0)).length(6)
    d += elm.Ground().at((x0 + 3, 0))


def sch_example2(d):
    d += (vs := elm.SourceV().up().label("10 V"))
    d += elm.Resistor().right().label("$R_1$ = 10 Ω")
    d += elm.Switch(action="open").right().label("t = 0", loc="top")
    d += (a := elm.Dot().label("a  ($v$)", loc="top"))
    d += elm.Inductor().down().label("L = 10 mH\n$i_L$ ↓", loc="top")
    d += (b := elm.Dot())
    d += elm.Line().left().tox(vs.start)
    d += elm.Ground()
    d += elm.Line().right().at(a.center).length(3)
    d += (c := elm.Capacitor().down().label("C = 1 µF", loc="bottom"))
    d += elm.Line().left().tox(b.center)
    d += elm.Line().right().at(c.start).length(3)
    d += elm.Resistor().down().label("$R_2$ = 25 Ω", loc="bottom")
    d += elm.Line().left().tox(c.end)


def sch_lc_filter(d):
    d += (vs := elm.SourceV().up().label("$V_S$ = 5 V\n(steps on)"))
    d += elm.Resistor().right().label("$R_s$ = 30 mΩ")
    d += elm.Inductor().right().label("L = 4.7 µH\n$i_L$ →")
    d += (o := elm.Dot().label("$v$", loc="top"))
    d += (c := elm.Capacitor().down().label("C = 22 µF", loc="bottom"))
    d += elm.Line().left().tox(vs.start)
    d += elm.Ground()
    d += elm.Line().right().at(o.center).length(3)
    d += elm.Resistor().down().label("$R_L$", loc="bottom")
    d += elm.Line().left().tox(c.end)


# ------------------------------------------------------------------ waveforms
def fig_example2_response():
    L, C, R2, I0 = 10e-3, 1e-6, 25.0, 1.0
    t = np.linspace(0, 1.5e-3, 3001)
    A = [[-1 / (R2 * C), -1 / C], [1 / L, 0.0]]
    v = simulate(A, [0, 0], [0.0, I0], t)[0]
    v_noC = -I0 * R2 * np.exp(-t * R2 / L)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(t * 1e3, v, color=B, label="with the 1 µF capacitor (overdamped, second order)")
    ax.plot(t * 1e3, v_noC, color=O, ls="--", label="without it (first order, 07-02)")
    tm = math.log(37320.508 / 2679.492) / (37320.508 - 2679.492)
    ax.plot([tm * 1e3], [-21.86], "o", color=B)
    ax.annotate("−21.86 V at 76 µs", (tm * 1e3, -21.86), (0.25, -16), fontsize=9, arrowprops={"arrowstyle": "->"})
    ax.set_xlabel("time after the switch opens (ms)")
    ax.set_ylabel("node a voltage $v$ (V)")
    ax.set_ylim(-27, 2)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    save(fig, f"{OUT}/example2-response.svg")


def fig_hot_plug():
    V, L, R, C, Cb, Rb = 12.0, 1e-6, 0.05, 10e-6, 47e-6, 0.3
    t = np.linspace(0, 100e-6, 4001)
    x = simulate([[-R / L, -1 / L], [1 / C, 0.0]], [V / L, 0], [0, 0], t)
    xd = simulate([[-R / L, -1 / L, 0], [1 / C, -1 / (Rb * C), 1 / (Rb * C)], [0, 1 / (Rb * Cb), -1 / (Rb * Cb)]],
                  [V / L, 0, 0], [0, 0, 0], t)
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.3))
    axes[0].plot(t * 1e6, x[1], color=B, label="ceramic only")
    axes[0].plot(t * 1e6, xd[1], color=O, ls="--", label="+ 47 µF, 0.3 Ω ESR")
    axes[0].axhline(V, color="0.5", lw=0.8)
    axes[0].set_ylabel("input voltage $v_C$ (V)")
    axes[0].legend(fontsize=8, loc="lower right")
    axes[1].plot(t * 1e6, x[0], color=B)
    axes[1].plot(t * 1e6, xd[0], color=O, ls="--")
    axes[1].axhline(V / math.sqrt(L / C), color="0.5", lw=0.8, ls=":")
    axes[1].text(60, V / math.sqrt(L / C) + 1.5, "$V/Z_0$ = 37.9 A", fontsize=8)
    axes[1].set_ylabel("cable current $i$ (A)")
    for ax in axes:
        ax.set_xlabel("time (µs)")
    fig.tight_layout()
    save(fig, f"{OUT}/hot-plug.svg")


def fig_snubber():
    V, L, C, R = 48.0, 2e-9, 250e-12, 0.1
    Rd = math.sqrt(L / C)
    t = np.linspace(0, 40e-9, 8001)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    x = simulate([[-R / L, -1 / L], [1 / C, 0.0]], [V / L, 0], [0, 0], t)
    ax.plot(t * 1e9, x[1], color="0.55", lw=1.0, label="no snubber")
    for k, col, ls in ((1, P, ":"), (4, B, "-"), (10, O, "--")):
        Cd = k * C
        A = [[-R / L, -1 / L, 0], [1 / C, -1 / (Rd * C), 1 / (Rd * C)], [0, 1 / (Rd * Cd), -1 / (Rd * Cd)]]
        y = simulate(A, [V / L, 0, 0], [0, 0, 0], t)
        ax.plot(t * 1e9, y[1], color=col, ls=ls, label=f"$C_d$ = {k}C, $R_d$ = $Z_0$")
    ax.axhline(V, color="0.3", lw=0.6)
    ax.set_xlabel("time (ns)")
    ax.set_ylabel("switch-node voltage (V)")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, f"{OUT}/snubber.svg")


if __name__ == "__main__":
    schematic("series-parallel-rlc.svg", sch_series_parallel)
    schematic("example2-schematic.svg", sch_example2)
    schematic("lc-filter-schematic.svg", sch_lc_filter)
    fig_example2_response()
    fig_hot_plug()
    fig_snubber()
    print("07-03 figures written to", OUT)
