# Problems 28-09 · The Business ↔ Engineering Translation Table

Chapter: [28-09](../chapters/28-09-business-engineering-translation.md) · Worked solutions: [28-09 solutions](../solutions/28-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** 300 mm wafers; dies per wafer from $\pi d^2/(4A) - \pi d/\sqrt{2A}$, rounded down unless stated; Poisson yield $e^{-AD_0}$ with $D_0$ = 0.001 per mm² unless stated. Wafer prices are reported estimates [R-575]; other parameters are assumed. A year is 8,766 hours.

---

## Problems

### Problem 28-09.1 [A]

**Which row?** For each statement, name the row of the translation table (§3.1) it belongs to and the engineering quantity you would ask for:

- (a) "Our next product will carry a 62% gross margin."
- (b) "We save hyperscalers millions a year in power."
- (c) "We are two quarters from revenue."
- (d) "Our parts are automotive-grade reliable."

### Problem 28-09.2 [B]

**On N2.** Repeat Example 28-09.1 on a $30,000 N2 wafer [R-575]: find the cost per good die at 100 and 120 mm², and the percentage increase.

### Problem 28-09.3 [B]

**A big die.** For a 600 mm² die, find $1 + AD_0$, the dies per wafer at 600 and 660 mm², and the cost increase and average elasticity for that 10% growth on an \$18,500 wafer.

### Problem 28-09.4 [B]

**Another area budget.** A part sells at $45 with $6 of package and test and must reach 55% gross margin on an $18,500 wafer. Find the maximum unit cost, the maximum die cost, and the largest die area (dies per wafer unrounded).

### Problem 28-09.5 [B]

**A cheaper respin.** A product earning $120M a year at 50% gross margin in a fixed window needs a respin with $15M of masks (assumed, an older node) and a 5-month delay. Find the lost revenue, lost gross profit and total profit impact.

### Problem 28-09.6 [B]

**A 100 W advantage.** Devices draw 700 W and 600 W at equal performance; PUE 1.2, $0.12 per kWh, 5-year life. Find each device's lifetime energy cost, the saving, and how many more of the lower-power devices fit in the same power budget, in percent.

### Problem 28-09.7 [A]

**A car fleet.** A part rated at 20 FIT goes into 5 million cars that each operate 500 hours a year. Find the expected failures a year and their cost at $2,000 each.

### Problem 28-09.8 [B]

**Energy as a share of price.** A $25,000 accelerator draws 1,000 W for 4 years at PUE 1.3. Find its lifetime energy cost and that cost as a share of its price at $0.08 and at $0.15 per kWh.

### Problem 28-09.9 [A]

**Break-even volume.** A leading-edge design costs $150M of engineering plus a \$40M mask set (the top of the range of estimates [R-321], [R-623]). Each unit earns $30 of gross profit. How many units are needed to recover the fixed cost?

### Problem 28-09.10 [C]

**Three derivations.**

- (a) Show that, ignoring the wafer-edge term, the elasticity of die cost to die area is $1 + AD_0$.
- (b) Show that a 10% rise in selling price raises gross margin by $(1 - \text{GM})(1 - 1/1.1)$, and check it against Example 28-09.6.
- (c) Show that a power saving of fraction $s$ per device allows $1/(1 - s) - 1$ more devices in a fixed power budget, and evaluate it for $s$ = 0.1.

### Problem 28-09.11 [B]

**A plausible-range tornado.** Start from the base case of Example 28-09.6 (ASP \$90, 100 mm², \$18,500 wafer, $D_0$ = 0.001 per mm², package and test \$8, whole dies). A skeptical engineer accepts these ranges for a die on a young node: ASP \$80–95, die area 98–103 mm², wafer price \$17,000–20,000, $D_0$ 0.0008–0.003 per mm², package and test \$7–10.

- (a) Find the change in gross margin (points) at each end of each range, and each driver's total swing.
- (b) Rank the drivers by swing and compare the ranking with the equal-swing tornado of Example 28-09.6.
- (c) Which engineering claim should diligence test hardest, and what would you ask for?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Margin from die area; elasticity | 1, 2, 3, 10 |
| 2. Reverse translation: area budgets | 4 |
| 3. Pricing schedule and power (including the masks and NRE a respin or a new design must recover) | 1, 5, 6, 8, 9, 10 |
| 4. FIT to field cost | 1, 7 |
| 5. Sensitivity of margin | 10, 11 |
