# Lab 10-05 · Amplifier Fundamentals

Chapter: [10-05 Amplifier Fundamentals](../../chapters/10-05-amplifier-fundamentals.md)

## Objective

Use amplifier models to see where a signal chain loses gain, find the best order for a set of stages, measure how far a real transistor stage can swing and how efficient it is at realistic signal levels, and plot a front end's low-frequency response.

## Background

Gains and decibels (§3.1), the four models (§3.2), loading and cascades (§3.3–3.4), swing (§3.6), coupling capacitors (§3.7) and efficiency (§3.8). Part 3 uses the exponential transistor of 10-04 and the exact harmonics $2I_1(x)$ and $I_0(x)$ of $e^{x\cos\theta}$ (10-04 §3.6) for the signal and supply currents.

## Files

- [10-05-amplifiers.ipynb](10-05-amplifiers.ipynb): the notebook (Parts 1–4).
- [amp_cascade.cir](amp_cascade.cir): ngspice cascades of Examples 10-05.2 and 10-05.5 from controlled sources, and the coupling-capacitor corner of Example 10-05.7.

## Procedure

1. **Bridging against matching (Part 1, the chapter's guided exercise).** *Predict first:* for Example 10-05.2's amplifier driven by 10 mV rms, at what load is the load power largest, and what is the voltage gain there? Then sweep $R_L$ from 10 Ω to 1 MΩ and plot both.
2. **Stage order (Part 2).** *Predict first:* for stages X and Y of Problem 10-05.6 plus a buffer Z ($R_i$ = 100 kΩ, $A_{vo}$ = 1, $R_o$ = 50 Ω), between a 50 kΩ source and a 1 kΩ load, which of the six orders is best? Then evaluate all six.
3. **Swing and efficiency (Part 3).** For the common-emitter stage of the chapter's Figure 2, compute the output's fundamental amplitude, the signal power in $R_C$, the supply power and the efficiency for inputs from 1 to 17 mV, and find the input amplitude at which the output first touches saturation.
4. **Front-end frequency response (Part 4).** Plot the gain of Example 10-05.7's front end from 1 mHz to 10 Hz with its 330 nF coupling capacitor.
5. **ngspice.** Run `python tools/run_spice.py 10-05`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Load power | peaks at $R_L = R_o$, where the gain is half its open-circuit value |
| 2 | Best order | X → Z → Y: the buffer goes where the worst interface was |
| 3 | Efficiency | a few percent at 10 mV input, far below the 25% limit; the output reaches saturation before a 20 mV input |
| 4 | Response | within 0.2% of midband by 1 Hz |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-05.a | load for maximum power | 2 | kΩ |
| Lab 10-05.b | maximum load power | 0.222 | mW |
| Lab 10-05.c | voltage gain at maximum power | 66.7 | — |
| Lab 10-05.d | best-order gain (X, Z, Y) | 767.9 | — |
| Lab 10-05.e | worst-order gain (Y, Z, X) | 3.493 | — |
| Lab 10-05.f | output fundamental at 10 mV | 1.970 | V |
| Lab 10-05.g | signal power at 10 mV | 0.388 | mW |
| Lab 10-05.h | supply power at 10 mV | 10.38 | mW |
| Lab 10-05.i | efficiency at 10 mV | 3.74 | % |
| Lab 10-05.j | input that first reaches saturation | 17.40 | mV |
| Lab 10-05.k | positive output peak there | 7.449 | V |
| Lab 10-05.l | front-end gain at 0.1 Hz | 1170 | — |
| Lab 10-05.m | front-end gain at 1 Hz | 1295 | — |

## Discussion questions

1. In Part 3 the supply power rises with the signal (10.38 mW at 10 mV against 10 mW at rest). Where does the extra current come from, and does it contradict §3.8's "the supply current averages $I_Q$ whatever the signal"?
2. Why is the best order in Part 2 not "buffer first", as it was in Example 10-05.7?
3. When the output first touches saturation (Part 3), the positive peak is only 2.45 V above the bias point while the negative peak is 4.8 V below it. What does that say about where to bias a bare BJT stage for symmetric swing?

### Answers

1. The exponential's even-order terms raise the average collector current by $I_C[I_0(x) - 1]$, 3.8% at 10 mV (10-04 lab). §3.8's statement is for a *linear* class-A stage; a real transistor rectifies part of the signal, which a DC-coupled design must allow for.
2. X already has a 1 MΩ input, so the source interface is good without a buffer. The worst interface in the X → Y order is X's 10 kΩ output into Y's 2 kΩ input (factor 1/6), and that is where the buffer helps most. A buffer belongs at the worst interface, wherever it is.
3. Without feedback, the exponential compresses the positive output swing (current falling) and stretches the negative swing (current rising), so distortion, not the bias-point arithmetic of §3.6, limits the usable swing. Linear swing requires feedback or degeneration (10-07, Course 12); then the §3.6 bias rule applies.

## Optional hardware extension

Build Example 10-05.4's measurement on any audio amplifier or op-amp stage: read the output open-circuit and with a load near the expected output resistance, then repeat with a load ten times larger and compare the scatter of the two estimates. (A meter's resolution is a fixed absolute error, so the load near $R_o$ should give the tighter estimate; chapter §3.3.)
