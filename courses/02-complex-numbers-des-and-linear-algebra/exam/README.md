# Course 02 · Final Exam (Complex Numbers, Differential Equations and Linear Algebra)

**Time limit:** 180 minutes. **Allowed:** a scientific calculator (its complex-number mode is allowed), and the [Course 02 equation sheet](../../../reference/equation-sheets/02-complex-numbers-des-and-linear-algebra.md) printed without its chapter links. No notes, no Python.
**Instructions:** answer all 15 questions and show every step. Each [A] is worth 5 points, each [B] 8 and each [C] 12 (128 points in total; 90 or more, about 70%, is a strong pass). Give numerical answers to 4 significant figures unless told otherwise, with units. Question 15(c) is a short-answer diligence question graded against the rubric in the solutions. Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

Angles are in degrees unless stated otherwise. A phasor's magnitude is the peak amplitude, with the cosine as reference.

---

**1 [A] · Complex arithmetic.** Let $z_1 = 3 + j4$ and $z_2 = 1 - j$.
(a) Write $z_1$ in polar form. Find $z_1z_2$ and $z_1/z_2$ in rectangular form.
(b) Find all three solutions of $z^3 = 8j$ in rectangular form.
(c) Write $v(t) = 10\cos(\omega t + 30°) + 5\sin(\omega t)$ as a single sinusoid $V_m\cos(\omega t + \phi)$.

**2 [B] · Impedance and sinusoidal steady state.** A series circuit of $R = 100\ \Omega$, $L = 0.1$ H and $C = 20$ µF is driven by $v_s(t) = 10\cos(1000t)$ V.
(a) Find the impedance of each element and the total impedance, in rectangular and polar form.
(b) Find the current phasor and $i(t)$. Does the current lead or lag the source?
(c) Find the capacitor voltage $v_C(t)$.
(d) Find the average power the source delivers, in two ways.
(e) At what frequency $\omega$ would the current be in phase with the source, and what would its amplitude be then?

**3 [A] · A first-order step response.** A 10 µF capacitor sits at 1 V. At $t = 0$ it is connected through a 2 kΩ resistor to a 5 V source.
(a) Write the differential equation for the capacitor voltage $v(t)$ and solve it.
(b) Find $v$ at $t = 10$ ms, and the time at which $v$ reaches 4 V.
(c) You simulate this circuit with forward Euler. What is the largest step that keeps the method stable, and the largest step for which the numerical solution does not alternate around the exact one?

**4 [B] · First-order methods.**
(a) Solve $t\,y' + 2y = t^2$ for $t > 0$ with $y(1) = 0$, using an integrating factor. Find $y(2)$.
(b) An RC low-pass filter with $\tau = 0.5$ ms starts at 0 V and is driven by the ramp $v_{in}(t) = kt$ with $k = 2$ V/ms. Find $v_{out}(t)$ and $v_{out}(1\text{ ms})$. Once the transient has died, by how many volts, and by how much time, does the output trail the input?
(c) For $y' = 1 - y^2$, find the equilibria and their stability from a phase line, and the local time constant at the stable one. Then solve the equation with $y(0) = 0$ by separation of variables and find $y(1)$.

**5 [C] · A second-order RLC step response.** A supply's output filter is modeled as a series RLC with $L = 1$ µH, $C = 1$ µF and $R = 0.5\ \Omega$, with the output taken across $C$. A 1 V step is applied at $t = 0$ with the circuit at rest.
(a) Derive the differential equation for the capacitor voltage. Find $\omega_0$, the neper frequency α, the damping ratio ζ and $Q$.
(b) Find the characteristic roots and the ringing frequency $\omega_d$.
(c) Write $v_C(t)$. Find the peak time, the percent overshoot and the peak voltage. Estimate the 2% settling time with the envelope rule.
(d) What resistance would make the circuit critically damped?
(e) A different filter's step response shows 25% overshoot, and successive ring peaks are 2 µs apart. Find its ζ and $\omega_0$.

**6 [B] · Forced response and resonance.**
(a) Solve $y'' + 4y = 3\cos 2t$ with $y(0) = y'(0) = 0$ by undetermined coefficients. Describe the solution's envelope, and find $y(\pi/4)$.
(b) Use complex replacement to find the steady-state solution of $y'' + 2y' + 5y = 10\cos 2t$ (amplitude and phase). At which input frequency would the steady-state amplitude be largest, and what is that largest amplitude?
(c) A series RLC band-pass filter uses $L = 1$ µH and must resonate at 10 MHz with $Q = 50$. Find $C$, $R$ and the half-power bandwidth. If the circuit is struck and left to ring, find the time constant of its decaying envelope and the number of cycles in one time constant.

