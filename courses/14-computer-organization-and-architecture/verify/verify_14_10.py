#!/usr/bin/env python3
"""Verify every number in chapter 14-10, its problem set and its lab.

Independent routes:
- Sv32 walks: the lab's walker (labs/14-10-lab/vm.py, written from the specification's algorithm) is compared
  with a second decoder written here directly from the bit layouts (VPN[1] = bits 31-22, VPN[0] = bits 21-12;
  PTE PPN = bits 31-10, flags in bits 7-0) for every published walk, including the faults;
- TLB miss counts of the matrix traversals are checked against closed forms (one miss per page for rows; for
  columns every access when the TLB holds fewer entries than the 1024 pages a column touches, otherwise one per
  page) and simulated with the lab's TLB and MMU;
- page-replacement counts are recomputed by a second implementation written here, and the MMU's demand paging
  (faults serviced with real page-table updates) must give the same counts as the reference-string model;
- sizes, costs and cause codes are evaluated from their formulas and the specification's tables.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(ROOT / "labs" / "14-10-lab"))
from eeverify import Verifier  # noqa: E402
import vm  # noqa: E402

CH = ROOT / "chapters" / "14-10-virtual-memory.md"
v = Verifier.from_files("14-10", CH, ROOT / "solutions" / "14-10-solutions.md", ROOT / "labs" / "14-10-lab" / "README.md")
KiB, MiB, GiB = 1 << 10, 1 << 20, 1 << 30


# ---------------------------------------------------------------------------------------------------------------
# An independent Sv32 decoder (user mode unless stated)
def decode(words: dict, root_ppn: int, va: int, access: str, user: bool = True):
    """Return ('ok', pa, reads) or ('fault', cause, reads)."""
    cause = {"fetch": 12, "load": 13, "store": 15}[access]
    vpn1, vpn0, off = va >> 22, (va >> 12) & 0x3FF, va & 0xFFF
    pte = words.get(root_ppn * 4096 + vpn1 * 4, 0)
    reads = 1
    if pte & 1 == 0 or (pte & 6) == 4:
        return "fault", cause, reads
    level = 1
    if pte & 0xA == 0:                      # neither R nor X: pointer
        pte = words.get((pte >> 10) * 4096 + vpn0 * 4, 0)
        reads += 1
        level = 0
        if pte & 1 == 0 or (pte & 6) == 4 or pte & 0xA == 0:
            return "fault", cause, reads
    ppn = pte >> 10
    if level == 1 and ppn & 0x3FF:
        return "fault", cause, reads
    if (pte >> 4 & 1) != user:              # U must match the mode (SUM = 0)
        return "fault", cause, reads
    need = {"fetch": 8, "load": 2, "store": 4}[access]
    if not pte & need:
        return "fault", cause, reads
    pa = ((ppn >> 10) << 22 | (va & 0x3FFFFF)) if level == 1 else (ppn << 12 | off)
    return "ok", pa, reads


def lab_walk(pt, va, access, user=True):
    try:
        pa, reads, _ = pt.walk(va, access, user=user)
        return "ok", pa, reads
    except vm.PageFault as e:
        return "fault", e.cause, None


# ---------------------------------------------------------------------------------------------------------------
# Example 1 and Problems 1, 2, 7
va = 0x12345678
f = vm.fields(va)
v.check("Ex 14-10.1a", f[0])
v.check("Ex 14-10.1b", f[1])
v.check("Ex 14-10.1c", f[2])
v.assert_true("fields as hex 0x48, 0x345, 0x678", f == (0x48, 0x345, 0x678))
v.check("Ex 14-10.1d", 2**20 * 4 / MiB)


def table_pages(regions) -> int:
    """Root plus one level-0 table per distinct VPN[1] touched by the [start, end) regions."""
    return 1 + len({p >> 22 for s, e in regions for p in range(s, e, 4096)})


ex1 = [(0x0001_0000, 0x0001_0000 + 64 * KiB), (0x1000_0000, 0x1000_0000 + 3 * MiB), (0x8000_0000 - 128 * KiB, 0x8000_0000)]
pages1 = table_pages(ex1)
v.check("Ex 14-10.1e", pages1 * 4)
v.check("Ex 14-10.1f", 4 * MiB / (pages1 * 4 * KiB))
mem = vm.Memory()
pt = vm.PageTable(mem)
for s, e in ex1:
    for p in range(s, e, 4096):
        pt.map(p, mem.alloc())
v.assert_true("lab page tables for Example 1 occupy 4 pages (root + 3; only PTEs are written)",
              len({a >> 12 for a in mem.words}) == 4)

p1 = vm.fields(0x80402ABC)
v.check("14-10.1a", p1[0])
v.check("14-10.1b", p1[1])
v.check("14-10.1c", p1[2])
v.check("14-10.2a", 4096 // 8)
v.check("14-10.2b", 9)
v.check("14-10.2c", 27 // 9)
v.check("14-10.2d", 2**27 * 8 / GiB)
ex7 = [(0x0040_0000, 0x0040_0000 + MiB), (0x1000_0000, 0x1000_0000 + 9 * MiB), (0x8000_0000 - MiB, 0x8000_0000)]
pages7 = table_pages(ex7)
v.check("14-10.7a", pages7)
v.check("14-10.7b", pages7 * 4)
megas = len({p >> 22 for p in range(0x1000_0000, 0x1000_0000 + 9 * MiB, 4096)})
v.check("14-10.7c", megas)
v.check("14-10.7d", megas * 4 - 9)
v.check("14-10.7e", table_pages([ex7[0], ex7[2]]))

# ---------------------------------------------------------------------------------------------------------------
# Example 2 and Problem 5: walks
mem = vm.Memory(first_frame=0x80000)
pt = vm.PageTable(mem)
v.assert_true("root at PPN 0x80000", pt.root == 0x80000)
pt.map(0x0040_3000, 0x12345, vm.R | vm.W | vm.U)
words = dict(mem.words)
v.assert_true("Example 2 memory image as published", words == {0x8000_0004: 0x2000_0401, 0x8000_100C: 0x048D_1417})
ind = decode(words, 0x80000, 0x0040_3ABC, "load")
res = lab_walk(pt, 0x0040_3ABC, "load")
v.assert_true("walker and independent decoder agree", ind == res[:2] + (ind[2],) and res[2] == ind[2])
v.check("Ex 14-10.2a", res[1])
v.check("Ex 14-10.2b", res[2])
v.check("Ex 14-10.2c", mem.read(0x8000_100C))
pt.walk(0x0040_3ABC, "store")
v.assert_true("a store then sets D: 0x048D14D7", mem.read(0x8000_100C) == 0x048D_14D7)
v.check("Ex 14-10.2d", lab_walk(pt, 0x0040_3ABC, "fetch")[1])
v.check("Ex 14-10.2e", lab_walk(pt, 0x0040_3ABC, "load", user=False)[1])
v.assert_true("decoder agrees on the two faults",
              decode(words, 0x80000, 0x0040_3ABC, "fetch")[:2] == ("fault", 12)
              and decode(words, 0x80000, 0x0040_3ABC, "load", user=False)[:2] == ("fault", 13))

mem5 = vm.Memory()
img5 = {0x8000_0000: 0x2000_0401, 0x8000_0008: 0x1000_0017, 0x8000_000C: 0x1000_0417,
        0x8000_1014: 0x0000_0000, 0x8000_1018: 0x091A_2813}
mem5.words.update(img5)
pt5 = vm.PageTable.__new__(vm.PageTable)
pt5.mem, pt5.root, pt5.asid = mem5, 0x80000, 0
cases = {"a": (0x0080_1234, "load"), "b": (0x0000_5010, "load"), "c": (0x0000_6020, "store"),
         "d": (0x00C0_0000, "load"), "e": (0x0000_6020, "load")}
out5 = {}
for k, (a, acc) in cases.items():
    lab = lab_walk(pt5, a, acc)
    ind = decode(img5, 0x80000, a, acc)
    v.assert_true(f"Problem 5{k}: walker and decoder agree", lab[:2] == ind[:2])
    out5[k] = ind
v.check("14-10.5a", out5["a"][1])
v.check("14-10.5b", out5["a"][2])
v.check("14-10.5c", out5["b"][1])
v.check("14-10.5d", out5["c"][1])
v.check("14-10.5e", out5["d"][1])
v.check("14-10.5f", out5["e"][1])
v.check("14-10.5g", out5["e"][2])
v.assert_true("(b) faults after 2 reads; (d) is a misaligned megapage (PPN 0x40001)",
              out5["b"][2] == 2 and out5["d"][2] == 1 and (0x1000_0417 >> 10) == 0x40001)

# ---------------------------------------------------------------------------------------------------------------
# Example 3 and Problems 3, 6, 11
v.check("Ex 14-10.3a", 0.005 * 2 * 14)
v.check("Ex 14-10.3b", 0.005 * 2 * 200)
fault_cyc = 5e-3 * 3e9
v.check("Ex 14-10.3c", 1e-6 * fault_cyc)
v.check("Ex 14-10.3d", fault_cyc / 0.4 / 1e6)
v.check("14-10.3a", 64 * 4)
v.check("14-10.3b", 2048 * 4 / 1024)
v.check("14-10.3c", 2048 * 2 / 1024)
v.check("14-10.6a", 0.02 * (7 + 0.1 * 60))
v.check("14-10.6b", 0.02 * 60)
v.check("14-10.11a", 100 * 64 * 30 / 3e6)
v.check("14-10.11b", 100 * (64 + 2048) * 30 / 3e6)

# ---------------------------------------------------------------------------------------------------------------
# Example 4 and Problem 8: TLB reach and the matrix traversals
N, BASE = 1024, 0x1000_0000


def traverse(order: str, entries: int, mega: bool):
    mem_ = vm.Memory()
    pt_ = vm.PageTable(mem_)
    if mega:
        pt_.map_mega(BASE, 0x40000)
    else:
        for p in range(N * N * 4 // 4096):
            pt_.map(BASE + 4096 * p, 0x40000 + p)
    m = vm.MMU(pt_, vm.TLB(entries))
    if order == "rows":
        for i in range(N):
            row = BASE + 4 * N * i
            for j in range(N):
                m.access(row + 4 * j)
    else:
        for j in range(N):
            for i in range(N):
                m.access(BASE + 4 * (i * N + j))
    return m


v.check("Ex 14-10.4a", vm.TLB(64).reach // KiB)
r4 = traverse("rows", 64, False)
c4 = traverse("cols", 64, False)
v.check("Ex 14-10.4b", r4.tlb.misses)
v.check("Ex 14-10.4c", c4.tlb.misses)
v.check("Ex 14-10.4d", c4.pte_reads)
mg = [traverse(o, 64, True).tlb.misses for o in ("rows", "cols")]
v.assert_true("megapage: 1 miss either way", mg == [1, 1])
v.check("Ex 14-10.4e", mg[1])
v.assert_true("closed forms: rows one miss per page (1024), columns every access (1024^2) when entries < 1024",
              r4.tlb.misses == N * N * 4 // 4096 and c4.tlb.misses == N * N and r4.pte_reads == 2 * 1024)
v.assert_true("rows miss rate 0.098%", round(100 * r4.tlb.misses / N**2, 3) == 0.098)
m1024 = traverse("cols", 1024, False).tlb.misses
m1023 = traverse("cols", 1023, False).tlb.misses
v.check("14-10.8a", m1024)
v.check("14-10.8b", m1023)
v.assert_true("closed forms for Problem 8: 1024 and 1024^2", (m1024, m1023) == (1024, N * N))

# Example 5 and Problem 4: traps
v.check("Ex 14-10.5a", 0x0001_0040)
v.check("Ex 14-10.5b", vm.CAUSE["load"])
v.check("Ex 14-10.5c", 8)
v.check("Ex 14-10.5d", 0x0001_0080 + 4)
v.check("Ex 14-10.5e", 1 << 31 | 7)
v.check("Ex 14-10.5f", 4 * 7)
v.check("14-10.4a", vm.CAUSE["store"])
v.check("14-10.4b", 8)
v.check("14-10.4c", 1 << 31 | 5)
v.check("14-10.4d", 4 * 11)

# Example 6 and Problem 9: VIPT
v.check("Ex 14-10.6a", 32 // 8)
v.check("Ex 14-10.6b", 64 // 8)
v.check("Ex 14-10.6c", (64 * KiB // 8) // 4096)
v.check("Ex 14-10.6d", 48 // 12)
for idc, ways in (("a", 8), ("b", 12), ("c", 16)):
    v.check(f"14-10.9{idc}", 4 * ways)
v.check("14-10.9d", 16 * 8)

# ---------------------------------------------------------------------------------------------------------------
# Problems 10 and 12: replacement, checked by a second implementation and by the MMU's demand paging
def ref_faults(refs, frames, policy):
    resident: list = []
    faults = 0
    for t, p in enumerate(refs):
        if p in resident:
            if policy == "lru":
                resident.append(resident.pop(resident.index(p)))
            continue
        faults += 1
        if len(resident) < frames:
            resident.append(p)
            continue
        if policy == "opt":
            nxt = {q: next((u for u in range(t + 1, len(refs)) if refs[u] == q), 10**9) for q in resident}
            resident.remove(max(resident, key=lambda q: (nxt[q], -resident.index(q))))
        else:
            resident.pop(0)
        resident.append(p)
    return faults


def mmu_faults(refs, frames, policy):
    mem_ = vm.Memory()
    m = vm.MMU(vm.PageTable(mem_), vm.TLB(64), frames=frames, policy=policy)
    for p in refs:
        m.access(0x1000_0000 + 4096 * p)
    return m.faults


belady = [5, 3, 4, 1, 5, 3, 2, 5, 3, 4, 1, 2]
ids = iter("abcdef")
for pol in ("fifo", "lru", "opt"):
    for fr in (3, 4):
        n = vm.page_faults(belady, fr, pol)
        v.assert_true(f"Belady string, {pol}, {fr} frames: two implementations agree", n == ref_faults(belady, fr, pol))
        if pol != "opt":
            v.assert_true(f"... and the MMU's demand paging agrees ({pol}, {fr})", n == mmu_faults(belady, fr, pol))
        v.check(f"14-10.10{next(ids)}", n)
cyc = list(range(10)) * 10
ids = iter("abcdef")
for fr in (9, 10):
    for pol in ("fifo", "lru", "opt"):
        n = vm.page_faults(cyc, fr, pol)
        v.assert_true(f"cyclic, {pol}, {fr} frames: implementations agree", n == ref_faults(cyc, fr, pol))
        v.check(f"14-10.12{next(ids)}", n)
v.check("14-10.12g", vm.page_faults(cyc, 9, "lru") * 5e-3)
v.check("14-10.12h", vm.page_faults(cyc, 10, "lru") * 5e-3)
v.assert_true("MMU demand paging on the cyclic loop: 100 and 10 faults (LRU)",
              (mmu_faults(cyc, 9, "lru"), mmu_faults(cyc, 10, "lru")) == (100, 10))

# ---------------------------------------------------------------------------------------------------------------
# Lab
v.check("Lab 14-10.a", traverse("rows", 16, False).tlb.misses)
v.check("Lab 14-10.b", traverse("cols", 512, False).tlb.misses)
v.check("Lab 14-10.c", table_pages([(BASE, BASE + 4 * MiB)]))
v.check("Lab 14-10.d", mmu_faults(cyc, 9, "clock"))
REUSE = [1, 2, 3, 1, 4, 1, 5, 1, 2, 1, 3, 1, 4]
v.check("Lab 14-10.e", mmu_faults(REUSE, 3, "clock"))
v.check("Lab 14-10.f", mmu_faults(REUSE, 3, "fifo"))
v.check("Lab 14-10.g", mmu_faults(REUSE, 3, "lru"))
v.check("Lab 14-10.h", vm.page_faults(REUSE, 3, "opt"))
v.assert_true("reuse string: MMU and reference-string models agree, and so does the second implementation",
              all(mmu_faults(REUSE, 3, p) == vm.page_faults(REUSE, 3, p) == ref_faults(REUSE, 3, p) for p in ("fifo", "lru"))
              and ref_faults(REUSE, 3, "opt") == vm.page_faults(REUSE, 3, "opt"))
v.check("Lab 14-10.i", vm.page_faults(cyc, 5, "opt"))


def evicted_pages(refs, frames, policy):
    m = vm.MMU(vm.PageTable(vm.Memory()), vm.TLB(64), frames=frames, policy=policy)
    out = []
    for p in refs:
        before = set(m.resident)
        m.access(0x1000_0000 + 4096 * p)
        out += [q - 0x10000 for q in before - set(m.resident)]
    return out


v.assert_true("discussion 1: page 1 evicted twice by FIFO, once by clock",
              evicted_pages(REUSE, 3, "fifo").count(1) == 2 and evicted_pages(REUSE, 3, "clock").count(1) == 1)
v.assert_true("clock on the Belady string behaves like FIFO here (9 and 10)", (mmu_faults(belady, 3, "clock"), mmu_faults(belady, 4, "clock")) == (9, 10))

# ---------------------------------------------------------------- the TLB caches permissions and the D bit (audit fix)
mem_t = vm.Memory()
pt_t = vm.PageTable(mem_t)
pt_t.map(0x1000_0000, 0x200, vm.R | vm.U)              # read-only user page
pt_t.map(0x1000_1000, 0x201)                            # read-write user page
mmu_t = vm.MMU(pt_t, vm.TLB(8))
mmu_t.access(0x1000_0000)                               # load fills the TLB
try:
    mmu_t.access(0x1000_0004, store=True)               # store hits the TLB entry of a read-only page
    ro_fault = False
except vm.PageFault:
    ro_fault = True
v.assert_true("a store that hits the TLB entry of a read-only page still faults", ro_fault)
mmu_t.access(0x1000_1000)                               # load: A set, D clear, entry cached
leaf = lambda va: mem_t.read((mem_t.read(pt_t.root * vm.PAGE + (va >> 22) * 4) >> 10) * vm.PAGE + (va >> 12 & 0x3FF) * 4)  # noqa: E731
d_before = bool(leaf(0x1000_1000) & vm.D)
mmu_t.access(0x1000_1008, store=True)                   # store hits the clean entry: the walker sets D
v.assert_true("a store that hits a clean TLB entry sets D in the PTE through the walker",
              not d_before and leaf(0x1000_1000) & vm.D and mmu_t.dirty_updates == 1 and mmu_t.walks == 2)
mmu_t.access(0x1000_100C, store=True)
v.assert_true("a second store to the now-dirty page needs no walk", mmu_t.dirty_updates == 1 and mmu_t.walks == 2)


def nested_refs(n, m):
    """Count memory references of a two-stage walk by enumeration: each guest level's PTE address is
    guest-physical (host walk of m reads, then the PTE read); the final guest-physical address needs one more host walk."""
    refs = 0
    for _ in range(n):
        refs += m + 1
    return refs + m


v.check("Txt 14-10.a", nested_refs(4, 4))
v.check("Txt 14-10.b", 4)
v.assert_true("nested references equal nm + n + m for 1..5 levels", all(nested_refs(a, b) == a * b + a + b for a in range(1, 6) for b in range(1, 6)))

v.check("14-10.13a", nested_refs(3, 4))
v.check("14-10.13b", nested_refs(4, 4))
v.check("14-10.13c", nested_refs(4, 2))

sys.exit(v.finish())
