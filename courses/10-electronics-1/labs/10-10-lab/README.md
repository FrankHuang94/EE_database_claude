# Lab 10-10 · Op-Amp Application Circuits

Chapter: [10-10 Op-Amp Application Circuits](../../chapters/10-10-op-amp-application-circuits.md)

## Objective

See each application circuit's dominant limit in numbers: the statistical spread of a difference amplifier's CMRR, the frequency dependence of a precision rectifier's error, the effect of hysteresis on comparator chatter, and how a transimpedance amplifier's feedback capacitor trades flatness against settling.

## Background

Difference-amplifier CMRR (§3.1), precision rectifiers (§3.3), Schmitt triggers (§3.4) and the transimpedance amplifier as a second-order loop (§3.5).

## Files

- [10-10-applications.ipynb](10-10-applications.ipynb): the notebook (Parts 1–4).
- [applications.cir](applications.cir): ngspice checks of Example 10-10.1(a) and Example 10-10.7.

## Procedure

1. **CMRR Monte Carlo (Part 1, the chapter's guided exercise).** *Predict first:* the median CMRR of a unity-gain difference amplifier with 0.1% resistors whose errors are uniform within tolerance. Then sample 20,000 amplifiers.
2. **Rectifier error against frequency (Part 2).** Model a precision half-wave rectifier whose output stays at zero for a dead time $2V_D/\text{SR}$ after each rising zero crossing (Example 10-10.4) and compute the error of the output's average value at 1, 10 and 100 kHz.
3. **Hysteresis against noise (Part 3).** Count output transitions for the noisy ramp of Figure 1 with 0, 20, 50 and 100 mV of hysteresis.
4. **TIA step response (Part 4).** Simulate the step response of Example 10-10.7's TIA for several $C_F$ and measure 1% settling time.
5. **ngspice.** Run `python tools/run_spice.py 10-10`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | CMRR | a median about 14 dB better than the worst case; very few units near it |
| 2 | Rectifier | average error tiny at 1 kHz, growing with the square of frequency |
| 3 | Chatter | dozens of transitions without hysteresis, one with 50 mV or more |
| 4 | Settling | the maximally flat design is not the fastest to settle to 1% |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-10.a | median CMRR | 67.9 | dB |
| Lab 10-10.b | fraction below 60 dB | 8.22 | % |
| Lab 10-10.c | lowest CMRR in the sample | 54.5 | dB |
| Lab 10-10.d | rectifier average error at 10 kHz | 0.00336 | % |
| Lab 10-10.e | rectifier average error at 100 kHz | 0.336 | % |
| Lab 10-10.f | transitions, no hysteresis | 111 | — |
| Lab 10-10.g | transitions, 20 mV hysteresis | 23 | — |
| Lab 10-10.h | transitions, 50 mV hysteresis | 1 | — |
| Lab 10-10.i | 1% settling, Butterworth C_F | 1.05 | µs |

## Discussion questions

1. Why is the worst-case CMRR (54 dB) almost never observed in Part 1?
2. In Part 2, why does the rectifier's average error grow with the square of frequency when Example 10-10.4's missed voltage grows only linearly?
3. In Part 4, a slightly larger $C_F$ than the Butterworth value settles faster to 1%. Why, and why might a designer still choose the Butterworth value?

### Answers

1. The worst case needs all four resistors at opposite ends of their tolerance at once; with independent errors, the sum $\delta_2 - \delta_1$ of four errors is usually much smaller than $4\varepsilon$ (03-04: sums of independent errors grow as the square root of their number, not linearly).
2. The missed part of each cycle is the area under the sine during the dead time, $\int_0^{\Delta t}V_p\sin\omega t\,dt \approx V_p\omega\Delta t^2/2$: the height grows with frequency and so does the fraction of the period the dead time occupies, giving $f^2$ overall.
3. A 1% settling specification rewards a response whose overshoot just stays inside the 1% band; a lower Q gives that. The Butterworth response is maximally flat in frequency, which matters for a receiver that must pass a band of frequencies evenly; settling and flatness are different specifications.

## Optional hardware extension

Build the Schmitt trigger of Example 10-10.5 with any comparator, drive it from a slow ramp plus a small noise source (or a noisy potentiometer), and watch the output with and without $R_2$ on an oscilloscope.
