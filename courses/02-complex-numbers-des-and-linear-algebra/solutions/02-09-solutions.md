# Solutions 02-09 · Systems of Linear ODEs and the Matrix Exponential

Problems: [02-09 problems](../problems/02-09-problems.md) · Chapter: [02-09](../chapters/02-09-systems-of-odes-and-matrix-exponential.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_02_09.py](../verify/verify_02_09.py). Problems 9 and 14 are also simulated in ngspice in the [lab](../labs/02-09-lab/README.md).

---

## Solutions

### Solution 02-09.1

(a) KCL at the top node gives $Cv_C' = i_s - v_C/R - i_L$, and the inductor gives $Li_L' = v_C$. So

$$
\mathbf{A} = \begin{bmatrix} -1/(RC) & -1/C \\ 1/L & 0\end{bmatrix} = \begin{bmatrix} -10^4 & -10^7 \\ 100 & 0\end{bmatrix}, \qquad \mathbf{B} = \begin{bmatrix} 1/C \\ 0\end{bmatrix} .
$$

(b) The trace is **−10⁴** s⁻¹ and the determinant is \$0 + 10^7\times100 = \$ **10⁹** s⁻². So $\lambda^2 + 10^4\lambda + 10^9 = 0$, giving $\lambda = -5000 \pm j\sqrt{10^9 - 2.5\times10^7} = -5000 \pm j$**31,225** s⁻¹: an underdamped parallel RLC with \$\omega_0 = 1/\sqrt{LC} = \$ **31,623** rad/s.

(c) Setting $\mathbf{x}' = \mathbf{0}$: the second equation forces $v_C = 0$, and then the first gives $i_L = i_s$. At DC the inductor is a short, so it carries all of the source current and the node sits at 0 V.

### Solution 02-09.2

With $\mathbf{x} = (y, y', y'')$:

$$
\mathbf{A} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -6 & -11 & -6\end{bmatrix}, \qquad \mathbf{B} = \begin{bmatrix} 0 \\ 0 \\ 1\end{bmatrix} .
$$

The characteristic polynomial is $\lambda^3 + 6\lambda^2 + 11\lambda + 6 = (\lambda + 1)(\lambda + 2)(\lambda + 3)$, so the eigenvalues are **−1, −2, −3**. *Checks:* the sum −6 equals the trace ✓, and the product −6 equals the determinant ✓ (expanding along the first column, $\det\mathbf{A} = -6$).

### Solution 02-09.3

(a) $e^{\mathbf{A}t} = \operatorname{diag}(e^{-t}, e^{-2t})$: a diagonal matrix exponentiates entry by entry.

(b) $\mathbf{N}^2 = \mathbf{0}$, so the series stops after two terms: $e^{\mathbf{N}t} = \mathbf{I} + \mathbf{N}t = \begin{bmatrix} 1 & t \\ 0 & 1\end{bmatrix}$. Its derivative is $\begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix} = \mathbf{N}$, and $\mathbf{N}e^{\mathbf{N}t} = \begin{bmatrix} 0 & 1 \\ 0 & 0\end{bmatrix}$ ✓. Physically, $x_2$ is constant and $x_1$ grows linearly: a "double integrator", such as position under constant velocity.

(c) $\operatorname{tr}\mathbf{A} = 5$, so \$\det e^{\mathbf{A}} = e^5 = \$ **148.4**.

### Solution 02-09.4

| Case | $T^2 - 4\Delta$ | Type | Stable? |
|---|---|---|---|
| (a) $T = -3$, $\Delta = 2$ | $9 - 8 = 1 > 0$ | node (eigenvalues −1, −2) | yes |
| (b) $T = 1$, $\Delta = 4$ | $1 - 16 < 0$ | spiral with $T > 0$ | no: it spirals outward |
| (c) $T = 0$, $\Delta = -1$ | — | saddle (eigenvalues ±1) | no |
| (d) $T = -2$, $\Delta = 1$ | $4 - 4 = 0$ | repeated eigenvalue −1: degenerate node | yes |

### Solution 02-09.5

The eigenvalues are **3**, with $\mathbf{v}_1 = (1, 1)$, and **−1**, with $\mathbf{v}_2 = (1, -1)$: a saddle. Since $\mathbf{x}(0) = (1, 0) = \tfrac12\mathbf{v}_1 + \tfrac12\mathbf{v}_2$,

$$
\mathbf{x}(t) = \tfrac12\big(e^{3t} + e^{-t},\ e^{3t} - e^{-t}\big), \qquad \mathbf{x}(1) = (\mathbf{10.23}, \mathbf{9.859}) .
$$

