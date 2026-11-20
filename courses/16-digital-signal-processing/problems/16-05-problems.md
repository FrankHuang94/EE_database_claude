# Problems 16-05 · Spectral Analysis and Windowing

Chapter: [16-05](../chapters/16-05-spectral-analysis-and-windowing.md) · Worked solutions: [16-05 solutions](../solutions/16-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Windows are periodic (DFT-even) with the figures of merit of §3.2; dB values for tones are relative to the fundamental unless marked dBFS; an "ideal" ADC has only quantization noise, $\text{SNR} = 6.02B + 1.76$ dB.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-05.1 [A]

**Which window?** Choose a window (rectangular, Hann, Blackman–Harris or flat-top) for each task, with a one-line reason: (a) measuring the amplitude of a tone of unknown frequency to 0.1 dB; (b) finding a −80 dBc spur 15 bins from a strong carrier; (c) resolving two equal tones 1.5 bins apart in a coherent test; (d) a general-purpose look at an unknown signal. Then give the noise bandwidth of one bin for a Blackman window with $N$ = 2048 at 48 kHz.

### Problem 16-05.2 [A]

**Undoing the window.** A 4096-point FFT with a 4-term Blackman–Harris window shows a peak of 367.4 for a tone on a bin. What is the tone's amplitude?

### Problem 16-05.3 [A]

**Where the floor sits.** An ideal 14-bit ADC is tested with a full-scale sine and a 16,384-point FFT (rectangular window). Find its SNR and the depth of the average noise floor below the tone.

### Problem 16-05.4 [B]

**ENBW of the Hann window.** Show from the definition that the periodic Hann window $w[n] = 0.5 - 0.5\cos(2\pi n/N)$ has $\sum w = N/2$, $\sum w^2 = 3N/8$ and therefore ENBW = 1.5 bins exactly.

### Problem 16-05.5 [B]

**From floor to SNR.** A data sheet plot shows a full-scale tone at 0 dBFS and an average noise floor at −120 dBFS in a 65,536-point FFT with a rectangular window. What SNR and ENOB does the converter actually have?

### Problem 16-05.6 [B]

**Record length for resolution.** Two equal tones 150 Hz apart must be resolved in audio sampled at 48 kHz. Using the −6 dB main-lobe widths of §3.3, what is the shortest record for a rectangular and for a Hann window, and the smallest power-of-2 FFT for each?

### Problem 16-05.7 [B]

**Averaging budget.** A noise spectrum must be estimated with a per-bin standard deviation of at most 10% of its mean, using 1024-point segments at 48 kHz without overlap. How many segments and how many seconds of data are needed?

### Problem 16-05.8 [B]

**A coherent test plan.** An ADC samples at 250 MS/s with $N$ = 32,768. Choose the coherent bin nearest 70 MHz, give the exact input frequency, and find the bins where the 2nd and 3rd harmonics land.

### Problem 16-05.9 [B]

**ENOB conventions.** A converter tested at −1 dBFS shows SINAD = 70.0 dB. Give its ENOB as measured and referred to full scale.

### Problem 16-05.10 [C]

**Combining distortion and noise.** A converter's harmonics are HD2 −85 dBc, HD3 −78 dBc, HD4 −95 dBc and HD5 −90 dBc, and its SNR is 72.0 dB. Find THD, SINAD and (if no other spur is larger) SFDR.

### Problem 16-05.11 [C]

**A spur 20 bins away.** A carrier falls halfway between bins of an 8192-point FFT. How far below the carrier's peak bin is its leakage 20 bins away with a rectangular window, and with 4-term Blackman–Harris?

### Problem 16-05.12 [C]

**Designing the measurement.** A −100 dBc spur sits 20 bins from a carrier in a system with 80 dB SNR, measured with an 8192-point FFT of a non-coherent record. With each of the rectangular and Blackman–Harris windows, how deep is the noise floor below the carrier, and can the spur be seen? (Use Problem 16-05.11 for leakage.)

---

## Objective coverage

| Learning objective (chapter 16-05) | Problems |
|---|---|
| 1. Leakage and window spectra | 1, 11 |
| 2. Figures of merit and corrections | 2, 4 |
| 3. Choosing window and record length | 1, 6, 12 |
| 4. Processing gain and the noise floor | 3, 5, 12 |
| 5. Periodogram and averaging | 7 |
| 6. ADC testing | 8, 9, 10 |
