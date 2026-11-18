# Solutions 02-07 · Determinants, Inverses, Rank and Vector Spaces

Problems: [02-07 problems](../problems/02-07-problems.md) · Chapter: [02-07](../chapters/02-07-determinants-inverses-and-vector-spaces.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_02_07.py](../verify/verify_02_07.py). The circuits of Problems 11–13 are also simulated in ngspice in the [lab](../labs/02-07-lab/README.md).

---

## Solutions

### Solution 02-07.1

$\det\begin{bmatrix} 4 & -2 \\ 3 & 1\end{bmatrix} = 4\cdot1 - (-2)\cdot3 = $ **10**.

Second matrix, cofactors along row 1:

$$
1\begin{vmatrix} -1 & 2 \\ 4 & 1\end{vmatrix} - 2\begin{vmatrix} 3 & 2 \\ 0 & 1\end{vmatrix} + 0 = 1(-1 - 8) - 2(3 - 0) = \mathbf{-15} .
$$

The third is upper triangular, so its determinant is the product of the diagonal: $2\cdot(-1)\cdot4 = $ **−8**.

### Solution 02-07.2

- $\det(3\mathbf{A}) = 3^3\cdot4 = $ **108**: each of the three rows is tripled.
- $\det\mathbf{A}^\mathsf{T} = $ **4**.
- $\det\mathbf{A}^{-1} = 1/4 = $ **0.25**.
- $\det\mathbf{A}^2 = 4^2 = $ **16**, by the product rule.
- A row exchange reverses the sign: **−4**.
- $\det(-\mathbf{A}) = (-1)^3\cdot4 = $ **−4**.

### Solution 02-07.3

(a) $\det = 3\cdot2 - 5\cdot1 = $ **1**, so

$$
\begin{bmatrix} 3 & 5 \\ 1 & 2\end{bmatrix}^{-1} = \frac11\begin{bmatrix} 2 & \mathbf{-5} \\ \mathbf{-1} & 3\end{bmatrix} .
$$

Check: $\begin{bmatrix} 3 & 5 \\ 1 & 2\end{bmatrix}\begin{bmatrix} 2 & -5 \\ -1 & 3\end{bmatrix} = \begin{bmatrix} 6 - 5 & -15 + 15 \\ 2 - 2 & -5 + 6\end{bmatrix} = \mathbf{I}$ ✓.

(b) $\det = 12 - 4k = 0$ when $k = $ **3**. Then the second column $(3, 6)$ is 1.5 times the first column $(2, 4)$: the columns are parallel, and the parallelogram they span has zero area.

### Solution 02-07.4

(a) With the vectors as columns, the determinant is

$$
1(5\cdot9 - 8\cdot6) - 4(2\cdot9 - 8\cdot3) + 7(2\cdot6 - 5\cdot3) = -3 + 24 - 21 = \mathbf{0},
$$

so the vectors are dependent. The middle vector is the average of the outer two: $(1, 2, 3) - $ **2**$(4, 5, 6) + (7, 8, 9) = \mathbf{0}$.

(b) With columns $(1, 0, 1)$, $(1, 1, 0)$ and $(0, 1, 1)$:

$$
\det\begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 1\end{bmatrix} = 1(1 - 0) - 1(0 - 1) + 0 = \mathbf{2} \ne 0 .
$$

So the three vectors are independent. Three independent vectors in a 3-dimensional space form a basis.

### Solution 02-07.5

Start from $[\mathbf{A} \mid \mathbf{I}]$. *Downward:* only row 3 needs work, $R_3 - 2R_1 = (0, 0, 1 \mid -2, 0, 1)$. *Upward:* $R_2 - 3R_3 = (0, 1, 0 \mid 6, 1, -3)$, then $R_1 - 2R_2 = (1, 0, 0 \mid -11, -2, 6)$. Every pivot is already 1, so

$$
\mathbf{A}^{-1} = \begin{bmatrix} \mathbf{-11} & -2 & \mathbf{6} \\ 6 & 1 & \mathbf{-3} \\ \mathbf{-2} & 0 & 1\end{bmatrix} .
$$

