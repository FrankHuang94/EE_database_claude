# Lab 06-03 · Kirchhoff's Laws, Dividers, Bridges and Delta–Wye

**Chapter:** [06-03](../../chapters/06-03-kirchhoffs-laws.md) · **Notebook:** [06-03-networks.ipynb](06-03-networks.ipynb) · **Time:** about 90 minutes (plus 45 minutes for the optional hardware part)

## Objective

1. Verify KCL at every node and KVL around every mesh from a simulator's results, and count the independent equations.
2. Measure how a load pulls down a divider, and find the load at which the error becomes acceptable.
3. Compare the linearity and sensitivity of quarter-, half- and full-bridge strain-gauge circuits.
4. Check the delta–wye formulas numerically on random networks.

## Background

Chapter sections 3.1 to 3.7 and Examples 06-03.2 to 06-03.5. You need Python with NumPy and Matplotlib, and ngspice for Part 1 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook solves the same networks with its own nodal solver and skips the simulator cell.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-03-networks.ipynb](06-03-networks.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [networks.cir](networks.cir) | Examples 06-03.2 to 06-03.5 and Problems 06-03.6, 06-03.12 and 06-03.13, solved by ngspice | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **Kirchhoff by simulation (Part 1).** *Predict first:* Example 06-03.5 has 4 nodes and 6 branches (counting the source). How many independent KCL and KVL equations? Then let the notebook check KCL at each node and KVL around each mesh with the simulated values.
2. **Loading a divider (Part 2).** *Predict first:* for Example 06-03.3's divider (source resistance 24.8 kΩ), what load keeps the error below 0.1%? The notebook sweeps the load from 10 kΩ to 100 MΩ.
3. **Bridge linearity (Part 3).** *Predict first:* which of the quarter, half and full bridges is exactly linear in strain? The notebook sweeps ±5000 µε at 2.5 V excitation.
4. **Delta–wye by numbers (Part 4).** Convert 1000 random deltas to wyes and back, and compare the terminal resistances.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 06-03.5 | 3 independent KCL and 3 independent KVL equations; KCL and KVL residuals at rounding level; bridge current 16.39 mA |
| 2 | load for 0.1% error | about 24.8 MΩ (error ≈ $R_{source}/(R_{source} + R_L)$) |
| 3 | deviation from linear at +5000 µε | quarter bridge −0.50%; half bridge (equal and opposite gauges) 0; full bridge 0 |
| 4 | delta → wye → delta | recovers the original to rounding (relative error below $10^{-12}$) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-03.a | independent KCL equations, Example 06-03.5 | 3 | — |
| Lab 06-03.b | independent KVL equations, Example 06-03.5 | 3 | — |
| Lab 06-03.c | load resistance for 0.1% error | 24.8 | MΩ |
| Lab 06-03.d | quarter-bridge deviation from linear at +5000 µε | −0.50 | % |

## Discussion questions

1. The notebook checked KCL at all four nodes of Example 06-03.5 and found every residual tiny. Why does that not prove that four KCL equations are independent?
2. In Part 2 the error falls as $1/R_L$ for large loads. Why does a 0.1% target need a load a thousand times the source resistance, rather than ten times?
3. Why is the half bridge exactly linear only when its two gauges change by equal and opposite amounts?
4. If delta–wye conversions always work, why do circuit simulators not use them?

<details><summary>Answers to the discussion questions</summary>

1. All four equations are satisfied because the solution satisfies them, but one of them is implied by the other three: each branch current enters one node and leaves another, so the four equations sum identically to zero. Independence is about the equations, not about whether a particular solution satisfies them; with only three independent KCL equations plus three KVL equations there are exactly as many as needed to pair with the six element laws.
2. The relative error is $R_s/(R_s + R_L)$. Setting it to $10^{-3}$ requires $R_L = 999R_s$: errors fall only in inverse proportion to the load, so each extra decimal place of accuracy costs a factor of ten in load resistance (or a buffer).
3. With gauges $R(1 + x)$ and $R(1 - x)$ in the two arms of one divider, the divider's total stays $2R$, so its output $V(1 + x)/2$ is exactly linear in $x$. If the changes are not equal and opposite (for example, a gauge in tension paired with one at a different gauge factor), the denominator changes too and a small nonlinearity returns.
4. They would need to recognize structure (which resistors form a delta, which are in series), which is fragile and does not extend to sources, dependent sources and nonlinear devices. Nodal analysis (06-04) writes one KCL equation per node directly from the netlist, for any element, and solves them as a matrix: it never needs to know whether anything is in series.

</details>

## Optional hardware version

Build Example 06-03.3's divider with 100 kΩ and 33 kΩ resistors from a 9 V battery or a bench supply. Measure the output with a multimeter (typically 10 MΩ input resistance), then connect a 1 MΩ resistor across the output and measure again. Compare the drop with the loaded-divider formula. If your meter has a high-impedance mode (often > 1 GΩ on its lowest DC range), compare the readings in both modes across a 10 MΩ / 10 MΩ divider.
