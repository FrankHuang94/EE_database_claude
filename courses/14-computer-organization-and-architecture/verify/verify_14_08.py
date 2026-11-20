#!/usr/bin/env python3
"""Verify every number in chapter 14-08, its problem set and its lab.

Independent routes:
- dependence counts, renaming, critical paths and issue timelines of the short code fragments are recomputed here
  from the published assembly text, by a parser, renamer and scheduler written in this file (not the lab's model),
  and the critical paths are cross-checked against the lab model's `critical_path` on simulator traces;
- the lab's trace-driven scheduler (labs/14-08-lab/ooo.py) gives the cycle counts; it is checked against two
  independent limits: with unlimited width and window it finishes exactly 2 cycles (dispatch and retire) after
  the dataflow limit, and as a 1-wide in-order machine its issue cycles equal those of the simple scalar
  recurrence t_i = max(t_{i-1} + 1, operands ready) computed here, plus the 1-cycle dispatch delay;
- every program's result (sums, products, array contents) is checked on the course simulator, so the traces
  are traces of correct programs;
- Little's law is checked inside the model: average occupancy = IPC x average residence time;
- the sizing formulas (Little's law, register counts, comparators, bypass paths) are evaluated directly.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "14-08-lab"))
from eeverify import Verifier, markdown_code_blocks  # noqa: E402
import ooo  # noqa: E402

CH = ROOT / "chapters" / "14-08-out-of-order-and-superscalar.md"
PR = ROOT / "problems" / "14-08-problems.md"
v = Verifier.from_files("14-08", CH, ROOT / "solutions" / "14-08-solutions.md", ROOT / "labs" / "14-08-lab" / "README.md")

LAT = {"lw": 3, "mul": 3, "div": 20}


# ---------------------------------------------------------------------------------------------------------------
# An independent toolkit for short fragments written as "I1: op rd, rs1, rs2" text
def parse(block: str) -> list[tuple[str, str | None, list[str]]]:
    """Return (op, destination or None, sources) for each line of a fragment."""
    out = []
    for line in block.strip().splitlines():
        line = re.sub(r"^\s*I\d+:\s*", "", line).strip()
        op, rest = line.split(None, 1)
        args = [a.strip() for a in rest.split(",")]
        if op in ("lw", "sw"):
            m = re.fullmatch(r"(-?\d+)\((\w+)\)", args[1])
            base = m.group(2)
            out.append((op, args[0], [base]) if op == "lw" else (op, None, [args[0], base]))
        else:
            srcs = [a for a in args[1:] if not re.fullmatch(r"-?\d+", a)]
            out.append((op, args[0], srcs))
    return out


def deps(code) -> tuple[int, int, int]:
    """RAW, WAR, WAW counts under the problem set's conventions."""
    raw = war = waw = 0
    for j, (_, d, srcs) in enumerate(code):
        for s in set(srcs):
            raw += any(code[i][1] == s for i in range(j))
            war += any(code[k][1] == s for k in range(j + 1, len(code)))
        waw += d is not None and any(code[i][1] == d for i in range(j))
    return raw, war, waw


def rename(code, table: dict, free: list) -> tuple[list, dict, int]:
    table, free, out, used = dict(table), list(free), [], 0
    for op, d, srcs in code:
        s = [table.get(r, r) for r in srcs]
        nd = None
        if d is not None:
            nd = free.pop(0)
            used += 1
            table[d] = nd
        out.append((op, nd, s))
    return out, table, used


def ready_times(code, in_order: bool) -> list[int]:
    """Result-ready cycle of each instruction: unlimited out-of-order issue, or single in-order issue."""
    ready: dict = {}
    t_prev, fin = -1, []
    for op, d, srcs in code:
        t = max([ready.get(s, 0) for s in srcs], default=0)
        if in_order:
            t = max(t, t_prev + 1)
        t_prev = t
        r = t + LAT.get(op, 1)
        fin.append(r)
        if d is not None:
            ready[d] = r
    return fin


