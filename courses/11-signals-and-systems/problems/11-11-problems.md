# Problems 11-11 · Modulation and Filtering Applications

Chapter: [11-11](../chapters/11-11-modulation-and-filtering-applications.md) · Worked solutions: [11-11 solutions](../solutions/11-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** messages band-limited to $W$; carriers $\cos(2\pi f_ct)$; high-side LO unless stated; filter orders from the standard analog design formulas.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-11.1 [A]

**Occupied band.** Audio with 10 kHz bandwidth DSB-SC modulates a 1 MHz carrier. Give the occupied band and its width.

### Problem 11-11.2 [A]

**Phase error.** A coherent demodulator's carrier is 60° out of phase. By what factor, and by how many decibels, is the output reduced?

### Problem 11-11.3 [A]

**Reading the index.** A conventional AM signal modulated by a tone has an envelope that swings between 0.5 V and 1.5 V. Find the modulation index and the unmodulated carrier amplitude.

### Problem 11-11.4 [A]

**An FM receiver's image.** A broadcast receiver with a 10.7 MHz IF and high-side LO is tuned to 98.1 MHz. Find the LO and image frequencies.

### Problem 11-11.5 [B]

**AM power.** A transmitter's unmodulated carrier power is 10 W. With tone modulation at $m$ = 0.8, find the total power, the sideband power and the efficiency.

### Problem 11-11.6 [B]

**An envelope detector.** For $m$ = 0.8 and a 10 kHz tone on a 455 kHz IF, find the largest $RC$ that avoids diagonal clipping and compare it with the IF period.

### Problem 11-11.7 [B]

**A drifting carrier.** A coherent demodulator's carrier is 0.5 Hz off. Describe the output and find the time between nulls.

### Problem 11-11.8 [B]

**Mixer products.** A 900 MHz signal is mixed with a 1000 MHz LO. List the output frequencies, say which is the IF in a receiver, and find the image frequency.

### Problem 11-11.9 [B]

**Stacking voice channels.** Twelve voice channels, each 3.1 kHz wide, are frequency-division multiplexed with 0.9 kHz guard bands. What spacing and total bandwidth result, and what sets the guard band?

### Problem 11-11.10 [B]

**Choosing a family.** A filter must pass 0–10 kHz with at most 1 dB of loss and attenuate by 60 dB from 20 kHz. Find the minimum order for Butterworth, Chebyshev type I and elliptic designs.

### Problem 11-11.11 [B]

**SNR for a gigabit.** What SNR does the Shannon bound require to carry 1 Gb/s in 80 MHz?

### Problem 11-11.12 [C]

**Picking an IF.** An AM receiver tuned to 600 kHz has a single tuned front end with $Q$ = 30. What is the smallest IF (high-side LO) that gives 40 dB of image rejection?

---

## Objective coverage

| Learning objective (chapter 11-11) | Problems |
|---|---|
| 1. DSB-SC and coherent demodulation | 1, 2, 7 |
| 2. Conventional AM and envelope detection | 3, 5, 6 |
| 3. Mixers, images and superheterodyne receivers | 4, 8, 12 |
| 4. Filter families | 9, 10 |
| 5. Link capacity | 11 |
