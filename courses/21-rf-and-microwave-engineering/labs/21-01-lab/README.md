# Lab 21-01 · S-Parameters, Calibration and Stability

Chapter: [21-01 · S-Parameters and Network Analysis](../../chapters/21-01-s-parameters.md)

## Objective

- Compute reflection, return loss and VSWR, and S-parameters of simple two-ports, and confirm three of them with ngspice's S-parameter analysis.
- Convert between S, Z and ABCD, cascade networks and check reciprocity and losslessness.
- Calibrate a simulated reflectometer with short, open and load standards and watch the raw error disappear.
- Test a transistor for stability, draw its stability circle and stabilize it with a resistor.

## Background

`sparam.py` contains the one-port quantities (`gamma`, `return_loss_db`, `vswr`, `mismatch_loss_db`), the S-parameters of a series impedance, a shunt admittance and a line (`s_series`, `s_shunt`, `s_line`), conversions (`z_to_s`, `s_to_z`, `abcd_to_s`, `s_to_abcd`, `s_to_t`, `t_to_s`), `shift_planes`, the three-term calibration (`one_port_cal`, `one_port_correct`) and stability tools (`gamma_in`, `stability`, `stability_circle`). `sparams.cir` holds three independent two-ports in one six-port S-parameter analysis at 1 GHz: the series 10 Ω + 6.366 nH of Example 21-01.2, a 6 dB π attenuator built from standard resistors (150 Ω, 37.4 Ω, 150 Ω) and the 75 Ω eighth-wave line of Example 21-01.3.

## Procedure

1. **Reflections.** Tabulate Γ, return loss, VSWR and mismatch loss for loads from 10 Ω to 250 Ω (Part 1). *Predict* which loads give the same return loss.
2. **ngspice.** *Predict* the S-parameters of the three networks, then run `ngspice -b sparams.cir` (Part 2).
3. **Conversions and checks.** Convert Problem 5's Z-matrix to S and back; check reciprocity and the power sum; cascade two 3 dB pads and a line with T-matrices (Part 3).
4. **Calibration.** Simulate a reflectometer with the error terms of Example 21-01.5 and a little measurement noise; calibrate it with ideal standards and correct a sweep of device reflections (Part 4). *Predict* the raw error at the worst point.
5. **Stability.** For the 500 MHz data of Example 21-01.6, map $\lvert\Gamma_{in}\rvert$ over the load plane and overlay the stability circle; then sweep a shunt output resistor for Problem 11's transistor and find where μ reaches 1 (Part 5).

## Expected results

- **Part 1.** Loads a factor $k$ above and below 50 Ω (for example 100 Ω and 25 Ω) give the same $\lvert\Gamma\rvert$ and return loss.
- **Part 2.** ngspice reproduces Examples 21-01.2 and 21-01.3 to all printed digits; the attenuator built from standard resistors gives $S_{21}$ = **−6.01** dB and $S_{11}$ = **−67.0** dB, an excellent match despite the rounded values.
- **Part 3.** The round trip Z → S → Z returns the original matrix; the T-matrix cascade of two pads and a 60° line gives −6.00 dB at −60.0°.
- **Part 4.** Raw readings are off by tens of degrees in phase; after calibration the residual error is at the level of the added noise.
- **Part 5.** The region with $\lvert\Gamma_{in}\rvert > 1$ is the part of the unit disk inside the stability circle (centre 8.20∠77.7°, radius 7.70); a shunt output resistor of about 240 Ω brings μ to 1.

## Discussion

1. **Why do rounded resistor values still give an excellent attenuator?** The pad's match depends on ratios; a 0.3% error in the shunt arms (and 0.1% in the series arm) moves $S_{11}$ only to about −67 dB.
2. **Why must calibration standards be known?** The three unknown error terms are solved from the standards' assumed reflections; any error in those assumptions becomes an error in every corrected measurement.
3. **Why does stabilizing with a resistor cost gain?** The resistor dissipates power and lowers the available gain to the maximum stable gain or below; designers place it where it costs least at the operating frequency.

## Optional hardware

With a low-cost hobbyist vector network analyzer (a NanoVNA-class instrument), calibrate with its short, open and load standards and measure a 50 Ω load, a 100 Ω resistor and an SMA attenuator. Compare the attenuator's measured $S_{21}$ with its label, and observe how the reading changes if you calibrate at the instrument port and then add a cable.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-01.a | attenuator S21 | −6.01 | dB |
| Lab 21-01.b | attenuator S11 | −67.0 | dB |
