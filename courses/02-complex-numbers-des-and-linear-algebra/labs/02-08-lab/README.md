# Lab 02-08 · Eigenvalues and Eigenvectors

**Chapter:** [02-08](../../chapters/02-08-eigenvalues-and-eigenvectors.md) · **Notebook:** [02-08-eigen.ipynb](02-08-eigen.ipynb) · **Netlists:** [coupled_lc.cir](coupled_lc.cir), [coupled_lc_beat.cir](coupled_lc_beat.cir) · **Time:** about 75 minutes

## Objective

1. Compute eigenpairs numerically and confirm them by multiplication and by the trace and determinant checks.
2. Watch a Markov chain converge to its steady state at the rate set by its second eigenvalue, and find the steady state by the power method.
3. See complex eigenvalues as spirals, and the stability boundary $\lvert\lambda\rvert = 1$.
4. See the eigenvectors of a symmetric matrix as orthogonal modes.
5. Find the normal modes of coupled resonators, numerically and in ngspice, by driving each mode's eigenvector pattern.
6. Use the SVD for low-rank approximation, and confirm that the error equals the first discarded singular value.

## Background

Chapter sections 3.1–3.9, and Examples 02-08.1 to 02-08.6.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict whether any arrow keeps its direction under $0.95\,\mathbf{R}_{30°}$.
3. **Part 2:** predict how many 1 ms steps the wearable's chain needs to come within 0.01 of steady state.
4. **Part 3:** predict the amplitude after one oscillation when $r = 1.02$.
5. **Part 4:** predict the shapes of the smoothest and the roughest ladder modes.
6. **Part 6:** predict how many singular values stand above the noise floor.
7. **Part 7:** from the repository root, run `python tools/run_spice.py 02-08`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Example 02-08.1 | eigenvalues 5 and 2; $\mathbf{A}^5$ = [[2094, 1031], [2062, 1063]]; no real eigenvector for the rotation |
| 2 | wearable chain | eigenvalues 1, 0.9338, 0.7462; steady state (0.1786, 0.1071, 0.7143); 0.9479 mA; every component within 0.01 (absolute) of the steady state after 66 steps. The chapter's relative criterion, $0.9338^k = 0.01$, gives 67.2 steps; the absolute count is a little smaller because the starting deviation is about 0.82 rather than 1 |
| 3 | spirals | $r = 0.95$ decays to 0.5404 after 12 steps; $r = 1.02$ grows to 1.268 |
| 4 | 20-node ladder | eigenvalues from 0.02234 to 3.978 S, equal to $2 - 2\cos(k\pi/21)$; modes are sampled sines; $\mathbf{Q}^\mathsf{T}\mathbf{Q} = \mathbf{I}$ |
| 5 | coupled resonators | the in-phase mode stays at 5.033 MHz for every $C_c$; complete transfer at 1.140 µs for $C_c = 0.1$ nF |
| 6 | noisy rank-3 image | three singular values well above the noise floor; 2-norm error of the rank-$k$ approximation equals $\sigma_{k+1}$ |
| 7 | `coupled_lc.cir` | peaks at 5.033 and 4.594 MHz (Example 02-08.5) and 4.949 and 4.518 MHz (Problem 02-08.13) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-08.a | first step within 0.01 of steady state | 66 | — |
| Lab 02-08.b | amplitude after 12 steps with r = 1.02 | 1.268 | — |
| Lab 02-08.c | smallest eigenvalue, 20-node ladder | 0.02234 | S |
| Lab 02-08.d | largest eigenvalue, 20-node ladder | 3.978 | S |
| Lab 02-08.e | rank of the noise-free image | 3 | — |

## Discussion questions

1. The power method needed hundreds of iterations, yet the chain is within 0.01 of its steady state after 66 steps. Why does the power method's stopping tolerance ($10^{-12}$) take so much longer, and which eigenvalue sets its speed?
2. In Part 5, the eigenvectors of the capacitance matrix do not depend on $C_c$, but the eigenvalues do. Why? What would break this if the two resonators were not identical?
3. In Part 6, how would you choose the rank $k$ for real data, where the noise level is not known in advance?

## Optional hardware version

Build two parallel LC tanks from 1 µH inductors and 1 nF capacitors, and couple them with a 100 pF capacitor. Drive one tank through a 10 kΩ resistor from a signal generator, and sweep from 4 to 5.5 MHz while watching the other tank's voltage on an oscilloscope (10× probe). You should see two peaks near 4.6 and 5.0 MHz. Component tolerances (often ±5–10%) shift them, and probe capacitance (a few pF) lowers both slightly. Measure the actual L and C first if you want a close comparison.
