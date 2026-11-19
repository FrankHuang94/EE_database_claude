# Problems 07-09 · Mutual Inductance and Transformers

Chapter: [07-09](../chapters/07-09-mutual-inductance-and-transformers.md) · Worked solutions: [07-09 solutions](../solutions/07-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** phasors are peak values unless labeled RMS; mains and transformer ratings are RMS; passive sign convention for each coil. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-09.1 [A]

**Signs from dots.** Coils with $L_1$ = 5 mH and $L_2$ = 20 mH have $M$ = 6 mH. At an instant $di_1/dt$ = 200 A/s and $di_2/dt$ = 100 A/s. Find $k$, and $v_1$ and $v_2$ (each in the passive sign convention with its own current) when (a) both currents enter their dotted terminals, (b) $i_1$ enters its dot and $i_2$ leaves its dot.

### Problem 07-09.2 [A]

**Measuring M.** Two coils of 20 mH and 30 mH are connected in series. One way round the series inductance measures 70 mH; reversed, 30 mH. Find $M$ and $k$.

### Problem 07-09.3 [A]

**An ideal step-down.** A 10:1 ideal transformer has 120 V (RMS) on its primary and a 12 Ω resistor on its secondary. Find the secondary voltage and current, the primary current and the resistance seen by the source.

### Problem 07-09.4 [B]

**Energy and the limit on k.** Coils with $L_1$ = 1 mH and $L_2$ = 4 mH have $M$ = 1.5 mH, connected so that their fluxes oppose. With $i_1$ = 2 A, find the value of $i_2$ that minimizes the stored energy and that minimum energy. What is $k$, and what would happen to the minimum if $M$ exceeded 2 mH?

### Problem 07-09.5 [B]

**T-equivalent and a shorted secondary.** For the coils of Example 07-09.1 ($L_1$ = 10 mH, $L_2$ = 40 mH, $M$ = 10 mH, aiding, common lower terminal), draw the T-equivalent and give its three inductances. Then find the impedance at the primary at 1 kHz with the secondary short-circuited.

### Problem 07-09.6 [B]

**Reflected impedance.** A secondary of $L_2$ = 1 mH feeds a 50 Ω resistor; the mutual inductance is 0.5 mH. Find the impedance reflected into the primary at 10 kHz, and its magnitude. Is it inductive or capacitive?

### Problem 07-09.7 [B]

**Matching a line.** A 600 Ω source of 1 V (RMS) open-circuit voltage must drive a 50 Ω load. Find the turns ratio for maximum power, the power delivered matched and the power delivered by a direct connection.

### Problem 07-09.8 [B]

**Tests.** A 10 kVA, 2400/240 V, 60 Hz transformer gives these test results. Open-circuit, on the low-voltage side: 240 V, 0.80 A, 60 W. Short-circuit, on the high-voltage side at rated current: 48 V, 180 W. Find the rated high-voltage current, $R_c$ and $X_m$ (low-voltage side), and $R_{eq}$ and $X_{eq}$ (high-voltage side).

### Problem 07-09.9 [B]

**The efficiency curve.** For the transformer of Problem 07-09.8, find the load fraction and the efficiency at maximum efficiency (unity power factor), and the efficiency at 25%, 50% and 100% load at power factors 1 and 0.8.

### Problem 07-09.10 [B]

**What the efficiency standard means in watts.** The US 2029 standard (§9) raises a 167 kVA single-phase liquid-immersed transformer from 99.33% to 99.46% at 50% load, and a 25 kVA unit from 98.95% to 99.00%. Assuming unity power factor, find each unit's losses at 50% load under both levels and the percentage cut in losses.

### Problem 07-09.11 [B]

**Regulation and power factor.** For the transformer of Problem 07-09.8 at full load, find the voltage regulation (approximately and exactly) for power factor 0.8 lagging and 0.8 leading. Why is the leading case smaller?

### Problem 07-09.12 [C]

**A wireless link.** Two identical coils of 24 µH, each with 0.2 Ω of resistance, transfer power at 360 kHz (the Qi Magnetic Power Profile frequency, §9) to a 5 Ω load. The secondary is tuned by a series capacitor to resonance. (a) Find the tuning capacitance. (b) For $k$ = 0.25, 0.1 and 0.03, find the reflected resistance and the link efficiency (power to the load over power into the primary coil). (c) For $k$ = 0.25 without the tuning capacitor, find the reflected impedance and the efficiency. What does tuning buy?

### Problem 07-09.13 [C]

**Turns, area and frequency.** A transformer winding must support 120 V (RMS) with a peak flux density no higher than 0.25 T (an assumed core limit). (a) On a 2 cm² core, how many turns are needed at 60 Hz and at 100 kHz? (b) At 100 kHz with 10 turns, what core area is needed? (c) What limits how far raising the frequency can shrink a transformer?

---

## Objective coverage

| Learning objective (chapter 07-09) | Problems |
|---|---|
| 1. Coupled-coil equations, the dot convention and series connections | 1, 2 |
| 2. Stored energy and k ≤ 1 | 4 |
| 3. Mesh analysis, reflected impedance, T-equivalent | 5, 6, 12 |
| 4. Ideal transformer and matching | 3, 7 |
| 5. Equivalent circuit, tests, efficiency, regulation | 8, 9, 11 |
| 6. Frequency, core material and coupling in products | 10, 12, 13 |
