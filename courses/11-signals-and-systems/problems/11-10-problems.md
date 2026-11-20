# Problems 11-10 · Sampling, Aliasing and Reconstruction

Chapter: [11-10](../chapters/11-10-sampling-aliasing-reconstruction.md) · Worked solutions: [11-10 solutions](../solutions/11-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** ideal sampling at $f_s = 1/T$ unless stated; $\operatorname{sinc}(u) = \sin(\pi u)/(\pi u)$; Butterworth filters have $\lvert H\rvert^2 = 1/[1 + (f/f_c)^{2n}]$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-10.1 [A]

**Rates.** A sensor signal is band-limited to 4 kHz. (a) What is its Nyquist rate? (b) It is sampled at 10 kHz: what is the Nyquist frequency, and how wide is the gap between the band edge and the first copy's lower edge?

### Problem 11-10.2 [A]

**Folding.** At $f_s$ = 1 kHz, find the apparent frequencies of tones at 600 Hz, 1100 Hz, 1900 Hz and 2450 Hz.

### Problem 11-10.3 [A]

**A phase flip.** $\cos(2\pi \cdot 700t + 30°)$ is sampled at 1 kHz. Write the sampled sequence as a cosine at a frequency below 500 Hz, with its phase.

### Problem 11-10.4 [A]

**Hold droop.** Find the zero-order hold's gain (relative to DC) at $f_s/4$ and at $f_s/2$, as ratios and in decibels.

### Problem 11-10.5 [B]

**Two tones, two rates.** $x(t) = \cos(2\pi \cdot 3\,\text{kHz}\,t) + \cos(2\pi \cdot 7\,\text{kHz}\,t)$. List the frequencies present in $[0, f_s/2]$ after sampling at (a) 8 kHz and (b) 12 kHz. (c) Above what sample rate do both tones appear at their true frequencies?

### Problem 11-10.6 [B]

**An ECG anti-aliasing filter.** An ECG band of 0–150 Hz is sampled at 500 SPS and needs 40 dB of attenuation at the first alias frequency. With a Butterworth filter at $f_c$ = 150 Hz, find the minimum order. Repeat for 4 kSPS. What does the comparison suggest?

### Problem 11-10.7 [B]

**Noise folding in volts.** An amplifier's noise is 20 nV/√Hz, flat to 1 MHz, and is sampled at 100 kSPS. Find the RMS noise in the samples without any filter and with an ideal filter at 50 kHz, and the difference in decibels.

### Problem 11-10.8 [B]

**CD-rate reconstruction.** A DAC runs at 44.1 kHz with a zero-order hold. Find the droop at 20 kHz and the level of the first image of a 20 kHz tone (where is it?), relative to DC and relative to the tone.

### Problem 11-10.9 [B]

**A three-point average at 1 kSPS.** $y[n] = \frac13(x[n] + x[n - 1] + x[n - 2])$ runs on samples at 1 kSPS. (a) Find its effective gain for a 100 Hz input. (b) What happens to an input at 900 Hz with no anti-aliasing filter? (c) Which input frequency below 500 Hz does it remove completely?

### Problem 11-10.10 [B]

**Sinc interpolation.** Samples at $T$ = 1 ms are $x[0] = 1$ and zero elsewhere. Find the ideally reconstructed $x_r(t)$ at $t$ = 0.5 ms and $t$ = 1.5 ms.

### Problem 11-10.11 [B]

**Undersampling an FM IF.** A 10.7 MHz IF is 200 kHz wide (10.6–10.8 MHz). Find the band-pass sampling window for $n$ = 54, $n$ = 50 and $n$ = 40, and the width of each window. What does the trend mean for the clock?

### Problem 11-10.12 [C]

**A jitter budget.** An ADC must reach 70 dB SNR for a full-scale sine at 100 MHz, and the clock is the only noise source. Find the largest allowed RMS jitter. Repeat for 1 GHz.

### Problem 11-10.13 [C]

**Oversampling instead of bits.** An ideal 12-bit ADC is oversampled by 64 and digitally filtered to the original band. Find the SNR before and after, and the equivalent number of bits.

### Problem 11-10.14 [C]

**Redesigning the ECG's RC filter.** In Example 11-10.7, the RC filter (4 kΩ effective) gives 23.7 dB at 127.95 kHz. Find the single-pole corner frequency and the capacitor needed for 40 dB there, and state the data sheet's warning about that choice.

---

## Objective coverage

| Learning objective (chapter 11-10) | Problems |
|---|---|
| 1. Sampled spectrum and the sampling theorem | 1, 5, 10 |
| 2. Aliasing of tones and noise | 2, 3, 5, 7, 9 |
| 3. Anti-aliasing filters and oversampling | 6, 7, 14 |
| 4. Reconstruction: sinc and zero-order hold | 4, 8, 10 |
| 5. DT processing, quantization, jitter, band-pass sampling | 9, 11, 12, 13 |
