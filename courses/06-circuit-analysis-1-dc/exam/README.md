# Course 06 · Final Exam (Circuit Analysis I, DC)

**Time limit:** 180 minutes. **Allowed:** a scientific calculator and the [Course 06 equation sheet](../../../reference/equation-sheets/06-circuit-analysis-1-dc.md) printed without its chapter links. No notes, no Python, no simulator.
**Instructions:** answer all 15 questions and show every step. Each [A] is worth 5 points, each [B] 8 and each [C] 12 (116 points in total; 81 or more, about 70%, is a strong pass). Within a question, the lettered parts carry equal weight unless the question states otherwise. Questions 8 and 14 ask for short derivations; show the reasoning, not just the formula. Give numerical answers to 4 significant figures unless told otherwise, with units and signs. Question 15 is a short-answer diligence question graded against the rubric in the solutions. Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions:** passive sign convention throughout. Circuits are given as element lists: "R1, node 1 to node 2, 2 kΩ" places a resistor between those nodes; node 0 is ground. For a voltage source, the first node named is its + terminal. For a current source, "from node a into node b" gives the direction of the current through the source. Op-amps are ideal unless a non-ideality is given. Copper: $\rho$ = 1.7241 µΩ·cm and $\alpha$ = 0.00393 /°C at 20 °C.

---

**1 [A] · Power and energy.** (a) A device has 12 V across it (+ at terminal a), and −0.5 A enters terminal a. Find the power it absorbs, and say whether it is a source or a load.
(b) A phone battery is rated 3.7 V nominal and 3000 mAh. Find the charge it holds, in coulombs.
(c) Find its energy in Wh and in kJ.
(d) Find how long it lasts at an average drain of 1.5 W.

**2 [A] · Real resistors.** (a) A copper motor winding measures 2.000 Ω at 20 °C and 2.472 Ω after running. Find the winding's temperature.
(b) Find the largest voltage a 10 kΩ, 0.25 W resistor may have across it, and the largest current a 100 Ω, 0.25 W resistor may carry.
(c) Find the range of a 4.7 kΩ ±5% resistor.

**3 [A] · Dividers.** A 12 V source feeds a divider of $R_1$ = 8 kΩ (top) and $R_2$ = 4 kΩ (bottom).
(a) Find the unloaded output.
(b) Find the output with a 4 kΩ load.
(c) Find the smallest load that keeps the loading error below 1%.
(d) A 6 mA current source drives 2 kΩ, 3 kΩ and 6 kΩ in parallel. Find the current in each.

**4 [B] · Nodal analysis with a supernode.** Elements: I1, 3 mA from node 0 into node 1; R1, node 1 to node 0, 2 kΩ; V1, node 1 (+) to node 2, 6 V; R2, node 2 to node 0, 4 kΩ; R3, node 2 to node 3, 2 kΩ; R4, node 3 to node 0, 1 kΩ; I2, 1 mA from node 0 into node 3.
(a) Write the nodal equations as a matrix equation in $v_1$, $v_2$, $v_3$ (two KCL equations and the source constraint).
(b) Solve for the three node voltages.
(c) Find the power delivered by V1.

**5 [B] · Mesh analysis with a supermesh.** Elements: V1, node 1 (+) to node 0, 12 V; R1, node 1 to node 2, 2 Ω; R4, node 2 to node 0, 4 Ω; R2, node 2 to node 3, 3 Ω; I1, 1 A from node 0 into node 3; R3, node 3 to node 0, 6 Ω. Draw it as three meshes side by side (V1 on the left; R4, then I1, then R3 as the vertical branches) and use clockwise mesh currents $i_1$, $i_2$, $i_3$.
(a) Write the constraint the current source imposes and the KVL equations, and solve for the three mesh currents.
(b) Find the voltage across R4 (node 2 relative to node 0).
(c) Find the power delivered by V1 and by I1.

**6 [B] · A transistor-like amplifier.** Elements: $v_s$, node s (+) to node 0; $R_s$, s to b, 1 kΩ; $r_\pi$, b to e, 2.5 kΩ; a current-controlled current source from node c into node e of value $\beta i_b$, where $i_b$ is the current in $r_\pi$ from b to e and β = 100; $R_C$, c to node 0, 4 kΩ; $R_E$, e to node 0, 200 Ω.
(a) Find the resistance seen looking into node b (to ground).
(b) Find the voltage gain $v_c/v_s$.
(c) Find the gain if $R_E$ is shorted, and state the tradeoff that $R_E$ buys.

**7 [B] · Superposition.** Elements: V1, node 1 (+) to node 0, 10 V; R1, node 1 to node x, 2 kΩ; I1, 3 mA from node 0 into node x; R2, node x to node 0, 3 kΩ.
(a) Find $v_x$ by superposition, giving each source's contribution.
(b) Find the power in R2, and compare it with the sum of the powers each source alone would cause in R2.
(c) If V1 is doubled, what is $v_x$?
(d) Replace V1 and R1 by their Norton equivalent and find $v_x$ again by current division.

