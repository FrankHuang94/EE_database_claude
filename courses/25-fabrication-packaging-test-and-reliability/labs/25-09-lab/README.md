# Lab 25-09 · Extrapolating Reliability: TDDB Models, Weibull Scaling, HTOL and ESD

**Objective.** Fit three breakdown models to the same stress data and see where they diverge, scale test-capacitor lives to chips and ppm targets, find out what a 60% confidence FIT bound really promises, and simulate an ESD discharge into a pad clamp in ngspice.

**Chapter:** [25-09 · Reliability Physics](../../chapters/25-09-reliability-physics.md)

## Background

§3.3 gave the E, 1/E and power-law TDDB models and the weakest-link scaling $t_F = \eta(A_{chip}/A_{test})^{-1/\beta}(-\ln(1 - F))^{1/\beta}$. §3.6 gave the HTOL bound $\lambda_U = \chi^2_{CL,\,2f+2}/(2NtAF)$. §3.5 gave the HBM clamp equations $I_{pk} = (V_0 - V_h)/(R_{HBM} + R_{on})$ and $V_{pad} = V_h + I_{pk}R_{on}$.

## Files

- `reliability.py`: Arrhenius and Black acceleration, the two-phase EM exponent, the Blech length, TDDB fits, Weibull scaling, BTI extrapolation, the HBM clamp, HTOL FIT bounds with a Monte Carlo check, and sums of mechanisms.
- `hbm_esd.cir`: ngspice netlist of a 2 kV HBM discharge into a 5 V, 1 Ω clamp, with `EXPECT` lines tied to Example 25-09.7.
- `25-09-reliability-lab.ipynb`: the notebook for Parts 1 to 3.

## Procedure

**Part 1 · Diverging models** (notebook). Fit the three models through Example 25-09.4's points, *predict* the field at which the E and power-law extrapolations differ by a factor of 1,000, then find it and plot all three against field.

**Part 2 · Weibull slope** (notebook). *Predict* how the 100 ppm scale factor of Example 25-09.5 changes when β falls from 2 to 1.2, then compute it and plot it against β.

**Part 3 · What 60% means** (notebook). Simulate many zero-failure HTOL runs of TI's test for a product whose true rate equals the 60% bound. *Predict* the pass fraction, then count it.

**Part 4 · ESD in ngspice** (netlist). Run `ngspice -b hbm_esd.cir` and compare its peak current, peak pad voltage and current at one time constant with Example 25-09.7. Then *predict* the peak pad voltage with a 2 Ω clamp, change `Ron`, and rerun.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-09.a | field where E and power law differ 1,000-fold | 3.79 | MV/cm |
| Lab 25-09.b | 100 ppm scale factor at beta 1.2 | 1.47e-6 | |
| Lab 25-09.c | zero-failure pass fraction at the bound | 0.40 | |
| Lab 25-09.d | peak pad voltage, 2 ohm clamp | 7.66 | V |

The simulated pass fraction (200,000 runs) agrees with $e^{-\chi^2/2}$ = 0.40 within 0.005, and ngspice reproduces Example 25-09.7's peak current, peak pad voltage and current at one time constant within 0.4%.

## Discussion

1. In Part 1, the models agree perfectly at the stress points. What kind of data would discriminate between them, and why is it expensive to collect?
2. Part 2 shows the scale factor is very sensitive to β. What physical property of thin oxides makes β small?
3. Part 3: a vendor quotes 2 FIT "at 60% confidence". What would you ask before using that number in a system reliability budget?
4. Part 4's clamp is linear. Real snapback clamps trigger at a higher voltage before settling to their holding voltage; how would that change the peak pad voltage, and what does CDM's faster edge add?

## Optional hardware

None needed. Published failure-analysis images (for example in IRPS proceedings) of electromigration voids and oxide breakdown spots show the physical damage these models describe.
