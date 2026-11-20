# Lab 12-08 · Op-Amp Internals

Chapter: [12-08 Op-Amp Internals](../../chapters/12-08-op-amp-internals.md)

## Objective

Go from bias currents to gain, bandwidth and phase margin for a two-stage CMOS op-amp; simulate its large-signal step response and find which stage limits each edge's slew rate; compare a folded cascode at the same power; and see the transconductance seam of a complementary input stage. Confirm the two-stage amplifier's small-signal figures in ngspice.

## Background

The two-stage op-amp (§3.1), slew rate (§3.2), the folded cascode (§3.3) and rail-to-rail input stages (§3.5).

## Files

- [12-08-op-amp-internals.ipynb](12-08-op-amp-internals.ipynb): the notebook (Parts 1–4).
- [two_stage_opamp.cir](two_stage_opamp.cir): ngspice AC analysis of Example 12-08.1's amplifier, measuring DC gain, crossover and phase margin. Run with `ngspice -b two_stage_opamp.cir`, or `python tools/run_spice.py 12-08` from the repository root.

## Procedure

1. **Design to performance (Part 1).** Tabulate gain, GBW, crossover and phase margin for Example 12-08.1's design, then with λ halved, the load doubled (with $C_c$ rescaled by the 0.22 rule, and with it fixed), and a lower input overdrive.
2. **Slew (Part 2, the chapter's guided exercise).** *Predict first:* with $I_7$ doubled, which edge speeds up? Then simulate both edges at both currents.
3. **Folded cascode (Part 3).** Solve Example 12-08.4's amplifier for loads of 1, 2 and 5 pF.
4. **Rail-to-rail seam (Part 4).** Plot $g_m$ against input common mode with and without constant-$g_m$ control.
5. **ngspice.** Run `two_stage_opamp.cir` and compare with Example 12-08.1.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Gain against λ | Halving λ quadruples the two-stage gain; GBW and margin barely change |
| 2 | Slew | Rising 16.2 V/µs (output-limited) and falling 17.7 V/µs; doubling $I_7$ lifts only the rising edge |
| 3 | Folded cascode | Phase margin rises with load capacitance; gain does not change |
| 4 | $g_m$ seam | Doubles between 0.9 and 1.6 V without control; flat with it |
| ngspice | Two-stage | Gain 2500, crossover 12.70 MHz, phase margin 59.78° |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-08.a | DC gain with λ = 0.05 V⁻¹ | 1.000 × 10⁴ | — |
| Lab 12-08.b | phase margin with C_L = 10 pF and C_c = 1.1 pF | 47.41 | ° |
| Lab 12-08.c | crossover then | 10.91 | MHz |

*These are recomputed by [verify_12_08.py](../../verify/verify_12_08.py) with its own nodal solver.*

## Discussion questions

1. In Part 1, why does doubling $C_L$ with $C_c$ kept at 1.1 pF cost 12° of margin, while rescaling $C_c$ to 2.2 pF keeps it?
2. In Part 2, why does doubling $I_7$ not bring the rising edge all the way to 18.18 V/µs?
3. In Part 3, why does the folded cascode's margin improve with load capacitance, the opposite of the two-stage op-amp?

### Answers

1. The non-dominant pole $g_{m6}/C_L$ halves while the crossover ($g_{m1}/C_c$) stays, so $p_2$ moves from 2.2 to 1.1 times the crossover. Rescaling $C_c$ halves the crossover too, restoring the ratio (at the cost of half the GBW).
2. While slewing, node 1 still moves and $R_1$ and $R_2$ divert part of the current, so the measured slope stays a few percent below the ideal $I_{SS}/C_c$.
3. Its load sets the dominant pole: a larger $C_L$ lowers the crossover $g_{m1}/C_L$ while the non-dominant pole at the folding node stays put, increasing their separation.

## Optional hardware extension

Drive a general-purpose op-amp as a unity-gain buffer with a 2 V square wave and measure the rising and falling slew rates on an oscilloscope; compare them with the data sheet. Then shrink the step to 50 mV and observe the small-signal response, whose rise time follows the bandwidth instead of the slew rate.
