# Lab 20-02 · Designing and Verifying a Two-Stage Op-Amp

Chapter: [20-02 · Two-Stage Op-Amp Design](../../chapters/20-02-two-stage-op-amp-design.md)

## Objective

- Run the chapter's design procedure in code, and find which choices actually minimize the supply current.
- Confirm the exact poles, crossover and margins of the designed op-amp, with three nulling-resistor choices, in ngspice.
- Measure the slew rate with a large-signal behavioral model, and explain why it falls short of $I_{SS}/C_c$.
- Measure the follower's negative-supply rejection against frequency.
- See indirect compensation's lightly damped pole pair in a step response, and re-tune a nested Miller amplifier for both margins.

## Background

The design of Example 20-02.3 is a PMOS-input, NMOS-second-stage op-amp in the illustrative T130 process: GBW 50 MHz into 2 pF, $C_c$ = 0.6 pF, $R_z = 1/g_{m6}$. Its small-signal model is the two-node circuit of §3.2 (node 1: $R_1$, $C_1$; output: $R_2$, $C_L$), with $C_c$ and $R_z$ between them. §3.3 gives the second-stage $g_{m6}$ that places $p_2$ at $2\omega_u$, including M6's own gate capacitance; §3.5 and §3.6 give the indirect and nested Miller models; §3.10 the supply-rejection model.

Files:

- `opamp.py`: the design procedure (`design_two_stage`, `total_current`, `optimum_cc`, `gm6_for_p2`), the transfer functions (`miller_tf`, `indirect_tf`, `nmc_tf`), `margins` (crossover, phase and gain margin), and helpers for settling, slewing and SC CMFB. It imports 20-01's `gmid.py`.
- `miller.cir`: the designed op-amp's small-signal model with $R_z$ = 0, $1/g_{m6}$ and the cancelling value.
- `slew.cir`: a behavioral large-signal follower (clipped first stage, M6 that can only sink) for slew-rate measurement.
- `psrr.cir`: the follower with a 1 V AC ripple on VSS.
- `indirect.cir`, `nmc.cir`: Example 20-02.5's and 20-02.6's small-signal models, with gain margin from the continuous phase.
- `20-02-opamp-lab.ipynb`: the procedure below.

## Procedure

1. **Where the current goes.** Plot Figure 3's current split, then repeat at $(g_m/I_D)_6$ = 6 S/A and predict the change. Then sweep $(g_m/I_D)_6$ from 6 to 26 S/A, optimizing $C_c$ at each value subject to the output-slew condition $I_6 \ge I_{SS}(1 + C_L/C_c)$, and find the minimum total current (Part 1).
2. **Exact margins in ngspice.** Predict the crossover and phase margin for each $R_z$ from Example 20-02.4, then run `ngspice -b miller.cir` (Part 2).
3. **Slew rate.** Predict the slew rate from $I_{SS}/C_c$, then run `ngspice -b slew.cir`. Compare both edges with the predictions of the discussion below (Part 3).
4. **Supply rejection.** Predict PSRR⁻ at 1 kHz and 1 MHz from §3.10, then run `ngspice -b psrr.cir` (Part 4).
5. **The pole pair.** Plot the closed-loop step response of Example 20-02.5's amplifier with $g_{mc} = g_{m1}$ and with 600 µS; predict which rings, then measure the overshoot. Run `ngspice -b indirect.cir` for the margins (Part 5).
6. **Re-tuning nested Miller.** On a grid ($g_{m3}$ from 1 to 3 times the Butterworth value in steps of 0.1, $g_{m2}/g_{m1}$ ∈ {1, 1.5, 2, 3}, $C_{m2}$ from 0.1 to 0.8 pF in steps of 0.05 pF), find the smallest $g_{m3}$ that gives PM ≥ 60° and gain margin ≥ 10 dB with Example 20-02.6's parasitics. Check one design with `ngspice -b nmc.cir` (Part 6).

## Expected results

