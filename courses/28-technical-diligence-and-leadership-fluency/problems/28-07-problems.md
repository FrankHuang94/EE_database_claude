# Problems 28-07 · Evaluating Engineering Teams

Chapter: [28-07](../chapters/28-07-evaluating-engineering-teams.md) · Worked solutions: [28-07 solutions](../solutions/28-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Base rates, prior weights, departure rates, scores and financial values are assumed unless a source is cited. Unless stated otherwise, the prior for first-silicon success is $\text{Beta}(1.4, 8.6)$ (mean 14% [R-621], weight 10). Schedule overruns are lognormal; standard deviations of log-ratios use $n - 1$.

---

## Problems

### Problem 28-07.1 [A]

**Read the room.** Classify each answer as strong, partial or evasive, and say what artifact would confirm the strong ones:

- (a) To T1: "Our B0 respin was a clock-domain-crossing bug in the DMA engine that our lint flow waived; we now require sign-off on every waiver, and the C0 tape-out had zero CDC escapes."
- (b) To T2: "Everyone on the team can work on any block."
- (c) To T3: "We were late on the last one, but that was the foundry."
- (d) To T6: "About 45% of designer time, from our time-tracking, plus 18 dedicated verification engineers."

### Problem 28-07.2 [B]

**Two records.** Find the posterior mean and the weight on the team's own record for a team with 1 success in 3 projects and for one with 6 in 8.

### Problem 28-07.3 [B]

**A wider interval.** Find the 95% credible interval (2.5th to 97.5th percentiles) of Example 28-07.1's posterior, $\text{Beta}(5.4, 9.6)$.

### Problem 28-07.4 [B]

**Another schedule.** A team's last three projects took 1.15, 1.35 and 1.50 times their plans. Its new plan is 24 months. Find the geometric mean overrun, the expected duration, the standard deviation of the log-ratios and the probability of meeting the plan.

### Problem 28-07.5 [B]

**Bench depth at 15%.** Each engineer leaves with probability 15% a year. Find the probability of losing a capability with one, two and three owners over one year and over three years.

### Problem 28-07.6 [B]

**Single points of failure.** Four capabilities each have a single owner; departures are 12% a year. Find the probability of losing at least one capability within two years.

### Problem 28-07.7 [B]

**A hidden weakness.** Weights 0.30, 0.25, 0.25 and 0.20; scores 5, 4, 1 and 4; gate: no score below 2. Find the weighted and geometric scores and say whether the gate passes.

### Problem 28-07.8 [B]

**A smaller team.** An acquirer values each of 40 engineers at $1.2M. Two-year retention is 65% without a package and 80% with one. Find the expected retained value each way, the gain, and the retention gain per $1M of package cost needed to break even.

### Problem 28-07.9 [A]

**Regression capacity.** A plan needs 3 million runs of 15 CPU-minutes each on 1,000 cores at 75% utilization. Find the wall-clock days for one full pass.

### Problem 28-07.10 [B]

**Effort, not heads.** A team has 40 design and 15 verification engineers; designers spend 49% of their time on verification, as in the 2022 study [R-651]. Find the verification effort in full-time equivalents, the design effort, and their ratio.

### Problem 28-07.11 [A]

**Channels.** A team grows from 20 to 30 people with every pair coordinating. Find the pairwise channels before and after and their ratio [R-650].

### Problem 28-07.12 [C]

**Three derivations.**

- (a) Show that a $\text{Beta}(\alpha_0, \beta_0)$ prior with a binomial likelihood ($s$ successes in $n$) gives a $\text{Beta}(\alpha_0 + s, \beta_0 + n - s)$ posterior, and write its mean as a weighted average of the prior mean and $s/n$.
- (b) For lognormal overrun ratios with log-mean $\mu$ and log-standard deviation $\sigma$, derive the probability of meeting the plan and the P90 duration.
- (c) Suppose that with probability $c$ a group event takes all $k$ owners of a capability at once, and otherwise each leaves independently with probability $q'$. Derive the probability of losing the capability, and evaluate it for $c = 0.05$, $q' = 0.2$ and $k = 1, 2, 3$. What floor does $c$ put under the benefit of redundancy?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Track records and shrinkage | 2, 3, 12 |
| 2. Schedule calibration | 4, 12 |
| 3. Composition and bench depth | 5, 6, 10, 11, 12 |
| 4. Tooling, process and interview signals | 1, 9 |
| 5. Scorecards and retention value | 7, 8 |
