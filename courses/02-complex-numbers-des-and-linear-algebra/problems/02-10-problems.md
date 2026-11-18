# Problems 02-10 · Numerical Methods for Engineers

Chapter: [02-10](../chapters/02-10-numerical-methods.md) · Worked solutions: [02-10 solutions](../solutions/02-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** "double" means IEEE 754 binary64 and "single" binary32. Answers to 4 significant figures unless exact. Where a computed floating-point result is asked for, run it (Python, NumPy) and compare with your prediction.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-10.1 [A]

Give machine epsilon (the gap between 1 and the next representable number) for double ($p = 52$ fraction bits), single ($p = 23$) and half precision ($p = 10$). About how many significant decimal digits does each carry? (Use $-\log_{10}$ of the unit roundoff, $\epsilon/2$.)

### Problem 02-10.2 [A]

(a) Which of 0.5, 0.375 and 0.1 are exactly representable in binary floating point? Why?
(b) Summing 0.1 ten times gives 0.9999999999999999 in double. Predict, then check, the result in single precision, and its error.

### Problem 02-10.3 [A]

Bisection starts with a bracket of length 1. How many steps does it need to locate a root to within $10^{-6}$?

### Problem 02-10.4 [A]

Apply Newton's method to $f(x) = x^2 - 2$ from $x_0 = 1$. Show that the iteration is $x_{k+1} = \tfrac12(x_k + 2/x_k)$, compute $x_1$ to $x_3$, and show that the error is roughly squared each step.

### Problem 02-10.5 [B]

**Two cancellation traps.**

(a) Evaluate $e^x - 1$ at $x = 10^{-10}$ directly and with the library function `expm1`. What is the relative error of the direct formula, and why?
(b) The variance of three readings $10^8 + 1$, $10^8 + 2$ and $10^8 + 3$ is $2/3$ (population variance). Compute it as $\overline{x^2} - \bar{x}^2$ and as $\overline{(x - \bar{x})^2}$ in double. Explain the difference, and say which formula a data logger should use.

### Problem 02-10.6 [B]

Solve $x = \cos x$ (a) by Newton's method on $f(x) = x - \cos x$ from $x_0 = 1$, and (b) by the fixed-point iteration $x_{k+1} = \cos x_k$. Count the iterations each needs to reach $10^{-10}$ accuracy, and explain the fixed-point iteration's rate from $\lvert f'\rvert$ of the map at the root.

### Problem 02-10.7 [B]

Use Newton's method for systems to solve $x^2 + y^2 = 4$, $xy = 1$, starting from $(2, 0.5)$. Write the Jacobian, take one step by hand, and give the converged root. Check it against the exact solution.

### Problem 02-10.8 [B]

Take one step of size $h = 0.1$ for $y' = -2y$, $y(0) = 1$, with forward Euler, Heun's method and RK4. Compare each with the exact $e^{-0.2}$.

### Problem 02-10.9 [B]

An RC circuit has τ = 10 µs.

(a) What is the largest stable forward-Euler step?
(b) Find the amplification factors of forward Euler, backward Euler and trapezoidal at $h = 30$ µs. Which are stable, and which oscillate?

### Problem 02-10.10 [B]

**A capacitor's companion model.** A 1 µF capacitor discharges through 100 Ω from 2 V.

(a) Write the backward-Euler companion model for a step $h = 10$ µs: the conductance and the current source.
(b) Take one step, by solving the resulting resistive circuit, and compare with the exact value.

### Problem 02-10.11 [B]

For the least-squares problem with columns $(1, 1, 1)$ and $(1, 1.01, 1.02)$, compute $\kappa(\mathbf{A})$ and $\kappa(\mathbf{A}^\mathsf{T}\mathbf{A})$. How many digits might the normal equations lose that a QR or SVD solve would not?

### Problem 02-10.12 [B]

In single precision, what is the spacing between adjacent representable numbers near $10^8$? What is $10^8 + 1$ in single precision? Explain the consequence for a single-precision accumulator that adds 1 to a running count.

### Problem 02-10.13 [C]

**Newton at a double root.** Apply Newton's method to $f(x) = (x - 1)^2$ from $x_0 = 2$.

(a) Show that the error halves each step: linear, not quadratic, convergence. How many steps are needed to reach $10^{-6}$?
(b) Show that the modified iteration $x_{k+1} = x_k - 2f(x_k)/f'(x_k)$ converges in one step, and explain why multiplicity matters.

### Problem 02-10.14 [C]

**The cost of stiffness.** A circuit has a 1 ps parasitic time constant and must be simulated for 10 µs.

(a) How many forward-Euler steps does stability require?
(b) An implicit method needs a step of about 10 ns for accuracy on the slow dynamics. How many steps is that, and by what factor does it beat Euler?
(c) What does each implicit step cost that an explicit step does not?

### Problem 02-10.15 [C]

**Mixed-precision iterative refinement.** A system with $\kappa = 10^3$ is factored in low precision and refined in double. Each refinement pass multiplies the error by about $\kappa u_{\text{low}}$.

(a) Find that factor for half precision ($u = 2^{-11}$) and for single precision ($u = 2^{-24}$).
(b) Starting from an error of about $\kappa u_{\text{low}}$, about how many passes does each need to reach $10^{-16}$?
(c) Above what κ does half-precision refinement stop converging at all?

---

## Objective coverage

| Learning objective (chapter 02-10) | Problems |
|---|---|
| 1. Floating point, machine epsilon, cancellation, low precision | 1, 2, 5, 12 |
| 2. Bisection and Newton–Raphson; convergence and failure | 3, 4, 6, 7, 13 |
| 3. SPICE's Newton iteration and companion models | 7, 10 |
| 4. ODE integrators and their order | 8, 10 |
| 5. Stability regions, stiffness, implicit methods | 9, 14 |
| 6. Conditioning and mixed precision | 11, 15 |
