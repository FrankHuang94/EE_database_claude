# Lab 05-08 · Data Structures and Algorithms

**Chapter:** [05-08](../../chapters/05-08-data-structures-and-algorithms.md) · **Files:** [ds.h](ds.h), [ds.c](ds.c), [ds_test.c](ds_test.c), [05-08-complexity.ipynb](05-08-complexity.ipynb) · **Time:** about 2 hours

## Objective

1. Read and test three core data structures in C: a ring buffer with free-running counters, a linear-probing hash map that resizes itself, and a binary min-heap.
2. Measure growth rates by counting operations, and compare them with the formulas of the chapter.
3. Measure hash-table probe counts against load factor.

## Background

Chapter sections 3.1 (Big-O), 3.3 (ring buffers), 3.6 (hash tables), 3.7 (heaps) and 3.8 (searching and sorting), and Examples 05-08.2 to 05-08.5. The C test runs in CI through [`tools/run_c.py`](../../../../tools/run_c.py) with strict warnings and sanitizers; the notebook runs through `tools/run_notebooks.py`. The map's keys are 32-bit integers hashed with FNV-1a over their four bytes, taken in a fixed (little-endian) order so the table behaves identically on every host (05-07).

## Procedure

1. **Run the C tests.**

   ```bash
   cc -std=c17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined -fno-sanitize-recover=all \
      ds_test.c ds.c -o ds_test
   ./ds_test
   ```

2. **Resizing.** The map starts with 8 slots and doubles whenever an insertion would push the load factor above 0.75. *Predict:* after 1000 insertions, what is the capacity and how many resizes happened? Check against the test's assertions.
3. **Probe counts.** Add a `printf` of `m.probes / 1000.0` after the lookup loop. *Predict* the average from the formula $\tfrac12(1 + 1/(1-\alpha))$ at the final load factor.
4. **Break the resize rule.** Change the threshold test to `4 * (m->count + 1) > 4 * m->cap` (resize only when the table is completely full) and rerun. *Predict:* what happens to the probe counts? (Be ready to stop the program with Ctrl-C.)
5. **Notebook.** Run [05-08-complexity.ipynb](05-08-complexity.ipynb) and answer its **🔮 Predict** prompts before running each part.

## Expected results

| Step | Expected |
|---|---|
| 1 | `TEST PASSED` |
| 2 | capacity 2048 after 8 resizes (8 → 16 → … → 2048); 1000 keys need at least $1000/0.75 = 1334$ slots |
| 3 | load $1000/2048 = 0.488$; formula 1.48 probes; measured 1.52 |
| 4 | the program hangs. With the new rule the table fills completely at 8 entries; `map_put` first searches for the new key, and a search for an absent key in a full table never meets an empty slot, so it loops forever. Even before that point, probe counts explode as the load approaches 1. An open-addressing table must never fill completely |
| 5 | linear search slope ≈ 1.0; binary search ≈ 15.2 comparisons at $n$ = 65,536; insertion sort slope 2.00, merge sort slope ≈ 1.2; probe counts within about 10% of the formulas at α = 0.5, 0.75 and 0.9 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-08.a | final map capacity | 2048 | slots |
| Lab 05-08.b | resizes during 1000 insertions | 8 | — |
| Lab 05-08.c | final load factor | 0.488 | — |
| Lab 05-08.d | formula: successful probes at that load | 1.48 | — |
| Lab 05-08.e | ring-buffer drops in the UART scenario | 2 | — |

## Discussion questions

1. The map stores a separate `used` flag per slot instead of reserving a special key value to mean "empty". Why?
2. The test jumps the ring buffer's counters to just below $2^{32}$ before pushing. What bug would that catch, and why is it unlikely to be found by ordinary testing?
3. This map does not support deletion. Why is deleting from a linear-probing table harder than it looks?
4. Why does the notebook count operations instead of timing them?

<details><summary>Answers to the discussion questions</summary>

1. Every 32-bit value is a legitimate key, so no key value can safely mean "empty"; a sentinel would make one key impossible to store, a bug that appears only when a user happens to use it. A separate flag (or a separate bitmap) costs a byte per slot here but keeps the key space whole.
2. A buffer that computes counts or indices with signed arithmetic, or compares counters with `<`, works until the counters wrap, which at realistic data rates happens after hours or days (49.7 hours for a 24 kB/s stream, Problem 05-08.4). Ordinary tests run for seconds and never reach the wrap; setting the counters directly reproduces the condition in microseconds.
3. Lookups stop at the first empty slot. Simply emptying a deleted entry's slot can break the probe chain of a later key that was placed beyond it, making that key unfindable. Implementations either mark deleted slots with a "tombstone" (treated as occupied by lookups and as free by insertions) or shift later entries of the cluster back (backward-shift deletion).
4. Timings depend on the processor, the cache, other running programs and the Python version, so they vary between machines and runs, and constant factors blur the growth rate. Operation counts are exactly reproducible and isolate the quantity Big-O describes. (Timing still matters for decisions; it answers a different question.)

</details>

## Optional hardware version

On a microcontroller board with a UART, implement the ring buffer in the receive interrupt (with the atomic counters and publish-last order of Example 05-08.2; the lab's `ds.c` version is single-threaded and is not safe to share with an interrupt as written), send a long burst from a PC while the main loop deliberately stalls, and compare the `dropped` counter with the overflow predicted from the baud rate, the buffer size and the stall time.
