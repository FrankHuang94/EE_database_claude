# Problems 10-09 · Real Op-Amps: Non-Idealities

Chapter: [10-09](../chapters/10-09-real-op-amps-nonidealities.md) · Worked solutions: [10-09 solutions](../solutions/10-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** single-pole op-amps unless stated; noise gain $1 + R_2/R_1$; data-sheet values are those quoted in the chapter [1–3]; "worst case" adds magnitudes.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-09.1 [A]

**Noise gain and bandwidth.** With an op-amp of GBW 5 MHz, find the noise gain and the bandwidth of (a) an inverting amplifier of gain −4, (b) a non-inverting amplifier of gain +4, (c) a follower.

### Problem 10-09.2 [A]

**Decibel specifications.** (a) Convert a CMRR of 90 dB to a ratio and find the input-referred error for a 1 V common-mode change. (b) Convert a PSRR of 100 dB to µV/V.

### Problem 10-09.3 [A]

**Full-power bandwidth.** (a) An op-amp slews at 1 V/µs. Find its full-power bandwidth at 5 V peak. (b) What slew rate does a 10 V peak, 20 kHz sine need?

### Problem 10-09.4 [B]

**Gain error at DC and in band.** A non-inverting amplifier of gain 50 uses an op-amp with $A_0$ = 100 dB and GBW = 1 MHz. (a) Find the exact DC gain and its error. (b) Find the closed-loop bandwidth, and the magnitude error and phase lag at 10 kHz.

### Problem 10-09.5 [B]

**A large step.** A follower uses an op-amp with GBW 5 MHz and SR 2 V/µs. (a) Find τ and the largest step that does not slew. (b) For a 4 V step, find the slewing time and the time of the final exponential approach from the end of slewing to within 4 mV (0.1%). (c) Compare the total with the 0.1% settling time a purely linear response would have.

### Problem 10-09.6 [B]

**Bias-current compensation that helps less than expected.** An OPA1611 is used as an inverting amplifier with $R_1$ = 10 kΩ and $R_2$ = 100 kΩ, input grounded for this test. Using maximum values ($V_{OS}$ = 500 µV, $I_B$ = 250 nA, $I_{OS}$ = 175 nA [3]), find the output error contributions and worst-case totals (a) with the + input grounded and (b) with a compensating resistor $R_1 \parallel R_2$ in the + input. Why does compensation help less here than the "cancels to $I_{OS}$" rule suggests?

### Problem 10-09.7 [B]

**Typical against guaranteed drift.** A TLV9062 has $V_{OS}$ = ±1.6 mV max at 25 °C, ±2 mV max over −40 to 125 °C, and a typical drift of ±0.53 µV/°C [1]. A design trims the offset at 25 °C. (a) Using the typical drift, how much can the offset move by 125 °C? (b) What change do the guaranteed values allow?

### Problem 10-09.8 [B]

**PSRR at frequency.** An op-amp's PSRR is 100 dB at DC and falls 20 dB per decade above 100 Hz. A switching regulator puts 100 mV of ripple at 100 kHz on the supply. Find the PSRR at 100 kHz and the input-referred ripple.

### Problem 10-09.9 [B]

**Output current.** An OPA333 (±5 mA typical short-circuit current [2]) runs on 5 V with its output biased at midsupply. (a) What peak current does a 2 V peak sine require into 1 kΩ (returned to midsupply)? Compare it with the short-circuit current, and say why that comparison is not a design guarantee. (b) Budgeting at most half the typical short-circuit current for linear drive (a designer's assumption, not a data-sheet number), what is the largest sine into 100 Ω? (c) What peak current does a 2 V peak, 10 kHz sine need into a 10 nF capacitor?

### Problem 10-09.10 [C]

**An ADC driver.** A follower must settle a 2 V step to within 0.01% in 1 µs, using an op-amp with SR = 4 V/µs. (a) Find the minimum GBW, accounting for slewing. (b) For that GBW, find τ, the slew-to-linear boundary, the slewing time and the exponential time. (c) What GBW would be needed with no slew limit?

### Problem 10-09.11 [C]

**A drift budget.** A sensor produces 50 µV/°C, and a design must keep the amplifier's offset change below the equivalent of 0.1 °C over 0–70 °C. (a) Find the allowable offset change and drift. (b) Which of the three chapter parts meets it by guaranteed values?

### Problem 10-09.12 [B]

**Rail-to-rail input on 1.8 V.** A TLV9062 follower runs on 1.8 V. Up to what input voltage does it stay in its high-CMRR region, and what fraction of the supply is that? Suggest a configuration that keeps the inputs in that region for a full-range signal.

---

## Objective coverage

| Learning objective (chapter 10-09) | Problems |
|---|---|
| 1. Finite gain and noise gain | 1, 4 |
| 2. Bandwidth and in-band error | 1, 4, 10 |
| 3. Slew rate and full-power bandwidth | 3, 5, 10 |
| 4. DC error budget | 2, 6, 7, 8, 11 |
| 5. Ranges and output current | 9, 12 |
| 6. Data-sheet reading and part choice | 6, 7, 11 |
