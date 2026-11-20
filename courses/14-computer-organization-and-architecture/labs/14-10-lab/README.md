# Lab 14-10 · Virtual Memory, TLBs and the OS Interface

Chapter: [14-10 Virtual Memory, TLBs and the OS Interface](../../chapters/14-10-virtual-memory.md)

## Objective

Build RISC-V Sv32 page tables in a simulated physical memory, walk them exactly as the hardware does, and measure what translation costs: TLB misses and PTE reads for different access patterns, TLB sizes and page sizes. Then play operating system: service page faults by demand paging, and compare replacement policies until you find the thrashing cliff.

## Background

Pages and translation (§3.1), Sv32 page tables and the walk (§3.2), the TLB (§3.3), VIPT caches (§3.4), page faults and replacement (§3.5), traps (§3.6) and the model (§3.7).

## Tools

Python only.

## Files

- [vm.py](vm.py):
  - `Memory` (physical words and a frame allocator);
  - `PageTable` (`map`, `map_mega`, `walk` per the Sv32 specification, raising `PageFault` with the RISC-V cause code);
  - `TLB` (LRU, 4 KiB and 4 MiB entries);
  - `MMU` (translation with demand paging under FIFO, LRU or clock);
  - `page_faults()` (reference-string model with FIFO, LRU and OPT).
- [14-10-virtual-memory-lab.ipynb](14-10-virtual-memory-lab.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Walks (Part 1).** Map a few pages and a megapage, print the PTEs, and walk addresses that succeed and that fault. Reproduce Example 14-10.2, including the A bit the walk sets.
2. **TLB reach (Part 2).** Traverse a 1024 × 1024 integer matrix by rows and by columns with TLBs of 16 to 1024 entries, with 4 KiB pages and with one megapage. *Predict first:* the column traversal's misses with 1023 and with 1024 entries.
3. **Page-table memory (Part 3).** Count the page-table pages of dense and sparse address spaces.
4. **Demand paging (Part 4).** Run reference strings through the MMU with too few frames, under FIFO, LRU and clock, and compare with OPT.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 14-10.2 | 0x1234_5ABC after 2 PTE reads; the PTE becomes 0x048D_1457; a fetch faults with cause 12 |
| 2 | TLB reach | rows: 1024 misses with any TLB of 16 entries or more; columns: every access misses below 1024 entries, 1024 misses from 1024 entries up, 1 with a megapage |
| 3 | Page tables | a dense 4 MiB mapping needs 2 table pages; Example 14-10.1's sparse process needs 4 |
| 4 | Replacement | on the string 1, 2, 3, 1, 4, 1, 5, 1, 2, 1, 3, 1, 4 with 3 frames: FIFO 10, clock 9, LRU 8, OPT 7 faults; the cyclic loop of Problem 14-10.12 thrashes under clock too (100 faults with 9 frames) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-10.a | TLB misses, rows, 16 entries | 1024 | — |
| Lab 14-10.b | TLB misses, columns, 512 entries | 1048576 | — |
| Lab 14-10.c | table pages, dense 4 MiB | 2 | — |
| Lab 14-10.d | clock faults, cyclic loop, 9 frames | 100 | — |
| Lab 14-10.e | clock faults, reuse string, 3 frames | 9 | — |
| Lab 14-10.f | FIFO faults, reuse string | 10 | — |
| Lab 14-10.g | LRU faults, reuse string | 8 | — |
| Lab 14-10.h | OPT faults, reuse string | 7 | — |
| Lab 14-10.i | OPT faults, cyclic loop, 5 frames | 60 | — |

*These are recomputed by [verify_14_10.py](../../verify/verify_14_10.py).*

## Discussion questions

1. Why does the clock algorithm do better than FIFO on the reuse string but no better on the cyclic loop?
2. The model flushes the whole TLB whenever a page is evicted. What would a real operating system do, and what does it cost on a multicore?
3. Why can a TLB miss be much cheaper than its two PTE reads suggest?

### Answers

1. Clock gives a page a second chance if its accessed bit is set. On the reuse string, clock evicts page 1 once, at the first eviction, when every bit is set and the sweep falls back to the oldest page. After that, page 1 is used every other reference, so its bit is set whenever the hand reaches it and it survives. FIFO evicts it a second time when it again becomes the oldest. In the cyclic loop every resident page has been used since the hand last passed, so every sweep clears all the bits, and clock degenerates to FIFO, as LRU itself does on that loop.
2. It would invalidate only the evicted page's translation (SFENCE.VMA with that address). On a multicore it must also send an interprocessor interrupt to every core that may cache the translation, and wait for them, which is a TLB shootdown and costs microseconds.
3. PTEs are ordinary data and are cached like any other. A walk whose PTEs hit in L1 costs a few cycles per level, and real cores also cache upper-level PTEs in dedicated structures, so most walks never reach DRAM.

## Optional hardware extension

On a Linux machine, time a loop that touches one byte in each 4 KiB page of a large buffer, with and without huge pages (for example with `madvise(MADV_HUGEPAGE)` or a huge-page mount), and count TLB misses with `perf stat -e dTLB-load-misses`.
