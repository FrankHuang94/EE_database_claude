# Lab 25-12 · Shmoo Plots, Bug Discovery and Fix Decisions

**Objective.** Generate and fit a synthetic shmoo plot, find minimum voltages, fit a bug-discovery curve, size trace buffers, and compare fix options with a decision tree.

**Chapter:** [25-12 · Post-Silicon Validation and Bring-Up](../../chapters/25-12-post-silicon-validation.md)

## Background

§3.2 gave the trace-buffer storage $SD$ and window $D/f$. §3.3 modelled the shmoo boundary with $F_{max}(V) = K(V - V_{TH})^{\alpha}/V$. §3.4 introduced the Goel–Okumoto curve $m(t) = a(1 - e^{-bt})$, and §3.5 the fix decision tree. §3.6 used the Wilson score interval.

## Files

- `postsi.py`: trace sizing, the alpha-power model and a synthetic shmoo with a least-squares boundary fit, Vmin, Goel–Okumoto fitting, the fix decision tree, Wilson intervals and characterization sample sizes.
- `25-12-postsi-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Trace window** (notebook). *Predict* the storage needed to trace 256 signals over 50 µs at 2 GHz, then compute it.

**Part 2 · Shmoo** (notebook). Generate a synthetic shmoo from Example 25-12.2's model with 30 MHz of measurement noise, *predict* how close a least-squares fit of the boundary comes to the true $K$, then fit it and find $V_{min}$ for 2.0 GHz.

**Part 3 · Bug discovery** (notebook). Generate a noisy weekly bug log from $a$ = 120 and $b$ = 0.173 per week, *predict* the fitted total, then fit it by least squares and plot the curve.

**Part 4 · Decisions and statistics** (notebook). *Predict* the break-even success probability of the metal ECO with delay at $2 M a week, then compute it, and compute the Wilson interval for 16 of 320.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-12.a | trace storage for 50 µs | 3.05 | MiB |
| Lab 25-12.b | Vmin for 2.0 GHz | 0.565 | V |
| Lab 25-12.c | break-even probability at $2 M/week | 0.338 | |
| Lab 25-12.d | Wilson upper bound, 16 of 320 | 8.0 | % |

The shmoo fit recovers $K$ within 2%, and the least-squares bug-discovery fit recovers the total within about 10% for the noise used.

## Discussion

1. Part 2: the boundary fit uses the highest passing point per voltage. Why does measurement noise bias it, and in which direction?
2. Part 3: how does the fitted total change if you use only the first six weeks of data? What does that say about early "we're nearly done" claims?
3. Part 4: which input to the decision tree is hardest to estimate in practice, and how would you bound it?
4. How would you design a trace buffer's signal selection before tape-out, knowing you cannot change it afterwards?

## Optional hardware

Any microcontroller board with a debugger shows bring-up in miniature: connect through the debug port, halt the core, read registers and memory, and set a hardware breakpoint, the same capabilities a large SoC's debug infrastructure provides at scale.
