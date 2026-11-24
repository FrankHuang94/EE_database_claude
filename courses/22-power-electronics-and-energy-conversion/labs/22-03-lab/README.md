# Lab 22-03 · Boost, Buck-Boost and SEPIC: Ratios, Ripple, the Gain Limit and Light Load

Chapter: [22-03 · Boost, Buck-Boost and Other Topologies](../../chapters/22-03-boost-buck-boost-topologies.md)

## Objective

- Confirm the boost's ratio, inductor ripple and pulsed-output ripple in ngspice.
- See the winding resistance cap a boost's gain, and find the duty cycle beyond which more duty gives less output.
- Build a SEPIC and confirm that its coupling capacitor averages the input voltage.
- Map the boost's CCM–DCM boundary and its load-dependent ratio at light load.

## Background

`topologies.py` collects the chapter's results:

- CCM ratios and duty cycles: `ratio`, `boost_duty`, `buck_boost_duty`;
- boost currents and ripples: `boost_inductor_current`, `boost_ripple_current`, `boost_output_ripple`, `boost_cout_rms`, `boost_rhp_zero_hz`;
- the boost with winding resistance: `boost_ratio_with_rl`, `boost_efficiency_with_rl`, `boost_max_gain`;
- boost DCM: `boost_k_crit`, `boost_dcm_ratio`, `boost_ratio_any`;
- an averaged SEPIC with winding resistances, `sepic_dc`, which solves its four balance equations for output voltage, coupling-capacitor voltage and both inductor currents;
- `switch_stress`.

The two netlists:

- `boost.cir` builds Example 22-03.1's synchronous boost (3.6 V to 5 V, 1 MHz) and a normalized boost with a 0.1 Ω winding into 25 Ω at $D$ = 0.8 and 0.9. With a 1 V input, the latter's outputs are the conversion ratios themselves. The initial conditions are set at the predicted steady state because the boost's LC is lightly damped.
- `sepic.cir` builds a synchronous SEPIC from 12 V at $D$ = 0.5 into 6 Ω. Its inductors have 50 mΩ windings, which damp the slow resonance between the coupling capacitor and the inductors.

## Procedure

1. **The boost.** *Predict* the output, inductor ripple and output ripple of Example 22-03.1, then run `ngspice -b boost.cir` (Part 1).
2. **The gain limit.** *Predict* the gain at $D$ = 0.8 and 0.9 with $R_L/R$ = 0.004, and the duty cycle where the gain peaks. Compare with ngspice, then sweep $D$ from 0 to 0.99 in the notebook (Part 2).
3. **The SEPIC.** *Predict* the output and the coupling capacitor's average voltage, with and without the windings, then run `sepic.cir` (Part 3).
4. **Light load.** *Predict* the boost's open-loop output at 50 mA, then plot $K_{crit} = DD'^2$ and the ratio against $K$ at three duty cycles (Part 4).

## Expected results

- **Part 1.** ngspice gives 5.00 V, 1.008 A of inductor ripple and 19.1 mV of output ripple, as Example 22-03.1 predicts.
- **Part 2.** The outputs are 4.545 and 7.140 V, matching $M$ = 4.55 and 7.14. The gain peaks at 7.91 at $D$ = 0.937, where the efficiency is 50%.
- **Part 3.** The averaged model with 50 mΩ windings gives **11.80** V out and **12.00** V on the coupling capacitor, and ngspice agrees to 0.02%. Without the windings the output would be exactly 12 V; the windings cost 1.6%.
- **Part 4.** At 50 mA the boost is in DCM ($K$ = 0.02 against $K_{crit}$ = 0.145), and its open-loop output would rise to 9.15 V.

## Discussion

1. **Why must the initial conditions be set for the boost?** Its averaged output filter resonates at $D'/(2\pi\sqrt{LC})$ and is damped only by the load reflected through $D'$, so a cold start rings for many milliseconds. Starting near steady state lets a short simulation measure the steady state.
2. **Why does the coupling capacitor average exactly $V_{in}$?** Both inductors average zero volts in steady state. The loop from the input through $L_1$, $C_1$ and $L_2$ to ground therefore puts the whole input across $C_1$ on average, plus the difference of the winding drops, which is zero here because the two inductor currents are equal.
3. **Why does the boost's gain fall beyond its peak?** The winding loss grows as $I_L^2 = (I/D')^2$, so near $D \to 1$ the extra inductor current wastes more power than the larger ratio gains.

## Optional hardware

A low-cost boost module (an adjustable 2–24 V type) and a power resistor show the gain limit: fix the load and raise the set-point. Beyond some point the output stops rising and the input current climbs steeply. Measuring input and output power there shows efficiency falling toward the 50% that §3.2 predicts at the peak.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-03.a | SEPIC output with 50 mΩ windings | 11.80 | V |
| Lab 22-03.b | SEPIC coupling-capacitor average | 12.00 | V |
