# Lab 15-08 · PID Control

Chapter: [15-08 PID Control](../../chapters/15-08-pid-control.md)

## Objective

Design, tune and harden PID controllers. You will place poles and watch the controller's zero change the overshoot, compare tuning rules on setpoint and disturbance responses, wind up an integrator against an actuator limit and cure it in Python and ngspice, and tame the derivative with a filter and setpoint weighting.

## Background

Read §3 of the chapter. `pid.simulate` integrates the plant, the integrator and the derivative filter with a fixed-step fourth-order Runge–Kutta method. A fixed step is used because saturation and clamping switch the dynamics abruptly, which makes variable-step solvers crawl; the verify script checks that halving the step changes the results by less than one part in a million.

## Files

- [pid.py](pid.py): `simulate` (limits, anti-windup, derivative filter, setpoint weights, input disturbance), `zn_ultimate`, `tyreus_luyben`, `simc_pi` and `pid_tf`.
- [15-08-pid-lab.ipynb](15-08-pid-lab.ipynb): the notebook (Parts 1–4).
- [windup.cir](windup.cir): Example 15-08.4's thermal loop with a ±10 W actuator, without and with back-calculation anti-windup.

## Procedure

1. **Pole placement (Part 1).** For Example 15-08.1, keep the closed-loop poles fixed and plot the step response; then compare with a design that moves the zero (use the same poles, but apply the proportional action to the measurement only, $b$ = 0). *Predict first:* which overshoots more?
2. **Tuning rules (Part 2).** Reproduce Example 15-08.3's table, then try SIMC on a first-order-plus-delay approximation of $1/(s + 1)^3$.
3. **Windup (Part 3).** Plot temperature and actuator power for Example 15-08.4 in the three anti-windup modes, and run `windup.cir`. *Predict first:* how long the actuator stays saturated without anti-windup.
4. **Kick and noise (Part 4).** Add white measurement noise to Example 15-08.5's loop and compare the actuator activity for $N$ = 5, 10 and 20.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Overshoot | 12.6% with the PI zero; much less with $b$ = 0, same poles |
| 2 | Tuning rules | the table of Example 15-08.3: ZN fast and oscillatory, TL robust and slow |
| 3 | Windup | saturation for 44.8 s and 23.6% overshoot without anti-windup; 4.08 K peak with back-calculation, in ngspice too |
| 4 | Noise | actuator noise grows roughly in proportion to $1 + N$ |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-08.a | time saturated, no anti-windup | 44.8 | s |
| Lab 15-08.b | time saturated, back-calculation | 16.1 | s |
| Lab 15-08.c | time saturated, clamping | 10.7 | s |
| Lab 15-08.d | overshoot with b = 0 (Example 15-08.1 poles) | 1.52 | % |

## Discussion

1. In Part 1, why does $b$ = 0 give exactly the overshoot that $\zeta$ = 0.8 predicts?
2. Why does clamping saturate for a shorter time than back-calculation in Part 3?
3. Why is the ngspice result for the no-anti-windup case identical to Python's, even though one integrates with variable steps and the other with fixed steps?
4. A colleague proposes removing the derivative entirely to avoid noise. When would you agree?

### Answers

1. With $b$ = 0 the reference enters only through the integral, so the reference-to-output transfer function is $KK_i/(\tau s^2 + (1 + KK_p)s + KK_i)$: the same poles with no zero, which is exactly the standard second-order system with $\zeta$ = 0.8 (1.52% overshoot). The disturbance response is unchanged.
2. Clamping stops integrating the moment saturation begins (while the error would deepen it), so the integral never grows beyond its value at that moment. Back-calculation lets the integrator move, pulled toward the limit with time constant $T_t$, so a little excess accumulates and the actuator stays saturated longer.
3. Both solve the same equations accurately; the saturation is a static nonlinearity, and away from the switching instants the dynamics are smooth. Both methods resolve the long, slow transient to many digits.
4. When the plant is close to first order (one dominant lag), the derivative adds little phase where it is needed, and a PI controller with a lower crossover meets the specification. Derivative action earns its noise cost with plants that have two or more significant lags, or when a fast response is needed near the stability limit.

## Optional hardware

An Arduino-class board, a small resistor heater, a thermistor and a MOSFET make a slow thermal plant. Implement PI with and without clamping, limit the duty cycle to 50%, and reproduce the windup overshoot of Example 15-08.4.
