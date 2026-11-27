# Solutions 06-04 · Nodal Analysis

Problems: [06-04 problems](../problems/06-04-problems.md) · Chapter: [06-04](../chapters/06-04-nodal-analysis.md). Every number below is recomputed by [verify_06_04.py](../verify/verify_06_04.py); the circuits of Problems 06-04.6, 06-04.7, 06-04.10 and 06-04.13 are also confirmed in ngspice ([lab netlists](../labs/06-04-lab/README.md)).

---

## Solutions

### Solution 06-04.1

(a) One unknown per non-reference node: $6 - 1 = $ **5**.

(b) Two per branch (voltage and current): $2 \times 9 = $ **18**.

(c) MNA adds one unknown per voltage source: $5 + 2 = $ **7**, a 7 × 7 matrix.

(d) The grounded source fixes $v_1$, leaving $v_2$ to $v_5$: **4** unknowns. Nodes 3 and 4 form a supernode, so the four equations are KCL at node 2, KCL at node 5, KCL for the supernode {3, 4}, and the constraint $v_3 - v_4 = V_s$.

### Solution 06-04.2

(a) In mS and mA:

$$
\mathbf{G} = \begin{bmatrix} 1 + 0.5 + 0.4 & -0.5 & -0.4 \\ -0.5 & 0.5 + 0.25 & -0.25 \\ -0.4 & -0.25 & 0.25 + 0.2 + 0.4 \end{bmatrix}
= \begin{bmatrix} 1.9 & -0.5 & -0.4 \\ -0.5 & 0.75 & -0.25 \\ -0.4 & -0.25 & 0.85 \end{bmatrix},
\qquad
\mathbf{i} = \begin{bmatrix} 3 \\ 0 \\ -1 \end{bmatrix}.
$$

The 1 mA source draws current *out of* node 3, so it enters $\mathbf{i}$ as −1.

(b) $G_{12} = G_{21} = -0.5$, $G_{13} = G_{31} = -0.4$, $G_{23} = G_{32} = -0.25$: symmetric. Row 1: $1.9 > 0.5 + 0.4 = 0.9$, strictly dominant by the 1 mS of $R_a$ to ground. Row 2: $0.75 = 0.5 + 0.25$, equality, because node 2 has no resistor to ground. Row 3: $0.85 > 0.25 + 0.4 = 0.65$, strict by the 0.2 mS of $R_d$.

(c) Eliminate $v_2$ with row 2: $v_2 = (0.5v_1 + 0.25v_3)/0.75 = (2v_1 + v_3)/3$. Substituting into rows 1 and 3 and multiplying by 30:

$$
47v_1 - 17v_3 = 90, \qquad -17v_1 + 23v_3 = -30 .
$$

The determinant is $47\times23 - 17^2 = 792$, so \$v_1 = (90\times23 - 17\times30)/792 = 1560/792 = \$ **1.970 V**, \$v_3 = (47\times(-30) + 17\times90)/792 = 120/792 = \$ **0.1515 V**, and \$v_2 = (2\times1.9697 + 0.1515)/3 = \$ **1.364 V**. (Exactly 65/33, 45/33 and 5/33 V.)

Resistor currents (mA): $R_a$, \$1.970/1 = \$ **1.970** to ground; $R_b$, \$(1.970 - 1.364)/2 = \$ **0.3030** from 1 to 2; $R_c$, \$(1.364 - 0.1515)/4 = \$ **0.3030** from 2 to 3; $R_d$, \$0.1515/5 = \$ **0.0303** to ground; $R_e$, \$(1.970 - 0.1515)/2.5 = \$ **0.7273** from 1 to 3. KCL at node 1: $1.970 + 0.303 + 0.727 = 3.000$ ✓.

(d) The 3 mA source delivers \$3\times1.9697 = \$ **5.909 mW**. The 1 mA sink carries current from node 3 (at +0.1515 V) to ground, so it *absorbs* $0.1515$ mW. Net delivered: \$5.909 - 0.152 = \$ **5.758 mW**. Resistors: $3.880 + 0.184 + 0.367 + 0.005 + 1.322 = 5.758$ mW ✓.

### Solution 06-04.3

(a) $\mathbf{G} = \begin{bmatrix} 1/3 + 1/6 & -1/6 \\ -1/6 & 1/6 + 1/3\end{bmatrix} = \begin{bmatrix} 0.5 & -0.1667 \\ -0.1667 & 0.5\end{bmatrix}$ mS, $\mathbf{i} = (2, -1)$ mA. \$\Delta = 0.25 - 1/36 = \$ **0.2222 mS²**.

