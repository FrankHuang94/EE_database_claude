# Lab 11-04 · LTI Systems and Differential/Difference Equations

Chapter: [11-04 LTI Systems and Differential/Difference Equations](../../chapters/11-04-lti-systems-and-differential-equations.md)

## Objective

Connect the three descriptions of an LTI system: the equation, the impulse response and the block diagram. Iterate difference equations and watch root locations decide stability; approach a circuit's impulse response with ever-narrower pulses; implement filter structures and see coefficient rounding break a high-order direct form but not a biquad cascade; and measure eigenvalues directly.

## Background

Difference equations, characteristic roots and stability (§3.2); differential equations and jump conditions (§3.3); direct forms, transposed forms and biquad cascades (§3.4); eigenfunctions and the frequency response (§3.5).

## Files

- [11-04-equations.ipynb](11-04-equations.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Iteration (Part 1).** Iterate Example 11-04.3's equation from rest and compare with the closed form. Then iterate a resonator with roots at radius 0.9, 1.0 and 1.02 and angle π/4.
2. **Narrowing pulses (Part 2).** Drive Example 11-04.5's RLC equation with unit-area pulses 20, 5 and 1 µs wide and compare with $h(t)$.
3. **Structures and rounding (Part 3, the chapter's guided exercise).** *Predict first:* which of a single eighth-order direct form and a cascade of four biquads survives rounding its coefficients to 12 fractional bits. Then check that direct form I, direct form II and transposed direct form II agree, and compare pole radii before and after rounding.
4. **Eigenfunctions (Part 4).** Drive Example 11-04.2's filter with a cosine at $\omega = \pi/3$ and with $0.9^nu[n]$, and measure the output-to-input ratio once transients have faded.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Iteration versus closed form | Agreement to rounding error; ringing that decays, persists or grows as the radius passes 1 |
| 2 | Pulse responses | Approach $h(t)$; the remaining difference is mostly a delay of half the pulse width, so it shrinks with the width |
| 3 | Rounding | Three structures agree exactly; the rounded direct form has a pole outside the unit circle, the rounded biquads do not |
| 4 | Eigenvalues | Steady-state ratio equals $\lvert H\rvert$ for the cosine and $H(0.9)$ for the exponential |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-04.a | resonator with r = 1.0, largest magnitude for n = 32 to 39 | 1.414 | — |
| Lab 11-04.b | resonator with r = 1.02, largest magnitude for n = 32 to 39 | 2.943 | — |
| Lab 11-04.c | designed largest pole radius | 0.9699 | — |
| Lab 11-04.d | rounded direct form, largest pole radius | 1.203 | — |
| Lab 11-04.e | rounded biquads, largest pole radius | 0.9699 | — |
| Lab 11-04.f | gain at ω = π/3 | 2.000 | — |
| Lab 11-04.g | output/input ratio at n = 2 | 3.593 | — |
| Lab 11-04.h | output/input ratio at n = 40 | 4.750 | — |
| Lab 11-04.i | transient share's factor per sample | 0.56 | — |

## Discussion questions

1. In Part 1 the resonator with $r = 1$ neither decays nor grows. Is it stable?
2. In Part 3 the rounded direct form fails while the rounded biquads are almost unaffected. Why is a high-order polynomial's root location so sensitive to its coefficients?
3. In Part 4 the ratio $y/x$ for the exponential input starts at 1 and approaches 4.75. Where does the difference come from, and how fast does it fade?

### Answers

1. No. Its impulse response is bounded but not absolutely summable, and a bounded input at its ringing frequency (a sinusoid at π/4 rad/sample) makes its output grow without limit: the DT version of the lossless LC resonator of 11-02.
2. An eighth-order low-pass with a low cutoff has eight poles crowded near $z = 1$. The polynomial's coefficients are large sums of products of those nearly equal roots, and a tiny change in a coefficient shifts the crowded roots by a much larger amount (the sensitivity grows with the number of nearby roots). A biquad has only two roots, controlled directly by two coefficients, so rounding moves each pole only slightly.
3. The input was switched on at $n = 0$, so the output contains a transient at the filter's own root, $-3.75 \times 0.5^n$, besides the eigen-part $4.75 \times 0.9^n$. The ratio is $4.75 - 3.75\,(0.5/0.9)^n$, and the transient's share falls by a factor $0.5/0.9$ = **0.56** per sample.

## Optional hardware extension

On any microcontroller with a floating-point unit (or in fixed point with CMSIS-DSP's Q15 biquad functions), run Example 11-04.3's filter on a stored impulse and send the first 20 outputs to a serial terminal; compare them with the closed form. Then enter the feedback coefficients with the wrong sign and observe the result.
