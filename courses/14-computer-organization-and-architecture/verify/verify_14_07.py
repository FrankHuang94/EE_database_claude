#!/usr/bin/env python3
"""Verify every number in chapter 14-07, its problem set and its lab.

Independent routes:
- control-flow traces are collected by running programs on the course RV32I simulator (_rv32.py) and replayed
  through the predictor models of labs/14-07-lab/bpred.py; the models themselves are cross-checked against
  hand-traced sequences and closed-form steady-state accuracies;
- load-use stalls come from 14-06's hazard model, and the no-prediction cycle count of the lab program equals
  the 2850 cycles measured on the Verilog pipeline in 14-06;
- the masking, storage and CPI formulas are evaluated directly.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "labs" / "14-07-lab"))
sys.path.insert(0, str(ROOT / "labs" / "14-06-lab"))
from eeverify import Verifier, markdown_code_blocks  # noqa: E402
from _rv32 import Sim, build  # noqa: E402
import bpred  # noqa: E402
import make_program  # noqa: E402

CH = ROOT / "chapters" / "14-07-branch-prediction-and-speculation.md"
PR = ROOT / "problems" / "14-07-problems.md"
v = Verifier.from_files("14-07", CH, ROOT / "solutions" / "14-07-solutions.md", ROOT / "labs" / "14-07-lab" / "README.md")

LOOP = "    .text\n    .globl _start\n_start:\n    li t2, 100\n1:  li t1, {trip}\n2:  addi t1, t1, -1\n    bnez t1, 2b\n    addi t2, t2, -1\n    bnez t2, 1b\n    ebreak\n"


def acc(r):
    return 100 * (1 - r["dir_wrong"] / r["branches"])


# Example 1 and 2: trip-10 inner loop run 100 times
ev10, _, _ = bpred.trace({"l.s": LOOP.format(trip=10)})
inner = [e for e in ev10 if e.kind == "br" and e.target < e.pc and e.pc == min(x.pc for x in ev10 if x.kind == "br")]
v.assert_true("inner branch: 1000 executions, 900 taken", len(inner) == 1000 and sum(e.taken for e in inner) == 900)
v.check("Ex 14-07.1a", acc(bpred.simulate(inner, direction="nt")))
v.check("Ex 14-07.1b", acc(bpred.simulate(inner, direction="btfn")))
v.check("Ex 14-07.1c", bpred.simulate(ev10, direction="btfn")["mispredicts"])
v.assert_true("predict-not-taken totals 999 of 1100", bpred.simulate(ev10, direction="nt")["mispredicts"] == 999)
r1, r2 = bpred.simulate(ev10, direction="1bit"), bpred.simulate(ev10, direction="2bit")
v.check("Ex 14-07.2a", (bpred.simulate(inner, direction="1bit")["dir_wrong"]) // 100)
v.check("Ex 14-07.2b", round(bpred.simulate(inner, direction="2bit")["dir_wrong"] / 100))
v.check("Ex 14-07.2c", r1["mispredicts"])
v.check("Ex 14-07.2d", r2["mispredicts"])
flags2: list = []
bpred.simulate(ev10, direction="2bit", flags=flags2)
pc_in = min(e.pc for e in ev10 if e.kind == "br")
wrong_in = [i for i, (e, f) in enumerate(zip(ev10, flags2)) if f and e.pc == pc_in]
wrong_out = [i for i, (e, f) in enumerate(zip(ev10, flags2)) if f and e.kind == "br" and e.pc != pc_in]
v.assert_true("2-bit extras: inner warm-up once (its first execution), outer warm-up once and the outer exit once",
              len(wrong_in) == 101 and wrong_in[0] == 0 and len(wrong_out) == 2 and wrong_out[-1] == len(ev10) - 1)

ev4, _, _ = bpred.trace({"l.s": LOOP.format(trip=4)})
r2b, rg = bpred.simulate(ev4, direction="2bit"), bpred.simulate(ev4, direction="gshare", hist_bits=8)
v.check("Ex 14-07.3a", r2b["mispredicts"])
v.check("Ex 14-07.3b", 100 * (1 - r2b["mispredicts"] / r2b["branches"]))
v.check("Ex 14-07.3c", rg["mispredicts"])
v.check("Ex 14-07.3d", 100 * (1 - rg["mispredicts"] / rg["branches"]))

for ID, a in (("Ex 14-07.4a", 0.90), ("Ex 14-07.4b", 0.95), ("Ex 14-07.4c", 0.99)):
    v.check(ID, 1 + 0.2 * (1 - a) * 15)
v.check("Ex 14-07.4d", (1 + 0.2 * 0.05 * 15) / (1 + 0.2 * 0.01 * 15))

# Example 5 and the lab: the lab program
prog = (ROOT / "labs" / "14-06-lab" / "program.s").read_text()
arr = make_program.ARRAY
data = {0x2000 + 4 * i + k: ((x & 0xFFFFFFFF) >> 8 * k) & 0xFF for i, x in enumerate(arr) for k in range(4)}
ev, n, sim = bpred.trace({"p.s": prog}, data)
N, S = n, 10
v.assert_true("lab program: N = 1924; 554 transfers (188 branches, 178 calls, 178 returns), 456 taken",
              N == 1924 and len(ev) == 554 and sum(e.kind == "br" for e in ev) == 188 and sum(e.call for e in ev) == 178
              and sum(e.ret for e in ev) == 178 and sum(e.taken for e in ev) == 456)
v.check("Ex 14-07.5g", len(ev))
v.check("Ex 14-07.5h", sum(e.kind == "br" for e in ev))
v.check("Ex 14-07.5i", sum(e.kind == "br" and e.taken for e in ev))
v.check("Ex 14-07.5j", sum(e.call for e in ev))
v.check("Ex 14-07.5k", sum(e.kind != "br" and not e.call and not e.ret for e in ev))
v.check("Ex 14-07.5l", sum(e.ret for e in ev))
v.check("Ex 14-07.5m", sum(e.taken for e in ev))
cyc = lambda m: N + 4 + S + 2 * m  # noqa: E731
m_none = bpred.simulate(ev, direction="none")["mispredicts"]
m_2b = bpred.simulate(ev, direction="2bit")["mispredicts"]
m_2br = bpred.simulate(ev, direction="2bit", ras_depth=16)["mispredicts"]
m_gs = bpred.simulate(ev, direction="gshare", ras_depth=16)["mispredicts"]
v.assert_true("no-prediction cycles equal 14-06's Verilog measurement (2850)", cyc(m_none) == 2850)
v.check("Ex 14-07.5a", cyc(m_none))
v.check("Ex 14-07.5b", cyc(m_2b))
v.check("Ex 14-07.5c", cyc(m_2br))
v.check("Ex 14-07.5d", m_gs)
v.check("Ex 14-07.5e", cyc(m_gs))
v.check("Ex 14-07.5f", cyc(m_none) / cyc(m_gs))
v.assert_true("guided exercise: RAS removes 112, gshare a further 51", m_2b - m_2br == 112 and m_2br - m_gs == 51)
v.check("Lab 14-07.a", len(ev))
v.check("Lab 14-07.b", sum(e.ret for e in ev))
v.check("Lab 14-07.d", m_gs)

# Example 6 and Problem 9: the count loop
HEAD = "    .text\n    .globl _start\n_start:\n    li   sp, 0x4000\n    li   a0, 0x2000\n    li   a1, 1000\n    li   a2, 128\n    call count\n    ebreak\n"
BR = """count:
    li   t0, 0
    beqz a1, 3f
