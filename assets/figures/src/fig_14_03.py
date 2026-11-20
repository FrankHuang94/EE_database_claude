#!/usr/bin/env python3
"""Figures for chapter 14-03 (assembly and the compilation stack).

Run from anywhere:  python assets/figures/src/fig_14_03.py   (needs LLVM: llvm-mc, ld.lld)
Outputs SVGs to assets/figures/14-03/:
- fib-stack.svg: the stack depth, in bytes below the initial stack pointer, after every instruction of the
  hand-written recursive fib(6) of Example 14-03.4, linked with LLD and executed on the course's RV32I
  simulator (courses/14-.../verify/_rv32.py). Each rise is a frame being allocated by a call, each fall a
  return; the peak is 16(n - 1) = 80 bytes.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "14-computer-organization-and-architecture" / "verify"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
from _rv32 import START, Sim, build  # noqa: E402

OUT = "assets/figures/14-03"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)


def fig_fib_stack(n: int = 6):
    fib = (ROOT / "courses/14-computer-organization-and-architecture/labs/14-03-lab/fib.s").read_text()
    mem, syms, entry, _ = build({"start.s": START.format(body=f"    li   a0, {n}\n    call fib"), "fib.s": fib})
    sim = Sim(mem, entry)
    trace: list = []
    sim.run(trace=trace)
    start = next(i for i, (pc, _) in enumerate(trace) if pc == syms["fib"])  # skip the start-up stub
    depth = [0x80000 - sp for _, sp in trace[start:]]
    F = [0, 1]
    while len(F) <= n + 1:
        F.append(F[-1] + F[-2])
    assert max(depth) == 16 * (n - 1) and sim.x[10] == F[n] and len(depth) == 21 * F[n + 1] - 18
    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    ax.step(range(1, len(depth) + 1), depth, where="post", color=PALETTE[0], lw=1.2)
    ax.axhline(16 * (n - 1), color=PALETTE[1], ls=":", lw=1)
    ax.text(len(depth) * 0.99, 16 * (n - 1) + 2, f"peak 16(n − 1) = {16 * (n - 1)} bytes", ha="right", va="bottom", fontsize=8, color=PALETTE[1])
    ax.set_xlabel("instructions executed inside fib")
    ax.set_ylabel("stack depth (bytes)")
    ax.set_title(f"Stack depth during the recursive fib({n}) = {sim.x[10]}: {len(depth)} instructions, {sim.calls[syms['fib']]} calls", fontsize=9)
    ax.set_ylim(0, 16 * (n - 1) + 16)
    ax.set_xlim(0, len(depth) + 1)
    save(fig, f"{OUT}/fib-stack.svg")


if __name__ == "__main__":
    fig_fib_stack()
