# Problems 10-10 · Op-Amp Application Circuits

Chapter: [10-10](../chapters/10-10-op-amp-application-circuits.md) · Worked solutions: [10-10 solutions](../solutions/10-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** op-amps ideal unless a limit is given; comparator outputs swing 0 to $V_{DD}$; single-pole op-amps $A(s) = \omega_t/s$ in TIA problems; data-sheet values as quoted in the chapter.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-10.1 [A]

**A low-grade difference amplifier.** A difference amplifier with $K$ = 2 uses 1% resistors. Find its worst-case CMRR as a ratio and in dB, and the output error for a 2 V common-mode input.

### Problem 10-10.2 [A]

**Setting an INA's gain.** For the INA333 ($G = 1 + 100\text{ kΩ}/R_G$), find $R_G$ for gains of 10 and 1000.

### Problem 10-10.3 [A]

**Schmitt thresholds.** A non-inverting Schmitt trigger on 3.3 V has $V_{ref}$ = 1.65 V, $R_1$ = 10 kΩ and $R_2$ = 330 kΩ. Find its thresholds and hysteresis.

### Problem 10-10.4 [B]

**An inverting Schmitt trigger.** The input drives a comparator's − input. Its + input connects through $R_1$ = 10 kΩ to $V_{ref}$ = 2.5 V and through $R_2$ = 240 kΩ to the output (0 or 5 V). Find the + input voltage, and so the switching thresholds, for each output state, and the hysteresis. Which threshold applies to a rising input?

### Problem 10-10.5 [B]

**Offset and bias current in an integrator.** An integrator has $R$ = 100 kΩ and $C$ = 100 nF; the op-amp has $V_{OS}$ = 0.5 mV and $I_B$ = 10 nA into the − input. (a) With the input grounded, find the output ramp rate. (b) A 10 MΩ leak resistor is added. Find the output offset and the new lower corner.

### Problem 10-10.6 [B]

**A slow precision rectifier.** A precision rectifier uses an op-amp with SR = 0.5 V/µs and diodes dropping 0.7 V. Find the dead time and the missed voltage for a 1 V peak sine at 1 kHz and 20 kHz.

### Problem 10-10.7 [B]

**An open-drain output.** An open-drain comparator on 3.3 V drives a 15 pF load through a 10 kΩ pull-up. (a) Find the time constant and the 10–90% rise time. (b) What pull-up gives a 50 ns rise time, and what current does it draw when the output is low?

### Problem 10-10.8 [B]

**A high-gain receiver without compensation.** A TIA has $R_F$ = 1 MΩ, $C_{in}$ = 5 pF and an op-amp of GBW 50 MHz. Find $f_0$ and $Q$ without a feedback capacitor.

### Problem 10-10.9 [C]

**Compensating it.** For Problem 10-10.8's TIA: (a) find $C_F$ for $Q = 1/\sqrt2$ by solving the loop equation; (b) find $f_0$, and the transimpedance's −3 dB bandwidth; (c) compare with the approximation $\sqrt{2(C_{in} + C_F)/(\omega_tR_F)}$.

### Problem 10-10.10 [C]

**CMRR at frequency.** A unity-gain difference amplifier has perfectly matched 10 kΩ resistors, but 1 pF more stray capacitance across one input resistor than across its partner. Treating the mismatch as a ratio error $\delta(f) = 2\pi fR\,\Delta C$, find the CMRR at 60 Hz and at 50 kHz.

### Problem 10-10.11 [B]

**INA offset at high gain.** An INA333 at $G$ = 1000 reads a bridge whose full-scale differential output is 1 mV. Find the maximum input-referred offset, the output offset and the offset as a fraction of full scale.

### Problem 10-10.12 [B]

**Timing error from delay.** A comparator with 47 ns propagation delay detects the zero crossings of a 1 MHz sine. Find the phase error, and explain how to reduce it without a faster comparator.

---

## Objective coverage

| Learning objective (chapter 10-10) | Problems |
|---|---|
| 1. Difference and instrumentation amplifier CMRR | 1, 2, 10, 11 |
| 2. Integrator with offset and leak | 5 |
| 3. Precision rectifier and slew rate | 6 |
| 4. Schmitt triggers and comparators | 3, 4, 7, 12 |
| 5. Transimpedance amplifier stability | 8, 9 |
