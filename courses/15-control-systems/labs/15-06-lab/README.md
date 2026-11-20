# Lab 15-06 · Root Locus

Chapter: [15-06 Root Locus](../../chapters/15-06-root-locus.md)

## Objective

Compute root loci numerically, overlay the sketching rules computed exactly, and use the locus to design. You will check every rule against the numerical locus, move a zero and watch the locus bend, follow a PLL's poles as its charge-pump current varies, and build a PD-controlled servo in ngspice.

## Background

Read §3 of the chapter. `rlocus.locus` computes the closed-loop roots over a grid of gains and matches each step's roots to the previous step's by minimum total movement (an assignment problem), so branches are continuous even where roots collide. The rule functions use the closed forms of §3.2.

## Files

- [rlocus.py](rlocus.py): `locus`, `asymptotes`, `real_axis_segments`, `breakpoints`, `departure_angle`, `gain_at`, `on_locus` and `zeta_point`.
- [15-06-root-locus-lab.ipynb](15-06-root-locus-lab.ipynb): the notebook (Parts 1–4).
- [pd_servo.cir](pd_servo.cir): Example 15-06.6's servo with $C = 4(s + 8)$, built from transconductors and capacitors.

## Procedure

1. **Rules against the numerical locus (Part 1).** For Examples 15-06.1 to 15-06.4, draw the numerical locus and overlay the asymptotes, breakpoints and departure angles. *Predict first:* how many branches cross into the right half-plane in each?
2. **Move a zero (Part 2).** For $K(s + z)/[s(s + 2)(s + 4)]$, vary $z$ from 0.5 to 10 and record the centroid and the largest stable gain. *Predict first:* for which $z$ can a large enough gain destabilize the loop?
3. **A PLL across its gain (Part 3).** Plot the damping ratio of Example 15-06.5's dominant pair against $K$, and mark the gains where the poles become real.
4. **A PD servo in ngspice (Part 4).** Run `pd_servo.cir` and compare its overshoot and settling time with the design values.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Rules | every breakpoint, asymptote and departure angle matches the numerical locus |
| 2 | Moving the zero | the centroid $(-6 + z)/2$ moves right as $z$ grows; stable at every gain for $z < 6$, only below $K = 48/(z - 6)$ for $z > 6$ |
| 3 | PLL | $\zeta$ = 0.761 at the design gain; real poles between 1.287 × 10¹¹ and 1.368 × 10¹¹ s⁻² |
| 4 | PD servo | 6.70% overshoot, 0.932 s settling, in ngspice and in Python |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-06.a | centroid for z = 8 | 1 | 1/s |
| Lab 15-06.b | largest stable K for z = 8 | 24 | 1/s² |
| Lab 15-06.c | crossing frequency for z = 8 | 5.657 | rad/s |
| Lab 15-06.d | ζ of the complex pair at K = 2e11 (PLL) | 0.745 | — |
| Lab 15-06.e | ζ of the complex pair at K = 5e10 (PLL) | 0.533 | — |

## Discussion

1. Why do roots computed independently at each gain need matching before they can be drawn as branches?
2. In Part 2, why is the loop stable at every gain when $z < 6$ but not when $z > 6$?
3. In Part 3, why does the PLL's damping first rise and then fall as $K$ increases?
4. The ngspice servo computes the derivative of the error without differentiating any node voltage. How, and why is that a good idea?

### Answers

1. `numpy.roots` returns roots in no particular order, so the same index can jump between branches from one gain to the next. Matching each new set to the previous one by minimum movement keeps a branch's identity, except exactly at collisions, where any matching is valid.
2. With one zero and three poles, $n - m$ = 2: the asymptotes are vertical lines through the centroid $(-6 + z)/2$, which is left of the axis only for $z < 6$. The Routh test on $s^3 + 6s^2 + (8 + K)s + Kz$ agrees: it needs $6(8 + K) > Kz$, true for every $K$ when $z \le 6$, but only for $K < 48/(z - 6)$ when $z > 6$ (24 at $z$ = 8, crossing at ±j5.66). A stabilizing zero must be close enough to the poles it is meant to help.
3. At low $K$ the double pole at the origin splits into a lightly damped pair; as $K$ rises the zero pulls the pair left and damps it, until it reaches the real axis. Beyond the second meeting point, the new complex pair (formed with the high-frequency pole) heads toward the vertical asymptotes, and its damping falls again.
4. The derivative of the error is $\dot r - \dot y$. Here $\dot y$ is the integrator's input, $v(a)$, already available, and $\dot r$ is generated as a separate source that is the exact derivative of the reference ramp. Numerical differentiation of a simulated node amplifies time-step noise; using signals that already exist avoids it. Real PD controllers likewise take derivatives of measured velocity when they can, or filter the derivative (15-08).

## Optional hardware

A DC motor with a potentiometer on its shaft and an op-amp PD controller (a resistor in series with a capacitor in the feedback path's input) reproduces the positioning servo; measure the overshoot of a step in angle for several derivative gains.
