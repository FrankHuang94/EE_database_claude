# Lab 22-08 · Power Management: DVS Ramps, Soft Start, Light-Load Modes and Battery Budgets

Chapter: [22-08 · PMICs and Power Management for SoCs](../../chapters/22-08-pmics.md)

## Objective

- Ramp the reference of Example 22-07.3's closed-loop buck and measure how far the output leads it.
- Switch on a power domain hard and with soft start, and show that the switch dissipates $\tfrac12CV^2$ either way.
- Plot PWM and PFM efficiency against load and locate the crossover.
- Build a usage-profile battery budget and find which state dominates it.
- See how temperature moves the power-gating break-even time.

## Background

`pmic.py` collects the chapter's results:

- rails: `ldo_efficiency`, `chain_efficiency`;
- light load: `pwm_loss`, `pfm_loss`, `pfm_pwm_crossover`, `efficiency`;
- battery life: `daily_energy`, `battery_energy`;
- voltage changes: `dvs_ramp`, `pfm_down_time`, `ramp_lead`, `avs_ratio`;
- switching domains: `soft_start`, `sequence_time`, `leakage_at`, `gating_breakeven`.

The two netlists:

- `dvs.cir` is Example 22-07.3's averaged voltage-mode buck (1.2 V from 12 V, 60 kHz crossover) with its type-III network around a high-gain op-amp whose non-inverting input carries the reference. The reference starts at 1.0 V and ramps to 1.2 V over 1 ms, a slew of 0.2 mV/µs. The netlist records the error $v_{out} - v_{ref}$ half-way through the ramp.
- `softstart.cir` charges two copies of a 1.0 V, 100 µF domain: one through a 0.1 Ω switch, the other through a switch that limits the current to 0.1 A until the domain is nearly charged. It integrates the power dissipated in each switch.

## Procedure

1. **DVS ramp tracking.** *Predict* the steady lead from $e = (S/\omega_I)(1 - V_M/V_g)$ with $\omega_I$ = 8396 rad/s, $V_M$ = 1 V and $V_g$ = 12 V. Run `ngspice -b dvs.cir` (Part 1). In the notebook, repeat at 1 mV/µs and compare with Problem 22-08.8.
2. **Soft start.** *Predict* the energy dissipated in each switch, the two peak currents and the time for the soft-started domain to reach 0.99 V. Run `ngspice -b softstart.cir` (Part 2).
3. **Light-load modes.** *Predict* which mode is more efficient at 1 mA and at 300 mA for Example 22-08.2's buck. Plot both efficiency curves from 10 µA to 1 A (Part 3).
4. **The battery budget.** *Predict* which state of Example 22-08.3's fitness band dominates its daily energy. Rebuild the budget, then halve the sleep power, the quiescent current and the active-state losses in turn, and compare the battery-life gains (Part 4).
5. **Gating when hot.** *Predict* how Problem 22-08.11's break-even time changes from 25 °C to 85 °C. Plot it against temperature (Part 5).

## Expected results

- **Part 1.** The output leads the reference by **21.8** mV during the ramp and settles at 1.200 V once the ramp ends. At 1 mV/µs the lead grows fivefold, to 109 mV. The output runs *ahead* because the reference also reaches the modulator directly through the op-amp's non-inverting input.
- **Part 2.** Both switches dissipate 50 µJ, which is $\tfrac12CV^2$ (Example 22-08.6). The hard switch draws a 10 A peak; the soft-started one 0.1 A, and it takes **0.99** ms to reach 0.99 V. Soft start trades time for peak current, not energy.
- **Part 3.** PFM is far ahead at 1 mA (93.5% against 8.3%), PWM ahead at 300 mA (93.4% against 85.7%); the curves cross at 119 mA.
- **Part 4.** The 55 active minutes and 5 display minutes take **95.1** % of the 111.8 J daily energy, and the band lasts 37.2 days. Halving the sleep power extends the life to **38.1** days and halving the PMIC's quiescent current to only **37.26** days, while halving the converter losses in the active and display states (for example, 88% becoming 93.6% efficient) extends it to **39.3** days.
- **Part 5.** The break-even time falls from 264 µs at 25 °C to 50.0 µs at 85 °C, as leakage rises fivefold.

## Discussion

1. **Why can soft start not save energy?** Whatever the current profile, the switch carries the charge $CV$ while the voltage across it falls from $V$ to zero. The integral $\int (V - v)\,C\,dv$ does not depend on time. Only a source whose voltage itself ramps (an adiabatic or resonant charger) can do better.
2. **Why does the output lead rather than lag?** In a unity-feedback loop with an integrator, a ramp produces a lag. Here the reference also passes through the op-amp's non-inverting input to the modulator, so the forward path receives the ramp directly and pushes the output ahead. A transconductance error amplifier with its compensation to ground does not have this path and lags instead.
3. **Why does halving the quiescent current barely help the band?** Its standing draw is 0.333 J of 111.8 J per day. The answer would change for a device that sleeps at a few microwatts (Problem 22-08.4).

## Optional hardware

A PMIC or buck evaluation board with programmable output voltage (through I²C or a resistor DAC) shows DVS directly. Program a step, watch $v_{out}$ and the inductor current on an oscilloscope with a current probe, and change the slew-rate register: the extra inductor current during the ramp should be $C\,S$. Switch a load switch's evaluation board into a large capacitor with and without its soft-start capacitor and compare the inrush current peaks.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-08.a | output lead during a 0.2 mV/µs ramp | 21.8 | mV |
| Lab 22-08.b | soft-start time to 0.99 V | 0.99 | ms |
| Lab 22-08.c | daily-energy share of active and display states | 95.1 | % |
| Lab 22-08.d | battery life with halved sleep power | 38.1 | days |
| Lab 22-08.e | battery life with halved quiescent current | 37.26 | days |
| Lab 22-08.f | battery life with halved active-state losses | 39.3 | days |
