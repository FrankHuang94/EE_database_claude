# Lab 15-12 · PLLs, Regulators and Thermal Management

Chapter: [15-12 Applications: PLLs, Voltage Regulators and Thermal Management](../../chapters/15-12-control-applications-pll-regulators-thermal.md)

## Objective

Apply the whole course to the three loops every chip runs on itself. You will design a charge-pump PLL's loop filter and check it in Python and in a phase-domain circuit; hop its frequency; choose its bandwidth for minimum jitter; find an LDO's ESR window; compare load-line and PI droop; and watch a thermal limiter turn a temperature limit into a falling power envelope.

## Background

Read §3 of the chapter. `loops.py` builds on the earlier labs: margins come from `labs/15-07-lab/freqdomain.py` and exact step and impulse responses from `labs/15-03-lab/specs.py`. The PLL functions use the phase-domain model of §3.1 and the maximum-margin design of §3.2; the LDO model is §3.3's; the droop model is §3.4's transconductance regulator; and `throttle` simulates the two-node thermal model of 15-01 under the ACPI-style velocity-form PI of §3.6, exactly between samples.

## Files

- [loops.py](loops.py): `pll_design`, `pll_loop`, `closed`, `peaking`, `bw3db`, `phase_error_peak`, `jitter`, `ldo_loop`, `ldo_pm`, `esr_window`, `droop`, `two_node` and `throttle`.
- [15-12-applications-lab.ipynb](15-12-applications-lab.ipynb): the notebook (Parts 1–6).
- [pll_phase.cir](pll_phase.cir): Example 15-12.2's PLL as a phase-domain circuit (node voltages are phases), measuring the closed-loop peak and bandwidth.
- [ldo_esr.cir](ldo_esr.cir): Example 15-12.6's LDO with a 0.3 Ω ESR, measuring crossover and phase margin with the loop broken at the error amplifier's input.

## Procedure

1. **Design the PLL (Part 1).** Run `pll_design` for Example 15-12.2, plot the Bode diagram of $L$, and confirm the 60° margin at 200 kHz. Then round the components to $R$ = 13.5 kΩ, $C$ = 220 pF and $C_2$ = 17 pF and recompute the margin. *Predict first:* does rounding to standard values matter?
2. **Close the loop and hop (Part 2).** Compare the closed-loop poles with §3.2's factorization; step the divider from 100 to 101 and measure overshoot, settling within 1 kHz and the PFD's peak phase error. Run `pll_phase.cir` and compare its peak and −3 dB bandwidth with Python.
3. **Choose the bandwidth (Part 3).** Plot integrated jitter against $f_c$ for Example 15-12.5 and mark the noise crossing.
4. **Sweep the ESR (Part 4).** Plot phase margin against $R_{ESR}$ from 1 mΩ to 10 Ω for Example 15-12.6, mark the 45° window, and run `ldo_esr.cir`. *Predict first:* what happens with a 5 mΩ ceramic capacitor?
5. **Droop (Part 5).** Plot the load-line and critically damped PI responses of Example 15-12.4 on one graph.
6. **Throttle (Part 6).** Simulate Example 15-12.7, overlay $130 + 70e^{-t'/31.5}$ W, and repeat with $K_p$ and $K_i$ halved and doubled.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Margin with exact components | 60.0° at 200 kHz |
| 1 | Margin with rounded components | about 60.0° at about 199.5 kHz (keys below) |
| 2 | Hop | 18.9% overshoot, 17.3 µs to 1 kHz, 0.412 rad PFD error |
| 2 | ngspice | 1.70 dB peak at 93.1 kHz, −3 dB at 313 kHz |
| 3 | Jitter | minimum about 413 fs near 316 kHz |
| 4 | ESR window | 0.094–0.568 Ω; 54.3° at 0.3 Ω in Python and ngspice |
| 5 | Droop | load line flat at −40 mV; PI (ω0 = g/C at 58.5 kHz, crossover 60.3 kHz) peaks at −40 mV at 5.44 µs and recovers |
| 6 | Throttling | power falls from 200 W at about 75 s toward 130 W; nearly identical curves for the other gains |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-12.a | phase margin with rounded components | 60.0 | ° |
| Lab 15-12.b | crossover with rounded components | 199.5 | kHz |

## Discussion

1. Why does rounding the loop-filter components to standard values change the margin so little?
2. Why do the PLL's closed-loop poles stay real while the frequency hop overshoots by 19%?
3. In Part 3, why is the jitter curve nearly symmetric about the optimum on a logarithmic axis?
4. In Part 4, why does too much ESR reduce the margin?
5. In Part 6, why do halving and doubling the PI gains barely change the power envelope?

### Answers

1. The margin depends on the ratio $b = \tau_z/\tau_p$ and on where crossover sits relative to $1/\sqrt{\tau_z\tau_p}$; near the peak of the phase curve the phase is flat, so small shifts of crossover or of the time constants change it only to second order. The rounded values move crossover by 0.2% and the margin by hundredths of a degree.
2. The overshoot comes from the loop filter's zero at $\omega_c/\sqrt b$, which is slower than all three poles; a slow zero adds a derivative-like term to the step response (15-03).
3. For a maximum-margin loop, $\lvert T(j\omega_c^2/\omega)\rvert = \lvert S(j\omega)\rvert$: the low-pass and high-pass shapes are mirror images about $\omega_c$, and with the noise crossing at the optimum the two noise shapes nearly mirror each other too.
4. The ESR zero moves to lower frequency, the gain flattens, and crossover moves up toward the 1 MHz gate pole, whose phase lag then takes the margin away.
5. The loop is fast compared with the heat sink: any of these gains holds the junction at its limit within a fraction of a kelvin, and the envelope is then set by the heat sink's time constant, not by the controller.

## Optional hardware

With a function generator, a 74HC4046-type PLL chip (phase-frequency detector and VCO in one package) and a passive loop filter, build a ×N synthesizer with a counter IC as the divider; switch $N$ and watch the VCO control voltage on an oscilloscope to measure the hop overshoot and settling. Compare with `phase_error_peak` and the step response for your measured $K_v$.
