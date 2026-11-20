"""Trace-driven models of in-order and out-of-order superscalar execution for Lab 14-08.

`dyn_trace(...)` runs a program on the course's RV32IM simulator and returns its dynamic instructions with their
register sources and destination, latency class and next PC. `schedule(...)` replays them through a simple
machine model (chapter 14-08, Section 3):

- up to `width` instructions are fetched and dispatched per cycle, in program order, into a reorder buffer (ROB)
  of `rob` entries; dispatch stops while the ROB is full;
- an instruction may issue once its source operands are ready; at most `width` instructions issue per cycle,
  oldest first; `in_order=True` forbids issuing past an older instruction that has not issued;
- without renaming (`rename=False`), an instruction must also wait for older readers (WAR) and writers (WAW) of its
  destination register to finish with it;
- results are available `latency` cycles after issue; completed instructions retire in order, `width` per cycle;
- a load depends on the most recent older store to the same word (memory RAW), as with perfect memory
  disambiguation: independent loads may pass stores, dependent ones wait for the store's data;
- a mispredicted control transfer (from `mispredicted`, a set of trace indices) stops fetch until it resolves, and
  fetch restarts `refill` cycles later.

`critical_path(...)` gives the dataflow limit: the longest chain of true (read-after-write) dependences.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verify"))
from _rv32 import Sim, build  # noqa: E402

LAT = dict(alu=1, load=3, store=1, branch=1, mul=3, div=20)


def classify(w: int) -> tuple[str, list[int], int]:
    """Return (class, source registers, destination register or 0) for an RV32IM instruction word."""
    op, rd, f3, rs1, rs2, f7 = w & 0x7F, w >> 7 & 31, w >> 12 & 7, w >> 15 & 31, w >> 20 & 31, w >> 25
    if op == 0x33:
        cls = ("div" if f3 >= 4 else "mul") if f7 == 1 else "alu"
        return cls, [rs1, rs2], rd
    if op == 0x13:
        return "alu", [rs1], rd
    if op == 0x03:
        return "load", [rs1], rd
    if op == 0x23:
        return "store", [rs1, rs2], 0
    if op == 0x63:
        return "branch", [rs1, rs2], 0
    if op == 0x6F:
        return "branch", [], rd
    if op == 0x67:
        return "branch", [rs1], rd
    if op in (0x37, 0x17):
        return "alu", [], rd
    return "alu", [], 0


def dyn_trace(sources: dict[str, str], data: dict | None = None, regs: dict | None = None, m: bool = True):
    """Run a program (defining _start, ending with EBREAK); return (list of (pc, cls, srcs, dst, word, addr),
    sim), where addr is the word address of a load or store (else None)."""
    mem, syms, entry, size = build(sources, text=0, m=m)
    sim = Sim({**mem, **(data or {})}, entry, regs=regs)
    tr: list = []
    mt: list = []
    sim.run(trace=tr, mtrace=mt, limit=10**8)
    word = lambda a: int.from_bytes(bytes(sim.mem.get(a + k, 0) for k in range(4)), "little")  # noqa: E731
    out = []
    mi = 0
    for pc, _ in tr:
        w = word(pc)
        cls, srcs, dst = classify(w)
        addr = None
        if cls in ("load", "store"):
            assert mt[mi][0] == pc
            addr = mt[mi][1] & ~3
            mi += 1
        out.append((pc, cls, [s for s in srcs if s], dst, w, addr))
    return out, sim


def mispredicted_indices(trace, **predictor) -> frozenset:
    """Trace indices of control transfers mispredicted by a 14-07 predictor model (direction, ras_depth, ...)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "14-07-lab"))
    import bpred
    pcs = [t[0] for t in trace]
    word = {t[0]: t[4] for t in trace}
    mem = {pc + k: (w >> 8 * k) & 0xFF for pc, w in word.items() for k in range(4)}
    ctl = [i for i, t in enumerate(trace) if t[1] == "branch"]
    events = bpred.events_from(mem, pcs + [pcs[-1] + 4])
    flags: list = []
    bpred.simulate(events, flags=flags, **predictor)
    assert len(flags) == len(ctl)
    return frozenset(i for i, f in zip(ctl, flags) if f)


def _producers(trace):
    """For each instruction: its RAW producers through registers and through memory (last store to the word)."""
    last_w, last_st, prods = {}, {}, []
    for i, (_, cls, srcs, dst, _, addr) in enumerate(trace):
        p = [last_w[s] for s in srcs if s in last_w]
        if cls == "load" and addr in last_st:
            p.append(last_st[addr])
        prods.append(p)
        if dst:
            last_w[dst] = i
        if cls == "store":
            last_st[addr] = i
    return prods


def critical_path(trace, lat=LAT, lat_of: dict | None = None) -> int:
    """Cycles to execute the trace with unlimited resources and perfect prediction: the longest chain of true
    (read-after-write) dependences, through registers and through memory. `lat_of` optionally overrides the
    latency of individual instructions (trace index -> cycles), for example loads that miss in a cache."""
    lat_of = lat_of or {}
    fin = []
    for i, p in enumerate(_producers(trace)):
        fin.append(max((fin[j] for j in p), default=0) + lat_of.get(i, lat[trace[i][1]]))
    return max(fin, default=0)


