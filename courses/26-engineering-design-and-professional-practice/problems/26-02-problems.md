# Problems 26-02 · Design Reviews, Documentation and Standards Bodies

Chapter: [26-02](../chapters/26-02-design-reviews-and-standards.md) · Worked solutions: [26-02 solutions](../solutions/26-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Reviewers work independently unless a problem says otherwise.
- IEEE SA ballot rules (26-02 §3.5): at least 75% of the balloting group returns a ballot; at least 75% of Approve plus Do Not Approve votes are Approve; the ballot is invalid if 30% or more of returned ballots are abstentions.
- "Assumed" values are illustrative.

---

## Problems

### Problem 26-02.1 [A]

**Peer or milestone?** Classify each as a peer review or a milestone review, and say what decision (if any) it makes: (a) two senior designers read a new cache controller's micro-architecture document and log issues; (b) the vice-president of engineering decides whether to order masks; (c) the analog team walks through a bandgap layout with an outside consultant; (d) the program decides whether to start detailed design of the chosen architecture.

### Problem 26-02.2 [A]

**RTL freeze.** Write three entry criteria and three exit criteria for an RTL-freeze review of an SoC, and say which document or metric shows that each is met.

### Problem 26-02.3 [B]

**Sizing a review.** A 60-page specification is expected to contain 30 defects. Each reviewer finds any given defect with probability 0.50, costs $8,000 of time, and each escaped defect costs $5,000 downstream (all assumed). (a) Find the marginal bound on the number of reviewers and the optimal number. (b) What fraction of defects does the optimal team find, how many escape, and what is the expected total cost? (c) Tabulate the cost for one to six reviewers and comment on how flat the optimum is.

### Problem 26-02.4 [B]

**Three kinds of defect.** In a design document, 60% of defects are easy (each reviewer finds them with probability 0.6), 25% are subtle (0.2) and 15% are invisible to reading the document (0). (a) What fraction does a single reviewer find? (b) Three reviewers? (c) Five, and ten? (d) What is the limit as the number of reviewers grows? (e) How many reviewers reach 75%, and what would independent reviewers with the same single-reviewer rate find with three?

### Problem 26-02.5 [B]

**Capture–recapture.** Two reviewers of a verification plan find 30 and 22 issues, 15 of them in common. Estimate (a) each reviewer's detection probability, (b) the total by Lincoln–Petersen and Chapman, and (c) the issues still undiscovered.

### Problem 26-02.6 [C]

**Why the estimate runs low.** (a) Derive the Lincoln–Petersen estimate by the method of moments, stating each assumption. (b) Show that Chapman's estimate is finite when the reviewers find no defect in common. (c) A document has 40 defects: 20 easy, each found by each reviewer with probability 0.8, and 20 hard, found with probability 0.2. Compute the expected $n_1$, $n_2$ and $m$, the Lincoln–Petersen estimate from those expectations, and its relative error. (d) Explain the direction of the error.

### Problem 26-02.7 [B]

**A ballot short of consensus.** A balloting group of 220 returns 160 ballots: 105 Approve, 40 Do Not Approve and 15 Abstain. (a) Check the three rules. (b) If five more members return Approve ballots, does it pass? (c) With those 165 ballots, how many Do Not Approve voters must change to Approve?

### Problem 26-02.8 [B]

**Too many abstentions.** A group of 200 returns 170 ballots: 90 Approve, 25 Do Not Approve and 55 Abstain. (a) Check the three rules. (b) What is the largest number of abstentions that keeps the ballot valid? (c) If that many abstainers instead vote Do Not Approve, does the ballot pass?

### Problem 26-02.9 [B]

**A Wi-Fi chip in a laptop.** A Wi-Fi chip sells for $6 and goes into a $1,000 laptop (assumed). Forty holders each ask 0.25% of the laptop's price (assumed). (a) Find the stacked royalty per laptop and its multiple of the chip's price. (b) What would the same total rate give on the chip? (c) Under a top-down aggregate of 3% of the laptop's price, what does a holder with 5% of the essential patents receive?

### Problem 26-02.10 [C]

**When the royalty eats the chip.** A chip priced $P_c$ goes into a device priced $P_d$. (a) Show that a device-level royalty rate $r_d$ is equivalent to a chip-level rate $r_c = r_dP_d/P_c$, and find the device rate at which the royalty equals the chip's whole price. (b) Evaluate both for $P_c$ = \$20 and $P_d$ = \$500 with $r_d$ = 1%. (c) If the chip supplier itself paid that 1% device-level royalty, what would happen to a 55% gross margin? (d) Explain why the "smallest saleable compliant implementation" language matters to component suppliers.

### Problem 26-02.11 [B]

**Draft or freeze, again.** Starting before a standard freezes gains four months, worth $3 M a month (assumed), with a 30% chance of a late change (assumed). (a) Find the net expected value of starting early if a change costs a metal ECO of $2 M and one month. (b) If it costs a respin of $20 M and five months. (c) Find the break-even probability in case (b).

### Problem 26-02.12 [A]

**Where does it belong?** Say whether each belongs in the datasheet, an application note, the errata or the internal specification only: (a) the maximum supply voltage; (b) a recommended PCB layout for the regulator; (c) a bug in stepping A0 that corrupts a register when two interrupts collide, with a software workaround; (d) the arbitration algorithm of an internal bus; (e) the typical power at a stated workload.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Review gates, entry and exit criteria | 1, 2 |
| 2. Reviewer count, cost and blind spots | 3, 4 |
| 3. Capture–recapture | 5, 6 |
| 4. Standards consensus and balloting | 7, 8, 11 |
| 5. FRAND, royalty stacking and the royalty base | 9, 10 |
| (Documentation, §3.4) | 12 |
