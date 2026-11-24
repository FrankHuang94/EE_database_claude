# Problems 22-03 · Boost, Buck-Boost and Other Topologies

Chapter: [22-03](../chapters/22-03-boost-buck-boost-topologies.md) · Worked solutions: [22-03 solutions](../solutions/22-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Continuous conduction, ideal switches and small ripple unless stated. $D' = 1 - D$, $K = 2L/(RT_s)$. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-03-lab/topologies.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-03.1 [A]

**A 5 V to 12 V boost.** Find (a) the duty cycle, (b) the inductor current at a 0.5 A load and (c) the voltage the switch must block.

### Problem 22-03.2 [A]

**A negative rail.** An inverting buck-boost makes −15 V from 5 V. Find (a) the duty cycle, (b) the switch voltage and (c) the average inductor current at a 0.1 A load.

### Problem 22-03.3 [A]

**SEPIC and Ćuk.** From 24 V, a SEPIC makes +12 V and a Ćuk makes −12 V. Find (a) the duty cycle (the same for both) and (b) the voltage each switch must block.

### Problem 22-03.4 [B]

**A 12 V to 48 V boost.** *(lab)* At 2 A out, 250 kHz, 33 µH and 47 µF, find (a) the duty cycle, (b) the inductor current, (c) the inductor ripple, (d) the output ripple and (e) the output capacitor's RMS current.

### Problem 22-03.5 [B]

**Efficiency at a 4× step-up.** The boost of Problem 22-03.4 has a 20 mΩ inductor (switches ideal). Find (a) the $D'$ that holds 48 V at 2 A, (b) the duty cycle, (c) the efficiency and (d) the inductor current. (e) What is the largest gain this inductor allows into a 24 Ω load?

### Problem 22-03.6 [B]

**Two duty cycles for one gain.** A boost has $R_L$ = 0.05 Ω and $R$ = 20 Ω. (a) Where does its gain peak, and (b) what is the peak? (c) Find the larger $D'$ (the normal operating side) that gives a gain of 5, (d) its duty cycle and (e) its efficiency. (f) Why does the other solution exist, and why must a controller avoid it?

### Problem 22-03.7 [B]

**Staying in CCM.** (a) Find $K_{crit}$ for a boost at $D$ = 0.5. (b) A 12 V to 24 V, 1 A boost at 200 kHz must stay in CCM down to 10% load. What is the smallest inductance?

### Problem 22-03.8 [B]

**The boost's DCM ratio.** At $D$ = 0.3 and $K$ = 0.02, find the boost's conversion ratio.

### Problem 22-03.9 [B]

**Holding 3.3 V through a Li-ion discharge.** A four-switch buck-boost makes 3.3 V from a cell that falls from 4.2 V to 3.0 V. Find the duty cycle (a) in buck mode at 4.2 V and (b) in boost mode at 3.0 V. (c) At what cell voltage must it leave pure buck or pure boost operation?

### Problem 22-03.10 [B]

**Boost or buck-boost?** Make 12 V from 5 V. Find the active switch's stress, $V_{pk}I_{pk}/P_{out}$ with small ripple, for (a) a boost and (b) an inverting buck-boost making −12 V. (c) For the buck-boost, find the duty cycle.

### Problem 22-03.11 [C]

**The right-half-plane zero sets bandwidth.** A 12 V to 24 V boost uses a 22 µH inductor. Find the RHP-zero frequency $f_z = D'^2R/(2\pi L)$ at (a) 2 A and (b) 3 A. (c, d) If the loop crossover is kept at a fifth of $f_z$, what crossover does each load allow? (e) Which load sets the design?

### Problem 22-03.12 [C]

**A PFC boost at low line.** A 500 W PFC boost makes 400 V from a 90 V RMS line (assume unity power factor and no loss). At the line peak, find (a) the instantaneous input voltage, (b) the duty cycle and (c) the inductor current.

### Problem 22-03.13 [C]

**The boost's hot capacitor.** (a) Derive the boost's output-capacitor RMS current, $I\sqrt{D/D'}$, from its capacitor-current waveform with small ripple. (b) Evaluate the ratio of that RMS current to the load current at $D$ = 0.75.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Conversion ratios of boost, buck-boost, Ćuk and SEPIC | 1, 2, 3 |
| 2. Currents, ripples and stresses | 1, 2, 4, 12, 13 |
| 3. Resistance, efficiency and maximum gain | 5, 6 |
| 4. Boost DCM boundary and ratio | 7, 8 |
| 5. Topology selection: stress, range, RHP zero | 9, 10, 11, 12 |
