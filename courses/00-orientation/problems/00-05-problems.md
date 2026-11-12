# Problems 00-05 · How Chip Companies' Engineering Organizations Work

Chapter: [00-05](../chapters/00-05-how-chip-companies-are-organized.md) · Worked solutions: [00-05 solutions](../solutions/00-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard · **[C]** challenge. Numbers marked "illustrative" are assumptions for practice, not facts about a particular company.

---

## Problems

### Problem 00-05.1 [A]

Match each deliverable to the function that owns it: (a) scan chains and test patterns; (b) the production test program on ATE; (c) the timing-clean layout (GDS); (d) the coverage report showing the RTL meets the spec; (e) the boot ROM code and drivers; (f) the AEC-Q100 qualification report.

### Problem 00-05.2 [A]

Put these milestones in order and say which ones are decision gates: first silicon; RTL freeze; production release; architecture freeze; tapeout; qualification complete.

### Problem 00-05.3 [B]

(a) A process has 60 mask layers. At 1.5 days per layer, what is the wafer cycle time in days?
(b) What is it for a best-in-class fab at 0.8 days per layer?
(c) A metal-only fix touches 12 layers at 1.2 days per layer. How many days of wafer processing does it need?

### Problem 00-05.4 [B]

(a) A chip has 20 independent blocks, each 99% likely to be bug-free. What is the probability of first-silicon success?
(b) With 100 blocks, what per-block probability gives 90% overall success?

### Problem 00-05.5 [B]

A product planned at \$300 M of annual revenue and 55% gross margin slips four months, and those months of sales are lost to a competitor (illustrative). Estimate the lost gross profit. Name one assumption that, if wrong, would make the loss much smaller.

### Problem 00-05.6 [B]

A design budget of \$400 M is 60% engineering labor. Assume \$350 k per fully loaded engineer-year and a 3-year program (illustrative). Estimate the average team size. A startup claims it will do a comparable chip with 60 engineers. List three things it might be doing differently.

### Problem 00-05.7 [B]

From [R-017](../../../reference/research-log.md#r-017--rd-intensity-latest-fiscal-year-10-k--annual-reports): NVIDIA reports about 31,000 R&D employees of about 42,000, and ADI about 13,000 engineering roles of about 24,500. Compute each share. Why would a fabless company have a higher R&D share than one that runs its own fabs?

### Problem 00-05.8 [B]

First-silicon success fell from about 30% (2010–2020) to 14% (2024) in the Wilson Research Group study. By what factor did the probability of needing at least one respin increase? List two reasons to be cautious about this comparison.

### Problem 00-05.9 [C] (schedule risk)

Three sequential phases have triangular durations (min, most likely, max) in weeks: verification (16, 20, 32), physical design (8, 10, 16) and fab (12, 14, 20).

(a) What is the sum of the most-likely values?
(b) What is the expected total duration?
(c) Using the lab simulator (or numerical convolution), estimate the probability of finishing within the most-likely sum, and the 80th-percentile duration.
(d) Recommend a committed date, and explain your choice to a CEO in two sentences.

### Problem 00-05.10 [C] (reading a contested estimate)

Arm's 2023 prospectus cited an IBS estimate of about \$725 M to design a 2 nm chip, of which about 71% is software, verification and IP qualification ([R-019](../../../reference/research-log.md#r-019--advanced-node-design-and-mask-cost-estimates-contested)).

(a) How much of the estimate is the remaining 29%?
(b) Critics argue such estimates run 50–66% above real-world costs. What range of actual costs does that imply?
(c) Give two reasons the cost of a *derivative* chip on the same node would be far lower.

---

## Objective coverage

| Learning objective (chapter 00-05) | Problems |
|---|---|
| 1. Engineering functions and their deliverables | 1, 6 |
| 2. Lifecycle, gates and steppings | 2, 3 |
| 3. Cycle time, team size and contested costs | 3, 6, 10 |
| 4. Probability of success; schedule skew | 4, 8, 9 |
| 5. Questions about organizations and risk | 5, 6, 7, 9 |
