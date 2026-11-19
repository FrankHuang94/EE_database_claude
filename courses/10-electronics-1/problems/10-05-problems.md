# Problems 10-05 · Amplifier Fundamentals

Chapter: [10-05](../chapters/10-05-amplifier-fundamentals.md) · Worked solutions: [10-05 solutions](../solutions/10-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** amplifiers are unilateral unless stated; $i_o$ flows into the load; voltage and current gains in dB are $20\log_{10}|A|$, power gains $10\log_{10}A_p$. Data-sheet values are those quoted in the chapter.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-05.1 [A]

**Decibel fluency.** Express in dB: (a) a power ratio of 2; (b) a voltage ratio of 2; (c) a power ratio of 1000; (d) a voltage ratio of $1/\sqrt2$. (e) Convert a 26 dB voltage gain to V/V. (f) What power is 10 dBm? (g) What rms voltage is 0 dBm across 50 Ω?

### Problem 10-05.2 [A]

**Ideal terminals.** For each of the four amplifier models, state the ideal input and output resistance and explain each in one sentence using a voltage or current divider.

### Problem 10-05.3 [A]

**A loaded stage.** An amplifier has $A_{vo}$ = 50, $R_i$ = 20 kΩ and $R_o$ = 500 Ω. Find the overall gain from a 2 kΩ source into a 1 kΩ load, in V/V and dB.

### Problem 10-05.4 [B]

**Converting a transconductance amplifier.** A transconductance amplifier has $G_m$ = 20 mS, $R_i$ = 5 kΩ and $R_o$ = 25 kΩ. (a) Find the equivalent $A_{vo}$, $R_m$ and $A_{is}$. (b) Find the overall voltage gain from a 1 kΩ source into a 25 kΩ load.

### Problem 10-05.5 [B]

**Bench measurements.** (a) An amplifier's output reads 1.20 V rms open-circuit and 0.90 V rms into 600 Ω. Find $R_o$. (b) A 50 mV source drives the input through a 47 kΩ series resistor, and the input reads 30 mV. Find $R_i$.

### Problem 10-05.6 [B]

**Order matters.** Stage X has $R_i$ = 1 MΩ, $A_{vo}$ = 10, $R_o$ = 10 kΩ; stage Y has $R_i$ = 2 kΩ, $A_{vo}$ = 100, $R_o$ = 100 Ω. The source has $R_{sig}$ = 50 kΩ and the load is 1 kΩ. Find the overall gain for the order X → Y and for Y → X, and explain the difference.

### Problem 10-05.7 [B]

**Class-A swing and efficiency with a MOSFET.** A common-source stage runs from $V_{DD}$ = 12 V with $R_D$ = 2 kΩ. To stay in saturation, the drain must not fall below 1.0 V. (a) Biased at $I_D$ = 3 mA, find the largest symmetric swing, the signal power in $R_D$ and the efficiency. (b) Find the bias current that maximizes the symmetric swing, and the swing, power and efficiency there.

### Problem 10-05.8 [B]

**Coupling capacitors on a data sheet.** The TPA3116D2 at 26 dB has a 30 kΩ input impedance with ±20% tolerance, and its data sheet recommends 3.3 µF coupling capacitors [chapter source 1]. Ignoring the source resistance: (a) find the corner frequency at the nominal impedance; (b) at the minimum impedance; (c) find the capacitor that keeps the corner at 2 Hz at the minimum impedance.

### Problem 10-05.9 [B]

**Full power.** The TPA3116D2 is set to 26 dB and delivers 50 W into 4 Ω. (a) Find the voltage gain in V/V. (b) Find the peak and rms output voltages. (c) Find the rms input that produces full power. (d) At 90% efficiency, how much power does the amplifier dissipate? (e) How much would an ideal resistively loaded class-A stage dissipate at the same output?

### Problem 10-05.10 [C]

**A bilateral amplifier.** A two-port has $y_{11}$ = 0.1 mS, $y_{12}$ = −0.01 mS, $y_{21}$ = 40 mS and $y_{22}$ = 0.05 mS (the $y_{12}$ could come from a 100 kΩ feedback resistor). It drives $R_L$ = 10 kΩ. (a) Find the voltage gain $v_2/v_1$. (b) Find the input resistance predicted by the unilateral model ($1/y_{11}$) and the actual input resistance, and the actual one with the output open. (c) From a 1 kΩ source, find the overall gain predicted unilaterally and the actual gain.

### Problem 10-05.11 [C]

**How many stages?** A 50 kΩ source must be amplified by at least 60 dB into a 2 kΩ load. Available: buffers B ($R_i$ = 1 MΩ, $A_{vo}$ = 0.95, $R_o$ = 200 Ω) and gain stages G ($R_i$ = 5 kΩ, $A_{vo}$ = 30, $R_o$ = 3 kΩ). (a) Find the gain of G-G-G, B-G-G-B and G-G-G-B. (b) Find the gain of B-G-G-G. (c) What is the fewest number of gain stages that can meet the specification, and where must the buffer go? Explain from the interface dividers.

### Problem 10-05.12 [C]

**Efficiency at real listening levels.** (a) A class-A stage reaches its 25% limit at full output. What is its efficiency at a tenth of full output power? (b) Model a class-D amplifier as dissipating a fixed idle power of 0.24 W (20 mA at 12 V) plus 1/9 of its output power (so that it is 90% efficient when idle loss is negligible). Find its efficiency at 1 W and at 10 W output. (c) What upper limit does the idle loss alone put on efficiency at 1 W?

---

## Objective coverage

| Learning objective (chapter 10-05) | Problems |
|---|---|
| 1. Gains and decibels | 1, 3, 9 |
| 2. The four models and conversion | 2, 4 |
| 3. Loading and cascades | 3, 4, 6, 11 |
| 4. Measuring resistances; unilateral limits | 5, 10 |
| 5. Swing and coupling corners | 7, 8 |
| 6. Efficiency and amplifier classes | 7, 9, 12 |
