# Problems 07-06 · AC Power and Power Factor

Chapter: [07-06](../chapters/07-06-ac-power-and-power-factor.md) · Worked solutions: [07-06 solutions](../solutions/07-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** phasors are peak values unless labeled rms; mains voltages are RMS; passive sign convention. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-06.1 [A]

**RMS values.** Find the RMS value, as a multiple of the peak $A$, of (a) a sawtooth rising linearly from 0 to $A$ and dropping back each period, (b) a half-wave rectified sine of peak $A$, (c) a full-wave rectified sine of peak $A$.

### Problem 07-06.2 [A]

**Power from phasors.** A load has $\mathbf{V} = 100\angle20°$ V and $\mathbf{I} = 5\angle{-15°}$ A (peak). Find $S$, $P$, $Q$, the power factor and whether it is leading or lagging. Then write the instantaneous power $p(t)$, taking the current's phase as the time reference, and find its largest and smallest values.

### Problem 07-06.3 [A]

**An inductor's reactive power.** A 10 mH inductor carries 1 A (RMS) at 1 kHz. Find its real and reactive power.

### Problem 07-06.4 [B]

**Conservation of complex power.** A 230 V (RMS), 50 Hz source feeds, through a line of $0.2 + j0.4$ Ω, two loads in parallel: $Z_1 = 20 + j15$ Ω and $Z_2 = 30$ Ω. Find the line current, the load voltage, and the complex power of the source, the line and each load, and show that they balance.

### Problem 07-06.5 [B]

**Correcting a motor.** A 5 kW motor runs at power factor 0.70 lagging from 230 V (RMS), 50 Hz. Find the capacitance that corrects the power factor to 0.95 lagging, and the line current before and after.

### Problem 07-06.6 [B]

**How far to correct.** For the motor of Problem 07-06.5, find the capacitance needed for unity power factor, and for 0.95 *leading*. Compare all three capacitors and explain why engineers stop near 0.95 lagging.

### Problem 07-06.7 [B]

**A demand surcharge.** A tariff bills demand as measured kW × 0.90 / PF when the power factor is below 0.90. A customer draws 100 kW at PF 0.70. (a) What demand is billed? (b) How many kvar of capacitors bring the power factor to exactly 0.90?

### Problem 07-06.8 [B]

**Matching.** A source has $\mathbf{V}_{Th,rms} = 20\angle0°$ V and $Z_{Th} = 4 + j3$ Ω. Find the maximum average power any load can take, and the power taken by the best purely resistive load.

### Problem 07-06.9 [B]

**Harmonics and power factor.** A load on a sinusoidal 230 V (RMS) supply draws a fundamental current of 5 A (RMS) in phase with the voltage, plus 2 A (RMS) of third harmonic and 1 A (RMS) of fifth. Find the RMS current, the THD, the power factor and the real power.

### Problem 07-06.10 [B]

**Displacement and distortion together.** A load's current has its fundamental lagging the voltage by 30°, and a THD of 50%. Find its true power factor. What would a meter that assumes sinusoidal current report?

### Problem 07-06.11 [A]

**A data-center supply at half load.** A redundant data-center supply delivers 1.5 kW at 96% efficiency (the 80 PLUS Titanium requirement at 50% load, [R-122](../../../reference/research-log.md#r-122--power-factor-harmonics-and-utility-tariffs)) with power factor 0.95 from 230 V (RMS). Find its input power, its losses, its apparent power and its input current.

### Problem 07-06.12 [C]

**Why distribution voltage and power factor matter together.** A load of 50 kW is supplied through cables of 0.05 Ω total resistance. Find the cable loss at (a) 230 V and PF 1, (b) 230 V and PF 0.8, (c) 400 V and PF 0.8, still treated as a single-phase supply for comparison (in practice 400 V is a three-phase line-to-line voltage, 07-11). Express each loss as a percentage of the load power, and state the scaling law.

---

## Objective coverage

| Learning objective (chapter 07-06) | Problems |
|---|---|
| 1. Instantaneous and average power; reactive elements | 2 |
| 2. RMS values, harmonics, crest factor | 1, 9 |
| 3. Complex, real, reactive, apparent power; conservation | 2, 3, 4 |
| 4. Power factor (displacement, distortion); correction | 5, 6, 7, 9, 10 |
| 5. Maximum average power transfer | 8 |
| 6. Standards, utilities and supplies in practice | 7, 11, 12 |
