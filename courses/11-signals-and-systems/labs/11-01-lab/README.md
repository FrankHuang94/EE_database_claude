# Lab 11-01 · Signals: Classification and Operations

Chapter: [11-01 Signals: Classification and Operations](../../chapters/11-01-signals-classification-and-operations.md)

## Objective

Make the chapter's definitions computable: find periods by search rather than by formula, watch a power estimate converge, apply time operations as function composition, see the impulse emerge as a limit of pulses, and see two analog frequencies collapse onto one sequence when sampled.

## Background

Energy and power (§3.2), periodicity in continuous and discrete time (§3.3), time-axis operations (§3.5), the impulse as a limit and its sifting property (§3.6), and discrete-time frequency (§3.7).

## Files

- [11-01-signals.ipynb](11-01-signals.ipynb): the notebook (Parts 1–5). There is no circuit to simulate in this chapter, so there is no netlist.

## Procedure

1. **Periods by search (Part 1).** Search for the smallest $T$ at which each signal of Example 11-01.1 repeats. For $\cos 2t + \cos\pi t$, plot the worst mismatch $\max_t\lvert x(t + T) - x(t)\rvert$ against $T$ up to 60 s and see that it dips but never reaches zero.
2. **Energy and power (Part 2).** Integrate the energy of Example 11-01.2 numerically. Then compute the windowed power $\frac{1}{2T}\int_{-T}^{T}\cos^2(2\pi t)\,dt$ for growing $T$, and compare its deviation from 1/2 with the bound $1/(8\pi T)$.
3. **Time operations (Part 3).** Implement $x(t)$ of Example 11-01.4 as a Python function and build $y(t) = x(4 - 2t)$ by composition. Reproduce Figure 2, including the wrong-order result, and compute $E_y/E_x$.
4. **The impulse as a limit (Part 4, the chapter's guided exercise).** *Predict first:* the value of $\int(t^2 + 1)p_\Delta(t - 2)\,dt$ for a unit-area pulse of width 0.1 s, and how its error changes when Δ halves. Then compute it for Δ = 0.4, 0.2, 0.1, 0.05.
5. **Sampled sinusoids (Part 5).** Sample 3, 7 and 13 kHz cosines at 10 kHz and print the largest difference between the sequences. Repeat with sines and explain the sign.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Periods | 1 s for Example 11-01.1(a); 20 and 24 samples for (c) and (e); no period for (b) or (d) |
| 2 | Windowed power | Deviation from 1/2 bounded by $1/(8\pi T)$, reaching the bound when $\sin 4\pi T = \pm1$ |
| 3 | Energy ratio | $E_y/E_x$ = 1/2 |
| 4 | Sifting with a pulse | Error $\Delta^2/12$, a factor of 4 smaller each time Δ halves |
| 5 | Sampled cosines | Identical to rounding error; the 7 kHz sine is the negated 3 kHz sine |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 11-01.a | sifting with a 0.1 s pulse | 5.000833 | — |
| Lab 11-01.b | error ratio when Δ halves | 4 | — |
| Lab 11-01.c | windowed power of cos 2πt at T = 10.125 s | 0.5039 | — |
| Lab 11-01.d | E_y / E_x | 0.5 | — |
| Lab 11-01.e | near-period of cos 2t + cos πt below 30 s | 22 | s |
| Lab 11-01.f | phase slip of cos 2t at that near-period | 0.018 | rad |
| Lab 11-01.g | windowed-power excess at T = 10.125 s | 0.0039 | — |

## Discussion questions

1. In Part 1, why does a numerical period search need a tolerance, and how can it mislead you for $\cos 2t + \cos\pi t$?
2. In Part 2, the windowed power at $T$ = 10.125 s exceeds 1/2 by **0.0039**. Why does a window that is not a whole number of periods bias the estimate, and why does the bias shrink as $1/T$?
3. In Part 4, why does the pulse's error depend on the second derivative of $t^2 + 1$ and not on the first?

### Answers

1. Floating-point arithmetic never gives an exact zero, so the search accepts a mismatch below a small tolerance. For $\cos 2t + \cos\pi t$ there are values of $T$ at which the mismatch is small. The best below 30 s is $T \approx$ **22** s: there $\cos\pi t$ completes exactly 11 cycles, and $2T$ = 44 rad is within **0.018** rad of $14\pi$, so $\cos 2t$ is only slightly out of step; a loose tolerance would wrongly report a period. Only the rationality argument of §3.3 settles the question.
2. The average of $\cos^2$ over whole periods is exactly 1/2; a window with a partial period adds or misses part of one oscillation of the $\cos 4\pi t$ term, an error of at most $\int\lvert\cos\rvert$ over half a cycle divided by the window length $2T$, which is $1/(8\pi T)$. The longer the window, the less a partial period matters.
3. Averaging $f$ over a symmetric interval $[t_0 - \Delta/2, t_0 + \Delta/2]$ cancels the linear term of its Taylor series (the first derivative's contributions on the two sides are equal and opposite), leaving $f''(t_0)\Delta^2/24$ as the leading error. With $f'' = 2$ that is $\Delta^2/12$ (01-08, Taylor series).

## Optional hardware extension

With a function generator and an oscilloscope that can sample at a chosen rate (or a USB audio interface at 48 kHz and a free recording program), generate a 3 kHz tone and then a 45 kHz tone, sample both at 48 kHz, and compare the recorded waveforms. The 45 kHz tone appears at 3 kHz, provided the interface's own anti-aliasing filter does not remove it first; most audio interfaces do, which is the point of 11-10.
