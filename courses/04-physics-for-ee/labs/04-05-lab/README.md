# Lab 04-05 · Current, Resistance and Conduction

**Chapter:** [04-05](../../chapters/04-05-current-resistance-and-conduction.md) · **Notebook:** [04-05-conduction.ipynb](04-05-conduction.ipynb) · **Netlist:** [wire_rc.cir](wire_rc.cir) · **Time:** about 60 minutes

## Objective

1. Watch Ohm's law emerge from random collisions in a simulated electron gas.
2. Compute the resistance of a non-uniform conductor by integration.
3. Find the steady temperature of a self-heating conductor and the onset of thermal runaway.
4. Show that a wire's RC delay is about 0.38 RC, not the 0.69 RC of a lumped circuit.
5. Confirm the on-chip wire delay of Example 04-05.6 in ngspice.

## Background

Chapter sections 3.2 to 3.5 and Examples 04-05.2 and 04-05.6; Problems 04-05.11 and 04-05.16. Part 1 uses random numbers with seed 2026, so its results reproduce exactly.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict how the drift velocity changes when the mean free time doubles.
3. **Part 2:** predict whether a tapered trace's resistance is above or below that of a uniform trace at its average width.
4. **Part 3:** predict the steady temperature at 1 A, and whether a runaway current exists.
5. **Part 4:** predict the 50% delay of a distributed RC line as a fraction of $RC$.
6. From the repository root, run `python tools/run_spice.py 04-05` to simulate the 1 mm wire.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Drude simulation, $E$ = 10 kV/m | drift ≈ −42 m/s at τ = 25 fs and ≈ −86 m/s at 50 fs, against −44.0 and −87.9 m/s from $-e\tau E/m$ |
| 2 | tapered trace, 1 mm → 0.2 mm over 100 mm | 99.23 mΩ; the average-width estimate (82.21 mΩ) is 17% low |
| 3 | self-heating, 1 Ω at 20 °C, θ = 30 K/W, 25 °C ambient | 59.68 °C at 1 A; runaway above 2.912 A |
| 4 | distributed RC line | 0.3466 RC with one section, converging to 0.3787 RC |
| netlist | 1 mm wire, 20 π-sections | 50% delay 1.402 ns |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-05.a | tapered trace resistance | 99.23 | mΩ |
| Lab 04-05.b | uniform trace at average width | 82.21 | mΩ |
| Lab 04-05.c | steady temperature at 1 A | 59.68 | °C |
| Lab 04-05.d | runaway current | 2.912 | A |
| Lab 04-05.e | one-section 50% delay coefficient | 0.3466 | — |
| Lab 04-05.f | distributed-line 50% delay coefficient | 0.3787 | — |

## Discussion questions

1. Part 1 shows the drift is independent of the random (thermal) speed. Why, physically, does the random motion not contribute to current, and what would change if collisions did *not* fully randomize the velocity?
2. Part 3's runaway condition is $\theta I^2R_{20}\alpha \ge 1$. A power semiconductor with a *negative* temperature coefficient (its resistance falls as it heats) is placed in parallel with an identical one. Why can that be dangerous, and why are MOSFETs (positive coefficient) easier to parallel?
3. Part 4 shows that a single lumped RC with the whole capacitance at the end would give 0.69 RC, almost twice the distributed answer. Which way does that error push a timing analysis, and why do signoff tools model wires as distributed networks?
4. The netlist uses 20 sections and matches the exact distributed answer to 0.01%. Why do π-sections (half the capacitance at each end of every resistor) converge so much faster than putting each section's full capacitance at one end?

<details><summary>Answers to the discussion questions</summary>

1. Each collision sends an electron off in a random direction, so the velocities between collisions average to zero over many electrons; only the small extra velocity the field adds since the last collision survives averaging, and that depends on τ and $E$, not on the random speed. If collisions only partly randomized the velocity (electrons "remembering" their direction), the effective τ for momentum loss would be longer than the time between collisions, and the mobility higher: real transport theory uses a momentum relaxation time for exactly this reason.
2. With a negative temperature coefficient, whichever device runs slightly hotter takes more current, heats further and hogs even more current until it fails: positive feedback between the parallel parts, the electrical version of Part 3's runaway. A positive coefficient (MOSFETs, whose channel resistance rises with temperature) gives negative feedback: the hotter device takes less current, so parallel devices share current naturally.
3. Putting all the capacitance at the far end overestimates delay, so a timing analysis would be pessimistic: it would report false violations and force unnecessary buffering or slower clocks. Signoff tools use distributed (many-segment) RC models, or reduced-order models matched to them, to get the delay right without either optimism or waste.
4. A π-section approximates the line's capacitance symmetrically around each resistor, so the leading discretization error cancels (it is second-order in the section length, like the midpoint rule of numerical integration). Putting the full capacitance at one end of each section is like a one-sided Riemann sum: its error is first-order and shrinks only as $1/N$.

</details>

## Optional hardware version

With a bench supply, a multimeter and a length of thin enameled copper wire (for example 10 m of 0.2 mm wire, a few ohms): measure its resistance at room temperature, then immerse the coil in hot water at a measured temperature and measure again. Compute α and compare with 0.00393 /°C. Then pass a modest current through the dry coil and track its temperature rise from its resistance (Example 04-05.5), keeping the power below a watt.
