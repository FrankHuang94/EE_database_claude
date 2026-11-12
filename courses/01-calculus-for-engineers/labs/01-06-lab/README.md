# Lab 01-06 · Techniques of Integration

**Chapter:** [01-06](../../chapters/01-06-techniques-of-integration.md) · **Notebook:** [01-06-techniques.ipynb](01-06-techniques.ipynb) · **Netlists:** [fourier_coeffs.cir](fourier_coeffs.cir), [noise_bw.cir](noise_bw.cir) · **Time:** about 60 minutes

## Objective

1. Use SymPy to check substitutions, integration by parts and partial fractions, and see what happens when no elementary antiderivative exists.
2. Compute Fourier coefficients of common waveforms by numerical integration, rebuild the waves, and measure the Gibbs overshoot.
3. See how numerical quadrature succeeds on smooth integrands and fails on oscillating and singular ones.
4. Confirm in ngspice a square wave's Fourier coefficients and the kT/C noise result.

## Background

Chapter sections 3.1–3.4 (substitution, parts, trigonometric integrals, orthogonality, partial fractions), 3.6 (improper integrals and noise bandwidth) and 3.7 (numerical integration).

## Procedure

1. Run all notebook cells in order.
2. **Part 1:** check that every derivative test prints True, and note that $e^{-x^2}$ produces the special function erf.
3. **Part 2:** before running, predict which of the three waves needs the most harmonics to look right.
4. **Part 3:** before running, predict which integral Simpson's rule (20 intervals) gets most wrong.
5. **Part 4:** from the repository root, run `python tools/run_spice.py 01-06`. Then, before re-running, predict the noise for the 1 MΩ, 1 pF circuit.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 2 | square-wave $b_1, b_3, b_5$ | 1.2732, 0.4244, 0.2546 (even ones 0) |
| 2 | triangle-wave $b_1, b_3, b_5$ | 0.8106, −0.0901, 0.0324: falling as $1/n^2$ |
| 2 | Gibbs peak with harmonics up to 11, and the limit | 1.1813; 1.1790 for many harmonics (it does not shrink) |
| 3 | Simpson(20) on $\sin^2(40x)$ over $[0, \pi]$ | 0, against the true $\pi/2$: every sample lands on a zero of the integrand (aliasing) |
| 3 | Simpson(20) on $1/\sqrt{x}$ near 0 | about 168, against the true 2: the singularity defeats a uniform grid |
| 4 | ngspice $b_1$, $b_3$, $b_5$ | 1.2732, 0.4244, 0.2546; $b_2 \approx 0$ |
| 4 | noise: 10 kΩ with $f_c$ = 10 kHz; 1 kΩ with 1 pF; 1 MΩ with 1 pF | 1.613 µV; 64.36 µV; 64.36 µV |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-06.a | kT/C noise, 1 MΩ and 1 pF | 64.36 | µV |
| Lab 01-06.b | Gibbs peak, harmonics up to 11 | 1.1813 | — |
| Lab 01-06.c | Simpson(20) on sin²(40x) | 0 | — |

## Discussion questions

1. Part 3's oscillating integral fails because of *aliasing*: the sample spacing matches the integrand's period. Where else in this curriculum does sampling at the wrong rate produce a confidently wrong answer? (Compare Problem 01-05.15.)
2. ngspice gives the same kT/C noise for 1 kΩ and 1 MΩ. In which circuit is the noise spread over a wider bandwidth, and why does that not change the total?
3. The sawtooth's coefficients fall as $1/n$, like the square wave's. What feature do the two waves share?

## Optional hardware version

With an oscilloscope that has an FFT function and a function generator: display a 1 kHz square wave's spectrum and compare the harmonic heights (in dB) with $20\log_{10}(1/n)$: −9.5 dB at the 3rd, −14 dB at the 5th. Switch to a triangle wave and compare with $20\log_{10}(1/n^2)$: −19 dB at the 3rd, −28 dB at the 5th.
