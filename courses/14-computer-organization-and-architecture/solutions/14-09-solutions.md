# Solutions 14-09 · Memory Hierarchy and Caches

Problems: [14-09 problems](../problems/14-09-problems.md) · Chapter: [14-09](../chapters/14-09-memory-hierarchy-and-caches.md). Every number below is recomputed by [verify_14_09.py](../verify/verify_14_09.py).

- Simulated miss counts come from the lab's `cache.py` on traces of the lab's C kernels, and every result is checked.
- Each LRU result is re-simulated by an independent implementation, and fully associative results are also checked by Mattson's stack-distance algorithm.

---

## Solutions

### Solution 14-09.1

$S = 65536 / (64 \times 4)$ = **256** sets. The field widths are:

- offset: $\log_2 64$ = **6** bits;
- index: $\log_2 256$ = **8** bits;
- tag: $32 - 8 - 6$ = **18** bits.

For 0xDEADBEEF:

- offset: 0xEF & 0x3F = 0x2F = **47**;
- index: (0xDEADBEEF >> 6) & 0xFF = 0xFB = **251**;
- tag: 0xDEADBEEF >> 14 = **0x37AB6**.

### Solution 14-09.2

There are $2^{20} / (64 \times 16) = 1024$ sets, so the index has 10 bits and the offset 6. The tag is $40 - 10 - 6$ = **24** bits. The $2^{20}/64 = 16384$ lines each store $24 + 2 = 26$ bits: 425,984 bits = **52** KiB. That is **5.08**% of the 8,388,608 data bits.

### Solution 14-09.3

(a) $\text{AMAT} = 1 + 0.04 \times 60$ = **3.4** cycles.

(b) For an AMAT of 2 we need $1 + 60m = 2$, so $m = 1/60$ = 1.67% and the hit rate is **98.33**%. Halving the AMAT needs the miss rate cut by a factor of 2.4, which shows how sensitive AMAT is to small miss rates.

### Solution 14-09.4

(a) **Direct-mapped:** blocks 0, 4 and 8 all map to set 0, and each evicts the one before. All **6** accesses miss.

(b) **2-way LRU:** with 2 sets, all three blocks still share set 0, now with two ways. LRU always evicts the block that is needed next: after 0 and 4, block 8 evicts 0; then 0 evicts 4; then 4 evicts 8; and so on. All **6** miss.

(c) **Fully associative LRU:** the cache holds all three blocks, so only the first access to each misses: **3**.

(a)'s misses are **3** compulsory and **3** conflict. (b) does no better because a cycle of three blocks through a two-way set is LRU's worst case. Random replacement would sometimes keep the right block and hit.

### Solution 14-09.5

**LRU** (most recently used block last):

| Block | 0 | 2 | 0 | 4 | 0 | 2 |
|---|---|---|---|---|---|---|
| Set 0 after | 0 | 0 2 | 2 0 | 0 4 | 4 0 | 0 2 |
| Result | M | M | H | M | H | M |

That is **4** misses.

**FIFO** (oldest inserted block first; a hit changes nothing):

| Block | 0 | 2 | 0 | 4 | 0 | 2 |
|---|---|---|---|---|---|---|
| Set 0 after | 0 | 0 2 | 0 2 | 2 4 | 4 0 | 0 2 |
| Result | M | M | H | M | M | M |

That is **5** misses. FIFO evicts block 0 at the access to block 4, although 0 was just used, because 0 was inserted first.

### Solution 14-09.6

(a) The rates follow from the counts:

- L1 miss rate: 20/400 = **5**%.
- L2 local miss rate: 8/20 = **40**%.
- L2 global miss rate: 8/400 = **2**%.
- L1 MPKI: 20 misses per 1000 instructions = **20**; L2 MPKI = **8**.

(b) $\text{AMAT} = 4 + 0.05\,(12 + 0.4 \times 150)$ = **7.6** cycles.

### Solution 14-09.7

