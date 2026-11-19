#!/usr/bin/env python3
"""Figures for chapter 08-12 (FPGA implementation flow).

Run from anywhere:  python assets/figures/src/fig_08_12.py
Outputs SVGs to assets/figures/08-12/, from the committed nextpnr reports of the 08-12 lab
(courses/08-digital-logic-design/labs/08-12-lab/reports/, produced by run_flow.py with Yosys 0.71 and
nextpnr-ice40 0.11.1 for an iCE40 UP5K, seed 1):
- coding-style.svg: logic cells and maximum frequency of the six implementations;
- critical-paths.svg: each design's critical path split into clock-to-Q, logic, routing and setup delay.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from plotstyle import PALETTE, save, use_style  # noqa: E402

OUT = "assets/figures/08-12"
REPORTS = ROOT / "courses/08-digital-logic-design/labs/08-12-lab/reports"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
NAMES = [("add_plus", "adder, a + b"), ("add_rca", "adder, gates"), ("mul_dsp", "multiplier, DSP"),
         ("mul_lut", "multiplier, LUTs"), ("fsm_auto", "FSM, one-hot"), ("fsm_bin", "FSM, binary")]


def load(name):
    r = json.loads((REPORTS / f"{name}.json").read_text())
    fmax = next(iter(r["fmax"].values()))["achieved"]
    cells = r["utilization"]["ICESTORM_LC"]["used"]
    seg = {}
    for s in r["critical_paths"][0]["path"]:
        seg[s["type"]] = seg.get(s["type"], 0.0) + s["delay"]
    return fmax, cells, seg


def fig_style():
    data = [load(n) for n, _ in NAMES]
    labels = [lab for _, lab in NAMES]
    colors = [PALETTE[0], PALETTE[1]] * 3
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.6))
    axs[0].barh(labels, [d[1] for d in data], color=colors)
    axs[0].set_xlabel("logic cells (of 5280)")
    axs[0].invert_yaxis()
    for i, d in enumerate(data):
        axs[0].text(d[1] + 8, i, str(d[1]), va="center", fontsize=8.5)
    axs[1].barh(labels, [d[0] for d in data], color=colors)
    axs[1].set_xlabel("maximum frequency (MHz)")
    axs[1].invert_yaxis()
    axs[1].set_yticklabels([])
    for i, d in enumerate(data):
        axs[1].text(d[0] + 1, i, f"{d[0]:.1f}", va="center", fontsize=8.5)
    axs[0].set_xlim(0, 880)
    axs[1].set_xlim(0, 118)
    fig.suptitle("Coding style on an iCE40 UP5K (Yosys 0.71, nextpnr 0.11.1, measured)", fontsize=10.5)
    plt.tight_layout()
    save(fig, f"{OUT}/coding-style.svg")


def fig_paths():
    data = [load(n) for n, _ in NAMES]
    labels = [lab for _, lab in NAMES]
    parts = [("clk-to-q", "clock-to-Q"), ("logic", "logic"), ("routing", "routing"), ("setup", "setup")]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    left = [0.0] * len(data)
    for k, (key, lab) in enumerate(parts):
        vals = [d[2].get(key, 0.0) for d in data]
        ax.barh(labels, vals, left=left, color=PALETTE[k], label=lab)
        left = [a + b for a, b in zip(left, vals)]
    ax.invert_yaxis()
    ax.set_xlabel("critical-path delay (ns)")
    ax.legend(ncol=4, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.2))
    ax.set_title("Where the time goes: routing dominates most FPGA critical paths", fontsize=10.5)
    save(fig, f"{OUT}/critical-paths.svg")


if __name__ == "__main__":
    fig_style()
    fig_paths()
    print("figures written to", OUT)
