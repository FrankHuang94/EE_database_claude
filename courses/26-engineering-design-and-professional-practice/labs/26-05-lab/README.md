# Lab 26-05 · Schedules, Respins and When to Tape Out

**Objective.** Check the normal approximation to a tape-out schedule with a Monte Carlo, see how learning between spins changes the expected number of tape-outs, and map the expected cost of a tape-out decision against verification time, with and without emulation.

**Chapter:** [26-05 · Schedule and Risk: Why Respins Happen](../../chapters/26-05-schedule-and-respin-risk.md)

## Background

§3.2 derived PERT estimates, path statistics and merge bias, and noted that the beta-PERT distribution is usually wider than $(b - a)/6$ suggests. §3.3 derived $E[N] = \sum_k P(N \ge k)$ for the number of tape-outs. §3.6 built the bug-discovery model $\lambda(t) = \phi N_0e^{-t/\tau}$ and the expected cost $f(t) = c_wt + C_r(1 - e^{-\lambda})$, with its maximum and minimum where $\lambda e^{-\lambda} = c_w\tau/C_r$.

## Files

- `risk.py`: PERT means and standard deviations, path statistics, the chance of meeting a date and merge bias, a Monte Carlo schedule with beta-PERT tasks; expected tape-outs and their distribution; ECO costs; expected monetary value and the best mitigations under a budget; escapes, respin probability, expected cost and the optimal tape-out time.
- `26-05-schedule-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Monte Carlo schedule** (notebook). *Predict* whether sampling Example 26-05.2's tasks from their beta-PERT distributions gives a higher or lower chance of tape-out by week 20 than the normal approximation's 0.826. Then run 200,000 trials, plot the histogram of the tape-out week and find the week with a 90% chance.

**Part 2 · Learning between spins** (notebook). *Predict* the expected number of tape-outs in Example 26-05.1 if A0's success probability doubles to 0.50, with later spins unchanged. Then plot $E[N]$ against $q_1$ from 0 to 1.

**Part 3 · The cost of stopping** (notebook). *Predict* the shape of Example 26-05.5's expected cost from 0 to 30 weeks of verification, including its value at 24 weeks. Then plot it, with and without emulation (Figure 1 of the chapter).

**Part 4 · What emulation must deliver** (notebook). *Predict* how far emulation must shorten the mean discovery time $\tau$ (from 4 weeks) to repay its \$3 M price. Then plot the minimum expected cost against $\tau$ and find the break-even.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 26-05.a | P(tape-out by week 20), beta-PERT | 0.77 | |
| Lab 26-05.a1 | 90% date, beta-PERT | 21 | weeks |
| Lab 26-05.b | expected tape-outs at q1 = 0.50 | 1.66 | |
| Lab 26-05.b1 | tape-outs saved | 0.33 | |
| Lab 26-05.b2 | weeks saved | 5.9 | weeks |
| Lab 26-05.c | expected cost at 24 weeks | 37.0 | $M |
| Lab 26-05.d | break-even discovery time | 3.51 | weeks |
| Lab 26-05.d1 | required speed-up | 12 | % |

## Discussion

1. The Monte Carlo gives 0.77 against the normal approximation's 0.826, and needs about 21 weeks for 90% confidence against 20.7. The beta-PERT tasks are wider than $(b - a)/6$ implies, and skewed, which the normal approximation ignores; for a committed date, simulate.
2. Doubling A0's success probability lowers the expected tape-outs from 1.99 to 1.66, worth **0.33** of a tape-out (**5.9** weeks at 18 weeks a spin).
3. The cost curve starts at $40 M (respin nearly certain), rises to a ridge near 5 weeks, falls to its minimum at 16.1 weeks and then rises slowly as the weekly cost dominates ($37.0 M at 24 weeks). Stopping on the ridge is the worst time to stop short of the optimum.
4. Emulation at \$3 M pays only if it shortens $\tau$ below 3.51 weeks, a **12**% faster discovery; the assumed 2.5 weeks clears that easily, which is why most large SoC programs use it.

## Optional hardware

None needed. If you manage a project, record the bugs found per week in your own tracker for a month and fit $N_0$ and $\tau$; the fitted curve is what a tape-out review should see.
