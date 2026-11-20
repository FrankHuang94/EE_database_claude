"""A trace-driven cache simulator for Lab 14-09.

`mem_trace(...)` compiles a C kernel, runs it on the course's RV32IM simulator and returns every data access as
(address, is_store). `Cache(...)` models one level of a set-associative cache:

- `size` bytes, `block` bytes per block, `assoc` ways (assoc = size // block gives a fully associative cache);
- replacement `"lru"`, `"fifo"` or `"random"` (seeded, so runs repeat);
- write-back or write-through, write-allocate or no-write-allocate;
- optional tagged next-line prefetching: a miss to block b also fetches b + 1, and the first demand hit on a
  prefetched block fetches the block after it;
- an optional `next` level, which sees this level's block fills (as reads) and write-backs (as writes).

Counters: accesses, hits, misses, fills (blocks read from below), writebacks (dirty blocks written below),
write-throughs (words written below), prefetches, and the resulting traffic in bytes.

`three_c(...)` splits a configuration's misses into compulsory, capacity and conflict misses.

The workloads (`traverse`, `histogram`, `copy`, `transpose`, `linked_list`, `matmul`) run the C kernels of
kernels.c on fixed data at fixed addresses and check each result before returning the trace.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verify"))
from _rv32 import run_function  # noqa: E402

WORD = 4


class Cache:
    def __init__(self, size: int, block: int, assoc: int, policy: str = "lru", write_back: bool = True,
                 write_allocate: bool = True, prefetch: bool = False, next: Cache | None = None, seed: int = 1):
        assert size % (block * assoc) == 0, "size must be a multiple of block x assoc"
        self.size, self.block, self.assoc = size, block, assoc
        self.nsets = size // (block * assoc)
        self.policy, self.write_back, self.write_allocate = policy, write_back, write_allocate
        self.prefetch, self.next = prefetch, next
        self.rng = random.Random(seed)
        # each set: list of lines [tag, dirty, prefetched]; for LRU the order is LRU first, MRU last;
        # for FIFO it is the order of insertion
        self.sets: list[list[list]] = [[] for _ in range(self.nsets)]
        self.accesses = self.hits = self.misses = 0
        self.fills = self.writebacks = self.write_throughs = self.prefetches = 0

    # ------------------------------------------------------------------ address mapping
    def split(self, addr: int) -> tuple[int, int, int]:
        """(tag, index, offset) of a byte address."""
        b = addr // self.block
        return b // self.nsets, b % self.nsets, addr % self.block

    def _find(self, s: list, tag: int):
        for line in s:
            if line[0] == tag:
                return line
        return None

    def _insert(self, blk: int, dirty: bool, prefetched: bool) -> None:
        """Bring block number `blk` into its set, evicting a victim if the set is full."""
        tag, idx = blk // self.nsets, blk % self.nsets
        s = self.sets[idx]
        if len(s) == self.assoc:
            victim = s.pop(self.rng.randrange(self.assoc) if self.policy == "random" else 0)
            if victim[1]:
                self.writebacks += 1
                if self.next:
                    self.next.access((victim[0] * self.nsets + idx) * self.block, store=True, whole_block=True)
        s.append([tag, dirty, prefetched])
        self.fills += 1
        if self.next:
            self.next.access(blk * self.block)

    def _prefetch(self, blk: int) -> None:
        tag, idx = blk // self.nsets, blk % self.nsets
        if self._find(self.sets[idx], tag) is None:
            self.prefetches += 1
            self._insert(blk, dirty=False, prefetched=True)

    # ------------------------------------------------------------------ the access
    def access(self, addr: int, store: bool = False, whole_block: bool = False) -> bool:
        """One access; returns True on a hit. `whole_block` marks a write-back arriving from the level above."""
        self.accesses += 1
        blk = addr // self.block
        tag, idx = blk // self.nsets, blk % self.nsets
        s = self.sets[idx]
        line = self._find(s, tag)
        if line is not None:
            self.hits += 1
            if self.policy == "lru":
                s.remove(line)
                s.append(line)
            if store:
                if self.write_back:
                    line[1] = True
                else:
                    self._write_through(addr, whole_block)
            if line[2]:                      # first demand use of a prefetched block
                line[2] = False
                if self.prefetch:
                    self._prefetch(blk + 1)
            return True
        self.misses += 1
        if store and not self.write_allocate:
            self._write_through(addr, whole_block)
            return False
        self._insert(blk, dirty=store and self.write_back, prefetched=False)
        if store and not self.write_back:
            self._write_through(addr, whole_block)
        if self.prefetch:
            self._prefetch(blk + 1)
        return False

    def _write_through(self, addr: int, whole_block: bool) -> None:
        self.write_throughs += 1
        if self.next:
            self.next.access(addr, store=True, whole_block=whole_block)

    def flush(self) -> None:
        """Write back every dirty block (end of a run), so traffic counts are complete."""
        for idx, s in enumerate(self.sets):
            for line in s:
                if line[1]:
                    self.writebacks += 1
                    line[1] = False
                    if self.next:
                        self.next.access((line[0] * self.nsets + idx) * self.block, store=True, whole_block=True)

    # ------------------------------------------------------------------ results
    @property
    def miss_rate(self) -> float:
        return self.misses / self.accesses if self.accesses else 0.0

    def traffic(self) -> dict:
        """Bytes moved to and from the next level (call flush() first for a write-back cache)."""
        return dict(read=self.fills * self.block, write=self.writebacks * self.block + self.write_throughs * WORD)

    def run(self, trace) -> Cache:
        for addr, st in trace:
            self.access(addr, st)
        return self


def three_c(trace, size: int, block: int, assoc: int, policy: str = "lru") -> dict:
    """Compulsory, capacity and conflict misses of a configuration (stores treated as accesses)."""
    seen: set = set()
    comp = 0
    for addr, _ in trace:
        b = addr // block
        if b not in seen:
            seen.add(b)
            comp += 1
    fa = Cache(size, block, size // block, policy="lru").run(trace).misses
    real = Cache(size, block, assoc, policy=policy).run(trace).misses
    return dict(compulsory=comp, capacity=fa - comp, conflict=real - fa, total=real)


def mem_trace(c_source: str, call: str, args: list[int] = (), data: dict | None = None, opt: str = "-O2"):
    """Compile a C kernel, call `call(args...)` on the course simulator and return (trace, result):
    trace is a list of (address, is_store) for every load and store executed inside the call."""
    import _rv32
    res_holder: dict = {}
    orig_run = _rv32.Sim.run

    def run(self, limit=10**7, trace=None, wtrace=None, mtrace=None):
        mt: list = []
        n = orig_run(self, limit=10**8, trace=trace, wtrace=wtrace, mtrace=mt)
        res_holder["mt"] = mt
        return n

    _rv32.Sim.run = run
    try:
        r = run_function({"k.c": c_source}, call, list(args), opt=opt, data=data, m=True)
    finally:
        _rv32.Sim.run = orig_run
    return [(a, st) for _, a, st in res_holder["mt"]], r


def words(values: list[int], base: int) -> dict:
    """Byte-addressed memory image of 32-bit words starting at `base`."""
    return {base + 4 * i + k: ((x & 0xFFFFFFFF) >> 8 * k) & 0xFF for i, x in enumerate(values) for k in range(4)}


# ---------------------------------------------------------------------------------------------------------------
# Workloads: the kernels of kernels.c on fixed data, each result checked
KERNELS = (Path(__file__).resolve().parent / "kernels.c").read_text()
BASE = 0x100000


def _signed(u: int) -> int:
    return u - (1 << 32) if u & 0x80000000 else u


def traverse(order: str = "rows", n: int = 64):
    """Sum an n x n matrix (values 0, 1, 2, ...) by rows or by columns."""
    tr, r = mem_trace(KERNELS, f"sum_{order}", [BASE, n], words(list(range(n * n)), BASE))
    assert r["value"] == n * n * (n * n - 1) // 2
    return tr, r


def histogram(n: int = 1000, seed: int = 7):
    """Histogram of n pseudo-random bytes into 16 integer bins (x at BASE, h at BASE + 0x4000)."""
    rng = random.Random(seed)
    xs = [rng.randrange(256) for _ in range(n)]
    h = BASE + 0x4000
    tr, r = mem_trace(KERNELS, "hist", [BASE, n, h], {BASE + i: v for i, v in enumerate(xs)})
    assert [r["sim"].load(h + 4 * k, 4) for k in range(16)] == [sum((v & 15) == k for v in xs) for k in range(16)]
    return tr, r


def copy(n: int = 256):
    """Copy n integers from BASE to BASE + 0x1000."""
    tr, r = mem_trace(KERNELS, "copy", [BASE + 0x1000, BASE, n], words(list(range(n)), BASE))
    assert all(r["sim"].load(BASE + 0x1000 + 4 * i, 4) == i for i in range(n))
    return tr, r


def transpose(n: int = 64, t: int | None = None):
    """Transpose an n x n matrix at BASE into BASE + 0x10000, untiled or in t x t tiles."""
    b = BASE + 0x10000
    args = [b, BASE, n] + ([t] if t else [])
    tr, r = mem_trace(KERNELS, "transpose_tiled" if t else "transpose", args, words(list(range(n * n)), BASE))
    assert all(r["sim"].load(b + 4 * (j * n + i), 4) == i * n + j for i in range(n) for j in range(n))
    return tr, r


def linked_list(n: int = 256, stride: int = 64):
    """Count the nodes of a list of n nodes placed `stride` bytes apart from BASE."""
    data: dict = {}
    for i in range(n):
        data.update(words([BASE + stride * (i + 1) if i < n - 1 else 0], BASE + stride * i))
    tr, r = mem_trace(KERNELS, "count", [BASE], data)
    assert r["value"] == n
    return tr, r


def matmul(version: str = "ikj", n: int = 32, t: int | None = None, seed: int = 5):
    """C = A B for n x n integer matrices at BASE, BASE + 0x4000 and BASE + 0x8000 (version ijk, ikj or tiled)."""
    rng = random.Random(seed)
    a = [rng.randrange(-9, 10) for _ in range(n * n)]
    b = [rng.randrange(-9, 10) for _ in range(n * n)]
    A, B, C = BASE, BASE + 0x4000, BASE + 0x8000
    args = [A, B, C, n] + ([t] if version == "tiled" else [])
    tr, r = mem_trace(KERNELS, f"mm_{version}", args, {**words(a, A), **words(b, B)})
    ref = [sum(a[i * n + k] * b[k * n + j] for k in range(n)) for i in range(n) for j in range(n)]
    assert [_signed(r["sim"].load(C + 4 * i, 4)) for i in range(n * n)] == ref
    return tr, r