def scalar_inorder(trace) -> list[int]:
    """Issue cycles of a trace on a 1-wide in-order machine: t_i = max(t_{i-1} + 1, producers ready)."""
    prods = ooo._producers(trace)
    fin, iss, t_prev = [], [], -1
    for i, p in enumerate(prods):
        t = max([fin[j] for j in p] + [t_prev + 1])
        t_prev = t
        iss.append(t)
        fin.append(t + ooo.LAT[trace[i][1]])
    return iss


def run(src, data=None, **kw):
    tr, sim = ooo.dyn_trace({"x.s": src}, data, **kw)
    return tr, sim


S = ooo.schedule

# ---------------------------------------------------------------------------------------------------------------
# Model cross-checks on the three main workloads
inc, sim_inc = run(ooo.INC)
ptr, sim_ptr = run(ooo.PTR, ooo.ptr_data())
src, data = ooo.lab_program()
fib, sim_fib = ooo.dyn_trace(src, data)
v.assert_true("INC adds 3 to all 256 words", all(sim_inc.load(0x2000 + 4 * i, 4) == 3 for i in range(256)))
v.assert_true("linked list sums to 5050", sim_ptr.x[5] == 5050)
v.assert_true("lab program results: sum and fib(10) = 55", sim_fib.load(0x104, 4) == 55)
for name, tr in (("INC", inc), ("PTR", ptr), ("FIB", fib)):
    n = len(tr)
    cp = ooo.critical_path(tr)
    v.assert_true(f"{name}: unlimited machine = dataflow limit + 2", S(tr, width=n, rob=n)["cycles"] == cp + 2)
    v.assert_true(f"{name}: 1-wide in-order issue cycles = scalar recurrence + 1, instruction by instruction",
                  [t - 1 for t in S(tr, width=1, rob=16, in_order=True, detail=True)["issue"]] == scalar_inorder(tr))
    for w, rob in ((2, 64), (4, 64), (8, 256)):
        c = S(tr, width=w, rob=rob)["cycles"]
        v.assert_true(f"{name}: {w}-wide >= max(dataflow, N/w)", c >= max(cp, math.ceil(n / w)))
v.assert_true("trace sizes 901, 402, 1923", (len(inc), len(ptr), len(fib)) == (901, 402, 1923))

# ---------------------------------------------------------------------------------------------------------------
# Examples 1-3: the fragment
frag_text = [c for lang, c, _, _ in markdown_code_blocks(CH) if lang == "text"][0]
frag = parse(frag_text)
raw, war, waw = deps(frag)
v.check("Ex 14-08.1a", raw)
v.check("Ex 14-08.1b", war)
v.check("Ex 14-08.1c", waw)
v.check("Ex 14-08.1d", sum(d is not None for _, d, _ in frag))
fin = ready_times(frag, in_order=False)
v.check("Ex 14-08.2a", max(fin))
v.check("Ex 14-08.2b", len(frag) / max(fin))
v.assert_true("finish times 3, 4, 1, 7, 1, 8", fin == [3, 4, 1, 7, 1, 8])
tr_f, sim_f = run(ooo.FRAG, ooo.words([6]))
blk = tr_f[ooo.FRAG_SETUP:]
v.assert_true("fragment assembled matches the chapter text; model critical path also 8",
              len(blk) == 6 and ooo.critical_path(blk) == max(fin) and sim_f.x[28] == (6 + 5) * (9 - 4))
ren, table, used = rename(frag, {"t1": "p11", "t2": "p12", "t3": "p13"}, [f"p{k}" for k in range(40, 60)])
v.check("Ex 14-08.3a", used)
v.check("Ex 14-08.3b", int(table["t1"][1:]))
v.assert_true("renamed: I4 = mul p43, p41, p42; t2 -> p44, t3 -> p43",
              ren[3] == ("mul", "p43", ["p41", "p42"]) and table["t2"] == "p44" and table["t3"] == "p43")
v.assert_true("after renaming only the 4 true dependences remain", deps(ren)[1:] == (0, 0) and deps(ren)[0] == 4)

