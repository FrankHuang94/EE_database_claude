# Problems 06-06 · Dependent Sources

Chapter: [06-06](../chapters/06-06-dependent-sources.md) · Worked solutions: [06-06 solutions](../solutions/06-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** passive sign convention; small-signal models with DC supplies replaced by small-signal grounds; $V_T$ = 25.852 mV (300 K). With resistances in kΩ and voltages in V, currents come out in mA and powers in mW. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 06-06.1 [A]

**Name that source.** Classify each source and give its gain with units: (a) a current source whose value is $0.04\,v_x$, with $v_x$ in volts and the current in amperes; (b) a voltage source equal to $5000\,i_x$; (c) a current source equal to $80\,i_x$; (d) a voltage source equal to $-20\,v_x$. Which of them model a bipolar transistor, a MOSFET, an inverting amplifier and a photodiode transimpedance amplifier?

### Problem 06-06.2 [A]

**A VCVS behind a divider.** A 2 V source drives a divider of $R_1$ = 1 kΩ (top) and $R_2$ = 3 kΩ (bottom); $v_x$ is the voltage across $R_2$. A VCVS of value $10\,v_x$ drives a 500 Ω load through a 100 Ω output resistance. (a) Find $v_x$ and the load voltage. (b) Find the power in the load, the power delivered by the VCVS, and the power delivered by the 2 V source. (c) Where does the extra power come from in a real amplifier?

### Problem 06-06.3 [A]

**A CCCS with feedback.** A 2 mA source pushes current into node 1; $R_1$ = 5 kΩ connects node 1 to ground and carries the controlling current $i_x$ (downward); $R_{12}$ = 10 kΩ joins nodes 1 and 2; $R_2$ = 2 kΩ connects node 2 to ground; a CCCS pushes $4\,i_x$ into node 2 from ground. (a) Write the nodal equations and the matrix; show it is not symmetric. (b) Solve for $v_1$, $v_2$ and $i_x$. (c) Check the power balance.

### Problem 06-06.4 [B]

**When the matrix goes singular.** In Example 06-06.1's circuit, let the VCCS gain $g$ (in mS) be a variable. (a) Show that $v_2/v_1 = 0.5 - 2g$ and $v_1 = 1/(0.625 + 0.5g)$ V. (b) Find the determinant of the nodal matrix as a function of $g$, and the value of $g$ at which it vanishes. What does a negative $g$ mean physically? (c) Find $v_1$ and $v_2$ for $g = -1$ mS, and comment.

### Problem 06-06.5 [B]

**A CCVS in mesh analysis.** Mesh 1 contains a 10 V source (rise) and $R_1$ = 2 Ω of its own and shares $R_2$ = 4 Ω with mesh 2. Mesh 2 contains $R_3$ = 6 Ω of its own and a CCVS of value $3\,i_1$ (Ω × A), a rise in mesh 2's direction, where $i_1$ is the current in $R_1$. (a) Write the mesh equations and the (nonsymmetric) matrix. (b) Solve for the mesh currents. (c) Find the power delivered by each source and check the balance.

### Problem 06-06.6 [B]

**A common-source amplifier.** A MOSFET with $g_m$ = 4 mS and $r_o$ = 25 kΩ has $R_D$ = 5 kΩ and drives a 20 kΩ load (AC-coupled, so the load appears in parallel with $R_D$ for signals). The source is grounded. (a) Find the intrinsic gain. (b) Find the voltage gain $v_{out}/v_{gs}$. (c) Find the output resistance seen by the load.

### Problem 06-06.7 [B]

**Degeneration against β spread.** A bipolar transistor is biased at $I_C$ = 1 mA, with $R_C$ = 5 kΩ, driven from a source with $R_s$ = 2 kΩ. Its $\beta$ may be anywhere from 60 to 120. (a) Find $g_m$ and $r_\pi$ for $\beta$ = 120 and for $\beta$ = 60. (b) With no emitter resistor, find the gain $v_o/v_s$ for each $\beta$ and the percentage change. (c) Repeat with $R_E$ = 200 Ω. (d) With an ideal source ($R_s$ = 0) and $R_E$ = 200 Ω, find the input resistance at the base and the gain for $\beta$ = 120, and compare with $-R_C/R_E$.

### Problem 06-06.8 [B]

**Output resistance by a test source.** A MOSFET with $g_m$ = 2 mS and $r_o$ = 50 kΩ has $R_S$ = 1 kΩ from source to ground, and its gate is held at small-signal ground. Apply a test current $i_t$ into the drain and show that the resistance looking into the drain is $R_{out} = R_S + r_o(1 + g_mR_S)$. Evaluate it and compare with $r_o$. (This boost is the principle of the cascode, Course 12.)

### Problem 06-06.9 [B]

**Miller loading.** An inverting amplifier with gain −200 (an ideal VCVS) has a 1 MΩ resistor from its input to its output. It is driven by a 10 mV source with 10 kΩ source resistance. (a) Find the input resistance due to the feedback resistor. (b) Find the amplifier's input voltage and output voltage. (c) Find the overall gain from the source, and explain why it is far below 200.

### Problem 06-06.10 [C]

**Negative resistance and the edge of stability.** A 1 mA current source drives a node with 10 kΩ to ground. A negative resistance $-R_n$ (made, for example, from the circuit of Example 06-06.4) is connected from the node to ground. (a) Find the node voltage for $R_n$ = 20 kΩ and for 12.5 kΩ. (b) What happens as $R_n$ approaches 10 kΩ? Relate this to the determinant of the nodal matrix. (c) Show that a VCCS that pushes current $g\,v$ into the node (from ground) is a negative resistance $-1/g$, and give $g$ for $R_n$ = 20 kΩ.

### Problem 06-06.11 [C]

**An inverting amplifier with finite gain.** An op-amp, modeled as a VCVS $A(v_+ - v_-)$ with infinite input resistance and zero output resistance, has $A = 10^4$. It is used in an inverting amplifier with $R_1$ = 1 kΩ and $R_2$ = 10 kΩ, the + input grounded. (a) Derive the closed-loop gain $v_{out}/v_{in} = -(R_2/R_1)/\bigl(1 + (1 + R_2/R_1)/A\bigr)$. (b) Evaluate it and the gain error in ppm. (c) Find the voltage at the − input for $v_{in}$ = 1 V (the "virtual ground"). (d) Find the input resistance seen by the source.

### Problem 06-06.12 [B]

**Stamping a VCCS.** Assemble the MNA system for this netlist (unknowns $v_1$, $v_2$, $v_3$ and the current $j$ into the + terminal of V1), solve it, and find the voltage gain $v_3/v_1$:

```text
V1 1 0 1
R1 1 2 1k
R2 2 0 1k
G1 3 0 2 0 10m
R3 3 0 2k
```

`G1` drives $10\ \text{mS}\times v_2$ from node 3 through itself to ground.

### Problem 06-06.13 [C]

**A source follower.** A MOSFET with $g_m$ = 2 mS and $r_o$ = 50 kΩ has its drain at small-signal ground and $R_S$ = 2 kΩ from source to ground; the output is the source voltage. (a) Derive the gain $v_s/v_g = g_m(r_o\parallel R_S)/\bigl(1 + g_m(r_o\parallel R_S)\bigr)$ and evaluate it. (b) Find the output resistance, and explain why it is close to $1/g_m$.

### Problem 06-06.14 [B]

**How good is a current mirror?** A current mirror copies a 100 µA reference to its output: model it as a CCCS of gain 1, controlled by the reference current, in parallel with an output resistance $r_o$, both from the output node to ground. The output node is connected to a 5 V supply through $R_L$ = 20 kΩ. (a) For $r_o$ = 100 kΩ, find the output voltage, the output current and the copying error. (b) Repeat for $r_o$ = 1 MΩ. (c) What does this say about why output resistance is the key specification of a current source?

---

## Objective coverage

| Learning objective (chapter 06-06) | Problems |
|---|---|
| 1. The four dependent sources and what they model | 1, 2, 14 |
| 2. Nodal and mesh analysis; nonsymmetric matrices | 3, 4, 5, 12 |
| 3. The test-source method; reflected and negative resistance | 8, 9, 10 |
| 4. Transistor and op-amp models | 6, 7, 11, 13, 14 |
| 5. SPICE elements and stamps | 12 |
