# Lab 15-05 · Stability and the Routh–Hurwitz Criterion

Chapter: [15-05 Stability and the Routh–Hurwitz Criterion](../../chapters/15-05-stability-routh-hurwitz.md)

## Objective

Build Routh arrays by program, check the criterion against computed roots, find stability boundaries for a gain, and watch an unstable loop become an oscillator. The ring oscillator of Example 15-05.3 is simulated twice, once in Python and once in ngspice, and its frequency is compared with the Routh boundary frequency.

## Background

Read §3 of the chapter. `routh.py` builds the array row by row as in §3.3, substitutes a small $\varepsilon$ for a zero first entry, and replaces an all-zero row by the derivative of the auxiliary polynomial. The ring oscillator's stages are inverting transconductors whose output current saturates as $\tanh$: small signals see a gain of $-A = -g_mR$ = −2.2 per stage, large signals see less.

## Files

- [routh.py](routh.py): `routh`, `first_column`, `rhp_count`, `jw_roots`, `is_stable` and `gain_range`.
- [15-05-routh-lab.ipynb](15-05-routh-lab.ipynb): the notebook (Parts 1–4).
- [ring3.cir](ring3.cir): a three-stage ring of saturating transconductance stages ($R$ = 1 kΩ, $C$ = 1 nF, $g_m$ = 2.2 mS), kicked by 1 mV.

## Procedure

1. **Criterion against roots (Part 1).** Generate random polynomials of degree 3 to 7, plus polynomials built to have imaginary-axis pairs or a zero first-column entry, and compare `rhp_count` with the roots. *Predict first:* will they ever disagree?
2. **Gain sweep (Part 2).** Plot the roots of Example 15-05.2's characteristic polynomial for $K$ from 1 to 80, and mark where two of them cross the imaginary axis.
3. **Ring oscillator (Part 3).** Compute the linear model's poles for $A$ = 2.2, simulate the nonlinear ring in Python, run `ring3.cir`, and compare the steady frequency with the linear model's frequency and with $\sqrt3 f_0$. *Predict first:* which does the oscillator choose?
4. **Relative stability (Part 4).** Shift the axis to $s = z - 0.5$ for Example 15-05.6 and scan $K$.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Routh count against roots | agreement on every polynomial (to the tolerance of root finding) |
| 2 | Crossing | $K$ = 48 at $\pm j2.83$ rad/s |
| 3 | Linear model at $A$ = 2.2 | poles at $+1.00 \times 10^5 \pm j1.905 \times 10^6$ s⁻¹ (303.2 kHz, growing) |
| 3 | Steady oscillation | 276.2 kHz in Python and ngspice, close to $\sqrt3 f_0$ = 275.7 kHz |
| 4 | Guaranteed decay of 0.5 s⁻¹ | $2.625 < K < 15$ |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-05.a | steady ring frequency | 276.2 | kHz |
| Lab 15-05.b | linear-model growth rate | 1.00e5 | 1/s |
| Lab 15-05.c | linear-model frequency | 303.2 | kHz |
| Lab 15-05.d | Routh boundary frequency √3 f0 | 275.7 | kHz |

## Discussion

1. Why does the oscillator settle near $\sqrt3 f_0$ and not at the linear model's 303 kHz?
2. Why is the steady frequency slightly above $\sqrt3 f_0$?
3. In Part 1, how can floating-point root finding disagree with an exact Routh count, and which would you trust for a polynomial with a pair exactly on the axis?
4. Real ring oscillators in CMOS use inverters, not transconductors with tanh limiting. What carries over from this model, and what does not?

### Answers

1. The linear model's poles are in the right half-plane, so the amplitude grows. As the stages saturate, their effective (describing-function) gain falls. The amplitude stops growing when the effective loop gain reaches the boundary value of 8 (a stage gain of 2). Because tanh limiting adds no phase shift, the boundary sits at the same frequency, where each stage lags 60°: $\sqrt3 f_0$.
2. The waveform is not a pure sinusoid: saturation creates harmonics, and the single-pole stages respond to them, which shifts the zero crossings slightly. The describing-function argument ignores harmonics, so it is accurate to a fraction of a percent here, not exactly.
3. Roots on the axis computed in floating point come out with tiny positive or negative real parts (about $10^{-16}$), so a count based on the sign of the real part is unreliable there. The Routh array with the auxiliary polynomial identifies the axis pair exactly. Away from the axis, the two always agree.
4. The start-up condition (loop gain above the boundary at a frequency where the phase lags 180°) and the role of the number of stages carry over. CMOS inverters switch rail to rail, so the waveform is closer to a square wave, and the frequency is set by the stages' propagation delay rather than by a single small-signal pole (12-09).

## Optional hardware

Build the three-stage ring with a 74HC04 hex inverter (three of its gates) and observe the oscillation on an oscilloscope; then add an RC network at each stage's output and watch the frequency fall as the RC delay comes to dominate the gate delay. Expect about $1/(2.9RC)$, not the small-signal $\sqrt3/(2\pi RC) \approx 1/(3.6RC)$: the gates switch hard, so each stage's delay is the time its RC node takes to cross mid-rail from where it was left half a period earlier (about $0.48RC$), rather than the phase shift of a soft-limiting linear stage.