# Example 4: the unrolled loop
r = {k: S(inc, **cfg) for k, cfg in {
    "io1": dict(width=1, rob=16, in_order=True), "io2": dict(width=2, rob=16, in_order=True),
    "io4": dict(width=4, rob=64, in_order=True), "oo4": dict(width=4, rob=64),
    "nr4": dict(width=4, rob=64, rename=False), "oo8": dict(width=8, rob=256),
    "w16": dict(width=8, rob=16)}.items()}
v.check("Ex 14-08.4a", r["io1"]["cycles"])
v.check("Ex 14-08.4b", r["io4"]["cycles"])
v.check("Ex 14-08.4c", r["oo4"]["cycles"])
v.check("Ex 14-08.4d", r["oo4"]["ipc"])
v.check("Ex 14-08.4e", r["oo8"]["cycles"])
v.check("Ex 14-08.4f", r["oo8"]["ipc"])
v.check("Ex 14-08.4g", ooo.critical_path(inc))
v.check("Ex 14-08.4h", r["io4"]["cycles"] / r["oo4"]["cycles"])
v.check("Ex 14-08.4i", r["io2"]["cycles"])
v.check("Ex 14-08.4j", r["io1"]["ipc"])
v.check("Ex 14-08.4k", r["io2"]["ipc"])
v.check("Ex 14-08.4l", r["io4"]["ipc"])
v.check("Ex 14-08.4m", r["nr4"]["cycles"])
v.check("Ex 14-08.4n", r["nr4"]["ipc"])
v.check("Ex 14-08.4o", r["w16"]["cycles"])
v.check("Ex 14-08.4p", r["w16"]["ipc"])
v.check("Ex 14-08.4q", math.ceil(len(inc) / 8))
v.assert_true("§3.2: in-order IPC 1.0, 1.7, 2.3 at widths 1, 2, 4",
              [round(r[k]["ipc"], 1) for k in ("io1", "io2", "io4")] == [1.0, 1.7, 2.3])

# Example 5: the linked list
v.check("Ex 14-08.5a", ooo.critical_path(ptr))
p4, p8 = S(ptr, width=4, rob=64), S(ptr, width=8, rob=256)
v.assert_true("pointer chase: 4- and 8-wide equal", p4["cycles"] == p8["cycles"])
v.check("Ex 14-08.5b", p4["cycles"])
v.check("Ex 14-08.5c", p4["ipc"])
v.check("Ex 14-08.5d", S(ptr, width=1, rob=16, in_order=True)["cycles"])
v.assert_true("critical path = 2 (li a0 and its use) + 100 loads x 3", ooo.critical_path(ptr) == 2 + 100 * 3)

# Example 6: window sizing
v.check("Ex 14-08.6a", 4 * 100)
v.check("Ex 14-08.6b", 448 / 8)
v.check("Ex 14-08.6c", 448 / 3)
v.check("Ex 14-08.6d", 448 / 2)

