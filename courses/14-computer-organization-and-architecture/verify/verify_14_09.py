#!/usr/bin/env python3
"""Verify every number in chapter 14-09, its problem set and its lab.

Independent routes:
- traces come from C kernels compiled with clang and run on the course RV32IM simulator; every kernel's result
  is checked (sums, histogram bins, copies, transposes, matrix products against a Python product);
- every LRU configuration of the lab's cache model (labs/14-09-lab/cache.py) is re-simulated here by a separate
  implementation (one OrderedDict per set, with its own write-back/write-through bookkeeping), and FIFO by a
  deque-based one; fully associative LRU results are also checked against Mattson's stack-distance algorithm,
  which counts misses for every cache size at once without simulating replacement;
- hand-traceable examples are compared with tables of expected states, and the address fields with Python's
  own bit operations;
- AMAT, CPI, MPKI, energy and Little's-law figures are evaluated directly from their formulas.
"""
from __future__ import annotations

import math
import sys
from collections import OrderedDict, deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "14-09-lab"))
sys.path.insert(0, str(ROOT / "labs" / "14-08-lab"))
from eeverify import Verifier  # noqa: E402
import cache  # noqa: E402
import ooo  # noqa: E402

CH = ROOT / "chapters" / "14-09-memory-hierarchy-and-caches.md"
v = Verifier.from_files("14-09", CH, ROOT / "solutions" / "14-09-solutions.md", ROOT / "labs" / "14-09-lab" / "README.md")


# ---------------------------------------------------------------------------------------------------------------
# Independent reference simulators
def ref_sim(trace, size, block, assoc, policy="lru", write_back=True, write_allocate=True):
    """Misses, block fills, dirty write-backs (including a final flush) and word write-throughs."""
    nsets = size // (block * assoc)
    sets = [OrderedDict() if policy == "lru" else deque() for _ in range(nsets)]
    dirty: set = set()
    misses = fills = wbs = wts = 0
    for addr, st in trace:
        b = addr // block
        s = sets[b % nsets]
        present = b in s
        if present:
            if policy == "lru":
                s.move_to_end(b)
            if st:
                if write_back:
                    dirty.add(b)
                else:
                    wts += 1
            continue
        misses += 1
        if st and not write_allocate:
            wts += 1
            continue
        if len(s) == assoc:
            victim = s.popitem(last=False)[0] if policy == "lru" else s.popleft()
            if victim in dirty:
                dirty.discard(victim)
                wbs += 1
        if policy == "lru":
            s[b] = True
        else:
            s.append(b)
        fills += 1
        if st:
            if write_back:
                dirty.add(b)
            else:
                wts += 1
    wbs += len(dirty)
    return dict(misses=misses, fills=fills, writebacks=wbs, write_throughs=wts)


def stack_distance_misses(trace, block, lines: int) -> int:
    """Misses of a fully associative LRU cache of `lines` blocks, by Mattson's stack algorithm."""
    stack: list = []
    miss = 0
    for addr, _ in trace:
        b = addr // block
        if b in stack:
            d = len(stack) - 1 - stack.index(b)   # distinct blocks used since b's last use
            if d >= lines:
                miss += 1
            stack.remove(b)
        else:
            miss += 1
        stack.append(b)
    return miss


def model(trace, size, block, assoc, **kw):
    c = cache.Cache(size, block, assoc, **kw).run(trace)
    c.flush()
    return c


def lru_both(trace, size, block, assoc) -> int:
    """Misses from the lab model, required to equal the independent simulator's."""
    m = model(trace, size, block, assoc).misses
    v.assert_true(f"model = reference LRU ({size} B, {block} B blocks, {assoc}-way)",
                  m == ref_sim(trace, size, block, assoc)["misses"])
    return m


# ---------------------------------------------------------------------------------------------------------------
# Example 1 and Problems 1-2: address fields
def fields(size, block, assoc, nbits, addr):
    sets = size // (block * assoc)
    ob, ib = int(math.log2(block)), int(math.log2(sets))
    return dict(sets=sets, ob=ob, ib=ib, tb=nbits - ob - ib, off=addr & (block - 1),
                idx=(addr >> ob) & (sets - 1), tag=addr >> (ob + ib))