- **Part 1.** At $(g_m/I_D)_6$ = 6 S/A the optimum $C_c$ barely moves (**0.672** pF), but the total current rises to **262.0** µA: a faster but less efficient M6 costs more current than its smaller gate saves. With the slew condition enforced, the minimum is at $(g_m/I_D)_6$ ≈ **18** S/A and $C_c$ ≈ **0.92** pF, at **136** µA, **23**% below Example 20-02.3. Beyond it, the slew condition forces a larger $C_c$ and the current rises again.
- **Part 2.** The ngspice crossovers and margins match Example 20-02.4 to the fourth digit.
- **Part 3.** Both edges slew at **32.7** V/µs, not 34.9 V/µs.
- **Part 4.** PSRR⁻ is **69.18** dB at 1 kHz and **33.72** dB at 1 MHz, within a hundredth of a decibel of the open-loop PSRR of §3.10 (the follower's loop gain is large at both frequencies).
- **Part 5.** With $g_{mc} = g_{m1}$ the step overshoots by **25.5**% and rings near **169** MHz; with 600 µS it does not overshoot (**0.0**%).
- **Part 6.** The smallest grid design is $g_{m3}$ = **1.8** times the Butterworth value (**452.4** µA at 10 S/A), with $g_{m2}$ = **2** $g_{m1}$ and $C_{m2}$ = **0.5** pF: PM = **61.8**°, gain margin **10.1** dB.

## Discussion

1. **Is 10 S/A for M6 a mistake?** Not a mistake but a choice. Running M6 at 18 S/A saves current because the $f_T$ bound (§3.3) is far above the target $p_2$, so the cheaper route is efficiency. The price is a width **3.4** times larger and a $C_1$ **2.7** times larger, so $p_3 \approx g_{m6}/C_1$ falls to about **0.98** GHz. M3–M4, which must share M6's $V_{GS}$ (§3.9), also move into weak inversion, raising $g_{m3}/g_{m1}$ and the noise. The design also loses margin against a larger load. Which design is better depends on the specification's slack.
2. **Why the slew rate is 32.7 V/µs, not 34.9.** In a steady ramp of slope SR, the output's current through $R_2$ changes at SR/$R_2$, which M6 must absorb: $g_{m6}\,dv_1/dt = -\text{SR}/R_2$. Node 1 therefore moves too, and the voltage across $C_c$ changes faster than the output by $\text{SR}/(g_{m6}R_2)$. With the $C_c$ current fixed at $I_{SS}$,

$$
\text{SR} = \frac{I_{SS}/C_c}{1 + 1/A_2} = \frac{34.9\text{ V/µs}}{1.05} = 33.2\text{ V/µs},
$$

   the steady-ramp estimate (**33.2** V/µs). The last **1.6**% is current that $R_1$ and $C_1$ take from node 1 during the ramp. The first-order formula is a good design tool, not a measurement.
3. **Why gain margin matters more than phase margin in Part 5.** The 81° phase margin in Example 20-02.5(b) is genuine; the ringing comes from the pole pair's peak near 169 MHz, where the loop gain is only 1 dB below unity.

## Optional hardware

A discrete two-stage op-amp can be built from CMOS transistor arrays (for example the CD4007 or ALD1106/ALD1107 matched pairs) on a breadboard. Compensate it with a few picofarads plus a potentiometer as $R_z$, drive a 100 pF load, and watch the step response change on an oscilloscope as $R_z$ sweeps through $1/g_{m6}$. Expect the numbers to differ from T130 by orders of magnitude, but the shape of the trade-off to be the same.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-02.a | optimum C_c at (g_m/I_D)_6 = 6 S/A | 0.672 | pF |
| Lab 20-02.b | total current at (g_m/I_D)_6 = 6 S/A | 262.0 | µA |
| Lab 20-02.c | simulated slew rate | 32.7 | V/µs |
| Lab 20-02.d | steady-ramp slew estimate | 33.2 | V/µs |
| Lab 20-02.e | follower PSRR- at 1 kHz | 69.18 | dB |
| Lab 20-02.f | follower PSRR- at 1 MHz | 33.72 | dB |
| Lab 20-02.g | slew-constrained optimum (g_m/I_D)_6 | 18 | S/A |
| Lab 20-02.h | minimum total current | 136 | µA |
| Lab 20-02.i | step overshoot, g_mc = g_m1 | 25.5 | % |
| Lab 20-02.j | step overshoot, g_mc = 600 uS | 0.0 | % |
| Lab 20-02.k | smallest g_m3 factor on the grid | 1.8 | — |
| Lab 20-02.l | g_m2/g_m1 of that design | 2 | — |
| Lab 20-02.m | C_m2 of that design | 0.5 | pF |
| Lab 20-02.n | slew-constrained optimum C_c | 0.92 | pF |
| Lab 20-02.o | PM of the re-tuned design | 61.8 | ° |
| Lab 20-02.p | gain margin of the re-tuned design | 10.1 | dB |
| Lab 20-02.q | output-stage current of the re-tuned design | 452.4 | µA |
| Lab 20-02.r | saving at the optimum against Example 20-02.3 | 23 | % |
| Lab 20-02.s | M6 width ratio, 18 S/A against 10 S/A | 3.4 | — |
| Lab 20-02.t | C_1 ratio, 18 S/A against 10 S/A | 2.7 | — |
| Lab 20-02.u | ringing frequency (phase-crossover), g_mc = g_m1 | 169 | MHz |
| Lab 20-02.v | A_2 correction factor 1 + 1/A_2 | 1.05 | — |
| Lab 20-02.w | p3 estimate g_m6/C_1 at 18 S/A | 0.98 | GHz |
| Lab 20-02.y | shortfall of the simulation against the steady-ramp estimate | 1.6 | % |
