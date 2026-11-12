# Lab 01-01 · Functions, Models and Units

**Chapter:** [01-01](../../chapters/01-01-functions-models-and-units.md) · **Notebook:** [01-01-functions-and-models.ipynb](01-01-functions-and-models.ipynb) · **Time:** about 45 minutes

## Objective

1. See which function family becomes a straight line on linear, semilog and log–log axes.
2. Do decibel and dBm arithmetic in code, and cascade a gain chain.
3. Watch the diode's millivolts-per-decade slope change with temperature.
4. Fit power-law and exponential models to data, and see how noise scatters the fitted parameters.

## Background

Chapter sections 3.3–3.6 (power laws, exponentials, logarithms, decibels) and 3.8 (building models from data).

## Procedure

1. Run all cells in order.
2. **Part 1:** change `n` and `tau` and confirm that the power law stays straight on log–log axes and the exponential on semilog axes.
3. **Part 2:** before running, predict the output of the chain −40 dBm → +20 dB → −3 dB → +15 dB → −6 dB, in dBm and µW.
4. **Part 3:** before running, predict the millivolts per decade at 360 K.
5. **Part 4:** before running, predict how widely the fitted exponent scatters with 5% noise on five points.
6. Do the "Your turn" exercises at the end.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 2 | output power | −14 dBm = 39.81 µW |
| 3 | $V_T$ at 360 K | 31.02 mV |
| 3 | slope at 360 K | 71.43 mV/decade (up from 59.53 at 300 K, in proportion to $T$) |
| 4 | clean-data exponent | 2.99 |
| 4 | noisy fits (seed 1, 2000 trials) | mean ≈ 3.01, standard deviation ≈ 0.12; about 58% land within ±0.1 of 3, and essentially all within ±0.5 |

Five points with 5% noise pin the exponent down only to about ±0.1, which is enough to tell "square" from "cube" but not to resolve finer effects. More points, or points spread over a wider range of $V$, shrink the scatter.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-01.a | thermal voltage at 360 K | 31.02 | mV |
| Lab 01-01.b | diode slope at 360 K | 71.43 | mV/decade |
| Lab 01-01.c | chain output | −14 | dBm |
| Lab 01-01.d | chain output | 39.81 | µW |

## Discussion questions

1. Why does a semilog plot make an exponential straight but leave a power law curved? What would you plot to straighten a power law?
2. The noisy-fit histogram is roughly bell-shaped. Where have you seen the same thing in finance, for example when estimating a stock's beta from a few data points?
3. Part 3 held $I_s$ fixed. In a real diode $I_s$ rises steeply with temperature. Will the voltage at a fixed current go up or down as the diode warms? (Answer in [09-06](../../../09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md); the usual result is about −2 mV/K.)

## Optional hardware version

With a multimeter, a 1N4148 (or any small-signal silicon) diode, a 9 V battery and resistors of 1 MΩ, 100 kΩ, 10 kΩ and 1 kΩ: put each resistor in series with the diode across the battery, then measure the diode voltage and the resistor voltage (current = resistor voltage / R). Plot current on a log axis against diode voltage. You should see a nearly straight line of roughly 60 mV per decade (somewhat more for real diodes, whose ideality factor exceeds 1), bending at the highest current where series resistance matters.
