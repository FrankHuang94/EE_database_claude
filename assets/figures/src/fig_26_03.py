#!/usr/bin/env python3
"""Figures for chapter 26-03 (engineering economics I).

Run from anywhere:  python assets/figures/src/fig_26_03.py
Outputs
  assets/figures/26-03/npv-slip-tornado.svg  left: NPV at 12% of Example 26-03.5's program against a slip of
                                             0-12 months, the window closing at the end of year 5 with the
                                             final year's sales prorated; right: tornado of +/-10% in ASP,
                                             COGS, volume and NRE
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "26-engineering-design-and-professional-practice" / "labs" / "26-03-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import econ as e  # noqa: E402

OUT = "assets/figures/26-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def main() -> None:
    stack = e.cost_stack(17000, e.dies_per_wafer(300, 100), math.exp(-0.1), 4.0, 0.99, 1.20, 0.98, 1.20)
    cogs, mfg = stack["cogs"], stack["after_test"]
    contrib = 60 - cogs
    units = [1e6, 3e6, 4e6, 2e6]
    slips = np.linspace(0, 1, 49)
    vals = []
    for s in slips:
        f, t = e.program_flows([30e6, 30e6], units, contrib, slip=s, window_end=5)
        vals.append(e.npv(0.12, f, t) / 1e6)
    fig, ax = plt.subplots(1, 2, figsize=(9.6, 3.6))
    ax[0].plot(12 * slips, vals, color=PALETTE[0])
    for m in (6, 12):
        ax[0].plot([m], [vals[int(m / 12 * 48)]], "ko", ms=4)
        ax[0].annotate(f"{vals[int(m / 12 * 48)]:.1f}", (m, vals[int(m / 12 * 48)]), textcoords="offset points",
                       xytext=(4, 6), fontsize=8)
    ax[0].set_xlabel("schedule slip (months)")
    ax[0].set_ylabel("NPV at 12% ($M)")
    ax[0].set_title("A slip costs revenue, not just hours")

    def model(p):
        f, t = e.program_flows([p["nre"] / 2] * 2, [p["vol"] * u for u in (1, 3, 4, 2)],
                            p["asp"] * 0.98 - p["cost"])  # royalty is 2% of ASP
        return e.npv(0.12, f, t) / 1e6

    base = {"asp": 60.0, "cost": mfg, "vol": 1e6, "nre": 60e6}
    rows = e.tornado(base, model)
    b0 = model(base)
    names = {"asp": "ASP", "cost": "mfg cost", "vol": "volume", "nre": "NRE"}
    for k, (name, lo, hi) in enumerate(rows):
        ax[1].barh(k, hi - b0, left=b0, color=PALETTE[0], label="+10%" if k == 0 else None)
        ax[1].barh(k, lo - b0, left=b0, color=PALETTE[1], label="−10%" if k == 0 else None)
    ax[1].axvline(b0, color="k", lw=1)
    ax[1].set_yticks(range(len(rows)), [names[r[0]] for r in rows])
    ax[1].invert_yaxis()
    ax[1].set_xlabel("NPV ($M)")
    ax[1].set_title(f"Tornado around the base NPV of ${b0:.1f} M")
    ax[1].legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/npv-slip-tornado.svg")


if __name__ == "__main__":
    main()
