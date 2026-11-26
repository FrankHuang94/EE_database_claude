# Problems 28-03 · Maturity Scales for Silicon

Chapter: [28-03](../chapters/28-03-silicon-maturity-scales.md) · Worked solutions: [28-03 solutions](../solutions/28-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Stage probabilities, durations and discount rates are assumed. Use the stage chain of Example 28-03.2 unless told otherwise: from tape-out, first silicon boots (0.95, 4.5 months), engineering samples (0.80, 6 months), qualification (0.85, 5 months), production release (0.95, 2 months), at 15% a year. Arrhenius factors use $k_B = 8.617 \times 10^{-5}$ eV/K and $T$ = °C + 273.15. FIT bounds use $\chi^2_{C;\,2r+2}/(2nt\,\text{AF}) \times 10^9$.

---

## Problems

### Problem 28-03.1 [A]

**Which level?** Place each on the scale of §3.1 and name the evidence that would confirm it: (a) "RTL complete, 92% functional coverage"; (b) "first silicon passed 60% of the validation plan at nominal voltage"; (c) "AEC-Q100 Grade 1 qualification report issued on the B1 stepping"; (d) "released part numbers shipping from two assembly sites".

### Problem 28-03.2 [A]

**Readiness levels.** Using NASA's definitions [R-701], which TRL is closest to each: a breadboard demonstrated in a realistic simulated environment; a fully functional prototype; a system "flight qualified" and ready for implementation; and the analogue of each in the silicon scale?

### Problem 28-03.3 [B]

**From first silicon.** A programme is at L3. Find its probability of reaching production, the remaining time if all goes well, and its value multiplier.

### Problem 28-03.4 [B]

**Paying for qualification.** Find the discount factor and value multiplier of a programme that has completed qualification (only the release step, 0.95 and 2 months, remains), and the most a buyer should pay for it relative to the same programme at tape-out.

### Problem 28-03.5 [B]

**Acceleration factors.** Find the Arrhenius acceleration factor between a 70 °C use junction and a 125 °C stress junction for activation energies of 0.7 eV and 0.9 eV.

### Problem 28-03.6 [B]

**Two lots more.** A product runs 462 devices (6 lots of 77) for 1000 hours at 125 °C with zero failures. Its use junction is 70 °C and the mechanism's activation energy 0.7 eV. Find the FIT bound at 60% confidence.

### Problem 28-03.7 [B]

**One failure.** Repeat Problem 28-03.6 if one device failed.

### Problem 28-03.8 [C]

**Planning for 5 FIT.** How many devices must a zero-failure 1000-hour test at 125 °C include to bound the failure rate at 5 FIT with 90% confidence, for a 55 °C use junction and 0.7 eV?

### Problem 28-03.9 [B]

**A driver's bug curve.** A driver team has found 160 defects by week 8 of system testing and 256 by week 16. Fit the Goel–Okumoto model, and find the defects remaining and the discovery rate at week 16.

### Problem 28-03.10 [B]

**When to release.** For Problem 28-03.9's team, find the week at which the discovery rate falls to 2 a week, the weeks still to go from week 16, and the defects remaining then.

### Problem 28-03.11 [A]

**Automotive grades.** Using AEC-Q100 Rev J [R-612]: (a) which grade covers −40 °C to +125 °C ambient; (b) which covers −40 °C to +150 °C; (c) what temperature-cycling condition and count does Grade 1 require (test A4)?

### Problem 28-03.12 [C]

**Two derivations.**

- (a) For a constant failure rate $\lambda$ and $T_{\text{eq}}$ equivalent device-hours, derive the zero-failure upper bound $\lambda_C = -\ln(1 - C)/T_{\text{eq}}$, and show it equals $\chi^2_{C;2}/(2T_{\text{eq}})$ using the chi-square distribution function with 2 degrees of freedom, $F(x) = 1 - e^{-x/2}$.
- (b) For the Goel–Okumoto model, derive the two-point fit for $t_2 = 2t_1$, and show that when the discovery rate is $\lambda^*$ the remaining defects are $\lambda^*/b$.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. The maturity scale and its evidence | 1, 2, 11 |
| 2. Probability, time and value from a level | 3, 4 |
| 3. Qualification bounds and sample sizes | 5, 6, 7, 8, 12 |
| 4. Software defect discovery | 9, 10, 12 |
| 5. Combining dimensions | 1, 11 |