# ---------------------------------------------------------------------------------------------------------------
# Lab
v.check("Lab 14-08.a", ooo.critical_path(inc))
v.check("Lab 14-08.b", ooo.critical_path(ptr))
v.check("Lab 14-08.c", ooo.critical_path(fib))
v.check("Lab 14-08.d", S(inc, width=2, rob=256)["cycles"])
v.check("Lab 14-08.e", S(inc, width=4, rob=16)["cycles"])
v.check("Lab 14-08.f", S(fib, width=4, rob=64)["cycles"])
v.check("Lab 14-08.g", S(fib, width=8, rob=64)["cycles"])
v.check("Lab 14-08.h", S(fib, width=8, rob=256)["cycles"])
v.check("Lab 14-08.i", S(inc, width=8, rob=256, rename=False)["cycles"])
mis = ooo.mispredicted_indices(fib, direction="gshare", ras_depth=16)
mis2 = ooo.mispredicted_indices(fib, direction="2bit", ras_depth=16)
v.check("Lab 14-08.j", len(mis))
v.check("Lab 14-08.k", S(fib, width=8, rob=256, mispredicted=mis, refill=10)["cycles"])
v.check("Lab 14-08.l", S(fib, width=8, rob=256, mispredicted=mis, refill=0)["cycles"])
v.check("Lab 14-08.m", S(fib, width=4, rob=64, in_order=True, mispredicted=mis, refill=10)["cycles"])
v.check("Lab 14-08.n", S(fib, width=8, rob=256, rename=False, mispredicted=mis, refill=10)["cycles"])
v.check("Lab 14-08.o", len(mis2))
v.check("Lab 14-08.p", S(fib, width=8, rob=256, mispredicted=mis2, refill=10)["cycles"])
v.check("Lab 14-08.q", S(fib, width=8, rob=256, rename=False)["cycles"])
v.check("Lab 14-08.r", S(fib, width=8, rob=256)["ipc"])
v.check("Lab 14-08.s", (S(fib, width=8, rob=256, mispredicted=mis, refill=0)["cycles"] - S(fib, width=8, rob=256)["cycles"]) / len(mis))
v.check("Lab 14-08.t", len(fib) / len(mis))
v.assert_true("renaming off costs about a fifth with mispredictions (979/819)", round(979 / 819, 1) == 1.2)
v.assert_true("expected results: INC 459 at 2-wide; widths 1, 2, 4, 8 give 905, 459, 262, 134 with 256 entries",
              [S(inc, width=w, rob=256)["cycles"] for w in (1, 2, 4, 8)] == [905, 459, 262, 134])
v.assert_true("guided exercise: 8-wide linked list 304 cycles, IPC 1.32", round(p8["ipc"], 2) == 1.32)
v.assert_true("predictor counts agree with 14-07 (gshare+RAS 42, 2-bit+RAS 93)", (len(mis), len(mis2)) == (42, 93))

# ---------------------------------------------------------------------------------------------------------------
# Problems
H = ooo.HEAD
# Problem 2: chains and trees
CHAIN = H + "    li a0, 0x2000\n" + "".join(f"    lw t{k}, {4 * k}(a0)\n" for k in range(4)) + \
    "    add t0, t0, t1\n    add t0, t0, t2\n    add t0, t0, t3\n    ebreak\n"
TREE = H + "    li a0, 0x2000\n" + "".join(f"    lw t{k}, {4 * k}(a0)\n" for k in range(4)) + \
    "    add t0, t0, t1\n    add t2, t2, t3\n    add t0, t0, t2\n    ebreak\n"
cps = []
for prog in (CHAIN, TREE):
    tr, sim = run(prog, ooo.words([10, 20, 30, 40]))
    v.assert_true("four-word sum = 100, 7 instructions after setup", sim.x[5] == 100 and len(tr) == 8)
    blkp = tr[1:]
    cps.append(ooo.critical_path(blkp))
v.check("14-08.2a", cps[0])
v.check("14-08.2b", cps[1])
v.check("14-08.2c", 7 / cps[0])
v.check("14-08.2d", 7 / cps[1])


def synth_sum(n: int, tree: bool) -> list:
    """Synthetic trace: n loads into virtual registers 100.., summed as a chain or a balanced tree."""
    tr = [(0, "load", [1], 100 + k, 0, 4 * k) for k in range(n)]
    regs, nxt = [100 + k for k in range(n)], 1000
    if not tree:
        acc = regs[0]
        for r_ in regs[1:]:
            tr.append((0, "alu", [acc, r_], nxt, 0, None))
            acc, nxt = nxt, nxt + 1
    else:
        while len(regs) > 1:
            new = []
            for a, b in zip(regs[::2], regs[1::2]):
                tr.append((0, "alu", [a, b], nxt, 0, None))
                new.append(nxt)
                nxt += 1
            regs = new
    return tr


v.assert_true("synthetic 4-word sums agree with the assembled ones",
              (ooo.critical_path(synth_sum(4, False)), ooo.critical_path(synth_sum(4, True))) == tuple(cps))
v.check("14-08.2e", ooo.critical_path(synth_sum(64, False)))
v.check("14-08.2f", ooo.critical_path(synth_sum(64, True)))
v.assert_true("64-word paths = 3 + 63 and 3 + log2 64",
              ooo.critical_path(synth_sum(64, False)) == 3 + 63 and ooo.critical_path(synth_sum(64, True)) == 3 + 6)

