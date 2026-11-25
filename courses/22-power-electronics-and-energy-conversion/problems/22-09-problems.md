# Problems 22-09 · Batteries, Charging and Fuel Gauging

Chapter: [22-09](../chapters/22-09-batteries-charging-fuel-gauging.md) · Worked solutions: [22-09 solutions](../solutions/22-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** "The teaching cell" is the chapter's 300 mAh cell: $V_{OC} = 3.30 + 0.90z$ V, $R_0$ = 0.20 Ω, $R_1$ = 0.10 Ω, $C_1$ = 200 F, $Q$ = 1080 C, charge voltage 4.20 V. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-09-lab/battery.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-09.1 [A]

**A phone cell's ratings.** A 4500 mAh phone cell has a 3.87 V nominal voltage and weighs 70 g (assumed). Find (a) its energy, (b) its specific energy and (c) the current at 0.7C.

### Problem 22-09.2 [A]

**Lithium iron phosphate from first principles.** An LFP cell averages 3.3 V. Find (a) the Gibbs energy released per mole of lithium, and (b) the theoretical specific capacity of LiFePO₄ (molar mass 157.76 g/mol) for one lithium per formula unit.

### Problem 22-09.3 [B]

**A camera-flash pulse.** *(lab)* A phone cell at 3.75 V OCV has $R_0$ = 0.08 Ω, $R_1$ = 0.05 Ω and $C_1$ = 400 F (assumed). It supplies 2 A for 10 s. Ignoring the SOC change, find the terminal voltage (a) at the first instant, (b) at 10 s, (c) just after the load is removed, and (d) 10 s after that.

### Problem 22-09.4 [B]

**Heavy load, cold cell.** For the teaching cell at 600 mA, with the 3.30 V cutoff and the quasi-static resistance of Example 22-09.3, find the usable fraction of capacity (a) at 25 °C ($R$ = 0.30 Ω) and (b) at −10 °C ($R$ = 1.20 Ω). (c) At −10 °C, what current still allows 90% of the capacity to be used?

### Problem 22-09.5 [B]

**A gentle charge.** *(lab)* The teaching cell is charged from empty at 0.5C, terminating at C/20 ($R$ = 0.30 Ω). Find (a) the SOC at the end of CC, (b) the CC time, (c) the CV time, (d) the total time and (e) the SOC at termination.

### Problem 22-09.6 [C]

**Charging an aged cell.** After years of use the teaching cell's resistance has doubled to 0.60 Ω (ignore its capacity loss). For a 1C charge terminating at C/10, find (a) the SOC at the end of CC, (b) the CC time, (c) the CV time constant, (d) the CV time, (e) the total time and (f) the SOC at termination. Compare with Example 22-09.4.

### Problem 22-09.7 [A]

**A wearable's linear charger.** A linear charger takes 5.0 V and charges a 4.0 V cell at 60 mA. Find (a) its dissipation and (b) its efficiency. Why is a linear charger acceptable here?

### Problem 22-09.8 [B]

**Direct charging.** A phone charges its 3.8 V battery at 6 A through a 2:1 switched-capacitor charger with 97% efficiency (assumed). Find (a) the battery power, (b) the input power and (c) the loss in the phone. (d) What would a 92%-efficient buck charger dissipate for the same charge?

### Problem 22-09.9 [B]

**A voltage gauge under load.** A gauge reads the teaching cell's terminal voltage under a 300 mA load ($R$ = 0.30 Ω) and looks it up as OCV. (a) By how much does it misjudge the SOC? (b) Repeat for a flatter cell whose OCV rises only 0.15 V over its whole range. With IR correction using a resistance that is 20% wrong, what are the residual errors (c) for the teaching cell and (d) for the flat cell?

### Problem 22-09.10 [B]

**The sense resistor's tradeoff.** A coulomb counter's amplifier has a 1 µV input offset. With a 10 mΩ sense resistor, find (a) the current offset, (b) the charge error it accumulates per day, and (c) that error as a share of the teaching cell's capacity. (d) What sense resistance would reduce the offset to 10 µA, and what would it (e) dissipate and (f) drop at 300 mA?

### Problem 22-09.11 [C]

**Calendar aging.** A cell loses 4% of its capacity in its first 6 months at 25 °C, and its loss follows the square-root law. Find the loss (a) after 2 years and (b) after 5 years. (c) If the growth constant follows an Arrhenius law with an activation energy of 0.5 eV (assumed), by what factor does it rise from 25 °C to 35 °C, and (d) what is the 2-year loss at 35 °C?

### Problem 22-09.12 [B]

**Cycles against calendar.** A cell retains 80% of its capacity after 1000 full cycles, and assume its cycle fade is linear. Counting one full cycle per charge, find the capacity left from cycling alone after 2 years for (a) a watch charged daily and (b) a ring charged every 5 days, and (c) the ring's number of cycles in those 2 years. Compare (b) with Problem 22-09.11(a).

### Problem 22-09.13 [C]

**A ring that must last a week.** A ring has a 22.5 mAh cell and must last 7 days on an aged cell at 80% of rated capacity on a cold day that strands another 10%. (a) What average current is allowed? (b) The sensors, radio, processor and converters average 85 µA: how much is left for the fuel gauge?

### Problem 22-09.14 [B]

**Capacity learning.** A gauge reads $z_1$ = 0.80 from the OCV after one rest and $z_2$ = 0.25 after the next, having counted 1.32 Ah of discharge between them. (a) What capacity does it learn, and (b) what state of health is that against a rated 2.6 Ah? (c) If each OCV reading may be off by ±0.005 in SOC, what are the largest overestimate and underestimate of the capacity, in per cent? (d) What is the smallest SOC swing between rests that keeps the overestimate within 2%? Why do gauges wait for deep discharges before updating their capacity?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Cell voltage, capacity and ratings | 1, 2 |
| 2. Equivalent circuit, pulses and usable capacity | 3, 4 |
| 3. CC/CV charging and charger architectures | 5, 6, 7, 8 |
| 4. Fuel-gauging errors and capacity learning | 9, 10, 14 |
| 5. Aging and wearable battery life | 11, 12, 13 |