**8 [B] · Thévenin with a dependent source.** Elements: V1, node 1 (+) to node 0, 12 V; R1, node 1 to node a, 6 kΩ; R2, node a to node 0, 3 kΩ; a current-controlled voltage source between nodes b (+) and a of value $2000\,i_x$ V, with $i_x$ the current in R2 from a to 0 in amperes; R3, node b to node out, 1 kΩ. The output port is node out and node 0.
(a) Find the open-circuit voltage.
(b) Derive the Thévenin resistance with a test source, explaining why the dependent source must stay in the circuit.
(c) Find the short-circuit current and the maximum power the port can deliver.

**9 [B] · Maximum power and efficiency.** A 48 V source has 0.5 Ω of internal resistance.
(a) Find the load for maximum power and the maximum power.
(b) Find the load for 90% efficiency and the power it receives, as watts and as a fraction of the maximum.
(c) A designer must drive a fixed 2 Ω load and may choose the source's internal resistance. What value maximizes the load's power, and why does this not contradict (a)?

**10 [A] · Op-amp configurations.** (a) An inverting amplifier has $R_1$ = 2.2 kΩ and $R_2$ = 33 kΩ. Find its gain and its output for a −0.2 V input.
(b) Choose $R_2$ for a non-inverting gain of 16 with $R_1$ = 1 kΩ.
(c) A summing amplifier with $R_f$ = 20 kΩ must give $v_{out} = -(v_1 + 2v_2)$. Choose the input resistors and find the output for $v_1$ = 0.5 V and $v_2$ = −1 V.
(d) A sensor with a 1 V open-circuit output and 90 kΩ of internal resistance drives an input of 10 kΩ. Find the voltage at the input, and again with a voltage follower inserted between them.

**11 [B] · Common-mode rejection.** A difference amplifier has $R_1 = R_3$ = 10 kΩ and $R_2 = R_4$ = 50 kΩ.
(a) Find the output for $v_1$ = 2.500 V and $v_2$ = 2.520 V.
(b) $R_4$ is 1% high (50.5 kΩ). Find the output with both inputs at 2.500 V, the common-mode gain, and the CMRR (ratio and dB).
(c) Find the worst-case CMRR with all four resistors ±1%, using the approximation from the chapter, in dB.

**12 [C] · A DC error budget.** A non-inverting amplifier ($R_1$ = 1 kΩ, $R_2$ = 49 kΩ) amplifies a 20 mV signal from a source with 5 kΩ of resistance. The op-amp has open-loop gain $A = 2\times10^4$, offset voltage up to ±2 mV, and bias currents of 100 nA flowing *into* both inputs.
(a) Find the exact closed-loop gain with finite $A$, its error in percent, and the output for the 20 mV signal.
(b) Treating the op-amp as ideal apart from each error, find the three output error terms (offset, bias current at −, bias current at +) with their signs where known.
(c) Find the worst-case total as a sum of magnitudes, and as a signed sum using the known bias-current signs.
(d) Express the signed worst case as a percentage of the output signal. Name two changes that would reduce it most.

**13 [B] · Measurement.** (a) A 10 MΩ voltmeter measures a node whose Thévenin equivalent is 3.3 V behind 220 kΩ. Find the reading, its error and the corrected value.
(b) An ammeter with 2.5 Ω internal resistance measures the current of a 5 V source into 100 Ω. Find the reading, its error and the burden voltage.
(c) A meter specified at ±(0.1% + 2 counts) reads 2.500 V on a range with 1 mV resolution. Find the uncertainty in millivolts and as a percentage of the reading.

**14 [C] · A strain-gauge front end.** A quarter bridge of four 350 Ω resistors, one of them a strain gauge with gauge factor 2, is excited by 5 V. Parts (a) and (b) carry 3 points each, (c) to (e) 2 points each.
(a) Derive the bridge output $v_o$ for a gauge resistance $R(1 + x)$, and show that it is approximately $V_{ex}x/4$ for small $x$.
(b) At 500 µε ($x = 10^{-3}$), find the exact output, the approximation and the nonlinearity error in percent.
(c) A three-op-amp in-amp with $R$ = 24.7 kΩ and $R_G$ = 24.7 Ω amplifies it. Find its gain and the output.
(d) The bridge's outputs sit near 2.5 V. With an in-amp CMRR of 100 dB, find the common-mode error at the output and as a percentage of the signal.
(e) The excitation reaches the bridge through two leads of 0.5 Ω each. Find the voltage across the bridge and the resulting gain error, and name a cure.

**15 [B] · Diligence: four claims.** For each claim, say in two or three sentences what is wrong or missing, and the one question you would ask.
(a) "Our sensor front end has 24-bit resolution, so it measures to better than one part per million."
(b) "Our 1 mΩ shunt is ±1%, so our current measurement is ±1% over temperature."
(c) "Our power supply holds 12.000 V ±0.1% at the load."
(d) "Our op-amp has 1 µV offset, so our measurement error is 1 µV."
