# Problems 06-07 · Linearity and Superposition

Chapter: [06-07](../chapters/06-07-linearity-and-superposition.md) · Worked solutions: [06-07 solutions](../solutions/06-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** passive sign convention; a switched-off voltage source is a short and a switched-off current source an open; dependent sources always stay. With resistances in kΩ and voltages in V, currents come out in mA. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-07.1 [A]

**Is it linear?** (a) Which of these input–output relations are linear: $y = 3x$; $y = 3x + 2$; $y = x^2$; $y = |x|$? (b) A circuit of resistors gives 2 V at its output for 5 V at its input. What does it give for 12 V? Which property did you use? (c) Why can you not answer (b) the same way for a circuit containing a diode?

### Problem 06-07.2 [A]

**Two voltage sources.** A 10 V source with 5 Ω series resistance and a 15 V source with 10 Ω series resistance both connect to node a, which has 10 Ω to ground. (a) Find $v_a$ by superposition. (b) Check it with Millman's theorem.

### Problem 06-07.3 [A]

**A chain of transformations.** A 24 V source with 6 Ω series resistance feeds a node with 3 Ω to ground; from that node, 2 Ω in series leads to a 4 Ω load. Use source transformations to find the load current and voltage.

### Problem 06-07.4 [B]

**Three sources and the cross terms.** Node a connects to a 6 V source through 3 Ω and to ground through 6 Ω; a 1 A source pushes current into node a, and a 0.5 A source draws current out of it. (a) Find each source's contribution to $v_a$ and the total. (b) Find the power in the 6 Ω resistor, and compare it with the sum of the three single-source powers. (c) Find the current the 6 V source delivers.

### Problem 06-07.5 [B]

**Superposition with a VCCS.** A 6 V source drives node 1 through 2 kΩ; 2 kΩ joins node 1 to node 2; node 2 has 4 kΩ to ground, a 1 mA source pushing current in, and a VCCS drawing $g\,v_1$ ($g$ = 0.25 mS) to ground. (a) Find $v_1$ and $v_2$ due to each independent source alone, and their sums. (b) Check by solving with both sources at once. (c) What would you get for the 1 mA source's contribution if you wrongly switched off the VCCS?

### Problem 06-07.6 [B]

**Unit output.** A two-section ladder: 1 kΩ in series, then 2 kΩ shunt; then 3 kΩ in series, then the 6 kΩ output shunt. (a) Use the unit-output method to find $v_{out}/v_{in}$. (b) Find the output for 12 V in. (c) Find the input resistance.

### Problem 06-07.7 [B]

**Three batteries in parallel.** Three 12 V lead-acid batteries at different states of charge, 12.6 V (50 mΩ), 12.4 V (60 mΩ) and 12.2 V (80 mΩ), are connected in parallel. (a) With a 0.5 Ω load, find the bus voltage, each battery's current and the load current. (b) With the load removed, find the bus voltage and each battery's current. Which batteries charge?

### Problem 06-07.8 [B]

**An error budget.** A sensor channel with a 2.5 V full scale has four independent error contributions at its output: offset +10 mV, bias-current error −4 mV, resistor-tolerance error ±6 mV and reference error ±3 mV. (a) Find the worst-case and RSS totals, and express both as a percentage of full scale. (b) The offset is trimmed to 1 mV. Find the new RSS total. (c) When is RSS the right way to combine errors, and when is it not?

### Problem 06-07.9 [C]

**Adding noise.** Two noise sources at the input of an amplifier have spectral densities of 4 nV/√Hz and 3 nV/√Hz. (a) If they are independent, what is the total density? (b) What would it be if they were perfectly correlated and in phase, and if perfectly anticorrelated? (c) For independent sources, find the total RMS noise in a 10 kHz bandwidth (white noise: RMS = density × √bandwidth). (d) Why does this mean you should reduce the largest noise source first?

### Problem 06-07.10 [C]

**A 4-bit DAC and its linearity.** A binary-weighted DAC has bit resistors of 1, 2, 4 and 8 kΩ (MSB to LSB), bit levels of 0 or 4 V, and an 8 kΩ load. (a) Find the LSB step and the full-scale output. (b) The MSB resistor is 0.5% high (1.005 kΩ). Find the outputs for codes 0111 and 1000, the DNL at that transition and the INL at code 1000 (the deviation from the ideal 2.000 V, in LSBs).

### Problem 06-07.11 [B]

**Signal plus offset.** A non-inverting amplifier with $R_1$ = 1 kΩ (− input to ground) and $R_2$ = 10 kΩ (output to − input) uses an op-amp modeled as a VCVS with $A = 10^5$, infinite input resistance and zero output resistance. Its input offset is modeled as a 2 mV source in series with the + input; the signal is 50 mV. (a) Find the closed-loop gain. (b) Find the output due to the signal alone, due to the offset alone, and in total. (c) Compare with the ideal gain of 11.

### Problem 06-07.12 [C]

**Superposition fails.** A 5 V source drives node d through 1 kΩ; a 1 mA source also pushes current into node d; a diode ($I_S = 10^{-14}$ A, $V_T$ = 25.852 mV) connects node d to ground. (a) Find $v_d$ with both sources (numerically). (b) Find $v_d$ with each source alone and add them. (c) Explain the discrepancy, and describe the situation in which superposition would still work for this circuit.

---

## Objective coverage

| Learning objective (chapter 06-07) | Problems |
|---|---|
| 1. Linearity and which elements break it | 1, 12 |
| 2. Superposition with dependent sources kept | 2, 4, 5, 11 |
| 3. Power does not superpose; when average powers add | 4, 9 |
| 4. Source transformation and the unit-output method | 3, 6, 7 |
| 5. Error budgets, converters and small-signal use | 8, 9, 10, 11 |
