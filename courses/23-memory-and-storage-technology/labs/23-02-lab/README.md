# Lab 23-02 · SRAM Assists, Variation and Vmin

Chapter: [23-02 · SRAM Technology](../../chapters/23-02-sram-technology.md)

## Objective

Simulate an SRAM cell's read and write contests with and without assists, then use the chapter's models to see how threshold mismatch turns into write failures, how much negative bitline buys back, how $V_{min}$ grows with array size, and what longer bitlines trade.

## Background

§3.4 and §3.5 found the read-disturb voltage and the written node's voltage where two transistors' currents balance, and §3.3 turned the margin a large array needs into a minimum voltage. Here the mismatch is one combined variable δ that works against the write: the pass gate's threshold rises by δ and the pull-up's falls by δ, with δ normally distributed (σ = 25 mV, assumed). A write fails when the written node stays above the opposite inverter's switching threshold.

## Files

- `assist.cir`: an inverter tied to itself (its switching threshold), three write half-cells (nominal, 50 mV mismatch, mismatch with a −43 mV bitline) and two read half-cells (wordline 0.7 V and 0.6 V), all with level-1 transistors.
- `sramtech.py`: the chapter's models.
- `23-02-sram-lab.ipynb`: the notebook for Parts 2 to 4.

## Procedure

**Part 1 · Assists in ngspice.**

1. Predict $V_M$, the written node in the three write half-cells, and the read-disturb voltage and read current at the two wordline voltages (Examples 23-02.4 and 23-02.5).
2. Run `ngspice -b assist.cir` and compare.

**Part 2 · Write failures** (notebook).

1. Find the mismatch δ* at which the write fails with no assist, and the failure probability $Q(\delta^*/\sigma)$.
2. Draw 20,000 random cells and count failures. Compare with $Q(\delta^*/\sigma)$.
3. Repeat with −50 mV and −100 mV bitlines. Find the negative bitline that covers a 6σ (150 mV) mismatch.

**Part 3 · Vmin against array size** (notebook). Plot Example 23-02.3's $V_{min}$ from 1 Kib to 1 Gib for σ_VT of 25 mV and 20.4 mV.

**Part 4 · Bitline length** (notebook). Sweep cells per bitline from 64 to 1024 with Example 23-02.6's model and plot density and bitline time.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 23-02.a | written node, mismatch with −43 mV bitline | 0.347 | V |
| Lab 23-02.b | failing mismatch, no assist | 24.6 | mV |
| Lab 23-02.c | write-failure probability, no assist | 0.162 | |
| Lab 23-02.d | failing mismatch, −50 mV bitline | 54.1 | mV |
| Lab 23-02.e | write-failure probability, −50 mV bitline | 0.0153 | |
| Lab 23-02.f | negative bitline for a 150 mV (6σ) mismatch | -209 | mV |

- Part 1: every simulated value within 0.2% of the chapter's.
- Part 2: the Monte Carlo counts land close to $Q(\delta^*/\sigma)$ for the first two cases; with a −100 mV bitline only a handful of the 20,000 draws fail, so that estimate is noisy. Even then the failure rate is far above what a large array can tolerate.
- Part 3: $V_{min}$ grows by tens of millivolts over six decades of array size; the tighter device shifts the whole curve down.

## Discussion

1. Why is the failure probability without assist so high, at 16%?

   <details><summary>Answer</summary>

   With these sizes the nominal written node (0.221 V) sits not far below the trip point (0.347 V), and the node is very sensitive to mismatch: about one sigma (24.6 mV) is enough to fail. Real cells are sized and assisted so that the failing mismatch is six or more sigma away.

   </details>

2. Why does covering a 6σ mismatch need so much more negative bitline than covering 2σ?

   <details><summary>Answer</summary>

   Each extra millivolt of mismatch both weakens the pass gate and strengthens the pull-up, and the pass gate's current falls quadratically with its shrinking overdrive. The negative bitline needed grows faster than the mismatch it covers, which is why designers combine assists (negative bitline with cell-supply collapse) and use redundancy rather than relying on one assist.

   </details>

3. Why can't the designer simply make the pass gate stronger instead?

   <details><summary>Answer</summary>

   A stronger pass gate raises the read-disturb voltage (§3.4) and so hurts read stability. Read and write pull the pass gate's size in opposite directions, which is why assists that act only during one operation are valuable.

   </details>

## Optional hardware

Commercial microcontrollers often specify a minimum retention voltage for their SRAM in low-power modes. On a development board with an adjustable supply, write a pattern, lower the supply in sleep, raise it again and check the pattern. The voltage at which bits start to flip is a measured data-retention voltage, and the failing addresses show the spread across cells.
