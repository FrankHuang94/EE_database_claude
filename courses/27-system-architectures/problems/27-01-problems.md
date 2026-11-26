# Problems 27-01 · Method: Analyzing a System End to End

Chapter: [27-01](../chapters/27-01-system-analysis-method.md) · Worked solutions: [27-01 solutions](../solutions/27-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** All component values are assumed. Battery-side power is load power divided by converter efficiency; an LDO's efficiency is at most $V_{out}/V_{in}$. Thermal problems use one dominant time constant. Dynamic power scales as $f^3$ under voltage–frequency scaling (14-01).

---

## Problems

### Problem 27-01.1 [A]

**A two-rail tree.** A 2.0 W processor core runs from a 90% buck converter on a 3.85 V battery; 0.3 W of I/O runs at 1.8 V through an LDO from the battery. Find (a) the LDO's best efficiency, (b) the battery-side power, (c) the system efficiency and the total loss.

### Problem 27-01.2 [A]

**Which budget binds?** For each product, name the budget most likely to bind first and say why in one sentence: (a) a wireless earbud; (b) a fanless tablet playing a game for an hour; (c) an AI accelerator serving a large language model to one user at a time; (d) a low-cost IoT sensor sold in millions.

### Problem 27-01.3 [B]

**Duty cycles.** A device draws 3.0 W (battery side) when active for 10% of the time and 0.25 W in standby the rest of the time; its battery holds 15 Wh, 90% usable. Find (a) the average power and the battery life, and (b) the battery life if standby power is halved, and if active power is halved instead. Which is worth more here?

### Problem 27-01.4 [B]

**A laptop's sustained power.** A laptop processor's junction may reach 100 °C in 35 °C air. With the fan on, junction-to-ambient resistance is 2.6 °C/W; with the fan off, 6.5 °C/W. Find the sustained power in each case.

### Problem 27-01.5 [B]

**How long can it burst?** A handheld has a thermal capacitance of 45 J/°C and a surface-to-ambient resistance of 5.0 °C/W in 25 °C air, and its surface must stay at or below 42 °C. It sits at a steady 1.0 W. Find (a) the time constant and the starting surface temperature, (b) how long a 6.0 W burst can last, and (c) the sustained power.

### Problem 27-01.6 [B]

**An NPU on a roofline.** A phone NPU peaks at 40 TOPS (INT8) with 64 GB/s of memory bandwidth. Find (a) its ridge point, (b) the rate for a convolution layer of intensity 900 operations/byte, (c) the rate and fraction of peak for a transformer decode step of intensity 2 operations/byte, and (d) the decode speed of a 3-billion-parameter model with 4-bit weights.

### Problem 27-01.7 [B]

**Serving a large model.** Using Example 27-01.3's accelerator (400 TFLOP/s, 3.2 TB/s), find (a) the single-user decode speed of a 70-billion-parameter model with 8-bit weights, and (b) the number of users that must be batched to reach the ridge point, if the intensity is 2 FLOP per byte per user.

### Problem 27-01.8 [B]

**A packet pipeline.** A network processor's four stages handle 10, 8, 12 and 9 Gb/s. Packets are 1,500 bytes, and each spends 2.0 ms in the device. Find (a) the throughput and bottleneck, (b) the packet rate, and (c) the packets in flight and the buffer memory they need.

### Problem 27-01.9 [B]

**A wearable BOM.** A smartwatch's BOM ($): SoC 18; memory 6; display 22; sensors 12; battery 4; PMIC and RF 9; mechanical 15; other 10. Assembly, test and royalties add $14; it sells for $249 (net to the maker). Find (a) the BOM, COGS and gross margin, (b) the display's share of the BOM, and (c) the COGS reduction needed for a 60% gross margin at the same price.

### Problem 27-01.10 [B]

**Amdahl and the NPU.** In an app, 40% of the time runs on work an NPU can accelerate 20 times; the rest stays on the CPU. Find (a) the overall speedup, (b) the limit if the NPU were infinitely fast, and (c) the speedup if the CPU part also becomes 1.25 times faster.

### Problem 27-01.11 [C]

**Is the wider core worth it?** Under a fixed power cap with $P_{dyn} \propto f^3$: (a) derive the condition $g > p^{1/3}$ for a change that multiplies IPC by $g$ and dynamic power at fixed frequency by $p$; (b) evaluate a change with $g$ = 1.10 and $p$ = 1.40; (c) evaluate a change with $g$ = 1.08 and $p$ = 1.20.

### Problem 27-01.12 [C]

**Sanity-check an efficiency claim.** An edge NPU is claimed to deliver 50 TOPS at 1 W. (a) What energy per operation does that imply, in femtojoules? (b) If every operation needed one byte from HBM-class memory at about 3.9 pJ/bit [R-459], what would the memory energy per operation be, and how many times the compute energy? (c) What does the claim therefore require of the design?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Decomposition and budget trees | 2, 9 |
| 2. Power trees and battery life | 1, 3 |
| 3. Sustained and burst thermal limits | 4, 5 |
| 4. Bottlenecks: roofline, pipelines, Amdahl, Little | 6, 7, 8, 10, 12 |
| 5. BOM roll-up and shadow prices | 9, 11 |
