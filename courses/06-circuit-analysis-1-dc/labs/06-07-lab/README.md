# Lab 06-07 · Linearity and Superposition

**Chapter:** [06-07](../../chapters/06-07-linearity-and-superposition.md) · **Notebook:** [06-07-superposition.ipynb](06-07-superposition.ipynb) · **Time:** about 75 minutes (plus 30 minutes for the optional hardware part)

## Objective

1. Confirm superposition in ngspice by running each circuit with all sources and with one source at a time.
2. See superposition fail with a diode, and see the small-signal (linearized) prediction succeed for small changes.
3. Find where a binary-weighted DAC's nonlinearity concentrates when its resistors are mismatched.
4. Compare worst-case and root-sum-square error totals with a Monte Carlo simulation.

## Background

Chapter sections 3.1 to 3.6 and Examples 06-07.1 to 06-07.5. You need Python with NumPy, SciPy and Matplotlib, and ngspice for Part 1 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips the simulator cell.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-07-superposition.ipynb](06-07-superposition.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [superposition.cir](superposition.cir) | Examples 06-07.1 to 06-07.5 and Problems 06-07.4, 06-07.5, 06-07.7 and 06-07.12, each with all sources and with single sources | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **Superposition in ngspice (Part 1).** *Predict first:* which source delivers power in Example 06-07.1? Then compare the all-sources runs with the sums of the single-source runs.
2. **Linearity fails (Part 2).** *Predict first:* does superposition become accurate for small added currents in the diode circuit? Sweep the added current from 1 µA to 10 mA.
3. **DAC mismatch (Part 3).** *Predict first:* which transition has the worst DNL? Simulate 1000 DACs with random 1% resistor errors.
4. **Worst case against RSS (Part 4).** *Predict first:* what fraction of units exceed the RSS of three uniform error limits (±2, ±3, ±6 mV)?

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 06-07.1 | $v_a$ = 12 V = 7.2 + 4.8 V; the 12 V source delivers 0 W and the 2 A source 24 W; the diode circuit's single-source runs add to 1.322 V against a true 0.6979 V |
| 2 | small changes | naive superposition wrong at every level; the small-signal prediction (incremental resistance 6.002 Ω) within 0.2% at 10 µA |
| 3 | DAC | worst DNL at the major carry, 011 → 100 |
| 4 | error totals | worst case 11 mV; RSS of the limits 7 mV; standard deviation of the total 4.041 mV; about 7.4% of units above 7 mV, none above 11 mV |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-07.a | power from the 12 V source, Example 06-07.1 | 0 | W |
| Lab 06-07.b | diode incremental resistance at the 5 V operating point | 6.002 | Ω |
| Lab 06-07.c | worst-case total | 11 | mV |
| Lab 06-07.d | RSS of the limits | 7 | mV |
| Lab 06-07.e | standard deviation of the total | 4.041 | mV |
| Lab 06-07.f | probability of exceeding the RSS figure | 7.4 | % |
| Lab 06-07.g | power absorbed by the 12 V source with a 3 A source | 7.2 | W |

## Discussion questions

1. In Part 1 the 12 V source of Example 06-07.1 delivers no power, yet its single-source run shows it driving 1.2 A. Is there a contradiction?
2. Why does the small-signal prediction in Part 2 drift away from the true change as the added current approaches the bias current?
3. In Part 3, the transitions 001 → 010 and 101 → 110 show the second-largest DNL. Why?
4. Part 4 found that 7.4% of units exceed the "RSS" figure. When would you specify a product with that figure, and when with the worst case?

<details><summary>Answers to the discussion questions</summary>

1. No. Currents superpose: 1.2 A from the 12 V source's own drive and −1.2 A pushed back by the 2 A source cancel, so the actual current, and hence the power, is zero. Powers computed run by run would wrongly credit the source with 14.4 W.
2. The small-signal model replaces the diode by its tangent at the operating point, with incremental resistance $V_T/I_D$. As the added current grows, the operating point moves along the exponential and the tangent's slope no longer describes it: the second-order (curvature) term of the Taylor expansion becomes significant (01-08).
3. Those are the transitions where bit 1 switches on while bit 0 switches off: the second-largest weight against the smallest, a "minor carry". The larger the weight that switches against the others, the larger the possible mismatch.
4. A statistical figure suits a specification that describes the population (typical performance, with production test screening the tails) and where the cost of the rare outlier is low. A worst-case figure is needed when every unit must meet the limit without test, such as safety, regulatory or interoperability limits, or when errors may be correlated.

</details>

## Optional hardware version

Build Example 06-07.1 at low power: replace the 12 V source by a 12 V bench supply (or 9 V battery, scaling the answers) and the 2 A source by a second supply in constant-current mode at 20 mA with 400 Ω and 600 Ω resistors (every resistance ×100, every current ÷100, so every voltage is unchanged). Measure $v_a$ with both sources, then with each source alone (replace the voltage source by a wire, and disconnect the current source). Check that the two partial readings add to the full one, and measure the current from the 12 V supply: it should be close to zero.
