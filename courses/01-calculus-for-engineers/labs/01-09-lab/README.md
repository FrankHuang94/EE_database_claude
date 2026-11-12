# Lab 01-09 · Multivariable Calculus I

**Chapter:** [01-09](../../chapters/01-09-multivariable-calculus-1.md) · **Notebook:** [01-09-multivariable.ipynb](01-09-multivariable.ipynb) · **Netlist:** [mosfet_tempco.cir](mosfet_tempco.cir) · **Time:** about 60 minutes

## Objective

1. Compute a MOSFET's partial derivatives symbolically and numerically.
2. See how the condition number limits gradient descent.
3. Check Lagrange-multiplier solutions (heterogeneous cores, water-filling) against a numerical constrained optimizer.
4. Read $g_m$ and $g_{ds}$ from a SPICE operating point, and measure a junction's temperature coefficient by sweeping temperature.

## Background

Chapter sections 3.2–3.4 (partial derivatives, small-signal models, implicit differentiation), 3.5 (gradient descent) and 3.7 (Lagrange multipliers).

## Procedure

1. Run all notebook cells in order.
2. **Part 1:** compare the symbolic and numerical partial derivatives.
3. **Part 2:** before running, predict the largest stable step size for $f = x^2 + 10y^2$, and how many steps the best fixed step needs.
4. **Part 3:** compare the optimizer's answers with the closed forms.
5. **Part 4:** from the repository root, run `python tools/run_spice.py 01-09`. Then change the diode current `I1` to 10 µA, predict $dV/dT$ before re-running, and explain the change.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $I_D$, $g_m$, $g_o$ | 99.00 µA, 0.6600 mS, 9.000 µS (symbolic and numerical agree) |
| 2 | stability limits for curvature ratios 1, 10, 100 | η < 1, 0.1, 0.01 |
| 2 | best steps to $f < 10^{-6}$ for ratios 10 and 100 | about 36 and about 348: roughly proportional to the condition number |
| 3 | three-core split and power | 1.855, 0.927, 0.618 GHz; 1.169 W |
| 3 | water-filling at 6 mW and at 1 mW | (4, 2) mW, 3.059 b/s/Hz; (1, 0) mW, 1 b/s/Hz |
| 4 | ngspice $g_m$, $g_{ds}$, diode V and dV/dT | 0.66 mS, 9 µS, 0.6548 V, −1.809 mV/K |
| 4 | with 10 µA | $V$ falls by $2V_T\ln10 = 0.119$ V, so dV/dT steepens by $0.119/300$ = −0.40 mV/K, to about −2.21 mV/K |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-09.a | gradient-descent stability limit, curvature ratio 100 | 0.01 | — |
| Lab 01-09.b | diode dV/dT at 10 µA | −2.21 | mV/K |

## Discussion questions

1. Why does the temperature coefficient become *more* negative at lower bias current?
2. The numerical optimizer and the Lagrange solution agree. When would you trust the optimizer *more* than a closed form? When *less*?
3. In machine-learning terms, what does "ill-conditioned loss landscape" mean, and what is the cost in accelerator hours?

## Optional hardware version

With a multimeter, a 1N4148 diode, a 9 V battery, a 10 kΩ resistor (about 0.8 mA) and a hair dryer or a cup of warm water (with the diode in a sealed plastic bag): measure the diode voltage at room temperature and when warmed, using a kitchen thermometer for the temperature. The voltage should fall by roughly 2 mV per °C. Never heat components beyond their ratings.
