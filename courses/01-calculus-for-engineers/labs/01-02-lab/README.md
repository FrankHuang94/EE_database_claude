# Lab 01-02 · Limits and Continuity

**Chapter:** [01-02](../../chapters/01-02-limits-and-continuity.md) · **Notebook:** [01-02-limits.ipynb](01-02-limits.ipynb) · **Netlists:** [switch_rc.cir](switch_rc.cir), [diode_op.cir](diode_op.cir) · **Time:** about 60 minutes

## Objective

1. Estimate limits from tables, and find the base $e$ from its defining limit.
2. See where numerical limits fail: truncation error against rounding error.
3. Implement bisection and use it to find a diode operating point.
4. Measure how quickly a low-pass response approaches its asymptotes.
5. Confirm a switching event's one-sided limits, and the bisection results, in ngspice.

## Background

Chapter sections 3.3 (standard limits), 3.4 (one-sided limits at a switch), 3.6 (IVT and bisection), 3.7 (asymptotes) and 3.9 (limits on a computer).

## Procedure

1. Run all notebook cells in order.
2. **Part 1:** before running, predict whether $(e^h - 1)/h$ at $h = 10^{-12}$ is closer to 1 than at $h = 10^{-6}$. Then study the error plot and locate its minimum.
3. **Part 2:** note how quickly $(1 + r/n)^n$ approaches $e^r$.
4. **Part 3:** before running, predict how many bisection steps shrink the bracket $[0, 1]$ V below 1 µV.
5. **Part 4:** read off the asymptote error at $f_c$, $10f_c$ and $100f_c$.
6. **Part 5:** from the repository root, run `python tools/run_spice.py 01-02`. Then open `switch_rc.cir` and change the capacitor to 1 µF. Predict $i_C$ at 1 µs and $v_C$ at 20 ms before re-running.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $(e^h - 1)/h$ at $h = 10^{-12}$ | about 1.0001: *worse* than at $10^{-6}$ (error about $5\times10^{-7}$), because rounding dominates |
| 1 | best step size | about $2\times10^{-8}$, error about $10^{-8}$ |
| 3 | bisection steps to 1 µV | 20, giving $V = 0.69249$ V |
| 5 | $v_C$ at 1 ns and at 1 µs | essentially 0, and 5.00 mV: continuous |
| 5 | $i_C$ at 1 µs | 0.4995 mA: it jumped from 0 at the switching instant |
| 5 | $v_C$ at 20 ms ($20\tau$) | 5.000 V: the final value |
| 5 | diode operating points | 0.6925 V / 4.308 mA and 0.6796 V / 0.2620 mA, matching bisection |

With $C = 1$ µF, $\tau = 10$ ms: $i_C(1\text{ µs})$ stays essentially 0.5 mA (since $e^{-0.0001} \approx 1$), and $v_C(20\text{ ms}) = 5(1 - e^{-2}) = 4.32$ V, not yet settled.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-02.a | bisection steps to 1 µV | 20 | — |
| Lab 01-02.b | capacitor current at 1 µs | 0.4995 | mA |
| Lab 01-02.c | capacitor voltage at 20 ms | 5.000 | V |
| Lab 01-02.d | capacitor voltage at 1 µs | 5.00 | mV |

## Discussion questions

1. ngspice uses Newton's method, not bisection. Why might it still fail to converge on a circuit where bisection would succeed? (Hint: 00-04, Problem 9.)
2. The simulated source rises in 1 ns rather than instantly. Why does that barely change the measured one-sided limits? When would it matter?
3. Where in your work (models, forecasts, valuations) do you rely on a limit that is never actually reached? How do you check that the approach is fast enough to matter?

## Optional hardware version

With a 9 V battery, a 10 kΩ resistor, a 100 µF capacitor (τ = 1 s, slow enough to watch) and a multimeter, close the circuit and read the capacitor voltage every second for 10 s. It starts at 0 (continuous) and approaches 9 V. Then put the meter in series on its current range (about 1 mA full scale) and repeat: the current is about 0.9 mA immediately and decays toward zero.
