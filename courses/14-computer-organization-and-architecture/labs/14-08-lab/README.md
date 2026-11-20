# Lab 14-08 · Out-of-Order and Superscalar Execution

Chapter: [14-08 Out-of-Order and Superscalar Execution](../../chapters/14-08-out-of-order-and-superscalar.md)

## Objective

Measure instruction-level parallelism the way architects first estimate it, with a trace-driven limit study. Run RISC-V programs on the course simulator, record every executed instruction with its registers and memory address, and replay the trace through a model of an in-order or out-of-order superscalar core. Then turn the knobs one at a time (width, window, renaming, branch prediction) and see which limit binds for each program.

## Background

Dependences and the dataflow limit (§3.1), superscalar issue (§3.2), renaming, the window and the reorder buffer (§3.3), the limits of ILP (§3.4) and the model itself (§3.5).

## Tools

Python with the LLVM tools of [Lab 14-03](../14-03-lab/README.md#tools) (`llvm-mc`, `ld.lld`), used through the course toolkit. Part 4 also uses the predictor models of [Lab 14-07](../14-07-lab/README.md).

## Files

- [ooo.py](ooo.py):
  - `dyn_trace()` runs a program on the course simulator and returns its dynamic instructions;
  - `critical_path()` gives the dataflow limit;
  - `schedule()` replays a trace through the machine model and returns cycles and IPC (and, with `detail=True`, each instruction's dispatch, issue, completion and retirement cycles);
  - `mispredicted_indices()` marks the control transfers a 14-07 predictor gets wrong;
  - the workloads: `INC` (the unrolled loop of Example 14-08.4), `PTR` (the linked list of Example 14-08.5), `ARR`, `DIV`, and `lab_program()` (the recursive-Fibonacci program of Labs 14-05 to 14-07).
- [14-08-ooo-lab.ipynb](14-08-ooo-lab.ipynb): the notebook (Parts 1–4).

## Procedure

1. **The dataflow limit (Part 1).** Find the critical path of `INC`, `PTR` and the lab program, and check that a machine with unlimited width and window finishes exactly 2 cycles later (one to dispatch, one to retire).
2. **Width and window (Part 2).** Sweep the width (1, 2, 4, 8) and the window (16, 64, 256 entries) for each workload, in order and out of order, and plot IPC. *Predict first:* what IPC does the 8-wide core reach on the linked list?
3. **Renaming (Part 3).** Turn renaming off for `INC` and for the lab program. Which suffers more, and why?
4. **Branch mispredictions (Part 4).** Mark the lab program's mispredicted transfers with the gshare and the 2-bit predictors of 14-07 (both with a return stack), and replay with refill penalties of 0, 5, 10 and 20 cycles.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Dataflow limits | 69 cycles for `INC` (901 instructions), 302 for `PTR` (402), 187 for the lab program (1923) |
| 2 | Width and window | `INC`: 905, 459, 262 and 134 cycles at widths 1, 2, 4, 8 with 256 entries; `PTR`: 304 from 4-wide on; the lab program: IPC 7.54 at 8-wide with perfect prediction |
| 3 | Renaming off | `INC` 8-wide: 324 cycles instead of 134; the lab program: 497 instead of 255 with perfect prediction, but only 979 instead of 819 with mispredictions |
| 4 | Mispredictions | gshare (42 mispredictions): 255 cycles become 819 at 8-wide; the 2-bit predictor (93): 1453 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-08.a | critical path, `INC` | 69 | cycles |
| Lab 14-08.b | critical path, `PTR` | 302 | cycles |
| Lab 14-08.c | critical path, lab program | 187 | cycles |
| Lab 14-08.d | `INC`, 2-wide out of order, 256 entries | 459 | cycles |
| Lab 14-08.e | `INC`, 4-wide out of order, 16 entries | 283 | cycles |
| Lab 14-08.f | lab program, 4-wide, 64 entries | 491 | cycles |
| Lab 14-08.g | lab program, 8-wide, 64 entries | 263 | cycles |
| Lab 14-08.h | lab program, 8-wide, 256 entries | 255 | cycles |
| Lab 14-08.i | `INC`, 8-wide, no renaming | 324 | cycles |
| Lab 14-08.j | mispredictions, gshare + RAS | 42 | — |
| Lab 14-08.k | lab program, 8-wide, gshare, refill 10 | 819 | cycles |
| Lab 14-08.l | lab program, 8-wide, gshare, refill 0 | 399 | cycles |
| Lab 14-08.m | lab program, 4-wide in order, gshare, refill 10 | 1275 | cycles |
| Lab 14-08.n | lab program, 8-wide, no renaming, gshare, refill 10 | 979 | cycles |
| Lab 14-08.o | mispredictions, 2-bit + RAS | 93 | — |
| Lab 14-08.p | lab program, 8-wide, 2-bit, refill 10 | 1453 | cycles |
| Lab 14-08.q | lab program, 8-wide, no renaming, perfect prediction | 497 | cycles |
| Lab 14-08.r | lab program, 8-wide IPC, perfect prediction | 7.54 | — |
| Lab 14-08.s | extra cycles per misprediction at refill 0 | 3.4 | cycles |
| Lab 14-08.t | instructions per misprediction | 46 | — |

*These are recomputed by [verify_14_08.py](../../verify/verify_14_08.py) from traces collected on the course simulator.*

## Discussion questions

1. The model has no caches, a fixed load latency and unlimited execution units. Which of its conclusions would survive in a real core, and which would change?
2. Even with no refill penalty (refill 0), the 8-wide core takes 399 cycles on the lab program instead of 255. Where do the other 144 cycles go?
3. Why does turning renaming off hurt `INC` so much, but the lab program much less once mispredictions are included?

### Answers

1. The *orderings* survive. The linked list is limited by its chain of loads, `INC` by width and window, and the lab program by branches. A real cache makes the load latency variable and sometimes hundreds of cycles, which makes the window matter more (Little's law) and the linked list worse still. Finite execution units and ports lower every IPC somewhat, especially for `INC`'s 4 loads and 4 stores per iteration. Wrong-path instructions occupy fetch and execution bandwidth that the model treats as idle.
2. Each misprediction still blocks fetch until the branch resolves, and the branch waits for its operands, often a reload of `ra` from the stack. Nothing younger than the branch was dispatched meanwhile, so after the refill the window must fill again with new work, which takes several cycles. The 144 cycles, about 3.4 per misprediction, are resolution delays and lost overlap.
3. In `INC`, iterations reuse t1 to t4, so without renaming each iteration waits for the previous one, removing almost all of the parallelism. With perfect prediction the lab program suffers too (497 cycles against 255), because its recursion reuses a0, t0, s0 and s1 constantly. With mispredictions, though, the 42 mispredictions already break the stream into short runs of about 46 instructions. Within a run there is less overlap left for renaming to unlock, so it costs only a fifth more time.

## Optional hardware extension

On a Linux machine, `perf stat -e instructions,cycles` reports a real core's IPC. Write the array sum and the linked-list sum of Problem 14-08.8 in C, with the list nodes allocated in shuffled order, and make the data larger than the caches. Compare the measured IPCs: the gap is far wider than in this model, because each list step becomes a cache miss.