**7 [B] · The Laplace transform.**
(a) Solve $y'' + 3y' + 2y = 4u(t)$, $y(0) = 1$, $y'(0) = 0$ with the Laplace transform. Find $y(1)$.
(b) Check $y(0^+)$ and $y(\infty)$ from $Y(s)$ with the initial- and final-value theorems. Explain why the final-value theorem must not be applied to $F(s) = s/(s^2 + 4)$.
(c) A system has $H(s) = 10/(s^2 + 2s + 10)$. Find its poles, ζ, its impulse response and its DC gain.
(d) A 1 V pulse lasting from $t = 0$ to $t = 2$ s drives $H_1(s) = 1/(s + 1)$, starting at rest. Use the time-shift property to find the output, and evaluate it at $t = 3$ s.

**8 [A] · Vectors and matrix products.** Let $\mathbf{a} = (1, 2, 2, 0)$ and $\mathbf{b} = (2, 0, 1, 2)$.
(a) Find $\mathbf{a}\cdot\mathbf{b}$, the lengths of both vectors and the angle between them.
(b) Find the projection $\mathbf{p}$ of $\mathbf{b}$ onto $\mathbf{a}$, show that $\mathbf{b} - \mathbf{p}$ is orthogonal to $\mathbf{a}$, and find $\lVert\mathbf{b} - \mathbf{p}\rVert$.
(c) With $\mathbf{A} = \begin{bmatrix}1 & 2\\ 0 & 1\end{bmatrix}$ and $\mathbf{B} = \begin{bmatrix}1 & 0\\ 3 & 1\end{bmatrix}$, find $\mathbf{A}\mathbf{B}$ and $\mathbf{B}\mathbf{A}$, and check that $(\mathbf{A}\mathbf{B})^{\mathsf{T}} = \mathbf{B}^{\mathsf{T}}\mathbf{A}^{\mathsf{T}}$.

**9 [C] · Nodal analysis, LU and reciprocity.** A resistive ladder has three nodes. A 1 mA current source feeds node 1. The resistors are: 1 kΩ from node 1 to ground, 2 kΩ from node 1 to node 2, 2 kΩ from node 2 to ground, 1 kΩ from node 2 to node 3, and 1 kΩ from node 3 to ground.
(a) Stamp the nodal equations $\mathbf{G}\mathbf{v} = \mathbf{i}$ (conductances in mS, currents in mA). Explain why $\mathbf{G}$ is symmetric and diagonally dominant.
(b) Factor $\mathbf{G} = \mathbf{L}\mathbf{U}$ by elimination, and find $\det\mathbf{G}$ from the pivots.
(c) Solve for the node voltages by forward and back substitution. Check your answer with a power balance.
(d) The source is moved to node 3. Reuse $\mathbf{L}$ and $\mathbf{U}$ to find the new node voltages. Compare the new $v_1$ with the old $v_3$, and explain the match.
(e) For a circuit with 3000 nodes and a dense $\mathbf{G}$, estimate the flops for the factorization and for each extra right-hand side.

**10 [B] · Rank, null space and least squares.**
(a) For $\mathbf{A} = \begin{bmatrix}1 & 2 & 1\\ 2 & 4 & 3\\ 3 & 6 & 4\end{bmatrix}$, find $\det\mathbf{A}$, the rank and a basis for the null space, and check the rank–nullity theorem.
(b) Find the complete solution of $\mathbf{A}\mathbf{x} = (1, 3, 4)$. Show that $\mathbf{A}\mathbf{x} = (1, 3, 5)$ has no solution, and say why in terms of the column space.
(c) A sensor is calibrated at inputs $x = 0, 1, 2, 3$ and reads $y = 1, 3, 4, 4$. Fit $y \approx c + mx$ by least squares through the normal equations. Find the residuals and their sum of squares, and show that the residual vector is orthogonal to both columns of the design matrix.

