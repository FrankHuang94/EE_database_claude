# Lab 22-02 · The Buck Converter in Steady State: Ripple, RMS Currents, Losses and Discontinuous Conduction

Chapter: [22-02 · Steady-State Analysis and the Buck Converter](../../chapters/22-02-buck-converter-steady-state.md)

## Objective

- Confirm the buck's volt-second-balance ratio and the ripple formulas against the exact steady state and ngspice.
- Measure RMS currents in the inductor and switches, and see why the input capacitor runs hot.
- Add switch and winding resistances, find the duty cycle that restores the output, and measure the efficiency.
- Drive the converter into discontinuous conduction, check the DCM ratio, and relate it to pulse-frequency modulation.

## Background

`buck.py` collects the chapter's results:

- CCM closed forms: `ripple_current`, `inductance_for_ratio`, `ripple_voltage`, `rms_currents`, `duty_with_resistances`, `duty_with_diode`;
- the exact periodic steady state with resistances, `pss` (matrix exponentials of the two switched circuits, returning the waveforms and the average input and output powers);
- DCM: `k_param`, `critical_current`, `dcm_ratio`, `dcm_duty_for_ratio`, `buck_ratio`;
- PFM and limits: `pfm_pulse`, `max_frequency`.

The two netlists:

- `buck_ccm.cir` builds Example 22-02.1's 12 V to 1.2 V, 10 A converter twice. Instance A has near-ideal switches at $D$ = 0.1 and is used for ripple and RMS currents. Instance B has 8 mΩ, 3 mΩ and 1 mΩ resistances at the duty cycle that restores 1.2 V, and is used for efficiency. Averages use 800–1000 µs; peak-to-peak values use the final period, because ngspice's time-step changes leave sub-millivolt steps earlier in the run.
- `buck_dcm.cir` replaces the low-side switch with a near-ideal diode and runs Example 22-02.5's 74.5 ns on-time into 4 Ω.

## Procedure

1. **Ripple and RMS.** *Predict* the inductor ripple, output ripple and RMS currents of Examples 22-02.1 to 22-02.3, then compute the exact steady state and run `ngspice -b buck_ccm.cir` (Part 1).
2. **Losses.** *Predict* the duty cycle and conduction-limited efficiency with the stated resistances, and the small extra loss from ripple. Compare the DC estimate, the exact steady state and ngspice (Part 2).
3. **DCM.** *Predict* the critical current and the on-time for 1.2 V at 0.3 A. Run `buck_dcm.cir`, then plot the conversion ratio against load at a fixed duty cycle (Part 3).
4. **PFM.** *Predict* the pulse rate of Example 22-02.6 at 1 mA and 1 µA. Plot the rate against load and mark the PWM boundary (Part 4).

## Expected results

- **Part 1.** The exact steady state gives 3.00 A of inductor ripple, 10.01 mV of output ripple, and RMS currents of 10.04, 3.17, 9.52, 3.01 and 0.87 A, matching Examples 22-02.1 to 22-02.3. ngspice agrees to within 0.2%.
- **Part 2.** The DC model gives $D$ = 0.1038 and 96.37%. The exact steady state, which includes the ripple's RMS effect, gives **96.34** %. ngspice gives 96.35%, because its output settles 0.3 mV higher.
- **Part 3.** The critical current is 1.5 A. The DCM on-time for 1.2 V at 0.3 A is 74.5 ns, with $D_2$ = 0.402 and a 1.34 A peak. ngspice settles within 1% of 1.2 V: its diode's small forward drop takes the rest. At a fixed $D$ = 0.1 the ratio stays at 0.1 down to 1.5 A and then climbs.
- **Part 4.** The pulse rate is 15.8 kHz at 1 mA and 15.8 Hz at 1 µA, reaching the 1.8 MHz PWM rate at 0.114 A.

## Discussion

1. **Why does the ripple barely change the conduction loss?** The RMS current is $I\sqrt{1 + r^2/12}$; at $r$ = 0.3 it is 0.37% above the DC current, so $I^2R$ rises by 0.75%. That is the small gap between the DC model's 96.37% and the exact 96.34%.
2. **Why does the output rise at light load when the duty cycle is fixed?** In DCM the idle interval carries no low-side volt-seconds, so the same on-time pushes the output higher until the volt-seconds balance again. A controller sees this as a change in gain and shortens the on-time.
3. **Why does ngspice's diode buck sit slightly below 1.2 V?** The near-ideal diode still drops about 15 mV while it freewheels. Volt-second balance then needs a slightly longer on-time for the same output, exactly as the diode term in §3.4 says.
4. **Why does the input capacitor carry more RMS current than the output capacitor?** The input capacitor supplies the pulsed difference between the switch current and its average, a square wave of amplitude about $I$. The output capacitor sees only the inductor's ripple triangle.

## Optional hardware

A synchronous buck evaluation board with a MODE pin (forced PWM or automatic PFM) shows the CCM–DCM transition directly. Watch the switch node and the inductor current with a current probe while lowering the load. In forced PWM the inductor current goes negative below the critical load; in automatic mode the switch node develops the idle "ring" of DCM and then breaks into bursts of pulses. Measure the burst rate at a few loads and compare it with $f = I/Q$.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-02.a | exact efficiency with resistances and ripple | 96.34 | % |
