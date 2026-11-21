# Lab 19-04 · Logical Effort: Sizing Paths and Buffer Chains

Chapter: [19-04 · Transistor Sizing and Logical Effort](../../chapters/19-04-sizing-and-logical-effort.md)

## Objective

- Compute gate efforts, path effort and optimal sizes, and confirm the equal-effort rule by brute-force numerical optimization.
- Find the best stage effort and number of stages, and see how flat the optimum is.
- Compare logical-effort predictions with transistor-level simulations of buffer chains in Python and ngspice.

## Background

A gate's delay is $d = gh + p$ in units of $\tau = 0.69RC_{inv}$ (§3.1). A path's effort $F = GBH$ is fixed by its topology and end capacitances, and its delay is smallest when every stage bears $\hat f = F^{1/N}$, giving $\hat D = NF^{1/N} + P$ (§3.3). Sizes follow backward from the load, $C_{in,i} = g_iC_{out,i}/\hat f$ (§3.4). The best stage effort satisfies $\rho(\ln\rho - 1) = p_{inv}$, 3.59 for $p_{inv}$ = 1 (§3.5).

Files:

- `chain.cir`: a unit inverter and a three-stage tapered chain (sizes 1, 4, 16) driving 128 fF, with the level-1 model and explicit gate (2 fF per unit size) and self-loading (2 fF per unit size) capacitances.
- `effort.py`: `logical_effort`, `parasitic_delay`, `stage_delay`, `path_effort`, `min_path_delay`, `stage_input_caps`, `best_stage_effort`, `chain_delay`, `best_stage_count` and `simulate_chain` (a square-law transistor-level simulation of an inverter chain).
- `19-04-effort-lab.ipynb`: the procedure below.

## Procedure

1. **Buffer chains at transistor level.** Predict the single inverter's and the three-stage chain's delays from logical effort (65τ and 15τ with τ = 17.43 ps). Run `ngspice -b chain.cir` and Part 1.
2. **How many stages?** Predict the best of one to four stages for $H$ = 64; simulate each with `simulate_chain` (Part 2).
3. **Equal efforts.** Size Example 19-04.3's path by numerically minimizing the total delay over the three sizes; compare with the backward rule (Part 3).
4. **The best stage effort.** Predict ρ for $p_{inv}$ from 0 to 3; plot it, and plot the delay per $\ln F$ against stage effort (Part 4).
5. **Topologies.** Predict which of Example 19-04.6's topologies wins as $H$ goes from 1 to 1000; plot all three (Part 5).

## Expected results

- Part 1: the single inverter takes 1095.9 ps (62.9τ, close to the predicted 65τ) and the chain 404.3 ps (23.2τ against 15τ), in both ngspice and Python: a speed-up of 2.71 rather than 4.33.
- Part 2: one, two, three and four stages take 1095.9, 437.0, 404.3 and 433.1 ps; three stages are best, as logical effort predicts, though the absolute delays are about 1.5 times longer than predicted for the chains.
- Part 3: the numerical optimum gives input capacitances 16.7 (NOR2) and 44.8 (inverter) and a delay of 18.39τ, exactly the logical-effort result.
- Part 4: ρ = 2.72, 3.59, 4.32 and 4.97 for $p_{inv}$ = 0, 1, 2 and 3; the delay per $\ln F$ curve is within 9% of its minimum from 2.4 to 6.
- Part 5: NAND4 + NOR2 wins below $H$ = 6.7; the four-stage tree wins above; NAND8 + INV never wins.

## Discussion

1. Why is the single inverter's simulated delay close to the logical-effort prediction while the chain's is not?
2. If the chain's absolute delay is mispredicted, why is the best number of stages still right?
3. Why does the numerical optimization of Part 3 land exactly on equal stage efforts?
4. Why does the four-stage tree lose to NAND4 + NOR2 for small loads?

**Answers.**

1. The single inverter is driven by a near-step, the condition under which τ was defined (19-02's step-input $R_{eq}$). Each stage of the chain is driven by the slow ramp of the previous one, which lengthens its delay (19-02 §3.6).
2. The slope penalty affects every stage of every candidate chain similarly, so it scales the delays without moving the optimum much; calibrating τ from an FO4 chain absorbs it (Problem 19-04.8).
3. Under the model the delay is $\sum g_ih_i + P$ with $\prod g_ih_i$ fixed, and the sum of numbers with a fixed product is smallest when they are equal (§3.3).
4. With little effort to share, the tree's extra stages add parasitic delay (7 against 6) without enough effort to divide.

## Optional hardware

With a CD4069 hex inverter, wire a single inverter and a chain of two or three paralleled inverters (one, two, then three gates of the package in parallel as larger stages) driving a large capacitor such as 1 nF, and compare their delays on an oscilloscope at 5 V.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-04.a | single inverter delay, transistor level | 1095.9 | ps |
| Lab 19-04.b | three-stage chain delay, transistor level | 404.3 | ps |
| Lab 19-04.c | simulated speed-up | 2.71 | — |
| Lab 19-04.d | two-stage chain delay | 437.0 | ps |
| Lab 19-04.e | four-stage chain delay | 433.1 | ps |
| Lab 19-04.f | chain delay over prediction, three stages | 1.5 | — |
| Lab 19-04.g | best stage effort, p_inv = 3 | 4.97 | — |
| Lab 19-04.h | H where the tree overtakes NAND4 + NOR2 | 6.7 | — |
