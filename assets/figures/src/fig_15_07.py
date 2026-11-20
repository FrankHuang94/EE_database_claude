#!/usr/bin/env python3
"""Figure for chapter 15-07 (frequency-domain design).

Run from anywhere:  python assets/figures/src/fig_15_07.py
Outputs assets/figures/15-07/margins.svg: left, the Bode plot of Example 15-07.2's loop gain
8.30/[s(s+2)(s+4)] with the gain and phase margins marked; right, the Nyquist plots of Example 15-07.5's
loop K(s+1)/[s(s-1)(s+6)] for K = 10 (stable) and K = 5 (unstable), near the critical point -1.
Uses labs/15-07-lab/freqdomain.py.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "15-control-systems" / "labs" / "15-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
from freqdomain import _unwrapped_phase, freq_resp, margins  # noqa: E402

OUT = "assets/figures/15-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_margins():
    fig = plt.figure(figsize=(9.6, 4.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.15, 1])
    am = fig.add_subplot(gs[0, 0])
    ap = fig.add_subplot(gs[1, 0], sharex=am)
    an = fig.add_subplot(gs[:, 1])

    num, den = [224 / 27], [1, 6, 8, 0]
    w = np.logspace(-2, 2, 3000)
    L = freq_resp(num, den, w)
    ph = np.degrees(_unwrapped_phase(np.array(num), np.array(den), w, 0.0))
    m = margins(num, den)
    am.semilogx(w, 20 * np.log10(np.abs(L)), color=PALETTE[0])
    am.axhline(0, color="gray", lw=0.6)
    am.axvline(m["w180"], color=PALETTE[1], ls=":", lw=1)
    am.annotate("", xy=(m["w180"], 0), xytext=(m["w180"], -m["gm_db"]),
                arrowprops=dict(arrowstyle="<->", color=PALETTE[1]))
    am.text(m["w180"] * 1.15, -8, f"GM = {m['gm_db']:.1f} dB", color=PALETTE[1], fontsize=7)
    am.set_ylabel("|L| (dB)")
    am.set_ylim(-60, 40)
    am.set_title("Example 15-07.2: L = 8.30/[s(s+2)(s+4)]", fontsize=9)
    ap.semilogx(w, ph, color=PALETTE[0])
    ap.axhline(-180, color="gray", lw=0.6)
    ap.axvline(m["wc"], color=PALETTE[2], ls=":", lw=1)
    ap.annotate("", xy=(m["wc"], -180), xytext=(m["wc"], -180 + m["pm"]),
                arrowprops=dict(arrowstyle="<->", color=PALETTE[2]))
    ap.text(m["wc"] * 1.15, -160, f"PM = {m['pm']:.1f}°", color=PALETTE[2], fontsize=7)
    ap.set_ylabel("phase (deg)")
    ap.set_xlabel("ω (rad/s)")
    ap.set_ylim(-270, -90)

    dn = np.polymul([1, 0], np.polymul([1, -1], [1, 6]))
    wv = np.logspace(-1.3, 2.5, 6000)
    for K, col, lab in ((10, PALETTE[0], "K = 10: one CCW encirclement, stable"),
                        (5, PALETTE[3], "K = 5: encirclement reversed, unstable")):
        Lw = freq_resp([K, K], dn, wv)
        an.plot(Lw.real, Lw.imag, color=col, label=lab)
        an.plot(Lw.real, -Lw.imag, color=col, ls="--", lw=0.8)
        an.plot(-K / 7.5, 0, "o", color=col, ms=4)
    an.plot([-1], [0], "kx", ms=8, mew=1.5)
    an.annotate("−1", (-1, 0), textcoords="offset points", xytext=(-6, 8), fontsize=8)
    an.axhline(0, color="gray", lw=0.5)
    an.axvline(0, color="gray", lw=0.5)
    an.set_xlim(-3, 0.5)
    an.set_ylim(-2.5, 2.5)
    an.set_aspect("equal", adjustable="box")
    an.set_xlabel("Re L")
    an.set_ylabel("Im L")
    an.set_title("Example 15-07.5: K(s+1)/[s(s−1)(s+6)] near −1", fontsize=9)
    an.legend(fontsize=7, loc="lower left")
    fig.tight_layout()
    save(fig, f"{OUT}/margins.svg")


if __name__ == "__main__":
    fig_margins()
