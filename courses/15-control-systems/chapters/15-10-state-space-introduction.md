<!-- status: reviewed -->
# 15-10 · State-Space Introduction

| | |
|---|---|
| **Course** | [15 · Control Systems](../README.md) |
| **University equivalent** | The state-space material of a first course in feedback control: state equations and their solution, similarity transformations and canonical forms, controllability and observability, pole placement by state feedback, observers and the separation principle, and integral action (Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 7; Nise, *Control Systems Engineering*, ch. 3, 4 and 12; Åström & Murray, *Feedback Systems*, ch. 6–8) |
| **Prerequisites** | [15-01 Modeling Dynamic Systems](15-01-modeling-dynamic-systems.md), [15-02 Transfer Functions and Block Diagrams](15-02-transfer-functions-and-block-diagrams.md), [02-09 Systems of ODEs and the Matrix Exponential](../../02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Write a state-space model, solve it with the matrix exponential, and move between state space, canonical forms and transfer functions.
2. Test controllability and observability with rank conditions, and connect a failure to a hidden mode or a pole–zero cancellation.
3. Place every closed-loop pole with state feedback, including the reference scaling for zero steady error.
4. Design a full-order observer and explain the separation principle.
5. Add integral action by augmenting the state, and relate state-feedback designs to PID and lead designs.

---

## 1. Big picture

Transfer functions describe a system from the outside: input to output. The **state-space** description looks inside: it tracks every energy store (15-01) as a state variable and writes the dynamics as first-order matrix equations. This view has three practical payoffs. It handles many inputs and outputs as easily as one. It exposes internal behaviour that a transfer function can hide, such as an unstable mode cancelled by a zero (15-02, 15-05). And it makes design systematic: with every state fed back, **all** closed-loop poles can be placed anywhere, not just moved along a root locus. When not every state can be measured, an **observer** estimates the missing ones from the outputs, and the separation principle guarantees that the two designs do not interfere.

- **Power converters are analyzed in state space** by state-space averaging: inductor currents and capacitor voltages are the states (22-07).
- **Multi-node thermal models of chips and packages** are state-space models with one state per thermal capacitance (15-01); thermal managers estimate unmeasured hot spots from a few sensors, which is an observer.
- **Modern control methods** (optimal LQR control, Kalman filtering, model predictive control) are built on the state-space form.
- **Simulators work with the same ideas.** Every ODE solver integrates $\dot{\mathbf{x}} = f(\mathbf{x}, \mathbf{u})$; SPICE instead assembles the circuit's modified nodal equations, a set of differential-algebraic equations, and integrates them implicitly, but the energy-storage elements still supply the dynamics.

## 2. Intuition first

**The state is the system's memory.** To predict a circuit's future you need the input from now on and the present values of its capacitor voltages and inductor currents; nothing else about the past matters. Those values are the state. A transfer function forgets the state (it assumes zero initial conditions); a state-space model keeps it.

**An analogy: a company's balance sheet.** A balance sheet summarizes the past in a few numbers (cash, inventory, debt) that, with future cash flows, determine the future. The income statement, flows over a period, is like the input. Controllability asks whether management's levers (the inputs) can move every balance-sheet line; observability asks whether published reports (the outputs) reveal every line. The analogy breaks down because a real balance sheet evolves nonlinearly and with discretion; a linear system evolves by a fixed matrix, and its controllability and observability are exact yes-or-no properties.

**Feeding back the state.** A proportional controller acts on one measured output. A state-feedback controller acts on every state: position *and* velocity, for a servo. Velocity feedback adds damping without the noise of differentiating position. With $n$ states and $n$ gains, $n$ closed-loop poles can be placed independently.

## 3. Theory

### 3.1 State equations

A linear time-invariant system with $n$ states, $m$ inputs and $p$ outputs is

$$
\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}, \qquad \mathbf{y} = C\mathbf{x} + D\mathbf{u} ,
$$

with $A$ ($n \times n$), $B$ ($n \times m$), $C$ ($p \times n$) and $D$ ($p \times m$). (Notation: as in most control texts, this course writes the state-space matrices as plain capitals $A, B, C, D, K, L$ and keeps bold for vectors; this deviates from the bold matrices of [notation.md](../../../reference/notation.md) and of 02-09.) Natural states are the energy stores: capacitor voltages, inductor currents, positions and velocities, temperatures of thermal capacitances. The transfer function is $C(sI - A)^{-1}B + D$ (15-02), and its poles are the eigenvalues of $A$ unless a cancellation hides one.

### 3.2 Solving the state equations

For the scalar equation $\dot x = ax + bu$, the solution is $x(t) = e^{at}x(0) + \int_0^te^{a(t - \tau)}bu(\tau)\,d\tau$. The matrix version has the same form, with the **matrix exponential** $e^{At} = I + At + (At)^2/2! + \cdots$ (02-09):