*Check:* row 1 of $\mathbf{A}$ times the columns of $\mathbf{A}^{-1}$ gives $(-11 + 12, -2 + 2, 6 - 6) = (1, 0, 0)$ ✓. Row 3 gives $(-22 + 24 - 2, -4 + 4 + 0, 12 - 12 + 1) = (0, 0, 1)$ ✓.

*Why integers:* $\det\mathbf{A} = $ **1** (the pivots are 1, 1 and 1). By the adjugate formula, $\mathbf{A}^{-1} = \mathbf{C}^\mathsf{T}/\det\mathbf{A}$ with integer cofactors.

### Solution 02-07.6

(a) $\det\mathbf{A} = 1(1 - 2) - 1(-2 - 1) + 1(4 + 1) = $ **7**. Replacing columns 1, 2 and 3 in turn by $\mathbf{b} = (6, 3, 2)$:

$$
\det\mathbf{B}_1 = \begin{vmatrix} 6 & 1 & 1 \\ 3 & -1 & 1 \\ 2 & 2 & -1\end{vmatrix} = 7, \quad \det\mathbf{B}_2 = \begin{vmatrix} 1 & 6 & 1 \\ 2 & 3 & 1 \\ 1 & 2 & -1\end{vmatrix} = 14, \quad \det\mathbf{B}_3 = \begin{vmatrix} 1 & 1 & 6 \\ 2 & -1 & 3 \\ 1 & 2 & 2\end{vmatrix} = 21 .
$$

So $\mathbf{x} = (7, 14, 21)/7 = $ **(1, 2, 3)**. Check equation 3: $1 + 4 - 3 = 2$ ✓.

(b) $20! = 2.433\times10^{18}$ terms, at $10^9$ per second, is $2.433\times10^9$ s, or about **77.09 years**. Elimination needs about $\tfrac23\cdot20^3 \approx $ **5333** flops, a few microseconds.

### Solution 02-07.7

$R_2 - 2R_1 = (0, 0, 2, 4)$, then $R_3 - R_2 = \mathbf{0}$. Dividing row 2 by 2 and clearing above its pivot ($R_1 - R_2$):

$$
\mathbf{R} = \begin{bmatrix} 1 & 3 & 0 & 0 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 0 & 0\end{bmatrix} .
$$

The pivots are in columns 1 and 3, so the rank is **2**. A column-space basis is columns 1 and 3 of $\mathbf{A}$: $(1, 2, 0)$ and $(1, 4, 2)$. The free variables are $x_2$ and $x_4$, so the null space has dimension **2**. Its special solutions are:

- $x_2 = 1$, $x_4 = 0$: $(\mathbf{-3}, 1, 0, 0)$;
- $x_2 = 0$, $x_4 = 1$: $(0, 0, \mathbf{-2}, 1)$.

*Checks:* $\mathbf{A}(0, 0, -2, 1) = (-2 + 2, -8 + 8, -4 + 4) = \mathbf{0}$ ✓. Rank–nullity: $2 + 2 = 4$ columns ✓.

### Solution 02-07.8

(a) Elimination with $\mathbf{b}$ carried along: $R_2 - 2R_1$ gives $(0, 1, 1 \mid b_2 - 2b_1)$, and $R_3 - R_1$ gives $(0, 1, 1 \mid b_3 - b_1)$. Subtracting the new row 2 from the new row 3 leaves $(0, 0, 0 \mid b_1 - b_2 + b_3)$. So the system is solvable exactly when $b_1 - b_2 + b_3 = 0$. The rank is 2, so $C(\mathbf{A})$ is the plane of $\mathbf{b}$ vectors satisfying this.

(b) For $(4, 9, 5)$: $4 - 9 + 5 = $ **0** ✓. With the free variable $x_3 = 0$: $x_2 = b_2 - 2b_1 = $ **1** and $x_1 = 4 - x_2 = $ **3**. Null space: $x_3 = 1$ gives $x_2 = -1$ and $x_1 = -x_2 - 2 = -1$. So

$$
\mathbf{x} = (3, 1, 0) + c\,(-1, -1, 1) .
$$

