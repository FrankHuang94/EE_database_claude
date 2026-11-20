#!/usr/bin/env python3
"""Figures for chapter 12-02 (active loads, cascodes and multistage amplifiers).

Run from anywhere:  python assets/figures/src/fig_12_02.py
Outputs SVGs to assets/figures/12-02/:
- gain-headroom.svg: gain against the voltage each load option needs across the stage (resistor drop plus
  overdrives), for devices with g_m = 1 mA/V, r_o = 100 kohm and V_ov = 0.2 V; gains by nodal analysis.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/12-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
GM, RO = 1e-3, 100e3


def gain(n_casc_in, load):
    """Small-signal gain of a CS stage (optionally cascoded) with load: ('R', ohms) or ('cas',) or ('cs',)."""
    nodes = ["out"] + (["x"] if n_casc_in else []) + (["y"] if load[0] == "cas" else [])
    idx = {n: i for i, n in enumerate(nodes)}
    G = np.zeros((len(nodes), len(nodes)))
    b = np.zeros(len(nodes))

    def stamp_m(d, g, s, vin=None):
        # drain current gm*(vg - vs) + (vd - vs)/ro leaves d, enters s; '0' and 'in' are fixed
        for node, sign in ((d, 1), (s, -1)):
            if node not in idx:
                continue
            i = idx[node]
            for ctrl, coef in ((g, GM), (s, -GM), (d, 1 / RO), (s, -1 / RO)):
                if ctrl in idx:
                    G[i, idx[ctrl]] += sign * coef
                elif ctrl == "in":
                    b[i] -= sign * coef * 1.0

    if n_casc_in:
        stamp_m("x", "in", "0")
        stamp_m("out", "0", "x")
    else:
        stamp_m("out", "in", "0")
    if load[0] == "R":
        G[idx["out"], idx["out"]] += 1 / load[1]
    elif load[0] == "cs":
        G[idx["out"], idx["out"]] += 1 / RO
    elif load[0] == "cas":
        stamp_m("out", "0", "y")
        stamp_m("y", "0", "0")
    return abs(np.linalg.solve(G, b)[idx["out"]])


def fig_gain_headroom():
    opts = [("resistor load\n(0.9 V drop)", gain(False, ("R", 9e3)), 1.1),
            ("current-source\nload", gain(False, ("cs",)), 0.4),
            ("cascode,\nsimple load", gain(True, ("cs",)), 0.6),
            ("cascode,\ncascode load", gain(True, ("cas",)), 0.8)]
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    offsets = [(10, -4), (10, -26), (10, -4), (10, -4)]
    for i, (name, a, h) in enumerate(opts):
        ax.scatter([h], [a], s=60, color=PALETTE[i], zorder=3)
        ax.annotate(f"{name}: {a:.4g}", (h, a), textcoords="offset points", xytext=offsets[i], fontsize=8)
    ax.set_yscale("log")
    ax.set_xlim(0.2, 1.6)
    ax.set_ylim(3, 2e4)
    ax.set_xlabel("voltage needed across the stage (V): resistor drop plus overdrives")
    ax.set_ylabel("voltage gain (log scale)")
    ax.set_title("g_m = 1 mA/V, r_o = 100 kΩ, V_ov = 0.2 V", fontsize=9)
    fig.tight_layout()
    save(fig, f"{OUT}/gain-headroom.svg")


if __name__ == "__main__":
    fig_gain_headroom()
