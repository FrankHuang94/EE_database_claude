#!/usr/bin/env python3
"""Figures for chapter 26-06 (team structures and sizing).

Run from anywhere:  python assets/figures/src/fig_26_06.py
Outputs
  assets/figures/26-06/team-output.svg  left: effective output of a flat team, n[1 - c(n - 1)] with c = 0.03,
                                        against its size; right: output of 96 engineers split evenly into k
                                        teams (each with a lead), c = 0.03 within teams and 0.02 per other team
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "26-engineering-design-and-professional-practice" / "labs" / "26-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import team as t  # noqa: E402

OUT = "assets/figures/26-06"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def main() -> None:
    c = 0.03
    n = np.arange(1, 41)
    out = np.clip([t.flat_output(x, c) for x in n], 0, None)
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.6))
    ax[0].plot(n, out, color=PALETTE[0], marker="o", ms=3)
    ax[0].plot(n, n, color="gray", ls=":", lw=1, label="no coordination cost")
    ax[0].plot([17], [t.flat_output(17, c)], "ko", ms=5)
    ax[0].annotate(f"best: 17 people, {t.flat_output(17, c):.2f} FTE", (17, t.flat_output(17, c)), xytext=(6, 8),
                   textcoords="offset points", fontsize=8)
    ax[0].set_ylim(0, 20)
    ax[0].set_xlabel("flat team size")
    ax[0].set_ylabel("effective output (FTE)")
    ax[0].set_title("A flat team peaks, then collapses")
    ax[0].legend(fontsize=8, loc="upper right")

    ks = [k for k in range(1, 97) if 96 % k == 0]
    outs = [max(t.hierarchy_output(k, 96 // k, c, 0.02), 0) for k in ks]
    ax[1].bar(range(len(ks)), outs, color=PALETTE[1])
    ax[1].set_xticks(range(len(ks)), [f"{k}×{96 // k}" for k in ks], rotation=45, fontsize=8)
    i = int(np.argmax(outs))
    ax[1].annotate(f"{outs[i]:.1f} FTE", (i, outs[i]), xytext=(-14, 4), textcoords="offset points", fontsize=8)
    ax[1].set_xlabel("teams × engineers per team (96 engineers)")
    ax[1].set_ylabel("effective output (FTE)")
    ax[1].set_title("Split into teams: best at 12 teams of 8")
    fig.tight_layout()
    save(fig, f"{OUT}/team-output.svg")


if __name__ == "__main__":
    main()
