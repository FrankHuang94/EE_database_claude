# Problems 25-10 · Qualification and Functional Safety

Chapter: [25-10](../chapters/25-10-qualification-and-functional-safety.md) · Worked solutions: [25-10 solutions](../solutions/25-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Coffin–Manson acceleration $(\Delta T_s/\Delta T_{field})^n$; one 60 K field cycle a day unless stated.
- Mission-profile stress hours $\sum_i w_it_{life}/AF(T_i \to T_{stress})$ with Arrhenius, $k$ = 8.617 × 10⁻⁵ eV/K.
- $SPFM = 1 - \sum(\lambda_{SPF} + \lambda_{RF})/\sum\lambda$; $LFM = 1 - \sum\lambda_L/\sum(\lambda - \lambda_{SPF} - \lambda_{RF})$; dual-point rate $\lambda_L\lambda_D\tau$.
- ASIL D: SPFM ≥ 99%, LFM ≥ 90%, PMHF < 10 FIT; ASIL C: SPFM ≥ 97%, LFM ≥ 80%, PMHF < 100 FIT [R-614].
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-10-lab/qual.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-10.1 [A]

**Other grades.** AEC-Q100 Grade 2 cycles from −55 to +125 °C for 1,000 cycles [R-612]. (a) Find its range, its acceleration with $n = 2$ and its equivalent field years. (b) Grade 0 used to require 2,000 cycles at −55 to +150 °C. What field years did that represent with $n = 2$?

### Problem 25-10.2 [B]

**What exponent is needed?** For Grade 1's 1,000 cycles at 205 K to cover 15 years of daily 60 K cycles, what Coffin–Manson exponent must the failure mechanism have at least?

### Problem 25-10.3 [B]

**A lower activation energy.** *(lab)* Repeat Example 25-10.2(b) with $E_a$ = 0.5 eV. What fraction of the profile does a 1,000 h test at 150 °C now cover?

### Problem 25-10.4 [C]

**How good must the lockstep be?** *(lab)* In Example 25-10.4, what diagnostic coverage of the dangerous faults is needed for SPFM to reach (a) 99% and (b) 97%?

### Problem 25-10.5 [B]

**A bigger checker.** If the comparator of Example 25-10.4 has 30 FIT instead of 20 (total 230 FIT), find (a) the LFM without self-test and (b) the self-test coverage needed for ASIL D's LFM.

### Problem 25-10.6 [B]

**Periodic test.** *(lab)* In Example 25-10.5(a), the comparator is instead tested every 1,000 h of operation by a test that reveals all of its faults. Estimate the dual-point rate.

### Problem 25-10.7 [A]

**Sharing the budget.** An ASIL D item has a 10 FIT PMHF budget and allocates 10% to one SoC. Does Example 25-10.4's element (PMHF ≈ 1.20 FIT) fit?

### Problem 25-10.8 [B]

**A bigger car.** A vehicle has 20,000 semiconductor components at 0.1 ppm each (assumed). What fraction of vehicles carries a defective component?

### Problem 25-10.9 [A]

**FIT to probability.** What probability of a safety-goal violation does 100 FIT allow over 10,000 h?

### Problem 25-10.10 [C]

**Demonstrating ppm by sampling.** How many units must pass a zero-failure test to show, at 90% confidence, a defective fraction below 100 ppm? Compare with the 231 units of a classical qualification.

### Problem 25-10.11 [B]

**ECC and soft errors.** A 4 Mb SRAM has a raw soft-error rate of 1,000 FIT per megabit (assumed). SEC-DED ECC corrects all single-bit events, and 0.1% of events are multi-bit in one word (assumed); treat every multi-bit event as residual, an upper bound because SEC-DED detects (and the system could safely handle) double-bit errors. Find the raw rate and the residual rate, and compare with an ASIL D item's 10 FIT budget.

### Problem 25-10.12 [A]

**What sets an ASIL.** For each hazard, say whether its severity, its exposure and its controllability push the ASIL up or down, and which is most likely to be rated QM: (a) unintended full braking at highway speed; (b) loss of power-steering assist while parking; (c) a dashboard clock showing the wrong time.

### Problem 25-10.13 [C]

**The dual-point rate, derived.** A safety mechanism's faults arrive at rate $\lambda_L$ and are revealed by a test every $T$ hours; dangerous faults that the mechanism would catch arrive at $\lambda_{DD}$. (a) Show that for small rates the time-averaged violation rate is $\lambda_L\lambda_{DD}T/2$. (b) Evaluate it in FIT for Example 25-10.5's rates ($\lambda_L$ = 20 FIT, $\lambda_{DD}$ = 118.8 FIT) with a monthly test, $T$ = 720 h. (c) By what factor does that beat never testing over a 15,000 h life?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. What qualification shows | 10 |
| 2. Equivalent field use | 1, 2, 3 |
| 3. ASILs and targets | 7, 9, 12 |
| 4. FMEDA metrics and latent faults | 4, 5, 6, 11, 13 |
| 5. ppm, ppb and vehicles | 8 |
