#!/usr/bin/env python3
"""Figures for chapter 19-10 (synthesis and static timing analysis).

Run from anywhere:  python assets/figures/src/fig_19_10.py
Outputs
  assets/figures/19-10/nldm-inverter.svg   SKY130 inv_1 rising delay from its Liberty table (tt_025C_1v80) against load
                                           for each characterized input slew, with Example 19-10.1's interpolated
                                           point; and the same row at the slow corner (ss_100C_1v60)
  assets/figures/19-10/timing-graph.svg    Example 19-10.2's gate network with arrival / required / slack at every
                                           node and the critical path highlighted
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "19-digital-vlsi-design" / "labs" / "19-10-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import sta  # noqa: E402

OUT = "assets/figures/19-10"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- NLDM table
lib = sta.load_library()
arc = lib["cells"]["inv_1"]["arcs"]["A"]
ss = lib["other_corners"]["ss_100C_1v60"]["inv_1"]["arcs"]["A"]
fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.0))
ax = axes[0]
for k, (slew, row) in enumerate(zip(arc["index_1"], arc["cell_rise"])):
    ax.plot(np.array(arc["index_2"]) * 1e3, np.array(row) * 1e3, "o-", ms=3, lw=1.2,
            color=plt.cm.viridis(k / 6), label=f"{slew:.3g} ns")
d1 = sta.arc_delay(lib, "inv_1", "A", "rise", 0.080, 0.005)[0]
ax.plot([5.0], [d1 * 1e3], "*", ms=11, color=PALETTE[1], label="Example 1 (0.08 ns, 5 fF)")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("output load (fF)")
ax.set_ylabel("cell_rise delay (ps)")
ax.set_title("inv_1, tt_025C_1v80: one curve per input slew", fontsize=10)
ax.legend(fontsize=7, title="input slew", title_fontsize=7, loc="upper left")

ax = axes[1]
loads = np.array(arc["index_2"]) * 1e3
ax.plot(loads, np.array(arc["cell_rise"][2]) * 1e3, "o-", color=PALETTE[0], label="tt_025C_1v80")
ax.plot(np.array(ss["index_2"]) * 1e3, np.array(ss["cell_rise"][2]) * 1e3, "s--", color=PALETTE[1], label="ss_100C_1v60")
r_eff = (arc["cell_rise"][2][5] - arc["cell_rise"][2][3]) / (arc["index_2"][5] - arc["index_2"][3])
ax.set_xlabel("output load (fF)")
ax.set_ylabel("cell_rise delay (ps)")
ax.set_xlim(0, 190)
ax.set_ylim(0, 1800)
ax.set_title(f"slew 0.053 ns: slope {r_eff:.2f} kΩ at tt", fontsize=10)
ax.legend(fontsize=8)
fig.tight_layout()
save(fig, f"{OUT}/nldm-inverter.svg")

# ---------------------------------------------------------------- timing graph of Example 2
gates = {"G1": (40, ["a", "b"]), "G2": (25, ["c"]), "G3": (60, ["G1", "G2"]), "G4": (45, ["G1", "c"]),
         "G5": (50, ["G3", "G4"])}
inputs = {"a": 0, "b": 20, "c": 10}
order = ["G1", "G2", "G3", "G4", "G5"]
at = dict(inputs)
for g in order:
    at[g] = max(at[f] for f in gates[g][1]) + gates[g][0]
rt = {"G5": 180}
for g in reversed(order):
    for f in gates[g][1]:
        rt[f] = min(rt.get(f, 1e9), rt[g] - gates[g][0])
pos = {"a": (0, 2.2), "b": (0, 1.2), "c": (0, 0.0), "G1": (1.6, 1.7), "G2": (1.6, 0.3), "G3": (3.2, 1.2),
       "G4": (3.2, -0.1), "G5": (4.8, 0.6)}
critical = {("b", "G1"), ("G1", "G3"), ("G3", "G5")}
fig, ax = plt.subplots(figsize=(8.4, 3.8))
for g, (d, fins) in gates.items():
    for f in fins:
        x0, y0 = pos[f]
        x1, y1 = pos[g]
        crit = (f, g) in critical
        ax.annotate("", xy=(x1 - 0.42, y1), xytext=(x0 + 0.42, y0),
                    arrowprops=dict(arrowstyle="->", lw=2.2 if crit else 1.0,
                                    color=PALETTE[1] if crit else "0.45"))
for n, (x, y) in pos.items():
    slack = rt[n] - at[n]
    crit = slack == min(rt[k] - at[k] for k in pos)
    box = dict(boxstyle="round,pad=0.35", fc="#fde9dc" if crit else "#eef3f8",
               ec=PALETTE[1] if crit else PALETTE[0], lw=1.2)
    label = n if n in inputs else f"{n} ({gates[n][0]} ps)"
    ax.text(x, y, f"{label}\nAT {at[n]}  RT {rt[n]}\nslack {slack}", ha="center", va="center", fontsize=8, bbox=box)
ax.text(5.55, 0.6, "y\nrequired\n180 ps", ha="left", va="center", fontsize=8)
ax.set_xlim(-0.6, 6.2)
ax.set_ylim(-0.7, 2.7)
ax.axis("off")
ax.set_title("Example 19-10.2: arrival (AT), required (RT) and slack in ps; critical path b → G1 → G3 → G5", fontsize=10)
save(fig, f"{OUT}/timing-graph.svg")