$$
\mathbf{x}(t) = e^{At}\mathbf{x}(0) + \int_0^te^{A(t - \tau)}B\mathbf{u}(\tau)\,d\tau .
$$

The first term is the **free response**, the second the **forced response**. If $A = V\Lambda V^{-1}$ has distinct eigenvalues $\lambda_i$ with eigenvectors $\mathbf{v}_i$, then $e^{At} = Ve^{\Lambda t}V^{-1}$: the free response is a sum of **modes** $\mathbf{v}_ie^{\lambda_it}$, each moving along its eigenvector. Stability means every eigenvalue has a negative real part (15-05).

### 3.3 Coordinates and canonical forms

The same system can be described with different states. With $\mathbf{x} = T\mathbf{z}$ for any invertible $T$:

$$
\dot{\mathbf{z}} = T^{-1}AT\,\mathbf{z} + T^{-1}B\,\mathbf{u}, \qquad \mathbf{y} = CT\,\mathbf{z} + D\mathbf{u} .
$$

A **similarity transformation** changes the matrices but not the eigenvalues or the transfer function. Two coordinate choices are especially useful.

**Controllable canonical form.** For $G(s) = (b_{n-1}s^{n-1} + \cdots + b_0)/(s^n + a_{n-1}s^{n-1} + \cdots + a_0)$,

$$
A_c = \begin{bmatrix} 0 & 1 & & \\ & \ddots & \ddots & \\ & & 0 & 1 \\ -a_0 & -a_1 & \cdots & -a_{n-1} \end{bmatrix}, \quad B_c = \begin{bmatrix} 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix}, \quad C_c = \begin{bmatrix} b_0 & b_1 & \cdots & b_{n-1} \end{bmatrix} .
$$

The characteristic polynomial's coefficients sit in the last row, which makes pole placement in these coordinates a matter of matching coefficients (§3.6).

**Modal (diagonal) form.** $\Lambda = V^{-1}AV$ decouples the modes.

### 3.4 Controllability

A system is **controllable** if some input can move the state from any initial value to any final value in finite time. The test, for any number of inputs, is the rank of the **controllability matrix**

$$
\mathcal{C} = \begin{bmatrix} B & AB & A^2B & \cdots & A^{n-1}B \end{bmatrix} ,
$$

which must be $n$.

> **Math refresher — the Cayley–Hamilton theorem.** Every square matrix satisfies its own characteristic equation: if $\det(sI - A) = s^n + a_{n-1}s^{n-1} + \cdots + a_0$, then $A^n + a_{n-1}A^{n-1} + \cdots + a_0I = 0$. For a diagonalizable $A = V\Lambda V^{-1}$ it is immediate: $A^k = V\Lambda^kV^{-1}$, so the polynomial evaluated at $A$ is $V\,\mathrm{diag}(p(\lambda_i))\,V^{-1}$, and every $p(\lambda_i) = 0$ because the $\lambda_i$ are the roots (02-08). The theorem holds for every square matrix. Its consequence: $A^n$, and therefore every higher power, is a combination of $I, A, \ldots, A^{n-1}$. So is $e^{At} = \sum_k A^kt^k/k!$, with coefficients that depend on time: $e^{At} = \sum_{k=0}^{n-1}\alpha_k(t)A^k$.

**Why the test is necessary.** Starting from $\mathbf{x}(0) = 0$, the state at time $t$ is

$$
\mathbf{x}(t) = \int_0^te^{A(t - \tau)}B\mathbf{u}(\tau)\,d\tau = \sum_{k=0}^{n-1}A^kB\int_0^t\alpha_k(t - \tau)\mathbf{u}(\tau)\,d\tau ,
$$

a combination of the columns of $\mathcal{C}$, whatever the input. If the rank is below $n$, the reachable states fill only a subspace, and the directions outside it can never be reached.

> **Going deeper — why the test is sufficient.** If $\operatorname{rank}\mathcal{C} = n$, the **controllability Gramian** $W(t_f) = \int_0^{t_f}e^{A\sigma}BB^Te^{A^T\sigma}d\sigma$ is invertible for every $t_f > 0$. (If $W\mathbf{v} = 0$ for some $\mathbf{v} \ne 0$, then $\mathbf{v}^TW\mathbf{v} = \int\lVert B^Te^{A^T\sigma}\mathbf{v}\rVert^2d\sigma = 0$, so $\mathbf{v}^Te^{A\sigma}B = 0$ for every $\sigma$; differentiating $n - 1$ times at $\sigma = 0$ gives $\mathbf{v}^T\mathcal{C} = 0$, contradicting full rank.) The input $\mathbf{u}(\tau) = B^Te^{A^T(t_f - \tau)}W(t_f)^{-1}(\mathbf{x}_f - e^{At_f}\mathbf{x}_0)$ then drives $\mathbf{x}_0$ to $\mathbf{x}_f$ exactly at $t_f$: substituting it into the solution of §3.2 and changing variable to $\sigma = t_f - \tau$ turns the integral into $W(t_f)W(t_f)^{-1}(\mathbf{x}_f - e^{At_f}\mathbf{x}_0)$. The input needed grows as $W$ approaches singularity, which is why a nearly uncontrollable system needs enormous effort (lab Part 3).

