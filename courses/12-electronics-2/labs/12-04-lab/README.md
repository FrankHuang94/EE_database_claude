# Lab 12-04 · High-Frequency Analysis Methods

Chapter: [12-04 High-Frequency Analysis Methods](../../chapters/12-04-high-frequency-analysis-methods.md)

## Objective

Compute open-circuit time constants by test sources and confirm that they sum to the full circuit's $b_1$; compare short-circuit time-constant estimates with exact low corners; watch two poles split as a compensation capacitor grows; and map where a source follower peaks. Confirm the split poles in ngspice.

## Background

Open-circuit time constants (§3.1), zero-value time constants (§3.2), short-circuit time constants (§3.3), pole splitting (§3.4) and the follower driven from a resistance (§3.5).

## Files

- [12-04-time-constants.ipynb](12-04-time-constants.ipynb): the notebook (Parts 1–4).
- [pole_split.cir](pole_split.cir): ngspice pole–zero analysis of Example 12-04.4's two-stage amplifier without and with the compensation capacitor. Run with `ngspice -b pole_split.cir`, or `python tools/run_spice.py 12-04` from the repository root.

## Procedure

1. **OCTC (Part 1).** Find the resistance each capacitor of Example 12-04.1's stage sees with a test current, form the time constants and their shares, and compare their sum with $b_1$ computed from the full circuit's poles.
2. **SCTC (Part 2).** For Example 12-04.3's amplifier, sweep the bypass capacitor over 1, 10 and 100 µF and compare the estimate with the exact low corner.
3. **Pole splitting (Part 3, the chapter's guided exercise).** *Predict first:* as $C_c$ grows from 0 to 1 pF, do the poles move steadily apart? Then plot both poles against $C_c$.
4. **Follower peaking (Part 4).** Tabulate the follower's peak for source resistances from 1 kΩ to 100 kΩ and loads from 0.1 pF to 10 pF.
5. **ngspice.** Run `pole_split.cir` and compare with Example 12-04.4.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | OCTC against $b_1$ | Equal to rounding; the load capacitor contributes about half |
| 2 | SCTC against exact | The estimate is always above the exact corner, by more when no capacitor dominates |
| 3 | Poles against $C_c$ | Monotonic, fastest at small $C_c$ |
| 4 | Follower | No peak from 1 kΩ; peaks of a few decibels from tens of kilohms |
| ngspice | Poles | 12.73 and 63.66 MHz uncompensated; 61.75 kHz and 596.6 MHz with 1 pF |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-04.a | SCTC estimate with a 100 µF bypass | 19.36 | Hz |
| Lab 12-04.b | exact low corner with a 100 µF bypass | 14.03 | Hz |
| Lab 12-04.c | follower peak, 100 kΩ and 1 pF | 4.92 | dB |
| Lab 12-04.d | follower peak, 10 kΩ and 0.1 pF | 2.81 | dB |

*These are recomputed by [verify_12_04.py](../../verify/verify_12_04.py) with its own solver.*

## Discussion questions

1. In Part 2, why does the SCTC estimate get worse as the bypass capacitor grows?
2. In Part 4, why does a 0.1 pF load peak *more* than a 1 pF load at 10 kΩ, but less at 100 kΩ?
3. What would you add to Part 1's stage to make $C_{gs}$ the largest contributor?

### Answers

1. As $C_S$ grows its corner falls toward the other two, so no capacitor dominates; the sum of the three corners then overestimates the true corner more.
2. $Q = \sqrt{g_mR_S\Sigma}/(C_{gs} + C_L + g_mR_SC_{gd})$ depends on both: a small $C_L$ shrinks the denominator, raising $Q$ at moderate $R_S$, but at very large $R_S$ the $g_mR_SC_{gd}$ term dominates the denominator and a larger $\Sigma$ (larger $C_L$) wins.
3. A larger source resistance: $\tau_{gs} = R_SC_{gs}$ grows in proportion, while the load's $R_LC_L$ does not change (the Miller term grows too).

## Optional hardware extension

Build a two-stage discrete amplifier (two common-emitter stages) and add a small capacitor (10–100 pF) from the second stage's collector to its base. Measure the open-loop frequency response with and without it: the low pole moves down by roughly the Miller factor while the response at high frequency becomes a single, clean roll-off.
