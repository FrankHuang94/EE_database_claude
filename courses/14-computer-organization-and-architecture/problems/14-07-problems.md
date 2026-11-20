# Problems 14-07 · Branch Prediction and Speculation

Chapter: [14-07](../chapters/14-07-branch-prediction-and-speculation.md) · Worked solutions: [14-07 solutions](../solutions/14-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** the predictor models of §4 (1024-entry tables, 2-bit counters starting weakly not taken (1), 1-bit flags starting not taken, 64-entry BTB, optional RAS). Cycle counts on the five-stage pipeline use $N + 4 + S + 2M$; for a "deep pipeline" replace the 2 by its penalty $P$. T = taken, N = not taken.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-07.1 [A]

**CPI from accuracy.** Control transfers are 15% of instructions, the predictor is 92% accurate, and a misprediction costs 12 cycles. With a base CPI of 1, what is the CPI?

### Problem 14-07.2 [A]

**Tracing predictors.** A branch's outcomes are T, T, N, T, T, T, N, N, T. Trace (a) a 2-bit counter starting at 1 and (b) a 1-bit predictor starting at N. Count each one's mispredictions and give the counter's final state.

### Problem 14-07.3 [A]

**Static prediction.** Under BTFN, what accuracy do you get on (a) a forward branch that skips an `if` body and is taken 30% of the time, and (b) a loop's backward branch with 20 iterations per loop execution?

### Problem 14-07.4 [B]

**Short loops.** A loop of $n$ iterations runs many times. In steady state, what is the accuracy of a 2-bit counter and of a 1-bit predictor on its backward branch, as functions of $n$? Evaluate both for $n$ = 3.

### Problem 14-07.5 [B]

**How much history?** The nested loops of Example 14-07.1 (an outer loop of 100, an inner loop of $k$ iterations) run under gshare with $h$ bits of history. Find the smallest $h$ that predicts the inner exit correctly after warm-up, for $k$ = 4 and $k$ = 10. Why is the answer $k$ and not $k - 1$?

### Problem 14-07.6 [B]

**How deep a return stack?** In the lab program, what is the deepest nesting of calls? How many mispredicted fetches does the 2-bit + BTB predictor have with return stacks of depth 2, 4 and 16?

### Problem 14-07.7 [B]

**Aliasing.** A 1024-entry BHT is indexed by PC bits 11–2. Which entries do branches at 0x1000 and 0x2000 use? If the two branches have opposite biases, what happens? What table size separates them?

### Problem 14-07.8 [B]

**MPKI.** A workload suffers 5 mispredictions per thousand instructions (MPKI). What CPI does that add on the five-stage pipeline (penalty 2) and on a deep pipeline (penalty 15)?

### Problem 14-07.9 [B]

**Removing the branch.** The count loop of Example 14-07.6 can be written without the data-dependent branch:

```asm
count:
    li   t0, 0
    beqz a1, 3f
1:  lw   t1, 0(a0)
    addi a0, a0, 4
    slt  t2, a2, t1
    add  t0, t0, t2
    addi a1, a1, -1
    bnez a1, 1b
3:  mv   a0, t0
    ret
```

On the 1000 unsorted values, the branchy version executes 5526 instructions with 1000 load-use stalls and 504 mispredictions; the branchless one executes 6010 with 0 stalls and 3 mispredictions. Compare their cycles with a penalty of 2 and of 15. Why does the branchless version also avoid the load-use stalls?

### Problem 14-07.10 [C]

**Index masking against Spectre variant 1.** A bounds-checked access `if (x < size) y = a[x]` with `size` = 256 can be hardened as `y = a[x & (size - 1)]` inside the check. (a) What index does an attacker's `x` = 1000 produce under speculation? (b) Why does this stop the leak, and why must `size` be a power of two? (c) What does the masking cost?

### Problem 14-07.11 [C]

**Predictor storage.** Estimate the storage of (a) a gshare predictor with $2^{12}$ 2-bit counters and a 12-bit history register, and (b) a 1024-entry BTB whose entries hold a 20-bit tag, a 30-bit target and a valid bit. Express each in KiB.

### Problem 14-07.12 [C]

**When one bit beats two.** In the lab program, the 1-bit predictor (185 mispredicted fetches, with BTB and no RAS) beats the 2-bit counter (205). Looking only at `fib`'s base-case branch (`blt a0, t0, base`, 177 executions, 89 taken), the 1-bit predictor is wrong 67 times, the 2-bit counter 87 times and gshare 35 times. Explain why hysteresis hurts here, and why global history helps.

---

## Objective coverage

| Learning objective (chapter 14-07) | Problems |
|---|---|
| 1. CPI cost of mispredictions | 1, 8, 9 |
| 2. Static, 1-bit, 2-bit and gshare predictors | 2, 3, 4, 5, 12 |
| 3. BTB and return-address stack | 6, 7, 11 |
| 4. Trace-driven evaluation and cycle counts | 5, 6, 9, 12 |
| 5. Speculation and Spectre | 10 |
