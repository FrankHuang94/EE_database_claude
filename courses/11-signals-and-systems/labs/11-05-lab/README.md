# Lab 11-05 · Fourier Series

Chapter: [11-05 Fourier Series](../../chapters/11-05-fourier-series.md)

## Objective

Compute Fourier coefficients numerically and check them against closed forms; measure the Gibbs overshoot; verify Parseval's relation and compute THD from power; and find a filtered PWM signal's ripple harmonic by harmonic, confirmed by a direct circuit simulation.

## Background

The analysis formula and orthogonality (§3.1–3.2); standard series (§3.4); convergence and the Gibbs phenomenon (§3.5); Parseval and THD (§3.6); LTI systems with periodic inputs (§3.8); the PWM DAC of Example 11-05.7.

## Files

- [11-05-fourier-series.ipynb](11-05-fourier-series.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Coefficients two ways (Part 1).** Integrate the analysis formula numerically for a square wave and a 25%-duty, 3.3 V PWM signal, and compute the same coefficients from an FFT of one sampled period.
2. **Gibbs (Part 2).** Find the first peak of the square wave's partial sums for $N$ = 9, 99 and 999.
3. **Parseval and THD (Part 3).** Compare each signal's power with the sum of its squared coefficients up to $k = 199$, and compute THD.
4. **PWM filtering (Part 4, the chapter's guided exercise).** *Predict first:* the ripple reduction from a first-order to a second-order filter with the same 1 kHz corner. Then compute both outputs harmonic by harmonic and compare the first-order result with a time-domain simulation of the RC circuit.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Coefficients | Integration, FFT and closed forms agree to four digits; the PWM 4th harmonic vanishes |
| 2 | Gibbs | Peak near 1.179 at $\omega_0t \approx \pi/(N + 1)$ for every large $N$ |
| 3 | Parseval | Sums approach the powers (slowly for the square wave, whose coefficients fall as $1/k$) |
| 4 | Ripple | Second order about 100 times smaller at 100 kHz; harmonic sum and simulation agree |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-05.a | PWM magnitude of c_3 | 0.2476 | V |
| Lab 11-05.b | Gibbs peak, N = 9 | 1.182 | — |
| Lab 11-05.c | Gibbs peak, N = 999 | 1.17898 | — |
| Lab 11-05.d | square-wave power from harmonics up to 199 | 0.9980 | — |
| Lab 11-05.e | second-order 100 kHz ripple amplitude | 0.1485 | mV |
| Lab 11-05.f | second-order ripple, peak to peak | 0.3053 | mV |
| Lab 11-05.g | simulated RC ripple, peak to peak | 38.87 | mV |

## Discussion questions

1. In Part 3 the square wave's partial Parseval sum is still 0.2% short of 1 after 199 harmonics, while the triangle's is complete to four digits. Why?
2. In Part 4 the second-order filter reduces the 100 kHz ripple a hundredfold but its peak-to-peak ripple is about twice the fundamental's amplitude, unlike the first-order case. Why is the ripple waveform closer to a pure sinusoid?
3. Part 1 sampled at midpoints of $M$ equal intervals. What goes wrong if a sample falls exactly on a jump, and why does the FFT then still give nearly the right answer?

### Answers

1. The square wave's harmonic powers fall as $1/k^2$ (coefficients as $1/k$), so the power beyond harmonic $N$ is about $\sum_{k>N}1/k^2 \sim 1/N$: a slow tail. The triangle's fall as $1/k^4$, so the tail beyond $N$ is of order $1/N^3$, negligible at $N = 199$.
2. Each harmonic is attenuated by about $(f_c/kf_0)^2$ instead of $f_c/(kf_0)$, so the 2nd and higher harmonics are much smaller relative to the fundamental: the output is dominated by the 100 kHz term, and a sinusoid's peak-to-peak value is twice its amplitude.
3. A sample on a jump takes one side's value instead of the midpoint the series converges to, adding an error of order $1/M$ to every coefficient. With $M$ = 4096 that is small, and the FFT coefficients still converge to the true ones as $M$ grows; sampling at midpoints simply avoids the ambiguity.

## Optional hardware extension

Generate a 25%-duty PWM signal on any microcontroller pin at a few kilohertz, filter it with an RC network, and record both the pin and the filtered output with a sound card or oscilloscope. Compare the measured DC value and ripple with Example 11-05.7's formulas, and use the oscilloscope's FFT to find the missing 4th harmonic in the pin's spectrum.
