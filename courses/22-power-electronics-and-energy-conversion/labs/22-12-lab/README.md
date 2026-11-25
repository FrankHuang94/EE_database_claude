# Lab 22-12 · Power Flow and Frequency Response

Chapter: [22-12 · Power Systems Fundamentals](../../chapters/22-12-power-systems-fundamentals.md)

## Objective

- Solve Example 22-12.4's two-bus power flow in volts and ohms with ngspice, and confirm the per-unit results.
- Simulate the frequency after a 1.8 GW loss of generation: the inertial fall, the nadir and the droop-governed settling.
- See how halving the system inertia changes the nadir and its timing.
- Compute fault currents and power flows across parameter sweeps.

## Background

`grid.py` collects the chapter's models:

- per unit: `bases`, `change_base`;
- lines: `line_parameters`, `sil`;
- power flow: `two_bus`, `voltage_drop`;
- faults: `fault_3ph`, `fault_slg`;
- frequency: `rocof`, `droop_df`, and `frequency_response`, a swing equation with one aggregate first-order governor and load damping.

The two netlists:

- `powerflow.cir` places 230 kV/√3 at 10° and 0.98 of that at 0° on either side of a 52.9 Ω reactance (0.1 pu), solves the circuit by AC analysis at 60 Hz, and computes three-phase $P$ and $Q$ from $3\mathbf{V}\mathbf{I}^*$.
- `freq.cir` integrates the swing equation on a 1 F capacitor whose voltage is the frequency deviation, with a governor modelled as a first-order lag (5 s) toward its 5% droop response and 1000 MW/Hz of load damping. The system has 50 GW of synchronous generation with $H$ = 4 s and loses 1.8 GW at $t$ = 0.

## Procedure

1. **Power flow.** *Predict* $P$, $Q_1$ and $Q_2$ from Example 22-12.4, then run `ngspice -b powerflow.cir` (Part 1).
2. **Frequency response.** *Predict* the initial RoCoF from §3.5 and the final deviation from the droop formula. *Guess* the nadir before running `ngspice -b freq.cir` (Part 2).
3. **Less inertia.** Repeat with $H$ = 2 s in the notebook and compare the nadir and its timing (Part 3).
4. **Sweeps.** Plot $P$ against $\delta$ for Example 22-12.4, and the three-phase and ground-fault currents against $Z_0/Z_1$ (Part 4).

## Expected results

- **Part 1.** 170 MW, 0.349 pu and 0.047 pu, as in Example 22-12.4.
- **Part 2.** The frequency falls at 0.27 Hz/s (Example 22-12.7), reaches its nadir of **0.344** Hz below 60 Hz at **2.27** s, and settles at **−0.102** Hz, the droop value $-\Delta P/(\sum S/(Rf_0) + D)$. The governor's 5 s lag is why the nadir is more than three times the final deviation.
- **Part 3.** With $H$ = 2 s the nadir deepens to **0.450** Hz and arrives earlier, at **1.52** s: less inertia means a faster, deeper excursion that the same governors cannot catch.
- **Part 4.** $P$ follows $\sin\delta$ to its 9.8 pu maximum at 90°. The ground fault exceeds the three-phase fault whenever $Z_0 < Z_1$.

## Discussion

1. **Why does the final deviation not depend on inertia?** At steady state nothing is accelerating, so only the governors and load damping balance the lost power. Inertia sets how fast the frequency moves and how deep the nadir is, not where it ends.
2. **What would fast frequency response from batteries do?** A response within a few hundred milliseconds adds power before the governors act, raising the nadir; in this model it is a second, much faster governor in parallel.
3. **Why per unit?** The netlist needs real volts and ohms; the per-unit example needed none of the 230 kV, 529 Ω or √3 factors. Both agree because per unit is only a scaling.

## Optional hardware

A frequency meter on a wall outlet (or a smartphone app that reads mains frequency through a power adapter's sensor, where available) shows the grid's normal ±0.02–0.05 Hz wander and, occasionally, a dip after a large plant trips. Public grid-operator dashboards also publish frequency and RoCoF in real time.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-12.a | frequency nadir below 60 Hz, H = 4 s | 0.344 | Hz |
| Lab 22-12.b | time of the nadir | 2.27 | s |
| Lab 22-12.c | settled frequency deviation | −0.102 | Hz |
| Lab 22-12.d | nadir with H = 2 s | 0.450 | Hz |
| Lab 22-12.e | time of the nadir with H = 2 s | 1.52 | s |
