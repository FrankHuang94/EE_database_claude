# Lab 11-02 · Systems and Their Properties

Chapter: [11-02 Systems and Their Properties](../../chapters/11-02-system-properties.md)

## Objective

Turn the chapter's definitions into tests you can run: refute (or gather evidence for) linearity, time invariance and causality with random inputs; construct the worst bounded input for a recursion; measure harmonic distortion with an FFT; and see why an exact but unstable inverse fails where a delayed approximate inverse works.

## Background

Linearity and time invariance (§3.3–3.4) are both "two paths must agree" tests; causality (§3.5) asks whether changing the future input changes the past output. The first-order recursion's stability bound and its worst-case input are derived in §3.6; the distortion formulas in §3.3; the echo channel and its inverses in §3.7 and Example 11-02.7.

## Files

- [11-02-systems.ipynb](11-02-systems.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Property tester (Part 1).** Code eight systems from the chapter's library as functions of a whole sequence, and test each with 20 random inputs, scale factors and shifts. Compare with the chapter's table.
2. **Worst bounded input (Part 2).** For $a = -0.8$, build the input that maximizes $\lvert y[29]\rvert$ and compare with a step.
3. **Distortion by FFT (Part 3, the chapter's guided exercise).** *Predict first:* how HD2 and HD3 change when the input of Example 11-02.5 rises from 0.1 V to 0.3 V. Then measure them at four levels and fit the slopes.
4. **Inverse systems (Part 4).** Recover a random ±1 data sequence through the echo channel with 1 mV rms of receiver noise, for $b$ = 0.5 and $b$ = 2. Then build the 8-tap delayed approximation of the noncausal inverse for $b$ = 2 and check the cascade.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Classification | Two nonlinear systems (offset, squarer), two time-varying (modulator, decimator), two noncausal (centered average, decimator) |
| 2 | Worst input | Nearly the bound $1/(1 - \lvert a\rvert) = 5$, about **9** times the step's limiting value |
| 3 | Distortion | 20 dB per decade for HD2, 40 dB per decade for HD3 |
| 4 | Inverses | Millivolt errors for $b$ = 0.5; astronomically large ones for $b$ = 2; a clean delayed inverse with a small residual |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-02.a | nonlinear systems found | 2 | — |
| Lab 11-02.b | time-varying systems found | 2 | — |
| Lab 11-02.c | noncausal systems found | 2 | — |
| Lab 11-02.d | worst-case magnitude of y[29], a = −0.8 | 4.994 | — |
| Lab 11-02.e | step's limiting value, a = −0.8 | 0.5556 | — |
| Lab 11-02.f | HD2 at 0.3 V | −42.49 | dB |
| Lab 11-02.g | HD3 at 0.3 V | −66.92 | dB |
| Lab 11-02.h | HD2 slope | 20.00 | dB/decade |
| Lab 11-02.i | HD3 slope | 40.00 | dB/decade |
| Lab 11-02.j | samples for a 1 mV error to exceed 1 V, b = 2 | 10 | — |
| Lab 11-02.k | residual of the 8-tap delayed inverse | 0.0039 | — |
| Lab 11-02.l | worst case / step's limiting value | 9 | — |

## Discussion questions

1. The tester reported the offset amplifier S1 as time-invariant but not linear. Is that right, and why did the first version of a time-invariance test (comparing every sample, including the first few) wrongly call it time-varying?
2. In Part 2, why is the worst input for $a = -0.8$ an alternating sequence, and why does its phase matter?
3. In Part 4, the exact inverse for $b$ = 2 fails catastrophically while an 8-tap approximation works. What does the approximation give up, and how would you trade its length against its accuracy?

### Answers

1. Yes: S1's rule does not depend on time, so delaying the input delays the output, but $\mathcal{T}\{0\} = 0.05 \ne 0$, so it is not linear. On a finite record that starts at $n = 0$, the delayed output has to be "filled in" for $n < k$. Filling with zeros assumes the system's output is zero before its input starts, which is true only for a linear system at rest. The fair comparison starts at $n = k$, where both paths are defined from real data. Edge effects like this are a common source of wrong conclusions in numerical tests.
2. $y[N] = \sum_k(-0.8)^kx[N - k]$, and the weights alternate in sign. Choosing $x[N - k]$ with the same sign as $(-0.8)^k$ makes every term positive, which needs an input that alternates with a specific phase relative to the chosen time $N$. The same alternating input with the opposite phase would make $y[N]$ as negative as possible; one shifted by one sample relative to that would push the output toward zero at $N$.
3. It gives up causality without delay (it needs an 8-sample latency) and exactness (a residual of $0.5^8 \approx 0.0039$ at the edge of its window, interference left in the output). Each extra tap halves the residual and adds one sample of latency; a link designer picks the shortest length whose residual is small compared with the noise.

## Optional hardware extension

Feed a 1 kHz sine from a sound card or signal generator into any small audio amplifier or op-amp stage, record its output with a sound card at 48 kHz, and compute the FFT as in Part 3 at several input levels. Plot HD2 and HD3 against level: a slope of 20 or 40 dB per decade identifies second- or third-order behavior, and a sudden jump marks clipping.
