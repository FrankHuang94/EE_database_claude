# Lab 01-03 · Derivatives

**Chapter:** [01-03](../../chapters/01-03-derivatives.md) · **Notebook:** [01-03-derivatives.ipynb](01-03-derivatives.ipynb) · **Netlists:** [cap_ind.cir](cap_ind.cir), [diode_ac.cir](diode_ac.cir) · **Time:** about 60 minutes

## Objective

1. Watch secant slopes converge to a derivative, and confirm the differentiation rules symbolically.
2. Compare forward and central numerical derivatives and find each one's best step size.
3. Compute capacitor currents from sampled voltages, and confirm that $\int p\,dt = \tfrac{1}{2}Cv^2$.
4. Measure the accuracy of the diode's tangent-line (small-signal) model.
5. Confirm $i = C\,dv/dt$, $v = L\,di/dt$ and $r_d = V_T/I$ in ngspice.

## Background

Chapter sections 3.1–3.6 (definition and rules), 3.8 (circuit elements and small-signal conductance) and 3.9 (numerical differentiation).

## Procedure

1. Run all notebook cells in order.
2. **Part 2:** before running, predict the best step size and the number of correct digits for each method.
3. **Part 3:** confirm that the numerical current matches Problem 01-03.7 and that the energy curves coincide.
4. **Part 4:** before running, predict $r_d$ at 1 mA and 2 mA. Note how the linear model's error grows with the size of the voltage step.
5. **Part 5:** from the repository root, run `python tools/run_spice.py 01-03`. Then, in `cap_ind.cir`, change the inductor's turn-off ramp from 1 µs to 10 µs. Predict the new kick voltage before re-running.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 2 | best forward step and error | about $10^{-8}$, error about $10^{-8}$ (8 digits) |
| 2 | best central step and error | about $10^{-5}$, error about $10^{-11}$ (10–11 digits) |
| 3 | capacitor current | +50 mA, 0, −100 mA in the three segments; peak energy 0.5 mJ |
| 4 | $r_d$ at 1 mA and 2 mA | 25.85 Ω and 12.93 Ω |
| 4 | linear-model error for a 1, 5 and 20 mV step | about −2%, −9% and −34% (the tangent always underestimates the exponential) |
| 5 | inductor kick for a 1 µs ramp | −1000 V; with a 10 µs ramp, −100 V |

A useful rule from Part 4: the tangent-line model stays within 10% for steps up to about $0.2V_T$, roughly 5 mV.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-03.a | small-signal resistance at 2 mA | 12.93 | Ω |
| Lab 01-03.b | linear-model error for a 5 mV step | −9.4 | % |

## Discussion questions

1. In Part 3, the numerical current shows brief spikes at the corners of the voltage waveform. Where do they come from, and what would a real circuit show instead?
2. Why does the linear model always *underestimate* the diode's current change for a positive step, and *overestimate* its magnitude for a negative one?
3. A relay driver's datasheet recommends a flyback diode. Using Part 5, explain to a non-engineer what happens without one.

## Optional hardware version

With a function generator, a 1 kΩ resistor, a 100 nF capacitor and a two-channel oscilloscope: drive the RC series with a 1 kHz triangle wave, and look at the voltage across the 1 kΩ resistor. Because the RC time constant (0.1 ms) is much shorter than the period, most of the input voltage appears across the capacitor. The current is then approximately $C\,dv/dt$, and the resistor voltage approximately $RC\,dv/dt$: a square wave. You are watching a differentiator.
