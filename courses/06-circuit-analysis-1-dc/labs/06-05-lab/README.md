# Lab 06-05 · Mesh Analysis, Loop Analysis and Shared Returns

**Chapter:** [06-05](../../chapters/06-05-mesh-analysis.md) · **Notebook:** [06-05-meshes.ipynb](06-05-meshes.ipynb) · **Time:** about 90 minutes (plus 45 minutes for the optional hardware part)

## Objective

1. Build mesh matrices from a description of which meshes pass through which branches, and handle current sources with constraint rows (the dual of MNA).
2. Compare the number of unknowns of mesh and nodal analysis, and confirm both against ngspice.
3. Solve a nonplanar circuit by loop analysis on an automatically found spanning tree.
4. Quantify common-impedance coupling through a shared ground return, and compare it with a star ground.

## Background

Chapter sections 3.1 to 3.6 and Examples 06-05.1 to 06-05.5. You need Python with NumPy and Matplotlib, and ngspice for Part 2 (see [SETUP.md](../../../../SETUP.md)); without ngspice the notebook skips the comparison and the rest still runs.

## Files

| File | What it does | Checks against |
|---|---|---|
| [06-05-meshes.ipynb](06-05-meshes.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s |
| [meshes.cir](meshes.cir) | Examples 06-05.1, 06-05.2, 06-05.3 and 06-05.5, and Problems 06-05.5, 06-05.6, 06-05.10, 06-05.12 and 06-05.13, solved by ngspice | Chapter and solution answer keys |

The netlist is run in CI by [`tools/run_spice.py`](../../../../tools/run_spice.py).

## Procedure

1. **Mesh matrices (Part 1).** *Predict first:* which entry of the bridge's mesh matrix is largest, and is the matrix symmetric? Then describe Examples 06-05.1 to 06-05.3 as branch lists and let `mesh_solve()` build and solve them.
2. **Three ways (Part 2).** *Predict first:* how many unknowns does each method need for each example? Then compare mesh, nodal and ngspice results.
3. **A nonplanar circuit (Part 3).** Let `loop_analysis()` find a spanning tree of $K_{3,3}$, form the fundamental loops and solve; check the source current against a nodal solve.
4. **Shared return (Part 4).** *Predict first:* how does the ADC error scale with the motor current, with a shared return and with a star ground? Then sweep the motor current from 0 to 3 A.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | bridge mesh matrix | symmetric; largest entry $R_{33}$ = 120 Ω; $i_1$ = 0.3443 A |
| 2 | unknowns (mesh, nodal) | Example 1: 2 and 1; Example 2: 3 and 2; Example 3: 1 and 2; all values agree with ngspice to its six printed digits |
| 3 | $K_{3,3}$ | the breadth-first tree is {1–4, 1–5, 1–6, 2–4, 3–4}, the same as Problem 06-05.12; source current 4.444 A |
| 4 | ADC error at 3 A | shared return: 30.05 mV, 24.6 LSB, rising about 8.2 LSB per ampere; star ground: 50.0 µV, 0.041 LSB, independent of the motor |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 06-05.a | largest bridge mesh-matrix entry | 120 | Ω |
| Lab 06-05.b | nodal unknowns, Example 06-05.1 | 1 | — |
| Lab 06-05.c | ground offset at 3 A, shared return | 30.05 | mV |
| Lab 06-05.d | ADC error at 3 A, shared return | 24.6 | LSB |
| Lab 06-05.e | error slope, shared return | 8.2 | LSB/A |
| Lab 06-05.f | ADC error at 3 A, star ground | 0.041 | LSB |

## Discussion questions

1. `mesh_solve()` never forms a supermesh, yet it solves Example 06-05.3. Where is the supermesh hiding?
2. In Part 2, Example 06-05.3 needs fewer mesh unknowns than nodal unknowns, while Example 06-05.2 is the other way round. What feature of each circuit decides it?
3. Why can `loop_analysis()` solve $K_{3,3}$ when mesh analysis cannot?
4. In Part 4 the error with a shared return is $R_g(I_m + I_s)$. Why does the star ground not simply move the problem to the motor's own return trace?

<details><summary>Answers to the discussion questions</summary>

1. The current source's unknown voltage appears, with opposite signs, in the KVL rows of both meshes it borders. Eliminating it (adding the two rows) leaves KVL around the combined loop, which is the supermesh equation; the constraint row is the supermesh's constraint. The solver keeps the voltage as an unknown, exactly as MNA keeps a voltage source's current.
2. Sources. Each current source removes a mesh unknown and each voltage source removes a node unknown. Example 06-05.3 has a current source (and a voltage source fixing one node), so mesh needs 1 unknown and nodal 2; the bridge has only a voltage source, so nodal needs 2 and mesh 3.
3. Loop analysis does not need a planar drawing: any spanning tree defines $b - n + 1$ fundamental loops, one per link, and their KVL equations are independent because each link appears in exactly one loop. Meshes are just one convenient choice of loops for planar circuits.
4. The motor's return still carries the motor current, but the motor does not care: its terminal voltage changes by tens of millivolts out of 5 V. What mattered was the voltage *at the sensor's ground*, which is now set by the sensor's own small current through its own trace. Separating returns moves each circuit's ground drop to the circuit that causes it.

</details>

## Optional hardware version

On a breadboard, power a small DC motor (or a 10 Ω power resistor drawing about 0.5 A from 5 V) and a 10 kΩ–10 kΩ divider (the "sensor") from one bench supply, returning both through a single long thin wire (a meter of 30 AWG wire is roughly a third of an ohm). Measure the divider's output with a multimeter referenced to the supply's − terminal, with the motor on and off. Then give the divider its own return wire to the supply and repeat. The shift in the first case is the shared-return offset of Example 06-05.5.
