# Lab 16-07 · From Analog Prototypes to Digital Biquads

Chapter: [16-07 IIR Filter Design](../../chapters/16-07-iir-filter-design.md)

## Objective

Translate analog filters into digital ones with impulse invariance and the bilinear transform, build Butterworth and Chebyshev filters from their pole formulas, design the running audio specification three ways and compare them with the FIR filter of 16-06, and see why IIR filters are implemented as second-order sections.

## Background

Read §3 of the chapter. `iirdesign.py` computes prewarped frequencies, discriminations and order bounds (the elliptic one from SciPy's complete elliptic integrals), Butterworth and Chebyshev I prototypes from the pole formulas of §3.1–§3.2, and the bilinear transform of poles, zeros and gain in three lines (§3.4). Responses and group delays are computed root by root. Elliptic prototypes come from SciPy's `ellipap`, as in practice. The verify script checks every design against SciPy's own `butter`, `cheby1` and `ellip`.

## Files

- [iirdesign.py](iirdesign.py): `prewarp`, `unwarp`, `discrimination`, `order_butter`, `order_cheb`, `order_ellip`, `butter_analog`, `cheb1_analog`, `bilinear`, `response`, `group_delay`, `impulse_invariant_first_order`, `bilinear_first_order`, `butter2_biquad`, `mults_sos`.
- [16-07-iir-design-lab.ipynb](16-07-iir-design-lab.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Warping (Part 1).** Plot the bilinear frequency map at 48 kHz; design a first-order low-pass at 1 kHz for $f_s$ = 8 kHz with and without prewarping and measure the −3 dB points.
2. **Impulse invariance (Part 2).** Sweep the cutoff of a first-order impulse-invariant design from 250 Hz to 3 kHz at $f_s$ = 8 kHz and plot the Nyquist-to-DC gain ratio against the analog filter's. *Predict first:* where the two curves part.
3. **Prototypes from poles (Part 3).** Build the order-38 Butterworth and order-14 Chebyshev designs of Example 16-07.4 from the pole formulas, map them, and compare with SciPy.
4. **Three IIR filters and an FIR filter (Part 4).** Check every design of Figure 2 against the mask, count multiplications, and plot the passband group delay.
5. **Quantize (Part 5).** Round the elliptic filter's coefficients as one polynomial and as biquads and track the largest pole radius.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | −3 dB points | 952.9 Hz unprewarped, 1000.0 Hz prewarped |
| 2 | Impulse invariance | the Nyquist/DC ratio exceeds the analog ratio at every cutoff, by 0.13 at 1 kHz (0.374 against 0.243) and more as the cutoff rises |
| 3 | Prototypes | the lab's Butterworth and Chebyshev filters equal SciPy's to about 1e-12; order 14 Chebyshev reaches 64.62 dB and order 38 Butterworth 61.75 dB at the 5 kHz edge (their stopbands fall monotonically, so the edge is the worst point) |
| 4 | Comparison | elliptic 14, Chebyshev 17, Butterworth 41 multiplications per output (sections, powers of two free), FIR 69; passband group-delay spreads 61.5, 89.4 and 49.9 samples against 0 |
| 5 | Quantization | the single polynomial is unstable at 12 fractional bits (radius 1.030); the biquads stay stable at 8 |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 16-07.a | Chebyshev order-14 attenuation | 64.62 | dB |
| Lab 16-07.b | Butterworth order-38 attenuation | 61.75 | dB |
| Lab 16-07.c | Chebyshev passband delay spread | 89.4 | samples |
| Lab 16-07.d | Butterworth passband delay spread | 49.9 | samples |
| Lab 16-07.e | Chebyshev SOS multiplications | 17 | — |
| Lab 16-07.f | Butterworth SOS multiplications | 41 | — |

## Discussion

1. In Part 1, why does the unprewarped filter's cutoff land below 1 kHz rather than above?
2. In Part 2, why does the impulse-invariant design's error grow as the cutoff approaches Nyquist?
3. In Part 4, the Butterworth filter has the smallest delay spread of the three IIR filters but the most multiplications. Why?
4. In Part 5, why does even the stable 16-bit direct form change the filter's response?

### Answers

1. The bilinear map compresses the analog axis: an analog frequency $\Omega$ lands at $\omega = 2\arctan(\Omega T/2) < \Omega T$. The analog cutoff of 1 kHz therefore appears below 1 kHz in the digital filter.
2. The aliased copies of the analog response, spaced $f_s$ apart, add to the response near Nyquist; the higher the cutoff, the less the analog response has fallen by $f_s/2$ and the larger the copies.
3. Its poles are spread around a circle rather than packed toward the axis near the band edge, so no pole is as close to the unit circle (largest radius 0.979 against 0.985 and 0.990), which keeps the delay peak down; but a flat, gently curving response needs many more poles to reach 60 dB within a 1 kHz transition.
4. The roots move even when they stay inside the circle: the largest radius drops from 0.98499 to 0.98451, which changes the gain and ripple near the band edge. Stability is necessary, not sufficient; the quantized response must be rechecked against the mask (16-10).

## Optional hardware

Implement the four biquads of Example 16-07.5 on a microcontroller with Arm's CMSIS-DSP (`arm_biquad_cascade_df1_f32`, remembering to negate $a_1$ and $a_2$ as its documentation requires) or in any audio plug-in host, and measure the response with a sound card and a sweep. Then implement it once as a single tenth-order difference equation in single-precision floating point and compare.