# Problem 3
v.check("14-08.3a", 6 * 40)
v.check("14-08.3b", 512 / 8)
v.check("14-08.3c", 128 / 100)
# Problem 4
v.check("14-08.4a", len(range(14, 21)))

# Problem 5: renaming by hand
blocks = [c for lang, c, _, _ in markdown_code_blocks(PR) if lang == "text"]
p5 = parse(blocks[0])
raw, war, waw = deps(p5)
v.check("14-08.5a", raw)
v.check("14-08.5b", war)
v.check("14-08.5c", waw)
ren5, table5, used5 = rename(p5, {"x5": "p5", "x6": "p6", "x7": "p7", "x8": "p8"}, [f"p{k}" for k in range(32, 64)])
v.check("14-08.5d", used5)
v.check("14-08.5e", int(table5["x5"][1:]))
v.check("14-08.5f", int(table5["x6"][1:]))
v.assert_true("renamed sequence as in the solution",
              ren5 == [("add", "p32", ["p6", "p7"]), ("lw", "p33", ["p32"]), ("add", "p34", ["p33", "p8"]),
                       ("sw", None, ["p34", "p33"]), ("addi", "p35", ["p33"])])

# Problem 6: issue timelines
p6 = parse(blocks[1])
v.check("14-08.6a", max(ready_times(p6, in_order=True)))
v.check("14-08.6b", max(ready_times(p6, in_order=False)))
v.check("14-08.6c", max(ready_times([p6[k] for k in (0, 2, 4, 1, 3, 5)], in_order=True)))
v.assert_true("in-order finish times 3, 4, 7, 8, 11, 12", ready_times(p6, in_order=True) == [3, 4, 7, 8, 11, 12])

# Problem 7: product reduction
PVALS = [2 if i % 8 == 0 else 1 for i in range(128)]
PROD1 = H + """    li a0, 0x2000
    li a1, 128
    li t0, 1
1:  lw   t1, 0(a0)
    mul  t0, t0, t1
    addi a0, a0, 4
    addi a1, a1, -1
    bnez a1, 1b
    ebreak
"""
PROD4 = H + """    li a0, 0x2000
    li a1, 32
    li t0, 1
    li t2, 1
    li t4, 1
    li t6, 1
1:  lw   t1, 0(a0)
    lw   t3, 4(a0)
    lw   t5, 8(a0)
    lw   a2, 12(a0)
    mul  t0, t0, t1
    mul  t2, t2, t3
    mul  t4, t4, t5
    mul  t6, t6, a2
    addi a0, a0, 16
    addi a1, a1, -1
    bnez a1, 1b
    mul  t0, t0, t2
    mul  t4, t4, t6
    mul  t0, t0, t4
    ebreak
"""
t1_, s1_ = run(PROD1, ooo.words(PVALS))
t4_, s4_ = run(PROD4, ooo.words(PVALS))
v.assert_true("both products = 2^16", s1_.x[5] == s4_.x[5] == 2**16)
v.check("14-08.7a", ooo.critical_path(t1_))
v.assert_true("388 = 4 + 128 x 3", ooo.critical_path(t1_) == 4 + 128 * 3)
v.check("14-08.7b", S(t1_, width=4, rob=64)["cycles"])
v.check("14-08.7c", S(t1_, width=8, rob=256)["cycles"])
v.check("14-08.7d", ooo.critical_path(t4_))
v.check("14-08.7e", S(t4_, width=4, rob=64)["cycles"])
v.check("14-08.7f", S(t4_, width=8, rob=256)["cycles"])
v.check("14-08.7g", S(t1_, width=4, rob=64)["cycles"] / S(t4_, width=4, rob=64)["cycles"])
v.assert_true("instruction counts 643 and 361", (len(t1_), len(t4_)) == (643, 361))
v.assert_true("106 = 4 + 32 x 3 + 2 x 3", ooo.critical_path(t4_) == 4 + 32 * 3 + 2 * 3)

