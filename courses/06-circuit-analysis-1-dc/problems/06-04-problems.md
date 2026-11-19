# Problems 06-04 · Nodal Analysis

Chapter: [06-04](../chapters/06-04-nodal-analysis.md) · Worked solutions: [06-04 solutions](../solutions/06-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** node voltages are relative to the reference node (ground); passive sign convention; a current source "into node $k$" returns through ground. With resistances in kΩ and currents in mA, voltages come out in V and powers in mW. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution. Problems 06-04.2, 06-04.10, 06-04.12 and 06-04.13 expect a computer (NumPy) for part of the work.

---

## Problems

### Problem 06-04.1 [A]

**Counting unknowns.** A circuit has 6 nodes (including the reference) and 9 branches. Two of the branches are voltage sources: one from node 1 to the reference, the other floating between nodes 3 and 4. (a) How many unknowns does basic nodal analysis start with? (b) How many unknowns would the branch-variable method of 06-03 have? (c) What is the size of the MNA matrix a simulator would build? (d) Solving by hand with a supernode, how many simultaneous equations remain, and which are they?

### Problem 06-04.2 [B]

**A matrix by inspection.** Three nodes: $R_a$ = 1 kΩ from node 1 to ground, $R_b$ = 2 kΩ between nodes 1 and 2, $R_c$ = 4 kΩ between nodes 2 and 3, $R_d$ = 5 kΩ from node 3 to ground and $R_e$ = 2.5 kΩ between nodes 1 and 3. A 3 mA source pushes current into node 1, and a 1 mA source draws current out of node 3. (a) Write $\mathbf{G}$ (in mS) and $\mathbf{i}$ (in mA) by inspection. (b) Check that $\mathbf{G}$ is symmetric and diagonally dominant, and say which rows are strictly dominant and why. (c) Solve for the node voltages (by computer or by elimination) and find the current in every resistor. (d) Check the power balance.

### Problem 06-04.3 [A]

**A negative node voltage.** A 2 mA source pushes current into node 1 and a 1 mA source draws current out of node 2. $R_1$ = 3 kΩ from node 1 to ground, $R_2$ = 6 kΩ between the nodes and $R_3$ = 3 kΩ from node 2 to ground. (a) Find $v_1$ and $v_2$ with Cramer's rule. (b) Interpret the sign of $v_2$. (c) Find the power delivered by each source and check it against the resistors' total.

### Problem 06-04.4 [B]

**A grounded voltage source.** A 9 V source holds node A at 9 V. $R_{AB}$ = 1 kΩ, $R_{B0}$ = 2 kΩ (B to ground), $R_{BC}$ = 1 kΩ and $R_{C0}$ = 1 kΩ, and a 2 mA source pushes current into node C. (a) How many unknowns are there, and why is KCL at node A not written? (b) Find $v_B$ and $v_C$. (c) Find the current and power delivered by the 9 V source, and check the power balance.

### Problem 06-04.5 [B]

**A supernode.** A 3 A source pushes current into node 1. A 10 V source floats between node 2 (+) and node 1 (−). 4 Ω connects node 1 to ground and 6 Ω connects node 2 to ground. (a) Write the supernode KCL equation and the constraint, and solve for $v_1$ and $v_2$. (b) Find the current delivered by the 10 V source and the power each source delivers; check the balance. (c) Set up the same circuit as an MNA system (unknowns $v_1$, $v_2$ and the source current $j$ into its + terminal) and confirm the sign of $j$.

### Problem 06-04.6 [B]

**A bridge with a meter.** A Wheatstone bridge is excited by 5 V at its top node (bottom grounded). $R_1$ = 1 kΩ (top to A), $R_2$ = 1 kΩ (A to ground), $R_3$ = 1 kΩ (top to B) and $R_4$ = 1.1 kΩ (B to ground). A galvanometer with 100 Ω internal resistance connects A to B. (a) Write and solve the nodal equations for $v_A$ and $v_B$. (b) Find the galvanometer current and its direction. (c) Find the open-circuit voltage between B and A (galvanometer removed) and explain why the galvanometer current is less than that voltage divided by 100 Ω. (d) Find the current the 5 V source delivers.

### Problem 06-04.7 [B]

**Stamps from a netlist.** Assemble the MNA system for the SPICE netlist below (unknowns $v_1$, $v_2$ and the current $j$ into the + terminal of V1), solve it, and interpret the sign of $j$. Recall that `I1 0 2 1` makes 1 A flow from node 0 through the source into node 2.

```text
V1 1 0 10
R1 1 2 2
R2 2 0 8
I1 0 2 1
```

Then check KCL at node 2 and the power balance.

### Problem 06-04.8 [B]

**A singular matrix.** Nodes 1 and 2 are joined by a 1 kΩ resistor, and a 1 mA current source pushes current from node 2 to node 1 through itself. Nothing else connects the pair to ground. (a) Write $\mathbf{G}$ and $\mathbf{i}$ for the two nodes and show that $\mathbf{G}$ is singular. (b) What is physically determined, and what is not? (c) A simulator adds 1 GΩ from node 2 to ground. Solve again, and explain why the answer does not depend on the size of that resistor (as long as it is the only path to ground).

### Problem 06-04.9 [C]

**Why the nodal matrix is positive definite.** (a) For a circuit of positive resistors whose nodal matrix $\mathbf{G}$ is written by inspection, prove that $\mathbf{v}^\mathsf{T}\mathbf{G}\mathbf{v} = \sum_{\text{resistors}} G_r\,(v_a - v_b)^2$, where each resistor runs between nodes $a$ and $b$ (with $v = 0$ for ground). (b) Use (a) to prove that $\mathbf{G}$ is positive definite when every node has a resistive path to ground, and hence nonsingular. (c) For Problem 06-04.2's network and the trial vector $\mathbf{v} = (1, -1, 2)$ V, compute $\mathbf{v}^\mathsf{T}\mathbf{G}\mathbf{v}$ both ways. (d) Find the smallest eigenvalue of that $\mathbf{G}$ numerically. What would it be for Problem 06-04.8's matrix?

### Problem 06-04.10 [B]

**Where to put the bump.** A 3 × 3 power grid has 20 mΩ between neighboring nodes, and each of its 9 nodes draws 1 A. (a) A single supply bump holds the center node at 0.75 V. Use symmetry to reduce the nodal equations to two unknowns, solve them by hand, and find the worst voltage. (b) Move the single bump to a corner and solve numerically. Where is the worst node, and what is its drop? (c) Use four bumps, one at each corner (all at 0.75 V). Find the worst drop. (d) Rank the three arrangements and state the design lesson.

### Problem 06-04.11 [B]

**A ladder by elimination.** A 1 A source pushes current into node 1 of a three-node ladder: 1 Ω between nodes 1 and 2, 1 Ω between nodes 2 and 3, and 2 Ω from each node to ground. (a) Write $\mathbf{G}$ and find its determinant. (b) Solve for the three node voltages with Cramer's rule. (c) Find the input resistance and the ratio $v_3/v_1$. (d) Check KCL at node 3.

### Problem 06-04.12 [C]

**How sparse is a power grid?** An $N \times N$ grid has every node an unknown (each also has a small conductance to ground, which only adds to the diagonal) and each node connected to its horizontal and vertical neighbors. (a) Show that the number of nonzero entries in $\mathbf{G}$ is $N^2 + 4N(N - 1)$. (b) For $N$ = 100, find the number of unknowns, the number of nonzeros and the fraction of the dense matrix they occupy. (c) Compare storage: dense, at 8 bytes per entry, against compressed sparse row storage (8 bytes per value plus 4 bytes per column index, plus 4 bytes for each of the $N^2 + 1$ row pointers). (d) Estimate the operation count of a dense LU factorization ($n^3/3$) for $N$ = 100, and the dense storage for $N$ = 1000. What does this say about how power grids must be solved?

### Problem 06-04.13 [C]

**Newton's method with a companion model.** A 5 V source drives node 1 through 1 kΩ; a diode from node 1 to ground obeys $i_D = I_S(e^{v/V_T} - 1)$ with $I_S = 10^{-14}$ A and $V_T$ = 25.852 mV (300 K). (a) Linearize the diode at a guess $v^{(k)}$ as a conductance $g$ in parallel with a current source $I_{eq}$, and write the nodal equation for the next iterate. (b) Starting from $v^{(0)}$ = 0.7 V, compute $g$, $I_{eq}$ and $v^{(1)}$, then $v^{(2)}$. (c) Iterate to convergence and give the diode voltage and current. (d) Why does a simulator stamp the companion model rather than the diode equation itself?

### Problem 06-04.14 [B]

**Source transformation inside nodal analysis.** A 10 V source with 2 Ω internal resistance feeds node 1. Node 1 has 3 Ω to ground and 1 Ω to node 2; node 2 has 6 Ω to ground, and a 2 A sink draws current out of node 2. (a) Replace the practical voltage source with its Norton equivalent and write the 2 × 2 nodal system. (b) Solve for $v_1$ and $v_2$. (c) Find the current the actual 10 V source delivers. Is it the Norton source's 5 A? (d) Compare the power delivered by the 10 V source with that delivered by the Norton current source, and explain why they differ although every external voltage and current is the same.

### Problem 06-04.15 [B]

**A current source in series with a resistor.** A 2 mA current source pushes current from ground through a 5 kΩ resistor into node 1. Node 1 has 2 kΩ to ground and 4 kΩ to node 2; node 2 has 4 kΩ to ground and a second 2 mA source pushing current into it from ground. (a) Write the two nodal equations, and explain why the 5 kΩ resistor does not appear in them. (b) Solve for $v_1$ and $v_2$. (c) Find the voltage across the first current source (its output terminal relative to ground), the power it delivers, and the power the 5 kΩ resistor dissipates.

### Problem 06-04.16 [B]

**A supernode in a larger circuit.** A 4 V source has its + terminal at node 1 and its − terminal at node 2. A 2 mA source pushes current from ground into node 1. Resistors: 2 kΩ from node 1 to ground, 4 kΩ from node 2 to ground, 1 kΩ from node 2 to node 3, 2 kΩ from node 3 to ground, 2 kΩ from node 3 to node 4 and 1 kΩ from node 4 to ground. A 1 mA source pushes current from ground into node 4. (a) Write the system as four equations in $v_1$ to $v_4$ (the source constraint, the supernode's KCL, and KCL at nodes 3 and 4). (b) Solve it. (c) Find the current through the 4 V source and the power it delivers.

---

## Objective coverage

| Learning objective (chapter 06-04) | Problems |
|---|---|
| 1. Node voltages and KCL in node voltages | 1, 3, 4, 15 |
| 2. The nodal matrix by inspection and its properties | 2, 8, 9, 11 |
| 3. Grounded and floating voltage sources (supernodes) | 4, 5, 6, 14, 16 |
| 4. Modified nodal analysis, stamps and sparse solvers | 1, 5, 7, 12, 13 |
| 5. Solving by hand and numerically, with checks | 2, 3, 6, 10, 11, 14, 15, 16 |