Check: $\mathbf{A}(-1, -1, 1) = (-1 - 1 + 2, -2 - 3 + 5, -1 - 2 + 3) = \mathbf{0}$ ✓.

(c) $1 - 0 + 0 = $ **1** $\ne 0$: no solution.

### Solution 02-07.9

(a) The edge vectors from $(1, 1)$ are $(3, 1)$ and $(1, 4)$. The parallelogram they span has area $\lvert3\cdot4 - 1\cdot1\rvert = 11$, and the triangle is half of it: **5.5**.

(b) $\det\begin{bmatrix} 1 & 1 & 1 \\ 0 & 2 & 1 \\ 0 & 0 & 3\end{bmatrix} = 1\cdot2\cdot3 = $ **6** (the edges are the columns, and the matrix is triangular).

(c) $\det\mathbf{A} = 6$, so every area is multiplied by 6. The unit disk, area π, becomes an ellipse of area $6\pi = $ **18.85**.

### Solution 02-07.10

The data give $\mathbf{A} = \begin{bmatrix} 1 & 1 & 1 & 1 \\ 0 & 1 & 2 & 3\end{bmatrix}^\mathsf{T}$ and $\mathbf{b} = (1, 3, 4, 4)$, so the normal equations are

$$
\begin{bmatrix} 4 & 6 \\ 6 & \mathbf{14}\end{bmatrix}\begin{bmatrix} c \\ d\end{bmatrix} = \begin{bmatrix} 12 \\ \mathbf{23}\end{bmatrix} .
$$

Subtracting 1.5 × row 1 from row 2 gives $5d = 5$, so $d = $ **1**, and then $c = (12 - 6)/4 = $ **1.5**. The line is $b = 1.5 + t$.

The residuals are $(1 - 1.5, 3 - 2.5, 4 - 3.5, 4 - 4.5) = (-0.5, 0.5, 0.5, -0.5)$, with sum of squares **1**.

*Orthogonality:* the residuals sum to zero (perpendicular to the ones column) ✓, and $0(-0.5) + 1(0.5) + 2(0.5) + 3(-0.5) = 0$ (perpendicular to the $t$ column) ✓.

### Solution 02-07.11

(a) $\mathbf{G} = \begin{bmatrix} 1.5 & -1 \\ -1 & 1.25\end{bmatrix}$ mS, with $\det\mathbf{G} = 1.875 - 1 = $ **0.875**. So

$$
\mathbf{R} = \frac{1}{0.875}\begin{bmatrix} 1.25 & 1 \\ 1 & 1.5\end{bmatrix} = \begin{bmatrix} \mathbf{1.429} & \mathbf{1.143} \\ 1.143 & \mathbf{1.714}\end{bmatrix}\text{ kΩ}.
$$

(b) $\mathbf{v} = \mathbf{R}(5, -1)$ mA: $v_1 = 1.429\cdot5 - 1.143 = $ **6 V** and $v_2 = 1.143\cdot5 - 1.714 = $ **4 V**, as in Problem 02-06.11 ✓. (Exactly: $(6.25 - 1)/0.875 = 6$ and $(5 - 1.5)/0.875 = 4$.)

(c) From node 1, with the sources removed, $R_1 = 2$ kΩ is in parallel with $R_2 + R_3 = 5$ kΩ: $2\parallel5 = 1.429$ kΩ ✓. From node 2, $R_3 = 4$ kΩ is in parallel with $R_2 + R_1 = 3$ kΩ: $4\parallel3 = 1.714$ kΩ ✓.

### Solution 02-07.12

(a) Stamping with the series conductance 1 mS between the ports, 2 mS from port 1 to ground and 1 mS from port 2 to ground:

$$
\mathbf{Y} = \begin{bmatrix} 3 & -1 \\ -1 & 2\end{bmatrix}\text{ mS}, \qquad \det\mathbf{Y} = \mathbf{5}\text{ mS}^2 .
$$

(b)

