# Lab 14-12 · Multicore, Coherence and Memory Consistency

Chapter: [14-12 Multicore, Coherence and Memory Consistency](../../chapters/14-12-multicore-coherence-consistency.md)

## Objective

Watch a snooping coherence protocol work, one bus transaction at a time, and measure what sharing costs: false sharing, contended locks, MSI against MESI. Then explore memory consistency exhaustively: enumerate every execution of small litmus tests under sequential consistency, TSO and a store-reordering model, and see exactly which outcomes each allows and which fences remove them.

## Background

The coherence invariants (§3.2), MSI and MESI (§3.3), directories (§3.4), false sharing (§3.5), consistency models and litmus tests (§3.6), and atomics and locks (§3.7).

## Tools

Python only.

## Files

- [mesi.py](mesi.py): `System(cores, protocol)` with `access(core, addr, write)`, statistics, and invariant checks after every operation. Workload generators: `round_robin`, `counters` (false sharing) and `spin_lock` (test-and-set against test-and-test-and-set).
- [litmus.py](litmus.py): `outcomes(test, model)` for models `"SC"`, `"TSO"` and `"PSO"`, and the tests `SB`, `SB_FENCED`, `MP` and `MP_FENCED`.
- [14-12-coherence-lab.ipynb](14-12-coherence-lab.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Tracing (Part 1).** Replay Example 14-12.1 under MSI and MESI and print each cache's state after every step.
2. **False sharing (Part 2).** Run `counters` for 2, 4 and 8 cores with strides of 4 and 64 bytes, and plot the bus transactions.
3. **Locks (Part 3).** Run `spin_lock` with test-and-set and test-and-test-and-set for 2 to 8 cores.
4. **Litmus tests (Part 4).** Enumerate SB and MP, with and without fences, under all three models. *Predict first:* does TSO allow MP's (1, 0)?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 14-12.1 | 6 bus transactions under both protocols |
| 2 | False sharing | $(2n - 1) \times 1000 + 1$ transactions packed ($n$ cores), $n$ padded; 14,000 invalidations packed at 8 cores |
| 3 | Locks | test-and-set grows by 100 transactions per waiter (709 at 8 cores); test-and-test-and-set by 3 (23) |
| 4 | Litmus | SB: SC 3 outcomes, TSO and PSO 4, with fences 3; MP: SC and TSO 3, PSO 4, PSO with a fence 3 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-12.a | invalidations, 8 cores, packed counters | 14000 | — |
| Lab 14-12.b | bus transactions, test-and-set, 8 cores | 709 | — |
| Lab 14-12.c | MP outcomes, PSO with a fence | 3 | — |
| Lab 14-12.d | SB outcomes, PSO | 4 | — |

*These are recomputed by [verify_14_12.py](../../verify/verify_14_12.py).*

## Discussion questions

1. The simulator's caches never evict. What would change with finite caches?
2. Why can't the litmus enumerator's PSO model produce the "load buffering" outcome, in which each thread's load reads the other thread's later store?
3. Why do real protocols add states such as O (Owned) or F (Forward) to MESI?

### Answers

1. Capacity and conflict misses would appear (14-09), and evictions of M blocks would add write-backs. An inclusive shared cache would also have to invalidate private copies when it evicts a block (back-invalidations). The coherence misses counted here would remain.
2. The model buffers only stores. Its loads always execute in program order and read the current memory or buffer state. Load buffering requires loads to be reordered after later stores, which RVWMO and Arm permit in principle but this simple machine cannot produce. A model checker built on the formal axiomatic model is needed for those cases.
3. In MESI, a block that is dirty in one cache and read by another must be written back to memory before both hold it in S. O lets the dirty owner keep supplying the data without writing it back. F designates one clean sharer to answer requests, so that several caches do not all respond. Both reduce memory traffic and latency, at the cost of more states to verify.

## Optional hardware extension

On a multicore Linux machine, write a C program in which two threads increment counters in a shared array, with the counters adjacent and then 64 bytes apart. Time both versions, and, where available, use `perf c2c` to see the cache-line contention.
