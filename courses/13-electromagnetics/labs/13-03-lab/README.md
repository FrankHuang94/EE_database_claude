# Lab 13-03 · Magnetostatics and Inductance

Chapter: [13-03 Magnetostatics and Inductance](../../chapters/13-03-magnetostatics-and-inductance.md)

## Objective

Compute magnetic fields and inductances numerically and check them against the chapter's closed forms: the Biot–Savart field of a loop, the inductance of a finite solenoid from loop-by-loop mutual inductances, the partial inductance of a bond wire from the Neumann integral, and the current range of a gapped core whose ferrite saturates. Then simulate ground bounce across a bond wire's inductance in ngspice.

## Background

The Biot–Savart law (§3.1), inductance by flux linkage and partial inductance (§3.5), and magnetic circuits with air gaps (§3.6).

## Files

- [13-03-magnetostatics.ipynb](13-03-magnetostatics.ipynb): the notebook (Parts 1–4).
- [ground_bounce.cir](ground_bounce.cir): a 0 to 40 mA current ramp in 400 ps through a 2 nH inductor. Run with `ngspice -b ground_bounce.cir`, or `python tools/run_spice.py 13-03` from the repository root.

## Procedure

1. **The Biot–Savart law (Part 1).** Approximate a 1 cm loop carrying 1 A by inscribed polygons of 4 to 64 sides and compare the centre field with the circle's. Then compute the field on the axis at $z = 2R$. *Predict first:* is the square's centre field higher or lower than the circle's?
2. **A finite solenoid (Part 2).** For 200 turns on a 5 mm radius, compute the Nagaoka factor against length from the current-sheet integral of loop mutual inductances, and find the length at which the long-solenoid formula is 5% high.
3. **Bond wires (Part 3).** Compute the partial self-inductance of a 25 µm wire from 0.5 to 5 mm by the Neumann integral and the formula, and plot nanohenries per millimetre.
4. **Saturation (Part 4).** With a $\tanh$ $B$–$H$ curve ($\mu_r$ = 2000, $B_s$ = 0.4 T, illustrative), find the current that brings Example 13-03.4's core to 0.3 T with and without its 1 mm gap.
5. **ngspice (the chapter's guided exercise).** Predict the voltage across the inductor during and after the ramp, and the area under the voltage pulse. Then run `ground_bounce.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Polygon centre field | The square is 27% high; the excess falls as $(\pi/n)^2/3$, about 0.08% at 64 sides |
| 2 | Nagaoka factor | 0.9201 at 5 cm; rising toward 1 only slowly as the coil lengthens |
| 3 | nH per mm | Rising from about 0.68 at 0.5 mm to above 1.1 at 5 mm; formula and integral agree within 0.5% |
| 4 | Gapped against ungapped current | A ratio below the linear factor of 21, because the core needs extra $H$ near saturation |
| ngspice | Inductor voltage | A flat 0.2 V during the ramp, zero after; pulse area $L\,\Delta I$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-03.a | loop field on the axis at z = 2R (R = 1 cm, 1 A) | 5.620 | µT |
| Lab 13-03.b | solenoid length at which the long formula is 5% high | 8.61 | cm |
| Lab 13-03.c | bond-wire inductance per mm at 5 mm | 1.137 | nH/mm |
| Lab 13-03.d | current for 0.3 T with the gap | 2.542 | A |
| Lab 13-03.e | current for 0.3 T without the gap | 154.9 | mA |
| Lab 13-03.f | ratio of the two | 16.4 | — |
| Lab 13-03.g | area under the bounce pulse | 80 | pV·s |

*These are recomputed by [verify_13_03.py](../../verify/verify_13_03.py) with its own Biot–Savart sum, current-sheet integral and root finding; Lab 13-03.g is checked against ngspice.*

## Discussion questions

1. Why is an inscribed square's centre field higher than the circle's, even though the square's wire is shorter?
2. Why does the ngspice pulse area not depend on how fast the current ramps?
3. Why does the gap's advantage in current fall below the linear factor of 21 near saturation?

### Answers

1. Each side of the square passes closer to the centre than the circle does: at $R\cos 45^\circ$ = 0.71$R$. The Biot–Savart field of a straight segment falls as one over its distance, so the nearer sides more than make up for the shorter total length. In general an $n$-gon gives $n\tan(\pi/n)/\pi$ times the circle's field.
2. The area is $\int L\,(di/dt)\,dt = L\,\Delta I$, the change in flux linkage. A faster ramp gives a taller, narrower pulse of the same area, which is why fast edges are dangerous: the same flux change produces a larger voltage.
3. In the linear model the core's share of the MMF is $\ell_c B/(\mu_r\mu_0)$; near saturation the ferrite's incremental permeability falls and the core needs more $H$ for each extra bit of $B$, so the core's share grows. Without the gap, the core's share is all of the MMF, and it grows by the same factor; with the gap it is a small part. At 0.3 T ($\tanh^{-1}0.75$ = 0.973 against a linear 0.75) the core needs 1.30 times its linear $H$, and the ratio becomes 16.4.

## Optional hardware extension

Wind two air-core coils of the same turns and radius on cardboard tubes, one short and one long, and measure their inductance with an LCR meter at 100 kHz. Compare the ratio with the Nagaoka factors from Part 2. Then wind 20 turns on a gapped ferrite pot core and measure its inductance against a DC bias current (with a bias tee or a meter with a DC-bias function) to see the inductance fall as the core saturates.
