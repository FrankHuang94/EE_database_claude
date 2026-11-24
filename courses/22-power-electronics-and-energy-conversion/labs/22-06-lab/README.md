# Lab 22-06 · Switch Losses: the Hard Turn-On, ZVS Transitions and Silicon against GaN

Chapter: [22-06 · Converter Losses and Wide-Bandgap Switches](../../chapters/22-06-converter-losses-and-wide-bandgap.md)

## Objective

- Confirm in ngspice that a hard turn-on in a half bridge dissipates $Q_{oss}V$, not $E_{oss}$, even with a strongly nonlinear output capacitance.
- Measure ZVS transition times for GaN-like and superjunction-like output capacitances.
- Build the loss budget of a 48 V buck against switching frequency for silicon and GaN.
- Find the device size that minimizes conduction plus gate-drive loss.

## Background

`losses.py` collects the chapter's formulas:

- loss mechanisms: `conduction`, `overlap`, `coss_hard_turn_on`, `recovery`, `gate_drive`, `dead_time`;
- a nonlinear output capacitance $C_0/(1 + v/V_0)^m$: `coss_junction`, `qoss_junction`, `eoss_junction`;
- sizing: `optimal_resistance`, `minimum_loss`, `baliga_relative`;
- temperature: `junction_temperature`, `runaway_current`;
- soft switching: `zvs_transition_time`, `zvs_min_current`, `llc_magnetizing_peak`.

The two netlists:

- `coss_loss.cir` gives each switch of a 400 V half bridge the depletion capacitance of a reverse-biased, non-conducting junction, $C(v) = 2\ \text{nF}/(1 + v/2\ \text{V})^{0.9}$, which falls steeply with voltage as a superjunction's does. The high-side switch (0.5 Ω channel) closes onto it, and the netlist integrates $i^2R$ in the channel. A linear twin with the same charge, $C = Q_{oss}/V$ = **69.95** pF, runs alongside.
- `zvs.cir` opens the high side of a 400 V half bridge while 2 A flows out of the switch node, with linear capacitances equal to $C_{o(tr)}$ of the chapter's GaN (88 pF) and superjunction (1212 pF) parts, and measures how long the node takes to reach 0 V.

## Procedure

1. **The hard turn-on.** *Predict* $Q_{oss}$, $E_{oss}$, $Q_{oss}V$ and $2E_{oss}$ for the junction model at 400 V, and which one the channel dissipates. Run `ngspice -b coss_loss.cir` (Part 1).
2. **ZVS transitions.** *Predict* both transition times of Example 22-06.7, then run `ngspice -b zvs.cir` (Part 2).
3. **Loss against frequency.** In the notebook, rebuild Example 22-06.6's budget from 100 kHz to 2 MHz for both technologies and find where each reaches 2% of 240 W (Part 3).
4. **Device size.** Sweep $R_{DS(on)}$ for Example 22-06.4 and confirm the optimum (Part 4).

## Expected results

- **Part 1.** $Q_{oss}$ = **27.98** nC and $E_{oss}$ = **2.42** µJ at 400 V. The channel dissipates **11.19** µJ, equal to $Q_{oss}V$, which is **4.62** times $E_{oss}$ and more than twice $2E_{oss}$ = **4.84** µJ. The linear twin dissipates the same 11.19 µJ: the hard turn-on loss depends only on the charge moved.
- **Part 2.** 35.2 ns for GaN and 484.8 ns for the superjunction (Example 22-06.7). ngspice measures the time to 0.5 V, a fraction of a nanosecond less.
- **Part 3.** Silicon reaches 2% at about 208 kHz and GaN at about 544 kHz (Problem 22-06.12).
- **Part 4.** The optimum falls where conduction and gate loss are equal: 2.09 mΩ and 1.26 W for silicon at 1 MHz (Example 22-06.4).

## Discussion

1. **Why is the loss $Q_{oss}V$ whatever the capacitance's shape?** The supply delivers charge $Q_{oss}$ at voltage $V$, energy $Q_{oss}V$, and at the end of the transition both capacitances together store the same total energy as at the start (one $E_{oss}$ moved from one switch to the other). Energy conservation then puts all of $Q_{oss}V$ into the channel.
2. **Why use $C_{o(tr)}$ for ZVS timing but $C_{o(er)}$ for stored energy?** A current source moves charge, so time depends on charge; stored energy depends on the integral of $vC(v)$.
3. **What would a real circuit add?** Package and loop inductance ring with $C_{oss}$, the channel resistance changes during the transition, and the gate driver takes time. Double-pulse tests measure these together.

## Optional hardware

GaN and SiC evaluation boards built as half-bridge double-pulse testers are widely sold. With a fast oscilloscope and a current shunt, the turn-on energy can be measured directly and compared with $Q_{oss}V$ plus the overlap term, as a function of current.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-06.a | output charge at 400 V | 27.98 | nC |
| Lab 22-06.b | stored energy at 400 V | 2.42 | µJ |
| Lab 22-06.c | energy dissipated at the hard turn-on | 11.19 | µJ |
| Lab 22-06.d | twice the stored energy | 4.84 | µJ |
| Lab 22-06.e | Q_oss·V over E_oss | 4.62 | |
| Lab 22-06.f | linear twin's capacitance | 69.95 | pF |
