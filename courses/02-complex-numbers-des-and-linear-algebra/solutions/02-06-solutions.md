# Solutions 02-06 · Vectors, Matrices and Linear Systems

Problems: [02-06 problems](../problems/02-06-problems.md) · Chapter: [02-06](../chapters/02-06-vectors-matrices-and-linear-systems.md)

Every numerical answer below is recomputed by [verify_02_06.py](../verify/verify_02_06.py). The circuits of Problems 11, 13 and 14 are also simulated in ngspice in the [lab](../labs/02-06-lab/README.md).

---

## Solutions

### Solution 02-06.1

(a) $2\mathbf{a} - \mathbf{b} = (2 - 4,\ -4 - 0,\ 4 + 3) = $ **(−2, −4, 7)**.

(b) $\mathbf{a}\cdot\mathbf{b} = 1\cdot4 + (-2)\cdot0 + 2\cdot(-3) = $ **−2**.

(c) $\lVert\mathbf{a}\rVert = \sqrt{1 + 4 + 4} = $ **3** and $\lVert\mathbf{b}\rVert = \sqrt{16 + 0 + 9} = $ **5**.

(d) $\mathbf{a}/\lVert\mathbf{a}\rVert = (1/3, -2/3, 2/3) = (0.3333, $ **−0.6667**$, 0.6667)$. Check: $1/9 + 4/9 + 4/9 = 1$ ✓.

(e) $\cos\theta = -2/(3\cdot5) = -0.1333$, so θ = **97.66°**: slightly obtuse, as the negative dot product requires.

### Solution 02-06.2

(a) $(1, c, 2)\cdot(3, -1, c) = 3 - c + 2c = 3 + c = 0$, so $c = $ **−3**. Check: $(1, -3, 2)\cdot(3, -1, -3) = 3 + 3 - 6 = 0$ ✓.

(b) $\cos\theta = \dfrac{(1, 1, 1)\cdot(1, 0, 0)}{\sqrt3\cdot1} = \dfrac{1}{\sqrt3}$, so θ = **54.74°**.

(c) $\cos\theta = \dfrac{1 + 1 - 1}{\sqrt3\sqrt3} = \dfrac13$, so θ = **70.53°**.

(d) Using $\sin\theta\cos\theta = \tfrac12\sin2\theta$,

$$
\sum_{k=0}^{7}\sin\theta_k\cos\theta_k = \frac12\sum_{k=0}^{7}\sin\frac{\pi k}{2} = \frac12(0 + 1 + 0 - 1 + 0 + 1 + 0 - 1) = \mathbf{0} .
$$

The sampled sine and cosine are orthogonal. This is the discrete version of the Fourier orthogonality of [01-06](../../01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md), and it is what makes the discrete Fourier transform work ([16](../../16-digital-signal-processing/README.md)).

### Solution 02-06.3

(a) *Row picture:* $(1\cdot2 + 2(-1),\ 3\cdot2 + (-1)(-1),\ 0\cdot2 + 4(-1)) = (\mathbf{0}, \mathbf{7}, \mathbf{-4})$. *Column picture:* $2(1, 3, 0) - 1(2, -1, 4) = (0, 7, -4)$, the same ✓.

(b) The equations are $x_1 + 2x_2 = 5$, $3x_1 - x_2 = 1$ and $4x_2 = 8$. The third gives $x_2 = $ **2**, the first then gives $x_1 = $ **1**, and the second checks: $3 - 2 = 1$ ✓. A solution exists because $\mathbf{b} = 1\cdot(1, 3, 0) + 2\cdot(2, -1, 4)$ happens to lie in the plane spanned by the two columns. A generic $\mathbf{b}$ in $\mathbb{R}^3$ would lie off that plane, and there would be no exact solution; the best approximate one is a least-squares problem ([02-07](../chapters/02-07-determinants-inverses-and-vector-spaces.md)).

### Solution 02-06.4

(a) Rows times columns:

