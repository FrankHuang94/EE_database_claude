# Lab 19-06 · Where the Power Goes

Chapter: [19-06 · Power and Low-Power Design](../../chapters/19-06-power-and-low-power-design.md)

## Objective

- Measure an inverter's switching charge and short-circuit charge in ngspice and match them to $C_LV_{DD}$ and Veendrick's formula.
- Explore leakage against threshold, temperature and stacking.
- Compare DVFS and parallelism, and find the minimum-energy supply of subthreshold logic.

## Background

Each full switching cycle costs $C_LV_{DD}^2$, so $P_{dyn} = \alpha CV_{DD}^2f$ (§3.1). An unloaded inverter driven by ramps of duration τ draws $\beta\tau(V_{DD} - 2V_T)^3/(24V_{DD})$ per transition (§3.2). Subthreshold leakage falls tenfold per subthreshold slope of threshold, and two stacked off transistors leak far less than one because of DIBL (§3.3). Lowering the supply with the frequency, or running parallel copies slower, saves energy (§3.4). In subthreshold, the energy per operation $V^2[\alpha + L_de^{-V/(nV_{th})}]$ has a minimum at a few hundred millivolts (§3.6).

Files:

- `power.cir`: an inverter charging 10 fF (circuit A) and an unloaded inverter driven by 50 ps ramps (circuit B), integrating the supply current.
- `power.py`: `dynamic_power`, `short_circuit_power_veendrick`, `short_circuit_charge_numeric`, `subthreshold_current`, `stack_leakage_ratio`, `leakage_factor_for_vt_shift`, `alpha_delay`, `supply_for_slowdown`, `energy_per_op`, `minimum_energy_supply` and `break_even_time`.
- `19-06-power-lab.ipynb`: the procedure below.

## Procedure

1. **Switching charge.** Predict the charge drawn while the inverter charges 10 fF from 0 to 1.2 V; run `ngspice -b power.cir` (circuit A) and Part 1.
2. **Short-circuit charge.** Predict the charge per period for 50 ps ramps; compare circuit B with Veendrick's formula, then sweep the ramp time in Part 2.
3. **Leakage.** Plot leakage against threshold shift and the stack-effect ratio against η (Part 3).
4. **DVFS and parallelism.** Plot the supply, power and energy per operation against the frequency fraction (Part 4).
5. **Minimum energy.** Plot energy per operation against supply for Example 19-06.6 and find the minimum (Part 5).

## Expected results

- Part 1: 12.0 fC drawn from the supply, energy 14.4 fJ, of which 7.2 fJ is stored on the capacitor at the end of the rise.
- Part 2: 0.0868 fC per 1 ns period (two transitions), the same in ngspice and Veendrick's formula; the charge grows linearly with ramp time, and at 200 ps it is 0.347 fC per period.
- Part 3: 12.9 times the leakage per 100 mV at 90 mV/decade; the stack ratio rises from 1.83 (η = 0) to 15.9 (η = 0.1) and 164.7 (η = 0.2).
- Part 4: half the frequency at 0.611 V (power 0.187, energy 0.373); a third at 0.518 V; a quarter at 0.477 V.
- Part 5: the minimum at 201 mV, with 33% of the energy in leakage; a local maximum near 70 mV marks where the model stops applying.

## Discussion

1. Why does the charge in circuit A not depend on the transistors' strength?
2. Why does Veendrick's formula hold exactly for circuit B but only as a bound for a loaded inverter?
3. Why is the stack effect so sensitive to η?
4. Why should a subthreshold design not simply run at the supply that minimizes the model's energy?

**Answers.**

1. The supply must deliver the charge $C_LV_{DD}$ that ends up on the capacitor, whatever the current waveform; the transistor only sets how fast.
2. Unloaded, the output follows the static curve, so the current at every instant is the saturation current of the transistor turning off. With a load, the output lags, and the transistor turning off sees less drain voltage and conducts less (19-02 §3.6).
3. The single device's leakage carries a factor $e^{\eta V_{DD}/(nV_{th})}$ from DIBL that the stacked device almost loses, and that factor is exponential in η.
4. The model ignores variation, SRAM's higher minimum voltage and the speed the application needs; real designs add margin, usually ending up a little above the minimum-energy point (§3.6).

## Optional hardware

Measure the supply current of a CD4069 driving a capacitor load with a square wave at several frequencies and two supplies (5 V and 10 V): the current grows linearly with frequency, and its slope, $CV_{DD}$, doubles with the supply. A small series resistor in the supply and an oscilloscope show the short-circuit spikes with slow input edges.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 19-06.a | charge drawn while charging 10 fF | 12.0 | fC |
| Lab 19-06.b | short-circuit charge per period, 50 ps ramps | 0.0868 | fC |
| Lab 19-06.c | energy drawn | 14.4 | fJ |
| Lab 19-06.d | energy stored at the end of the rise | 7.2 | fJ |
| Lab 19-06.e | short-circuit charge per period, 200 ps ramps | 0.347 | fC |
| Lab 19-06.f | local maximum of the energy model | 70 | mV |
