# Lab 11-07 · The Discrete-Time Fourier Transform

Chapter: [11-07 The Discrete-Time Fourier Transform](../../chapters/11-07-discrete-time-fourier-transform.md)

## Objective

Compute DTFTs two ways, measure a filter's frequency response with sinusoids, see how truncation length and windows trade ripple against transition width, and find how long a record must be to separate two close tones.

## Background

The DTFT and its periodicity (§3.1), the Dirichlet kernel (§3.2), frequency response and linear phase (§3.4), windows and resolution (§3.5), and the DFT (§3.6).

## Files

- [11-07-dtft.ipynb](11-07-dtft.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Two ways (Part 1).** Compare the FFT of a zero-padded sequence with the DTFT summed directly at the FFT's frequencies.
2. **Measured response (Part 2).** Drive the five-point average at 500 SPS with 50, 100, 150 and 200 Hz sinusoids and compare steady-state amplitudes with $\lvert H\rvert$.
3. **Windowed design (Part 3, the chapter's guided exercise).** *Predict first:* what lengthening a rectangular-window design from 21 to 81 taps does to its overshoot and transition. Then tabulate peak, transition and stopband for rectangular and Hamming windows at 21, 81 and 201 taps.
4. **Resolution (Part 4).** Compare the DTFT midway between tones at 1000 and 1050 Hz with its value at the tones, for records of 64, 160 and 512 samples at 8 kHz; check that zero-padding samples the same DTFT.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | FFT versus sum | Agreement to rounding |
| 2 | Measured amplitudes | Equal to $\lvert H\rvert$; zero at the nulls (100 and 200 Hz) |
| 3 | Windows | Rectangular overshoot stays near 9% as length grows; Hamming keeps it near 0.2–0.4% with a transition about twice as wide |
| 4 | Resolution | One merged peak at 8 ms; separated tones at 20 ms and beyond |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-07.a | measured gain at 150 Hz | 0.2472 | — |
| Lab 11-07.b | rectangular, 81 taps: peak | 1.094 | — |
| Lab 11-07.c | rectangular, 201 taps: peak | 1.091 | — |
| Lab 11-07.d | Hamming, 81 taps: transition | 0.0456 | π rad/sample |
| Lab 11-07.e | Hamming, 81 taps: stopband | −64.6 | dB |
| Lab 11-07.f | midpoint ratio, 64 samples | 1.057 | — |
| Lab 11-07.g | midpoint ratio, 160 samples | 0.028 | — |
| Lab 11-07.h | midpoint ratio, 512 samples | 0.107 | — |
| Lab 11-07.i | Hamming, 201 taps: stopband | −72.0 | dB |
| Lab 11-07.j | Hamming, 21 taps: stopband | −49.8 | dB |

## Discussion questions

1. In Part 2 the measured amplitude at 100 Hz is zero. Explain it in the time domain, without any transform.
2. In Part 4 the midpoint ratio is much smaller for 160 samples than for 512. Does that mean 160 samples resolve the tones better?
3. Why does the Hamming window's stopband keep improving with length (−49.8, −64.6, −72.0 dB in Part 3) while its passband peak stays near 1.002?

### Answers

1. At 500 SPS a 100 Hz cosine completes exactly one cycle in five samples, and five equally spaced samples of one cycle of a sinusoid sum to zero. The average of any five consecutive samples is therefore zero.
2. No. With 160 samples the tones are exactly $f_s/N$ = 50 Hz apart, so each tone's Dirichlet kernel has a zero at the other tone's frequency and the midpoint falls near a deep notch of their combined pattern. With 512 samples both main lobes are narrower and the midpoint sits in a sidelobe region. Both resolve the tones; the ratio is a crude measure, and the longer record also separates them from other nearby components better.
3. The passband ripple of a windowed design is set by the window's shape (its sidelobe level), which does not change with length; longer filters sharpen the transition and push the stopband sidelobes down further from the edge, so the worst stopband value measured from a fixed frequency (π/2) improves.

## Optional hardware extension

Record a few seconds of room sound containing mains hum with a sound card, and compute FFTs of 0.05 s, 0.2 s and 1 s segments. Watch the 50 or 60 Hz line and its harmonics separate from nearby content as the segment grows, and compare a rectangular with a Hamming window.
