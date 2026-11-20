# Lab 11-08 · The Laplace Transform and System Functions

Chapter: [11-08 The Laplace Transform and System Functions](../../chapters/11-08-laplace-transform-and-system-functions.md)

## Objective

See the region of convergence happen numerically, check the geometric rule for frequency responses, watch feedback move a system's poles, compare minimum- and non-minimum-phase responses, and tabulate a high-speed link's equalizer settings. Confirm the RLC example's poles and resonance in ngspice.

## Background

The bilateral transform and its ROC (§3.1–3.3), inversion with the ROC (§3.4), system functions and feedback (§3.6), geometric evaluation (§3.7), and all-pass and minimum-phase systems (§3.8).

## Files

- [11-08-laplace.ipynb](11-08-laplace.ipynb): the notebook (Parts 1–4).
- [rlc_poles.cir](rlc_poles.cir): ngspice pole–zero and AC analysis of the series RLC circuit of Example 11-08.4. Run with `ngspice -b rlc_poles.cir`, or `python tools/run_spice.py 11-08` from the repository root.

## Procedure

1. **The ROC, numerically (Part 1).** For the three signals of Example 11-08.2, integrate $x(t)e^{-\sigma t}$ over growing windows at values of σ inside and outside each ROC. Inside, the integral settles; outside, it grows with the window. Evaluate the two-sided signal's transform at $s = 0.5$ and compare with $3/[(s + 1)(s - 2)]$.
2. **Geometric evaluation (Part 2).** Map $\lvert H(s)\rvert$ over the s-plane for the RLC circuit, then compute $\lvert H(j\omega)\rvert$ as the product of pole distances and $\angle H$ as the sum of pole angles, and compare with direct evaluation on a grid.
3. **Feedback moves poles (Part 3, the chapter's guided exercise).** *Predict first:* as $K$ rises from 1 to 25 in Example 11-08.3, what happens to the overshoot, the ringing frequency and the decay of the transient? Then plot the closed-loop poles against $K$ and simulate the step responses.
4. **Phase and the CTLE (Part 4).** Simulate the step responses of the two systems of Example 11-08.5. Then compute the reference CTLE's DC gain, Nyquist gain and boost at every setting from 0 to −20 dB.
5. **ngspice.** Run `rlc_poles.cir` and compare its poles, peak and band-pass edges with Example 11-08.4.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Integrals inside and outside the ROC | Converge inside; grow without bound outside |
| 2 | Geometric against direct | Agreement to rounding at every frequency |
| 3 | Poles against $K$ | Real for $K < 1$, double at $K = 1$, then moving straight up from −1 |
| 4 | Step responses | The right-half-plane zero dips below zero first; same final value |
| 4 | CTLE boost | Grows by about 1 dB per dB of setting below about −5 dB; slightly negative at −1 dB |
| ngspice | Poles, peak, edges | $-10 \pm j30$ krad/s; 1.667 at 4.502 kHz; 3.687 and 6.870 kHz |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-08.a | two-sided transform at s = 0.5, by quadrature | −1.333 | s |
| Lab 11-08.b | measured overshoot, K = 5 | 20.79 | % |
| Lab 11-08.c | measured overshoot, K = 25 | 52.66 | % |
| Lab 11-08.d | measured ringing frequency, K = 25 | 4.899 | rad/s |
| Lab 11-08.e | simulated undershoot, zero at +5 | −0.07143 | — |
| Lab 11-08.f | CTLE boost at −20 dB | 16.91 | dB |
| Lab 11-08.g | CTLE boost at −1 dB | −0.33 | dB |
| Lab 11-08.h | first setting with positive boost | −2 | dB |

## Discussion questions

1. In Part 1, the integral for the causal signal converges at σ = 3 but not at σ = 1. Which term of the signal is responsible, and how does that explain why its ROC starts at the rightmost pole?
2. In Part 3 the transient decays at the same rate for every $K > 1$. Why, from the pole positions? What would you change in the plant to make the loop settle faster?
3. In Part 4, why does the shallowest CTLE setting give slightly *negative* boost, and why do the deeper settings approach $\lvert g_{DC}\rvert - 3.1$ dB?

### Answers

1. The $e^{2t}$ term: $e^{2t}e^{-\sigma t}$ is integrable on $t > 0$ only for σ > 2. The other term, $-e^{-t}$, only needs σ > −1. A right-sided signal's integral converges only where *every* term decays after weighting, so the ROC starts at the largest growth rate, the rightmost pole.
2. For $K > 1$ the poles are $-1 \pm j\sqrt{K - 1}$: the gain changes only the imaginary part, and the real part, which sets the envelope $e^{-t}$, is fixed by the sum of the open-loop poles (0 and −2 average to −1). To settle faster, the open-loop poles must move left (a faster plant) or a zero must be added (lead compensation, Course 13).
3. At −1 dB the zero sits just below the first pole, so it barely lifts the response before the poles pull it down; the second pole's droop at Nyquist (−0.97 dB at 0 dB setting) outweighs the small rise. At deep settings the zero is far below Nyquist, the numerator is essentially $jf/f_z$, and the Nyquist gain approaches $1.25/(1.6008 \times 1.1180)$, −3.1 dB, while the DC gain is $g_{DC}$.

## Optional hardware extension

Build the series RLC of Example 11-08.4 (1 mH, 1 µF, 20 Ω plus the inductor's own resistance) and drive it from a function generator through a low-impedance buffer. Sweep the frequency and measure the capacitor voltage's peak and the resistor voltage's −3 dB edges, then apply a square wave and measure the ringing frequency and the envelope's decay. Fit α and ω_d from the ringing and check that they predict the swept response.