$$
\mathbf{Z} = \mathbf{Y}^{-1} = \frac15\begin{bmatrix} 2 & 1 \\ 1 & 3\end{bmatrix} = \begin{bmatrix} \mathbf{0.4} & \mathbf{0.2} \\ 0.2 & \mathbf{0.6}\end{bmatrix}\text{ kΩ}.
$$

(c) $Z_{11}$ is the resistance seen at port 1 with port 2 open: $0.5\text{ kΩ}\parallel(1 + 1)\text{ kΩ} = 0.4$ kΩ ✓. $Z_{22}$ is the resistance seen at port 2 with port 1 open: $1\text{ kΩ}\parallel(1 + 0.5)\text{ kΩ} = 0.6$ kΩ ✓.

$Z_{21}$ is the open-circuit voltage at port 2 per ampere driven into port 1. 1 mA into port 1 gives $v_1 = 0.4$ V, and the 1 kΩ + 1 kΩ path divides it in half: $v_2 = 0.2$ V, so $Z_{21} = 0.2$ kΩ ✓. $Z_{12} = Z_{21}$ by reciprocity.

### Solution 02-07.13

(a) With columns for nodes 0, 1, 2 and 3, the rows are:

- branch 1→2: $(0, 1, -1, 0)$;
- branch 1→3: $(0, 1, 0, -1)$;
- branch 2→3: $(0, 0, 1, -1)$;
- branch 2→0: $(-1, 0, 1, 0)$;
- branch 3→0: $(-1, 0, 0, 1)$.

The graph is connected, so the rank is $4 - 1 = $ **3**, and there are $5 - 3 = $ **2** independent loops: for example 1→2→3→1 and 2→3→0→2.

(b) Deleting the ground column and using $\mathbf{C} = \mathbf{I}$ mS:

$$
\mathbf{G} = \begin{bmatrix} 2 & -1 & -1 \\ -1 & 3 & -1 \\ -1 & -1 & 3\end{bmatrix}\text{ mS}.
$$

Solving $\mathbf{G}\mathbf{v} = (1, 0, 0)$: rows 2 and 3 are symmetric, so $v_2 = v_3$. Then row 2 gives $-v_1 + 2v_2 = 0$, and row 1 gives $2v_1 - 2v_2 = 1$. So $v_1 = $ **1 V** and $v_2 = v_3 = $ **0.5 V**. The 2–3 resistor carries $(v_2 - v_3)/1\text{ kΩ} = $ **0**: the bridge is **balanced**, because the two sides are identical, so nodes 2 and 3 sit at the same voltage.

(c) Now $G_{33} = 1 + 1 + 0.5 = 2.5$ mS. Solving gives

$$
\mathbf{v} = \left(\tfrac{13}{11}, \tfrac{7}{11}, \tfrac{8}{11}\right) = (\mathbf{1.182}, \mathbf{0.6364}, \mathbf{0.7273})\text{ V}.
$$

The 2–3 resistor carries $(v_2 - v_3)/1\text{ kΩ} = -1/11$ mA, that is **0.09091 mA** flowing from node 3 to node 2. Raising the 3–0 resistance lifted node 3 above node 2. The source sees $v_1/(1\text{ mA}) = $ **1.182 kΩ**.

*Check (KCL at node 3):* in from node 1, $(1.182 - 0.7273)/1 = 0.4545$ mA; out to ground, $0.7273/2 = 0.3636$ mA; out to node 2, 0.0909 mA. And $0.3636 + 0.0909 = 0.4545$ ✓.

### Solution 02-07.14

(a) The logarithms of the readings are $(1.6094, 1.1151, 0.6152, 0.1133, -0.3857)$. The normal equations for $\ln v = a + bt$ are

$$
\begin{bmatrix} 5 & 10 \\ 10 & 30\end{bmatrix}\begin{bmatrix} a \\ b\end{bmatrix} = \begin{bmatrix} \sum\ln v_i \\ \sum t_i\ln v_i\end{bmatrix} .
$$

They give $b = $ **−0.4992** ms⁻¹ and $a = 1.6119$. So $V_0 = e^a = $ **5.012 V** and $\tau = -1/b = $ **2.003 ms**.

