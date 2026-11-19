# Lab 10-02 · MOSFET DC Operation and Biasing

Chapter: [10-02 MOSFET DC Operation and Biasing](../../chapters/10-02-mosfet-dc-operation-and-biasing.md)

## Objective

Find MOSFET operating points the way a simulator does, and measure how much each bias scheme suppresses the spread of threshold voltage that manufacturing and temperature impose.

## Background

The chapter's square-law model (§3.1), its region checks (§3.2), the sensitivity of a fixed-$V_{GS}$ bias to the threshold (§3.3), source degeneration and current-source bias (§3.4–3.5), the switch's on-resistance (§3.6) and the body effect (§3.7).

## Files

- [10-02-mosfet-bias.ipynb](10-02-mosfet-bias.ipynb): the notebook (Parts 1–4).
- [mosfet_bias.cir](mosfet_bias.cir): ngspice operating points of Examples 10-02.2 and 10-02.3 with the level-1 (square-law) MOSFET.

## Procedure

1. **Regions and load lines (Part 1).** *Predict first:* as $R_D$ grows from 1 kΩ to 20 kΩ in Example 10-02.1, at what value does the transistor leave saturation, and how much does $I_D$ change on the way? Then sweep it.
2. **Bias Monte Carlo (Part 2, the chapter's guided exercise).** *Predict first:* the spread of $I_D$ for σ = 25 mV of threshold variation, for each bias scheme. Then sample 10,000 thresholds (2,000 for the schemes that need a root solve per sample).
3. **Switch resistance (Part 3).** Plot $R_{on}$ against gate drive for the integrated switch of Example 10-02.6, and compare the deep-triode formula with the exact slope at a 0.1 V drop.
4. **Body effect (Part 4).** Iterate Example 10-02.7 and compare with a two-variable root finder.
5. **ngspice.** Run `python tools/run_spice.py 10-02`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Edge of saturation | at $R_D$ = 11.2 kΩ; the current changes by only a few percent across the sweep |
| 2 | Current spread | fixed bias several times worse than degenerated, which is worse than the current reference |
| 3 | $R_{on}$ | falls as $1/V_{ov}$ |
| 4 | Iteration | converges in three or four passes |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-02.a | σ of I_D, fixed V_GS | 7.56 | % |
| Lab 10-02.b | σ of I_D, divider with R_S | 2.13 | % |
| Lab 10-02.c | σ of I_D, current reference | 0.95 | % |
| Lab 10-02.d | improvement from degeneration | 3.55 | — |
| Lab 10-02.e | resistance excess at 0.1 V drop | 4.0 | % |
| Lab 10-02.f | g_m R of the reference | 14.0 | — |

## Discussion questions

1. The simulated spreads (7.56% and 2.13%) are close to the chapter's first-order predictions (7.7% and 2.1%). Why is the fixed-bias spread slightly smaller than predicted?
2. Why does the current reference beat source degeneration here, and what does it cost?
3. In Part 3, why does the deep-triode formula underestimate the resistance at larger drops?

### Answers

1. The first-order formula uses the slope at the nominal point. The square law curves upward: a threshold that falls by 25 mV raises the current by more than one that rises by 25 mV lowers it. The standard deviation weighs both directions, and the sample's spread comes out a little under the linear estimate, **7.56**% against 7.7%, while the mean shifts slightly upward.
2. In the reference, 2.45 V sits across a 10 kΩ resistor, so a threshold shift of 25 mV changes the current by only about 1%: an effective degeneration of $g_mR$ = **14.0** rather than 2.6. It costs a second transistor and a resistor, and the mirror that copies the current adds its own errors (channel-length modulation, mismatch between the two transistors; 10-08).
3. The formula keeps only the linear term. At a drop $V_{DS}$, the triode current is $k_n(V_{ov}V_{DS} - V_{DS}^2/2)$, so the actual resistance is $1/[k_n(V_{ov} - V_{DS}/2)]$, larger by the factor $V_{ov}/(V_{ov} - V_{DS}/2)$: about **4.0**% at 0.1 V with 1.3 V of overdrive.

## Optional hardware extension

With a BSS138 (or any small logic-level MOSFET), a 10 kΩ potentiometer as a gate divider and a 1 kΩ drain resistor from 5 V, measure $I_D$ against $V_{GS}$, extract $V_{TN}$ and $k_n$ from a plot of $\sqrt{I_D}$ against $V_{GS}$, then add a source resistor and observe how much less the current drifts as you warm the part with your fingers.
