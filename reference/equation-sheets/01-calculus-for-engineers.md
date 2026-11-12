# Equation Sheet · 01 Calculus for Engineers

The relations to know cold from Course 01, each with its conditions and where it is derived. The FE Reference Handbook lists many of these, but knowing where each comes from is what lets you use it correctly.

## Functions, logarithms and decibels

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $e^ae^b = e^{a+b}$; $\ln(ab) = \ln a + \ln b$; $\log_b x = \ln x/\ln b$ | Positive arguments for logarithms | [01-01](../../courses/01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md) |
| $x(t) = x_0e^{-t/\tau}$; time to fall to a fraction $p$ is $\tau\ln(1/p)$ | First-order decay: 63.2% of the change by $\tau$, 1% left after $4.6\tau$ | [01-01](../../courses/01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md) |
| $\text{dB} = 10\log_{10}(P_2/P_1) = 20\log_{10}(V_2/V_1)$ | The 20 form assumes equal impedances; gains in dB add along a chain | [01-01](../../courses/01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md) |
| dBm $= 10\log_{10}(P/1\text{ mW})$; 3 dB ≈ 2× and 10 dB = 10× in power | dBm is an absolute power; dB is a ratio | [01-01](../../courses/01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md) |
| $\omega = 2\pi f$; $\theta_{rad} = \theta_{deg}\,\pi/180$ | Arguments of sin, cos and exp must be dimensionless (radians) | [01-01](../../courses/01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md) |

## Limits and continuity

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\lim_{x\to0}\sin x/x = 1$; $\lim_{x\to0}(e^x - 1)/x = 1$; $\lim_{x\to0}(1 - \cos x)/x^2 = 1/2$ | The standard limits (radians) | [01-02](../../courses/01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md) |
| $\lim_{n\to\infty}(1 + x/n)^n = e^x$ | Continuous compounding, the origin of $e$ | [01-02](../../courses/01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md) |
| Rational function as $x \to \infty$: ratio of the leading terms | Gives high- and low-frequency asymptotes of transfer functions | [01-02](../../courses/01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md) |
| Capacitor voltage and inductor current are continuous | Finite currents and voltages; sets initial conditions at a switching event | [01-02](../../courses/01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md) |
| Bisection: error after $n$ halvings $\le (b - a)/2^n$ | Continuous $f$ with a sign change on $[a, b]$ (intermediate value theorem) | [01-02](../../courses/01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md) |

## Derivatives

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $f'(x) = \lim_{h\to0}\big(f(x + h) - f(x)\big)/h$ | Slope of the tangent; instantaneous rate of change | [01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md) |
| $(fg)' = f'g + fg'$; $(f/g)' = (f'g - fg')/g^2$; $\big(f(g(x))\big)' = f'(g(x))\,g'(x)$ | Product, quotient and chain rules | [01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md) |
| $(x^n)' = nx^{n-1}$; $(e^{ax})' = ae^{ax}$; $(\ln x)' = 1/x$; $(\sin x)' = \cos x$; $(\cos x)' = -\sin x$ | Angles in radians | [01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md) |
| $i_C = C\,dv/dt$; $v_L = L\,di/dt$ | Passive sign convention | [01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md) |
| $r_d = dV/dI = V_T/I$; $g_m = dI/dV = I/V_T$ | Exponential diode or BJT law, $I \gg I_S$ | [01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md) |
| $f'(x) \approx \big(f(x + h) - f(x - h)\big)/(2h)$, error $\propto h^2$ | Central difference; too small an $h$ amplifies round-off | [01-03](../../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md) |

## Applications of derivatives

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Extremum where $f' = 0$: minimum if $f'' > 0$, maximum if $f'' < 0$ | Also check endpoints and points where $f'$ does not exist | [01-04](../../courses/01-calculus-for-engineers/chapters/01-04-applications-of-derivatives.md) |
| $R_L = R_s$ gives $P_{max} = V_s^2/(4R_s)$ | Maximum power transfer from a fixed source; efficiency is then only 50% | [01-04](../../courses/01-calculus-for-engineers/chapters/01-04-applications-of-derivatives.md) |
| $f(x_0 + \Delta x) \approx f(x_0) + f'(x_0)\,\Delta x$ | Linearization, the small-signal idea; the error is second order | [01-04](../../courses/01-calculus-for-engineers/chapters/01-04-applications-of-derivatives.md) |
| $x_{k+1} = x_k - g(x_k)/g'(x_k)$ | Newton's method; quadratic convergence near a simple root, can diverge from a poor start | [01-04](../../courses/01-calculus-for-engineers/chapters/01-04-applications-of-derivatives.md) |
| $\lim f/g = \lim f'/g'$ | L'Hôpital's rule, only for 0/0 or ∞/∞ forms | [01-04](../../courses/01-calculus-for-engineers/chapters/01-04-applications-of-derivatives.md) |

