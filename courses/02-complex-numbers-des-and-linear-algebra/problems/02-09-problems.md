# Problems 02-09 · Systems of Linear ODEs and the Matrix Exponential

Chapter: [02-09](../chapters/02-09-systems-of-odes-and-matrix-exponential.md) · Worked solutions: [02-09 solutions](../solutions/02-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** states are capacitor voltages and inductor currents unless stated; answers to 4 significant figures unless exact. Check every solution against its initial condition, and every steady state by setting $\mathbf{x}' = \mathbf{0}$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-09.1 [A]

A current source $i_s$ drives a parallel RLC: $R = 1$ kΩ, $L = 10$ mH and $C = 100$ nF, all from the same node to ground. With states $(v_C, i_L)$:

(a) write $\mathbf{A}$ and $\mathbf{B}$;
(b) find the trace, the determinant and the eigenvalues;
(c) find the DC steady state for a constant $i_s$, and explain it physically.

### Problem 02-09.2 [A]

Write $y''' + 6y'' + 11y' + 6y = u$ in companion form with $\mathbf{x} = (y, y', y'')$. Find the eigenvalues of $\mathbf{A}$ (hint: try small negative integers), and check them against the trace and the determinant.

### Problem 02-09.3 [A]

(a) Write $e^{\mathbf{A}t}$ for $\mathbf{A} = \operatorname{diag}(-1, -2)$.
(b) Compute $e^{\mathbf{N}t}$ for $\mathbf{N} = \begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}$ from the series, and check that it solves $\mathbf{x}' = \mathbf{N}\mathbf{x}$.
(c) Using $\det e^{\mathbf{A}t} = e^{\operatorname{tr}(\mathbf{A})t}$, find $\det e^{\mathbf{A}}$ for $\mathbf{A} = \begin{bmatrix} 1 & 2 \\ 3 & 4\end{bmatrix}$ without computing the exponential.

### Problem 02-09.4 [A]

Classify the equilibrium of a 2-state system with each (trace, determinant) pair, and say whether it is stable: (a) $(-3, 2)$; (b) $(1, 4)$; (c) $(0, -1)$; (d) $(-2, 1)$.

### Problem 02-09.5 [B]

Solve $\mathbf{x}' = \begin{bmatrix} 1 & 2 \\ 2 & 1\end{bmatrix}\mathbf{x}$ with $\mathbf{x}(0) = (1, 0)$, and evaluate $\mathbf{x}(1)$. Which initial conditions lead to solutions that decay?

### Problem 02-09.6 [B]

Solve $\mathbf{x}' = \begin{bmatrix} -1 & -4 \\ 1 & -1\end{bmatrix}\mathbf{x}$ with $\mathbf{x}(0) = (1, 0)$ twice: first with the complex-eigenvector construction of §3.2 (real and imaginary parts of $e^{\lambda t}\mathbf{v}$), then by computing $e^{\mathbf{A}t}$. (Hint: write $\mathbf{A} = -\mathbf{I} + \mathbf{K}$ and compute $\mathbf{K}^2$.) Evaluate $\mathbf{x}(0.5)$.

### Problem 02-09.7 [B]

Solve $\mathbf{x}' = \begin{bmatrix} -2 & 1 \\ 0 & -2\end{bmatrix}\mathbf{x}$ with $\mathbf{x}(0) = (0, 1)$, using the generalized-eigenvector construction of §3.2 (then check against $e^{\mathbf{A}t}$). When does $x_1$ peak, and what is its peak value?

### Problem 02-09.8 [B]

For $\mathbf{A} = \begin{bmatrix} 0 & 1 \\ -2 & -3\end{bmatrix}$, compute $(s\mathbf{I} - \mathbf{A})^{-1}$, invert each entry by partial fractions to get $e^{\mathbf{A}t}$, and evaluate its first row at $t = 1$.

### Problem 02-09.9 [B]

**A driven RC pair.** In the circuit of Example 02-09.2 (τ = 1), the resistor from node 1 to ground is reconnected from node 1 to a 1 V source, switched on at $t = 0$ with both capacitors uncharged.

(a) Show that $\mathbf{A}$ is unchanged, and find $\mathbf{B}$.
(b) Find the steady state, and check it with a voltage divider.
(c) Find $v_2(t)$ and evaluate it at $t = τ$.

### Problem 02-09.10 [B]

For the circuit of Problem 02-09.9 with output $v_2$, find $H(s) = \mathbf{C}(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B}$, its poles and DC gain, and $\lvert H\rvert$ at $\omega = 1/\tau$.

### Problem 02-09.11 [B]

(a) For which $k$ is $\begin{bmatrix} -1 & k \\ 1 & -2\end{bmatrix}$ stable?
(b) What kind of equilibrium does it have at $k = 2$, and at $k = 3$?

### Problem 02-09.12 [B]

**Sampling a single RC.** The scalar system $x' = -x/\tau + u/\tau$ with $\tau = 2$ ms is sampled at $T = 0.5$ ms with a zero-order hold.

(a) Find $a_d$ and $b_d$ exactly, and by forward Euler.
(b) Starting from $x = 1$ with $u = 0$, compare one exact step with one Euler step.
(c) What is the largest stable Euler step?

### Problem 02-09.13 [C]

**Coupled resonators in time.** Write the coupled resonators of Example 02-08.5 ($L = 1$ µH, $C = 1$ nF, $C_c = 0.1$ nF) as a 4-state system with $\mathbf{x} = (v_1, v_2, i_{L1}, i_{L2})$. Show that

$$
\mathbf{A} = \begin{bmatrix} \mathbf{0} & -\mathbf{C}_m^{-1} \\ \mathbf{I}/L & \mathbf{0}\end{bmatrix},
$$

where $\mathbf{C}_m$ is the capacitance matrix of 02-08 §3.8. Find the eigenvalues, and relate them to the mode frequencies of 02-08.

### Problem 02-09.14 [C]

**Using a datasheet Foster model.** A power MOSFET datasheet gives a Foster thermal model (illustrative values) with $R_1 = 0.2$ K/W, $\tau_1 = 1$ ms; $R_2 = 0.5$ K/W, $\tau_2 = 50$ ms; $R_3 = 1.3$ K/W, $\tau_3 = 2$ s.

(a) What is the steady-state junction-to-case thermal resistance?
(b) Find $Z_{th}$ for a single 10 ms pulse, and the junction temperature rise for a 50 W pulse of that length.
(c) What single-pulse power of 10 ms keeps the rise under 100 K? Compare with the continuous power for the same rise.

### Problem 02-09.15 [C]

**A state-space layer, as in sequence models.** A one-state continuous model $h' = ah + bx$ with $a = -1/\tau$ and $b = 1/\tau$ ($\tau = 50$ ms) is sampled with step $h = 1$ ms by a zero-order hold. (Sequence-model papers write this step as Δ.)

(a) Find $\bar{a} = e^{ah}$ and $\bar{b} = (e^{ah} - 1)\,b/a$, and compare with forward Euler.
(b) After an input impulse, how many steps until the state has decayed to 1%? How does that "memory length" scale with τ/h?
(c) Show that for a constant input the sampled model's step response equals the continuous one at every sample time.

### Problem 02-09.16 [B]

**Linearizing a latch.** A latch is modeled as in §3.8 with inverter gain $a = 2$ and τ = 20 ps: $\tau x_1' = -x_1 - \tanh(2x_2)$, $\tau x_2' = -x_2 - \tanh(2x_1)$.

(a) Find the Jacobian at the origin, classify the equilibrium, and give the growth and decay time constants with their eigenvector directions.
(b) A synchronizer gives the latch 200 ps to resolve its imbalance to 0.5 (normalized units). What is the smallest initial imbalance that resolves in time?
(c) Why does doubling the allowed time reduce the failure rate enormously rather than by half?

### Problem 02-09.17 [B]

**A forced response by convolution.** For $\mathbf{x}' = \begin{bmatrix} -1 & 0 \\ 1 & -2\end{bmatrix}\mathbf{x} + \begin{bmatrix} 1 \\ 0\end{bmatrix}u$ with $\mathbf{x}(0) = \mathbf{0}$ and the ramp input $u(t) = t$:

(a) Find $e^{\mathbf{A}t}$.
(b) Use the convolution formula $\mathbf{x}(t) = \int_0^te^{\mathbf{A}(t - \lambda)}\mathbf{B}\,u(\lambda)\,d\lambda$ to find $\mathbf{x}(t)$, and evaluate it at $t = 1$.
(c) Check $x_1$ by solving its scalar equation directly, and check that $x_2(0) = 0$.

---

## Objective coverage

| Learning objective (chapter 02-09) | Problems |
|---|---|
| 1. State-space form from circuits and ODEs | 1, 2, 9, 13 |
| 2. Eigenvector solutions: real, complex, repeated | 5, 6, 7 (complex and generalized eigenvectors) |
| 3. The matrix exponential | 3, 6, 8 |
| 4. Phase plane and stability; linearization at an equilibrium | 4, 5, 11, 16 |
| 5. Forced response, steady state, transfer function | 1, 9, 10, 14, 17 |
| 6. Sampling: zero-order hold versus Euler | 12, 15 |
