# Problems 06-09 · Maximum Power Transfer

Chapter: [06-09](../chapters/06-09-maximum-power-transfer.md) · Worked solutions: [06-09 solutions](../solutions/06-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** sources are given or reduced to Thévenin form; efficiency is the fraction of the source's power that reaches the load. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-09.1 [A]

**Symmetric loads.** A source has $V_{th}$ = 6 V and $R_{th}$ = 300 Ω. (a) Find the maximum power and the load that receives it. (b) Find the power into 100 Ω and into 900 Ω. Why are they equal?

### Problem 06-09.2 [A]

**Efficiency and power.** A load is four times the source resistance. (a) What is the efficiency? (b) What fraction of the maximum power does the load receive? Check with $4\eta(1 - \eta)$.

### Problem 06-09.3 [A]

**A Norton source.** A current source of 10 mA in parallel with 2 kΩ drives a load. Find the maximum load power, the load that receives it and the load voltage.

### Problem 06-09.4 [B]

**Matching to earlier networks.** (a) What is the most power the divider network of Example 06-08.1 ($V_{th}$ = 4 V, $R_{th}$ = 3 kΩ) can deliver? (b) What is the most power the bridge of Example 06-08.2 ($V_{th}$ = 119.05 mV, $R_{th}$ = 1.0238 kΩ) can deliver to a meter, and what meter resistance receives it?

### Problem 06-09.5 [B]

**A 48 V battery pack.** A pack has 48 V open-circuit voltage and 0.25 Ω internal resistance. (a) Find its maximum power. (b) Find the load for 95% efficiency and the power it receives. (c) The pack is rated for 30 A. Find the load voltage, the power and the efficiency at 30 A.

### Problem 06-09.6 [B]

**Designing a source, not a load.** A 5 V USB supply must deliver 2 A to a device with at least 4.75 V at the device. (a) What is the largest allowed total resistance of the supply and cable? (b) What is the efficiency at that limit? (c) Why would matching the supply's resistance to the device make no sense?

### Problem 06-09.7 [B]

**Maximum power from an emitter follower.** The emitter follower of Problem 06-08.5 has $V_{th}$ = 0.9665 V per volt of input and $R_{th}$ = 33.49 Ω. Find the load and the maximum power per V² of input, and say what would limit the real circuit.

### Problem 06-09.8 [C]

**A negative source resistance.** A source has $V_{th}$ = 1 V and $R_{th}$ = −50 Ω (made with a dependent source, 06-06). (a) Find the load voltage and power for $R_L$ = 100 Ω and 60 Ω. (b) What happens as $R_L$ approaches 50 Ω? (c) Why does the formula $V_{th}^2/4R_{th}$ fail here?

### Problem 06-09.9 [B]

**A thermoelectric generator in changing conditions.** A TEG behaves as $V_{oc} = 40\ \text{mV/K}\times\Delta T$ behind a constant 4 Ω. (a) Find its maximum power at $\Delta T$ = 20 K and at 10 K. (b) A converter holds its input at a fixed 0.4 V. What does it get at each temperature difference? (c) A fixed 4 Ω load is used instead. What does it get? (d) What do (b) and (c) say about tracking the maximum-power point of a linear source?

### Problem 06-09.10 [C]

**Coax with PTFE.** For coax with a PTFE dielectric ($\varepsilon_r$ = 2.1): (a) find the impedances for minimum conductor loss and for maximum peak power; (b) for a 50 Ω PTFE line, find $b/a$ and its loss relative to the minimum and its power capacity relative to the maximum (both for the same outer diameter and dielectric).

### Problem 06-09.11 [B]

**An audio amplifier and its speaker.** An amplifier's output resistance is 0.05 Ω and it drives an 8 Ω speaker. (a) What fraction of the amplifier's output power reaches the speaker? (b) The "damping factor" is defined as $R_L/R_{out}$; find it. (c) Why would an 8 Ω output resistance (a "matched" amplifier) be a poor design?

### Problem 06-09.12 [C]

**Two sources feeding one load.** The two practical sources of Example 06-07.3 (12 V with 4 Ω and 6 V with 3 Ω, in parallel) feed a variable load. (a) Find the load for maximum power and that power. (b) Find each source's current at the matched load. Does either source absorb power?

---

## Objective coverage

| Learning objective (chapter 06-09) | Problems |
|---|---|
| 1. Deriving and applying the maximum | 1, 3, 4, 7, 8, 12 |
| 2. Efficiency and the power–efficiency tradeoff | 2, 5, 11 |
| 3. When to match and when not to | 6, 11 |
| 4. Coax optima and 50 Ω | 10 |
| 5. Energy harvesting | 9 |