Only initial conditions exactly on the line through $(1, -1)$, the stable eigenvector, give decaying solutions. Any component along $(1, 1)$ eventually grows like $e^{3t}$. A saddle is unstable even though one of its eigenvalues is negative.

### Solution 02-09.6

$\mathbf{K} = \mathbf{A} + \mathbf{I} = \begin{bmatrix} 0 & -4 \\ 1 & 0\end{bmatrix}$, and $\mathbf{K}^2 = -4\mathbf{I}$. So the powers of $\mathbf{K}$ cycle like those of $2j$, and the series gives $e^{\mathbf{K}t} = \mathbf{I}\cos2t + \tfrac12\mathbf{K}\sin2t$. Since $-\mathbf{I}$ commutes with $\mathbf{K}$:

$$
e^{\mathbf{A}t} = e^{-t}\begin{bmatrix} \cos2t & -2\sin2t \\ \tfrac12\sin2t & \cos2t\end{bmatrix}, \qquad \mathbf{x}(t) = e^{-t}\big(\cos2t,\ \tfrac12\sin2t\big) .
$$

*By complex eigenvectors.* The eigenvalues are $-1 \pm 2j$. For $\lambda = -1 + 2j$, $(\mathbf{A} - \lambda\mathbf{I})\mathbf{v} = \mathbf{0}$ has first row $-2jv_1 - 4v_2 = 0$, so $\mathbf{v} = (2j, 1)$. Then $e^{\lambda t}\mathbf{v} = e^{-t}(\cos2t + j\sin2t)(2j, 1)$ has real part $e^{-t}(-2\sin2t, \cos2t)$ and imaginary part $e^{-t}(2\cos2t, \sin2t)$, two real solutions. Fitting $\mathbf{x}(0) = (1, 0) = c_1(0, 1) + c_2(2, 0)$ gives $c_1 = 0$, $c_2 = \tfrac12$, so $\mathbf{x}(t) = e^{-t}(\cos2t, \tfrac12\sin2t)$, the same answer.

At $t = 0.5$: \$e^{-0.5}(\cos1, \tfrac12\sin1) = \$ (**0.3277**, **0.2552**). This is a stable spiral, with eigenvalues $-1 \pm 2j$: decay rate 1, rotation at 2 rad/s.

*Check:* $\mathbf{x}(0) = (1, 0)$ ✓, and $x_1' = -e^{-t}(\cos2t + 2\sin2t)$ at $t = 0$ is $-1 = -x_1 - 4x_2$ ✓.

### Solution 02-09.7

λ = −2 is repeated, with only one eigenvector, $\mathbf{v} = (1, 0)$. *Generalized eigenvector:* solve $(\mathbf{A} + 2\mathbf{I})\mathbf{w} = \mathbf{v}$, that is $\begin{bmatrix}0 & 1\\ 0 & 0\end{bmatrix}\mathbf{w} = (1, 0)$, so $\mathbf{w} = (0, 1)$. The two solutions are $e^{-2t}\mathbf{v}$ and $e^{-2t}(t\mathbf{v} + \mathbf{w}) = e^{-2t}(t, 1)$, and $\mathbf{x}(0) = (0, 1) = \mathbf{w}$ picks the second. *Check with the exponential:* from §3.3, $e^{\mathbf{A}t} = e^{-2t}\begin{bmatrix} 1 & t \\ 0 & 1\end{bmatrix}$, so $\mathbf{x}(t) = e^{-2t}(t, 1)$. Then $x_1 = te^{-2t}$ peaks where $(1 - 2t)e^{-2t} = 0$, at \$t = \$ **0.5**, with value \$0.5e^{-1} = \$ **0.1839**. This is the critically damped shape of 02-03.

### Solution 02-09.8

$$
s\mathbf{I} - \mathbf{A} = \begin{bmatrix} s & -1 \\ 2 & s + 3\end{bmatrix}, \qquad (s\mathbf{I} - \mathbf{A})^{-1} = \frac{1}{(s + 1)(s + 2)}\begin{bmatrix} s + 3 & 1 \\ -2 & s\end{bmatrix} .
$$

Partial fractions on the first row: $\dfrac{s + 3}{(s + 1)(s + 2)} = \dfrac{2}{s + 1} - \dfrac{1}{s + 2}$ and $\dfrac{1}{(s + 1)(s + 2)} = \dfrac{1}{s + 1} - \dfrac{1}{s + 2}$. So

