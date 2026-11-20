# Lab 14-09 · Memory Hierarchy and Caches

Chapter: [14-09 Memory Hierarchy and Caches](../../chapters/14-09-memory-hierarchy-and-caches.md)

## Objective

Measure caches the way architects first evaluate them, with trace-driven simulation. Compile small C kernels, run them on the course simulator, record every data address, and replay the traces through caches of different size, associativity, block size, replacement, write policy and prefetching. Then change the *code* (loop order, tiling) and see that it often matters more than the cache.

## Background

Locality and the hierarchy (§3.1), cache organization (§3.2), AMAT (§3.3), the three Cs (§3.4), replacement (§3.5), writes (§3.6), software and hardware techniques (§3.7–3.8) and the model (§3.10).

## Tools

Python with the LLVM tools of [Lab 14-03](../14-03-lab/README.md#tools) (`clang`, `ld.lld`), used through the course toolkit. Part 6 also uses the out-of-order model of [Lab 14-08](../14-08-lab/README.md).

## Files

- [kernels.c](kernels.c): the C kernels (matrix sums by rows and by columns, histogram, copy, list traversal, transpose, three matrix multiplies).
- [cache.py](cache.py): `mem_trace()` compiles and runs a kernel and returns its data accesses; `Cache` simulates one cache level; `three_c()` classifies misses; `traverse()`, `histogram()`, `copy()`, `linked_list()`, `transpose()` and `matmul()` produce checked traces.
- [14-09-caches-lab.ipynb](14-09-caches-lab.ipynb): the notebook (Parts 1–6).

## Procedure

1. **Mapping (Part 1).** Split addresses with `Cache.split`, and replay the nine accesses of Example 14-09.2 through direct-mapped, 2-way and fully associative caches, printing each set after every access.
2. **The three Cs (Part 2).** Classify the misses of the row and column traversals for direct-mapped caches of 1 to 16 KB, and for associativities 1 to 128 at 4 KB.
3. **Matrix multiply (Part 3).** Compare `ijk`, `ikj` and tiled versions across cache sizes, tile sizes, block sizes and replacement policies. *Predict first:* which tile size is best for a 2 KB cache?
4. **Writes (Part 4).** Count the memory traffic of the histogram and copy loops under the four combinations of write-back/write-through and allocate/no-allocate.
5. **Prefetching (Part 5).** Turn on next-line prefetching for the row and column traversals and the linked list, and count useful and wasted prefetches.
6. **Hiding misses (Part 6).** Feed each load's hit or miss latency into 14-08's out-of-order model, for an array sum and a list traversal, and sweep the window size.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 14-09.2 | 9, 7 and 5 misses |
| 2 | Column traversal | 3584 conflict misses for direct-mapped caches from 2 to 8 KB, none at 16 KB; at 4 KB, associativity up to 16 ways does not help, full associativity does |
| 3 | Matrix multiply | at 2 KB: 34,952, 4,480 and 1,284 misses; random replacement beats LRU on the untiled versions (30,271 against 34,952 for `ijk`); the best tile grows with the cache (771 misses with 16 × 16 tiles at 4 KB) |
| 4 | Writes | the histogram writes 64 bytes with write-back, 4000 with write-through; the copy reads 2048 bytes with write-allocate, 1024 without |
| 5 | Prefetching | rows: 1 miss left; columns and list: no misses removed, every prefetch wasted |
| 6 | Hiding misses | the array's 16 misses cost 1713 cycles with a 64-entry window, 913 with 128 and 537 with 256; the list's 256 misses cost 25,604 at any window |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-09.a | conflict misses, columns, 8 KB direct-mapped | 3584 | — |
| Lab 14-09.b | misses, ijk, 16 KB 4-way | 384 | — |
| Lab 14-09.c | misses, 16 × 16 tiles, 4 KB 4-way | 771 | — |
| Lab 14-09.d | misses, ijk, 2 KB 4-way, random | 30271 | — |
| Lab 14-09.e | misses, ikj, 2 KB 4-way, FIFO | 4720 | — |
| Lab 14-09.f | compulsory misses, rows | 512 | — |
| Lab 14-09.g | cycles, array sum, 4-wide, 128-entry window | 913 | — |

*These are recomputed by [verify_14_09.py](../../verify/verify_14_09.py), with the LRU and FIFO results re-simulated by independent code.*

## Discussion questions

1. Trace-driven cache simulation ignores timing. What does that miss in a real out-of-order core?
2. Why does random replacement beat LRU on the untiled matrix multiplies but lose on the tiled one?
3. A 16 KB 4-way cache brings every matrix multiply down to its compulsory misses. Why tile at all, then?

### Answers

1. The order of accesses in a real core is not program order. Out-of-order execution and prefetchers reorder and overlap accesses, and wrong-path loads after a mispredicted branch touch the cache too. A later access to a block whose miss is still outstanding is a "hit under miss" that still waits. Hit counts from a program-order trace are therefore a good first approximation, but timing needs a cycle-level model (Part 6 combines the two crudely).
2. The untiled loops sweep cyclically through more blocks than a set holds, which is LRU's worst case: the evicted block is always the next one needed. Random eviction sometimes keeps it. The tiled loop's working set fits, and there LRU's ordering keeps exactly the blocks being reused, while random evictions sometimes throw them out.
3. Because real problems are far bigger than 32 × 32. A 4096 × 4096 matrix of 4-byte values is 64 MB, larger than any on-chip cache. Tiling, at several levels for L1, L2 and L3, is what lets large problems run near the speed of the cache.

## Optional hardware extension

On a Linux machine, write the row and column traversals of a matrix much larger than the L3 cache in C, time them, and count misses with `perf stat -e cache-references,cache-misses`. Then measure the latency of a random pointer chase over a large array (the time per step is close to the DRAM load latency) and compare it with the "of order 100 ns" of the chapter's Numbers to know.
