# Solutions 02-08 · Eigenvalues and Eigenvectors

Problems: [02-08 problems](../problems/02-08-problems.md) · Chapter: [02-08](../chapters/02-08-eigenvalues-and-eigenvectors.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_02_08.py](../verify/verify_02_08.py). Problem 13 is also simulated in ngspice in the [lab](../labs/02-08-lab/README.md).

---

## Solutions

### Solution 02-08.1

The trace is 7 and the determinant is $10 - 4 = 6$, so the characteristic equation is $\lambda^2 - 7\lambda + 6 = (\lambda - 6)(\lambda - 1) = 0$: λ = **6** and **1**.

- λ = 6: $\mathbf{A} - 6\mathbf{I} = \begin{bmatrix} -1 & 2 \\ 2 & -4\end{bmatrix}$, giving $\mathbf{x}_1 = (2, 1)$.
- λ = 1: $\mathbf{A} - \mathbf{I} = \begin{bmatrix} 4 & 2 \\ 2 & 1\end{bmatrix}$, giving $\mathbf{x}_2 = (1, -2)$.

*Checks:* $6 + 1 = 7$ and $6\cdot1 = 6$ ✓. $\mathbf{A}(2, 1) = (12, 6) = 6(2, 1)$ ✓. $(2, 1)\cdot(1, -2) = $ **0**: the eigenvectors are orthogonal, as the spectral theorem guarantees for a symmetric matrix with distinct eigenvalues.

### Solution 02-08.2

The matrix is triangular, so its eigenvalues are its diagonal entries: **3**, **−1** and **2**. *Checks:* trace $3 - 1 + 2 = $ **4** ✓ and determinant $3\cdot(-1)\cdot2 = $ **−6** ✓.

The eigenvectors carry over to powers, inverses and shifts, and the eigenvalues transform the same way:

- $\mathbf{A}^2$: 9, 1, 4;
- $\mathbf{A}^{-1}$: $\tfrac13$, −1, $\tfrac12$;
- $\mathbf{A} + 2\mathbf{I}$: **5**, 1, 4.

### Solution 02-08.3

(a) Vectors on the line are unchanged, so λ = **1** with eigenvector $(1, 1)$. Vectors perpendicular to the line are sent to zero, so λ = **0** with eigenvector $(1, -1)$. *Check:* $\mathbf{P} = \tfrac12\begin{bmatrix} 1 & 1 \\ 1 & 1\end{bmatrix}$ has trace 1 and determinant 0 ✓.

(b) The reflection keeps $(1, 1)$, so λ = 1, and flips $(1, -1)$, so λ = **−1**. *Check:* the reflection is $\begin{bmatrix} 0 & 1 \\ 1 & 0\end{bmatrix}$, with trace 0 and determinant −1 ✓.

(c) No real direction survives a 90° rotation, so the eigenvalues are complex: $e^{\pm j90°} = \pm j$, with imaginary parts ±**1**. *Check:* $\begin{bmatrix} 0 & -1 \\ 1 & 0\end{bmatrix}$ has trace 0 and determinant 1, and indeed $j + (-j) = 0$ and $j(-j) = 1$ ✓.

### Solution 02-08.4

With $\mathbf{X} = \begin{bmatrix} 1 & 1 \\ 0 & 1\end{bmatrix}$ (eigenvectors as columns) and $\mathbf{X}^{-1} = \begin{bmatrix} 1 & -1 \\ 0 & 1\end{bmatrix}$:

$$
\mathbf{A} = \mathbf{X}\begin{bmatrix} 2 & 0 \\ 0 & 3\end{bmatrix}\mathbf{X}^{-1} = \begin{bmatrix} 2 & 3 \\ 0 & 3\end{bmatrix}\begin{bmatrix} 1 & -1 \\ 0 & 1\end{bmatrix} = \begin{bmatrix} 2 & \mathbf{1} \\ 0 & \mathbf{3}\end{bmatrix} .
$$

*Check:* $\mathbf{A}(1, 1) = (3, 3) = 3(1, 1)$ ✓.

### Solution 02-08.5

