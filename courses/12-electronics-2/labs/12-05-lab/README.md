# Lab 12-05 · Feedback: Theory and the Four Topologies

Chapter: [12-05 Feedback: Theory and the Four Topologies](../../chapters/12-05-feedback-topologies.md)

## Objective

Measure how the gain error tracks $1/T$; watch the poles of a two-pole amplifier move as the loop closes, until they become complex; confirm the asymptotic-gain formula against direct solution as $g_m$ varies; and measure how a loop reduces second-harmonic distortion. Confirm Example 12-05.4's stage in ngspice.

## Background

The closed-loop gain and its error (§3.1), bandwidth extension (§3.3), distortion (§3.4), and return-ratio analysis with Blackman's formula (§3.6).

## Files

- [12-05-feedback.ipynb](12-05-feedback.ipynb): the notebook (Parts 1–4).
- [shunt_shunt.cir](shunt_shunt.cir): ngspice operating-point solution of Example 12-05.4's stage as a small-signal circuit, measuring its transresistance and port resistances. Run with `ngspice -b shunt_shunt.cir`, or `python tools/run_spice.py 12-05` from the repository root.

## Procedure

1. **Gain error (Part 1).** Sweep the open-loop gain with β = 0.01 and plot the gain error against the loop gain, with $1/T$ for comparison.
2. **Two poles (Part 2).** For $A_0$ = 10⁴ with poles at 1 kHz and 1 MHz, plot the closed-loop poles as β rises from 10⁻⁵ to 1. Find where they meet, and their quality factor at β = 0.1.
3. **Asymptotic gain (Part 3).** For $g_m$ from 0.5 to 16 mA/V, tabulate $T$, $A_\infty$, $A_{\mathrm{dir}}$, the formula's closed-loop gain and the direct solution.
4. **Distortion (Part 4, the chapter's guided exercise).** *Predict first:* by how much does the loop reduce the second harmonic at the same output level? Then run it.
5. **ngspice.** Run `shunt_shunt.cir` and compare with Example 12-05.4.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Gain error | Follows $1/(1 + T)$: about 1/T once $T$ exceeds 10 |
| 2 | Closed-loop poles | Move together along the real axis, meet, then rise vertically as a complex pair |
| 3 | Asymptotic-gain formula | Equals the direct solution at every $g_m$; $A_\infty$ = −50 kΩ and $A_{\mathrm{dir}}$ = 1.4286 kΩ throughout |
| 4 | Second harmonic | Falls by close to $1 + T$ |
| ngspice | Stage | −42.34 kΩ transresistance; 1.277 kΩ in and out |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-05.a | feedback factor at which the poles meet | 0.02495 | — |
| Lab 12-05.b | where they meet | 500.5 | kHz |
| Lab 12-05.c | quality factor at β = 0.1 | 0.9995 | — |
| Lab 12-05.d | gain error at A = 10³, β = 0.01 | 9.09 | % |

*These are recomputed by [verify_12_05.py](../../verify/verify_12_05.py) from the closed-loop denominator's roots.*

## Discussion questions

1. In Part 2, why do the poles meet at the average of the two open-loop pole frequencies?
2. In Part 3, why are $A_\infty$ and $A_{\mathrm{dir}}$ independent of $g_m$, and what does change?
3. In Part 4, why does the amplifier's error input have about the same amplitude open loop and closed loop?

### Answers

1. The closed-loop denominator is $s^2 + (\omega_1 + \omega_2)s + \omega_1\omega_2(1 + T_0)$: feedback changes only the constant term, so the sum of the poles stays $-(\omega_1 + \omega_2)$. When they coincide each is half the sum, about 500 kHz here; beyond that the real part stays fixed and only the imaginary part grows.
2. $A_\infty$ is the gain with the gate at virtual ground and $A_{\mathrm{dir}}$ the gain with the transistor removed; neither involves $g_m$. Only the return ratio $T$ grows in proportion to $g_m$, which moves $A_f$ from near $A_0$ toward $A_\infty$.
3. The output is held at the same 1 V, and the amplifier needs about 1 mV of input to produce it whether or not a loop is present; what changes is that the loop's input is now about 100 times larger (0.1 V), and the loop subtracts the harmonic the amplifier generates.

## Optional hardware extension

Build a single-transistor common-emitter stage with a collector-to-base feedback resistor, driven from a signal generator through a series resistor (a shunt–shunt stage). Measure its transresistance and input resistance with and without the feedback resistor, and compare with the asymptotic-gain and Blackman predictions using $g_m = I_C/V_T$.
