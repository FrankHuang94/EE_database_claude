# Problems 12-05 · Feedback: Theory and the Four Topologies

Chapter: [12-05](../chapters/12-05-feedback-topologies.md) · Worked solutions: [12-05 solutions](../solutions/12-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $T$ is the loop gain (return ratio), positive for negative feedback; $A_f$ is the closed-loop gain; "error" means the fractional shortfall of $A_f$ from its ideal value. Op-amps are modelled as a differential input resistance $R_{id}$, a controlled voltage source $A\,v_d$ and an output resistance $R_o$; small-signal transistor models use $g_m$ and $r_o$ only.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-05.1 [A]

**Closed-loop gain.** An amplifier with $A$ = 5000 has feedback with β = 0.1. Find the loop gain, the closed-loop gain and the gain error.

### Problem 12-05.2 [A]

**How much loop gain?** A closed-loop gain of 10 must be within 0.01% of its ideal value. Find the minimum loop gain and the minimum open-loop gain.

### Problem 12-05.3 [A]

**Bandwidth from a data sheet.** An op-amp has an open-loop gain of 130 dB and a gain–bandwidth product of 10 MHz, with a single pole. Find the open-loop pole frequency, and the closed-loop bandwidth at gains of 100 and 1.

### Problem 12-05.4 [A]

**Name the topology.** Identify the mixing and sampling in each circuit, and the kind of amplifier it is: (a) a non-inverting op-amp amplifier; (b) a photodiode transimpedance amplifier, where the photodiode's current enters the op-amp's inverting input and a resistor connects the output back to that input; (c) an op-amp whose output drives the gate of a transistor, with a sense resistor in the transistor's source connected back to the op-amp's inverting input, and the load in the drain; (d) an amplifier whose output current flows through a small resistor to ground, with a resistor from the top of that small resistor back to a current-driven input node.

### Problem 12-05.5 [B]

**Riding out a 3:1 gain spread.** An op-amp's gain varies by a factor of 3 between its slowest and fastest corners. The closed-loop gain may vary by no more than 0.05% across that range. Find the minimum loop gain at the slow corner, and the open-loop gain it needs with β = 0.01.

### Problem 12-05.6 [B]

**Series–shunt impedances.** An op-amp with $R_{id}$ = 2 MΩ, $R_o$ = 50 Ω and $A$ = 2 × 10⁵ is used as a non-inverting amplifier with a gain of 10. Estimate the closed-loop input and output resistances with the topology rules.

### Problem 12-05.7 [B]

**A photodiode transimpedance amplifier.** A photodiode with a shunt resistance of 1 MΩ drives the inverting input of an op-amp with $A$ = 10⁴ (infinite input resistance, zero output resistance); the non-inverting input is grounded and $R_F$ = 100 kΩ connects output to inverting input. Find the return ratio, the transresistance by the asymptotic-gain formula, and the input resistance by Blackman's formula.

### Problem 12-05.8 [B]

**An inverting amplifier with loading.** An op-amp with $A$ = 1000, $R_{id}$ = 10 kΩ and $R_o$ = 1 kΩ is wired as an inverting amplifier with $R_1$ = 1 kΩ and $R_2$ = 10 kΩ. Find (a) the loop gain a naive "$A\beta$ with β = $R_1/(R_1 + R_2)$" would give; (b) the true return ratio at the op-amp's controlled source; (c) $A_\infty$ and $A_0$; (d) the closed-loop gain and its error from −10.

### Problem 12-05.9 [B]

**The follower as a feedback circuit.** A source follower has $g_m$ = 2 mA/V, $r_o$ = 20 kΩ and a 10 kΩ load, driven from an ideal source. Find its return ratio, its gain by the asymptotic-gain formula, and the resistance at the source node (load included) by Blackman's formula. Compare with $1/g_m \parallel r_o \parallel R_L$.

### Problem 12-05.10 [B]

**Buying bandwidth with gain.** An amplifier has $A_0$ = 2000 and a single pole at 50 kHz. Find the feedback factor for a closed-loop bandwidth of 10 MHz, the resulting closed-loop gain, and the gain–bandwidth product.

### Problem 12-05.11 [C]

**Example 12-05.4 with $r_o$.** Repeat Example 12-05.4 with $r_o$ = 40 kΩ: find the return ratio, $A_\infty$, $A_0$, the transresistance, and the input and output resistances.

### Problem 12-05.12 [C]

**Exact degeneration from the asymptotic gain.** For Example 12-05.6's degenerated stage ($g_m$ = 2 mA/V, $R_S$ = 1 kΩ, $r_o$ = 50 kΩ), find the short-circuit transconductance exactly with the asymptotic-gain formula, taking the output as the drain current into a short.

### Problem 12-05.13 [C]

**Designing the loop.** A series–shunt amplifier needs a closed-loop gain of 20 with an error of at most 0.05% and a bandwidth of at least 1 MHz, using a single-pole op-amp. Find the minimum loop gain and open-loop gain, and, at that open-loop gain, the minimum pole frequency and gain–bandwidth product.

### Problem 12-05.14 [A]

**What feedback cleans up.** An amplifier with 1% second-harmonic distortion at 1 V output and an input-referred noise of 10 nV/√Hz is placed in a loop with $T$ = 49 and a closed-loop gain of 10. Estimate the second harmonic at the same output level, and the noise density at the output.

---

## Objective coverage

| Learning objective (chapter 12-05) | Problems |
|---|---|
| 1. Closed-loop gain, loop gain, error and sensitivity | 1, 2, 5, 13 |
| 2. Bandwidth, distortion and what feedback does not fix | 3, 10, 13, 14 |
| 3. The four topologies and their impedances | 4, 6, 7, 9 |
| 4. Return ratio and the asymptotic-gain formula | 7, 8, 9, 11, 12 |
| 5. Blackman's impedance formula | 7, 9, 11 |
