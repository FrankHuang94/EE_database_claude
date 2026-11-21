# Lab 18-09 · Current Budgets, Sleep Modes and Battery Pulses

Chapter: [18-09 · Ultra-Low-Power Design](../../chapters/18-09-ultra-low-power-design.md)

## Objective

- Build duty-cycled current budgets and check the averages against a sum over every event of a day (`simulate_day`).
- Find the crossovers between sleep modes from their currents and wake-up costs.
- Compare running fast and sleeping with running slowly, with and without voltage scaling.
- Size a reservoir capacitor for a coin cell's pulse loads and confirm it in ngspice.

## Background

Average current is $I_{sleep} + \sum I_kt_k/T$ (§3.3); a deeper mode pays after $Q_{tr}/\Delta I$ (§3.2); at a fixed voltage the charge per task falls as the clock rises (§3.4); a capacitor $C$ limits a pulse's droop to $IR_{int}(1 - e^{-t/R_{int}C})$ (§3.6).

## Files

- `ulp.py`: `average_current`, `battery_life_hours`, `break_even_time`, `charge_per_task`, `dynamic_energy_ratio`, `battery_current_ldo`, `battery_current_buck`, `droop_no_cap`, `droop_with_cap`, `cap_for_droop`, `simulate_day`.
- `coin_cell_pulse.cir`: a 3.0 V cell with 100 Ω internal resistance and an 8 mA, 2 ms burst, with and without 100 µF (Example 18-09.5).
- `18-09-ulp-lab.ipynb`: the guided notebook.

## Procedure

1. **Budget.** For Example 18-09.1, predict the average current and battery life if advertising slows to once every 2 s; compute with `average_current`, then simulate a day with `simulate_day` and compare the charge.
2. **Modes.** Plot charge per idle period against idle time (10 µs to 100 s) for the sleep, stop and shutdown modes of Example 18-09.2; read off the crossovers.
3. **Race.** Plot the charge per second of Example 18-09.3 against clock frequency from 2 to 48 MHz; then let the clock be at most 24 MHz at 1.2 V with the per-MHz and fixed currents both scaled by $1.2/1.8$, and find the best operating point. The linear factor models a core fed by an internal LDO, whose battery charge per cycle falls as $V$, not $V^2$ (chapter §3.4); scaling the fixed current the same way is a simplifying assumption (regulator bias may not scale, while leakage usually falls faster).
4. **The burst.** Predict the droop with 47, 100 and 220 µF; run `ngspice -b coin_cell_pulse.cir` and `droop_with_cap`.
5. **Self-discharge.** Compare battery lives with 0%, 1% per year and 3% per month of self-discharge for nodes averaging 2, 20 and 200 µA on 1000 mAh.

## Expected results

- Part 1: advertising every 2 s gives 16.5 µA and 556 days; the day's simulated charge matches the budget to within the simulation's rounding.
- Part 2: crossovers at 0.125 ms (sleep to stop) and 1.38 s (stop to shutdown).
- Part 3: at 1.8 V the charge falls monotonically with frequency (70.3 µC at 48 MHz); with the 1.2 V range capped at 24 MHz the best point is the top of the low-voltage range, 53.0 µC, which beats 48 MHz at 1.8 V.
- Part 4: 277, 145 and 70 mV with 47, 100 and 220 µF (the netlist confirms 100 µF); 0.80 V without.
- Part 5: at 2 µA, a 3% per month self-discharge dominates (about 42 µA equivalent) and cuts the life from 57 to 2.6 years; at 200 µA it shortens the life by under a fifth.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-09.a | average current, advertising every 2 s | 16.5 | µA |
| Lab 18-09.b | battery life, advertising every 2 s | 556 | days |
| Lab 18-09.c | charge per second at 24 MHz, 1.2 V | 53.0 | µC |
| Lab 18-09.d | droop with 47 µF | 277 | mV |
| Lab 18-09.e | droop with 220 µF | 70 | mV |

## Discussion

1. Why does the event simulation of a day give the same charge as the budget formula, and when would it not?
2. In Part 3, why is the best point at the top of the low-voltage range rather than at its bottom?
3. Why might a designer still choose 220 µF when 100 µF meets the droop target?

## Answers

1. Charge is additive: integrating a piecewise-constant current over a day gives the sum of each phase's current times its total duration. They differ when phases overlap (two activities at once draw more than either), when the simulation's time step truncates phases, or when currents depend on the battery's state.
2. Within one voltage range, the race-to-idle argument holds: the fixed current is paid for less time at a higher clock. So the best point in each range is its maximum clock, and the comparison is only between ranges.
3. For margin: the cell's internal resistance rises further at end of life and in deeper cold, capacitors lose capacitance with DC bias (ceramics) and age, and bursts can be longer than nominal (retransmissions). The cost is board area and leakage current.

## Optional hardware

Measure a development board's current in each power mode with a power analyzer or a source-measure unit (a multimeter on its microamp range will usually upset the supply during wake-ups), then remove pull-ups, dividers and LEDs one by one and watch the sleep current fall to the MCU's own figure.