# Problem 8: array against list
arr, sim_arr = run(ooo.ARR, ooo.words(list(range(1, 101))))
a4 = S(arr, width=4, rob=64)
v.assert_true("array sum 5050 in 503 instructions", sim_arr.x[5] == 5050 and len(arr) == 503)
v.check("14-08.8a", ooo.critical_path(arr))
v.check("14-08.8b", a4["cycles"])
v.check("14-08.8c", a4["ipc"])
v.check("14-08.8d", p4["cycles"] / a4["cycles"])

# Problem 9: one register for everything
INC1 = H + """    li a0, 0x2000
    li a1, 256
    li a2, 3
    slli t0, a1, 2
    add  t0, a0, t0
1:""" + "".join(f"""    lw   t1, {4 * k}(a0)
    add  t1, t1, a2
    sw   t1, {4 * k}(a0)
""" for k in range(4)) + """    addi a0, a0, 16
    bne  a0, t0, 1b
    ebreak
"""
inc1, sim1 = run(INC1)
v.assert_true("same 901 instructions and same memory result",
              len(inc1) == 901 and all(sim1.load(0x2000 + 4 * i, 4) == 3 for i in range(256)))
v.check("14-08.9a", S(inc1, width=4, rob=64)["cycles"])
v.check("14-08.9b", S(inc1, width=4, rob=64, rename=False)["cycles"])
v.assert_true("four-register version: 262 and 388", (r["oo4"]["cycles"], r["nr4"]["cycles"]) == (262, 388))

# Problem 10: misprediction cost
f4, f4m = S(fib, width=4, rob=64)["cycles"], S(fib, width=4, rob=64, mispredicted=mis, refill=10)["cycles"]
f8, f8m = S(fib, width=8, rob=256)["cycles"], S(fib, width=8, rob=256, mispredicted=mis, refill=10)["cycles"]
v.assert_true("table: 491, 1027, 255, 819", (f4, f4m, f8, f8m) == (491, 1027, 255, 819))
v.check("14-08.10a", (f4m - f4) / len(mis))
v.check("14-08.10b", (f8m - f8) / len(mis))
v.check("14-08.10c", 100 * (f8m - f8) / f8m)

# Problem 11
v.check("14-08.11a", 32 + math.ceil(0.7 * 256))
v.check("14-08.11d", 32 + 256)
v.check("14-08.11e", 31 + 256)
v.check("14-08.11b", 240 - 16)
v.check("14-08.11c", 100 * (240 - 16) / 448)

# Problem 12: recurrence through memory
assert blocks[2].strip().startswith("1:  lw")
REC = H + "    li a0, 0x2000\n    li a1, 256\n" + blocks[2].rstrip() + "\n    ebreak\n"
REG = H + """    li a0, 0x2000
    li a1, 256
    lw   t1, 0(a0)
1:  addi t1, t1, 1
    sw   t1, 4(a0)
    addi a0, a0, 4
    addi a1, a1, -1
    bnez a1, 1b
    ebreak
"""
rec, sim_rec = run(REC, ooo.words([5]))
reg, sim_reg = run(REG, ooo.words([5]))
v.assert_true("both set a[i] = 5 + i; 1538 and 1283 instructions",
              all(sim_rec.load(0x2000 + 4 * i, 4) == 5 + i == sim_reg.load(0x2000 + 4 * i, 4) for i in range(257))
              and (len(rec), len(reg)) == (1538, 1283))
v.check("14-08.12a", 3 + 1 + 1)
v.check("14-08.12b", ooo.critical_path(rec))
v.assert_true("1281 = 1 + 256 x 5", ooo.critical_path(rec) == 1 + 256 * 5)
rc4, rc8 = S(rec, width=4, rob=64)["cycles"], S(rec, width=8, rob=256)["cycles"]
v.assert_true("4- and 8-wide equal", rc4 == rc8)
v.check("14-08.12c", rc4)
v.check("14-08.12d", S(reg, width=4, rob=64)["cycles"])
v.check("14-08.12e", rc4 / S(reg, width=4, rob=64)["cycles"])
v.assert_true("register version: critical path 261, 8-wide 263",
              ooo.critical_path(reg) == 261 and S(reg, width=8, rob=256)["cycles"] == 263)

