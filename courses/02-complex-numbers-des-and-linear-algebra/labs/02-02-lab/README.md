# Lab 02-02 · First-Order Linear ODEs

**Chapter:** [02-02](../../chapters/02-02-first-order-linear-odes.md) · **Notebook:** [02-02-first-order-odes.ipynb](02-02-first-order-odes.ipynb) · **Netlists:** [rc_inputs.cir](rc_inputs.cir), [thermal_rc.cir](thermal_rc.cir), [thermal_runaway.cir](thermal_runaway.cir) · **Time:** about 75 minutes

## Objective

1. Read direction fields, and see a smooth equation blow up in finite time.
2. Compare forward Euler, backward Euler and the trapezoidal rule for stability and accuracy.
3. See how little early S-curve data reveal about saturation.
4. Explore thermal runaway: stable and unstable equilibria, and the critical thermal resistance.
5. Confirm the ramp, sinusoid and thermal results of the chapter in ngspice.

## Background

Chapter sections 3.2 (equilibria and stability), 3.3 (the logistic equation), 3.6 (standard inputs), 3.7 (existence and blow-up), 3.9 (Euler's method) and 3.10 (the thermal model), and Examples 02-02.3 to 02-02.5.

## Procedure

1. Run all notebook cells in order. Before each cell marked **🔮 Predict**, write down your prediction.
2. **Part 1:** predict where $y' = y^2$, $y(0) = 1$, goes and when.
3. **Part 2:** predict which methods survive a step of $3\tau$; then compare the error ratios when the step halves.
4. **Part 3:** predict how well three years of adoption data determine the capacity $K$.
5. **Part 4:** predict whether the chip recovers from 120 °C and from 130 °C at $R_{th} = 0.25$ K/W.
6. **Part 5:** from the repository root, run `python tools/run_spice.py 02-02`. Then edit `thermal_rc.cir` to set `RT1` to 0.32 Ω (K/W), predict the final temperature, and re-run. (The notebook's Part 4 gives the answer for comparison.)

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | $y' = y^2$, $y(0) = 1$ | blows up at $t = 1$; the solver stops just before |
| 2 | forward Euler at $h = 3\tau$ | grows by a factor −2 per step: unstable |
| 2 | backward Euler and trapezoid at $h = 3\tau$ | stable (factors 0.25 and −0.2 per step) |
| 2 | error ratio when $h$ halves | about 2 for both Euler methods (first order), 4 for the trapezoid (second order) |
| 3 | capacity fitted from 3 years | far from the true 200 million, with an error bar that does not cover it |
| 3 | capacity fitted from 10 years | close to 200 million |
| 4 | $R_{th} = 0.25$ K/W from 35 °C and from 120 °C | settles at 64.25 °C |
| 4 | $R_{th} = 0.25$ K/W from 130 °C | runs away past 300 °C in about 14.4 s |
| 4 | $R_{th} = 0.32$ K/W | settles slowly (local time constant about 55.7 s) toward 81.98 °C; reads 81.90 °C at 300 s |
| 4 | $R_{th} = 0.40$ K/W | runs away: crosses 150 °C at about 101.2 s |
| 5 | `rc_inputs.cir` | ramp error 99.33 mV at 1 ms; cosine amplitude 0.4472 V; RL current amplitude 0.3033 A |
| 5 | `thermal_rc.cir`, `thermal_runaway.cir` | 64.25 °C at 300 s; 150 °C crossed at 101.2 s |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 02-02.a | forward-Euler factor per step at h = 3τ | −2 | — |
| Lab 02-02.b | trapezoidal factor per step at h = 3τ | −0.2 | — |
| Lab 02-02.c | time to cross 150 °C at 0.40 K/W | 101.2 | s |
| Lab 02-02.d | time to run away past 300 °C from 130 °C at 0.25 K/W | 14.4 | s |
| Lab 02-02.e | temperature at 300 s, 0.32 K/W | 81.90 | °C |
| Lab 02-02.g | equilibrium at 0.32 K/W | 81.98 | °C |
| Lab 02-02.h | local time constant at 0.32 K/W | 55.7 | s |
| Lab 02-02.f | backward-Euler factor per step at h = 3τ | 0.25 | — |

## Discussion questions

1. The trapezoidal rule is stable for every step, yet its factor approaches −1 for very large steps. What does that do to a stiff circuit's fast, already-decayed components, and why do simulators sometimes switch to backward Euler?
2. In Part 3, why does the fit report a small error bar when the estimate is badly wrong? What would you ask a startup that projects a market size from two years of growth data?
3. In Part 4, the response becomes very slow near the critical thermal resistance. How could you use that slowing as an early warning in a product's thermal measurements?

## Optional hardware version

With a 10 kΩ resistor, a 100 µF electrolytic capacitor (τ = 1 s), a function generator and an oscilloscope (or a microcontroller's ADC): drive the RC with a slow triangle wave of 0.1 Hz and 1 V peak, and measure the output. On each ramp, after a few seconds, the output runs parallel to the input, lagging by about 1 s, so the error is the slope times τ. Then drive it with a 0.16 Hz sine ($\omega\tau \approx 1$) and confirm a 0.71 amplitude ratio and a 45° lag.
