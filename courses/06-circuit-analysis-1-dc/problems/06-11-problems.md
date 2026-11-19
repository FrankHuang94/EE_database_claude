# Problems 06-11 · Practical DC Circuits and Measurement

Chapter: [06-11](../chapters/06-11-practical-dc-circuits-and-measurement.md) · Worked solutions: [06-11 solutions](../solutions/06-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** copper has ρ = 1.7241 × 10⁻⁸ Ω·m and α = 0.00393 /°C at 20 °C; 1 oz copper is 35 µm thick. Meters are modeled as the resistances stated. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-11.1 [A]

**Voltmeter loading.** A 10 V source with 100 kΩ of internal resistance is measured with (a) a 10 MΩ meter and (b) a 10 GΩ meter. Find each reading and its error.

### Problem 06-11.2 [A]

**Ammeter burden.** A 1.5 V source drives a 15 Ω load. An ammeter with 2 Ω internal resistance is inserted. Find the reading, its error, the burden voltage and the corrected current.

### Problem 06-11.3 [A]

**An accuracy specification.** A meter specified at ±(0.05% + 1) reads 12.47 V on a range with 0.01 V resolution. Find the uncertainty in millivolts and as a percentage of the reading.

### Problem 06-11.4 [B]

**Finding a source's resistance with a voltmeter.** A 10 MΩ meter reads 4.500 V across a high-resistance sensor. With a second 10 MΩ resistor connected in parallel with the meter, it reads 4.000 V. Find the sensor's Thévenin resistance and its open-circuit voltage.

### Problem 06-11.5 [B]

**Choosing a shunt.** A current of 0 to 5 A is measured with a shunt and an amplifier whose input full scale is 50 mV and whose offset is 50 µV. (a) Find the shunt resistance that uses the full scale and its dissipation at 5 A. (b) A 1 mΩ shunt is proposed instead. Find its full-scale signal and dissipation. (c) Express the amplifier's offset as a percentage of full scale in each case.

### Problem 06-11.6 [B]

**A board trace.** A trace in 1 oz copper is 0.5 mm wide and 40 mm long and carries 2 A. Find (a) the sheet resistance, the number of squares and the resistance at 20 °C; (b) the voltage drop and dissipation; (c) the resistance when the board is at 85 °C.

### Problem 06-11.7 [B]

**A shared return.** A sensor's 0–1 V output is read by an ADC whose ground connects to the sensor's ground through a 20 mΩ trace that also carries a motor's 3 A return current. Find the error voltage and its size as a percentage of full scale. Name two cures.

### Problem 06-11.8 [B]

**Measuring a 10 mΩ shunt.** A 10 mΩ shunt is measured with a two-wire ohmmeter whose leads and contacts total 0.1 Ω. (a) What does it read, and by what factor is the reading wrong? (b) A four-wire measurement forces 1 A. What voltage is sensed?

### Problem 06-11.9 [C]

**A 48 V bus monitor.** A bus nominally at 48 V is divided by $R_1$ = 140 kΩ (top) and $R_2$ = 10 kΩ (bottom), both ±1%, into an ADC with 1 MΩ input resistance and ±0.5% of reading accuracy. (a) Find the nominal ADC voltage with an ideal ADC. (b) Find the loading error the 1 MΩ input causes, and the nominal ADC voltage including it. (c) Ignoring loading (it is systematic and can be corrected), find the worst-case high and low errors of the divider ratio. (d) Combine them with the ADC's ±0.5% for the total worst case. (e) Repeat (c) and (d) with ±0.1% resistors.

### Problem 06-11.10 [B]

**Remote-sense headroom.** A supply with remote sensing can raise its output by at most 0.5 V above its set point to compensate lead drop. It must deliver 10 A. (a) What round-trip lead resistance can it compensate? (b) What is the longest pair (one-way length) of 16 AWG copper wire it can use at 20 °C? (c) Repeat (b) for 14 AWG, giving its diameter and resistance per meter.

### Problem 06-11.11 [C]

**Self-heating of a shunt.** A shunt in a 2512 four-terminal family (1.0 W at 70 °C; TCR ±250 ppm/°C for 1–2.9 mΩ, ±75 ppm/°C for 3–4.9 mΩ, ±35 ppm/°C for 5 mΩ–0.2 Ω) must measure 15 A. On this board the shunt's temperature rises 50 °C per watt. For a 2 mΩ part, find the dissipation, the temperature rise and the worst-case resistance change from self-heating. Can a 5 mΩ part be used? Evaluate a 3 mΩ part the same way and compare its signal with the 2 mΩ part's.

### Problem 06-11.12 [B]

**Readings that do not add up.** Three 1 MΩ resistors in series are connected across a 9 V source of negligible resistance. (a) What Thévenin resistance does a voltmeter see across any one resistor? (b) What does a 10 MΩ meter read across each, and what is the sum of the three readings? (c) What does a 10 GΩ meter read across each? Explain why the 10 MΩ readings do not sum to 9 V.

### Problem 06-11.13 [C]

**Copper in the sense path, and a current-measurement budget.** A 2 mΩ shunt (±0.5%, ±250 ppm/°C) measures 10 A. A layout error puts 0.02 mΩ of copper (α = 0.00393 /°C) inside the sense connection at each end. (a) Find the resistance the amplifier sees and the error at 25 °C. (b) Find the effective temperature coefficient of that resistance. (c) After a one-point calibration at 25 °C, the board heats by 40 °C. Find the worst-case drift with the misplaced taps and with correct Kelvin taps. (d) With Kelvin taps and no calibration, the budget is: shunt tolerance ±0.5%, shunt TCR over the 40 °C rise ±1.0%, amplifier gain ±0.3%, ADC ±0.2% of reading. Combine them by worst case and by RSS, and say which figure a datasheet guarantee may quote.

---

## Objective coverage

| Learning objective (chapter 06-11) | Problems |
|---|---|
| 1. Loading and burden | 1, 2, 4, 9, 12 |
| 2. Accuracy specifications and combining errors | 3, 5, 9, 13 |
| 3. Four-terminal (Kelvin) measurement | 8, 13 |
| 4. Wire and trace resistance, remote sensing | 6, 7, 10 |
| 5. Worst-case analysis of a measurement chain | 9, 11, 13 |