$\text{AMAT} = 2 + (\text{misses}/\text{accesses}) \times (80 + B/8)$:

| Block | 16 | 32 | 64 | 128 |
|---|---|---|---|---|
| Penalty (cycles) | 82 | 84 | 88 | 96 |
| `ijk` AMAT | **11.195** | **10.567** | **9.420** | **9.650** |
| `ikj` AMAT | **4.441** | **3.251** | **2.657** | **2.360** |

The best block size is **64** bytes for `ijk` and **128** bytes for `ikj`.

`ikj` streams along rows, so every byte of a larger block is used. Its miss count halves with each doubling of the block, faster than the penalty grows. `ijk` walks down a column of $B$, using only 4 bytes of each block it brings in. Larger blocks help it only a little (the neighbouring columns are used on later $j$ iterations, if the block survives), while costing a longer penalty and fewer blocks in the cache. The best block size depends on the workload's spatial locality, which is why real caches settle on a compromise, usually 64 bytes.

### Solution 14-09.8

| Version | 2-way | Direct-mapped |
|---|---|---|
| Untiled | **4608** | **4664** |
| Tiled, 8 × 8 | **1026** | **1194** |

The compulsory misses number **1024** (two 16 KB matrices in 32-byte blocks). The untiled version writes `b` down columns, 256 bytes apart, so each block of `b` is evicted before its neighbouring column fills the next 4 bytes. That is about 8 misses per block of `b`. The tiled version writes an 8 × 8 tile of `b`: 8 blocks, each filled completely before moving on. With 2 ways it misses only twice beyond the compulsory floor, both times on the stack, where the function saves registers. Direct-mapped adds conflicts between the tiles of `a` and `b`, whose addresses differ by a multiple of the cache size.

### Solution 14-09.9

(a) **Write-back, write-allocate:**

- reads: **2048** bytes, the 1 KB source plus the 1 KB destination, which is fetched on each store miss only to be overwritten;
- writes: **1024** bytes, the destination written back.

(b) **Write-through, no-write-allocate:**

- reads: **1024** bytes, the source only;
- writes: **1024** bytes, 256 stores of 4 bytes.

(b) moves a third less data. A pure streaming store never reads its destination, so write-allocate wastes a read of every block. Real cores detect such streams, or offer non-temporal store instructions, to avoid this.

### Solution 14-09.10

| Trace | Misses without | Misses with | Prefetches |
|---|---|---|---|
| (a) Rows | 512 | **1** | **512** |
| (b) Columns | 4096 | **4096** | **4096** |
| (c) Linked list | 256 | **256** | **256** |

(a) Only the first block misses. Each first use of a prefetched block fetches the next, so the stream stays one block ahead. All 512 prefetches but the last, which fetches the block after the matrix, are useful. This relies on the model's instant prefetches: in hardware, one block of lead is only 8 loads, far less than a memory latency, so a real prefetcher must run several blocks ahead to be on time.

(b) Every access still misses, and every prefetch is wasted. The next block in memory belongs to the same row, but it is first needed when the traversal reaches column $j_0 + 8$, up to 8 column passes later, by which time it has been evicted. The prefetches double the traffic for nothing.

(c) Each node is 64 bytes from the next, so the next 32-byte block is the unused second half of the node. All 256 prefetches are wasted. Next-line prefetching fails here because the stride is two blocks, not because the next address is unknowable: the lab places the nodes at a constant stride, so a stride prefetcher would cover nearly every miss. In a real heap the nodes are scattered, and the next address is known only after the current load returns. That is true pointer chasing, which defeats both prefetchers.

### Solution 14-09.11

(a) $10 \times 64 \text{ B} / 100 \text{ ns}$ = **6.4** GB/s.

(b) $1.2 \times 10^{12} \text{ B/s} \times 100 \times 10^{-9} \text{ s} / 64 \text{ B}$ = **1875** blocks in flight.

(c) $1875 / 24 = 78.1$, so **79** cores. A single core cannot use HBM's bandwidth. Accelerators get there with thousands of threads or deep DMA engines, each keeping requests in flight (14-13, 14-14).