(b) The log fit minimizes squared errors in $\ln v$, which are roughly *relative* errors $\Delta v/v$. A ±5 mV reading error at 0.68 V is a 0.7% relative error, but at 5 V only 0.1%. So the log fit gives the small, late readings as much influence as the large, early ones. The direct fit minimizes squared errors in volts and so trusts the large readings more. Which is right depends on the noise. If each reading has the same *absolute* uncertainty, the direct fit (or a log fit weighted by $v_i^2$) is the appropriate one. If the uncertainty is a fixed *percentage*, the plain log fit is. Here the two estimates of τ differ by **0.3%**, small but larger than the rounding of the data alone would suggest. That is why calibration procedures state which error model they assume.

### Solution 02-07.15

(a)

$$
\mathbf{u}\mathbf{v}^\mathsf{T} = \begin{bmatrix} 1 \\ 2 \\ 3\end{bmatrix}\begin{bmatrix} 4 & 5\end{bmatrix} = \begin{bmatrix} 4 & 5 \\ 8 & 10 \\ 12 & 15\end{bmatrix} .
$$

Every column is a multiple of $\mathbf{u}$, and every row is a multiple of $\mathbf{v}^\mathsf{T}$, so the column space is the line through $\mathbf{u}$: rank **1**.

(b) Each column of $\mathbf{B}\mathbf{A}$ is $\mathbf{B}$ times a column of $\mathbf{A}$, so it is a combination of the $r$ columns of $\mathbf{B}$. Therefore $C(\mathbf{B}\mathbf{A}) \subseteq C(\mathbf{B})$, whose dimension is at most $r$.

(c) The full update has $d^2 = $ **16,777,216** parameters. The factored one has $dr + rd = 2dr = $ **65,536**, a ratio of $d/(2r) = $ **256**. In 16-bit storage, that is **32 MiB** against **128 KiB**.

(d) $\mathbf{W}\mathbf{x}$ costs $d^2 = 16{,}777{,}216$ multiply–adds. Computing $\mathbf{B}(\mathbf{A}\mathbf{x})$, with the parentheses in that order, costs $rd + dr = 65{,}536$: the same 256× saving. Forming $\mathbf{B}\mathbf{A}$ first would cost $d^2r$ and throw the saving away. Associativity guarantees the same answer either way, but not the same cost.

---

## Answer key

### Solution 02-07.16

A subspace must contain $\mathbf{0}$ and be closed under addition and scalar multiplication.

- (a) **Yes**, dimension 2: if $\mathbf{u}$ and $\mathbf{v}$ satisfy $x + 2y - z = 0$, so does $c\mathbf{u} + d\mathbf{v}$, because the left side is linear. It is the null space of $[1\ 2\ -1]$, with $3 - 1 = 2$ free variables.
- (b) **No**: $\mathbf{0}$ gives $0 \ne 1$. (Doubling a vector in it also leaves it.)
- (c) **Yes**, dimension 1: all multiples of $(1, 2, 3)$.
- (d) **No**: $(1, 0, 0)$ is in it but $-1\cdot(1, 0, 0)$ is not, so it is not closed under scaling.
- (e) **No**: $(1, 0, 0)$ and $(0, 1, 0)$ are in it but their sum $(1, 1, 0)$ is on neither axis, so it is not closed under addition.
- (f) **Yes**, dimension 1: all multiples of $(1, 1, 1)$.

So **3** of the six are subspaces.

### Solution 02-07.17

(a) Suppose row $i$ is $\sum_{k\ne i}c_k\,\text{row}_k$. By rule 3 (linearity in row $i$), the determinant splits into $\sum_kc_k\det\mathbf{A}_k$, where $\mathbf{A}_k$ has row $k$ copied into row $i$. Each $\mathbf{A}_k$ has two equal rows, so each term is zero.

(b) Adding a multiple of column $j$ to column $i$ of $\mathbf{A}$ is adding a multiple of row $j$ to row $i$ of $\mathbf{A}^\mathsf{T}$, which does not change $\det\mathbf{A}^\mathsf{T}$. Since $\det\mathbf{A} = \det\mathbf{A}^\mathsf{T}$, $\det\mathbf{A}$ is unchanged too.