1:  lw   t1, 0(a0)
    ble  t1, a2, 2f
    addi t0, t0, 1
2:  addi a0, a0, 4
    addi a1, a1, -1
    bnez a1, 1b
3:  mv   a0, t0
    ret
"""
BL = [c for lang, c, _, _ in markdown_code_blocks(PR) if lang == "asm"][0]


def lcg(n, seed=12345):
    x, out = seed, []
    for _ in range(n):
        x = (1103515245 * x + 12345) % 2**31
        out.append((x >> 16) % 256)
    return out


vals = lcg(1000)


def run_count(body, values):
    data = {0x2000 + 4 * i + k: (x >> 8 * k) & 0xFF for i, x in enumerate(values) for k in range(4)}
    ev_, n_, sim_ = bpred.trace({"c.s": HEAD + body}, data)
    mem, _, entry, size = build({"c.s": HEAD + body}, text=0)
    words = [int.from_bytes(bytes(mem[a + k] for k in range(4)), "little") for a in range(0, size, 4)]
    s2 = Sim({**mem, **data}, entry)
    tr: list = []
    s2.run(trace=tr)
    h = make_program.hazard_model(words, [p for p, _ in tr] + [s2.pc])
    m = bpred.simulate(ev_, direction="2bit", ras_depth=16)["mispredicts"]
    v.assert_true(f"count correct ({sum(x > 128 for x in values)})", sim_.x[10] == sum(x > 128 for x in values))
    return dict(N=n_, S=h["stalls"], M=m, ev=ev_)


un, so, bl = run_count(BR, vals), run_count(BR, sorted(vals)), run_count(BL, vals)
v.check("Ex 14-07.6a", un["M"])
v.check("Ex 14-07.6b", so["M"])
v.check("Ex 14-07.6c", (un["M"] - so["M"]) * 15)
v.assert_true("loop executes 5526 instructions; unsorted run more than twice the sorted at P = 15",
              un["N"] == 5526 and (un["N"] + 4 + un["S"] + 15 * un["M"]) > 2 * (so["N"] + 4 + so["S"] + 15 * so["M"]))
v.assert_true("gshare no better than 2-bit on random data", bpred.simulate(un["ev"], direction="gshare", ras_depth=16)["mispredicts"] >= un["M"])
v.assert_true("Problem 9's stated counts", (un["N"], un["S"], un["M"], bl["N"], bl["S"], bl["M"]) == (5526, 1000, 504, 6010, 0, 3))
c = lambda r, p: r["N"] + 4 + r["S"] + p * r["M"]  # noqa: E731
v.check("14-07.9a", c(un, 2))
v.check("14-07.9b", c(un, 15))
v.check("14-07.9c", c(bl, 2))
v.check("14-07.9d", c(bl, 15))
v.check("14-07.9e", c(un, 15) / c(bl, 15))
v.assert_true("branchless wins by 1.252 at P = 2; sorted branchy takes 6542 at P = 2", round(c(un, 2) / c(bl, 2), 3) == 1.252 and c(so, 2) == 6542)
v.check("Lab 14-07.c", bpred.simulate(so["ev"], direction="2bit", entries=4, ras_depth=16)["mispredicts"])
v.assert_true("sorted count loop: 6 mispredictions with 1024 entries", bpred.simulate(so["ev"], direction="2bit", entries=1024, ras_depth=16)["mispredicts"] == 6)

# Problems
v.check("14-07.1a", 1 + 0.15 * 0.08 * 12)
seq = [1, 1, 0, 1, 1, 1, 0, 0, 1]
t = bpred.TwoBit(1, init=1)
m2 = 0
for o in seq:
    m2 += t.predict(0) != bool(o)
    t.update(0, bool(o))
last, m1 = False, 0
for o in seq:
    m1 += last != bool(o)
    last = bool(o)
v.check("14-07.2a", m2)
v.check("14-07.2b", t.t[0])
v.check("14-07.2c", m1)
v.check("14-07.3a", 70)
v.check("14-07.3b", 100 * 19 / 20)
v.check("14-07.4a", 100 * 2 / 3)
v.check("14-07.4b", 100 * 1 / 3)
ev3, _, _ = bpred.trace({"l.s": LOOP.format(trip=3)})
in3 = [e for e in ev3 if e.kind == "br" and e.pc == min(x.pc for x in ev3 if x.kind == "br")]
v.assert_true("steady-state: n = 3 loop mispredicted once (2-bit) and twice (1-bit) per execution",
              abs(bpred.simulate(in3, direction="2bit")["dir_wrong"] - 100) <= 2 and bpred.simulate(in3, direction="1bit")["dir_wrong"] == 200)


def min_hist(trip, slack=25):
    evk, _, _ = bpred.trace({"l.s": LOOP.format(trip=trip)})
    return next(h for h in range(0, 16) if bpred.simulate(evk, direction="gshare", hist_bits=h)["mispredicts"] <= slack)


v.check("14-07.5a", min_hist(4))
v.check("14-07.5b", min_hist(10))
depth = mx = 0
for e in ev:
    depth += (e.call - e.ret)
    mx = max(mx, depth)
v.check("14-07.6a", mx)
v.check("14-07.6b", bpred.simulate(ev, direction="2bit", ras_depth=2)["mispredicts"])
v.check("14-07.6c", bpred.simulate(ev, direction="2bit", ras_depth=4)["mispredicts"])
v.check("14-07.6d", bpred.simulate(ev, direction="2bit", ras_depth=16)["mispredicts"])
v.assert_true("any RAS depth >= 10 gives 93", all(bpred.simulate(ev, direction="2bit", ras_depth=d)["mispredicts"] == 93 for d in (10, 11, 32)))
v.check("14-07.7a", (0x1000 >> 2) % 1024)
v.assert_true("0x2000 maps to entry 0 too; 2048 entries separate them", (0x2000 >> 2) % 1024 == 0 and (0x1000 >> 2) % 2048 != (0x2000 >> 2) % 2048)
v.check("14-07.7b", 2048)
v.check("14-07.8a", 5 / 1000 * 2)
v.check("14-07.8b", 5 / 1000 * 15)
v.check("14-07.10a", 1000 & 255)
bits_g, bits_b = 2**12 * 2 + 12, 1024 * (20 + 30 + 1)
v.assert_true("8204 and 52,224 bits", bits_g == 8204 and bits_b == 52224)
v.check("14-07.11a", bits_g / 8 / 1024)
v.check("14-07.11b", bits_b / 8 / 1024)
bc = [e for e in ev if e.kind == "br" and e.pc == max(x.pc for x in ev if x.kind == "br")]
v.assert_true("base-case branch: 177 executions, 89 taken; wrong 67 (1-bit), 87 (2-bit), 35 (gshare)",
              len(bc) == 177 and sum(e.taken for e in bc) == 89 and bpred.simulate(bc, direction="1bit")["dir_wrong"] == 67
              and bpred.simulate(bc, direction="2bit")["dir_wrong"] == 87 and bpred.simulate(bc, direction="gshare")["dir_wrong"] == 35)
v.assert_true("whole program: 1-bit 185 against 2-bit 205 (BTB, no RAS)", bpred.simulate(ev, direction="1bit")["mispredicts"] == 185 and m_2b == 205)

# ---------------------------------------------------------------- Problem 13: a (1,1) correlating predictor, by its own model
outs = []
for i in range(8):
    b1 = i % 2 == 0
    outs += [("b1", b1), ("b2", b1)]
one_bit = {"b1": False, "b2": False}
miss_1 = 0
for br, taken in outs:
    miss_1 += one_bit[br] != taken
    one_bit[br] = taken
v.check("14-07.13a", miss_1)
corr = {(br, h): False for br in ("b1", "b2") for h in (False, True)}
hist, miss_c, rows_c = False, 0, []
for br, taken in outs:
    pred = corr[(br, hist)]
    rows_c.append((br, hist, pred, taken))
    miss_c += pred != taken
    corr[(br, hist)] = taken
    hist = taken
v.check("14-07.13b", miss_c)
v.assert_true("(1,1) mispredictions all in iteration 0", [k for k, (_, _, p, t) in enumerate(rows_c) if p != t] == [0, 1])
tn = lambda b: "T" if b else "N"  # noqa: E731
sol13 = (ROOT / "solutions" / "14-07-solutions.md").read_text().split("### Solution 14-07.13")[1].split("\n---")[0]
table13 = [tuple(c.strip() for c in ln.strip("|").split("|")) for ln in sol13.split("\n") if ln.startswith("| ") and ln[2].isdigit()]
v.assert_true("Solution 13's trace table matches the model row by row",
              [(r[1], r[2], r[4], r[5]) for r in table13] == [(b, tn(h), tn(p), tn(t)) for b, h, p, t in rows_c[:6]])

sys.exit(v.finish())
