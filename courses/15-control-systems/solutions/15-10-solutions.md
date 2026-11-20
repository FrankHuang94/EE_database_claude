# Solutions 15-10 · State-Space Introduction

Problems: [15-10 problems](../problems/15-10-problems.md) · Chapter: [15-10](../chapters/15-10-state-space-introduction.md)

Every number below is recomputed by [verify_15_10.py](../verify/verify_15_10.py): ranks and singular values with numpy, gains with Ackermann's formula and checked by the resulting eigenvalues, and responses by the matrix exponential.

---

## Solutions

### Solution 15-10.1

$m\ddot x = u - 3\dot x - 2x$ gives $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = [0,\ 1]^T$, $C = [1,\ 0]$. Then $G(s) = 1/(s^2 + 3s + 2)$ and the eigenvalues are **−1** and **−2** s⁻¹ (the matrix of Example 15-10.2).

### Solution 15-10.2

**(a)** $[B,\ AB] = \begin{bmatrix} 1 & -1 \\ 0 & 0 \end{bmatrix}$: rank **1**. The input never reaches $x_2$, so the mode at **−2** is uncontrollable (it is stable, so the system is stabilizable).

**(b)** $[B,\ AB] = \begin{bmatrix} 1 & -1 \\ 1 & -2 \end{bmatrix}$, determinant −1: rank **2**, controllable. Distinct eigenvalues and an input that touches every mode make it controllable.

### Solution 15-10.3

**(a)** $\mathcal{O} = \begin{bmatrix} 1 & 0 \\ -1 & 0 \end{bmatrix}$: rank **1**; the mode at −2 never appears in the output.

**(b)** $\mathcal{O} = \begin{bmatrix} 1 & 1 \\ -1 & -2 \end{bmatrix}$: rank **2**, observable.

### Solution 15-10.4

In controllable canonical form ($a_0 = 0$, $a_1 = 2$) and with the desired $(s + 4)^2 + 16 = s^2 + 8s + 32$: $k_1$ = **32**, $k_2 = 8 - 2$ = **6**. Then $N = -1/[C(A - BK)^{-1}B]$ = **32**, and $T = 32/(s^2 + 8s + 32)$ has $\zeta = 8/(2\sqrt{32}) = 0.707$, so the overshoot is **4.32**%.

### Solution 15-10.5

$\mathcal{C} = [B,\ AB] = \begin{bmatrix} 0 & 1 \\ 1 & -2 \end{bmatrix}$ and $\phi(s) = (s + 3)(s + 4) = s^2 + 7s + 12$, so $\phi(A) = A^2 + 7A + 12I$. Ackermann's formula $K = [0\ \ 1]\mathcal{C}^{-1}\phi(A)$ gives $K$ = [**6**, **4**]. Check: $A - BK = \begin{bmatrix} -1 & 1 \\ -6 & -6 \end{bmatrix}$, whose characteristic polynomial is $s^2 + 7s + 6 + 6 = s^2 + 7s + 12$, roots −3 and −4.

### Solution 15-10.6

$A - LC = \begin{bmatrix} -l_1 & 1 \\ -l_2 & -2 \end{bmatrix}$ has characteristic polynomial $s^2 + (2 + l_1)s + (2l_1 + l_2)$. Matching $(s + 20)^2 = s^2 + 40s + 400$: $l_1$ = **38**, $l_2 = 400 - 76$ = **324**.

### Solution 15-10.7

$A^2 = 0$, so the series stops: $e^{At} = I + At = \begin{bmatrix} 1 & t \\ 0 & 1 \end{bmatrix}$. Free response at 2 s from $[0,\ 1]^T$: $\mathbf{x}$ = [**2**, **1**]$^T$ (constant velocity). With $u = 1$ the forced part adds $\int_0^2\begin{bmatrix} 2 - \tau \\ 1 \end{bmatrix}d\tau = [2,\ 2]^T$, so $\mathbf{x}(2)$ = [**4**, **3**]$^T$: position $t + t^2/2$, velocity $1 + t$.

### Solution 15-10.8

In millisecond units, $A = \operatorname{diag}(-1, -1/\tau_2)$ and $B = [1,\ 1/\tau_2]^T$.

