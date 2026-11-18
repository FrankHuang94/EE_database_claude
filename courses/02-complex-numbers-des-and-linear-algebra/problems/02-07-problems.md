# Problems 02-07 · Determinants, Inverses, Rank and Vector Spaces

Chapter: [02-07](../chapters/02-07-determinants-inverses-and-vector-spaces.md) · Worked solutions: [02-07 solutions](../solutions/02-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** answers to 4 significant figures unless exact. In circuit problems, mS × V = mA and kΩ × mA = V, and node voltages are measured from ground. Check every inverse by multiplying back, every null-space vector by substituting it, and every least-squares fit by checking that the residuals are orthogonal to the columns.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-07.1 [A]

Find the determinants of

$$
\begin{bmatrix} 4 & -2 \\ 3 & 1\end{bmatrix}, \qquad \begin{bmatrix} 1 & 2 & 0 \\ 3 & -1 & 2 \\ 0 & 4 & 1\end{bmatrix}, \qquad \begin{bmatrix} 2 & 7 & -3 \\ 0 & -1 & 5 \\ 0 & 0 & 4\end{bmatrix} .
$$

Use cofactors for the second, and the shortest valid method for the third.

### Problem 02-07.2 [A]

A 3×3 matrix $\mathbf{A}$ has $\det\mathbf{A} = 4$. Find $\det(3\mathbf{A})$, $\det\mathbf{A}^\mathsf{T}$, $\det\mathbf{A}^{-1}$, $\det\mathbf{A}^2$, the determinant after exchanging two rows of $\mathbf{A}$, and $\det(-\mathbf{A})$.

### Problem 02-07.3 [A]

(a) Invert $\begin{bmatrix} 3 & 5 \\ 1 & 2\end{bmatrix}$ with the 2×2 formula, and check by multiplying.
(b) For which $k$ is $\begin{bmatrix} 2 & k \\ 4 & 6\end{bmatrix}$ not invertible? Describe its columns in that case.

### Problem 02-07.4 [A]

(a) Show that $(1, 2, 3)$, $(4, 5, 6)$ and $(7, 8, 9)$ are linearly dependent, and find the dependence.
(b) Show that $(1, 0, 1)$, $(1, 1, 0)$ and $(0, 1, 1)$ form a basis of $\mathbb{R}^3$.

### Problem 02-07.5 [B]

Find the inverse of

$$
\mathbf{A} = \begin{bmatrix} 1 & 2 & 0 \\ 0 & 1 & 3 \\ 2 & 4 & 1\end{bmatrix}
$$

by Gauss–Jordan elimination. Check that $\mathbf{A}\mathbf{A}^{-1} = \mathbf{I}$, and explain why every entry of $\mathbf{A}^{-1}$ is an integer.

### Problem 02-07.6 [B]

(a) Solve by Cramer's rule:

$$
\begin{aligned}
x_1 + x_2 + x_3 &= 6 \\
2x_1 - x_2 + x_3 &= 3 \\
x_1 + 2x_2 - x_3 &= 2
\end{aligned}
$$

(b) A full cofactor (Leibniz) expansion of a 20×20 determinant has $20!$ terms. How long would evaluating them take at $10^9$ terms per second? Compare with the flops for elimination.

### Problem 02-07.7 [B]

For $\mathbf{A} = \begin{bmatrix} 1 & 3 & 1 & 2 \\ 2 & 6 & 4 & 8 \\ 0 & 0 & 2 & 4\end{bmatrix}$, find the reduced row echelon form, the rank, a basis for the column space, and a basis for the null space. Check the rank–nullity theorem.

### Problem 02-07.8 [B]

For $\mathbf{A} = \begin{bmatrix} 1 & 1 & 2 \\ 2 & 3 & 5 \\ 1 & 2 & 3\end{bmatrix}$:

(a) find the condition on $\mathbf{b}$ for $\mathbf{A}\mathbf{x} = \mathbf{b}$ to have a solution;
(b) find the complete solution for $\mathbf{b} = (4, 9, 5)$;
(c) decide whether $\mathbf{b} = (1, 0, 0)$ is solvable.

### Problem 02-07.9 [B]

**Areas and volumes.**

(a) Find the area of the triangle with vertices $(1, 1)$, $(4, 2)$ and $(2, 5)$.
(b) Find the volume of the parallelepiped with edges $(1, 0, 0)$, $(1, 2, 0)$ and $(1, 1, 3)$.
(c) The map $\mathbf{A} = \begin{bmatrix} 2 & 1 \\ 0 & 3\end{bmatrix}$ is applied to the unit disk. What is the area of the resulting ellipse?

### Problem 02-07.10 [B]

Fit a straight line $b = c + dt$ by least squares to the points $(0, 1)$, $(1, 3)$, $(2, 4)$ and $(3, 4)$. Write the normal equations, solve them, list the residuals, and verify both orthogonality conditions.

### Problem 02-07.11 [B]

**A resistance matrix.** For the circuit of Problem 02-06.11 ($R_1 = 2$ kΩ from node 1 to ground, $R_2 = 1$ kΩ between nodes 1 and 2, $R_3 = 4$ kΩ from node 2 to ground):

(a) find $\mathbf{R} = \mathbf{G}^{-1}$ in kΩ;
(b) use it to recover the node voltages of Problem 02-06.11 (5 mA into node 1, 1 mA drawn from node 2);
(c) check $R_{11}$ and $R_{22}$ by series and parallel combination.

### Problem 02-07.12 [B]

**Two-port parameters.** A π network has a 1 kΩ resistor between port 1 and port 2, a 500 Ω shunt from port 1 to ground and a 1 kΩ shunt from port 2 to ground.

(a) Write its admittance matrix $\mathbf{Y}$ (in mS), which relates the port currents to the port voltages by $\mathbf{i} = \mathbf{Y}\mathbf{v}$.
(b) Invert it to get the impedance matrix $\mathbf{Z} = \mathbf{Y}^{-1}$ in kΩ.
(c) Interpret $Z_{11}$, $Z_{22}$ and $Z_{21}$ physically, and check each by series and parallel combination.

### Problem 02-07.13 [C]

**A bridge as a graph.** Five 1 kΩ resistors connect nodes 1–2, 1–3, 2–3, 2–0 and 3–0, where node 0 is ground.

(a) Write the 5×4 incidence matrix (directions as listed, first node to second), and find its rank and the number of independent loops.
(b) Form $\mathbf{G} = \mathbf{A}_r^\mathsf{T}\mathbf{C}\mathbf{A}_r$, and solve for the node voltages when 1 mA is injected at node 1. What current flows in the 2–3 resistor, and why?
(c) Change the 3–0 resistor to 2 kΩ. Find the new node voltages, the current in the 2–3 resistor (with its direction), and the resistance seen by the source.

### Problem 02-07.14 [C]

**Fitting an exponential.** A capacitor discharging through a resistor gives these readings (illustrative data):

| t (ms) | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| v (V) | 5.00 | 3.05 | 1.85 | 1.12 | 0.68 |

(a) Fit $\ln v = a + bt$ by least squares, and find $V_0 = e^a$ and the time constant $\tau = -1/b$.
(b) A direct nonlinear least-squares fit of $v = V_0e^{-t/\tau}$, minimizing the squared errors in volts, gives $V_0 = 5.003$ V and $\tau = 2.010$ ms. Explain why the two fits differ, and which errors each one treats as most important.

### Problem 02-07.15 [B]

**Low rank.**

(a) Compute the outer product $\mathbf{u}\mathbf{v}^\mathsf{T}$ for $\mathbf{u} = (1, 2, 3)$ and $\mathbf{v} = (4, 5)$, and show that it has rank 1.
(b) Show that if $\mathbf{B}$ is $d\times r$ and $\mathbf{A}$ is $r\times d$, then $\operatorname{rank}(\mathbf{B}\mathbf{A}) \le r$.
(c) A $d\times d$ weight update with $d = 4096$ is replaced by a product $\mathbf{B}\mathbf{A}$ with $r = 8$. Compare the number of parameters, and the memory in 16-bit storage (2 bytes per number).
(d) Compare the multiply–adds needed to apply each form to one vector.

### Problem 02-07.16 [A]

**Is it a subspace?** Decide which of these subsets of $\mathbb{R}^3$ are subspaces. For each one that is, give its dimension; for each one that is not, name the rule it breaks.

(a) The plane $x + 2y - z = 0$. (b) The plane $x + 2y - z = 1$. (c) The line through the origin and $(1, 2, 3)$. (d) All vectors with $x \ge 0$. (e) The union of the $x$-axis and the $y$-axis. (f) All vectors with $x = y = z$.

### Problem 02-07.17 [B]

**Determinant properties from the three rules.** Use only rules 1–3 of §3.1 and the consequences derived there.

(a) Show that if one row is a combination of the other rows, the determinant is zero.
(b) Show that adding a multiple of one column to another leaves the determinant unchanged.
(c) Evaluate $\det\begin{bmatrix}0 & 2 & 1\\ 1 & 1 & 1\\ 2 & 0 & 3\end{bmatrix}$ by elimination, counting row exchanges, and check it by cofactor expansion down column 1.

### Problem 02-07.18 [B]

**Projection matrices.**

(a) For $\mathbf{P} = \mathbf{A}(\mathbf{A}^\mathsf{T}\mathbf{A})^{-1}\mathbf{A}^\mathsf{T}$ (independent columns), show that $\mathbf{P}^\mathsf{T} = \mathbf{P}$ and $\mathbf{P}^2 = \mathbf{P}$, and explain each property geometrically.
(b) For projection onto the line through $\mathbf{a} = (1, 2, 2)$, write $\mathbf{P}$ and find its trace.
(c) Project $\mathbf{b} = (1, 0, 0)$. Show that $\mathbf{I} - \mathbf{P}$ is also a projection, and that $(\mathbf{I} - \mathbf{P})\mathbf{b}$ is perpendicular to $\mathbf{a}$.

### Problem 02-07.19 [B]

**The four subspaces.**

(a) A $5\times7$ matrix has rank 3. Give the dimensions of its column space, null space, row space and left null space, and say which space each lives in.
(b) Three nodes are joined in a triangle by branches 1→2, 2→3 and 3→1. Write the $3\times3$ incidence matrix (rows are branches, columns nodes). Find its rank and a basis for its null space and its left null space, and interpret each physically.

### Problem 02-07.20 [B]

**Gram–Schmidt by hand.** Let $\mathbf{a}_1 = (1, 2, 2)$ and $\mathbf{a}_2 = (1, 0, 1)$.

(a) Apply Gram–Schmidt to find $\mathbf{q}_1$ and $\mathbf{q}_2$, and write $\mathbf{A} = \mathbf{Q}\mathbf{R}$.
(b) Use $\mathbf{R}\hat{\mathbf{x}} = \mathbf{Q}^\mathsf{T}\mathbf{b}$ to find the least-squares solution for $\mathbf{b} = (3, 3, 3)$, and check it with the normal equations.
(c) Find the residual and its length, and check that it is orthogonal to both columns.

---

## Objective coverage

| Learning objective (chapter 02-07) | Problems |
|---|---|
| 1. Determinants: computation, properties, volume, invertibility test | 1, 2, 9, 17 |
| 2. Inverses, Gauss–Jordan, Cramer's rule, cost | 3, 5, 6, 11, 12 |
| 3. Linear independence, basis, dimension | 4, 7, 15, 16, 20 |
| 4. Rank, column and null spaces, complete solution | 7, 8, 13, 15, 16, 19 |
| 5. Least squares and data fitting | 10, 14, 18, 20 |
| 6. Incidence matrices; resistance matrices | 11, 12, 13, 19 |
