# Lab 07-05 · Sinusoidal Steady State, Phasors and Impedance

**Chapter:** [07-05](../../chapters/07-05-sinusoidal-steady-state-and-impedance.md) · **Notebook:** [07-05-phasors.ipynb](07-05-phasors.ipynb) · **Time:** about 2 hours (plus 1 hour for the optional hardware part)

## Objective

1. Confirm that a circuit driven by a sinusoid settles to the amplitude and phase the phasor solution predicts.
2. See how an LCR meter's series and parallel readings of one capacitor diverge as its losses grow with frequency.
3. Read a phasor diagram as a picture of KVL.
4. Hear (or see) phase: pass a waveform through an all-pass filter that leaves every amplitude unchanged.

## Background

Chapter sections 3.2 to 3.7 and Examples 07-05.1 to 07-05.6. You need Python with NumPy, SciPy and Matplotlib, and ngspice for the simulator checks (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips them.

## Files

| File | What it does | Checks against |
|---|---|---|
| [07-05-phasors.ipynb](07-05-phasors.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [ac.cir](ac.cir) | AC analyses of Example 07-05.2 (1 kHz) and Problem 07-05.5 (50 Hz) | Chapter and solution answer keys |
| [ac2.cir](ac2.cir) | AC analyses of Example 07-05.3 (10 kHz), the all-pass of Example 07-05.6 (3 kHz) and the tissue model of Problem 07-05.13 (50 kHz) | Chapter and solution answer keys |

Each netlist begins with `* EXPECT` lines naming the measurement and the published answer it must reproduce. Run them from the repository root:

```bash
python tools/run_spice.py 07-05
```

## Procedure

1. **Into steady state (Part 1).** *Predict first:* how many periods Example 07-05.2's circuit needs before its node voltages match the phasors to 0.1%. (Hint: find its slowest natural frequency.)
2. **Two readings of one capacitor (Part 2).** *Predict first:* at which frequency do the series and parallel capacitances of Example 07-05.1's capacitor differ by 10%?
3. **The phasor diagram (Part 3).** *Predict first:* how the source-voltage arrow of Example 07-05.4 moves if the load becomes capacitive with the same magnitude of current.
4. **Phase and shape (Part 4).** *Predict first:* whether an all-pass filter changes a square wave's RMS value, its peak, both or neither.
5. **Guided exercise (chapter §5).** Raise the capacitor's ESL from 2 nH to 20 nH. *Predict first:* the series-mode capacitance at 100 kHz and the new self-resonant frequency.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | steady state | the lock-in amplitudes and phases match 7.542 V ∠ −70.33° and 10.80 V ∠ −56.28° |
| 2 | two readings | $C_s$ and $C_p$ agree at 1 kHz and differ by a factor $1 + D^2$ that grows with frequency |
| 3 | phasor diagram | with a capacitive load the reactive drop subtracts and the source voltage can fall below the load voltage |
| 4 | all-pass | RMS unchanged, peak changed (1.333 V to 1.134 V) |
| 5 | larger ESL | see the key |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 07-05.a | series-mode capacitance at 100 kHz with 20 nH ESL | 10.86 | µF |
| Lab 07-05.b | self-resonant frequency with 20 nH ESL | 355.9 | kHz |
| Lab 07-05.c | −90° frequency of the hardware all-pass with 15 nF | 1.061 | kHz |

## Discussion questions

1. Why is a phasor solution useless for an unstable circuit, even though the algebra can be done?
2. In Part 2, why do series and parallel capacitances agree at low frequency?
3. In Part 3, how can a capacitive load raise the voltage at the end of a line above the source voltage?
4. In Part 4, an audio engineer says "the ear is deaf to phase". What does the all-pass result say about where that claim can and cannot hold?

<details><summary>Answers to the discussion questions</summary>

1. The steady state is what remains after the natural response dies out. If a pole is in the right half-plane the natural response grows instead, so the circuit never reaches the computed sinusoid; the phasor answer is a particular solution that nothing converges to.
2. They differ by the factor $1 + D^2$, and $D = \omega C R_{ESR}$ is tiny at low frequency (0.006 at 1 kHz for this part), so the two models describe almost the same thing.
3. A leading current through the line's reactance makes the reactive drop $jX\mathbf{I}$ point partly *against* the load voltage, so the source voltage needed is smaller than the load's. Conversely, a lightly loaded long cable with capacitive charging current shows a rise in voltage toward its far end (the Ferranti effect, [22-12](../../../22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md)).
4. The all-pass leaves every amplitude, and the RMS value, unchanged but changes the waveform's peak and shape. Whether a listener notices depends on the signal and the size of the shifts; what the result shows is that phase changes the waveform, so any system with a peak limit (an amplifier that clips, an ADC's full scale) is not deaf to it.

</details>

## Optional hardware version

With a function generator, two 1% resistors (10 kΩ), a 15 nF film capacitor and a general-purpose op-amp on ±5 V supplies, build the all-pass of chapter §3.7. Drive it with a 1 kHz sine and measure the phase shift between input and output on a two-channel oscilloscope (the time between zero crossings times 360° × f). Then switch the generator to a square wave and compare the shapes. Expect the −90° point near 1.061 kHz with 15 nF (the nearest standard value to 15.92 nF), and small departures from a perfect all-pass because of resistor mismatch and the op-amp's finite bandwidth.
