# Lab 06-06 · Dependent Sources

**Chapter:** [06-06](../../chapters/06-06-dependent-sources.md) · **Notebook:** [06-06-dependent.ipynb](06-06-dependent.ipynb) · **Time:** about 90 minutes (plus 60 minutes for the optional hardware part)

## Objective

1. Use SPICE's dependent sources (E, G, F and H elements, with 0 V sense sources for current control) and read their results correctly.
2. Add VCCS and VCVS stamps to a small MNA solver and see where symmetry is lost.
3. Explore the Miller effect, bootstrapping and negative resistance by sweeping a VCVS gain.
4. Measure how an op-amp circuit's accuracy depends on its open-loop gain.

## Background

Chapter sections 3.1 to 3.6 and Examples 06-06.1 to 06-06.5. You need Python with NumPy and Matplotlib, and ngspice for Part 1 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips Part 1 and the rest still runs.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-06-dependent.ipynb](06-06-dependent.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [dependent.cir](dependent.cir) | Examples 06-06.1 to 06-06.5 and Problems 06-06.3, 06-06.5, 06-06.7, 06-06.11, 06-06.12 and 06-06.14, with E, G, F and H elements | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **SPICE's dependent sources (Part 1).** *Predict first:* what sign does ngspice report for the base-current sense source in Example 06-06.3? Then run the netlist and compare every value with the hand analysis.
2. **Nonsymmetric matrices (Part 2).** *Predict first:* which entry of Example 06-06.1's nodal matrix has no mirror image? Then print the matrices built with the new stamps.
3. **Gain sweep (Part 3).** *Predict first:* where does $R_{in} = R_f/(1 - \mu)$ change sign? Sweep $\mu$ from −100 to 100 and spot-check against the MNA solver.
4. **Loop gain (Part 4).** *Predict first:* how does the closed-loop error scale with $A$? Sweep $A$ from 10 to $10^7$.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | base-current sense source | +0.7353 µA (current enters its + terminal); every value matches the hand analysis |
| 2 | Example 06-06.1 matrix | $G_{21}$ = 0.75 mS against $G_{12}$ = −0.25 mS; Example 06-06.5's largest asymmetry is $\mu = 10^5$ |
| 3 | $R_{in}$ against $\mu$ | 1 kΩ at $\mu = -99$, 200 kΩ at $\mu = 0.5$, infinite at $\mu = 1$, −100 kΩ at $\mu = 2$ |
| 4 | gain error | 1.050% at $A = 10^3$, 1.061 ppm at $A = 10^7$, falling one decade per decade |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-06.a | base-current sense reading | 0.7353 | µA |
| Lab 06-06.b | R_in at μ = 0.5 | 200 | kΩ |
| Lab 06-06.c | gain error at A = 1e3 | 1.050 | % |
| Lab 06-06.d | gain error at A = 1e7 | 1.061 | ppm |
| Lab 06-06.e | largest matrix asymmetry, Example 06-06.5 | 100000 | — |

## Discussion questions

1. Why does SPICE need a 0 V voltage source to define a current-controlled source, but not a voltage-controlled one?
2. A VCVS with $\mu$ slightly above 1 and a large $R_f$ gives a huge negative input resistance. Why is such a circuit hard to use in practice?
3. The error in Part 4 falls as $1/A$. Why do practical precision amplifiers not simply use op-amps with $A = 10^9$?
4. The small-signal models in this lab have no supply rails. Name one result in this lab that a real circuit could not produce.

<details><summary>Answers to the discussion questions</summary>

1. MNA's unknowns are node voltages plus the currents of voltage sources (06-04). A controlling voltage is already a combination of unknowns, but an arbitrary branch current is not; inserting a 0 V source makes that current an MNA unknown that the F or H stamp can refer to.
2. Its resistance depends on $1 - \mu$, the difference of two nearly equal numbers, so small changes in the gain (with temperature, supply or frequency) change the resistance enormously and can flip its sign. Connected to anything with a smaller positive resistance in parallel, the net resistance can approach zero conductance, the condition for oscillation or latch-up.
3. Gain costs stages, power and bandwidth, and high-gain loops are hard to stabilize (Course 11). Beyond a point other errors dominate: resistor tolerances and drift, the op-amp's offset voltage and bias currents (06-10), and noise. Accuracy budgets balance all of them.
4. For example, Example 06-06.1's VCCS delivering power indefinitely, or a gain-of-$10^5$ VCVS producing 100 kV from a 1 V input with the loop opened. A real amplifier is limited by its supply voltage and output current, so its small-signal model is valid only near its operating point.

</details>

## Optional hardware version

Build Example 06-06.2 with a real small-signal MOSFET (for example a 2N7000) biased from a 9–12 V supply: drain resistor 10 kΩ, source resistor 1 kΩ, gate biased through a 1 MΩ divider so that the drain sits near half the supply. Apply a 50 mV peak, 1 kHz sine through a coupling capacitor to the gate and measure the drain's AC amplitude with an oscilloscope. Compare the gain with $-R_D/(R_S + 1/g_m)$, estimating $g_m \approx 2I_D/(V_{GS} - V_{TH})$ from the measured DC operating point. Then bypass $R_S$ with a 100 µF capacitor and measure again: the gain rises toward $-g_m(R_D\parallel r_o)$ and becomes much more sensitive to the transistor.
