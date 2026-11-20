# Lab 16-09 · Changing Sample Rates Without Damage

Chapter: [16-09 Multirate DSP](../../chapters/16-09-multirate-dsp.md)

## Objective

See aliasing and imaging happen, prove that polyphase structures compute exactly what direct structures compute at a fraction of the cost, build a multistage half-band decimator and a 44.1-to-48 kHz converter, and run a CIC decimator in Python and Verilog to see why its integrators may (and must) wrap around.

## Background

Read §3 of the chapter. `multirate.py` implements down- and upsampling, direct and polyphase decimators and interpolators, rational resampling (a direct reference and a polyphase version that computes only the phase each output needs), half-band and CIC helpers, and a bit-true CIC model with two's-complement wrap-around. `cic_decim.v` is a four-stage CIC decimator by 8 with 24-bit registers; `make_vectors.py` writes its test vectors from the bit-true model.

## Files

- [multirate.py](multirate.py): `downsample`, `upsample`, `decimate_direct`, `polyphase`, `decimate_polyphase`, `interpolate_direct`, `interpolate_polyphase`, `resample_rational`, `resample_polyphase`, `mults_per_second`, `halfband_taps_nonzero`, `cic_response`, `cic_decimate_int`, `wrap`.
- [cic_decim.v](cic_decim.v), [cic_decim_tb.v](cic_decim_tb.v), [make_vectors.py](make_vectors.py), [vectors.hex](vectors.hex): the CIC decimator, its self-checking testbench and its vectors (12 sequences).
- [16-09-multirate-lab.ipynb](16-09-multirate-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Aliasing and imaging (Part 1).** Decimate tones by 4 without filtering and find the aliases (Example 16-09.1); upsample a tone by 3 and find the images (Example 16-09.2).
2. **Polyphase equivalence (Part 2).** Compare direct and polyphase decimators and interpolators on random data for several factors and count the multiplications.
3. **Multistage decimator (Part 3).** Design the three half-band stages of Example 16-09.4, cascade them, and measure the overall passband ripple and the worst alias that lands on 0–20 kHz.
4. **44.1 kHz to 48 kHz (Part 4).** Convert a 1 kHz tone with a 3201-tap Kaiser-window prototype ($\beta$ = 9) in polyphase form and measure the error against an ideal delayed sine.
5. **CIC (Part 5).** Run the bit-true model, confirm the vectors, run the Verilog testbench, then make the integrators saturate instead of wrap and watch a full-scale DC input fail. *Predict first:* the output with saturating integrators.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Aliases and images | 10 kHz → 2 kHz and 17 kHz → 5 kHz; images at 11 and 21 kHz |
| 2 | Polyphase | identical outputs to about 1e-12; multiplications divided by the factor |
| 3 | Multistage | stages of 11, 15 and 59 taps; overall passband ripple within ±0.001 dB; aliases onto 0–20 kHz at least 84.3 dB down |
| 4 | Sample-rate conversion | peak error about −96 dB relative to the tone |
| 5 | CIC | TEST PASSED; with saturating integrators the full-scale DC output is wrong |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-09.a | 44.1 to 48 kHz peak error | −95.8 | dB |
| Lab 16-09.b | worst alias onto 0–20 kHz, three half-bands | 84.3 | dB |

## Discussion

1. In Part 2, why are the polyphase outputs *exactly* equal to the direct outputs, not just close?
2. In Part 3, why can the first stage get away with only 11 taps?
3. In Part 4, what sets the residual error: the filter's passband ripple, its stopband, or the arithmetic?
4. In Part 5, why does saturation break the CIC while wrap-around does not?

### Answers

1. Polyphase is an algebraic rearrangement of the same sum of products (§3.5): every kept output uses the same coefficients and samples; only the discarded outputs (or the multiplications by inserted zeros) are skipped. Differences are only floating-point rounding.
2. It only needs to stop components that would alias onto 0–20 kHz after all three stages; at 384 kHz, those start at 192 − 20 = 172 kHz, so its transition band is 152 kHz wide.
3. Mostly the prototype's stopband: images of the tone that leak through at −96 dB-ish levels appear as error; the passband ripple of a Kaiser design at $\beta$ = 9 is of the same order. Double-precision arithmetic is far below both.
4. The integrators of a CIC have infinite DC gain and must overflow on any DC input. With wrap-around every operation is exact modulo $2^W$ and the output, which fits in $W$ bits, comes out right. Saturation is not a modular operation: once an integrator clips, information is lost and the combs subtract equal clipped values, driving the output toward zero.

## Optional hardware

Synthesize `cic_decim.v` for an FPGA and compare its resources (adders and registers only, no DSP blocks) with a 64-tap polyphase FIR decimator by 8. Then cascade a small half-band FIR after it and design an inverse-sinc compensator for the CIC's droop.
