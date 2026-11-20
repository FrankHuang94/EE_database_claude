# Lab 15-07 · Frequency-Domain Design: Bode, Nyquist and Margins

Chapter: [15-07 Frequency-Domain Design](../../chapters/15-07-frequency-domain-design.md)

## Objective

Read stability from a loop gain's frequency response. You will plot Bode and Nyquist diagrams with their margins, count Nyquist encirclements for a loop with an unstable plant, check Bode's sensitivity integral numerically, and measure an op-amp's loop gain in ngspice by voltage injection.

## Background

Read §3 of the chapter. `freqdomain.margins` finds crossovers by root finding on $\lvert L\rvert - 1$ and on a phase built factor by factor (so it never wraps). `nyquist_encirclements` traces the Nyquist contour, with small indentations around imaginary-axis poles and a large closing arc, and counts how many times $1 + KL$ winds around the origin. `bode_integral` integrates $\ln\lvert S(j\omega)\rvert$ decade by decade.

## Files

- [freqdomain.py](freqdomain.py): `freq_resp`, `margins`, `nyquist_encirclements`, `closed_loop_rhp`, `sensitivity_peak`, `bode_integral` and `pm_from_zeta`.
- [15-07-frequency-domain-lab.ipynb](15-07-frequency-domain-lab.ipynb): the notebook (Parts 1–4).
- [opamp_loop.cir](opamp_loop.cir): a two-pole op-amp macromodel as a unity-gain buffer, with an AC injection source in the feedback path.

## Procedure

1. **Bode and Nyquist (Part 1).** Plot Examples 15-07.1, 15-07.2 and 15-07.4 and mark the margins. *Predict first:* which of the three has a finite gain margin?
2. **Encirclements (Part 2).** For Example 15-07.5, count encirclements for $K$ from 2 to 30 and compare $Z = N + P$ with the closed-loop roots.
3. **The waterbed (Part 3).** Plot $\ln\lvert S\rvert$ for Example 15-07.2's loop at $K$ = 4, 8.3 and 20, and integrate each.
4. **Injection in ngspice (Part 4).** Run `opamp_loop.cir`, then edit the second pole to 10 MHz and rerun. *Predict first:* the new phase margin.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Margins | Example 15-07.1 infinite GM; 15-07.2 GM 5.79; 15-07.4 GM 3.14 |
| 2 | Encirclements | $Z$ = 0 for $K > 7.5$, $Z$ = 2 below, matching the roots |
| 3 | Bode integral | zero for every stable gain; the peak of $\lvert S\rvert$ grows with $K$ |
| 4 | Injection | 9.10 MHz and 65.5° at $f_2$ = 20 MHz; about 7.86 MHz and 51.8° at 10 MHz |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-07.a | sensitivity peak at K = 4 | 1.28 | — |
| Lab 15-07.b | sensitivity peak at K = 20 | 2.83 | — |
| Lab 15-07.c | crossover with f2 = 10 MHz | 7.86 | MHz |

## Discussion

1. Why does an integrator in the loop make the Nyquist plot swing around through infinity, and how does the contour's indentation handle it?
2. In Part 2, why does raising the gain stabilize the loop rather than destabilize it?
3. In Part 3, why does a larger gain raise the sensitivity peak even though the integral stays at zero?
4. Why must the injection source sit where it does, between the amplifier output and the feedback network, for the measurement to be accurate?

### Answers

1. Near $s = 0$, $L \approx K_0/s$ is huge. The indentation $s = \varepsilon e^{j\theta}$, $\theta$ from −90° to +90°, maps to $(K_0/\varepsilon)e^{-j\theta}$, a large arc swinging clockwise through 180°. Without the indentation the contour would pass through a pole and the argument principle would not apply.
2. The plant has an unstable pole, so the plot must encircle −1 once counterclockwise. That happens only when the negative-real-axis crossing, at $-K/7.5$, lies to the left of −1, which needs a large enough gain.
3. With more gain, $\lvert S\rvert$ is smaller at low frequency (more negative area), so the positive area must grow by the same amount. It does so mostly as a taller, narrower peak near the now-higher crossover, closer to −1.
4. The ratio $-v_x/v_y$ equals the loop gain only if inserting the source does not change how the loop loads itself. At the amplifier output (a low-impedance source) feeding a high-impedance input, the injected source sees no current division. At a high-impedance node, a voltage injection would mis-measure the loop gain, and a current injection (or a combination of both) is needed.

## Optional hardware

With a network analyzer (or a function generator and a two-channel oscilloscope) and a 10 Ω injection resistor in the feedback path of an op-amp buffer driving a capacitive load, measure $v_x/v_y$ across frequency and compare the phase margin with and without a 100 Ω isolation resistor at the output.