$$
\mathbf{A}\mathbf{B} = \begin{bmatrix} 1 + 6 & 0 + 2 \\ 0 + 3 & 0 + 1\end{bmatrix} = \begin{bmatrix} \mathbf{7} & 2 \\ \mathbf{3} & 1\end{bmatrix}, \qquad \mathbf{B}\mathbf{A} = \begin{bmatrix} 1 & 2 \\ 3 & 6 + 1\end{bmatrix} = \begin{bmatrix} 1 & 2 \\ 3 & \mathbf{7}\end{bmatrix} .
$$

(b) $(\mathbf{A}\mathbf{B})^\mathsf{T} = \begin{bmatrix} 7 & 3 \\ 2 & 1\end{bmatrix}$. With $\mathbf{B}^\mathsf{T} = \begin{bmatrix} 1 & 3 \\ 0 & 1\end{bmatrix}$ and $\mathbf{A}^\mathsf{T} = \begin{bmatrix} 1 & 0 \\ 2 & 1\end{bmatrix}$:

$$
\mathbf{B}^\mathsf{T}\mathbf{A}^\mathsf{T} = \begin{bmatrix} 1 + 6 & 3 \\ 2 & 1\end{bmatrix} = \begin{bmatrix} 7 & 3 \\ 2 & 1\end{bmatrix}\ ✓, \qquad \mathbf{A}^\mathsf{T}\mathbf{B}^\mathsf{T} = \begin{bmatrix} \mathbf{1} & 3 \\ 2 & 7\end{bmatrix} \ne (\mathbf{A}\mathbf{B})^\mathsf{T} .
$$

In fact $\mathbf{A}^\mathsf{T}\mathbf{B}^\mathsf{T} = (\mathbf{B}\mathbf{A})^\mathsf{T}$.

(c) $\mathbf{A}^2 = \begin{bmatrix} 1 & 2 + 2 \\ 0 & 1\end{bmatrix} = \begin{bmatrix} 1 & \mathbf{4} \\ 0 & 1\end{bmatrix}$. $\mathbf{A}$ sends $(x, y)$ to $(x + 2y, y)$: a **horizontal shear** that slides each point sideways by twice its height. Applying it twice slides by $4y$.

### Solution 02-06.5

(a) $\hat{x} = \dfrac{\mathbf{a}\cdot\mathbf{b}}{\mathbf{a}\cdot\mathbf{a}} = \dfrac{1 + 2 + 6}{3} = $ **3**, so $\mathbf{p} = (3, 3, 3)$, $\mathbf{e} = (-2, -1, 3)$ and $\lVert\mathbf{e}\rVert^2 = 4 + 1 + 9 = $ **14**.

In general, with $\mathbf{a} = (1, \dots, 1)$, $\mathbf{a}\cdot\mathbf{b} = \sum b_i$ and $\mathbf{a}\cdot\mathbf{a} = n$, so $\hat{x} = \sum b_i/n$ is the mean. The error components $e_i = b_i - \hat{x}$ are the deviations from the mean, so $\lVert\mathbf{e}\rVert^2/n$ is the population variance: here $14/3 = $ **4.667**. The orthogonality condition $\mathbf{e}\cdot(1, \dots, 1) = 0$ is the familiar fact that deviations from the mean sum to zero.

(b) $\mathbf{a}\cdot\mathbf{b} = 1 + 4 + 12 = 17$ and $\mathbf{a}\cdot\mathbf{a} = 9$, so $\hat{x} = 17/9 = $ **1.889** and $\mathbf{p} = (1.889, 3.778, 3.778)$. The error is $\mathbf{e} = (-0.8889, -1.778, 2.222)$, and $\mathbf{e}\cdot\mathbf{a} = -0.8889 - 3.556 + 4.444 = 0$ ✓. Its length is $\sqrt{0.7901 + 3.160 + 4.938} = $ **2.981**.

*Check by Pythagoras:* $\lVert\mathbf{b}\rVert^2 = 41$ should equal $\lVert\mathbf{p}\rVert^2 + \lVert\mathbf{e}\rVert^2 = (17/9)^2\cdot9 + 8.889 = 32.11 + 8.889 = 41$ ✓.

### Solution 02-06.6

Augmented matrix and column 1 (pivot 1): $\ell_{21} = $ **3** and $\ell_{31} = $ **2**.