$$
v_1 = \frac{2\times0.5 - (-\tfrac16)(-1)}{0.2222} = \frac{0.8333}{0.2222} = \mathbf{3.75\ V}, \qquad
v_2 = \frac{0.5\times(-1) - 2\times(-\tfrac16)}{0.2222} = \frac{-0.1667}{0.2222} = \mathbf{-0.75\ V}.
$$

(b) Node 2 sits 0.75 V *below* the reference. The sink pulls 1 mA out of node 2, but only $(3.75 + 0.75)/6 = 0.75$ mA arrives through $R_2$; the other 0.25 mA must flow up from ground through $R_3$, which requires node 2 to be below ground. A negative node voltage is a normal answer, not an error.

(c) The 2 mA source delivers \$2\times3.75 = \$ **7.5 mW**. The sink pushes −1 mA into a node at −0.75 V: it delivers \$(-1)(-0.75) = \$ **0.75 mW** (current passes through it from −0.75 V up to 0 V, so it supplies energy). Resistors: \$3.75^2/3 + 4.5^2/6 + 0.75^2/3 = 4.6875 + 3.375 + 0.1875 = \$ **8.25 mW** $= 7.5 + 0.75$ ✓.

### Solution 06-04.4

(a) **2** unknowns, $v_B$ and $v_C$; $v_A = 9$ V is fixed by the source. KCL at A would only involve the source's unknown current, so it is not needed to find the node voltages (it gives that current afterwards).

(b) In kΩ, mA and V. Node B: $(v_B - 9)/1 + v_B/2 + (v_B - v_C)/1 = 0$, so $2.5v_B - v_C = 9$. Node C: $(v_C - v_B)/1 + v_C/1 = 2$, so $-v_B + 2v_C = 2$. From the second, $v_C = (2 + v_B)/2$; substituting, $2v_B - 1 = 9$: \$v_B = \$ **5 V** and \$v_C = \$ **3.5 V**.

(c) The source current is the current leaving node A through $R_{AB}$: \$(9 - 5)/1 = \$ **4 mA**, and it delivers \$9\times4 = \$ **36 mW**. The current source delivers $2\times3.5 = 7$ mW. Resistors: \$4^2\times1 + 5^2/2 + 1.5^2\times1 + 3.5^2/1 = 16 + 12.5 + 2.25 + 12.25 = \$ **43 mW** $= 36 + 7$ ✓.

### Solution 06-04.5

(a) Supernode {1, 2}, currents leaving through its boundary equal the 3 A entering:

$$
\frac{v_1}{4} + \frac{v_2}{6} = 3, \qquad v_2 - v_1 = 10 .
$$

Substituting and multiplying by 12: $3v_1 + 2(v_1 + 10) = 36$, so \$v_1 = \$ **3.2 V** and \$v_2 = \$ **13.2 V**.

