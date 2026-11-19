# Lab 10-06 · MOS Single-Stage Amplifiers

Chapter: [10-06 MOS Single-Stage Amplifiers](../../chapters/10-06-mos-single-stage-amplifiers.md)

## Objective

Build each MOS configuration as a small-signal matrix, sweep its components to see the limits of Figure 2, measure how degeneration trades gain for linearity, check the gain–headroom identity, and watch the common-gate input resistance move with its load. Then confirm the chapter's examples with level-1 transistors in ngspice.

## Background

The configurations and their formulas (§3.2–3.6), the degeneration distortion result (Problem 10-06.9) and the square-law large-signal model of 10-02.

## Files

- [10-06-mos-stages.ipynb](10-06-mos-stages.ipynb): the notebook (Parts 1–4).
- [mos_stages.cir](mos_stages.cir): ngspice AC analyses of the stages of Examples 10-06.1 to 10-06.4. The netlist's header explains how level-1 parameters are chosen to reproduce the chapter's $g_m$, $r_o$ and χ exactly.

## Procedure

1. **Limits (Part 1).** *Predict first:* the CS gain magnitude when $R_D = r_o$, and the follower gain with $R_S$ = 2 kΩ (with body effect and $r_o$). Then sweep $R_D$ and $R_S$ and reproduce Figure 2.
2. **Degeneration and distortion (Part 2, the chapter's guided exercise).** *Predict first:* $\text{HD}_2$ of Example 10-06.1's stage at 50 mV, with and without $R_S$ = 500 Ω. Then solve the large-signal square law over a cycle for amplitudes from 10 to 200 mV and plot $\text{HD}_2$ and $\text{HD}_3$.
3. **Gain and headroom (Part 3).** Hold $V_{RD}$ = 2.5 V and vary $V_{ov}$; then hold $V_{ov}$ and vary the current (scaling $R_D$ to keep $V_{RD}$). Plot the gains.
4. **Common-gate input resistance (Part 4).** Sweep the drain load from 0 to 1 MΩ and find where the input resistance reaches 1 kΩ.
5. **ngspice.** Run `python tools/run_spice.py 10-06`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | CS at $R_D = r_o$ | half the intrinsic gain |
| 2 | Distortion | $\text{HD}_2$ falls about fourfold at the same input with $g_mR_S$ = 1; degeneration creates a small $\text{HD}_3$ the bare square law does not have |
| 3 | Gain | depends on $V_{ov}$ at fixed $V_{RD}$, not on current |
| 4 | CG input | rises linearly with the drain load |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-06.a | CS gain with R_D = r_o | -40 | — |
| Lab 10-06.b | follower gain with R_S = 2 kΩ | 0.6838 | — |
| Lab 10-06.c | HD2 at 100 mV, no degeneration | 5.0 | % |
| Lab 10-06.d | HD3 at 100 mV with R_S = 500 Ω | 0.0315 | % |
| Lab 10-06.e | gain magnitude at V_ov = 0.2 V, V_RD = 2.5 V | 25 | — |
| Lab 10-06.f | drain load for a 1 kΩ CG input | 57 | kΩ |

## Discussion questions

1. Why does degeneration create a third harmonic when the bare square law has none?
2. In Part 3, why is the gain independent of current at fixed $V_{RD}$ and $V_{ov}$, and what physical resource does a higher current buy instead?
3. The netlist's transistors need a different `LAMBDA` and `KP` in each stage to match the chapter's $r_o$ = 40 kΩ. What does that say about quoting "λ" as a device constant?

### Answers

1. With degeneration, $v_{gs}$ depends on the output current, which already contains a second harmonic; squaring a signal that contains $\omega$ and $2\omega$ produces $3\omega$. Feedback around a quadratic device generates all higher harmonics, though they fall rapidly.
2. $g_m = 2I_D/V_{ov}$ and $R_D = V_{RD}/I_D$, so their product $2V_{RD}/V_{ov}$ has no current in it. A higher current buys speed (it charges capacitances faster, Course 12) and lower noise, not gain.
3. Level 1's output resistance $(1 + \lambda V_{DS})/(\lambda I_D)$ depends on $V_{DS}$ as well as $I_D$, and real devices depart from either form. "λ" is a fitting parameter for one operating region; designers read $r_o$ (or $g_{ds}$) from simulation at the actual bias.

## Optional hardware extension

Build Example 10-06.1 with a small-signal MOSFET such as the BSS138 (10-02), biasing with a gate divider and a source resistor bypassed by a capacitor. Measure the gain with and without the bypass capacitor, and drive a 1 kΩ load directly and through a second BSS138 as a source follower.
