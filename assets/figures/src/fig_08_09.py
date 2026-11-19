#!/usr/bin/env python3
"""Figures for chapter 08-09 (arithmetic circuits).

Run from anywhere:  python assets/figures/src/fig_08_09.py
Outputs SVGs to assets/figures/08-09/:
- adder-delay.svg: delay to the slowest sum bit against width for ripple-carry, Brent-Kung,
  Sklansky and Kogge-Stone adders, from an arrival-time simulation of each prefix network in the
  unit-delay model of the chapter (every network is also checked on random additions);
- energy.svg: Horowitz's 45 nm energy-per-operation estimates (ISSCC 2014, Figure 1.1.9; R-157).
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-09"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def ripple(n):
    return [[(i, i - 1)] for i in range(1, n)]


def kogge_stone(n):
    levels, d = [], 1
    while d < n:
        levels.append([(i, i - d) for i in range(d, n)])
        d *= 2
    return levels


def sklansky(n):
    levels, d = [], 1
    while d < n:
        levels.append([(i, (i // d) * d - 1) for i in range(n) if (i // d) % 2 == 1])
        d *= 2
    return levels


def brent_kung(n):
    levels, d = [], 1
    while d < n:
        levels.append([(i, i - d) for i in range(2 * d - 1, n, 2 * d)])
        d *= 2
    d //= 4
    while d >= 1:
        lv = [(i, i - d) for i in range(3 * d - 1, n, 2 * d)]
        if lv:
            levels.append(lv)
        d //= 2
    return levels


def simulate(levels, n, a, b, cin):
    """Values and unit-delay arrival times. Carry-in folded into bit 0's generate (arrives at 3)."""
    A = [(a >> i) & 1 for i in range(n)]
    B = [(b >> i) & 1 for i in range(n)]
    P = [x ^ y for x, y in zip(A, B)]
    g = [x & y for x, y in zip(A, B)]
    g[0] |= P[0] & cin
    p = P[:]
    tg, tp = [1] * n, [1] * n
    tg[0] = 3
    for lv in levels:
        ng, np_, ntg, ntp = g[:], p[:], tg[:], tp[:]
        for i, j in lv:
            ng[i] = g[i] | (p[i] & g[j])
            np_[i] = p[i] & p[j]
            ntg[i] = max(tg[i], max(tp[i], tg[j]) + 1) + 1
            ntp[i] = max(tp[i], tp[j]) + 1
        g, p, tg, tp = ng, np_, ntg, ntp
    s = sum((P[i] ^ (g[i - 1] if i else cin)) << i for i in range(n)) | (g[n - 1] << n)
    t_sum = max(max(1, tg[i - 1] if i else 0) + 1 for i in range(n))
    return s, t_sum


NETS = {"ripple-carry": ripple, "Brent–Kung": brent_kung, "Sklansky": sklansky, "Kogge–Stone": kogge_stone}


def fig_delay():
    widths = [4, 8, 16, 32, 64]
    rng = random.Random(809)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for k, (name, f) in enumerate(NETS.items()):
        ds = []
        for n in widths:
            L = f(n)
            for _ in range(200):
                a, b, c = rng.getrandbits(n), rng.getrandbits(n), rng.getrandbits(1)
                assert simulate(L, n, a, b, c)[0] == a + b + c
            ds.append(simulate(L, n, 0, 0, 0)[1])
        ax.plot(widths, ds, "o-", color=PALETTE[k], label=name)
        ax.annotate(str(ds[-1]), (widths[-1], ds[-1]), textcoords="offset points", xytext=(6, -3),
                    fontsize=8.5, color=PALETTE[k])
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xticks(widths)
    ax.set_xticklabels([str(w) for w in widths])
    ax.set_yticks([4, 8, 16, 32, 64, 128])
    ax.set_yticklabels(["4", "8", "16", "32", "64", "128"])
    ax.set_xlabel("adder width $n$ (bits)")
    ax.set_ylabel("delay to slowest sum bit (unit gate delays)")
    ax.set_title("Ripple carry grows as $n$; prefix adders as $\\log_2 n$", fontsize=10.5)
    ax.legend(loc="upper left")
    save(fig, f"{OUT}/adder-delay.svg")


def fig_energy():
    ops = ["8-bit\nint add", "32-bit\nint add", "16-bit\nFP add", "32-bit\nFP add",
           "8-bit\nint mult", "16-bit\nFP mult", "32-bit\nFP mult", "32-bit\nint mult"]
    pj = [0.03, 0.1, 0.4, 0.9, 0.2, 1.1, 3.7, 3.1]
    order = np.argsort(pj)
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    colors = [PALETTE[0] if "add" in ops[i] else PALETTE[1] for i in order]
    ax.bar(range(len(pj)), [pj[i] for i in order], color=colors)
    for x, i in enumerate(order):
        ax.text(x, pj[i] * 1.15, f"{pj[i]:g} pJ", ha="center", fontsize=8.5)
    ax.set_yscale("log")
    ax.set_ylim(0.015, 8)
    ax.set_yticks([0.03, 0.1, 0.3, 1, 3])
    ax.set_yticklabels(["0.03", "0.1", "0.3", "1", "3"])
    ax.minorticks_off()
    ax.set_xticks(range(len(pj)))
    ax.set_xticklabels([ops[i] for i in order], fontsize=8.5)
    ax.set_ylabel("energy per operation (pJ)")
    ax.set_title("Energy per operation, 45 nm, 0.9 V (Horowitz, ISSCC 2014): adds blue, multiplies orange",
                 fontsize=9.5)
    ax.grid(axis="x", visible=False)
    save(fig, f"{OUT}/energy.svg")


if __name__ == "__main__":
    fig_delay()
    fig_energy()
    print("figures written to", OUT)
