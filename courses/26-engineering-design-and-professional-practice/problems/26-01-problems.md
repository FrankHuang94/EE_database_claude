# Problems 26-01 · Requirements, Specifications and the Design Process

Chapter: [26-01](../chapters/26-01-requirements-and-specifications.md) · Worked solutions: [26-01 solutions](../solutions/26-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Contributions to a budget are independent and zero-mean Gaussian unless a problem says otherwise, and every "±" bound is a 3σ bound.
- $\Phi$ is the standard normal CDF; $\Phi^{-1}(0.99)$ = 2.326.
- "Assumed" values are illustrative.

---

## Problems

### Problem 26-01.1 [A]

**Make them verifiable.** Rewrite each statement as a requirement with a criterion, conditions and a verification method, and say what you had to assume. (a) "The PMIC shall be efficient." (b) "The SerDes shall work with all customer channels." (c) "The NPU shall run large models fast."

### Problem 26-01.2 [A]

**Choosing the method.** For each requirement, name the primary verification method (test, analysis, inspection or demonstration) and justify it in one sentence. (a) The package marking shows the part number and date code. (b) The interconnect shall meet a 15-year electromigration lifetime at 105 °C. (c) The PCIe interface shall train to the full link width with a reference host. (d) The core shall run at 2.0 GHz at 125 °C junction and minimum supply. (e) The product shall contain no substance on a regulated restricted-substance list.

### Problem 26-01.3 [B]

**A smart ring's battery.** A ring has a 22 mAh battery, of which 80% is usable (assumed), and must last 120 h (five days). Its profile is sleep 0.010 mA for 90% of the time, sensing 0.40 mA for 8.5% and radio 3.0 mA for 1.5% (assumed). (a) What average current does the requirement allow? (b) What does the profile draw, and what life does it give? (c) If sensing stays fixed and the radio takes time from sleep, what is the largest radio duty that still meets 120 h? (d) Repeat (c) for a battery aged to 70% usable.

### Problem 26-01.4 [B]

**A jitter budget.** A 32 Gb/s receiver tolerates a total jitter of 0.50 UI at a bit-error ratio of 10⁻¹². Deterministic jitter adds linearly; random jitter combines as RSS of rms values, and total jitter is $TJ = DJ + 2Q\sigma_{RJ}$ with $Q$ = 7.03 (the dual-Dirac model of 24-02). The contributions are deterministic 4, 3 and 2 ps, and random 0.30, 0.25 and 0.22 ps rms (assumed). (a) Find the unit interval, $DJ$, $\sigma_{RJ}$, $TJ$ and the margin. (b) What $TJ$ results if someone wrongly RSSes the deterministic terms? (c) What if someone wrongly adds the random terms linearly? (d) Which error is dangerous, and why?

### Problem 26-01.5 [B]

**A systematic offset.** A regulator's output must stay within ±3.0% of nominal. Its random contributions combine to σ = 0.90%, and a calibration error shifts the mean by +0.50% (assumed). (a) Find the fraction of units outside the limit, split into the upper and lower tails. (b) Compare with the case of no offset. (c) Why does a requirement on the mean belong in the specification as well as one on the spread?

### Problem 26-01.6 [C]

**Correlation and the RSS.** (a) Starting from $\operatorname{Var}(X + Y) = \operatorname{Var}X + \operatorname{Var}Y + 2\operatorname{Cov}(X, Y)$, derive the variance of a sum of $n$ contributions with correlation coefficients $\rho_{ij}$. (b) Show that if every $\rho_{ij}$ = 1 the standard deviation of the sum equals the sum of the standard deviations, so RSS becomes worst case. (c) For $n$ equal contributions of standard deviation σ with a common correlation ρ, show that $\sigma_E = \sigma\sqrt{n + n(n - 1)\rho}$. (d) Evaluate it for $n$ = 6 and ρ = 0.2, and compare with independence and with worst case.

### Problem 26-01.7 [B]

**Splitting a budget.** A system must keep a total error within ±1.0%. (a) If $n$ blocks share it equally, what may each block contribute under worst-case allocation and under RSS allocation, for $n$ = 4 and $n$ = 9? (b) What is the ratio of the two allowances? (c) With $n$ = 4, one block is granted ±0.50%. What may each of the other three contribute under each method?

### Problem 26-01.8 [B]

**Closing the gaps.** A specification has 250 requirements, of which 231 have a verifying test. Of the 19 untested, 4 are high risk (a 25% chance that an error in them escapes to silicon) and 15 low risk (4%). An escape costs $1.5 M, and a test costs $15,000 to write (all assumed). (a) Find the coverage. (b) Find the expected escapes and the expected cost of the gaps. (c) What does closing all 19 cost, and what is the ratio of expected loss to that cost? (d) If the budget allows only six new tests, which do you write, and what expected cost remains?

### Problem 26-01.9 [B]

**A different program's escalation.** A program introduces 60 requirement errors. Design catches 50% of those present, build 20% and integration and test 70%, and the rest escape. Relative fix costs are 1, 4, 12, 40 and 200 for requirements, design, build, test and field, each inside the NASA ranges of 26-01 §3.6 (assumed). (a) Find the downstream average cost per error that passes the requirements review, term by term. (b) Find where the errors are found and the total cost for review catch rates of 30% and 50%. (c) At $8,000 per unit, what does the better review save?

### Problem 26-01.10 [C]

**When is a review worth it?** (a) Show that the downstream average cost obeys the recursion $\bar c_k = p_kc_k + (1 - p_k)\bar c_{k+1}$, starting from the field phase, and use it to confirm Problem 26-01.9(a). (b) Using §3.6's result, find the value of one percentage point of review catch rate for Problem 26-01.9's program at $8,000 per unit. (c) A formal review costs $250,000. What increase in catch rate pays for it? (d) Why might the answer overstate the value of reviews?

### Problem 26-01.11 [B]

**Integrated or external radio.** An IoT SoC team weighs an integrated radio (I) against an external radio chip (E). Weights: bill-of-materials cost 0.35, power 0.30, time to market 0.20, flexibility 0.15. Scores (1–5): I = 5, 4, 2, 2; E = 2, 3, 5, 5 (all assumed). (a) Rank the options. (b) Sweeping the time-to-market weight with the others rescaled in proportion, find each option's score on the other criteria and the tie weight. (c) Is this decision robust? Compare with Example 26-01.6.

### Problem 26-01.12 [C]

**Scales are weights in disguise.** (a) Show that adding the same constant to every option's score on one criterion does not change the ranking, but multiplying that criterion's scores by a factor $m$ has the same effect as multiplying its weight by $m$ and renormalizing. (b) In Problem 26-01.11, one reviewer scores time to market on a 1–10 scale (I = 4, E = 10) while keeping the others on 1–5. Find the new scores. (c) What effective weight on time to market does that imply, and how does it compare with the tie weight of Problem 26-01.11(b)?

### Problem 26-01.13 [A]

**Which process?** Name the process model (or combination) you would use, with a one-sentence reason, for: (a) the firmware of an MCU product that receives field updates; (b) the tape-out plan of a 3 nm SoC; (c) a new analog block of a kind the team has never built; (d) an automotive braking controller that must meet a functional-safety standard.

### Problem 26-01.14 [B]

**The cost of churn.** After specification freeze, a program absorbs 40 requirement changes. Each needs 2.5 engineer-weeks of rework on average, and 15% of them land on the critical path, adding 1.0 week each (assume they add in sequence). Engineering costs $5,000 per engineer-week and delay costs $2.0 M of gross profit per week (all assumed). (a) Find the rework effort and its cost. (b) Find the expected schedule slip and its cost. (c) Which dominates, and what does that imply for how changes after freeze should be approved?

### Problem 26-01.15 [C]

**Every unit, not the average.** A device's mean battery life is 175 h against a requirement of at least 168 h for every unit. Battery capacity and average current vary from unit to unit as independent lognormal variables with log-standard deviations 0.03 and 0.05 (assumed). (a) Find the log-standard deviation of life. (b) What fraction of units falls short of 168 h, taking 175 h as the median life? (c) What median life is needed for 99% of units to meet 168 h? (d) Rewrite the requirement so that it says what the customer actually needs.

### Problem 26-01.16 [B]

**Build the matrix.** A fitness band's MRD lists five needs: M1, a week between charges; M2, accurate heart rate during exercise; M3, easy phone sync; M4, rugged outdoor use; M5, a low price. The PRD derives eight requirements, each tracing to the need in brackets: R1, battery life ≥ 168 h under profile UP-1 (M1); R2, sleep current ≤ 50 µA (M1); R3, heart-rate error ≤ ±5 bpm from 60 to 180 bpm while running (M2); R4, optical sampling ≥ 25 Hz (M2); R5, a day's data synced in under 30 s (M3); R6, BOM ≤ $38 at 1 M units (M5); R7, operation from −10 to 50 °C (M4); R8, firmware updates over the air (M3). The verification plan has six tests: T1, battery rundown under UP-1 (verifies R1); T2, sleep-current measurement (R2); T3, treadmill heart-rate test against a chest strap (R3); T4, sampling-rate check (R4); T5, a 1.5 m drop test (no requirement listed); T6, BOM roll-up analysis (R6). The architecture has five design elements: D1, a PMIC with 30 µA quiescent current (implements R1, R2); D2, a PPG front end sampling at 32 Hz (R3, R4); D3, a BLE radio and bootloader (R5, R8); D4, a low-cost MCU (R1, R6); D5, an NFC payment module (no requirement listed). (a) Build the traceability matrix with requirements as rows and tests and design elements as columns. (b) Find the test coverage and list the unverified requirements. (c) List the childless requirements. (d) List the orphan tests and design elements, and say what each orphan suggests. (e) Which MRD needs are not yet fully verified?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Market requirements to verifiable specifications | 1, 2, 16 |
| 2. Flow-down, worst-case and RSS budgets, compliance probability | 3, 4, 5, 6, 7, 15 |
| 3. Traceability and the cost of gaps | 8, 16 |
| 4. Process models and changes after freeze | 13, 14 |
| 5. Escalation of late errors and decision matrices | 9, 10, 11, 12 |