Expand along row 1: $\det(\mathbf{A} - \lambda\mathbf{I}) = (2 - \lambda)\big[(3 - \lambda)^2 - 1\big] = (2 - \lambda)(2 - \lambda)(4 - \lambda)$. So λ = **2** (twice) and **4**. *Checks:* trace $2 + 3 + 3 = $ **8** $= 2 + 2 + 4$ ✓ and determinant $2(9 - 1) = $ **16** $= 2\cdot2\cdot4$ ✓.

- λ = 4: $\mathbf{A} - 4\mathbf{I} = \begin{bmatrix} -2 & 0 & 0 \\ 1 & -1 & 1 \\ 1 & 1 & -1\end{bmatrix}$ forces $x_1 = 0$ and $x_2 = x_3$, giving $(0, 1, 1)$.
- λ = 2: $\mathbf{A} - 2\mathbf{I} = \begin{bmatrix} 0 & 0 & 0 \\ 1 & 1 & 1 \\ 1 & 1 & 1\end{bmatrix}$ has rank 1, so its null space has dimension **2**, spanned for example by $(-1, 1, 0)$ and $(-1, 0, 1)$.

That makes three independent eigenvectors in all, so **yes**, the matrix is diagonalizable, even though an eigenvalue repeats.

### Solution 02-08.6

λ = 3 is repeated, and $\mathbf{A} - 3\mathbf{I} = \begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}$ has rank 1, so its null space is one-dimensional, spanned by $(1, 0)$. A second independent eigenvector is missing: $\mathbf{A}$ is defective.

Write $\mathbf{A} = 3\mathbf{I} + \mathbf{N}$ with $\mathbf{N} = \begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}$. Since $\mathbf{N}^2 = \mathbf{0}$ and $\mathbf{I}$ commutes with $\mathbf{N}$, the binomial theorem stops after two terms: $\mathbf{A}^k = 3^k\mathbf{I} + k\,3^{k-1}\mathbf{N}$. So

$$
\mathbf{A}^4 = \begin{bmatrix} 81 & \mathbf{108} \\ 0 & 81\end{bmatrix}, \qquad 108 = 4\cdot3^3\ ✓.
$$

The factor $k$ multiplying $3^k$ is the discrete version of the $t\,e^{st}$ term of a critically damped circuit (02-03). There, too, a repeated characteristic root comes with only one exponential solution, and the second solution acquires a factor $t$.

### Solution 02-08.7

(a) Each column sums to 1 ✓. The trace is 1.25 and the determinant is $0.375 - 0.125 = 0.25$, so $\lambda^2 - 1.25\lambda + 0.25 = (\lambda - 1)(\lambda - 0.25) = 0$: λ = 1 and **0.25**. For λ = 1, $(\mathbf{P} - \mathbf{I})\boldsymbol{\pi} = \mathbf{0}$ gives $-0.5\pi_1 + 0.25\pi_2 = 0$, so $\pi_2 = 2\pi_1$. Normalized: $\boldsymbol{\pi} = (\tfrac13, \tfrac23)$, about (**0.3333**, 0.6667). For λ = 0.25 the eigenvector is $(1, -1)$ (its entries sum to 0, as they must for any eigenvalue other than 1).

(b) $\mathbf{u}_0 = (1, 0) = \boldsymbol{\pi} + \tfrac23(1, -1)$. Each piece evolves with its own eigenvalue, so

$$
\mathbf{u}_k = \left(\tfrac13, \tfrac23\right) + \tfrac23(0.25)^k(1, -1) .
$$

At $k = 10$, the deviation from steady state in each component is $\tfrac23(0.25)^{10} = $ **6.358×10⁻⁷**. The chain has essentially forgotten its start.

### Solution 02-08.8

(a) With $\mathbf{u}_k = (y[k], y[k - 1])$,

$$
\mathbf{u}_{k+1} = \begin{bmatrix} 1.2 & -0.8 \\ 1 & 0\end{bmatrix}\mathbf{u}_k, \qquad \lambda^2 - 1.2\lambda + 0.8 = 0, \qquad \lambda = 0.6 \pm j\,\mathbf{0.6633} .
$$

