# Lab 14-07 · Branch Prediction and Speculation

Chapter: [14-07 Branch Prediction and Speculation](../../chapters/14-07-branch-prediction-and-speculation.md)

## Objective

Evaluate branch predictors the way architects do, by trace-driven simulation. Run RISC-V programs on the course simulator, record every control transfer, and replay the trace through static, 1-bit, 2-bit and gshare predictors with a branch target buffer and a return-address stack. Turn the mispredictions into cycle counts with 14-06's pipeline model, and see when a branch is better removed than predicted.

## Background

The cost of misprediction (§3.1), static and dynamic predictors (§3.2–3.3), the BTB and return-address stack (§3.4) and speculation (§3.5–3.6).

## Tools

Python with the LLVM tools of [Lab 14-03](../14-03-lab/README.md#tools) (`llvm-mc`, `ld.lld`), used through the course toolkit.

## Files

- [bpred.py](bpred.py): `trace()` collects a program's control-flow events from the course simulator; `simulate()` replays them through a predictor and counts mispredicted fetches.
- [14-07-branch-prediction-lab.ipynb](14-07-branch-prediction-lab.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Loops (Part 1).** Trace the nested loops of Examples 14-07.1 to 14-07.3 and print each predictor's state branch by branch for the first few outer iterations.
2. **The lab program (Part 2).** Replay the program of Labs 14-05 and 14-06 through five predictor configurations and convert the mispredictions to cycles. *Predict first:* which helps more, gshare or a return-address stack?
3. **Data-dependent branches (Part 3).** Count elements above a threshold in random and in sorted data, then with the branchless loop of Problem 14-07.9.
4. **Aliasing (Part 4).** Shrink the BHT from 1024 entries to 1 and count mispredictions for the sorted count loop of Part 3, whose loop branch and data branch then share counters.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Loops | 1-bit: 2 mispredictions per inner-loop execution, 2-bit: 1; gshare learns the 4-iteration loop (12 mispredictions against 103) |
| 2 | Lab program | 2850 cycles without prediction, 2348 with 2-bit + BTB, 2124 adding a RAS, 2022 with gshare + RAS |
| 3 | Data | 504 mispredictions unsorted, 6 sorted; branchless 3, and the fastest at any penalty |
| 4 | Aliasing | 6 mispredictions with 1024 entries; 520 with 4 entries or fewer, where the always-taken loop branch and the data branch share a counter |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 14-07.a | control transfers in the lab program | 554 | — |
| Lab 14-07.b | returns among them | 178 | — |
| Lab 14-07.c | mispredicted fetches, sorted count loop, 4-entry BHT (2-bit, BTB, RAS) | 520 | — |
| Lab 14-07.d | mispredicted fetches, gshare + BTB + RAS | 42 | — |

*These are recomputed by [verify_14_07.py](../../verify/verify_14_07.py) from traces collected on the course simulator.*

## Discussion questions

1. Why does trace-driven simulation give the same misprediction counts whatever the pipeline's timing, and when is that assumption wrong?
2. In Part 4, why can a *smaller* table occasionally do better than a larger one?
3. The branchless count loop executes more instructions but runs faster. When would the branchy version win?

### Answers

1. The trace is the program's correct path, and the models update their tables in program order, as if each branch resolved before the next one was predicted. In a real pipeline a branch may be predicted before an older instance of itself has updated the table, and wrong-path instructions may disturb the global history. Trace-driven results are therefore an approximation, usually a good one. Cycle-level simulators model the delayed updates.
2. When two branches share an entry and happen to have the same bias, sharing can warm the entry faster ("constructive aliasing"). It is luck, not design: in general sharing destroys information.
3. When the branch is highly predictable (sorted data, or a rare condition), because then it costs almost nothing while the branchless version always pays for its extra instructions. On the sorted data at $P$ = 2, for example, the branchy loop takes 6542 cycles against the branchless 6020, but that gap is due to the load-use stalls. With those scheduled away, the branchy loop would win.

## Optional hardware extension

On a Linux machine, `perf stat -e branches,branch-misses` measures real mispredictions. Write the count loop in C, run it on random and on sorted data, and compare the measured miss rates and run times with Part 3.
