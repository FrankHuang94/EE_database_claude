# Lab 22-09 · Cell Models, CC/CV Charging and Gauging Errors

Chapter: [22-09 · Batteries, Charging and Fuel Gauging](../../chapters/22-09-batteries-charging-fuel-gauging.md)

## Objective

- Apply a load pulse to an equivalent-circuit cell model whose OCV falls with the charge drawn, and watch the voltage relax after the pulse.
- Charge the model under a CC/CV charger and measure the CC time, the CV taper and the charge time at two rates.
- Repeat the chapter's calculations with an S-shaped OCV curve and with the RC branch included, to see which simplifications matter.
- Quantify the voltage-gauge and coulomb-counting errors of §3.6.

## Background

`battery.py` collects the chapter's models:

- fundamentals: `cell_voltage`, `theoretical_capacity_mah_per_g`;
- OCV curves: `ocv_linear` (the teaching cell) and `ocv_curved` (an illustrative S-shaped curve from 3.00 V to 4.20 V, not a real cell);
- the equivalent circuit: `step_voltage`, `simulate_cell`, `max_current`, `usable_fraction_linear`;
- charging: `cccv_linear` (closed form), `simulate_cccv` (time-stepped, any OCV curve), `linear_charger`, `converter_loss`;
- gauging: `voltage_gauge_error`, `coulomb_offset_error`, `learned_capacity`;
- aging and life: `sqrt_aging`, `arrhenius_factor`, `battery_life_hours`.

The two netlists:

- `pulse.cir` builds the teaching cell in ngspice. Its SOC is the voltage on a 1080 F capacitor that the cell current discharges, and a behavioral source turns it into the OCV. A 0.5 A load runs from 1 s to 41 s, then the cell rests for 40 s.
- `cccv.cir` charges two copies of the resistive teaching cell from empty, at 1C and at 2C, with a charger that supplies $\min(I_{cc}, (4.20 - V_{OC})/R)$, and records when CC ends and when the current falls to 30 mA.

## Procedure

1. **The pulse.** *Predict* the terminal voltage at the first instant and after 20 s (Example 22-09.2), and the voltage 40 s after a 40 s pulse ends. Run `ngspice -b pulse.cir` (Part 1).
2. **Relaxation and the gauge.** *Predict* the SOC error a voltage gauge would make if it read the cell as relaxed 40 s after the pulse (Part 1).
3. **CC/CV.** *Predict* the CC time, the charge time and the final SOC at 1C, and the charge time at 2C (Example 22-09.4). Run `ngspice -b cccv.cir` and plot the current, voltage and SOC (Part 2).
4. **Model simplifications.** Repeat the 1C charge with the RC branch included, then with the S-shaped OCV; repeat Example 22-09.3's usable capacity with the S-shaped OCV and a 3.00 V cutoff (Part 3).
5. **Gauging errors.** Plot the SOC estimate of a coulomb counter with a 10 µA offset over a week, and of a voltage gauge under a pulsed load (Part 4).

## Expected results

- **Part 1.** The terminal voltage drops to 3.700 V at once and to 3.660 V after 20 s (Example 22-09.2). Forty seconds after the 40 s pulse it has recovered to **3.7775** V, still 5.9 mV below the new OCV of 3.7833 V: a voltage gauge reading it as relaxed would put the SOC **0.65** % low. This is why TI's Impedance Track gauges wait for $dV/dt$ < 4 µV/s before reading the OCV (§3.6 of the chapter).
- **Part 2.** At 1C, CC ends after 54.0 min at 90% SOC and the charge terminates at 67.8 min at 99.0%; at 2C it terminates at 42.0 min (Example 22-09.4).
- **Part 3.**
  - With the RC branch included, the 1C charge takes **68.0** min, within a few seconds of the quasi-static 67.8 min: the CV taper (360 s) is slow compared with $\tau_1$ = 20 s.
  - With the S-shaped OCV, the 1C charge takes **63.5** min and terminates at **0.996** SOC, because the curve's steep top end raises the OCV quickly toward 4.20 V.
  - With the S-shaped OCV and a 3.00 V cutoff, a 1C load uses **97.9** % of the capacity at 25 °C and **86.6** % at −10 °C, against 90% and 60% for the straight line. The curve's steep knee near empty means a given $IR$ strands little charge; a flat curve would strand far more. The shape of the OCV curve, not just the resistance, sets the cold penalty.
- **Part 4.** The offset drifts the counter by 1.68 mAh in a week (Example 22-09.6), while the voltage gauge's error swings by $IR/(dV_{OC}/dz)$ with every load pulse.

## Discussion

1. **Why does the pulse netlist need `uic`?** The SOC capacitor has no DC path, so ngspice cannot find an operating point; the initial SOC is set with `.ic` and the operating-point solve is skipped.
2. **Why is the quasi-static charge model good enough?** The CV current decays with a 6-minute time constant, while the RC branch settles in about a minute ($3\tau_1$), so the branch tracks the current closely and adds only its small lag.
3. **What does the S-shaped curve change in practice?** Charge time and usable capacity depend on where the curve is steep. Gauges and chargers therefore carry measured OCV tables for each cell, not a straight line.

## Optional hardware

With a single lithium-ion cell in a holder with its protection circuit, a programmable electronic load and a bench supply with current limit (or a charger evaluation board), apply a 1C load pulse and log the voltage at 10 samples per second. Fit $R_0$ from the instant drop and $R_1$, $\tau_1$ from the slow sag, then repeat in a refrigerator at 5 °C. Charge with the supply's current limit set to 0.5C and voltage to 4.20 V, and watch the current taper. Never exceed the cell's rated charge voltage or charge below its minimum charge temperature.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-09.a | voltage 40 s after a 40 s, 0.5 A pulse | 3.7775 | V |
| Lab 22-09.b | voltage-gauge SOC error at that moment | 0.65 | % |
| Lab 22-09.c | 1C charge time with the RC branch | 68.0 | min |
| Lab 22-09.d | 1C charge time with the S-shaped OCV | 63.5 | min |
| Lab 22-09.e | SOC at termination with the S-shaped OCV | 0.996 | |
| Lab 22-09.f | usable fraction at 25 °C, S-shaped OCV | 97.9 | % |
| Lab 22-09.g | usable fraction at −10 °C, S-shaped OCV | 86.6 | % |
