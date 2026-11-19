# Problems 06-08 · Thévenin and Norton Equivalents

Chapter: [06-08](../chapters/06-08-thevenin-and-norton.md) · Worked solutions: [06-08 solutions](../solutions/06-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $V_{th} = v_a - v_b$ open-circuited; $I_N$ flows out of terminal a through a short to b; dependent sources stay on when finding $R_{th}$. With resistances in kΩ and voltages in V, currents come out in mA. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-08.1 [A]

**Conversions.** (a) Give the Norton equivalent of 9 V in series with 3 kΩ. (b) Give the Thévenin equivalent of 20 mA in parallel with 250 Ω. (c) A network has an open-circuit voltage of 2.4 V and a short-circuit current of 8 mA. Find $R_{th}$.

### Problem 06-08.2 [A]

**Seen from one resistor.** In Example 06-07.1's circuit (12 V in series with 4 Ω to node a, 6 Ω from a to ground, 2 A pushed into a), remove the 6 Ω resistor and find the Thévenin equivalent of the rest at its terminals. Reconnect the 6 Ω and confirm $v_a$ = 12 V.

### Problem 06-08.3 [A]

**Loading.** A source has $V_{th}$ = 5 V and $R_{th}$ = 50 Ω. Find the load voltage and the loading error (the shortfall from 5 V, in percent) for loads of 50 Ω, 450 Ω and 4950 Ω. What load ratio gives a 1% error?

### Problem 06-08.4 [B]

**A strain-gauge bridge into an amplifier.** The quarter bridge of Example 06-03.4 (2.5 V excitation, three 350 Ω arms and an active gauge of 350.7 Ω at the bottom left) is read by an amplifier with 10 kΩ input resistance. (a) Find the bridge's Thévenin equivalent at its output terminals. (b) Find the voltage the amplifier sees and the loading loss in percent. (c) What input resistance would keep the loss below 0.1%?

### Problem 06-08.5 [B]

**An emitter follower's output.** A bipolar transistor ($\beta$ = 100, $r_\pi$ = 2.5 kΩ) has its collector at small-signal ground and $R_E$ = 1 kΩ from emitter to ground; the base is driven from a source with $R_s$ = 1 kΩ. The output is the emitter. (a) Find the open-circuit voltage gain (the Thévenin voltage per volt of source). (b) Find the output resistance with a test source. (c) Find the gain into a 100 Ω load.

### Problem 06-08.6 [B]

**A battery's equivalent.** A lithium-ion cell reads 3.70 V with no load and 3.58 V while delivering 2 A. (a) Find its Thévenin resistance. (b) Predict its terminal voltage at 5 A, the power lost inside it and the power delivered. (c) Why is the "equivalent" of a battery only approximately constant?

### Problem 06-08.7 [B]

**Two loads, with the meter included.** A sensor is measured with a 10 MΩ voltmeter alone (reading 4.99750 V) and with a 10 kΩ resistor connected across its output in addition to the meter (reading 3.33222 V). (a) Find $V_{th}$ and $R_{th}$, treating the meter as part of each load. (b) How large is the error if the meter's 10 MΩ is ignored? Compare with Example 06-08.5 and explain the difference.

### Problem 06-08.8 [B]

**PoE budgets.** (a) For 802.3af Type 1 (44 V minimum, 20 Ω worst-case loop, 15.4 W at the source) and 802.3at Type 2 Class 4 (50 V, 12.5 Ω, 30 W), find the current, the PD voltage and power, and the cable efficiency. (b) A Type 2 device that needs exactly 25.5 W is used on a 50 m cable (4-pair powering, 6.25 Ω) from a 50 V source. Find its voltage and current, and the power the source must deliver.

### Problem 06-08.9 [C]

**A constant-power load.** A 20 W constant-power load (a switching converter) is fed from $V_{th}$ = 12 V behind $R_{th}$ = 1 Ω. (a) Show that the load voltage satisfies $v^2 - V_{th}v + PR_{th} = 0$ and find both solutions. Which is the normal operating point? (b) Find the largest power the source can deliver, and the load voltage at that power. (c) What happens if the load demands more?

### Problem 06-08.10 [C]

**The Norton view of an amplifier stage.** The degenerated MOSFET of Example 06-06.2 ($g_m$ = 2 mS, $r_o$ = 50 kΩ, $R_S$ = 1 kΩ) is viewed at its drain, with $R_D$ removed. (a) Find the Norton current (short-circuit drain current) per volt of gate input. (b) Its Norton resistance is the output resistance found in Problem 06-06.8. Use the Norton equivalent to find the gain with $R_D$ = 10 kΩ, and compare with Example 06-06.2.

### Problem 06-08.11 [B]

**Cascaded stages.** A sensor (1 V behind 10 kΩ) drives an amplifier with 100 kΩ input resistance, a voltage gain of 10 (an ideal VCVS) and 100 Ω output resistance, which drives a 1 kΩ load. (a) Find the overall gain from the sensor's open-circuit voltage to the load. (b) Repeat with a 10 MΩ input resistance. (c) Which interface dominates the loss in each case?

### Problem 06-08.12 [B]

**A DAC's output equivalent.** For the 3-bit DAC of Example 06-07.5 with $R_L$ removed: (a) find its Thévenin resistance (all bit lines are voltage sources, 0 V or 4 V); (b) find its Thévenin voltage for code 101; (c) reconnect $R_L$ = 4 kΩ and confirm the 2.5 V of Example 06-07.5. Why does a DAC's output resistance matter to whatever it drives?

---

## Objective coverage

| Learning objective (chapter 06-08) | Problems |
|---|---|
| 1. The theorems and conversions | 1, 2, 10 |
| 2. Finding the equivalent by each method | 2, 4, 5, 10, 12 |
| 3. Loading and interfaces | 3, 4, 8, 11, 12 |
| 4. Measuring an equivalent | 6, 7 |
| 5. Limits: internal power, nonlinear loads | 6, 9 |
