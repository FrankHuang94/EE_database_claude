# Lab 26-01 · Budgets, Flow-Down and Decisions

**Objective.** Check an error budget by Monte Carlo, including what happens when contributions are not Gaussian; flow a battery-life requirement down to a display-time budget; test how robust the value of a requirements review is to the escalation factors; and sweep a decision matrix's weights.

**Chapter:** [26-01 · Requirements, Specifications and the Design Process](../../chapters/26-01-requirements-and-specifications.md)

## Background

§3.3 derived duty-cycle averages, worst-case and RSS stacking, the effect of correlation and the out-of-spec fraction $P_{out}$ of a Gaussian total. §3.6 built the phase-by-phase escalation model, with total cost $C = N[p_1c_1 + (1 - p_1)\bar c_{down}]$. §3.7 derived the tie weight of a decision matrix when one weight is swept and the others are rescaled in proportion.

## Files

- `reqs.py`: duty-cycle averages and battery life; worst-case, RSS and correlated stacking; $P_{out}$; a Monte Carlo of a summed budget (Gaussian or uniform contributions, with optional correlated groups); the expected cost of traceability gaps; the defect-flow model; weighted scores, weight sweeps and tie weights.
- `26-01-requirements-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Does the distribution matter?** (notebook). Example 26-01.3's six contributions have ±bounds of 0.40, 0.35, 0.30, 0.25, 0.20 and 0.30% against a ±1.0% limit. *Predict* whether the out-of-spec fraction changes if each contribution is uniform with that bound as its half-width (rather than Gaussian with the bound at 3σ). Then run the Monte Carlo, compute the total's standard deviation (a uniform of half-width $b$ has σ = $b/\sqrt3$), and compare the simulated fraction with a Gaussian of the same σ.

**Part 2 · Display time** (notebook). *Predict* the display duty that gives exactly 168 h with no margin under Example 26-01.2's profile, then sweep the display duty from 0 to 6% and plot battery life against display minutes per day.

**Part 3 · How robust is the review's value?** (notebook). *Predict* the range of Example 26-01.5's saving when each escalation factor is drawn at random (log-uniformly) from its NASA range: design 3–8, build 7–16, test 21–78, field 29–1,500. Compute the saving at the two ends of the ranges, then sample 10,000 sets of factors and plot the distribution of the saving.

**Part 4 · Decision sweep** (notebook). *Predict* the capability weight at which option B overtakes option A in Example 26-01.6, then sweep the weight from 0 to 1, plot the three scores and mark the tie points.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 26-01.a | out of spec, uniform contributions | 1.77 | % |
| Lab 26-01.a1 | sigma of the total, uniform contributions | 0.434 | % |
| Lab 26-01.a2 | Gaussian with that sigma | 2.12 | % |
| Lab 26-01.a3 | uniform sigma per unit half-width | 0.577 | |
| Lab 26-01.b | display duty for exactly 168 h | 3.51 | % |
| Lab 26-01.b1 | display minutes per day | 50.6 | min |
| Lab 26-01.b2 | more than with margin | 8.0 | min |
| Lab 26-01.c | saving at the low ends of the ranges | 465 | units |
| Lab 26-01.c1 | saving at the high ends of the ranges | 1.11e4 | units |
| Lab 26-01.c3 | saving at the high ends, exact | 11069 | units |
| Lab 26-01.c2 | ratio of the two | 23.8 | |

## Discussion

1. The uniform case fails far more often (1.77% against 66 ppm) because the same "±bound" now describes a much wider spread: σ = $b/\sqrt3$ = **0.577**$b$ against $b/3$. A bound is meaningless until its distribution and confidence level are stated. The exact tail is somewhat thinner than a Gaussian of the same σ, because a sum of six uniforms has no tail beyond the worst case (here ±1.80%).
2. The display budget without margin (about 51 min a day) is only **8.0** minutes more than with 10% margin (42.6 min). Margin is cheap to hold early and expensive to recover late.
3. Across the NASA ranges the saving varies by a factor of **23.8**, from 465 to **11069** units, but it is positive and large everywhere: the decision to hold a formal review does not depend on knowing the factors precisely, even though the dollar value does.
4. The decision sweep turns a scoring argument into a single question: how much does capability matter to the customer? (§3.7)

## Optional hardware

Measure a real budget: with a USB power monitor on a development board or a wearable, log the current through a day of use, estimate the duty fraction and current of each mode from the log, and compare the measured battery life with the duty-cycle prediction. The gap between the two is a lesson in how use profiles are validated.
