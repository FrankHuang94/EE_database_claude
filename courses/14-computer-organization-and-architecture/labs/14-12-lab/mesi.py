"""A snooping cache-coherence simulator for Lab 14-12.

`System(cores, protocol="MESI" | "MSI", block=64)` gives each core a private cache (unbounded, so every miss after
the first access to a block is a coherence miss) on a shared snooping bus. `access(core, addr, write)` applies
one memory operation and the protocol's transitions:

- read hit (M, E or S): no bus traffic;
- read miss: BusRd; a core holding the block in M supplies it and writes it back (flush), and every holder drops
  to S; the requester gets E if no other core holds the block (MESI) or S otherwise (MSI always gives S);
- write hit in M: nothing; in E: silent upgrade to M (MESI); in S: BusUpgr invalidates the other copies;
- write miss: BusRdX; an M holder flushes, every other copy is invalidated, the requester gets M.

Each write stores a fresh version number, and every read checks that it returns the most recent write (the
data-value invariant); after every operation the simulator checks the single-writer/multiple-reader invariant.
`stats` counts bus transactions, invalidations, flushes, cache-to-cache transfers and misses by kind.
"""
from __future__ import annotations

from collections import Counter


class System:
    def __init__(self, cores: int, protocol: str = "MESI", block: int = 64):
        assert protocol in ("MESI", "MSI")
        self.n, self.protocol, self.block = cores, protocol, block
        self.state = [dict() for _ in range(cores)]   # block -> 'M' | 'E' | 'S'
        self.value = [dict() for _ in range(cores)]   # block -> version held in that cache
        self.memory: dict = {}                         # block -> version in memory
        self.latest: dict = {}                         # block -> newest version written anywhere
        self.seen: set = set()                         # (core, block) pairs ever cached, to classify misses
        self.stats = Counter()

    def _others(self, core, b):
        return [c for c in range(self.n) if c != core and b in self.state[c]]

    def _flush_from(self, c, b):
        """Core c holds b in M: write it back (memory and requester get its data)."""
        self.memory[b] = self.value[c][b]
        self.stats["flush"] += 1

    def access(self, core: int, addr: int, write: bool = False) -> None:
        b = addr // self.block
        st = self.state[core].get(b)
        s = self.stats
        s["accesses"] += 1
        if not write:
            if st is None:
                s["misses"] += 1
                s["coherence_misses" if (core, b) in self.seen else "cold_misses"] += 1
                s["BusRd"] += 1
                holders = self._others(core, b)
                data = self.memory.get(b, 0)
                for c in holders:
                    if self.state[c][b] == "M":
                        self._flush_from(c, b)
                        data = self.value[c][b]
                    self.state[c][b] = "S"
                if holders:
                    s["cache_to_cache"] += 1
                self.state[core][b] = "E" if (self.protocol == "MESI" and not holders) else "S"
                self.value[core][b] = data
                self.seen.add((core, b))
            assert self.value[core][b] == self.latest.get(b, 0), "data-value invariant violated"
        else:
            if st == "M":
                pass
            elif st == "E":
                s["silent_upgrades"] += 1
            elif st == "S":
                s["BusUpgr"] += 1
                for c in self._others(core, b):
                    del self.state[c][b]
                    s["invalidations"] += 1
            else:
                s["misses"] += 1
                s["coherence_misses" if (core, b) in self.seen else "cold_misses"] += 1
                s["BusRdX"] += 1
                for c in self._others(core, b):
                    if self.state[c][b] == "M":
                        self._flush_from(c, b)
                        s["cache_to_cache"] += 1
                    del self.state[c][b]
                    s["invalidations"] += 1
                self.seen.add((core, b))
            self.state[core][b] = "M"
            v = self.latest.get(b, 0) + 1
            self.latest[b] = v
            self.value[core][b] = v
        self._check(b)

    def _check(self, b):
        sts = [self.state[c].get(b) for c in range(self.n)]
        owners = sum(x in ("M", "E") for x in sts)
        assert owners <= 1 and not (owners == 1 and "S" in sts), f"SWMR violated for block {b}: {sts}"

    @property
    def bus(self) -> int:
        """Bus transactions (requests; flushes ride on the same transaction)."""
        return self.stats["BusRd"] + self.stats["BusRdX"] + self.stats["BusUpgr"]

    def run(self, ops) -> System:
        for core, addr, write in ops:
            self.access(core, addr, write)
        return self


# ---------------------------------------------------------------------------------------------------------------
# Workloads: per-core operation streams interleaved round-robin
def round_robin(streams: list[list]) -> list:
    """Interleave per-core lists of (addr, write) one operation at a time: core 0, core 1, ..., core 0, ..."""
    out, i = [], 0
    while any(i < len(st) for st in streams):
        for c, st in enumerate(streams):
            if i < len(st):
                out.append((c, *st[i]))
        i += 1
    return out


def counters(n_cores: int, increments: int, stride: int, base: int = 0x1000) -> list:
    """Each core increments its own counter (a load then a store) `increments` times; counters `stride` bytes
    apart (4 = packed into one block: false sharing; 64 = one block each)."""
    return round_robin([[(base + stride * c, w) for _ in range(increments) for w in (False, True)]
                        for c in range(n_cores)])


def spin_lock(n_cores: int, spins: int, kind: str, lock: int = 0x2000) -> list:
    """Core 0 holds the lock; cores 1.. spin `spins` times each with test-and-set (an atomic swap, a write) or
    test-and-test-and-set (read until free); then core 0 releases it (a write) and every spinner tries once."""
    streams = [[] for _ in range(n_cores)]
    streams[0].append((lock, True))                          # acquire
    for c in range(1, n_cores):
        streams[c] = [(lock, kind == "tas")] * spins
    ops = round_robin(streams)
    ops.append((0, lock, True))                              # release
    for c in range(1, n_cores):                              # each waiter sees it free and attempts the swap
        if kind == "ttas":
            ops.append((c, lock, False))
        ops.append((c, lock, True))
    return ops
