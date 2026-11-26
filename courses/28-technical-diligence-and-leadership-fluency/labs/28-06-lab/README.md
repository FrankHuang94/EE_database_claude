# Lab 28-06 · Flags, False Alarms and Funnels

**Objective.** Use small models to see how a checklist's false alarms grow with its length, how a flag-count threshold separates healthy from troubled companies, how key-person risk accumulates over an integration, and how much a design-win pipeline shrinks when it is risk-adjusted.

**Chapter:** [28-06 · Red Flags and Green Flags](../../chapters/28-06-red-and-green-flags.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.1: a flag's likelihood ratios $s/f$ and $(1 - s)/(1 - f)$, and posterior odds.
- §3.2: false alarms $1 - (1 - f)^n$ and binomial flag counts.
- §3.4–3.5: key-person risk $1 - (1 - q)^{mt}$, HHI and the risk-adjusted funnel value.

## Files

- `flagmodel.py`: the models.
- `28-06-flag-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · False alarms** (notebook). *Predict* the probability that a healthy company shows at least one of 50 flags, each with a 3% false-positive rate. Then plot that probability against the number of flags for false-positive rates of 2%, 5% and 10%.

**Part 2 · Count thresholds** (notebook). For Example 28-06.2's checklist (25 flags; 4% healthy, 30% troubled), *predict* the smallest threshold whose likelihood ratio exceeds 100. Then tabulate sensitivity, false-positive rate and ratio for thresholds 1 to 8 and plot the two count distributions.

**Part 3 · Key-person risk over time** (notebook). *Predict* the probability of losing at least one of five key engineers within three years at 12% a year. Then plot it against time for 6%, 12% and 20% a year.

**Part 4 · The funnel** (notebook). *Predict* Example 28-06.5's risk-adjusted value if only 40% of wins reach production. Then plot the value against the conversion rate for discount rates of 8%, 12% and 16%.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-06.a | at least one false alarm, 50 flags at 3% | 78.2 | % |
| Lab 28-06.b | smallest threshold with ratio above 100 | 5 | flags |
| Lab 28-06.b1 | sensitivity at that threshold | 91.0 | % |
| Lab 28-06.c | key-person loss in three years | 85.3 | % |
| Lab 28-06.d | funnel value at 40% conversion | 34.3 | $M |

## Discussion

1. Fifty flags at 3% give a healthy company a **78.2**% chance of at least one false alarm. Longer checklists find more real problems but make single flags nearly meaningless.
2. A threshold of **5** flags is the first with a likelihood ratio above 100, and it still catches **91.0**% of troubled companies, because the two count distributions barely overlap there. The independence assumption makes this look cleaner than reality; clustered flags blur the separation.
3. Over three years the chance of losing at least one of five key engineers reaches **85.3**%. Integration plans should assume departures and plan successors, not hope to avoid them.
4. At 40% conversion the funnel is worth **34.3** $M, under 30% of the $120M headline. The conversion rate is the single most valuable number to ask a target for.

## Optional hardware

None. As an exercise, write down sensitivities and false-positive rates for ten flags before your next diligence project, and record which flags appeared and how the deal turned out; after a few deals, compare your guesses with your own data.
