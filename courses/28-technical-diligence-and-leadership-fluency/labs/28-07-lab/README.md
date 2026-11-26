# Lab 28-07 · Track Records, Schedules and Bench Depth

**Objective.** Use small models to see how a team's track record should move an estimate of its success rate, how its schedule history forecasts its next project, how bench depth protects a capability, and when a retention package pays for itself.

**Chapter:** [28-07 · Evaluating Engineering Teams](../../chapters/28-07-evaluating-engineering-teams.md)

## Background

The lab uses the chapter's models with its assumed parameters:

- §3.1: a $\text{Beta}(\alpha_0, \beta_0)$ prior updated by $s$ successes in $n$ projects, with mean $(\alpha_0 + s)/(n_0 + n)$.
- §3.2: lognormal overruns with the plug-in $P(\text{on time}) = \Phi(-\mu/s_{\ln})$ and $T_{90} = T_{\text{plan}}e^{\mu + z_{0.9}s_{\ln}}$ (overconfident for a short record; §3.2 gives the $t$ predictive form).
- §3.3: capability loss $q^k$, or $c + (1 - c)q'^k$ with group departures.
- §3.6: retained value $NV\rho$.

## Files

- `teameval.py`: the models.
- `28-07-team-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Shrinkage** (notebook). *Predict* the posterior mean for a team with 5 successes in 5 projects (prior mean 14%, weight 10). Then plot the posterior mean and 90% interval against the number of projects for a team that always succeeds and one that succeeds half the time.

**Part 2 · Schedule forecast** (notebook). *Predict* the P90 duration if Example 28-07.2's team plans 24 months. Then plot the distribution of its duration.

**Part 3 · Bench depth over time** (notebook). *Predict* the probability of losing a capability held by two people over three years at 12% a year. Then plot capability loss against time for one, two and three owners, with and without a 5% group-event probability.

**Part 4 · Retention** (notebook). *Predict* the break-even cost of Example 28-07.5's retention package. Then plot the package's net value against its cost for retention gains of 10, 15 and 20 points.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 28-07.a | posterior mean, 5 of 5 | 42.7 | % |
| Lab 28-07.b | plug-in P90 duration for a 24-month plan | 34.4 | months |
| Lab 28-07.c | two owners, three years | 10.1 | % |
| Lab 28-07.d | break-even package cost | 13.5 | $M |

## Discussion

1. Five successes in five projects lift the estimate from 14% to **42.7**%: impressive, but far from the raw 100%, because five projects are little evidence against a low base rate. Each further success adds less.
2. With a 24-month plan the plug-in P90 is **34.4** months, and the $t$ predictive P90 is later still because four projects leave the spread uncertain. A deal model that schedules milestone payments at 24 months is betting against the team's own history.
3. Two owners cut the three-year loss probability to **10.1**%, but a 5% chance of the group leaving together sets a floor that no amount of redundancy inside the team removes.
4. The package breaks even at **13.5** $M. Concentrating it on the engineers whose departure would cost the most raises its value per dollar.

## Optional hardware

None. As an exercise, collect the plan and actual durations of five projects you know (from any industry), fit $\mu$ and $\sigma$, and compare the P90 with the plans now on the table.
