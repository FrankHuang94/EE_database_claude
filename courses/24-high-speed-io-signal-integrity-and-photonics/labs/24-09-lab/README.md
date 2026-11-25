# Lab 24-09 · Linear Budgets, Laser Sharing and Reliability Bounds

**Objective.** Sweep a linear link's margin against its optical segment; size external-laser sharing; check the rule of three for zero-failure reliability tests by simulation; and compare the availability cost of pluggable and co-packaged failures.

**Chapter:** [24-09 · Linear-Drive and Co-Packaged Optics](../../chapters/24-09-lpo-and-cpo.md)

## Background

§3.2 used 24-08's result that a linear chain adds $1/Q^2$, so its margin above the KP4 threshold shrinks as any segment degrades. §3.3 introduced external laser sources shared across lanes. §3.4 derived the zero-failure bound $\lambda_U = -\ln(0.05)/T$ and the unavailability per port, proportional to failure rate, ports lost per failure and repair time.

## Files

- `cpo.py`: energy per bit, dB conversions, linear budgets and margins, laser sharing, chi-square failure-rate bounds, port-hours lost and a Monte Carlo of zero-failure tests.
- `24-09-cpo-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Linear budget** (notebook). With both host channels at $Q$ = 10, *predict* the optical segment's $Q$ at which the linear link's margin above KP4 falls to 2 dB, then sweep it from 5 to 12.

**Part 2 · Laser sharing** (notebook). *Predict* how many lanes UHP (23 dBm) and SHP (26 dBm) sources can feed with Example 24-09.4's losses, then compute them.

**Part 3 · Zero-failure tests** (notebook). Set the true failure rate equal to the rule-of-three bound for one million device-hours. *Predict* the fraction of simulated tests that see no failures, then simulate 100,000 tests. Then compute the chi-square bounds for 0, 1 and 2 failures.

**Part 4 · Blast radius** (notebook). *Predict* the repair time at which a CPO port (400 FIT, 8 ports per engine) loses no more port-hours than a pluggable (200 FIT, 1 h repair), then sweep the repair time.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 24-09.a | optical Q for a 2 dB margin | 5.61 | |
| Lab 24-09.b | UHP lanes, binary | 32 | |
| Lab 24-09.b1 | SHP lanes, binary | 64 | |
| Lab 24-09.c | zero-failure probability at the bound | 0.0500 | |
| Lab 24-09.d | bound with 0 failures in 1 M h | 2996 | FIT |
| Lab 24-09.d1 | bound with 1 failure in 1 M h | 4744 | FIT |
| Lab 24-09.d2 | bound with 2 failures in 1 M h | 6296 | FIT |
| Lab 24-09.e | break-even repair time | 0.5 | h |

- Part 1: the margin falls to 2 dB when the optical segment's $Q$ reaches 5.61, even though each host channel alone has $Q$ = 10.
- Part 2: 32 lanes (UHP) and 64 lanes (SHP) with binary splitting, far more than the four per laser that NVIDIA describes; the difference is headroom for unmodelled losses and a smaller blast radius.
- Part 3: the simulated fraction of zero-failure tests lands within about ±0.002 of 0.0500, confirming that the rule-of-three rate is the one for which "no failures" happens only 5% of the time. One and two failures raise the bound to 4,744 and 6,296 FIT.
- Part 4: break-even at 0.5 h; with a 24 h switch replacement, the CPO port loses 48 times as many port-hours.

## Discussion

1. Why does the optical segment dominate Part 1's budget?

   <details><summary>Answer</summary>

   Its $1/Q^2$ term is the largest: at $Q$ = 5.61 it contributes 0.032 against 0.01 from each host channel. Improving the worst segment pays most, which is why LPO's feasibility depends on the optics' own linearity and noise.

   </details>

2. Why does a reliability engineer prefer a test that sees a few failures to one that sees none?

   <details><summary>Answer</summary>

   A zero-failure test only bounds the rate from above; it cannot tell a 300 FIT part from a 3 FIT one. Observed failures give an estimate of the rate itself (and of the failure mechanism), at the cost of a somewhat higher upper bound for the same exposure.

   </details>

## Optional hardware

None needed. Operators with fleet data can apply Part 3's chi-square bounds to their own transceiver failure logs, using total installed device-hours and recorded failures.
