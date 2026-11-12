# Lab 01-07 · Applications of Integration

**Chapter:** [01-07](../../chapters/01-07-applications-of-integration.md) · **Notebook:** [01-07-applications.ipynb](01-07-applications.ipynb) · **Netlist:** [rms_power.cir](rms_power.cir) · **Time:** about 60 minutes

## Objective

1. Compute average, RMS and crest factor for common and distorted waveforms, and see where average-responding meters go wrong.
2. Confirm the quantization-noise variance Δ²/12 and the ideal ADC SNR of 6.02N + 1.76 dB by simulation.
3. Check exponential-lifetime and Gaussian-yield integrals against simulated populations.
4. Measure RMS values and average AC power in ngspice.

## Background

Chapter sections 3.1–3.2 (RMS and average power), 3.5 (probability densities) and 3.6 (quantization noise and ADC SNR).

## Procedure

1. Run all notebook cells in order.
2. **Part 1:** compare the average-responding meter with the true RMS for each waveform. (The meter model here rectifies the whole signal, DC included. Real meters on their AC range block the DC first.)
3. **Part 2:** before running, predict the SNR of a 10-bit quantizer driven at half of full scale.
4. **Part 3:** compare the simulated fractions with the integrals.
5. **Part 4:** from the repository root, run `python tools/run_spice.py 01-07`. Then change the load so that its angle becomes 60° while $\lvert Z\rvert$ stays 17 Ω: set `R3` to $17\cos60° = 8.5\ \Omega$ and `L3` to $17\sin60°/(2\pi\cdot60) = 39.05$ mH. Predict the new average power, and re-run. (If you change `L3` alone, $\lvert Z\rvert$ grows as well, the current falls, and the power drops much further, to 245.4 W. Predict that case too.)

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | average-responding error: square, triangle, rectifier-like pulses | +11.1%, −3.8%, −40.5% |
| 2 | measured SNR, 8 to 14 bits at full scale | within about 0.1 dB of 6.02N + 1.76 |
| 2 | error standard deviation | about 0.289 LSB ($1/\sqrt{12}$) |
| 2 | 10 bits at half scale | about 56 dB: 6.02 dB below full scale, since the signal is 6 dB smaller and the noise unchanged |
| 3 | 720 h survival and ±1% yield | 0.866 and 0.955, matching the integrals |
| 4 | PWM average and RMS; triangle RMS | 3.000 V and 6.000 V; 0.5774 V |
| 4 | R–L load: average power and RMS current | 736.1 W and 7.071 A |
| 4 | with a 60° load angle ($\lvert Z\rvert$ = 17 Ω: R3 = 8.5 Ω, L3 = 39.05 mH) | ½ × 170 × 10 × cos 60° = 425 W |
| 4 | with only L3 changed (R3 = 14.722 Ω, X = 25.50 Ω, $\lvert Z\rvert$ = 29.44 Ω) | $V_{rms}^2R/\lvert Z\rvert^2$ = 245.4 W |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-07.a | RMS current of the R–L load | 7.071 | A |
| Lab 01-07.b | ideal SNR, 10 bits at half scale | 55.94 | dB |
| Lab 01-07.c | average-responding error, rectifier-like pulses | −40.5 | % |
| Lab 01-07.d | average power at a 60° load angle | 425 | W |
| Lab 01-07.e | L3 for 60° at 17 Ω | 39.05 | mH |
| Lab 01-07.f | reactance with only L3 changed | 25.50 | Ω |
| Lab 01-07.g | impedance with only L3 changed | 29.44 | Ω |
| Lab 01-07.h | power with only L3 changed | 245.4 | W |

## Discussion questions

1. Why do average-responding meters under-read peaky waveforms such as rectifier currents, and over-read flat-topped ones such as square waves?
2. Part 2 assumes a "busy" input. What happens to the uniform-error model for a DC input, or for a very slow ramp? (Hint: is the error still random?)
3. A supplier quotes MTBF = 5000 h for a server. Using Part 3, how many failures should a 200-server fleet expect per month?

## Optional hardware version

With an inexpensive average-responding multimeter, a true-RMS multimeter and a function generator: measure a 1 kHz sine, square and triangle wave of the same peak amplitude on both meters (AC voltage range). The meters should agree for the sine and differ by about +11% (square) and −4% (triangle), as computed in Part 1. Check that both meters' bandwidth covers 1 kHz first.
