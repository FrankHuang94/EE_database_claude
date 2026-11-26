# Lab 26-07 · Putting Numbers on Safety Claims

**Objective.** Use the probability behind safety arguments: how a small per-unit risk becomes a near-certainty across a fleet, why redundant protections fail together, and how much failure-free evidence a safety claim needs.

**Chapter:** [26-07 · Engineering Ethics and Professional Responsibility](../../chapters/26-07-engineering-ethics.md)

## Background

§3.3 derived the fleet probability $1 - (1 - p)^N$, the expected failures from a FIT rate, the beta-factor model of common-cause failure, and the zero-failure upper bound on a failure rate, $\lambda_U = -\ln(1 - C)/T$ (with $k$ failures, $\chi^2_{C,\,2k+2}/(2T)$).

## Files

- `safety.py`: fleet probability and expected events, fleet failures from a FIT rate, the beta-factor model, upper confidence bounds and the hours needed to demonstrate a rate, total processing performance and performance density, and protection-term dates.
- `26-07-safety-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Rare per unit, common per fleet** (notebook). *Predict* the fleet size at which a failure with probability one in a million per unit has an even chance of happening at least once. Then plot the fleet probability against fleet size for $p = 10^{-6}$ and $10^{-8}$.

**Part 2 · Common cause** (notebook). *Predict* the beta factor at which the common-cause term equals the independent term for two channels that each fail on demand with $p = 10^{-3}$. Then plot the probability that both fail against $\beta$ from $10^{-5}$ to 0.1.

**Part 3 · Proving a rate** (notebook). *Predict* how many failure-free device-hours it takes to show a rate below 1 FIT with 95% confidence. Then plot the hours needed against the target rate, for 90% and 95% confidence.

**Part 4 · When failures occur** (notebook). *Predict* how the 95% upper bound on the rate grows when 1, 2 or 3 failures are seen in $10^9$ device-hours instead of none. Then compute the bounds.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 26-07.a | fleet for a 50% chance at p = 1e-6 | 6.93e5 | units |
| Lab 26-07.b | beta where the terms are equal | 1.00e-3 | |
| Lab 26-07.b1 | ratio to independence at beta = 0.001 | 2.0 | |
| Lab 26-07.c | hours to show 1 FIT at 95% | 3.00e9 | hours |
| Lab 26-07.d | bound, 0 failures | 3.00 | FIT |
| Lab 26-07.d1 | bound, 1 failure | 4.74 | FIT |
| Lab 26-07.d2 | bound, 2 failures | 6.30 | FIT |
| Lab 26-07.d3 | bound, 3 failures | 7.75 | FIT |
| Lab 26-07.d4 | smallest step | 1.46 | FIT |
| Lab 26-07.d5 | largest step | 1.75 | FIT |

## Discussion

1. A one-in-a-million risk per unit is more likely than not to occur somewhere in a fleet of 693,000 units, a modest production volume. Safety arguments must be made per fleet, not per unit.
2. Common cause dominates as soon as $\beta$ exceeds about $p$: two channels with $p = 10^{-3}$ and only 0.1% of their failures in common are already **2.0** times as likely to fail together as independence predicts. Diversity (different designs, different physics, as a hardware interlock alongside software) is what keeps $\beta$ small.
3. Showing 1 FIT with confidence needs three billion failure-free device-hours, more than any test programme can run directly; field data, accelerated testing (25-09, 25-10) and design arguments carry the rest of the case.
4. Each failure observed raises the bound by **1.46** to **1.75** FIT here: a handful of field failures quickly rules out an ambitious claim.

## Optional hardware

None needed. Find a published FIT figure for a part you know (25-09) and compute how many device-hours of field data it would take to confirm it.