$$
\left[\begin{array}{ccc|c} 1 & 1 & 2 & 3 \\ 3 & 4 & 5 & 7 \\ 2 & -2 & 1 & 7\end{array}\right] \xrightarrow{\;R_2 - 3R_1,\ R_3 - 2R_1\;} \left[\begin{array}{ccc|c} 1 & 1 & 2 & 3 \\ 0 & 1 & -1 & -2 \\ 0 & -4 & -3 & 1\end{array}\right] .
$$

Column 2 (pivot 1): $\ell_{32} = -4/1 = $ **−4**, so add 4 times row 2 to row 3:

$$
\xrightarrow{\;R_3 + 4R_2\;} \left[\begin{array}{ccc|c} 1 & 1 & 2 & 3 \\ 0 & 1 & -1 & -2 \\ 0 & 0 & -7 & -7\end{array}\right] .
$$

The pivots are 1, 1 and **−7**. Back substitution: $x_3 = -7/-7 = $ **1**; $x_2 = -2 + x_3 = $ **−1**; $x_1 = 3 - x_2 - 2x_3 = $ **2**.

**Check.** Equation 2: $6 - 4 + 5 = 7$ ✓. Equation 3: $4 + 2 + 1 = 7$ ✓.

### Solution 02-06.7

(a) The permutation exchanging rows 1 and 2 is $\mathbf{P} = \begin{bmatrix} 0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix}$. It gives $\mathbf{P}\mathbf{A}$ with rows $(1, 2, 1)$, $(0, 1, 2)$ and $(2, 7, 9)$, and $\mathbf{P}\mathbf{b} = (0, 1, 4)$.

- Column 1: $\ell_{21} = 0$ and $\ell_{31} = 2$. Row 3 becomes $(0, 3, 7 \mid 4)$.
- Column 2: $\ell_{32} = $ **3**. Row 3 becomes $(0, 0, 1 \mid 1)$.

So

$$
\mathbf{L} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 2 & 3 & 1\end{bmatrix}, \qquad \mathbf{U} = \begin{bmatrix} 1 & 2 & 1 \\ 0 & 1 & 2 \\ 0 & 0 & 1\end{bmatrix} .
$$

Back substitution: $x_3 = $ **1**, $x_2 = 1 - 2x_3 = $ **−1**, $x_1 = 0 - 2x_2 - x_3 = $ **1**. Check row 1 of the original: $0 - 1 + 2 = 1$ ✓.

(b) *Column 1:* the largest magnitude is the 2 in row 3, so exchange rows 1 and 3: $(2, 7, 9 \mid 4)$, $(1, 2, 1 \mid 0)$, $(0, 1, 2 \mid 1)$. Then $\ell_{21} = $ **0.5**, so row 2 becomes $(0, -1.5, -3.5 \mid -2)$; and $\ell_{31} = 0$.

*Column 2:* the candidates are −1.5 and 1, so −1.5 stays as pivot. Then $\ell_{32} = 1/(-1.5) = $ **−0.6667**, and row 3 becomes

$$
(0, 1, 2 \mid 1) - \left(-\tfrac23\right)(0, -1.5, -3.5 \mid -2) = (0, 0, -\tfrac13 \mid -\tfrac13).
$$

The pivots are **2**, **−1.5** and **−0.3333**. The multipliers 0.5, 0 and −0.6667 all have magnitude at most 1 ✓. Back substitution gives the same solution: $x_3 = 1$, $x_2 = (-2 + 3.5)/(-1.5) = -1$, and $x_1 = (4 + 7 - 9)/2 = 1$ ✓.

Note that the two sets of pivots differ, but their products ($1\cdot1\cdot1$ and $2\cdot(-1.5)\cdot(-\tfrac13)$) are both 1. That is no accident: it is $\lvert\det\mathbf{A}\rvert$ ([02-07](../chapters/02-07-determinants-inverses-and-vector-spaces.md)).

### Solution 02-06.8

(a) $R_2 - 2R_1$ gives $0 = k - 6$. If $k = $ **6**, that row is $0 = 0$, $x_2$ is free, and there are infinitely many solutions $(3 - 2t, t)$. Otherwise the row reads $0 = $ nonzero, so there is no solution. Exactly one solution is impossible, since the second column is twice the first.

