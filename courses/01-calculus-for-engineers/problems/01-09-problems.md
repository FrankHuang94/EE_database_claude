# Problems 01-09 · Multivariable Calculus I: Partial Derivatives and Gradients

Chapter: [01-09](../chapters/01-09-multivariable-calculus-1.md) · Worked solutions: [01-09 solutions](../solutions/01-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $k = 1.380649\times10^{-23}$ J/K, $q = 1.602176634\times10^{-19}$ C, $E_g = 1.12$ eV for silicon; answers to 4 significant figures unless stated. State what is held constant for every partial derivative, and give its units.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-09.1 [A]

For $f(x, y) = x^2y + e^{xy}$:

(a) Find $f_x$ and $f_y$, and evaluate them at (1, 2).
(b) Find $f_{xy}$ and $f_{yx}$, confirm Clairaut's theorem, and evaluate the mixed partial at (1, 2).

### Problem 01-09.2 [A]

A resistor dissipates $P = V^2/R$. At $V = 10$ V and $R = 50\ \Omega$, find $\partial P/\partial V$ and $\partial P/\partial R$ with units. Which change raises $P$ more: +1 V or −1 Ω?

### Problem 01-09.3 [A]

For $f(x, y) = x^2 + xy + y^2$ at $(1, -1)$:

(a) Find $\nabla f$ and its magnitude.
(b) Find the directional derivative toward $(3, 4)$, i.e. along the unit vector $(3, 4)/5$.
(c) In which direction is the directional derivative zero?

### Problem 01-09.4 [A]

$z = x^2y$ with $x = \cos t$ and $y = \sin t$. Use the chain rule to find $dz/dt$ at $t = \pi/4$. Check by substituting first and differentiating.

### Problem 01-09.5 [B]

A PCB trace has resistance $R = \rho L/(wt)$, with $\rho = 1.72\times10^{-8}$ Ω·m (copper), length $L = 50$ mm ± 1%, width $w = 0.2$ mm ± 5% and thickness $t = 35$ µm ± 10%.

(a) Find the nominal resistance.
(b) Using the elasticities (each ±1 here), find the worst-case and RSS relative tolerance of $R$.
(c) Which parameter should be controlled first?

### Problem 01-09.6 [B]

A MOSFET has $k = 4$ mA/V², $V_{TH} = 0.4$ V and $V_A = 6$ V, biased at $V_{GS} = 0.7$ V and $V_{DS} = 0.9$ V.

(a) Find $I_D$, $g_m$, $g_o$ and $r_o$.
(b) Find the intrinsic gain $g_mr_o$.
(c) Verify the shortcut $g_m = 2I_D/(V_{GS} - V_{TH})$.

### Problem 01-09.7 [B]

(a) Repeat chapter Example 01-09.3 for a junction at $V = 0.600$ V and $T = 350$ K (a hot chip, at a different bias current).
(b) Using implicit differentiation, find $dy/dx$ for $x^3 + y^3 = 9$ at (1, 2).

### Problem 01-09.8 [B]

Find and classify the critical points of $f(x, y) = x^3 - 3x + y^2 - 2y$, and give $f$ at each.

### Problem 01-09.9 [B]

**Least squares.** Fit $y = a + bx$ to the points (0, 1), (1, 3), (2, 4), (3, 6).

(a) Solve the normal equations for $a$ and $b$.
(b) Find the sum of squared residuals.
(c) Show that the Hessian of $S(a, b)$ is positive definite, so this is a minimum.
(d) If $x$ were a market index's return and $y$ a stock's, what would $b$ be called?

### Problem 01-09.10 [B]

**Conditioning in gradient descent.** Minimize $f(x, y) = x^2 + 10y^2$ from (1, 1).

(a) Show that gradient descent multiplies $x$ by $(1 - 2\eta)$ and $y$ by $(1 - 20\eta)$ each step.
(b) For which step sizes does it converge?
(c) With η = 0.04, find $(x, y)$ and $f$ after three steps.
(d) What is the condition number (ratio of curvatures)? Why does it make the $x$ coordinate converge slowly?

### Problem 01-09.11 [B]

(a) Use a Lagrange multiplier to find the rectangle of largest area with perimeter 20.
(b) Find λ and verify that it equals $dA^\ast/dP$, the marginal area per unit of perimeter.

### Problem 01-09.12 [C]

**Water-filling.** Two channels have noise powers $N_1 = 1$ mW and $N_2 = 3$ mW. Total transmit power is $P$, split as $P_1 + P_2 = P$. Capacity (in b/s/Hz) is $C = \log_2(1 + P_1/N_1) + \log_2(1 + P_2/N_2)$.

(a) Show with a Lagrange multiplier that the optimum has $P_i + N_i = \mu$, the same for both channels.
(b) For $P = 6$ mW, find $P_1$, $P_2$, μ and $C$. Compare with an equal split.
(c) For $P = 1$ mW, the formula gives a negative $P_2$. What is the correct allocation, and the capacity?

### Problem 01-09.13 [C]

**Three heterogeneous cores.** Throughput $F = 3.4$ GHz must be split among three cores with $P_i = k_if_i^3$ and $k = 0.1$, 0.4 and 0.9 W/GHz³.

(a) Show that the optimum has $f_i \propto 1/\sqrt{k_i}$.
(b) Find each $f_i$, the total power and λ.
(c) Explain why no core is switched off entirely, and what would change if each core also had a fixed idle power when on.

### Problem 01-09.14 [C]

**The bandgap reference.** A circuit outputs $V_{out} = V_{BE} + K\,V_T$, where $V_{BE}$ is a junction voltage at constant current (tempco from Example 01-09.3) and $V_T = kT/q$.

(a) Find $dV_T/dT$.
(b) At 300 K with $V_{BE} = 0.6548$ V, find the value of $K$ that makes $dV_{out}/dT = 0$.
(c) Find $V_{out}$, and show that it equals $E_g/q + 3kT/q$ exactly, whatever the bias. Why is this circuit called a "bandgap" reference?

### Problem 01-09.15 [C]

**Fitting a power model with two parameters.** A chip's measured power at three supply voltages is 0.40 W at 0.6 V, 0.70 W at 0.8 V and 1.05 W at 1.0 V (synthetic data). Model $P = aV^2 + b$, with $aV^2$ the dynamic power at fixed frequency and $b$ the static (leakage) power, treated as constant.

(a) This is linear in the unknowns $a$ and $b$. Set up and solve the least-squares problem.
(b) Find the residual sum of squares.
(c) What fraction of the power at 0.8 V is leakage according to the fit? Why should you distrust a leakage estimate from three points taken at fixed temperature over a narrow voltage range?

---

## Objective coverage

| Learning objective (chapter 01-09) | Problems |
|---|---|
| 1. Partial derivatives as sensitivities | 1, 2, 6 |
| 2. Linearization, small-signal models, tolerances | 5, 6 |
| 3. Chain rule and implicit differentiation; tempco | 4, 7, 14 |
| 4. Gradient, directional derivative, gradient descent | 3, 10 |
| 5. Critical points, least squares, Lagrange multipliers | 8, 9, 11, 12, 13, 15 |
