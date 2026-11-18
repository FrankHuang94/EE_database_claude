# Lab 03-01 · Probability in EE Language

**Chapter:** [03-01](../../chapters/03-01-probability-in-ee-language.md) · **Notebook:** [03-01-probability.ipynb](03-01-probability.ipynb) · **Time:** about 60 minutes

## Objective

1. See when the union bound is accurate and when it fails, and why $1 - (1 - p)^n$ must be computed with care.
2. Measure birthday collisions and compare with the product formula and its square-root rule.
3. Run a simulated test floor and measure the defect level and the overkill that Bayes' rule predicts.
4. Watch independence fail when defects cluster, while conditional independence still holds.
5. Check majority voting and common-mode failures by simulation.
6. Understand what "95% confidence" means for a zero-error BER test.

## Background

Chapter sections 3.1–3.8 and Examples 03-01.1 to 03-01.7. No circuit simulation is needed: the "hardware" here is random-number generation, with a fixed seed so your numbers match these.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict where the union bound fails.
3. **Part 2:** predict the 50% collision point for 16-bit IDs.
4. **Part 3:** predict the shipped DPPM and the fraction of scrap that is good.
5. **Part 4:** predict whether clustering raises or lowers $P(L \cap M)$ relative to $P(L)P(M)$.
6. **Part 5:** predict TMR reliability at $R = 0.9$ and $R = 0.4$.
7. **Part 6:** predict how often a test at exactly the BER limit would pass.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | packet error rate, 12,000 bits | measured close to the exact $1 - (1 - p)^n$: 0.0119, 0.1131 and 0.6988 at $p = 10^{-6}$, $10^{-5}$, $10^{-4}$; the union bound gives 0.012, 0.12 and 1.2 |
| 1 | literal formula at $p = 10^{-12}$ | wrong in the fifth digit (about $1.19997\times10^{-8}$) from cancellation; the `expm1`/`log1p` form gives $1.2000\times10^{-8}$ |
| 2 | 16-bit IDs | collision more likely than not from 302 devices (approximation 301.4); simulated rates within a few thousandths of the formula |
| 3 | test floor | pass fraction about 0.883; defect level about 1130 DPPM, within statistical scatter of about ±35 (the seeded run gives 1173); good dies among rejects 0.154 |
| 4 | clustered defects | $P(L \cap M)$ about twice $P(L)P(M)$ |
| 5 | voting | TMR about 0.972 at $R = 0.9$ and 0.352 at $R = 0.4$; duplicated supplies with β = 0.1 fail about ten times as often as independent ones |
| 6 | zero-error test | about 5% of tests at the BER limit still pass ($e^{-3}$); 90%, 95% and 99% confidence need 2.303, 2.996 and 4.605 times $1/p$ bits |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 03-01.a | exact packet error rate at 1e-5 | 0.1131 | — |
| Lab 03-01.b | pass probability at the BER limit, e^-3 | 0.04979 | — |
| Lab 03-01.c | 50% collision point, 16-bit IDs | 302 | devices |
| Lab 03-01.d | defect level, formula | 1132.5 | DPPM |

## Discussion questions

1. Part 3's simulated DPPM differs from the formula by a few percent. How many shipped bad dies did the simulation see, and why does that number set the scatter? How many dies would you simulate to pin the DPPM to ±1%?
2. In Part 4, the failure modes are independent within each region but dependent overall. Name two real mechanisms in a fab that create this structure, and say how a test engineer would detect it in data.
3. A vendor quotes a BER of $10^{-15}$ for a 100 Gb/s link. Using Part 6, how long must they have tested to support that at 95% confidence, and what should you ask them?

## Optional hardware version

Measure a real link's error behavior with any board that exposes a bit-error-rate test, such as an FPGA transceiver's built-in PRBS generator and checker (most vendor transceiver wizards include one). Run at a data rate and loopback that gives occasional errors, record errors over several intervals, and compare the counts with the Poisson behavior previewed in Part 6. Then lower the rate until no errors appear, and compute the BER bound your error-free run supports.
