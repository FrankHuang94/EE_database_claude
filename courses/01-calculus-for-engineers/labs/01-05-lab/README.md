# Lab 01-05 · Integrals

**Chapter:** [01-05](../../chapters/01-05-integrals.md) · **Notebook:** [01-05-integrals.ipynb](01-05-integrals.ipynb) · **Netlists:** [cap_charge.cir](cap_charge.cir), [integrator.cir](integrator.cir) · **Time:** about 60 minutes

## Objective

1. Measure the convergence order of the left, trapezoid, midpoint and Simpson rules.
2. Simulate a battery fuel gauge and see how sensor errors accumulate in an integral.
3. Find the minimum sampling rate for exact energy metering of a sinusoidal load.
4. Confirm in ngspice that a capacitor integrates its current, that charging dissipates ½CV² in the resistor, and that an op-amp integrator turns a square wave into a triangle.

## Background

Chapter sections 3.1 (Riemann sums and their orders), 3.5 (charge, voltage and energy as integrals), 3.6 (averages) and 3.7 (integrators).

## Procedure

1. Run all notebook cells in order.
2. **Part 1:** before running, predict the slope (order) of each rule's error on the log–log plot.
3. **Part 2:** before running, predict the gauge's error after 7 days, and how it splits between offset and gain error.
4. **Part 3:** before running, predict the minimum number of samples per cycle for exact average power.
5. **Part 4:** from the repository root, run `python tools/run_spice.py 01-05`. Then change `R2` in `cap_charge.cir` from 1 kΩ to 100 Ω, predict the dissipated energy, and re-run.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | fitted orders | left 1, trapezoid 2, midpoint 2, Simpson 4 |
| 2 | true charge used in 7 days | 109.2 mAh |
| 2 | gauge error after 7 days | 2.77 mAh (2.5%): 1.68 mAh from the 10 µA offset, 1.09 mAh from the 1% gain error |
| 3 | samples per cycle for exact average power | 3 (any phase); 1 and 2 fail by up to 1.6 kW |
| 4 | capacitor voltage at 1 ms and 3.5 ms (Problem 01-05.5) | 6.000 V and 1.000 V |
| 4 | energy in R, from the source, and stored (Example 01-05.3) | 1.250, 2.500 and 1.250 mJ |
| 4 | with R = 100 Ω | still 1.25 mJ dissipated: the loss does not depend on R |
| 4 | integrator output at 2 ms; triangle peak-to-peak | −1.000 V; 0.500 V |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 01-05.a | true charge used in 7 days | 109.2 | mAh |
| Lab 01-05.b | gauge error from offset alone | 1.68 | mAh |
| Lab 01-05.c | gauge error from gain alone | 1.09 | mAh |
| Lab 01-05.d | minimum samples per cycle | 3 | — |

## Discussion questions

1. The offset error grows with time whatever the load, while the gain error grows with the charge used. Which dominates for a device that sleeps most of the time, and what does that imply for the sensor specification?
2. Why does the trapezoid rule, which SPICE uses by default, sometimes produce small oscillations ("trapezoidal ringing") after a sudden step? (Hint: what does a second-order rule do at a discontinuity? The answer is in [02-10](../../../02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md).)
3. Real electricity meters sample at kilohertz rates, far above the 3-sample minimum. Give two reasons.

## Optional hardware version

With a USB power meter (an inline USB "power monitor" that displays mAh) and a phone: charge the phone for 30 minutes and note the mAh counted. Compare with the change in the phone's battery percentage times its rated capacity. The two differ because of charging losses, the phone's own consumption during charging, and gauge error: three integrals that do not quite agree.
