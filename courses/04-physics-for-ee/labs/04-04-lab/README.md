# Lab 04-04 · Electric Potential, Capacitance and Dielectrics

**Chapter:** [04-04](../../chapters/04-04-potential-capacitance-and-dielectrics.md) · **Notebook:** [04-04-potential.ipynb](04-04-potential.ipynb) · **Netlist:** [charge_sharing.cir](charge_sharing.cir) · **Time:** about 60 minutes

## Objective

1. Map a potential, draw equipotentials and recover the field as the negative gradient.
2. Show numerically that the work per unit charge between two points does not depend on the path.
3. Recover capacitance from the energy stored in the field.
4. Explore equivalent oxide thickness and the field in each layer of a gate stack.
5. See how an electrostatic chuck's force depends on a small gap.
6. Simulate charge sharing in ngspice and watch half the energy vanish, whatever the resistance.

## Background

Chapter sections 3.1 to 3.6 and Examples 04-04.1, 04-04.4 to 04-04.8; Problems 04-04.10, 04-04.13, 04-04.15 and 04-04.16. The notebook has no random elements.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict where the dipole's potential is zero, and whether the field is zero there.
3. **Part 2:** predict how much the straight and wiggly paths differ.
4. **Part 3:** predict the sphere's capacitance from its field energy.
5. **Part 4:** predict the EOT of 3 nm of HfO₂ on 0.4 nm of SiO₂.
6. **Part 5:** predict the chuck's force with a 5 µm gap.
7. From the repository root, run `python tools/run_spice.py 04-04` to simulate Example 04-04.7.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | dipole map | $V = 0$ on the bisector $x$ = 2 cm, where $E$ ≈ 7.67 kV/m; finite differences match Coulomb's field |
| 2 | work per unit charge from A to B | 329.5 V on both paths, equal to $-(V_B - V_A)$ |
| 3 | capacitance from field energy | sphere 5.563 pF; coax 40.13 pF/m |
| 4 | gate stack | EOT 0.868 nm; at 0.7 V, 8.06 MV/cm in the SiO₂ and 1.26 MV/cm in the HfO₂ |
| 5 | chuck force | 36.94 N with no gap, 31.58 N with 5 µm |
| netlist | charge sharing | 5 V final; 25 µJ dissipated in both 10 Ω and 1 kΩ; DRAM bit line +45.45 mV |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-04.a | work per unit charge, A to B | 329.5 | V |
| Lab 04-04.b | sphere capacitance from field energy | 5.563 | pF |
| Lab 04-04.c | coax capacitance from field energy | 40.13 | pF/m |
| Lab 04-04.d | EOT, 3 nm HfO₂ on 0.4 nm SiO₂ | 0.868 | nm |
| Lab 04-04.e | chuck force with a 5 µm gap | 31.58 | N |

## Discussion questions

1. Part 1 shows a point where $V = 0$ but the field is strong. A technician measures 0 V between a probe and ground and declares the area "field-free". What is wrong with the reasoning?
2. Part 2's two paths agree. In which situations in a real circuit would a voltmeter's reading depend on how its leads are routed?
3. Part 3 recovers capacitance from field energy. Why is this the method field-solver software often uses for complicated wiring, rather than computing charge and voltage directly?
4. In the netlist, a 10 Ω resistor and a 1 kΩ resistor dissipate the same 25 µJ. Where would the energy go with a 1 mΩ connection, and why does this matter for switched-capacitor circuits and DRAM?

<details><summary>Answers to the discussion questions</summary>

1. A voltmeter measures a potential *difference*. Zero difference between two points says nothing about the slope of the potential, which is the field; the probe could sit on the zero equipotential of a strong dipole field. To check for a field you need the potential at several nearby points (its gradient) or a field meter.
2. When magnetic fields change: the loop formed by the voltmeter leads and the circuit encloses changing magnetic flux, which induces an EMF (Faraday's law, 04-07), so different lead routes give different readings. This is common near switching power converters, motors and high-speed digital edges, which is why probes have short ground leads.
3. For an arbitrary 3-D structure, total field energy is a single, robust number that converges smoothly as the mesh is refined, and it is minimized by the true charge distribution (a variational principle), so small errors in the field give even smaller errors in the energy and hence in $C$.
4. With a tiny resistance, the circuit's inductance takes over: charge oscillates between the capacitors and the energy leaves as radiation and as heat in whatever resistance remains, still half in total. Every time a switched-capacitor circuit or a DRAM read connects capacitors at different voltages, it pays this energy cost, so designers minimize the voltage difference (precharging the bit line to the midpoint, for instance) and count it in the power budget.

</details>

## Optional hardware version

With two identical electrolytic or film capacitors (say 100 µF), a 9 V battery, a resistor and a multimeter: charge one capacitor, connect it to the uncharged one through the resistor, and measure the final voltage on both. Compute the energy before and after. Repeat with a different resistor. (Discharge capacitors through a resistor before handling them, and observe polarity on electrolytics.)
