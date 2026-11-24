# Lab 22-01 · Power Conversion Principles: Linear Regulators, Charging Loss, an Ideal Buck and Loss Models

Chapter: [22-01 · Power Conversion Principles](../../chapters/22-01-power-conversion-principles.md)

## Objective

- See a linear regulator sit at its $V_{out}/V_{in}$ ceiling at heavy load and fall below it when quiescent current matters.
- Show by simulation that charging a capacitor from a voltage source loses ½CV² whatever the resistance, and that a staircase recovers most of it.
- Build an ideal synchronous buck, confirm $V_{out} = DV_{in}$ and its power balance, and measure its ripple against a first-harmonic estimate.
- Plot a converter's efficiency curve from a loss model, and see what PFM and a second phase do to it.
- Recompute power-density and hold-up numbers from published dimensions.

## Background

`power.py` collects the chapter's formulas:

- efficiency and chains: `loss_from_efficiency`, `chain_efficiency`, `chain_losses`;
- linear regulators: `ldo_efficiency`, `buck_input_current`;
- capacitor losses: `charge_loss`, `share_loss`;
- the buck: `buck_pss` (the exact periodic steady state, by matrix exponentials of the two switched circuits) and `switch_node_harmonic`;
- the loss model: `model_loss`, `model_efficiency`, `peak_efficiency_current`, `shed_current`, `phased_loss`;
- density and hold-up: `density_w_per_in3`, `thermal_density_limit`, `holdup_capacitance`.

The three netlists:

- `ldo.cir` builds two identical PMOS-pass regulators (an ideal error amplifier, a 25 nA quiescent-current source, loads of 180 Ω and 1.8 MΩ) and reports their efficiencies from the simulated input current.
- `cap_charge.cir` charges three 10 µF capacitors to 5 V: through 1 Ω, through 100 Ω, and from a four-step staircase. It integrates $i^2R$ in each resistor.
- `buck.cir` is the synchronous buck of Example 22-01.4 with 1 mΩ switches. It reports the average output, the peak-to-peak ripple and the average input current over the last ten periods.

## Procedure

1. **Leverage.** *Predict* the loss per kilowatt delivered at 90, 96 and 99% efficiency; then plot loss against efficiency (Part 1).
2. **A linear regulator.** *Predict* the efficiency from 3.6 V to 1.8 V with 25 nA of quiescent current at 10 mA and at 1 µA. Plot efficiency against load for three quiescent currents, then run `ngspice -b ldo.cir` (Part 2).
3. **Charging loss.** *Predict* the energy lost charging 10 µF to 5 V through 0.1, 1 and 100 Ω and in four steps. Integrate the ODE, then run `cap_charge.cir` (Part 3).
4. **Switching plus filtering.** *Predict* the buck's average output and ripple. Compute the periodic steady state, compare it with the first-harmonic estimate, repeat at 1 MHz with half the L and C, and run `buck.cir` (Part 4).
5. **Loss model.** *Predict* the peak-efficiency load and the phase-adding loads for Example 22-01.5's converter; then plot the three efficiency curves (Part 5).
6. **Density and hold-up.** *Predict* the densities and hold-up capacitances of Examples 22-01.6 and 22-01.7, and the stage losses of Example 22-01.8 (Part 6).

## Expected results

- **Part 1.** The loss is 111.11, 41.67 and 10.10 W per kW delivered at 90, 96 and 99%.
- **Part 2.** The regulator is at its 50% ceiling at 10 mA and at 48.78% at 1 µA. ngspice gives 0.50001 and 0.48781: its error amplifier holds the output at 1.80003 V, which is why the first is a hair above 50%. The buck's battery current at 1 µA is 0.625 µA.
- **Part 3.** 125.000 µJ is lost for every resistance, and 31.250 µJ for the staircase; ngspice gives 125.0 µJ for both resistors and 31.25 µJ for the staircase. Sharing between 1 µF capacitors at 5.0 and 4.8 V loses 10.00 nJ.
- **Part 4.** The exact average is 3.3000 V with 120.33 mV of ripple. The inductor ripple is **0.482** A peak to peak, against the small-ripple formula's **0.4785** A (22-02 derives it). The first-harmonic estimate is 118.9 mV, and the 1 MHz design with 5 µH and 0.5 µF gives the same 120.33 mV. ngspice, with 1 mΩ switches and a finite time step, gives 3.2994 V, 120.5 mV and 0.2750 A of input current.
- **Part 5.** Efficiency peaks at **7.07** A at 93.25%; phases 2, 3 and 4 pay above 10.00, 17.32 and 24.49 A. PFM lifts the 0.1 A efficiency from about 40% to about 85%.
- **Part 6.** The densities are 99.9 and 47.9 W/in³, and the thermal limits at 3 W/in³ are 57, 117 and 297 W/in³ for 95, 97.5 and 99% efficiency. The hold-up capacitance is 3.88 mF to 320 V and 3.19 mF to 300 V. The chain's stage losses are 36.1, 29.2, 26.2 and 111.1 W, for 1202.5 W of input.

## Discussion

1. **Why does the ngspice regulator show slightly more than 50% at 10 mA?** Its error amplifier has a finite gain of 10⁵, so the output settles 30 µV above the reference. Output power rises by twice that fraction, while the input current still equals the load current plus 25 nA. The true ceiling is $V_{out}/V_{in}$ for the actual output voltage, and the amplifier shifted the output, not the physics.
2. **Why is the loss the same through 1 Ω and 100 Ω?** The loss is $\int i^2R\,dt$ with $i = (V/R)e^{-t/RC}$. Doubling $R$ halves the peak current (quartering $i^2$) but doubles the time constant and the resistance, so the product does not change: $\tfrac12CV^2$ either way.
3. **Why does the first-harmonic estimate fall slightly short of the exact ripple?** It ignores the higher harmonics, which add a little to the peak-to-peak value, and it uses the unloaded filter. The load damps the filter, which lowers the true attenuation slightly. Both effects are small because the filter attenuates the second harmonic four times more than the fundamental.
4. **Why does the 1 MHz design give exactly the same ripple?** At each new harmonic frequency the halved inductor and capacitor have the same impedances as the old ones at the old frequency, and the load resistance is unchanged. The circuit's response is therefore identical, compressed in time.

## Optional hardware

A low-cost buck evaluation board (any synchronous buck with an enable pin and a light-load mode) and a bench supply with a current display show §3.5 directly. Measure input and output power at loads from a few milliamps to full load, with the light-load mode forced off and then allowed. Plot both efficiency curves. The peak will sit where the board's fixed loss equals its conduction loss, and the light-load mode will lift the low end exactly as the PFM curve in Part 5 does.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-01.a | exact inductor ripple, Example 22-01.4's buck | 0.482 | A |
| Lab 22-01.b | small-ripple formula for the inductor ripple | 0.4785 | A |
| Lab 22-01.c | peak-efficiency load, Example 22-01.5 | 7.07 | A |
