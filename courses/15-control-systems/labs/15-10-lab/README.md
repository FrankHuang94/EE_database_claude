# Lab 15-10 · State-Space Introduction

Chapter: [15-10 State-Space Introduction](../../chapters/15-10-state-space-introduction.md)

## Objective

Work inside the system: solve state equations, test controllability, place every pole with state feedback, estimate unmeasured states with an observer, and see the separation principle at work. The pole-placed servo is built in ngspice.

## Background

Read §3 of the chapter. `statespace.py` implements the controllability and observability matrices, Ackermann's formula (and, by duality, the observer gain), integral augmentation, and exact closed-loop responses with the matrix exponential of an augmented matrix (the same trick as 15-03's `specs.py`).

## Files

- [statespace.py](statespace.py): `ctrb`, `obsv`, `acker`, `observer_gain`, `tf_of`, `augment_integral` and `closed_loop_response`.
- [15-10-state-space-lab.ipynb](15-10-state-space-lab.ipynb): the notebook (Parts 1–4).
- [state_feedback.cir](state_feedback.cir): the servo $1/[s(s + 1)]$ with $u = 16r - 16x_1 - 3x_2$, built from transconductors and capacitors.

## Procedure

1. **Modes (Part 1).** Plot Example 15-10.2's trajectories from several initial states in the $(x_1, x_2)$ plane, with the eigenvector directions.
2. **State feedback in ngspice (Part 2).** Run `state_feedback.cir` and compare its overshoot and peak time with $16/(s^2 + 4s + 16)$. *Predict first:* both numbers.
3. **Nearly uncontrollable (Part 3).** For two RC circuits with time constants 1 ms and $\tau_2$, sweep $\tau_2$ toward 1 ms and plot the smallest singular value of the controllability matrix (time in ms).
4. **Observer and noise (Part 4).** Add noise to the measured position in Example 15-10.5 and compare the estimated velocity's noise for observer poles at −5, −10 and −40.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Modes | trajectories bend from the fast eigenvector direction (slope −2) onto the slow one (slope −1) |
| 2 | Servo | 16.3% overshoot at 0.907 s, in ngspice and Python |
| 3 | Singular value | falls in proportion to $\lvert\tau_2 - 1\ \text{ms}\rvert$ |
| 4 | Observer noise | faster observers give noisier velocity estimates |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-10.a | slope of the slow eigenvector | −1 | — |
| Lab 15-10.b | slope of the fast eigenvector | −2 | — |

## Discussion

1. In Part 1, why do trajectories end up approaching the origin along the slow eigenvector?
2. In Part 2, the circuit uses the velocity node directly. How does that differ from a lead compensator's approach to damping?
3. In Part 3, the rank never drops until the time constants are exactly equal. Why is the rank a poor engineering test here?
4. In Part 4, what sets the best observer speed?

### Answers

1. The free response is $c_1\mathbf{v}_1e^{-t} + c_2\mathbf{v}_2e^{-2t}$; the fast mode dies first, leaving the slow eigenvector's direction.
2. State feedback measures velocity and feeds it back with gain $k_2$, adding damping with no zero. A lead compensator approximates the derivative of position from the position signal alone, adding a zero (and a pole) that change the response (Example 15-09.4: 27.4% overshoot against 16.3%).
3. Rank is a yes-or-no test; engineering needs a "how much" test. The smallest singular value measures how much input is needed to move the weak direction; it shrinks continuously long before the rank drops.
4. A trade between convergence and noise: faster poles need larger $L$, which multiplies measurement noise. Faster than the noise allows is useless; slower than the controller's poles makes the estimate the bottleneck. A Kalman filter computes the best compromise from the noise statistics.

## Optional hardware

Build the servo with an op-amp integrator chain (two integrators with resistor-set gains), feed back both outputs through summing resistors chosen for $k_1$ = 16 and $k_2$ = 3 (with time scaled to milliseconds), and measure the step response on an oscilloscope.