(b) $R_2 - 2R_1$ gives $(a - 4)x_2 = -1$. For $a = $ **4** this reads $0 = -1$: no solution (parallel lines). Otherwise $x_2 = -1/(a - 4)$. For $a = 5$: $x_2 = $ **−1** and $x_1 = 3 - 2x_2 = $ **5**. Check: $2\cdot5 + 5(-1) = 5$ ✓.

(c) $R_2 - 2R_1 = (0, 1, 1)$, $R_3 - 3R_1 = (0, 1, q - 9)$, then $R_3 - R_2 = (0, 0, q - 10)$. The third pivot is $q - 10$, so the matrix is singular exactly when $q = $ **10**. Then column 3 = column 1 + column 2, since $(1 + 2, 2 + 5, 3 + 7) = (3, 7, 10)$ ✓.

### Solution 02-06.9

(a) $\ell_{21} = 6/4 = $ **1.5**. Row 2 of $\mathbf{U}$ is $(6, 3) - 1.5(4, 3) = (0, $ **−1.5**$)$. So $\mathbf{L} = \begin{bmatrix} 1 & 0 \\ 1.5 & 1\end{bmatrix}$ and $\mathbf{U} = \begin{bmatrix} 4 & 3 \\ 0 & -1.5\end{bmatrix}$.

(b) For $\mathbf{b} = (10, 12)$: $c_1 = 10$ and $c_2 = 12 - 1.5\cdot10 = -3$; then $x_2 = -3/-1.5 = $ **2** and $x_1 = (10 - 3\cdot2)/4 = $ **1**. For $\mathbf{b} = (1, 0)$: $\mathbf{c} = (1, -1.5)$, so $x_2 = 1$ and $x_1 = (1 - 3)/4 = $ **−0.5**.

(c) The first column of $\mathbf{A}^{-1}$ is the second solution of (b), $(-0.5, 1)$. For $(0, 1)$: $\mathbf{c} = (0, 1)$, so $x_2 = 1/(-1.5) = $ **−0.6667** and $x_1 = (0 - 3x_2)/4 = $ **0.5**. So

$$
\mathbf{A}^{-1} = \begin{bmatrix} -0.5 & 0.5 \\ 1 & -0.6667\end{bmatrix}, \qquad \mathbf{A}\mathbf{A}^{-1} = \begin{bmatrix} -2 + 3 & 2 - 2 \\ -3 + 3 & 3 - 2\end{bmatrix} = \mathbf{I}\ ✓.
$$

Computing the inverse took $n$ solves. To solve a single system, that is wasted work (Common mistake 6).

### Solution 02-06.10

(a) Each elimination matrix is the identity with one off-diagonal entry, the negative of its multiplier:

- $\mathbf{E}_{21}$ has $-2$ in position $(2, 1)$;
- $\mathbf{E}_{31}$ has $+1$ in position $(3, 1)$;
- $\mathbf{E}_{32}$ has $-2$ in position $(3, 2)$.

(b) First, $\mathbf{E}_{31}\mathbf{E}_{21}$ has rows $(1, 0, 0)$, $(-2, 1, 0)$ and $(1, 0, 1)$. Multiplying by $\mathbf{E}_{32}$ replaces row 3 with row 3 minus 2 × row 2: $(1 + 4, -2, 1) = (5, -2, 1)$. So

$$
\mathbf{E} = \begin{bmatrix} 1 & 0 & 0 \\ \mathbf{-2} & 1 & 0 \\ \mathbf{5} & \mathbf{-2} & 1\end{bmatrix} .
$$

The $(3, 1)$ entry is $\ell_{32}\ell_{21} - \ell_{31} = 2\cdot2 - (-1) = 5$ ✓. The extra term arises because $\mathbf{E}_{32}$ subtracts twice the *new* row 2, which already contains $-2$ times row 1.

(c) In reverse order, each inverse adds a multiple of an earlier row to a later one. $\mathbf{E}_{31}^{-1}\mathbf{E}_{32}^{-1}$ has rows $(1, 0, 0)$, $(0, 1, 0)$ and $(-1, 2, 1)$. Then $\mathbf{E}_{21}^{-1}$ adds 2 × row 1 to row 2:

$$
\mathbf{L} = \begin{bmatrix} 1 & 0 & 0 \\ 2 & 1 & 0 \\ \mathbf{-1} & 2 & 1\end{bmatrix},
$$

which holds $\ell_{21} = 2$, $\ell_{31} = -1$ and $\ell_{32} = 2$ unchanged ✓. Multiplying $\mathbf{E}$ by Example 02-06.3's $\mathbf{A}$ reproduces its $\mathbf{U}$, and $\mathbf{E}\mathbf{L} = \mathbf{I}$.

### Solution 02-06.11

(a) The conductances are $g_1 = 0.5$, $g_2 = 1$ and $g_3 = 0.25$ mS. Stamping:

$$
\mathbf{G} = \begin{bmatrix} g_1 + g_2 & -g_2 \\ -g_2 & g_2 + g_3\end{bmatrix} = \begin{bmatrix} 1.5 & -1 \\ -1 & 1.25\end{bmatrix}\text{ mS}, \qquad \mathbf{i} = \begin{bmatrix} 5 \\ -1\end{bmatrix}\text{ mA}.
$$

Eliminate with $\ell_{21} = -2/3$: $u_{22} = 1.25 - 2/3 = 0.5833$ and $c_2 = -1 + (2/3)\cdot5 = 2.333$. So $v_2 = 2.333/0.5833 = $ **4 V** and $v_1 = (5 + v_2)/1.5 = $ **6 V**.

(b) $i_{R2} = (6 - 4)\text{ V}/1\text{ kΩ} = $ **2 mA**, from node 1 to node 2.

(c) The 5 mA source delivers $6\text{ V}\times5\text{ mA} = $ **30 mW**. The 1 mA source carries current out of node 2 down to ground, so it absorbs $4\text{ V}\times1\text{ mA} = $ **4 mW**. The resistors dissipate $R_1$: $36/2 = 18$ mW, $R_2$: $2^2/1 = 4$ mW, and $R_3$: $16/4 = 4$ mW, in total **26 mW** = 30 − 4 ✓. KCL at node 2: 2 mA in = 1 mA through $R_3$ + 1 mA through the sink ✓.

### Solution 02-06.12

(a) $\tfrac23(2000)^3 = $ **5.333×10⁹ flops**; at $5\times10^{10}$ flops/s that takes **0.1067 s**.

(b) $2n^2 = 8\times10^6$ flops, which takes **0.16 ms**.

(c) $\tfrac23n^3/(2n^2) = n/3 = $ **666.7**: about 667 right-hand sides cost as much as the factorization, counting flops. In time the break-even comes sooner. Triangular solves do about 2 flops per matrix entry read (8 bytes in FP64), about 0.25 flop/byte, so they run at memory speed, well below the 50 GFLOP/s that the cache-friendly factorization reaches (the arithmetic-intensity argument of Example 02-06.6). Each solve therefore costs several times its flop share, and the break-even is several times fewer than 667 solves.

(d) Factoring grows as $n^3$, by **8**; each solve grows as $n^2$, by **4**.

(e) $8n^2 = 8\times(2000)^2 = 3.2\times10^7$ bytes = **32 MB**.

### Solution 02-06.13

(a) With $g_{12} = 1$, $g_{23} = 1$ and $g_{13} = 0.5$ mS,

$$
\mathbf{G} = \begin{bmatrix} 1.5 & -1 & -0.5 \\ -1 & 2 & -1 \\ -0.5 & -1 & 1.5\end{bmatrix}\text{ mS}.
$$

Each row sums to zero, because each conductance appears once with + on the diagonal and once with − off it. So $\mathbf{G}(1, 1, 1)$, whose components are the row sums, is $\mathbf{0}$.

(b) If $\mathbf{G}\mathbf{v} = \mathbf{i}$, then $\mathbf{G}(\mathbf{v} + c(1, 1, 1)) = \mathbf{G}\mathbf{v} + c\cdot\mathbf{0} = \mathbf{i}$, so every shifted vector is also a solution. Grounding node 3 fixes $v_3 = 0$. Its column then drops out, and its row becomes redundant (it is minus the sum of the other two). That leaves

