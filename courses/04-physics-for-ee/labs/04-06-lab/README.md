# Lab 04-06 · Magnetic Fields and Forces

**Chapter:** [04-06](../../chapters/04-06-magnetic-fields-and-forces.md) · **Notebook:** [04-06-magnetism.ipynb](04-06-magnetism.ipynb) · **Time:** about 60 minutes

## Objective

1. Integrate the Lorentz force and discover the E×B drift.
2. Compute fields of coils by brute-force Biot–Savart summation and design a uniform-field Helmholtz pair.
3. Check Ampère's law numerically.
4. See why Hall sensors are made of semiconductors.
5. Explore how an air gap raises a ferrite core's saturation current.

## Background

Chapter sections 3.1 to 3.6 and Examples 04-06.1, 04-06.4, 04-06.6 and 04-06.8; Problem 04-06.15. The notebook has no random elements, and there is no ngspice netlist for this chapter (it has no circuit results).

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict which way a proton released from rest drifts in crossed E and B fields, and how fast.
3. **Part 2:** predict how uniform a Helmholtz pair's field is near its midpoint compared with a single coil.
4. **Part 3:** predict $\oint\vec B\cdot d\vec l/(\mu_0I)$ for loops that do and do not enclose a wire.
5. **Part 4:** predict how the Hall voltage scales with plate thickness and doping.
6. **Part 5:** predict the saturation current at 100 °C with a 1 mm gap.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | electron at 10⁶ m/s in 0.1 T | orbit diameter 113.71 µm, closing after one period |
| 1 | proton in 1 kV/m × 0.1 T | average drift 10.00 km/s along E×B (−y), no net motion along E |
| 2 | Helmholtz pair, R = 5 cm, 10 turns, 1 A | 0.1798 mT at the center; 0.176% lower 1 cm away, against 5.71% for a single coil |
| 3 | Ampère's law | 1.00000 around the wire; essentially zero (−5×10⁻⁷) beside it |
| 4 | Hall plate, 10¹⁶ cm⁻³, 1 mA, 0.1 T, 10 µm | 6.242 mV; $V_H \propto 1/(nt)$ |
| 5 | gapped core at 100 °C, 1 mm gap | 15.91 A |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-06.a | E×B drift speed | 10.00 | km/s |
| Lab 04-06.b | Helmholtz center field | 0.1798 | mT |
| Lab 04-06.c | Helmholtz field drop 1 cm from center | 0.176 | % |
| Lab 04-06.d | single-coil field drop 1 cm from center | 5.71 | % |
| Lab 04-06.e | saturation current, 1 mm gap, 100 °C | 15.91 | A |

## Discussion questions

1. Part 1 shows charges drifting perpendicular to both E and B at E/B, regardless of charge and mass. In a magnetron sputtering source, magnets above the target trap electrons near its surface. Why does that make the plasma denser and the deposition faster?
2. Part 2's Helmholtz pair cancels the field's second derivative at the midpoint. Why is a uniform field what you want to calibrate a Hall sensor or a compass chip?
3. Part 3 gives zero for a loop beside the wire even though B is nonzero along it. Explain this in terms of where the field is stronger along the loop.
4. Part 5 shows a gap raising saturation current many-fold. If gaps are so effective, why are any inductors built with ungapped cores?

<details><summary>Answers to the discussion questions</summary>

1. Electrons near the target drift around a closed racetrack (the E×B direction) instead of escaping to the walls, so each one travels much farther and ionizes many more gas atoms before being lost. The denser plasma bombards the target harder, sputtering material faster at lower gas pressure.
2. A sensor calibrated in a uniform field reads the same wherever its tiny sensing element sits within the region, so the result does not depend on precise positioning; the known field (from the coil formula and the measured current) becomes a traceable reference.
3. On the side of the loop nearer the wire, B is stronger and points one way along the loop; on the far side, B is weaker but the loop's direction is reversed relative to it, and the far arc is longer in the relevant sense. The contributions cancel exactly, because no current threads the loop.
4. A gap trades inductance per turn for saturation current. Where the DC current is small and the most inductance per volume is wanted (common-mode chokes, signal transformers, low-current filters), an ungapped high-permeability core gives far more inductance with fewer turns; gaps also cause fringing loss and stray fields.

</details>

## Optional hardware version

A smartphone contains a three-axis magnetometer (usually a Hall or magnetoresistive sensor). With a free sensor-logging app, record the field as you bring a long straight wire carrying a known DC current (for example 2 A from a bench supply through a resistor) toward the phone, and plot B against 1/r. Keep the supply and return wires far apart so their fields do not cancel.
