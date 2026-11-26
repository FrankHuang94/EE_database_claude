#!/usr/bin/env python3
"""Figures for chapter 26-05 (schedule and respin risk).

Run from anywhere:  python assets/figures/src/fig_26_05.py
Outputs
  assets/figures/26-05/tapeout-cost.svg  expected cost of Example 26-05.5 (N0 = 40, phi = 0.25, $1.5 M a week,
                                         $40 M respin) against weeks of final verification, for tau = 4 weeks
                                         and with emulation (tau = 2.5 weeks, +$3 M), with the ridge and minima
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "26-engineering-design-and-professional-practice" / "labs" / "26-05-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import risk as r  # noqa: E402

OUT = "assets/figures/26-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def main() -> None:
    t = np.linspace(0, 30, 601)
    f0 = np.array([r.total_cost(x, 40, 4.0, 0.25, 1.5, 40) for x in t])
    f1 = np.array([r.total_cost(x, 40, 2.5, 0.25, 1.5, 40, fixed=3.0) for x in t])
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(t, f0, color=PALETTE[0], label=r"no emulation ($\tau$ = 4 weeks)")
    ax.plot(t, f1, color=PALETTE[1], label=r"emulation ($\tau$ = 2.5 weeks, +\$3 M)")
    ts0, _ = r.optimal_tapeout(40, 4.0, 0.25, 1.5, 40)
    ts1, _ = r.optimal_tapeout(40, 2.5, 0.25, 1.5, 40)
    for ts, tau, fixed, col in ((ts0, 4.0, 0.0, PALETTE[0]), (ts1, 2.5, 3.0, PALETTE[1])):
        y = r.total_cost(ts, 40, tau, 0.25, 1.5, 40, fixed)
        ax.plot([ts], [y], "o", color=col, ms=5)
        ax.annotate(f"minimum {ts:.1f} wk, \\${y:.1f} M", (ts, y), xytext=(6, -16), textcoords="offset points",
                    fontsize=8)
    i = int(np.argmax(f0[:300]))
    ax.plot([t[i]], [f0[i]], "kv", ms=5)
    ax.annotate(f"worst stop before optimum\n{t[i]:.1f} wk, \\${f0[i]:.1f} M", (t[i], f0[i]), xytext=(8, 2),
                textcoords="offset points", fontsize=8)
    ax.set_xlabel("weeks of final verification before tape-out")
    ax.set_ylabel("expected cost ($M)")
    ax.set_ylim(15, 50)
    ax.set_title("Tape out at the minimum, never on the ridge")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, f"{OUT}/tapeout-cost.svg")


if __name__ == "__main__":
    main()