$$
\begin{bmatrix} 1.5 & -1 \\ -1 & 2\end{bmatrix}\begin{bmatrix} v_1 \\ v_2\end{bmatrix} = \begin{bmatrix} 1 \\ 0\end{bmatrix} .
$$

With $\ell_{21} = -2/3$: $u_{22} = 4/3$ and $c_2 = 2/3$, so $v_2 = $ **0.5 V** and $v_1 = (1 + 0.5)/1.5 = $ **1 V**. The resistance between nodes 1 and 3 is $v_1/(1\text{ mA}) = $ **1 kΩ**. *Check:* the path 1→2→3 (2 kΩ) is in parallel with the direct 2 kΩ, giving 1 kΩ ✓.

(c) Adding the three equations gives $(1, 1, 1)\cdot(\mathbf{G}\mathbf{v}) = 0$ on the left, because $\mathbf{G}$ is symmetric and its rows sum to zero. So a solution requires $i_1 + i_2 + i_3 = 0$: the net current injected into a floating network must be zero. That is charge conservation, since current cannot flow into an isolated network without flowing out again. If the condition fails there is no solution; if it holds there are infinitely many. These are the two singular cases of §3.6.

(d) *Unknowns:* $v_1$, $v_2$ and $i_V$, the current delivered by the source into node 1.

*Equations:*

- KCL at node 1: $1.5v_1 - v_2 = i_V$ (the resistor currents leaving equal the source current entering).
- KCL at node 2: $-v_1 + 2v_2 = 0$.
- The source: $v_1 = 2$.

$$
\begin{bmatrix} 1.5 & -1 & -1 \\ -1 & 2 & 0 \\ 1 & 0 & 0\end{bmatrix}\begin{bmatrix} v_1 \\ v_2 \\ i_V\end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 2\end{bmatrix} .
$$

This gives $v_1 = 2$ V, $v_2 = $ **1 V** and $i_V = 3 - 1 = $ **2 mA**. *Check:* 2 V across the 1 kΩ found in (b) drives 2 mA ✓. If instead $i_V$ is defined as the current *entering* the source's positive terminal from node 1, its column becomes $(+1, 0, 0)$ and the matrix is symmetric. That is SPICE's convention, which is why SPICE reports a negative current for a source that delivers power ([00-04](../../00-orientation/chapters/00-04-toolchain-walkthrough.md)).

### Solution 02-06.14

(a) The current from tap $k - 1$ to tap $k$ is $(v_{k-1} - v_k)/R = (d_k - d_{k-1})/R$. KCL at tap $k$ says current in from the left equals the load current plus current out to the right:

$$
\frac{d_k - d_{k-1}}{R} = I + \frac{d_{k+1} - d_k}{R} \quad\Longrightarrow\quad \frac{-d_{k-1} + 2d_k - d_{k+1}}{R} = I \qquad (k = 1, \dots, 4),
$$

with $d_0 = 0$. At the last tap nothing flows onward, so $(d_5 - d_4)/R = I$. Hence

$$
\mathbf{G} = \frac1R\begin{bmatrix} 2 & -1 & 0 & 0 & 0 \\ -1 & 2 & -1 & 0 & 0 \\ 0 & -1 & 2 & -1 & 0 \\ 0 & 0 & -1 & 2 & -1 \\ 0 & 0 & 0 & -1 & 1\end{bmatrix}, \qquad \frac1R = \mathbf{50}\text{ S}.
$$

(b) Segment $k$ carries the current of every tap from $k$ to $N$, that is $(N - k + 1)I$: 1.0, 0.8, 0.6, 0.4 and 0.2 A. The drops accumulate along the rail: $d_1 = 20$ mΩ × 1.0 A = **20 mV**, then $d_2 = 36$, $d_3 = 48$, $d_4 = 56$ and $d_5 = 60$ mV. In general,

$$
d_N = RI\sum_{k=1}^N(N - k + 1) = RI\,\frac{N(N + 1)}{2} = 0.02\times0.2\times15 = \mathbf{60\text{ mV}}.
$$

Solving the 5×5 system numerically gives the same drops.

