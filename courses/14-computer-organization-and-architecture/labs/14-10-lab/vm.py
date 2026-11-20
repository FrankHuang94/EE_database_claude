"""Sv32 virtual memory for Lab 14-10: page tables, a page-table walker, TLBs and demand paging.

- `Memory` is a sparse physical memory of 32-bit words, with a frame allocator.
- `PageTable` builds RISC-V Sv32 page tables in that memory (`map` for 4 KiB pages, `map_mega` for 4 MiB
  megapages) and `walk`s them following the privileged specification's translation algorithm (§11.1.3.2):
  two levels, 4-byte PTEs, V/R/W/X/U/A/D checks, misaligned-superpage faults, A and D updates. A walk returns
  the physical address and the number of PTE reads, or raises `PageFault` with the RISC-V exception code
  (12 instruction, 13 load, 15 store/AMO page fault).
- `TLB` is a set-associative (or fully associative) LRU cache of translations, holding 4 KiB and 4 MiB entries.
- `MMU` translates a stream of (virtual address, is_store) accesses through the TLB and the walker, and can
  service page faults by demand paging with a limited number of frames and FIFO, LRU or clock replacement.
"""
from __future__ import annotations

from collections import OrderedDict

PAGE = 4096
MEGA = 4 * 1024 * 1024
V, R, W, X, U, G, A, D = (1 << k for k in range(8))
CAUSE = {"fetch": 12, "load": 13, "store": 15}


class PageFault(Exception):
    def __init__(self, va: int, access: str, reason: str):
        super().__init__(f"{access} page fault at {va:#010x}: {reason}")
        self.va, self.access, self.reason, self.cause = va, access, reason, CAUSE[access]


def fields(va: int) -> tuple[int, int, int]:
    """(VPN[1], VPN[0], page offset) of an Sv32 virtual address."""
    return va >> 22 & 0x3FF, va >> 12 & 0x3FF, va & 0xFFF


class Memory:
    """Sparse physical memory of 32-bit words; frames are allocated from `first_frame` upward."""

    def __init__(self, first_frame: int = 0x80000):
        self.words: dict[int, int] = {}
        self.next_frame = first_frame

    def read(self, pa: int) -> int:
        return self.words.get(pa, 0)

    def write(self, pa: int, val: int) -> None:
        self.words[pa] = val & 0xFFFFFFFF

    def alloc(self) -> int:
        """A fresh, zeroed physical page number."""
        f = self.next_frame
        self.next_frame += 1
        return f


class PageTable:
    def __init__(self, mem: Memory, asid: int = 0):
        self.mem = mem
        self.root = mem.alloc()           # satp.PPN
        self.asid = asid

    @property
    def satp(self) -> int:
        return 1 << 31 | self.asid << 22 | self.root

    def _l1_entry(self, va: int) -> int:
        return self.root * PAGE + fields(va)[0] * 4

    def map(self, va: int, ppn: int, flags: int = R | W | U) -> None:
        """Map the 4 KiB page containing `va` to physical page `ppn` (allocating a level-0 table if needed)."""
        e1 = self._l1_entry(va)
        pte1 = self.mem.read(e1)
        if not pte1 & V:
            t = self.mem.alloc()
            pte1 = t << 10 | V
            self.mem.write(e1, pte1)
        assert not pte1 & (R | X), "region already mapped by a megapage"
        e0 = (pte1 >> 10) * PAGE + fields(va)[1] * 4
        self.mem.write(e0, ppn << 10 | flags | V)

    def map_mega(self, va: int, ppn: int, flags: int = R | W | U) -> None:
        """Map the 4 MiB megapage containing `va` to physical pages ppn ... ppn + 1023 (ppn 1024-aligned)."""
        self.mem.write(self._l1_entry(va), ppn << 10 | flags | V)

    def unmap(self, va: int) -> None:
        e1 = self.mem.read(self._l1_entry(va))
        if e1 & V and not e1 & (R | X):
            self.mem.write((e1 >> 10) * PAGE + fields(va)[1] * 4, 0)

    def walk(self, va: int, access: str = "load", user: bool = True, sum_: bool = False) -> tuple[int, int, int]:
        """Translate per the Sv32 algorithm. Returns (pa, PTE reads, level of the leaf: 1 megapage, 0 page)."""
        vpn = [va >> 12 & 0x3FF, va >> 22 & 0x3FF]
        a, i, reads = self.root * PAGE, 1, 0
        while True:
            pte_addr = a + vpn[i] * 4
            pte = self.mem.read(pte_addr)
            reads += 1
            if not pte & V or (not pte & R and pte & W):
                raise PageFault(va, access, "invalid PTE")
            if pte & (R | X):
                break
            i -= 1
            if i < 0:
                raise PageFault(va, access, "no leaf at level 0")
            a = (pte >> 10) * PAGE
        ppn = pte >> 10
        if i > 0 and ppn & 0x3FF:
            raise PageFault(va, access, "misaligned superpage")
        if user and not pte & U:
            raise PageFault(va, access, "supervisor page")
        if not user and pte & U and (access == "fetch" or not sum_):
            raise PageFault(va, access, "user page from supervisor mode")
        need = {"fetch": X, "load": R, "store": W}[access]
        if not pte & need:
            raise PageFault(va, access, "permission")
        new = pte | A | (D if access == "store" else 0)
        if new != pte:
            self.mem.write(pte_addr, new)
        if i == 1:
            pa = (ppn >> 10) << 22 | (va & (MEGA - 1))
        else:
            pa = ppn << 12 | (va & 0xFFF)
        return pa, reads, i


