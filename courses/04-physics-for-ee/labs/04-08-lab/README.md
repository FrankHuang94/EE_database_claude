# Lab 04-08 · Energy in Fields and Maxwell's Equations (Preview)

**Chapter:** [04-08](../../chapters/04-08-maxwell-preview.md) · **Notebook:** [04-08-fdtd.ipynb](04-08-fdtd.ipynb) · **Netlist:** [stripline_delay.cir](stripline_delay.cir) · **Time:** about 60 minutes

## Objective

1. Solve Maxwell's curl equations numerically (FDTD) and watch a wave propagate, reflect and transmit at a dielectric boundary.
2. Check that the field energy is conserved as the wave splits.
3. Measure attenuation in a lossy dielectric and compare it with the loss-tangent formula.
4. Compare board laminates' dielectric loss against frequency.
5. Simulate a board trace's propagation delay in ngspice.

## Background

Chapter sections 3.2 to 3.6 and Examples 04-08.3 and 04-08.6; Problems 04-08.6 and 04-08.9. The notebook has no random elements.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict the pulse's speed in $\varepsilon_r$ = 4 and the sign and size of the reflection.
3. **Part 2:** predict whether total field energy changes when the pulse splits.
4. **Part 3:** predict the attenuation for a loss tangent of 0.05 at 10 GHz.
5. **Part 4:** predict the FR-4-class laminate's loss at 5 GHz.
6. From the repository root, run `python tools/run_spice.py 04-08` to simulate the 100 mm stripline.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | pulse at an air/ε_r = 4 boundary | reflection −0.334 (theory −0.3333); transmission 0.654 (theory 0.6667); speed 0.499c (theory 0.5c) |
| 2 | energy after the source stops | constant to about 1% |
| 3 | lossy dielectric, tan δ = 0.05, 10 GHz | fitted 10.53 Np/m against the formula's 10.48 Np/m |
| 4 | Isola 370HR at 5 GHz | 22.53 dB/m |
| netlist | 100 mm stripline, ε_r = 4.6 | 715.4 ps |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-08.a | reflection coefficient, air to ε_r = 4 | −0.3333 | — |
| Lab 04-08.b | transmission coefficient | 0.6667 | — |
| Lab 04-08.c | speed in ε_r = 4, as a fraction of c | 0.5 | — |
| Lab 04-08.d | attenuation for tan δ = 0.05 at 10 GHz, ε_r = 4 | 10.48 | Np/m |
| Lab 04-08.e | 370HR dielectric loss at 5 GHz | 22.53 | dB/m |

## Discussion questions

1. The FDTD code contains only Faraday's law and the Ampère–Maxwell law, yet waves appear. Which term in the code is the displacement current, and what happens to the wave if you delete it?
2. Part 1's reflected pulse is inverted. On a circuit board, a signal going from a 50 Ω trace into a 25 Ω section reflects. Using Problem 04-08.6's formula with impedances, what fraction of the voltage reflects, and with what sign?
3. Part 3's attenuation grows with frequency. Why does that make a digital eye diagram close at high data rates even when the low-frequency loss is small?
4. Why do commercial electromagnetic solvers use FDTD and similar grid methods for antennas and packages rather than closed-form formulas?

<details><summary>Answers to the discussion questions</summary>

1. The E-update, which changes E in proportion to the curl of H divided by ε, is the Ampère–Maxwell law; the rate of change of E it computes *is* the displacement current. Without it, E would never change in empty space, so a changing H could not regenerate E and no wave would propagate: the disturbance would stay put.
2. $\Gamma = (25 - 50)/(25 + 50) = -1/3$ of the voltage reflects, inverted, exactly as in Part 1 (an impedance step down). Impedance discontinuities from vias, connectors and width changes cause such reflections.
3. Higher harmonics of the data signal are attenuated more than lower ones, so sharp edges are smeared into slow ones and each bit spills into its neighbors (inter-symbol interference). The eye closes even though the average signal level is fine; equalizers boost the high frequencies to compensate (Course 24).
4. Real structures (antennas near hands, packages with vias and bond wires, connectors) have arbitrary shapes and materials; only numerical solutions of Maxwell's equations on a grid or mesh handle them. FDTD is simple, handles broadband pulses in one run, and scales well on parallel hardware.

</details>

## Optional hardware version

With a fast-edge pulse generator (or a microcontroller toggling a pin) and an oscilloscope of a few hundred MHz bandwidth, send a step down a long coaxial cable (several meters) with the far end open. Measure the delay of the reflection returning to the input, and compute the cable's velocity factor and its dielectric's $\varepsilon_r$. Then terminate the far end with a resistor equal to the cable's impedance and watch the reflection disappear.
