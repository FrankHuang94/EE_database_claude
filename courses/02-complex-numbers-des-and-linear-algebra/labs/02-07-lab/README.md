# Lab 02-07 · Determinants, Inverses, Rank and Vector Spaces

**Chapter:** [02-07](../../chapters/02-07-determinants-inverses-and-vector-spaces.md) · **Notebook:** [02-07-subspaces-least-squares.ipynb](02-07-subspaces-least-squares.ipynb) · **Netlist:** [resistance_matrix.cir](resistance_matrix.cir) · **Time:** about 70 minutes

## Objective

1. Confirm that $\lvert\det\mathbf{A}\rvert$ is the area scale factor of a linear map, and see why cofactor expansion is never used for large matrices.
2. Compare forming an inverse with solving directly, in time and in accuracy.
3. Find rank, column space and null space exactly, and see why numerical rank needs a stated tolerance.
4. Fit data by least squares three ways, check the orthogonality of the residuals, and see overfitting happen.
5. Build a circuit's incidence matrix, find its loops, form $\mathbf{G} = \mathbf{A}^\mathsf{T}\mathbf{C}\mathbf{A}$, and read the resistance matrix both from $\mathbf{G}^{-1}$ and from ngspice.

## Background

Chapter sections 3.1–3.4 (determinants, volume, inverses), 3.7 (rank and the complete solution), 3.8 (least squares) and 3.9 (incidence matrices), and Examples 02-07.2 to 02-07.5.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict how the cofactor time grows from $n = 9$ to $n = 12$.
3. **Part 2:** predict which of `inv(A) @ b` and `solve(A, b)` is faster, and by how much.
4. **Part 3:** predict the rank NumPy reports for a rank-2 matrix with $10^{-13}$ noise added.
5. **Part 4:** predict what happens to the residuals and the coefficients as the polynomial degree rises to 4.
6. **Part 5:** read the loop basis and the resistance matrix, and check reciprocity.
7. **Part 6:** from the repository root, run `python tools/run_spice.py 02-07`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | image area vs determinant | equal: 10, 2 and 0 for the three matrices (the last has parallel columns) |
| 1 | cofactor time growth | about ×$n$ per step; 12!/9! = 1,320 times longer at $n = 12$ than at $n = 9$ |
| 2 | `inv(A) @ b` vs `solve(A, b)` | the inverse is roughly 3× slower (machine-dependent) and no more accurate |
| 3 | Example 02-07.3 | rank 2; null space (−2, 1, 0, 0), (−1, 0, −2, 1); condition $b_1 - 2b_2 + b_3 = 0$ |
| 3 | noisy rank-2 matrix | rank 5 at NumPy's default tolerance (the noise exceeds it), 2 at a tolerance of $10^{-10}$ |
| 4 | Example 02-07.4 | all three methods agree: 0.3996 V and 10.025 mV/°C; $\mathbf{A}^\mathsf{T}\mathbf{e} = \mathbf{0}$ |
| 4 | polynomial degree | SSE falls from $3.87\times10^{-5}$ to $1.806\times10^{-5}$ V² (degree 2), then to essentially 0 at degree 4, which interpolates the noise |
| 5 | Example 02-07.5 | rank 3, two independent loops, $\mathbf{G}$ as in 02-06, $\mathbf{R}$ symmetric with first column (1.074, 0.4815, 0.2593) kΩ |
| 6 | `resistance_matrix.cir` | matches Examples 02-07.2 and 02-07.5 and Problems 02-07.11 to 02-07.13, including $R_{13} = R_{31}$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-07.a | image area under [[1, 2], [3, 4]] | 2 | — |
| Lab 02-07.b | cofactor work ratio 12!/9! | 1320 | — |
| Lab 02-07.c | numerical rank at tolerance 1e-10 | 2 | — |
| Lab 02-07.d | sum of squared residuals, quadratic fit | 1.806×10^-5 | V² |
| Lab 02-07.e | sum of squared residuals, degree-4 fit | 0 | V² |

## Discussion questions

1. The degree-4 polynomial fits the five calibration points perfectly. Why is it a worse calibration than the straight line? What would you need in order to justify a quadratic term?
2. The ladder's resistance matrix has every entry positive, and its largest entry is on the diagonal of the middle node. Explain both facts physically.
3. Your colleague computes $\det\mathbf{G}$ for a 10,000-node power grid, finds $10^{-4000}$ (an underflow), and concludes the grid model is broken. What is wrong with the reasoning, and what should they check instead?

## Optional hardware version

Build the 1 Ω ladder of Example 02-07.2 at a safer scale with 1 kΩ resistors (so the resistance matrix is in kΩ). Use a bench supply with a 10 kΩ series resistor as an approximate 1 mA current source into node 1. Measure all three node voltages and divide by the measured current. You should find a column close to (0.75, 0.5, 0.25) kΩ. Then inject at node 3 and measure node 1 to check reciprocity.