def schedule(trace, width=4, rob=64, in_order=False, rename=True, lat=LAT, mispredicted=frozenset(), refill=0,
             detail=False, lat_of: dict | None = None) -> dict:
    """Replay `trace` through the machine model described in the module docstring; return cycles, instr, ipc and,
    with detail=True, each instruction's dispatch, issue, done and retire cycles. `lat_of` optionally overrides
    individual instructions' latencies (trace index -> cycles)."""
    lat_of = lat_of or {}
    n = len(trace)
    issue = [None] * n
    done = [None] * n
    disp = [None] * n
    ret = [None] * n
    # producer index for each source (RAW), and for no-renaming the WAR/WAW predecessors
    last_w = {}
    readers = {}
    prod, falsedeps = _producers(trace), []
    for i, (_, _, srcs, dst, _, _) in enumerate(trace):
        fd = []
        if not rename and dst:
            if dst in last_w:
                fd.append(last_w[dst])                      # WAW: older writer must complete first
            fd += readers.get(dst, [])                      # WAR: older readers must have issued (read) first
        falsedeps.append(fd)
        for s in srcs:
            readers.setdefault(s, []).append(i)
        if dst:
            last_w[dst] = i
            readers[dst] = []
    cycle = 0
    fetched = retired = 0
    window: list[int] = []
    fetch_block_until = 0
    pending_branch = None
    while retired < n:
        # retire (in order) up to width completed instructions
        r = 0
        while window and r < width and done[window[0]] is not None and done[window[0]] <= cycle:
            ret[window.pop(0)] = cycle
            retired += 1
            r += 1
        # issue
        issued = 0
        blocked = False
        for i in window:
            if issue[i] is not None:
                continue
            ok = all(done[p] is not None and done[p] <= cycle for p in prod[i])
            for p in falsedeps[i]:
                if issue[p] is None or (trace[p][3] == trace[i][3] and (done[p] is None or done[p] > cycle)):
                    ok = False                              # WAR: reader must have issued; WAW: writer done
            if ok and not (in_order and blocked):
                issue[i] = cycle
                done[i] = cycle + lat_of.get(i, lat[trace[i][1]])
                issued += 1
                if issued == width:
                    break
            elif in_order:
                blocked = True
                break
        # fetch / dispatch
        if pending_branch is not None and done[pending_branch] is not None and done[pending_branch] <= cycle:
            fetch_block_until = done[pending_branch] + refill
            pending_branch = None
        if pending_branch is None and cycle >= fetch_block_until:
            d = 0
            while fetched < n and d < width and len(window) < rob:
                window.append(fetched)
                disp[fetched] = cycle
                if fetched in mispredicted:
                    pending_branch = fetched
                    fetched += 1
                    break
                fetched += 1
                d += 1
        cycle += 1
    out = dict(cycles=cycle, instr=n, ipc=n / cycle)
    if detail:
        out.update(dispatch=disp, issue=issue, done=done, retire=ret)
    return out


# ---------------------------------------------------------------------------------------------------------------
# Workloads used in chapter 14-08, its problems and its lab
HEAD = "    .text\n    .globl _start\n_start:\n"

FRAG = HEAD + """    li a0, 0x2000
    li a1, 5
    li a2, 9
    li a3, 4
    li a4, 7
    lw   t1, 0(a0)
    add  t2, t1, a1
    sub  t1, a2, a3
    mul  t3, t2, t1
    addi t2, a4, 1
    sw   t3, 4(a0)
    ebreak
"""
FRAG_SETUP = 5          # the five li instructions before the fragment

INC = HEAD + """    li a0, 0x2000
    li a1, 256
    li a2, 3
    slli t0, a1, 2
    add  t0, a0, t0
1:  lw   t1, 0(a0)
    lw   t2, 4(a0)
    lw   t3, 8(a0)
    lw   t4, 12(a0)
    add  t1, t1, a2
    add  t2, t2, a2
    add  t3, t3, a2
    add  t4, t4, a2
    sw   t1, 0(a0)
    sw   t2, 4(a0)
    sw   t3, 8(a0)
    sw   t4, 12(a0)
    addi a0, a0, 16
    bne  a0, t0, 1b
    ebreak
"""

PTR = HEAD + """    li a0, 0x2000
    li t0, 0
1:  lw t1, 4(a0)
    lw a0, 0(a0)
    add t0, t0, t1
    bnez a0, 1b
    ebreak
"""

ARR = HEAD + """    li a0, 0x2000
    li a1, 100
    li t0, 0
1:  lw   t1, 0(a0)
    add  t0, t0, t1
    addi a0, a0, 4
    addi a1, a1, -1
    bnez a1, 1b
    ebreak
"""

DIV = HEAD + """    li a0, 0x2000
    li a1, 200
    li a2, 7
    li t0, 0
1:  lw   t1, 0(a0)
    div  t2, t1, a2
    add  t0, t0, t2
    addi a0, a0, 4
    addi a1, a1, -1
    bnez a1, 1b
    ebreak
"""
DIV_VALUES = [7 * i + 3 for i in range(200)]


def words(values: list[int], base: int = 0x2000) -> dict:
    """Byte-addressed memory image of 32-bit words starting at `base`."""
    return {base + 4 * i + k: ((x & 0xFFFFFFFF) >> 8 * k) & 0xFF for i, x in enumerate(values) for k in range(4)}


def ptr_data(n: int = 100, base: int = 0x2000) -> dict:
    """A linked list of n nodes at base + 8i, each [next, value = i + 1]; the last next is 0."""
    vals: list[int] = []
    for i in range(n):
        vals += [base + 8 * (i + 1) if i < n - 1 else 0, i + 1]
    return words(vals, base)


def lab_program() -> tuple[dict, dict]:
    """The recursive-Fibonacci lab program of 14-06 and 14-07, with its data array."""
    lab = Path(__file__).resolve().parents[1] / "14-06-lab"
    sys.path.insert(0, str(lab))
    import make_program
    return {"p.s": (lab / "program.s").read_text()}, words(make_program.ARRAY)
