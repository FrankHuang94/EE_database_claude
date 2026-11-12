# Lab 01-08 · Sequences, Series and Taylor Expansions

**Chapter:** [01-08](../../chapters/01-08-sequences-series-and-taylor.md) · **Notebook:** [01-08-series.ipynb](01-08-series.ipynb) · **Netlists:** [diode_hd.cir](diode_hd.cir), [opamp_gain_error.cir](opamp_gain_error.cir) · **Time:** about 60 minutes

## Objective

1. Compare actual Taylor-series errors with Lagrange bounds, and see how the argument affects the number of terms needed.
2. Compare a slowly and a quickly converging series for the same number (π).
3. Measure the harmonic distortion of an exponential device and a cubic amplifier with an FFT, and compare it with Taylor and exact (Bessel) predictions.
4. Confirm in ngspice a diode model's distortion and a feedback amplifier's gain error.

## Background

Chapter sections 3.2–3.6 (series, convergence, Taylor's theorem), 3.7 (approximations and feedback gain error) and 3.8 (distortion from Taylor coefficients).

## Procedure

1. Run all notebook cells in order.
2. **Part 1:** note how the required degree grows with $\lvert x\rvert$.
3. **Part 2:** before running, predict how many Leibniz and Machin terms give 6 correct decimals.
4. **Part 3:** before running, predict HD2 of the exponential device at 3 mV and HD3 of the cubic at 1 V.
5. **Part 4:** from the repository root, run `python tools/run_spice.py 01-08`. Then change the open-loop gain of `E1` to $10^4$, predict the new gain error, and re-run.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | degree for 10⁻⁶ at x = 0.5, 1, 3 | 7, 9, 16 |
| 2 | Leibniz terms for about 10⁻⁶; Machin terms each | about 2,000,000; 5 (error 3×10⁻⁸) |
| 3 | exponential HD2 at 1, 3, 10 mV | 0.967%, 2.900%, 9.611% (Taylor overstates by 0%, 0.06%, 0.6%) |
| 3 | cubic at 1 V: fundamental, HD3 | 0.9625 V, 1.299%; −1.00 dB gain at 1.7 V (the 1 dB compression point) |
| 4 | ngspice diode HD2 at 1 mV and 3 mV; HD3 at 1 mV | 0.967%, 2.900%; 0.00623% |
| 4 | amplifier gains | 99.90 (error −0.0999%), 10.99940 (55.0 ppm), 10.8803 (1.088%) |
| 4 | with $A = 10^4$ and ideal gain 100 | error ≈ $1/(A\beta)$ = 1%, gain ≈ 99.01 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-08.a | exponential HD2 at 3 mV | 2.900 | % |
| Lab 01-08.b | cubic gain at 1.7 V | −1.00 | dB |
| Lab 01-08.c | gain with A = 1e4, ideal 100 | 99.01 | — |

## Discussion questions

1. In Part 3, why does the cubic amplifier produce no second harmonic, while the exponential device does?
2. The differential version in "Your turn" cancels HD2. Which Taylor coefficients survive in an odd function such as $e^{x/2} - e^{-x/2} = 2\sinh(x/2)$?
3. Part 1 shows $e^{-3}$ needing as many terms as $e^{3}$. Why is computing $e^{-30}$ from its series a bad idea in floating point?

## Optional hardware version

With a function generator, an oscilloscope with FFT, a 1N4148 diode, 8.2 kΩ and 10 kΩ resistors, a 10 µF coupling capacitor and a 9 V battery: bias the diode at about 1 mA (9 V through 8.2 kΩ), and add a 1 kHz signal through a coupling capacitor and a 10 kΩ resistor. The diode's small-signal resistance is about 26 Ω, so each volt of generator amplitude puts about 2.6 mV across the diode. Watch the second harmonic in the FFT of the diode voltage grow by about 6 dB each time you double the signal amplitude, the 20 dB-per-decade slope of HD2.