class TLB:
    """LRU translation cache with `entries` entries in `assoc`-way sets (assoc = entries: fully associative).
    Holds 4 KiB entries (key: VPN) and 4 MiB entries (key: VPN[1]); a lookup checks both."""

    def __init__(self, entries: int = 64, assoc: int | None = None):
        self.entries, self.assoc = entries, assoc or entries
        self.nsets = self.entries // self.assoc
        self.sets = [OrderedDict() for _ in range(self.nsets)]
        self.hits = self.misses = 0

    def _set(self, key) -> OrderedDict:
        return self.sets[key[1] % self.nsets]

    def lookup(self, va: int):
        for key in ((0, va >> 12), (1, va >> 22)):
            s = self._set(key)
            if key in s:
                s.move_to_end(key)
                self.hits += 1
                return s[key]
        self.misses += 1
        return None

    def insert(self, va: int, level: int, frame_base: int) -> None:
        key = (level, va >> (22 if level else 12))
        s = self._set(key)
        if len(s) == self.assoc:
            s.popitem(last=False)
        s[key] = (level, frame_base)

    def flush(self) -> None:
        for s in self.sets:
            s.clear()

    @property
    def reach(self) -> int:
        return self.entries * PAGE


class MMU:
    """Translates accesses through a TLB and the walker. With `frames` set, page faults are serviced by demand
    paging: the faulting page gets a frame, evicting a resident page (policy fifo, lru or clock) when all
    `frames` are in use."""

    def __init__(self, pt: PageTable, tlb: TLB, frames: int | None = None, policy: str = "lru"):
        self.pt, self.tlb, self.frames, self.policy = pt, tlb, frames, policy
        self.walks = self.pte_reads = self.faults = self.evictions = 0
        self.resident: OrderedDict = OrderedDict()   # virtual page -> physical page, in FIFO/LRU order
        self.refbit: dict = {}                        # clock: the A bit the OS reads and clears
        self.slots: list = []                         # clock: virtual pages in frame order (a circular buffer)
        self.hand = 0

    def _evict(self) -> tuple[int, int]:
        """Choose a victim page; return (its slot in the clock buffer or -1, its physical page)."""
        slot = -1
        if self.policy == "clock":
            while self.refbit.get(self.slots[self.hand]):
                self.refbit[self.slots[self.hand]] = False       # second chance: clear and move on
                self.hand = (self.hand + 1) % len(self.slots)
            slot, vp = self.hand, self.slots[self.hand]
            self.hand = (self.hand + 1) % len(self.slots)
            ppn = self.resident.pop(vp)
        else:
            vp, ppn = self.resident.popitem(last=False)
        self.pt.unmap(vp << 12)
        self.tlb.flush()                             # a real OS would flush just this entry (SFENCE.VMA va)
        self.evictions += 1
        return slot, ppn

    def access(self, va: int, store: bool = False) -> int:
        vp = va >> 12
        if vp in self.resident:
            self.refbit[vp] = True
            if self.policy == "lru":
                self.resident.move_to_end(vp)
        hit = self.tlb.lookup(va)
        if hit is not None:
            level, base = hit
            return base | (va & ((MEGA if level else PAGE) - 1))
        try:
            pa, reads, level = self.pt.walk(va, "store" if store else "load")
        except PageFault:
            if self.frames is None:
                raise
            self.faults += 1
            if len(self.resident) >= self.frames:
                slot, ppn = self._evict()
            else:
                slot, ppn = -1, self.pt.mem.alloc()
            self.pt.map(va, ppn)
            self.resident[vp] = ppn
            self.refbit[vp] = True
            if slot >= 0:
                self.slots[slot] = vp
            else:
                self.slots.append(vp)
            pa, reads, level = self.pt.walk(va, "store" if store else "load")
        self.walks += 1
        self.pte_reads += reads
        self.tlb.insert(va, level, pa & ~((MEGA if level else PAGE) - 1))
        return pa


def page_faults(refs: list[int], frames: int, policy: str = "fifo") -> int:
    """Page faults of a reference string of page numbers with `frames` frames (fifo, lru or opt)."""
    mem: list = []
    faults = 0
    for t, p in enumerate(refs):
        if p in mem:
            if policy == "lru":
                mem.remove(p)
                mem.append(p)
            continue
        faults += 1
        if len(mem) == frames:
            if policy == "opt":
                future = refs[t + 1:]
                victim = max(mem, key=lambda q: future.index(q) if q in future else len(future) + 1)
                mem.remove(victim)
            else:
                mem.pop(0)
        mem.append(p)
    return faults
