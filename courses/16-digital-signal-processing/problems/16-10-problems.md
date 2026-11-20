# Problems 16-10 · Quantization and Fixed-Point Effects

Chapter: [16-10](../chapters/16-10-quantization-and-fixed-point.md) · Worked solutions: [16-10 solutions](../solutions/16-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Q$I$.$F$ has $I$ integer bits including the sign and $F$ fractional bits; $\Delta = 2^{-F}$. An $N$-bit quantizer for full-scale ±1 has $\Delta = 2^{1-N}$. Rounding is to nearest with ties up unless stated; "LSB" is $\Delta$. Problems marked *(lab)* need the lab's `quant.py` or an equivalent simulation.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-10.1 [A]

**Formats.** (a) Give the range and step of Q4.12 and the step of Q1.31. (b) A sensor value spans ±20 and needs a resolution of 0.001. How many integer and fractional bits are needed, and how many in total?

### Problem 16-10.2 [A]

**Bits and SQNR.** Find the full-scale-sine SQNR of 10-bit and 14-bit quantizers, and the number of bits needed for 100 dB.

### Problem 16-10.3 [A]

**Truncation bias.** A Q1.15 accumulator adds 1000 values, each truncated (two's complement) before it is added. What is the expected accumulated error?

### Problem 16-10.4 [B]

**Products and sums.** Two Q1.15 numbers are multiplied, and 64 such products are summed. Give the exact format of one product, the format that holds the sum without overflow, and the noise variance added when the sum is rounded once back to Q1.15.

### Problem 16-10.5 [B]

**More bits do not cure clipping.** Repeat the Gaussian-loading calculation of Example 16-10.2 for a 16-bit quantizer at $L = 4$: give the granular-only SQNR and the SQNR including clipping. What does the comparison with 12 bits show?

### Problem 16-10.6 [B]

**Noise gain of a first-order section.** For $H(z) = 1/(1 - az^{-1})$, show that the noise gain is $1/(1 - a^2)$. Evaluate it in dB for $a$ = 0.9 and 0.99, and the number of extra bits needed inside the loop for $a$ = 0.99 to keep its rounding noise at the input's level.

### Problem 16-10.7 [B]

**Round once, not 64 times.** A 64-tap FIR filter rounds every product to Q1.15 before adding, instead of accumulating at full precision and rounding once. By how many dB does the output rounding noise increase?

### Problem 16-10.8 [B]

**Coefficient-error estimates.** A 101-tap FIR filter has coefficients rounded to 12 fractional bits. Give the statistical (rms) estimate and the worst-case bound of the response error, in dB.

### Problem 16-10.9 [B]

**Dead bands.** *(lab)* Compute the dead band of $y[n] = Q(ay[n - 1])$ for $a$ = 0.95 and $a$ = 0.99, and confirm by simulation starting from 200 LSB.

### Problem 16-10.10 [C]

**Choosing a scaling norm.** *(lab)* For the resonator $1/(1 - 0.95z^{-1} + 0.9025z^{-2})$ (16-08 Problem 16-08.5), compute the $L_1$ norm, the $L_\infty$ norm (peak gain) and the $L_2$ norm $\sqrt{\sum g^2}$ of its impulse response. How many bits of scaling does each rule demand, and which would you use for a speech codec and which for a safety-critical controller?

### Problem 16-10.11 [C]

**The cost of dither.** Compare the total error power, relative to undithered rounding, for (a) rectangular dither uniform on ±½ LSB and (b) triangular dither on ±1 LSB. Why do audio engineers accept the larger penalty of (b)?

### Problem 16-10.12 [C]

**Low-precision floating point.** Round 0.3 and 1000 to E4M3, E5M2, bfloat16 and IEEE binary16 (round to nearest; E4M3 saturates at its maximum). Give the relative error for 0.3 in each, and comment.

---

## Objective coverage

| Learning objective (chapter 16-10) | Problems |
|---|---|
| 1. Fixed-point formats, rounding, overflow | 1, 3, 4 |
| 2. Noise model and SQNR | 2, 7, 11 |
| 3. Loading and clipping | 5 |
| 4. Noise through filters | 6, 7 |
| 5. Coefficient quantization | 8 |
| 6. Overflow, limit cycles, scaling, dither | 9, 10, 11 |
| 2 (extension). Floating-point formats: relative error and range | 12 |