(c) The (1, 1) entry is zero, so exchange rows 1 and 2 (one exchange, a factor −1): $\begin{bmatrix}1 & 1 & 1\\ 0 & 2 & 1\\ 2 & 0 & 3\end{bmatrix}$. Subtract 2 × row 1 from row 3: $(0, -2, 1)$. Add row 2 to row 3: $(0, 0, 2)$. The pivots are 1, 2 and 2, so $\det = -(1\cdot2\cdot2) = $ **−4**. Cofactor check down column 1: $0\cdot C_{11} - 1\cdot\det\begin{bmatrix}2 & 1\\ 0 & 3\end{bmatrix} + 2\cdot\det\begin{bmatrix}2 & 1\\ 1 & 1\end{bmatrix} = -6 + 2 = -4$ ✓.

### Solution 02-07.18

(a) $\mathbf{P}^\mathsf{T} = \mathbf{A}\big((\mathbf{A}^\mathsf{T}\mathbf{A})^{-1}\big)^\mathsf{T}\mathbf{A}^\mathsf{T} = \mathbf{P}$, because $\mathbf{A}^\mathsf{T}\mathbf{A}$ is symmetric and so is its inverse. And $\mathbf{P}^2 = \mathbf{A}(\mathbf{A}^\mathsf{T}\mathbf{A})^{-1}(\mathbf{A}^\mathsf{T}\mathbf{A})(\mathbf{A}^\mathsf{T}\mathbf{A})^{-1}\mathbf{A}^\mathsf{T} = \mathbf{P}$. Geometrically, projecting twice changes nothing ($\mathbf{P}^2 = \mathbf{P}$): a vector already in the column space stays put. Symmetry says the projection is *orthogonal*: the error $\mathbf{b} - \mathbf{P}\mathbf{b}$ is perpendicular to the space.

(b) For one column, $\mathbf{P} = \mathbf{a}\mathbf{a}^\mathsf{T}/(\mathbf{a}^\mathsf{T}\mathbf{a})$ with $\mathbf{a}^\mathsf{T}\mathbf{a} = 9$:

$$
\mathbf{P} = \frac19\begin{bmatrix}1 & 2 & 2\\ 2 & 4 & 4\\ 2 & 4 & 4\end{bmatrix},
$$

so $P_{11} = $ **0.1111** and $P_{22} = $ **0.4444**. Its trace is $(1 + 4 + 4)/9 = $ **1**, the dimension of the line it projects onto.

(c) $\mathbf{P}\mathbf{b}$ is the first column of $\mathbf{P}$: $(0.1111, 0.2222, 0.2222)$. $(\mathbf{I} - \mathbf{P})^2 = \mathbf{I} - 2\mathbf{P} + \mathbf{P}^2 = \mathbf{I} - \mathbf{P}$, and it is symmetric, so it is a projection too: onto the plane perpendicular to $\mathbf{a}$. Then $(\mathbf{I} - \mathbf{P})\mathbf{b} = (0.8889, -0.2222, -0.2222)$, and its dot product with $\mathbf{a}$ is $(8 - 4 - 4)/9 = 0$ ✓.

### Solution 02-07.19

(a) With $m = 5$, $n = 7$ and $r = 3$: the column space has dimension **3** (in $\mathbb{R}^5$), the null space $n - r = $ **4** (in $\mathbb{R}^7$), the row space **3** (in $\mathbb{R}^7$) and the left null space $m - r = $ **2** (in $\mathbb{R}^5$).

(b) With $+1$ at each branch's start and $-1$ at its end:

$$
\mathbf{A} = \begin{bmatrix}1 & -1 & 0\\ 0 & 1 & -1\\ -1 & 0 & 1\end{bmatrix}.
$$

The rows sum to zero (row 3 is minus the sum of rows 1 and 2), so the rank is **2**. The null space is spanned by $(1, 1, 1)$: raising all three node voltages together produces no branch voltage. The left null space ($\mathbf{A}^\mathsf{T}\mathbf{y} = \mathbf{0}$) is spanned by $(1, 1, 1)$ in branch space: equal currents in the three branches circulate around the loop and satisfy KCL at every node. Its dimension, $b - r = 3 - 2 = 1$, is the number of independent loops ✓.

