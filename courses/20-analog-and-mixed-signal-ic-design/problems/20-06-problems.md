# Problems 20-06 · Data Converter Fundamentals

Chapter: [20-06](../chapters/20-06-data-converter-fundamentals.md) · Worked solutions: [20-06 solutions](../solutions/20-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Transition levels $T_k$ are measured from the bottom of the range; ideally $T_k = (k - \tfrac12)\Delta$. DNL and INL use the endpoint definition unless stated. ENOB = (SINAD − 1.76)/6.02. $kT$ = 4.1419 × 10⁻²¹ J (300 K). Problems marked *(lab)* can be checked with `labs/20-06-lab/adc.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-06.1 [A]

**Ideal SNR.** Find the ideal SQNR for a full-scale sine at 8, 10, 14 and 16 bits, and for a 16-bit converter with a sine at −6 dBFS.

### Problem 20-06.2 [A]

**Reading ENOB.** A data sheet gives SINAD = 70.2 dB for a −1 dBFS input. Find the ENOB as measured and normalized to a full-scale input.

### Problem 20-06.3 [B]

**A missing code.** A 3-bit ADC with a 0.8 V range (LSB 100 mV) has transition levels 48, 150, 262, 390, 390, 548 and 655 mV. Find the offset and gain errors, $\Delta_{avg}$, the DNL of codes 1 to 6, the endpoint INL at each transition, and identify any missing code.

### Problem 20-06.4 [A]

**INL from DNL.** A 3-bit converter's DNL for codes 1 to 6 is +0.2, −0.4, +0.5, −0.1, +0.3 and −0.5 LSB. Find the endpoint INL at transitions 1 to 7, and its worst case.

### Problem 20-06.5 [B]

**MSB matching.** What relative error of the MSB capacitor gives a mid-scale DNL of 0.5 LSB in a 10-bit, 12-bit and 14-bit binary-weighted SAR?

### Problem 20-06.6 [C]

**Matching sets the capacitor.** Unit capacitors in an illustrative process have a relative mismatch of 1% for 1 µm² (scaling as $1/\sqrt{\text{area}}$) and a density of 1 fF/µm². (a) What is the mismatch of a 2 µm × 2 µm unit? (b) For a 10-bit SAR with a mid-scale DNL of 0.1 LSB rms, find the unit mismatch, unit area, unit capacitance and total DAC capacitance. (c) Compare with the 104 fF per side that kT/C requires at 10 bits (Problem 20-05.1). Which constraint sets the capacitor?

### Problem 20-06.7 [B]

**Planning a histogram test.** A 10-bit ADC with a 1.0 V range is tested with a sine 1% above full scale. (a) How many samples give 1000 counts in a mid-scale code? (b) How many counts does a code at 95% of the full-scale amplitude then receive?

### Problem 20-06.8 [B]

**Random phases and INL.** For the test of Problem 20-06.7, but with 10⁶ samples at random phases, find the standard deviation of the mid-scale transition level estimated from the cumulative histogram, in LSB. What should the tester do instead?

### Problem 20-06.9 [B]

**From a spectrum.** An FFT test with a −1.0 dBFS input shows: total noise (excluding signal and harmonics) at −72.5 dBFS, HD2 at −80 dBc, HD3 at −76 dBc, and a non-harmonic spur at −88 dBFS. Find SNR (dBc and dBFS), THD, SINAD, SFDR (dBc) and ENOB, both as measured and normalized to full scale.

### Problem 20-06.10 [A]

**Coherent sampling.** For $f_s$ = 250 MS/s and an 8192-point FFT, find the coherent input frequency closest to 70 MHz with an odd number of cycles. Confirm that it is co-prime with the record length.

### Problem 20-06.11 [B]

**Noise density.** An ADC has 65 dBFS of SNR at 1 GS/s. Find its noise spectral density, its SNR within a 20 MHz channel, and how many bits of resolution the narrower band gains.

### Problem 20-06.12 [C]

**INL shape and harmonics.** A 12-bit converter with a 1.6 V range ($A$ = 0.8 V) has a static nonlinearity $v' = v - a_3v^3$ (with $v$ measured from mid-scale). (a) Show that its endpoint INL is $a_3v(A^2 - v^2)$ and find its peak in terms of $a_3A^3$. (b) What $a_3$ gives HD3 = −70 dBc for a full-scale sine, and what is the peak INL then, in LSB? (c) Conversely, what HD3 does an S-shaped INL of exactly 1 LSB peak produce?

### Problem 20-06.13 [B]

**Ranking converters.** Compute the Walden and Schreier figures for three converters, taking the Nyquist rate as twice the bandwidth: C1 (SNDR 50 dB, 5 GHz bandwidth, 100 mW); C2 (SNDR 70 dB, 50 MHz, 1 mW); C3 (SNDR 100 dB, 20 kHz, 100 µW). Rank them by each figure and explain the difference.

### Problem 20-06.14 [C]

**The thermal limit.** (a) Using $P/f_s = 8kT\cdot\text{SNR}$, find the minimum power of an ideal 16-bit converter (SNR 98.1 dB) at 1 MS/s and of an ideal 12-bit converter (74.0 dB) at 1 GS/s. (b) Repeat §3.6's derivation for a class-A driver whose supply current is constant and equal to the sine's peak current $CA\omega$ at the Nyquist frequency. By what factor does the minimum power rise over the ideal class-B driver at the same frequency, what is the limit on $\text{FoM}_S$, and how far is it below the survey's 191.8 dB line?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Quantization noise and signal statistics | 1 |
| 2. Static errors, DNL, INL, mismatch | 3, 4, 5, 6, 12 |
| 3. Histogram testing | 7, 8 |
| 4. Dynamic metrics, dBc and dBFS, NSD | 2, 9, 10, 11 |
| 5. Figures of merit and the thermal limit | 13, 14 |
