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

**An op-amp with a 10 kΩ source.** An op-amp has $e_n$ = 5 nV/√Hz and $i_n$ = 2 pA/√Hz, driven from 10 kΩ at the standard $T_0$ = 290 K. Find the source's thermal noise, the current-noise term, the total input noise and the noise figure. Find the optimum source resistance and the minimum noise figure.

### Problem 12-10.10 [B]

**A 14-bit ADC.** For a 2 V full-scale, 14-bit ADC, find the LSB, the quantization noise and the sampling capacitance whose kT/C noise equals it.

### Problem 12-10.11 [C]

**Designing a low-noise stage.** Design a common-source stage (γ = 2/3) for 1.5 nV/√Hz of input-referred noise, with its load contributing 10% of the noise power. Find the equivalent noise resistance, $g_m$, $R_D$ and the resulting gain.

### Problem 12-10.12 [C]

**Noise bandwidth.** White noise of 4 nV/√Hz passes through a first-order low-pass filter with a 10 kHz corner. Find the filter's equivalent noise bandwidth and the RMS output noise, and explain why the noise bandwidth exceeds the −3 dB bandwidth.

### Problem 12-10.13 [B]

**Noise of an OTA and a folded cascode.** A five-transistor OTA has input devices of $g_{m1}$ = 1 mA/V and mirror devices of $g_{m3}$ = 0.5 mA/V, all with γ = 2/3 (flicker noise ignored). Find its input-referred noise density and equivalent noise resistance. A folded cascode with the same input pair has folding current sources of $g_m$ = 1 mA/V and a cascoded mirror load of 0.5 mA/V (the cascode devices' own noise is negligible). Find its noise density and the ratio of the two.

### Problem 12-10.14 [B]

**An op-amp circuit's noise and SNR.** A CMOS op-amp with $e_n$ = 10 nV/√Hz (its white floor) and negligible current noise is wired as a non-inverting amplifier of gain 10 with $R_1$ = 1 kΩ and $R_2$ = 9 kΩ, driven from a 1 kΩ source. (a) Find the input-referred noise density, the output noise density and the RMS output noise over 20 kHz (treat all sources as white). (b) Find the SNR for a 1 V RMS output. (c) Repeat (a)'s input density with $R_1$ = 10 kΩ and $R_2$ = 90 kΩ, and find how much SNR is lost.

### Problem 12-10.15 [A]

**Reading noise specifications.** (a) Convert an op-amp's 16 nV/√Hz into an equivalent noise resistance at 300 K. (b) A data sheet quotes 1.5 µV peak-to-peak from 0.1 to 10 Hz (an illustrative value). Find the RMS noise by the usual convention. (c) Using §9's fitted model of the TLV9062 (white floor 9.092 nV/√Hz, corner 2.1 kHz), find the RMS noise from 0.1 to 10 Hz and the peak-to-peak value the convention would quote.

---

## Objective coverage

| Learning objective (chapter 12-10) | Problems |
|---|---|
| 1. Noise densities and integrated noise | 1, 2, 3, 5, 12 |
| 2. kT/C noise and sampling capacitors | 4, 10 |
| 3. Input-referred noise of stages and chains | 6, 7, 8, 11, 13 |
| 4. Voltage and current noise, noise figure | 9, 14 |
| 5. Data-sheet interpretation | 5, 9, 14, 15 |