### Solution 02-07.20

(a) $r_{11} = \lVert\mathbf{a}_1\rVert = 3$, so $\mathbf{q}_1 = (1, 2, 2)/3$. Then $r_{12} = \mathbf{q}_1\cdot\mathbf{a}_2 = (1 + 0 + 2)/3 = 1$, and $\mathbf{w}_2 = \mathbf{a}_2 - \mathbf{q}_1 = (2/3, -2/3, 1/3)$, whose length is $\sqrt{(4 + 4 + 1)/9} = 1$. So $r_{22} = 1$ and $\mathbf{q}_2 = (2/3, -2/3, 1/3)$:

$$
\mathbf{A} = \begin{bmatrix}1/3 & 2/3\\ 2/3 & -2/3\\ 2/3 & 1/3\end{bmatrix}\begin{bmatrix}3 & 1\\ 0 & 1\end{bmatrix}.
$$

(b) $\mathbf{Q}^\mathsf{T}\mathbf{b} = \big((3 + 6 + 6)/3,\ (6 - 6 + 3)/3\big) = (5, 1)$. Back substitution: $x_2 = $ **1**, then $3x_1 + 1 = 5$ gives $x_1 = 4/3 = $ **1.333**. Normal equations: $\mathbf{A}^\mathsf{T}\mathbf{A} = \begin{bmatrix}9 & 3\\ 3 & 2\end{bmatrix}$ and $\mathbf{A}^\mathsf{T}\mathbf{b} = (15, 6)$; then $9(4/3) + 3 = 15$ ✓ and $3(4/3) + 2 = 6$ ✓.

