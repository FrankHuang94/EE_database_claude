# Lab 06-02 · Element Laws, Real Sources and Real Resistors

**Chapter:** [06-02](../../chapters/06-02-circuit-elements-and-ohms-law.md) · **Notebook:** [06-02-elements.ipynb](06-02-elements.ipynb) · **Time:** about 90 minutes (plus 45 minutes for the optional hardware part)

## Objective

1. Plot the i–v characteristics of a resistor, practical voltage and current sources and a diode, and read element parameters from them.
2. Distinguish a diode's static resistance from its incremental resistance in simulation.
3. Recover a battery's open-circuit voltage and internal resistance from a simulated load sweep.
4. See what happens when sources that "cannot" be paralleled are paralleled with realistic internal resistances.
5. Find out where the E-series values come from, and compare worst-case and statistical views of tolerance.

## Background

Chapter sections 3.2 (Ohm's law and power), 3.5 (independent sources and impossible connections), 3.6 (internal resistance) and 3.7 (real resistors); Examples 06-02.3 to 06-02.5. You need Python with NumPy and Matplotlib, and ngspice for Parts 1 to 3 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook computes the same curves from the element laws and skips the simulator cells.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-02-elements.ipynb](06-02-elements.ipynb) | The guided notebook (Parts 1 to 5) | Its own `assert`s |
| [elements.cir](elements.cir) | Diode voltages and incremental resistance at 300 K; Example 06-02.3's cell under load; Problem 06-02.7's supply; a load sweep that recovers $R_{int}$ | Chapter and solution answer keys |
| [parallel_cells.cir](parallel_cells.cir) | Example 06-02.5 with and without a load; Problem 06-02.12; two cells 0.1 V apart | Chapter, solution and handout answer keys |

Both netlists are run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **i–v characteristics (Part 1).** *Predict first:* which of the four elements' curves pass through the origin? What is the diode's slope $dv/di$ at 1 mA? Run the notebook cell, which plots all four curves from their element laws and, if ngspice is installed, overlays the simulator's diode points.
2. **A battery under load (Part 2).** The netlist sweeps the load current drawn from Example 06-02.3's cell from 0 to 5 A. *Predict first:* what straight line will the terminal voltage follow? Fit a line to the sweep and read $V_{oc}$ and $R_{int}$.
3. **Cells in parallel (Part 3).** *Predict first:* two cells differ by only 0.1 V, each with 50 mΩ. How large is the current that flows between them? Then vary the difference from 0 to 0.6 V and plot the circulating current and the heat.
4. **Where the E-series comes from (Part 4).** Generate $10^{k/n}$, rounded to two significant figures, for $n$ = 12 and 24, and compare with the standard values. *Predict first:* how many of the 24 E24 values does the formula reproduce?
5. **Tolerance, statistically (Part 5).** Draw 100 000 random resistor values (uniform within ±5%) and supply voltages (uniform within ±5%) for Example 06-02.4's LED circuit. *Predict first:* will any sample fall outside the worst-case range 8.41 to 11.05 mA? What fraction falls within ±5% of the nominal 9.67 mA?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | diode at 1 mA (300 K) | 0.6548 V; static resistance 654.8 Ω; incremental resistance 25.85 Ω |
| 2 | fitted terminal line | $v = 3.90 - 0.40\,i$: $V_{oc}$ = 3.90 V, $R_{int}$ = 0.40 Ω |
| 3 | circulating current for a 0.1 V difference | 1.0 A (0.1 V over 0.1 Ω), 0.1 W of heat; 6.0 A and 3.6 W for 0.6 V |
| 4 | formula versus standard | E12: 5 of 12 values differ (2.7, 3.3, 3.9, 4.7, 8.2); E24: 8 of 24 differ; the largest E24 step is 1.3 → 1.5 (×1.154) |
| 5 | Monte Carlo LED current | every sample inside the worst-case range; most samples well inside it (the extremes need both tolerances at their limits) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-02.a | circulating current for a 0.1 V difference | 1.0 | A |
| Lab 06-02.b | E12 values that differ from rounded 10^(k/12) | 5 | — |
| Lab 06-02.c | E24 values that differ from rounded 10^(k/24) | 8 | — |
| Lab 06-02.d | largest ratio between adjacent E24 values | 1.154 | — |
| Lab 06-02.e | internal resistance recovered from the sweep | 0.40 | Ω |

## Discussion questions

1. The battery model's terminal line is straight. What would make a real battery's line curve, and over what range would you trust the model?
2. Why is the circulating current between parallel cells so large for such a small voltage difference, and what do battery packs do about it?
3. If the E24 values were the pure geometric series, the largest step would be about 1.10. The real series has a step of 1.154. Does that leave values that no ±5% E24 resistor can reach?
4. In Part 5, why are the worst-case extremes so rare in the Monte Carlo, and when should a designer still design for them?

<details><summary>Answers to the discussion questions</summary>

1. The internal resistance itself depends on the current (electrochemical effects make the voltage drop grow less than linearly at high currents), on the state of charge, on temperature and on time (a pulse sees less drop at first than a sustained load, because part of the drop builds up over seconds). The linear model is trustworthy near the currents at which it was measured, here 0 to about 0.4 A, and only roughly beyond them.
2. The only thing limiting the current is the sum of the two internal resistances, here 0.1 Ω, so every 0.1 V of difference drives 1 A. Lithium cells' internal resistances are milliohms to tens of milliohms, so connecting cells at different states of charge can drive tens of amperes. Packs therefore connect cells only when their voltages match, and in service they balance them (bleeding charge from the highest cells or moving it between cells) and use switches or diodes to isolate strings.
3. Between 1.3 and 1.5 a ±5% part covers 1.235 to 1.365 and 1.425 to 1.575, leaving a gap from 1.365 to 1.425 that no E24 ±5% part guarantees. In practice designers use the next series (E48 or E96 with tighter tolerance) for such values, or combine two resistors. The historical E24 values are a convention, not an optimum.
4. The current depends on two independent tolerances; reaching an extreme needs both at their limits together, which is improbable for uniform distributions (and the density falls off toward the corners of the joint distribution). A designer still designs for the worst case when a failure is unacceptable (safety, or a product shipped in millions where rare combinations will occur), and uses statistical results to judge yield when a small fraction of out-of-spec units can be screened or tolerated (03-04).

</details>

## Optional hardware version

With a bench supply, a multimeter and an alkaline AA cell, measure the cell's open-circuit voltage, then its terminal voltage across a 10 Ω, 1 W resistor (current about 0.15 A; disconnect within a few seconds so that the cell does not heat). Compute the internal resistance as in Example 06-02.3. Repeat with a 4.7 Ω resistor and compare: is the resistance the same at both currents? Then measure a 1 Ω resistor's resistance with the meter's ordinary two-wire ohms range, short the probes together to read the lead resistance, and compare the corrected value (Problem 06-02.14).
