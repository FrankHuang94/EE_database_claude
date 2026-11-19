# Lab 10-01 · Diodes and Diode Circuits

Chapter: [10-01 Diodes and Diode Circuits](../../chapters/10-01-diodes-and-diode-circuits.md)

## Objective

Solve diode circuits the way a simulator does, and measure how far the hand models of the chapter are from the exponential diode: in a resistor circuit, in a peak rectifier, in a Zener regulator and in wave-shaping circuits.

## Background

The chapter derives four diode models (§3.1–3.3), the small-signal resistance (§3.4), the peak rectifier's ripple, conduction interval and diode current (§3.6), the Zener regulator's line and load regulation (§3.7), and limiters, clamps and doublers (§3.8). This lab integrates the circuits' differential equations directly, with an exponential diode, and compares.

## Files

- [10-01-diodes.ipynb](10-01-diodes.ipynb): the notebook (Parts 1–4).
- [diode_bias.cir](diode_bias.cir): ngspice operating point of Example 10-01.1.
- [rectifier.cir](rectifier.cir): ngspice half-wave peak rectifier with an exponential "course rectifier diode" ($I_S$ = 10 nA, $n$ = 1.9; a teaching model, not a particular part).
- [zener.cir](zener.cir): ngspice Zener regulator of Example 10-01.6 at 8 V and 10 V supply.

## Procedure

1. **Solving one diode (Part 1).** *Predict first:* from which starting voltages will Newton's method overshoot? Then solve Example 10-01.1 by fixed-point iteration, Newton's method and Lambert W, and map the number of Newton steps against the starting guess.
2. **A real peak rectifier (Part 2, the chapter's guided exercise).** *Predict first:* with an exponential diode instead of a 0.7 V drop, will the ripple and the peak diode current rise or fall? Then simulate Example 10-01.4 with the course rectifier diode, and repeat the constant-drop simulation with a 500 Ω load.
3. **Zener regulator (Part 3).** Sweep the supply from 7 to 11 V and the load from 0 to 60 mA; find where the Zener drops out of regulation, and compare with a 0.2 Ω shunt reference.
4. **Wave shaping (Part 4).** Plot the limiter's transfer curve, and simulate the clamp and doubler from switch-on until they settle.
5. **ngspice.** Run the three netlists with `python tools/run_spice.py 10-01`; each checks its result against the keys below or in the chapter.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Newton steps | three to reach 4 digits from 0.7 V; overshoot from any start above the answer is avoided only by step limiting |
| 2 | Exponential diode | lower ripple and a much lower peak current than the constant-drop model |
| 2 | 500 Ω load | ripple about twice, peak current about $\sqrt2$ times the 1 kΩ values |
| 3 | Dropout | the Zener current reaches zero at low supply and heavy load |
| 4 | Clamp | settles to its steady-state shift within a few tens of cycles |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-01.a | ripple with the exponential rectifier diode | 0.364 | V |
| Lab 10-01.b | average output with the exponential diode | 11.05 | V |
| Lab 10-01.c | peak diode current with the exponential diode | 371 | mA |
| Lab 10-01.d | ripple at 500 Ω, constant drop | 0.731 | V |
| Lab 10-01.e | peak diode current at 500 Ω, constant drop | 752 | mA |
| Lab 10-01.f | Zener V_O at 10 V, 50 mA | 5.028 | V |
| Lab 10-01.g | peak-current reduction from the exponential diode | 31 | % |
| Lab 10-01.h | Zener dropout supply at 60 mA | 8.12 | V |
| Lab 10-01.i | exponential diode drop at its peak current | 0.856 | V |

## Discussion questions

1. The exponential diode lowers the peak diode current by about a third compared with the constant-drop model. Why?
2. Why does the average output fall from 11.11 V (constant drop) to 11.05 V with the exponential diode?
3. At what supply voltage does the Zener regulator of Example 10-01.6 stop regulating with a 60 mA load, and what happens to $V_O$ below it?
4. Why does a circuit simulator limit the voltage step of Newton's method on a diode, and what would happen without it?

### Answers

1. The constant-drop model makes the diode a switch that turns on abruptly when the source reaches $V_O + 0.7$ V, so the capacitor must be charged by a steep current pulse. The exponential diode starts conducting earlier and gradually, as the source rises through the region where $v_D$ is 0.6–0.8 V, so the same charge is delivered over a longer interval at a lower peak: **371** mA instead of 540 mA, **31**% lower.
2. At its 371 mA peak the exponential diode drops **0.856** V rather than 0.7 V, so the capacitor charges to a lower peak; the smaller ripple partly compensates, and the average falls to **11.05** V.
3. The Zener current is $(V_S - V_O)/R - I_L$; it reaches zero when $V_S = V_{Z0} + RI_L$ = 4.757 + 56 × 0.060 = **8.12** V (the piecewise-linear model's $V_O$ at zero Zener current is $V_{Z0}$). Below that the Zener is off and the circuit is just a resistor feeding the load: $V_O = V_S - RI_L$, falling volt for volt with the supply.
4. The exponential's slope at a high trial voltage is enormous, so a Newton step from there is tiny and accurate, but a step from a low trial voltage lands far beyond the answer, where $e^{v/V_T}$ overflows. Simulators clip each step to a few $V_T$ (or work on the logarithm) so the iteration approaches the answer from safe territory.

## Optional hardware extension

With a 1N4001, a 1000 µF capacitor, a 1 kΩ resistor and a 12 V AC adapter (or a signal generator and a power amplifier), measure the ripple and compare with §3.6. With a 1N4733A, a 56 Ω resistor and a bench supply, measure line and load regulation. A current-sense resistor of 0.1 Ω in series with the rectifier diode shows the narrow current pulses on an oscilloscope.
