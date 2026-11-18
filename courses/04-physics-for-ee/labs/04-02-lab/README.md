# Lab 04-02 · Charge, Coulomb's Law and Electric Fields

**Chapter:** [04-02](../../chapters/04-02-charge-coulomb-and-electric-fields.md) · **Notebook:** [04-02-fields.ipynb](04-02-fields.ipynb) · **Netlist:** [hbm.cir](hbm.cir) · **Time:** about 60 minutes

## Objective

1. Compute fields by brute-force superposition and check the chapter's examples.
2. See how fast a discretized charge distribution converges to the integral.
3. Confirm the dipole's $1/r^3$ far field and where the approximation fails.
4. Find a ring's field maximum numerically.
5. Integrate an electron's path through deflection plates.
6. Compare the HBM and IEC 61000-4-2 ESD pulses.

## Background

Chapter sections 3.2 to 3.6 and Examples 04-02.3, 04-02.4, 04-02.6 and 04-02.8; Problems 04-02.6 and 04-02.11. The notebook has no random elements.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict the direction of the net force on the test charge.
3. **Part 2:** predict how many segments give 0.1% accuracy.
4. **Part 3:** predict the far-field slope on log axes.
5. **Part 4:** predict where the ring's on-axis field peaks.
6. **Part 5:** predict the deflection at the plates' exit.
7. **Part 6:** predict the ratio of the two pulses' peak currents.
8. From the repository root, run `python tools/run_spice.py 04-02` to simulate Example 04-02.8.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | net force on +1 nC | 15.34 µN along +$x$; the field map shows lines from the positive to the negative charge |
| 2 | finite line at 1 mm, 10 nC/m | closed form 1.271×10⁵ V/m; midpoint sums are 1.193% high with 2 segments, 0.1248% with 10, 0.0312% with 20 (errors fall as $1/N^2$) |
| 3 | dipole on axis | far-field slope −3.000; the exact field is 1.00005 times $2k_ep/r^3$ at 10 cm but 1.0580 times at 3 mm |
| 4 | ring maximum | at $z = R/\sqrt2$ = 3.536 cm, $E$ = 1.384×10⁴ V/m |
| 5 | deflection plates | 0.5000 mm at the exit, tan θ = 0.05000 |
| 6 | ESD pulses at 8 kV | HBM 5.333 A, 150 ns, 0.8 µC; IEC 24.24 A, 49.5 ns, 1.2 µC |
| netlist | HBM at 2 kV | 1.333 A peak, 0.1804 A at 300 ns |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-02.a | midpoint error, 2 segments | 1.193 | % |
| Lab 04-02.b | midpoint error, 10 segments | 0.1248 | % |
| Lab 04-02.c | midpoint error, 20 segments | 0.0312 | % |
| Lab 04-02.d | exact over approximate dipole field at 10 cm | 1.00005 | — |
| Lab 04-02.f | exact over approximate dipole field at 3 mm | 1.0580 | — |
| Lab 04-02.e | far-field slope | −3.000 | — |

## Discussion questions

1. Part 2 shows that a few segments are enough at a distance equal to the line's half-length. A circuit-board field solver must compute the capacitance between traces 50 µm apart. What does the result suggest about how finely it must mesh the conductors near the gap?
2. Part 3 shows the dipole approximation is about 6% off at three spacings. The charges on the two sides of a semiconductor junction form a dipole layer only tens of nanometers thick, and the fields that matter are inside it. Would you use the dipole formula there? What would you use instead?
3. Part 6 shows the IEC pulse is far harsher than HBM. If you were qualifying a wearable's charging contacts, which test would drive the protection design, and why?

<details><summary>Answers to the discussion questions</summary>

1. The midpoint error falls as $1/N^2$ but grows rapidly as the observation point approaches the charges, because the field varies on the scale of the distance. Near a 50 µm gap the mesh must be much finer than 50 µm at the facing edges; solvers refine the mesh adaptively where fields change fastest.
2. No: the dipole formula describes the field far from a compact pair of charges, and inside a junction you are between the charge layers, not far from them. Use superposition of the actual charge distribution, or Gauss's law for the planar geometry (04-03): the field is confined between the two charge layers, like a parallel-plate capacitor, and is zero outside.
3. The system-level test (IEC 61000-4-2): users touch the contacts directly, and its peak current is about 4.5 times the HBM's at the same voltage. Component HBM and CDM ratings matter in the factory; product-level protection at the connector is designed against the system-level pulse.

</details>

## Optional hardware version

Rub a balloon or plastic comb and hold it near small bits of paper: the neutral paper is pulled into the stronger field (§3.5). With an inexpensive electrometer or a charge-sensing app on an oscilloscope probe, measure the charge on the comb and estimate the field at 1 cm with Coulomb's law. For ESD, never discharge into a powered board; use a commercial ESD simulator only under its safety instructions.
