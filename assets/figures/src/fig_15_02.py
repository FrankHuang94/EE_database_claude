#!/usr/bin/env python3
"""Figure for chapter 15-02 (transfer functions and block diagrams).

Run from anywhere:  python assets/figures/src/fig_15_02.py
Outputs assets/figures/15-02/loops.svg: left, the magnitudes of S and T for Example 15-02.4's proportional loop
(plant 1/(s+1)) at K = 9 and K = 99; right, the unit-step responses of Example 15-02.3's loop with and without
the inner velocity loop. Uses labs/15-02-lab/blocks.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "15-control-systems" / "labs" / "15-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
from blocks import TF, feedback  # noqa: E402

OUT = "assets/figures/15-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_loops():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6))
    w = np.logspace(-2, 3, 500)
    P = TF([1], [1, 1])
    for K, col in ((9, PALETTE[0]), (99, PALETTE[1])):
        L = K * P
        S = feedback(1, L)          # 1/(1+L)
        T = feedback(L, 1)          # L/(1+L)
        a1.loglog(w, np.abs(S(1j * w)), color=col, ls="--", label=f"|S|, K = {K}")
        a1.loglog(w, np.abs(T(1j * w)), color=col, label=f"|T|, K = {K}")
    a1.axhline(1, color="gray", lw=0.6, ls=":")
    a1.set_xlabel("ω (rad/s)")
    a1.set_ylabel("magnitude")
    a1.set_ylim(1e-3, 3)
    a1.set_title("Sensitivity S and complementary sensitivity T", fontsize=9)
    a1.legend(fontsize=7, loc="lower left", ncol=2)

    G1, G2 = TF([10], [1, 1]), TF([1], [1, 0])
    t = np.linspace(0, 10, 4001)
    for T, col, lab in ((feedback(G1 * feedback(G2, 2), 1), PALETTE[0], "with inner loop: 10/(s²+3s+12)"),
                        (feedback(G1 * G2, 1), PALETTE[2], "without: 10/(s²+s+10)")):
        a2.plot(t, T.step(t), color=col, label=lab)
        a2.axhline(T.dcgain(), color=col, lw=0.6, ls=":")
    a2.set_xlabel("time (s)")
    a2.set_ylabel("output y for a unit step r")
    a2.set_title("Example 15-02.3: the inner loop adds damping", fontsize=9)
    a2.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/loops.svg")


if __name__ == "__main__":
    fig_loops()
