# Lab 06-11 · Practical DC Circuits and Measurement

**Chapter:** [06-11](../../chapters/06-11-practical-dc-circuits-and-measurement.md) · **Notebook:** [06-11-measurement.ipynb](06-11-measurement.ipynb) · **Time:** about 60 minutes (plus 60 minutes for the optional hardware part)

## Objective

1. See how a voltmeter's loading error grows with the source's Thévenin resistance, and find where it reaches 1%.
2. Map a meter's relative uncertainty across its ranges, and learn where on a range to read.
3. Compare a milliohm shunt read through Kelvin taps with one read through taps that include copper, over temperature.
4. Simulate many units of a measurement chain and compare the spread with the worst case.

## Background

Chapter sections 3.1 to 3.6 and Examples 06-11.1 to 06-11.6. You need Python with NumPy and Matplotlib, and ngspice for the simulator checks in Parts 1 and 3 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips those cells.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-11-measurement.ipynb](06-11-measurement.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [measure.cir](measure.cir) | Every instrument as the resistor it is: Examples 06-11.1, 06-11.2, 06-11.4, 06-11.5 (a temperature sweep with resistor temperature coefficients) and 06-11.6 (remote sensing with an error amplifier), and Problems 06-11.1, 06-11.2, 06-11.4, 06-11.8, 06-11.9 and 06-11.12 | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **Loading curves (Part 1).** *Predict first:* the source resistance at which 10 MΩ and 10 GΩ meters read 1% low.
2. **Range choice (Part 2).** *Predict first:* the relative uncertainty of a ±(0.05% + 1) 6000-count meter at 10% of a range and at full scale.
3. **Shunt over temperature (Part 3).** *Predict first:* the temperature rise at which the misplaced taps drift 5%.
4. **Monte Carlo (Part 4).** *Predict first:* the fraction of 48 V monitors outside ±1.5%.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | 1% loading | at 101.0 kΩ for a 10 MΩ meter, 101.0 MΩ for 10 GΩ; ngspice reproduces Example 06-11.1 |
| 2 | range choice | 0.22% at 10% of range, 0.067% at full scale |
| 3 | shunt drift | misplaced taps reach 5% at a rise of 85.5 °C, when Kelvin taps are at 2.14% worst case; ngspice agrees |
| 4 | Monte Carlo | about 6% of units beyond ±1.5%; standard deviation 0.81%; none near the worst case |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-11.a | source resistance for 1% loading, 10 MΩ meter | 101.0 | kΩ |
| Lab 06-11.b | source resistance for 1% loading, 10 GΩ meter | 101.0 | MΩ |
| Lab 06-11.c | relative uncertainty at 10% of range | 0.22 | % |
| Lab 06-11.d | relative uncertainty at full scale | 0.067 | % |
| Lab 06-11.e | temperature rise for 5% drift, misplaced taps | 85.5 | °C |
| Lab 06-11.f | Kelvin worst-case drift at that rise | 2.14 | % |
| Lab 06-11.g | fraction of monitors beyond ±1.5% | 6 | % |
| Lab 06-11.h | standard deviation of the monitor error | 0.81 | % |
| Lab 06-11.i | circuit resistance for 1% ammeter error (1.8 Ω) | 178.2 | Ω |
| Lab 06-11.j | effective TC, 5 mΩ shunt with 0.1 mΩ copper | 111 | ppm/°C |
| Lab 06-11.k | fraction beyond ±1.5% with 0.1% resistors | 0 | % |

## Discussion questions

1. A colleague measures 4.76 V at the midpoint of a megohm divider and concludes a resistor is out of tolerance. What would you check first?
2. Why do autoranging meters change range near full scale and near 10% of range, rather than at other points?
3. Part 3's misplaced taps drift faster than the shunt itself. Why can a one-temperature calibration not fix this?
4. In Part 4, the worst case is ±2.4% but almost every unit is within ±2%. How would you write the specification for a product, and what would you need to do in production?

<details><summary>Answers to the discussion questions</summary>

1. The meter's loading. The midpoint's Thévenin resistance is 500 kΩ, so a 10 MΩ meter reads 4.76% low (Example 06-11.1): the reading is exactly what a perfect divider gives. Repeat with a high-impedance mode, or correct with $V_m(1 + R_{th}/R_{in})$.
2. Relative uncertainty is the gain term plus one count divided by the reading. Near full scale the reading uses almost all the counts; below about 10% of range, the next range down offers ten times finer counts. Switching near those points keeps the reading in the part of the range where the count term is small.
3. Calibration removes the error at the calibration temperature. The drift is a change with temperature, set by copper's 0.39%/°C, which appears as soon as the board heats. Only a correct layout (Kelvin taps), or temperature measurement and compensation, removes it.
4. Either specify the guaranteed worst case (±2.4%), or specify a tighter limit and enforce it by testing every unit and rejecting or calibrating those outside it. A statistical figure alone (for example "±1.5%, 94% of units") is not a guarantee a customer can design to. Better resistors (0.1%) make the worst case ±0.69% and remove the problem.

</details>

## Optional hardware version

Build a divider of two 1 MΩ resistors from a 10 V supply. Measure the midpoint with a handheld meter, then with a bench meter in its 10 GΩ mode if available, and compare with Example 06-11.1. Then measure a 0.1 Ω or 1 Ω resistor with two wires and with four (two clip leads for a bench supply set to a current limit of 100 mA, two more for the meter at the resistor's leads), and compare the readings. Finally, wiggle the two-wire probes on the resistor's leads and watch the contact resistance change the two-wire reading but not the four-wire one.
