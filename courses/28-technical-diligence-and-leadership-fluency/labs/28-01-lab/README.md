# Lab 28-01 · Scorecards, Evidence and the Value of a Test

**Objective.** Use small decision models to see when a scorecard's ranking can be trusted, how much a piece of evidence should move belief, what a spin plan really implies, and what an independent test of a target's silicon is worth.

**Chapter:** [28-01 · A Framework for Evaluating a Chip Company's Technology](../../chapters/28-01-technology-evaluation-framework.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.2: weighted arithmetic and geometric scores, score variance $\sum w_i^2\sigma_i^2$ (plus correlation terms) and the probability of rank reversal $\Phi(-\mu_D/\sigma_D)$.
- §3.3: Bayes' rule in odds form, $O(T \mid E) = O(T)\prod_k\Lambda_k$.
- §3.4: spins beyond plan from the 2024 spin distribution, milestone chains and earn-out values.
- §3.5: EVPI and EVSI for a buy-or-pass decision.

## Files

- `dilmodel.py`: the models and the chapter's cases.
  - Scorecards, gates, score variance and rank reversal (analytic and Monte Carlo).
  - Posterior probability from likelihood ratios, and the ratio a target probability needs.
  - Spin statistics, milestone chains and earn-out present values.
  - EVPI and EVSI.
- `28-01-diligence-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · What a deep-dive changes** (notebook). *Predict* the probability that target B is ahead in Example 28-01.2 if an architecture deep-dive revises A's architecture score from 4.5 to 4.0, with a standard deviation of 0.3. Then plot the probability against A's revised architecture score from 3.0 to 5.0.

**Part 2 · One more signal** (notebook). *Predict* the posterior of Example 28-01.3 if a fourth, independent signal arrives: a second customer ends its evaluation (likelihood ratio 0.25). Then plot posterior against prior for likelihood ratios of 0.25, 0.5, 2, 4 and 16.

**Part 3 · A three-spin plan** (notebook). *Predict* Example 28-01.4's expected delay and extra mask cost (4 months and \$25 million per spin) if the plan budgets three spins. Then sample 10,000 projects from the 2024 distribution and plot a histogram of their delays beyond the original two-spin plan; the third budgeted spin covers the first 4 months of that delay.

**Part 4 · A less specific test** (notebook). *Predict* the EVSI of Example 28-01.6's test if its specificity falls from 0.9 to 0.7, with the sensitivity still 0.8. Then plot EVSI against sensitivity for specificities of 0.7, 0.8, 0.9 and 0.99.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-01.a | A's revised arithmetic score | 3.575 | — |
| Lab 28-01.a1 | standard deviation of the difference | 0.249 | — |
| Lab 28-01.a3 | A's deficit after the deep-dive | 0.075 | — |
| Lab 28-01.a2 | probability B is ahead | 61.8 | % |
| Lab 28-01.b | posterior with the fourth signal | 33.3 | % |
| Lab 28-01.c | probability a three-spin plan holds | 69.1 | % |
| Lab 28-01.c1 | expected spins beyond plan | 0.495 | spins |
| Lab 28-01.c2 | expected delay | 1.98 | months |
| Lab 28-01.c3 | expected extra mask cost | 12.4 | million \$ |
| Lab 28-01.d | probability of a pass | 0.50 | — |
| Lab 28-01.d1 | P(works given pass) | 0.64 | — |
| Lab 28-01.d2 | value of buying after a pass | 248 | million \$ |
| Lab 28-01.d3 | EVSI | 44.0 | million \$ |

## Discussion

1. The deep-dive lowers A's score to **3.575**, so A now trails B by 0.075; with less uncertainty about architecture the standard deviation of the difference falls to **0.249**, and the probability that B is ahead rises to **61.8**%. A deep-dive is valuable because it moves the mean as well as narrowing the spread.
2. A second customer walking away halves the odds twice over: the posterior falls from 66.7% to **33.3**%. Negative evidence from a party with its own incentives (a customer evaluating for its own product) usually carries a strong likelihood ratio.
3. With three spins budgeted the plan holds **69.1**% of the time; the expected overrun falls to **0.495** spins, **1.98** months and **12.4** million dollars. The histogram is lumpy, not bell-shaped: most projects overrun by zero, one or two whole spins, so a mean delay hides a large chance of a long one.
4. At a specificity of 0.7 the test passes **0.50** of targets, a pass raises the probability of working technology only to **0.64**, and buying after a pass is worth **248** million dollars; the EVSI falls from 68 to **44.0** million dollars. False passes are costly here because a pass leads to buying.

## Optional hardware

None. For a real exercise, take a public chip company's investor presentation and score it on the seven dimensions with standard deviations that reflect how much of each score rests on the presentation alone; then list the three diligence steps with the highest contribution to the variance.
