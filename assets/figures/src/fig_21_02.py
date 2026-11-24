#!/usr/bin/env python3
"""Figures for chapter 21-02 (impedance matching networks).

Run from anywhere:  python assets/figures/src/fig_21_02.py
Outputs
  assets/figures/21-02/sections.svg  return loss of the one- and two-section 5-to-50 ohm matches of Example 21-02.4
                                     against frequency, with the 10 dB line and the two bands marked
  assets/figures/21-02/loss.svg      inductor insertion loss 10 log10(1 + Qn/Qu) against the inductor's unloaded Q
                                     for network Q of 1, 2, 3 and 5, with the three cases of Example 21-02.5 marked
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "21-rf-and-microwave-engineering" / "labs" / "21-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import match  # noqa: E402

OUT = "assets/figures/21-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

F0 = 2e9
W0 = 2 * math.pi * F0


def l_section(r_low, r_high):
    x, b, _ = match.l_match(r_low, r_high)
    return [("sL", x / W0), ("pC", b / W0)]


one = l_section(5, 50)
rs, _ = match.cascade_l(5, 50, 2)
two = l_section(rs[0], rs[1]) + l_section(rs[1], rs[2])
f = np.linspace(0.8e9, 4.0e9, 1601)
fig, ax = plt.subplots(figsize=(6.0, 3.8))
for els, lab, col in ((one, "one L-section (Q = 3)", PALETTE[0]), (two, "two L-sections (Q = 1.47 each)", PALETTE[1])):
    rl = np.array([-20 * math.log10(abs(match.gamma_of(match.zin_ladder(els, 5, ff)))) for ff in f])
    ax.plot(f / 1e9, rl, color=col, lw=1.4, label=lab)
    band = rl >= 10
    ax.fill_between(f / 1e9, 0, 10, where=band, color=col, alpha=0.12, lw=0)
ax.axhline(10, color="0.4", lw=0.8, ls="--")
ax.text(3.35, 10.8, "10 dB return loss", fontsize=8, color="0.3")
ax.set_ylim(0, 40)
ax.set_xlabel("frequency (GHz)")
ax.set_ylabel("return loss (dB)")
ax.legend(fontsize=8, loc="upper right")
ax.set_title("5 Ω to 50 Ω at 2 GHz: two small steps give three times the band", fontsize=10)
save(fig, f"{OUT}/sections.svg")

qu = np.logspace(math.log10(3), math.log10(200), 400)
fig, ax = plt.subplots(figsize=(6.0, 3.8))
for qn, col in zip((1, 2, 3, 5), PALETTE):
    ax.plot(qu, 10 * np.log10(1 + qn / qu), color=col, lw=1.4, label=f"$Q_n$ = {qn}")
for qn, qv, txt in ((2, 15, "Ex. 5(a)"), (3, 15, "Ex. 5(b)"), (3, 8, "Ex. 5(c)")):
    il = 10 * math.log10(1 + qn / qv)
    ax.plot([qv], [il], "o", color="k", ms=4)
    ax.annotate(txt, (qv, il), textcoords="offset points", xytext=(6, 4), fontsize=8, color="0.25")
ax.set_xscale("log")
ax.set_ylim(0, 4)
ax.set_xlabel("inductor unloaded Q, $Q_u$")
ax.set_ylabel("insertion loss (dB)")
ax.legend(fontsize=8, loc="upper right")
ax.set_title("Loss in the match grows with the ratio $Q_n/Q_u$", fontsize=10)
save(fig, f"{OUT}/loss.svg")
