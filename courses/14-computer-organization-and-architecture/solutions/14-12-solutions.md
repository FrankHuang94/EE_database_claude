# Solutions 14-12 · Multicore, Coherence and Memory Consistency

Problems: [14-12 problems](../problems/14-12-problems.md) · Chapter: [14-12](../chapters/14-12-multicore-coherence-consistency.md). Every number below is recomputed by [verify_14_12.py](../verify/verify_14_12.py).

- Coherence counts come from the lab's simulator, which checks the coherence invariants after every operation, and from closed forms derived here.
- Sequentially consistent litmus outcomes are re-derived by brute force over all interleavings.

---

## Solutions

### Solution 14-12.1

| Step | Operation | Bus | P0 | P1 | P2 |
|---|---|---|---|---|---|
| 1 | P0 read | BusRd | E | I | I |
| 2 | P1 read | BusRd | S | S | I |
| 3 | P2 read | BusRd | S | S | S |
| 4 | P0 write | BusUpgr | M | I | I |
| 5 | P1 write | BusRdX | I | M | I |
| 6 | P2 read | BusRd | I | S | S |

That is **6** bus transactions, **3** invalidations (two at step 4, one at step 5) and **2** write-backs (P0 at step 5, P1 at step 6).

### Solution 14-12.2

Each 1024-bit block needs $32 + 2 = 34$ bits: **3.32**% overhead. Larger blocks and fewer cores make full bit vectors cheap.

### Solution 14-12.3

Choosing which positions in the global order belong to each thread gives the interleavings:

- (a) $\binom{4}{2}$ = **6**;
- (b) $\binom{6}{3}$ = **20**;
- (c) $6!/(2!\,2!\,2!)$ = **90**.

The count grows exponentially with program length, which is why litmus tests are kept tiny and exhaustive tools prune repeated states.

### Solution 14-12.4

- **MSI:** BusRd (A in S), BusUpgr (A in M), BusRd (P1 reads A; P0 writes it back, both in S), BusRd (B in S), BusUpgr (B in M): **5** transactions.
- **MESI:** BusRd (A in E), a silent upgrade, BusRd (P1), BusRd (B in E), a silent upgrade: **3**.

### Solution 14-12.5

With $n$ threads, each round of $n$ loads and $n$ stores costs:

- $n - 1$ BusRd, because the last writer's copy is still valid for itself;
- one BusUpgr for the first store, which invalidates the $n - 1$ readers;
- $n - 1$ BusRdX for the other stores, each invalidating the previous writer.

That is $2n - 1$ transactions and $2n - 2$ invalidations per round, plus one initial miss.

- **4 threads:** **7001** transactions and **6000** invalidations packed, against **4** padded (one miss per core).
- **8 threads:** **15,001** packed against **8** padded.

The traffic grows linearly with the threads, while the useful work per thread stays the same.

### Solution 14-12.6

Each core moves $2 \times 10^9 \times 10/1000 \times 64$ = **1.28** GB/s. The bus supports $51.2 / 1.28$ = **40** cores before saturating, and in practice fewer, because queueing delay grows steeply near saturation. This is one reason large chips use directories and meshes.

### Solution 14-12.7

SC allows **3** outcomes and TSO **4**. Under TSO, each thread's load of its own variable reads its buffered store (r1 = r3 = 1) while the other variable's store is still buffered in the other core (r2 = r4 = 0), so $(1, 0, 1, 0)$ is allowed. Under SC it is not: whichever store comes first in the global order is seen by the other thread's later load. Store-to-load forwarding is exactly what TSO's "read your own newest buffered write" rule describes.

### Solution 14-12.8

SC allows **3** outcomes, TSO **3** and PSO **4**. Only PSO allows $(1, 0)$: its store buffer may make `flag` visible before `data`. TSO keeps stores in order, so a reader that sees the flag also sees the data.

Put the fence between the two stores in thread 0 (`fence w,w` on RISC-V). On weakly ordered machines the reader also needs ordering between its two loads (`fence r,r`, or acquire semantics on the flag load), because RVWMO and Arm may reorder loads too. The PSO model here reorders only stores.

### Solution 14-12.9

```text
inc:  lr.w   t0, (a0)        # load-reserved
      addi   t0, t0, 1
      sc.w   t1, t0, (a0)    # t1 = 0 on success
      bnez   t1, inc         # retry if the reservation was lost
```

The single AMO is `amoadd.w zero, t2, (a0)` with t2 = 1 (or `amoadd.w t3, t2, (a0)` to also get the old value).

