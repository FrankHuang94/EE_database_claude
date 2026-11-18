# Equation Sheet · 02 Complex Numbers, Differential Equations and Linear Algebra

The relations to know cold from Course 02, each with its conditions and where it is derived. The FE Reference Handbook lists many of these, but knowing where each comes from is what lets you use it correctly.

## Complex numbers and phasors

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $z = x + jy = r\angle\theta = re^{j\theta}$; $r = \sqrt{x^2 + y^2}$, $\theta = \operatorname{atan2}(y, x)$ | Check the quadrant; never plain $\arctan(y/x)$ | [02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| $e^{j\theta} = \cos\theta + j\sin\theta$; $\cos\theta = \tfrac12(e^{j\theta} + e^{-j\theta})$, $\sin\theta = \tfrac{1}{2j}(e^{j\theta} - e^{-j\theta})$ | Euler's formula, from the Taylor series | [02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| $z_1z_2 = r_1r_2\angle(\theta_1 + \theta_2)$; $z_1/z_2 = (r_1/r_2)\angle(\theta_1 - \theta_2)$; $zz^* = \lvert z\rvert^2$ | Multiply and divide in polar form; divide in rectangular form with the conjugate | [02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| $z^n = r^n\angle n\theta$; $n$th roots: $r^{1/n}\angle\big((\theta + 2\pi k)/n\big)$, $k = 0, \dots, n - 1$ | De Moivre; the roots are equally spaced on a circle | [02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| $V_m\cos(\omega t + \phi) \leftrightarrow \mathbf{V} = V_m\angle\phi$; $v(t) = \operatorname{Re}\{\mathbf{V}e^{j\omega t}\}$ | Peak-amplitude phasor, cosine reference; one frequency only | [02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| $d/dt \leftrightarrow j\omega$; $\int dt \leftrightarrow 1/(j\omega)$ | Sinusoidal steady state of a linear system | [02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| $Z_R = R$, $Z_L = j\omega L$, $Z_C = 1/(j\omega C)$ | Impedances combine like resistances | [02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| $P = \tfrac12\operatorname{Re}\{\mathbf{V}\mathbf{I}^*\} = \tfrac12V_mI_m\cos(\theta_v - \theta_i)$ | Average power with peak phasors; $V_{rms} = V_m/\sqrt2$ | [02-01](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |

## First-order ODEs

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\tau y' + y = K$: $y(t) = K + (y(0) - K)e^{-t/\tau}$ | Step response; 63.2% of the change at $\tau$, 99.3% at $5\tau$ | [02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) |
| $t_{50\%} = \tau\ln2$; $t_{10\text{–}90} = \tau\ln9 = 2.197\tau$ | First-order timing | [02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) |
| $y' + p(t)y = q(t)$: $\mu = e^{\int p\,dt}$, $(\mu y)' = \mu q$ | Integrating factor; any linear first-order equation | [02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) |
| $y' = f(y)$: equilibria $f(y^*) = 0$; stable if $f'(y^*) < 0$, local $\tau = 1/\lvert f'(y^*)\rvert$ | Phase line; no need to solve | [02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) |
| Ramp $kt$ into $\tau y' + y = kt$: $y = k(t - \tau) + k\tau e^{-t/\tau}$ | From rest; lags by $\tau$ in time and $k\tau$ in value | [02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) |
| Forward Euler on $y' = -y/\tau$: stable for $h < 2\tau$, non-alternating for $h \le \tau$ | Backward Euler: stable for any $h$ | [02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) |
| Logistic $y' = ry(1 - y/N)$: 10% → 90% in $2\ln9/r$ | Separable; independent of the starting level | [02-02](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) |

## Second-order ODEs

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $y'' + 2\alpha y' + \omega_0^2y = 0$; $\zeta = \alpha/\omega_0$; $Q = 1/(2\zeta)$ | Standard form; roots $-\alpha \pm \sqrt{\alpha^2 - \omega_0^2}$ | [02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md) |
| Series RLC: $\alpha = R/(2L)$, $\omega_0 = 1/\sqrt{LC}$, $Q = \omega_0L/R$; parallel: $\alpha = 1/(2RC)$, $Q = \omega_0RC$ | Critical series resistance $2\sqrt{L/C}$ | [02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md) |
| ζ > 1: $c_1e^{s_1t} + c_2e^{s_2t}$; ζ = 1: $(c_1 + c_2t)e^{-\alpha t}$; ζ < 1: $e^{-\alpha t}(A\cos\omega_dt + B\sin\omega_dt)$ | $\omega_d = \omega_0\sqrt{1 - \zeta^2}$ | [02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md) |
| Unit step from rest, ζ < 1: $1 - e^{-\alpha t}\big[\cos\omega_dt + (\alpha/\omega_d)\sin\omega_dt\big]$ | Output of $y'' + 2\alpha y' + \omega_0^2y = \omega_0^2u(t)$ | [02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md) |
| $\text{OS} = e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$; $\zeta = -\ln\text{OS}/\sqrt{\pi^2 + \ln^2\text{OS}}$; $t_p = \pi/\omega_d$ | Overshoot depends on ζ only | [02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md) |
| 2% settling $\approx 4/(\zeta\omega_0) = 4/\alpha$ | Envelope rule; fastest ±2% settling near ζ = 0.78 | [02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md) |
| Ring-down: amplitude falls by $e$ in $Q/\pi$ cycles | Energy loses about $2\pi/Q$ per cycle | [02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md) |
| $W = y_1y_2' - y_2y_1' \ne 0$ | Wronskian test for independent solutions | [02-03](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md) |

## Forced response and resonance

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $y = y_h + y_p$; input $e^{st}$: $y_p = e^{st}/p(s)$ if $p(s) \ne 0$ | Exponential response formula; if $p(s) = 0$, multiply the guess by $t$ | [02-04](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md) |
| $p(D)y = \cos\omega t$: $y_{ss} = \operatorname{Re}\{e^{j\omega t}/p(j\omega)\}$ | Amplitude $1/\lvert p(j\omega)\rvert$, phase $-\arg p(j\omega)$ | [02-04](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md) |
| $H(j\omega) = \dfrac{\omega_0^2}{\omega_0^2 - \omega^2 + j2\zeta\omega_0\omega}$; $\lvert H(j\omega_0)\rvert = Q$, phase −90° | Second-order low-pass | [02-04](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md) |
| Peak at $\omega_0\sqrt{1 - 2\zeta^2}$, height $1/(2\zeta\sqrt{1 - \zeta^2})$ | Only for ζ < 0.707 (Butterworth: ζ = 0.707, −3.01 dB at $\omega_0$) | [02-04](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md) |
| Band-pass half-power bandwidth $\omega_0/Q$; $\omega_1\omega_2 = \omega_0^2$ | Exact for the second-order band-pass | [02-04](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md) |
| $y'' + \omega_0^2y = \cos\omega_0t$ from rest: $y = \dfrac{t}{2\omega_0}\sin\omega_0t$ | Undamped resonance: linear growth | [02-04](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md) |
| $\cos\omega_1t - \cos\omega_2t = -2\sin\frac{(\omega_1 + \omega_2)t}{2}\sin\frac{(\omega_1 - \omega_2)t}{2}$ | Beats; envelope period $2\pi/\lvert\omega_1 - \omega_2\rvert$ | [02-04](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md) |
| Build-up time constant $2Q/\omega_0$ | High $Q$: narrow band and slow settling | [02-04](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md) |

## The Laplace transform

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $F(s) = \int_{0^-}^\infty f(t)e^{-st}\,dt$ | Converges to the right of the abscissa of convergence | [02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md) |
| $1 \leftrightarrow 1/s$; $\delta(t) \leftrightarrow 1$; $e^{at} \leftrightarrow 1/(s - a)$; $te^{at} \leftrightarrow 1/(s - a)^2$ | Basic pairs | [02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md) |
| $\cos\omega t \leftrightarrow s/(s^2 + \omega^2)$; $\sin\omega t \leftrightarrow \omega/(s^2 + \omega^2)$ | Damped versions: replace $s$ by $s + \alpha$ | [02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md) |
| $f' \leftrightarrow sF - f(0^-)$; $f'' \leftrightarrow s^2F - sf(0^-) - f'(0^-)$; $\int_0^tf \leftrightarrow F/s$ | Initial conditions enter automatically | [02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md) |
| $f(t - a)u(t - a) \leftrightarrow e^{-as}F(s)$; $e^{at}f(t) \leftrightarrow F(s - a)$; $tf(t) \leftrightarrow -F'(s)$ | Time shift, $s$-shift, multiplication by $t$ | [02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md) |
| $(f * g)(t) \leftrightarrow F(s)G(s)$; $Y(s) = H(s)X(s)$ | Convolution theorem; zero initial conditions for $H$ | [02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md) |
| Residue at a simple pole: $[(s - p)F(s)]_{s = p}$ | Cover-up rule for partial fractions | [02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md) |
| $f(0^+) = \lim_{s\to\infty}sF(s)$; $f(\infty) = \lim_{s\to0}sF(s)$ | FVT only if all poles of $sF$ are in the open left half-plane | [02-05](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md) |

## Vectors, matrices and linear systems

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\mathbf{a}\cdot\mathbf{b} = \sum a_ib_i = \lVert\mathbf{a}\rVert\lVert\mathbf{b}\rVert\cos\theta$; $\lVert\mathbf{a}\rVert = \sqrt{\mathbf{a}\cdot\mathbf{a}}$ | Cauchy–Schwarz: $\lvert\mathbf{a}\cdot\mathbf{b}\rvert \le \lVert\mathbf{a}\rVert\lVert\mathbf{b}\rVert$ | [02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md) |
| $\mathbf{p} = \dfrac{\mathbf{a}\cdot\mathbf{b}}{\mathbf{a}\cdot\mathbf{a}}\mathbf{a}$ | Projection of $\mathbf{b}$ onto $\mathbf{a}$; residual orthogonal to $\mathbf{a}$ | [02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md) |
| $(\mathbf{A}\mathbf{B})^{\mathsf{T}} = \mathbf{B}^{\mathsf{T}}\mathbf{A}^{\mathsf{T}}$; $\mathbf{A}\mathbf{B} \ne \mathbf{B}\mathbf{A}$ in general | Product costs $2mnp$ flops | [02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md) |
| $\mathbf{P}\mathbf{A} = \mathbf{L}\mathbf{U}$: $\mathbf{L}\mathbf{y} = \mathbf{P}\mathbf{b}$, then $\mathbf{U}\mathbf{x} = \mathbf{y}$ | Factor $\approx\tfrac23n^3$ flops; each solve $\approx 2n^2$ | [02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md) |
| Stamp $g$ between $j$, $k$: $+g$ at $(j,j)$, $(k,k)$; $-g$ at $(j,k)$, $(k,j)$ | Nodal analysis $\mathbf{G}\mathbf{v} = \mathbf{i}$; to ground, only the diagonal | [02-06](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md) |

## Determinants, inverses and vector spaces

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\det\mathbf{A} = \pm\prod(\text{pivots})$; $\det(\mathbf{A}\mathbf{B}) = \det\mathbf{A}\det\mathbf{B}$; $\det(c\mathbf{A}) = c^n\det\mathbf{A}$ | Sign flips with each row exchange; $\det = 0$ ⇔ singular | [02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md) |
| $\begin{bmatrix}a & b\\ c & d\end{bmatrix}^{-1} = \dfrac{1}{ad - bc}\begin{bmatrix}d & -b\\ -c & a\end{bmatrix}$; $(\mathbf{A}\mathbf{B})^{-1} = \mathbf{B}^{-1}\mathbf{A}^{-1}$ | Never invert to solve a large system | [02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md) |
| Cramer: $x_i = \det\mathbf{A}_i/\det\mathbf{A}$ | $\mathbf{A}_i$: column $i$ replaced by $\mathbf{b}$; small systems only | [02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md) |
| $\operatorname{rank} + \dim N(\mathbf{A}) = n$ | Rank–nullity ($n$ = number of columns) | [02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md) |
| $\mathbf{x} = \mathbf{x}_p + \mathbf{x}_n$ | Solvable iff $\mathbf{b}$ is in the column space | [02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md) |
| $\mathbf{A}^{\mathsf{T}}\mathbf{A}\hat{\mathbf{x}} = \mathbf{A}^{\mathsf{T}}\mathbf{b}$; $\mathbf{P} = \mathbf{A}(\mathbf{A}^{\mathsf{T}}\mathbf{A})^{-1}\mathbf{A}^{\mathsf{T}}$ | Least squares; residual orthogonal to the column space | [02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md) |
| $\mathbf{G} = \mathbf{A}^{\mathsf{T}}\operatorname{diag}(g)\mathbf{A}$; $\mathbf{R} = \mathbf{G}^{-1}$ symmetric | Incidence matrix; driving-point and transfer resistances; reciprocity | [02-07](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md) |

## Eigenvalues and eigenvectors

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\det(\mathbf{A} - \lambda\mathbf{I}) = 0$; 2×2: $\lambda^2 - (\operatorname{tr}\mathbf{A})\lambda + \det\mathbf{A} = 0$ | $\sum\lambda_i = \operatorname{tr}\mathbf{A}$, $\prod\lambda_i = \det\mathbf{A}$ | [02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |
| $\mathbf{A} = \mathbf{X}\boldsymbol{\Lambda}\mathbf{X}^{-1}$; $\mathbf{A}^k = \mathbf{X}\boldsymbol{\Lambda}^k\mathbf{X}^{-1}$ | Needs $n$ independent eigenvectors | [02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |
| $\mathbf{A}^k$, $\mathbf{A}^{-1}$, $\mathbf{A} + c\mathbf{I}$ have eigenvalues $\lambda^k$, $1/\lambda$, $\lambda + c$ | Same eigenvectors | [02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |
| $\mathbf{x}_{k+1} = \mathbf{A}\mathbf{x}_k$ stable iff all $\lvert\lambda_i\rvert < 1$ | Markov: steady state at $\lambda = 1$; error $\propto \lvert\lambda_2\rvert^k$ | [02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |
| $\mathbf{S} = \mathbf{S}^{\mathsf{T}} \Rightarrow \mathbf{S} = \mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^{\mathsf{T}}$, $\mathbf{Q}^{\mathsf{T}}\mathbf{Q} = \mathbf{I}$ | Spectral theorem: real eigenvalues, orthonormal eigenvectors | [02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |
| Positive definite: all $\lambda > 0$ ⇔ all pivots > 0 ⇔ $\mathbf{x}^{\mathsf{T}}\mathbf{S}\mathbf{x} > 0$ | Symmetric $\mathbf{S}$ | [02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |
| $\mathbf{A} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^{\mathsf{T}}$; $\sigma_i = \sqrt{\lambda_i(\mathbf{A}^{\mathsf{T}}\mathbf{A})}$; $\mathbf{u}_i = \mathbf{A}\mathbf{v}_i/\sigma_i$ | $\prod\sigma_i = \lvert\det\mathbf{A}\rvert$, $\sum\sigma_i^2 = \lVert\mathbf{A}\rVert_F^2$ | [02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |
| $\kappa = \sigma_1/\sigma_n$; best rank-$k$ error $= \sigma_{k+1}$ (2-norm) | Eckart–Young; MIMO channel gains $\sigma_i^2$ | [02-08](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md) |

## Systems of ODEs and the matrix exponential

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\mathbf{x}' = \mathbf{A}\mathbf{x} + \mathbf{B}u$, $y = \mathbf{C}\mathbf{x} + Du$ | States: capacitor voltages and inductor currents | [02-09](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |
| $\mathbf{x}(t) = e^{\mathbf{A}t}\mathbf{x}_0 = \sum c_ie^{\lambda_it}\mathbf{v}_i$ | Modes; fit $c_i$ to $\mathbf{x}_0$ | [02-09](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |
| $e^{\mathbf{A}t} = \sum_k(\mathbf{A}t)^k/k! = \mathbf{X}e^{\boldsymbol{\Lambda}t}\mathbf{X}^{-1}$; $\mathcal{L}\{e^{\mathbf{A}t}\} = (s\mathbf{I} - \mathbf{A})^{-1}$ | $\det e^{\mathbf{A}t} = e^{\operatorname{tr}(\mathbf{A})t}$ | [02-09](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |
| $\mathbf{x}(t) = e^{\mathbf{A}t}\mathbf{x}_0 + \int_0^te^{\mathbf{A}(t - \tau)}\mathbf{B}u(\tau)\,d\tau$ | Forced response | [02-09](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |
| $H(s) = \mathbf{C}(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B} + D$; DC gain $-\mathbf{C}\mathbf{A}^{-1}\mathbf{B} + D$ | Poles = eigenvalues of $\mathbf{A}$ | [02-09](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |
| 2-state: stable iff $\operatorname{tr}\mathbf{A} < 0$ and $\det\mathbf{A} > 0$; with $\det > 0$: node if $\operatorname{tr}^2 \ge 4\det$, spiral if $\operatorname{tr}^2 < 4\det$ and $\operatorname{tr} \ne 0$ | $\det < 0$: saddle; $\operatorname{tr} = 0$, $\det > 0$: center | [02-09](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |
| $\mathbf{A}_d = e^{\mathbf{A}T}$, $\mathbf{B}_d = \int_0^Te^{\mathbf{A}\sigma}d\sigma\,\mathbf{B} = \mathbf{A}^{-1}(e^{\mathbf{A}T} - \mathbf{I})\mathbf{B}$; $z = e^{sT}$ | Exact zero-order-hold discretization; the last form needs $\mathbf{A}$ invertible | [02-09](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |
| Forward Euler: real mode stable for $T < 2/\lvert\lambda\rvert$ | The fastest mode sets the limit | [02-09](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md) |

## Numerical methods

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\epsilon = 2^{-52} \approx 2.22\times10^{-16}$ (FP64), $2^{-23} \approx 1.19\times10^{-7}$ (FP32), $2^{-10} \approx 9.77\times10^{-4}$ (FP16); $u = \epsilon/2$ | $\operatorname{fl}(x\circ y) = (x\circ y)(1 + \delta)$, $\lvert\delta\rvert \le u$ | [02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md) |
| $1 - \cos x = 2\sin^2(x/2)$; small root $= 2c/(-b - \sqrt{b^2 - 4ac})$ | Rewrites that avoid cancellation ($b > 0$) | [02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md) |
| Bisection: $n \ge \log_2\big((b - a)/\text{tol}\big)$ | 1 bit per step; 3.32 steps per digit | [02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md) |
| Newton: $x_{k+1} = x_k - f(x_k)/f'(x_k)$; $e_{k+1} \approx \dfrac{f''}{2f'}e_k^2$ | Simple root, good start; linear at a multiple root | [02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md) |
| Forward Euler $R = 1 + h\lambda$; backward Euler $1/(1 - h\lambda)$; trapezoidal $\dfrac{1 + h\lambda/2}{1 - h\lambda/2}$ | Stable where $\lvert R\rvert \le 1$; the implicit two are A-stable | [02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md) |
| Global error $\propto h^p$: Euler $p = 1$, Heun 2, RK4 4 | Halving $h$ divides the error by $2^p$ | [02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md) |
| $\dfrac{\lVert\delta\mathbf{x}\rVert}{\lVert\mathbf{x}\rVert} \le \kappa(\mathbf{A})\dfrac{\lVert\delta\mathbf{b}\rVert}{\lVert\mathbf{b}\rVert}$ | Lose up to $\log_{10}\kappa$ digits; relative error of a solve $\approx \kappa u$ | [02-10](../../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md) |
