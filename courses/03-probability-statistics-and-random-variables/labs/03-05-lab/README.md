# Lab 03-05 · Estimation and Hypothesis Testing for Engineers

**Chapter:** [03-05](../../chapters/03-05-estimation-and-hypothesis-testing.md) · **Notebook:** [03-05-statistics.ipynb](03-05-statistics.ipynb) · **Time:** about 60 minutes

## Objective

1. Confirm by simulation why the sample variance divides by $n - 1$.
2. Measure the true coverage of z- and t-intervals for small and moderate samples.
3. Check the chi-square interval for noise power.
4. Trace the power curve of a counting test.
5. See how much an estimated Cpk scatters between studies.
6. Measure how well eight failures determine a Weibull shape.
7. Check that Poisson upper bounds on a failure rate cover the truth at least as often as promised.

## Background

Chapter sections 3.1–3.7 and Examples 03-05.1 to 03-05.7. Every statistical method makes a promise about long-run frequencies; this lab repeats each experiment thousands of times to check the promise. The seed is 2026.

## Procedure

1. Run all cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict the average of the divide-by-$n$ variance for $n = 5$.
3. **Part 2:** predict the coverage of a 1.96-multiplier interval with $s$ at $n = 5$.
4. **Part 4:** predict the power against a 20% lower rate.
5. **Part 6:** predict the scatter of γ̂ from eight-unit tests.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | variance estimators, $n = 5$ | divide by $n$: $(n - 1)/n = 0.8$ on average; divide by $n - 1$: 1; mean of $s$ about 0.94 |
| 2 | coverage of nominal 95% intervals | z-with-$s$: theory 0.8784 at $n = 5$ (seeded 0.8842) and 0.9403 at $n = 30$; t-intervals about 0.95 at both |
| 3 | chi-square interval, ν = 50 | coverage about 0.95 (seeded 0.9486); typical width 0.83 times the true power |
| 4 | power of the fleet test | 0.047 at the vendor's rate, 0.25 at 10% lower, 0.6602 at 20% lower, 0.94 at 30% lower |
| 5 | Cpk scatter, true 1.389 | standard deviation 0.20 for 30 parts (formula 0.1923) and 0.095 for 125 parts (formula 0.09310); estimates below 1.33 in about 35% and 25% of studies |
| 6 | Weibull shape from 8 failures, true 2.5 | median about 2.3, 5th–95th percentile about 1.3 to 4.2; Example 03-05.6 data give 2.498 |
| 7 | FIT bound coverage, true 150 FIT | 2.691 expected failures per test; the bound misses only when zero failures occur (probability 0.06784), so coverage is 0.9322, above the nominal 0.90 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 03-05.a | expected divide-by-n variance, n = 5 | 0.8 | — |
| Lab 03-05.b | coverage of z-with-s at n = 5 | 0.8784 | — |
| Lab 03-05.c | coverage of z-with-s at n = 30 | 0.9403 | — |
| Lab 03-05.d | power at a 20% lower rate | 0.6602 | — |
| Lab 03-05.e | Cpk standard error formula, n = 30 | 0.1923 | — |
| Lab 03-05.f | Cpk standard error formula, n = 125 | 0.09310 | — |
| Lab 03-05.g | expected failures at 150 FIT | 2.691 | — |
| Lab 03-05.h | probability of zero failures | 0.06784 | — |
| Lab 03-05.i | coverage of the 90% bound | 0.9322 | — |

## Discussion questions

1. Part 2 shows a 1.96-multiplier interval covering only 88% at $n = 5$. A characterization report quotes "mean ± 1.96 s/√n" from five parts. How would you restate its claim?
2. In Part 5, a supplier's 30-part study shows Cpk = 1.40 and a competitor's 125-part study shows 1.35. Which supplier has demonstrated more, and what would you ask each for?
3. Part 7 shows that discreteness makes Poisson bounds conservative. Why might a vendor prefer to report a 60% bound, and what should a customer do about it?

## Optional hardware version

Measure the offset voltage of 30 nominally identical op-amps (or the frequency of 30 crystal oscillators) with a bench meter. Compute the mean, standard deviation, a 95% t-interval for the mean, and the Cpk against the datasheet limits with its 95% lower bound. Compare with the datasheet's typical and maximum values, and decide whether your sample supports them.