The SC fails if another core wrote the reserved block between the LR and the SC (its coherence request invalidated the reservation), or for implementation reasons such as an interrupt. For *constrained* LR/SC loops the specification guarantees livelock freedom, not success for every hart: if harts sit in such loops and nothing else writes the reservation set, at least one of them eventually exits its loop (or the loop is left by a branch or a trap). A constrained loop has at most 16 instructions, with only simple integer instructions (no loads, stores or backward jumps) between the LR and the SC ([R-218](../../../reference/research-log.md#r-218--risc-v-rvwmo-ztso-and-atomics)). Under heavy contention, AMOs, which complete at the cache or even nearer the data, avoid the retries altogether.

### Solution 14-12.10

| Cores | Test-and-set | Test-and-test-and-set |
|---|---|---|
| 2 | **4** | **5** |
| 8 | **709** | **23** |

With one waiter, test-and-set wins narrowly. The waiter's first swap takes the block in M, and every later spin hits in its own cache: no other spinner exists to steal it. Test-and-test-and-set pays one extra read after the release.

With 7 waiters, test-and-set's swaps steal the block from one another on every spin, 700 transactions. Test-and-test-and-set's waiters spin quietly in S until the release.

### Solution 14-12.11

$S(N)$ peaks where $0.95/N^2 = 0.005$, at $N = \sqrt{190} \approx 13.8$. The best integer is **14** cores, for a speedup of **5.469**. Beyond that, the communication overhead grows faster than the parallel work shrinks, and adding cores slows the program down. Coherence-heavy programs have such an optimum well below the core count of a modern server.

### Solution 14-12.12

It is the store-buffering (SB) test. Each thread's "set my flag" is the store and its "read the other's flag" the load. Under TSO both stores can sit in store buffers while both loads read 0 from memory, so both threads enter the critical section. One fence per thread between its store and its load, **2** in all, restores mutual exclusion: the fenced SB test allows only the three SC outcomes, none of them (0, 0). In practice one uses atomic instructions or locks, which include the necessary ordering.

### Solution 14-12.13

<!-- directory trace -->

| Access | Messages | Directory afterwards |
|---|---|---|
| core 3 reads X | 2 (request, data) | S {3} |
| core 7 reads X | 2 (request, data) | S {3, 7} |
| core 12 writes X | 6 (request, data, 2 invalidations, 2 acknowledgements) | M {12} |
| core 3 reads X | 4 (request, forward, data to core 3, copy to home) | S {3, 12} |

(a) **14** messages in all. The write sends one invalidation per sharer, and its acknowledgements go straight to core 12. That is why the home includes the number of acknowledgements to expect with the data.

(b) The write completes when the last acknowledgement arrives: requester → home → sharer → requester, **3** traversals (the data from the home travels in parallel). The last read is also **3**: requester → home → owner → requester. A snooping bus does either in one broadcast, which is the latency a directory pays for scalability.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-12.1a | bus transactions | 6 | — |
| 14-12.1b | invalidations | 3 | — |
| 14-12.1c | write-backs | 2 | — |
| 14-12.2a | directory overhead | 3.32 | % |
| 14-12.3a | interleavings, 2 + 2 | 6 | — |
| 14-12.3b | interleavings, 3 + 3 | 20 | — |
| 14-12.3c | interleavings, 2 + 2 + 2 | 90 | — |
| 14-12.4a | bus transactions, MSI | 5 | — |
| 14-12.4b | bus transactions, MESI | 3 | — |
| 14-12.5a | transactions, 4 threads packed | 7001 | — |
| 14-12.5b | invalidations, 4 threads packed | 6000 | — |
| 14-12.5c | transactions, 4 threads padded | 4 | — |
| 14-12.5d | transactions, 8 threads packed | 15001 | — |
| 14-12.5e | transactions, 8 threads padded | 8 | — |
| 14-12.6a | traffic per core | 1.28 | GB/s |
| 14-12.6b | cores supported | 40 | — |
| 14-12.7a | outcomes, SC | 3 | — |
| 14-12.7b | outcomes, TSO | 4 | — |
| 14-12.8a | outcomes, SC | 3 | — |
| 14-12.8b | outcomes, TSO | 3 | — |
| 14-12.8c | outcomes, PSO | 4 | — |
| 14-12.10a | test-and-set, 2 cores | 4 | — |
| 14-12.10b | test-and-test-and-set, 2 cores | 5 | — |
| 14-12.10c | test-and-set, 8 cores | 709 | — |
| 14-12.10d | test-and-test-and-set, 8 cores | 23 | — |
| 14-12.11a | best core count | 14 | — |
| 14-12.11b | maximum speedup | 5.469 | — |
| 14-12.12a | fences needed | 2 | — |
| 14-12.13a | messages, first read | 2 | — |
| 14-12.13b | messages, second read | 2 | — |
| 14-12.13c | messages, write | 6 | — |
| 14-12.13d | messages, read of the modified block | 4 | — |
| 14-12.13e | total messages | 14 | — |
| 14-12.13f | traversals on the write's critical path | 3 | — |
| 14-12.13g | traversals on the last read's critical path | 3 | — |
