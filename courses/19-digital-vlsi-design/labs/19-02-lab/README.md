# Lab 19-02 · Inverter Delay, Ring Oscillators and Supply Scaling

Chapter: [19-02 · The CMOS Inverter: Dynamic Behavior and Delay](../../chapters/19-02-cmos-inverter-dynamic.md)

## Objective

- Measure an inverter's step delays in ngspice and match them to the exact square-law result and to the RC model.
- See how the RC model's error depends on the threshold-to-supply ratio, and how delay scales with load and strength.
- Simulate a ring oscillator, and see why its stage delay is longer than a step-input delay.
- Plot delay, energy and the energy–delay product against supply for two values of α.

## Background

A step-driven NMOS discharging $C_L$ is saturated for the first $V_{TN}$ of the swing and linear after it, giving $t_{pHL} = \dfrac{C_L}{k_nV_{ov}}\left[\dfrac{2V_{TN}}{V_{ov}} + \ln\left(\dfrac{4V_{ov}}{V_{DD}} - 1\right)\right]$ (§3.3). The RC model replaces the transistor by the average of $V/I$ over the transition, $R_{eq}$, and gives $t_p = \ln 2\,R_{eq}C_L$ (§3.4). Sizing by $S$ leaves the intrinsic delay $t_{p0}$ unchanged: $t_p = t_{p0}(1 + C_{ext}/(SC_{int}))$ (§3.5). A ring of $N$ stages oscillates at $1/(2Nt_p)$ (§3.6), and with the alpha-power law the delay scales as $V_{DD}/(V_{DD} - V_{TH})^\alpha$ (§3.7).

Files:

- `delay.cir`: a step-driven inverter with SPICE's level-1 model ($k_n$ = 200 µA/V², $k_p$ = 100 µA/V², 20 fF), measuring $t_{pHL}$ and $t_{pLH}$, plus the RC model with 12.57 kΩ.
- `ring.cir`: the five-stage ring of Example 19-02.5 (10 fF per node), measuring the stage delay and frequency.
- `delay.py`: `tp_step_exact` and `tp_step_ode` (closed form and numerical integration), `r_eq` and `r_eq_approx`, `tp_rc`, `tp_with_fanout`, `ring_frequency`, `simulate_ring` (coupled ODEs), `delay_vs_supply` and `edp_optimal_vdd`.
- `19-02-delay-lab.ipynb`: the procedure below.

## Procedure

1. **Step delays.** Predict $t_{pHL}$ and $t_{pLH}$ for Example 19-02.2. Run `ngspice -b delay.cir` and the notebook's Part 1.
2. **Scaling.** Predict $t_{pHL}$ when the load doubles, and when $k_n$ doubles; check with `tp_step_exact` (Part 2).
3. **The RC model's error.** Predict whether the ratio of the RC delay to the exact delay depends on $C$ or $k$; plot it against $V_{TN}/V_{DD}$ from 0.2 to 0.45 (Part 3).
4. **Fan-out and sizing.** Plot $t_p$ against $C_{ext}$ for $S$ = 1, 2 and 4 with Example 19-02.4's inverter (Part 4).
5. **Ring oscillator.** Predict the period with seven stages instead of five; simulate both with `simulate_ring` and compare the stage delays with the step-input delay (Part 5). Edit `ring.cir` to seven stages and compare.
6. **Supply scaling.** Plot normalized delay, energy and EDP from 0.5 to 1.5 V for α = 1.3 and 2 with $V_{TH}$ = 0.35 V, and find each minimum (Part 6).

## Expected results

- Part 1: $t_{pHL}$ = 168.2 ps from the closed form, the ODE and ngspice; $t_{pLH}$ = 336.4 ps; the RC model gives 174.3 ps.
- Part 2: the delay doubles with the load and halves with $k_n$: it is proportional to $C_L/k_n$.
- Part 3: the ratio depends only on $V_{TN}/V_{DD}$; it rises from 1.032 at 0.2 to 1.040 at 0.45, so the RC model is 3–4% pessimistic throughout.
- Part 4: every curve starts at $t_{p0}$ = 17.4 ps and rises linearly with slope $t_{p0}/(SC_{int})$; at 50 fF the delays are 453.1, 235.2 and 126.3 ps.
- Part 5: the five-stage ring has a period of 1.605 ns and the seven-stage ring 2.247 ns, both a stage delay of 160.5 ps, 1.91 times the 84.1 ps step-input delay.
- Part 6: EDP minima at 0.618 V (α = 1.3) and 1.05 V (α = 2).

## Discussion

1. Why does the RC model's error not depend on the load or the transistor's size?
2. Why is a ring oscillator's stage delay independent of the number of stages, and longer than the step delay?
3. ngspice's level-1 model here has no device capacitances. What would adding gate–drain overlap capacitance do to the measured delays, and why?
4. Why does the EDP optimum move to a higher supply when α grows?

**Answers.**

1. Both delays are $C/(kV_{DD})$ times a function of $V_{TN}/V_{DD}$, so the scale cancels in the ratio (Problem 19-02.10).
2. Each stage drives an identical load from an identical input waveform, so each takes the same time; the number of stages sets only how many delays make up a period. The stage delay is longer because each input is a ramp, not a step: the pull-down turns on gradually while the pull-up is still conducting (§3.6).
3. It would add a Miller-doubled $C_{gd}$ to each output (§3.1) and couple the input edge into the output, slightly overshooting it at first; both lengthen the delay.
4. With a larger α the current falls faster as the supply approaches threshold, so the delay penalty of a low supply is steeper and the balance with the $V_{DD}^2$ energy shifts upward: $3V_{TH}/(3 - \alpha)$ grows with α (§3.7).

## Optional hardware

A CD4069 (hex inverter) or the inverters of a CD4007 on a breadboard at 5 V form a three- or five-stage ring oscillator; measure its frequency with an oscilloscope, then add a capacitor at each node and watch the frequency fall in proportion to the load. Lower the supply to 3 V and compare the slowdown with $V_{DD}/(V_{DD} - V_{TH})^\alpha$.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-02.a | RC over exact delay at V_TN/V_DD = 0.45 | 1.040 | — |
| Lab 19-02.b | delay driving 50 fF at S = 2 | 235.2 | ps |
| Lab 19-02.c | seven-stage ring period | 2.247 | ns |
| Lab 19-02.d | seven-stage ring stage delay | 160.5 | ps |
