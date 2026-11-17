# Lab 02-05 · The Laplace Transform for ODEs

**Chapter:** [02-05](../../chapters/02-05-laplace-transform-for-odes.md) · **Notebook:** [02-05-laplace.ipynb](02-05-laplace.ipynb) · **Netlists:** [rlc_step_vs_sxfer.cir](rlc_step_vs_sxfer.cir), [rc_pulse.cir](rc_pulse.cir) · **Time:** about 60 minutes

## Objective

1. Check the transform table and the derivative rule with a computer-algebra system.
2. Compute partial fractions with SymPy and SciPy, including a repeated pole.
3. See how pole positions control the impulse response.
4. See when the final-value theorem gives a right answer and when it gives a wrong one.
5. Simulate a transfer function directly as an $s$-domain block, and compare it with the physical circuit.

## Background

Chapter sections 3.1–3.3 (definition, properties, partial fractions), 3.6 (transfer functions and poles) and 3.7 (initial- and final-value theorems), and Examples 02-05.3 and 02-05.4.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 2:** predict the partial-fraction terms of $1/(s^2(s + 1))$ before running.
3. **Part 3:** predict what happens to the impulse response as the poles approach and cross the imaginary axis.
4. **Part 4:** for each transform, decide from its poles whether the final-value theorem applies, then compare with the printed long-time value.
5. **Part 5:** from the repository root, run `python tools/run_spice.py 02-05`. Then edit the `s_xfer` denominator in `rlc_step_vs_sxfer.cir` to `[1 2000 1.000025e8]`, which places the poles at $-1000 \pm j9950$, predict the overshoot, and re-run.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | table and derivative rule | every check "True"; $\mathcal{L}\{f'\} = sF - f(0)$ |
| 2 | $1/(s^2(s + 1))$ | $1/s^2 - 1/s + 1/(s + 1)$, so $y = t - 1 + e^{-t}$ |
| 2 | SciPy residues of $(s + 4)/(s^2(s + 2))$ | −0.5 and 2 at the double pole 0; 0.5 at −2 |
| 3 | poles at σ ± 3j | ringing at 3 rad/s (0.4775 Hz) with envelope $e^{\sigma t}$ |
| 4 | final-value theorem | correct only for the stable case (2); wrong for the others, e.g. $e^{20} = 4.852\times10^8$ for $1/(s - 1)$ |
| 5 | `rlc_step_vs_sxfer.cir` | 44.43% overshoot from both the circuit and the `s_xfer` block, at 0.3245 ms |
| 5 | `rc_pulse.cir` | 4.323 V at 2 ms, 1.590 V at 3 ms |
| 5 | poles moved to $-1000 \pm j9950$ | overshoot about 72.93% |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-05.a | ringing frequency for poles at σ ± 3j | 0.4775 | Hz |
| Lab 02-05.b | e^20 for 1/(s − 1) at t = 20 | 4.852×10^8 | — |
| Lab 02-05.c | overshoot with poles −1000 ± j9950 | 72.93 | % |
| Lab 02-05.d | constant term of the new denominator | 1.000025×10^8 | — |

## Discussion questions

1. The `s_xfer` block and the R-L-C circuit give the same step response. What would differ if the inductor saturated at high current, and which model would still be right?
2. Why does SciPy report a double pole twice, and how do you assign its two residues to the $1/s$ and $1/s^2$ terms?
3. A colleague applies the final-value theorem to an oscillator's transfer function and concludes the output settles to zero. What is wrong?

## Optional hardware version

With a function generator, an oscilloscope, a 1 kΩ resistor and a 1 µF capacitor (τ = 1 ms): apply a 5 V, 2 ms pulse repeating every 20 ms, and measure the capacitor voltage at the end of the pulse and 1 ms later. Compare with 4.323 V and 1.590 V; the generator's own output resistance (often 50 Ω) slightly lengthens τ, so add it to $R$ in your prediction.
