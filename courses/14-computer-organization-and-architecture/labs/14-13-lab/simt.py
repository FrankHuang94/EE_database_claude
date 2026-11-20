"""Small models of SIMT execution for Lab 14-13.

- `run_warp(program, lanes=32)` executes a structured per-lane program on a SIMT warp with an active mask: each
  ("op", n) costs n issue slots for the whole warp; ("if", pred, then_body, else_body) runs each side only if some
  lane takes it, with the other lanes masked off; ("loop", trips, body) iterates while any lane still has trips
  left. It returns the warp's issue slots and the useful lane-slots, whose ratio is the SIMD efficiency.
- `sectors(addrs, size=32)` counts the distinct memory sectors (or segments) a warp's addresses touch.
- `bank_conflict(word_indices, banks=32)` is the worst number of distinct words requested from one shared-memory
  bank, i.e. how many serialized passes the access needs.
- `occupancy(...)` gives resident warps per SM and the limiting resource; `warps_to_hide(latency, k)` is the
  Little's-law estimate of warps a scheduler needs when each warp issues k instructions between long waits.
"""
from __future__ import annotations

import math


def run_warp(program, lanes: int = 32) -> tuple[int, int]:
    def run(prog, mask):
        slots = useful = 0
        for stmt in prog:
            kind = stmt[0]
            if kind == "op":
                if any(mask):
                    slots += stmt[1]
                    useful += stmt[1] * sum(mask)
            elif kind == "if":
                _, pred, then_b, else_b = stmt
                tmask = [m and pred(i) for i, m in enumerate(mask)]
                emask = [m and not pred(i) for i, m in enumerate(mask)]
                for sub, sm in ((then_b, tmask), (else_b, emask)):
                    if any(sm):
                        s, u = run(sub, sm)
                        slots += s
                        useful += u
            elif kind == "loop":
                _, trips, body = stmt
                it = 0
                while True:
                    lm = [m and trips(i) > it for i, m in enumerate(mask)]
                    if not any(lm):
                        break
                    s, u = run(body, lm)
                    slots += s
                    useful += u
                    it += 1
        return slots, useful

    return run(program, [True] * lanes)


def efficiency(program, lanes: int = 32) -> float:
    slots, useful = run_warp(program, lanes)
    return useful / (slots * lanes)


def sectors(addrs, size: int = 32) -> int:
    return len({a // size for a in addrs})


def bank_conflict(word_indices, banks: int = 32) -> int:
    per_bank: dict = {}
    for w in word_indices:
        per_bank.setdefault(w % banks, set()).add(w)
    return max(len(s) for s in per_bank.values())


def occupancy(regs_per_thread: int, threads_per_block: int, smem_per_block: int, *, regs_per_sm: int = 65536,
              smem_per_sm: int = 196608, max_warps: int = 64, max_blocks: int = 32) -> tuple[int, str]:
    """Resident warps per SM and the resource that limits them (register allocation granularity ignored)."""
    warps_per_block = math.ceil(threads_per_block / 32)
    limits = {
        "registers": regs_per_sm // (regs_per_thread * threads_per_block),
        "shared memory": smem_per_sm // smem_per_block if smem_per_block else max_blocks,
        "warp slots": max_warps // warps_per_block,
        "block slots": max_blocks,
    }
    # on a tie, report the hardware's fixed limits first (the kernel is not what is holding occupancy back)
    priority = ["warp slots", "block slots", "registers", "shared memory"]
    name = min(limits, key=lambda k: (limits[k], priority.index(k)))
    return limits[name] * warps_per_block, name


def warps_to_hide(latency: float, instructions_between: float) -> int:
    """Warps one scheduler (1 instruction per cycle) needs so it can always issue: each warp is busy for k cycles,
    then waits `latency`, so N k >= k + latency."""
    return math.ceil(1 + latency / instructions_between)
