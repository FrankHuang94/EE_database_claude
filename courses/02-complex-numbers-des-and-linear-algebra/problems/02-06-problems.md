# Problems 02-06 · Vectors, Matrices and Linear Systems

Chapter: [02-06](../chapters/02-06-vectors-matrices-and-linear-systems.md) · Worked solutions: [02-06 solutions](../solutions/02-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** vectors are columns, written $(v_1, \dots, v_n)$ in text; angles in degrees; answers to 4 significant figures unless exact. In circuit problems, mS × V = mA, and node voltages are measured from ground. Check every solution by substituting it back into the original equations.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-06.1 [A]

For $\mathbf{a} = (1, -2, 2)$ and $\mathbf{b} = (4, 0, -3)$, find (a) $2\mathbf{a} - \mathbf{b}$; (b) $\mathbf{a}\cdot\mathbf{b}$; (c) $\lVert\mathbf{a}\rVert$ and $\lVert\mathbf{b}\rVert$; (d) the unit vector in the direction of $\mathbf{a}$; (e) the angle between $\mathbf{a}$ and $\mathbf{b}$.

### Problem 02-06.2 [A]

(a) Find $c$ so that $(1, c, 2)$ and $(3, -1, c)$ are orthogonal.
(b) Find the angle between a cube's main diagonal $(1, 1, 1)$ and one of its edges $(1, 0, 0)$.
(c) Find the angle between two main diagonals of the cube, $(1, 1, 1)$ and $(1, 1, -1)$.
(d) Sample $\sin\theta$ and $\cos\theta$ at $N = 8$ equally spaced angles $\theta_k = 2\pi k/8$, $k = 0, \dots, 7$. Show that the two sample vectors are orthogonal.

### Problem 02-06.3 [A]

Let $\mathbf{A} = \begin{bmatrix} 1 & 2 \\ 3 & -1 \\ 0 & 4\end{bmatrix}$.

(a) Compute $\mathbf{A}\mathbf{x}$ for $\mathbf{x} = (2, -1)$ in both the row picture and the column picture.
(b) Find $\mathbf{x}$ with $\mathbf{A}\mathbf{x} = (5, 1, 8)$. There are three equations and only two unknowns; explain why a solution exists anyway.

### Problem 02-06.4 [A]

Let $\mathbf{A} = \begin{bmatrix} 1 & 2 \\ 0 & 1\end{bmatrix}$ and $\mathbf{B} = \begin{bmatrix} 1 & 0 \\ 3 & 1\end{bmatrix}$.

(a) Compute $\mathbf{A}\mathbf{B}$ and $\mathbf{B}\mathbf{A}$.
(b) Verify that $(\mathbf{A}\mathbf{B})^\mathsf{T} = \mathbf{B}^\mathsf{T}\mathbf{A}^\mathsf{T}$, and show that $\mathbf{A}^\mathsf{T}\mathbf{B}^\mathsf{T}$ is different.
(c) Compute $\mathbf{A}^2$ and describe geometrically what $\mathbf{A}$ does to the plane.

### Problem 02-06.5 [B]

**Projection and least squares.**

(a) The best constant approximation to the data vector $\mathbf{b} = (1, 2, 6)$ is its projection onto $\mathbf{a} = (1, 1, 1)$. Find $\hat{x}$, the error vector and $\lVert\mathbf{e}\rVert^2$. Show that in general $\hat{x}$ is the mean, and $\lVert\mathbf{e}\rVert^2/n$ is the population variance.
(b) Project the same $\mathbf{b}$ onto $\mathbf{a} = (1, 2, 2)$. Find $\hat{x}$, $\mathbf{p}$ and $\lVert\mathbf{e}\rVert$, and check that $\mathbf{e}\perp\mathbf{a}$.

### Problem 02-06.6 [B]

Solve by elimination and back substitution, listing the multipliers and the pivots:

$$
\begin{aligned}
x_1 + x_2 + 2x_3 &= 3 \\
3x_1 + 4x_2 + 5x_3 &= 7 \\
2x_1 - 2x_2 + x_3 &= 7
\end{aligned}
$$

### Problem 02-06.7 [B]

**A row exchange.** Solve $\mathbf{A}\mathbf{x} = \mathbf{b}$ with

$$
\mathbf{A} = \begin{bmatrix} 0 & 1 & 2 \\ 1 & 2 & 1 \\ 2 & 7 & 9\end{bmatrix}, \qquad \mathbf{b} = \begin{bmatrix} 1 \\ 0 \\ 4\end{bmatrix} .
$$

(a) Exchange rows 1 and 2 to get a nonzero first pivot, eliminate, and write $\mathbf{P}$, $\mathbf{L}$ and $\mathbf{U}$ with $\mathbf{P}\mathbf{A} = \mathbf{L}\mathbf{U}$.
(b) Repeat with partial pivoting, choosing the largest available entry in each column as pivot. List the pivots and multipliers, and check that every multiplier has magnitude at most 1.

### Problem 02-06.8 [B]

**When elimination breaks down.**

(a) For which $k$ does $x_1 + 2x_2 = 3$, $2x_1 + 4x_2 = k$ have infinitely many solutions? How many does it have otherwise?
(b) For which $a$ does $x_1 + 2x_2 = 3$, $2x_1 + ax_2 = 5$ fail to have exactly one solution? Solve it for $a = 5$.
(c) For which $q$ is $\begin{bmatrix} 1 & 2 & 3 \\ 2 & 5 & 7 \\ 3 & 7 & q\end{bmatrix}$ singular? Find the dependence among its columns in that case.

### Problem 02-06.9 [B]

**Factor once, solve many.** Let $\mathbf{A} = \begin{bmatrix} 4 & 3 \\ 6 & 3\end{bmatrix}$.

(a) Find $\mathbf{L}$ and $\mathbf{U}$.
(b) Use them to solve $\mathbf{A}\mathbf{x} = (10, 12)$ and $\mathbf{A}\mathbf{x} = (1, 0)$.
(c) Find $\mathbf{A}^{-1}$ one column at a time by solving $\mathbf{A}\mathbf{x} = (1, 0)$ and $\mathbf{A}\mathbf{x} = (0, 1)$, and check $\mathbf{A}\mathbf{A}^{-1} = \mathbf{I}$.

### Problem 02-06.10 [B]

**Why L is so tidy.** For the matrix of Example 02-06.3, the multipliers were $\ell_{21} = 2$, $\ell_{31} = -1$ and $\ell_{32} = 2$.

(a) Write $\mathbf{E}_{21}$, $\mathbf{E}_{31}$ and $\mathbf{E}_{32}$.
(b) Compute $\mathbf{E} = \mathbf{E}_{32}\mathbf{E}_{31}\mathbf{E}_{21}$ and show that its $(3, 1)$ entry is $\ell_{32}\ell_{21} - \ell_{31}$.
(c) Compute $\mathbf{L} = \mathbf{E}^{-1} = \mathbf{E}_{21}^{-1}\mathbf{E}_{31}^{-1}\mathbf{E}_{32}^{-1}$ and confirm that it holds the multipliers unchanged.

### Problem 02-06.11 [B]

**Nodal analysis.** A 5 mA current source drives node 1 from ground. $R_1 = 2$ kΩ connects node 1 to ground, $R_2 = 1$ kΩ connects nodes 1 and 2, and $R_3 = 4$ kΩ connects node 2 to ground. A second current source draws 1 mA out of node 2 to ground.

(a) Stamp $\mathbf{G}$ and $\mathbf{i}$, and solve for $v_1$ and $v_2$.
(b) Find the current in $R_2$.
(c) Find the power delivered by the 5 mA source and absorbed by the 1 mA source, and check that the resistors dissipate the difference.

### Problem 02-06.12 [B]

**What a dense solve costs.** A workstation sustains 50 GFLOP/s on dense LU.

(a) How long does factoring a dense $n = 2000$ matrix take?
(b) How long does each subsequent solve (forward plus back substitution) take?
(c) After how many right-hand sides does the total solve time equal the factorization time?
(d) By what factors do (a) and (b) grow if $n$ doubles?
(e) How much memory does the matrix take in double precision?

### Problem 02-06.13 [C]

**The ground node, and modified nodal analysis.** Three resistors form a triangle: $R_{12} = 1$ kΩ between nodes 1 and 2, $R_{23} = 1$ kΩ between 2 and 3, and $R_{13} = 2$ kΩ between 1 and 3. At first, no node is grounded.

(a) Stamp the 3×3 matrix $\mathbf{G}$. Show that its rows sum to zero and that $\mathbf{G}(1, 1, 1) = \mathbf{0}$.
(b) A source pushes 1 mA into node 1 and draws 1 mA out of node 3. Explain why the solutions form a family $\mathbf{v} + c(1, 1, 1)$. Ground node 3, solve for $v_1$ and $v_2$, and find the resistance between nodes 1 and 3. Check it by series and parallel combination.
(c) Add the three KCL equations of (a) together. What must be true of the injected currents for any solution to exist? Interpret physically.
(d) Replace the current source with an ideal 2 V voltage source from node 3 (ground) to node 1. Write the 3×3 modified-nodal-analysis system for $v_1$, $v_2$ and the source current $i_V$ (flowing into node 1), and solve it.

### Problem 02-06.14 [C]

**IR drop on a power rail.** A metal rail is fed from a supply pad at its left end. It runs through five segments of $R = 20$ mΩ each to five taps, numbered 1 to 5 from the pad. Each tap draws $I = 0.2$ A. Work with the drops $d_k = V_{DD} - v_k$, so the pad has $d_0 = 0$.

(a) Write KCL at each tap and show that $\mathbf{G}\mathbf{d} = I(1, 1, 1, 1, 1)$ with a tridiagonal $\mathbf{G}$. Give $\mathbf{G}$.
(b) Without solving the matrix, find the current in each segment, and hence the drop at each tap. Show that the worst drop is $RI\,N(N + 1)/2$ for $N$ taps, and evaluate it.
(c) A second pad is added at the right end, after a sixth segment, also at $V_{DD}$. Find the new worst drop and where it occurs.
(d) By what factor did the second pad reduce the worst drop? Explain why chips spread many supply bumps across the die.

### Problem 02-06.15 [C]

**A wearable's neural-network accelerator.** A hypothetical edge accelerator has 512 8-bit multiply–add units at 1 GHz. It reads weights from external memory at 8 GB/s, or from on-chip SRAM at 256 GB/s. One fully connected layer multiplies a 1024×1024 matrix of 8-bit weights (1 byte each) by an input vector (batch 1). Count each multiply–add as 2 operations.

(a) Find the peak throughput in TOPS, and the layer's operations, weight bytes and arithmetic intensity.
(b) With weights in external memory, find the memory time, the compute time and the fraction of peak the layer achieves.
(c) What arithmetic intensity would the accelerator need to be compute-bound with external memory?
(d) Repeat (b) with the weights held in on-chip SRAM, and comment on why edge accelerators carry large on-chip memories.

---

## Objective coverage

| Learning objective (chapter 02-06) | Problems |
|---|---|
| 1. Vectors, dot products, lengths, angles, projections | 1, 2, 5 |
| 2. Matrix–vector and matrix–matrix products; transposes | 3, 4, 10, 15 |
| 3. Row and column pictures; one, none or infinitely many solutions | 3, 8, 13 |
| 4. Elimination and back substitution; row exchanges; operation counts | 6, 7, 12, 15 |
| 5. LU and PA = LU; many right-hand sides; pivoting | 7, 9, 10, 12 |
| 6. Nodal analysis as G v = i by stamping | 11, 13, 14 |