(c) By symmetry, each pad supplies half of the 1.0 A total, and the middle tap is fed 0.1 A from each side. From the left pad the segment currents are 0.5, 0.3 and 0.1 A, so the drops are $d_1 = 10$ mV, $d_2 = 16$ mV and $d_3 = $ **18 mV**, then 16 and 10 mV on the way to the right pad. The worst drop is at the middle tap, tap 3.

(d) $60/18 = $ **3.333**. For a long rail with $N$ taps, the drop fed from one end grows as $RIN^2/2$. Fed from both ends, each half carries half the current over half the length, giving about $RIN^2/8$, an improvement approaching 4×. More generally, the worst drop falls as the *square* of the pad spacing. That is why flip-chip packages place supply bumps in an array across the whole die, not just at its edges: pad spacing is the most powerful knob on IR drop ([22-10](../../22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)).

### Solution 02-06.15

(a) Peak throughput is $512\times2\times10^9 = 1.024\times10^{12}$ ops/s = **1.024 TOPS**. The layer needs $2\times1024^2 = $ **2.097×10⁶** operations and reads $1024^2 = 1{,}048{,}576$ bytes = **1.049 MB** of weights. Its arithmetic intensity is **2** operations per byte, because each weight byte feeds exactly one multiply–add.

(b) The memory time is $1{,}048{,}576/(8\times10^9) = $ **131.1 µs** and the compute time is $2.097\times10^6/(1.024\times10^{12}) = $ **2.048 µs**. The layer takes about the longer of the two, so it achieves $2.048/131.1 = $ **1.56%** of peak.

(c) To be compute-bound it would need at least $1.024\times10^{12}/(8\times10^9) = $ **128** operations per byte, the ridge point.

