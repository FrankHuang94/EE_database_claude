# Lab 12-03 · Frequency Response: Device Capacitances, Miller Effect, Poles and Zeros

Chapter: [12-03 Frequency Response](../../chapters/12-03-frequency-response-miller-poles-zeros.md)

## Objective

Measure a MOSFET's short-circuit current gain and read off $f_T$; compare the common-source stage's exact bandwidth with the Miller and dominant-pole estimates as the source resistance changes; compare common-source, common-gate and cascode stages built from one device; and see a source follower peak when driven from a high resistance. Confirm the common-source stage's bandwidth, poles and zero in ngspice.

## Background

Device capacitances and $f_T$ (§3.1), poles and the dominant-pole approximation (§3.2), the Miller theorem (§3.3), the common-source stage (§3.4), the common-gate stage (§3.5), the source follower (§3.6) and the cascode (§3.7).

## Files

- [12-03-frequency-response.ipynb](12-03-frequency-response.ipynb): the notebook (Parts 1–4).
- [cs_freq.cir](cs_freq.cir): ngspice AC sweep and pole–zero analysis of Example 12-03.2's stage. Run with `ngspice -b cs_freq.cir`, or `python tools/run_spice.py 12-03` from the repository root.

## Procedure

1. **$f_T$ (Part 1).** Drive the gate with a current, short the drain, and find where the current gain falls to 1.
2. **Estimates against exact (Part 2, the chapter's guided exercise).** *Predict first:* if $R_S$ falls from 10 kΩ to 1 kΩ, does the bandwidth rise tenfold? Then tabulate the exact −3 dB frequency, the Miller input-pole estimate and $1/(2\pi b_1)$ for $R_S$ from 100 Ω to 100 kΩ.
3. **Three stages (Part 3).** Compare the gain, bandwidth and gain–bandwidth product of common-source, common-gate and cascode stages with a 10 kΩ source.
4. **Follower peaking (Part 4).** Drive a source follower with a 1 pF load from 100 Ω to 30 kΩ and find the peak of its response.
5. **ngspice.** Run `cs_freq.cir` and compare with Example 12-03.2.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $f_T$ | 2.02 GHz, matching $g_m/[2\pi(C_{gs} + C_{gd})]$ |
| 2 | Estimates | Miller-only far too high at low $R_S$; both estimates converge at high $R_S$ |
| 3 | Stages | The cascode has the common-source gain with most of the common-gate bandwidth |
| 4 | Follower | Flat at low $R_S$; a peak of a few decibels at 30 kΩ |
| ngspice | Bandwidth, poles, zero | 42.93 MHz; 43.58 and 350.0 MHz; 26.53 GHz |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 12-03.a | CS −3 dB with a 100 kΩ source | 7.50 | MHz |
| Lab 12-03.b | CG gain–bandwidth product, 10 kΩ source | 136.4 | MHz |
| Lab 12-03.c | follower peak, 30 kΩ source, 1 pF load | 2.59 | dB |
| Lab 12-03.d | frequency of that peak | 84.6 | MHz |

*These are recomputed by [verify_12_03.py](../../verify/verify_12_03.py) with its own nodal solver; the peak by bounded optimization of $\lvert H\rvert$.*

## Discussion questions

1. Why does the Miller-only estimate become accurate at high source resistance?
2. The cascode's gain–bandwidth product exceeds the common-source stage's. Where did the extra come from?
3. Why does a follower peak when driven from a high resistance?

### Answers

1. As $R_S$ grows, the input time constant $R_SC_{in}$ dwarfs the output's $R_L(C_L + C_{gd})$, so the input node alone sets the bandwidth, which is what the Miller estimate assumes.
2. From the input node: the cascode cuts the gate's capacitance from 198.7 fF to 84.67 fF by holding M1's drain nearly still, so the input pole moves from 80 MHz to 188 MHz and the output node becomes the limit.
3. The follower's output impedance, seen from the load, rises with frequency when the gate is driven from a resistance (it looks inductive), and an inductive source driving a capacitive load forms a resonant pair; 12-04 derives the condition.

## Optional hardware extension

Build a common-emitter stage with a 2N3904 at about 1 mA and a 5 kΩ collector load, driven from a 10 kΩ source resistor. Measure its bandwidth with a function generator and oscilloscope, then add a 10 pF capacitor from collector to base and measure again: the bandwidth falls by roughly the Miller factor.
