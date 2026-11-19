# Lab 06-08 · Thévenin and Norton Equivalents

**Chapter:** [06-08](../../chapters/06-08-thevenin-and-norton.md) · **Notebook:** [06-08-thevenin.ipynb](06-08-thevenin.ipynb) · **Time:** about 75 minutes (plus 45 minutes for the optional hardware part)

## Objective

1. Find Thévenin equivalents in ngspice by open circuit, short circuit and test source, and see which method fails with a dependent source.
2. Confirm that an equivalent reproduces the terminal behavior exactly but not the internal power.
3. Find the operating points of a constant-power load on a Thévenin source and the power limit beyond which none exists.
4. Choose load values that make a two-load measurement reliable in the presence of noise.

## Background

Chapter sections 3.1 to 3.5 and Examples 06-08.1 to 06-08.5. You need Python with NumPy and Matplotlib, and ngspice for Part 1 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips the simulator cell.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-08-thevenin.ipynb](06-08-thevenin.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [thevenin.cir](thevenin.cir) | Open-circuit voltages, short-circuit currents and test-source resistances for Examples 06-08.1 to 06-08.4 and Problems 06-08.2, 06-08.4, 06-08.5 and 06-08.10 | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **Three methods (Part 1).** *Predict first:* which method fails for Example 06-08.3? Then compare $v_{oc}/i_{sc}$ with the test-source resistance.
2. **Terminals versus inside (Part 2).** *Predict first:* will the internal power of the original circuit, its Thévenin and its Norton equivalent agree? Sweep the load from 10 Ω to 1 MΩ.
3. **Constant-power load (Part 3).** *Predict first:* above what power does a 52 V, 6.25 Ω port have no operating point? Plot both solutions against power.
4. **Two loads with noise (Part 4).** *Predict first:* which second load gives the most reliable estimate of a 200 MΩ source resistance, with 0.1% reading noise?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 06-08.1 | $v_{oc}$ = 4 V, $i_{sc}$ = 1.333 mA, $R_{th}$ = 3 kΩ by all three methods; Example 06-08.3: series–parallel reduction impossible, test source gives 909.1 Ω |
| 2 | at a 1 kΩ load | identical 1 V across the load; internal power 19 mW (original), 3 mW (Thévenin), 0.333 mW (Norton) |
| 3 | PoE port | maximum 108.2 W at 26 V; at 100 W the device would sit at 33.14 V |
| 4 | second load | most reliable at the largest loads, about 10 GΩ (relative spread near 0.14%); loads near the first one are useless |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-08.a | internal power of the original circuit at 1 kΩ | 19 | mW |
| Lab 06-08.b | internal power of the Thévenin equivalent at 1 kΩ | 3 | mW |
| Lab 06-08.c | internal power of the Norton equivalent at 1 kΩ | 0.3333 | mW |
| Lab 06-08.d | device voltage at 100 W | 33.14 | V |
| Lab 06-08.e | R_th with a 99 kΩ feedback resistor | 1.786 | kΩ |
| Lab 06-08.f | maximum power on a 3.125 Ω cable | 216.3 | W |

## Discussion questions

1. Why can a Thévenin equivalent be found for Example 06-08.3 at all, when it contains a dependent source?
2. The original circuit of Part 2 wastes 19 mW to deliver 1 mW. Which equivalent is "closer" to it, and does the question make sense?
3. In Part 3, why is the lower-voltage solution never seen in practice?
4. Why does a second load near the first one give such a poor estimate in Part 4?

<details><summary>Answers to the discussion questions</summary>

1. The theorem needs only linearity, and a linear dependent source keeps the network linear. What fails is the shortcut of combining resistors; the test source (or $v_{oc}/i_{sc}$) still works.
2. Neither: both equivalents agree with the original only at the terminals. The original's internal dissipation depends on its own structure (here the 6 kΩ–3 kΩ divider wasting current), which the two-number description discards. Asking which equivalent is closer inside is like asking which of two summaries of a balance sheet better describes the company's payroll.
3. A converter that regulates its output draws more current when its input voltage drops, on both branches. What decides stability is the comparison of slopes: after a dip δ the source supplies $\delta/R_{th}$ more current and the load demands $P\delta/v^2$ more, so a point is stable only if $v^2/P > R_{th}$. On the upper branch the source wins and the voltage recovers; on the lower branch the load's extra demand exceeds the source's extra supply, the voltage falls further, and in practice the input collapses or the converter's undervoltage lockout shuts it off.
4. With nearly equal loads, the two readings are nearly equal, so the line through the two points in the $1/v$ against $1/R_L$ plot is determined by a tiny difference between two noisy numbers: its slope (which gives $R_{th}$) is dominated by the noise. Widely spaced loads make the difference large compared with the noise.

</details>

## Optional hardware version

Measure the Thévenin equivalent of a 9 V battery and of a USB port with a multimeter and two power resistors (for example 100 Ω and 22 Ω for the battery, rated at least 1 W, connected only for a few seconds). Use the two-load method to find $V_{th}$ and $R_{th}$, then predict the voltage with a third resistor and check it. Repeat the battery measurement after a minute of load to see how its "equivalent" drifts as it discharges and warms.
