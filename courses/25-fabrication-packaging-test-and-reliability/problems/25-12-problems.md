# Problems 25-12 · Post-Silicon Validation and Bring-Up

Chapter: [25-12](../chapters/25-12-post-silicon-validation.md) · Worked solutions: [25-12 solutions](../solutions/25-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Trace storage $SD$ bits, window $D/f$.
- $F_{max}(V) = K(V - V_{TH})^{\alpha}/V$ with Example 25-12.2's fit ($V_{TH}$ = 0.30 V, α = 1.3, 3.0 GHz at 0.75 V).
- Goel–Okumoto $m(t) = a(1 - e^{-bt})$.
- Wilson score interval at 95% ($z$ = 1.96).
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-12-lab/postsi.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-12.1 [A]

**A longer window.** *(lab)* What trace depth covers 50 µs at 2 GHz, and how much storage does it need for 256 signals, in MiB?

### Problem 25-12.2 [B]

**Other operating points.** *(lab)* With Example 25-12.2's model, what voltage reaches (a) 2.0 GHz and (b) 3.4 GHz?

### Problem 25-12.3 [B]

**Another bug log.** A team finds 40 bugs by week 3 and 70 by week 6 (assumed). Fit the Goel–Okumoto model: find (a) $b$, (b) $a$, (c) the bugs remaining at week 6 and (d) the time to find 90% of them.

### Problem 25-12.4 [B]

**Cheaper delay.** *(lab)* Repeat Example 25-12.4 with delay costing $2 M per week. Find both expected costs and the break-even success probability.

### Problem 25-12.5 [A]

**Tighter characterization.** How many parts are needed to know the standard deviation of $V_{min}$ within ±5% at 95% confidence?

### Problem 25-12.6 [B]

**Comparing surveys.** *(lab)* Suppose 2024's 14.4% had come from 46 of 320 IC/ASIC respondents (assumed; the actual count is not published). Find its 95% Wilson interval and compare with 2026's.

### Problem 25-12.7 [A]

**Mask cost in context.** A leading-edge mask set costs $20–40 M by estimate [R-623]. What share is that of (a) a $650 M design budget and (b) a $50–75 M startup budget (use the extremes)?

### Problem 25-12.8 [C]

**Deriving the discovery curve.** (a) Derive $m(t) = a(1 - e^{-bt})$ from the assumption that each of the remaining $a - m$ bugs is found at a constant rate $b$. (b) What is the "half-life" of the remaining bugs for Example 25-12.3?

### Problem 25-12.9 [B]

**Compressed tracing.** The 1 Mbit buffer of Example 25-12.1 instead stores an entry only when the traced signals change, each entry carrying a 32-bit timestamp with the 256 signal bits. If signals change on 5% of cycles (assumed), how many entries fit, and what window does it cover at 2 GHz?

### Problem 25-12.10 [B]

**Cold silicon.** At low temperature the threshold voltage rises to 0.33 V (assumed) while $K$ stays as fitted. What voltage now reaches 2.5 GHz, and how much does it exceed Example 25-12.2's 0.651 V?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Bring-up and debug infrastructure | 1, 9 |
| 2. Characterization and Vmin | 2, 5, 10 |
| 3. Bug discovery | 3, 8 |
| 4. Fix decisions | 4, 7 |
| 5. Reading first-silicon statistics | 6 |