An uncontrollable mode is untouched by the input, and therefore by any feedback through it: its eigenvalue appears unchanged in every closed loop. If it is stable the system is still **stabilizable**; if it is unstable no controller can fix it. In the transfer function, an uncontrollable mode cancels.

### 3.5 Observability and duality

A system is **observable** if its initial state can be determined from the output over a finite time. The input's contribution to the output is known and can be subtracted, so take $\mathbf{u} = 0$. Then $\mathbf{y} = C\mathbf{x}$, and differentiating, $\dot{\mathbf{y}} = CA\mathbf{x}$, …, $\mathbf{y}^{(n-1)} = CA^{n-1}\mathbf{x}$. At $t = 0$ these stack into

$$
\begin{bmatrix} \mathbf{y}(0) \\ \dot{\mathbf{y}}(0) \\ \vdots \\ \mathbf{y}^{(n-1)}(0) \end{bmatrix} = \mathcal{O}\,\mathbf{x}(0), \qquad \mathcal{O} = \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{n-1} \end{bmatrix} .
$$

If $\operatorname{rank}\mathcal{O} = n$, this linear system has exactly one solution $\mathbf{x}(0)$. (In practice an observer, §3.7, recovers the state without differentiating noisy measurements.) If the rank is below $n$, some $\mathbf{x}(0) \ne 0$ has $\mathcal{O}\mathbf{x}(0) = 0$, and by Cayley–Hamilton $Ce^{At}\mathbf{x}(0) = \sum_k\alpha_k(t)CA^k\mathbf{x}(0) = 0$ for all $t$: that initial state produces no output at all and cannot be told apart from zero. So the test is rank $\mathcal{O} = n$. Observability of $(A, C)$ is controllability of $(A^T, C^T)$, since $\mathcal{O}^T = [C^T\ \ A^TC^T\ \cdots]$: the **duality** that lets every controller result be reused for estimators. An unobservable mode also cancels in the transfer function, and it can be unstable while the output looks fine.

> **Going deeper — minimal realizations.** A transfer function of order $n$ (after cancelling common factors) has state-space realizations of dimension $n$ that are both controllable and observable, called **minimal**. Any realization with more states contains uncontrollable or unobservable parts. Kalman's decomposition splits a general system into four parts (controllable and observable, controllable only, observable only, neither); the transfer function sees only the first.

### 3.6 State feedback and pole placement

With $u = -K\mathbf{x} + Nr$, the closed loop is

$$
\dot{\mathbf{x}} = (A - BK)\mathbf{x} + BNr .
$$

If $(A, B)$ is controllable, the eigenvalues of $A - BK$ can be placed anywhere (complex ones in conjugate pairs). In controllable canonical form, $A_c - B_cK$ is again a companion matrix whose last row is $-(a_0 + k_1), \ldots, -(a_{n-1} + k_n)$, so $k_i = \alpha_{i-1} - a_{i-1}$, the difference between desired and open-loop characteristic coefficients. In other coordinates, **Ackermann's formula** gives the same gain directly:

$$
K = \begin{bmatrix} 0 & \cdots & 0 & 1 \end{bmatrix}\mathcal{C}^{-1}\phi(A) ,
$$

where $\phi(s)$ is the desired characteristic polynomial evaluated at the matrix $A$ (single input).

**Where Ackermann's formula comes from ($n = 2$).** Let $A_K = A - BK$ have the desired polynomial $\phi(s) = s^2 + \alpha_1s + \alpha_0$, so $\phi(A_K) = 0$ by Cayley–Hamilton. Write $A = A_K + BK$ and expand: $A^2 = A(A_K + BK) = (A_K + BK)A_K + ABK = A_K^2 + BKA_K + ABK$. Then

$$
\phi(A) = \underbrace{A_K^2 + \alpha_1A_K + \alpha_0I}_{=\,0} + B(KA_K + \alpha_1K) + ABK = \begin{bmatrix} B & AB \end{bmatrix}\begin{bmatrix} KA_K + \alpha_1K \\ K \end{bmatrix} .
$$

