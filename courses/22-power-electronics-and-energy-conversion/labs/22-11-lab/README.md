# Lab 22-11 · Machines: a DC Motor Start, the Induction Equivalent Circuit and Torque–Speed Curves

Chapter: [22-11 · Electric Machines and Drives](../../chapters/22-11-electric-machines.md)

## Objective

- Simulate a PM DC motor starting a load, with its armature inductance and rotor inertia, and measure the current peak and the speed rise.
- Solve an induction motor's per-phase equivalent circuit in ngspice and compute torque and current at standstill and at rated slip.
- Plot induction torque–speed curves for several rotor resistances and for V/f operation at several frequencies.
- Draw an EV motor's constant-torque and constant-power envelope.

## Background

`machines.py` collects the chapter's models:

- the DC motor: `dc_motor`;
- AC machines: `sync_speed_rpm`, `slip`, the `Induction` class (Thevenin equivalent, torque, slip and torque at maximum, stator current), `power_flow`, `sync_power`;
- drives: `v_over_f`, `inverter_vll_rms`, `affinity`, `ev_envelope`.

The two netlists:

- `dcmotor.cir` models Example 22-11.1's motor (24 V, $R_a$ = 0.5 Ω, $k$ = 0.05 V·s/rad) with $L_a$ = 1 mH and $J$ = 10⁻⁴ kg·m², starting against 0.5 N·m. The rotor speed is the voltage on a capacitor of value $J$ charged by the net torque, the mechanical-to-electrical analogy of 15-01.
- `induction.cir` builds Example 22-11.4's per-phase circuit with its reactances as 50 Hz inductances, solves it by AC analysis at standstill ($R_2/s$ = 0.4 Ω) and at 3% slip ($R_2/s$ = 13.33 Ω), and computes $T = 3|I_2|^2(R_2/s)/\omega_s$.

## Procedure

1. **The DC motor start.** *Predict* the final speed and current (Example 22-11.1), the mechanical time constant $JR_a/k^2$, and whether the current peak reaches the 48 A stall value. Run `ngspice -b dcmotor.cir` (Part 1).
2. **The equivalent circuit.** *Predict* the starting torque and current and the running torque and current of Example 22-11.4. Run `ngspice -b induction.cir` (Part 2).
3. **Rotor resistance.** Plot torque against speed for $R_2$ = 0.4, 1.0 and 2.03 Ω (Part 3). *Predict* how the curves differ at standstill, at the peak and near synchronous speed.
4. **V/f.** Plot torque–speed curves at 50, 40, 30 and 20 Hz with constant $V/f$ (Part 4). *Predict* how the curves move, and what happens to the peak torque at 20 Hz, where the stator resistance matters more.
5. **The EV envelope.** Plot Example 22-11.8's torque and power against motor speed (Part 5).

## Expected results

- **Part 1.** The motor settles at 380 rad/s (3629 rpm) and 10 A (Example 22-11.1). The current peaks at **41.7** A about 6 ms after switch-on, below the 48 A stall value because the rotor is already turning and building back EMF while the 1 mH inductance slows the current's rise. The speed reaches 63% of its final value at **20.5** ms, close to the mechanical time constant $JR_a/k^2$ = 20 ms.
- **Part 2.** At standstill, 81.9 N·m and 107.0 A; at 3% slip, 65.4 N·m and 18.0 A (Example 22-11.4).
- **Part 3.** The peak torque is the same 190.9 N·m for every $R_2$, but it moves toward standstill as $R_2$ rises; with 2.03 Ω it sits at standstill. Near synchronous speed the higher-resistance rotors give far less torque for a given slip (Problem 22-11.6).
- **Part 4.** The curves shift left almost in parallel, as the same slip speed gives nearly the same torque. At low frequency the stator resistance takes a larger share of the voltage, and the peak torque at 20 Hz falls from 190.9 to **136.1** N·m, which is why drives add a voltage boost at low speed.
- **Part 5.** 400 N·m up to 5000 rpm, then constant 209 kW, with torque falling to 133 N·m at 15 000 rpm (Example 22-11.8).

## Discussion

1. **Why does the DC motor's current peak fall short of the stall current?** Current needs time to rise through $L_a$ (electrical time constant $L_a/R_a$ = 2 ms), and by then the rotor is turning and its back EMF is already opposing the supply.
2. **Why does the ngspice circuit model a rotating machine with fixed elements?** The slip-dependent resistor $R_2/s$ carries the rotation: it is the rotor's resistance plus the load that the mechanical output presents, referred to the stator.
3. **Why do V/f drives boost the voltage at low speed?** The stator's $I_1R_1$ drop is roughly fixed while the induced voltage falls with frequency, so constant $V/f$ no longer means constant air-gap flux. Raising the voltage slightly restores the flux and the torque.

## Optional hardware

A small brushed DC motor, a bench supply with current readout and a flywheel or a fan: measure the no-load speed (with an optical tachometer or a phone's slow-motion video of a marked shaft) at two voltages to find $k$, the stall current to find $R_a$, and compare a loaded run with the speed–torque line. A hobby BLDC kit with a field-oriented-control evaluation board shows the speed changing with frequency and the current rising with load.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-11.a | DC motor starting current peak | 41.7 | A |
| Lab 22-11.b | time to 63% of final speed | 20.5 | ms |
| Lab 22-11.c | peak torque at 20 Hz with constant V/f | 136.1 | N·m |
