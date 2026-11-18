# Problems 02-05 · The Laplace Transform for ODEs

Chapter: [02-05](../chapters/02-05-laplace-transform-for-odes.md) · Worked solutions: [02-05 solutions](../solutions/02-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** unilateral transform with lower limit $0^-$; initial conditions at $0^-$; answers to 4 significant figures unless stated. Check every inverse transform against the initial conditions or with the initial-value theorem.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-05.1 [A]

From the definition, find the transform and its region of convergence: (a) $e^{-2t}$; (b) $t$; (c) $5u(t - 3)$.

### Problem 02-05.2 [A]

(a) Use integration by parts to show $\mathcal{L}\{t^n\} = \dfrac{n}{s}\mathcal{L}\{t^{n-1}\}$, and conclude that $\mathcal{L}\{t^n\} = n!/s^{n+1}$.
(b) Find $\mathcal{L}\{t^3\}$ and $\mathcal{L}\{t^2e^{-t}\}$.

### Problem 02-05.3 [A]

Use the table and properties to transform: (a) $2\cos5t - 3\sin5t$; (b) $e^{-3t}\sin4t$; (c) $(t - 2)\,u(t - 2)$.

### Problem 02-05.4 [A]

Invert, and evaluate each result at $t = 1$: (a) $\dfrac{6}{s(s + 3)}$; (b) $\dfrac{2s + 3}{s^2 + 9}$; (c) $\dfrac{1}{(s + 2)^3}$.

### Problem 02-05.5 [B]

**A repeated pole.** Invert $Y(s) = \dfrac{s + 4}{s^2(s + 2)}$ by partial fractions, and evaluate $y(1)$.

### Problem 02-05.6 [B]

**Complex poles.** Invert $Y(s) = \dfrac{3s + 7}{s^2 + 4s + 13}$ by completing the square, and evaluate $y(0.5)$. Check $y(0^+)$ with the initial-value theorem.

### Problem 02-05.7 [B]

Solve $y' + 4y = 8$ with $y(0) = 5$ by Laplace transform, and evaluate $y(0.25)$.

### Problem 02-05.8 [B]

Solve $y'' + 4y = \sin t$ with $y(0) = y'(0) = 0$, and evaluate $y(\pi/2)$. Which part of the solution is the steady state, and which the natural response?

### Problem 02-05.9 [B]

**A delayed step.** An RC low-pass with τ = 2 s, initially at 0 V, receives $10u(t - 1)$ V. Find $v(t)$ and evaluate $v(3)$.

### Problem 02-05.10 [B]

**An impulsive kick.** Solve $y'' + 2y' + 5y = 3\delta(t)$ with zero initial conditions (at $0^-$).

(a) Find $y(t)$.
(b) Show that the impulse is equivalent to the initial conditions $y(0^+) = 0$, $y'(0^+) = 3$.
(c) Find the time and value of the first peak.

### Problem 02-05.11 [B]

**Initial- and final-value theorems.**

(a) For $F(s) = \dfrac{2s + 3}{s(s + 1)(s + 3)}$, find $f(0^+)$ and $f(\infty)$.
(b) For $F(s) = \dfrac{4}{s(s^2 - s + 2)}$, explain why the final-value theorem cannot be used.
(c) Find the DC gain of $H(s) = \dfrac{10(s + 2)}{s^2 + 3s + 20}$, and the final value of its unit-step response.

### Problem 02-05.12 [B]

**Convolution.** Compute $e^{-t} * e^{-2t} = \int_0^te^{-\lambda}e^{-2(t - \lambda)}\,d\lambda$ directly, then check it with the convolution theorem. Evaluate it at $t = 1$.

### Problem 02-05.13 [C]

**A band-pass transfer function.** A series RLC with $R = 100$ Ω, $L = 10$ mH and $C = 1$ µF has its output taken across the resistor.

(a) Show that $H(s) = \dfrac{(R/L)\,s}{s^2 + (R/L)s + 1/(LC)}$, and find its poles, zero, ζ and $Q$.
(b) Find the unit-step response and its peak (time and value).
(c) Use the final-value theorem to explain the step response's final value physically.

### Problem 02-05.14 [C]

**The PDN droop by partial fractions.** For the power-delivery network of chapter Example 02-05.5, invert $\Delta V(s) = -\dfrac{\Delta I\,(R + sL)}{s\,(LCs^2 + RCs + 1)}$ by partial fractions. Show that the result has the form $-\Delta I\,R + e^{-\alpha t}(A\cos\omega_dt + B\sin\omega_dt)$, find $A$ and $B$, and confirm numerically the worst droop of 160.3 mV found in 02-03.

### Problem 02-05.15 [C]

**An imperfect pole-zero cancellation.** A compensator is meant to cancel a slow pole at $s = -1$ with a zero, giving $H = 1/(s + 10)$. Because of component tolerance, the zero lands at $-1.1$ instead: $H(s) = \dfrac{s + 1.1}{(s + 1)(s + 10)}$.

(a) Find the unit-step response by partial fractions.
(b) How large is the slow $e^{-t}$ term, as a percentage of the final value?
(c) How long does the response take to settle within 1% of its final value? Compare with perfect cancellation.

### Problem 02-05.16 [B]

**Piecewise, impulsive and periodic inputs.** The system is $y' + y = v(t)$ with $y(0^-) = 0$ (an RC filter with τ = 1 s; $t$ in seconds).

(a) Transform $t\,u(t - 2)$ correctly, showing the rewrite.
(b) The input is a ramp-and-hold: $v = t$ for $0 \le t < 1$ and $v = 1$ for $t \ge 1$. Write $v$ with unit steps, find $Y(s)$ and $y(t)$, and evaluate $y(2)$.
(c) Instead, the input is an impulse $0.5\,\delta(t - 1)$. Find $y(t)$ and $y(2)$.
(d) Find the transform of the square wave that equals 1 for the first half of each 2 s period and 0 for the second half, and evaluate it at $s = 1$.

### Problem 02-05.17 [B]

**Convolution and the other transform rules.**

(a) For $y'' + 3y' + 2y = g(t)$ with zero initial conditions, find the impulse response and write $y(t)$ as a convolution integral valid for any input $g$.
(b) Evaluate the integral for $g = 1$ and check it against a partial-fraction solution. Find $y(1)$.
(c) Use the same integral, or partial fractions, for $g = e^{-3t}$, and find $y(1)$.
(d) Use the multiplication-by-$t$ rule to find $\mathcal{L}\{t\sin2t\}$, and the integral rule to find $\mathcal{L}\{\int_0^t\sin2\lambda\,d\lambda\}$. Evaluate both at $s = 1$, and check the second by integrating first.

---

## Objective coverage

| Learning objective (chapter 02-05) | Problems |
|---|---|
| 1. Definition; transforms from the integral; convergence | 1, 2 |
| 2. Properties: derivative, shifts, multiplication by t, convolution | 2, 3, 9, 12, 16, 17 |
| 3. Inversion by partial fractions | 4, 5, 6, 14, 15 |
| 4. Solving IVPs, including switched and impulsive inputs | 7, 8, 9, 10, 16, 17 |
| 5. Initial- and final-value theorems | 6, 11, 13 |
| 6. Transfer functions, poles, zeros, impulse response | 10, 13, 14, 15 |
