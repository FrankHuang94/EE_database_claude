# Lab 15-01 · Modeling Dynamic Systems

Chapter: [15-01 Modeling Dynamic Systems](../../chapters/15-01-modeling-dynamic-systems.md)

## Objective

Build the chapter's plant models as state-space systems and nonlinear right-hand sides, simulate them, and check two of them as circuits in ngspice. You will see a mechanism and its analogue circuit trace identical curves, find a DC motor's two time constants, watch a processor's junction temperature rise on two time scales, and push a leakage-dependent thermal loop into runaway.

## Background

Read §3 of the chapter. Every model here has states equal to its energy stores and is linear except the leakage loop and the pendulum, which the notebook linearizes about their operating points (§3.7).

## Files

- [plants.py](plants.py): `msd`, `analogs`, `motor`, `motor_first_order`, `thermal_two_node`, `leakage_rhs`, `pendulum_rhs` and `step` (the exact step response through the matrix exponential).
- [15-01-modeling-lab.ipynb](15-01-modeling-lab.ipynb): the notebook (Parts 1–4).
- [analog_msd.cir](analog_msd.cir): the force–voltage circuit of Example 15-01.1.
- [thermal_two_node.cir](thermal_two_node.cir): Example 15-01.3's thermal network, with temperatures as voltages and heat flows as currents.

## Procedure

1. **Analogues (Part 1).** Simulate Example 15-01.1's mass–spring–damper and its force–voltage circuit, overlay displacement and capacitor charge, and run `analog_msd.cir` in ngspice. *Predict first:* the peak displacement and its time.
2. **Motor (Part 2).** Step 12 V onto Example 15-01.2's motor with the full model and with the first-order model ($L$ = 0). Compare speeds at 5 ms and 50 ms.
3. **Thermal (Part 3).** Step 100 W onto Example 15-01.3's network. Plot $T_J$ and $T_C$ on a logarithmic time axis, and run `thermal_two_node.cir`. *Predict first:* $T_J$ at 1 s with a one-node model of time constant 107 s, and with the two-node model.
4. **Runaway (Part 4).** Integrate Example 15-01.4's leakage model from 25 °C for $R$ = 0.5, 0.6 and 0.65 K/W. Find where each settles, or when it passes 150 °C.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Peak displacement, time | 0.0763 m at 0.160 s, in both the mechanical model and the circuit |
| 2 | Speed at 5 ms and 50 ms | full model 60.2 and 228.6 rad/s; first-order model 64.3 and 227.9 rad/s (ahead early, 0.3% behind later) |
| 3 | $T_J$ at 1 s | 41.1 °C (two nodes) against 30.5 °C (one node) |
| 4 | Final temperatures | 64.25 °C at 0.5 K/W; runaway at 0.65 K/W |

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 15-01.a | junction at 1 s, one-node model | 30.5 | °C |
| Lab 15-01.b | junction at 1 s, two-node model | 41.1 | °C |
| Lab 15-01.c | full motor model at 5 ms | 60.2 | rad/s |
| Lab 15-01.d | first-order model at 5 ms | 64.3 | rad/s |
| Lab 15-01.e | full motor model at 50 ms | 228.6 | rad/s |
| Lab 15-01.f | first-order model at 50 ms | 227.9 | rad/s |
| Lab 15-01.g | first-order shortfall at 50 ms | 0.3 | % |
| Lab 15-01.h | equilibrium at 0.6 K/W | 79.4 | °C |
| Lab 15-01.i | loop gain at 0.6 K/W | 0.61 | — |
| Lab 15-01.j | effective time constant at 0.6 K/W | 77 | s |
| Lab 15-01.l | nonlinear 2% settling from 25 °C at 0.6 K/W | 245 | s |
| Lab 15-01.k | passive time constant at 0.6 K/W | 30 | s |

## Discussion

1. Why do the mechanical model and the force–voltage circuit agree exactly, not just approximately?
2. In Part 2, the full model starts more slowly than the first-order model but is slightly ahead by 50 ms. Why?
3. A colleague proposes estimating the thermal capacitance of the processor package from the slow time constant alone. What would that miss?
4. In Part 4, what happens at $R$ = 0.6 K/W, which is below the critical 0.628 K/W, and how long does it take to settle?

### Answers

1. They obey the same differential equation with the same coefficients: $L = m$, $R = b$, $C = 1/k$, and the charge plays the displacement. The analogy is an exact mapping of the equations, not an approximation.
2. In the first-order model the current jumps instantly to $V/R$, while in the full model it rises with $\tau_e$ = 0.5 ms, so the full model's torque, and its speed, start more slowly. Later the full model's slow pole is the faster one (15.36 ms against 15.87 ms), because the first-order model folds the electrical lag into its single time constant, so the full model pulls slightly ahead.
3. The junction's own small capacitance and $R_{JC}$, which set the fast 0.74 s rise. The slow time constant is essentially $R_{CA}C_H$, the heat sink's, so it says nothing about how quickly the junction overshoots the case.
4. It still settles, at **79.4** °C, closer to the point where the two equilibria merge. The loop gain there is **0.61**, so the time constant near equilibrium is $RC/(1 - G)$ = **77** s instead of the passive **30** s. The linear estimate of 2% settling (about four time constants, 5 minutes) is pessimistic far from equilibrium, where $G$ is smaller: the nonlinear model, started at 25 °C, enters the 2% band of its 54.4 K rise after **245** s, about 4 minutes. Near the critical resistance the restoring force almost vanishes, so the system lingers.

## Optional hardware

A small brushed DC motor, a bench supply and a current probe let you measure stall current, no-load speed (with a tachometer or a phone's slow-motion video) and the current spike at start-up. Compare with the model.
