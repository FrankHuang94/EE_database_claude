# Lab 12-09 · Oscillators

Chapter: [12-09 Oscillators](../../chapters/12-09-oscillators.md)

## Objective

See where RC feedback networks reach zero phase; watch a Wien-bridge oscillator grow from a millivolt and settle where its describing-function gain equals three; find the Colpitts oscillator's critical transconductance from its poles; and map a crystal's reactance and pulling. Simulate the Wien oscillator in ngspice.

## Background

The Barkhausen criterion (§3.1), RC oscillators (§3.2), LC oscillators (§3.3), crystals (§3.4) and amplitude stabilization (§3.6).

## Files

- [12-09-oscillators.ipynb](12-09-oscillators.ipynb): the notebook (Parts 1–4).
- [wien.cir](wien.cir): ngspice transient simulation of a Wien-bridge oscillator with a behavioural tanh amplifier, measuring its frequency and amplitude after it settles. Run with `ngspice -b wien.cir`, or `python tools/run_spice.py 12-09` from the repository root.

## Procedure

1. **Networks (Part 1).** Plot |β| and phase for the Wien bridge and the three-section ladder against ωRC; check β = 1/3 and −1/29 at the zero-phase points.
2. **Startup (Part 2, the chapter's guided exercise).** *Predict first:* exactly 1592 Hz? Then integrate the oscillator from 1 mV and measure its settled frequency and amplitude.
3. **Colpitts (Part 3).** Sweep $g_m$ and plot the largest real part of the natural frequencies.
4. **Crystal (Part 4).** Plot the reactance from 20 kHz below to 50 kHz above $f_s$, and the frequency offset against load capacitance.
5. **ngspice.** Run `wien.cir` and compare with Part 2.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Zero-phase points | Wien 1/3 at ωRC = 1; ladder −1/29 at ωRC = √6 |
| 2 | Wien oscillator | Exponential growth, then a steady amplitude matching the describing function |
| 3 | Colpitts | Real part crosses zero at 1 mA/V, at 7.118 MHz |
| 4 | Crystal | Inductive only between $f_s$ and $f_p$ (25 kHz wide); pulling falls with $C_L$ |
| ngspice | Wien oscillator | The same frequency and amplitude as Part 2 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-09.a | settled frequency | 1584 | Hz |
| Lab 12-09.b | amplitude at the bridge output | 0.1949 | V |

*These are recomputed by [verify_12_09.py](../../verify/verify_12_09.py) by integrating the oscillator's two state equations from the same initial condition.*

## Discussion questions

1. Why does the oscillator's frequency fall slightly below $1/(2\pi RC)$?
2. Why is the describing function so accurate here?
3. Why does more load capacitance lower a crystal oscillator's frequency?

### Answers

1. The tanh amplifier generates odd harmonics; the bridge passes them with phase shift, and the loop's phase balance at the fundamental moves slightly to compensate.
2. The bridge is a band-pass filter that strongly attenuates the harmonics, so the signal at the amplifier input is nearly sinusoidal: the describing function's one assumption.
3. The motional branch resonates with $C_0 + C_L$ in series with its own $C_m$; a larger $C_L$ adds less series elastance, moving the resonance toward $f_s$.

## Optional hardware extension

Build a Wien-bridge oscillator with a general-purpose op-amp, $R$ = 10 kΩ and $C$ = 10 nF, and two antiparallel diodes in series with part of the feedback resistor for amplitude limiting. Measure its frequency and amplitude with an oscilloscope, then change the diode-shunted resistor and watch the amplitude and distortion trade against each other.