(b) KCL at node 2 alone: 2.2 A leaves through the 6 Ω, and the only other branch is the source, so the source delivers **2.2 A** out of its + terminal and \$10\times2.2 = \$ **22 W**. (Node 1 check: 3 A in = 0.8 A through 4 Ω + 2.2 A into the source's − terminal ✓.) The current source delivers \$3\times3.2 = \$ **9.6 W**. Resistors: $3.2^2/4 + 13.2^2/6 = 2.56 + 29.04 = 31.6$ W $= 22 + 9.6$ ✓.

(c) The source column has +1 at node 2 (its + terminal) and −1 at node 1:

$$
\begin{bmatrix} 0.25 & 0 & -1 \\ 0 & 0.1667 & 1 \\ -1 & 1 & 0 \end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \\ j \end{bmatrix} =
\begin{bmatrix} 3 \\ 0 \\ 10 \end{bmatrix}.
$$

Row 2 gives $j = -v_2/6 = $ **−2.2 A**: the current into the + terminal is negative, so 2.2 A comes *out* of it and the source delivers power, as found in (b).

### Solution 06-04.6

(a) In kΩ, mA and V. Node A: $(v_A - 5)/1 + v_A/1 + (v_A - v_B)/0.1 = 0$, so $12v_A - 10v_B = 5$. Node B: $(v_B - 5)/1 + v_B/1.1 + (v_B - v_A)/0.1 = 0$, so $-10v_A + 11.909v_B = 5$. $\Delta = 12\times11.909 - 100 = 42.909$:

$$
v_A = \frac{5\times11.909 + 10\times5}{42.909} = \mathbf{2.5530\ V}, \qquad
v_B = \frac{12\times5 + 10\times5}{42.909} = \mathbf{2.5636\ V}.
$$

(b) $(v_B - v_A)/0.1\ \text{kΩ} = 0.010593/0.1 = $ **0.1059 mA** (105.9 µA), flowing from B to A through the galvanometer.

(c) With the galvanometer removed, $v_A = 2.5$ V and $v_B = 5\times1.1/2.1 = 2.6190$ V, so \$v_{BA} = \$ **119.0 mV**. Dividing by 100 Ω would give 1.19 mA, but the bridge's own resistances are in series with the meter: seen from A and B, with the source replaced by a short, the bridge is \$1\parallel1 + 1\parallel1.1 = \$ **1.024 kΩ**. Then $119.05\ \text{mV}/(1.024 + 0.1)\ \text{kΩ} = 0.1059$ mA ✓. This "open-circuit voltage over total resistance" shortcut is Thévenin's theorem ([06-08](../chapters/06-08-thevenin-and-norton.md)).

(d) $(5 - 2.5530)/1 + (5 - 2.5636)/1 = 2.4470 + 2.4364 = $ **4.883 mA**.

### Solution 06-04.7

Unknowns $(v_1, v_2, j)$. R1 (0.5 S between 1 and 2) adds ±0.5; R2 (0.125 S, node 2 to ground) adds 0.125 at (2,2); I1 adds +1 to row 2 of the right side; V1 adds +1 at (1,3) and (3,1) and 10 to row 3:

$$
\begin{bmatrix} 0.5 & -0.5 & 1 \\ -0.5 & 0.625 & 0 \\ 1 & 0 & 0 \end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \\ j \end{bmatrix} =
\begin{bmatrix} 0 \\ 1 \\ 10 \end{bmatrix}.
$$

Row 3: $v_1 = 10$ V. Row 2: $-5 + 0.625v_2 = 1$, so \$v_2 = \$ **9.6 V**. Row 1: $5 - 4.8 + j = 0$, so \$j = \$ **−0.2 A**: 0.2 A flows out of V1's + terminal, and V1 delivers \$10\times0.2 = \$ **2 W**.

KCL at node 2: 0.2 A in through R1 plus 1 A from I1 equals $9.6/8 = 1.2$ A out through R2 ✓. Power: I1 delivers $1\times9.6 = 9.6$ W; R1 absorbs $0.2^2\times2 = 0.08$ W and R2 $9.6^2/8 = 11.52$ W; \$0.08 + 11.52 = \$ **11.6 W** $= 2 + 9.6$ ✓.

### Solution 06-04.8

(a) In mS and mA: $\mathbf{G} = \begin{bmatrix} 1 & -1 \\ -1 & 1\end{bmatrix}$, $\mathbf{i} = (1, -1)$. \$\det\mathbf{G} = 1 - 1 = \$ **0**: singular. Its rows sum to zero, so $\mathbf{G}(1, 1)^\mathsf{T} = \mathbf{0}$.

(b) The difference is determined: 1 mA through 1 kΩ gives $v_1 - v_2 = $ **1 V**. The common level is not: adding the same constant to both node voltages changes no current, because the pair has no connection to ground. The equations have infinitely many solutions, and a simulator reports a singular matrix.

(c) $\mathbf{G} = \begin{bmatrix} 1 & -1 \\ -1 & 1 + 10^{-6}\end{bmatrix}$ mS, determinant $10^{-6}$ mS². Adding the two rows gives $10^{-6}v_2 = 1 - 1 = 0$, so \$v_2 = \$ **0 V** and \$v_1 = \$ **1 V**. The source's current circulates inside the pair, so no net current crosses a surface enclosing both nodes; the only branch crossing it, the 1 GΩ resistor, therefore carries zero current and has zero voltage, whatever its value.

### Solution 06-04.9

(a) Write each resistor's contribution with its incidence vector $\mathbf{a}_r$, which has +1 in row $a$, −1 in row $b$, and no entry for ground. The outer product $G_r\mathbf{a}_r\mathbf{a}_r^\mathsf{T}$ has $+G_r$ at $(a,a)$ and $(b,b)$ and $-G_r$ at $(a,b)$ and $(b,a)$, which is exactly the resistor's stamp (a resistor to ground contributes only $+G_r$ at $(a,a)$). So $\mathbf{G} = \sum_r G_r\mathbf{a}_r\mathbf{a}_r^\mathsf{T}$, and

$$
\mathbf{v}^\mathsf{T}\mathbf{G}\mathbf{v} = \sum_r G_r(\mathbf{a}_r^\mathsf{T}\mathbf{v})^2 = \sum_r G_r(v_a - v_b)^2 .
$$

(b) Every term is non-negative, so $\mathbf{v}^\mathsf{T}\mathbf{G}\mathbf{v} \ge 0$. If it equals zero, every resistor has equal voltages at its ends. Walk along a resistive path from any node to ground: each step keeps the voltage equal, so every node voltage equals ground's, zero. Hence $\mathbf{v}^\mathsf{T}\mathbf{G}\mathbf{v} > 0$ for every $\mathbf{v} \ne \mathbf{0}$: $\mathbf{G}$ is positive definite. If $\mathbf{G}\mathbf{v} = \mathbf{0}$ then $\mathbf{v}^\mathsf{T}\mathbf{G}\mathbf{v} = 0$, so $\mathbf{v} = \mathbf{0}$: the only null vector is zero, and $\mathbf{G}$ is nonsingular.

(c) Resistor by resistor (mS × V² = mW): $R_a$, $1\times1^2 = 1$; $R_b$, $0.5\times2^2 = 2$; $R_c$, $0.25\times3^2 = 2.25$; $R_d$, $0.2\times2^2 = 0.8$; $R_e$, $0.4\times1^2 = 0.4$; total **6.45 mW**. Matrix: $1.9 + 0.75 + 0.85\times4 + 2[(-0.5)(1)(-1) + (-0.4)(1)(2) + (-0.25)(-1)(2)] = 6.05 + 2(0.2) = 6.45$ mW ✓.

(d) `numpy.linalg.eigvalsh(G)` gives eigenvalues 0.2904, 1.055 and 2.155 mS; the smallest is **0.2904 mS** > 0, as (b) requires. Problem 06-04.8's matrix has smallest eigenvalue **0** (eigenvector (1, 1)), the signature of a floating subcircuit.

### Solution 06-04.10

The edge conductance is $g = 1/0.020 = 50$ S.

(a) By symmetry the four edge-center nodes share one voltage $v_E$ and the four corners share $v_C$. Corner: its two neighbors are edge centers, and it draws 1 A: $2g(v_C - v_E) = -1$, so $v_E - v_C = 1/100 = 0.01$ V. Edge center: neighbors are the bump (0.75 V) and two corners: $g(v_E - 0.75) + 2g(v_E - v_C) = -1$, so $50(v_E - 0.75) + 1 = -1$ and \$v_E = \$ **0.71 V**; then \$v_C = \$ **0.70 V**. The worst nodes are the corners, with a drop of **50 mV**. Each edge center receives $g\times0.04 = 2$ A from the bump, so the bump supplies $4\times2 = 8$ A through the grid plus the center's own 1 A.

(b) Solving the eight unknowns numerically (bump at the top-left corner):

$$
\begin{bmatrix} 0.75 & 0.67 & 0.6375 \\ 0.67 & 0.6425 & 0.625 \\ 0.6375 & 0.625 & 0.615 \end{bmatrix}\ \text{V}.
$$

The worst node is the **opposite corner**, at 0.615 V: a drop of **135 mV**.

(c) Now the center $v_X$ and the four edge centers $v_E$ are unknown. Center: $4g(v_X - v_E) = -1$, so $v_E - v_X = 0.005$ V. Edge center (two bump neighbors and the center): $2g(v_E - 0.75) + g(v_E - v_X) = -1$, so $100(v_E - 0.75) + 0.25 = -1$ and $v_E = 0.7375$ V, $v_X = 0.7325$ V. Worst drop **17.5 mV**, at the center.

(d) Four corner bumps (17.5 mV) beat one center bump (50 mV), which beats one corner bump (135 mV). Drop grows with the distance current must travel and with how much current shares each path; many distributed supply connections, rather than one well-placed one, are what keep a large grid flat, which is why chips use thousands of bumps.

### Solution 06-04.11

(a) In S: $\mathbf{G} = \begin{bmatrix} 1.5 & -1 & 0 \\ -1 & 2.5 & -1 \\ 0 & -1 & 1.5\end{bmatrix}$ (each node: 0.5 S to ground plus 1 S to each neighbor), $\mathbf{i} = (1, 0, 0)$ A. Expanding along the first row: \$\Delta = 1.5(2.5\times1.5 - 1) - (-1)(-1\times1.5 - 0) = 4.125 - 1.5 = \$ **2.625 S³**.

(b) Replace column $k$ by $\mathbf{i}$:

$$
v_1 = \frac{1\times(2.5\times1.5 - 1)}{2.625} = \frac{2.75}{2.625} = \mathbf{1.048\ V}, \quad
v_2 = \frac{\det\begin{bmatrix} 1.5 & 1 & 0 \\ -1 & 0 & -1 \\ 0 & 0 & 1.5\end{bmatrix}}{2.625} = \frac{1.5}{2.625} = \mathbf{0.5714\ V}, \quad
v_3 = \frac{\det\begin{bmatrix} 1.5 & -1 & 1 \\ -1 & 2.5 & 0 \\ 0 & -1 & 0\end{bmatrix}}{2.625} = \frac{1}{2.625} = \mathbf{0.3810\ V}.
$$

(The second determinant expands along its last row: $1.5\times(1.5\times0 - 1\times(-1)) = 1.5$; the third along its last column: $1\times((-1)(-1) - 2.5\times0) = 1$.) Exactly 22/21, 4/7 and 8/21 V.

(c) Input resistance $v_1/(1\ \text{A}) = $ **1.048 Ω**; $v_3/v_1 = $ **0.3636** (exactly 4/11).

(d) Node 3: current arriving from node 2, $(0.5714 - 0.3810)/1 = 0.1905$ A, equals the current to ground, $0.3810/2 = 0.1905$ A ✓.

### Solution 06-04.12

(a) Each of the $N^2$ nodes has a diagonal entry. A grid has $N(N - 1)$ horizontal and $N(N - 1)$ vertical edges, $2N(N - 1)$ in all, and each edge creates two symmetric off-diagonal entries. Total: $N^2 + 4N(N - 1)$.

(b) $N$ = 100: **10,000** unknowns; \$10^4 + 4\times100\times99 = \$ **49,600** nonzeros, out of $10^8$ entries: **0.0496%**.

(c) Dense: $10^8\times8 = 8\times10^8$ bytes, **800 MB**. Sparse: $49{,}600\times12 + 10{,}001\times4 = 595{,}200 + 40{,}004 = 635{,}204$ bytes, **0.635 MB**, about **1259** times less.

(d) Dense LU: \$(10^4)^3/3 = \$ **3.33 × 10^11** operations, for a matrix that sparse methods factor almost instantly. For $N$ = 1000 ($10^6$ unknowns) the dense matrix alone needs $8\times10^{12}$ bytes, **8 TB**, while its about $5\times10^6$ nonzeros fit in tens of megabytes. Power grids are therefore solved only with sparse direct solvers or with iterative methods (such as conjugate gradients, which suit symmetric positive definite matrices like this one), never with dense ones.

### Solution 06-04.13

(a) Linearize at $v^{(k)}$: $i_D \approx f(v^{(k)}) + g\,(v - v^{(k)}) = g\,v + I_{eq}$ with $g = f'(v^{(k)}) = (I_S/V_T)\,e^{v^{(k)}/V_T}$ and $I_{eq} = f(v^{(k)}) - g\,v^{(k)}$. KCL at node 1 with the companion model:

$$
\frac{v - 5}{1000} + g\,v + I_{eq} = 0 \;\Rightarrow\; v^{(k+1)} = \frac{5/1000 - I_{eq}}{1/1000 + g}.
$$

(b) At 0.7 V: $0.7/0.025852 = 27.077$, $f = 10^{-14}e^{27.077} = 5.748$ mA, \$g = 5.748\ \text{mA}/25.852\ \text{mV} = \$ **0.2223 S**, \$I_{eq} = 0.005748 - 0.2223\times0.7 = \$ **−0.1499 A**. Then \$v^{(1)} = (0.005 + 0.1499)/(0.001 + 0.2223) = \$ **0.6935 V**. Repeating at 0.6935 V ($g$ = 0.1730 S, $I_{eq}$ = −0.1155 A) gives \$v^{(2)} = \$ **0.6926 V**.

(c) The next iterates agree to better than 1 µV: $v_D = $ **0.6925 V** (0.692544 V) and $i_D = (5 - 0.6925)/1000 = $ **4.307 mA**. The lab's ngspice run gives the same operating point.

(d) The simulator's core is a linear solver for the stamped MNA matrix. The companion model turns each Newton step into a linear circuit with the same sparsity pattern, so the same assembly code and the same sparse ordering are reused at every iteration; only the numbers in the diode's stamp change.

### Solution 06-04.14

(a) The Norton equivalent is a 5 A source ($10\ \text{V}/2\ \Omega$) into node 1 with 2 Ω from node 1 to ground. In S and A:

$$
\begin{bmatrix} \tfrac12 + \tfrac13 + 1 & -1 \\ -1 & 1 + \tfrac16 \end{bmatrix}
\begin{bmatrix} v_1 \\ v_2 \end{bmatrix} =
\begin{bmatrix} 5 \\ -2 \end{bmatrix}, \qquad \Delta = 1.8333\times1.1667 - 1 = 1.1389\ \text{S}^2 .
$$

(b) $v_1 = (5\times1.1667 - (-1)(-2))/1.1389 = 3.8333/1.1389 = $ **3.366 V**; $v_2 = (1.8333\times(-2) - 5\times(-1))/1.1389 = 1.3333/1.1389 = $ **1.171 V** (exactly 138/41 and 48/41 V).

(c) The actual source current flows through its 2 Ω: $(10 - 3.366)/2 = $ **3.317 A**, not 5 A. The Norton source's 5 A splits between its own 2 Ω shunt (1.683 A) and the external circuit (3.317 A).

(d) The 10 V source delivers \$10\times3.317 = \$ **33.17 W**, of which its series 2 Ω dissipates \$3.317^2\times2 = \$ **22.01 W**. The Norton source delivers \$5\times3.366 = \$ **16.83 W**, of which its shunt 2 Ω dissipates \$3.366^2/2 = \$ **5.664 W**. Both pass the same \$33.17 - 22.01 = 16.83 - 5.66 = \$ **11.16 W** to the external circuit (3 Ω: 3.776 W, 1 Ω: 4.819 W, 6 Ω: 0.228 W, and the sink absorbs $2\times1.171 = 2.341$ W). Equivalent sources agree at their terminals only; what happens inside them is not equivalent ([06-08](../chapters/06-08-thevenin-and-norton.md)).

### Solution 06-04.15

(a) In kΩ, mA and V:

$$
\text{node 1: } 2 = \frac{v_1}{2} + \frac{v_1 - v_2}{4}, \qquad \text{node 2: } 2 = \frac{v_2}{4} + \frac{v_2 - v_1}{4}.
$$

The branch made of the current source and the 5 kΩ resistor delivers exactly 2 mA into node 1 whatever the resistor's value: a current source fixes its branch current, so anything in series with it changes only the voltage across the source, not the current. The resistor therefore never appears in a KCL equation.

(b) Node 2 gives $v_1 = 2v_2 - 8$; substituting into node 1, $0.75(2v_2 - 8) - 0.25v_2 = 2$, so $1.25v_2 = 8$: **$v_2$ = 6.4 V** and **$v_1$ = 4.8 V**.

(c) The source's output terminal sits $2\ \text{mA}\times5\ \text{kΩ} = 10$ V above node 1: **14.8 V**. The source delivers \$14.8\times2 = \$ **29.6 mW**, of which the 5 kΩ resistor dissipates \$2^2\times5 = \$ **20 mW**: the series resistor wastes power without changing any node voltage.

### Solution 06-04.16

(a) In kΩ, mA and V, with the supernode around nodes 1 and 2:

$$
\begin{bmatrix} 1 & -1 & 0 & 0\\ \tfrac12 & \tfrac14 + 1 & -1 & 0\\ 0 & -1 & 1 + \tfrac12 + \tfrac12 & -\tfrac12\\ 0 & 0 & -\tfrac12 & \tfrac12 + 1 \end{bmatrix}
\begin{bmatrix} v_1\\ v_2\\ v_3\\ v_4 \end{bmatrix} =
\begin{bmatrix} 4\\ 2\\ 0\\ 1 \end{bmatrix}.
$$

Row 1 is the constraint $v_1 - v_2 = 4$; row 2 is the supernode's KCL (2 mA in, leaving through 2 kΩ, 4 kΩ and 1 kΩ); rows 3 and 4 are KCL at nodes 3 and 4.

(b) Substitute $v_1 = v_2 + 4$ into row 2: $1.75v_2 - v_3 = 0$, so $v_3 = 1.75v_2$. Row 4 gives $v_4 = (1 + 0.5v_3)/1.5$. Row 3 becomes $-v_2 + 2(1.75v_2) - 0.5v_4 = 0$, that is $2.5v_2 = 0.5v_4 = (1 + 0.875v_2)/3$, so $v_2(7.5 - 0.875) = 1$: **$v_2$ = 0.1509 V**, **$v_1$ = 4.151 V**, **$v_3$ = 0.2642 V**, **$v_4$ = 0.7547 V**.

(c) KCL at node 1: 2 mA arrives from the source, and $v_1/2 = 2.075$ mA leaves through the 2 kΩ, so **0.07547 mA** flows from node 2 up through the 4 V source and out of its + terminal into node 1. The source delivers \$4\times0.07547 = \$ **0.3019 mW**.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 06-04.1a | basic nodal unknowns | 5 | — |
| 06-04.1b | branch-method unknowns | 18 | — |
| 06-04.1c | MNA size | 7 | — |
| 06-04.1d | equations by hand | 4 | — |
| 06-04.2a | v_1 | 1.970 | V |
| 06-04.2b | v_2 | 1.364 | V |
| 06-04.2c | v_3 | 0.1515 | V |
| 06-04.2d | current in R_a | 1.970 | mA |
| 06-04.2e | current in R_b | 0.3030 | mA |
| 06-04.2f | current in R_c | 0.3030 | mA |
| 06-04.2g | current in R_d | 0.0303 | mA |
| 06-04.2h | current in R_e | 0.7273 | mA |
| 06-04.2i | power delivered by the 3 mA source | 5.909 | mW |
| 06-04.2j | net power delivered | 5.758 | mW |
| 06-04.2k | power absorbed by the 1 mA sink | 0.1515 | mW |
| 06-04.2l | reduced-system determinant (scaled by 900) | 792 | — |
| 06-04.3a | determinant | 0.2222 | mS² |
| 06-04.3b | v_1 | 3.75 | V |
| 06-04.3c | v_2 | −0.75 | V |
| 06-04.3d | power delivered by the 2 mA source | 7.5 | mW |
| 06-04.3e | power delivered by the sink | 0.75 | mW |
| 06-04.3f | total resistor power | 8.25 | mW |
| 06-04.3g | current in R_2 | 0.75 | mA |
| 06-04.3h | current up from ground in R_3 | 0.25 | mA |
| 06-04.4a | unknowns | 2 | — |
| 06-04.4b | v_B | 5 | V |
| 06-04.4c | v_C | 3.5 | V |
| 06-04.4d | 9 V source current | 4 | mA |
| 06-04.4e | 9 V source power | 36 | mW |
| 06-04.4f | total resistor power | 43 | mW |
| 06-04.4g | power delivered by the 2 mA source | 7 | mW |
| 06-04.5a | v_1 | 3.2 | V |
| 06-04.5b | v_2 | 13.2 | V |
| 06-04.5c | current delivered by the 10 V source | 2.2 | A |
| 06-04.5d | power delivered by the 10 V source | 22 | W |
| 06-04.5e | power delivered by the 3 A source | 9.6 | W |
| 06-04.5f | MNA current j | −2.2 | A |
| 06-04.5g | total resistor power | 31.6 | W |
| 06-04.6a | v_A | 2.5530 | V |
| 06-04.6b | v_B | 2.5636 | V |
| 06-04.6c | galvanometer current | 0.1059 | mA |
| 06-04.6d | open-circuit voltage v_BA | 119.0 | mV |
| 06-04.6e | bridge resistance seen by the meter | 1.024 | kΩ |
| 06-04.6f | source current | 4.883 | mA |
| 06-04.6g | open-circuit voltage over 100 Ω alone | 1.19 | mA |
| 06-04.6h | determinant | 42.909 | mS² |
| 06-04.7a | v_2 | 9.6 | V |
| 06-04.7b | j | −0.2 | A |
| 06-04.7c | power delivered by V1 | 2 | W |
| 06-04.7d | total resistor power | 11.6 | W |
| 06-04.7e | power delivered by I1 | 9.6 | W |
| 06-04.7f | current in R2 | 1.2 | A |
| 06-04.8a | determinant | 0 | mS² |
| 06-04.8b | v_1 − v_2 | 1 | V |
| 06-04.8c | v_2 with 1 GΩ to ground | 0 | V |
| 06-04.8d | v_1 with 1 GΩ to ground | 1 | V |
| 06-04.9a | v^T G v | 6.45 | mW |
| 06-04.9b | smallest eigenvalue | 0.2904 | mS |
| 06-04.9c | smallest eigenvalue, Problem 06-04.8 | 0 | mS |
| 06-04.9d | middle eigenvalue | 1.055 | mS |
| 06-04.9e | largest eigenvalue | 2.155 | mS |
| 06-04.10a | v_E, center bump | 0.71 | V |
| 06-04.10b | v_C, center bump | 0.70 | V |
| 06-04.10c | worst drop, center bump | 50 | mV |
| 06-04.10d | worst drop, corner bump | 135 | mV |
| 06-04.10e | worst drop, four corner bumps | 17.5 | mV |
| 06-04.10f | bump current through the grid, center bump | 8 | A |
| 06-04.10g | opposite-corner voltage, corner bump | 0.615 | V |
| 06-04.10h | center voltage, four corner bumps | 0.7325 | V |
| 06-04.10i | edge-center voltage, four corner bumps | 0.7375 | V |
| 06-04.11a | determinant | 2.625 | S³ |
| 06-04.11b | v_1 | 1.048 | V |
| 06-04.11c | v_2 | 0.5714 | V |
| 06-04.11d | v_3 | 0.3810 | V |
| 06-04.11e | input resistance | 1.048 | Ω |
| 06-04.11f | v_3/v_1 | 0.3636 | — |
| 06-04.12a | unknowns, N = 100 | 10000 | — |
| 06-04.12b | nonzeros, N = 100 | 49600 | — |
| 06-04.12c | nonzero fraction | 0.0496 | % |
| 06-04.12d | dense storage, N = 100 | 800 | MB |
| 06-04.12e | sparse storage, N = 100 | 0.635 | MB |
| 06-04.12f | storage ratio | 1259 | — |
| 06-04.12g | dense LU operations, N = 100 | 3.33×10^11 | — |
| 06-04.12h | dense storage, N = 1000 | 8 | TB |
| 06-04.13a | companion conductance at 0.7 V | 0.2223 | S |
| 06-04.13b | companion current at 0.7 V | −0.1499 | A |
| 06-04.13c | first iterate | 0.6935 | V |
| 06-04.13d | second iterate | 0.6926 | V |
| 06-04.13e | converged diode voltage | 0.6925 | V |
| 06-04.13f | diode current | 4.307 | mA |
| 06-04.13g | diode current at 0.7 V | 5.748 | mA |
| 06-04.13h | companion conductance at the first iterate | 0.1730 | S |
| 06-04.13i | companion current at the first iterate | −0.1155 | A |
| 06-04.13j | exponent at 0.7 V | 27.077 | — |
| 06-04.14a | determinant | 1.1389 | S² |
| 06-04.14b | v_1 | 3.366 | V |
| 06-04.14c | v_2 | 1.171 | V |
| 06-04.14d | actual source current | 3.317 | A |
| 06-04.14e | power delivered by the 10 V source | 33.17 | W |
| 06-04.14f | power delivered by the Norton source | 16.83 | W |
| 06-04.14g | power in the series 2 Ω | 22.01 | W |
| 06-04.14h | power in the shunt 2 Ω | 5.664 | W |
| 06-04.14i | power to the external circuit | 11.16 | W |
| 06-04.14j | current in the Norton shunt | 1.683 | A |
| 06-04.14k | power in the 3 Ω | 3.776 | W |
| 06-04.14l | power in the 1 Ω | 4.819 | W |
| 06-04.14m | power in the 6 Ω | 0.228 | W |
| 06-04.14n | power absorbed by the sink | 2.341 | W |
| 06-04.15a | v_1 | 4.8 | V |
| 06-04.15b | v_2 | 6.4 | V |
| 06-04.15c | current-source terminal voltage | 14.8 | V |
| 06-04.15d | power delivered by the current source | 29.6 | mW |
| 06-04.15e | power in the 5 kΩ | 20 | mW |
| 06-04.16a | v_1 | 4.151 | V |
| 06-04.16b | v_2 | 0.1509 | V |
| 06-04.16c | v_3 | 0.2642 | V |
| 06-04.16d | v_4 | 0.7547 | V |
| 06-04.16e | current out of the 4 V source's + terminal | 0.07547 | mA |
| 06-04.16f | power delivered by the 4 V source | 0.3019 | mW |