**11 [C] · Eigenvalues and a two-state power model.** A wearable's radio is either awake or asleep in each 1 ms slot. An awake radio stays awake in the next slot with probability 0.9; an asleep radio wakes with probability 0.2. Let $\mathbf{x}_k = (p_k, q_k)$ hold the probabilities of being awake and asleep in slot $k$, so $\mathbf{x}_{k+1} = \mathbf{M}\mathbf{x}_k$.
(a) Write $\mathbf{M}$. Find its eigenvalues and eigenvectors, and check them with the trace and the determinant.
(b) Find the steady state. The radio draws 10 mW awake and 0.1 mW asleep: find the long-run average power.
(c) Starting asleep, $\mathbf{x}_0 = (0, 1)$, find $p_k$ by eigenvector expansion. Evaluate $p_5$, and find how many slots it takes for $p_k$ to come within 0.01 of its steady value.
(d) New firmware makes an awake radio fall asleep with probability 0.3 per slot instead of 0.1. Find the new steady state, the new average power and the new second eigenvalue. What does the second eigenvalue tell you?

**12 [B] · Symmetric matrices and the SVD.**
(a) For $\mathbf{K} = \begin{bmatrix}2 & -1\\ -1 & 2\end{bmatrix}$, find the eigenvalues and orthonormal eigenvectors and write $\mathbf{K} = \mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^{\mathsf{T}}$. Show that $\mathbf{K}$ is positive definite in three ways: eigenvalues, pivots and energy $\mathbf{x}^{\mathsf{T}}\mathbf{K}\mathbf{x}$.
(b) Find the singular values and the right and left singular vectors of $\mathbf{H} = \begin{bmatrix}3 & 0\\ 4 & 5\end{bmatrix}$, and its condition number.
(c) $\mathbf{H}$ is the channel matrix of a 2×2 MIMO link. Give the power gains, as ratios and in dB, of the two parallel channels the SVD reveals. What is the error, in the 2-norm, of the best rank-1 approximation to $\mathbf{H}$?

**13 [C] · State space and the matrix exponential.** A series circuit of $R = 3\ \Omega$, $L = 1$ µH and $C = 0.5$ µF is driven by a source $u(t)$. Take the state $\mathbf{x} = (v_C, i_L)$ and measure time in microseconds.
(a) Derive $\mathbf{x}' = \mathbf{A}\mathbf{x} + \mathbf{B}u$, and show that $\mathbf{A} = \begin{bmatrix}0 & 2\\ -1 & -3\end{bmatrix}$ per µs. Classify the equilibrium from the trace and the determinant.
(b) With the source off, $v_C(0) = 1$ V and $i_L(0) = 0$, solve by eigenvector expansion. Find $v_C$ and $i_L$ at $t = 1$ µs, and the time and value of the most negative current.
(c) Find $e^{\mathbf{A}t}$ by diagonalization, and check it at $t = 0$ and against (b).
(d) Find the transfer function $V_C(s)/U(s)$, its DC gain, and the steady state for a constant 1 V source.
(e) Discretize with a zero-order hold and $T = 0.1$ µs: find the eigenvalues of $\mathbf{A}_d$. What is the largest stable forward-Euler step?

**14 [C] · Numerical methods.**
(a) Give machine epsilon for double and for single precision. Evaluate $1 - \cos(10^{-4})$ accurately, explain why single-precision arithmetic returns exactly 0 for it, and give a rewritten formula that works in single precision.
(b) Apply three Newton steps to $f(x) = x^2 - 2$ from $x_0 = 1$. Tabulate the errors and show that $e_{k+1}/e_k^2$ approaches its theoretical limit. How many bisection steps on [1, 2] would shrink the bracket below $10^{-6}$?
(c) A solver's test log shows a global error of $3.2\times10^{-5}$ at step $h = 0.02$ and $2.0\times10^{-6}$ at $h = 0.01$. Find its order of accuracy, and predict the error at $h = 0.005$.
(d) A circuit has two decaying modes, $\lambda_1 = -1000$ s⁻¹ and $\lambda_2 = -1$ s⁻¹, and is simulated for 5 s. What is the largest stable forward-Euler step, and how many steps does that force? With $h = 10$ ms, find the per-step amplification of the fast mode for backward Euler and for the trapezoidal rule, and say what each does to it.

**15 [A] · Conditioning and a low-precision pitch.** A startup says its accelerator solves circuit matrices "entirely in FP16 with no loss of accuracy". FP16 has unit roundoff $u = 2^{-11}$.
(a) Find the 2-norm condition number of $\mathbf{K} = \begin{bmatrix}1 & 1\\ 1 & 1.001\end{bmatrix}$.
(b) Use the rule of thumb (relative error up to about $\kappa u$) to estimate the error of solving $\mathbf{K}\mathbf{x} = \mathbf{b}$ in FP16, FP32 ($u = 2^{-24}$) and FP64 ($u = 2^{-53}$).
(c) In two or three sentences, say whether the claim can be true and what technique could make a low-precision solver accurate. Name two questions you would ask the founders.
