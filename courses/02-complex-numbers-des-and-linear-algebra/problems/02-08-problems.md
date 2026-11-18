# Problems 02-08 · Eigenvalues and Eigenvectors

Chapter: [02-08](../chapters/02-08-eigenvalues-and-eigenvectors.md) · Worked solutions: [02-08 solutions](../solutions/02-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** answers to 4 significant figures unless exact. Markov matrices use the column convention ($\mathbf{u}_{k+1} = \mathbf{P}\mathbf{u}_k$, columns summing to 1). Check every eigenpair by multiplying $\mathbf{A}\mathbf{x}$, and every set of eigenvalues against the trace and the determinant.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-08.1 [A]

Find the eigenvalues and eigenvectors of $\mathbf{A} = \begin{bmatrix} 5 & 2 \\ 2 & 2\end{bmatrix}$. Check them with the trace and determinant, and verify that the eigenvectors are orthogonal. Why must they be?

### Problem 02-08.2 [A]

For $\mathbf{A} = \begin{bmatrix} 3 & 1 & 4 \\ 0 & -1 & 5 \\ 0 & 0 & 2\end{bmatrix}$, write down the eigenvalues without calculation, and check them against the trace and the determinant. Then give the eigenvalues of $\mathbf{A}^2$, $\mathbf{A}^{-1}$ and $\mathbf{A} + 2\mathbf{I}$.

### Problem 02-08.3 [A]

Without computing a characteristic polynomial, find the eigenvalues and eigenvectors of each of these 2×2 matrices from its geometric meaning:

(a) $\mathbf{P}$, the projection onto the line through $(1, 1)$;
(b) the reflection across that line;
(c) the rotation by 90°.

Check each against its trace and determinant.

### Problem 02-08.4 [A]

Find the matrix with eigenvalue 2 for eigenvector $(1, 0)$ and eigenvalue 3 for eigenvector $(1, 1)$.

### Problem 02-08.5 [B]

Find the eigenvalues and eigenvectors of $\mathbf{A} = \begin{bmatrix} 2 & 0 & 0 \\ 1 & 3 & 1 \\ 1 & 1 & 3\end{bmatrix}$. It has a repeated eigenvalue. Is it diagonalizable?

### Problem 02-08.6 [B]

**A defective matrix.** Show that $\mathbf{A} = \begin{bmatrix} 3 & 1 \\ 0 & 3\end{bmatrix}$ has only one independent eigenvector. Compute $\mathbf{A}^4$, and show that its $(1, 2)$ entry is $k\,3^{k-1}$ with $k = 4$. Relate this to the critically damped response of 02-03.

### Problem 02-08.7 [B]

**A two-state Markov chain.** $\mathbf{P} = \begin{bmatrix} 0.5 & 0.25 \\ 0.5 & 0.75\end{bmatrix}$.

(a) Find the eigenvalues and the steady-state distribution.
(b) Starting from $\mathbf{u}_0 = (1, 0)$, write $\mathbf{u}_k$ in closed form, and find how far $\mathbf{u}_{10}$ is from the steady state.

### Problem 02-08.8 [B]

**Is this digital filter stable?** The recurrence $y[k] = 1.2\,y[k - 1] - 0.8\,y[k - 2]$ is written as $\mathbf{u}_{k+1} = \mathbf{A}\mathbf{u}_k$ with $\mathbf{u}_k = (y[k], y[k - 1])$.

(a) Find $\mathbf{A}$ and its eigenvalues.
(b) Is the recurrence stable? Find the magnitude and angle of the eigenvalues, and the number of samples per oscillation.

### Problem 02-08.9 [B]

For the symmetric matrix $\mathbf{S} = \begin{bmatrix} 2 & 1 \\ 1 & 2\end{bmatrix}$:

(a) find $\mathbf{Q}$ and $\boldsymbol{\Lambda}$ with $\mathbf{S} = \mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^\mathsf{T}$, and check that $\mathbf{Q}^\mathsf{T}\mathbf{Q} = \mathbf{I}$;
(b) write $\mathbf{S}$ as a weighted sum of two rank-1 projections;
(c) find the semi-axes of the ellipse $2x^2 + 2xy + 2y^2 = 1$, and their directions.

### Problem 02-08.10 [B]

(a) For which $b$ is $\begin{bmatrix} 2 & -1 \\ -1 & b\end{bmatrix}$ positive definite? Use two different tests.
(b) Show that $\begin{bmatrix} 1 & 2 \\ 2 & 1\end{bmatrix}$ is not positive definite, although all its entries are positive. Find a vector $\mathbf{x}$ with $\mathbf{x}^\mathsf{T}\mathbf{A}\mathbf{x} < 0$.

### Problem 02-08.11 [B]

Find the critical point of $f(x, y) = x^2 + xy + y^2 - 3x$, and decide whether it is a minimum, a maximum or a saddle by examining the Hessian's eigenvalues. Give the value of $f$ there.

### Problem 02-08.12 [B]

(a) Find the SVD of $\begin{bmatrix} 1 & 1 \\ 1 & 1\end{bmatrix}$ and its rank.
(b) Find the singular values of $\begin{bmatrix} 3 & 0 \\ 0 & -2\end{bmatrix}$ and its condition number. Where does the minus sign go?
(c) What are the singular values of any orthogonal matrix, and why?

### Problem 02-08.13 [B]

**Coupled tanks.** Two resonators, each $L = 4.7$ µH in parallel with $C = 220$ pF to ground, are coupled by $C_c = 22$ pF.

(a) Find the two normal-mode frequencies and the split.
(b) Resonator 1 is set ringing and resonator 2 starts at rest (both inductor currents zero). How long until the energy has moved (almost) completely to resonator 2?
(c) Define the fractional split as $f_1/f_2 - 1$. For small coupling, show that it is approximately $C_c/C$, and find how good the approximation is here.

### Problem 02-08.14 [C]

**Nearly rank 1.** Three measurements of two quantities give the data matrix

$$
\mathbf{A} = \begin{bmatrix} 2 & 4 \\ 1 & 2.1 \\ 3 & 5.9\end{bmatrix} .
$$

(a) Find its singular values.
(b) What fraction of $\lVert\mathbf{A}\rVert_F^2$ does the best rank-1 approximation capture, and what is the error in the Frobenius norm?
(c) Interpret: what physical relationship between the two columns does the near-rank-1 structure reveal?

### Problem 02-08.15 [C]

**Principal components of two sensors.** Two nearby sensors each have noise with standard deviation 2 (in some unit), and their noises have correlation 0.6. Their covariance matrix is $\begin{bmatrix} 4 & 2.4 \\ 2.4 & 4\end{bmatrix}$.

(a) Find its eigenvalues and eigenvectors, and interpret the eigenvectors as common-mode and differential-mode combinations.
(b) What fraction of the total variance lies in the first principal component? What are the standard deviations along each component?
(c) The wanted signal appears with opposite signs on the two sensors ($+s$ on sensor 1 and $-s$ on sensor 2). By what factor does the differential combination improve the amplitude signal-to-noise ratio over a single sensor? How much of that gain comes from the noise correlation?

### Problem 02-08.16 [B]

**MIMO streams from the SVD.** A 2×2 link has the real channel matrix $\mathbf{H} = \begin{bmatrix}2 & 1\\ 1 & 2\end{bmatrix}$ and white receiver noise of power $N$ per antenna. The transmitter has total power $P$, with $P/N = 10$ (10 dB).

(a) Find the singular values and the singular vectors of $\mathbf{H}$, and describe the two parallel channels the SVD creates.
(b) Split the power equally between the two streams. Find each stream's SNR, $(P/2)\sigma_i^2/N$, in dB.
(c) Find the total capacity $\sum_i\log_2\big(1 + (P/2)\sigma_i^2/N\big)$ in bit/s/Hz, and compare it with sending all the power on the strong stream alone.

### Problem 02-08.17 [B]

**Similar matrices.** Two matrices are **similar** if $\mathbf{B} = \mathbf{M}^{-1}\mathbf{A}\mathbf{M}$ for some invertible $\mathbf{M}$: the same linear map written in a different basis.

(a) Show that similar matrices have the same characteristic polynomial, and so the same eigenvalues, trace and determinant. How are their eigenvectors related?
(b) With $\mathbf{A} = \begin{bmatrix}4 & 1\\ 2 & 3\end{bmatrix}$ and $\mathbf{M} = \begin{bmatrix}1 & 1\\ 0 & 1\end{bmatrix}$, compute $\mathbf{B}$ and check (a).
(c) Diagonalization is a similarity transformation. Which $\mathbf{M}$ makes $\mathbf{M}^{-1}\mathbf{A}\mathbf{M}$ diagonal?

---

## Objective coverage

| Learning objective (chapter 02-08) | Problems |
|---|---|
| 1. Eigenvalues, eigenvectors and their geometry | 1, 2, 3, 4 |
| 2. Trace/determinant checks, powers and inverses, diagonalization | 2, 4, 5, 6, 17 |
| 3. Powers, recurrences, Markov chains, stability | 6, 7, 8 |
| 4. Complex eigenvalues as rotation and poles | 3, 8 |
| 5. Symmetric matrices, the spectral theorem, positive definiteness | 1, 9, 10, 11, 15 |
| 6. The SVD, rank, low-rank approximation, conditioning, MIMO channels | 12, 14, 15, 16 |
| Application: coupled resonators and normal modes | 13 |
