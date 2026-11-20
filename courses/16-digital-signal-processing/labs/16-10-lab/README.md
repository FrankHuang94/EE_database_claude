# Lab 16-10 · Bits, Noise and Limit Cycles

Chapter: [16-10 Quantization and Fixed-Point Effects](../../chapters/16-10-quantization-and-fixed-point.md)

## Objective

Measure the 6 dB-per-bit law, find the best loading for a random signal, see quantization turn into distortion and dither turn it back into noise, find how many coefficient bits a filter needs, and trap granular and overflow limit cycles.

## Background

Read §3 of the chapter. `quant.py` quantizes with three rounding modes (nearest with ties up, two's-complement truncation, magnitude truncation) and two overflow modes (saturate, wrap), measures SQNR, computes noise gains and $L_1$ norms from impulse responses, generates TPDF dither, measures harmonics of coherent tones, and simulates first- and second-order zero-input recursions in integer arithmetic.

## Files

- [quant.py](quant.py): `quantize`, `sqnr_db`, `sine_sqnr`, `gaussian_sqnr`, `noise_gain`, `l1_norm`, `limit_cycle_first_order`, `second_order_zero_input`, `tpdf_dither`, `harmonic_levels_db`.
- [16-10-quantization-lab.ipynb](16-10-quantization-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **6 dB per bit (Part 1).** Quantize full-scale sines from 8 to 20 bits, fit SQNR against $N$, and compare slope and intercept with 6.02 and 1.76.
2. **Loading (Part 2).** Simulate a Gaussian signal at loading factors $L$ = 3 to 4 at 12 and 16 bits and compare with the granular-plus-clipping formula of §3.3; then use the formula to find the best $L$ (beyond about $4.5\sigma$ clipping is so rare that a million-sample simulation sees only a handful of clips and cannot be trusted). *Predict first:* the best $L$ at each word length.
3. **Dither (Part 3).** Quantize a 1.5 LSB sine with and without TPDF dither and compare spectra and error variances (Example 16-10.3).
4. **Coefficient bits (Part 4).** Quantize the 137-tap equiripple filter of 16-06 to 10–18 fractional bits and plot attenuation against bits (Example 16-10.4).
5. **Limit cycles (Part 5).** Run the first-order recursions of Example 16-10.5 with rounding and magnitude truncation, and the second-order zero-input recursion with wrap-around and saturation.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Fit | slope 6.02 dB per bit, intercept 1.81 dB (theory 1.76: every simulated point lies within 0.05 dB of $6.02N + 1.76$, the scatter of a finite record's noise estimate) |
| 2 | Loading | simulation within 0.3 dB of the formula for $L$ = 3 to 4; best near $L = 5$ (12 bits, 62.7 dB) and $L = 6$ (16 bits, 85.4 dB) |
| 3 | Dither | undithered third harmonic −14.6 dB; dithered, no harmonic above the noise and error variance near 0.25 LSB² |
| 4 | Coefficient bits | 51.85 dB at 12 bits rising to 60.17 dB at 18 |
| 5 | Limit cycles | stuck at 5 LSB ($a = 0.9$), ±4 LSB ($a = -0.9$), zero with magnitude truncation; 31,039 LSB with wrap-around, 3 LSB with saturation (after the transient) |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-10.a | fitted slope | 6.02 | dB/bit |
| Lab 16-10.b | fitted intercept | 1.81 | dB |
| Lab 16-10.c | simulated SQNR at L = 4, 12 bits (10⁶ samples) | 51.7 | dB |

## Discussion

1. In Part 1, why does the fit match the theory so closely even though the "noise" is a deterministic function of the sine?
2. In Part 2, why does the optimum move to a larger $L$ at 16 bits?
3. In Part 4, why does the attenuation not improve smoothly by 6 dB per bit?
4. In Part 5, why does saturation leave a small limit cycle while wrap-around leaves a huge one?

### Answers

1. A full-scale sine at a frequency unrelated to the sample rate crosses thousands of levels in an irregular order, so the error is spread almost uniformly and looks white; the model's assumptions hold.
2. Granular noise falls by 6 dB per bit, but clipping noise depends only on $L$. With finer quantization, clipping becomes relatively more costly, so it pays to back off further.
3. The designed stopband ripple (−60.36 dB) is a floor that quantization error adds to; once the coefficient error is well below it, extra bits only recover the remaining fraction of a dB, and the error's peak over frequency, not its rms, decides.
4. Saturation bounds each error and keeps the arithmetic close to the stable linear filter, whose response decays; only rounding's dead band remains. Wrap-around turns an overflow into a near-full-scale jump of the opposite sign, which the feedback can sustain indefinitely.

## Optional hardware

On a microcontroller, implement the first-order recursion $y = Q(0.99y)$ in Q15 with rounding, feed it an impulse, and watch the output stick at about 50 LSB in a debugger or on a DAC output; then switch to magnitude truncation.
