# Problems 14-12 · Multicore, Coherence and Memory Consistency

Chapter: [14-12](../chapters/14-12-multicore-coherence-consistency.md) · Worked solutions: [14-12 solutions](../solutions/14-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Snooping MSI or MESI as in the chapter's transition table, with 64-byte blocks and private caches large enough never to evict. A "bus transaction" is a BusRd, BusRdX or BusUpgr. Litmus-test variables start at 0. Interleaved workloads alternate one operation per core, as in the lab's `round_robin`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-12.1 [A]

**Three cores.** Under MESI, three cores perform: P0 reads X, P1 reads X, P2 reads X, P0 writes X, P1 writes X, P2 reads X. Give the bus request and the three states after each step, and count the bus transactions, invalidations and write-backs.

### Problem 14-12.2 [A]

**A small directory.** A full bit-vector directory serves 32 cores with 128-byte blocks and 2 state bits per entry. What is its overhead relative to the data?

### Problem 14-12.3 [A]

**Counting interleavings.** How many sequentially consistent interleavings are there of (a) two threads of 2 operations each, (b) two threads of 3 operations each, (c) three threads of 2 operations each?

### Problem 14-12.4 [B]

**MSI against MESI.** Count the bus transactions under MSI and MESI for: P0 reads A, P0 writes A, P1 reads A, P0 reads B, P0 writes B, where A and B are different blocks.

### Problem 14-12.5 [B]

**False sharing at scale.** Four threads each increment their own counter 1000 times, interleaved. Count the bus transactions and invalidations with the four counters packed in one block, and with each in its own block. Repeat for eight threads.

### Problem 14-12.6 [B]

**How many cores can a bus feed?** Each core executes $2 \times 10^9$ instructions per second with 10 misses per thousand instructions, each moving a 64-byte block. The snooping bus delivers 51.2 GB/s. How many cores can it support before saturating?

### Problem 14-12.7 [B]

**Store forwarding.** Thread 0 runs `x = 1; r1 = x; r2 = y`, and thread 1 runs `y = 1; r3 = y; r4 = x`. How many outcomes $(r1, r2, r3, r4)$ are allowed under SC and under TSO? Is $(1, 0, 1, 0)$ allowed under either?

### Problem 14-12.8 [B]

**Message passing.** Thread 0 writes `data = 42` then `flag = 1`; thread 1 reads `flag` into r1, then `data` into r2. How many outcomes does each of SC, TSO and PSO allow, and which allow $(r1, r2) = (1, 0)$? Where should a fence go?

### Problem 14-12.9 [B]

**An atomic increment.** Write a RISC-V LR/SC loop that atomically increments the word at the address in a0, and the single AMO instruction that does the same. Why can an LR/SC loop fail and retry, and what makes it eventually succeed?

### Problem 14-12.10 [C]

**Locks with more waiters.** Using the scenario of Example 14-12.6 (100 spins per waiter, then a release and one attempt each), count the bus transactions of test-and-set and test-and-test-and-set with 2 and with 8 cores. Why does test-and-set win with a single waiter?

### Problem 14-12.11 [C]

**Amdahl meets coherence.** A program is 95% parallel, and each additional core adds communication overhead equal to 0.5% of the single-core run time: $S(N) = 1 / \bigl(0.05 + 0.95/N + 0.005(N - 1)\bigr)$. Which core count maximizes the speedup, and what is the maximum?

### Problem 14-12.12 [C]

**Dekker's handshake.** In a two-thread mutual-exclusion protocol, each thread sets its own flag and then reads the other's, entering the critical section only if the other flag is 0. Which litmus test is this? Show that TSO lets both enter, and count the fences needed to prevent it.

---

## Objective coverage

| Learning objective (chapter 14-12) | Problems |
|---|---|
| 1. The coherence problem and its invariants | 1, 12 |
| 2. Tracing MSI and MESI | 1, 4 |
| 3. Directories and scaling | 2, 6, 11 |
| 4. True and false sharing | 5, 11 |
| 5. Litmus tests and fences | 3, 7, 8, 12 |
| 6. Atomics and locks | 9, 10 |
