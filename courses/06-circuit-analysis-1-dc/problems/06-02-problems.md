# Problems 06-02 · Circuit Elements and Ohm's Law

Chapter: [06-02](../chapters/06-02-circuit-elements-and-ohms-law.md) · Worked solutions: [06-02 solutions](../solutions/06-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** passive sign convention unless stated. Copper (IACS): $\rho$ = 1.7241 µΩ·cm at 20 °C, $\alpha$ = 0.00393 /°C. Diode: $I_s = 10^{-14}$ A, $V_T$ = 25.852 mV. E12 values per decade: 1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-02.1 [A]

**Ohm's law both ways.** (a) A 2.2 kΩ resistor has 3.3 V across it. Find its current and power. (b) A resistor of conductance 10 mS carries 50 mA. Find its voltage and power.

### Problem 06-02.2 [A]

**Reading i–v characteristics.** Identify each element from its i–v characteristic (voltage on the horizontal axis, current on the vertical) and give its parameters: (a) the vertical line $v = 0$; (b) the horizontal line $i = 0$; (c) a straight line through the origin with slope 2 mA/V; (d) the vertical line $v$ = 3.3 V; (e) a straight line from (0 V, 4 mA) to (8 V, 0 mA), where $i$ is the current *delivered* by the element.

### Problem 06-02.3 [A]

**Allowed or not?** Say whether each connection of ideal elements has a solution, and why: (a) two 5 V voltage sources in parallel, + to +; (b) a 5 V and a 3.3 V source in parallel, + to +; (c) two 1 mA current sources in series, pointing the same way; (d) a 1 mA and a 2 mA current source in series, pointing the same way; (e) a 1 mA current source with nothing connected across it; (f) a 9 V voltage source with a wire across its terminals; (g) a 9 V voltage source in series with a 1 mA current source and a 1 kΩ resistor in a single loop. (h) a 1 mA current source in series with an ideal switch, when the switch opens; (i) an ideal closed switch connected directly across a 9 V voltage source.

### Problem 06-02.4 [A]

**Preferred values.** (a) What is the step ratio between neighbouring E12 values, and between E96 values? (b) Which E12 value is closest (in ratio) to a calculated 4.1 kΩ? (c) The E96 values near 4.1 kΩ are 4.02 kΩ and 4.12 kΩ. Which is closer? (d) Explain why E24 pairs naturally with ±5% tolerance.

### Problem 06-02.5 [B]

**An extension cord.** A 20 m extension cord has two copper conductors of 2.08 mm² cross-section (14 AWG). It carries 10 A to a heater at 20 °C. (a) Find the resistance of the round trip. (b) Find the voltage lost in the cord and the power it dissipates. (c) What would the loss be at 100 A, and why are cords rated for a maximum current?

### Problem 06-02.6 [B]

**A thermometer made of copper.** A motor winding of copper wire measures 2.000 Ω at 20 °C. After an hour of running, it measures 2.400 Ω. Assuming the whole winding is at one temperature, how hot is it?

### Problem 06-02.7 [B]

**A supply's internal resistance.** A power supply delivers 2.0 A at 11.6 V and 5.0 A at 11.0 V. (a) Find its open-circuit voltage and internal resistance. (b) Find its short-circuit current and give its current-source (Norton) form. (c) What is its terminal voltage at 8.0 A?

### Problem 06-02.8 [B]

**Rating a resistor for the worst case.** A 1.0 kΩ ±5% resistor sits across a 12 V ±10% supply. (a) Find the maximum and minimum power it can dissipate. (b) Ratings of 1/8, 1/4 and 1/2 W are available. Which is the smallest that keeps the resistor at or below half its rating in the worst case?

### Problem 06-02.9 [B]

**Drift with temperature.** A 10.00 kΩ resistor is used from 25 °C to 125 °C. (a) Find its value at 125 °C if it is a thick-film part with TCR +100 ppm/K, and if it is a thin-film part with +25 ppm/K. (b) Two such thick-film resistors form a voltage divider with a 1:1 ratio. If both have exactly +100 ppm/K, what happens to the ratio at 125 °C? (c) If one has +100 ppm/K and the other −100 ppm/K (both within a ±100 ppm/K specification), by how much does the ratio $R_1/R_2$ change?

### Problem 06-02.10 [B]

**A resistor on a chip.** An integrated resistor is drawn in polysilicon with sheet resistance 200 Ω/□ (illustrative) and width 1.00 µm. (a) What length gives 10.0 kΩ? (b) Lithography makes the width 0.95 µm or 1.05 µm instead (the length stays as drawn). Find the resistance in each case. (c) Why do analog designers draw precision on-chip resistors wider than the minimum width?

### Problem 06-02.11 [C]

**Sizing a current-sense shunt.** A battery-management circuit must measure up to 20 A. Its amplifier and converter accept up to 100 mV across the shunt. (a) What is the largest shunt resistance that keeps the signal within range? (b) What power does a 5 mΩ shunt dissipate at 20 A? (c) A 5 mΩ, ±1%, ±35 ppm/°C four-terminal shunt is specified at 25 °C, used uncalibrated, and operated up to 85 °C. What is its worst-case resistance error, tolerance and temperature together? (d) A 0.5 mΩ, ±1%, ±350 ppm/°C shunt from the same family is considered instead. Find its signal at 20 A, its power and its worst-case error over the same range, and weigh the choice.

### Problem 06-02.12 [C]

**Three cells in parallel.** Two cells at 4.0 V and one at 3.7 V, each with 60 mΩ internal resistance, are connected in parallel with no load. (a) Find the common terminal voltage. (b) Find each cell's current. (c) Find the heat in the internal resistances and check the power balance.

### Problem 06-02.13 [C]

**Static and incremental resistance.** For the diode $i = I_s(e^{v/V_T} - 1)$: (a) find $v$, the static resistance $v/i$ and the incremental resistance $dv/di$ at 1 mA and at 10 mA; (b) a 1 mV change is added to the diode voltage at the 1 mA point. By about how much does the current change? (c) Which resistance would you use to predict (b), and why?

### Problem 06-02.14 [B]

**Two wires or four.** An ohmmeter measures a 0.100 Ω current-sense resistor through test leads of 0.050 Ω each. (a) What does a two-wire measurement read, and what is its error? (b) A four-wire (Kelvin) measurement passes the test current through one pair of leads and measures the voltage with another pair that carries essentially no current. What does it read, and why? (c) For a 10 kΩ resistor, how large is the two-wire error?

### Problem 06-02.15 [B]

**Short and open.** A 12 V supply has 0.1 Ω internal resistance. (a) Its output is shorted. Find the current and the power dissipated inside the supply. (b) Its output is left open. Find the terminal voltage and the power. (c) Real bench supplies limit their output current. With a 5 A limit, what output voltage and current does the shorted supply show?

---

## Objective coverage

| Learning objective (chapter 06-02) | Problems |
|---|---|
| 1. Element laws, i–v characteristics and switches | 2, 3, 13, 15 |
| 2. Ohm's law and power | 1, 8, 15 |
| 3. Resistance from geometry and temperature | 5, 6, 10 |
| 4. Real sources and impossible connections | 3, 7, 12, 15 |
| 5. Choosing real resistors and worst case | 4, 8, 9, 11, 14 |