# Problem 13: window sizing with a divide
dv, sim_dv = run(ooo.DIV, ooo.words(ooo.DIV_VALUES))
v.assert_true("divide loop: 1204 instructions, sum of quotients 19900",
              len(dv) == 1204 and sim_dv.x[5] == sum(x // 7 for x in ooo.DIV_VALUES) == 19900)
L = 1 + 3 + 20 + 1
v.assert_true("L = 25", L == 25)
v.check("14-08.13a", 16 / L)
v.check("14-08.13b", 32 / L)
v.check("14-08.13c", 64 / L)
v.check("14-08.13d", 4 * L)
d = {rob: S(dv, width=4, rob=rob, detail=True) for rob in (16, 32, 64, 128, 256)}
v.check("14-08.13e", d[16]["ipc"])
v.check("14-08.13f", d[32]["ipc"])
v.check("14-08.13g", d[64]["ipc"])
v.check("14-08.13h", d[128]["ipc"])
v.assert_true("256 entries no better than 128", d[256]["cycles"] == d[128]["cycles"])
res = [d[16]["retire"][i] - d[16]["dispatch"][i] for i in range(len(dv))]
avg_res = sum(res) / len(res)
occ = sum(res) / d[16]["cycles"]
v.check("14-08.13i", avg_res)
v.check("14-08.13j", occ)
v.assert_true("Little's law inside the model: occupancy = IPC x residence",
              abs(occ - d[16]["ipc"] * avg_res) < 1e-9 and occ <= 16)
v.assert_true("divide-loop: loads and branches stay about 18 cycles in the 16-entry window",
              round(sum(res[i] for i, t in enumerate(dv) if t[1] == "load") / 200) == 18)

# Problem 14
v.check("14-08.14a", 2 * 4 * 48)
v.check("14-08.14b", 2 * 8 * 96)
v.check("14-08.14c", 2 * 4**2)
v.check("14-08.14d", 2 * 8**2)

# ---------------------------------------------------------------- Problem 15: a Tomasulo table, from its stated rules
TOMA = [("lw", "x1", ["x10"]), ("mul", "x2", ["x1", "x3"]), ("add", "x4", ["x2", "x5"]),
        ("lw", "x6", ["x10"]), ("sub", "x1", ["x6", "x9"]), ("add", "x7", ["x1", "x4"])]
TLAT = {"lw": 2, "mul": 4, "add": 1, "sub": 1}


def tomasulo(prog, cdbs=1):
    producer: dict = {}                     # register -> index of the latest instruction writing it (renaming)
    srcs, issue = [], []
    for k, (op, rd, rs) in enumerate(prog):
        issue.append(k + 1)
        srcs.append([producer.get(r) for r in rs])
        producer[rd] = k
    start, end, cdb = [None] * len(prog), [None] * len(prog), [None] * len(prog)
    cycle = 0
    while None in cdb:
        cycle += 1
        for k in range(len(prog)):           # start execution
            if start[k] is None and cycle > issue[k] and all(p is None or (cdb[p] is not None and cdb[p] < cycle) for p in srcs[k]):
                start[k], end[k] = cycle, cycle + TLAT[prog[k][0]] - 1
        ready = [k for k in range(len(prog)) if end[k] is not None and end[k] < cycle and cdb[k] is None]
        for k in sorted(ready)[:cdbs]:        # oldest first
            cdb[k] = cycle
    return issue, start, end, cdb


iss, st, en, cdb1 = tomasulo(TOMA)
for key, k in zip("abcde", range(5)):
    v.check(f"14-08.15{key}", cdb1[k])
v.check("14-08.15f", max(cdb1))
_, _, _, cdb2 = tomasulo(TOMA, cdbs=2)
v.check("14-08.15g", cdb2[4])
v.check("14-08.15h", max(cdb2))
sol_txt = (ROOT / "solutions" / "14-08-solutions.md").read_text(encoding="utf-8")
trows = re.findall(r"^\| (\d) \| `[^`]+` \| (\d+) \| (\d+)–(\d+) \| (\d+) \|$", sol_txt.split("<!-- tomasulo table -->")[1], re.M)
v.assert_true("Solution 15's table matches the simulator row by row",
              [tuple(int(x) for x in row) for row in trows] == [(k + 1, iss[k], st[k], en[k], cdb1[k]) for k in range(6)])

# ---------------------------------------------------------------- Problem 16: VLIW packing, by exhaustive search and a schedule checker


def vliw_min(k):
    ops = [("lw", i) for i in range(k)] + [("add", i) for i in range(k)] + [("addi", 0), ("bne", 0)]
    for K in range(1, 3 * k + 6):
        def ok(a):
            alu = [b for (t, _), b in a.items() if t != "lw"]
            ls = [b for (t, _), b in a.items() if t == "lw"]
            if len(set(alu)) < len(alu) or len(set(ls)) < len(ls):
                return False
            for (t, i), b in a.items():
                if t == "add" and (("lw", i) in a and b < a[("lw", i)] + 2 or i and ("add", i - 1) in a and b < a[("add", i - 1)] + 1):
                    return False
                if t == "bne" and (b != K or ("addi", 0) in a and b < a[("addi", 0)] + 1):
                    return False
            return True

        def dfs(n, a):
            if n == len(ops):
                return True
            for b in range(1, K + 1):
                a[ops[n]] = b
                if ok(a) and dfs(n + 1, a):
                    return True
                del a[ops[n]]
            return False

        if dfs(0, {}):
            return K
    return None


def check_schedule(marker, k):
    """Parse a published bundle table and check slots, latencies, the branch position and the load offsets."""
    block = sol_txt.split(marker)[1].lstrip("\n").split("\n\n")[0]      # the table right after the marker
    rows = re.findall(r"^\| (\d+) \| (.+?) \| (.+?) \|$", block, re.M)
    where, offs = {}, {}
    for b, alu, ls in rows:
        b = int(b)
        a_op, l_op = alu.strip("` "), ls.strip("` ")
        if a_op.startswith("addi"):
            where["addi"] = b
        elif a_op.startswith("add"):
            where[("add", int(a_op.split("t")[-1]))] = b
        elif a_op.startswith("bne"):
            where["bne"] = b
        if l_op.startswith("lw"):
            m = re.match(r"lw t(\d), (-?\d+)\(a0\)", l_op)
            where[("lw", int(m.group(1)))] = b
            offs[int(m.group(1))] = int(m.group(2))
    n = len(rows)
    good = where.get("bne") == n and where["bne"] > where["addi"]
    for i in range(k):
        good &= where[("add", i)] >= where[("lw", i)] + 2
        good &= i == 0 or where[("add", i)] > where[("add", i - 1)]
        good &= offs[i] == 4 * i - (4 * k if where[("lw", i)] > where["addi"] else 0)
    return n, good


for k, mark, keys in ((1, "<!-- vliw schedule 1 -->", ("16a",)), (2, "<!-- vliw schedule 2 -->", ("16b", "16c")),
                      (4, "<!-- vliw schedule 4 -->", ("16d", "16e"))):
    n_pub, good = check_schedule(mark, k)
    best = vliw_min(k)
    v.assert_true(f"unroll {k}: the published schedule is legal (slots, latencies, branch last, offsets) and optimal",
                  good and n_pub == best, f"published {n_pub}, minimum {best}")
    if k == 1:
        v.check("14-08.16a", best)
    else:
        v.check(f"14-08.{keys[0]}", best)
        v.check(f"14-08.{keys[1]}", best / k)
v.check("14-08.16f", vliw_min(1) / (vliw_min(4) / 4))
v.assert_true("bundles = k + 3 for k = 2 and 4, so bundles per element tend to 1", all(vliw_min(k) == k + 3 for k in (2, 4)))
v.check("14-08.16g", 1)

sys.exit(v.finish())
