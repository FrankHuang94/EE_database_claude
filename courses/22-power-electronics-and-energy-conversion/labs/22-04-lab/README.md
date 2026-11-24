# Lab 22-04 · Isolated Converters: a Flyback, a Forward Converter and the Cost of Leakage

Chapter: [22-04 · Isolated Converters: Flyback and Forward](../../chapters/22-04-isolated-converters.md)

## Objective

- Build a flyback from coupled inductors and confirm its ratio and its switch's off-state voltage.
- Build a forward converter with a three-winding transformer and watch the tertiary reset the core to zero magnetizing current every cycle.
- Compute the RCD clamp's loss against leakage and clamp voltage.
- Tabulate the insulation limits of a reinforced barrier: clearance with altitude, creepage by material group, and the Y-capacitance that the touch-current limit allows.

## Background

`isolated.py` collects the chapter's formulas:

- flyback: `flyback_duty`, `flyback_switch_voltage`, `flyback_dcm_power`, `flyback_boundary_design`, `flyback_dcm_boundary_current`, `clamp_energy`;
- forward: `forward_duty`, `forward_max_duty`, `forward_switch_voltage`;
- core flux: `flux_swing`;
- insulation: `y_cap_current`, `y_cap_limit`.

ngspice models a transformer as coupled inductors (`K` elements). The netlists use unity coupling, so they have no leakage; the clamp is studied in the notebook.

- `flyback.cir` runs Example 22-04.1's 150 V to 20 V flyback ($n$ = 6.4, 500 µH primary, 100 kHz) and samples the drain in the middle of an off-time.
- `forward.cir` runs a 48 V to 5 V forward converter with 3:1:3 windings and tertiary reset. It samples the drain in the middle of the reset interval and checks that the primary (magnetizing) current is back to zero before the next on-time.

## Procedure

1. **Flyback.** *Predict* the duty cycle, the output and the drain voltage while the switch is off, then run `ngspice -b flyback.cir` (Part 1).
2. **Forward.** *Predict* the output, the drain voltage during reset and when reset ends. Run `forward.cir` and plot the drain voltage and primary current over a period in the notebook (Part 2).
3. **Leakage.** *Predict* the clamp loss for 1%, 2% and 5% leakage in Example 22-04.2's flyback with a 200 V clamp, then plot clamp loss against clamp voltage (Part 3).
4. **Insulation.** *Predict* the Y-capacitance limit at 264 V for 50 and 60 Hz mains, and the reinforced clearance at sea level and at 5000 m (Part 4).

## Expected results

- **Part 1.** $D$ = 0.460, an output within 1% of 20 V (the near-ideal diode drops about 15 mV), and 278 V on the drain during the off-time, the input plus the 128 V reflected voltage.
- **Part 2.** An output within 1% of 5 V and **96** V on the drain during reset, twice the input. The primary current returns to zero before each on-time.
- **Part 3.** With 2% leakage and a 200 V clamp, the clamp absorbs 3.93 W, 5.6% of the input (Example 22-04.5). It scales linearly with leakage, to **1.96** W at 1% and **9.81** W at 5%, and falls as the clamp voltage rises.
- **Part 4.** About 5.02 nF at 60 Hz and **6.03** nF at 50 Hz for 0.5 mA; 3.8 mm of reinforced clearance at sea level and 5.62 mm at 5000 m (IEC 62368-1 basis).

## Discussion

1. **Why does the flyback's drain sit at exactly 278 V?** With the switch off, the secondary is clamped at the output plus the diode drop, and the primary reflects it multiplied by $n$. Unity coupling means no leakage spike, so the drain is simply $V_{in} + nV$. A real transformer adds a spike set by the clamp.
2. **Why does the forward converter's drain step down after reset?** Once the magnetizing current reaches zero, the tertiary diode stops conducting and no winding drives the core. In this idealized circuit the drain returns to the input; in a real one it rings with the drain capacitance. That ring is what quasi-resonant controllers use for valley switching.
3. **Why is the clamp loss larger than the leakage energy?** During the clamp interval the leakage inductance sees only $V_c - V_R$, so the clamp absorbs charge at the higher voltage $V_c$, which includes energy that the magnetizing inductance would otherwise have sent to the output.

## Optional hardware

An inexpensive isolated flyback module (for example a 5 V, 1 W isolated DC-DC converter) and an oscilloscope show the switch node's plateau at $V_{in} + nV$, the leakage spike and the ring after the secondary current stops. Measuring the plateau and the input voltage gives the reflected voltage and so the turns ratio, without opening the part.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 22-04.a | forward drain voltage during reset | 96 | V |
| Lab 22-04.b | clamp power at 1% leakage | 1.96 | W |
| Lab 22-04.c | clamp power at 5% leakage | 9.81 | W |
| Lab 22-04.d | Y-capacitance limit at 50 Hz | 6.03 | nF |
