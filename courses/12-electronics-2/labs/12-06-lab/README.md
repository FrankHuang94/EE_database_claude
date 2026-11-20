# Lab 12-06 · Stability and Frequency Compensation

Chapter: [12-06 Stability and Frequency Compensation](../../chapters/12-06-stability-and-compensation.md)

## Objective

Read phase and gain margins from loop gains and watch a loop go from ringing to oscillation; measure how step overshoot follows phase margin; sweep the Miller capacitor of a two-stage amplifier and compare exact margins with the design estimates; and see what a nulling resistor does. Confirm the two-stage amplifier's margins in ngspice.

## Background

Stability and the margins (§3.1–3.2), phase margin and the closed-loop response (§3.3), Miller compensation (§3.5) and the nulling resistor (§3.6).

## Files

- [12-06-stability.ipynb](12-06-stability.ipynb): the notebook (Parts 1–4).
- [two_stage.cir](two_stage.cir): ngspice AC analysis of Example 12-06.5's amplifier without and with the cancelling nulling resistor, measuring crossover and phase margin. Run with `ngspice -b two_stage.cir`, or `python tools/run_spice.py 12-06` from the repository root.

## Procedure

1. **Three poles (Part 1).** For Example 12-06.3's amplifier, tabulate the margins at β = 0.001, 0.005, 0.0122, 0.02 and 1, and plot the closed-loop step responses of the stable cases.
2. **Overshoot (Part 2).** Simulate two-pole loops with the second pole at 1, 1.5, 2 and 3 times $f_u$ and measure the overshoot.
3. **Miller sweep (Part 3, the chapter's guided exercise).** *Predict first:* what does halving $C_c$ do to the crossover and the phase margin? Then sweep $C_c$ from 0.3 to 3 pF.
4. **Nulling resistor (Part 4).** Sweep $R_z$ from 0 to 1 kΩ and plot the phase margin.
5. **ngspice.** Run `two_stage.cir` and compare with Examples 12-06.5 and 12-06.6.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Margins against β | Both margins shrink as β grows; both pass zero near β = 0.0122 |
| 2 | Overshoot | 16.30%, 8.77%, 4.32% and 0.43%, as in Table 1 |
| 3 | Phase margin against $C_c$ | Rises with $C_c$; the estimate is conservative at small $C_c$ |
| 4 | Phase margin against $R_z$ | Rises steadily through 100 Ω (zero removed) and 554.5 Ω (zero on $p_2$) |
| ngspice | Margins | 129.5 MHz and 58.56° without $R_z$; 143.3 MHz and 84.37° with it |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-06.a | gain margin at β = 0.005 | 7.76 | dB |
| Lab 12-06.b | phase margin at β = 0.005 | 16.32 | ° |
| Lab 12-06.c | phase margin with R_z = 1 kΩ | 98.75 | ° |
| Lab 12-06.d | crossover with R_z = 1 kΩ | 202.4 | MHz |

*These are recomputed by [verify_12_06.py](../../verify/verify_12_06.py) with its own nodal solver.*

## Discussion questions

1. In Part 1, a gain margin of 7.76 dB at β = 0.005 sounds comfortable, yet the step response rings badly. Why?
2. In Part 3, why does the exact crossover fall further below $g_{m1}/(2\pi C_c)$ as $C_c$ shrinks?
3. In Part 4, the phase margin passes 90° above about 700 Ω. Is that desirable?

### Answers

1. The phase margin is only 16.32°: the two margins measure different things, and a loop can have plenty of gain margin while its phase at crossover is close to −180°, which is what sets the ringing.
2. A smaller $C_c$ raises $\omega_u$ toward $p_2$ (and lowers $p_2$ through the improved estimate); near $p_2$ the magnitude falls faster than $1/\omega$, so it reaches unity before $\omega_u$.
3. Not by itself. The margin rises because a left-half-plane zero now sits below the old $p_2$, adding lead; but the crossover climbs toward the new pole near $1/(R_zC_1)$, and an imperfectly cancelled pole–zero pair leaves a slow settling component. Designers stop near the cancelling value.

## Optional hardware extension

Build a unity-gain buffer from a general-purpose op-amp and drive capacitive loads from 100 pF to 10 nF through a short lead. Apply a small square wave and photograph the overshoot at each load; convert the overshoot into an estimated phase margin with Problem 12-06.12's method, and add a 50–100 Ω isolation resistor to see the margin recover.
