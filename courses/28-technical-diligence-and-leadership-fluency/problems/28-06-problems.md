# Problems 28-06 · Red Flags and Green Flags

Chapter: [28-06](../chapters/28-06-red-and-green-flags.md) · Worked solutions: [28-06 solutions](../solutions/28-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Sensitivities, false-positive rates, base rates, attrition rates and financial parameters are assumed unless a source is cited. Flags are independent given the truth unless the problem says otherwise. $\text{LR}^+ = s/f$ and $\text{LR}^- = (1 - s)/(1 - f)$.

---

## Problems

### Problem 28-06.1 [A]

**Weigh the signal.** For each observation, say whether it is a red flag, a green flag or weak evidence either way, and what evidence would settle it:

- (a) The last tape-out slipped once, by six weeks.
- (b) The CEO answers every technical question; the engineers present say little.
- (c) Two customers ran the target's benchmarks on their own systems and matched the claims within 5%.
- (d) Three senior designers left in the last quarter.
- (e) A leading-edge product depends on one foundry and one packaging house.

### Problem 28-06.2 [B]

**A sharper flag.** A flag appears in 50% of troubled and 5% of healthy programs; the base rate of trouble is 30%. Find its positive and negative likelihood ratios, and the posterior odds and probability of trouble when it is present and when it is absent.

### Problem 28-06.3 [B]

**A longer checklist.** A checklist has 40 independent flags, each appearing in 2.5% of healthy companies. Find the probability that a healthy company shows at least one, the expected number, the probability of two or more, and the exponential approximation $1 - e^{-nf}$ to the first.

### Problem 28-06.4 [B]

**Choosing thresholds.** For Example 28-06.2's checklist (25 flags; 4% healthy, 30% troubled), find the sensitivity, false-positive rate and likelihood ratio of "two or more flags" and of "five or more flags". Which would you use to trigger deeper diligence, and which to recommend walking away?

### Problem 28-06.5 [B]

**Three architects.** Three key architects each leave with probability 15% a year (independent). Find the probability of losing at least one within one year and within three years, and the three-year figure if retention halves the rate.

### Problem 28-06.6 [A]

**Concentration.** A target's six customers have revenue shares of 30%, 25%, 15%, 10%, 10% and 10%. Find the HHI, the effective number of customers, and the revenue lost if the two largest leave.

### Problem 28-06.7 [B]

**Another funnel.** A target claims a $120M pipeline from 60 design wins at $2M lifetime revenue each. Assume 35% reach production, revenue arrives evenly over years 1 to 3, and the discount rate is 10%. Find the average discount factor, the risk-adjusted undiscounted revenue, its present value and the ratio of the claim to it.

### Problem 28-06.8 [B]

**Shared causes.** The prior probability of trouble is 40%. Two red flags have likelihood ratios 4 and 2; a green flag has 0.5. Find the posterior if all three are independent, and if the second red flag reports the same underlying fact as the first.

### Problem 28-06.9 [B]

**Three for three.** A target says its last three chips all reached production on first silicon. Find the probability of that record by chance if each project independently succeeds with probability 14% (the 2024 survey rate [R-621]), 30% (the historical rate) and 5% (the 2026 rate [R-321]). What share of 2024 projects needed four or more spins [R-645]? What would you ask?

### Problem 28-06.10 [B]

**Verification staffing.** A target has 40 design and 15 verification engineers. Find its verification-to-design ratio, the verification hires needed to reach the industry's reported one-to-one peak ratio [R-651], and their annual cost at an assumed \$250k fully loaded each. Is the comparison like for like?

### Problem 28-06.11 [A]

**Schedule credibility.** A team's last three projects took 25%, 40% and 30% longer than planned. Its new plan is 18 months. Find the mean overrun and the duration it implies for the new plan if the team's history repeats.

### Problem 28-06.12 [C]

**Four derivations.**

- (a) Derive the posterior odds of trouble when a flag is present and when it is absent, from Bayes' rule.
- (b) Derive $P(\ge 1) = 1 - (1 - f)^n$ for $n$ independent flags, and show that it is approximately $1 - e^{-nf}$ for small $f$.
- (c) Show that $\text{HHI} = 1/N$ for $N$ equal customers and that $\text{HHI} \ge 1/N$ for any $N$ shares that sum to 1.
- (d) Show that the likelihood ratio of "$K \ge k$" for binomial counts is $P(K \ge k; n, s)/P(K \ge k; n, f)$, and explain why it rises with $k$ when $s > f$.
- (e) Show that the likelihood ratio of observing *exactly* $k$ of $n$ independent flags is $(\text{LR}^+)^k(\text{LR}^-)^{n - k}$, and evaluate it for Example 28-06.2's checklist at $k = 2$. Why is it below 1?

### Problem 28-06.13 [C]

**Two flags that are not independent.** Flag $F_1$ (a slipped tape-out) appears in 60% of troubled and 20% of healthy targets. Flag $F_2$ (a revised revenue ramp) is more likely when $F_1$ is present: among targets showing $F_1$ it appears in 90% of troubled and 60% of healthy ones; among those without $F_1$, in 20% and 5% (all assumed). Both flags are present and the prior is 25%. Find (a) $\text{LR}(F_1)$, the marginal $\text{LR}(F_2)$ and the correct joint ratio $\text{LR}(F_1)\,\text{LR}(F_2 \mid F_1)$; (b) the posterior with the correct joint ratio, with the two ratios wrongly multiplied as if independent, and with only the stronger flag counted. Which shortcut is closer here, and why?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Flags as tests; likelihood ratios | 1, 2, 12 |
| 2. False alarms, thresholds and observed counts | 3, 4, 12 |
| 3. Technical, organizational and commercial flags | 1, 9, 10, 11 |
| 4. Key-person risk, concentration and funnels | 5, 6, 7, 12 |
| 5. Combining flags without double-counting | 8, 13 |