(b) $\lvert\lambda\rvert = \sqrt{0.8} = $ **0.8944** < 1, so the recurrence is stable: every solution decays. (For a complex pair, the product $\lvert\lambda\rvert^2$ equals the determinant, 0.8.) The angle is $\arctan(0.6633/0.6) = $ **47.87°** per sample, so one oscillation takes $360/47.87 = $ **7.520** samples, a decaying ringing. This is the state-space view of a two-pole digital resonator; its poles are these eigenvalues ([11-09](../../11-signals-and-systems/chapters/11-09-z-transform.md)).

### Solution 02-08.9

(a) The trace is 4 and the determinant is 3, so λ = **3** and **1**. The eigenvectors are $(1, 1)$ for 3 and $(-1, 1)$ for 1. Normalized:

$$
\mathbf{Q} = \frac{1}{\sqrt2}\begin{bmatrix} 1 & -1 \\ 1 & 1\end{bmatrix}, \quad \boldsymbol{\Lambda} = \begin{bmatrix} 3 & 0 \\ 0 & 1\end{bmatrix}, \quad \mathbf{Q}^\mathsf{T}\mathbf{Q} = \frac12\begin{bmatrix} 2 & 0 \\ 0 & 2\end{bmatrix} = \mathbf{I}\ ✓.
$$

(b) $\mathbf{S} = 3\cdot\tfrac12\begin{bmatrix} 1 & 1 \\ 1 & 1\end{bmatrix} + 1\cdot\tfrac12\begin{bmatrix} 1 & -1 \\ -1 & 1\end{bmatrix} = \begin{bmatrix} 2 & 1 \\ 1 & 2\end{bmatrix}$ ✓.

(c) $2x^2 + 2xy + 2y^2 = \mathbf{x}^\mathsf{T}\mathbf{S}\mathbf{x}$, so the ellipse has semi-axes $1/\sqrt{\lambda}$:

- along $(1, 1)$: $1/\sqrt3 = $ **0.5774**, the short axis;
- along $(-1, 1)$: $1/\sqrt1 = $ **1**, the long axis.

### Solution 02-08.10

(a) *Leading determinants:* $2 > 0$ and $2b - 1 > 0$. *Pivots:* the first pivot is 2 and the second is $b - \tfrac12$. Both tests give positive definiteness exactly when $b > $ **0.5**.

(b) The eigenvalues are $1 \pm 2$: **3** and **−1**. A negative eigenvalue means the matrix is not positive definite; it is *indefinite*. The eigenvector for −1 is $(1, -1)$, and indeed $\mathbf{x}^\mathsf{T}\mathbf{A}\mathbf{x} = 1 - 2 - 2 + 1 = $ **−2** < 0. Positive *entries* say nothing about positive *definiteness*. Here the off-diagonal coupling (2) is stronger than the diagonal (1), the opposite of a conductance matrix's diagonal dominance.

### Solution 02-08.11

The gradient is zero where $2x + y - 3 = 0$ and $x + 2y = 0$. So $x = -2y$, then $-3y = 3$, giving $y = $ **−1** and $x = $ **2**. The Hessian $\begin{bmatrix} 2 & 1 \\ 1 & 2\end{bmatrix}$ has eigenvalues 3 and 1, both positive, so it is positive definite and the point is a **minimum**. There $f = 4 - 2 + 1 - 6 = $ **−3**.

### Solution 02-08.12

(a) $\mathbf{A}^\mathsf{T}\mathbf{A} = \begin{bmatrix} 2 & 2 \\ 2 & 2\end{bmatrix}$, with eigenvalues 4 and 0. So $\sigma_1 = $ **2** and $\sigma_2 = 0$, and the rank is **1**. Here $\mathbf{v}_1 = \mathbf{u}_1 = \tfrac{1}{\sqrt2}(1, 1)$, and

$$
\mathbf{A} = 2\cdot\tfrac{1}{\sqrt2}(1, 1)\cdot\tfrac{1}{\sqrt2}(1, 1)^\mathsf{T},
$$

a single outer product.

