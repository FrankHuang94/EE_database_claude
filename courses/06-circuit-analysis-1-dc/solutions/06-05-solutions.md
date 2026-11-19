# Solutions 06-05 · Mesh Analysis

Problems: [06-05 problems](../problems/06-05-problems.md) · Chapter: [06-05](../chapters/06-05-mesh-analysis.md). Every number below is recomputed by [verify_06_05.py](../verify/verify_06_05.py); the circuits of Problems 06-05.5, 06-05.6, 06-05.10, 06-05.12 and 06-05.13 are also confirmed in ngspice ([lab netlist](../labs/06-05-lab/meshes.cir)).

---

## Solutions

### Solution 06-05.1

(a) Meshes: $b - n + 1 = 13 - 8 + 1 = $ **6**. Nodal: $n - 1 = $ **7**. A voltage source in series with a resistor fixes neither a node voltage nor a mesh current, so neither count drops.

(b) Nodal: $7 - 2 = $ **5** (each grounded voltage source fixes a node). Mesh: $6 - 1 = $ **5** (the outer current source fixes a mesh current). A tie: choose by what you need to find.

(c) The ladder has $n = k + 2$ nodes (ground, the source's top node and one node per section) and $b = 2k + 1$ branches. Meshes: $2k + 1 - (k + 2) + 1 = $ **$k$**. Nodal: $(k + 1) - 1 = $ **$k$** (the source fixes its top node). Another tie.

(d) Two nodes and $p + 1$ branches. Nodal: $1 - 1 = $ **0** unknowns, since the source fixes the only non-reference node and every resistor current follows at once. Mesh: $(p + 1) - 2 + 1 = $ **$p$** equations. Parallel structure strongly favors nodal analysis.

### Solution 06-05.2

(a) $\mathbf{R} = \begin{bmatrix} 1 + 3 & -3 & 0 \\ -3 & 3 + 2 + 6 & -6 \\ 0 & -6 & 6 + 4 \end{bmatrix} = \begin{bmatrix} 4 & -3 & 0 \\ -3 & 11 & -6 \\ 0 & -6 & 10 \end{bmatrix}$ Ω, $\mathbf{v} = (12, 0, 6)$ V. Meshes 1 and 3 share nothing, so $R_{13} = 0$.

(b) Row 1 gives $i_1 = 3 + 0.75\,i_2$; row 3 gives $i_3 = 0.6 + 0.6\,i_2$. Substituting into row 2: $-3(3 + 0.75i_2) + 11i_2 - 6(0.6 + 0.6i_2) = 0$, so $5.15\,i_2 = 12.6$:

$$
i_2 = \mathbf{2.447\ A}, \qquad i_1 = \mathbf{4.835\ A}, \qquad i_3 = \mathbf{2.068\ A}
$$

(exactly 252/103, 498/103 and 213/103 A; $\det\mathbf{R} = $ **206 Ω³**).

(c) Shared 3 Ω: $i_1 - i_2 = $ **2.388 A** in mesh 1's direction. Shared 6 Ω: $i_2 - i_3 = $ **0.3786 A** in mesh 2's direction.

(d) Sources: $12\times4.835 + 6\times2.068 = $ **70.43 W**. Resistors: $1\times4.835^2 + 3\times2.388^2 + 2\times2.447^2 + 6\times0.3786^2 + 4\times2.068^2 = 23.38 + 17.11 + 11.97 + 0.86 + 17.11 = 70.43$ W ✓.

### Solution 06-05.3

(a) $\begin{bmatrix} 5 & -3 \\ -3 & 8 \end{bmatrix}\begin{bmatrix} i_1 \\ i_2\end{bmatrix} = \begin{bmatrix} 10 \\ 5 \end{bmatrix}$; $\Delta = 40 - 9 = $ **31 Ω²**.

$$
i_1 = \frac{10\times8 - (-3)\times5}{31} = \frac{95}{31} = \mathbf{3.065\ A}, \qquad
i_2 = \frac{5\times5 - 10\times(-3)}{31} = \frac{55}{31} = \mathbf{1.774\ A}.
$$

(b) $i_1 - i_2 = $ **1.290 A**, flowing in mesh 1's direction through the shared resistor (positive, so mesh 1 wins).

(c) The 10 V source delivers $10\times3.065 = $ **30.65 W** and the 5 V source $5\times1.774 = $ **8.871 W**: **39.52 W** in all. Resistors: $2\times3.065^2 + 3\times1.290^2 + 5\times1.774^2 = 18.78 + 4.99 + 15.74 = 39.52$ W ✓.

### Solution 06-05.4

(a) The current source sits on mesh 1's outer branch, so it fixes $i_1 = 2$ A. Only $i_2$ is unknown, and mesh 1's KVL is not needed (it would give the source's voltage).

(b) Mesh 2: $6(i_2 - 2) + 3i_2 = 12$, so $9i_2 = 24$ and $i_2 = $ **2.667 A**. The shared 6 Ω carries $i_1 - i_2 = $ **−0.667 A** in mesh 1's direction, that is, 0.667 A in mesh 2's direction.

(c) KVL around mesh 1, with the source's voltage $v_s$ as a rise: $v_s = 4\times2 + 6\times(2 - 2.667) = 8 - 4 = $ **4 V**. The current source delivers $4\times2 = $ **8 W** and the 12 V source $12\times2.667 = $ **32 W**. Resistors: $4\times2^2 + 6\times0.667^2 + 3\times2.667^2 = 16 + 2.667 + 21.33 = $ **40 W** $= 8 + 32$ ✓.

### Solution 06-05.5

(a) In the shared branch mesh 2 flows up and mesh 1 down, so the source's upward current is $i_2 - i_1 = 2$ A. The supermesh (meshes 1 and 2 without the source's branch) contains the 20 V source, 2 Ω, 4 Ω and the shared 3 Ω:

$$
20 = 2i_1 + 4i_2 + 3(i_2 - i_3), \qquad \text{mesh 3: } 3(i_3 - i_2) + 6i_3 = 0 .
$$

(b) Mesh 3 gives $i_3 = i_2/3$. Then the supermesh equation becomes $20 = 2i_1 + 6i_2$, and with $i_1 = i_2 - 2$: $8i_2 = 24$. So $i_2 = $ **3 A**, $i_1 = $ **1 A**, $i_3 = $ **1 A**.

(c) KVL around mesh 1 alone, from the bottom of the current source to its top: $20 - 2\times1 = $ **18 V** (check with mesh 2: $4\times3 + 3\times(3 - 1) = 18$ V ✓). The source delivers $18\times2 = $ **36 W**; the 20 V source delivers 20 W. Resistors: $2\times1 + 4\times9 + 3\times4 + 6\times1 = $ **56 W** $= 36 + 20$ ✓.

### Solution 06-05.6

(a) Mesh 1 goes up through A and down through B's branch (passing B from + to −): $v_1 = 12.6 - 12.0 = 0.6$ V. Mesh 2 goes up through B's branch and down through the load: $v_2 = 12.0$ V. Resistances: $R_{11} = 0.05 + 0.08 = 0.13$, $R_{22} = 0.08 + 1.2 = 1.28$, $R_{12} = -0.08$ Ω. $\Delta = 0.13\times1.28 - 0.08^2 = $ **0.16 Ω²**:

$$
i_1 = \frac{0.6\times1.28 + 0.08\times12}{0.16} = \mathbf{10.8\ A}, \qquad i_2 = \frac{0.13\times12 + 0.08\times0.6}{0.16} = \mathbf{10.05\ A}.
$$

(b) Battery A carries $i_1$ = 10.8 A out of its + terminal (discharging). Battery B's branch carries $i_2 - i_1 = -0.75$ A upward, that is, **0.75 A** *into* its + terminal: B is **charging**, fed by A.

(c) Load: **10.05 A**, $1.2\times10.05 = $ **12.06 V**, $1.2\times10.05^2 = $ **121.2 W**.

(d) A delivers $12.6\times10.8 = $ **136.08 W**. It goes to the load (121.20 W), to charging B ($12.0\times0.75 = $ **9.0 W**), and to the internal resistances ($0.05\times10.8^2 = 5.832$ W and $0.08\times0.75^2 = 0.045$ W): $121.20 + 9.0 + 5.832 + 0.045 = 136.08$ W ✓. Paralleling batteries at different voltages makes the stronger one charge the weaker through their small internal resistances; with no load the circulating current would be $0.6/0.13 = 4.6$ A. Packs therefore parallel only matched cells, or isolate strings until their voltages agree.

### Solution 06-05.7

(a) Nodal: $(4 - 1) - 1 = $ **2** (nodes A, B, C plus ground; A fixed). Mesh: three meshes, minus one for the current source on mesh 3's outer branch: **2**. A tie.

(b) Mesh 3 runs up through $R_{C0}$ and down through the current source; the source pushes current up, against mesh 3's direction, so $i_3 = $ **−2 mA**. In kΩ and mA, mesh 1: $3i_1 - 2i_2 = 9$; mesh 2: $-2i_1 + (2 + 1 + 1)i_2 - 1\times i_3 = 0$, that is, $-2i_1 + 4i_2 = -2$. From mesh 1, $i_1 = (9 + 2i_2)/3$; substituting, $8i_2 = 12$: $i_2 = $ **1.5 mA** and $i_1 = $ **4 mA**.

(c) $v_B = R_{B0}(i_1 - i_2) = 2\times2.5 = $ **5 V** and $v_C = R_{C0}(i_2 - i_3) = 1\times3.5 = $ **3.5 V**, exactly as in Problem 06-04.4. The source current, 4 mA, is now simply $i_1$.

### Solution 06-05.8

(a) A resistor on mesh $k$'s outer boundary has $\mathbf{m}_r = \mathbf{e}_k$; one shared by meshes $j$ and $k$, referenced in mesh $j$'s direction, has $\mathbf{m}_r = \mathbf{e}_j - \mathbf{e}_k$ (clockwise neighbors traverse it oppositely). The outer product $R_r\mathbf{m}_r\mathbf{m}_r^\mathsf{T}$ is $R_r$ at $(k,k)$ for an outer resistor, and $+R_r$ at $(j,j)$ and $(k,k)$ with $-R_r$ at $(j,k)$ and $(k,j)$ for a shared one: exactly the by-inspection rule. Summing, $\mathbf{R} = \sum_r R_r\mathbf{m}_r\mathbf{m}_r^\mathsf{T}$. The branch current is $i_r = \mathbf{m}_r^\mathsf{T}\mathbf{i}$, so

$$
\mathbf{i}^\mathsf{T}\mathbf{R}\,\mathbf{i} = \sum_r R_r(\mathbf{m}_r^\mathsf{T}\mathbf{i})^2 = \sum_r R_r\,i_r^2 .
$$

(b) Each term is non-negative, so $\mathbf{i}^\mathsf{T}\mathbf{R}\,\mathbf{i} \ge 0$, with equality only if every resistor carries zero current. Mesh currents that are not all zero but leave every resistor without current would have to circulate entirely through zero-resistance elements: a loop of ideal voltage sources or wires. Without such a loop, $\mathbf{i}^\mathsf{T}\mathbf{R}\,\mathbf{i} > 0$ for every $\mathbf{i} \ne \mathbf{0}$, so $\mathbf{R}$ is positive definite and invertible.

(c) At the solution of Problem 06-05.2, $\mathbf{i}^\mathsf{T}\mathbf{R}\,\mathbf{i} = $ **70.43 W**, the resistor total, and $\mathbf{i}^\mathsf{T}\mathbf{v} = 12\times4.835 + 6\times2.068 = 70.43$ W, the source total: since $\mathbf{R}\,\mathbf{i} = \mathbf{v}$, the two are the same number, which is the power balance in matrix form.

(d) `numpy.linalg.eigvalsh` gives **2**, **6.092** and **16.91** Ω, all positive.

### Solution 06-05.9

(a) The shared 3 A current source becomes a **3 V voltage source** between dual nodes 1 and 2, a floating source. The 2 Ω and 6 Ω, in series on mesh 2's outer boundary, become **2 S and 6 S in parallel** from dual node 2 to the reference. The 36 V source and 4 Ω on mesh 1's boundary become a 36 A source into node 1 and 4 S from node 1 to the reference.

(b) The 3 V source makes {1, 2} a supernode. Its KCL, currents leaving through the conductances equal to the 36 A entering, and the constraint (the current source's $i_2 - i_1 = 3$ becomes $v_2 - v_1 = 3$):

$$
4v_1 + (2 + 6)v_2 = 36, \qquad v_2 - v_1 = 3 .
$$

(c) $4v_1 + 8(v_1 + 3) = 36$, so $v_1 = $ **1 V** and $v_2 = $ **4 V**: the same numbers as $i_1$ = 1 A and $i_2$ = 4 A in Example 06-05.3. The dual of a supermesh is a supernode.

### Solution 06-05.10

(a) In kΩ: $R_{11} = R_1 + R_2 = 2$, $R_{22} = R_1 + R_3 + R_G = 2.1$, $R_{33} = R_G + R_4 + R_2 = 2.2$; shared $R_{12} = -R_1 = -1$, $R_{13} = -R_2 = -1$, $R_{23} = -R_G = -0.1$. $\mathbf{v} = (5, 0, 0)$ V. $\det\mathbf{R} = $ **4.72 kΩ³**.

(b) Solving: $i_1 = $ **4.883 mA**, $i_2 = $ **2.436 mA**, $i_3 = $ **2.331 mA**. Mesh 2 traverses the galvanometer from B to A and mesh 3 from A to B, so the current from A to B is $i_3 - i_2 = $ **−0.1059 mA**: 0.1059 mA (105.9 µA) flows from B to A, as in Problem 06-04.6.

(c) The source current is $i_1$ = **4.883 mA** ✓.

(d) Nodal needed 2 unknowns ($v_A$, $v_B$; the top node is fixed by the source); mesh needed 3. Nodal wins, as it did for the plain bridge (Example 06-05.2).

(e) First, nodal analysis can be stamped directly from a netlist, element by element, because every element names its two nodes; mesh analysis needs a planar drawing (which may not exist) or a spanning tree to define its loops. Second, every kind of element, including nonlinear and dependent ones, fits the same modified nodal framework, so one formulation serves every circuit; the nodal matrix is also typically sparser (06-04, §3.5 and the practitioner section of this chapter).

### Solution 06-05.11

(a) Mesh $k$ contains its series 1 kΩ and the shunts on either side; neighbors share one 2 kΩ shunt:

$$
\mathbf{R} = \begin{bmatrix} 3 & -2 & 0 \\ -2 & 5 & -2 \\ 0 & -2 & 5 \end{bmatrix}\ \text{kΩ}, \qquad \mathbf{v} = (10, 0, 0)\ \text{V}.
$$

It is **tridiagonal**: each mesh touches only its neighbors, the same structure as the ladder's nodal matrix (Problem 06-04.11). $\det\mathbf{R} = 3(25 - 4) + 2(-10) = $ **43 kΩ³**.

(b) Cramer's rule with first-row cofactors 21, 10 and 4: $i_1 = 210/43 = $ **4.884 mA**, $i_2 = 100/43 = $ **2.326 mA**, $i_3 = 40/43 = $ **0.9302 mA**.

(c) Output: $2\times i_3 = 80/43 = $ **1.860 V**. Intermediate nodes: $2(i_1 - i_2) = $ **5.116 V** and $2(i_2 - i_3) = $ **2.791 V**. Input resistance: $10\ \text{V}/4.884\ \text{mA} = $ **2.048 kΩ**.

### Solution 06-05.12

(a) $n = 6$, $b = 9$ (the source and its 1 Ω form one branch): $b - n + 1 = $ **4** independent loops.

(b) The tree {1–4, 1–5, 1–6, 2–4, 3–4} has $n - 1 = 5$ branches and reaches every node. The fundamental loops, each oriented along its link from top to bottom node and back through the tree:

- $L_{25}$: 2 → 5 → 1 → 4 → 2;
- $L_{26}$: 2 → 6 → 1 → 4 → 2;
- $L_{35}$: 3 → 5 → 1 → 4 → 3;
- $L_{36}$: 3 → 6 → 1 → 4 → 3.

(c) Each loop has four 1 Ω branches: diagonal 4 Ω. Shared branches, all traversed in the same direction: $L_{25}$ and $L_{26}$ share 1→4 and 4→2 (2 Ω); $L_{25}$ and $L_{35}$ share 5→1 and 1→4 (2 Ω); $L_{25}$ and $L_{36}$ share only 1→4 (1 Ω); and similarly for the others. Every loop passes through the source from + (node 1) to − (node 4), a drop of 10 V:

$$
\begin{bmatrix} 4 & 2 & 2 & 1 \\ 2 & 4 & 1 & 2 \\ 2 & 1 & 4 & 2 \\ 1 & 2 & 2 & 4 \end{bmatrix}
\begin{bmatrix} i_{25} \\ i_{26} \\ i_{35} \\ i_{36} \end{bmatrix} =
\begin{bmatrix} -10 \\ -10 \\ -10 \\ -10 \end{bmatrix}.
$$

(The off-diagonal signs are + here because shared branches are traversed in the same direction; that is a property of this choice of loops, not of loop analysis in general.)

(d) By symmetry all four loop currents are equal, and every row sums to 9: $9i = -10$, so $i = $ **−1.111 A**. Each link carries 1.111 A from bottom to top. The source branch carries all four loop currents: **4.444 A** out of the source's + terminal, so the source delivers $10\times4.444 = 44.44$ W. The source sees $10/4.444 = 2.25$ Ω, of which 1 Ω is its own, so the rest of the network presents **1.25 Ω**.

(e) A nodal solve (5 unknowns, ground at node 6) gives the same 4.444 A. As a further check, Foster's theorem (R. M. Foster, 1949) says that the effective resistances across the edges of a network of $n$ nodes, each divided by its own resistance, sum to $n - 1$. In $K_{3,3}$ with all branches 1 Ω, all nine edges are equivalent, so each has $5/9$ Ω across it; the remainder in parallel with 1 Ω must give $5/9$ Ω, so the remainder is $1\times(5/9)/(1 - 5/9) = 1.25$ Ω ✓.

### Solution 06-05.13

(a) Draw the cube as a small square inside a large square with corresponding corners joined: no crossings, so it is planar. $n = 8$, $b = 12$: **5** meshes (four quadrilaterals around the inner square, plus the inner square itself).

(b) Color each corner by the parity of its coordinates (000, 011, 101, 110 even; the rest odd): every edge joins opposite parities, so the graph is bipartite, and opposite corners (000 and 111) have opposite parities, so adding the source branch keeps it bipartite. In a planar bipartite graph every face has at least 4 edges, so $2b \ge 4f$; with Euler's $f = 2 - n + b$ this gives $b \le 2n - 4 = 12$. The cube plus the source branch has $b = 13 > 12$: **nonplanar**. (Mesh analysis cannot be used directly; symmetry or nodal analysis can.)

(c) Inject 1 A at one corner and remove it at the opposite corner. By symmetry it splits equally into the 3 edges leaving the first corner (1/3 A each), then each of those corners splits its 1/3 A into 2 edges (1/6 A each on the 6 middle edges), and 3 edges carry 1/3 A each into the far corner. Along any path: $1/3 + 1/6 + 1/3 = 5/6$ V, so $R = $ **0.8333 Ω** (5/6 Ω).

(d) A nodal solve gives **0.5833 Ω** (7/12 Ω) between adjacent corners and **0.75 Ω** (3/4 Ω) across a face diagonal. Foster's check: all 12 edges are equivalent, and $12\times7/12 = 7 = n - 1$ ✓.

### Solution 06-05.14

(a) $5\ \text{mΩ}\times4\ \text{A} = $ **20 mV**.

(b) 12-bit LSB: $5/4096 = 1.221$ mV, so the offset is **16.4 LSB**. 16-bit LSB: $5/65{,}536 = $ **76.29 µV**, so it is **262 LSB**: the bottom eight bits of the 16-bit converter are meaningless.

(c) The sensor's own return carries only its 2 mA: $5\ \text{mΩ}\times2\ \text{mA} = $ **10 µV**, or **0.131 LSB** of the 16-bit converter: negligible, and no longer dependent on the load.

(d) Measure the sensor differentially: connect the ADC's negative (or reference-ground) input to the sensor's own ground at the sensor (Kelvin or pseudo-differential sensing), so that the ground offset appears equally on both inputs and cancels.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-05.1a | meshes, (a) | 6 | — |
| 06-05.1b | nodal unknowns, (a) | 7 | — |
| 06-05.1c | mesh unknowns, (b) | 5 | — |
| 06-05.1d | nodal unknowns, (b) | 5 | — |
| 06-05.1e | nodal unknowns, (d) | 0 | — |
| 06-05.2a | i_1 | 4.835 | A |
| 06-05.2b | i_2 | 2.447 | A |
| 06-05.2c | i_3 | 2.068 | A |
| 06-05.2d | determinant | 206 | Ω³ |
| 06-05.2e | current in the shared 3 Ω | 2.388 | A |
| 06-05.2f | current in the shared 6 Ω | 0.3786 | A |
| 06-05.2g | source power | 70.43 | W |
| 06-05.3a | determinant | 31 | Ω² |
| 06-05.3b | i_1 | 3.065 | A |
| 06-05.3c | i_2 | 1.774 | A |
| 06-05.3d | shared current | 1.290 | A |
| 06-05.3e | power from the 10 V source | 30.65 | W |
| 06-05.3f | power from the 5 V source | 8.871 | W |
| 06-05.3g | total power | 39.52 | W |
| 06-05.4a | i_2 | 2.667 | A |
| 06-05.4b | shared current in mesh 1's direction | −0.667 | A |
| 06-05.4c | current-source voltage | 4 | V |
| 06-05.4d | power from the current source | 8 | W |
| 06-05.4e | power from the 12 V source | 32 | W |
| 06-05.4f | total resistor power | 40 | W |
| 06-05.5a | i_1 | 1 | A |
| 06-05.5b | i_2 | 3 | A |
| 06-05.5c | i_3 | 1 | A |
| 06-05.5d | current-source voltage | 18 | V |
| 06-05.5e | power from the current source | 36 | W |
| 06-05.5f | total resistor power | 56 | W |
| 06-05.6a | determinant | 0.16 | Ω² |
| 06-05.6b | i_1 (battery A) | 10.8 | A |
| 06-05.6c | i_2 (load) | 10.05 | A |
| 06-05.6d | charging current into B | 0.75 | A |
| 06-05.6e | load voltage | 12.06 | V |
| 06-05.6f | load power | 121.2 | W |
| 06-05.6g | power from A | 136.08 | W |
| 06-05.6h | power into B's emf | 9.0 | W |
| 06-05.6i | power in A's internal resistance | 5.832 | W |
| 06-05.6j | power in B's internal resistance | 0.045 | W |
| 06-05.6k | circulating current with no load | 4.6 | A |
| 06-05.7a | unknowns, either method | 2 | — |
| 06-05.7b | i_1 | 4 | mA |
| 06-05.7c | i_2 | 1.5 | mA |
| 06-05.7d | i_3 | −2 | mA |
| 06-05.7e | v_B | 5 | V |
| 06-05.7f | v_C | 3.5 | V |
| 06-05.8a | i^T R i | 70.43 | W |
| 06-05.8b | smallest eigenvalue | 2 | Ω |
| 06-05.8c | middle eigenvalue | 6.092 | Ω |
| 06-05.8d | largest eigenvalue | 16.91 | Ω |
| 06-05.9a | dual v_1 | 1 | V |
| 06-05.9b | dual v_2 | 4 | V |
| 06-05.10a | determinant | 4.72 | kΩ³ |
| 06-05.10b | i_1 | 4.883 | mA |
| 06-05.10c | i_2 | 2.436 | mA |
| 06-05.10d | i_3 | 2.331 | mA |
| 06-05.10e | galvanometer current, A to B | −0.1059 | mA |
| 06-05.11a | determinant | 43 | kΩ³ |
| 06-05.11b | i_1 | 4.884 | mA |
| 06-05.11c | i_2 | 2.326 | mA |
| 06-05.11d | i_3 | 0.9302 | mA |
| 06-05.11e | output voltage | 1.860 | V |
| 06-05.11f | first node voltage | 5.116 | V |
| 06-05.11g | second node voltage | 2.791 | V |
| 06-05.11h | input resistance | 2.048 | kΩ |
| 06-05.12a | independent loops | 4 | — |
| 06-05.12b | loop current | −1.111 | A |
| 06-05.12c | source current | 4.444 | A |
| 06-05.12d | source power | 44.44 | W |
| 06-05.12e | resistance seen by the source | 2.25 | Ω |
| 06-05.12f | resistance of the rest of the network | 1.25 | Ω |
| 06-05.12g | effective resistance across each edge | 0.5556 | Ω |
| 06-05.13a | meshes of the cube | 5 | — |
| 06-05.13b | planar bipartite edge limit for 8 nodes | 12 | — |
| 06-05.13c | resistance between opposite corners | 0.8333 | Ω |
| 06-05.13d | resistance between adjacent corners | 0.5833 | Ω |
| 06-05.13e | resistance across a face diagonal | 0.75 | Ω |
| 06-05.14a | ground offset | 20 | mV |
| 06-05.14b | offset in 12-bit LSB | 16.4 | — |
| 06-05.14c | 16-bit LSB | 76.29 | µV |
| 06-05.14d | offset in 16-bit LSB | 262 | — |
| 06-05.14e | offset with a star ground | 10 | µV |
| 06-05.14f | star-ground offset in 16-bit LSB | 0.131 | — |
