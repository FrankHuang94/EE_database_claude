# Lab 15-03 · Time Response and Specifications

Chapter: [15-03 Time Response and Specifications](../../chapters/15-03-time-response.md)

## Objective

Measure time-domain specifications exactly, and learn where the rules of thumb fail. You will reproduce the second-order specification table, measure a real RLC circuit's step response in ngspice, watch extra poles, zeros and a doublet reshape a response, and test pole pairs against a set of specifications.

## Background

Read §3 of the chapter. `specs.py` computes step responses exactly with the matrix exponential of an augmented state matrix, $\exp\!\left(\begin{bmatrix}A & B\\ 0 & 0\end{bmatrix}t\right)$, whose top-right block is $\int_0^te^{A\tau}d\tau\,B$. That works for any pole pattern, including repeated poles and integrators. `step_specs` finds each crossing on a dense grid, then refines it with a root finder on the exact response, so its specifications do not depend on the grid spacing. It finds peaks as zeros of the impulse response.

## Files

- [specs.py](specs.py): `step_at`, `impulse_at`, `step_curve`, `step_specs`, `second_order` and `zeta_from_overshoot`.
- [15-03-time-response-lab.ipynb](15-03-time-response-lab.ipynb): the notebook (Parts 1–4).
- [rlc_step.cir](rlc_step.cir): a series RLC low-pass with $\zeta$ = 0.5 and $\omega_n$ = 31,623 rad/s, with ngspice measurements of rise time, peak time, overshoot and settling time.

## Procedure

1. **The table (Part 1).** Sweep $\zeta$ from 0.2 to 1.2 for $1/(s^2 + 2\zeta s + 1)$. Plot overshoot, $\omega_nt_r$, $\omega_nt_s$ and the rule $4/\zeta$ against $\zeta$. *Predict first:* is the exact settling time a smooth function of $\zeta$?
2. **A circuit (Part 2).** Run `rlc_step.cir` and compare its four measurements with `step_specs` for the same transfer function, $\omega_n^2/(s^2 + (R/L)s + \omega_n^2)$. *Predict first:* overshoot and peak time.
3. **Extra poles, zeros and a doublet (Part 3).** Reproduce the tables of Examples 15-03.4 and 15-03.5, and plot Example 15-03.6's response on a logarithmic error axis.
4. **Specifications to poles (Part 4).** For overshoot at most 5%, 2% settling at most 2 s and rise time at most 0.6 s, test the pole pairs of Problem 15-03.5 with the rules and with `step_specs`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Settling time against $\zeta$ | a staircase with jumps where the last band exit moves to an earlier half-cycle; $4/\zeta$ is only a trend line |
| 2 | RLC circuit | rise 51.8 µs, peak at 114.7 µs, 16.3% overshoot, 2% settling at 255.4 µs, in ngspice and in Python |
| 3 | Doublet | a fast drop to about 5% error, then a straight line on the log-error plot with slope set by the 159 ns tail |
| 4 | Pole pairs | only −4 ± j3 meets all three exactly; −3 ± j2 passes the rise-time rule but fails the exact rise time |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-03.a | RLC rise time | 51.8 | µs |
| Lab 15-03.b | RLC peak time | 114.7 | µs |
| Lab 15-03.c | RLC overshoot | 16.3 | % |
| Lab 15-03.d | RLC 2% settling time | 255.4 | µs |

## Discussion

1. Why does the exact settling time jump as $\zeta$ changes smoothly?
2. The ngspice and Python results agree to better than 0.2%. What small differences remain between the circuit and the ideal transfer function?
3. In Part 3, why does the doublet's tail look like a straight line on a logarithmic error axis, and what does its slope tell you?
4. In Part 4, the rise-time rule passes −3 ± j2 but the exact response fails. What would you tell a colleague who designs only with the rules?

### Answers

1. Settling time is the last time the response leaves the band. The response oscillates inside a decaying envelope, so the last exit is a crossing next to one of its peaks or troughs. As $\zeta$ increases, the last peak or trough that poked out of the band shrinks inside it, and the last exit jumps back by about half a damped period.
2. The source has a 1 ns rise time rather than an ideal step, and ngspice integrates with finite time steps and interpolates its crossing measurements. Both effects are tiny compared with the 115 µs time scale. The circuit itself is exactly second-order: with ideal elements its transfer function is exactly $1/(LCs^2 + RCs + 1)$.
3. After the fast pole has died out, the error is $A e^{-pt}$, and $\ln(\text{error}) = \ln A - pt$ is a straight line. Its slope is $-p$, so the tail's time constant $1/p$ can be read from a measured settling plot, which is how designers find doublets in silicon.
4. The rules are approximations fitted near $\zeta \approx$ 0.5 to 0.6; at $\zeta$ = 0.83 the exact rise time is 44% longer than $1.8/\omega_n$. Use the rules to find a region, then verify the candidate design by simulation, with margin.

## Optional hardware

Build the RLC circuit with a 1 mH inductor and a 1 µF film capacitor, and choose the series resistor so that it plus the inductor's own resistance totals about 31.6 Ω. Drive it from a function generator's 500 Hz square wave through an op-amp voltage follower: the generator's 50 Ω output resistance alone exceeds the 31.6 Ω needed for $\zeta$ = 0.5. Measure overshoot, peak time and settling on an oscilloscope.