(b) Singular values are never negative: they are **3** and **2**. The sign moves into $\mathbf{U}$: $\mathbf{U} = \begin{bmatrix} 1 & 0 \\ 0 & -1\end{bmatrix}$, $\boldsymbol{\Sigma} = \operatorname{diag}(3, 2)$, $\mathbf{V} = \mathbf{I}$. The condition number is $3/2 = $ **1.5**.

(c) All equal to **1**: $\mathbf{Q}^\mathsf{T}\mathbf{Q} = \mathbf{I}$ has every eigenvalue equal to 1. Geometrically, an orthogonal matrix maps the unit circle to the unit circle, stretching nothing. Its condition number is 1, the best possible, which is why orthogonal transformations are numerically safe.

### Solution 02-08.13

(a) $f_1 = 1/(2\pi\sqrt{4.7\text{ µH}\times220\text{ pF}}) = $ **4.949 MHz** (in phase). The out-of-phase mode sees $220 + 2\times22 = 264$ pF, so $f_2 = $ **4.518 MHz**. The split is **431.2 kHz**.

(b) Complete transfer takes half a beat period: $1/(2\times431.2\text{ kHz}) = $ **1.159 µs**.

(c) $f_1/f_2 = \sqrt{1 + 2C_c/C} = \sqrt{1.2} = 1.0954$, a fractional split of **0.09545**. For small $x$, $\sqrt{1 + 2x} \approx 1 + x$, so $f_1/f_2 - 1 \approx C_c/C = 0.1$. The approximation is about 5% high at this fairly strong coupling, and improves as $C_c/C$ shrinks.

### Solution 02-08.14

(a) $\mathbf{A}^\mathsf{T}\mathbf{A} = \begin{bmatrix} 14 & 27.8 \\ 27.8 & 55.22\end{bmatrix}$. Its eigenvalues are $\sigma_1^2$ and $\sigma_2^2$, so σ₁ = **8.320** and σ₂ = **0.05888**.

(b) The rank-1 approximation keeps $\sigma_1^2/(\sigma_1^2 + \sigma_2^2) = $ **99.995%** of $\lVert\mathbf{A}\rVert_F^2$. Its Frobenius error is $\sigma_2 = $ **0.05888**, against entries of size 2–6.

(c) The second column is almost exactly twice the first, $(4, 2.1, 5.9) \approx 2(2, 1, 3)$, with small deviations (0.1 and −0.1 in the last two rows). The data lie almost on a line through the origin: the two quantities are proportional, plus a little noise. The SVD finds that line (the first right singular vector is close to $(1, 2)/\sqrt5$) and measures the scatter about it. This is principal component analysis on a 3×2 data set.

### Solution 02-08.15

(a) The trace is 8 and the determinant is $16 - 5.76 = 10.24$, so $\lambda^2 - 8\lambda + 10.24 = 0$, giving λ = $4 \pm 2.4$: **6.4** and **1.6**. The eigenvectors are $\tfrac{1}{\sqrt2}(1, 1)$, the **common mode** (the average of the two sensors), and $\tfrac{1}{\sqrt2}(1, -1)$, the **differential mode** (their difference).

(b) The first component carries $6.4/8 = $ **80%** of the total variance. The standard deviations along the components are $\sqrt{6.4} = $ **2.530** (common mode) and $\sqrt{1.6} = $ **1.265** (differential mode).

(c) Project both signal and noise onto the unit differential direction $\mathbf{q}_2 = \tfrac{1}{\sqrt2}(1, -1)$. The signal $(s, -s)$ projects to $\sqrt2\,s$, and the noise along $\mathbf{q}_2$ has standard deviation $\sqrt{1.6} = 1.265$. One sensor alone sees signal $s$ with noise standard deviation 2. The amplitude signal-to-noise ratio therefore improves by

$$
\frac{\sqrt2\,s/1.265}{s/2} = \frac{2\sqrt2}{1.265} = \mathbf{2.236}\quad(\text{about 7 dB}).
$$

