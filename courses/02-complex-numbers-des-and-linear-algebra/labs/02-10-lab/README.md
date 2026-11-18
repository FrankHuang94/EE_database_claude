# Lab 02-10 · Numerical Methods for Engineers

**Chapter:** [02-10](../../chapters/02-10-numerical-methods.md) · **Notebook:** [02-10-numerics.ipynb](02-10-numerics.ipynb) · **Netlist:** [diode_newton.cir](diode_newton.cir) · **Time:** about 70 minutes

## Objective

1. See floating-point rounding, cancellation and saturation happen, in double, single and half precision.
2. Run Newton's method on a diode circuit with and without SPICE's junction limiting, and confirm that the companion-model iteration is Newton's method.
3. Measure the order of accuracy of Euler, Heun and RK4.
4. Compare explicit and implicit solvers on a stiff problem.
5. Watch an ill-conditioned system amplify a tiny change, and watch mixed-precision iterative refinement recover double-precision accuracy.
6. Confirm the diode operating point in ngspice and read its Newton iteration count.

## Background

Chapter sections 3.1–3.6 and Examples 02-10.1 to 02-10.6.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict the floating-point results, and which format drifts most in a long sum.
3. **Part 2:** predict where plain Newton's first step lands from 0.6 V.
4. **Part 3:** predict the error ratios when the step is halved.
5. **Part 4:** predict the step counts of explicit and implicit solvers on the stiff problem.
6. **Part 5:** predict the effect of a 0.0001 change in the ill-conditioned system.
7. **Part 6:** from the repository root, run `python tools/run_spice.py 02-10`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | floating-point surprises | `0.1 + 0.2 - 0.3` = 5.551×10⁻¹⁷; $1 - \cos(10^{-8})$ = 0 directly; float32 $10^8 + 1 = 10^8$ (spacing 8) |
| 1 | 20,000 × 0.1 | float64 2000.000000; float32 1999.658813; float16 stuck at 256 (spacing 0.25 there) |
| 2 | diode circuit | 0.6929 V, 4.307 mA; plain Newton 5 / 33 / 173 iterations from 0.7 / 0.6 / 0 V; limited 5 / 8 / 9; the companion-model iterates equal Newton's to every printed digit |
| 3 | order | error ratios near 2, 4 and 16 |
| 4 | stiffness | RK45 takes about ten times more steps than Radau or BDF (counts depend on the SciPy version); trapezoidal fast-mode factor −0.9231 |
| 5 | conditioning | κ = 40,002; $\mathbf{x}$ jumps from (1, 1) to (0, 2); single-precision factorization plus 2 refinement passes reaches about $10^{-14}$ |
| 6 | ngspice | 0.6929 V and 4.307 mA, in a handful of iterations (5 with ngspice-42) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-10.a | float16 sum of 0.1 stalls at | 256 | — |
| Lab 02-10.b | float16 spacing at 256 | 0.25 | — |
| Lab 02-10.c | float32 sum of 20,000 × 0.1 | 1999.659 | — |
| Lab 02-10.d | float32 spacing near 1e8 | 8 | — |

## Discussion questions

1. Plain Newton from 0.6 V eventually converged. Why would a real simulator still fail on it, and which of its safeguards (limiting, GMIN, source stepping) would rescue it?
2. Why can an AI accelerator accumulate a dot product of FP8 or BF16 values safely in FP32, but not in BF16? Use the stalled float16 sum of Part 1 as evidence.
3. In Part 5, refinement in single precision converged in two passes. Would it converge for κ = 10⁸? What would you change?

## Optional hardware version

Measure a real silicon diode (for example a 1N4148) in the circuit of Example 02-10.2, with a 5 V supply and a 1 kΩ resistor, using a multimeter. Then fit $I_S$ and the ideality factor $n$ from two measurements at different resistor values (say 1 kΩ and 10 kΩ), by solving the two diode equations with Newton's method for systems. Real small-signal diodes have $n$ between 1 and 2 and $I_S$ in the nanoampere-to-femtoampere range, so expect your fitted values to differ from the textbook $10^{-14}$ A.