Multiplying on the left by $[0\ \ 1]\,\mathcal{C}^{-1}$ picks out the bottom block: $K = [0\ \ 1]\,\mathcal{C}^{-1}\phi(A)$. For general $n$ the same expansion gives $\phi(A) = \mathcal{C}\,[\,\cdots;\ K\,]$ with $K$ in the last block, hence the formula. It needs $\mathcal{C}$ invertible, which is controllability again.

The **reference scaling** $N$ makes the DC gain 1. At steady state $\dot{\mathbf{x}} = 0$, so $\mathbf{x}_{ss} = -(A - BK)^{-1}BNr$ and

$$
N = \frac{-1}{C(A - BK)^{-1}B} .
$$

State feedback does not move the plant's zeros: the closed-loop transfer function keeps them, and $N$ fixes only the DC gain.

### 3.7 Observers and the separation principle

When only $\mathbf{y}$ is measured, a **Luenberger observer** runs a copy of the model, corrected by the output error:

$$
\dot{\hat{\mathbf{x}}} = A\hat{\mathbf{x}} + B\mathbf{u} + L(\mathbf{y} - C\hat{\mathbf{x}}) .
$$

The estimation error $\mathbf{e} = \mathbf{x} - \hat{\mathbf{x}}$ obeys $\dot{\mathbf{e}} = (A - LC)\mathbf{e}$, independent of the input. If $(A, C)$ is observable, $L$ places the eigenvalues of $A - LC$ anywhere (by duality, $L^T$ is Ackermann's gain for $(A^T, C^T)$). Observer poles are usually chosen 2 to 10 times faster than the controller's, a trade between fast convergence and noise amplification.

Now feed back the estimate, $u = -K\hat{\mathbf{x}} + Nr = -K\mathbf{x} + K\mathbf{e} + Nr$. In the coordinates $(\mathbf{x}, \mathbf{e})$:

$$
\frac{d}{dt}\begin{bmatrix} \mathbf{x} \\ \mathbf{e} \end{bmatrix} = \begin{bmatrix} A - BK & BK \\ 0 & A - LC \end{bmatrix}\begin{bmatrix} \mathbf{x} \\ \mathbf{e} \end{bmatrix} + \begin{bmatrix} BN \\ 0 \end{bmatrix}r .
$$

The matrix is block triangular, so its eigenvalues are those of $A - BK$ together with those of $A - LC$: the **separation principle**. The controller and observer can be designed separately. The reference-to-output transfer function is the same as with full-state feedback, because the observer error is not excited by $r$.

### 3.8 Integral action

State feedback with $N$ gives zero steady error only if the model is exact. To reject constant disturbances and model errors, add the integral of the tracking error as an extra state, $\dot x_i = r - C\mathbf{x}$ (15-04), and place the poles of the augmented system:

$$
\frac{d}{dt}\begin{bmatrix} \mathbf{x} \\ x_i \end{bmatrix} = \begin{bmatrix} A & 0 \\ -C & 0 \end{bmatrix}\begin{bmatrix} \mathbf{x} \\ x_i \end{bmatrix} + \begin{bmatrix} B \\ 0 \end{bmatrix}u + \begin{bmatrix} 0 \\ 1 \end{bmatrix}r, \qquad u = -\begin{bmatrix} K & k_i \end{bmatrix}\begin{bmatrix} \mathbf{x} \\ x_i \end{bmatrix} .
$$

For a first-order plant this is exactly a PI controller with its proportional action on the measurement only (setpoint weight $b$ = 0, 15-08): Example 15-10.6 recovers 15-08's gains.

> **Going deeper — choosing the poles optimally.** Where to put the poles is a design choice. The linear-quadratic regulator (LQR) instead minimizes $\int(\mathbf{x}^TQ\mathbf{x} + \mathbf{u}^TR\mathbf{u})\,dt$, trading state error against control effort, and returns $K$ from a Riccati equation; its dual, the Kalman filter, chooses $L$ from noise statistics. Together they form LQG control. Both are beyond a first course but use exactly the structures of §3.6–3.7.

## 4. Worked examples

### Example 15-10.1 · The motor in state space and in canonical form (tier A)

**Setup.** The motor of 15-01 Example 15-01.2 has $\mathbf{x} = [i,\ \omega]^T$, $A = \begin{bmatrix} -R/L_a & -K_m/L_a \\ K_m/J & -b/J \end{bmatrix}$, $B = [1/L_a,\ 0]^T$ and $C = [0,\ 1]$ with $R$ = 2 Ω, armature inductance $L_a$ = 1 mH, motor constant $K_m$ = 0.05 V·s/rad, $J$ = 2 × 10⁻⁵ kg·m² and friction $b$ = 10⁻⁵ N·m·s/rad. (Subscripts keep these apart from the input matrix $B$, the feedback gain $K$ and the observer gain $L$.) Find the eigenvalues, check controllability, and write the controllable canonical form.

**Solution.** The eigenvalues are **−65.1** and **−1935.4** s⁻¹ (15-02 Example 15-02.2). The controllability matrix $[B,\ AB] = \begin{bmatrix} 1/L_a & -R/L_a^2 \\ 0 & K_m/(JL_a) \end{bmatrix}$ has determinant $K_m/(JL_a^2)$ = **2.5 × 10⁹**, nonzero, so the voltage controls both current and speed. From $G(s) = 2.5 \times 10^6/(s^2 + 2000.5s + 126{,}000)$:

$$
A_c = \begin{bmatrix} 0 & 1 \\ -126{,}000 & -2000.5 \end{bmatrix}, \quad B_c = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \quad C_c = \begin{bmatrix} 2.5 \times 10^6 & 0 \end{bmatrix} .
$$

**Units check.** The columns of $\mathcal{C}$ carry different units (the first is $B$, the second $AB$), so the determinant's numerical value depends on the units chosen. Only whether it is zero matters.

**Sanity check.** $A$ and $A_c$ have the same trace (−2000.5) and determinant (126,000): similar matrices share eigenvalues.

### Example 15-10.2 · Solving with the matrix exponential (tier B)

**Setup.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $\mathbf{x}(0) = [1,\ 0]^T$, $u = 0$. Find $\mathbf{x}(t)$ and its value at $t$ = 1 s.

**Solution.** The eigenvalues are −1 and −2, with eigenvectors $[1,\ -1]^T$ and $[1,\ -2]^T$. Writing $\mathbf{x}(0) = 2[1,\ -1]^T - [1,\ -2]^T$:

$$
\mathbf{x}(t) = 2e^{-t}\begin{bmatrix} 1 \\ -1 \end{bmatrix} - e^{-2t}\begin{bmatrix} 1 \\ -2 \end{bmatrix} .
$$

At $t$ = 1 s: $x_1 = 2e^{-1} - e^{-2}$ = **0.600** and $x_2 = -2e^{-1} + 2e^{-2}$ = **−0.465**.

**Units check.** With $t$ in seconds, the eigenvalues are in 1/s.

**Sanity check.** $x_2 = \dot x_1$: differentiating $x_1 = 2e^{-t} - e^{-2t}$ gives $-2e^{-t} + 2e^{-2t}$, as found.

### Example 15-10.3 · Pole placement for a servo (tier B)

**Setup.** A servo with position $x_1$ and velocity $x_2$ obeys $\dot x_1 = x_2$, $\dot x_2 = -x_2 + u$ (plant $1/[s(s + 1)]$). Both states are measured. Place the closed-loop poles at $-2 \pm j2\sqrt3$ ($\zeta$ = 0.5, $\omega_n$ = 4 rad/s), find $N$, and give the step response. Compare with 15-09's lead design for the same poles.

**Solution.** The model is already in controllable canonical form ($a_0 = 0$, $a_1 = 1$). The desired polynomial is $s^2 + 4s + 16$, so $k_1 = 16 - 0$ = **16** and $k_2 = 4 - 1$ = **3**. Then $A - BK = \begin{bmatrix} 0 & 1 \\ -16 & -4 \end{bmatrix}$ and $N = -1/[C(A - BK)^{-1}B]$ = **16**, giving

$$
T(s) = \frac{16}{s^2 + 4s + 16} ,
$$

exactly second-order: overshoot **16.3**%, peak at **0.907** s. The lab builds this loop in ngspice and measures the same.

The lead design of Example 15-09.4 placed the same dominant poles but overshot by 27.4%, because it added a zero and a third pole. State feedback adds neither: it uses the velocity measurement instead of a lead network's estimate of it.

**Units check.** With $u$ in rad/s² per unit, $k_1$ is in 1/s² and $k_2$ in 1/s.

**Sanity check.** Ackermann's formula (§3.6), applied by the verify script, returns the same $K = [16,\ 3]$.

### Example 15-10.4 · Two identical RC circuits: an uncontrollable mode (tier B)

**Setup.** Two identical RC low-pass circuits ($R$ = 1 kΩ, $C$ = 1 µF) are driven in parallel by one source. With states $v_1$, $v_2$, check controllability and interpret.

**Solution.** $A = -1000I$ and $B = 1000[1,\ 1]^T$, so $\mathcal{C} = [B,\ AB] = 1000\begin{bmatrix} 1 & -1000 \\ 1 & -1000 \end{bmatrix}$, which has rank **1**. The input moves only the sum direction $v_1 + v_2$. The difference $v_1 - v_2$ obeys $\frac{d}{dt}(v_1 - v_2) = -1000(v_1 - v_2)$ whatever the source does: it decays with its own **−1000** s⁻¹ eigenvalue and cannot be steered. Since that mode is stable, the system is stabilizable, but no input can, for example, hold $v_1 = 1$ V with $v_2 = 0$.

**Units check.** $1/(RC)$ = 1000 s⁻¹.

**Sanity check.** Symmetry: a common input cannot create an asymmetric state. The transfer function from the source to either output is first-order, $1000/(s + 1000)$; the second mode is hidden.

### Example 15-10.5 · Measuring position only: an observer (tier C)

**Setup.** In Example 15-10.3's servo only position is measured, $C = [1,\ 0]$. Design an observer with both poles at −10, combine it with $K = [16,\ 3]$, and check the separation principle. Start with a 0.5 rad error in the estimated position and $r = 0$: how large is the estimation error after 0.5 s, and how far does the output stray?

**Solution.** $A - LC = \begin{bmatrix} -l_1 & 1 \\ -l_2 & -1 \end{bmatrix}$ has characteristic polynomial $s^2 + (1 + l_1)s + (l_1 + l_2)$. Matching $(s + 10)^2 = s^2 + 20s + 100$: $l_1$ = **19**, $l_2$ = **81**. The combined system's eigenvalues are $-2 \pm j3.46$ and −10 (twice), as the separation principle predicts.

Simulating the four-state closed loop: the estimation error decays from 0.5 to **0.0118** rad in 0.5 s (passing through zero on the way), while the controller, acting on the wrong estimate, pushes the true position to a peak of **0.137** rad at **0.575** s before both settle. The step response from $r$ is identical to the full-state design (to about $10^{-13}$), because the reference does not excite the estimation error.

**Units check.** $l_1$ in 1/s and $l_2$ in 1/s².

**Sanity check.** Faster observer poles would shrink the transient but amplify measurement noise through the large $L$; −10 is 2.5 times the controller's $\omega_n$, at the low end of the usual range.

### Example 15-10.6 · Integral action by augmentation (tier C)

**Setup.** The thermal plant of 15-08, $\dot x = -0.1x + 0.05u$ (time constant 10 s, gain 0.5 K/W), is augmented with $\dot x_i = r - x$. Place the augmented poles at $-0.4 \pm j0.3$ ($\omega_n$ = 0.5 rad/s, $\zeta$ = 0.8). Find the gains, the step overshoot and the peak temperature error after a 20 W input disturbance.

**Solution.** The augmented system is $A_a = \begin{bmatrix} -0.1 & 0 \\ -1 & 0 \end{bmatrix}$, $B_a = [0.05,\ 0]^T$. Ackermann's formula gives $K_a = [14,\ -5]$, so $u = -14x + 5x_i$: a PI controller with $K_i$ = 5 W/(K·s) acting on the error and $K_p$ = **14** W/K acting on the measurement only. These are exactly 15-08's gains with setpoint weight $b$ = 0. The step overshoot is **1.52**%, the value $\zeta$ = 0.8 predicts, because no zero appears in the reference path. A 20 W disturbance raises the temperature by at most **0.848** K, at **2.15** s, then the integrator removes it: the same as Example 15-08.1, since the feedback path is the same.

**Units check.** $K_a$: W/K for the temperature state, W/(K·s) for the integral.

**Sanity check.** State-space design and PI design are two descriptions of one controller; they must agree, and they do.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 15-10.1a | slow eigenvalue | −65.1 | 1/s |
| Ex 15-10.1b | fast eigenvalue | −1935.4 | 1/s |
| Ex 15-10.1c | determinant of the controllability matrix | 2.5e9 | — |
| Ex 15-10.2a | x1 at 1 s | 0.600 | — |
| Ex 15-10.2b | x2 at 1 s | −0.465 | — |
| Ex 15-10.3a | k1 | 16 | 1/s² |
| Ex 15-10.3b | k2 | 3 | 1/s |
| Ex 15-10.3c | N | 16 | 1/s² |
| Ex 15-10.3f | overshoot | 16.3 | % |
| Ex 15-10.3g | peak time | 0.907 | s |
| Ex 15-10.4a | rank of the controllability matrix | 1 | — |
| Ex 15-10.4b | uncontrollable eigenvalue | −1000 | 1/s |
| Ex 15-10.5a | l1 | 19 | 1/s |
| Ex 15-10.5b | l2 | 81 | 1/s² |
| Ex 15-10.5c | estimation error at 0.5 s | 0.0118 | rad |
| Ex 15-10.5d | peak position excursion | 0.137 | rad |
| Ex 15-10.5e | time of the excursion | 0.575 | s |
| Ex 15-10.6a | proportional gain | 14 | W/K |
| Ex 15-10.6b | overshoot | 1.52 | % |
| Ex 15-10.6c | disturbance peak | 0.848 | K |
| Ex 15-10.6d | time of the peak | 2.15 | s |

## 5. Simulate it

The lab, [labs/15-10-lab](../labs/15-10-lab/README.md), provides `statespace.py`: controllability and observability matrices, Ackermann's formula for state feedback and (by duality) for observers, integral augmentation, and exact closed-loop responses through the matrix exponential. You:

1. **Solve and visualize** Example 15-10.2's modes in the phase plane.
2. **Place poles** for the servo, build it in ngspice (`state_feedback.cir`), and compare with the lead design of 15-09.
3. **Break controllability**: perturb Example 15-10.4's twin RC circuits slightly and watch the controllability matrix's smallest singular value, and the control effort needed, explode as they become identical.
4. **Run an observer** with noisy position measurements and compare observer poles at −5, −10 and −40.

**Guided exercise (predict, then run).** **Before Part 3,** predict what happens to the input needed to separate $v_1$ and $v_2$ as the two time constants approach each other. (It grows without bound: the system is "nearly uncontrollable".)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Faster controller poles (larger $K$) | Speed and disturbance rejection | Actuator effort and saturation; sensitivity to model error | Control designer |
| Faster observer poles (larger $L$) | Quicker convergence of estimates | Amplified measurement noise; less robustness to model error | Control / estimation designer |
| Measuring more states | Less reliance on the model; no observer lag | Sensors, wiring, cost | System architect |
| Integral augmentation | Zero steady error despite model error and disturbances | One more pole; windup if the actuator saturates (15-08) | Control designer |
| Model order (more states) | Fidelity | Design complexity; parameters to identify; observability of every state | Modeling engineer |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Solution | $\mathbf{x}(t) = e^{At}\mathbf{x}(0) + \int_0^te^{A(t - \tau)}B\mathbf{u}\,d\tau$ | §3.2 |
| Controllability / observability tests | rank $[B\ AB\ \cdots\ A^{n-1}B] = n$; rank of the stacked $C, CA, \ldots$ = $n$ | §3.4–3.5 |
| Reference scaling | $N = -1/[C(A - BK)^{-1}B]$ | §3.6 |
| Observer speed | 2 to 10 times the controller's poles | §3.7 |
| Separation principle | closed-loop poles = eig($A - BK$) ∪ eig($A - LC$) | §3.7 |

## 8. Common mistakes

- **Assuming the transfer function shows every mode.** Uncontrollable or unobservable modes cancel; check the ranks.
- **Forgetting $N$.** Without reference scaling, state feedback generally leaves a steady error.
- **Expecting state feedback to remove plant zeros.** It moves poles only; a right-half-plane zero stays.
- **Making the observer much too fast.** Noise passes through $L$; estimates become noisy.
- **Relying on $N$ for accuracy.** It is exact only for an exact model; use integral action against model error and disturbances.
- **Ignoring numerical conditioning.** A nearly singular controllability matrix means huge gains and effort, even if the rank is technically full (lab Part 3).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

These are established practice; no perishable figures are quoted.

- **State-space averaging is the standard small-signal model of switching converters**, from which control-to-output transfer functions are derived (22-07) **[Established]**.
- **Estimation is common in power and thermal management**: hot-spot temperatures between sensors are estimated from multi-node thermal models and measured power, an application of observers and Kalman filters **[Established]**.
- **Motor drives use field-oriented control with state observers** to estimate rotor position and speed without mechanical sensors ("sensorless" control) **[Established]**.

### Why it matters commercially

- **Fewer sensors, lower cost.** A good observer can replace a sensor, saving cost and a failure point; sensorless motor control is the familiar example.
- **Hidden modes are product risks.** A transfer-function-only analysis can miss an unstable internal mode; state-space checks catch it before silicon or firmware ships.
- **Model-based control needs models.** State-space methods are only as good as the model, so the cost of characterization and the robustness to model error must be in the budget.

### Marketing vs Reality

- **"Sensorless."** *Reality:* an observer estimates the missing quantity from a model and other measurements; accuracy depends on the model and degrades in some operating regions (for motors, near zero speed). *Sanity check:* ask for estimation error across the operating range.
- **"Model-based, so it's optimal."** *Reality:* optimal for the model; robustness to model error must be checked separately. *Sanity check:* ask for margins with the model perturbed.
- **"Places all poles exactly."** *Reality:* only if all states are measured or well estimated, and actuators do not saturate. *Sanity check:* ask what is measured and what is estimated.

### Questions for engineering leaders

1. **"Which states are measured and which are estimated, and how fast does the estimator converge?"**
   *Strong:* a clear list with observer poles and noise analysis. *Evasive:* "the model handles it".
2. **"Is the system controllable and observable from the actuators and sensors you have, and how well conditioned?"**
   *Strong:* rank and conditioning checked, with any weakly controllable modes identified. *Evasive:* rank not checked.
3. **"How does performance degrade if the model is 20% off?"**
   *Strong:* robustness analysis or tests. *Evasive:* nominal results only.
4. **"How is steady-state accuracy guaranteed?"**
   *Strong:* integral action with anti-windup. *Evasive:* reference scaling only.

## 10. Concept check

**Q1.** Why are the poles of $C(sI - A)^{-1}B$ the eigenvalues of $A$ unless something cancels?

<details><summary>Answer</summary>

$(sI - A)^{-1} = \operatorname{adj}(sI - A)/\det(sI - A)$, and $\det(sI - A)$ is the characteristic polynomial. A pole disappears only if a numerator factor cancels it, which happens exactly for uncontrollable or unobservable modes.

</details>

**Q2.** What does the controllability matrix's rank tell you, and why?

<details><summary>Answer</summary>

Rank $n$ means every state direction can be reached. By Cayley–Hamilton, the forced response lies in the span of $B, AB, \ldots, A^{n-1}B$; if that span is smaller than $\mathbb{R}^n$, some directions are unreachable.

</details>

**Q3.** How does state feedback differ from output feedback in what it can do to the poles?

<details><summary>Answer</summary>

With all $n$ states fed back through $n$ gains, all $n$ closed-loop poles can be placed anywhere (if controllable). Output feedback through a single adjustable gain moves the poles only along a root locus; a dynamic output controller, such as an observer plus state feedback (§3.7), can again place every pole (if the plant is also observable).

</details>

**Q4.** Why is the reference scaling $N$ needed, and why is it not robust?

<details><summary>Answer</summary>

State feedback changes the DC gain; $N$ restores it to 1. It is computed from the model, so a model error or a disturbance leaves a steady error; integral action is the robust fix.

</details>

**Q5.** State the separation principle.

<details><summary>Answer</summary>

With feedback from observer estimates, the closed-loop eigenvalues are those of $A - BK$ together with those of $A - LC$, so the controller and observer can be designed independently.

</details>

**Q6.** Why does the observer not change the reference-to-output response?

<details><summary>Answer</summary>

The estimation error obeys $\dot{\mathbf{e}} = (A - LC)\mathbf{e}$ with no input from $r$, so if it starts at zero it stays at zero, and $u$ equals the full-state feedback.

</details>

**Q7.** What controller results from augmenting a first-order plant with the integral of the error and placing two poles?

<details><summary>Answer</summary>

A PI controller with the proportional action on the measurement only (setpoint weight $b$ = 0), as Example 15-10.6 shows.

</details>

Practice: [Problems 15-10](../problems/15-10-problems.md) · [Solutions](../solutions/15-10-solutions.md)

## 11. Key terms

[State-space model](../../../reference/glossary.md#state-space-model) · [Matrix exponential](../../../reference/glossary.md#matrix-exponential) · [Similarity transformation](../../../reference/glossary.md#similarity-transformation) · [Controllability](../../../reference/glossary.md#controllability) · [Observability](../../../reference/glossary.md#observability) · [Pole placement](../../../reference/glossary.md#pole-placement) · [State observer](../../../reference/glossary.md#state-observer) · [Separation principle](../../../reference/glossary.md#separation-principle)

## 12. Connections

- **Builds on:** state models ([15-01](15-01-modeling-dynamic-systems.md)); transfer functions from state space and hidden modes ([15-02](15-02-transfer-functions-and-block-diagrams.md)); the matrix exponential ([02-09](../../02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md)); PID ([15-08](15-08-pid-control.md)); lead ([15-09](15-09-lead-lag-compensation.md)).
- **Next:** [15-11 Digital Control](15-11-digital-control.md), which discretizes these models and controllers.
- **Used later:** thermal estimation and regulator models ([15-12](15-12-control-applications-pll-regulators-thermal.md)); converter state-space averaging ([22-07](../../22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)).

## 13. Further study

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 7 (state-space design: pole placement, estimators, the separation principle, integral control).
- K. J. Åström and R. M. Murray, *Feedback Systems*, ch. 6–8 (linear systems, state feedback, output feedback; free online).
- N. S. Nise, *Control Systems Engineering*, ch. 12 (design via state space).
- MIT OpenCourseWare 16.30/16.31, *Feedback Control Systems*: state-space lectures.

## 14. Sources

1. Franklin, Powell and Emami-Naeini; Åström and Murray; Nise (Further study): state-space analysis and design (textbook material).

This chapter has no perishable industry figures; its practitioner statements are tagged [Established]. Every number in the examples is recomputed by the verify script (eigenvalues, ranks, Ackermann gains checked by the resulting eigenvalues, responses by the matrix exponential), and Example 15-10.3 is confirmed in ngspice.