With *uncorrelated* noise, the noise along $\mathbf{q}_2$ would have the full standard deviation 2, and the gain would be only $\sqrt2 = $ **1.414**, from adding two looks at the signal. The rest, a factor of $2.236/1.414 = $ **1.581**, comes from the correlation. The common interference (pickup, supply ripple, drift) lives mostly in the common mode, and subtraction removes it. This is the eigenvector argument behind differential signaling and differential sensing ([12](../../12-electronics-2/README.md)).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-08.1a | larger eigenvalue | 6 | — |
| 02-08.1b | smaller eigenvalue | 1 | — |
| 02-08.1c | dot product of the eigenvectors | 0 | — |
| 02-08.2a | trace | 4 | — |
| 02-08.2b | determinant | −6 | — |
| 02-08.2c | largest eigenvalue of A + 2I | 5 | — |
| 02-08.3a | projection's larger eigenvalue | 1 | — |
| 02-08.3b | projection's other eigenvalue | 0 | — |
| 02-08.3c | reflection's negative eigenvalue | −1 | — |
| 02-08.3d | imaginary part of the rotation's eigenvalue | 1 | — |
| 02-08.4a | (1, 2) entry | 1 | — |
| 02-08.4b | (2, 2) entry | 3 | — |
| 02-08.5a | repeated eigenvalue | 2 | — |
| 02-08.5b | other eigenvalue | 4 | — |
| 02-08.5c | dimension of the λ = 2 eigenspace | 2 | — |
| 02-08.5d | trace | 8 | — |
| 02-08.5e | determinant | 16 | — |
| 02-08.6a | (1, 2) entry of A⁴ | 108 | — |
| 02-08.7a | second eigenvalue | 0.25 | — |
| 02-08.7b | steady-state probability of state 1 | 0.3333 | — |
| 02-08.7c | deviation at k = 10 | 6.358×10^-7 | — |
| 02-08.8a | imaginary part of the eigenvalues | 0.6633 | — |
| 02-08.8b | eigenvalue magnitude | 0.8944 | — |
| 02-08.8c | angle per sample | 47.87 | ° |
| 02-08.8d | samples per oscillation | 7.520 | — |
| 02-08.9a | larger eigenvalue | 3 | — |
| 02-08.9b | smaller eigenvalue | 1 | — |
| 02-08.9c | short semi-axis | 0.5774 | — |
| 02-08.9d | long semi-axis | 1 | — |
| 02-08.10a | threshold b | 0.5 | — |
| 02-08.10b | positive eigenvalue | 3 | — |
| 02-08.10c | negative eigenvalue | −1 | — |
| 02-08.10d | quadratic form at (1, −1) | −2 | — |
| 02-08.11a | x at the minimum | 2 | — |
| 02-08.11b | y at the minimum | −1 | — |
| 02-08.11c | minimum value | −3 | — |
| 02-08.12a | σ1 of the all-ones matrix | 2 | — |
| 02-08.12b | its rank | 1 | — |
| 02-08.12c | σ1 of diag(3, −2) | 3 | — |
| 02-08.12d | σ2 of diag(3, −2) | 2 | — |
| 02-08.12e | its condition number | 1.5 | — |
| 02-08.12f | singular values of an orthogonal matrix | 1 | — |
| 02-08.13a | in-phase frequency | 4.949 | MHz |
| 02-08.13b | out-of-phase frequency | 4.518 | MHz |
| 02-08.13c | split | 431.2 | kHz |
| 02-08.13d | complete-transfer time | 1.159 | µs |
| 02-08.13e | exact fractional split | 0.09545 | — |
| 02-08.14a | σ1 | 8.320 | — |
| 02-08.14b | σ2 | 0.05888 | — |
| 02-08.14c | captured fraction | 99.995 | % |
| 02-08.15a | larger eigenvalue | 6.4 | — |
| 02-08.15b | smaller eigenvalue | 1.6 | — |
| 02-08.15c | variance fraction of the first component | 80 | % |
| 02-08.15d | common-mode standard deviation | 2.530 | — |
| 02-08.15e | differential-mode standard deviation | 1.265 | — |
| 02-08.15f | SNR improvement with correlated noise | 2.236 | — |
| 02-08.15g | SNR improvement with uncorrelated noise | 1.414 | — |
| 02-08.15h | factor due to the correlation | 1.581 | — |