(d) From SRAM, the memory time is $1{,}048{,}576/(2.56\times10^{11}) = $ **4.096 µs**. The layer is still memory-bound (the SRAM ridge point is 4 operations per byte), but it now reaches $2.048/4.096 = $ **50%** of peak, 32 times faster. On-chip SRAM costs die area, but it buys both bandwidth and energy: reading a byte from external DRAM costs far more energy than reading it from nearby SRAM. That is why edge accelerators for wearables keep weights on chip wherever possible, and compress them or store them at low precision to make them fit ([14-14](../../14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md)).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-06.1a | first component of 2a − b | −2 | — |
| 02-06.1b | second component of 2a − b | −4 | — |
| 02-06.1c | third component of 2a − b | 7 | — |
| 02-06.1d | a·b | −2 | — |
| 02-06.1e | length of a | 3 | — |
| 02-06.1f | length of b | 5 | — |
| 02-06.1g | second component of the unit vector | −0.6667 | — |
| 02-06.1h | angle between a and b | 97.66 | ° |
| 02-06.2a | c for orthogonality | −3 | — |
| 02-06.2b | diagonal-to-edge angle | 54.74 | ° |
| 02-06.2c | diagonal-to-diagonal angle | 70.53 | ° |
| 02-06.2d | dot product of sampled sine and cosine | 0 | — |
| 02-06.3a | first component of Ax | 0 | — |
| 02-06.3b | second component of Ax | 7 | — |
| 02-06.3c | third component of Ax | −4 | — |
| 02-06.3d | x1 for (5, 1, 8) | 1 | — |
| 02-06.3e | x2 for (5, 1, 8) | 2 | — |
| 02-06.4a | (1, 1) entry of AB | 7 | — |
| 02-06.4b | (2, 1) entry of AB | 3 | — |
| 02-06.4c | (2, 2) entry of BA | 7 | — |
| 02-06.4d | (1, 1) entry of AᵀBᵀ | 1 | — |
| 02-06.4e | (1, 2) entry of A² | 4 | — |
| 02-06.5a | best constant (mean) | 3 | — |
| 02-06.5b | squared error | 14 | — |
| 02-06.5c | population variance | 4.667 | — |
| 02-06.5d | projection coefficient onto (1, 2, 2) | 1.889 | — |
| 02-06.5e | error length | 2.981 | — |
| 02-06.6a | ℓ21 | 3 | — |
| 02-06.6b | ℓ31 | 2 | — |
| 02-06.6c | ℓ32 | −4 | — |
| 02-06.6d | third pivot | −7 | — |
| 02-06.6e | x1 | 2 | — |
| 02-06.6f | x2 | −1 | — |
| 02-06.6g | x3 | 1 | — |
| 02-06.7a | x1 | 1 | — |
| 02-06.7b | x2 | −1 | — |
| 02-06.7c | x3 | 1 | — |
| 02-06.7d | ℓ32 with the hand exchange | 3 | — |
| 02-06.7e | first pivot, partial pivoting | 2 | — |
| 02-06.7f | second pivot, partial pivoting | −1.5 | — |
| 02-06.7g | third pivot, partial pivoting | −0.3333 | — |
| 02-06.7h | ℓ21, partial pivoting | 0.5 | — |
| 02-06.7i | ℓ32, partial pivoting | −0.6667 | — |
| 02-06.8a | k for infinitely many solutions | 6 | — |
| 02-06.8b | a for no unique solution | 4 | — |
| 02-06.8c | x1 for a = 5 | 5 | — |
| 02-06.8d | x2 for a = 5 | −1 | — |
| 02-06.8e | q for singularity | 10 | — |
| 02-06.9a | ℓ21 | 1.5 | — |
| 02-06.9b | u22 | −1.5 | — |
| 02-06.9c | x1 for (10, 12) | 1 | — |
| 02-06.9d | x2 for (10, 12) | 2 | — |
| 02-06.9e | x1 for (1, 0) | −0.5 | — |
| 02-06.9f | (2, 2) entry of the inverse | −0.6667 | — |
| 02-06.9g | (1, 2) entry of the inverse | 0.5 | — |
| 02-06.10a | (2, 1) entry of E | −2 | — |
| 02-06.10b | (3, 1) entry of E | 5 | — |
| 02-06.10c | (3, 2) entry of E | −2 | — |
| 02-06.10d | (3, 1) entry of L | −1 | — |
| 02-06.11a | v1 | 6 | V |
| 02-06.11b | v2 | 4 | V |
| 02-06.11c | current in R2 | 2 | mA |
| 02-06.11d | power delivered by the 5 mA source | 30 | mW |
| 02-06.11e | power absorbed by the 1 mA source | 4 | mW |
| 02-06.11f | total resistor dissipation | 26 | mW |
| 02-06.12a | factorization flops | 5.333×10^9 | flop |
| 02-06.12b | factorization time | 0.1067 | s |
| 02-06.12c | solve time | 0.16 | ms |
| 02-06.12d | break-even number of solves | 666.7 | — |
| 02-06.12e | factor-time growth when n doubles | 8 | — |
| 02-06.12f | solve-time growth when n doubles | 4 | — |
| 02-06.12g | memory | 32 | MB |
| 02-06.13a | v1 with node 3 grounded | 1 | V |
| 02-06.13b | v2 with node 3 grounded | 0.5 | V |
| 02-06.13c | resistance between nodes 1 and 3 | 1 | kΩ |
| 02-06.13d | v2 with the 2 V source | 1 | V |
| 02-06.13e | source current i_V | 2 | mA |
| 02-06.14a | 1/R | 50 | S |
| 02-06.14b | drop at tap 1, one pad | 20 | mV |
| 02-06.14c | worst drop, one pad | 60 | mV |
| 02-06.14d | worst drop, two pads | 18 | mV |
| 02-06.14e | improvement factor | 3.333 | — |
| 02-06.14f | drop at tap 3, one pad | 48 | mV |
| 02-06.14g | first-segment current, two pads | 0.5 | A |
| 02-06.15a | peak throughput | 1.024 | TOPS |
| 02-06.15b | operations per layer | 2.097×10^6 | — |
| 02-06.15c | weight bytes | 1.049 | MB |
| 02-06.15d | arithmetic intensity | 2 | op/B |
| 02-06.15e | memory time (external) | 131.1 | µs |
| 02-06.15f | compute time | 2.048 | µs |
| 02-06.15g | fraction of peak (external) | 1.56 | % |
| 02-06.15h | ridge point (external) | 128 | op/B |
| 02-06.15i | memory time (SRAM) | 4.096 | µs |
| 02-06.15j | fraction of peak (SRAM) | 50 | % |
| 02-06.15k | ridge point (SRAM) | 4 | op/B |
| 02-06.15l | speedup from SRAM | 32 | — |
