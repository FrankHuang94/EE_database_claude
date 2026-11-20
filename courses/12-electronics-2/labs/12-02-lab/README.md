# Lab 12-02 · Active Loads, Cascodes and Multistage Amplifiers

Chapter: [12-02 Active Loads, Cascodes and Multistage Amplifiers](../../chapters/12-02-active-loads-cascodes-multistage.md)

## Objective

Compare load options by solving their small-signal circuits; solve the five-transistor OTA's large-signal transfer and see how a 1% current mismatch moves its output; measure how its common-mode rejection depends on the tail; and refer a second stage's offset to the input of a two-stage amplifier. Confirm the OTA and cascode results in ngspice.

## Background

Resistor and active loads (§3.1–3.2), the five-transistor OTA (§3.3), cascodes (§3.4), the telescopic cascode (§3.5) and multistage amplifiers (§3.6).

## Files

- [12-02-active-loads-cascodes.ipynb](12-02-active-loads-cascodes.ipynb): the notebook (Parts 1–4).
- [ota_cascode.cir](ota_cascode.cir): ngspice small-signal models of the OTA (differential and common-mode drive) and of the cascode (output resistance, open-circuit gain, cascode and simple loads), plus a level-1 OTA whose matched output must settle at the diode node's voltage. Run with `ngspice -b ota_cascode.cir`, or `python tools/run_spice.py 12-02` from the repository root.

## Procedure

1. **Load options (Part 1).** Solve a common-source stage with a resistor load, a current-source load, a cascode with a simple load and a cascode with a cascode load, and tabulate gain against the headroom each needs.
2. **The OTA's transfer (Part 2, the chapter's guided exercise).** *Predict first:* how far does the open-loop output move if M4 carries 1% more current than M3 copies? Then solve the OTA's large-signal transfer over ±20 mV and the mismatched case.
3. **Gains against tail resistance (Part 3).** Sweep $R_{SS}$ from 10 kΩ to 5 MΩ and compare the full circuit's $A_d$, $A_{cm}$ and CMRR with the hand estimates.
4. **Two stages (Part 4).** Combine the OTA with a common-source second stage, find the total gain, and refer a 10 mV second-stage offset to the input.
5. **ngspice.** Run `ota_cascode.cir` and compare with Examples 12-02.2 and 12-02.3.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Gains | 8.26, 50.00, 98.06 and 5050 for 1.1, 0.4, 0.6 and 0.8 V of headroom |
| 2 | Transfer and mismatch | The high-gain region spans tens of millivolts; a 1% mismatch moves the output by about 50 mV |
| 3 | Against $R_{SS}$ | $A_d$ nearly constant; $A_{cm}$ ∝ $1/R_{SS}$; CMRR up 20 dB per decade |
| 4 | Two stages | Gain about 2500; the offset divided by the first stage's gain |
| ngspice | Small-signal values | As in Examples 12-02.2 and 12-02.3; the large-signal output equal to the diode node |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-02.a | OTA CMRR with a 500 kΩ tail | 94.1 | dB |
| Lab 12-02.b | OTA common-mode gain with a 500 kΩ tail | 0.000979 | — |
| Lab 12-02.c | 10 mV second-stage offset at the input, full circuit | 0.2010 | mV |
| Lab 12-02.d | OTA CMRR with a 10 kΩ tail | 60.6 | dB |

*These are recomputed by [verify_12_02.py](../../verify/verify_12_02.py) from its own nodal analysis of the full OTA.*

## Discussion questions

1. Part 2's large-signal slope at balance is a little above the hand gain of 50. Why?
2. In Part 3, why does the differential gain not depend on the tail resistance?
3. Why is the OTA's output level in Part 2 equal to the diode node's voltage only when the halves match?

### Answers

1. The large-signal model's output resistance includes the $(1 + \lambda v_{DS})$ factor of the square law with channel-length modulation, so each $r_o$ is a few percent above $1/(\lambda I_D)$, and the gain rises with it.
2. The gain is $G_mR_{out}$: $G_m$ is found with the output held still, when the two halves are nearly symmetric and the tail barely moves, and $R_{out} \approx r_{o2} \parallel r_{o4}$ is set by the mirror action. Neither depends on $R_{SS}$ once $R_{SS} \gg 1/g_m$: the full circuit gives 49.74 with a 10 kΩ tail and 49.75 with an ideal one, even though, with the output open, the tail node moves by about a quarter of $v_{id}$ (the circuit is not symmetric, so the tail is not a virtual ground).
3. Matching makes the two branches mirror images: when the output equals the diode node, every transistor on the output side has the same voltages as its partner. With mismatch the branches differ, and the output must move until the current difference is absorbed across the large output resistance.

## Optional hardware extension

Build the five-transistor OTA from a CMOS transistor array (such as a CD4007, which has three NMOS and three PMOS devices) with a resistor tail, on a 5 V supply. Close a unity-gain feedback loop (output to the inverting input), then open it and watch how far the output wanders for small input changes: the open-loop gain is high enough that the output sticks to one rail unless the input difference is set to within millivolts.
