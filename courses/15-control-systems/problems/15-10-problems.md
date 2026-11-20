# Problems 15-10 · State-Space Introduction

Chapter: [15-10](../chapters/15-10-state-space-introduction.md) · Worked solutions: [15-10 solutions](../solutions/15-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $u = -K\mathbf{x} + Nr$ for state feedback; observers $\dot{\hat{\mathbf{x}}} = A\hat{\mathbf{x}} + Bu + L(y - C\hat{\mathbf{x}})$. Single input and single output unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 15-10.1 [A]

**From a mechanism to state space.** A 1 kg mass on a spring of 2 N/m with damping 3 N·s/m is pushed by a force $u$. With states position and velocity, write $A$, $B$ and $C$ (output: position), and find the transfer function and the eigenvalues.

### Problem 15-10.2 [A]

**Which mode is uncontrollable?** For $A = \operatorname{diag}(-1, -2)$, test controllability with (a) $B = [1,\ 0]^T$ and (b) $B = [1,\ 1]^T$. Name any uncontrollable mode.

### Problem 15-10.3 [A]

**Which mode is unobservable?** For the same $A$, test observability with (a) $C = [1,\ 0]$ and (b) $C = [1,\ 1]$.

### Problem 15-10.4 [B]

**Pole placement.** For $\dot x_1 = x_2$, $\dot x_2 = -2x_2 + u$ (plant $1/[s(s + 2)]$), place the closed-loop poles at $-4 \pm j4$. Find $K$, $N$ and the step overshoot.

### Problem 15-10.5 [B]

**Ackermann outside canonical form.** For $A = \begin{bmatrix} -1 & 1 \\ 0 & -2 \end{bmatrix}$, $B = [0,\ 1]^T$, find $K$ that places the poles at −3 and −4, and verify by computing the characteristic polynomial of $A - BK$.

### Problem 15-10.6 [B]

**An observer.** For Problem 15-10.4's plant with $C = [1,\ 0]$, find $L$ that places both observer poles at −20.

### Problem 15-10.7 [B]

**The double integrator.** For $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = [0,\ 1]^T$: find $e^{At}$; the state at $t$ = 2 s from $\mathbf{x}(0) = [0,\ 1]^T$ with $u = 0$; and with a unit-step input $u = 1$.

### Problem 15-10.8 [C]

**Nearly uncontrollable.** Two RC circuits driven in parallel have time constants 1 ms and $\tau_2$. With time measured in milliseconds, find the singular values and condition number of the controllability matrix for $\tau_2$ = 1.1 ms and 1.01 ms. What does the trend mean for the input needed to set the two voltages independently? (The singular values of a matrix $M$ are the square roots of the eigenvalues of $M^TM$; the condition number is the largest divided by the smallest, a measure of how close $M$ is to losing rank; see 02-10 for its role in solving linear systems.)

### Problem 15-10.9 [C]

**Integral action for a speed loop.** The motor $\Omega/V = 50/(0.025s + 1)$ is written $\dot x = -40x + 2000u$. Augment it with $\dot x_i = r - x$ and place the poles at $-100 \pm j100$. Find the gains, interpret them as a PI controller, and find the step overshoot.

### Problem 15-10.10 [C]

**Separation in numbers.** Combine Problem 15-10.4's $K$ with Problem 15-10.6's $L$, and find the eigenvalues of the four-state closed loop.

### Problem 15-10.11 [B]

**Coordinates do not matter.** Transform Problem 15-10.1's model with $\mathbf{x} = T\mathbf{z}$, $T = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$. Find the new matrices and show that the transfer function is unchanged.

### Problem 15-10.12 [A]

**Counting states.** How many states does each need? (a) A buck converter's power stage with one inductor and one output capacitor. (b) A DC motor with winding inductance driving a load inertia through a flexible shaft.

---

## Objective coverage

| Learning objective (chapter 15-10) | Problems |
|---|---|
| 1. Models, solutions and coordinates | 1, 7, 11, 12 |
| 2. Controllability and observability | 2, 3, 8 |
| 3. Pole placement and reference scaling | 4, 5 |
| 4. Observers and separation | 6, 10 |
| 5. Integral action and links to PID | 9 |
