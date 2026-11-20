#!/usr/bin/env python3
"""Figures for chapter 14-07 (branch prediction and speculation).

Run from anywhere:  python assets/figures/src/fig_14_07.py   (needs LLVM for the course simulator's builds)
Outputs SVGs to assets/figures/14-07/:
- predictors.svg: left, cycles of the lab program (sum + recursive fib(10)) on the five-stage pipeline,
  N + 4 + S + 2M, for four predictor configurations; right, cycles of the count loop of Example 14-07.6 at a
  15-cycle misprediction penalty for branchy code on random and sorted data and branchless code on random data.
  Every misprediction count M comes from trace-driven simulation (labs/14-07-lab/bpred.py).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
C14 = ROOT / "courses" / "14-computer-organization-and-architecture"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(C14 / "verify"))
sys.path.insert(0, str(C14 / "labs" / "14-07-lab"))
sys.path.insert(0, str(C14 / "labs" / "14-06-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import bpred  # noqa: E402
import make_program  # noqa: E402
from _rv32 import Sim, build  # noqa: E402
from eeverify import markdown_code_blocks  # noqa: E402

OUT = "assets/figures/14-07"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def lcg(n, seed=12345):
    x, out = seed, []
    for _ in range(n):
        x = (1103515245 * x + 12345) % 2**31
        out.append((x >> 16) % 256)
    return out


def fig_predictors():
    prog = (C14 / "labs" / "14-06-lab" / "program.s").read_text()
    data = {0x2000 + 4 * i + k: ((x & 0xFFFFFFFF) >> 8 * k) & 0xFF for i, x in enumerate(make_program.ARRAY) for k in range(4)}
    ev, n, _ = bpred.trace({"p.s": prog}, data)
    cfgs = [("none", dict(direction="none")), ("2-bit + BTB", dict(direction="2bit")),
            ("2-bit + BTB\n+ RAS", dict(direction="2bit", ras_depth=16)), ("gshare + BTB\n+ RAS", dict(direction="gshare", ras_depth=16))]
    cyc = [n + 4 + 10 + 2 * bpred.simulate(ev, **c)["mispredicts"] for _, c in cfgs]
    assert cyc == [2850, 2348, 2124, 2022]

    head = "    .text\n    .globl _start\n_start:\n    li   sp, 0x4000\n    li   a0, 0x2000\n    li   a1, 1000\n    li   a2, 128\n    call count\n    ebreak\n"
    branchy = ("count:\n    li   t0, 0\n    beqz a1, 3f\n1:  lw   t1, 0(a0)\n    ble  t1, a2, 2f\n    addi t0, t0, 1\n"
               "2:  addi a0, a0, 4\n    addi a1, a1, -1\n    bnez a1, 1b\n3:  mv   a0, t0\n    ret\n")
    branchless = [c for lang, c, _, _ in markdown_code_blocks(C14 / "problems" / "14-07-problems.md") if lang == "asm"][0]
    vals = lcg(1000)

    def cycles15(body, values):
        d = {0x2000 + 4 * i + k: (x >> 8 * k) & 0xFF for i, x in enumerate(values) for k in range(4)}
        e_, n_, _ = bpred.trace({"c.s": head + body}, d)
        mem, _, entry, size = build({"c.s": head + body}, text=0)
        words = [int.from_bytes(bytes(mem[a + k] for k in range(4)), "little") for a in range(0, size, 4)]
        s = Sim({**mem, **d}, entry)
        tr: list = []
        s.run(trace=tr)
        st = make_program.hazard_model(words, [p for p, _ in tr] + [s.pc])["stalls"]
        return n_ + 4 + st + 15 * bpred.simulate(e_, direction="2bit", ras_depth=16)["mispredicts"]

    cyc2 = [cycles15(branchy, vals), cycles15(branchy, sorted(vals)), cycles15(branchless, vals)]
    assert cyc2 == [14090, 6620, 6059]

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.0, 3.4), gridspec_kw=dict(width_ratios=[4, 3]))
    ax.bar(range(4), cyc, color=[PALETTE[7], PALETTE[0], PALETTE[2], PALETTE[1]], alpha=0.8)
    for i, c in enumerate(cyc):
        ax.text(i, c + 30, str(c), ha="center", fontsize=8)
    ax.set_xticks(range(4), [l for l, _ in cfgs], fontsize=7.5)
    ax.set_ylabel("cycles (five-stage pipeline)")
    ax.set_title("Lab program: 1924 instructions", fontsize=9)
    ax.set_ylim(0, 3200)
    bx.bar(range(3), cyc2, color=[PALETTE[1], PALETTE[2], PALETTE[0]], alpha=0.8)
    for i, c in enumerate(cyc2):
        bx.text(i, c + 150, str(c), ha="center", fontsize=8)
    bx.set_xticks(range(3), ["branchy,\nrandom data", "branchy,\nsorted data", "branchless,\nrandom data"], fontsize=7.5)
    bx.set_ylabel("cycles (15-cycle penalty)")
    bx.set_title("Counting elements > 128 in 1000 bytes", fontsize=9)
    bx.set_ylim(0, 16000)
    save(fig, f"{OUT}/predictors.svg")


if __name__ == "__main__":
    fig_predictors()
