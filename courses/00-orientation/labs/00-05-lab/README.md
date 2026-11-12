# Lab 00-05 · A Chip-Project Schedule-Risk Simulator

**Chapter:** [00-05](../../chapters/00-05-how-chip-companies-are-organized.md) · **Notebook:** [00-05-schedule-risk.ipynb](00-05-schedule-risk.ipynb) · **Time:** about 45 minutes

## Objective

1. See how right-skewed task durations make "most-likely" plans late.
2. Quantify the schedule effect of a possible respin.
3. See how first-silicon success depends on the number of blocks and on per-block quality.

## Background

Chapter §3.4–3.6 and Examples 00-05.4–5.

- Each phase duration is modeled as triangular (min, most likely, max), with mean $(a + m + b)/3$.
- The total is the sum of the phases; the simulator samples it (Monte Carlo).
- First-silicon success with $n$ independent blocks is $p^n$.

## Procedure

1. Run all cells. Check that the simulated mean and percentiles for Example 00-05.5 match the chapter: 58.0 weeks mean, 11.4% chance of meeting 52 weeks, 80th percentile 62.4 weeks.
2. **Predict, then run:** add a 30% chance of a metal-only fix taking 6–10 weeks (triangular, most likely 8). Predict the new mean and the new 80th percentile before running.
3. Enter your own estimates for a project you know, from work or from a public product announcement. Compare the committed date with the simulator's 50th and 80th percentiles.
4. In the last cell, find the per-block quality needed for a 50% chance of first-silicon success with 100 blocks.

## Expected results

| Exercise | Expected |
|---|---|
| Example 00-05.5 baseline | mean 58.0 weeks; P(≤ 52) ≈ 11.4%; 80th percentile ≈ 62.4 weeks |
| With a 30% chance of a 6–10-week metal fix | mean $58.0 + 0.3 \times 8 = 60.4$ weeks; 80th percentile ≈ 65.7 weeks |
| Per-block quality for 50% success with 100 blocks | $0.5^{1/100} = 0.99309$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 00-05.1 | mean with 30 % metal-fix risk | 60.4 | weeks |
| Lab 00-05.2 | 80th percentile with 30 % metal-fix risk | 65.7 | weeks |
| Lab 00-05.3 | per-block quality for 50 % success, 100 blocks | 0.99309 | — |

## Discussion questions

1. Why does adding a 30%-likely, 8-week fix raise the 80th percentile by *more* than its contribution to the mean?
2. How would correlated risks (for example, one late IP block delaying both verification and physical design) change the distribution compared with independent phases?
3. How would you present the 80th-percentile date to a sales team that wants the earliest possible date?

## Optional hardware version

None. Pick a recently announced chip from public news, note its announced tapeout and production dates, and compare the gap with the fab cycle times in [R-020](../../../../reference/research-log.md#r-020--fab-cycle-time-and-maskeuv-layer-counts).
