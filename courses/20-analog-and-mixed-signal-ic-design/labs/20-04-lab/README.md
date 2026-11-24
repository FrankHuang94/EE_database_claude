# Lab 20-04 · An LDO across Load, Capacitor and Supply Ripple

Chapter: [20-04 · Low-Dropout Regulators](../../chapters/20-04-ldo-regulators.md)

## Objective

- Size a PMOS pass device for a dropout specification, with the charge-based model and a velocity-saturation correction.
- See the loop's crossover and phase margin move with load current and output capacitance, and confirm them in ngspice.
- Compare supply rejection with a gate driver that tracks the input and one referenced to ground, and confirm it in ngspice.
- Simulate a large load step with the nonlinear pass device, and see how a smaller output capacitor changes the dip.
- See what a slower error amplifier costs in margin and in supply rejection.

## Background

The running design: a T130 PMOS pass device ($L$ = 0.15 µm, $W$ = 1.877 mm for 150 mV of dropout at 100 mA from 1.35 V), $V_{out}$ = 1.2 V from $V_{REF}$ = 0.6 V (β = 0.5), an error amplifier with $g_{ma}$ = 1 mS, $R_a$ = 100 kΩ and $C_a$ = 0.2 pF, a gate buffer with $g_{mb}$ = 2 mS driving $C_g$ = 1.614 pF, a 1.2 MΩ divider, and a 1 µF output capacitor with 5 mΩ ESR. The loop gain is

$$
L(s) = \frac{A_{EA}\,\beta\,g_{mp}\,Z_{out}(s)}{(1 + s/p_a)(1 + s/p_g)}
$$

(chapter §3.4), and the supply rejection is $1/\text{PSRR} = [g_{mp}(1 - k) + g_{ds}]Z_{out}/(1 + L)$ (§3.5).

Files:

- `ldo.py`: the PMOS model (`PMOS`), `size_pass_device`, `operating_point`, the `LDO` class (loop gain, output impedance and PSRR as functions of $s$), `margins`, a linear step response (`load_step_droop`) and a nonlinear load-step simulation (`load_step_nonlinear`).
- `ldo_loop.cir`: the loop broken at the error amplifier's input, at 100 µA and 100 mA with 1 µF, and at 100 mA with 0.1 µF.
- `ldo_psrr.cir`: the closed loop with a 1 V ripple on the input, at 100 mA with $k$ = 1 and $k$ = 0, and at 100 µA with $k$ = 1.
- `20-04-ldo-lab.ipynb`: the procedure below.

## Procedure

1. **Sizing.** Predict how much wider the pass device must be for 100 mV of dropout from a 1.3 V input instead of 150 mV from 1.35 V. Size it (Part 1).
2. **Stability across load.** Predict whether the phase margin is worst at light or full load. Plot $L(j\omega)$ at 100 µA, 1 mA, 10 mA and 100 mA, list the crossovers and margins, and run `ngspice -b ldo_loop.cir` (Part 2).
3. **Supply rejection.** Predict the DC PSRR at 100 mA with $k$ = 1 and $k$ = 0. Plot PSRR from 1 Hz to 1 GHz and run `ngspice -b ldo_psrr.cir` (Part 3).
4. **Load steps.** Predict the dip for a step from 100 µA to 100 mA (1 ns edge). Run the nonlinear simulation from 100 µA, 1 mA and 10 mA, then from 100 µA with $C_L$ = 0.1 µF (Part 4).
5. **A slower error amplifier.** Set $C_a$ = 2 pF. Predict the full-load margin and the PSRR at 1 MHz, then compute them (Part 5, Problem 20-04.14).

## Expected results

- **Part 1.** The width grows to **2.745** mm, 1.46 times the original: lower gate drive and a smaller $V_{SD}$ both cost current per micrometer.
- **Part 2.** Crossovers of 22.5 kHz, 169 kHz, 780 kHz and 2.39 MHz with margins of 89.9°, 89.1°, 85.8° and 77.5° (Example 20-04.4). ngspice agrees, and gives 13.0 MHz and 31.2° with 0.1 µF at full load.
- **Part 3.** 45.6 dB ($k$ = 1) and 32.0 dB ($k$ = 0) at DC and full load, 64.6 dB at light load (Example 20-04.5). The curves rise above the crossover, where the output capacitor shorts the ripple.
- **Part 4.** From 100 µA the output reaches −13.43 mV at 0.304 µs and settles at −13.41 mV (Example 20-04.6). From 1 mA the minimum is **−11.62** mV, and from 10 mA **−8.50** mV: a smaller change of $V_{SG}$ means a smaller regulation error. With 0.1 µF the loop rings (31° of margin at full load): the output reaches **−24.0** mV at **31.6** ns before settling to the same −13.41 mV.
- **Part 5.** The full-load margin falls to 34.6° and the 1 MHz PSRR to 37.9 dB (Problem 20-04.14).

## Discussion

1. **Why does a smaller capacitor make the dip worse, when the DC error is the same?** The 0.1 µF loop has 31° of phase margin at full load, so its step response overshoots: the dip is the regulation error plus the ringing. The 1 µF loop has 77.5°, and its dip is essentially the regulation error (chapter §3.6).
2. **What does the simulation leave out?** The error amplifier and gate buffer are linear: a real buffer has finite output current and slews when the gate must move hundreds of millivolts, and the capacitor's ESR and inductance add an immediate step at the edge. Both make real dips larger.
3. **Why is the PSRR netlist's $C_g$ connected to $k\,v_{in}$?** In the chapter's model the gate carries the fraction $k$ of the ripple at all frequencies, which requires the gate's capacitance to be referenced to the same node as the driver. A real driver tracks the input only up to its own bandwidth.

## Optional hardware

An adjustable LDO evaluation module (any vendor's) with a programmable electronic load shows Part 2 and Part 4 directly. Step the load between 1 mA and its full rating and watch the output on an oscilloscope with a short ground spring, once with the recommended output capacitor and once with a tenth of it. The ringing in the second case is the low phase margin. A function generator coupled to the input through a large capacitor (or an injection transformer) and an oscilloscope's FFT show the PSRR at a few frequencies.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-04.a | width for 100 mV dropout | 2.745 | mm |
| Lab 20-04.b | minimum, step from 1 mA | −11.62 | mV |
| Lab 20-04.c | minimum, step from 10 mA | −8.50 | mV |
| Lab 20-04.d | minimum with 0.1 uF | −24.0 | mV |
| Lab 20-04.e | time of the minimum with 0.1 uF | 31.6 | ns |
