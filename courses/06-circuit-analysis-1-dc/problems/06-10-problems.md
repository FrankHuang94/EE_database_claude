# Problems 06-10 · The Ideal Op-Amp

Chapter: [06-10](../chapters/06-10-ideal-op-amp.md) · Worked solutions: [06-10 solutions](../solutions/06-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** op-amps are ideal unless a non-ideality is given; supplies are ±15 V unless stated. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-10.1 [A]

**Inverting amplifier.** $R_1$ = 4.7 kΩ and $R_2$ = 100 kΩ. Find the gain, the output for a 0.1 V input and the input resistance.

### Problem 06-10.2 [A]

**Choosing resistors.** Design a non-inverting amplifier with a gain of exactly 25 using $R_1$ = 1 kΩ. What is the output for 0.2 V in, and what is the input resistance?

### Problem 06-10.3 [A]

**A summing amplifier.** Inputs of 1 V, −0.5 V and 2 V drive a virtual ground through 10 kΩ, 20 kΩ and 40 kΩ; $R_f$ = 20 kΩ. Find the output.

### Problem 06-10.4 [B]

**A difference amplifier with one mismatched resistor.** A difference amplifier has $R_1 = R_3$ = 10 kΩ and $R_2 = R_4$ = 100 kΩ, with $v_1$ = 2.00 V and $v_2$ = 2.05 V. (a) Find the output. (b) $R_4$ is 1% high (101 kΩ). Find the output, the error, and the output when both inputs are 2.00 V. (c) Interpret the result as a common-mode gain.

### Problem 06-10.5 [B]

**A photodiode amplifier.** A photodiode delivers 0 to 5 µA into the virtual ground of a transimpedance amplifier with $R_f$ = 500 kΩ. (a) Find the output range. (b) Find the output error due to bias current for an LM358 (−250 nA maximum) and an OPA187 (350 pA maximum). Which is usable?

### Problem 06-10.6 [B]

**Curing a loading problem.** A sensor with 1 V open-circuit output and 100 kΩ source resistance drives an ADC whose input resistance is 10 kΩ. (a) What does the ADC see? (b) Insert a follower. What does it see now? (c) With a follower of finite gain $A = 10^5$, what is the follower's exact gain?

### Problem 06-10.7 [B]

**Noise gain.** An inverting amplifier with $R_1$ = 1 kΩ and $R_2$ = 10 kΩ uses an op-amp with a 2 mV offset voltage. (a) What is the signal gain? (b) What output offset does the 2 mV produce? Why is it not 20 mV?

### Problem 06-10.8 [B]

**Bias-current compensation.** An inverting amplifier with $R_1$ = 10 kΩ and $R_2$ = 100 kΩ uses an op-amp whose two bias currents are each about 100 nA and differ by at most 10 nA. (a) With the + input grounded directly, find the output error due to bias current. (b) What resistor should be placed in series with the + input to cancel it, and what error remains?

### Problem 06-10.9 [C]

**When the virtual short fails.** An inverting amplifier with gain −4.7 ($R_1$ = 10 kΩ, $R_2$ = 47 kΩ) has outputs limited to ±12 V. (a) Find the input range over which it is linear. (b) For a 3 V input, find the output and the voltage at the − input. Why are the two inputs no longer at the same voltage?

### Problem 06-10.10 [C]

**An instrumentation amplifier design.** A three-op-amp in-amp uses $R$ = 24.7 kΩ and a unity-gain difference stage. (a) Find $R_G$ for gains of 1000 and 100. (b) The difference stage uses a resistor network matched to 0.02%. Estimate its CMRR from $(1 + G)/(4t)$, and the overall CMRR at a total gain of 100, in dB.

### Problem 06-10.11 [B]

**Finite gain in an inverting amplifier.** An inverting amplifier with $R_2/R_1$ = 100 uses an op-amp with $A = 10^4$. (a) Show that its gain is $-(R_2/R_1)/\bigl(1 + (1 + R_2/R_1)/A\bigr)$ and evaluate it. (b) What is the gain error in percent? Which quantity sets it, the signal gain or the noise gain?

### Problem 06-10.12 [B]

**Choosing an op-amp.** A 50 mV full-scale signal from a current-sense resistor must be amplified with a total DC error below 0.1% of full scale, referred to the input. (a) What is the error budget in microvolts? (b) Using maximum offsets at 25 °C, which of the LM358 (7 mV) and OPA187 (10 µV) fits, and what fraction of the budget does it use?

### Problem 06-10.13 [A]

**A threshold detector.** An op-amp with no feedback and outputs limited to ±12 V has a temperature sensor's output on its + input. Its − input is fed from a 5 V supply through a divider of 30 kΩ (top) and 20 kΩ (bottom). (a) Find the threshold voltage. (b) Find the output for sensor voltages of 1.8 V and 2.3 V. (c) At 2.3 V, how far apart are the two inputs, and why does the virtual short not apply? (d) With $A = 10^5$, what input difference is enough to drive the output to a rail?

---

## Objective coverage

| Learning objective (chapter 06-10) | Problems |
|---|---|
| 1. The ideal rules and when they fail | 6, 9, 11, 13 |
| 2. The standard configurations | 1, 2, 3, 5, 6 |
| 3. Common-mode rejection and in-amps | 4, 10 |
| 4. DC error budgets | 5, 7, 8, 11, 12 |
| 5. Choosing an op-amp | 5, 12 |
