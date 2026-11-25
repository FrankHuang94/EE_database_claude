#!/usr/bin/env python3
"""Figures for chapter 23-04 (DRAM interfaces).

Run from anywhere:  python assets/figures/src/fig_23_04.py
Outputs
  assets/figures/23-04/reflections.svg    far-end voltage of a 1.0 V step from 34 ohm on a 40 ohm, 300 ps line with a
                                          matched, a 120 ohm and an open far end (ideal edges; Example 23-04.5)
  assets/figures/23-04/pam-rc-eyes.svg    worst-case eye opening at 48 Gb/s through a first-order channel against its
                                          time constant, for NRZ, PAM3 and PAM4 (Lab Part 3; Problem 23-04.14)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "23-memory-and-storage-technology" / "labs" / "23-04-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import ddrio as dd  # noqa: E402

OUT = "assets/figures/23-04"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
TD = 300e-12


def reflections() -> None:
    t = np.linspace(0, 3.2e-9, 1601)
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    for r_l, lab, col in ((40, "40 Ω (matched)", PALETTE[2]), (120, "120 Ω", PALETTE[0]),
                          (math.inf, "open", PALETTE[1])):
        arr = dd.far_end_arrivals(1.0, 34, 40, r_l, 6)
        v = np.zeros_like(t)
        for k, val in enumerate(arr):
            v[t >= TD * (1 + 2 * k)] = val
        ax.plot(t * 1e9, v, color=col, label=lab, drawstyle="steps-post")
    ax.set_xlabel("time (ns)")
    ax.set_ylabel("far-end voltage (V)")
    ax.set_ylim(0, 1.2)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("A 1.0 V step on a 40 Ω, 300 ps line driven from 34 Ω", fontsize=10)
    save(fig, f"{OUT}/reflections.svg")


def pam_rc_eyes() -> None:
    taus = np.linspace(4e-12, 32e-12, 300)
    fig, ax = plt.subplots(figsize=(6.0, 3.5))
    for (m, b, lab), col in zip(((2, 1.0, "NRZ"), (3, 1.5, "PAM3"), (4, 2.0, "PAM4")), PALETTE):
        eyes = []
        for tau in taus:
            a = math.exp(-(b / 48e9) / tau)
            eyes.append(dd.worst_eye(1 - a, a, m))
        ax.plot(taus * 1e12, eyes, color=col, label=lab)
    ax.axhline(0, color="0.5", lw=0.8)
    ax.set_xlabel("channel time constant τ (ps)")
    ax.set_ylabel("worst-case eye (fraction of swing)")
    ax.set_ylim(-0.2, 1.0)
    ax.legend(fontsize=8)
    ax.set_title("48 Gb/s through a first-order channel: NRZ leads throughout", fontsize=10)
    save(fig, f"{OUT}/pam-rc-eyes.svg")


if __name__ == "__main__":
    reflections()
    pam_rc_eyes()
