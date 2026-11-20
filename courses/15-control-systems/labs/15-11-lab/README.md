# Lab 15-11 · Digital Control

Chapter: [15-11 Digital Control](../../chapters/15-11-digital-control.md)

## Objective

See exactly what sampling does to a loop. You will discretize plants and controllers, simulate sampled loops with the continuous plant running between samples, measure the phase the hold costs, build a sampler from a switch and a capacitor in ngspice, and compare discretization methods.

## Background

Read §3 of the chapter. `digital.sampled_loop` advances the continuous plant exactly between samples with the matrix exponential (as in 15-10), calls a user-supplied controller once per sample, and holds its output. `dmargins` evaluates a discrete loop gain on the unit circle up to the Nyquist frequency.

## Files

- [digital.py](digital.py): `zoh`, `tustin`, `pi_tustin`, `sampled_loop`, `dfreq`, `dmargins` and `jury2`.
- [15-11-digital-lab.ipynb](15-11-digital-lab.ipynb): the notebook (Parts 1–4).
- [sample_hold.cir](sample_hold.cir): proportional control ($K$ = 1) of $1/[s(s + 1)]$ through a switch-and-capacitor sampler with $T$ = 0.5 s.

## Procedure

1. **Discretize (Part 1).** Compute the ZOH equivalents of Example 15-11.2 with `zoh` and with the matrix exponential, and compare.
2. **Sweep $T$ (Part 2).** For Example 15-11.3's PI loop, plot overshoot and discrete phase margin against $T$ from 0.1 s to 2 s, with the $\omega_cT/2$ prediction.
3. **A real sampler (Part 3).** Run `sample_hold.cir` and compare its overshoot and peak time with `sampled_loop`. *Predict first:* more or less overshoot than the continuous 16.3%?
4. **Discretization methods (Part 4).** Discretize Example 15-09.2's lead at $T$ = 0.2 s by forward Euler, backward Euler, Tustin and prewarped Tustin, and overlay their phase curves with the continuous one.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | ZOH equivalents | identical to rounding by both methods |
| 2 | PI loop | overshoot rises and margin falls with $T$, close to the $\omega_cT/2$ rule for small $T$ |
| 3 | Sampler | 28.6–28.7% overshoot at 3.45 s, against 16.3% continuous |
| 4 | Methods | prewarped Tustin peaks at 4.42 rad/s; the others shift the peak |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-11.a | continuous-loop overshoot (K = 1) | 16.3 | % |
| Lab 15-11.b | discrete phase margin, K = 1, T = 0.5 s | 40.8 | ° |

## Discussion

1. Why is the ngspice sampler's overshoot slightly lower than the ideal ZOH simulation's?
2. In Part 2, why does the $\omega_cT/2$ rule underestimate the damage at large $T$?
3. In Part 4, why does forward Euler distort the lead most?
4. A colleague proposes sampling 100 times faster than crossover "to be safe". What does it cost?

### Answers

1. The switch is closed for 1 ms at the start of each period, so the held value is the error at about 1 ms after the ideal sample instant, slightly more recent information. The 0.2% timing shift changes the overshoot by about 0.2% of its value.
2. The rule treats the hold as a pure delay of $T/2$, valid when $\omega_cT \ll \pi$. At large $T$ the crossover approaches the Nyquist frequency, aliasing and the discrete loop's own dynamics dominate, and the first held sample can be a large step (Example 15-11.3 at $T$ = 2 s).
3. Forward Euler maps $s$ to $(z - 1)/T$, a poor approximation of $e^{sT}$ except for $\lvert sT\rvert \ll 1$; the lead's pole at 8.88 rad/s has $\lvert sT\rvert$ = 1.8, where the error is large. Tustin's mapping is accurate to second order.
4. More computation and power, ADC bandwidth, and coefficient sensitivity: poles near $z$ = 1 need more bits to represent, and integrators accumulate tiny increments that fixed-point arithmetic may round away. Sampling 10 to 30 times the bandwidth is usually the better balance.

## Optional hardware

Implement the Tustin PI of Example 15-11.3 on a microcontroller controlling a small heater (Lab 15-08's optional plant), log temperature at several sample periods, and compare the overshoot with the simulation.
