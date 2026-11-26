# Problems 28-10 · Conversation Scenarios

Chapter: [28-10](../chapters/28-10-conversation-scenarios.md) · Worked solutions: [28-10 solutions](../solutions/28-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Treat each problem as a live check you must do in about a minute, then say what you would ask next. Parameters are assumed unless a source is cited; the methods are those of the pocket card (§3.5). A year is 8,766 hours. Use N3 wafers at \$18,500 [R-575] and $D_0$ = 0.001 per mm² where needed.

---

## Problems

### Problem 28-10.1 [A]

**Better questions.** Rewrite each as a question that invites a number with conditions:

- (a) "How efficient is your power stage?"
- (b) "Is your memory interface fast?"
- (c) "How reliable is the part?"

### Problem 28-10.2 [B]

**A bigger roofline.** An accelerator has 3 PFLOP/s dense FP8 and 6 TB/s. A team claims high decode utilization at batch 32 with FP8 weights. Find the ridge, the decode intensity, the attainable throughput and its share of peak, and the batch at the ridge.

### Problem 28-10.3 [B]

**Another iso-power claim.** A CPU claims 15% more performance at the same power with 5% more IPC and 5% more switched capacitance. Find the frequency ratio, the power factor and the required reduction in energy per operation.

### Problem 28-10.4 [A]

**A link budget.** What does 25.6 Tb/s of SerDes cost at 3.5 pJ/bit all-in?

### Problem 28-10.5 [B]

**Half a million link-hours.** Zero flaps in 500,000 link-hours: find the 95% upper bound on the flap rate per million link-hours and the bound on flaps per day for a 4,000-link cluster.

### Problem 28-10.6 [B]

**A metering node.** A node sleeps at 2 µA, runs at 5 mA for 10 ms every 5 s, and transmits at 8 mA for 3 ms every 60 s. Find its average current and its life on a 1,000 mAh cell before derating.

### Problem 28-10.7 [A]

**Five for six.** With the chapter's prior (mean 14%, weight 10), find the posterior mean first-silicon success rate for a team with 5 successes in 6 projects, and the weight on its record.

### Problem 28-10.8 [B]

**A mixed meeting.** Prior 0.3; answers with likelihood ratios 3, 0.4, 2, 1 and 0.5. Find the posterior odds and probability. Then suppose the 0.4 and 0.5 answers concern the same fact and are counted once at 0.4; find the new posterior.

### Problem 28-10.9 [B]

**A $100M pipeline.** Fifty design wins at $2M lifetime revenue each; 30% convert; revenue arrives evenly over years 1–3; discount 10%. Find the average discount factor, the risk-adjusted value and the ratio of the $100M claim to it.

### Problem 28-10.10 [B]

**Scoring yourself.** Find the Brier score of a forecaster who said 0.8 on five claims that came true and 0.6 on five that did not; of one who always says 0.5; and of an overconfident one who said 0.95 on six claims that came true and 0.95 on four that did not.

### Problem 28-10.11 [B]

**A small part.** A $25 part with $3 of package and test must reach 50% gross margin on N3. Find the unit-cost and die-cost budgets and the area budget (dies per wafer unrounded).

### Problem 28-10.12 [C]

**Two properties of the method.**

- (a) Show that the order in which answers arrive does not change the posterior, provided they are conditionally independent.
- (b) Show that the expected Brier score of reporting $p$ when the true probability is $q$ is $(p - q)^2 + q(1 - q)$, so reporting $p = q$ minimizes it (a proper scoring rule). Evaluate it for $q = 0.7$ with $p = 0.7$ and $p = 0.9$.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Preparation and question design | 1 |
| 2. Moves and anti-patterns | 1, 8 |
| 3. Live calculations | 2, 3, 4, 5, 6, 9, 11 |
| 4. Debrief scoring | 7, 8, 12 |
| 5. Calibration | 10, 12 |
