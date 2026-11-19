# Problems 06-05 · Mesh Analysis

Chapter: [06-05](../chapters/06-05-mesh-analysis.md) · Worked solutions: [06-05 solutions](../solutions/06-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** all mesh currents clockwise unless stated; passive sign convention; a source is a "rise" in a mesh when the mesh direction passes through it from − to +. With resistances in kΩ and voltages in V, currents come out in mA. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution. Problems 06-05.8, 06-05.12 and 06-05.13 expect a computer (NumPy) for part of the work.

---

## Problems

### Problem 06-05.1 [A]

**Counting unknowns.** For each planar circuit, give the number of mesh equations and the number of nodal unknowns after sources are used (§3.6). (a) 8 nodes and 13 branches, with its only source a voltage source in series with a resistor inside one branch (so it fixes no node voltage and no mesh current). (b) The same circuit, but two of its branches are grounded voltage sources and one outer branch is a current source. (c) A ladder of $k$ sections (each a series resistor followed by a shunt resistor to ground) driven by one voltage source. (d) $p$ resistors all connected in parallel across one voltage source.

### Problem 06-05.2 [A]

**Three meshes by inspection.** Three meshes sit side by side. Mesh 1 contains a 12 V source (a rise in its direction) and 1 Ω of its own; meshes 1 and 2 share 3 Ω; mesh 2 has 2 Ω of its own; meshes 2 and 3 share 6 Ω; mesh 3 has 4 Ω of its own and a 6 V source that is a rise in its direction. (a) Write $\mathbf{R}$ and $\mathbf{v}$. (b) Solve for the mesh currents. (c) Find the currents in the two shared resistors. (d) Check the power balance.

### Problem 06-05.3 [A]

**Two meshes by Cramer's rule.** Mesh 1 contains a 10 V source (rise) and 2 Ω of its own; the meshes share 3 Ω; mesh 2 has 5 Ω of its own and a 5 V source that is a rise in mesh 2's direction. (a) Write the mesh equations and solve them with Cramer's rule. (b) Find the current in the shared resistor and its direction. (c) Check the power balance.

### Problem 06-05.4 [B]

**A current source on an outer branch.** Mesh 1's outer branch is a 2 A current source pointing in mesh 1's direction, in series with 4 Ω. The meshes share 6 Ω. Mesh 2 has 3 Ω of its own and a 12 V source that is a rise in its direction. (a) Why is there only one unknown? (b) Find $i_2$ and the current in the shared resistor. (c) Find the voltage across the current source (as a rise in mesh 1's direction) and the power each source delivers. Check the balance.

### Problem 06-05.5 [B]

**A supermesh in a three-mesh circuit.** Mesh 1 has a 20 V source (rise) and 2 Ω of its own; mesh 2 has 4 Ω of its own; mesh 3 has 6 Ω of its own. Meshes 1 and 2 share a 2 A current source pointing up (in the shared branch, mesh 1 flows down and mesh 2 flows up); meshes 2 and 3 share 3 Ω. (a) Write the constraint, the supermesh KVL equation and mesh 3's equation. (b) Solve for the three mesh currents. (c) Find the current source's voltage and the power it delivers, and check the balance.

### Problem 06-05.6 [B]

**Two batteries in parallel.** Battery A (12.6 V, internal resistance 50 mΩ) and battery B (12.0 V, 80 mΩ) are connected in parallel, + to +, and feed a 1.2 Ω load. Mesh 1 is the loop through the two batteries; mesh 2 is the loop through battery B and the load. (a) Write and solve the mesh equations. (b) Find the current in each battery and say which one is charging. (c) Find the load voltage and power. (d) Check the power balance. What does this say about paralleling batteries at different states of charge?

### Problem 06-05.7 [B]

**The same circuit both ways.** Solve Problem 06-04.4's circuit (a 9 V source holding node A; $R_{AB}$ = 1 kΩ, $R_{B0}$ = 2 kΩ, $R_{BC}$ = 1 kΩ, $R_{C0}$ = 1 kΩ; 2 mA pushed into node C from ground) by mesh analysis. Use mesh 1 through the source, $R_{AB}$ and $R_{B0}$; mesh 2 through $R_{B0}$, $R_{BC}$ and $R_{C0}$; mesh 3 between $R_{C0}$ and the current source. (a) How many unknowns does each method need here? (b) Find the mesh currents. (c) Recover $v_B$ and $v_C$ and compare with Problem 06-04.4.

### Problem 06-05.8 [C]

**Why the mesh matrix is positive definite.** (a) For a planar circuit with clockwise mesh currents, define each resistor's mesh-incidence vector $\mathbf{m}_r$ (+1 for each mesh that traverses the resistor in its reference direction, −1 for each that traverses it the opposite way). Show that the stamp rule of §3.3 gives $\mathbf{R} = \sum_r R_r\,\mathbf{m}_r\mathbf{m}_r^\mathsf{T}$ and hence $\mathbf{i}^\mathsf{T}\mathbf{R}\,\mathbf{i} = \sum_r R_r\,i_r^2$. (b) Explain why $\mathbf{R}$ is positive definite unless the circuit contains a loop of zero-resistance elements. (c) For Problem 06-05.2's circuit, compute $\mathbf{i}^\mathsf{T}\mathbf{R}\,\mathbf{i}$ at the solution and compare it with $\mathbf{i}^\mathsf{T}\mathbf{v}$. (d) Find that matrix's eigenvalues numerically.

### Problem 06-05.9 [C]

**The dual of a supermesh.** Construct the dual of Example 06-05.3's circuit. (a) What does the shared 3 A current source become, and what do the series 2 Ω and 6 Ω of mesh 2 become? (b) Write the dual's nodal equations; you will need a supernode. (c) Solve them and compare with the mesh currents of Example 06-05.3.

### Problem 06-05.10 [B]

**A bridge with a meter, by meshes.** Re-solve Problem 06-04.6 (5 V excitation; $R_1$ = 1 kΩ top to A, $R_2$ = 1 kΩ A to ground, $R_3$ = 1 kΩ top to B, $R_4$ = 1.1 kΩ B to ground, a 100 Ω galvanometer between A and B) with three mesh currents laid out as in Figure 3 of the chapter: mesh 1 through the source, $R_1$ and $R_2$; mesh 2 through $R_1$, $R_3$ and the galvanometer; mesh 3 through the galvanometer, $R_4$ and $R_2$. (a) Write $\mathbf{R}$ and $\mathbf{v}$. (b) Solve and find the galvanometer current and its direction. (c) Find the source current. (d) Which method needed fewer unknowns here?

### Problem 06-05.11 [B]

**A ladder attenuator.** A 10 V source drives three ladder sections, each a 1 kΩ series resistor followed by a 2 kΩ shunt resistor to ground (the last shunt is the output). (a) Write the 3 × 3 mesh matrix; what structure does it have? (b) Solve for the mesh currents. (c) Find the output voltage, the two intermediate node voltages and the input resistance.

### Problem 06-05.12 [C]

**Loop analysis of a nonplanar circuit.** Figure 2 of the chapter shows $K_{3,3}$: nodes 1, 2, 3 each joined to nodes 4, 5, 6 by 1 Ω resistors, except that the 1–4 branch is a 10 V source (+ toward node 1) in series with 1 Ω. (a) Count nodes, branches and independent loops. (b) Take the spanning tree made of branches 1–4, 1–5, 1–6, 2–4 and 3–4. List the four fundamental loops (one per link 2–5, 2–6, 3–5, 3–6), each oriented along its link from the top node to the bottom node. (c) Write the 4 × 4 loop matrix and the source vector. (d) Use symmetry to solve it, and find the source current and the resistance that the rest of the network presents to the source branch. (e) Check with nodal analysis (by computer).

### Problem 06-05.13 [C]

**The resistor cube.** Twelve 1 Ω resistors form the edges of a cube. (a) Show that the cube's graph is planar (draw it), and count its meshes. (b) A source is connected between two *opposite* corners. Show that the resulting circuit is nonplanar (hint: the cube's graph is bipartite, and a planar bipartite graph has at most $2n - 4$ edges). (c) Use symmetry to find the resistance between opposite corners. (d) By computer (nodal or mesh), find the resistance between adjacent corners and between the ends of a face diagonal.

### Problem 06-05.14 [B]

**Ground offset and ADC resolution.** A sensor shares a 5 mΩ return trace with a load drawing 4 A. The sensor's output is read by an ADC referenced to the supply's − terminal. (a) Find the ground offset (ignore the sensor's own small current). (b) Express it in LSBs of a 12-bit and of a 16-bit ADC, both over 5 V. (c) The sensor gets its own 5 mΩ return and draws 2 mA. Find the offset now, in µV and in 16-bit LSBs. (d) Name a second way to remove the error without rerouting the ground.

---

## Objective coverage

| Learning objective (chapter 06-05) | Problems |
|---|---|
| 1. Mesh currents and KVL in mesh currents | 1, 2, 3 |
| 2. The mesh matrix by inspection and its properties | 2, 8, 11 |
| 3. Current sources: outer branches and supermeshes | 4, 5, 7, 9 |
| 4. Counting unknowns and choosing nodal or mesh | 1, 7, 10, 11 |
| 5. Planarity, loop analysis, duality, shared-impedance coupling | 6, 9, 12, 13, 14 |
