# Problems 12-08 · Op-Amp Internals

Chapter: [12-08](../chapters/12-08-op-amp-internals.md) · Worked solutions: [12-08 solutions](../solutions/12-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** square-law MOSFETs with $g_m = 2I_D/V_{ov}$ and $r_o = 1/(\lambda I_D)$; $I_{SS}$ is the input pair's tail current; two-stage op-amps follow chapter §3.1 and 12-06 §3.5; $V_T$ = 25.852 mV.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-08.1 [A]

**Two-stage gain.** A two-stage op-amp has $g_{m1}$ = 0.2 mA/V, $R_1$ = 400 kΩ, $g_{m6}$ = 2 mA/V and $R_2$ = 40 kΩ. Find each stage's gain and the total, in V/V and decibels.

### Problem 12-08.2 [A]

**Slew rate.** An op-amp has $I_{SS}$ = 50 µA and $C_c$ = 2 pF. Find its internal slew rate and the time it needs to slew 2 V.

### Problem 12-08.3 [A]

**Full-power bandwidth.** An op-amp slews at 10 V/µs. Up to what frequency can it deliver a 2 V-peak sine without slew distortion?

### Problem 12-08.4 [B]

**Slew rate from GBW.** An op-amp has a 20 MHz GBW. Find its internal slew rate if its input pair is MOS with $V_{ov}$ = 0.15 V, and if it is an undegenerated bipolar pair.

### Problem 12-08.5 [B]

**Degenerating a bipolar input pair.** A bipolar input pair runs each transistor at 50 µA. What emitter resistor quadruples $\text{SR}/\omega_u$? What does it cost?

### Problem 12-08.6 [B]

**Which edge limits?** A two-stage op-amp has $I_{SS}$ = 50 µA, $C_c$ = 2 pF, $I_7$ = 200 µA and $C_L$ = 10 pF. Find the internal and output-stage slew limits, say which edge is limited by which, and find the $I_7$ that would balance them.

### Problem 12-08.7 [B]

**Folded-cascode gain.** A folded cascode has $g_{m1}$ = 1 mA/V. Looking up from the output: a PMOS cascode with $g_m$ = 1 mA/V and $r_o$ = 100 kΩ above a folding node of resistance 50 kΩ. Looking down: an NMOS cascode with $g_m$ = 1 mA/V and $r_o$ = 100 kΩ on a current source of $r_o$ = 100 kΩ. Find $R_{up}$, $R_{dn}$, $R_{out}$ and the estimated gain.

### Problem 12-08.8 [B]

**Folded-cascode speed.** The amplifier of Problem 12-08.7 drives 3 pF, and its folding node has 0.4 pF with a cascode $g_m$ of 1 mA/V. Find the GBW, the folding-node pole and the estimated phase margin at unity gain.

### Problem 12-08.9 [B]

**Common-mode feedback.** A fully differential version of Problem 12-08.7's amplifier has 100 µA pull-up and pull-down currents that mismatch by 0.5%. Find the common-mode shift without CMFB, and the CMFB loop gain and residual error with $g_{m,cm}$ = 0.2 mA/V.

### Problem 12-08.10 [B]

**Complementary input range.** A 3.3 V complementary input stage has $V_{TH}$ = 0.6 V, input overdrive 0.2 V and tail overdrive 0.2 V for both pairs. Find the common-mode range of each pair and the overlap. By what factor does $g_m$ change across the range with constant tail currents?

### Problem 12-08.11 [C]

**A two-stage design.** Design a two-stage op-amp for a 20 MHz GBW and about 60° of phase margin into 4 pF, with both stages at $V_{ov}$ = 0.2 V. Using the rules $C_c = 0.22C_L$ and $g_{m6} = 10g_{m1}$, find $C_c$, $g_{m1}$, $g_{m6}$, $I_{SS}$, $I_6$ and both slew limits.

### Problem 12-08.12 [C]

**Checking the design.** For Problem 12-08.11's design with λ = 0.1 V⁻¹ (so $R_1 = r_o/2$ at $I_{SS}/2$ and $R_2 = r_o/2$ at $I_6$) and 0.15 pF at node 1, find $R_1$, $R_2$ and the DC gain. The exact solution gives a phase margin of 59.97° at a crossover of 17.59 MHz. Why is the crossover below the 20 MHz target?

---

## Objective coverage

| Learning objective (chapter 12-08) | Problems |
|---|---|
| 1. Two-stage gain, GBW and phase margin | 1, 11, 12 |
| 2. Slew rate and its link to GBW | 2, 3, 4, 5, 6, 11 |
| 3. The folded cascode | 7, 8 |
| 4. Fully differential amplifiers and CMFB | 9 |
| 5. Rail-to-rail input stages | 10 |
