# Lab 11-06 · The Continuous-Time Fourier Transform

Chapter: [11-06 The Continuous-Time Fourier Transform](../../chapters/11-06-continuous-time-fourier-transform.md)

## Objective

Use the FFT as a numerical Fourier transform and check it against exact pairs; confirm the convolution theorem; derive a converter's bandwidth from its filter structure; and test the quadrature rule for rise times in cascades.

## Background

The transform pairs of §3.2; the convolution theorem (§3.3); Parseval (§3.5); bandwidth and rise time (§3.6); Examples 11-06.4, 11-06.5 and 11-06.7.

## Files

- [11-06-fourier-transform.ipynb](11-06-fourier-transform.ipynb): the notebook (Parts 1–4).

## Procedure

1. **FFT as a transform (Part 1).** Sample $e^{-at}u(t)$, a 1 µs pulse and a Gaussian, scale the FFT by $\Delta t$, correct the phase for the window's start, and compare with the exact transforms at the same frequency bins.
2. **Convolution theorem (Part 2).** Filter the 5 V, 2 ms pulse with the RC impulse response by direct convolution and by multiplying FFTs (zero-padded to avoid wraparound); compare outputs and energies.
3. **sinc³ bandwidth (Part 3).** Find the −3 dB point of the exact digital response and of its continuous-time limit.
4. **Rise times (Part 4, the chapter's guided exercise).** *Predict first:* whether two 1 ns single-pole stages give 1.41 ns. Then compute cascades of 1 to 4 single-pole stages and of 2 Gaussian stages.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | FFT versus exact | Agreement to about four digits once compared at the same bin; a small bias for the exponential, whose jump at $t = 0$ the samples resolve only to $\Delta t$ |
| 2 | Two routes | Identical to rounding; output energy about 28.4 V²·ms |
| 3 | −3 dB | 131.0 Hz, $0.2619f_{DR}$, for both the exact and the limiting response |
| 4 | Rise times | Single-pole cascades exceed the quadrature rule by a growing margin; Gaussian stages follow it exactly |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-06.a | pulse spectrum at the 0.4883 MHz bin | 0.6515 | µs |
| Lab 11-06.b | Gaussian spectrum at the 0.2014 bin | 1.1254 | — |
| Lab 11-06.c | output energy by FFT convolution | 28.4 | V²·ms |
| Lab 11-06.d | exact digital −3 dB frequency | 131.0 | Hz |
| Lab 11-06.e | two single-pole stages | 1.528 | ns |
| Lab 11-06.f | four single-pole stages | 2.245 | ns |
| Lab 11-06.g | two Gaussian stages | 1.414 | ns |
| Lab 11-06.h | rise time of a 20 MHz limit | 17.5 | ns |

## Discussion questions

1. Why must the FFTs in Part 2 be zero-padded to at least twice the signal length?
2. In Part 3 the exact digital response and its continuous-time limit give the same −3 dB point to four digits. When would they differ?
3. Part 4 shows the quadrature rule underestimating single-pole cascades by more as stages are added. A reference you read says the rule "works well for oscilloscopes". Reconcile the two.

### Answers

1. Multiplying FFTs computes a *circular* convolution: the output wraps around the end of the record. Padding each sequence with zeros to at least the sum of their lengths leaves room for the full linear convolution, so nothing wraps. This is the basis of FFT-based fast convolution (Course 16).
2. When the decimation ratio $N$ is small, or near frequencies approaching $f_{MOD}/2$, where $N\sin(\pi f/f_{MOD})$ is no longer close to $N\pi f/f_{MOD}$. At $N$ = 256 and frequencies of a few hundred hertz against 128 kHz, the approximation error is negligible.
3. Oscilloscope front ends are designed to have near-Gaussian (or flatter) responses, for which the rule is close to exact. The rule fails for stages whose rise-time-to-width ratio differs from the overall response's, as single poles do; the more such stages, the larger the error.

## Optional hardware extension

With an oscilloscope that has a bandwidth-limit setting (for example 20 MHz), view the same fast edge (a logic output) with the limit off and on. Measure both rise times and check that the limited one is close to $0.35/(20\ \text{MHz})$ = **17.5** ns, and that the quadrature combination of the scope's and the signal's rise times predicts what you see.