f1 = fields(32 * 1024, 64, 8, 32, 0x12345678)
v.check("Ex 14-09.1a", f1["sets"])
v.check("Ex 14-09.1b", f1["ob"])
v.check("Ex 14-09.1c", f1["ib"])
v.check("Ex 14-09.1d", f1["tb"])
v.check("Ex 14-09.1e", f1["off"])
v.check("Ex 14-09.1f", f1["idx"])
v.check("Ex 14-09.1g", f1["tag"])
c1 = cache.Cache(32 * 1024, 64, 8)
v.assert_true("model's split agrees", c1.split(0x12345678) == (f1["tag"], f1["idx"], f1["off"]))
bits1 = (32 * 1024 // 64) * (f1["tb"] + 2)
v.check("Ex 14-09.1h", bits1)
v.check("Ex 14-09.1i", 100 * bits1 / (32 * 1024 * 8))
v.assert_true("1.375 KiB", bits1 / 8 / 1024 == 1.375)

p1 = fields(64 * 1024, 64, 4, 32, 0xDEADBEEF)
v.check("14-09.1a", p1["sets"])
v.check("14-09.1b", p1["ob"])
v.check("14-09.1c", p1["ib"])
v.check("14-09.1d", p1["tb"])
v.check("14-09.1e", p1["off"])
v.check("14-09.1f", p1["idx"])
v.check("14-09.1g", p1["tag"])
p2 = fields(1024 * 1024, 64, 16, 40, 0)
bits2 = (1024 * 1024 // 64) * (p2["tb"] + 2)
v.check("14-09.2a", p2["tb"])
v.check("14-09.2b", bits2 / 8 / 1024)
v.check("14-09.2c", 100 * bits2 / (1024 * 1024 * 8))
v.assert_true("1024 sets, 16384 lines, 425,984 bits", p2["sets"] == 1024 and bits2 == 425984)

# ---------------------------------------------------------------------------------------------------------------
# Example 2 and Problems 4-5: hand traces
ex2 = [(a, False) for a in (0x000, 0x040, 0x004, 0x080, 0x044, 0x008, 0x010, 0x050, 0x014)]
m_dm, m_2w, m_fa = (model(ex2, 64, 16, a).misses for a in (1, 2, 4))
v.check("Ex 14-09.2a", m_dm)
v.check("Ex 14-09.2b", m_2w)
v.check("Ex 14-09.2c", m_fa)
tc = cache.three_c(ex2, 64, 16, 1)
v.check("Ex 14-09.2d", tc["conflict"])
v.assert_true("Example 2: 5 compulsory, 0 capacity", (tc["compulsory"], tc["capacity"]) == (5, 0))
v.assert_true("Example 2 agrees with the reference simulator",
              [ref_sim(ex2, 64, 16, a)["misses"] for a in (1, 2, 4)] == [9, 7, 5])
c2 = cache.Cache(64, 16, 2).run(ex2)
v.assert_true("2-way final state: set 0 holds 4 then 0 (LRU first), set 1 holds 5 then 1",
              [[ln[0] * 2 + i for ln in s] for i, s in enumerate(c2.sets)] == [[4, 0], [5, 1]])

p4 = [(16 * b, False) for b in (0, 4, 8, 0, 4, 8)]
v.check("14-09.4a", model(p4, 64, 16, 1).misses)
v.check("14-09.4b", model(p4, 64, 16, 2).misses)
v.check("14-09.4c", model(p4, 64, 16, 4).misses)
tc4 = cache.three_c(p4, 64, 16, 1)
v.check("14-09.4d", tc4["compulsory"])
v.check("14-09.4e", tc4["conflict"])

p5 = [(16 * b, False) for b in (0, 2, 0, 4, 0, 2)]
v.check("14-09.5a", model(p5, 64, 16, 2, policy="lru").misses)
v.check("14-09.5b", model(p5, 64, 16, 2, policy="fifo").misses)
v.assert_true("Problem 5 agrees with the reference simulators",
              (ref_sim(p5, 64, 16, 2)["misses"], ref_sim(p5, 64, 16, 2, policy="fifo")["misses"]) == (4, 5))

# ---------------------------------------------------------------------------------------------------------------
# Example 3 and Problems 3, 6: AMAT and CPI
pen = 14 + 0.2 * 200
v.check("Ex 14-09.3a", 4 + 0.05 * pen)
v.check("Ex 14-09.3b", 100 * 0.05 * 0.2)
v.check("Ex 14-09.3c", 4 + 0.05 * 200)
v.check("Ex 14-09.3d", 1 + 0.35 * 0.05 * pen)
v.check("Ex 14-09.3e", 1 + 0.35 * 0.05 * 200)
v.check("Ex 14-09.3f", 1000 * 0.35 * 0.05)
v.check("14-09.3a", 1 + 0.04 * 60)
v.check("14-09.3b", 100 * (1 - (2 - 1) / 60))
m1, m2l = 20 / 400, 8 / 20
v.check("14-09.6a", 100 * m1)
v.check("14-09.6b", 100 * m2l)
v.check("14-09.6c", 100 * 8 / 400)
v.check("14-09.6d", 1000 * 20 / 1000)
v.check("14-09.6e", 1000 * 8 / 1000)
v.check("14-09.6f", 4 + m1 * (12 + m2l * 150))

# ---------------------------------------------------------------------------------------------------------------
# Example 4: rows and columns
rows, _ = cache.traverse("rows")
cols, _ = cache.traverse("cols")
v.assert_true("each traversal: 4096 loads, no stores", len(rows) == len(cols) == 4096 and not any(s for _, s in rows + cols))
v.check("Ex 14-09.4a", lru_both(rows, 4096, 32, 1))
v.check("Ex 14-09.4b", 100 * lru_both(rows, 4096, 32, 1) / len(rows))
v.check("Ex 14-09.4c", lru_both(cols, 4096, 32, 1))
v.check("Ex 14-09.4d", 100 * lru_both(cols, 4096, 32, 1) / len(cols))
tcc = cache.three_c(cols, 4096, 32, 1)
v.assert_true("columns: 512 compulsory, 0 capacity", (tcc["compulsory"], tcc["capacity"]) == (512, 0))
v.check("Ex 14-09.4e", tcc["conflict"])
v.check("Ex 14-09.4f", lru_both(cols, 4096, 32, 128))
v.check("Ex 14-09.4g", lru_both(cols, 4096, 32, 4))
v.check("Ex 14-09.4h", lru_both(cols, 1024, 32, 32))
v.assert_true("16 KB direct-mapped: 512", lru_both(cols, 16384, 32, 1) == 512)
v.assert_true("lab: columns at 4 KB miss 4096 times up to 16 ways", all(lru_both(cols, 4096, 32, w) == 4096 for w in (8, 16)))
v.assert_true("stack distances: fully associative 4 KB 512 and 1 KB 4096 misses",
              stack_distance_misses(cols, 32, 128) == 512 and stack_distance_misses(cols, 32, 32) == 4096)

# Example 5: histogram write policies
hist, _ = cache.histogram()
v.assert_true("histogram: 3000 accesses, 1000 stores", len(hist) == 3000 and sum(s for _, s in hist) == 1000)
wb = model(hist, 1024, 32, 2)
wt = model(hist, 1024, 32, 2, write_back=False, write_allocate=False)
r_wb = ref_sim(hist, 1024, 32, 2)
r_wt = ref_sim(hist, 1024, 32, 2, write_back=False, write_allocate=False)
v.assert_true("histogram agrees with the reference simulator",
              (wb.misses, wb.writebacks, wt.misses, wt.write_throughs) == (r_wb["misses"], r_wb["writebacks"], r_wt["misses"], r_wt["write_throughs"]))
v.check("Ex 14-09.5a", wb.misses)
v.assert_true("both policies: 34 misses", wt.misses == wb.misses)
v.check("Ex 14-09.5b", wb.traffic()["read"])
v.assert_true("same reads", wt.traffic()["read"] == wb.traffic()["read"])
v.check("Ex 14-09.5c", wb.traffic()["write"])
v.check("Ex 14-09.5d", wt.traffic()["write"])
v.assert_true("62.5 times the write traffic", wt.traffic()["write"] / wb.traffic()["write"] == 62.5)

# Example 6 and Problems 7, 12: matrix multiply
mm = {k: cache.matmul(*a) for k, a in {"ijk": ("ijk",), "ikj": ("ikj",), **{f"t{t}": ("tiled", 32, t) for t in (4, 8, 16, 32)}}.items()}
ins = {k: r["count"] for k, (_, r) in mm.items()}
v.assert_true("instruction and access counts", (ins["ijk"], ins["ikj"], ins["t8"]) == (272644, 307467, 340165)
              and (len(mm["ijk"][0]), len(mm["ikj"][0]), len(mm["t8"][0])) == (66560, 100352, 103444))
mi = {k: lru_both(mm[k][0], 2048, 32, 4) for k in ("ijk", "ikj", "t8")}
v.check("Ex 14-09.6a", mi["ijk"])
v.check("Ex 14-09.6b", mi["ikj"])
v.check("Ex 14-09.6c", mi["t8"])
cyc = {k: ins[k] + 100 * mi[k] for k in mi}
v.check("Ex 14-09.6d", cyc["ijk"])
v.check("Ex 14-09.6e", cyc["ikj"])
v.check("Ex 14-09.6f", cyc["t8"])
v.check("Ex 14-09.6g", cyc["ijk"] / cyc["t8"])
v.assert_true("miss rates 52.51%, 4.46%, 1.24%", [round(100 * mi[k] / len(mm[k][0]), 2) for k in ("ijk", "ikj", "t8")] == [52.51, 4.46, 1.24])
v.assert_true("25% more instructions; within 3.3x of 384 compulsory; 27x fewer misses than ijk",
              round(ins["t8"] / ins["ijk"] - 1, 2) == 0.25 and round(mi["t8"] / 384, 1) == 3.3 and round(mi["ijk"] / mi["t8"]) == 27)
v.assert_true("compulsory misses: 384 (ijk, ikj), 386 (tiled; two stack blocks)",
              [cache.three_c(mm[k][0], 2048, 32, 4)["compulsory"] for k in ("ijk", "ikj", "t8")] == [384, 384, 386])
# §3.4 going deeper and §3.5 claims
v.assert_true("§3.4: ikj 4 KB 4-way 1495 against fully associative 4480 (conflict -2985)",
              lru_both(mm["ikj"][0], 4096, 32, 4) == 1495 and stack_distance_misses(mm["ikj"][0], 32, 128) == 4480
              and cache.three_c(mm["ikj"][0], 4096, 32, 4)["conflict"] == -2985)
rnd = {k: model(mm[k][0], 2048, 32, 4, policy="random").misses for k in ("ijk", "ikj", "t8")}
v.assert_true("§3.5: random beats LRU on ijk and ikj, loses on tiled", rnd["ijk"] < mi["ijk"] and rnd["ikj"] < mi["ikj"] and rnd["t8"] > mi["t8"])

blocks = (16, 32, 64, 128)
for prog, acc, stated, ids in (("ijk", 66560, (7464, 6788, 5612, 5304), "abcd"), ("ikj", 100352, (2987, 1495, 749, 376), "efgh")):
    ms = tuple(lru_both(mm[prog][0], 4096, b, 4) for b in blocks)
    v.assert_true(f"Problem 7 table, {prog}", ms == stated and len(mm[prog][0]) == acc)
    amat = [2 + m / acc * (80 + b / 8) for m, b in zip(ms, blocks)]
    for idc, a in zip(ids, amat):
        v.check(f"14-09.7{idc}", a)
    v.check(f"14-09.7{'i' if prog == 'ijk' else 'j'}", blocks[amat.index(min(amat))])

tiles = {s: tuple(lru_both(mm[f"t{t}"][0], s, 32, 4) for t in (4, 8, 16, 32)) for s in (2048, 4096)}
v.assert_true("Problem 12 table", tiles == {2048: (4356, 1284, 2714, 4484), 4096: (2671, 1089, 771, 1499)})
v.check("14-09.12a", (4, 8, 16, 32)[tiles[2048].index(min(tiles[2048]))])
v.check("14-09.12b", (4, 8, 16, 32)[tiles[4096].index(min(tiles[4096]))])
v.check("14-09.12c", 8 * 8 * 4)
v.check("14-09.12d", 16 * 16 * 4)

# ---------------------------------------------------------------------------------------------------------------
# Problem 8: transpose
tp = cache.transpose()[0]
tt = cache.transpose(t=8)[0]
v.check("14-09.8a", lru_both(tp, 4096, 32, 2))
v.check("14-09.8b", lru_both(tt, 4096, 32, 2))
v.check("14-09.8c", lru_both(tp, 4096, 32, 1))
v.check("14-09.8d", lru_both(tt, 4096, 32, 1))
v.check("14-09.8e", cache.three_c(tp, 4096, 32, 2)["compulsory"])
v.assert_true("tiled transpose: 1025 compulsory (one stack block) and 1 capacity miss, both on the stack",
              cache.three_c(tt, 4096, 32, 2) == dict(compulsory=1025, capacity=1, conflict=0, total=1026)
              and sum(a < cache.BASE for a, _ in tt) == 10)

# Problem 9: copy
cp = cache.copy()[0]
a9 = model(cp, 4096, 32, 2)
b9 = model(cp, 4096, 32, 2, write_back=False, write_allocate=False)
v.assert_true("copy agrees with the reference simulator",
              (a9.fills, a9.writebacks, b9.fills, b9.write_throughs)
              == tuple(ref_sim(cp, 4096, 32, 2, **kw)[k] for kw, k in ((dict(), "fills"), (dict(), "writebacks"),
                       (dict(write_back=False, write_allocate=False), "fills"), (dict(write_back=False, write_allocate=False), "write_throughs"))))
v.check("14-09.9a", a9.traffic()["read"])
v.check("14-09.9b", a9.traffic()["write"])
v.check("14-09.9c", b9.traffic()["read"])
v.check("14-09.9d", b9.traffic()["write"])

# Problem 10: prefetching
lst = cache.linked_list()[0]
pr = {k: model(t, 4096, 32, 4, prefetch=True) for k, t in (("rows", rows), ("cols", cols), ("list", lst))}
v.check("14-09.10a", pr["rows"].misses)
v.check("14-09.10b", pr["rows"].prefetches)
v.check("14-09.10c", pr["cols"].misses)
v.check("14-09.10d", pr["cols"].prefetches)
v.check("14-09.10e", pr["list"].misses)
v.check("14-09.10f", pr["list"].prefetches)
v.assert_true("without prefetching: 512, 4096 and 256 misses",
              [lru_both(t, 4096, 32, 4) for t in (rows, cols, lst)] == [512, 4096, 256])
v.assert_true("columns and list: every prefetched block is never used (hits stay 0)",
              pr["cols"].hits == 0 and pr["list"].hits == 0)

# Problem 11 and concept check 7: Little's law
v.check("14-09.11a", 10 * 64 / 100e-9 / 1e9)
n11 = 1.2e12 * 100e-9 / 64
v.check("14-09.11b", n11)
v.check("14-09.11c", math.ceil(n11 / 24))
v.assert_true("§3.8: 6.4 GB/s; concept check: 100 outstanding for 64 GB/s",
              10 * 64 / 100e-9 == 6.4e9 and round(64e9 * 100e-9 / 64) == 100)

# Problem 13: energy
for idc, m, e in (("a", 0.05, 1.3e3), ("b", 0.01, 1.3e3), ("c", 0.05, 2.6e3), ("d", 0.01, 2.6e3)):
    v.check(f"14-09.13{idc}", 20 + m * e)
v.check("14-09.13e", (20 + 0.01 * 1.3e3) / 0.1)
v.assert_true("DRAM share at 1%: 39% and 57%", (round(100 * 13 / 33), round(100 * 26 / 46)) == (39, 57))

# Problem 14: misses fed into the out-of-order model
H = ooo.HEAD
ARR = H + """    li a0, 0x2000
    li a1, 256
    li t0, 0
1:  lw   t1, 0(a0)
    add  t0, t0, t1
    addi a0, a0, 4
    addi a1, a1, -1
    bnez a1, 1b
    ebreak
"""
LST = H + """    li a0, 0x2000
    li t0, 0
1:  lw   a0, 0(a0)
    addi t0, t0, 1
    bnez a0, 1b
    ebreak
"""
lst_data: dict = {}
for i in range(256):
    lst_data.update(ooo.words([0x2000 + 64 * (i + 1) if i < 255 else 0], 0x2000 + 64 * i))


def with_cache(src, data):
    tr, sim = ooo.dyn_trace({"x.s": src}, data)
    c = cache.Cache(4096, 64, 4)
    lat = {}
    for i, t in enumerate(tr):
        if t[1] in ("load", "store") and not c.access(t[5], t[1] == "store") and t[1] == "load":
            lat[i] = 100
    return tr, sim, lat, c


ta, sa, la, ca = with_cache(ARR, ooo.words(list(range(1, 257))))
tl, sl, ll, cl = with_cache(LST, lst_data)
v.assert_true("array sum 32896 (1203 + 80 instructions); list length 256; 256 loads each",
              sa.x[5] == 32896 and sl.x[5] == 256 and sum(t[1] == "load" for t in ta) == sum(t[1] == "load" for t in tl) == 256)
v.check("14-09.14a", ca.misses)
v.check("14-09.14b", cl.misses)
S = ooo.schedule
v.check("14-09.14c", S(ta, width=1, rob=16, in_order=True, lat_of=la)["cycles"])
v.check("14-09.14d", S(tl, width=1, rob=16, in_order=True, lat_of=ll)["cycles"])
v.check("14-09.14e", S(ta, width=4, rob=64, lat_of=la)["cycles"])
v.check("14-09.14f", S(ta, width=4, rob=256, lat_of=la)["cycles"])
v.check("14-09.14g", S(tl, width=4, rob=64, lat_of=ll)["cycles"])
v.assert_true("list: 256-entry window no faster", S(tl, width=4, rob=256, lat_of=ll)["cycles"] == S(tl, width=4, rob=64, lat_of=ll)["cycles"])
v.assert_true("list: critical path = 256 x 100 + 2", ooo.critical_path(tl, lat_of=ll) == 256 * 100 + 2)
v.check("14-09.14h", 16 * 5)
v.assert_true("in-order: each miss adds 97 cycles to the no-miss time",
              S(ta, width=1, rob=16, in_order=True, lat_of=la)["cycles"] - S(ta, width=1, rob=16, in_order=True)["cycles"] == 16 * 97
              and S(tl, width=1, rob=16, in_order=True, lat_of=ll)["cycles"] - S(tl, width=1, rob=16, in_order=True)["cycles"] == 256 * 97)

# ---------------------------------------------------------------------------------------------------------------
# Lab
v.check("Lab 14-09.a", cache.three_c(cols, 8192, 32, 1)["conflict"])
v.assert_true("columns, direct-mapped: 3584 conflict misses at 2, 4 and 8 KB, none at 16 KB",
              [cache.three_c(cols, s, 32, 1)["conflict"] for s in (2048, 4096, 8192, 16384)] == [3584, 3584, 3584, 0])
v.check("Lab 14-09.b", lru_both(mm["ijk"][0], 16384, 32, 4))
v.assert_true("figure: misses at 1, 4, 8 KB for ijk, ikj, tiled",
              [lru_both(mm[k][0], sz, 32, 4) for k in ("ijk", "ikj", "t8") for sz in (1024, 4096, 8192)]
              == [35008, 6788, 384, 4480, 1495, 463, 5072, 1089, 610])
v.check("Lab 14-09.c", lru_both(mm["t16"][0], 4096, 32, 4))
v.check("Lab 14-09.d", rnd["ijk"])
v.check("Lab 14-09.e", model(mm["ikj"][0], 2048, 32, 4, policy="fifo").misses)
v.assert_true("FIFO agrees with the reference", model(mm["ikj"][0], 2048, 32, 4, policy="fifo").misses == ref_sim(mm["ikj"][0], 2048, 32, 4, policy="fifo")["misses"])
v.check("Lab 14-09.f", cache.three_c(rows, 4096, 32, 1)["compulsory"])
v.check("Lab 14-09.g", S(ta, width=4, rob=128, lat_of=la)["cycles"])

sys.exit(v.finish())
