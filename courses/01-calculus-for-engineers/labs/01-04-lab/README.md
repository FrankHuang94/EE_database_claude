# Lab 01-04 · Applications of Derivatives

**Chapter:** [01-04](../../chapters/01-04-applications-of-derivatives.md) · **Notebook:** [01-04-applications.ipynb](01-04-applications.ipynb) · **Netlist:** [max_power.cir](max_power.cir) · **Time:** about 60 minutes

## Objective

1. Locate three engineering optima and measure how flat each one is.
2. Compare worst-case, root-sum-of-squares and Monte Carlo tolerance analysis.
3. Watch Newton's method converge quadratically, and map where it diverges.
4. Check a L'Hôpital limit numerically, and see floating-point cancellation spoil the direct formula.
5. Confirm maximum power transfer with an ngspice load sweep.

## Background

Chapter sections 3.2 (classifying optima, flatness), 3.4 (optimization), 3.5 (linearization and tolerances), 3.6 (Newton's method) and 3.8 (L'Hôpital's rule).

## Procedure

1. Run all notebook cells in order.
2. **Part 1:** note the penalty for missing each optimum by a factor of 2.
3. **Part 2:** before running, predict whether the Monte Carlo standard deviation matches the worst case, the RSS of the tolerance limits, or the RSS of the standard deviations ($t/\sqrt3$ for a uniform ±$t$ spread).
4. **Part 3:** confirm that the number of correct digits roughly doubles per Newton step, and find the edge of the arctan convergence region.
5. **Part 4:** before running, predict at what relative gap between $\tau_1$ and $\tau_2$ the direct formula loses accuracy.
6. **Part 5:** from the repository root, run `python tools/run_spice.py 01-04`. Then change `RS1` to 25 Ω and predict the new optimum and maximum power before re-running.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | penalty for a 2× error | max power −11.1% (both sides); repeaters +25.0% (both sides); minimum energy +41.7% (V/2) and +66.7% (2V) |
| 2 | Monte Carlo standard deviation | 2.95%, close to the uniform-distribution value $\sqrt{(1^2 + 5^2)/3} = 2.94\%$ |
| 2 | Monte Carlo 99.73% interval | about −5.5% to +6.1%, near the exact worst case (−5.70%, +6.33%), because one uniform term dominates |
| 3 | Newton digits for √2 | about 1, 2, 5, 11, then full precision |
| 3 | arctan convergence region | $\lvert x_0\rvert < 1.39$ |
| 4 | best relative gap | about $10^{-8}$; smaller gaps lose accuracy to cancellation (error $10^{-3}$ at $10^{-14}$) |
| 5 | ngspice optimum | 50 Ω, 0.5 W; 0.4444 W at 100 Ω; 2 kΩ, 125 µW for the sensor. With $R_s = 25\ \Omega$: 25 Ω, 1 W |

The penalties in Part 1 differ because the optima differ in curvature (§3.2). Maximum power transfer is symmetric in $\ln R_L$: $P(R_s/2) = P(2R_s)$. The stylized energy curve is asymmetric: a factor-of-2 error costs 41.7% below the optimum and 66.7% above it, so per factor of 2 it rises more steeply *above* the optimum (though more steeply per volt below it).

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-04.a | max-power penalty at a 2× load error | 11.1 | % |
| Lab 01-04.b | repeater-delay penalty at a 2× count error | 25.0 | % |
| Lab 01-04.c | uniform-distribution standard deviation | 2.94 | % |
| Lab 01-04.d | max power with R_s = 25 Ω | 1 | W |
| Lab 01-04.e | min-energy penalty at V*/2 | 41.7 | % |
| Lab 01-04.f | min-energy penalty at 2V* | 66.7 | % |
| Lab 01-04.g | RSS of the tolerance limits | 5.10 | % |

## Discussion questions

1. A design review proposes spending money to hold the repeater count exactly at its optimum. Using Part 1, how would you respond?
2. In Part 2, when is worst-case analysis the right choice despite its pessimism?
3. In Part 4, why does making $\tau_2$ *closer* to $\tau_1$ eventually make the answer *worse*? How does the L'Hôpital form avoid the problem?

## Optional hardware version

With a 9 V battery, a 100 Ω resistor as the "internal resistance", a set of load resistors (22 Ω to 470 Ω) and a multimeter: measure the load voltage for each load, compute $P = V^2/R_L$, and plot it against $R_L$ on a log axis. The peak should sit near 100 Ω (allowing for the battery's own internal resistance, a few ohms), and the curve should look symmetric on the log axis.