$$
e^{\mathbf{A}t} = \begin{bmatrix} 2e^{-t} - e^{-2t} & e^{-t} - e^{-2t} \\ -2e^{-t} + 2e^{-2t} & -e^{-t} + 2e^{-2t}\end{bmatrix} .
$$

For the second row: $\dfrac{-2}{(s + 1)(s + 2)} = \dfrac{-2}{s + 1} + \dfrac{2}{s + 2}$ and $\dfrac{s}{(s + 1)(s + 2)} = \dfrac{-1}{s + 1} + \dfrac{2}{s + 2}$ (cover-up: at $s = -1$, $-1/1 = -1$; at $s = -2$, $-2/(-1) = 2$).

At $t = 1$, the first row is (**0.6004**, **0.2325**). *Check:* at $t = 0$ the matrix is $\mathbf{I}$ ✓.

### Solution 02-09.9

(a) The resistor from node 1 still contributes $-v_1/R$ to node 1's KCL, and now also $+v_s/R$. So $\mathbf{A}$ is unchanged and $\mathbf{B} = (1/\tau, 0)$, with input $v_s = 1$ V.

(b) $\mathbf{x}_{ss} = -\mathbf{A}^{-1}\mathbf{B}$. With τ = 1, $\mathbf{A}^{-1} = \tfrac13\begin{bmatrix} -2 & -1 \\ -1 & -2\end{bmatrix}$, so \$\mathbf{x}_{ss} = \tfrac13(2, 1) = \$ (**0.6667**, **0.3333**) V. *Divider check:* at DC the capacitors are open, leaving three equal resistors in series from 1 V to ground. Node 1 is at 2/3 V and node 2 at 1/3 V ✓.

(c) $\mathbf{x}(t) = \mathbf{x}_{ss} - e^{\mathbf{A}t}\mathbf{x}_{ss}$. In eigenvectors, $\mathbf{x}_{ss} = \tfrac12(1, 1) + \tfrac16(1, -1)$, so

$$
v_2(t) = \tfrac13 - \tfrac12e^{-t/\tau} + \tfrac16e^{-3t/\tau},
$$

and at $t = τ$: \$0.3333 - 0.1839 + 0.0083 = \$ **0.1577 V**.

### Solution 02-09.10

With τ = 1, $\det(s\mathbf{I} - \mathbf{A}) = (s + 2)^2 - 1 = (s + 1)(s + 3)$. With $\mathbf{B} = (1, 0)$ and $\mathbf{C} = (0, 1)$, $H(s)$ is the (2, 1) entry of $(s\mathbf{I} - \mathbf{A})^{-1}$:

$$
H(s) = \frac{1}{(s\tau + 1)(s\tau + 3)} .
$$

The poles are at $-1/\tau$ and $-3/\tau$, the eigenvalues. The DC gain is \$H(0) = \$ **1/3** (0.3333), matching $v_{2,ss}$ ✓. At $\omega\tau = 1$: \$\lvert H\rvert = 1/(\lvert1 + j\rvert\,\lvert3 + j\rvert) = 1/(\sqrt2\sqrt{10}) = \$ **0.2236**.

### Solution 02-09.11

(a) $T = -3 < 0$ always. $\Delta = 2 - k$, so the system is stable exactly when \$k < \$ **2**.

(b) At $k = 2$, $\Delta = 0$: one eigenvalue is 0 (here 0 and −3), a marginal case with a whole line of equilibria. At $k = 3$, $\Delta = -1 < 0$: a saddle, unstable.

### Solution 02-09.12

(a) Exact: \$a_d = e^{-T/\tau} = e^{-0.25} = \$ **0.7788** and \$b_d = 1 - e^{-0.25} = \$ **0.2212** (the one-state version of $\mathbf{A}^{-1}(e^{\mathbf{A}T} - \mathbf{I})\mathbf{B}$). Euler: \$a_d = 1 - T/\tau = \$ **0.75** and $b_d = T/\tau = 0.25$.

(b) One exact step gives 0.7788, one Euler step 0.75: about 3.7% low after one step, and the error compounds.

(c) $\lvert1 - T/\tau\rvert < 1$ requires \$T < 2\tau = \$ **4 ms**.

### Solution 02-09.13

KCL at each node: the capacitor currents, collected as $\mathbf{C}_m\mathbf{v}'$, plus the inductor current leaving to ground, sum to zero. So $\mathbf{C}_m\mathbf{v}' = -\mathbf{i}_L$. Each inductor obeys $L\,i_{Lk}' = v_k$. Stacking $\mathbf{x} = (\mathbf{v}, \mathbf{i}_L)$:

