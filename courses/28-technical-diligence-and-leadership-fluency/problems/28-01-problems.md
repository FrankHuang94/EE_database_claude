# Problems 28-01 · A Framework for Evaluating a Chip Company's Technology

Chapter: [28-01](../chapters/28-01-technology-evaluation-framework.md) · Worked solutions: [28-01 solutions](../solutions/28-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All scores, probabilities and payoffs are assumed for teaching unless a source is cited. Scores use a 1–5 scale and weights sum to 1. Score errors are independent and normal unless a correlation is given. Evidence is conditionally independent unless stated otherwise. Money is in millions of dollars unless marked.

---

## Problems

### Problem 28-01.1 [A]

**Which dimension, and how strong?** For each item, name the dimension of §3.1 it tests and say whether it is strong or weak evidence, with a reason:

- (a) a freedom-to-operate opinion from outside counsel on the target's network-on-chip patents;
- (b) a slide claiming "10× the TOPS/W of a GPU";
- (c) a 2027 CoWoS allocation confirmed in writing by the packaging supplier;
- (d) the public release history and open-issue list of the target's compiler;
- (e) wafer-sort yield by lot for the B0 stepping;
- (f) the CTO's résumé.

### Problem 28-01.2 [A]

**Two ways to add.** Four dimensions carry weights 0.3, 0.3, 0.2 and 0.2. Target X scores 5, 5, 1 and 4; target Y scores 4, 4, 3 and 3.5. Find each target's weighted arithmetic and geometric scores. Which leads under each, and why do they disagree?

### Problem 28-01.3 [B]

**A gate.** X's score of 1 on the third dimension (IP position) reflects a core licence that terminates on a change of control. Treat an IP score of at least 2 as a knockout gate.

- (a) Does X pass the gate? What does that mean for its scores in Problem 28-01.2?
- (b) The buyer makes the licensor's consent a closing condition, and the IP score rises to 3. Find X's new arithmetic and geometric scores.

### Problem 28-01.4 [B]

**Where to look first.** X's score standard deviations are 1.0, 0.5, 0.5 and 0.3 (weights as in Problem 28-01.2).

- (a) Find the variance and standard deviation of X's arithmetic score, and the first dimension's share of the variance.
- (b) A deep-dive cuts the first dimension's standard deviation to 0.4. Find the new variance and standard deviation.

### Problem 28-01.5 [B]

**Is X really ahead?** Y's four scores each have a standard deviation of 0.4.

- (a) Find the variance of Y's score, the standard deviation of $S_X - S_Y$ and the probability that Y is truly ahead, using Problem 28-01.4(a)'s uncertainty for X.
- (b) Repeat with X's score errors correlated pairwise at $\rho = 0.6$ (a halo effect from one impressive meeting).

### Problem 28-01.6 [B]

**The compiler claim.** The claim: the target's compiler runs the buyer's ten most important models without hand-tuning. The prior is 0.3. Evidence: release notes list 8 of the 10 as supported (likelihood ratio 2); a buyer's engineer compiles three of them in a sandbox, all successfully (likelihood ratio 5); the target's largest customer still uses hand-written kernels (likelihood ratio 0.5). Find the prior odds, the posterior odds and the posterior probability.

### Problem 28-01.7 [B]

**The same test twice.** A second engineer repeats the sandbox test on the same three models. Find the posterior if it is wrongly counted as independent (likelihood ratio 5 again), and if its likelihood ratio given the first test is only 1.2.

### Problem 28-01.8 [B]

**How strong must it be?** Find the combined likelihood ratio needed to move a claim from 10% to 50%, and from 10% to 90%. How many independent signals, each with a likelihood ratio of 3, reach 90%?

### Problem 28-01.9 [B]

**A three-spin plan.** A plan budgets three spins; each extra spin costs 5 months and a \$30 million mask set (assumed). Using the 2024 spin distribution of Example 28-01.4, find the probability that the plan holds, the expected spins beyond plan, and the expected delay and extra cost.

### Problem 28-01.10 [B]

**A milestone chain.** A product's value depends on four stages: the tape-out lands on time (0.8), the silicon meets specification within the planned spins (0.5), the product qualifies (0.9) and the lead customer ramps (0.6), each conditional on the previous ones. Success is worth \$1.2 billion in present value and failure leaves \$0.1 billion of salvage. Find the probability of success, the expected value, and the probability that the chain fails at the silicon stage.

### Problem 28-01.11 [C]

**Why earn-outs close deals.** A buyer pays \$600 million upfront plus \$400 million in 3 years if the product reaches \$250 million of annual revenue. The seller believes the probability is 0.7, the buyer 0.3; both discount at 12% a year.

- (a) Find the discount factor and each side's present value of the earn-out and of the total.
- (b) The alternative is an all-cash price of \$700 million. Which structure does each side prefer?
- (c) What does the gap between their valuations of the earn-out represent?

### Problem 28-01.12 [C]

**When a test is worthless.** Repeat Example 28-01.6 (gain \$500 million, loss \$200 million, sensitivity 0.8, specificity 0.9) with a prior of 0.9, and again with a prior of 0.2. In each case find the expected value of buying now, the EVPI, the probability of a pass, the relevant posterior, and the EVSI. Explain the two results.

### Problem 28-01.13 [B]

**Checking a roadmap.** A startup has \$150 million of cash and burns \$3.0 million a month excluding NRE. It plans two 3 nm chips in 24 months, each with \$45 million of NRE (within the 2026 range of \$30–100 million or more [R-623]). Find:

- (a) its runway without NRE;
- (b) the cash needed for the plan over 24 months, and the shortfall;
- (c) the shortfall if one chip needs a respin with a \$20 million mask set (the top of the 3–5 nm range in [R-623]);
- (d) the runway left after paying both NREs up front.

What question does the result tell you to ask?

### Problem 28-01.14 [C]

**Two derivations.**

- (a) Starting from Bayes' rule for $P(T \mid E)$ and $P(\bar T \mid E)$, derive the odds form $O(T \mid E) = O(T)\,\Lambda$, and show that for conditionally independent evidence the log-odds add.
- (b) For $n$ equally weighted scores ($w_i = 1/n$), each with standard deviation $\sigma$ and every pair correlated at $\rho$, derive $\operatorname{Var}(S) = \dfrac{\sigma^2}{n}\left[1 + (n - 1)\rho\right]$ and its limit as $n \to \infty$. Evaluate the standard deviation for $n = 7$ and $\sigma = 0.5$ at $\rho = 0$ and $\rho = 0.5$, and the limit at $\rho = 0.5$. What does the limit say about scoring more dimensions to beat a halo effect?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Seven dimensions and their evidence | 1, 13 |
| 2. Scorecards, gates and uncertainty | 2, 3, 4, 5, 14 |
| 3. Updating claims with likelihood ratios | 6, 7, 8, 14 |
| 4. Spins, milestone chains and earn-outs | 9, 10, 11 |
| 5. The value of information | 12 |
