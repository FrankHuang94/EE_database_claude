# Lab 25-01 · Oxidation, Gate Trenches, Wire Tiers and Fab Flow

**Objective.** Check the Deal–Grove closed form against a numerical solution and explore oxidation recipes; size a replacement-gate trench; compare wire tiers against the time-of-flight floor, confirming the delays in ngspice; and test Little's law on a simulated fab.

**Chapter:** [25-01 · Process Flow Overview: FEOL, MOL and BEOL](../../chapters/25-01-process-flow-overview.md)

## Background

§3.2 derived the linear-parabolic law $x^2 + Ax = B(t + \tau)$ from three fluxes in series, with Arrhenius coefficients for dry and wet oxidation. §3.3 gave the trench-fill budget $w_{fill} = L_t - 2(t_{hk} + t_{wf})$. §3.5 showed that scaling a wire's cross-section by $s$ cuts its RC delay by $s^2$ down to the time-of-flight floor $L\sqrt{\varepsilon_r}/c$. §3.6 derived Little's law, WIP = $\lambda T$.

## Files

- `process.py`: Deal–Grove coefficients, closed-form and ODE thickness, oxidation time and recipe temperature, silicon consumption, trench fill, contact resistance and drive loss, wire resistance with barrier, RC delay and time of flight, step survival, cycle time, Little's law and a fab simulation, mixed density.
- `rc_tiers.cir`: 1 mm routes on the local, intermediate and global tiers of Example 25-01.6 as 200-section RC ladders, with `EXPECT` lines tied to the chapter's answer key.
- `25-01-process-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Oxidation** (notebook). *Predict* whether 1 h of wet oxidation at 1000 °C on bare (100) silicon grows more or less than half of Example 25-01.2's 500 nm. Compute it with the closed form and with the ODE, then plot thickness against time for wet and dry ambients at 900, 1000 and 1100 °C. Finally compute dry growth for 1 h at 1000 °C with $x_i$ = 25 nm.

**Part 2 · Gate trench** (notebook). With 1.8 nm of HfO₂ and the 4.5 nm work-function flavour, *predict* the narrowest trench that leaves 3.0 nm of fill, then sweep the trench width for both flavours.

**Part 3 · Wire tiers** (notebook and ngspice). *Predict* the length at which the global tier's RC delay equals its time of flight ($\varepsilon_r$ = 3.0), then compute it and plot delay against length for all three tiers. Run `ngspice -b rc_tiers.cir` (or `python tools/run_spice.py 25-01`) and compare the measured delays with Example 25-01.6.

**Part 4 · Little's law** (notebook). A fab starts 100,000 wafers a month with random cycle times averaging 12 weeks. *Predict* its average WIP, then simulate it.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-01.a | wet oxide after 1 h at 1000 C | 388 | nm |
| Lab 25-01.b | dry oxide after 1 h at 1000 C, xi = 25 nm | 58 | nm |
| Lab 25-01.c | narrowest trench for 3 nm fill | 15.6 | nm |
| Lab 25-01.d | global length where RC equals time of flight | 1.27 | mm |
| Lab 25-01.e | Little's-law WIP | 2.76e5 | wafers |

The closed form and the ODE agree to better than 0.01 nm. The simulated WIP is within 1% of $\lambda T$. The ngspice ladders run about 0.5% above the distributed-line delays, converging as the number of sections grows.

## Discussion

1. Part 1's 388 nm is more than three quarters of 500 nm in two thirds of the time: why does the second hour add so much less than the first?
2. The dry result with $x_i$ = 25 nm depends strongly on that patch. What would a process engineer measure to calibrate it?
3. Below 1.27 mm the global wire's RC delay is smaller than its time of flight. What sets that wire's delay in practice, and which chapter models it?
4. Little's law needed no assumption about the cycle-time distribution. Change the simulation's gamma shape parameter and confirm that the average WIP does not change. What does change?

## Optional hardware

None needed. A university microfabrication lab (EE143 or 6.152J style) typically lets students grow and measure oxides with an ellipsometer or by colour chart; comparing measured thicknesses with Part 1's model is the classic first experiment.
