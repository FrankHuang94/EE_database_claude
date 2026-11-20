# Problems 12-10 · Noise in Circuits

Chapter: [12-10](../chapters/12-10-noise-in-circuits.md) · Worked solutions: [12-10 solutions](../solutions/12-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** one-sided spectral densities; $T$ = 300 K unless stated; $k$ = 1.380649 × 10⁻²³ J/K, $q$ = 1.602176634 × 10⁻¹⁹ C, $V_T$ = 25.852 mV; MOSFET γ = 2/3; uncorrelated sources add in power.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-10.1 [A]

**Cooling a resistor.** Find the noise density of a 10 kΩ resistor at 300 K and at 77 K (liquid nitrogen).

### Problem 12-10.2 [A]

**Series and parallel.** Find the noise density of 1 kΩ and 3 kΩ resistors in series, and in parallel.

### Problem 12-10.3 [A]

**A photodiode.** A photodiode carries 10 nA. Find its shot-noise density and its RMS noise current in a 1 kHz bandwidth.

### Problem 12-10.4 [B]

**kT/C.** Find the kT/C noise of a 10 pF capacitor, and the capacitance needed for 10 µV RMS.

### Problem 12-10.5 [B]

**Flicker noise at DC.** A precision amplifier has a white floor of 10 nV/√Hz and a flicker corner at 1 kHz. Find its integrated noise from 0.1 Hz to 10 Hz: the flicker part, the white part and the total.

### Problem 12-10.6 [B]

**A bipolar input.** A bipolar transistor runs at $I_C$ = 100 µA with β = 100. Find $g_m$, its equivalent noise resistance, its input voltage noise density and its base-current shot noise.

### Problem 12-10.7 [B]

**Sizing a MOSFET for noise.** What $g_m$ gives a MOSFET an input-referred thermal noise of 2 nV/√Hz, and what drain current does that need at 0.2 V overdrive?

### Problem 12-10.8 [B]

**A two-stage chain.** Stage 1 has 2 nV/√Hz of input noise and a gain of 10; stage 2 has 10 nV/√Hz. Find the input-referred noise. Repeat with a first-stage gain of 3.

### Problem 12-10.9 [B]

**An op-amp with a 10 kΩ source.** An op-amp has $e_n$ = 5 nV/√Hz and $i_n$ = 2 pA/√Hz, driven from 10 kΩ. Find the source's thermal noise, the current-noise term, the total input noise and the noise figure. Find the optimum source resistance and the minimum noise figure.

### Problem 12-10.10 [B]

**A 14-bit ADC.** For a 2 V full-scale, 14-bit ADC, find the LSB, the quantization noise and the sampling capacitance whose kT/C noise equals it.

### Problem 12-10.11 [C]

**Designing a low-noise stage.** Design a common-source stage (γ = 2/3) for 1.5 nV/√Hz of input-referred noise, with its load contributing 10% of the noise power. Find the equivalent noise resistance, $g_m$, $R_D$ and the resulting gain.

### Problem 12-10.12 [C]

**Noise bandwidth.** White noise of 4 nV/√Hz passes through a first-order low-pass filter with a 10 kHz corner. Find the filter's equivalent noise bandwidth and the RMS output noise, and explain why the noise bandwidth exceeds the −3 dB bandwidth.

---

## Objective coverage

| Learning objective (chapter 12-10) | Problems |
|---|---|
| 1. Noise densities and integrated noise | 1, 2, 3, 5, 12 |
| 2. kT/C noise and sampling capacitors | 4, 10 |
| 3. Input-referred noise of stages and chains | 6, 7, 8, 11 |
| 4. Voltage and current noise, noise figure | 9 |
| 5. Data-sheet interpretation | 5, 9 |