(c) $\mathbf{e} = \mathbf{b} - \mathbf{A}\hat{\mathbf{x}} = (3, 3, 3) - (7/3, 8/3, 11/3) = (2/3, 1/3, -2/3)$, of length $\sqrt{(4 + 1 + 4)/9} = $ **1**. Dot products: with $\mathbf{a}_1$, $(2 + 2 - 4)/3 = 0$ ✓; with $\mathbf{a}_2$, $(2 + 0 - 2)/3 = 0$ ✓.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-07.1a | det of the 2×2 | 10 | — |
| 02-07.1b | det of the 3×3 by cofactors | −15 | — |
| 02-07.1c | det of the triangular matrix | −8 | — |
| 02-07.2a | det(3A) | 108 | — |
| 02-07.2b | det Aᵀ | 4 | — |
| 02-07.2c | det A⁻¹ | 0.25 | — |
| 02-07.2d | det A² | 16 | — |
| 02-07.2e | det after a row exchange | −4 | — |
| 02-07.2f | det(−A) | −4 | — |
| 02-07.3a | det of [[3, 5], [1, 2]] | 1 | — |
| 02-07.3b | (1, 2) entry of the inverse | −5 | — |
| 02-07.3c | (2, 1) entry of the inverse | −1 | — |
| 02-07.3d | k for singularity | 3 | — |
| 02-07.4a | det of the dependent set | 0 | — |
| 02-07.4b | weight on (4, 5, 6) in the dependence | −2 | — |
| 02-07.4c | det of the basis matrix | 2 | — |
| 02-07.5a | det A | 1 | — |
| 02-07.5b | (1, 1) entry of the inverse | −11 | — |
| 02-07.5c | (1, 3) entry of the inverse | 6 | — |
| 02-07.5d | (2, 3) entry of the inverse | −3 | — |
| 02-07.5e | (3, 1) entry of the inverse | −2 | — |
| 02-07.6a | det A | 7 | — |
| 02-07.6b | x1 | 1 | — |
| 02-07.6c | x2 | 2 | — |
| 02-07.6d | x3 | 3 | — |
| 02-07.6e | time for 20! terms at 1e9/s | 77.09 | years |
| 02-07.6f | elimination flops for n = 20 | 5333 | flop |
| 02-07.7a | rank | 2 | — |
| 02-07.7b | dimension of the null space | 2 | — |
| 02-07.7c | first entry of the first special solution | −3 | — |
| 02-07.7d | third entry of the second special solution | −2 | — |
| 02-07.8a | solvability value for (4, 9, 5) | 0 | — |
| 02-07.8b | x1 of the particular solution | 3 | — |
| 02-07.8c | x2 of the particular solution | 1 | — |
| 02-07.8d | solvability value for (1, 0, 0) | 1 | — |
| 02-07.9a | triangle area | 5.5 | — |
| 02-07.9b | parallelepiped volume | 6 | — |
| 02-07.9c | ellipse area | 18.85 | — |
| 02-07.10a | intercept c | 1.5 | — |
| 02-07.10b | slope d | 1 | — |
| 02-07.10c | sum of squared residuals | 1 | — |
| 02-07.10d | (2, 2) entry of AᵀA | 14 | — |
| 02-07.10e | second entry of Aᵀb | 23 | — |
| 02-07.11a | det G | 0.875 | mS² |
| 02-07.11b | R11 | 1.429 | kΩ |
| 02-07.11c | R12 | 1.143 | kΩ |
| 02-07.11d | R22 | 1.714 | kΩ |
| 02-07.11e | v1 | 6 | V |
| 02-07.11f | v2 | 4 | V |
| 02-07.12a | det Y | 5 | mS² |
| 02-07.12b | Z11 | 0.4 | kΩ |
| 02-07.12c | Z21 | 0.2 | kΩ |
| 02-07.12d | Z22 | 0.6 | kΩ |
| 02-07.13a | rank of the incidence matrix | 3 | — |
| 02-07.13b | independent loops | 2 | — |
| 02-07.13c | v1, balanced | 1 | V |
| 02-07.13d | v2 = v3, balanced | 0.5 | V |
| 02-07.13e | current in the 2–3 resistor, balanced | 0 | mA |
| 02-07.13f | v1, unbalanced | 1.182 | V |
| 02-07.13g | v2, unbalanced | 0.6364 | V |
| 02-07.13h | v3, unbalanced | 0.7273 | V |
| 02-07.13i | current from node 3 to node 2, unbalanced | 0.09091 | mA |
| 02-07.13j | resistance seen by the source, unbalanced | 1.182 | kΩ |
| 02-07.14a | slope b of ln v | −0.4992 | 1/ms |
| 02-07.14b | V0 from the log fit | 5.012 | V |
| 02-07.14c | τ from the log fit | 2.003 | ms |
| 02-07.14d | V0 from the direct fit | 5.003 | V |
| 02-07.14e | τ from the direct fit | 2.010 | ms |
| 02-07.14f | relative difference of the two τ estimates | 0.3 | % |
| 02-07.15a | rank of the outer product | 1 | — |
| 02-07.15b | full-update parameters | 16777216 | — |
| 02-07.15c | factored parameters | 65536 | — |
| 02-07.15d | ratio | 256 | — |
| 02-07.15e | full-update memory in 16-bit storage | 32 | MiB |
| 02-07.15f | factored memory in 16-bit storage | 128 | KiB |
| 02-07.16a | number of subspaces | 3 | — |
| 02-07.16b | dimension of the plane in (a) | 2 | — |
| 02-07.17a | determinant | −4 | — |
| 02-07.18a | P11 | 0.1111 | — |
| 02-07.18b | P22 | 0.4444 | — |
| 02-07.18c | trace of P | 1 | — |
| 02-07.18d | second entry of Pb | 0.2222 | — |
| 02-07.19a | dim N(A), 5×7 rank 3 | 4 | — |
| 02-07.19b | dim N(Aᵀ), 5×7 rank 3 | 2 | — |
| 02-07.19c | rank of the triangle incidence matrix | 2 | — |
| 02-07.20a | r11 | 3 | — |
| 02-07.20b | r12 | 1 | — |
| 02-07.20c | x1 | 1.333 | — |
| 02-07.20d | x2 | 1 | — |
| 02-07.20e | residual length | 1 | — |