- $\tau_2$ = 1.1 ms: singular values **1.873** and **0.0441**, condition number **42.4**.
- $\tau_2$ = 1.01 ms: singular values **1.985** and **0.00494**, condition number **402**.

The rank is 2 in both cases, so the system is technically controllable, but the smallest singular value shrinks in proportion to the mismatch. Setting the two voltages independently needs an input whose size grows roughly as the inverse of that singular value: tenfold more for a tenfold smaller mismatch. In practice such modes are "uncontrollable" with any reasonable actuator.

### Solution 15-10.9

The augmented closed loop has $A - BK = \begin{bmatrix} -40 - 2000k_1 & 2000k_i \\ -1 & 0 \end{bmatrix}$ with $u = -k_1x + k_ix_i$, characteristic polynomial $s^2 + (40 + 2000k_1)s + 2000k_i$. Matching $(s + 100)^2 + 100^2 = s^2 + 200s + 20{,}000$: $k_1$ = **0.08** V·s/rad and $k_i$ = **10** V/rad. As a PI controller: $K_i$ = 10 on the integral of the error and $K_p$ = 0.08 on the measured speed only. The poles have $\zeta$ = 0.707 and there is no reference zero, so the overshoot is **4.32**%.

### Solution 15-10.10

The closed-loop eigenvalues are **−4 ± j4** (from $A - BK$) and **−20** twice (from $A - LC$), as the separation principle predicts.

### Solution 15-10.11

$T^{-1} = \begin{bmatrix} 1 & -1 \\ 0 & 1 \end{bmatrix}$, so $T^{-1}AT = \begin{bmatrix} 2 & 6 \\ -2 & -5 \end{bmatrix}$, $T^{-1}B = [-1,\ 1]^T$ and $CT = [1,\ 1]$. The new matrices look different, but $C T (sI - T^{-1}AT)^{-1}T^{-1}B$ = $1/(s^2 + 3s + 2)$ again: the trace (−3) and determinant (2) of $T^{-1}AT$ are unchanged.

### Solution 15-10.12

**(a)** **2**: the inductor current and the capacitor voltage. **(b)** **4**: the winding current, the motor speed, the shaft twist (relative angle) and the load speed. The motor's absolute angle would add a fifth state only if it were an output of interest.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 15-10.1a | first eigenvalue | −1 | 1/s |
| 15-10.1b | second eigenvalue | −2 | 1/s |
| 15-10.2a | rank with B = [1, 0] | 1 | — |
| 15-10.2b | uncontrollable eigenvalue | −2 | 1/s |
| 15-10.2c | rank with B = [1, 1] | 2 | — |
| 15-10.3a | rank with C = [1, 0] | 1 | — |
| 15-10.3b | rank with C = [1, 1] | 2 | — |
| 15-10.4a | k1 | 32 | 1/s² |
| 15-10.4b | k2 | 6 | 1/s |
| 15-10.4c | N | 32 | 1/s² |
| 15-10.4d | overshoot | 4.32 | % |
| 15-10.5a | k1 | 6 | — |
| 15-10.5b | k2 | 4 | — |
| 15-10.6a | l1 | 38 | 1/s |
| 15-10.6b | l2 | 324 | 1/s² |
| 15-10.7a | free position at 2 s | 2 | — |
| 15-10.7b | free velocity at 2 s | 1 | — |
| 15-10.7c | forced position at 2 s | 4 | — |
| 15-10.7d | forced velocity at 2 s | 3 | — |
| 15-10.8a | larger singular value, 1.1 ms | 1.873 | — |
| 15-10.8b | smaller singular value, 1.1 ms | 0.0441 | — |
| 15-10.8c | condition number, 1.1 ms | 42.4 | — |
| 15-10.8d | smaller singular value, 1.01 ms | 0.00494 | — |
| 15-10.8e | condition number, 1.01 ms | 402 | — |
| 15-10.8f | larger singular value, 1.01 ms | 1.985 | — |
| 15-10.9a | k1 | 0.08 | V·s/rad |
| 15-10.9b | ki | 10 | V/rad |
| 15-10.9c | overshoot | 4.32 | % |
| 15-10.10a | controller poles | −4 + j4 | 1/s |
| 15-10.10b | observer poles | −20 | 1/s |
| 15-10.12a | states, buck power stage | 2 | — |
| 15-10.12b | states, motor with flexible shaft | 4 | — |
