# Lab 08-05 · Verilog and Testbenches

**Chapter:** [08-05](../../chapters/08-05-verilog-and-testbenches.md) · **Notebook:** [08-05-verilog-semantics.ipynb](08-05-verilog-semantics.ipynb) · **Time:** about 3 hours

## Objective

1. Confirm in a real simulator every claim of the chapter's worked examples: widths, signedness, four-valued logic, blocking and non-blocking assignment, sensitivity lists.
2. Write and run a self-checking testbench with directed, exhaustive and random stimulus.
3. Measure the coverage of a random test and compare it with the theory of §3.8.
4. Look at a waveform in GTKWave.

## Background

Chapter sections 3.1 to 3.9 and Examples 08-05.1 to 08-05.7. You need Icarus Verilog and Python with NumPy and Matplotlib; GTKWave is optional (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [08-05-verilog-semantics.ipynb](08-05-verilog-semantics.ipynb) | Python models of four-valued logic, assignment semantics and random coverage; runs the testbenches if Icarus is installed | Its own `assert`s and this handout's key |
| [semantics_tb.v](semantics_tb.v) | Evaluates the simulator-checkable examples of chapter §4 (08-05.1 to 08-05.4 and 08-05.7) and checks the chapter's answers | Prints `TEST PASSED` |
| [cmp8.v](cmp8.v) | An 8-bit comparator (equal, unsigned less-than, signed less-than) built from a subtractor | `cmp8_tb.v` |
| [cmp8_tb.v](cmp8_tb.v) | Directed corner cases, an exhaustive sweep and a measured random run; writes `cmp8.vcd` | Prints `TEST PASSED` |

Run from the repository root:

```bash
python tools/run_hdl.py
```

or by hand, from this folder:

```bash
iverilog -g2012 -o cmp8.vvp cmp8_tb.v cmp8.v && vvp cmp8.vvp && gtkwave cmp8.vcd
```

## Procedure

1. **The chapter, checked by the simulator.** Read `semantics_tb.v` next to chapter §4, predict each result, then run it. Change one expected value and watch the testbench report the mismatch.
2. **Four-valued logic (notebook Part 1).** Regenerate the AND, OR and XOR tables for 0, 1, X and Z, and count the definite results.
3. **Assignment semantics (notebook Part 2).** Replay the shift register and swap of Example 08-05.4 with both update rules, and enumerate the process orders of the race in Problem 08-05.13.
4. **Random coverage (notebook Part 3, the chapter's guided exercise).** *Predict first:* of the comparator's 65 536 input pairs, how many will 65 536 random vectors hit, and how much will that count vary from seed to seed? Then run `cmp8_tb.v` (it prints its count) and the notebook's simulation over many seeds.
5. **Waveforms.** Open `cmp8.vcd` in GTKWave and find the directed corner cases: at which one do `ltu` and `lts` disagree first?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | `semantics_tb.v` | `TEST PASSED`: Icarus agrees with every number in chapter §4 |
| 2 | definite results of 16 | AND 8, OR 8, XOR 4 |
| 3 | assignment semantics | non-blocking: 3-edge delay and a swap; blocking: 1 edge and a copy; the race has 2 outcomes |
| 4 | random coverage | see the key; `cmp8_tb.v` checks that its own count lies within 1% of the mean |
| 5 | waveform | `ltu` and `lts` disagree when the operands' sign bits differ, first at 7F₁₆ against 80₁₆ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 08-05.a | comparator input pairs | 65536 | — |
| Lab 08-05.b | vectors checked by `cmp8_tb.v` | 131077 | — |
| Lab 08-05.c | expected distinct pairs hit by 65 536 random vectors | 41427 | — |
| Lab 08-05.d | standard deviation of that count | 79.8 | — |
| Lab 08-05.e | the testbench's ±1% window, in standard deviations | 5.19 | — |

**Reading the key.** The mean follows from §3.8: $M\left(1 - (1 - 1/M)^{M}\right)$ with $M = 65\,536$. The spread comes from the variance of a sum of dependent indicators: for the count $D$ of distinct inputs hit, $\operatorname{Var}(D) = M q_1(1 - q_1) + M(M - 1)(q_2 - q_1^2)$, where $q_1 = (1 - 1/M)^N$ is the probability that a given input is missed and $q_2 = (1 - 2/M)^N$ the probability that two given inputs are both missed. A ±1% window is about ±5 standard deviations, so the testbench's coverage check will essentially never fail by chance, yet any real bug in the coverage bookkeeping would trip it.

## Discussion questions

1. `semantics_tb.v` assigns `y_bad` with an incomplete sensitivity list. Would Verilator's lint flag it if it were in a design file?
2. Why does `cmp8_tb.v` check the outputs `#1` after changing the inputs, rather than at the same instant?
3. The exhaustive sweep already covers every input. What do the directed and random parts add?
4. A colleague's testbench prints "PASS" after comparing outputs with `!=`. What class of bug can it miss?
5. Why is `cmp8.v` written with an explicit 9-bit subtraction instead of `assign ltu = a < b;`? When would the shorter form be better?

<details><summary>Answers to the discussion questions</summary>

1. Yes, though not by that name. Verilator 5.020 treats `always @(a)` as a sequential process (one triggered by a specific signal, not by everything it reads) and warns `BLKSEQ`, "Blocking assignment '=' in sequential logic process", which points straight at the mistake. Writing `always @(*)` or `always_comb` avoids the problem altogether. The testbench keeps the bug on purpose, outside the linted design files, to demonstrate the mismatch.
2. The inputs and the continuous assignments inside `cmp8` change in the same time step; checking in that step would race with the update. Waiting 1 ns lets every assignment settle, so the checker sees the final outputs.
3. Directed cases document the corners a reader cares about (signed/unsigned disagreement, overflow) and appear first in the waveform; they also survive if the exhaustive loop is later cut down for a wider design. The random run demonstrates coverage measurement, which is the only option when exhaustive testing becomes impossible, as it does at 16-bit operands (2³² pairs) and beyond.
4. Any output that becomes X or Z: `!=` returns X, an `if` treats it as false, and the testbench passes. Uninitialized registers, missing resets and multiply-driven nets all show up as X.
5. To mirror the hardware of 08-04 §3.7 and expose the borrow and overflow signals for study. In production RTL, `a < b` (with `$signed` where needed) is clearer, and synthesis builds an equally good comparator.

</details>

## Optional hardware

Any FPGA board can run `cmp8` with switches for `a` and `b` and LEDs for the three outputs; the synthesis flow is covered in [08-12](../../chapters/08-12-fpga-implementation-flow.md). The testbench itself never goes to hardware, which is the point: it is the executable specification.
