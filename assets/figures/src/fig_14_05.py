#!/usr/bin/env python3
"""Figures for chapter 14-05 (single-cycle datapath and control).

Run from anywhere:  python assets/figures/src/fig_14_05.py
Outputs SVGs to assets/figures/14-05/:
- paths.svg: the critical path of each instruction class through the single-cycle datapath, as stacked bars
  of component delays, using the illustrative delays of §3.4; the load's path sets the clock period.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/14-05"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# (component, delay in ps) along each class's longest path, in order (§3.4 and Example 14-05.3)
PATHS = {
    "load":    [("clk-to-Q", 40), ("instr. memory", 200), ("register read", 100), ("mux", 25), ("ALU", 120), ("data memory", 200), ("mux", 25), ("setup", 20)],
    "R-type":  [("clk-to-Q", 40), ("instr. memory", 200), ("register read", 100), ("mux", 25), ("ALU", 120), ("mux", 25), ("setup", 20)],
    "store":   [("clk-to-Q", 40), ("instr. memory", 200), ("register read", 100), ("mux", 25), ("ALU", 120), ("setup", 20)],
    "branch":  [("clk-to-Q", 40), ("instr. memory", 200), ("register read", 100), ("comparator / adder", 80), ("mux", 25), ("setup", 20)],
    "JAL":     [("clk-to-Q", 40), ("instr. memory", 200), ("immediate gen.", 50), ("comparator / adder", 80), ("mux", 25), ("setup", 20)],
}
COLORS = {"clk-to-Q": "0.6", "setup": "0.8", "instr. memory": PALETTE[0], "register read": PALETTE[2], "immediate gen.": PALETTE[5],
          "mux": PALETTE[6], "ALU": PALETTE[1], "comparator / adder": PALETTE[3], "data memory": PALETTE[4]}


def fig_paths():
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    names = list(PATHS)[::-1]
    seen = set()
    for y, cls in enumerate(names):
        x = 0
        for comp, d in PATHS[cls]:
            ax.barh(y, d, left=x, color=COLORS[comp], edgecolor="white", lw=0.6, label=None if comp in seen else comp)
            seen.add(comp)
            x += d
        ax.text(x + 8, y, f"{x} ps", va="center", fontsize=8)
    total = sum(d for _, d in PATHS["load"])
    assert total == 730
    ax.axvline(total, color="k", ls=":", lw=1)
    ax.text(total, len(names) - 0.4, "clock period = load path", ha="right", va="bottom", fontsize=8)
    ax.set_yticks(range(len(names)), names)
    ax.set_xlabel("delay along the critical path (ps)")
    ax.set_xlim(0, 850)
    ax.set_ylim(-0.6, len(names) - 0.1)
    ax.legend(fontsize=7, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False)
    save(fig, f"{OUT}/paths.svg")


if __name__ == "__main__":
    fig_paths()
