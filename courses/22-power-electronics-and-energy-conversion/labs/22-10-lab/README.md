# Lab 22-10 · Power Delivery: Interleaving, the Package Resonance and Damping

Chapter: [22-10 · Datacenter Power Delivery](../../chapters/22-10-datacenter-power-delivery.md)

## Objective

- Interleave four buck phases from 12 V to 0.8 V and measure how much of the inductor ripple cancels in the sum.
- Sweep the summed ripple against phase count and find the counts that cancel it completely.
- Measure the impedance a die sees through its package, and the first droop for a fast load step.
- Find the capacitor ESR that minimizes the first droop, and see why too much damping is as bad as too little.

## Background

`pdn.py` collects the chapter's models:

- distribution: `bar_resistance`, `busbar_loss`, `per_conductor_ratio`, `chain_efficiency`, `facility_power`;
- the multiphase regulator: `phase_ripple`, `summed_ripple`, `max_slew`, `load_line`;
- the PDN: `target_impedance`, `resonance`, `first_droop_undamped`, `sheet_resistance`, `plane_path_loop`, `storage_capacitance`.

The two netlists:

- `multiphase.cir` drives four 100 nH inductors from ideal 0–12 V pulse sources shifted by a quarter period, into an output held at 0.8 V, and measures one phase's ripple and the ripple of their sum.
- `pdn.cir` models Example 22-10.6: a stiff 0.8 V source, 2 pH of package inductance, and 20 µF of die capacitance with 0.1 mΩ of ESR. An AC run finds the impedance peak seen from the die; a transient run applies a 100 A step with a 10 ps edge and measures the first droop.

## Procedure

1. **Interleaving.** *Predict* one phase's ripple and the four-phase sum from §3.4. Run `ngspice -b multiphase.cir` (Part 1).
2. **Phase count.** *Predict* which phase counts cancel the ripple completely at $D$ = 1/15, then plot the summed ripple for 1 to 24 phases (Part 2).
3. **The package resonance.** *Predict* the resonant frequency and the impedance peak (about $Z_0^2/R_{ESR}$ for light damping) and the first droop. Run `ngspice -b pdn.cir` (Part 3).
4. **Damping.** Sweep the ESR from 0 to 0.5 mΩ and plot the first droop (Part 4). *Predict* first: does more resistance always help?

## Expected results

- **Part 1.** One phase ripples by 7.47 A; the four-phase sum by 5.87 A at 4 MHz (Example 22-10.4). At this low duty cycle, interleaving four phases cancels only a fifth of the ripple; its main gift is the fourfold ripple frequency.
- **Part 2.** The sum cancels completely when $ND$ is an integer: at 15 phases (and 30, 45, …) for $D$ = 1/15.
- **Part 3.** The impedance peaks at **1.05** mΩ near 25.3 MHz, close to the estimate $Z_0^2/R_{ESR}$ = **1.00** mΩ and more than three times the 316 µΩ characteristic impedance. The first droop is 26.5 mV about 7 ns after the step (Example 22-10.6).
- **Part 4.** The droop is 31.6 mV with no ESR, falls to a minimum of **25.6** mV at an ESR of **0.17** mΩ, about half of $Z_0$, and rises again beyond it: at 0.5 mΩ the instant $\Delta I\,R_{ESR}$ step alone is 50 mV. Power-integrity engineers choose capacitor ESR, or add damping resistance, near this optimum.

## Discussion

1. **Why hold the output at a fixed 0.8 V in the interleaving netlist?** It isolates the inductor ripple from the output capacitor's response, so the measured ripple is exactly what the capacitor will have to absorb.
2. **Why does the impedance peak exceed $Z_0$?** At resonance the inductor and capacitor exchange energy and only the ESR dissipates it; the parallel resonance's impedance is $Q$ times $Z_0$, with $Q = Z_0/R_{ESR}$ for light damping.
3. **Why does too much ESR hurt?** The capacitor can then not deliver the step current without an immediate $\Delta I\,R_{ESR}$ drop. The best damping balances the instant resistive drop against the ringing.

## Optional hardware

On a processor or FPGA evaluation board with a programmable load (or a test pattern that toggles a large block), probe the core rail at the package's sense points with a short ground spring and a 1 GHz oscilloscope. Trigger on the load step and measure the first droop; then disable some on-board decoupling capacitors (on a board you can rework) and watch the droop grow. Many controller evaluation boards also allow the load line to be set over PMBus.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-10.a | impedance peak seen from the die | 1.05 | mΩ |
| Lab 22-10.b | estimate Z0²/R_ESR | 1.00 | mΩ |
| Lab 22-10.c | minimum first droop over ESR | 25.6 | mV |
| Lab 22-10.d | ESR at the minimum | 0.17 | mΩ |