## Integrals

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\int_a^b f\,dx = F(b) - F(a)$ where $F' = f$ | Fundamental theorem of calculus | [01-05](../../courses/01-calculus-for-engineers/chapters/01-05-integrals.md) |
| $q = \int i\,dt$; $w = \int p\,dt$; $v_C(t) = v_C(0) + \frac{1}{C}\int_0^t i\,dt'$ | Accumulation | [01-05](../../courses/01-calculus-for-engineers/chapters/01-05-integrals.md) |
| $\bar f = \frac{1}{b - a}\int_a^b f\,dx$ | Average value; over one period it is the DC component | [01-05](../../courses/01-calculus-for-engineers/chapters/01-05-integrals.md) |
| $v_{out} = -\frac{1}{RC}\int v_{in}\,dt$ | Ideal inverting op-amp integrator | [01-05](../../courses/01-calculus-for-engineers/chapters/01-05-integrals.md) |

## Techniques of integration

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\int u\,dv = uv - \int v\,du$ | Integration by parts; choose a $u$ that simplifies when differentiated | [01-06](../../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md) |
| $\int_0^T\sin(m\omega t)\sin(n\omega t)\,dt = 0$ for $m \ne n$, $T/2$ for $m = n \ge 1$ | Orthogonality over one period $T = 2\pi/\omega$; the basis of Fourier series | [01-06](../../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md) |
| $\int_0^\infty e^{-t/\tau}dt = \tau$; $\int_0^\infty te^{-t/\tau}dt = \tau^2$ | Improper integrals of decaying exponentials | [01-06](../../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md) |
| Trapezoid error $\propto h^2$; Simpson error $\propto h^4$ | Smooth integrands; check convergence by halving $h$ | [01-06](../../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md) |

## Applications of integration

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $V_{rms} = \sqrt{\frac{1}{T}\int_0^Tv^2\,dt}$ | Heating value: average power into $R$ is $V_{rms}^2/R$ | [01-07](../../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md) |
| Sine $V_p/\sqrt2$; square (±$V_p$) $V_p$; triangle $V_p/\sqrt3$; half-wave sine $V_p/2$ | RMS of standard waveforms | [01-07](../../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md) |
| $P = \tfrac12V_pI_p\cos\varphi = V_{rms}I_{rms}\cos\varphi$ | Sinusoidal steady state; $\varphi$ is the voltage–current phase angle | [01-07](../../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md) |
| $W_C = \tfrac12CV^2$; $W_L = \tfrac12LI^2$ | Stored energy | [01-07](../../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md) |
| $\int f\,dx = 1$; $\mu = \int xf\,dx$; $\sigma^2 = \int(x - \mu)^2f\,dx$ | Probability density $f$ | [01-07](../../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md) |
| $e_{rms} = \Delta/\sqrt{12}$; SNR $= 6.02N + 1.76$ dB | Uniform quantization error; full-scale sine into an ideal $N$-bit ADC | [01-07](../../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md) |

