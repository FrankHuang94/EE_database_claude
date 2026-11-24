# Lab 20-06 · Measuring a Converter: Quantization, DNL/INL, Histograms, Spectra and Figures of Merit

Chapter: [20-06 · Data Converter Fundamentals](../../chapters/20-06-data-converter-fundamentals.md)

## Objective

- See quantization error turn from white noise into spurs when the input is periodic in the record, and dither undo it.
- Confirm the flash ladder of Example 20-06.2 in ngspice.
- Draw a SAR ADC with random capacitor mismatch and measure its DNL and INL.
- Run the sine-wave histogram test with random and with coherent phases and compare the INL errors.
- Run a full FFT test of a converter with mismatch, thermal noise and third-order distortion, and compute its figures of merit.

## Background

`adc.py` models a 12-bit SAR ADC (1.6 V range) whose binary-weighted DAC is built from unit capacitors with independent relative errors (σ = 0.5%, seeded with `numpy.random.default_rng(2006)`). `sar_code` performs the binary search; `sar_transitions` finds each transition level by bisection (the SAR's transfer is monotonic). `dnl_inl` computes endpoint or best-fit DNL and INL; `histogram_transitions` inverts a sine histogram with $T_k = V_0 - A\cos(\pi C_{k-1})$; `spectrum_metrics` computes SNR, THD, SINAD, SFDR and ENOB from a coherent record; `fom_walden`, `fom_schreier` and `thermal_limit_fom_s` give the figures of merit.

Files:

- `adc.py`: the models above.
- `ladder.cir`: the 3-bit flash reference ladder.
- `20-06-converter-lab.ipynb`: the procedure below.

## Procedure

1. **Quantization spectra.** Quantize a full-scale sine with an ideal 12-bit quantizer at bin 1001 and at bin 64 of a 4096-point record; compare SINAD and SFDR. Repeat bin 64 at 98% amplitude with 0.5 LSB rms of Gaussian dither (seed 20061) (Part 1).
2. **Flash ladder.** Predict the taps of Example 20-06.2, run `ngspice -b ladder.cir`, and compare the resistor-only DNL with the DNL including comparator offsets (Part 2).
3. **SAR mismatch.** Plot DNL and INL of the seeded instance (Part 3).
4. **Histogram test.** Apply $2^{22}$ samples of a sine 2% above full scale, first with coherent phases ($\theta_n = 2\pi(1048573\,n/2^{22} + 0.123)$), then with random phases (seed 2007); compare the recovered DNL and INL with the true ones (Part 4).
5. **FFT test.** Apply a 16,384-point coherent sine near 49 MHz at $f_s$ = 100 MS/s, with 20-05's thermal noise (seed 2008) and a cubic nonlinearity sized for HD3 = −64.4 dBc; compute the metrics and both figures of merit for 1.5 mW (Part 5).

## Expected results

- **Part 1.** At bin 1001 the error is white: SINAD **73.65** dB and SFDR **93.7** dBc. At bin 64 the error repeats every 64 samples, so its power collects in harmonics: SINAD **73.83** dB (essentially unchanged) but SFDR only **79.9** dBc. With dither, SFDR returns to **92.4** dBc at the cost of SINAD (**67.72** dB).
- **Part 2.** ngspice gives the taps of Example 20-06.2. The resistor errors alone produce a worst-case DNL of only **0.037** LSB, against 0.631 LSB with the comparator offsets.
- **Part 3.** Worst-case DNL 0.370 LSB at mid-scale and INL 0.328 LSB (Example 20-06.4).
- **Part 4.** With coherent phases the histogram recovers DNL to within **0.0024** LSB and INL to within **0.0013** LSB. With random phases, the DNL error is **0.035** LSB rms, close to the $1/\sqrt{\text{count}}$ = **0.040** LSB expected from about 640 counts per code, but the INL error reaches **1.43** LSB: the cumulative counts random-walk (Example 20-06.5).
- **Part 5.** At **49.0051** MHz: SNR **68.67** dB, THD **−63.96** dBc, SINAD **62.69** dB, SFDR **63.99** dBc and ENOB (normalized to full scale) **10.13** bits. With 1.5 mW: $\text{FoM}_W$ = **13.4** fJ/step and $\text{FoM}_S$ = **167.9** dB, close to Example 20-06.8's estimate. The thermal noise added is **172.7** µV rms.

## Discussion

1. **Why does SINAD barely change at bin 64 while SFDR drops by 14 dB?** The quantization error's total power is still about $\Delta^2/12$; only its distribution in frequency changes. SINAD counts total power; SFDR sees the largest single spur.
2. **Why does the random-phase histogram get DNL right and INL wrong?** Each code's count error is about $1/\sqrt{\text{count}}$, small for DNL. INL sums all the counts below a code, so the errors accumulate; coherent sampling removes the randomness in the cumulative sum.
3. **Why does mismatch barely affect the full FFT test?** The seeded instance's DNL errors are a third of an LSB at most and scattered; spread over the spectrum they add little to 20-05's thermal noise. The switch's third harmonic dominates SINAD, exactly as Example 20-06.6 predicted.

## Optional hardware

Any microcontroller with a 12-bit ADC and a low-distortion audio oscillator (or a DAC output filtered by a few poles) can run Part 4 for real: capture a few million samples of a sine slightly beyond full scale, build the histogram, and invert it. Compare the DNL you find with the data sheet's, and see the large codes at the ends.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-06.a | SINAD, bin 1001 | 73.65 | dB |
| Lab 20-06.b | SFDR, bin 1001 | 93.7 | dBc |
| Lab 20-06.c | SINAD, bin 64 | 73.83 | dB |
| Lab 20-06.d | SFDR, bin 64 | 79.9 | dBc |
| Lab 20-06.e | SFDR with dither | 92.4 | dBc |
| Lab 20-06.f | SINAD with dither | 67.72 | dB |
| Lab 20-06.g | coherent histogram DNL error | 0.0024 | LSB |
| Lab 20-06.h | coherent histogram INL error | 0.0013 | LSB |
| Lab 20-06.i | random-phase DNL error, rms | 0.035 | LSB |
| Lab 20-06.j | random-phase INL error, max | 1.43 | LSB |
| Lab 20-06.k | expected DNL error | 0.040 | LSB |
| Lab 20-06.l | coherent input frequency | 49.0051 | MHz |
| Lab 20-06.m | SNR | 68.67 | dB |
| Lab 20-06.n | THD | −63.96 | dBc |
| Lab 20-06.o | SINAD | 62.69 | dB |
| Lab 20-06.p | SFDR | 63.99 | dBc |
| Lab 20-06.q | ENOB, normalized | 10.13 | bits |
| Lab 20-06.r | FoM_W | 13.4 | fJ |
| Lab 20-06.s | FoM_S | 167.9 | dB |
| Lab 20-06.t | thermal noise added | 172.7 | µV |
| Lab 20-06.u | resistor-only worst-case DNL | 0.037 | LSB |
