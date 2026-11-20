"""Trace-driven branch-prediction models for Lab 14-07.

`trace(...)` runs a program on the course's RV32I simulator and returns its dynamic control-flow events.
`simulate(events, ...)` replays them through a predictor and counts the fetches whose predicted next PC was wrong.
The models follow chapter 14-07, Section 3: a direction predictor (static or table-based) consulted in IF, a
branch target buffer (BTB) that supplies targets, and an optional return-address stack (RAS) for returns.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verify"))
from _rv32 import Sim, build  # noqa: E402


@dataclass
class Event:
    pc: int
    kind: str        # "br" (conditional), "jal", "jalr"
    taken: bool
    target: int      # actual next PC if taken (for jal/jalr: the jump target)
    next_pc: int     # actual next PC
    call: bool       # writes ra (a call)
    ret: bool        # jalr x0, 0(ra) (a return)


def sx(x, b):
    return x - (1 << b) if x >> (b - 1) & 1 else x


def events_from(mem: dict, pcs: list[int]) -> list[Event]:
    ev = []
    word = lambda a: int.from_bytes(bytes(mem.get(a + k, 0) for k in range(4)), "little")  # noqa: E731
    for k in range(len(pcs) - 1):
        pc, nxt = pcs[k], pcs[k + 1]
        w = word(pc)
        op, rd, rs1 = w & 0x7F, w >> 7 & 31, w >> 15 & 31
        if op == 0x63:
            imm = sx((w >> 31 & 1) << 12 | (w >> 7 & 1) << 11 | (w >> 25 & 0x3F) << 5 | (w >> 8 & 0xF) << 1, 13)
            tgt = (pc + imm) & 0xFFFFFFFF
            ev.append(Event(pc, "br", nxt == tgt and tgt != pc + 4, tgt, nxt, False, False))
        elif op == 0x6F:
            ev.append(Event(pc, "jal", True, nxt, nxt, rd == 1, False))
        elif op == 0x67:
            ev.append(Event(pc, "jalr", True, nxt, nxt, rd == 1, rd == 0 and rs1 == 1 and (w >> 20) == 0))
    return ev


def trace(sources: dict[str, str], data: dict | None = None, regs: dict | None = None, opt: str = "-O2"):
    """Build and run a program that defines _start and ends with EBREAK; return (events, instructions)."""
    mem, syms, entry, size = build(sources, text=0, opt=opt)
    sim = Sim({**mem, **(data or {})}, entry, regs=regs)
    tr: list = []
    n = sim.run(trace=tr, limit=10**8)
    pcs = [pc for pc, _ in tr] + [sim.pc]
    return events_from(sim.mem, pcs), n + 1, sim


class TwoBit:
    """A table of 2-bit saturating counters (0, 1 = predict not taken; 2, 3 = predict taken)."""
    def __init__(self, entries: int, init: int = 1):
        self.t = [init] * entries
        self.n = entries

    def predict(self, i):
        return self.t[i % self.n] >= 2

    def update(self, i, taken):
        j = i % self.n
        self.t[j] = min(3, self.t[j] + 1) if taken else max(0, self.t[j] - 1)


def simulate(events: list[Event], direction: str = "2bit", entries: int = 1024, hist_bits: int = 8,
             btb_entries: int = 64, ras_depth: int = 0) -> dict:
    """Count mispredicted fetches. direction: 'none' (always PC + 4), 'nt' (static not taken), 'btfn' (backward
    taken, forward not taken), '1bit', '2bit', 'gshare'. Targets come from a direct-mapped BTB (full-PC tags);
    returns use the RAS if ras_depth > 0."""
    btb: dict[int, tuple[int, int]] = {}
    one = [False] * entries
    two = TwoBit(entries)
    ghr = 0
    ras: list[int] = []
    mis = dir_wrong = br = 0
    for e in events:
        idx = e.pc >> 2
        slot = idx % btb_entries
        hit = slot in btb and btb[slot][0] == e.pc
        btb_t = btb[slot][1] if hit else None
        # ---- predicted next PC
        if direction == "none":
            pred_taken = False
        elif e.kind != "br":
            pred_taken = True
        elif direction == "nt":
            pred_taken = False
        elif direction == "btfn":
            pred_taken = e.target < e.pc
        elif direction == "1bit":
            pred_taken = one[idx % entries]
        elif direction == "2bit":
            pred_taken = two.predict(idx)
        else:  # gshare
            pred_taken = two.predict(idx ^ (ghr & ((1 << hist_bits) - 1)))
        if pred_taken and e.ret and ras_depth and ras:
            pnext = ras[-1]
        elif pred_taken and direction != "none" and hit:
            pnext = btb_t
        elif pred_taken and direction in ("btfn",) and e.kind == "br":
            pnext = e.target          # BTFN computes the target from the instruction (predecode)
        else:
            pnext = e.pc + 4
        mis += pnext != e.next_pc
        if e.kind == "br":
            br += 1
            dir_wrong += pred_taken != e.taken
        # ---- update
        if e.kind == "br":
            if direction == "1bit":
                one[idx % entries] = e.taken
            elif direction == "2bit":
                two.update(idx, e.taken)
            elif direction == "gshare":
                two.update(idx ^ (ghr & ((1 << hist_bits) - 1)), e.taken)
            ghr = ((ghr << 1) | int(e.taken)) & 0xFFFFFFFF
        if e.taken:
            btb[slot] = (e.pc, e.target)
        if ras_depth:
            if e.ret and ras:
                ras.pop()
            if e.call:
                ras.append(e.pc + 4)
                if len(ras) > ras_depth:
                    ras.pop(0)
    return dict(mispredicts=mis, branches=br, dir_wrong=dir_wrong, events=len(events))