## Series and Taylor expansions

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\sum_{n=0}^\infty r^n = 1/(1 - r)$ | Geometric series, valid for $-1 < r < 1$ | [01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) |
| $f(x) = \sum_n f^{(n)}(a)(x - a)^n/n!$ | Taylor series, inside its radius of convergence | [01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) |
| $e^x = \sum x^n/n!$; $\sin x = x - x^3/3! + \cdots$; $\cos x = 1 - x^2/2! + \cdots$; $\ln(1 + x) = x - x^2/2 + x^3/3 - \cdots$ | Maclaurin series; the last needs $-1 < x \le 1$ | [01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) |
| $R_n = f^{(n+1)}(\xi)\,(x - a)^{n+1}/(n + 1)!$ | Lagrange remainder, with $\xi$ between $a$ and $x$ | [01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) |
| $(1 + x)^n \approx 1 + nx$; $\sqrt{1 + x} \approx 1 + x/2$; $1/(1 + x) \approx 1 - x$ | Small $x$; the error is about the first neglected term | [01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) |
| $G = A/(1 + A\beta) \approx (1/\beta)\big(1 - 1/(A\beta)\big)$ | Feedback gain error ≈ 1/loop gain | [01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) |
| HD2 $\approx \dfrac{a_2}{2a_1}A$; HD3 $\approx \dfrac{a_3}{4a_1}A^2$ | Weak nonlinearity $y = a_1x + a_2x^2 + a_3x^3$, input $A\cos\omega t$ | [01-08](../../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) |

## Multivariable calculus I

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $df = \frac{\partial f}{\partial x}dx + \frac{\partial f}{\partial y}dy$ | Total differential; linear sensitivity | [01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md) |
| $\frac{\Delta f}{f} \approx \sum_i \frac{\partial\ln f}{\partial\ln x_i}\frac{\Delta x_i}{x_i}$ | Relative sensitivity; worst case adds magnitudes, RSS adds squares (independent errors) | [01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md) |
| $\nabla f = (f_x, f_y, f_z)$; $D_{\mathbf{u}}f = \nabla f\cdot\mathbf{u}$ | The gradient points uphill and is normal to level sets | [01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md) |
| $\frac{d}{dt}f\big(x(t), y(t)\big) = f_x\,\dot x + f_y\,\dot y$ | Multivariable chain rule | [01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md) |
| $D = f_{xx}f_{yy} - f_{xy}^2$ | Second-derivative test: minimum if $D > 0$ and $f_{xx} > 0$; maximum if $D > 0$ and $f_{xx} < 0$; saddle if $D < 0$ | [01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md) |
| $\nabla f = \lambda\nabla g$ on $g = c$; $\lambda = df^*/dc$ | Lagrange multiplier; $\lambda$ is the shadow price of the constraint | [01-09](../../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md) |

## Multivariable calculus II

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $dA = r\,dr\,d\theta$; $dV = r\,dr\,d\theta\,dz$; $dV = \rho^2\sin\phi\,d\rho\,d\phi\,d\theta$ | Polar, cylindrical and spherical area and volume elements (Jacobians) | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
| $\int_{-\infty}^{\infty}e^{-x^2}dx = \sqrt\pi$ | Evaluated by squaring and switching to polar coordinates | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
| $W = \int_C\mathbf{F}\cdot d\mathbf{r}$; $V_a - V_b = -\int_b^a\mathbf{E}\cdot d\mathbf{l}$ | Line integral; path-independent if $\mathbf{F} = \nabla\varphi$ | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
| $\Phi = \iint_S\mathbf{F}\cdot d\mathbf{A}$ | Flux through a surface | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
| $\nabla\cdot\mathbf{F} = \partial_xF_x + \partial_yF_y + \partial_zF_z$; $(\nabla\times\mathbf{F})_z = \partial_xF_y - \partial_yF_x$ | Divergence (source density) and curl (circulation density) | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
| $\oint_S\mathbf{F}\cdot d\mathbf{A} = \iiint_V\nabla\cdot\mathbf{F}\,dV$; $\oint_C\mathbf{F}\cdot d\mathbf{r} = \iint_S(\nabla\times\mathbf{F})\cdot d\mathbf{A}$ | Divergence and Stokes' theorems; Green's theorem is the planar case | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
| $\oint_S\mathbf{E}\cdot d\mathbf{A} = Q_{enc}/\varepsilon_0$; $\oint_C\mathbf{B}\cdot d\mathbf{l} = \mu_0I_{enc}$ | Gauss's and Ampère's laws (static fields, vacuum) | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
| Sphere $E = Q/(4\pi\varepsilon_0r^2)$; wire $B = \mu_0I/(2\pi r)$; coax $C' = 2\pi\varepsilon/\ln(b/a)$ | Symmetric fields from the integral laws | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
| Dies per wafer $\approx \pi d^2/(4A) - \pi d/\sqrt{2A}$; Poisson yield $Y = e^{-AD_0}$ | Gross dies on a wafer of diameter $d$, then good dies | [01-10](../../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md) |
