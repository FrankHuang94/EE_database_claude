# Lab 05-06 · C Pointers, Arrays and Memory

**Chapter:** [05-06](../../chapters/05-06-c-pointers-and-memory.md) · **Files:** [samplelog.h](samplelog.h), [samplelog.c](samplelog.c), [samplelog_test.c](samplelog_test.c), [membugs_demo.c](membugs_demo.c) · **Time:** about 90 minutes

## Objective

1. Read and test a heap-backed data structure: a growable sample log that owns its memory, reports statistics and formats a bounded string.
2. Reproduce five classic memory bugs and learn to read AddressSanitizer's reports.
3. Measure how field order changes a struct's size.

## Background

Chapter sections 3.3 (arrays and pointer arithmetic), 3.4 (strings), 3.5 (structs), 3.7 (dynamic allocation) and 3.8 (memory bugs), and Examples 05-06.3 to 05-06.5. The test runs in CI through [`tools/run_c.py`](../../../../tools/run_c.py) under AddressSanitizer, LeakSanitizer (on Linux) and UndefinedBehaviorSanitizer, so a leak or overflow in `samplelog.c` fails the build even if every check passes. `main(int argc, char **argv)` in the demo receives the command-line words as an array of strings: `argv[1]` is the first word after the program's name.

## Procedure

1. **Run the tests.**

   ```bash
   cc -std=c17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined samplelog_test.c samplelog.c -o samplelog_test
   ./samplelog_test
   ```

2. **Growth.** *Predict:* the log starts with capacity 8 and doubles. How many reallocations does storing 1000 samples cause, and what is the final capacity? Check against the `log.reallocs` and `log.cap` assertions.
3. **Break the ownership rule.** In a copy of `samplelog.c`, delete the `free(log->data);` line in `samplelog_free`, rebuild and run. *Predict:* do the checks still pass? What does the program report when it exits?
4. **The five bugs.** *Predict:* for each of bugs 1 to 5 in `membugs_demo.c`, which report will ASan print, and which bug is reported only when the program exits?

   ```bash
   cc -std=c17 -g -O1 -fsanitize=address -fno-omit-frame-pointer membugs_demo.c -o membugs
   ./membugs 1     # then 2, 3, 4, 5
   cc -std=c17 -O1 membugs_demo.c -o membugs_plain
   ./membugs_plain 1     # the same bugs without ASan
   ```

5. **Struct layout.** Write a short program printing `sizeof` and `offsetof` for `struct { uint8_t id; uint32_t value; uint16_t flags; }`, then reorder the fields largest first.

## Expected results

| Step | Expected |
|---|---|
| 1 | `TEST PASSED` |
| 2 | 7 reallocations (8 → 16 → … → 1024), final capacity 1024 |
| 3 | every check passes, then LeakSanitizer reports `detected memory leaks`, 2048 bytes (the final 1024-sample block) in 1 allocation, and the run fails |
| 4 | 1: `heap-buffer-overflow`; 2: `heap-use-after-free`; 3: `attempting double-free`; 4: LeakSanitizer `detected memory leaks`, 6400 bytes in 100 allocations, at exit; 5: `stack-use-after-return` (older toolchains need `ASAN_OPTIONS=detect_stack_use_after_return=1`). Without ASan: bugs 1 and 4 print 0 silently, 2 and 5 print arbitrary numbers, and 3 is caught by glibc's allocator (`free(): double free detected`) and aborts |
| 5 | 12 bytes with offsets 0, 4, 8; 8 bytes reordered |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 05-06.a | reallocations for 1000 samples | 7 | — |
| Lab 05-06.b | final capacity | 1024 | samples |
| Lab 05-06.c | mean of the 1000 test samples | 0.01 | — |
| Lab 05-06.d | length of the full status text | 31 | characters |
| Lab 05-06.e | bytes leaked if samplelog_free does not free | 2048 | bytes |
| Lab 05-06.f | bytes leaked by bug 4 | 6400 | bytes |

## Discussion questions

1. Why does the mean of the samples $(37i \bmod 101) - 50$ for $i = 0, \dots, 999$ come out as exactly 0.01?
2. In step 3 every check passed, yet the build failed. What does that say about "the tests pass" as evidence of correctness?
3. Without ASan, bugs 1 and 4 produced correct-looking output. Why are these the dangerous ones?
4. `samplelog_push` assigns `realloc`'s result to a temporary before updating `log->data`. What would go wrong if it wrote `log->data = realloc(log->data, ...)`?

<details><summary>Answers to the discussion questions</summary>

1. Because 37 and 101 have no common factor, $37i \bmod 101$ runs through all residues 0 to 100 exactly once in every 101 consecutive values of $i$, and those residues minus 50 sum to $\sum_{r=0}^{100}(r - 50) = 0$. 1000 samples are 9 complete cycles (909 samples, summing to 0) plus the first 91 values of the next cycle, $i = 909, \dots, 999$, which are the same as $i = 0, \dots, 90$. Their sum is 10, so the mean is $10/1000 = 0.01$. The verify script recomputes this independently.
2. The checks tested behavior (values, sizes, strings) but not resource ownership; only the leak checker, run automatically at exit, saw that memory was never returned. A passing test suite is evidence about what it checks, nothing more; that is why the course's C tests always run under sanitizers.
3. They give no sign of failure. The overflow corrupted memory nobody happened to read afterward, and the leak only costs memory, which on a desktop test run is plentiful. In a long-running device the leak exhausts RAM after hours or days, and the overflow corrupts whatever the next code version places next to the array: failures that appear far from their cause.
4. If `realloc` fails it returns `NULL` but leaves the old block allocated. Assigning directly would overwrite the log's only pointer to its data with `NULL`: the samples would be lost and the block leaked, and the next push would treat the log as empty-but-full. With a temporary, the function returns −1 and the log is unchanged, so the caller can still use or free it.

</details>

## Optional hardware version

On a microcontroller board, replace the heap in `samplelog.c` with a static array of fixed capacity (as MISRA C requires), make `samplelog_push` return −1 when it is full, and measure the board's free RAM before and after with the vendor's tools or the linker map file.
