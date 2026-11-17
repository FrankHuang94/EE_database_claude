# Lab 02-04 · Forced Response and Resonance

**Chapter:** [02-04](../../chapters/02-04-forced-response-and-resonance.md) · **Notebook:** [02-04-resonance.ipynb](02-04-resonance.ipynb) · **Netlists:** [rlc_ac.cir](rlc_ac.cir), [nfc_tank.cir](nfc_tank.cir) · **Time:** about 75 minutes

## Objective

1. Find a sinusoidal steady state by complex replacement, and see how long a simulation must wait for it.
2. Measure the resonant peak of a second-order low-pass and compare with $\omega_0\sqrt{1 - 2\zeta^2}$ and $1/(2\zeta\sqrt{1 - \zeta^2})$.
3. Confirm that the half-power bandwidth of a band-pass is exactly $\omega_0/Q$, centered geometrically.
4. Watch beats turn into linear growth, and linear growth into a saturating build-up, as tuning and damping change.
5. Confirm the chapter's frequency responses with ngspice AC analyses.

## Background

Chapter sections 3.3 (exponential response formula), 3.4 (frequency response and peak), 3.5 (bandwidth), 3.6 (undamped resonance and beats) and 3.7 (build-up), and Examples 02-04.2 and 02-04.4.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict how many cycles a $Q = 20$ resonator needs to come within 1% of steady state.
3. **Part 2:** predict the ζ at which the peak disappears.
4. **Part 3:** check $r_2 - r_1 = 1/Q$ and $r_1r_2 = 1$ for four values of $Q$.
5. **Part 4:** compare the three time-domain plots.
6. **Part 5:** from the repository root, run `python tools/run_spice.py 02-04`. Then change `R1` in `nfc_tank.cir` to 10.65 Ω, predict the gain at the upper sideband, and re-run.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $\lvert H(j\omega_0)\rvert$ at $Q = 20$ | 20 |
| 1 | cycles to reach 99% | 29 (theory $Q\ln100/\pi = 29.3$) |
| 2 | peak at ζ = 0.1 | $r = 0.9899$, gain 5.025 |
| 2 | peak at ζ = 0.5 | $r = 0.7071$, gain 1.155 |
| 2 | peak disappears | for ζ ≥ 0.707 |
| 3 | $r_2 - r_1$ and $r_1r_2$ | $1/Q$ and 1, for Q = 0.7, 2, 10, 50 |
| 5 | `rlc_ac.cir` | peak 2.066 at 1488.8 Hz (9354 rad/s); gain 2.000 at 1591.5 Hz |
| 5 | `nfc_tank.cir` | half-power points 13.32 and 13.80 MHz; 0.2787 at 14.41 MHz |
| 5 | `nfc_tank.cir` with $R$ = 10.65 Ω | 0.718 at the upper sideband (Q = 8), close to half power |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-04.a | cycles to 99 % at Q = 20, theory | 29.3 | — |
| Lab 02-04.b | peak gain at ζ = 0.5 | 1.155 | — |
| Lab 02-04.c | peak frequency of rlc_ac.cir | 1488.8 | Hz |
| Lab 02-04.d | f0 of rlc_ac.cir | 1591.5 | Hz |
| Lab 02-04.e | upper sideband gain with R = 10.65 Ω | 0.718 | — |
| Lab 02-04.f | upper sideband frequency | 14.41 | MHz |

## Discussion questions

1. A colleague measures a resonator's gain by driving it at $\omega_0$ for 10 cycles and reading the amplitude. For $Q = 100$, how wrong is the measurement, and how should it be done instead?
2. Why does the half-power band of a low-$Q$ band-pass extend much further above $\omega_0$ than below it?
3. In Part 4, damping turns linear growth into a saturating build-up. What sets the final amplitude, and how long does it take to get there?

## Optional hardware version

With a 10 mH inductor, a 100 nF capacitor, a 100 Ω resistor, a function generator and an oscilloscope: build the series RLC ($f_0 \approx 5$ kHz) and sweep the generator from 2 to 10 kHz, measuring the resistor voltage. Find the peak and the two frequencies where the voltage is $1/\sqrt2$ of the peak, and compute $Q = f_0/(f_2 - f_1)$. Compare with $\omega_0L/R$; the measured $Q$ will be lower, because the inductor's winding resistance adds to the 100 Ω. Then measure the capacitor voltage at $f_0$: it should be $Q$ times the source.