$$
\mathbf{x}' = \begin{bmatrix} \mathbf{0} & -\mathbf{C}_m^{-1} \\ \mathbf{I}/L & \mathbf{0}\end{bmatrix}\mathbf{x} .
$$

Eliminating $\mathbf{i}_L$ gives $\mathbf{v}'' = -\mathbf{C}_m^{-1}\mathbf{v}/L$, so the eigenvalues of $\mathbf{A}$ are $\pm j\omega$, where $\omega^2$ runs over the eigenvalues of $\mathbf{C}_m^{-1}/L$. That is, ω = $1/\sqrt{Lc}$ with $c$ an eigenvalue of $\mathbf{C}_m$. Numerically, $\lambda = \pm j2\pi\times$**5.033 MHz** and $\pm j2\pi\times$**4.594 MHz**: two pairs on the imaginary axis (the model is lossless, so these are two centers), at exactly the normal-mode frequencies of 02-08 ✓.

### Solution 02-09.14

(a) \$R_1 + R_2 + R_3 = \$ **2.0 K/W**: the value as $t \to \infty$.

(b) $Z_{th}(10\text{ ms}) = 0.2(1 - e^{-10}) + 0.5(1 - e^{-0.2}) + 1.3(1 - e^{-0.005}) = 0.2000 + 0.0906 + 0.0065 = $ **0.2971 K/W**. For 50 W, $\Delta T = 50\times0.2971 = $ **14.86 K**.

(c) \$100/0.2971 = \$ **336.6 W** for a single 10 ms pulse, against $100/2 = 50$ W continuous. The short pulse is absorbed mostly by the die's heat capacity before the slow, large-τ modes) have warmed. This is why MOSFET datasheets plot $Z_{th}$ against pulse width: pulse ratings can be many times the continuous rating.

### Solution 02-09.15

(a) $ah = -0.02$, so \$\bar{a} = e^{-0.02} = \$ **0.9802** and \$\bar{b} = (e^{-0.02} - 1)(1/\tau)/(-1/\tau) = 1 - e^{-0.02} = \$ **0.01980**. Forward Euler gives $1 - 0.02 = 0.98$ and $0.02$: very close here, because $h$ is much smaller than τ.

