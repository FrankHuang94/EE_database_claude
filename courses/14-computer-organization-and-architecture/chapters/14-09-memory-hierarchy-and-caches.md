<!-- status: verified -->
# 14-09 · Memory Hierarchy and Caches

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The memory-hierarchy unit of a computer organization and architecture course: locality, cache organization, average memory access time, replacement and write policies, multilevel caches, software and hardware techniques for reducing misses (Patterson & Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 5; Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, ch. 2 and App. B) |
| **Prerequisites** | [14-08 Out-of-Order and Superscalar Execution](14-08-out-of-order-and-superscalar.md), [08-11 Memories and Programmable Logic](../../08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md), [05-06 C Pointers, Arrays and Memory](../../05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Explain temporal and spatial locality, and why a hierarchy of small fast memories and large slow ones gives nearly the speed of the first at nearly the cost of the second.
2. Split an address into tag, index and offset for direct-mapped, set-associative and fully associative caches, and compute a cache's storage overhead.
3. Compute average memory access time (AMAT) and the CPI cost of misses for one- and two-level hierarchies, using local and global miss rates.
4. Simulate a cache on an address trace, classify its misses as compulsory, capacity or conflict, and compare replacement and write policies by misses and traffic.
5. Reduce misses in software (loop order, tiling) and explain the hardware techniques (prefetching, non-blocking caches, memory-level parallelism) that hide the rest.

---

## 1. Big picture

A processor core can start several instructions per cycle (14-08), but main memory takes hundreds of cycles to answer a load. A core that waited for memory on every access would run hundreds of times slower than its pipeline allows. The **memory hierarchy** solves this with a sequence of memories. Each level is smaller, faster and more expensive per bit than the one below it. The levels are registers, level-1 (L1) caches of tens of kilobytes, an L2 of around a megabyte, a shared L3 of tens of megabytes, then DRAM or HBM of gigabytes. The hierarchy works because programs do not access memory at random: they reuse recently used data and touch neighbouring addresses. A cache that keeps recently used blocks close to the core serves almost every access, and the rare misses go further down.

- **Locality makes it work.** Most loops find nearly all of their data in the L1 cache. The exceptions, such as pointer chasing, huge random tables and streams too big to reuse, are where performance problems live.
- **Misses dominate time and energy.** A DRAM access costs about a hundred times the energy of a cache read [1, R-208]. Most data-movement optimizations, in CPUs and in AI accelerators, exist to avoid it.
- **Software matters as much as hardware.** The same matrix multiply runs 8 times faster after a change of loop order and tiling (Example 14-09.6), on the same cache.
- **Bandwidth is a separate problem.** Out-of-order cores and accelerators overlap many misses at once. Then the limit becomes how many bytes per second the memory can deliver, which is why AI processors use HBM (§3.9).

## 2. Intuition first

**A desk, a bookshelf and a library.** You are writing a report. The books you are using lie open on your desk (the L1 cache): you can reach them in a second. A shelf behind you holds a few dozen more (L2). Anything else means a walk to the library stacks (main memory), which takes minutes. You do not fetch one page at a time; you fetch the whole book, because the next page you need is probably nearby (**spatial locality**). You keep the books you just used on the desk, because you will probably use them again soon (**temporal locality**). When the desk is full, something must go back to the shelf. The best choice is the book you will not need for longest, and the usual approximation is the one you have not touched for longest (**least recently used**).

**Where the analogy breaks.**

- A cache decides by rules fixed in hardware, not by judgment. Each block may only sit in a few fixed places (its **set**), so two blocks can keep evicting each other while the rest of the desk lies empty. These are *conflict misses*, which a person would never suffer.
- A cache cannot see the future. It cannot know which block will be needed next, only which were used recently.
- Writing changes things. A corrected page must eventually go back to the library copy, now (write-through) or when the book leaves the desk (write-back).

## 3. Theory

### 3.1 Locality and the hierarchy

A program shows **temporal locality** when data it has accessed is likely to be accessed again soon: a loop counter, a running sum, the instructions of a loop body. It shows **spatial locality** when data near a recent access is likely to be accessed soon: the next element of an array, the next instruction. A cache exploits both. It keeps recently used data, and it moves data in **blocks** (or **lines**) of typically 32 to 128 bytes, so one miss brings in the neighbours too.

Why not make all memory fast? Because size and speed conflict physically. A larger SRAM array has longer word lines and bit lines, with more capacitance to charge through the same small transistors, so it is slower and costs more energy per access. Horowitz's 45 nm figures show the trend [1, R-208]:

| Access (64 bits, 45 nm) | Energy |
|---|---|
| 8 KB cache | 10 pJ |
| 32 KB cache | 20 pJ |
| 1 MB cache | 100 pJ |
| DRAM | 1.3–2.6 nJ |

A 32-bit integer add costs 0.1 pJ in the same table, so fetching its operands from DRAM costs over 10,000 times more energy than the arithmetic. (SRAM cell design is the subject of [19-08](../../19-digital-vlsi-design/chapters/19-08-sram-design.md); DRAM's of [23-03](../../23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md).)

The hierarchy's promise: if a fraction $h$ of accesses hit in a fast level of access time $t_1$, and the rest pay a penalty $t_p$, the average time is $t_1 + (1-h)t_p$. With $h$ close to 1 this is close to $t_1$, while the capacity is that of the slow level.

### 3.2 Cache organization

A cache of capacity $C$ bytes holds $C/B$ blocks of $B$ bytes each. The blocks are grouped into $S$ **sets** of $A$ blocks (**ways**) each, so

$$
S = \frac{C}{B \cdot A}.
$$

A block of memory may be placed only in one set, chosen by its address, but in any way of that set. The address of a byte is split into three fields:

$$
\underbrace{\text{tag}}_{n - \log_2 S - \log_2 B \text{ bits}} \;\Big|\; \underbrace{\text{index}}_{\log_2 S \text{ bits}} \;\Big|\; \underbrace{\text{offset}}_{\log_2 B \text{ bits}}
$$

- The **offset** selects a byte within the block.
- The **index** selects the set. It is the block number $\lfloor \text{address}/B \rfloor$ modulo $S$.
- The **tag** is the rest of the address. It is stored with the block, so that a lookup can tell which of the many memory blocks that map to this set is actually present.

A lookup reads the $A$ tags of the indexed set in parallel and compares each with the address's tag. A match on a **valid** line is a **hit**. Three special cases have names:

- **Direct-mapped** ($A = 1$): each block has exactly one possible place. It is the simplest and fastest design (one comparator, no choice of victim), but two blocks with the same index evict each other.
- **$A$-way set-associative:** $A$ comparators, and a replacement policy chooses the victim within the set.
- **Fully associative** ($S = 1$, $A = C/B$): any block anywhere. A comparator per line makes this practical only for small structures, such as TLBs (14-10).

Each line also stores a valid bit, a **dirty** bit for write-back caches (§3.6), and replacement state. The tag and state bits are the cache's storage overhead (Example 14-09.1).

> **Math refresher — logarithms base 2.** A field that selects one of $2^k$ things needs $k$ bits: $\log_2 64 = 6$, $\log_2 1024 = 10$. Cache parameters are powers of two so that the fields are plain bit ranges of the address, extracted with no arithmetic.

### 3.3 Measuring performance: AMAT and CPI

The **hit rate** is the fraction of accesses that hit; the **miss rate** $m = 1 - h$. The **average memory access time** is

$$
\text{AMAT} = t_\text{hit} + m \cdot t_\text{penalty},
$$

where $t_\text{hit}$ is the hit time and $t_\text{penalty}$ the extra time to fetch the block from the next level. With two levels of cache,

$$
\text{AMAT} = t_{1} + m_1 \bigl(t_{2} + m_{2,\text{local}} \, t_\text{mem}\bigr).
$$

Here $m_1$ is L1's miss rate and $m_{2,\text{local}}$ is L2's **local** miss rate: the fraction of *the accesses that reach L2* that miss there. The **global** L2 miss rate, $m_1 m_{2,\text{local}}$, is the fraction of *all* accesses that go to memory. Local miss rates of large L2s look poor (L2 sees only the hard accesses that L1 missed), so compare levels by global rates, or by **misses per thousand instructions (MPKI)**:

$$
\text{MPKI} = 1000 \times \frac{\text{memory accesses}}{\text{instruction}} \times m .
$$

For a simple in-order core that stalls on every miss, the CPI rises by

$$
\Delta\text{CPI} = \frac{\text{accesses}}{\text{instruction}} \times m \times t_\text{penalty}
$$

(Example 14-09.3). An out-of-order core hides part of the penalty by executing independent work, and overlaps several misses at once. How much it hides depends on whether the misses are independent of each other (Problem 14-09.14).

### 3.4 Why misses happen: the three Cs

Every miss falls into one of three classes:

- **Compulsory (cold) misses:** the first access to a block. Even an infinite cache has them.
- **Capacity misses:** the program's working set is larger than the cache, so blocks are evicted before they are reused. A fully associative cache of the same size still has them.
- **Conflict misses:** too many active blocks map to the same set. A fully associative cache of the same size would not have them.

Operationally, compulsory misses are counted with an infinite cache, capacity misses as the extra misses of a fully associative LRU cache of the same size, and conflict misses as the extra misses of the real cache beyond that. Each design knob acts on a different class:

| Change | Compulsory | Capacity | Conflict | Cost |
|---|---|---|---|---|
| Larger cache | — | fewer | fewer | Slower hit, more area and energy |
| Higher associativity | — | — | fewer | More comparators, slower and costlier hit |
| Larger blocks | fewer (more spatial locality captured) | can rise (fewer blocks) | can rise | Longer miss penalty, more traffic for unused bytes |
| Prefetching | fewer | fewer | — | Traffic and pollution when wrong |

> **Going deeper — when conflict misses are negative.** The classification compares against a fully associative cache with LRU replacement, but LRU is not optimal. A loop that cycles through slightly more blocks than the cache holds makes LRU miss on *every* access, because the block evicted is always the next one needed. A set-associative cache splits that cycle across sets, and some sets keep their blocks. In the lab, the `ikj` matrix multiply on a 4 KB 4-way cache misses 1495 times, while the same-size fully associative LRU cache misses 4480 times, giving a "conflict" count of −2985. Belady's optimal policy, which evicts the block used furthest in the future, needs the future and so is only a yardstick for simulation, but it never does worse than any other policy.

### 3.5 Replacement

When a set is full, a miss must evict one of its $A$ blocks.

- **LRU (least recently used)** evicts the block unused for longest. It exploits temporal locality well, but exact LRU needs an ordering of $A$ ways, which costs state and logic for $A > 4$ or so. Real designs use approximations such as **tree pseudo-LRU**, with $A - 1$ bits per set.
- **FIFO** evicts the oldest *inserted* block, ignoring reuse. It is simpler but usually worse than LRU.
- **Random** evicts any block. It needs no state, and it avoids LRU's worst case on cyclic patterns (Problem 14-09.4). In the lab, random beats LRU on the untiled matrix multiplies and loses on the tiled one.

### 3.6 Writes

A store that hits can update the cache in one of two ways:

- **Write-through:** update the next level on every store as well. Memory is always current and lines are never dirty. Every store costs bandwidth, so a **write buffer** holds stores and lets the core continue.
- **Write-back:** update only the cache and set the line's dirty bit. The block is written to the next level once, when it is evicted. This saves bandwidth when a block is written many times (Example 14-09.5), at the cost of dirty-bit state and an extra write on eviction.

A store that misses also has two options:

- **Write-allocate:** fetch the block, then write into it. This is natural with write-back.
- **No-write-allocate:** send the store to the next level without fetching. This is natural with write-through. It is better for **streaming** stores that overwrite whole blocks without reading them, because write-allocate fetches data that is immediately overwritten (Problem 14-09.9).

### 3.7 Software: loop order and tiling

A cache rewards code whose access pattern matches its blocks. C stores a two-dimensional array **row-major**: `a[i][j]` and `a[i][j+1]` are adjacent. Traversing rows touches each block once for $B/4$ consecutive integers. Traversing columns jumps $4n$ bytes per access, so each access lands in a different block. In Example 14-09.4 a column traversal misses on every access and a row traversal on one in eight.

Matrix multiplication $C = AB$ has the three loops $i$, $j$, $k$, which can be nested in any order with the same result:

- In `ijk` order, the inner loop walks along a row of $A$ but down a column of $B$, which is the bad stride.
- In `ikj` order, the inner loop walks along rows of $B$ and $C$, which is unit stride.
- **Tiling** (blocking) goes further. It splits the matrices into $t \times t$ tiles and finishes all the work on a set of tiles that fits in the cache before moving on, so every block brought in is reused about $t$ times.

![Two charts. Left: misses of three 32 by 32 matrix-multiply versions against cache size from 1 to 16 KB, 4-way with 32-byte blocks, on a log scale. ijk misses about 35,000 times at 1 and 2 KB, 6788 at 4 KB and 384 from 8 KB; ikj 4480 at 1 and 2 KB, 1495 at 4 KB, 463 at 8 KB and 384 at 16 KB; the tiled version 5072 at 1 KB, 1284 at 2 KB, 1089 at 4 KB, 610 at 8 KB and 386 at 16 KB. Right: stacked bars of the column traversal's misses for direct-mapped caches of 1 to 16 KB: 512 compulsory throughout, plus 3584 capacity misses at 1 KB, 3584 conflict misses at 2, 4 and 8 KB, and nothing more at 16 KB.](../../../assets/figures/14-09/caches.svg)

*Figure 1. Left: loop order and tiling matter most when the data do not fit. Once the cache holds a whole matrix (8 KB and up), every version approaches the 384 compulsory misses, and tiling can even cost a little. Right: the column traversal's extra misses change class with cache size: capacity at 1 KB, conflict from 2 to 8 KB, none at 16 KB.*

Example 14-09.6 shows the resulting gap: a factor of 27 in misses between `ijk` and tiled code, on the same cache. Tiling is the central idea of every high-performance linear-algebra library and of the data reuse in AI accelerators (14-14).

### 3.8 Hardware: multilevel caches, prefetching and memory-level parallelism

**Multilevel caches.** A small, fast L1 (split into instruction and data caches so that fetch and loads do not compete) keeps the hit time short. A larger L2 behind it catches most L1 misses, and a large shared L3 catches most of the rest before DRAM. Designs differ in whether a block in L1 must also be in L2 (**inclusive**), may not be (**exclusive**), or neither.

**Prefetching** fetches blocks before they are requested.

- The simplest form, **next-line** prefetching, fetches block $b + 1$ whenever block $b$ is missed or first used. On a sequential stream it removes nearly all misses in the lab's model, where a prefetched block arrives instantly (Problem 14-09.10).
- **Stride** prefetchers learn the distance between successive addresses of the same load instruction, and follow strided patterns.
- A prefetcher is judged by **coverage** (the fraction of misses it removes), **accuracy** (the fraction of prefetches used) and **timeliness**. A wrong prefetch wastes bandwidth and evicts useful data. The lab's model cannot measure timeliness: its prefetches have no latency, so they are never late. A real next-line prefetcher one block ahead of a tight loop often is late, which is why real prefetchers run several blocks ahead (the prefetch distance).
- No simple prefetcher helps true pointer chasing, because the next address is unknown until the current load returns. (The lab's linked list places its nodes at a constant 64-byte stride, which a stride prefetcher would follow; a real heap scatters them.)

**Non-blocking caches and memory-level parallelism (MLP).** An out-of-order core keeps executing after a miss, and may miss again. A **non-blocking** cache tracks each outstanding miss in a **miss status holding register (MSHR)** and continues to serve hits and further misses. By Little's law (14-08), the bandwidth a core can draw from memory is

$$
\text{bandwidth} = \frac{\text{outstanding misses} \times B}{\text{latency}} .
$$

With 64-byte blocks and 100 ns latency, 10 outstanding misses sustain only 6.4 GB/s (Problem 14-09.11). Streaming at hundreds of GB/s needs hundreds of misses in flight, from many cores, prefetchers and deep queues.

### 3.9 Main memory: DRAM and HBM

Main memory is DRAM. Each bit is stored as charge on a capacitor, so a DRAM cell is much smaller than an SRAM cell but slower and needs refresh. A DRAM chip is organized in banks of rows. An access opens a row into sense amplifiers, then reads a burst of columns from it. Latency has improved slowly for decades, while bandwidth has improved by widening and speeding up the interface.

**High Bandwidth Memory (HBM)** takes width to an extreme. A stack of DRAM dies, connected by through-silicon vias, sits beside the processor on a silicon interposer and connects through a 1024-bit interface (2048 bits in HBM4).

| Generation | Per-pin rate | Bandwidth per stack | Source |
|---|---|---|---|
| HBM3 (JEDEC JESD238, Jan 2022) | up to 6.4 Gb/s | 819 GB/s | [2, R-214] |
| HBM3E (vendor parts) | above 9.2 Gb/s | above 1.2 TB/s | [3, 4, R-214] |
| HBM4 (JEDEC JESD270-4, Apr 2025) | up to 8 Gb/s × 2048 bits | up to 2 TB/s | [2, R-214] |

The bandwidth per stack is the pin rate times the width: $6.4 \text{ Gb/s} \times 1024 / 8 = 819.2$ GB/s. AI accelerators use several stacks per package for multiple TB/s. The memory hierarchy beyond caches, including DRAM interfaces and HBM's packaging, cost and supply, is the subject of Course 23 ([23-01](../../23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md), [23-05](../../23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md)).

### 3.10 The lab's cache model

The lab's `cache.py` is a **trace-driven** cache simulator:

- `mem_trace()` compiles a C kernel with clang, runs it on the course's RV32IM simulator, and records every load and store address (14-08's `mtrace`).
- `Cache` replays the trace through one cache level: any size, block size and associativity; LRU, FIFO or random replacement; write-back or write-through; write-allocate or not; optional next-line prefetching; an optional next level.
- `three_c()` classifies misses as in §3.4.

The verify script checks every LRU configuration against an independent simulator, and the fully associative results against Mattson's **stack-distance** algorithm. That algorithm computes, for each access, how many distinct blocks were touched since the last access to the same block. A fully associative LRU cache of $L$ lines misses exactly when that distance is $L$ or more.

## 4. Worked examples

All simulations use the lab's model on data-access traces of the C kernels in the lab, compiled with clang at `-O2` for RV32IM. Integers are 4 bytes.

### Example 14-09.1 · Splitting an address (tier A)

**Setup.** A 32 KB, 8-way set-associative cache has 64-byte blocks, and addresses are 32 bits. (a) Find the number of sets and the widths of the offset, index and tag fields. (b) Split the address 0x1234_5678. (c) Each line stores its tag, a valid bit and a dirty bit. What is the storage overhead?

**Solution.**

(a) $S = 32768 / (64 \times 8)$ = **64** sets. The offset has $\log_2 64$ = **6** bits, the index $\log_2 64$ = **6** bits, and the tag $32 - 6 - 6$ = **20** bits.

(b) The offset is the low 6 bits: 0x78 & 0x3F = 0x38 = **56**. The index is the next 6 bits: (0x12345678 >> 6) & 0x3F = 0x19 = **25**. The tag is the top 20 bits: 0x12345678 >> 12 = **0x12345**.

(c) There are $32768 / 64 = 512$ lines, each with $20 + 1 + 1 = 22$ bits of overhead: **11264** bits, or 1.375 KiB. As a fraction of the 262,144 data bits, the overhead is **4.3**%.

**Units check.** Bits of address: $20 + 6 + 6 = 32$.

**Sanity check.** Doubling the associativity at the same size halves the sets, so one index bit moves into the tag: more comparators *and* wider tags.

### Example 14-09.2 · Tracing three caches by hand (tier A)

**Setup.** A tiny cache holds 4 blocks of 16 bytes. It accesses the byte addresses 0x000, 0x040, 0x004, 0x080, 0x044, 0x008, 0x010, 0x050, 0x014. Count the misses if the cache is (a) direct-mapped, (b) 2-way set-associative with LRU, (c) fully associative with LRU. Classify the direct-mapped cache's misses.

**Solution.** Dividing by 16 gives the block numbers 0, 4, 0, 8, 4, 0, 1, 5, 1.

(a) **Direct-mapped, 4 sets** (set = block mod 4). Blocks 0, 4 and 8 all map to set 0, and 1 and 5 to set 1. Each access evicts the previous occupant of its set, and no block is found again before being replaced:

| Block | 0 | 4 | 0 | 8 | 4 | 0 | 1 | 5 | 1 |
|---|---|---|---|---|---|---|---|---|---|
| Set 0 after | 0 | 4 | 0 | 8 | 4 | 0 | 0 | 0 | 0 |
| Set 1 after | – | – | – | – | – | – | 1 | 5 | 1 |
| Result | M | M | M | M | M | M | M | M | M |

That is **9** misses.

(b) **2-way, 2 sets** (set = block mod 2). Blocks 0, 4 and 8 share set 0, with LRU order listed oldest first:

| Block | 0 | 4 | 0 | 8 | 4 | 0 | 1 | 5 | 1 |
|---|---|---|---|---|---|---|---|---|---|
| Set 0 after | 0 | 0 4 | 4 0 | 0 8 | 8 4 | 4 0 | 4 0 | 4 0 | 4 0 |
| Set 1 after | – | – | – | – | – | – | 1 | 1 5 | 5 1 |
| Result | M | M | H | M | M | M | M | M | H |

That is **7** misses.

(c) **Fully associative LRU.** Only five distinct blocks occur and the cache holds four. The fifth (block 5) evicts block 8, which is never used again. Only the first access to each block misses: **5** misses.

The direct-mapped cache has 5 compulsory misses, no capacity misses (the fully associative cache has only the 5 compulsory ones) and **4** conflict misses.

**Units check.** Counts of accesses.

**Sanity check.** More associativity removes conflict misses step by step: 9, then 7, then 5.

### Example 14-09.3 · AMAT and CPI with two levels (tier B)

**Setup.** L1 hits in 4 cycles and misses on 5% of accesses. L2 hits in 14 cycles and misses on 20% of the accesses that reach it. Memory takes 200 cycles. (a) Find the AMAT, the global L2 miss rate, and the AMAT without the L2. (b) An in-order core with a base CPI of 1 makes 0.35 data accesses per instruction and stalls for every miss. Find its CPI with and without the L2, and the L1 MPKI.

**Solution.**

(a) $\text{AMAT} = 4 + 0.05\,(14 + 0.2 \times 200) = 4 + 0.05 \times 54$ = **6.7** cycles. The global L2 miss rate is $0.05 \times 0.2$ = **1**%. Without L2, $\text{AMAT} = 4 + 0.05 \times 200$ = **14** cycles.

(b) The miss penalty seen by L1 is $14 + 0.2 \times 200 = 54$ cycles, so $\text{CPI} = 1 + 0.35 \times 0.05 \times 54$ = **1.945**. Without L2, $\text{CPI} = 1 + 0.35 \times 0.05 \times 200$ = **4.5**. The L1 MPKI is $1000 \times 0.35 \times 0.05$ = **17.5**.

**Units check.** Accesses/instruction × misses/access × cycles/miss = cycles/instruction.

**Sanity check.** The L2's local miss rate of 20% looks poor, but it removes 80% of the trips to memory, which more than halves the CPI.

### Example 14-09.4 · Rows against columns (tier B)

**Setup.** A function sums a 64 × 64 matrix of integers (16 KB) either by rows or by columns. The cache is 4 KB, direct-mapped, with 32-byte blocks. Find the misses and miss rates of each traversal, classify the column traversal's misses, and find what 4-way associativity, full associativity, and a 16 KB direct-mapped cache would do. What if the cache were only 1 KB, fully associative?

**Solution.** Each traversal makes 4096 loads (the simulator confirms this; the loop variables stay in registers).

- **By rows:** each 32-byte block holds 8 consecutive integers, so each block misses once: **512** misses, a miss rate of 1/8 = **12.5**%. All of them are compulsory.
- **By columns:** consecutive accesses are 256 bytes apart, 8 blocks. The cache has 128 sets, so a column's 64 blocks land in only 128/8 = 16 sets, 4 blocks per set. Each block is evicted before the next column, 4 bytes along, can reuse it. Every access misses: **4096**, a miss rate of **100**%.

The column traversal's 4096 misses are 512 compulsory, no capacity, and **3584** conflict, since a fully associative 4 KB cache would hold one column's 64 blocks and miss only **512** times.

- A 4-way cache of the same size still misses **4096** times. Its 32 sets receive the column in 4 sets of 4 ways, 16 lines for 64 blocks.
- A 16 KB direct-mapped cache (512 sets) spreads the column over 64 sets and misses only 512 times.
- A 1 KB fully associative cache holds 32 lines, fewer than a column's 64 blocks. Cycling through 64 blocks with LRU, it misses on every access: **4096**, of which 512 are compulsory and the other **3584** now capacity misses.

**Units check.** Misses are counts; miss rates are misses per access.

**Sanity check.** The fix is to change the code (sum by rows), not the cache: no realistic associativity rescues a power-of-two stride.

### Example 14-09.5 · Write-back against write-through (tier B)

**Setup.** A histogram loop reads 1000 bytes `x[i]` and increments `h[x[i] & 15]`, an array of 16 integers (64 bytes). The cache is 1 KB, 2-way, with 32-byte blocks. Compare the traffic to memory for write-back with write-allocate and write-through with no-write-allocate.

**Solution.** The trace has 3000 accesses: 1000 byte loads of `x`, 1000 loads and 1000 stores of `h`. Both caches miss **34** times: the 32 blocks of `x` (1000 bytes span 32 blocks) and the 2 blocks of `h`, which are first read and so are allocated even without write-allocate. Reads from memory are $34 \times 32$ = **1088** bytes in both cases. Writes differ:

- **Write-back:** the two blocks of `h` stay dirty in the cache and are written once, at the end: $2 \times 32$ = **64** bytes.
- **Write-through:** all 1000 stores go to memory: $1000 \times 4$ = **4000** bytes.

**Units check.** Bytes = blocks × bytes per block, or stores × bytes per store.

**Sanity check.** Write-through costs $4000 / 64 = 62.5$ times the write traffic here, because the same 64 bytes are written over and over. A write buffer hides the latency of those writes, but not their bandwidth or energy.

### Example 14-09.6 · Matrix multiply: loop order and tiling (tier C)

**Setup.** Three versions multiply two 32 × 32 integer matrices (4 KB each): the `ijk` order, the `ikj` order, and an `ikj` version tiled into 8 × 8 tiles. The cache is 2 KB, 4-way, with 32-byte blocks. Compare the misses. Then estimate each version's run time on an in-order core with CPI 1 that stalls 100 cycles per miss.

**Solution.** The simulations give:

| Version | Instructions | Accesses | Misses | Miss rate | Cycles ≈ instructions + 100 × misses |
|---|---|---|---|---|---|
| `ijk` | 272,644 | 66,560 | **34,952** | 52.51% | **3,767,844** |
| `ikj` | 307,467 | 100,352 | **4,480** | 4.46% | **755,467** |
| tiled, $t$ = 8 | 340,165 | 103,444 | **1,284** | 1.24% | **468,565** |

- `ijk` walks down columns of $B$ with a stride of 128 bytes. With 16 sets, a column's 32 blocks fall into 4 sets (16 lines), so they never survive from one $j$ to the next.
- `ikj` walks along rows. Its misses are mostly capacity misses: all of $B$ (4 KB) is reused for each row of $C$ but does not fit.
- Tiling reuses each $8 \times 8$ tile of $B$ (256 bytes) for all 32 rows before moving on.

Tiled code is **8.04** times faster than `ijk`, although it executes 25% more instructions.

**Units check.** Cycles = instructions × 1 + misses × 100 cycles.

**Sanity check.** All three versions have at least the 384 compulsory misses of three 4 KB matrices in 32-byte blocks. The tiled version is within a factor of 3.3 of that floor.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-09.1a | sets | 64 | — |
| Ex 14-09.1b | offset bits | 6 | bits |
| Ex 14-09.1c | index bits | 6 | bits |
| Ex 14-09.1d | tag bits | 20 | bits |
| Ex 14-09.1e | offset of 0x12345678 | 56 | — |
| Ex 14-09.1f | index of 0x12345678 | 25 | — |
| Ex 14-09.1g | tag of 0x12345678 | 0x12345 | — |
| Ex 14-09.1h | tag and state storage | 11264 | bits |
| Ex 14-09.1i | storage overhead | 4.3 | % |
| Ex 14-09.2a | misses, direct-mapped | 9 | — |
| Ex 14-09.2b | misses, 2-way LRU | 7 | — |
| Ex 14-09.2c | misses, fully associative LRU | 5 | — |
| Ex 14-09.2d | conflict misses, direct-mapped | 4 | — |
| Ex 14-09.3a | AMAT | 6.7 | cycles |
| Ex 14-09.3b | global L2 miss rate | 1 | % |
| Ex 14-09.3c | AMAT without L2 | 14 | cycles |
| Ex 14-09.3d | CPI with L2 | 1.945 | — |
| Ex 14-09.3e | CPI without L2 | 4.5 | — |
| Ex 14-09.3f | L1 MPKI | 17.5 | — |
| Ex 14-09.4a | misses, rows | 512 | — |
| Ex 14-09.4b | miss rate, rows | 12.5 | % |
| Ex 14-09.4c | misses, columns | 4096 | — |
| Ex 14-09.4d | miss rate, columns | 100 | % |
| Ex 14-09.4e | conflict misses, columns | 3584 | — |
| Ex 14-09.4f | misses, columns, fully associative 4 KB | 512 | — |
| Ex 14-09.4g | misses, columns, 4-way 4 KB | 4096 | — |
| Ex 14-09.4h | misses, columns, fully associative 1 KB | 4096 | — |
| Ex 14-09.4i | capacity misses, fully associative 1 KB | 3584 | — |
| Ex 14-09.5a | misses | 34 | — |
| Ex 14-09.5b | bytes read from memory | 1088 | B |
| Ex 14-09.5c | bytes written, write-back | 64 | B |
| Ex 14-09.5d | bytes written, write-through | 4000 | B |
| Ex 14-09.6a | misses, ijk | 34952 | — |
| Ex 14-09.6b | misses, ikj | 4480 | — |
| Ex 14-09.6c | misses, tiled | 1284 | — |
| Ex 14-09.6d | cycles, ijk | 3767844 | — |
| Ex 14-09.6e | cycles, ikj | 755467 | — |
| Ex 14-09.6f | cycles, tiled | 468565 | — |
| Ex 14-09.6g | speedup, tiled over ijk | 8.04 | — |

## 5. Simulate it

The lab, [labs/14-09-lab](../labs/14-09-lab/README.md), provides `cache.py`, the trace-driven simulator of §3.10. In the notebook you:

1. **Check Examples 14-09.1 and 14-09.2** with the simulator's address split and a nine-access trace.
2. **Classify misses** for row and column traversals over a sweep of sizes and associativities.
3. **Tune a matrix multiply:** loop orders, tile sizes, cache sizes, block sizes and replacement policies.
4. **Count traffic** for write policies on the histogram and copy loops.
5. **Turn on prefetching** for rows, columns and a linked list.
6. **Feed the misses into 14-08's out-of-order model** to see which misses an out-of-order core can hide.

**Guided exercise (predict, then run).** **Before Part 5,** predict how many misses a next-line prefetcher leaves in the row traversal and in the column traversal of Example 14-09.4. (Rows: 1, the first block, since every later block is prefetched one block ahead. Columns: still 4096, and every prefetch is wasted, because the next block in memory is not the next one used.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Cache size | Capacity and conflict misses | Hit time, area, leakage and access energy | CPU architect, SoC architect |
| Associativity | Conflict misses | Hit time (wider compare and select), energy per access | CPU architect |
| Block size | Compulsory misses, tag overhead | Miss penalty, traffic for unused bytes, more conflict misses | CPU and memory-system architects |
| Levels of cache | Average latency at low area per level | Latency of each miss path, coherence complexity (14-12) | SoC architect |
| Write-back against write-through | Memory traffic and energy | Dirty state; slower eviction; coherence complexity | CPU architect |
| Prefetcher aggressiveness | Hides latency on regular streams | Bandwidth and pollution when wrong | CPU architect, tuned per product |
| MSHRs (outstanding misses) | Memory-level parallelism, bandwidth | Area, queue complexity | CPU architect |
| Loop order and tiling | Misses, by large factors | Code complexity; tuning per cache | Software and library engineers |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Energy per 64-bit read, 45 nm | 10 pJ (8 KB), 20 pJ (32 KB), 100 pJ (1 MB) cache; 1.3–2.6 nJ DRAM | Horowitz [1, R-208] |
| AMAT | $t_\text{hit} + m \, t_\text{penalty}$, nested for each level | §3.3 |
| Sets | $S = C/(B \cdot A)$ | §3.2 |
| Bandwidth from MLP | outstanding misses × $B$ / latency | Little's law |
| HBM3 / HBM3E / HBM4 per stack | 819 GB/s / above 1.2 TB/s / up to 2 TB/s | [2–4, R-214] |
| Zen 5 caches | L1 data 48 KB 12-way; L2 1 MB 16-way; L3 32 MB per 8-core complex | AMD, Hot Chips 2024 [5, R-212] |
| DRAM load latency | of order 100 ns: the round figure this chapter's examples use, not a sourced measurement | Illustrative; measure the target system (lab extension) |

## 8. Common mistakes

- **Confusing local and global miss rates.** L2's local miss rate can be 50% while its global rate is 1%.
- **Adding hit time to the penalty twice.** In $t_\text{hit} + m \, t_\text{penalty}$ the penalty is the *extra* time of a miss.
- **Expecting associativity to fix a bad stride.** A power-of-two stride crowds a few sets; changing the code fixes it, more ways rarely do.
- **Ignoring writes.** Write-through with many stores, or write-allocate with streaming stores, can double the memory traffic.
- **Reading AMAT as run time on an out-of-order core.** Overlapped misses cost less than AMAT suggests, and dependent misses cost the full latency each.
- **Trusting peak bandwidth.** Delivered bandwidth needs enough misses in flight (Little's law), and real access patterns lose some to row switches and refresh.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Deep, large hierarchies.** AMD's Zen 5 core has a 48 KB 12-way L1 data cache serving 4 memory operations per cycle and a 1 MB 16-way L2 in each core, and each 8-core complex shares 32 MB of L3 [5, R-212] **[Established]** (vendor disclosure).
- **HBM for AI.** HBM3 (JEDEC JESD238, January 2022) runs up to 6.4 Gb/s per pin for 819 GB/s per stack [2, R-214]. Vendor HBM3E parts exceed 9.2 Gb/s and 1.2 TB/s per stack, in 24 GB 8-high and 36 GB 12-high stacks [3, 4, R-214]. HBM4 (JESD270-4, April 2025) doubles the interface to 2048 bits for up to 2 TB/s per stack and up to 64 GB [2, R-214] **[Established]**. (The JEDEC figures were read from verbatim reprints of JEDEC's releases; see R-214.)
- **Energy is the binding constraint.** A DRAM access costs about 100 times a 32 KB cache read [1, R-208] **[Established]**, so accelerators are designed around on-chip reuse (14-14) and AI workloads are often memory-bound ([23-01](../../23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md)).

### Why it matters commercially

- **Cache is silicon area, and area is cost.** Large L3 caches occupy a large share of a server processor's die. Stacking extra cache dies on top of a processor is one way vendors add capacity without enlarging the base die.
- **HBM is a supply-chain story.** HBM sets the memory bandwidth, and much of the bill of materials, of AI accelerators. Its stacking, packaging and yield are covered in [23-05](../../23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md).

### Marketing vs Reality

- **"Huge cache."** *Reality:* a larger cache helps only workloads whose working set fits in the new size but not the old one, and it raises hit latency. *Sanity check:* ask for the miss-rate or performance curve against cache size on your workload.
- **"X TB/s of memory bandwidth."** *Reality:* that is the pin rate times the width, a peak. Delivered bandwidth depends on access pattern, on enough outstanding requests, and on refresh and row overheads. *Sanity check:* ask for measured bandwidth on a streaming benchmark and on your access pattern.
- **"Up to N× faster with our new memory."** *Reality:* only memory-bound phases gain; compute-bound phases do not. *Sanity check:* ask what fraction of time the workload is memory-bound (a roofline, 14-15).

### Questions for engineering leaders

1. **"What is your workload's working set, and where does it sit in the hierarchy?"**
   *Strong:* miss rates or MPKI per level from counters, and the working-set curve. *Evasive:* "it fits in cache".
2. **"How much of your bandwidth is used, and what limits it?"**
   *Strong:* achieved against peak bandwidth, outstanding requests per core, and the effect of prefetchers. *Evasive:* the peak figure.
3. **"What did the last cache-size increase buy, and what did it cost in latency and area?"**
   *Strong:* specific performance per area, with the latency change. *Evasive:* "more is better".
4. **"How does the software stack exploit locality?"**
   *Strong:* tiled kernels, data-layout choices, prefetch hints, measured. *Evasive:* "the compiler handles it".

## 10. Concept check

**Q1.** Why does a cache move whole blocks rather than single words?

<details><summary>Answer</summary>

To exploit spatial locality: the neighbours of an accessed word are likely to be needed soon, and fetching them with it costs little extra time, because DRAM and buses deliver bursts efficiently. It also amortizes one tag over many bytes.

</details>

**Q2.** What distinguishes a conflict miss from a capacity miss?

<details><summary>Answer</summary>

A conflict miss would not occur in a fully associative cache of the same size: it comes from too many active blocks mapping to one set. A capacity miss occurs even in the fully associative cache, because the working set is larger than the cache.

</details>

**Q3.** Why is L2's local miss rate often high, and why does that not mean L2 is useless?

<details><summary>Answer</summary>

L2 sees only the accesses that missed in L1, which are the hard ones with poor locality, so a large fraction of them also miss. What matters is the global miss rate and the time saved: every L2 hit replaces a trip to memory.

</details>

**Q4.** When is write-through with no-write-allocate better than write-back with write-allocate?

<details><summary>Answer</summary>

For streaming stores that overwrite data without reading it: write-allocate would first fetch each block only to overwrite it, doubling the traffic. Write-back wins when the same blocks are written repeatedly.

</details>

**Q5.** Why does tiling reduce misses in matrix multiplication?

<details><summary>Answer</summary>

It reorders the computation so that a working set of tiles small enough to fit in the cache is reused many times before eviction, turning capacity misses into hits.

</details>

**Q6.** Why can an out-of-order core hide array misses but not linked-list misses?

<details><summary>Answer</summary>

The array's addresses are known in advance, so the core (or a prefetcher) can issue several misses at once and overlap them. Each list address comes from the previous load, so the misses are serialized and each costs the full latency.

</details>

**Q7.** How many misses must be in flight to stream 64-byte blocks at 64 GB/s with 100 ns latency?

<details><summary>Answer</summary>

By Little's law, $64 \times 10^9 \times 100 \times 10^{-9} / 64 = 100$ outstanding misses.

</details>

Now work the [problem set](../problems/14-09-problems.md).

## 11. Key terms

[Locality](../../../reference/glossary.md#locality) · [Cache block](../../../reference/glossary.md#cache-block) · [Set-associative cache](../../../reference/glossary.md#set-associative-cache) · [Direct-mapped cache](../../../reference/glossary.md#direct-mapped-cache) · [Fully associative cache](../../../reference/glossary.md#fully-associative-cache) · [Tag (cache)](../../../reference/glossary.md#tag-cache) · [Average memory access time (AMAT)](../../../reference/glossary.md#average-memory-access-time-amat) · [Miss rate](../../../reference/glossary.md#miss-rate) · [Three Cs (compulsory, capacity, conflict)](../../../reference/glossary.md#three-cs-compulsory-capacity-conflict) · [Least recently used (LRU)](../../../reference/glossary.md#least-recently-used-lru) · [Write-back](../../../reference/glossary.md#write-back) · [Write-through](../../../reference/glossary.md#write-through) · [Write-allocate](../../../reference/glossary.md#write-allocate) · [Prefetching](../../../reference/glossary.md#prefetching) · [Memory-level parallelism (MLP)](../../../reference/glossary.md#memory-level-parallelism-mlp) · [Loop tiling](../../../reference/glossary.md#loop-tiling) · [High Bandwidth Memory (HBM)](../../../reference/glossary.md#high-bandwidth-memory-hbm)

## 12. Connections

- **Builds on:** memory arrays ([08-11](../../08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md)); arrays and pointers in C ([05-06](../../05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md)); out-of-order execution and Little's law ([14-08](14-08-out-of-order-and-superscalar.md)).
- **Next:** [14-10 Virtual Memory, TLBs and the OS Interface](14-10-virtual-memory.md), which adds address translation in front of the caches.
- **Used later:** coherence between private caches ([14-12](14-12-multicore-coherence-consistency.md)); GPU memory coalescing ([14-13](14-13-gpus-and-simt.md)); on-chip SRAM and HBM in accelerators ([14-14](14-14-ai-accelerators.md)); arithmetic intensity and the roofline ([14-15](14-15-roofline-and-benchmarks.md)); SRAM circuits ([19-08](../../19-digital-vlsi-design/chapters/19-08-sram-design.md)); DRAM and HBM in depth ([23-01](../../23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md), [23-03](../../23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md), [23-05](../../23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md)).

## 13. Further study

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 5 (large and fast: exploiting memory hierarchy).
- J. L. Hennessy and D. A. Patterson, *Computer Architecture: A Quantitative Approach*, App. B (review of memory hierarchy) and ch. 2 (memory hierarchy design).
- R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, "Evaluation Techniques for Storage Hierarchies," *IBM Systems Journal* 9(2), 1970 (stack distances).
- M. D. Hill, "Aspects of Cache Memory and Instruction Buffer Performance," PhD thesis, UC Berkeley, 1987 (the three Cs).
- U. Drepper, "What Every Programmer Should Know About Memory," 2007 (a long practical tour; some numbers are dated).

## 14. Sources

1. M. Horowitz, "Computing's Energy Problem (and What We Can Do About It)," ISSCC 2014. [R-208](../../../reference/research-log.md#r-208--energy-per-operation-at-45-nm-horowitz-isscc-2014)
2. JEDEC, releases for JESD238 HBM3 (Jan 2022) and JESD270-4 HBM4 (Apr 2025), read as reprints. [R-214](../../../reference/research-log.md#r-214--hbm3-hbm3e-and-hbm4-bandwidth-and-capacity)
3. Micron, HBM3E product page. [R-214](../../../reference/research-log.md#r-214--hbm3-hbm3e-and-hbm4-bandwidth-and-capacity)
4. Samsung Semiconductor, HBM3E and HBM3 product pages. [R-214](../../../reference/research-log.md#r-214--hbm3-hbm3e-and-hbm4-bandwidth-and-capacity)
5. AMD, "Next Generation 'Zen 5' Core," Hot Chips 2024. [R-212](../../../reference/research-log.md#r-212--amd-zen-5-core-hot-chips-2024)

Locality, cache organization, AMAT, the three Cs, replacement, write policies and tiling are textbook material (Further study). Every miss count in the examples comes from the lab's simulator and is re-run, and cross-checked by independent simulators, in the verify script.
