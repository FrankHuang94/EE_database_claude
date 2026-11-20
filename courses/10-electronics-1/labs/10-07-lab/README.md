# Lab 10-07 · BJT Single-Stage Amplifiers

Chapter: [10-07 BJT Single-Stage Amplifiers](../../chapters/10-07-bjt-single-stage-amplifiers.md)

## Objective

See which properties of bipolar stages move with β and which do not, measure the ceiling on degenerated output resistance, find where an emitter follower clips into a load, and compare bipolar and MOS transconductance across bias current. Then confirm the chapter's examples with Gummel–Poon transistors in ngspice.

## Background

The CE, CB and CC results (§3.1–3.4), the output-resistance derivation of §3.2, swing with a coupled load (10-05 §3.6) and the MOS–BJT comparison (§3.5).

## Files

- [10-07-bjt-stages.ipynb](10-07-bjt-stages.ipynb): the notebook (Parts 1–4).
- [bjt_stages.cir](bjt_stages.cir): ngspice AC analyses of Examples 10-07.1, 10-07.2, 10-07.4 and 10-07.5.
- [ceiling_bypass.cir](ceiling_bypass.cir): ngspice β ceiling on the collector output resistance (Example 10-07.3) and the bypass-capacitor corner (Example 10-07.8).

## Procedure

1. **β sweep (Part 1, the chapter's guided exercise).** *Predict first:* in Example 10-07.1's bypassed amplifier, does the overall gain from the 1 kΩ source rise or fall when β goes from 100 to 300 at fixed bias current? Then sweep β from 50 to 400 for the bypassed and the degenerated (Example 10-07.7) stages and plot input resistance, stage gain and overall gain.
2. **The output-resistance ceiling (Part 2).** Compute the collector output resistance by test-source simulation against $R_E$ and find where it reaches 90% of its ceiling.
3. **Follower clipping (Part 3).** Drive Example 10-07.5's follower with a growing sine at the base and find the amplitude at which the transistor cuts off on the negative half-cycle.
4. **MOS against BJT across current (Part 4).** For a MOSFET of fixed size ($k_n$ = 25 mA/V², $n$ = 1.3) described by the EKV interpolation, plot the BJT/MOS $g_m$ ratio from 1 µA to 10 mA.
5. **ngspice.** Run `python tools/run_spice.py 10-07`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | β sweep | stage gain flat for the degenerated stage; input resistance and overall gain track β |
| 2 | Ceiling | reached only at $R_E$ of tens of kilohms, many times $r_\pi$ |
| 3 | Clipping | the negative output peak is limited to $I_E(R_E \parallel R_L)$ = 0.842 V, reached (to 99%) at a base amplitude of 0.952 V; the positive side does not clip |
| 4 | Ratio | about 1.6 at 10 µA, approaching $n$ = 1.3 deeper in weak inversion; about 4.6 at 0.5 mA; about 20 at 10 mA, deep in strong inversion |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 10-07.a | r_pi at β = 300 (Example 10-07.1 bias) | 6.029 | kΩ |
| Lab 10-07.b | stage R_in at β = 300 | 3.483 | kΩ |
| Lab 10-07.c | input factor at β = 300 | 0.7769 | — |
| Lab 10-07.d | overall gain change, β 100 to 300 | 25.8 | % |
| Lab 10-07.e | R_E for 90% of the ceiling | 23.01 | kΩ |
| Lab 10-07.f | follower negative swing limit | 0.842 | V |
| Lab 10-07.g | BJT/MOS g_m ratio, square law at V_ov = 0.2 V | 3.868 | — |
| Lab 10-07.h | base amplitude for the negative limit (to 99%) | 0.952 | V |
| Lab 10-07.i | BJT/MOS ratio at 10 µA, EKV | 1.64 | — |
| Lab 10-07.j | BJT/MOS ratio at 0.5 mA, EKV | 4.56 | — |
| Lab 10-07.k | BJT/MOS ratio at 10 mA, EKV | 19.7 | — |

## Discussion questions

1. In Part 1, the bypassed stage's overall gain rises with β although its gain from the base does not change. Why, and how would a lower source resistance change the picture?
2. Why does the output resistance need $R_E$ several times $r_\pi$ to approach its ceiling?
3. The follower clips on the negative half-cycle only. What would make it clip on the positive half-cycle instead?

### Answers

1. The gain from the base is $-g_mR_C$, set by the bias current; β enters only through $r_\pi$, which forms the input divider with the source. With a source resistance much smaller than $R_B \parallel r_\pi$, the divider approaches 1 and the gain stops depending on β.
2. The effective degeneration is $R_E \parallel r_\pi$, which approaches $r_\pi$ only when $R_E \gg r_\pi$: at $R_E$ = 9$r_\pi$, $R_E \parallel r_\pi$ is still only 0.9$r_\pi$.
3. Saturation: if the input drives the emitter up until the collector–emitter voltage falls to $V_{CE,sat}$, the positive peak flattens. With the collector at $V_{CC}$ that needs an input near the supply; with a collector resistor, much less.

## Optional hardware extension

Build Example 10-07.1 with a 2N3904 and the 10-03 bias values. Measure the gain with $R_E$ bypassed, then with 100 Ω left unbypassed, and swap in transistors from different batches: the bypassed stage's overall gain moves with the part, the degenerated one barely does.
