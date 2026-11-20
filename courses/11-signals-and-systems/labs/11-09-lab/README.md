# Lab 11-09 · The z-Transform

Chapter: [11-09 The z-Transform](../../chapters/11-09-z-transform.md)

## Objective

See ROCs as convergence of partial sums, design and test pole–zero filters (a resonator and a mains notch on a synthetic ECG), map the biquad stability triangle and the poles a fixed-point biquad can realize, and measure what the bilinear transform does to a link equalizer at different oversampling ratios.

## Background

The z-transform and its ROC (§3.1–3.3), inversion (§3.4), system functions and the stability triangle (§3.6), geometric evaluation and the IIR notch (§3.7), and the s-to-z maps (§3.8).

## Files

- [11-09-z-transform.ipynb](11-09-z-transform.ipynb): the notebook (Parts 1–4).

## Procedure

1. **ROCs as convergence (Part 1).** For the three sequences of Example 11-09.2, compute partial sums of $\sum x[n]z^{-n}$ over growing windows at $\lvert z\rvert$ = 0.3, 1 and 3, and see which settle and to what.
2. **Pole–zero filters (Part 2, the chapter's guided exercise).** Compare geometric and direct magnitude responses for the resonator. Then build a synthetic ECG with 60 Hz hum at 500 SPS and filter it with the three-tap FIR notch of 11-07 and the IIR notch of Example 11-09.4. *Predict first:* when the hum's amplitude doubles, how many samples does the IIR notch ($r$ = 0.98) need to bring the new hum down to 1%, and what about $r$ = 0.995? Then measure.
3. **Stability and word length (Part 3).** Draw the stability triangle with the parabola of complex poles. Plot every pole a biquad can realize when $a_1$ and $a_2$ have 4 fractional bits, and count the complex pole pairs inside the circle.
4. **Digitizing the CTLE (Part 4).** Transform 11-08's reference CTLE at $g_{DC}$ = −12 dB with `scipy.signal.bilinear_zpk` at $M$ = 2, 4, 8 and 32 samples per UI and compare the digital gain at Nyquist with the analog one, with and without prewarping.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Partial sums | Each sequence's sum settles only inside its own ROC, to $X(z)$ |
| 2 | FIR and IIR notches | Both remove 60 Hz; the FIR notch also distorts the ECG's slower content, the IIR notch barely touches it |
| 2 | Hum transient | Decays as $r^n$: about 228 samples ($r$ = 0.98) and 919 ($r$ = 0.995) to 1% |
| 3 | Realizable poles | Sparse near $z = \pm1$, denser near $\pm j$ |
| 4 | Warping error at Nyquist | Falls roughly as $1/M^2$; prewarping removes it at the prewarped frequency |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-09.a | IIR notch gain at 50 Hz, measured with a sinusoid | 0.9879 | — |
| Lab 11-09.b | hum transient to 1%, r = 0.98 | 228 | samples |
| Lab 11-09.c | hum transient to 1%, r = 0.995 | 919 | samples |
| Lab 11-09.d | complex pole pairs realizable with 4 fractional bits | 641 | — |
| Lab 11-09.e | Nyquist gain error, M = 4 | 0.061 | dB |
| Lab 11-09.f | Nyquist gain error, M = 8 | 0.017 | dB |
| Lab 11-09.g | Nyquist gain error, M = 2 | 0.130 | dB |

## Discussion questions

1. In Part 2 the FIR notch visibly changes the ECG's shape and the IIR notch does not. Explain with the pole–zero plots.
2. In Part 3 the realizable poles crowd near $z = \pm j$ and thin out near $z = \pm1$. Why, and which applications suffer?
3. In Part 4, why does the warping error fall roughly as $1/M^2$?

### Answers

1. The FIR notch has only zeros, at $e^{\pm j\omega_0}$; their distance to the point $e^{j\omega}$ varies strongly across the whole band, so the gain changes from 0.30 at 50 Hz to 2.5 at 120 Hz and reshapes the waveform. In the IIR notch each zero has a pole right beside it; away from ω₀ their distances nearly cancel, so the gain is close to 1 everywhere except within a few hertz of 60 Hz.
2. The poles of $z^2 + a_1z + a_2$ are at radius $\sqrt{a_2}$ and angle $\arccos(-a_1/2\sqrt{a_2})$. A uniform grid in $a_1$ maps through the arccosine, whose slope is infinite at $\pm1$ (angles near 0 and π) and smallest near 0 (angles near π/2): angles near 0 and π are coarsely spaced. Low-frequency, high-Q filters at high sample rates (audio DC blockers, sensor low-passes, hum filters at 48 kHz) suffer most.
3. The warping $\Omega = (2/T)\tan(\omega/2)$ differs from $\omega/T$ by a relative error of about $(\omega/2)^2/3$ for small ω. At Nyquist $\omega = \pi/M$, so the frequency error, and with it the gain error for a smooth response, scales as $1/M^2$.

## Optional hardware extension

On a microcontroller board with an ADC (or a sound card), sample a signal with deliberate 50 or 60 Hz pickup at a few hundred to a few thousand samples per second and run the IIR notch of Example 11-09.4 in floating point and in 16-bit fixed point. Compare the notch depth and the transient after unplugging and replugging the noise source, and check the quantized coefficients' poles against the stability triangle.
