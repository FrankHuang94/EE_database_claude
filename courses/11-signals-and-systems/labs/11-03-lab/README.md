# Lab 11-03 · Convolution

Chapter: [11-03 Convolution](../../chapters/11-03-convolution.md)

## Objective

Compute convolutions in every form the chapter uses and confirm they agree; see continuous-time convolution as a numerical integral with a measurable error; build a real ADC decimation filter from boxcars; and use convolution with a reversed pattern to find a signal in noise.

## Background

The convolution sum and its four computational forms (§3.1–3.2); the convolution integral as the limit of a staircase sum (§3.3); graphical convolution (§3.4); the support and area rules and cascades (§3.5); correlation and matched filtering (§3.7). Example 11-03.6 describes the ADS1292R's sinc³ filter.

## Files

- [11-03-convolution.ipynb](11-03-convolution.ipynb): the notebook (Parts 1–5).

## Procedure

1. **Four ways (Part 1).** Convolve Example 11-03.1's sequences with a double loop, `np.convolve`, a Toeplitz matrix and polynomial multiplication; repeat on random sequences.
2. **Graphical, numerically (Part 2).** Sample Example 11-03.3's pulses with a step Δ = 0.001 (the example's time units) and approximate the integral by a sum.
3. **RC by convolution (Part 3, the chapter's guided exercise).** *Predict first:* how the error of the discretized integral at 2 ms changes when Δ halves, for the rectangle and trapezoidal rules. Then compare with an ODE solution of the circuit.
4. **Decimation filter (Part 4).** Build the sinc³ filter from three 256-sample boxcars and plot its step response.
5. **Matched filter (Part 5).** Insert a 21-chip pattern into noise of standard deviation 0.8 and locate it.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Four methods | Identical to rounding error |
| 2 | Pulses | Trapezoid with a flat top of 3 and area 6; edge values off by about 3Δ (the slope 3 times the step) |
| 3 | RC | Rectangle-rule error halves with Δ; trapezoidal error falls fourfold; both converge to the ODE's 4.323 V |
| 4 | sinc³ | 766 samples (5.984 ms) long; step response symmetric about its midpoint |
| 5 | Matched filter | Peak at the true position despite noise comparable to the chips |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-03.a | methods that agree | 4 | — |
| Lab 11-03.b | numerical y(1.5) | 3.000 | — |
| Lab 11-03.c | numerical area | 6.000 | — |
| Lab 11-03.d | rectangle-rule error ratio | 2.00 | — |
| Lab 11-03.e | trapezoidal error ratio | 4.00 | — |
| Lab 11-03.f | ODE y(2 ms) | 4.323 | V |
| Lab 11-03.g | sinc³ step response after one output period | 0.1686 | — |
| Lab 11-03.h | sinc³ 50% point | 2.988 | ms |
| Lab 11-03.i | detected pattern position | 137 | — |
| Lab 11-03.j | noise growth over 21 chips, √21 | 4.6 | — |
| Lab 11-03.k | edge error at t = 0.5 | 0.003 | — |

## Discussion questions

1. In Part 2 the edge values (at 0.5 and 2.5) are off by about 0.003 while the flat top is exact. Why?
2. In Part 4, why is the 50% point of the step response exactly at the middle of the impulse response?
3. In Part 5 the noise standard deviation (0.8) is almost as large as each chip (1). Why does the matched filter still find the pattern?

### Answers

1. Each sample of the discretized pulse represents an interval of width Δ, and whether an edge sample is counted as "in" or "out" shifts the effective edge by up to one Δ. Where the output is rising or falling (slope 3 per unit time), a shift of Δ = 0.001 changes the value by about 0.003. On the flat top the overlap is complete either way, so the error vanishes.
2. The sinc³ impulse response is symmetric about its midpoint, so exactly half its area lies before the midpoint. The step response is the running sum of $h$ (normalized to total 1), so it passes 0.5 at the midpoint, here sample 382.5 of 766, or 2.988 ms.
3. The matched filter adds 21 chips coherently: the signal parts add in amplitude (21 × 1) while independent noise adds in power, so its standard deviation grows only by $\sqrt{21}$ (about 4.6, times 0.8). The peak stands well above the noise even though each chip alone does not. This processing gain is the principle of spread-spectrum and radar receivers (Course 17).

## Optional hardware extension

Record a hand clap in a room with a phone at 48 kHz as an estimate of the room's impulse response, then convolve a dry speech recording with it (`np.convolve` or `scipy.signal.fftconvolve`) and listen: the result sounds as if spoken in that room. Compare the cost of direct and FFT convolution for a one-second response (48,000 taps).
