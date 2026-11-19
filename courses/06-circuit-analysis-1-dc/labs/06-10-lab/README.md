# Lab 06-10 · The Ideal Op-Amp

**Chapter:** [06-10](../../chapters/06-10-ideal-op-amp.md) · **Notebook:** [06-10-opamps.ipynb](06-10-opamps.ipynb) · **Time:** about 60 minutes (plus 60 minutes for the optional hardware part)

## Objective

1. Measure how close real (finite-gain) op-amp circuits come to their ideal gains, and confirm that the noise gain over $A$ sets the error.
2. See the virtual short fail when the output saturates, and find the voltage the − input moves to.
3. Compare the statistical CMRR of a difference amplifier built from ±1% resistors with its worst case.
4. Build a DC error budget with the bias currents' physical signs and compare it with the sum of magnitudes.

## Background

Chapter sections 3.1 to 3.7 and Examples 06-10.1 to 06-10.5. You need Python with NumPy, SciPy and Matplotlib, and ngspice for the simulator check in Part 1 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips that cell.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-10-opamps.ipynb](06-10-opamps.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [opamps.cir](opamps.cir) | Examples 06-10.1 to 06-10.5 and Problems 06-10.1, 06-10.3, 06-10.4, 06-10.9 and 06-10.11, with E-source op-amps (gain $10^8$, or $10^4$ for Problem 06-10.11), a three-op-amp in-amp subcircuit, explicit offset and bias-current sources, and a $\tanh$ output limit | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **Finite gain (Part 1).** *Predict first:* the inverting stage of Example 06-10.1 (gain −4.7) and a gain-of-101 non-inverting stage at $A = 10^3$, $10^5$ and $10^8$. Which one is further from ideal, and why?
2. **Saturation (Part 2).** *Predict first:* the input at which the − input leaves 0 V, and its voltage for a 3 V input.
3. **Monte Carlo CMRR (Part 3).** *Predict first:* the median CMRR of Example 06-10.3's amplifier with independent, uniformly distributed ±1% resistors.
4. **Signed error budget (Part 4).** *Predict first:* whether the LM358's two bias-current terms add or partly cancel.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | finite gain | inverting −4.673 at $A = 10^3$ (0.57% low), 57 ppm low at $10^5$; non-inverting 91.73 instead of 101 at $10^3$ |
| 2 | saturation | linear up to ±2.553 V; at 3 V in, output −12 V and $v_-$ = 0.3684 V |
| 3 | CMRR | median about 82 dB, 1st percentile about 71 dB, every unit above the 67.9 dB worst case |
| 4 | error budget | signed total 934.5 mV against 984.5 mV for the sum of magnitudes |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-10.a | inverting gain at A = 10^3 | −4.673 | — |
| Lab 06-10.b | inverting gain error at A = 10^3 | 0.57 | % |
| Lab 06-10.c | inverting gain error at A = 10^5 | 57 | ppm |
| Lab 06-10.d | gain-of-101 non-inverting gain at A = 10^3 | 91.73 | — |
| Lab 06-10.e | linear input limit | 2.553 | V |
| Lab 06-10.f | inverting-input voltage at 3 V in | 0.3684 | V |
| Lab 06-10.g | median CMRR, ±1% uniform resistors | 82 | dB |
| Lab 06-10.h | 1st-percentile CMRR | 71 | dB |
| Lab 06-10.i | LM358 signed worst-case total | 934.5 | mV |
| Lab 06-10.j | open-loop gain for 0.1% at a gain of 1000 | 1.0e6 | — |
| Lab 06-10.k | worst-case CMRR with 0.1% resistors | 88 | dB |
| Lab 06-10.l | + bias term with R_s = R_1∥R_2 | 25.0 | mV |

## Discussion questions

1. Part 1's non-inverting stage at $A = 10^3$ is 9% low while the inverting stage is only 0.57% low. Both use the same formula. What makes the difference?
2. In Part 2, why does $v_-$ follow a resistive divider once the output saturates, and why is that a useful diagnostic on a bench?
3. Part 3's Monte Carlo is far better than the worst case. When may a designer quote the statistical figure, and when must the worst case be used?
4. In Part 4, the offset voltage still enters as a magnitude. Why is its sign unknown when the bias currents' signs are known?

<details><summary>Answers to the discussion questions</summary>

1. The relative error is about (noise gain)/$A$. The inverting stage has a noise gain of 5.7, so $5.7/1000 \approx 0.57\%$; the gain-of-101 stage has a noise gain of 101, so about $101/1000 \approx 10\%$ (9.2% exactly, from $1/(1 + 101/1000)$). Feedback can only correct errors by the loop gain $A/(\text{noise gain})$, and a high-gain stage has little of it left.
2. A saturated output is a fixed voltage, so the op-amp no longer adjusts anything: the − input is just a node between two resistors connecting the input and a constant output. On a bench, a measurable voltage between the two inputs of a feedback circuit is the quickest sign that the output has hit a rail (or the loop is broken).
3. A statistical figure is fine when occasional out-of-spec units can be tested and rejected (or a yield loss is acceptable), or when the specification is itself statistical. A guaranteed specification, a safety function or a part that cannot be tested in production must use the worst case, or a matched network that tightens it.
4. The offset comes from random mismatch between the two halves of the input stage (transistor sizes, thresholds, currents), so it is positive in some units and negative in others. The bias currents' direction is set by the input transistors' type: base current flows out of a PNP stage's inputs in every unit.

</details>

## Optional hardware version

Build Example 06-10.1's inverting amplifier with a general-purpose op-amp on ±12 V supplies (or ±5 V, scaling the limits), measured 10 kΩ and 47 kΩ resistors and a bench supply or potentiometer as the input. Record the output from −4 V to +4 V in 0.5 V steps, and measure $v_-$ with a DMM at each step. Find where $v_-$ leaves 0 V and compare it with the supply voltage divided by 4.7 (real outputs saturate a volt or two inside the rails). Then ground the input and measure the output offset; divide it by the noise gain, 5.7, to estimate the op-amp's $V_{OS}$ and compare with the datasheet.
