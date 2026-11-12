# Problems 00-01 · The Map of Electrical Engineering

Chapter: [00-01](../chapters/00-01-map-of-electrical-engineering.md) · Worked solutions: [00-01 solutions](../solutions/00-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard · **[C]** challenge. Values marked "illustrative" are realistic round numbers, not specifications of a particular product. Use $k = 1.381\times10^{-23}$ J/K.

---

## Problems

### Problem 00-01.1 [A]

For each product, name the two EE subdisciplines most central to its main function, and one chapter of this curriculum where each is developed: (a) a laptop charger; (b) a 5G base-station radio; (c) a datacenter AI accelerator; (d) an electric-vehicle traction inverter; (e) a hearing aid.

### Problem 00-01.2 [A]

A smartwatch battery is rated 300 mAh at 3.85 V (illustrative). Find its energy in Wh and in J, and the average power it can supply for a two-day battery life.

### Problem 00-01.3 [A]

A phone charger delivers 9 V at 2.22 A. What is its output power? How much energy does it deliver in 30 minutes, in kJ and in Wh?

### Problem 00-01.4 [B]

A network switch port carries 400 Gb/s and its electrical-plus-optical interface consumes about 15 pJ/bit (illustrative). What power does one port use? What do 64 ports use? Why do datacenter architects care?

### Problem 00-01.5 [B]

(a) Compute Landauer's limit at 77 K (liquid-nitrogen temperature).
(b) A future logic gate dissipates 0.1 fJ per operation. How many times the 300 K Landauer limit is that?

### Problem 00-01.6 [B]

Using $C = B\log_2(1 + \text{SNR})$ with SNR = 25 dB:

(a) find the capacity of an 80 MHz channel;
(b) find the capacity of a 160 MHz channel at the same SNR;
(c) find the capacity of the 80 MHz channel if the SNR is doubled.

Which upgrade helps more?

### Problem 00-01.7 [B]

WSTS reports 2025 sales of \$795.6 B, up 26.2% ([R-016](../../../reference/research-log.md#r-016--global-semiconductor-market-wsts--sia)).

(a) What were 2024 sales?
(b) Logic was \$299.5 B and analog \$86.5 B. What is the ratio of logic to analog?
(c) Give one reason why the two segments might grow at very different rates.

### Problem 00-01.8 [B]

From [R-017](../../../reference/research-log.md#r-017--rd-intensity-latest-fiscal-year-10-k--annual-reports): NVIDIA spent about \$18.5 B on R&D with about 42,000 employees; ADI spent about \$1.77 B with about 24,500 employees.

(a) Compute R&D spend per employee for each.
(b) Give two reasons why R&D per employee is a poor measure of engineering productivity.

### Problem 00-01.9 [C] (power budget)

A pair of smart glasses has a 0.6 Wh battery (illustrative) and draws an average of 0.75 W while in use.

(a) How long does it run?
(b) Engineers cut the average power to 0.5 W. How long now?
(c) Name three subdisciplines that would contribute to that 33% power reduction, and how.

### Problem 00-01.10 [C] (efficiency chain)

Power reaches an AI accelerator through four conversion stages with efficiencies 98% (utility transformer and switchgear), 96% (rack AC-DC power supply), 94% (rack DC-DC conversion) and 90% (the voltage regulators next to the chip). These are illustrative values.

(a) What is the end-to-end efficiency?
(b) To deliver 1 MW to the chips, how much power must the facility draw?
(c) How much power is lost as heat in conversion, before any computing happens?

---

## Objective coverage

| Learning objective (chapter 00-01) | Problems |
|---|---|
| 1. Subdisciplines and their questions | 1, 9 |
| 2. Energy, power, data rate, energy per bit | 2, 3, 4, 5, 10 |
| 3. Trace a product through the map | 1, 9 |
| 4. Industry size and structure from dated data | 7, 8 |
| 5. Unifying ideas (tradeoffs, frequency/Shannon) | 6, 9, 10 |
