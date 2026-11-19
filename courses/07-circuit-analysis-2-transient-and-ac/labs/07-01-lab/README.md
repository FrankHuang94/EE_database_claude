# Lab 07-01 · Capacitors and Inductors

**Chapter:** [07-01](../../chapters/07-01-capacitors-and-inductors.md) · **Notebook:** [07-01-storage.ipynb](07-01-storage.ipynb) · **Time:** about 60 minutes (plus 60 minutes for the optional hardware part)

## Objective

1. See the element laws act on waveforms: a capacitor's current follows the slope of its voltage, an inductor's voltage the slope of its current.
2. Show that charge redistribution between capacitors loses the same energy whatever the resistance.
3. Measure the inductive kick with and without a flyback diode.
4. Sweep a real capacitor's impedance and see what paralleling does and does not change.

## Background

Chapter sections 3.1 to 3.7 and Examples 07-01.1 to 07-01.6. You need Python with NumPy, SciPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips them.

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-01-storage.ipynb](07-01-storage.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [storage.cir](storage.cir) | Examples 07-01.1 to 07-01.6 and Problems 07-01.3, 07-01.6, 07-01.7, 07-01.11 and 07-01.14 in ngspice: piecewise-linear sources, a switch and a diode, an AC sweep of the real-capacitor model, and op-amp integrator and differentiator | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **Waveforms (Part 1).** *Predict first:* sketch the capacitor current of Example 07-01.1 and the inductor voltage of Example 07-01.2.
2. **Charge sharing (Part 2).** *Predict first:* the energy lost and the peak current with 1 Ω and with 0.01 Ω.
3. **The kick (Part 3).** *Predict first:* the coil voltage when the current is forced to zero in 1 µs, and with a flyback diode.
4. **Impedance (Part 4).** *Predict first:* the self-resonant frequency and the minimum impedance, for one capacitor and for 20 in parallel.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | element laws | 50 mA and −100 mA in the capacitor; 4.7 V and −3.133 V across the inductor |
| 2 | charge sharing | 250 µJ lost for both resistances; peak currents 10 A and 1000 A |
| 3 | kick | −5000 V with no path; the switch sees about 12.7 V with a flyback diode |
| 4 | impedance | self-resonance 2.251 MHz for one and for 20 in parallel; minimum 5 mΩ and 0.25 mΩ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-01.a | energy lost in charge sharing | 250 | µJ |
| Lab 07-01.b | peak current with 1 Ω | 10 | A |
| Lab 07-01.c | peak current with 0.01 Ω | 1000 | A |
| Lab 07-01.d | self-resonant frequency, one or twenty | 2.251 | MHz |
| Lab 07-01.e | minimum impedance, one capacitor | 5 | mΩ |
| Lab 07-01.f | minimum impedance, twenty in parallel | 0.25 | mΩ |
| Lab 07-01.g | energy left after a three-way share | 167 | µJ |
| Lab 07-01.h | self-resonance with 1 µF parts | 7.118 | MHz |
| Lab 07-01.i | ESL for a 10 MHz self-resonance at 10 µF | 25.33 | pH |

## Discussion questions

1. Part 2's energy loss does not depend on the resistance. Where does the energy go when the resistance is made extremely small?
2. Why does paralleling 20 identical capacitors not move the self-resonant frequency?
3. A relay driven through a flyback diode releases slowly. Why, and what would make it release faster?
4. In Part 1, the capacitor current jumps at the corners of the voltage waveform. Could the voltage itself have corners in a real circuit?

<details><summary>Answers to the discussion questions</summary>

1. Into the shrinking resistance as a larger, shorter current pulse, always the same total; with essentially no resistance the wiring's inductance makes the charges oscillate, and the energy leaves as radiation and in sparks. The loss is set by charge conservation, not by the dissipating element.
2. Paralleling divides the total ESL by 20 and multiplies the capacitance by 20, so the product $LC$, and with it $f_{SR} = 1/(2\pi\sqrt{LC})$, is unchanged. Only the impedance level falls, by 20, at every frequency.
3. The diode clamps the coil voltage to about −0.7 V, so the current decays slowly through the coil's own resistance (time constant $L/R$). A higher clamp voltage (a Zener or TVS in series with the diode) makes $di/dt = -V_{clamp}/L$ larger and releases the relay faster, at the cost of a higher voltage on the switch (Problem 07-01.8).
4. Only approximately. A corner needs an instantaneous jump in current, which the circuit's own inductance forbids; real waveforms have rounded corners whose sharpness is set by the source and wiring. The ideal piecewise-linear source is a model.

</details>

## Optional hardware version

Charge a 100 µF electrolytic capacitor to 5 V through 1 kΩ from a bench supply (observe polarity), disconnect the supply, and record its voltage every few seconds on a DMM to see its leakage (a 10 MΩ meter also discharges it with a 1000 s time constant, so note which effect dominates). Then, with a 12 V relay and a small NPN transistor or logic MOSFET, observe the coil's turn-off voltage on an oscilloscope without and then with a 1N4148 diode across the coil (cathode to the supply), keeping in mind that without the diode the spike is set by $L\,di/dt$, not by the supply, and can destroy a small transistor at any supply voltage: run that case only with a spare part or a MOSFET rated for avalanche energy.