(b) After an impulse the state decays as $\bar{a}^k$, which reaches 1% when \$k = \ln100/0.02 = \$ **230.3** steps. In general $k_{1\%} = (\tau/h)\ln100$: the memory length in steps scales with $\tau/h$. A layer that must remember far back needs $\bar{a}$ close to 1 (a slow pole), and a larger step Δ makes it forget faster. Selective state-space models exploit exactly that, by making Δ depend on the input ([R-052](../../../reference/research-log.md#r-052--state-space-sequence-models-s4-and-mamba)).

(c) For constant $x = 1$ from $h_0 = 0$, the recursion $h_{k+1} = \bar{a}h_k + \bar{b}$ gives $h_k = \bar{b}(1 - \bar{a}^k)/(1 - \bar{a}) = 1 - e^{-kh/\tau}$, since $\bar{b} = 1 - \bar{a}$. The continuous step response is $1 - e^{-t/\tau}$, so the two agree exactly at $t = kh$ ✓. That is what the zero-order hold guarantees.

---

## Answer key

### Solution 02-09.16

(a) Near the origin $\tanh(2x) \approx 2x$, so $\mathbf{J} = \frac{1}{\tau}\begin{bmatrix} -1 & -2 \\ -2 & -1\end{bmatrix}$, with trace $-2/\tau$ and determinant $-3/\tau^2 < 0$: a **saddle**. The eigenvalues are $(-1 - 2)/\tau = -3/\tau$ along $(1, 1)$, a decay time constant of \$\tau/3 = \$ **6.667 ps**, and $(2 - 1)/\tau = +1/\tau$ along $(1, -1)$, a growth time constant of \$\tau/(a - 1) = \$ **20 ps**.

(b) The imbalance grows as $\delta_0e^{t/20\text{ ps}}$. Reaching 0.5 by 200 ps needs \$\delta_0 \ge 0.5e^{-200/20} = 0.5e^{-10} = \$ **2.270×10⁻⁵**.

(c) The required initial imbalance shrinks *exponentially* with the allowed time: at 400 ps it is $0.5e^{-20}$, about $2\times10^4$ times smaller. If the imbalance at the sampling instant is spread roughly uniformly near zero (it is set by when the data edge lands relative to the clock), the probability of failing to resolve is proportional to that threshold, so each extra $\tau/(a - 1)$ of time divides the failure rate by $e$. That is why synchronizer reliability is quoted as a mean time between failures that grows exponentially with the settling time allowed.

### Solution 02-09.17

(a) $\mathbf{A}$ is lower triangular with eigenvalues −1 and −2. From $\mathbf{x}(0) = (1, 0)$: $x_1 = e^{-t}$ and $x_2' = -2x_2 + e^{-t}$, so $x_2 = e^{-t} - e^{-2t}$. From $\mathbf{x}(0) = (0, 1)$: $x_1 = 0$, $x_2 = e^{-2t}$. So

$$
e^{\mathbf{A}t} = \begin{bmatrix} e^{-t} & 0 \\ e^{-t} - e^{-2t} & e^{-2t}\end{bmatrix} .
$$

(b) $e^{\mathbf{A}(t - \lambda)}\mathbf{B}$ is the first column at $t - \lambda$. Using $\int_0^t\lambda e^{-a(t - \lambda)}d\lambda = \dfrac{t}{a} - \dfrac{1}{a^2} + \dfrac{e^{-at}}{a^2}$ (integration by parts):

$$
x_1 = t - 1 + e^{-t}, \qquad x_2 = (t - 1 + e^{-t}) - \left(\frac{t}{2} - \frac14 + \frac{e^{-2t}}{4}\right) = \frac{t}{2} - \frac34 + e^{-t} - \frac{e^{-2t}}{4} .
$$

At $t = 1$: \$x_1 = e^{-1} = \$ **0.3679** and \$x_2 = 0.5 - 0.75 + 0.3679 - 0.0338 = \$ **0.08405**.

(c) $x_1' + x_1 = t$ has particular solution $t - 1$ and, from $x_1(0) = 0$, homogeneous part $e^{-t}$: the same $x_1$ ✓. And $x_2(0) = -\tfrac34 + 1 - \tfrac14 = 0$ ✓.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 02-09.1a | trace | −1×10^4 | 1/s |
| 02-09.1b | determinant | 1×10^9 | 1/s² |
| 02-09.1d | undamped natural frequency | 31623 | rad/s |
| 02-09.1c | imaginary part of the eigenvalues | 31225 | 1/s |
| 02-09.2a | trace | −6 | — |
| 02-09.2b | determinant | −6 | — |
| 02-09.3a | det e^A | 148.4 | — |
| 02-09.5a | x1(1) | 10.23 | — |
| 02-09.5b | x2(1) | 9.859 | — |
| 02-09.6a | x1(0.5) | 0.3277 | — |
| 02-09.6b | x2(0.5) | 0.2552 | — |
| 02-09.7a | time of the x1 peak | 0.5 | — |
| 02-09.7b | x1 peak | 0.1839 | — |
| 02-09.8a | (1, 1) entry of e^A | 0.6004 | — |
| 02-09.8b | (1, 2) entry of e^A | 0.2325 | — |
| 02-09.9a | steady v1 | 0.6667 | V |
| 02-09.9b | steady v2 | 0.3333 | V |
| 02-09.9c | v2 at t = τ | 0.1577 | V |
| 02-09.10a | gain magnitude at ωτ = 1 | 0.2236 | — |
| 02-09.11a | stability threshold for k | 2 | — |
| 02-09.12a | exact a_d | 0.7788 | — |
| 02-09.12b | exact b_d | 0.2212 | — |
| 02-09.12c | Euler a_d | 0.75 | — |
| 02-09.12d | largest stable Euler step | 4 | ms |
| 02-09.13a | higher mode frequency | 5.033 | MHz |
| 02-09.13b | lower mode frequency | 4.594 | MHz |
| 02-09.14a | steady-state thermal resistance | 2.0 | K/W |
| 02-09.14b | Zth at 10 ms | 0.2971 | K/W |
| 02-09.14c | rise for 50 W, 10 ms | 14.86 | K |
| 02-09.14d | 10 ms pulse power for a 100 K rise | 336.6 | W |
| 02-09.15a | sampled a | 0.9802 | — |
| 02-09.15b | sampled b | 0.01980 | — |
| 02-09.15c | steps to 1% | 230.3 | — |
| 02-09.10b | DC gain | 0.3333 | — |
| 02-09.16a | growth time constant | 20 | ps |
| 02-09.16b | decay time constant | 6.667 | ps |
| 02-09.16c | smallest imbalance resolved in 200 ps | 2.270×10^-5 | — |
| 02-09.17a | x1(1) | 0.3679 | — |
| 02-09.17b | x2(1) | 0.08405 | — |
