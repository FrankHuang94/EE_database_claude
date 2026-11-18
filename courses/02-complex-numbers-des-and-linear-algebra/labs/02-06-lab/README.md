# Lab 02-06 · Vectors, Matrices and Linear Systems

**Chapter:** [02-06](../../chapters/02-06-vectors-matrices-and-linear-systems.md) · **Notebook:** [02-06-linear-systems.ipynb](02-06-linear-systems.ipynb) · **Netlists:** [nodal.cir](nodal.cir), [power_rail.cir](power_rail.cir) · **Time:** about 75 minutes

## Objective

1. Compute dot products, angles and projections, and connect the angle between two signals to their correlation.
2. Measure how the cost of a matrix product grows with size.
3. Implement Gaussian elimination with back substitution, then factor once and solve many times with library routines.
4. See roundoff destroy an unpivoted solve, and partial pivoting repair it.
5. Build conductance matrices by stamping, solve circuits, and check them against ngspice.
6. Solve a sparse power-grid model and see how supply-pad placement sets the IR drop.

## Background

Chapter sections 3.2–3.3 (dot product, projection), 3.5 (matrix multiplication and its cost), 3.7–3.9 (elimination, LU, pivoting) and 3.10 (nodal analysis), and Examples 02-06.1, 02-06.3, 02-06.4 and 02-06.5.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict the angle between a sine and a cosine sampled over whole periods.
3. **Part 2:** predict the time ratio when $n$ doubles, then compare with the largest sizes.
4. **Parts 3–4:** compare the hand-written solver with the library, and predict how many digits the unpivoted solve keeps at $\varepsilon = 10^{-8}$.
5. **Part 5:** solve Example 02-06.5 and Problem 02-06.11 with the stamping function.
6. **Part 6:** predict where the worst IR drop sits with one corner pad, and how much four corner pads reduce it.
7. **Part 7:** from the repository root, run `python tools/run_spice.py 02-06` and compare ngspice's node voltages with your matrix solutions.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 02-06.1 | u·v = 14, θ = 21.04°, error length 1.795, error ⟂ u |
| 1 | sampled sine vs cosine over whole periods | 90°: orthogonal |
| 1 | correlation coefficient vs cos θ of centered vectors | identical (0.6188 with the notebook's random seed) |
| 2 | time ratio when $n$ doubles | approaches 8 for large $n$; machine-dependent |
| 3 | Example 02-06.3 | x = (1, 2, 3); second right-hand side (−0.5, 1, 0); product of pivots 30 |
| 4 | unpivoted relative error | 2.8×10⁻¹³ at ε = 10⁻⁴; 5.0×10⁻⁹ at 10⁻⁸ (about 8 correct digits); 100% at 10⁻¹⁷ |
| 5 | Example 02-06.5 | 10.74, 4.815 and 2.593 V; 107.4 mW |
| 6 | 20×20 grid, 0.1 Ω links, 1 mA per node | worst drop 77.85 mV (one corner pad, at the opposite corner) vs 15.06 mV (four corner pads, near the center): 5.170× less |
| 6 | sparsity | 399 unknowns, 1,915 nonzeros: 4.8 per row |
| 7 | `nodal.cir` and `power_rail.cir` | match Example 02-06.5 and Problems 02-06.11, 13 and 14 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-06.a | angle between sampled sine and cosine | 90 | ° |
| Lab 02-06.b | unpivoted relative error at ε = 1e-8 | 5.0×10^-9 | — |
| Lab 02-06.c | worst drop, one corner pad | 77.85 | mV |
| Lab 02-06.d | worst drop, four corner pads | 15.06 | mV |
| Lab 02-06.e | reduction factor | 5.170 | — |
| Lab 02-06.f | unknowns with one pad | 399 | — |
| Lab 02-06.g | nonzeros of G | 1915 | — |
| Lab 02-06.h | correlation coefficient with seed 0 | 0.6188 | — |
| Lab 02-06.i | unpivoted relative error at ε = 1e-4 | 2.8×10^-13 | — |

## Discussion questions

1. Part 6's grid has 399 unknowns but only 1,915 nonzeros. Why would a dense solver waste almost all its work, and how does the gap scale as the grid grows?
2. Partial pivoting changed the answer of Part 4 but not of Part 3. What property of the matrix decides whether pivoting matters numerically?
3. Four corner pads helped by about 5×, but chips use hundreds or thousands of supply bumps. Using Problem 02-06.14's result that drop scales with the square of pad spacing, explain why.

## Optional hardware version

Build Example 02-06.5 on a breadboard from 1% resistors (1 kΩ, 2 kΩ, 1 kΩ, 2 kΩ, 500 Ω, the last as two 1 kΩ in parallel). Replace the 10 mA source with a bench supply set to the computed 10.74 V across nodes 1 and ground. Measure the other two node voltages with a multimeter, and compare with 4.815 V and 2.593 V. Resistor tolerance alone should keep you within about 1%.
