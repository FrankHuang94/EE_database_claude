# Problems 14-09 · Memory Hierarchy and Caches

Chapter: [14-09](../chapters/14-09-memory-hierarchy-and-caches.md) · Worked solutions: [14-09 solutions](../solutions/14-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Addresses are byte addresses; integers are 4 bytes; 1 KB = 1024 bytes.
- "The simulator" is the lab's `cache.py` (chapter §3.10), run on data-access traces of the lab's C kernels compiled for RV32IM. Caches use LRU replacement, write-back and write-allocate unless stated.
- Matrices are 32 × 32 integers for the matrix multiplies and 64 × 64 integers otherwise, stored row-major.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-09.1 [A]

**Address fields.** A 64 KB, 4-way set-associative cache has 64-byte blocks, and addresses are 32 bits. Find the number of sets and the field widths, then the offset, index and tag of the address 0xDEADBEEF.

### Problem 14-09.2 [A]

**Overhead of a large cache.** A 1 MB, 16-way cache with 64-byte blocks serves 40-bit physical addresses. Each line stores its tag, a valid bit and a dirty bit. Find the tag width, the total tag-and-state storage in KiB, and the overhead as a percentage of the data storage.

### Problem 14-09.3 [A]

**AMAT.** A cache hits in 1 cycle, misses on 4% of accesses, and a miss costs 60 extra cycles. (a) What is the AMAT? (b) What hit rate is needed for an AMAT of 2 cycles?

### Problem 14-09.4 [A]

**A cycle too long.** A cache of 4 blocks sees the block sequence 0, 4, 8, 0, 4, 8. Count the misses if it is (a) direct-mapped, (b) 2-way with LRU, (c) fully associative with LRU. Classify (a)'s misses. Why does (b) do no better than (a)?

### Problem 14-09.5 [B]

**LRU against FIFO.** In a 2-way set-associative cache with two sets, blocks 0, 2 and 4 all map to set 0. Trace the block sequence 0, 2, 0, 4, 0, 2 under LRU and under FIFO, and count each policy's misses.

### Problem 14-09.6 [B]

**From counters to rates.** Over 1000 instructions, a core makes 400 data accesses. 20 miss in L1, and 8 of those also miss in L2.

- (a) Find the L1 miss rate, the L2 local and global miss rates, and the L1 and L2 MPKI.
- (b) With hit times of 4 cycles (L1) and 12 cycles (L2) and a memory time of 150 cycles, find the AMAT.

### Problem 14-09.7 [B]

**Choosing a block size.** A 4 KB 4-way cache hits in 2 cycles. A miss costs 80 cycles plus the transfer of the block at 8 bytes per cycle. The simulator gives these miss counts for the `ijk` matrix multiply (66,560 accesses) and the `ikj` one (100,352 accesses):

| Block size (bytes) | 16 | 32 | 64 | 128 |
|---|---|---|---|---|
| `ijk` misses | 7464 | 6788 | 5612 | 5304 |
| `ikj` misses | 2987 | 1495 | 749 | 376 |

Find the AMAT for each block size and program, and the best block size for each. Why do they differ?

### Problem 14-09.8 [B]

**Transposing a matrix.** `b[j][i] = a[i][j]` for a 64 × 64 integer matrix reads `a` by rows and writes `b` by columns. A tiled version does the same work in 8 × 8 tiles. The cache is 4 KB with 32-byte blocks. Use the simulator to find each version's misses with a 2-way and a direct-mapped cache, and compare them with the compulsory misses.

### Problem 14-09.9 [B]

**Copying.** A loop copies 256 integers (1 KB) from one array to another. The cache is 4 KB, 2-way, with 32-byte blocks. Compare the bytes read from and written to memory with (a) write-back and write-allocate, and (b) write-through and no-write-allocate. Which is better here, and why?

### Problem 14-09.10 [B]

**Prefetching.** A tagged next-line prefetcher is added to a 4 KB 4-way cache with 32-byte blocks. Find the misses and the number of prefetches for:

- (a) the row traversal of Example 14-09.4;
- (b) the column traversal of Example 14-09.4;
- (c) a loop that follows a linked list of 256 nodes placed 64 bytes apart.

Which prefetches were useful?

### Problem 14-09.11 [B]

**Memory-level parallelism.** Memory latency is 100 ns and blocks are 64 bytes.

- (a) What bandwidth do 10 outstanding misses sustain?
- (b) How many must be in flight to stream at 1.2 TB/s, the bandwidth of one HBM3E stack?
- (c) If each core supports 24 outstanding misses, how many cores are needed?

### Problem 14-09.12 [C]

**Choosing a tile size.** The tiled matrix multiply of Example 14-09.6 is run with tiles of 4, 8, 16 and 32 on a 2 KB and on a 4 KB 4-way cache with 32-byte blocks. The simulator gives:

| Tile | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| 2 KB | 4356 | 1284 | 2714 | 4484 |
| 4 KB | 2671 | 1089 | 771 | 1499 |

Explain the best tile for each cache from the size of a tile of $B$, and why both very small and very large tiles do badly.

### Problem 14-09.13 [C]

**Energy per access.** Use Horowitz's 45 nm figures: 20 pJ per 64-bit read of a 32 KB cache, and 1.3–2.6 nJ per DRAM access. A miss costs a cache read plus a DRAM access. Find the average energy per access at miss rates of 5% and 1%, at both ends of the DRAM range. Compare it with a 32-bit add (0.1 pJ).

### Problem 14-09.14 [C]

**Which misses can an out-of-order core hide?** Two loops each make 256 loads.

- One sums an array of 256 integers.
- The other counts the nodes of a linked list whose 256 nodes are placed 64 bytes apart, one node per block.

The data cache is 4 KB, 4-way, with 64-byte blocks. A miss takes 100 cycles and a hit 3. The loads' latencies are taken from the cache simulator and fed into 14-08's model.

- (a) How many misses does each loop have?
- (b) Find their cycles on a 1-wide in-order core, and on a 4-wide out-of-order core with 64-entry and with 256-entry windows.
- (c) Explain the differences with Little's law.

---

## Objective coverage

| Learning objective (chapter 14-09) | Problems |
|---|---|
| 1. Locality and the hierarchy | 10, 13 |
| 2. Address fields and storage overhead | 1, 2 |
| 3. AMAT, CPI, local and global miss rates | 3, 6, 7 |
| 4. Simulation, the three Cs, replacement and write policies | 4, 5, 8, 9 |
| 5. Software and hardware techniques against misses | 8, 10, 11, 12, 14 |
