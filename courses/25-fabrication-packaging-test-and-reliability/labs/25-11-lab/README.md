# Lab 25-11 · Test Cost, Burn-In and Guard Bands

**Objective.** Price multisite testing, size a burn-in against a weak subpopulation and check it by Monte Carlo, set a guard band for an escape target, and see how process spread changes bin revenue.

**Chapter:** [25-11 · Test](../../chapters/25-11-test-ate-sort-burn-in.md)

## Background

§3.2 gave the cost per die $r(T_N + t_i)/N$ with $T_N = T_1[1 + (N - 1)(1 - \eta)]$. §3.4 modelled infant mortality as a weak fraction with Weibull shape $\beta < 1$, removed by a burn-in of $AF\,t_b$ use-equivalent hours. §3.3 defined escapes and overkill at a guard-banded limit, and §3.5 bin fractions and revenue.

## Files

- `testcost.py`: multisite time and cost, the weak-population burn-in model with a Monte Carlo check, bin fractions and revenue, and escapes and overkill by integration and Monte Carlo.
- `25-11-test-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Four sites or eight?** (notebook). With Example 25-11.1's tester rate, test time and index time, *predict* the eight-site multisite efficiency at which eight sites cost the same per die as four sites at 90%, then solve for it and plot cost per die against sites for several efficiencies.

**Part 2 · Burn-in** (notebook). For a 1% weak population with Weibull shape 0.3 and scale 100 h, *predict* the fraction removed by 1,200 use-equivalent hours, then compute it and confirm by Monte Carlo.

**Part 3 · Guard band** (notebook). For Example 25-11.6's population and tester, *predict* the guard band for 100 ppm escapes, then solve for it, confirm escapes and overkill by Monte Carlo at 40 MHz, and plot both against guard band.

**Part 4 · Process spread** (notebook). *Predict* how bin revenue changes when σ falls from 0.15 to 0.10 GHz, then compute it.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-11.a | eight-site efficiency for equal cost | 0.75 | |
| Lab 25-11.b | weak fraction removed, beta 0.3 | 0.878 | |
| Lab 25-11.c | guard band for 100 ppm escapes | 50.4 | MHz |
| Lab 25-11.d | bin revenue at sigma 0.10 GHz | 345 | $ |

The Monte Carlo burn-in fraction agrees with the closed form within 0.5%, and the simulated escapes and overkill at 40 MHz agree with the integrals within 5% (escapes) and 1% (overkill).

## Discussion

1. Part 1: eight sites pay only if efficiency stays above 75%. What usually limits efficiency on analog or RF parts?
2. Part 2: why does a shallow weak population make burn-in so expensive, and what else could reduce it?
3. Part 3: if tester error fell from 20 to 10 MHz, how would the guard band and overkill for 100 ppm change?
4. Part 4: what does the revenue gain from tighter process control imply about the value of a fab's process-control investment to its customers?

## Optional hardware

None needed. If you have access to a microcontroller board, measure the maximum clock frequency of several boards with a simple timing-loop test; the spread you see is the raw material of speed binning.