### Solution 14-09.12

The best tile is **8** for the 2 KB cache and **16** for the 4 KB cache.

The inner loops reuse a $t \times t$ tile of $B$ for every row $i$. A tile of $B$ occupies $8 \times 8 \times 4$ = **256** bytes for $t$ = 8, and $16 \times 16 \times 4$ = **1024** bytes for $t$ = 16. The cache must also hold the current row segments of $A$ and $C$ and absorb conflicts, so the tile should use about half the cache or less:

- 1 KB in a 2 KB cache is too much, so $t$ = 16 does badly there;
- 1 KB in a 4 KB cache works best, giving the most reuse per tile.

Very small tiles (4) do not lose reuse of $B$: each tile of $B$ still serves all 32 rows, and on the 2 KB cache $B$ misses only **128** times, its compulsory blocks. The cost moves to $A$ and $C$. The loops sweep them $n/t$ = **8** times, and each 16-byte tile row uses only half of a 32-byte block, so $A$ misses **2048** times and $C$ **2176**. Smaller tiles also add loop overhead. A tile of 32 is the whole matrix, the same as no tiling (4484 against `ikj`'s 4480).

### Solution 14-09.13

Average energy per access $= 20 \text{ pJ} + m \times E_\text{DRAM}$:

| Miss rate | DRAM 1.3 nJ | DRAM 2.6 nJ |
|---|---|---|
| 5% | **85** pJ | **150** pJ |
| 1% | **33** pJ | **46** pJ |

Even at a 1% miss rate, the average access costs **330** times a 32-bit add (33 pJ against 0.1 pJ), and DRAM accounts for 39–57% of it. This is the quantitative reason why accelerators are organized around reuse in on-chip SRAM.

### Solution 14-09.14

(a) The array has **16** misses, one per 64-byte block of 16 integers. The list has **256**, one per node.

(b) The model gives:

| Core | Array | List |
|---|---|---|
| 1-wide in order | **3349** | **25861** |
| 4-wide out of order, 64 entries | **1713** | **25604** |
| 4-wide out of order, 256 entries | **537** | 25604 |

(c) Little's law explains the differences. The misses a core can overlap are limited by how far ahead its window reaches.

- **Array:** each block holds 16 elements of 5 instructions each, so consecutive misses are **80** instructions apart. A 64-entry window cannot reach the next block's load while a miss is outstanding, so the array's misses are still serviced one at a time: about 16 × 100 cycles plus the work. A 256-entry window spans three blocks, so about three misses overlap and the time falls to 537.
- **List:** each address is the previous load's result, so its 256 misses form a chain of 256 × 100 cycles. No window size helps. Only a shorter latency or a different data structure does.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-09.1a | sets | 256 | — |
| 14-09.1b | offset bits | 6 | bits |
| 14-09.1c | index bits | 8 | bits |
| 14-09.1d | tag bits | 18 | bits |
| 14-09.1e | offset of 0xDEADBEEF | 47 | — |
| 14-09.1f | index of 0xDEADBEEF | 251 | — |
| 14-09.1g | tag of 0xDEADBEEF | 0x37AB6 | — |
| 14-09.2a | tag bits | 24 | bits |
| 14-09.2b | tag and state storage | 52 | KiB |
| 14-09.2c | overhead | 5.08 | % |
| 14-09.3a | AMAT | 3.4 | cycles |
| 14-09.3b | hit rate for AMAT 2 | 98.33 | % |
| 14-09.4a | misses, direct-mapped | 6 | — |
| 14-09.4b | misses, 2-way LRU | 6 | — |
| 14-09.4c | misses, fully associative | 3 | — |
| 14-09.4d | compulsory misses | 3 | — |
| 14-09.4e | conflict misses | 3 | — |
| 14-09.5a | misses, LRU | 4 | — |
| 14-09.5b | misses, FIFO | 5 | — |
| 14-09.6a | L1 miss rate | 5 | % |
| 14-09.6b | L2 local miss rate | 40 | % |
| 14-09.6c | L2 global miss rate | 2 | % |
| 14-09.6d | L1 MPKI | 20 | — |
| 14-09.6e | L2 MPKI | 8 | — |
| 14-09.6f | AMAT | 7.6 | cycles |
| 14-09.7a | ijk AMAT, 16-byte blocks | 11.195 | cycles |
| 14-09.7b | ijk AMAT, 32-byte blocks | 10.567 | cycles |
| 14-09.7c | ijk AMAT, 64-byte blocks | 9.420 | cycles |
| 14-09.7d | ijk AMAT, 128-byte blocks | 9.650 | cycles |
| 14-09.7e | ikj AMAT, 16-byte blocks | 4.441 | cycles |
| 14-09.7f | ikj AMAT, 32-byte blocks | 3.251 | cycles |
| 14-09.7g | ikj AMAT, 64-byte blocks | 2.657 | cycles |
| 14-09.7h | ikj AMAT, 128-byte blocks | 2.360 | cycles |
| 14-09.7i | best block, ijk | 64 | B |
| 14-09.7j | best block, ikj | 128 | B |
| 14-09.8a | misses, untiled, 2-way | 4608 | — |
| 14-09.8b | misses, tiled, 2-way | 1026 | — |
| 14-09.8c | misses, untiled, direct-mapped | 4664 | — |
| 14-09.8d | misses, tiled, direct-mapped | 1194 | — |
| 14-09.8e | compulsory misses | 1024 | — |
| 14-09.9a | bytes read, write-back | 2048 | B |
| 14-09.9b | bytes written, write-back | 1024 | B |
| 14-09.9c | bytes read, write-through | 1024 | B |
| 14-09.9d | bytes written, write-through | 1024 | B |
| 14-09.10a | misses, rows | 1 | — |
| 14-09.10b | prefetches, rows | 512 | — |
| 14-09.10c | misses, columns | 4096 | — |
| 14-09.10d | prefetches, columns | 4096 | — |
| 14-09.10e | misses, list | 256 | — |
| 14-09.10f | prefetches, list | 256 | — |
| 14-09.11a | bandwidth, 10 outstanding | 6.4 | GB/s |
| 14-09.11b | outstanding misses for 1.2 TB/s | 1875 | — |
| 14-09.11c | cores needed | 79 | — |
| 14-09.12a | best tile, 2 KB | 8 | — |
| 14-09.12b | best tile, 4 KB | 16 | — |
| 14-09.12c | tile of B, t = 8 | 256 | B |
| 14-09.12d | tile of B, t = 16 | 1024 | B |
| 14-09.12e | B misses, t = 4, 2 KB | 128 | — |
| 14-09.12f | sweeps of A and C, t = 4 | 8 | — |
| 14-09.12g | A misses, t = 4, 2 KB | 2048 | — |
| 14-09.12h | C misses, t = 4, 2 KB | 2176 | — |
| 14-09.13a | energy, 5%, 1.3 nJ | 85 | pJ |
| 14-09.13b | energy, 1%, 1.3 nJ | 33 | pJ |
| 14-09.13c | energy, 5%, 2.6 nJ | 150 | pJ |
| 14-09.13d | energy, 1%, 2.6 nJ | 46 | pJ |
| 14-09.13e | ratio to a 32-bit add, 1%, 1.3 nJ | 330 | — |
| 14-09.14a | misses, array | 16 | — |
| 14-09.14b | misses, list | 256 | — |
| 14-09.14c | cycles, array, in order | 3349 | — |
| 14-09.14d | cycles, list, in order | 25861 | — |
| 14-09.14e | cycles, array, 64 entries | 1713 | — |
| 14-09.14f | cycles, array, 256 entries | 537 | — |
| 14-09.14g | cycles, list, out of order | 25604 | — |
| 14-09.14h | instructions between array misses | 80 | — |
