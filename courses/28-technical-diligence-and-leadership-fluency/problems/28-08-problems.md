# Problems 28-08 · Post-Acquisition Integration Risk

Chapter: [28-08](../chapters/28-08-integration-risk.md) · Worked solutions: [28-08 solutions](../solutions/28-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Synergies, costs, probabilities and impacts are assumed unless a source is cited. Synergies arrive at year-ends. TPP is dense TOPS × bit length (2 × MacTOPS × bits, 28-02). Export-control questions use the 2023 text of ECCN 3A090 [R-659] for illustration only; they are not legal advice, and later rules apply.

---

## Problems

### Problem 28-08.1 [A]

**Integration answers.** Classify each answer from a target's engineering leaders as strong, partial or evasive, and say what would make it strong:

- (a) "We'll move to your flow right away; our engineers are flexible."
- (b) "Our current tape-out is in 10 weeks on our flow; we propose to finish it there, then migrate the next project, which starts in month 4, with two of our methodology engineers paired with yours."
- (c) "Our products are complementary to yours."
- (d) "Our CPU cores are under an Arm license we negotiated in 2021; I'd have to check whether it has change-of-control terms."

### Problem 28-08.2 [B]

**A smaller synergy plan.** Synergies of $30M a year for 4 years at 12%. Find the annuity factor and planned value, the value if integration slips one year and two years with 75% realization, and the fractional losses.

### Problem 28-08.3 [B]

**A bigger migration.** Migrating 40 engineers takes 6 months at $22k per engineer-month. Done mid-project, it delays a product earning $90M a year in a fixed window by 4 months. Its gross margin is 55% (assumed). Find the migration's direct cost, the lost revenue and the lost gross profit, and say whether to migrate now.

### Problem 28-08.4 [B]

**Correlated paths.** Two programs for a $150M socket succeed with probabilities 0.7 and 0.4; keeping the second costs $25M. (a) If they are independent, find the probability that both fail, the probability that at least one succeeds, the value with both and with the better alone, the gain, and the decision. (b) If shared IP raises the probability that both fail to 0.25, find the gain.

### Problem 28-08.5 [A]

**Royalty points.** A combined product line ships 30 million chips a year at $12 each. Find the annual royalty at 1.5% and at 3% of the selling price, and the margin points the difference represents.

### Problem 28-08.6 [B]

**Another earn-out.** A deal pays $1.2B upfront and $0.8B contingent (all-or-nothing) in 2 years; the discount rate is 10%. Find the contingent share of the maximum, and the expected present value of the contingent part and of the deal for a payout probability of 0.5 and of 0.7.

### Problem 28-08.7 [B]

**A register with a tail risk.** Four risks (probability, impact $M): (0.40, 25), (0.15, 80), (0.05, 300), (0.30, 15). Find the expected loss and the largest contributor. A pre-signing license review would cut the third risk's probability to 0.01; find the new expected loss and the saving.

### Problem 28-08.8 [B]

**Export status.** Find the TPP of an accelerator with 400 dense INT8 TOPS and its performance density on a 600 mm² die; the TPP of one with 1,200 dense INT8 TOPS; and the TPP of an edge NPU with 150 dense INT8 TOPS. Compare each with the 3A090.a thresholds (TPP of 4800, or TPP of 1600 with performance density of 5.92) and say whether it could fall in the lower 3A090.b band [R-659].

### Problem 28-08.9 [A]

**Two years late.** Repeat Example 28-08.1 with a two-year slip and 80% realization. Find the value and the fractional loss.

### Problem 28-08.10 [B]

**A fixed window.** In Example 28-08.1, suppose a one-year slip removes the first year of synergies but the window still ends after year 5 (full realization). Find the value and the fractional loss, and compare with a slip that shifts all five years by one year.

### Problem 28-08.11 [B]

**A vesting cliff.** Without a package, key engineers leave at 1% a month (assumed). Package L vests in one lump at month 24: it lowers the rate to 0.3% a month before the cliff, but 5% a month leave in months 25–27 once it has paid (assumed). Package S costs the same but vests in thirds at months 12, 24 and 36, holding the rate at 0.5% a month throughout (assumed). Find retention at month 24 and at month 27 under each. Which does a dashboard that reports month-24 retention favor, and which keeps more people?

### Problem 28-08.12 [C]

**Four derivations.**

- (a) Derive the annuity factor $[1 - (1 + r)^{-n}]/r$ from the geometric series.
- (b) Show that a delay of $d$ years with realization $\rho$ multiplies a synergy plan's value by $\rho(1 + r)^{-d}$ when the synergies still last $n$ years.
- (c) Show that the gain from a second program is $W[1 - P(\text{both fail}) - \max(p_1, p_2)]$, and explain why positive correlation between failures reduces it.
- (d) Show that expected loss is additive across risks, and that a mitigation's value is the reduction in $p_iI_i$ it buys, whatever the other risks are.

### Problem 28-08.13 [B]

**Keep both until first silicon.** In Example 28-08.3 (programs succeed with probability 0.6 and 0.5, independent; socket worth \$200M; the second program costs \$30M to finish), suppose \$12M of that cost falls before first silicon and first silicon reveals which programs will succeed (assumed). After first silicon the buyer finishes only one working program. Find the net gain over keeping the better program alone for (a) keeping both to the end and (b) keeping both to first silicon, and (c) the value of the option to cancel at first silicon. Why is (b) an upper bound for a real milestone?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Synergy value with delay and realization | 2, 9, 10, 12 |
| 2. Migration and delay costs | 1, 3 |
| 3. Roadmap overlap as parallel paths | 1, 4, 12, 13 |
| 4. Licensing, royalties and export controls | 1, 5, 8 |
| 5. Risk registers, retention and earn-outs | 6, 7, 11, 12 |
