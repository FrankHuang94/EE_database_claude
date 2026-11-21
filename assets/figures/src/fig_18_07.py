#!/usr/bin/env python3
"""Figures for chapter 18-07 (RTOS concepts).

Run from anywhere:  python assets/figures/src/fig_18_07.py
Outputs
  assets/figures/18-07/priority-inversion.svg  the timelines of Example 18-07.4 (L holds mutex S, H needs it, M runs
                                              without it) under no protocol, priority inheritance and an immediate
                                              priority ceiling, from the lab's kernel simulator; hatched bars are
                                              time inside the critical section
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs" / "18-07-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import rtsched as rs  # noqa: E402

OUT = "assets/figures/18-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def tasks():
    return [rs.Task("L", 100, [(1, None), (4, "S"), (1, None)], priority=1, offset=0, max_jobs=1),
            rs.Task("M", 100, [(10, None)], priority=2, offset=3, max_jobs=1),
            rs.Task("H", 100, [(1, None), (1, "S"), (1, None)], priority=3, offset=2, max_jobs=1)]


rows = {"H": 2, "M": 1, "L": 0}
colors = {"H": PALETTE[1], "M": PALETTE[0], "L": PALETTE[2]}
fig, axs = plt.subplots(3, 1, figsize=(8.6, 5.4), sharex=True)
for ax, (proto, title) in zip(axs, (("none", "no protocol: H waits for M (response 16 ms)"),
                                    ("inherit", "priority inheritance (response 6 ms)"),
                                    ("ceiling", "immediate priority ceiling (response 6 ms)"))):
    res = rs.simulate(tasks(), 20, protocol=proto)
    # reconstruct which steps were inside S: replay the scripts against the trace
    done = {"L": 0, "H": 0, "M": 0}
    crit = {"L": (1, 5), "H": (1, 2), "M": (0, 0)}
    for t, name in enumerate(res.trace):
        if name is None:
            continue
        k = done[name]
        inside = crit[name][0] <= k < crit[name][1]
        ax.barh(rows[name], 1, left=t, color=colors[name], edgecolor="white", hatch="///" if inside else None)
        done[name] += 1
    for name, rel in (("H", 2), ("M", 3)):
        ax.plot([rel], [rows[name] + 0.45], marker="v", color="black", ms=5)
    ax.set_yticks(list(rows.values()))
    ax.set_yticklabels(list(rows.keys()))
    ax.set_title(title, fontsize=9, loc="left")
axs[-1].set_xlabel("time (ms); ▼ release; hatched: holding mutex S")
axs[-1].set_xlim(0, 20)
fig.suptitle("Priority inversion (Example 18-07.4): L holds S, H needs S, M does not", fontsize=10)
fig.tight_layout()
save(fig, f"{OUT}/priority-inversion.svg")
