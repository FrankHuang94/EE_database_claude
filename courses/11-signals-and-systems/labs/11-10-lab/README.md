# Lab 11-10 · Sampling, Aliasing and Reconstruction

Chapter: [11-10 Sampling, Aliasing and Reconstruction](../../chapters/11-10-sampling-aliasing-reconstruction.md)

## Objective

Watch tones, a chirp and noise fold when sampled; rebuild a signal by sinc interpolation and by a zero-order hold; and simulate a biopotential converter's two-stage anti-aliasing chain against interference.

## Background

The sampled spectrum and the sampling theorem (§3.1–3.2), aliasing of tones and noise (§3.3), anti-aliasing filters (§3.4), reconstruction (§3.5), and decimation (§3.7).

## Files

- [11-10-sampling.ipynb](11-10-sampling.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Folding (Part 1).** Sample tones at 30, 50 and 96.5 kHz and a 0–100 kHz chirp at 48 kHz; locate the FFT peaks and watch the chirp's apparent frequency zigzag.
2. **Reconstruction (Part 2).** Rebuild a band-limited signal from its samples by sinc interpolation and measure the error. Then build a zero-order-hold staircase of a 20 kHz tone at 48 kHz on a fine time grid and measure the levels of the tone and its images in its spectrum.
3. **Noise and filters (Part 3).** Sample white noise extending to 1 MHz at 48 kHz with and without an ideal 24 kHz filter and compare the in-band noise power; tabulate Butterworth orders against oversampling ratio.
4. **A converter's chain (Part 4, the chapter's guided exercise).** *Predict first:* which interferer reaches the 500 SPS output more strongly, 450 Hz or 127.95 kHz at the same amplitude? Then simulate: an RC filter at 8.4 kHz, sampling at 128 kHz, and a sinc³ decimator by 256.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Apparent frequencies | 18, 2 and 0.5 kHz; the chirp folds at every multiple of 24 kHz |
| 2 | Sinc interpolation | Error near zero away from the record's ends |
| 2 | Hold spectrum | Tone at −2.64 dB, images at −5.56 dB (28 kHz) and −13.27 dB (68 kHz) |
| 3 | Noise folding | About 16.2 dB more in-band noise without the filter |
| 4 | Interference | 127.95 kHz arrives about 34 dB stronger than 450 Hz |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-10.a | apparent frequency of 30 kHz, from the FFT | 18 | kHz |
| Lab 11-10.b | hold spectrum: tone at 20 kHz | −2.64 | dB |
| Lab 11-10.c | hold spectrum: image at 28 kHz | −5.56 | dB |
| Lab 11-10.d | simulated noise increase without filter | 16.2 | dB |
| Lab 11-10.e | simulated output from 450 Hz interferer | −57.7 | dB |
| Lab 11-10.f | simulated output from 127.95 kHz interferer | −24.1 | dB |

## Discussion questions

1. In Part 1 the chirp's apparent frequency falls between 24 and 48 kHz of input. Explain with the folding diagram, and say what a listener would hear.
2. In Part 2, why is the sinc interpolation's error largest near the ends of the record?
3. In Part 4, how would you protect the ECG against a 128 kHz interferer without degrading THD?

### Answers

1. Inputs from $f_s/2$ to $f_s$ fold back as $f_s - f$: as the input rises from 24 to 48 kHz, the apparent frequency falls from 24 kHz to 0. A listener would hear a falling whistle while the real tone rises, then a rising one again above 48 kHz.
2. Sinc interpolation needs all samples, past and future; a finite record omits the sinc tails of the samples beyond its ends, and those tails decay only as $1/t$, so the truncation error is largest near the edges.
3. Options include a second-order RC (two poles give 40 dB per decade instead of 20), moving the interferer (a regulator's switching frequency set away from multiples of $f_{MOD}$), shielding and layout, or a different modulator clock; each trades parts, power or flexibility instead of the THD that a larger single capacitor costs.

## Optional hardware extension

With a sound card at 48 kHz and a signal generator, play tones from 15 to 40 kHz into the line input. Record and plot their apparent frequencies. Many sound cards have strong anti-aliasing filters; if the tones above 24 kHz vanish instead of folding, that is the filter doing its job. Then repeat with a microcontroller ADC sampling at a few kilohertz without any filter, and watch the folding happen.
