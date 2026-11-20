#!/usr/bin/env python3
"""Figures for chapter 14-08 (out-of-order and superscalar execution).

Run from anywhere:  python assets/figures/src/fig_14_08.py   (needs LLVM for the course simulator's builds)
Outputs SVGs to assets/figures/14-08/:
- ilp-limits.svg: left, IPC against width for four workloads on the trace-driven model of labs/14-08-lab/ooo.py
  (out of order with a 256-entry window, perfect prediction unless stated; the unrolled loop also in order);
  right, IPC of the divide loop of Problem 14-08.13 against window size at width 4, with the Little's-law
  estimate min(4, W / 25).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
C14 = ROOT / "courses" / "14-computer-organization-and-architecture"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(C14 / "labs" / "14-08-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import ooo  # noqa: E402

OUT = "assets/figures/14-08"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)
WIDTHS = [1, 2, 4, 8]
WINDOWS = [8, 16, 32, 64, 128, 256]


def series():
    inc, _ = ooo.dyn_trace({"i.s": ooo.INC})
    ptr, _ = ooo.dyn_trace({"p.s": ooo.PTR}, ooo.ptr_data())
    src, data = ooo.lab_program()
    fib, _ = ooo.dyn_trace(src, data)
    mis = ooo.mispredicted_indices(fib, direction="gshare", ras_depth=16)
    ipc = lambda tr, **kw: [ooo.schedule(tr, width=w, rob=256, **kw)["ipc"] for w in WIDTHS]  # noqa: E731
    rows = [
        ("unrolled loop, out of order", ipc(inc), PALETTE[0], "-", "o"),
        ("unrolled loop, in order", ipc(inc, in_order=True), PALETTE[0], "--", "s"),
        ("lab program, perfect prediction", ipc(fib), PALETTE[2], "-", "^"),
        ("lab program, gshare, refill 10", ipc(fib, mispredicted=mis, refill=10), PALETTE[1], "-", "v"),
        ("linked list, out of order", ipc(ptr), PALETTE[3], "-", "D"),
    ]
    dv, _ = ooo.dyn_trace({"d.s": ooo.DIV}, ooo.words(ooo.DIV_VALUES))
    div = [ooo.schedule(dv, width=4, rob=w)["ipc"] for w in WINDOWS]
    return rows, div


def fig_limits():
    rows, div = series()
    # spot checks against the keyed values of chapter 14-08 and its lab
    assert round(rows[0][1][3], 3) == 6.724 and round(rows[4][1][2], 3) == 1.322
    assert round(rows[2][1][3], 2) == 7.54 and round(rows[3][1][3], 3) == round(1923 / 819, 3)
    assert [round(div[k], 3) for k in (1, 2, 3, 4)] == [0.717, 1.410, 2.514, 3.562]

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.0, 3.6))
    ax.plot(WIDTHS, WIDTHS, color="0.6", lw=0.8, ls=":", label="IPC = width")
    for label, y, c, ls, m in rows:
        ax.plot(WIDTHS, y, color=c, ls=ls, marker=m, ms=4, label=label)
    ax.set_xscale("log", base=2)
    ax.set_xticks(WIDTHS, [str(w) for w in WIDTHS])
    ax.set_xlabel("width (instructions per cycle)")
    ax.set_ylabel("IPC")
    ax.set_ylim(0, 8.3)
    ax.set_title("Which limit binds? (256-entry window)", fontsize=9)
    ax.legend(fontsize=6.8, loc="upper left")

    grid = [8 * 2 ** (k / 20) for k in range(101)]
    bx.plot(WINDOWS, div, color=PALETTE[0], marker="o", ms=4, label="model, width 4")
    bx.plot(grid, [min(4, w / 25) for w in grid], color=PALETTE[1], ls="--", label="Little's law: min(4, W/25)")
    bx.set_xscale("log", base=2)
    bx.set_xticks(WINDOWS, [str(w) for w in WINDOWS])
    bx.set_xlabel("window (reorder-buffer entries)")
    bx.set_ylabel("IPC")
    bx.set_ylim(0, 4.3)
    bx.set_title("Loop with a 20-cycle divide per element", fontsize=9)
    bx.legend(fontsize=7, loc="upper left")
    save(fig, f"{OUT}/ilp-limits.svg")
    return rows, div


if __name__ == "__main__":
    r, d = fig_limits()
    for label, y, *_ in r:
        print(label, [round(x, 2) for x in y])
    print("div", [round(x, 2) for x in d])
