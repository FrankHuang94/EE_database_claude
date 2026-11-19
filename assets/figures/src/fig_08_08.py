#!/usr/bin/env python3
"""Figures for chapter 08-08 (finite state machines).

Run from anywhere:  python assets/figures/src/fig_08_08.py
Outputs SVGs to assets/figures/08-08/: a timing diagram of the Moore and Mealy 101 detectors on the
input of Example 08-08.1 (both machines simulated from their state tables), and the flip-flop area
of binary versus one-hot encoding against the number of states, using SKY130 cell areas (R-156).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# Moore 101 detector: state -> (next on 0, next on 1); output 1 only in S3
MOORE = {0: (0, 1), 1: (2, 1), 2: (0, 3), 3: (2, 1)}
# Mealy 101 detector: state -> ((next, z) on 0, (next, z) on 1)
MEALY = {0: ((0, 0), (1, 0)), 1: ((2, 0), (1, 0)), 2: ((0, 0), (1, 1))}
X = [1, 1, 0, 1, 0, 1, 1, 0, 1]


def simulate():
    sm, se = [0], [0]
    zm, ze = [], []
    for x in X:
        zm.append(1 if sm[-1] == 3 else 0)
        nxt, z = MEALY[se[-1]][x]
        ze.append(z)
        sm.append(MOORE[sm[-1]][x])
        se.append(nxt)
    zm.append(1 if sm[-1] == 3 else 0)
    return sm, zm, se, ze


def fig_timing():
    sm, zm, se, ze = simulate()
    assert [t for t, z in enumerate(zm) if z] == [4, 6, 9]
    assert [t for t, z in enumerate(ze) if z] == [3, 5, 8]
    n = 10
    d = 0.12                                       # input and state change this long after the edge
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    rows = ["clk", "x", "Mealy state", "Mealy z", "Moore state", "Moore z"]
    base = {r: (len(rows) - 1 - i) * 1.4 for i, r in enumerate(rows)}

    def wave(name, vals, delay, color):
        ts, ys = [0.0], [vals[0]]
        for t in range(1, len(vals)):
            ts += [t + delay, t + delay]
            ys += [vals[t - 1], vals[t]]
        ts.append(n)
        ys.append(vals[-1])
        ax.plot(ts, [base[name] + 0.8 * y for y in ys], color=color, lw=1.6)

    def bus(name, vals, delay, color):
        b = base[name]
        for t, v in enumerate(vals):
            t0 = t + (delay if t else 0)
            t1 = min(t + 1 + delay, n)
            ax.plot([t0, t1], [b, b], color=color, lw=1.2)
            ax.plot([t0, t1], [b + 0.8, b + 0.8], color=color, lw=1.2)
            ax.text((t0 + t1) / 2, b + 0.4, f"S{v}", ha="center", va="center", fontsize=8.5)
            if t:
                ax.plot([t0, t0], [b, b + 0.8], color=color, lw=1.2)

    ts, ys = [], []
    for t in range(n):
        ts += [t, t, t + 0.5, t + 0.5]
        ys += [0, 1, 1, 0]
    ts.append(n)
    ys.append(0)
    ax.plot(ts, [base["clk"] + 0.8 * y for y in ys], color="black", lw=1.4)
    wave("x", X + [X[-1]], d, "black")
    bus("Mealy state", se[:n], d, PALETTE[1])
    ze_full = ze + [0]
    # the Mealy output follows x within the cycle: draw it with the input's timing
    wave("Mealy z", ze_full, d + 0.05, PALETTE[1])
    bus("Moore state", sm[:n], d, PALETTE[0])
    wave("Moore z", zm[:n], d + 0.05, PALETTE[0])
    for name, b in base.items():
        ax.text(-0.25, b + 0.4, name, ha="right", va="center", fontsize=9.5)
    for t in range(n):
        ax.text(t + 0.5, base["clk"] + 1.15, str(t), ha="center", fontsize=8, color="0.4")
    ax.text(-0.25, base["clk"] + 1.15, "cycle", ha="right", fontsize=8, color="0.4")
    ax.set_xlim(-0.1, n)
    ax.set_ylim(-0.3, base["clk"] + 1.5)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.grid(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.set_title("101 detectors: the Mealy output (cycles 3, 5, 8) leads the Moore output (4, 6, 9)",
                 fontsize=10.5)
    save(fig, f"{OUT}/moore-mealy-timing.svg")


def fig_encoding():
    a_ff, a_nand = 25.024, 3.7536                  # SKY130 dfrtp_1 and nand2_1 areas, µm²
    ns = list(range(2, 65))
    binary = [math.ceil(math.log2(k)) * a_ff for k in ns]
    onehot = [k * a_ff for k in ns]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(ns, onehot, label="one-hot ($N$ flip-flops)")
    ax.step(ns, binary, where="mid", label=r"binary ($\lceil \log_2 N \rceil$ flip-flops)")
    ax.axvline(31.5, color="0.5", lw=1.0, ls="--")
    ax.text(33.0, 380, "Yosys automatic encoding:\none-hot below 32 states,\nbinary from 32",
            ha="left", fontsize=8.5, color="0.3")
    ax.set_xlabel("number of states $N$")
    ax.set_ylabel("flip-flop area (µm²)")
    sec = ax.secondary_yaxis("right", functions=(lambda a: a / a_nand, lambda q: q * a_nand))
    sec.set_ylabel("NAND2 equivalents")
    ax.set_title("State-register area in SKY130 (flip-flop with reset, 25.024 µm²)", fontsize=10.5)
    ax.legend(loc="upper left")
    save(fig, f"{OUT}/encoding-cost.svg")


if __name__ == "__main__":
    fig_timing()
    fig_encoding()
    print("figures written to", OUT)
