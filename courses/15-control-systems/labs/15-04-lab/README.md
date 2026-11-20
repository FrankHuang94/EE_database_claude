# Lab 15-04 · Feedback Properties and Steady-State Error

Chapter: [15-04 Feedback Properties and Steady-State Error](../../chapters/15-04-feedback-and-steady-state-error.md)

## Objective

Predict steady-state errors from a loop's type and error constants, then check every prediction by simulation. You will see why an integrator in the plant does not reject a load, remove the offset with integral action in Python and in ngspice, hold a motor's speed under load, and watch a PLL follow a chirp.

## Background

Read §3 of the chapter. `steady.py` computes the type and the error constants from the loop gain's polynomials, and `simulate_error` simulates the closed-loop error $E = R/(1 + L)$ with `scipy.signal.lsim`, an independent check on the final-value theorem.

## Files

- [steady.py](steady.py): `system_type`, `error_constants`, `ss_errors`, `simulate_error`, `loop_from` and `is_stable`.
- [15-04-steady-state-lab.ipynb](15-04-steady-state-lab.ipynb): the notebook (Parts 1–4).
- [disturbance.cir](disturbance.cir): Example 15-04.4's two position loops (proportional and PI) built from transconductors and capacitors, with a 0.5 V step disturbance at the plant input.

## Procedure

1. **Error table (Part 1).** For the three loops of Problem 15-04.2 and Example 15-04.2, print type, $K_p$, $K_v$, $K_a$ and predicted errors, then simulate step, ramp and parabola errors. *Predict first:* which entries are infinite?
2. **Where the integrator sits (Part 2).** Simulate Example 15-04.4's loop with a step disturbance at the plant input, with proportional and with PI control, and run `disturbance.cir`. *Predict first:* the steady offset in each case.
3. **Speed under load (Part 3).** Simulate Example 15-04.3's motor with a 0.01 N·m load step for $K_i$ = 0 (proportional only), 2 and 9.75 V/rad.
4. **Chirps and hum (Part 4).** Drive Example 15-04.5's PLL with a frequency step and a frequency ramp, and Problem 15-04.10's loop with a 60 Hz output disturbance, with and without the resonant term.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Simulated errors | equal to the table's predictions; ∞ entries grow without bound |
| 2 | Position offset under a 0.5 V input disturbance | 0.0500 rad (proportional) and 0 (PI); peaks 0.0582 rad and 0.0505 rad |
| 3 | Speed after a 0.01 N·m load step | steady droop 2.27 rad/s, then 0 with PI; peak dips 2.13 and 1.90 rad/s |
| 4 | PLL and hum | zero steady phase error to a frequency step, 0.628 rad during the chirp; hum removed by the resonant term |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-04.a | peak offset, proportional | 0.0582 | rad |
| Lab 15-04.b | peak offset, PI | 0.0505 | rad |
| Lab 15-04.c | time of the PI peak | 0.300 | s |

## Discussion

1. Why does the proportional position loop overshoot its final offset (0.0582 against 0.0500 rad)?
2. The PI loop's peak offset (0.0505 rad) is barely smaller than the proportional loop's final offset. What does integral action buy, and what does it not?
3. In Part 4, why does the PLL's phase error during a chirp not depend on the loop-filter resistor $R$?
4. Why does the resonant controller of Problem 15-04.10 need a stability check that a pure integrator (at DC) might seem not to?

### Answers

1. The closed loop $s^2 + 10s + 100$ has $\zeta$ = 0.5, so its response to the disturbance step overshoots by 16.3%: 0.05 × 1.163 = 0.0582 rad.
2. Integral action removes the lasting error; it acts slowly, so the initial excursion is set mostly by the proportional gain and the plant. To reduce the peak, raise the bandwidth (more proportional gain, if the stability margin allows), or add feedforward from a measured disturbance.
3. In steady state the error depends only on $K_a = \lim s^2L = \omega_n^2$; the resistor's zero $(1 + sRC)$ equals 1 at DC. $R$ sets how quickly the error settles, not its final value.
4. The resonant term adds a pair of poles on the imaginary axis to the loop, and with them a sharp phase change near $\omega_0$. A pure integrator does the same at DC. Either way, the closed-loop poles move, and a large gain can destabilize the loop; Problem 15-04.10 checks the characteristic polynomial (15-05 gives a systematic test).

## Optional hardware

Build Example 15-04.4's loops with op-amp integrators and summers (time scaled by $RC$ = 1 ms), inject a DC offset at the plant input, and measure the offset at the output with and without the integrating path.
